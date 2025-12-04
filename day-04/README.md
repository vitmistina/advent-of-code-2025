# Day 4 Part 1: Accessible Paper Rolls Counter

This solution counts accessible paper rolls in a warehouse grid. A paper roll (marked '@') is accessible if fewer than 4 paper rolls exist in its 8 adjacent positions (horizontal, vertical, and diagonal).

## Files

- `solution.py`: Main implementation
- `test_solution.py`: Pytest test suite
- `input.txt`: Actual puzzle input
- `test_input.txt`: Example input from puzzle description
- `description.md`: Challenge description

## Approach

- Parse the grid from input
- For each paper roll, count adjacent rolls
- Determine accessibility (< 4 neighbors)
- Return total accessible rolls

## Usage

Run tests:

```bash
uv run pytest test_solution.py -v
```

Run solution:

```bash
uv run solution.py
```

## References

- [spec.md](../specs/011-day-04-part-1/spec.md)
- [plan.md](../specs/011-day-04-part-1/plan.md)
