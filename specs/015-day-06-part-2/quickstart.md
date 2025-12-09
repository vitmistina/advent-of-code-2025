# Quickstart: Day 6 Part 2 - Cephalopod Math (Right-to-Left Columns)

## Example Usage

```python
import solution_part2
# From file
result = solution_part2.solve_worksheet("input.txt", verbose=True)
print(f"Grand Total: {result}")

# From string
import io
worksheet = """123 328  51 64\n 45 64  387 23\n  6 98  215 314\n*   +   *   +\n"""
total = solution_part2.solve_worksheet(io.StringIO(worksheet), verbose=True)
print(f"Grand Total: {total}")
# Should print: Grand Total: 3263827
```

## Acceptance Criteria

- Example worksheet (see spec) produces grand total 3263827
- All edge cases and malformed inputs are handled as specified
