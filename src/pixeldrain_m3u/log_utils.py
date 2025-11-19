"""Custom logging utilities honoring the user's preferred format."""

from __future__ import annotations

from .constants import SYSTEM_NAME


def log(message: str) -> None:
    """Emit a log entry to stdout."""
    print(f"[{SYSTEM_NAME}]:{message}")

