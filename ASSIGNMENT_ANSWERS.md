# Campus Library API — Refactoring Assignment

## Part 1: Diagnose

| Location | Problem | Main type | Future change made harder |
|---|---|---|---|
| `app.py` overall | HTTP, database, rules, validation and notifications share one file | Low cohesion | Updating one feature without affecting others |
| `CURRENT_MEMBER` and `notify()` | Email depends on a global database row | Common/stamp coupling | Supporting multiple requests or changing member fields |
| `check(value, kind)` | String argument controls unrelated validation rules | Control coupling | Adding new validation types |
| Route functions | SQL appears directly inside HTTP handlers | External coupling / low cohesion | Switching database or changing table schema |
| Fine calculations | $0.50 per day appears in multiple handlers | High coupling | Updating the fine rate consistently |
| `notify(kind, ...)` | Notification content depends on a control string | Control coupling | Adding or changing notifications |
| Repeated `sqlite3.connect()` | Connection setup repeated throughout routes | External coupling | Changing database connection details |

## Part 2: Refactor

The project is separated into route, service, repository and database layers. Route modules handle HTTP and JSON. Service modules apply library rules. Repository modules contain SQL. `db.py` manages database setup and connections. `fines.py` is a pure calculation module. `notifications.py` receives an email address explicitly instead of reading `CURRENT_MEMBER`.

### Measurements

| Measure | Before | After |
|---|---:|---:|
| Tests passing | 53 expected by teacher | Not verified here; Flask unavailable in build environment |
| Lines in largest application Python file (excluding tests) | 555 | 68 |
| Fine rate definition | Repeated across handlers | 1 (`fines.py`) |
| Route handlers containing SQL | 16 (teacher's baseline) | 0 |
| Places edited for change request | n/a | Pending instructor's requirement |
| Fine rule testable without HTTP/database | No | Yes (`fines.fine_for`) |

### Reflection questions

**1. Most cohesive module:** `fines.py`. Its single responsibility is calculating overdue days and fine amounts.

**2. Dependency removed:** Notifications no longer rely on the global `CURRENT_MEMBER`. The loan service supplies the email directly, so notification formatting can change without changing how member data is stored.

**3. Remaining coupling:** Services depend on repository interfaces and the shared loan service rules. This is acceptable because services need stored information to apply the library rules; keeping these dependencies explicit makes them easier to maintain.

## Part 3: Change request

The uploaded assignment says the instructor will announce the new requirement separately. No specific change request was included. **Do not invent a requirement or claim this part is completed.** Once the instructor supplies it, implement it and record which files were changed and how many places were edited.

## How to run on macOS

1. Open this folder in VS Code.
2. Open Terminal in this folder.
3. Run `python3 -m venv .venv`.
4. Run `source .venv/bin/activate`.
5. Run `pip install -r requirements.txt`.
6. Run `python -m unittest` (expect 53 tests and OK).
7. Run `python -m flask run --port 8000` to start the API.

Keep `test_api.py` unchanged. If tests fail, send the error output for correction before submitting.
