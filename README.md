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

```powershell
# Via module invocation
python -m pixeldrain_m3u https://pixeldrain.net/l/VmpS467P -o romance_dawn.m3u

# Or via the console script after installation
pixeldrain-m3u https://pixeldrain.net/l/VmpS467P --overwrite
```

Key flags:

- `--output`: destination file (default `playlist.m3u`)
- `--base-url`: point at a Pixeldrain mirror or self-host
- `--overwrite`: replace an existing playlist file

You can also pass a raw list ID instead of the full URL. The CLI honors `PIXELDRAIN_BASE_URL` so you can globally override the domain.

## Tests

```powershell
pytest
```

[^1]: https://deepwiki.com/xteve-project/xTeVe/3.1-m3u-playlist-management

