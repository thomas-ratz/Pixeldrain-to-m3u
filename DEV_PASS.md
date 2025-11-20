# Development Pass Log

## Pass 1 – 2025-11-19

### Completed
- Initialized Python project scaffold (venv, `requirements.txt`)
- Implemented `pixeldrain_m3u.py` CLI scraper with configurable base URL and logging
- Documented setup and usage in `README.md`

### In Progress
- N/A

### Not Started / Future Work
- Automated tests for different Pixeldrain list shapes
- Packaging for distribution (e.g., `pyproject.toml`, `pipx` support)
- Optional metadata enrichment (durations, thumbnails, etc.)

### Next Pass Goals
- Backfill automated tests exercising the HTTP layer via fixtures/mocks
- Evaluate need for retry/backoff when Pixeldrain throttles requests

## Pass 2 – 2025-11-19

### Completed
- Restructured project into a `src/` package with dedicated API, playlist, and CLI modules
- Added project metadata (`pyproject.toml`), editable install, and optional dev dependencies
- Created pytest smoke tests plus `.gitignore`, updated README, and maintained DEV_PASS log

### In Progress
- None

### Not Started / Future Work
- HTTP-layer integration tests with mocked Pixeldrain responses
- Retry/backoff strategy for network hiccups
- Packaging/publishing automation (GitHub Actions, release workflows)

### Next Pass Goals
- Expand test coverage (API error handling, CLI argument parsing)
- Add configurable logging levels and optional structured logs

## Pass 3 – 2025-11-19

### Completed
- Implemented One Pace scraper that selects the highest-quality English subtitle Pixeldrain link per arc
- Added playlist entry struct, IPTV-friendly metadata (group-title/tvg-name), and enhanced CLI flags (`--onepace`, `--arc-filter`)
- Updated README docs, dependency metadata, and expanded pytest coverage (playlist rendering + One Pace parsing)

### In Progress
- None

### Not Started / Future Work
- Network retries/backoff for both One Pace and Pixeldrain HTTP calls
- Local caching of One Pace HTML to reduce load and speed up repeated runs
- CLI UX polish (progress bars, selective arc ranges, JSON export)

### Next Pass Goals
- Add integration tests that stub HTTP responses for One Pace + Pixeldrain
- Introduce retry/session pooling for the scraper clients

## Pass 4 – 2025-11-19

### Completed
- Added series-aware metadata formatting (season/episode numbering, tvg-name/tvg-logo/tvg-id support)
- Introduced CLI overrides for series name/group/logo/tvg-id prefix to mirror IPTV series semantics
- Documented the workflow updates and added new tests covering metadata formatting

### In Progress
- None

### Not Started / Future Work
- Smarter episode number extraction from filenames (beyond sequential ordering)
- Optional per-arc artwork ingestion for `tvg-logo`
- Player-specific playlist exports (e.g., JSON or XMLTV)

### Next Pass Goals
- Capture episode numbering directly from Pixeldrain filenames when available
- Add CLI option to emit multiple playlist files (one per arc/season)

## Pass 5 – 2025-11-19

### Completed
- Added `--mode` flag supporting `m3u` (default) and `m3u8` outputs, plus an HLS renderer that uses tags from the Mux reference (`#EXT-X-VERSION`, `#EXTINF`, `#EXT-X-DATERANGE`, `#EXT-X-ENDLIST`)
- Simplified One Pace naming to `Romance Dawn E01` (no season metadata) so IPTV clients classify entries as series/VOD
- Updated README/tests to reflect the new format and ensured attribute ordering matches common IPTV expectations
- Introduced the default One Piece `tvg-logo` and enforced the exact `Episode Sxx Exx` + `group-title="<Arc> Sxx"` IPTV naming pattern with `tvg-id=""` when no prefix is provided

### In Progress
- None

### Not Started / Future Work
- Investigate deriving durations (for more accurate `#EXTINF`/`#EXT-X-TARGETDURATION`)
- Explore multi-quality variant generation for future adaptive streaming mode
- Consider exporting companion metadata (JSON/XMLTV) for richer clients

### Next Pass Goals
- Integrate actual durations if available (ffprobe or Pixeldrain metadata)
- Add validation to ensure `--mode m3u8` output passes HLS linters
