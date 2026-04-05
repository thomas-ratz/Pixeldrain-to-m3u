from pixeldrain_m3u.onepace import (
    OnePaceLink,
    build_onepace_entries,
    format_arc_episode_metadata,
    parse_watch_page,
    sanitize_arc_filename,
    select_best_quality,
)

SAMPLE_HTML = """
<html>
  <body>
    <main>
      <ol>
        <li>
          <div>
            <h2>Romance Dawn</h2>
            <ul class="mx-auto max-w-3xl space-y-6 p-6 sm:space-y-2">
              <li>
                <span class="flex gap-x-2 font-semibold">
                  <span class="flex-1">English Subtitles</span>
                </span>
                <ul class="flex flex-col items-end gap-2 sm:flex-row">
                  <li><a href="https://pixeldrain.net/l/AAA">Pixeldrain:480p</a></li>
                  <li><a href="https://pixeldrain.net/l/BBB">Pixeldrain:1080p</a></li>
                </ul>
              </li>
              <li>
                <span class="flex gap-x-2 font-semibold">
                  <span class="flex-1">English Dub</span>
                </span>
              </li>
            </ul>
          </div>
        </li>
      </ol>
    </main>
  </body>
</html>
"""


def test_parse_watch_page_extracts_english_links():
    arcs = parse_watch_page(SAMPLE_HTML)
    assert len(arcs) == 1
    arc = arcs[0]
    assert arc.title == "Romance Dawn"
    assert len(arc.english_subtitles) == 2
    assert arc.english_subtitles[1].href.endswith("BBB")


def test_select_best_quality_prefers_highest_resolution():
    links = [
        OnePaceLink(label="Pixeldrain:480p", href="https://pixeldrain.net/l/AAA"),
        OnePaceLink(label="Pixeldrain:720p", href="https://pixeldrain.net/l/BBB"),
        OnePaceLink(label="Pixeldrain:1080p", href="https://pixeldrain.net/l/CCC"),
    ]

    best = select_best_quality(links)

    assert best is not None
    assert best.href.endswith("CCC")


def test_format_arc_episode_metadata_builds_tvg_fields():
    title, attrs = format_arc_episode_metadata(
        arc_title="Romance Dawn",
        group_title="Romance Dawn",
        tvg_logo="http://logo.png",
        tvg_prefix="onepace-",
        episode_index=3,
        series_prefix="One Pace",
    )

    assert title == "One Pace Romance Dawn E03"
    assert attrs["group-title"] == "Romance Dawn"
    assert attrs["tvg-name"] == "One Pace Romance Dawn E03"
    assert attrs["tvg-logo"] == "http://logo.png"
    assert attrs["tvg-id"] == "onepace-romance-dawn-E03"


def test_format_arc_episode_metadata_without_prefix():
    title, attrs = format_arc_episode_metadata(
        arc_title="Romance Dawn",
        group_title="Romance Dawn",
        tvg_logo=None,
        tvg_prefix=None,
        episode_index=1,
        series_prefix="",
    )

    assert title == "Romance Dawn E01"
    assert attrs["tvg-name"] == "Romance Dawn E01"
    assert attrs["group-title"] == "Romance Dawn"
    assert attrs["tvg-id"] == ""


def test_sanitize_arc_filename_strips_invalid_chars():
    assert sanitize_arc_filename('A/B:C', ".m3u") == "A_B_C.m3u"


def test_build_onepace_entries_sets_group_title_per_arc(monkeypatch):
    monkeypatch.setattr(
        "pixeldrain_m3u.onepace.fetch_watch_page",
        lambda _url: SAMPLE_HTML,
    )
    monkeypatch.setattr(
        "pixeldrain_m3u.onepace.fetch_list_payload",
        lambda _list_id, _base: {
            "files": [
                {"id": "f1", "name": "a.mkv"},
                {"id": "f2", "name": "b.mkv"},
            ]
        },
    )

    entries = build_onepace_entries(
        watch_url="https://example.invalid/watch",
        base_url="https://pixeldrain.net",
    )

    assert len(entries) == 2
    assert entries[0].title == "Romance Dawn E01"
    assert entries[0].attrs is not None
    assert entries[0].attrs["group-title"] == "Romance Dawn"
    assert "f1" in entries[0].url

