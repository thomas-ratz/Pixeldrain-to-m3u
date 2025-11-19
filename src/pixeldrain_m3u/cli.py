"""Command-line interface for the Pixeldrain playlist builder."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from .api import compose_download_url, extract_list_id, fetch_list_payload, normalize_base_url
from .constants import DEFAULT_SERIES_GROUP, DEFAULT_SERIES_NAME
from .log_utils import log
from .onepace import build_onepace_entries
from .playlist import PlaylistEntry, render_m3_playlist, render_m3u8_playlist, write_playlist


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Scrape Pixeldrain list content and build an M3U playlist."
    )
    parser.add_argument(
        "source",
        nargs="?",
        help=(
            "Pixeldrain list URL/ID or (when --onepace) the One Pace watch URL "
            "(default: One Pace English watch page)."
        ),
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
    parser.add_argument(
        "--onepace",
        action="store_true",
        help="Scrape the One Pace watch page for arcs and build a combined playlist.",
    )
    parser.add_argument(
        "--arc-filter",
        dest="arc_filters",
        action="append",
        help="(One Pace only) include arcs whose title contains this substring. Repeatable.",
    )
    parser.add_argument(
        "--mode",
        choices=("m3u", "m3u8"),
        default="m3u",
        help="Output playlist format (default: %(default)s).",
    )
    parser.add_argument(
        "--series-name",
        default=DEFAULT_SERIES_NAME,
        help="(One Pace only) optional prefix prepended to each episode title.",
    )
    parser.add_argument(
        "--series-group",
        default=DEFAULT_SERIES_GROUP,
        help="(One Pace only) override the IPTV group-title value (default: %(default)s).",
    )
    parser.add_argument(
        "--series-logo",
        default=None,
        help="(One Pace only) optional logo URL injected as tvg-logo.",
    )
    parser.add_argument(
        "--tvg-prefix",
        default=None,
        help="(One Pace only) optional prefix for tvg-id (e.g., 'onepace-').",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv or sys.argv[1:])
    try:
        base_url = normalize_base_url(args.base_url)
        if args.onepace:
            entries = build_onepace_entries(
                watch_url=args.source,
                base_url=base_url,
                arc_filters=args.arc_filters,
                series_name=args.series_name,
                series_group=args.series_group,
                series_logo=args.series_logo,
                tvg_prefix=args.tvg_prefix,
            )
            playlist_title = "One Pace – English Subtitles"
        else:
            if not args.source:
                parser.error("source is required unless --onepace is supplied.")
            list_id = extract_list_id(args.source)
            payload = fetch_list_payload(list_id, base_url)
            files = payload.get("files") or []
            if not files:
                raise RuntimeError(f"No files were found in Pixeldrain list '{list_id}'.")
            playlist_title = payload.get("title")
            entries = [
                PlaylistEntry(
                    title=file_info.get("name") or file_info["id"],
                    url=compose_download_url(file_info["id"], base_url),
                    duration=file_info.get("duration", -1),
                )
                for file_info in files
            ]

        if args.mode == "m3u8":
            playlist_content = render_m3u8_playlist(entries, playlist_title)
        else:
            playlist_content = render_m3_playlist(entries, playlist_title)
        destination = Path(args.output)
        write_playlist(playlist_content, destination, args.overwrite)
        log(f"Playlist created with {len(entries)} entries.")
        return 0
    except Exception as exc:  # pylint: disable=broad-except
        log(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

