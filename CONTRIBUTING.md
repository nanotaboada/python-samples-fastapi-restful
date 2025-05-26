# Contributing

Thank you for improving this project! We value small, precise changes that solve real problems.
We value **incremental, detail‑first contributions** over big rewrites or abstractions.

## 1. Philosophy

> "Nobody should start to undertake a large project. You start with a small _trivial_ project, and you should never expect it to get large. If you do, you'll just overdesign and generally think it is more important than it likely is at that stage. Or worse, you might be scared away by the sheer size of the work you envision. So start small, and think about the details. Don't think about some big picture and fancy design. If it doesn't solve some fairly immediate need, it's almost certainly over-designed. And don't expect people to jump in and help you. That's not how these things work. You need to get something half-way _useful_ first, and then others will say "hey, that _almost_ works for me", and they'll get involved in the project." — [Linus Torvalds](https://web.archive.org/web/20050404020308/http://www.linuxtimes.net/modules.php?name=News&file=article&sid=145)

## 2. Code & Commit Conventions

- **Conventional Commits**
  Follow <https://www.conventionalcommits.org/en/v1.0.0/>:
  - `feat: ` for new features
  - `fix: ` for bug fixes
  - `chore: ` for maintenance or tooling

- **Logical Commits**
  Group changes by purpose. Multiple commits are fine, but avoid noise. Squash when appropriate.

- **Python Formatting & Style**
  - Use **[Black](https://black.readthedocs.io/)** for consistent code formatting.
    - Black is opinionated: don't argue with it, just run it.
    - Line length is set to **88**, matching the default.
  - Use **[flake8](https://flake8.pycqa.org/en/latest/)** for static checks.
    - Line length also set to 88.
    - Some flake8 warnings are disabled (e.g. `E203`, `W503`) to avoid conflicts with Black.
  - Run `black .` and `flake8` before submitting.
  - Use Python **3.13.x** for local testing and formatting.

- **Testing**
  - Run `pytest` before pushing.
  - Ensure coverage isn’t regressing.

## 3. Pull Request Workflow

- **One logical change per PR.**
- **Rebase or squash** before opening to keep history clean.
- **Title & Description**
  - Use Conventional Commit format.
  - Explain _what_ and _why_ concisely in the PR body.

## 4. Issue Reporting

- Search open issues before creating a new one.
- Include clear steps to reproduce and environment details.
- Prefer **focused** issues—don’t bundle multiple topics.

## 5. Automation & Checks

All PRs and pushes go through CI:

- **Commitlint** for commit style
- **Black** for formatting
- **flake8** for static checks
- **pytest** with coverage

PRs must pass all checks to be reviewed.

## 6. Code of Conduct & Support

- See `CODE_OF_CONDUCT.md` for guidelines and reporting.
- For questions or planning, open an issue and use the `discussion` label, or mention a maintainer.

---

Thanks again for helping keep this project small, sharp, and focused.
