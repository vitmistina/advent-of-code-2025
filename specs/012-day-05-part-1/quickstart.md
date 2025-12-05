# Quickstart — Day 5 Part 1

## 1. Sync Inputs

```pwsh
uv run -m cli.meta_runner download --day 5
```

- Ensures `day-05/description.md`, `input.txt`, and `test_input.txt` exist.

## 2. Follow TDD Workflow

1. **RED** — add/extend tests in `day-05/test_solution.py` using the acceptance criteria (IDs 1,5,8,11,17,32).
   ```pwsh
   uv run pytest day-05/test_solution.py -k part1
   ```
2. **GREEN** — implement `solve_part1(data: str) -> int` plus helper interval utilities in `day-05/solution.py`.
3. **REFACTOR** — clean up, ensure docstrings + Ruff compliance (`uv run ruff check day-05`).

## 3. Execute Solution

```pwsh
uv run day-05/solution.py --part 1
```

- CLI prints the count of fresh ingredient IDs for both sample and real input.

## 4. Validate Performance

- Optional benchmark: `uv run python -m timeit -s "from day_05.solution import solve_part1, load" "solve_part1(load())"`
- Ensure runtime stays near `O(R log R + I log I)` for the given inputs.

## 5. Commit & Track

```pwsh
git add day-05/*.py day-05/test_solution.py specs/012-day-05-part-1/*
git commit -m "feat: solve day 05 part 1"
```

- Update central README progress tracker afterwards.
