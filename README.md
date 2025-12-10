# Progress

| Day | Part 1 | Part 2 | Notes                         |
| --- | ------ | ------ | ----------------------------- |
| 1   | ✅     | ✅     | List distance/similarity      |
| 2   | ✅     | ✅     | Report safety analysis        |
| 3   | ✅     | ✅     | Regex parsing                 |
| 4   | ✅     | ⬜     | Grid adjacency counting       |
| 5   | ✅     | ✅     | Topological sorting           |
| 6   | ✅     | ✅     | Worksheet validation          |
| 7   | ✅     | ✅     | Equation solver               |
| 8   | ✅     | ✅     | Circuit analysis (Union-Find) |

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

3. **Setup a new day (scaffold + download)**:

   ```powershell
   uv run -m cli.meta_runner setup --day 1 --year 2025
   # Or dry-run to see what would happen
   uv run -m cli.meta_runner setup --day 1 --dry-run
   ```

4. **Generate spec & tasks**:

   ```powershell
   uv run -m cli.meta_runner specify --day 1
   ```

5. **Follow TDD flow**:
   - RED: Run tests (they should fail initially)
   - GREEN: Implement minimal solution
   - REFACTOR: Clean up while keeping tests green

## Progress Tracker

| Day | Part 1 | Part 2 | Notes                                                                                                                                                         |
| --- | ------ | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 01  | ✅     | ✅     | 10 % Tokens spent. Spec drift looks to be a concern.                                                                                                          |
| 02  | ✅     | ✅     | 14 % Tokens spent. Speckit/Copilot wanted to bruteforce, caught at research.md phase. Still, I wasn't able to steer to a "nice" solution fully.               |
| 03  | ✅     | ✅     | 16 % Tokens spent. Another "lazy" attempt at bruteforce. Based on a vague description, the robot aligned description with "monotonic stack" algo.             |
| 04  | ✅     | ✅     | 19 % Tokens spent. Spent 5 minutes debugging, because I've written wrong answer to the AoC UI 😅. Part 2, I've told it what to do in the Plan/Research phase. |
| 05  | ✅     | ✅     | 21 % Tokens spent. I love the fact I can tell ideas to the robot (set theory, set merging/union) and it does the low level stuff                              |
| ... | ...    | ...    | ...                                                                                                                                                           |

Legend: ⬜ Not started | ✅ Complete

## Commands

Run `uv run -m cli.meta_runner --help` for full command reference.

## Development

- **Lint**: `uv run ruff check .`
- **Format**: `uv run ruff format .`
- **Test**: `uv run pytest`
- **Coverage**: `uv run pytest --cov=cli --cov-report=html`

## License

MIT
