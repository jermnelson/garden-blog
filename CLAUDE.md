# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

"Garden Reflections" is a personal gardening blog by Jeremy Nelson, hosted on GitHub Pages at https://jermnelson.github.io/garden-blog. The active branch is `gh-pages`.

## Running the generator

```bash
python3 generate.py
```

Regenerates `rss.xml` from all posts. This also runs automatically via the `pre-commit` git hook — `rss.xml` is staged and included in every commit automatically.

## Architecture

The blog is a **PyScript single-page application** using the `puepy` framework (loaded from `./wheels/puepy-0.6.5-py3-none-any.whl`). PyScript runs Python directly in the browser.

- `index.html` — entry point; loads PyScript 2025.8.1 and runs `main.py`
- `main.py` — defines the app, router, and three pages (`BlogHome`, `YearBlogPosts`, `BlogPost`) using hash-based routing (`#posts/<year>/<post_id>`)
- `common.py` — shared PyScript components: `BlogHeader`, `BlogFooter`, `BlogPost`, `PostListing`
- `pyscript.json` — PyScript config; lists every post file that PyScript must fetch at runtime
- `generate.py` — standalone script (runs server-side, not in browser) that generates `rss.xml`

## Adding a new post

1. Create `posts/0{YYYY}/MM-DD.md` (year directories use a leading zero, e.g. `02025`)
2. Add an entry to `pyscript.json` under `"files"`:
   ```json
   "./posts/02025/MM-DD.md": "./02025/MM-DD.md"
   ```
   Both keys (source under `posts/`) and values (destination without `posts/`) are required — PyScript uses this mapping to make files available to the in-browser Python runtime.
3. Commit — the pre-commit hook runs `generate.py` and stages the updated `rss.xml` automatically.

## Embedding images

Google Drive photos use this URL format:
```
https://drive.google.com/uc?export=view&id=<file_id>
```

## Deprecated

`index-template.html` is no longer used. The old `generate.py` previously wrote `index.html` from this template; that behavior has been removed.
