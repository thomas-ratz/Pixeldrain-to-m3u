"""HTTP and Pixeldrain API helpers."""

from __future__ import annotations

import os
from typing import Any, Dict
from urllib.parse import urlparse

import requests

from .constants import DEFAULT_BASE_URL
from .log_utils import log


def normalize_base_url(url: str | None) -> str:
    """Ensure the base URL is well-formed and without a trailing slash."""
    base = (url or os.getenv("PIXELDRAIN_BASE_URL") or DEFAULT_BASE_URL).strip()
    if not base:
        raise ValueError("Pixeldrain base URL cannot be empty")
    return base.rstrip("/")


def extract_list_id(source: str) -> str:
    """Pull the list ID from either a raw ID or a Pixeldrain share URL."""
    candidate = (source or "").strip()
    if not candidate:
        raise ValueError("List identifier cannot be blank")

    parsed = urlparse(candidate)
    if parsed.scheme:
        segments = [seg for seg in parsed.path.split("/") if seg]
        for idx, segment in enumerate(segments):
            if segment.lower() in {"l", "list"} and idx + 1 < len(segments):
                return segments[idx + 1]
        if segments:
            return segments[-1]
        raise ValueError(f"Unable to derive list id from URL: {candidate}")

    return candidate


def fetch_list_payload(list_id: str, base_url: str) -> Dict[str, Any]:
    """Retrieve Pixeldrain list metadata."""
    url = f"{base_url}/api/list/{list_id}"
    log(f"Requesting list metadata from {url}")
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    payload = response.json()
    if not payload.get("success"):
        raise RuntimeError(f"Pixeldrain returned unsuccessful response for list '{list_id}'")
    return payload


def compose_download_url(file_id: str, base_url: str) -> str:
    """Build a direct download URL for a Pixeldrain file."""
    if not file_id:
        raise ValueError("file_id cannot be empty")
    return f"{base_url}/api/file/{file_id}?download"

