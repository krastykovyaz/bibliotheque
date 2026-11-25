#!/bin/bash
# From the Mac, for a book with an "episodes" list in book.json: makes the series playlist (podcast) if the book has none, makes the
# episode thumbnails and puts them on the main server, copies the book to aak-llm and starts chain_split_on_server.sh there
# (audio, video, cut into episodes, delivery; the main server's timer then uploads each part privately into the series playlist).
#   production/pipeline/launch_episodes.sh night-before-christmas Night_Before_Christmas [--no-start]
set -e
SLUG=$1; PREFIX=$2; NOSTART=${3:-}
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"; cd "$ROOT/production/$SLUG"
PY="$ROOT/production/pipeline/.venv/bin/python"; K=~/.ssh/id_ed25519_bibliotheque_server
if ! $PY -c "import json,sys; sys.exit(0 if json.load(open('book.json')).get('series_playlist') else 1)"; then
  T=$($PY -c "import json; b=json.load(open('book.json')); print(f\"{b['title']}, {b['author']}: full-cast audiobook in {len(b['episodes'])} parts\")")
  D=$($PY -c "import json; b=json.load(open('book.json')); print(f\"{b['title']} ({b['year']}) by {b['author']}, a full-cast audiobook in English in {len(b['episodes'])} parts. Voices and translation are made with AI. Read the text and download the book: https://biblio.unilu.space/book/{b['slug']}/\")")
  ID=$(cd "$ROOT" && node scripts/youtube-create-playlist.mjs "$T" "$D" public | sed -n 's/^playlist id: //p')
  [ -n "$ID" ] || { echo "could not create the playlist"; exit 1; }
  $PY -c "import json; b=json.load(open('book.json',encoding='utf-8')); b['series_playlist']='$ID'; json.dump(b,open('book.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)"
  echo "series playlist: $ID"
fi
BOOK_DIR=$PWD $PY ../pipeline/make_episode_thumbs.py >/dev/null
$PY ../pipeline/make_series_square.py "${PREFIX}_series_card.png" >/dev/null
(cd "$ROOT" && node scripts/youtube-playlist-image.mjs "$($PY -c "import json;print(json.load(open('production/$SLUG/book.json'))['series_playlist'])")" "production/$SLUG/${PREFIX}_series_square.png") || echo "could not set the playlist cover"
N=$($PY -c "import json; print(len(json.load(open('book.json'))['episodes']))")
for i in $(seq 1 $N); do
  ssh -n -i $K -o IdentitiesOnly=yes root@31.207.7.3 "mkdir -p /srv/bibliotheque-incoming/$SLUG-ep$i && chown deliver:deliver /srv/bibliotheque-incoming/$SLUG-ep$i"
  scp -q -i $K -o IdentitiesOnly=yes ${PREFIX}_EP${i}_thumbnail.png root@31.207.7.3:/srv/bibliotheque-incoming/$SLUG-ep$i/${PREFIX}_thumbnail.png
  ssh -n -i $K -o IdentitiesOnly=yes root@31.207.7.3 "chown -R deliver:deliver /srv/bibliotheque-incoming/$SLUG-ep$i"
done
ssh -n -o ConnectTimeout=20 -o BatchMode=yes aak-llm "mkdir -p ~/bibliotheque-production/pipeline ~/bibliotheque-production/$SLUG && cd ~/bibliotheque-production/$SLUG && ln -sfn ../models models && echo aak-llm is up"
scp -q ../pipeline/*.py ../pipeline/*.sh aak-llm:bibliotheque-production/pipeline/
scp -q book.json ${PREFIX}_voice_script.json voices_kokoro.json aak-llm:bibliotheque-production/$SLUG/
rsync -a video_assets aak-llm:bibliotheque-production/$SLUG/
[ "$NOSTART" = "--no-start" ] && { echo "synced, not started"; exit 0; }
ssh -n aak-llm "cd ~/bibliotheque-production/$SLUG && chmod +x ../pipeline/*.sh && (nohup ../pipeline/chain_split_on_server.sh $SLUG $PREFIX > chain_split.log 2>&1 & echo \$! > chain_split.pid) && sleep 2 && cat chain_split.log"
