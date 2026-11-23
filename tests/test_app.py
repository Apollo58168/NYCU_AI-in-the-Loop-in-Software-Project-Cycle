from streamlit.testing.v1 import AppTest


def test_app_starts_with_four_tabs():
    at = AppTest.from_file("../app/main.py").run()
    assert not at.exception
    assert [t.label for t in at.tabs] == ["Draft", "Review", "Ask", "Approved cards"]
