#!/usr/bin/env python3
"""Runs the book pipeline for one book, stage by stage.

  production/pipeline/.venv/bin/python production/pipeline/run_book.py <slug> [--stages a,b,c] [--youtube URL]

Stages (in this order; the default is everything up to and including "deliver"):
  check    the book folder has everything the next stages need, and aak-llm answers
  pdf      A5 reading PDF and A4 booklet                              (this Mac, Chrome)
  assets   pictures as PNG, and the images the video needs            (this Mac, Chrome)
  audio    multi-voice audiobook with Kokoro                          (aak-llm)
  video    1920x1080 video from the pictures and the real audio timing (aak-llm)
  package  subtitles, YouTube description with chapters, thumbnail    (this Mac)
  deliver  finished files to the main server's incoming folder, checksums verified
  upload   (only when asked) upload to YouTube as PRIVATE, into the podcast, from the main server
  publish  (only when asked, needs --youtube URL) add the book to the site and deploy it

The book folder is production/<slug>/ and holds book.json, translation_en.json, art/*.svg (with art/cover.svg),
<prefix>_voice_script.json and voices_kokoro.json. Every long step can be run again: finished work is reused."""
import argparse, glob, json, os, shlex, subprocess, sys, time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PIPE = os.path.join(ROOT, "production", "pipeline")
PY = os.path.join(PIPE, ".venv", "bin", "python")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
REMOTE, REMOTE_DIR = "aak-llm", "bibliotheque-production"          # the production machine, folder in its home
MAIN, MAIN_KEY, INBOX = "root@31.207.7.3", os.path.expanduser("~/.ssh/id_ed25519_bibliotheque_server"), "/srv/bibliotheque-incoming"
STAGES = ["check", "pdf", "assets", "audio", "video", "package", "deliver", "upload", "publish"]
DEFAULT = STAGES[:7]


def say(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def run(cmd, cwd=None, env=None, capture=False, check=True):
    r = subprocess.run(cmd, cwd=cwd, env=env, text=True, capture_output=capture)
    if check and r.returncode != 0:
        sys.exit(f"command failed ({r.returncode}): {' '.join(map(str, cmd))[:200]}\n{(r.stderr or '')[-600:]}")
    return r


def remote(cmd, timeout=40):
    """One command on aak-llm. Returns (ok, output). ssh -n so it never swallows our input."""
    try:
        r = subprocess.run(["ssh", "-n", "-o", "BatchMode=yes", "-o", "ConnectTimeout=25", REMOTE, cmd], text=True, capture_output=True, timeout=timeout)
        return r.returncode == 0, (r.stdout + r.stderr).strip()
    except subprocess.TimeoutExpired:
        return False, "ssh timed out"


def main_srv(cmd, stdin=None, timeout=300):
    r = subprocess.run(["ssh", "-i", MAIN_KEY, "-o", "IdentitiesOnly=yes", "-o", "BatchMode=yes", "-o", "ConnectTimeout=20", MAIN, cmd],
                       stdin=stdin, text=True, capture_output=True, timeout=timeout)
    return r.returncode == 0, (r.stdout + r.stderr).strip()


class Book:
    def __init__(self, slug):
        self.slug = slug
        self.dir = os.path.join(ROOT, "production", slug)
        p = os.path.join(self.dir, "book.json")
        if not os.path.exists(p):
            sys.exit(f"No book.json in {self.dir}. Make the book folder first (see .claude/commands/make-book.md).")
        self.b = json.load(open(p, encoding="utf-8"))
        self.prefix = self.b["prefix"]
        self.env = dict(os.environ, BOOK_DIR=self.dir)

    def f(self, name):
        return os.path.join(self.dir, name)

    def script(self, name, *args, cwd=None):
        say(f"running {name}")
        run([PY, "-W", "ignore", os.path.join(PIPE, name), *args], cwd=cwd or self.dir, env=self.env)


# ---------------------------------------------------------------------------------------------- stages
def st_check(k):
    need = ["book.json", "translation_en.json", f"{k.prefix}_voice_script.json", "voices_kokoro.json", "art/cover.svg"]
    need += [f"art/{a}.svg" for a in sorted(set(k.b["art"].values()))]
    missing = [n for n in need if not os.path.exists(k.f(n))]
    if missing:
        sys.exit("Missing in " + k.dir + ":\n  " + "\n  ".join(missing))
    ok, out = remote(f"echo up; test -d ~/{REMOTE_DIR}/models && echo models-ok")
    if not ok or "models-ok" not in out:
        sys.exit(f"aak-llm is not reachable or not ready ({out[:150]}). Nothing was changed; try again later.")
    ok, out = main_srv("test -d " + INBOX + " && echo inbox-ok")
    if not ok or "inbox-ok" not in out:
        sys.exit(f"the main server is not reachable or has no incoming folder ({out[:150]}).")
    say(f"check ok: {len(need)} files present, aak-llm and the main server answer")


def st_pdf(k):
    k.script("build_pdf.py")
    A5, A4 = k.f(f"{k.prefix}_A5_reading.pdf"), k.f(f"{k.prefix}_A4_booklet.pdf")
    run([PY, "-W", "ignore", os.path.join(PIPE, "make_booklet.py"), A5, A4])


def render_png(svg, png, w, h):
    html = os.path.join(os.path.dirname(png), "_wrap.html")
    open(html, "w").write(f'<style>html,body{{margin:0;background:#000}}img{{display:block;width:{w}px;height:{h}px}}</style><img src="file://{svg}">')
    run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1", "--virtual-time-budget=8000",
         f"--screenshot={png}", f"--window-size={w},{h}", f"file://{html}"], capture=True)
    os.remove(html)


