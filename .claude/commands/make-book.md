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
5b. Children's books: when the book's item in `data/queue.json` has `"kids": true` (or the user says it is for children), right after the private upload mark every video of the book as made for kids: `node scripts/youtube-made-for-kids.mjs <video id> [...]` (`--check` only shows the setting). YouTube then turns off comments, personalised ads and notifications for them. Tell the user. Books that are about children but meant for adults (Chekhov's Children, The Blind Musician) are not marked.

## Children's books (queue items with `"kids": true`)

More pictures, and suitable ones:
- Video: one scene per 1-1.5 minutes of audio (not 2-4), 3-4 shots per picture, a friendly character on screen whenever one speaks; where the tale has weather use `fx`.
- PDF: a picture on every part opening and about one more per 300-400 words, so a child sees a picture on almost every spread; frame and a short italic caption under each.
- Suitable: soft bright colours, rounded friendly shapes, no frightening or violent imagery (villains and sad moments are shown gently, as the tale tells them), simple clear English a child can follow, a warm unhurried narrator, child-friendly glossary. The description says it is a tale for children and for listening together. After the private upload mark the videos as made for kids (5b).

## Rules for pictures, scenes and animation (from the user)

Video:
- A scene is a change of place or time in the story. Aim for one scene per 2-4 minutes of audio (a 30-minute story needs 8-15 scenes, not 5).
- A scene change is tied to a paragraph of the story where the place changes (for example, Yalta -> the hotel room at paragraph 18 of part I). In book.json list them as `"scenes": [{"id": <first voice-script row id of the scene>, "art": "<picture name>"}, ...]` (make_video.py `plan_scenes`; every part start also starts a scene, keeping the previous picture if none is listed). Letter books use `art_pool` instead.
- Inside a scene the camera changes shot about every 20-30 seconds (3-5 prepared shots per picture: a wide one and several close ones, repeated in reverse when the scene is long). Weather animation goes over the picture where the story has it (snow, rain, falling leaves, candle flicker: `fx` in book.json).
- Under the picture there is always the thin gold line and the label "PART I · NAME".
- Draw more pictures for the video than for the PDF: the PDF gets only the key illustrations (one per part, `art`), the video gets the whole series (`scenes`/`art_pool`), drawn as extra scenes in the same style.

PDF (reading edition): the part number in gold with the part name, the illustration at the top of a part (full page width, about a third of the page height), then the text with a drop capital; every part starts on a new page. A frame and an italic caption under each picture, and a picture about every 1,500 words in long parts, are wanted too (not built yet: tell the user).

6. Never put secrets, keys or the user's email in commits. Commit with the noreply identity.
