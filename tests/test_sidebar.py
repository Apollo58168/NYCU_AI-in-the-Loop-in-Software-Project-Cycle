from streamlit.testing.v1 import AppTest

from decisiontrace import store


def _app(tmp_path, monkeypatch):
    path = tmp_path / "cards.json"
    monkeypatch.setattr(store, "DEFAULT_PATH", path)
    return AppTest.from_file("../app/main.py").run(), path


def test_load_sample_data_saves_six_cards(tmp_path, monkeypatch):
    at, path = _app(tmp_path, monkeypatch)
    at.sidebar.button(key="sidebar_load_sample").click().run()
    assert not at.exception
    statuses = sorted(c.status for c in store.load(path))
    assert statuses == ["approved"] * 4 + ["draft", "rejected"]


def test_reset_needs_confirmation_then_empties_the_store(tmp_path, monkeypatch):
    at, path = _app(tmp_path, monkeypatch)
    at.sidebar.button(key="sidebar_load_sample").click().run()
    assert at.sidebar.button(key="sidebar_reset").disabled
    at.sidebar.checkbox(key="sidebar_confirm_reset").check().run()
    at.sidebar.button(key="sidebar_reset").click().run()
    assert not at.exception
    assert store.load(path) == []