def st_assets(k):
    os.makedirs(k.f("art/png"), exist_ok=True)
    for svg in sorted(glob.glob(k.f("art/*.svg"))):
        name = os.path.splitext(os.path.basename(svg))[0]
        png = k.f(f"art/png/{name}.png")
        if not os.path.exists(png) or os.path.getmtime(png) < os.path.getmtime(svg):
            say(f"drawing {name}.png")
            render_png(svg, png, *( (3000, 3000) if name.startswith("cover") else (1600, 900)))
    k.script("make_video_assets.py")


def wait_remote(label, pidfile, logfile, workdir, every=30, give_up_after_failures=4):
    fails = 0
    while True:
        time.sleep(every)
        ok, out = remote(f"cd ~/{REMOTE_DIR}/{workdir} && if kill -0 $(cat {pidfile}) 2>/dev/null; then echo RUNNING; else echo EXITED; fi; tail -c 300 {logfile} | tail -2")
        if not ok:
            fails += 1
            say(f"{label}: aak-llm did not answer ({fails}/{give_up_after_failures})")
            if fails >= give_up_after_failures:
                sys.exit(f"{label}: aak-llm stopped answering. The job keeps running there; run this stage again later, it will pick up where it is.")
            continue
        fails = 0
        if out.startswith("EXITED"):
            return out
        say(f"{label}: running ... {out.splitlines()[-1][:90] if out.splitlines() else ''}")


def sync_remote(k):
    d = f"~/{REMOTE_DIR}/{k.slug}"
    ok, out = remote(f"mkdir -p {d} ~/{REMOTE_DIR}/pipeline && cd {d} && ln -sfn ../models models && echo ok")
    if not ok:
        sys.exit("could not prepare aak-llm: " + out)
    run(["scp", "-q", *glob.glob(os.path.join(PIPE, "*.py")), f"{REMOTE}:{REMOTE_DIR}/pipeline/"])
    run(["scp", "-q", k.f("book.json"), k.f(f"{k.prefix}_voice_script.json"), k.f("voices_kokoro.json"), f"{REMOTE}:{REMOTE_DIR}/{k.slug}/"])


