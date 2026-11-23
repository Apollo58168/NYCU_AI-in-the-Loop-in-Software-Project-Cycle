"""DecisionTrace Streamlit app: one tab per module.

Each tab lives in its own file and exposes render(), so the four modules can be
built in parallel without editing the same file.
"""

import streamlit as st

import tab_ask
import tab_cards
import tab_draft
import tab_review

st.set_page_config(page_title="DecisionTrace", layout="wide")
st.title("DecisionTrace")
st.caption("Draft decision cards from team discussions; a teammate reviews every card.")

draft, review, ask, cards = st.tabs(["Draft", "Review", "Ask", "Approved cards"])
with draft:
    tab_draft.render()
with review:
    tab_review.render()
with ask:
    tab_ask.render()
with cards:
    tab_cards.render()
