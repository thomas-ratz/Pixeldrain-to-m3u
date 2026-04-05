# Pixeldrain Playlist Scraper

Automate the creation of an `m3u` playlist from a Pixeldrain share link. The package fetches list metadata via Pixeldrain's public API and emits a standards-compliant playlist that any compatible media player can stream [^1].

## Project Layout

```
.
├─ src/pixeldrain_m3u/   # Package code (API helpers, playlist utils, CLI)
├─ tests/                # Pytest suite
├─ output/               # Generated playlists (git-ignored)
├─ README.md             # This file
├─ DEV_PASS.md           # Development pass journal
├─ pyproject.toml        # Project metadata & dependencies
├─ requirements.txt      # Shorthand: installs the package in editable mode
└─ requirements-dev.txt  # Shorthand: installs with dev/test extras
```

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .          # runtime
pip install -e ".[dev]"   # optional: dev/test tooling (pytest)
```

## Usage

### Single Pixeldrain list

```powershell
python -m pixeldrain_m3u https://pixeldrain.net/l/VmpS467P -o output/romance_dawn.m3u
# or, once installed:
pixeldrain-m3u VmpS467P --overwrite
```

### One Pace auto-scrape

One combined playlist is written. Each episode’s **IPTV `group-title`** is the scraped arc name from the watch page (for example `Romance Dawn`), so apps that group by `group-title` show arcs as separate series or folders. Episode display names look like `Romance Dawn E01` (or `One Pace Romance Dawn E01` if you set `--series-name`).

```powershell
# Default output: output/onepace.m3u
python -m pixeldrain_m3u --onepace https://onepace.net/en/watch --mode m3u --overwrite

# Limit to arcs whose titles contain "Wano" or "Dressrosa"
pixeldrain-m3u --onepace --arc-filter Wano --arc-filter Dressrosa --mode m3u8 -o output/favorites.m3u8 --overwrite
```

Key flags:

- `--output`: defaults to `output/playlist.m3u`, or `output/onepace.m3u` with `--onepace`
- `--base-url`: point at a Pixeldrain mirror or self-host
- `--overwrite`: replace an existing playlist file
- `--onepace`: interpret `source` as a One Pace watch page (or omit to use the default page)
- `--arc-filter`: repeatable filter that keeps arcs whose title contains the provided text
- `--mode`: `m3u` (default) for extended M3U, `m3u8` for a VOD-style HLS manifest
- `--series-name`: optional prefix for episode display names (default empty; e.g. `One Pace` → `One Pace Romance Dawn E01`)
- `--series-group`: force the same IPTV `group-title` on every arc (default: each arc’s scraped title)
- `--series-logo`: override the default One Piece logo used for `tvg-logo`
- `--tvg-prefix`: assign deterministic `tvg-id`s, e.g. `--tvg-prefix onepace-`

You can pass a raw list ID instead of a full Pixeldrain URL, and the CLI honors `PIXELDRAIN_BASE_URL` so you can globally override the domain. In One Pace mode, the overall playlist title stays **One Pace – English Subtitles**; per-line metadata uses the arc name in `group-title` and `tvg-name` so players and IPTV tools can split the library by arc. The default One Piece image is used for `tvg-logo` unless you pass `--series-logo`.

**Xtream Codes / IPTV panels:** this tool outputs a static M3U/M3U8 file, not the Xtream Codes HTTP API (`player_api.php`). Many apps read M3U VOD lines and use `group-title` as the category or series name—host the generated file over HTTP(S) and add that URL as an M3U source, or import the M3U into a panel that maps groups to VOD categories. Full Xtream-style VOD listing requires panel software that exposes that API.

## Tests

```powershell
pytest
```

[^1]: https://deepwiki.com/xteve-project/xTeVe/3.1-m3u-playlist-management

