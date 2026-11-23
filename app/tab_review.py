"""Review tab (module B): a teammate approves or rejects each draft card.

Streamlit reruns this file on every click. After a card is saved the page is
rerun so it leaves the list; the result message is kept in st.session_state
so it survives that rerun.
"""

import streamlit as st

from decisiontrace import store
from decisiontrace.drafter import MOCK
from decisiontrace.review import review

MOCK_LABEL = "MOCK draft, not AI - needs human review"


def render() -> None:
    st.subheader("Review draft cards")
    st.caption("Check each card against its quote. You cannot review a card you wrote.")

    done = st.session_state.pop("review_done", None)
    if done:
        st.success(done)

    try:
        cards = store.load(store.DEFAULT_PATH)
    except Exception as exc:  # a broken data file must not crash the page
        st.error(f"Could not read the saved cards: {exc}")
        return

    drafts = [c for c in cards if c.status == "draft"]
    if not drafts:
        st.info("No draft cards to review. Draft one in the Draft tab.")
        return

    reviewer = st.text_input("Your name (reviewer)", key="review_reviewer")

    for card in drafts:
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

            approve_col, reject_col = st.columns(2)
            action = None
            if approve_col.button("Approve", key=f"review_approve_{card.id}"):
                action = "approve"
            if reject_col.button("Reject", key=f"review_reject_{card.id}"):
                action = "reject"
            if action is None:
                continue

            try:
                review(card, reviewer, action)
                store.upsert(card, store.DEFAULT_PATH)
            except ValueError as exc:
                st.error(str(exc))
            except Exception as exc:  # a failed save must not crash the page
                st.error(f"Could not save the card: {exc}")
            else:
                st.session_state["review_done"] = f"Card {card.id} {card.status} by {card.reviewer}."
                st.rerun()
