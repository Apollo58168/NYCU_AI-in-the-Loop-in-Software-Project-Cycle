from decisiontrace.cards import UNKNOWN, Card, check_quote

SOURCE = "We decided to use polling. Because WebSockets kept dropping behind the proxy."


def make_card(quote: str) -> Card:
    return Card(
        decision="Use polling",
        reason="WebSockets dropped behind the proxy",
        verbatim_quote=quote,
        alternatives=["WebSockets"],
        confidence="high",
        source="pasted text",
        author="alice",
        drafted_by="test",
    )


def test_exact_quote_is_kept():
    card = check_quote(make_card("WebSockets kept dropping behind the proxy"), SOURCE)
    assert card.verbatim_quote == "WebSockets kept dropping behind the proxy"
    assert card.confidence == "high"
    assert card.warnings == []


def test_invented_quote_is_replaced_with_unknown():
    card = check_quote(make_card("The TA told us to use polling"), SOURCE)
    assert card.verbatim_quote == UNKNOWN
    assert card.confidence == "low"
    assert len(card.warnings) == 1


def test_paraphrased_quote_is_replaced():
    card = check_quote(make_card("websockets kept dropping behind the proxy"), SOURCE)
    assert card.verbatim_quote == UNKNOWN


def test_empty_quote_becomes_unknown():
    card = check_quote(make_card("   "), SOURCE)
    assert card.verbatim_quote == UNKNOWN


def test_unknown_quote_stays_unknown_without_warning():
    card = check_quote(make_card(UNKNOWN), SOURCE)
    assert card.verbatim_quote == UNKNOWN
    assert card.warnings == []


def test_round_trip_through_dict():
    card = make_card("x")
    assert Card.from_dict(card.to_dict()) == card
