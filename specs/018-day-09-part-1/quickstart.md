# Quickstart: AoC Day 9 Part 1 - Largest Red Tile Rectangle

## Steps

1. **Parse Input**

   - Read `input.txt` for red tile coordinates in `x,y` format (one per line).
   - Validate each line; raise error on malformed or empty input.

2. **Store Coordinates**

   - Store each coordinate as a tuple `(x, y)` in a list.

3. **Calculate Rectangle Areas**

   - Use `itertools.combinations` to generate all distinct pairs of red tiles.
   - For each pair, calculate area: `abs(x1 - x2) * abs(y1 - y2)`.

4. **Find Largest Rectangle**

   - Track the maximum area found across all pairs.
   - Return the largest area value only.

5. **Testing**

   - Add test cases in `test_solution.py` using `pytest`.
   - Use inline asserts for quick checks in `solution.py`.

6. **Linting & Style**

   - Run `ruff` for linting and PEP8 compliance.

7. **Documentation**
   - Update `README.md` with progress and notes.

## Example

- Input:
  ```
  2,5
  11,1
  7,3
  ```
- Output: Largest rectangle area (e.g., 36)

## Folder Structure

```text
day-09/
├── solution.py
├── test_solution.py
├── input.txt
├── test_input.txt
├── README.md
```

## Requirements

- Python 3.10+
- Standard library only
- pytest, ruff, uv
