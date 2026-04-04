# Pre-commit checklist

Before running the checklist, run `git fetch origin`. If the current branch is behind `origin/master`, stop and rebase before proceeding.

Run the pre-commit checklist for this project:

1. Update `CHANGELOG.md` `[Unreleased]` section — add an entry under the
   appropriate subsection (Added / Changed / Fixed / Removed) describing the
   changes made, referencing the issue number.
2. Run `uv run flake8 .` — must pass.
3. Run `uv run black --check .` — must pass (run `uv run black .` to auto-fix).
4. Run `uv run pytest --cov=./ --cov-report=term --cov-fail-under=80` — all tests must pass, coverage must be ≥80%.
5. If Docker is running, run `docker compose build` — must succeed with no
   errors. Skip this step with a note if Docker Desktop is not running.
6. If `coderabbit` CLI is installed, run `coderabbit review --type uncommitted --prompt-only`:
   - If actionable/serious findings are reported, stop and address them before proposing the commit.
   - If only nitpick-level findings, report them and continue to the commit proposal.
   - If `coderabbit` is not installed, skip this step with a note.

Run steps 1–5, report the results clearly, then run step 6 (CodeRabbit review) if available, then propose a branch name and commit message for my approval using the format `type(scope): description (#issue)` (max 80 chars; types: `feat` `fix` `chore` `docs` `test` `refactor` `ci` `perf`). Do not create the branch or commit until I explicitly confirm.
