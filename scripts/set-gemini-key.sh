#!/bin/bash
# Puts your Gemini API key on aak-llm (the production machine), without it appearing on screen, in the shell history,
# in a command line, in git or in any log. Run it yourself in a terminal:
#
#   scripts/set-gemini-key.sh
#
# It asks for the key (typing is hidden), stores it in ~/.config/bibliotheque/gemini.key on aak-llm (only you can read it),
# and tests it with one small request, printing only the HTTP status (200 = works).
# To remove the key later:  ssh aak-llm 'rm ~/.config/bibliotheque/gemini.key'
set -u
HOST=${1:-aak-llm}
printf 'Gemini API key (hidden): '
read -rs KEY; echo
[ -n "$KEY" ] || { echo "no key entered, nothing done"; exit 1; }
# the key travels through ssh's standard input, so it is not in any command line
printf '%s' "$KEY" | ssh -o ConnectTimeout=30 "$HOST" 'umask 077; mkdir -p ~/.config/bibliotheque && cat > ~/.config/bibliotheque/gemini.key && chmod 600 ~/.config/bibliotheque/gemini.key' \
  || { echo "could not reach $HOST (it may be too busy: try again in a few minutes)"; unset KEY; exit 1; }
unset KEY
echo "stored on $HOST: ~/.config/bibliotheque/gemini.key"
# test: list the models with the stored key (the key is sent in a header, never in the address)
CODE=$(ssh -o ConnectTimeout=30 "$HOST" 'curl -s -o /dev/null -w "%{http_code}" -H "x-goog-api-key: $(cat ~/.config/bibliotheque/gemini.key)" https://generativelanguage.googleapis.com/v1beta/models')
echo "test request to Google from $HOST: HTTP $CODE"
case "$CODE" in
  200) echo "OK: the key works." ;;
  400|403) echo "Google refused the key (check that it is a Gemini API key from aistudio.google.com and that the Generative Language API is enabled)." ;;
  000) echo "$HOST could not reach Google: audio would have to be made on this Mac instead." ;;
  *) echo "Unexpected answer; tell Claude the number above." ;;
esac
