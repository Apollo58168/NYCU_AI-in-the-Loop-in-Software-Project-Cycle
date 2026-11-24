"""Answer questions from approved decision cards only (module C).

Matching is plain keyword overlap, no AI: the question and each card are cut
into tokens, and cards are ranked by how many tokens they share with the
question. English is split into words; Chinese has no spaces, so each run of
Chinese characters is cut into overlapping two-character pieces (bigrams).

An answer uses up to MAX_SOURCES cards and cites each one by id and verbatim
quote, so the reader can check every statement against its source.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from .cards import Card

NO_ANSWER = "No approved decision found."
MAX_SOURCES = 3

# Words that appear in almost every question or card, so matching on them
# would make an unrelated card look relevant.
_STOP_WORDS = {
    "a", "about", "an", "and", "are", "as", "at", "be", "by", "did", "do",
    "does", "for", "from", "how", "in", "is", "it", "of", "on", "or", "our",
    "so", "that", "the", "this", "to", "us", "was", "we", "were", "what",
    "when", "which", "who", "why", "will", "with",
    "decide", "decided", "decision", "decisions", "choose", "chose", "chosen",
}
_STOP_BIGRAMS = {
    "我們", "為什", "什麼", "決定", "怎麼", "是否", "為何", "哪個", "一個", "這個",
}

_WORD = re.compile(r"[a-z0-9]+")
_CJK_RUN = re.compile(r"[㐀-䶿一-鿿]+")


@dataclass
class Answer:
    text: str
    card_ids: list[str] = field(default_factory=list)


def tokens(text: str) -> set[str]:
    """Lowercase words plus Chinese character bigrams, minus stop words."""
    text = text.lower()
    found = {w for w in _WORD.findall(text) if len(w) > 1 and w not in _STOP_WORDS}
    for run in _CJK_RUN.findall(text):
        if len(run) == 1:
            found.add(run)
        found.update(run[i : i + 2] for i in range(len(run) - 1))
    return found - _STOP_BIGRAMS


def _card_tokens(card: Card) -> set[str]:
    return tokens(" ".join([card.decision, card.reason, *card.alternatives]))


def rank(question: str, cards: list[Card]) -> list[Card]:
    """Approved cards that match the question, best first, at most MAX_SOURCES.

    A card counts as relevant when it shares at least a third of the
    question's keywords (so one stray shared word such as "server" does not
    make an unrelated card the answer) and at least half as many keywords as
    the best card. Equal scores put the newer card first, since a later
    decision may have replaced an earlier one.
    """
    wanted = tokens(question)
    scored = [
        (len(wanted & _card_tokens(card)), card)
        for card in cards
        if card.status == "approved"
    ]
    scored = [(score, card) for score, card in scored if score > 0 and 3 * score >= len(wanted)]
    if not scored:
        return []
    scored.sort(key=lambda sc: (sc[0], sc[1].created_at), reverse=True)
    best_score = scored[0][0]
    return [card for score, card in scored if 2 * score >= best_score][:MAX_SOURCES]


def _cite(card: Card) -> str:
    return (
        f"[{card.id}] {card.decision}\n"
        f"Reason: {card.reason}\n"
        f'Quote: "{card.verbatim_quote}"'
    )


def answer(question: str, cards: list[Card]) -> Answer:
    """Answer from the best-matching approved cards, citing each one.

    Raises ValueError for an empty question. Cards that are not approved are
    never used. If no approved card shares a token with the question, the
    answer is exactly NO_ANSWER with no card ids. A reason or quote that is
    "unknown" stays "unknown": nothing is filled in.
    """
    if not question or not question.strip():
        raise ValueError("Please type a question.")

    sources = rank(question, cards)
    if not sources:
        return Answer(NO_ANSWER, [])
    return Answer("\n\n".join(_cite(c) for c in sources), [c.id for c in sources])
