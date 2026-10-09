# Punjab & Kashmir Explorer

A website on the tribes, clans and biradaris of Pakistani Punjab and Azad Kashmir.

**Open the site: https://bigsmokelondon.github.io/punjab-kashmir-explorer/**

## What's in it

- 109 groups, from Arain, Awan and Gujjar to the Baloch tribes of Dera Ghazi Khan and the clans of the Salt Range.
- Each entry shows where the group was recorded, how it was classified and any origin stories, with a link to the exact source passage.
- The main historical source is Denzil Ibbetson's *Panjab Castes*, his account of the 1881 census (published 1883, reprinted 1916). You can read the cited passages and search the whole book on the site.

## How to use it

- Search for a name, spelling or place, or filter by region (Punjab or AJK), type, or the book's own groupings.
- Tap a name to open its record. "Read uploaded passage" shows the original text.
- You can save records and add your own notes. They stay on your device.

## A word of caution

The book is a colonial record from 1881. Its categories and place names belong to that time, and it includes the author's own prejudices and theories. A name being listed under a group, or an origin story being reported, doesn't prove any family's ancestry. Each entry keeps those caveats next to the claims.

The site works on phones too. If you spot a mistake or know a better source for a group, please [open an issue](https://github.com/BigsmokeLondon/punjab-kashmir-explorer/issues).

## Project notes

A buildless website. This folder is the master copy, kept in the public GitHub repository https://github.com/BigsmokeLondon/punjab-kashmir-explorer. GitHub Pages publishes it at https://bigsmokelondon.github.io/punjab-kashmir-explorer/ on every push to `main`; `.github/workflows/pages.yml` runs `check.mjs` first and leaves the project Design Report and the original banner out of the published site. A private claude.ai copy also exists: https://claude.ai/artifact/MCd5tP8iJdZoKhCJ9gSNUY.

The collection contains 109 records: 23 names from the AJK and Rajput project posters, plus 86 entries from the owner's uploaded `PANJAB  CASTES.txt`. Eighteen poster records have richer book context. Khawaja links a related book passage but stays a research lead. Every record has an "1881 grouping" that follows the part and section where the book discusses it (`GROUPS` in `book_research.py`, labels in `dist/core.js`). The book covers British Punjab, not the princely state of Jammu and Kashmir, so it adds Kashmiri settlers and Jammu-border tribes but no AJK-district records. The Chuhra/Musalli section (597–600) is deliberately not curated because of its language. It remains searchable in the full text. The text describes the 1881 census, first published in 1883 and reprinted in 1916. Its 1916 introduction explicitly says its figures and boundaries were not updated. Historical localities remain separate from modern poster examples. Source spellings are searchable, and unconfirmed labels remain marked as unconfirmed.

Review marks, saved records and notes use browser-local storage. They do not change the source dataset or sync between devices. Copy saved puts saved records on the clipboard with their caveats, source locators and personal review notes.

Edit `prepare-data.py` and `book_research.py` to maintain the collection, then run `python3 prepare-data.py` (or `python prepare-data.py` on Windows; output is always UTF-8 with LF line endings). The original upload is preserved byte-for-byte in `dist/assets/sources/Panjab_Castes_uploaded.txt`. The generator extracts 98 curated passages with one-based upload line ranges into `dist/passages.js`, and attaches reader links to individual claims. Separated ranges are displayed as omitted intervening material, never as continuous quotations. `dist/book.html` also searches the complete OCR on demand, with literal phrase matching and flexible whitespace. Application files are in `dist/`. No dependencies or build step are required.

On 9 October 2026 the owner chose to make the repository and the GitHub Pages site public. The pages keep noindex metadata, which asks search engines not to list them. To update the private claude.ai copy after changing `dist/`, run `python make_artifact.py <staging folder>` and republish the staged files to the same artifact, using `files.json` for the published paths. That host cannot start file downloads, so the pages offer none (`check.mjs` enforces this).

Historical source categories are period-specific and do not authenticate present-day genealogy. The decorative landscape and collection mark are not clan emblems or political boundary maps.

The heritage edition follows the supplied parchment and sepia reference. `dist/heritage.css` provides the theme. Two dated historical photographs have local copies, source credits and an accessible modal viewer. The hero panorama is explicitly labelled as AI-created decorative artwork. Artwork notes and the generation prompt are in `artwork-brief.md`.

Run `node check.mjs` for collection, export, passage integrity and full-text search checks. Run `node --check` on the browser scripts for syntax verification. Browser visual QA was unavailable in the managed environment for this edition. On 9 October 2026 the layout was checked in a browser at 360, 375, 414, 700 and 1280px. Phones (up to 760px) show the header links as a wrapping row, crop the banner from the centre only when it would be under 200px tall, and apply the reading-size floor at the end of `dist/heritage.css`.
