# Reflection

## 1. Which issues were the easiest to fix and which were the hardest?

The easiest issues were the Flake8 formatting problems (blank lines, line length, the unused `logging` import) and the Pylint naming and docstring warnings, because the tools say exactly what to change. The hardest were the logic bugs: duplicate asset IDs, empty IDs, a negative service interval and unvalidated dates. No tool reports these, so I had to run the program, notice the strange output (a blank-named asset in the alerts, the Crane overwriting the Forklift) and decide what the correct behaviour should be.

## 2. Did the tools report any false positives?

Not really, but some warnings were a judgment call. Bandit's `assert` warning (B101) is Low severity and harmless in test code, but here the `assert` was doing real input checking, so it was worth replacing with an explicit `if` check. Pylint's `global-statement` warning is partly a style preference. I fixed it by storing the interval in a `settings` dictionary instead of ignoring the warning.

## 3. How would you integrate static analysis tools into your actual development workflow?

I would run Flake8, Pylint and Bandit automatically in two places: in a pre-commit hook on my machine, and in a CI pipeline (for example GitHub Actions) on every pull request. The build should fail if Bandit finds any Medium or High issue or if the Pylint score drops below a set threshold such as 9.5. Keeping the tool settings in a shared config file would make sure the whole team follows the same rules.

## 4. What tangible improvements did you observe in the code after applying the fixes?

The Pylint score went from 6.55 to 10.00, Flake8 issues went from 12 to 0, and Bandit issues went from 2 to 0. Readability improved through docstrings, consistent formatting and clearer names. Security improved by replacing the insecure `mktemp` with `mkstemp`. Files are now closed safely with `with` blocks. Reliability also improved because the program now rejects invalid input with a clear message instead of storing bad data or crashing later. The main lesson is that static analysis is very good at style and security patterns, but it cannot replace running the program and thinking about what correct behaviour should be.