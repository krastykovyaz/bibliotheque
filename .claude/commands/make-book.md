---
description: Make one book end to end (text, translation, art, voices, PDFs, video), up to delivery on the main server
argument-hint: <author or NEXT> <title>
---

Make the audiobook-video and reading edition for: $ARGUMENTS

If the argument is NEXT, take the first item of `data/queue.json`.

1. Rights: confirm the text is in the public domain (author died before 1955 or published before 1929 in the US) and find a clean source (Wikisource or Gutenberg). Stop and tell the user if unclear.
2. Create `production/<slug>/` with `book.json` (use `production/how-much-land/book.json` as the model), the cleaned source (`source_clean.json`), `translation_en.json` if the source is not English, the voice script `<prefix>_voice_script.json`, `voices_kokoro.json`, and the illustrations `art/*.svg` with `art/cover.svg`.
2b. Length: estimate the audio (about 150 words a minute). If it is longer than about an hour, plan to split it into several videos of 40-60 minutes, cut at part boundaries (group the parts by topic), and tell the user the plan before starting. (The pipeline builds one video per book today; splitting needs one run per group or a `groups` setting that has to be built first.)
3. Run the pipeline: `production/pipeline/.venv/bin/python production/pipeline/run_book.py <slug>`. It runs check, pdf, assets, audio (aak-llm), video (aak-llm), package, deliver (main server). Finished stages are reused, so it can be run again.
4. Report what was made and the sound/picture checks. Do NOT upload to YouTube and do NOT publish to the site until the user says so.
5. Upload and publish: the upload goes to the main server's incoming folder with a READY marker (`touch READY` there); its 2-minute timer uploads PRIVATE into the playlist and deletes the files, and the result link is in /root/bibliotheque-uploaded/<slug>.txt. Then publish to the site at once, without waiting for the video to be public: `... publish_to_site.py <slug> --youtube <link>` (and `--lang ru` for the Russian text and PDFs; build the Russian PDF first with `BOOK_LANG=ru build_pdf.py` and `make_booklet.py`). The book page asks our own server whether the video is public and shows the player by itself as soon as the user makes it public. After the upload ask the user to set the video Public and tick the AI-voice disclosure; add the book-page link to the YouTube description with `scripts/youtube-set-description.mjs`.
6. Never put secrets, keys or the user's email in commits. Commit with the noreply identity.
