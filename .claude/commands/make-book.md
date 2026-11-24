---
description: Make one book end to end (text, translation, art, voices, PDFs, video), up to delivery on the main server
argument-hint: <author or NEXT> <title>
---

Make the audiobook-video and reading edition for: $ARGUMENTS

If the argument is NEXT, take the first item of `data/queue.json`.

1. Rights: confirm the text is in the public domain (author died before 1955 or published before 1929 in the US) and find a clean source (Wikisource or Gutenberg). Stop and tell the user if unclear.
2. Create `production/<slug>/` with `book.json` (use `production/how-much-land/book.json` as the model), the cleaned source (`source_clean.json`), `translation_en.json` if the source is not English, the voice script `<prefix>_voice_script.json`, `voices_kokoro.json`, and the illustrations `art/*.svg` with `art/cover.svg`.
3. Run the pipeline: `production/pipeline/.venv/bin/python production/pipeline/run_book.py <slug>`. It runs check, pdf, assets, audio (aak-llm), video (aak-llm), package, deliver (main server). Finished stages are reused, so it can be run again.
4. Report what was made and the sound/picture checks. Do NOT upload to YouTube and do NOT publish to the site until the user says so.
5. When the user agrees: `... run_book.py <slug> --stages upload` (private upload into the playlist). After the user makes the video Public or Unlisted and gives the link: `... run_book.py <slug> --stages publish --youtube <link>`. A Russian edition of the text and PDFs: `BOOK_LANG=ru` for `build_pdf.py`, then `publish_to_site.py <slug> --lang ru`.
6. Never put secrets, keys or the user's email in commits. Commit with the noreply identity.
