from pixeldrain_m3u.playlist import render_m3u


def test_render_m3u_generates_valid_extinf_entries():
    files = [
        {"id": "abc123", "name": "Episode 1", "duration": 120},
        {"id": "def456", "name": "Episode 2"},
    ]
    content = render_m3u(files, "https://pixeldrain.net", "Test List")

    assert content.startswith("#EXTM3U")
    assert "Episode 1" in content
    assert "Episode 2" in content
    assert content.count("#EXTINF") == 2

