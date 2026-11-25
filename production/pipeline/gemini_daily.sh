#!/bin/bash
# Daily Gemini (free tier) Russian audio for the kids' books, runs ON aak-llm from cron. Reads gemini_queue.txt ("slug Prefix" per line,
# in order), makes <Prefix>_RU_audiobook.mp3 for each book that has none (chunk mode, gemini-3.1-flash-tts-preview, about 15 requests a
# day), and after a finished book starts its video chain (chain_ru.sh, DELIVER=no, one render at a time) in the background.
# Free quota resets at midnight Pacific = 09:00 CET: the cron lines run at 09:10 and 12:10 CET (see `crontab -l`, they are marked
# "bibliotheque gemini daily"). A book whose voices_gemini.json, Russian script or video_assets_ru is not there yet is skipped for the day.
# Exit code 3 of the audio script (daily quota used up) stops the whole run; finished chunks are kept and the next run goes on.
#
# TO REMOVE THE SCHEDULE: run `crontab -e` and delete the two lines marked "bibliotheque gemini daily" (or: crontab -l | grep -v 'bibliotheque gemini daily' | crontab -).
# To stop a run in progress: kill the PID in gemini_daily.lock (do not kill other jobs). To skip a book: delete its line from gemini_queue.txt.
# Log: gemini_daily.log (timestamps, book names, counts; never the key or any text).
export PATH=/usr/local/bin:/usr/bin:/bin:$PATH
ROOT=$HOME/bibliotheque-production
LOG=$ROOT/gemini_daily.log
LOCK=$ROOT/gemini_daily.lock
log() { echo "[$(date '+%F %H:%M:%S %Z')] $*" >> "$LOG"; }
if [ -f "$LOCK" ] && kill -0 "$(cat "$LOCK" 2>/dev/null)" 2>/dev/null; then log "another run is active (pid $(cat "$LOCK")): leaving"; exit 0; fi
echo $$ > "$LOCK"
trap 'rm -f "$LOCK"' EXIT
log "run start (pid $$)"
export GEMINI_TTS_MODEL=gemini-3.1-flash-tts-preview BOOK_LANG=ru

start_chain() {   # slug Prefix: video + package in the background, one render at a time, no delivery
  local slug=$1 P=$2 d=$ROOT/$1
  [ -s "$d/${P}_RU_YouTube.mp4" ] && return
  [ -e "$d/CHAIN_RU_STARTED" ] && [ ! -e "$d/CHAIN_RU_FAILED" ] && return
  [ -e "$d/CHAIN_RU_FAILED" ] && { log "$slug: the video chain failed earlier (CHAIN_RU_FAILED), not restarting"; return; }
  : > "$d/CHAIN_RU_STARTED"
  ( cd "$d" && DELIVER=no WORKERS=2 setsid nohup flock -x "$ROOT/gemini_render.lock" nice -n 10 ./chain_ru.sh "$slug" "$P" > chain_ru.log 2>&1 < /dev/null & )
  log "$slug: video chain started in the background (waits for the render lock)"
}

while read -r slug P; do
  [ -z "$slug" ] && continue
  case "$slug" in \#*) continue;; esac
  d=$ROOT/$slug
  [ -d "$d" ] || { log "$slug: folder missing, skipped"; continue; }
  cd "$d" || continue
  if [ -s "${P}_RU_audiobook.mp3" ] && [ -s "${P}_RU_audiobook_timing.json" ]; then start_chain "$slug" "$P"; continue; fi
  miss=""
  for f in voices_gemini.json "${P}_voice_script_ru.json" chain_ru.sh; do [ -s "$f" ] || miss="$miss $f"; done
  [ -d video_assets_ru ] || miss="$miss video_assets_ru"
  [ -n "$miss" ] && { log "$slug: not ready (missing:$miss), skipped for today"; continue; }
  if ! ../venv/bin/python - "${P}_voice_script_ru.json" <<'PY'
import json, sys
v = json.load(open("voices_gemini.json", encoding="utf-8"))
need = {r["speaker"] for r in json.load(open(sys.argv[1], encoding="utf-8")) if r["text"].strip()}
sys.exit(0 if all(v.get(s, {}).get("voice") for s in need) else 1)
PY
  then log "$slug: voices_gemini.json does not cover every speaker yet, skipped for today"; continue; fi
  log "$slug: audio (chunk mode)"
  BOOK_DIR=$PWD nice -n 10 ../venv/bin/python ../pipeline/make_audio_gemini.py --chunk --script "${P}_voice_script_ru.json" \
    --voices voices_gemini.json --name "${P}_RU_audiobook" --seg-dir segments_gemini_ru > run_audio_ru_daily.log 2>&1
  rc=$?
  log "$slug: audio script exit code $rc ($(grep -c '^  chunk ' run_audio_ru_daily.log) chunks reported this run)"
  if [ $rc -eq 3 ]; then log "daily quota used up: stopping for today"; break; fi
  if [ $rc -eq 0 ] && [ -s "${P}_RU_audiobook.mp3" ]; then log "$slug: audio finished"; start_chain "$slug" "$P"; else log "$slug: audio not finished (see $slug/run_audio_ru_daily.log)"; fi
done < "$ROOT/gemini_queue.txt"
log "run end"
