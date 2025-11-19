"""Playlist rendering helpers."""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence

from .log_utils import log

PREFERRED_ATTR_ORDER = (
    "tvg-id",
    "tvg-name",
    "tvg-logo",
    "group-title",
)


@dataclass(frozen=True)
class PlaylistEntry:
    """Represents a single playlist entry."""

    title: str
    url: str
    duration: int = -1
    attrs: Mapping[str, str] | None = None


def render_m3_playlist(entries: Sequence[PlaylistEntry], title: str | None = None) -> str:
    """Render an extended M3U playlist."""
    if not entries:
        raise ValueError("Cannot render a playlist with zero entries")

    lines: list[str] = ["#EXTM3U"]
    if title:
        lines.append(f"# Playlist: {title}")

    for entry in entries:
        attr_text = ""
        if entry.attrs:
            formatted: list[str] = []
            ordered_items = _order_attributes(entry.attrs)
            for key, value in ordered_items:
                safe_value = str(value).replace('"', "'")
                formatted.append(f'{key}="{safe_value}"')
            attr_text = " " + " ".join(formatted)
        duration = entry.duration if entry.duration >= 0 else -1
        lines.append(f"#EXTINF:{duration}{attr_text},{entry.title}")
        lines.append(entry.url)

    return "\n".join(lines) + "\n"


def render_m3u8_playlist(entries: Sequence[PlaylistEntry], title: str | None = None) -> str:
    """Render a simple VOD HLS playlist."""
    if not entries:
        raise ValueError("Cannot render a playlist with zero entries")

    durations = [_coerce_duration(entry.duration) for entry in entries]
    target_duration = max(durations) if durations else 1

    lines: list[str] = [
        "#EXTM3U",
        "#EXT-X-VERSION:3",
        "#EXT-X-MEDIA-SEQUENCE:0",
        "#EXT-X-PLAYLIST-TYPE:VOD",
        f"#EXT-X-TARGETDURATION:{target_duration}",
    ]
    if title:
        lines.append(f"#EXT-X-SESSION-DATA:DATA-ID=\"com.onepace.title\",VALUE=\"{title}\"")

    for idx, (entry, duration) in enumerate(zip(entries, durations)):
        lines.extend(_render_m3u8_entry(entry, duration, idx))

    lines.append("#EXT-X-ENDLIST")
    return "\n".join(lines) + "\n"


def write_playlist(content: str, destination: Path, overwrite: bool) -> Path:
    """Write the playlist to disk and return the path."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and not overwrite:
        raise FileExistsError(f"{destination} already exists. Use --overwrite to replace it.")

    destination.write_text(content, encoding="utf-8")
    log(f"Playlist written to {destination.resolve()}")
    return destination


def _order_attributes(attrs: Mapping[str, str | None]) -> list[tuple[str, str]]:
    ordered: list[tuple[str, str]] = []
    used = set()
    for key in PREFERRED_ATTR_ORDER:
        if key in attrs and attrs[key] is not None:
            ordered.append((key, attrs[key]))
            used.add(key)
    for key, value in attrs.items():
        if key in used or value is None:
            continue
        ordered.append((key, value))
    return ordered


def _render_m3u8_entry(entry: PlaylistEntry, duration: int, index: int) -> list[str]:
    title = entry.title
    attrs = entry.attrs or {}
    group = attrs.get("group-title", "")
    tvg_id = attrs.get("tvg-id", f"entry-{index}")
    tvg_logo = attrs.get("tvg-logo", "")
    lines = [
        f"#EXTINF:{duration},{title}",
        _build_daterange_tag(
            entry_id=tvg_id or f"entry-{index}",
            group=group or "One Pace",
            title=title,
            logo=tvg_logo,
            sequence=index,
        ),
        entry.url,
    ]
    return lines


def _coerce_duration(value: int) -> int:
    if value and value > 0:
        return int(math.ceil(value))
    return 1


def _build_daterange_tag(*, entry_id: str, group: str, title: str, logo: str, sequence: int) -> str:
    start_seconds = sequence
    start_date = f"1970-01-01T00:00:{start_seconds:02d}Z"
    parts = [
        f'ID="{entry_id}"',
        f'CLASS="{group or "One Pace"}"',
        f'START-DATE="{start_date}"',
        'END-ON-NEXT=YES',
        f'X-TITLE="{title}"',
    ]
    if logo:
        parts.append(f'X-TVG-LOGO="{logo}"')
    return "#EXT-X-DATERANGE:" + ",".join(parts)

