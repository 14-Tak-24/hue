# Pull Request: fix(pylint): top lint fixes — encodings, logging, exception chaining, test tidy

This PR bundles a set of low-risk, high-ROI lint fixes to improve our pylint score and make error traces more helpful.

Summary
- Add explicit encoding="utf-8" to file open() calls to avoid unspecified-encoding (W1514).
- Replace f-string interpolation inside logging calls with lazy logging formatting to avoid logging-fstring-interpolation (W1203).
- Chain exceptions using `raise ... from exc` to preserve tracebacks and satisfy raise-missing-from (W0707).
- Move some imports in tests to module-top and clean up static f-strings, unused imports, and minor formatting.

Files changed in this PR (initial batch):
- src/modules/utils.py (encodings, exception chaining, lazy logging)
- src/modules/souls_manager.py (lazy logging, encodings, exception chaining)
- tests/test_ai_content.py (move traceback import, remove static f-strings)

Why this PR
- These are safe changes that do not alter business logic but address many of the repeated lint warnings observed in CI. This makes subsequent targeted refactors easier.

Notes
- The branch `fix/pylint-top-fixes-1` contains additional commits and I will continue to push related fixes as follow-ups.
- Larger refactors (duplicate code R0801, too-many-statements R0915, and heavy test refactors) will be addressed in follow-up PRs to keep review scope small.

How to review
- Focus review on correctness of exception chaining and that file encodings were added where appropriate.

CI
- Pylint and tests will run on this PR. Expect improvements but additional iterations will be needed for a clean score.

If this looks good, I will continue applying the rest of the planned quick fixes in follow-up commits/PRs.