def st_audio(k):
    sync_remote(k)
    ok, out = remote(f"cd ~/{REMOTE_DIR}/{k.slug} && ls {k.prefix}_audiobook.mp3 {k.prefix}_audiobook_timing.json 2>/dev/null | wc -l")
    if ok and out.strip() == "2":
        say("audio already made on aak-llm, reusing it")
    else:
        say("starting the audio on aak-llm (Kokoro, about 3.5x real time)")
        ok, out = remote(f"cd ~/{REMOTE_DIR}/{k.slug} && (nohup nice -n 10 ../venv/bin/python ../pipeline/make_audio_kokoro.py > run_audio.log 2>&1 & echo $! > run_audio.pid) && echo started")
        if not ok:
            sys.exit("could not start the audio: " + out)
        wait_remote("audio", "run_audio.pid", "run_audio.log", k.slug)
    ok, out = remote(f"cd ~/{REMOTE_DIR}/{k.slug} && ls -la {k.prefix}_audiobook.mp3 && grep -E 'Done:|Speed this run' run_audio.log | tail -2")
    if not ok:
        sys.exit("the audio did not finish; see run_audio.log on aak-llm:\n" + out)
    say(out.splitlines()[-1][:120])
    run(["scp", "-q", f"{REMOTE}:{REMOTE_DIR}/{k.slug}/{k.prefix}_audiobook.mp3", f"{REMOTE}:{REMOTE_DIR}/{k.slug}/{k.prefix}_audiobook_timing.json", k.dir + "/"])


def st_video(k):
    d = f"{REMOTE_DIR}/{k.slug}"
    run(["scp", "-q", "-r", k.f("video_assets"), f"{REMOTE}:{d}/"])
    ok, out = remote(f"cd ~/{d} && test -s {k.prefix}_YouTube.mp4 && echo have")
    if ok and "have" in out:
        say("video already rendered on aak-llm, reusing it")
    else:
        say("rendering the video on aak-llm (about 5 to 10 minutes)")
        ok, out = remote(f"cd ~/{d} && rm -rf scenes video_only.mp4 && (nohup nice -n 5 ../venv/bin/python ../pipeline/make_video.py --workers 10 > run_video.log 2>&1 & echo $! > run_video.pid) && echo started")
        if not ok:
            sys.exit("could not start the video: " + out)
        wait_remote("video", "run_video.pid", "run_video.log", k.slug, every=45)
    ok, out = remote(f"cd ~/{d} && ffprobe -v error -show_entries format=duration -of csv=p=0 {k.prefix}_YouTube.mp4; ffprobe -v error -show_entries format=duration -of csv=p=0 {k.prefix}_audiobook.mp3; ffprobe -v error -select_streams v:0 -show_entries stream=width,height,nb_frames -of csv=p=0 {k.prefix}_YouTube.mp4")
    if not ok or len(out.splitlines()) < 3:
        sys.exit("the video is missing or unreadable:\n" + out)
    v, a, info = out.splitlines()[:3]
    say(f"video check: {info} | video {float(v):.2f} s, audio {float(a):.2f} s (difference {float(v) - float(a):+.2f} s)")
    if abs(float(v) - float(a)) > 0.5:
        sys.exit("the video and audio lengths differ by more than half a second; not continuing")


def st_package(k):
    k.script("make_package.py")


