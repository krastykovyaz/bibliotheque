#!/bin/bash
# Russian-only (Gemini voice) chain, runs ON aak-llm: waits for this book's Russian audio job, renders the Russian video, makes the Russian
# subtitles + description, and (only when DELIVER=yes) sends everything to the main server's incoming folder and drops READY.
#   nohup ./chain_ru.sh <slug> <Prefix> > chain_ru.log 2>&1 &                  (render + package only: the pilot)
#   DELIVER=yes nohup ./chain_ru.sh <slug> <Prefix> [incoming-name] > ...      (also deliver; incoming-name default <slug>-ru)
# The Russian thumbnail needs Chrome (not on aak-llm): make it on the Mac first (BOOK_LANG=ru PKG_MODE=thumb make_package.py) and copy
# <Prefix>_RU_thumbnail.png and video_assets_ru/ (BOOK_LANG=ru make_video_assets.py) into the book folder here.
# Playlist / placement of Russian kids videos is not decided: it is not handled here.
set -u
SLUG=$1; PREFIX=$2; INBOX=${3:-$SLUG-ru}; DELIVER=${DELIVER:-no}; WORKERS=${WORKERS:-4}
cd ~/bibliotheque-production/$SLUG || exit 1
export BOOK_DIR=$PWD BOOK_LANG=ru
say() { echo "[$(date +%H:%M:%S)] $*"; }
fail() { say "STOPPED: $*"; echo "$*" > CHAIN_RU_FAILED; exit 1; }
rm -f CHAIN_RU_FAILED
say "waiting for the Russian audio"
while ( for p in $(pgrep -f make_audio_gemini); do [ "$(readlink /proc/$p/cwd)" = "$PWD" ] && exit 0; done; exit 1 ); do sleep 30; done   # only this book's own audio job
A_=${PREFIX}_RU_audiobook
[ -s $A_.mp3 ] && [ -s ${A_}_timing.json ] || fail "the Russian audio is missing (see run_audio_ru.log; a daily quota stop needs a re-run)"
say "audio ready: $(ffprobe -v error -show_entries format=duration -of csv=p=0 $A_.mp3) s"
[ -d video_assets_ru ] || fail "video_assets_ru is missing (make it on the Mac: BOOK_LANG=ru make_video_assets.py)"
if [ ! -s ${PREFIX}_RU_YouTube.mp4 ]; then
  while [ "$(df --output=avail -BG ~ | tail -1 | tr -dc 0-9)" -lt 20 ]; do sleep 600; done   # needs about 20 GB free for the audio, video and episode cuts (the disk was full on 2026-11-28)
  say "rendering the video"
  rm -rf scenes video_only.mp4
  nice -n 5 ../venv/bin/python ../pipeline/make_video.py --workers $WORKERS > run_video_ru.log 2>&1
  [ -s ${PREFIX}_RU_YouTube.mp4 ] || fail "the video was not made (see run_video_ru.log)"
fi
V=$(ffprobe -v error -show_entries format=duration -of csv=p=0 ${PREFIX}_RU_YouTube.mp4)
A=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $A_.mp3)
python3 -c "import sys; sys.exit(0 if abs($V-$A) < 0.5 else 1)" || fail "video $V s and audio $A s differ by more than half a second"
say "video ok: $V s (audio $A s)"
PKG_MODE=text ../venv/bin/python ../pipeline/make_package.py > run_package_ru.log 2>&1 || fail "subtitles/description failed (see run_package_ru.log)"
[ -s ${PREFIX}_RU_thumbnail.png ] || fail "the Russian thumbnail is missing (make it on the Mac with BOOK_LANG=ru PKG_MODE=thumb)"
say "package ready: ${PREFIX}_RU_YouTube.mp4, ${PREFIX}_RU_youtube_description.txt, ${PREFIX}_RU.srt, ${PREFIX}_RU_thumbnail.png"
if python3 -c "import json,sys; sys.exit(0 if json.load(open('book.json')).get('episodes') else 1)"; then   # split book (over an hour): cut the Russian video into its episodes here
  say "cutting the Russian video into the episodes of book.json"
  BOOK_DIR=$PWD python3 split_ru.py > run_split_ru.log 2>&1 || fail "the split failed (see run_split_ru.log)"
  cat run_split_ru.log
  say "episodes ready (${PREFIX}_RU_EP<n>.mp4 and descriptions); delivery of Russian episodes is not decided (playlist/placement), nothing was sent"
  exit 0
fi
if [ "$DELIVER" != "yes" ]; then say "DELIVER is not yes: stopping before delivery"; exit 0; fi
KEY=~/.ssh/id_ed25519_bibliotheque_deliver
SSHO="ssh -i $KEY -o IdentitiesOnly=yes -o BatchMode=yes -o ConnectTimeout=20"
FILES="${PREFIX}_RU_YouTube.mp4 ${PREFIX}_RU_youtube_description.txt ${PREFIX}_RU_thumbnail.png"
say "sending to the main server: $INBOX"
for i in 1 2 3 4 5; do rsync -a --partial -e "$SSHO" $FILES deliver@31.207.7.3:$INBOX/ && break; sleep 30; done
DIFF=$(rsync -ac --dry-run -i -e "$SSHO" $FILES deliver@31.207.7.3:$INBOX/ | grep -c '^[<>]')
[ "$DIFF" = "0" ] || fail "the copy on the main server differs ($DIFF files)"
say "delivered and verified; dropping READY"
: > READY
rsync -a -e "$SSHO" READY deliver@31.207.7.3:$INBOX/ || fail "could not drop the READY marker"
rm -f READY
say "done: the main server takes it from here"
