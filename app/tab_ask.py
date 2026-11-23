"""Ask tab (module C): answer a question from approved cards only."""

import streamlit as st

from decisiontrace import store
from decisiontrace.ask import answer


def render() -> None:
    st.subheader("Ask about a past decision")
    st.caption("Answers come only from cards a teammate has approved.")

    question = st.text_input("Your question", key="ask_question")
    if not st.button("Ask", key="ask_button"):
        return

    try:
        cards = store.load(store.DEFAULT_PATH)
    except Exception as exc:  # a broken data file must not crash the page
        st.error(f"Could not read the saved cards: {exc}")
        return

    try:
        result = answer(question, cards)
    except ValueError as exc:
        st.error(str(exc))
        return

    st.markdown(result.text)
    by_id = {c.id: c for c in cards}
    for card_id in result.card_ids:
        card = by_id[card_id]
        with st.container(border=True):
            st.markdown("**Source card**")
            st.markdown(f"**Decision:** {card.decision}")
            st.markdown(f"**Reason:** {card.reason}")
            st.markdown(f"**Quote:** {card.verbatim_quote}")
            if card.alternatives:
                st.markdown(f"**Alternatives:** {', '.join(card.alternatives)}")
            st.caption(
                f"Card {card.id} · written by {card.author} · "
                f"drafted by {card.drafted_by} · approved by {card.reviewer}"
            )
