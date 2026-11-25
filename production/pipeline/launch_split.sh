#!/bin/bash
# From the Mac: copy the current scripts and files to aak-llm and start chain_split_on_server.sh there (it then needs nothing else).
#   production/pipeline/launch_split.sh poor-folk Poor_Folk 236 243 248     (the last numbers: ids of the voice-script rows that changed)
set -e
SLUG=$1; PREFIX=$2; shift 2
cd "$(dirname "$0")/../$SLUG"
ssh -n -o ConnectTimeout=20 -o BatchMode=yes aak-llm 'echo aak-llm is up' || { echo "aak-llm does not answer; try again later"; exit 1; }
scp -q ../pipeline/*.py ../pipeline/*.sh aak-llm:bibliotheque-production/pipeline/
scp -q book.json ${PREFIX}_voice_script.json voices_kokoro.json aak-llm:bibliotheque-production/$SLUG/
rsync -a video_assets/strip_*.png aak-llm:bibliotheque-production/$SLUG/video_assets/
ssh -n aak-llm "cd ~/bibliotheque-production/$SLUG && chmod +x ../pipeline/*.sh && (nohup ../pipeline/chain_split_on_server.sh $SLUG $PREFIX $* > chain_split.log 2>&1 & echo \$! > chain_split.pid) && sleep 2 && cat chain_split.log"
