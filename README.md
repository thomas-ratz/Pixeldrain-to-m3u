# Pixeldrain Playlist Scraper

Automate the creation of an `m3u` playlist from a Pixeldrain share link. The package fetches list metadata via Pixeldrain's public API and emits a standards-compliant playlist that any compatible media player can stream [^1].

## Project Layout

```
.
├─ src/pixeldrain_m3u/   # Package code (API helpers, playlist utils, CLI)
├─ tests/                # Pytest suite
├─ README.md             # This file
├─ DEV_PASS.md           # Development pass journal
└─ pyproject.toml        # Project metadata & dependencies
```

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt        # runtime
pip install -r requirements-dev.txt    # optional: dev/test tooling
```

The package can also be installed directly:

```powershell
pip install -e .
```

## Usage

### Single Pixeldrain list

```powershell
python -m pixeldrain_m3u https://pixeldrain.net/l/VmpS467P -o romance_dawn.m3u
# or, once installed:
pixeldrain-m3u VmpS467P --overwrite
```

### One Pace auto-scrape

```powershell
# Grab every arc (best English-sub Pixeldrain link) and stitch into one playlist
python -m pixeldrain_m3u --onepace https://onepace.net/en/watch -o onepace_all.m3u

# Use defaults (One Pace watch URL) and limit to arcs containing "Wano" or "Dressrosa"
pixeldrain-m3u --onepace --arc-filter Wano --arc-filter Dressrosa -o favorites.m3u
```

Key flags:

- `--output`: destination file (default `playlist.m3u`)
- `--base-url`: point at a Pixeldrain mirror or self-host
- `--overwrite`: replace an existing playlist file
- `--onepace`: interpret `source` as a One Pace watch page (or omit to use the default page)
- `--arc-filter`: repeatable filter that keeps arcs whose title contains the provided text

You can pass a raw list ID instead of a full Pixeldrain URL, and the CLI honors `PIXELDRAIN_BASE_URL` so you can globally override the domain. In One Pace mode, each playlist entry is grouped by arc (`group-title`) and prepends the arc name in the title, matching common IPTV playlist conventions.

## Tests

```powershell
pytest
```

[^1]: https://deepwiki.com/xteve-project/xTeVe/3.1-m3u-playlist-management

