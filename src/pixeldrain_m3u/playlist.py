"""Playlist rendering helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

from .api import compose_download_url
from .log_utils import log


def render_m3u(files: Sequence[dict], base_url: str, title: str | None = None) -> str:
    """Generate M3U content for the provided files."""
    if not files:
        raise ValueError("Cannot render a playlist for an empty file list")

    lines: list[str] = ["#EXTM3U"]
    if title:
        lines.append(f"# Pixeldrain List: {title}")

    for index, file_info in enumerate(files, start=1):
        file_name = file_info.get("name") or f"Pixeldrain File {index}"
        download_url = compose_download_url(file_info["id"], base_url)
        duration = file_info.get("duration", -1)
        lines.append(f"#EXTINF:{duration},{file_name}")
        lines.append(download_url)

    return "\n".join(lines) + "\n"


def write_playlist(content: str, destination: Path, overwrite: bool) -> Path:
    """Write the playlist to disk and return the path."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and not overwrite:
        raise FileExistsError(f"{destination} already exists. Use --overwrite to replace it.")

    destination.write_text(content, encoding="utf-8")
    log(f"Playlist written to {destination.resolve()}")
    return destination

