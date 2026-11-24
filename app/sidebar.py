"""Sidebar controls (module C): start a demo or user-testing session from a known state."""

import streamlit as st

from decisiontrace import store
from decisiontrace.sample_data import SAMPLE_DISCUSSION, sample_cards


def render() -> None:
    st.sidebar.header("Demo data")
    st.sidebar.caption(
        "Load the sample team history to try Ask and Review right away "
        "(it replaces every saved card), or reset to an empty decision log."
    )
    if st.sidebar.button("Load sample data", key="sidebar_load_sample"):
        try:
            store.save(sample_cards(), store.DEFAULT_PATH)
        except Exception as exc:  # a failed save must not crash the page
            st.sidebar.error(f"Could not save the sample data: {exc}")
        else:
            st.sidebar.success("Loaded 6 sample cards: 4 approved, 1 rejected, 1 draft.")

    confirm = st.sidebar.checkbox("I want to delete every saved card", key="sidebar_confirm_reset")
    if st.sidebar.button("Reset data", key="sidebar_reset", disabled=not confirm):
        try:
            store.save([], store.DEFAULT_PATH)
        except Exception as exc:
            st.sidebar.error(f"Could not reset the data: {exc}")
        else:
            st.sidebar.success("All cards deleted.")

    with st.sidebar.expander("Sample discussion to paste in the Draft tab"):
        st.code(SAMPLE_DISCUSSION, language=None)
