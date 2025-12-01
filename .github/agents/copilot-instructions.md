# advent-of-code-2025 Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-11-28

## Active Technologies
- Python 3.10+ (per constitution) + `uv` (runner/deps), `pytest`, `ruff`, `python-dotenv`, `requests` (001-meta-cli)
- Local filesystem only (day folders, specs) (001-meta-cli)
- Python 3.10+ + requests (existing), python-dotenv (existing), beautifulsoup4 (new), html2text (new) (002-aoc-auto-download)
- Local filesystem (`day-XX/input.txt`, `day-XX/task.md`) (002-aoc-auto-download)
- Python 3.10+ + requests, beautifulsoup4, html2text, python-dotenv (003-save-description-md)
- Local filesystem (day-XX/description.md) (003-save-description-md)
- Python 3.10+ + pytest (dev), no runtime dependencies beyond stdlib (004-day-01-part-1)
- File-based input (input.txt, test_input.txt) (004-day-01-part-1)

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

## Recent Changes
- 004-day-01-part-1: Added Python 3.10+ + pytest (dev), no runtime dependencies beyond stdlib
- 003-save-description-md: Added Python 3.10+ + requests, beautifulsoup4, html2text, python-dotenv
- 002-aoc-auto-download: Added Python 3.10+ + requests (existing), python-dotenv (existing), beautifulsoup4 (new), html2text (new)


<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
