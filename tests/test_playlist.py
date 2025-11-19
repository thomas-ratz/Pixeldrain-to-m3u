from pixeldrain_m3u.playlist import PlaylistEntry, render_playlist


def test_render_playlist_formats_attributes_and_titles():
    entries = [
        PlaylistEntry(
            title="Arc • Episode 1",
            url="https://example.com/1",
            attrs={"tvg-name": 'Episode "1"', "group-title": "Arc"},
        ),
        PlaylistEntry(title="Arc • Episode 2", url="https://example.com/2"),
    ]

    content = render_playlist(entries, "Test List")

    assert content.startswith("#EXTM3U")
    assert '#EXTINF:-1 group-title="Arc" tvg-name="Episode \'1\'",Arc • Episode 1' in content
    assert content.count("#EXTINF") == 2

