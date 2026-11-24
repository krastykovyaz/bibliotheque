#!/usr/bin/env bash
# Deploys the site to the main server: builds the main branch from a fresh clone for the real address,
# copies the result over and restarts the service. Commit and push first.
#   scripts/deploy-site.sh
# Settings (defaults are for this project): SERVER, SERVER_KEY, SITE_URL, REPO_URL
set -euo pipefail
SERVER=${SERVER:-root@31.207.7.3}
KEY=${SERVER_KEY:-$HOME/.ssh/id_ed25519_bibliotheque_server}
URL=${SITE_URL:-https://biblio.unilu.space}
REPO=${REPO_URL:-https://github.com/krastykovyaz/bibliotheque.git}
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
echo "building from a fresh clone of $REPO for $URL ..."
git clone -q "$REPO" "$TMP/src"
(cd "$TMP/src" && npm ci --no-audit --no-fund >/dev/null 2>&1 && SITE_URL="$URL" npm run build >/dev/null)
ssh_() { ssh -i "$KEY" -o IdentitiesOnly=yes -o BatchMode=yes -o ConnectTimeout=20 "$SERVER" "$@"; }
ssh_ 'git -C /opt/bibliotheque pull --ff-only -q; rm -rf /opt/bibliotheque/dist.new; mkdir -p /opt/bibliotheque/dist.new'
COPYFILE_DISABLE=1 tar -C "$TMP/src/dist" -cf - . | ssh_ 'tar -C /opt/bibliotheque/dist.new -xf -'
ssh_ 'cd /opt/bibliotheque && rm -rf dist.old && mv dist dist.old && mv dist.new dist && systemctl restart bibliotheque && sleep 3 && echo "service: $(systemctl is-active bibliotheque)" && rm -rf dist.old'
curl -s -o /dev/null -m 20 -w "live site $URL/: %{http_code}\n" "$URL/"
