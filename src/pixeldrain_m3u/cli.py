"""Command-line interface for the Pixeldrain playlist builder."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from .api import extract_list_id, fetch_list_payload, normalize_base_url
from .log_utils import log
from .playlist import render_m3u, write_playlist


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Scrape Pixeldrain list content and build an M3U playlist."
    )
    parser.add_argument(
        "source",
        help="Pixeldrain list URL or ID (e.g., https://pixeldrain.net/l/XXXXXXXX or XXXXXXXX)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="playlist.m3u",
        help="Destination path for the generated playlist (default: %(default)s).",
    )
    parser.add_argument(
        "--base-url",
        dest="base_url",
        default=None,
        help="Override the Pixeldrain base URL (defaults to PIXELDRAIN_BASE_URL env or official domain).",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite the output file if it already exists.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv or sys.argv[1:])
    try:
        base_url = normalize_base_url(args.base_url)
        list_id = extract_list_id(args.source)
        payload = fetch_list_payload(list_id, base_url)
        files = payload.get("files") or []
        if not files:
            raise RuntimeError(f"No files were found in Pixeldrain list '{list_id}'.")
        playlist_title = payload.get("title")
        playlist_content = render_m3u(files, base_url, playlist_title)
        destination = Path(args.output)
        write_playlist(playlist_content, destination, args.overwrite)
        log(f"Processed {len(files)} files from list '{list_id}'.")
        return 0
    except Exception as exc:  # pylint: disable=broad-except
        log(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

