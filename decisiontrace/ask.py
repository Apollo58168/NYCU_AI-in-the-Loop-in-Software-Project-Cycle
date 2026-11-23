"""Answer questions from approved decision cards only (module C).

Matching is plain keyword overlap, no AI: the question and each card are cut
into tokens, and the card sharing the most tokens with the question wins.
English is split into words; Chinese has no spaces, so each run of Chinese
characters is cut into overlapping two-character pieces (bigrams).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from .cards import Card

NO_ANSWER = "No approved decision found."

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


def answer(question: str, cards: list[Card]) -> Answer:
    """Answer from the best-matching approved card.

    Raises ValueError for an empty question. Cards that are not approved are
    never used. If no approved card shares a token with the question, the
    answer is exactly NO_ANSWER with no card ids. On a tie the newer card wins,
    since a later decision may have replaced an earlier one.
    """
    if not question or not question.strip():
        raise ValueError("Please type a question.")

    wanted = tokens(question)
    best: Card | None = None
    best_score = 0
    for card in cards:
        if card.status != "approved":
            continue
        score = len(wanted & _card_tokens(card))
        if score > best_score or (
            score == best_score and best is not None and card.created_at > best.created_at
        ):
            best, best_score = card, score

    if best is None or best_score == 0:
        return Answer(NO_ANSWER, [])
    return Answer(f"{best.decision}\n\nReason: {best.reason}", [best.id])
