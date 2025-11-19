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
