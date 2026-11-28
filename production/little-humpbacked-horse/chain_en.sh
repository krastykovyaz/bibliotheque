#!/bin/bash
# Runs ON aak-llm for The Little Humpbacked Horse (English, 2 episodes): WAITS until no other book's chain, audio or video job is running, then makes the
# English audio (Kokoro), renders the video, cuts it into the episodes of book.json (pipeline/split_episodes.py), and sends both episodes to the main
# server's incoming folders (little-humpbacked-horse-ep1/-ep2, thumbnails already there). It does NOT drop READY: nothing is uploaded to YouTube until
# the user says so (then `touch READY` in each incoming folder on the main server, part 1 first).
#   nohup ./chain_en.sh > chain_en.log 2>&1 &
set -u
SLUG=little-humpbacked-horse; PREFIX=The_Little_Humpbacked_Horse
cd ~/bibliotheque-production/$SLUG || exit 1
export BOOK_DIR=$PWD
say() { echo "[$(date +%H:%M:%S)] $*"; }
fail() { say "STOPPED: $*"; echo "$*" > CHAIN_FAILED; exit 1; }
rm -f CHAIN_FAILED
say "waiting for the other books' chains and jobs to finish"
while pgrep -f 'chain_split_on_server.sh|chain_on_server.sh|chain_ru.sh|make_audio_kokoro.py|make_video.py' > /dev/null; do sleep 120; done
say "no other job is running; waiting for 20 GB of free disk if needed"
while [ "$(df --output=avail -BG ~ | tail -1 | tr -dc 0-9)" -lt 20 ]; do sleep 600; done   # needs about 20 GB free for the audio, video and episode cuts (the disk was full on 2026-11-28)
say "starting"
if ! { [ -s ${PREFIX}_audiobook.mp3 ] && [ -s ${PREFIX}_audiobook_timing.json ]; }; then
  nice -n 10 ../venv/bin/python ../pipeline/make_audio_kokoro.py > run_audio.log 2>&1
  [ -s ${PREFIX}_audiobook.mp3 ] && grep -q "Done:" run_audio.log || fail "audio failed (run_audio.log)"
fi
say "audio ready: $(ffprobe -v error -show_entries format=duration -of csv=p=0 ${PREFIX}_audiobook.mp3) s"
if [ ! -s ${PREFIX}_YouTube.mp4 ]; then
  rm -rf scenes video_only.mp4
  nice -n 5 ../venv/bin/python ../pipeline/make_video.py --workers 10 > run_video.log 2>&1
  [ -s ${PREFIX}_YouTube.mp4 ] || fail "the video was not made (run_video.log)"
fi
V=$(ffprobe -v error -show_entries format=duration -of csv=p=0 ${PREFIX}_YouTube.mp4)
A=$(ffprobe -v error -show_entries format=duration -of csv=p=0 ${PREFIX}_audiobook.mp3)
python3 -c "import sys; sys.exit(0 if abs($V-$A) < 0.5 else 1)" || fail "video $V s and audio $A s differ"
say "video ok: $V s"
../venv/bin/python ../pipeline/split_episodes.py > run_split.log 2>&1 || fail "split failed (run_split.log)"
cat run_split.log
KEY=~/.ssh/id_ed25519_bibliotheque_deliver
SSHO="ssh -i $KEY -o IdentitiesOnly=yes -o BatchMode=yes -o ConnectTimeout=20"
N=$(grep -c '^part ' run_split.log)
for i in $(seq 1 $N); do
  D=$SLUG-ep$i
  mkdir -p stage_ep$i && cp ${PREFIX}_EP$i.mp4 stage_ep$i/${PREFIX}_YouTube.mp4 && cp ${PREFIX}_EP${i}_youtube_description.txt stage_ep$i/${PREFIX}_youtube_description.txt
  SZ=$(du -m stage_ep$i/${PREFIX}_YouTube.mp4 | cut -f1)
  if [ "$SZ" -gt 1000 ] || [ $i -gt 1 ]; then say "part $i staged in stage_ep$i ($SZ MB), NOT sent: the main server has little free disk (1.6 GB on 2026-11-28); send it by hand when the previous part is uploaded and removed"; continue; fi
  say "sending part $i (no READY)"
  for t in 1 2 3 4 5; do rsync -a --partial -e "$SSHO" stage_ep$i/ deliver@31.207.7.3:$D/ && break; sleep 30; done
  DIFF=$(rsync -ac --dry-run -i -e "$SSHO" stage_ep$i/ deliver@31.207.7.3:$D/ | grep -c '^[<>]')
  [ "$DIFF" = "0" ] || fail "the copy of part $i differs ($DIFF files)"
  say "part $i delivered and verified"
done
say "done: part 1 (if it fit) is in the main server's incoming folder without READY, the rest is staged here; nothing uploaded"
