from decisiontrace import store
from decisiontrace.cards import Card


def make_card(decision: str) -> Card:
    return Card(
        decision=decision,
        reason="unknown",
        verbatim_quote="unknown",
        alternatives=[],
        confidence="low",
        source="pasted text",
        author="alice",
        drafted_by="test",
    )


def test_missing_file_means_no_cards(tmp_path):
    assert store.load(tmp_path / "cards.json") == []


def test_save_and_load_round_trip_keeps_chinese(tmp_path):
    path = tmp_path / "data" / "cards.json"
    cards = [make_card("改用 polling"), make_card("Use uv")]
    store.save(cards, path)
    assert store.load(path) == cards
    assert "改用" in path.read_text(encoding="utf-8")


def test_upsert_adds_then_replaces(tmp_path):
    path = tmp_path / "cards.json"
    card = make_card("Use polling")
    store.upsert(card, path)
    card.status = "approved"
    store.upsert(card, path)
    loaded = store.load(path)
    assert len(loaded) == 1
    assert loaded[0].status == "approved"
