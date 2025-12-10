# Quickstart — Day 7 Part 2 Timeline Counter

## Prerequisites

- Python toolchain managed via `uv` (already configured in repo)
- Puzzle assets downloaded with meta runner: `uv run -m cli.meta_runner download --day 7`

## Recommended Workflow

1. **Read the spec**: `specs/002-day-07-part-2/spec.md`
2. **Study research & design**: `research.md`, `data-model.md`, `contracts/`
3. **Follow TDD**:
   - RED: add/extend cases in `day-07/test_solution_part2.py`
   - GREEN: implement solver updates in `day-07/solution_part2.py`
   - REFACTOR: clean logic after tests pass

## Commands

```pwsh
# Run focused tests for Day 7
uv run pytest day-07/test_solution_part2.py

# Run all Day 7 suites (including shared helpers)
uv run pytest day-07

# Execute solver against real input
uv run day-07/solution_part2.py
```

## Debugging Tips

- Use `debug_trace.py` in `day-07/` to log traversal paths when memoization counts look suspicious.
- Set `AOC_DEBUG=1` to have the CLI emit diagnostics (per meta runner options).
- When comparing outputs, leverage `tests/fixtures` for reusable diagrams.

## Next Steps

- Once the solver is green, update `README.md` progress trackers.
- Prepare `/specs/002-day-07-part-2/tasks.md` via `/speckit.tasks` before coding if new tasks are needed.
