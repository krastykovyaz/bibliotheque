#!/bin/bash
# Runs ON aak-llm, no Mac needed: waits for the audio, renders the video, makes subtitles and description,
# sends the video + description to the main server's incoming folder (restricted delivery key), verifies the
# copy with checksums, and then drops the READY marker. The main server uploads (private, into the playlist)
# and removes the files by itself.
#   nohup ./chain_on_server.sh <slug> <Prefix> > chain.log 2>&1 &
set -u
SLUG=$1; PREFIX=$2
cd ~/bibliotheque-production/$SLUG || exit 1
export BOOK_DIR=$PWD
say() { echo "[$(date +%H:%M:%S)] $*"; }
fail() { say "STOPPED: $*"; echo "$*" > CHAIN_FAILED; exit 1; }
rm -f CHAIN_FAILED
say "waiting for the audio"
while ( for p in $(pgrep -f make_audio_kokoro); do [ "$(readlink /proc/$p/cwd)" = "$PWD" ] && exit 0; done; exit 1 ); do sleep 60; done   # only this book's own audio job
[ -s ${PREFIX}_audiobook.mp3 ] && [ -s ${PREFIX}_audiobook_timing.json ] || fail "the audio is missing (see run_audio.log)"
say "audio ready: $(ffprobe -v error -show_entries format=duration -of csv=p=0 ${PREFIX}_audiobook.mp3) s"
if [ ! -s ${PREFIX}_YouTube.mp4 ]; then
  say "rendering the video"
  rm -rf scenes video_only.mp4
  nice -n 5 ../venv/bin/python ../pipeline/make_video.py --workers 10 > run_video.log 2>&1
  [ -s ${PREFIX}_YouTube.mp4 ] || fail "the video was not made (see run_video.log)"
fi
V=$(ffprobe -v error -show_entries format=duration -of csv=p=0 ${PREFIX}_YouTube.mp4)
A=$(ffprobe -v error -show_entries format=duration -of csv=p=0 ${PREFIX}_audiobook.mp3)
python3 -c "import sys; sys.exit(0 if abs($V-$A) < 0.5 else 1)" || fail "video $V s and audio $A s differ by more than half a second"
say "video ok: $V s (audio $A s)"
PKG_MODE=text ../venv/bin/python ../pipeline/make_package.py > run_package.log 2>&1 || fail "subtitles/description failed (see run_package.log)"
KEY=~/.ssh/id_ed25519_bibliotheque_deliver
SSHO="ssh -i $KEY -o IdentitiesOnly=yes -o BatchMode=yes -o ConnectTimeout=20"
FILES="${PREFIX}_YouTube.mp4 ${PREFIX}_youtube_description.txt"
say "sending to the main server"
for i in 1 2 3 4 5; do rsync -a --partial -e "$SSHO" $FILES deliver@31.207.7.3:$SLUG/ && break; sleep 30; done
# verify the copy with checksums (a dry run that reports any file that differs)
DIFF=$(rsync -ac --dry-run -i -e "$SSHO" $FILES deliver@31.207.7.3:$SLUG/ | grep -c '^[<>]')
[ "$DIFF" = "0" ] || fail "the copy on the main server differs ($DIFF files)"
say "delivered and verified; handing over to the main server (upload and cleanup)"
: > READY
rsync -a -e "$SSHO" READY deliver@31.207.7.3:$SLUG/ || fail "could not drop the READY marker"
rm -f READY
say "done: the main server takes it from here"
