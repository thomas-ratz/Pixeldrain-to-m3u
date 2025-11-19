"""Playlist rendering helpers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence

from .log_utils import log


@dataclass(frozen=True)
class PlaylistEntry:
    """Represents a single EXTINF + URL pair."""

    title: str
    url: str
    duration: int = -1
    attrs: Mapping[str, str] | None = None


def render_playlist(entries: Sequence[PlaylistEntry], title: str | None = None) -> str:
    """Render an M3U playlist from structured entries."""
    if not entries:
        raise ValueError("Cannot render a playlist with zero entries")

    lines: list[str] = ["#EXTM3U"]
    if title:
        lines.append(f"# Playlist: {title}")

    for entry in entries:
        attr_text = ""
        if entry.attrs:
            formatted: list[str] = []
            for key, value in sorted(entry.attrs.items()):
                if value is None:
                    continue
                safe_value = str(value).replace('"', "'")
                formatted.append(f'{key}="{safe_value}"')
            attr_text = " " + " ".join(formatted)
        lines.append(f"#EXTINF:{entry.duration}{attr_text},{entry.title}")
        lines.append(entry.url)

    return "\n".join(lines) + "\n"


def write_playlist(content: str, destination: Path, overwrite: bool) -> Path:
    """Write the playlist to disk and return the path."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and not overwrite:
        raise FileExistsError(f"{destination} already exists. Use --overwrite to replace it.")

    destination.write_text(content, encoding="utf-8")
    log(f"Playlist written to {destination.resolve()}")
    return destination

