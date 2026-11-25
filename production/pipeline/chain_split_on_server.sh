#!/bin/bash
# Runs ON aak-llm. Fixes the three narrator dates (August 1-3) in the audio, renders the video again, cuts it into the
# episodes of book.json, sends every episode to the main server (its own folder, with the thumbnail already there and
# the series playlist id), verifies the copies and drops READY markers in order. The main server uploads each one
# privately into the series playlist and deletes the files.
#   nohup ./chain_split_on_server.sh <slug> <Prefix> <first changed segment id> ... > chain_split.log 2>&1 &
set -u
SLUG=$1; PREFIX=$2; shift 2; CHANGED="$@"
cd ~/bibliotheque-production/$SLUG || exit 1
export BOOK_DIR=$PWD
say() { echo "[$(date +%H:%M:%S)] $*"; }
fail() { say "STOPPED: $*"; echo "$*" > CHAIN_FAILED; exit 1; }
rm -f CHAIN_FAILED
say "regenerating the changed narrator segments: $CHANGED"
for id in $CHANGED; do rm -f segments/$(printf '%04d' $id)_*.wav; done
nice -n 10 ../venv/bin/python ../pipeline/make_audio_kokoro.py > run_audio2.log 2>&1
[ -s ${PREFIX}_audiobook.mp3 ] && grep -q "Done:" run_audio2.log || fail "audio failed (run_audio2.log)"
say "audio ready"
rm -rf scenes video_only.mp4 ${PREFIX}_YouTube.mp4
nice -n 5 ../venv/bin/python ../pipeline/make_video.py --workers 10 > run_video2.log 2>&1
[ -s ${PREFIX}_YouTube.mp4 ] || fail "the video was not made (run_video2.log)"
V=$(ffprobe -v error -show_entries format=duration -of csv=p=0 ${PREFIX}_YouTube.mp4)
A=$(ffprobe -v error -show_entries format=duration -of csv=p=0 ${PREFIX}_audiobook.mp3)
python3 -c "import sys; sys.exit(0 if abs($V-$A) < 0.5 else 1)" || fail "video $V s and audio $A s differ"
say "video ok: $V s"
../venv/bin/python ../pipeline/split_episodes.py > run_split.log 2>&1 || fail "split failed (run_split.log)"
cat run_split.log
KEY=~/.ssh/id_ed25519_bibliotheque_deliver
SSHO="ssh -i $KEY -o IdentitiesOnly=yes -o BatchMode=yes -o ConnectTimeout=20"
N=$(grep -c '^part ' run_split.log)
SERIES=$(python3 -c "import json;print(json.load(open('book.json'))['series_playlist'])")
for i in $(seq 1 $N); do
  D=$SLUG-ep$i
  mkdir -p stage_ep$i && cp ${PREFIX}_EP$i.mp4 stage_ep$i/${PREFIX}_YouTube.mp4 && cp ${PREFIX}_EP${i}_youtube_description.txt stage_ep$i/${PREFIX}_youtube_description.txt && echo $SERIES > stage_ep$i/playlist.id
  say "sending part $i"
  for t in 1 2 3 4 5; do rsync -a --partial -e "$SSHO" stage_ep$i/ deliver@31.207.7.3:$D/ && break; sleep 30; done
  DIFF=$(rsync -ac --dry-run -i -e "$SSHO" stage_ep$i/ deliver@31.207.7.3:$D/ | grep -c '^[<>]')
  [ "$DIFF" = "0" ] || fail "the copy of part $i differs ($DIFF files)"
done
say "all parts delivered and verified; dropping the READY markers in order"
for i in $(seq 1 $N); do : > READY; rsync -a -e "$SSHO" READY deliver@31.207.7.3:$SLUG-ep$i/; rm -f READY; done
say "done: the main server takes it from here"
