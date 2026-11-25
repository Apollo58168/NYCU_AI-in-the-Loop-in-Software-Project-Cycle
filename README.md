# NYCU_AI-in-the-Loop-in-Software-Project-Cycle

- [AI Usage Guidelines](AI_GUIDELINES.md)
- [Evaluation Plan](EVALUATION_PLAN.md)
- [Prompt Engineering Log](PROMPT_LOG.md)
- [Prompt Test Suite](docs/prompt_test_suite.md)

**Current status (2026-11-25):** Draft can use Claude, but no API key is needed to run the app. Without `ANTHROPIC_API_KEY` the Draft tab uses the keyword MOCK (`decisiontrace/drafter.py`), and every card says which one drafted it. To use Claude, copy `.env.example` to `.env` and fill in the key (the `.env` file is never committed). The Claude drafter has not been run against the real API yet: the course key has not arrived (#21). Ask uses keyword matching (`decisiontrace/ask.py`).

## Run the prototype

DecisionTrace is a Python 3.12 app built with Streamlit and managed with [uv](https://docs.astral.sh/uv/).
uv installs the right Python version and every dependency into `.venv/` inside this folder.

1. Install uv (once per machine): see [Installing uv](https://docs.astral.sh/uv/getting-started/installation/).
   On macOS or Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`.
2. Clone the repository and install the dependencies:

   ```sh
   git clone git@github.com:Apollo58168/NYCU_AI-in-the-Loop-in-Software-Project-Cycle.git
   cd NYCU_AI-in-the-Loop-in-Software-Project-Cycle
   uv sync
   ```

3. Start the app and open the URL it prints (usually http://localhost:8501):

   ```sh
   uv run streamlit run app/main.py
   ```

4. Run the tests:

   ```sh
   uv run pytest
   ```

Cards are stored in `data/cards.json`, which is not committed. Delete that file to start from an empty state.

## Code layout

| Path | What it is | Module owner |
| --- | --- | --- |
| `decisiontrace/cards.py` | `Card` and the verbatim-quote check (`check_quote`) | A |
| `decisiontrace/store.py` | Load and save cards as JSON | A |
| `app/main.py` | The page and its four tabs | A |
| `app/tab_draft.py` | Draft tab | D |
| `app/tab_review.py` | Review tab | B |
| `app/tab_ask.py` | Ask tab | C |
| `app/tab_cards.py` | Approved cards tab | A |
| `decisiontrace/prompt_suite.py`, `tests/prompt_suite/cases.json` | Prompt test suite for the drafter (`uv run python -m decisiontrace.prompt_suite`) | A |
| `decisiontrace/drafter.py`, `decisiontrace/llm.py`, `prompts/draft_card.md` | Drafter: MOCK without a key, Claude with one; the system prompt ([prompt card](docs/PROMPT_CARD.md)) | D |
