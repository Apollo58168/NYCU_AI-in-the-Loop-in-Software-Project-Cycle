"""Approved cards tab (module A): the decisions a teammate has approved.

Only approved cards are listed; drafts wait in the Review tab and rejected
cards are never shown as decisions.
"""

import streamlit as st

from decisiontrace import store
from decisiontrace.drafter import MOCK
from decisiontrace.listing import approved_cards


def render() -> None:
    st.subheader("Approved decisions")
    st.caption("Every card here was approved by a teammate who did not write it.")

    try:
        cards = approved_cards(store.load(store.DEFAULT_PATH))
    except Exception as exc:  # a broken data file must not crash the page
        st.error(f"Could not read the saved cards: {exc}")
        return

    if not cards:
        st.info("No approved cards yet.")
        return

    for card in cards:
        with st.container(border=True):
            st.markdown(f"**Decision:** {card.decision}")
            st.markdown(f"**Reason:** {card.reason}")
            st.markdown(f"**Quote:** {card.verbatim_quote}")
            if card.alternatives:
                st.markdown(f"**Alternatives:** {', '.join(card.alternatives)}")
            drafted = "MOCK (not AI)" if card.drafted_by == MOCK else card.drafted_by
            st.caption(
                f"Card {card.id} · written by {card.author} · approved by {card.reviewer} · "
                f"drafted by {drafted} · {card.created_at}"
            )
