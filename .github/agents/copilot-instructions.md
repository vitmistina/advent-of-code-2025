# advent-of-code-2025 Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-11-28

## Active Technologies

- HTML5, CSS3, JavaScript (ES6+) + None (vanilla JavaScript, no frameworks) (006-dial-visualization)
- File-based input (reads from day-01/input.txt or test_input.txt) (006-dial-visualization)
- Python 3.10+ + None (stdlib only, following AoC Constitution) (007-day-02-part-1)
- File-based input (`day-02/input.txt`, `day-02/test_input.txt`) (007-day-02-part-1)
- [e.g., Python 3.11, Swift 5.9, Rust 1.75 or NEEDS CLARIFICATION] + [e.g., FastAPI, UIKit, LLVM or NEEDS CLARIFICATION] (009-day-03-part-1)
- [if applicable, e.g., PostgreSQL, CoreData, files or N/A] (009-day-03-part-1)
- Python 3.10+ + None (stdlib only, pytest for testing) (009-day-03-part-1)
- Files (input.txt, test_input.txt) (009-day-03-part-1)
- Python 3.10+ + pytest, ruff (linting/formatting), uv (package management) (011-day-04-part-1)
- File-based (`day-04/input.txt`, `day-04/test_input.txt`) (011-day-04-part-1)
- Python 3.10+ + pytest (already in project) (001-day-04-part-2)
- File-based (input.txt, test_input.txt) (001-day-04-part-2)
- Python 3.10+ + uv, ruff, pytest (for tests) (001-day-04-part-2)
- Python 3.10+ (uv-managed virtual environment) + Standard library (pathlib, typing), pytest for local tests, uv tooling; no third-party runtime deps needed (012-day-05-part-1)
- Local filesystem inputs (`day-05/input.txt`, `day-05/test_input.txt`) (012-day-05-part-1)
- Python 3.10+ + Built-in (dataclasses, typing) (013-day-05-part-2)

- Python 3.10+ (per constitution) + `uv` (runner/deps), `pytest`, `ruff`, `python-dotenv`, `requests` (001-meta-cli)
- Local filesystem only (day folders, specs) (001-meta-cli)
- Python 3.10+ + requests (existing), python-dotenv (existing), beautifulsoup4 (new), html2text (new) (002-aoc-auto-download)
- Local filesystem (`day-XX/input.txt`, `day-XX/task.md`) (002-aoc-auto-download)
- Python 3.10+ + requests, beautifulsoup4, html2text, python-dotenv (003-save-description-md)
- Local filesystem (day-XX/description.md) (003-save-description-md)
- Python 3.10+ + pytest (dev), no runtime dependencies beyond stdlib (004-day-01-part-1)
- File-based input (input.txt, test_input.txt) (004-day-01-part-1)
- Python 3.10+ + Standard library only (pathlib for file I/O) (005-day-01-part-2)
- File-based (input.txt, test_input.txt in day-01/ folder) (005-day-01-part-2)

- Python 3.10+ (per Constitution) + UV (package manager), pytest (tests), ruff (lint/format), requests (HTTP with backoff) — NEEDS CLARIFICATION for backoff strategy library vs custom (001-meta-cli)

## Project Structure

```text
src/
tests/
```

## Commands

cd src; pytest; ruff check .

## Code Style

Python 3.10+ (per Constitution): Follow standard conventions

## Git Commit Guidelines

- **MUST use Conventional Commits format**: `type(scope): description`
- Common types: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`
- Example: `feat(day-01): implement part 2 similarity score calculation`

## Recent Changes

- 013-day-05-part-2: Added [e.g., Python 3.11, Swift 5.9, Rust 1.75 or NEEDS CLARIFICATION] + [e.g., FastAPI, UIKit, LLVM or NEEDS CLARIFICATION]
- 013-day-05-part-2: Added Python 3.10+ + Built-in (dataclasses, typing)
- 012-day-05-part-1: Added Python 3.10+ (uv-managed virtual environment) + Standard library (pathlib, typing), pytest for local tests, uv tooling; no third-party runtime deps needed

<!-- MANUAL ADDITIONS START -->

User USES POWERSHELL! Do not suggest bash commands.

<!-- MANUAL ADDITIONS END -->
