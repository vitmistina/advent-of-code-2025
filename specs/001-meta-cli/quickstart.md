# Quickstart: Meta Runner & CLI (AoC 2025)

## Prerequisites

- Python 3.10+
- UV installed
- `.env` with `AOC_SESSION` (optional; can enter interactively) and `AOC_YEAR`

## Initialize

```powershell
uv init
uv sync
```

## Scaffold a Day

```powershell
uv run -m cli.meta_runner scaffold --day 1
```

## Download Inputs (dry-run supported)

```powershell
uv run -m cli.meta_runner download --day 1 --year 2025
uv run -m cli.meta_runner download --day 1 --dry-run
```

## Generate Spec & Tasks

```powershell
uv run -m cli.meta_runner specify --day 1
```

## TDD Flow

- RED: run tests, see them fail
- GREEN: implement minimal code
- REFACTOR: clean while keeping tests green

## Manual Submission

- Run solution on `input.txt`
- CLI prints answers and link to submission page
- Submit manually; CLI does not auto-post
