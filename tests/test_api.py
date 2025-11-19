from pixeldrain_m3u.api import extract_list_id, normalize_base_url


def test_extract_list_id_accepts_raw_id():
    assert extract_list_id("VmpS467P") == "VmpS467P"


def test_extract_list_id_accepts_url():
    assert extract_list_id("https://pixeldrain.net/l/VmpS467P") == "VmpS467P"


def test_normalize_base_url_trims_trailing_slash(monkeypatch):
    monkeypatch.delenv("PIXELDRAIN_BASE_URL", raising=False)
    assert normalize_base_url("https://pixeldrain.net/") == "https://pixeldrain.net"

