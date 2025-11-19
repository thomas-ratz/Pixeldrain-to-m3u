from pixeldrain_m3u.playlist import PlaylistEntry, render_m3_playlist, render_m3u8_playlist


def test_render_playlist_formats_attributes_and_titles():
    entries = [
        PlaylistEntry(
            title="Arc • Episode 1",
            url="https://example.com/1",
            attrs={"tvg-name": 'Episode "1"', "group-title": "Arc"},
        ),
        PlaylistEntry(title="Arc • Episode 2", url="https://example.com/2"),
    ]

    content = render_m3_playlist(entries, "Test List")

    assert content.startswith("#EXTM3U")
    assert '#EXTINF:-1 tvg-name="Episode \'1\'" group-title="Arc",Arc • Episode 1' in content
    assert content.count("#EXTINF") == 2


def test_render_m3u8_playlist_emits_required_tags():
    entries = [
        PlaylistEntry(title="Episode 1", url="https://example.com/1", attrs={"group-title": "Arc"}),
    ]

    content = render_m3u8_playlist(entries, "Arc Playlist")

    assert "#EXT-X-VERSION:3" in content
    assert "#EXT-X-TARGETDURATION" in content
    assert "#EXTINF:1,Episode 1" in content
    assert "#EXT-X-DATERANGE:" in content
    assert content.strip().endswith("#EXT-X-ENDLIST")

