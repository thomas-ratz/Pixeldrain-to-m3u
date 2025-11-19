from pixeldrain_m3u.onepace import (
    OnePaceLink,
    format_series_metadata,
    parse_watch_page,
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


def test_format_series_metadata_builds_tvg_fields():
    title, attrs = format_series_metadata(
        series_prefix="",
        group_title="One Pace",
        tvg_logo="http://logo.png",
        tvg_prefix="onepace-",
        arc_title="Romance Dawn",
        season_index=1,
        episode_index=3,
    )

    assert title == "Romance Dawn E03"
    assert attrs["group-title"] == "One Pace"
    assert attrs["tvg-name"] == "Romance Dawn E03"
    assert attrs["tvg-logo"] == "http://logo.png"
    assert attrs["tvg-id"] == "onepace-E03"


def test_format_series_metadata_allows_prefix():
    title, attrs = format_series_metadata(
        series_prefix="Custom",
        group_title="Custom Group",
        tvg_logo=None,
        tvg_prefix=None,
        arc_title="Arc",
        season_index=2,
        episode_index=1,
    )

    assert title == "Custom Arc E01"
    assert attrs["tvg-name"] == "Custom Arc E01"
    assert attrs["group-title"] == "Custom Group"

