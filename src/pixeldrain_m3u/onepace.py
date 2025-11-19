"""Scraper for One Pace watch pages."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Sequence

import requests
from bs4 import BeautifulSoup

from .api import compose_download_url, extract_list_id, fetch_list_payload
from .constants import DEFAULT_ONEPACE_WATCH_URL, DEFAULT_SERIES_GROUP, DEFAULT_SERIES_NAME
from .log_utils import log
from .playlist import PlaylistEntry


QUALITY_PATTERN = re.compile(r"(\d{3,4})p")


@dataclass(frozen=True)
class OnePaceLink:
    """Represents a Pixeldrain link exposed on the One Pace site."""

    label: str
    href: str


@dataclass(frozen=True)
class OnePaceArc:
    """Structured data for a One Pace arc entry."""

    title: str
    description: str | None
    english_subtitles: Sequence[OnePaceLink]


def fetch_watch_page(url: str = DEFAULT_ONEPACE_WATCH_URL) -> str:
    """Retrieve the One Pace watch page HTML."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.text


def parse_watch_page(html: str) -> List[OnePaceArc]:
    """Parse One Pace HTML into structured arc data."""
    soup = BeautifulSoup(html, "html.parser")
    arcs: List[OnePaceArc] = []
    for arc_li in soup.select("main ol > li"):
        heading = arc_li.find("h2")
        if not heading:
            continue
        title = heading.get_text(" ", strip=True)
        description = None
        description_candidate = heading.find_next("p")
        if description_candidate and description_candidate.parent is heading.parent:
            description = description_candidate.get_text(" ", strip=True)

        english_links = _extract_english_subtitles(arc_li)
        arcs.append(OnePaceArc(title=title, description=description, english_subtitles=english_links))
    return arcs


def _extract_english_subtitles(arc_li) -> List[OnePaceLink]:
    languages_container = arc_li.find("ul", class_=lambda c: c and "space-y-6" in c)
    if not languages_container:
        return []

    for language_li in languages_container.find_all("li", recursive=False):
        label_block = language_li.find("span")
        if not label_block:
            continue
        label_text = label_block.get_text(" ", strip=True)
        if "English Subtitles" not in label_text:
            continue
        link_ul = language_li.find("ul", class_=lambda c: c and "flex" in c)
        if not link_ul:
            continue
        links: List[OnePaceLink] = []
        for anchor in link_ul.find_all("a", href=True):
            href = anchor["href"]
            if "pixeldrain.net" not in href:
                continue
            label = anchor.get_text(" ", strip=True)
            links.append(OnePaceLink(label=label, href=href))
        return links
    return []


def select_best_quality(links: Sequence[OnePaceLink]) -> OnePaceLink | None:
    """Pick the highest resolution available link."""
    if not links:
        return None

    def score(link: OnePaceLink) -> tuple[int, str]:
        match = QUALITY_PATTERN.search(link.label)
        numeric = int(match.group(1)) if match else 0
        return (numeric, link.label)

    return max(links, key=score)


def arc_matches_filters(title: str, filters: Sequence[str] | None) -> bool:
    if not filters:
        return True
    lower_title = title.lower()
    return any(filt.lower() in lower_title for filt in filters)


def build_onepace_entries(
    *,
    watch_url: str | None,
    base_url: str,
    arc_filters: Sequence[str] | None = None,
    series_name: str | None = None,
    series_group: str | None = None,
    series_logo: str | None = None,
    tvg_prefix: str | None = None,
) -> list[PlaylistEntry]:
    """Fetch arcs from One Pace and convert them into playlist entries."""
    resolved_watch_url = (watch_url or DEFAULT_ONEPACE_WATCH_URL).strip() or DEFAULT_ONEPACE_WATCH_URL
    html = fetch_watch_page(resolved_watch_url)
    arcs = parse_watch_page(html)
    entries: list[PlaylistEntry] = []
    series_prefix = (series_name or DEFAULT_SERIES_NAME).strip()
    normalized_group_title = (series_group or DEFAULT_SERIES_GROUP).strip() or DEFAULT_SERIES_GROUP

    for season_index, arc in enumerate(arcs, start=1):
        if not arc_matches_filters(arc.title, arc_filters):
            continue
        best_link = select_best_quality(arc.english_subtitles)
        if not best_link:
            log(f"Skipping arc '{arc.title}' (no English subtitle links found)")
            continue

        list_id = extract_list_id(best_link.href)
        payload = fetch_list_payload(list_id, base_url)
        files = payload.get("files") or []
        if not files:
            log(f"Skipping arc '{arc.title}' (Pixeldrain list '{list_id}' empty)")
            continue

        for episode_index, file_info in enumerate(files, start=1):
            file_name = file_info.get("name") or file_info.get("id")
            if not file_name:
                continue
            url = compose_download_url(file_info["id"], base_url)
            entry_title, attrs = format_series_metadata(
                series_prefix=series_prefix,
                group_title=normalized_group_title,
                tvg_logo=series_logo,
                tvg_prefix=tvg_prefix,
                arc_title=arc.title,
                season_index=season_index,
                episode_index=episode_index,
            )
            entries.append(PlaylistEntry(title=entry_title, url=url, attrs=attrs))

    if not entries:
        raise RuntimeError("No playable entries were discovered from One Pace.")
    return entries


def format_series_metadata(
    *,
    series_prefix: str,
    group_title: str,
    tvg_logo: str | None,
    tvg_prefix: str | None,
    arc_title: str,
    season_index: int,  # kept for potential future numbering logic
    episode_index: int,
) -> tuple[str, dict[str, str]]:
    """Create IPTV-friendly metadata for a playlist entry."""
    episode_label = f"E{episode_index:02d}"
    display_title = f"{arc_title} {episode_label}"
    if series_prefix:
        display_title = f"{series_prefix} {display_title}"
    attrs: dict[str, str] = {
        "group-title": group_title,
        "tvg-name": display_title,
    }
    if tvg_logo:
        attrs["tvg-logo"] = tvg_logo
    if tvg_prefix is not None:
        attrs["tvg-id"] = f"{tvg_prefix}{episode_label}"
    return display_title, attrs

