Run the pre-release checklist for this project.

**Working style**: propose before acting at every step — do not commit, push,
open PRs, or create tags until I explicitly confirm. Apply this throughout.

1. **Detect current release and propose next**: Read `CHANGELOG.md` for the
   coach naming convention (A–Z table) and the most recent release heading.
   Run `git tag --sort=-v:refname` to confirm the latest tag. Determine the
   next codename (next letter in the A–Z sequence after the current one) and
   infer the version bump from the `[Unreleased]` section: any entry marked
   BREAKING → MAJOR; entries under Added → MINOR; only Changed/Fixed/Removed
   → PATCH. Present the proposed `vX.Y.Z-{codename}` and wait for confirmation
   or override before proceeding.

2. **Verify working tree**: Confirm we are on `master` with a clean working
   tree. Pull latest if behind remote.

3. **Create release branch**: `release/vX.Y.Z-{codename}`.

4. **Update CHANGELOG.md**: Move all content under `[Unreleased]` to a new
   release heading `[X.Y.Z - Codename] - {today's date}`. Leave a fresh
   `[Unreleased]` with all four empty subsections:
   Added / Changed / Fixed / Removed.

5. **Propose commit**: `docs(changelog): release vX.Y.Z Codename`

6. **After confirmation**: commit the changelog update. Then run `/precommit`
   to execute the full pre-commit checklist (linting, formatting, tests,
   coverage). Only push the branch and open a PR into `master` once all
   checks pass.

7. **Stop and wait** for confirmation that:
   - All CI checks have passed
   - CodeRabbit review comments have been addressed
   - The PR has been merged into `master`

8. **After confirmation**: pull `master`, then propose the annotated tag
   `vX.Y.Z-{codename}` with message `Release X.Y.Z - Codename`.

9. **After confirmation**: create and push the tag. The CD pipeline triggers
   automatically.
