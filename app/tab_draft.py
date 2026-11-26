"""Draft tab (module D): draft a decision card from a pasted discussion.

Streamlit reruns this file on every click, so the drafted card is kept in
st.session_state between "Draft card" and "Save as draft". Every card drafted
here is labelled MOCK until module D's second PR connects the Claude API.
"""

import streamlit as st

from decisiontrace import store
from decisiontrace.cards import UNKNOWN
from decisiontrace.drafter import MOCK, draft_card

MOCK_LABEL = "MOCK draft, not AI - needs human review"


def render() -> None:
    st.subheader("Draft a decision card")
    st.caption("Paste one discussion about one decision. A teammate reviews every card.")

    author = st.text_input("Your name (author)", key="draft_author")
    source = st.text_input("Source label", value="pasted text", key="draft_source")
    text = st.text_area("Discussion text", height=200, key="draft_text")

    if st.button("Draft card", key="draft_button"):
        st.session_state.pop("draft_saved", None)
        if not author.strip():
            st.session_state.pop("draft_card", None)
            st.error("Please enter your name as the author.")
        else:
            try:
                st.session_state["draft_card"] = draft_card(
                    text, author.strip(), source.strip() or "pasted text"
                )
            except ValueError as exc:
                st.session_state.pop("draft_card", None)
                st.error(str(exc))

    card = st.session_state.get("draft_card")
    if card is None:
        return

    with st.container(border=True):
        if card.drafted_by == MOCK:
            st.warning(MOCK_LABEL)
        st.markdown(f"**Decision:** {card.decision}")
        st.markdown(f"**Reason:** {card.reason}")
        st.markdown(f"**Quote:** {card.verbatim_quote}")
        if card.alternatives:
            st.markdown(f"**Alternatives:** {', '.join(card.alternatives)}")
        st.markdown(f"**Confidence:** {card.confidence}")
        for warning in card.warnings:
            st.warning(warning)
        st.caption(
            f"Card {card.id} · written by {card.author} · source: {card.source} · "
            f"drafted by {card.drafted_by}"
        )

    if card.decision == UNKNOWN:
        st.info("No decision found. Add the sentence that states the decision, then draft again.")
    elif st.session_state.get("draft_saved") == card.id:
        st.success(
            "Saved as draft. It now waits in the Review tab: ask a teammate to open it "
            "and enter their own name as reviewer."
        )
    elif st.button("Save as draft", key="draft_save"):
        try:
            store.upsert(card, store.DEFAULT_PATH)
        except Exception as exc:  # a broken data file must not crash the page
            st.error(f"Could not save the card: {exc}")
        else:
            st.session_state["draft_saved"] = card.id
            st.rerun()
