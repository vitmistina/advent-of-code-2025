# Advent of Code 2025

Meta Runner & CLI for Advent of Code 2025 per Constitution 1.3.0.

## Features

- 🚀 Scaffold new day folders with one command
- 📥 Download puzzle descriptions and inputs safely
- 📝 Generate specs and tasks via Specify integration
- ✅ Enforce TDD workflow (RED→GREEN→REFACTOR)
- 🔒 Secure token handling with masked input
- 🎯 Manual submission guidance (AoC-compliant)

## Prerequisites

- Python 3.10+
- [UV](https://github.com/astral-sh/uv) installed

## Quick Start

1. **Setup environment**:

   ```powershell
   # Copy example env file
   cp .env.example .env

   # Edit .env and add your AOC_SESSION token
   # Get it from browser cookies after logging in to adventofcode.com
   ```

2. **Initialize project**:

   ```powershell
   uv sync
   ```

3. **Scaffold a new day**:

   ```powershell
   uv run -m cli.meta_runner scaffold --day 1
   ```

4. **Download inputs** (with dry-run option):

   ```powershell
   uv run -m cli.meta_runner download --day 1 --year 2025
   # Or dry-run to see what would happen
   uv run -m cli.meta_runner download --day 1 --dry-run
   ```

5. **Generate spec & tasks**:

   ```powershell
   uv run -m cli.meta_runner specify --day 1
   ```

6. **Follow TDD flow**:
   - RED: Run tests (they should fail initially)
   - GREEN: Implement minimal solution
   - REFACTOR: Clean up while keeping tests green

## Progress Tracker

| Day | Part 1 | Part 2 | Notes                                                                      |
| --- | ------ | ------ | -------------------------------------------------------------------------- |
| 01  | ✅     | ✅     | 10 % Tokens spent. Spec drift looks to be a concern.                       |
| 02  | ✅     | ⬜     | Part 1: Invalid ID detection (string pattern matching). Answer: 9188031749 |
| ... | ...    | ...    | ...                                                                        |

Legend: ⬜ Not started | 🟨 In progress | ✅ Complete

## Commands

Run `uv run -m cli.meta_runner --help` for full command reference.

## Development

- **Lint**: `uv run ruff check .`
- **Format**: `uv run ruff format .`
- **Test**: `uv run pytest`
- **Coverage**: `uv run pytest --cov=cli --cov-report=html`

## License

MIT
