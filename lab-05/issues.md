# Issue Table

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| mktemp insecure (Bandit B306) | Security | 40 | Filename can be hijacked before the file is created | Use tempfile.mkstemp |
| assert for validation (Bandit B101) | Security | 61 | Removed when Python runs with -O | Replace with an if check |
| Mutable default logs=[] (Pylint W0102) | Bug | 10 | List is shared across all calls | Default to None |
| Bare except (Pylint W0702, Flake8 E722) | Bug | 18 | Hides every error | Check asset exists, catch only ValueError |
| Unused import logging (F401) | Style | 2 | Dead import | Removed |
| Line too long and blank lines (E501, E302, E305) | Style | 11, 15, 66 | PEP 8 formatting | Wrapped the line, added blank lines |
| open() without with or encoding (R1732, W1514) | Quality | 34, 41 | File may stay open, encoding depends on OS | Use with open(..., encoding="utf-8") |
| global statement (W0603) | Quality | 30 | Hard to track state | Use a settings dict |
| printAlerts name (C0103) | Style | 46 | Not snake_case | Renamed to print_alerts |
| Missing docstrings (C0114, C0116) | Style | all | No documentation | Added docstrings |
| Empty asset ID accepted | Logic bug | 10 | Blank asset got registered | Reject empty IDs |
| Duplicate ID overwrites | Logic bug | 11 | Crane replaced Forklift | Reject duplicates |
| Negative interval | Logic bug | 29 | Everything marked overdue | Require days > 0 |
| Invalid date accepted | Logic bug | 15 | "banana" crashed the program later | Validate with strptime |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 6.55/10 | 10.00/10 |
| Bandit | 2 issues | 0 |
| Flake8 | 12 issues | 0 |