def sha(path):
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def st_deliver(k):
    dest = f"{INBOX}/{k.slug}"
    ok, out = main_srv(f"mkdir -p {dest} && chown deliver:deliver {dest}")
    if not ok:
        sys.exit("cannot prepare the incoming folder: " + out)
    local = [f"{k.prefix}_A5_reading.pdf", f"{k.prefix}_A4_booklet.pdf", f"{k.prefix}.srt", f"{k.prefix}_youtube_description.txt",
             f"{k.prefix}_thumbnail.png", f"{k.prefix}_voice_script.json", f"{k.prefix}_voice_script.md", "translation_en.json", "book.json"]
    local = [n for n in local if os.path.exists(k.f(n))]
    import shutil, tempfile
    stage = tempfile.mkdtemp()
    for n in local:
        shutil.copy(k.f(n), stage)
    shutil.copy(k.f("art/png/cover.png"), os.path.join(stage, f"{k.prefix}_cover_3000.png"))
    sums = {n: sha(os.path.join(stage, n)) for n in os.listdir(stage)}
    open(os.path.join(stage, "SHA256SUMS_mac"), "w").write("".join(f"{v}  {n}\n" for n, v in sums.items()))
    say(f"sending {len(sums)} files from this Mac")
    env = dict(os.environ, COPYFILE_DISABLE="1")
    tar = subprocess.Popen(["tar", "-C", stage, "-cf", "-", "."], stdout=subprocess.PIPE, env=env, stderr=subprocess.DEVNULL)
    ok, out = main_srv(f"tar -C {dest} -xf - 2>/dev/null; find {dest} -name '._*' -delete; cd {dest} && sha256sum -c SHA256SUMS_mac 2>&1 | grep -vc ': OK'; chown -R deliver:deliver {dest}", stdin=tar.stdout)
    if out.strip().splitlines()[-1:] != ["0"]:
        sys.exit("checksum mismatch after sending from the Mac:\n" + out)
    # the two big files go straight from aak-llm with the restricted delivery key
    say("aak-llm sends the video and the audio (restricted delivery key)")
    key = "~/.ssh/id_ed25519_bibliotheque_deliver"
    files = f"{k.prefix}_YouTube.mp4 {k.prefix}_audiobook.mp3 {k.prefix}_audiobook_timing.json"
    ok, out = remote(f"cd ~/{REMOTE_DIR}/{k.slug} && sha256sum {files} > /tmp/{k.slug}.sums && rsync -a --partial -e 'ssh -i {key} -o IdentitiesOnly=yes -o BatchMode=yes -o ConnectTimeout=20' {files} deliver@31.207.7.3:{k.slug}/ && cat /tmp/{k.slug}.sums", timeout=1500)
    if not ok:
        sys.exit("sending from aak-llm failed:\n" + out[-500:])
    sums_remote = out.strip() + "\n"
    ok, out = main_srv(f"cd {dest} && cat > /tmp/{k.slug}.check && sha256sum -c /tmp/{k.slug}.check 2>&1; rm -f /tmp/{k.slug}.check", stdin=subprocess.Popen(["printf", "%s", sums_remote], stdout=subprocess.PIPE).stdout)
    bad = [l for l in out.splitlines() if not l.endswith(": OK")]
    if bad:
        sys.exit("checksum mismatch on the main server:\n" + "\n".join(bad))
    say(f"delivered and verified in {dest}: {len(sums) + 3} files")


def st_upload(k):
    dest = f"{INBOX}/{k.slug}"
    pl = k.b.get("playlist", "")
    cmd = (f"bibliotheque-youtube-upload {dest}/{k.prefix}_YouTube.mp4 --package {dest}/{k.prefix}_youtube_description.txt "
           f"--thumbnail {dest}/{k.prefix}_thumbnail.png {('--playlist ' + pl) if pl else ''} --privacy private")
    say("uploading to YouTube from the main server (private) ...")
    ok, out = main_srv(cmd + f" 2>&1 | tee {dest}/UPLOADED", timeout=3600)
    print(out[-900:])
    if "Done." not in out:
        sys.exit("the upload did not report Done; see the output above")
    say("uploaded as PRIVATE. In YouTube Studio set it to Public or Unlisted, then run the publish stage with --youtube <link>.")


def st_publish(k, youtube):
    if not youtube:
        sys.exit("publish needs --youtube <the public YouTube link of the finished video>")
    run([PY, "-W", "ignore", os.path.join(PIPE, "publish_to_site.py"), k.slug, "--youtube", youtube], cwd=ROOT)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug")
    ap.add_argument("--stages", help="comma separated; default: " + ",".join(DEFAULT))
    ap.add_argument("--youtube")
    a = ap.parse_args()
    stages = a.stages.split(",") if a.stages else DEFAULT
    bad = [s for s in stages if s not in STAGES]
    if bad:
        sys.exit(f"unknown stage(s): {bad}. Stages: {STAGES}")
    k = Book(a.slug)
    t0 = time.time()
    for s in STAGES:
        if s in stages:
            t = time.time()
            say(f"=== {s}")
            (st_publish(k, a.youtube) if s == "publish" else globals()["st_" + s](k))
            open(k.f("timing.log"), "a").write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} stage {s} done in {time.time() - t:.0f} s\n")
    say(f"all requested stages done in {(time.time() - t0) / 60:.1f} minutes")


if __name__ == "__main__":
    main()
