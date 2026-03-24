Run the pre-commit checklist for this project:

1. Remind me to update `CHANGELOG.md` `[Unreleased]` section (Added / Changed / Fixed / Removed) — I must do this manually.
2. Run `uv run flake8 .` — must pass.
3. Run `uv run black --check .` — must pass (run `uv run black .` to auto-fix).
4. Run `uv run pytest` — all tests must pass.
5. Run `uv run pytest --cov=./ --cov-report=term` — coverage must be ≥80%.

Run steps 2–5, report the results clearly, then propose a branch name and commit message for my approval using the format `type(scope): description (#issue)` (max 80 chars; types: `feat` `fix` `chore` `docs` `test` `refactor` `ci` `perf`). Do not create the branch or commit until I explicitly confirm.
