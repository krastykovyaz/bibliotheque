# Bibliothèque

A small static showcase of audiobook-videos made from public-domain classics. Visitors pick a book and a language, read a short description, and open or play the YouTube video voiced in that language.

Book pages are static HTML. A small Node server adds a Settings page where a visitor can connect a Grandlivre account. There are no payments, no logins of its own, no analytics and no tracking. It is built with [Astro](https://astro.build) and outputs plain HTML.

## Run it

You need Node.js 22.18 or newer (the Grandlivre connection uses Node's built-in SQLite and runs TypeScript tests directly).

```bash
npm install
npm run dev      # local preview with live reload, http://localhost:4321
npm run build    # validates data/books.json, then writes the site to dist/
npm run preview  # serves the built site locally
npm start        # runs the built server (reads .env)
npm test         # tests for the Grandlivre connection
```

## Add a book

1. Put the cover image in `public/covers/` (PNG, JPEG or WebP; a 2:3 portrait such as 600×900 works well).
2. Add an entry to `data/books.json`:

```json
{
  "id": "lady-with-the-little-dog",
  "author": { "en": "Anton Chekhov", "ru": "Антон Чехов" },
  "year": 1899,
  "cover": "/covers/lady.png",
  "languages": {
    "en": {
      "title": "The Lady with the Little Dog",
      "description": "Three to five sentences in English.",
      "youtube": "https://www.youtube.com/watch?v=VIDEO_ID"
    },
    "ru": {
      "title": "Дама с собачкой",
      "description": "Три-пять предложений на русском.",
      "youtube": "https://www.youtube.com/watch?v=VIDEO_ID"
    }
  }
}
```

That is all. The build creates the book pages and adds the card to the home page.

Rules the build checks (it stops with a message naming the book and the field):

- `id` is unique and uses lowercase letters, digits and hyphens. It becomes the URL `/book/<id>/`.
- `author.en`, `year` and `cover` are present, and the cover file exists in `public/`.
- `languages.en` is present. English is the fallback when a book has no video in the visitor's language.
- Every language has `title`, `description` and a valid `youtube` link.

Language keys are two- or three-letter codes (`en`, `ru`, `de`, `zh`, …). Any code works as an audio language. To show a readable name for a new code, add it to `names` in `src/lib/i18n.ts`.

The two sample books use placeholder covers and the placeholder video id `PLACEHOLDER`. The build prints a warning for each placeholder link. Replace them before publishing.

## Search

The top bar of every page has a search over the books: a magnifier that opens into a field when clicked (a full field on wide screens). It also finds the children's stories (one common search: they appear as cards among the results, marked "For children"). It matches titles and authors in every language, the year, and audio languages (by code or name, in English or Russian), and ignores case and accents. On the home page it filters as you type; on other pages, Enter opens the home page with the results. It keeps the query in the address (`?q=`), and needs JavaScript; without it the box is hidden and all books are shown. Nothing is sent anywhere: all matching happens in the browser.

## Next on the shelf (daily announcement)

The home page ends with a "Next on the shelf" block that announces one upcoming book per day, in the order of `data/queue.json` (starting at its `start` date, then looping). It only announces: nothing is translated, voiced or published from the queue. Reorder or edit the file freely.

The page is built ahead of time, so the block changes when the site is rebuilt. A daily scheduled task on this Mac runs `npm run build` each morning for that. Without it the announcement stays on the day of the last build.

## Children's page

`/children/` (and `/ru/children/`) lists children's authors and their stories from `data/sources/children.json`, each with a link to the Russian original on Wikisource (from `data/sources/wikisource-children.json`). These are catalogue entries only: there are no videos yet, so they are not book cards. To refresh the links after editing the list: `node scripts/find-on-wikisource.mjs data/sources/children.json data/sources/wikisource-children.json`. To turn a story into a real book, add it to `data/books.json` as described above.

## Read online (reading mode)

A language can have its full text on the site, so visitors read the whole book in the browser without downloading anything:

```json
"text": "texts/lady-en.txt",
"textNote": "Machine translation from the Russian, a draft that needs a human editor."
```

`text` is a file in `data/texts/`: a line starting with `## ` begins a part (for example `## I · Yalta`), and blank lines separate paragraphs. `textNote` is optional and is shown above the text. The book page then shows **Read online** (instead of the short preview), and the whole text is on its own page at `/read/<id>/<language>/`, in a reading layout that works without JavaScript and sets no cookie.

To get the text out of one of our reading PDFs: `python scripts/extract-text-from-pdf.py public/pdf/lady-en.pdf data/texts/lady-en.txt` (needs `pip install pymupdf`; it expects the layout our PDFs have).

## Preview (no registration)

Each language can have an optional excerpt:

```json
"preview": "/preview/lady-en.txt"
```

Put a UTF-8 text file in `public/preview/`; blank lines separate paragraphs. The book page then shows "Read a preview", which opens the excerpt for everyone. It needs no registration and no JavaScript. Use only a short opening of a public-domain text.

## Full version download (PDF)

Each language of a book can have these optional fields:

```json
"pdf": "/pdf/lady-en.pdf",
"booklet": "/pdf/lady-en-booklet.pdf"
```

Put the files in `public/pdf/`. `booklet` is optional: an A4 print layout offered next to the reading PDF (the page then shows two download buttons). To make one from a reading PDF: `python3 scripts/make-booklet.py reading.pdf booklet.pdf`. The book page then shows "Download full version (PDF)". The button opens a box with two choices: "Connect Grandlivre", which starts the same connection as the Settings page, and "Skip and download the PDF".

The site has no registration form and does not check whether a visitor connected: the PDF is a public file and connecting can always be skipped. After Allow or Deny on Grandlivre the visitor returns to Settings, not to the book. The sample books use placeholder PDFs.

## How languages work

- The interface has two languages. English pages live at `/`, Russian pages at `/ru/`. The visitor switches the interface language on the Settings page.
- The chosen language is kept in the URL as `?lang=ru`, so links can be shared. Nothing is stored in the browser.
- On a book page, `?lang=` also selects the audio language. If the book has no video in that language, the English one is shown with a short note.
- Without JavaScript, a book page lists every language one after another with plain links.
- Page title, description and Open Graph tags are generated per book for English and Russian. Other audio languages share the page of the interface language they are opened in.

## Connect Grandlivre

Visitors can connect their Grandlivre account on the Settings page (`/settings/`) or from the download box on a book page. This is OAuth 2.1 with PKCE; the site has no login of its own.

- **Who the tokens belong to:** an anonymous session. The first click on "Connect Grandlivre" sets one cookie (`bib_sid`, HttpOnly). Clearing the cookie loses the connection on our side.
- **Storage:** sessions and tokens live in a SQLite file (`.data/bibliotheque.sqlite`). Tokens are encrypted with `GRANDLIVRE_TOKEN_KEY`; session ids are stored hashed. Tokens never reach the browser or the logs.
- **Disconnect:** forgets the tokens on our side. The visitor can also switch the connection off in Grandlivre: Profile > Money > API keys.
- **Limits:** the token does not identify a person, connecting makes nobody a partner in Grandlivre, and Grandlivre never moves money or confirms that money arrived.

Setup, once per environment:

```bash
node scripts/grandlivre-register.mjs https://your-domain.example/grandlivre/callback
```

This registers the app with Grandlivre and writes `GRANDLIVRE_CLIENT_ID`, `GRANDLIVRE_REDIRECT_URI` and a new `GRANDLIVRE_TOKEN_KEY` to `.env` (see `.env.example`). Without an argument it registers `http://localhost:4321/grandlivre/callback`. Keep `.env` and `.data/` out of git and back up the key: without it stored tokens cannot be read.

To call the Grandlivre API from server code, use `grandlivreFetch` in `src/server/grandlivre.ts`. On a 401 it refreshes the tokens, saves the new refresh token and retries once; if that fails it throws `ReconnectNeeded` and Settings shows "Reconnect Grandlivre". Nothing in the site calls the API yet.

## Upload videos to YouTube

`scripts/youtube-upload.mjs` uploads a finished video with the YouTube Data API. The title and description come from `data/books.json`, so the video matches the site, and the AI-voice disclosure is switched on.

One-time setup (about ten minutes, in your browser):

1. In [Google Cloud Console](https://console.cloud.google.com) create a project and enable **YouTube Data API v3**.
2. **OAuth consent screen**: type External, leave it in *Testing*, and add your own Google account under *Test users*.
3. **Credentials > Create credentials > OAuth client ID**, type *Desktop app*. Download the JSON and save it as `.data/youtube-client.json` (`.data/` is not committed).

Upload:

```bash
node scripts/youtube-upload.mjs video.mp4 --book lady-with-the-little-dog --lang en --dry-run   # check the metadata first
node scripts/youtube-upload.mjs video.mp4 --book lady-with-the-little-dog --lang en             # real upload, private
```

The first real run opens Google sign-in in your browser; the login is kept in `.data/youtube-token.json`. The script prints the video link, which you put into `languages.<code>.youtube` in `data/books.json`.

Things to know:

- **Videos come out private.** Google locks API uploads from projects it has not audited to private. Open YouTube Studio > Content and set Visibility to Unlisted or Public yourself. The site cannot play a private video.
- **Testing mode** sign-ins expire after seven days; just run the script again to sign in.
- **Custom thumbnails** need a phone-verified channel; if the script cannot set one, add it in YouTube Studio.
- The script never uploads without you running it, and it never changes `data/books.json` itself.

## Deploy

Set `SITE_URL` to the public address at build time. It is used for canonical links and share images, and it is the host the server accepts form posts for.

**Node host (full site)**

On the main server, `scripts/deploy-site.sh` does all of this: it builds `main` from a fresh clone for the real address, copies the result over and restarts the service.

```bash
SITE_URL=https://your-domain.example npm run build
HOST=0.0.0.0 PORT=4321 npm start
```

Serve it over HTTPS and keep `.data/` on a persistent disk.

**Cloudflare Pages or GitHub Pages (static part only)**

The book, home and about pages are plain HTML in `dist/client/` and can be hosted statically. Settings and the Grandlivre connection need the Node server, so they do not work on a static host; if you deploy this way, remove the Settings link in `src/layouts/Layout.astro` and the Connect form in `src/views/Book.astro`. For a GitHub project site also set `BASE_PATH=/<repo>`.

## Where things are

| Path | What it is |
| --- | --- |
| `data/books.json` | All book content |
| `public/covers/` | Cover images |
| `src/styles/global.css` | Colours and fonts (CSS variables at the top) |
| `src/lib/i18n.ts` | Interface texts in English and Russian, About page text |
| `public/pdf/` | Full-version PDF files |
| `src/views/Book.astro` | Book page, with the download block and a marked `FUTURE STORE SLOT` for a price and Buy button |
| `src/scripts/book.ts` | Language switch and click-to-load player |
| `src/lib/validate.mjs` | Rules for `data/books.json` |
| `scripts/youtube-upload.mjs` | Uploads a video to YouTube from `data/books.json` metadata |
| `src/server/` | Grandlivre connection: OAuth flow, token refresh, encrypted storage |
| `src/pages/grandlivre/` | Connect, callback and disconnect routes |
| `src/views/Settings.astro` | Settings page with the Connected / Disconnect state |
| `tests/` | Tests for the state check, the denied case and refresh rotation |

## Privacy

Fonts are self-hosted. The YouTube player uses `youtube-nocookie.com` and is created only after the visitor clicks "Play here". The site sets no cookie for reading; one session cookie is set only when a visitor clicks "Connect Grandlivre". There is no analytics or tracking.
