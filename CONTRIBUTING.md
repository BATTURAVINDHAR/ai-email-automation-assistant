# Contributing

Thanks for considering a contribution! This is a portfolio project, but it's
built to real engineering standards and welcomes improvements.

## Getting started
1. Fork the repo and clone your fork.
2. Create a virtual environment: `python -m venv venv && source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and fill in your own API keys.
5. Run tests: `pytest tests/`

## Making a change
1. Create a branch: `git checkout -b feature/your-feature-name`
2. Write code following the existing style (PEP 8, type hints, docstrings).
3. Add or update tests for any behavior change.
4. Run `black src/ main.py tests/` to auto-format.
5. Run `flake8 src/ main.py` to lint.
6. Commit with a clear message and open a pull request.

## Code style
- All functions have type hints and docstrings.
- Business logic (email_workflow.py) stays separate from API clients
  (gmail_client.py, ai_processor.py) — see the architecture section in
  README.md before adding new integrations.
- Never commit secrets. `.env`, `credentials.json`, and `token.json` are
  git-ignored on purpose.

## Reporting bugs
Open a GitHub issue with: what you expected, what happened instead, and
the relevant lines from `logs/email_assistant.log` (with any personal
data redacted).
