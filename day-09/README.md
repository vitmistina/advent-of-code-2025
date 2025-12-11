# Day 09 - Largest Red Tile Rectangle

## Puzzle Description

**Part 1**: Find the largest rectangle in a grid using two red tiles as opposite corners. The solution parses red tile coordinates from input, evaluates all distinct pairs, calculates rectangle areas, and returns the maximum area found.

**Part 2**: Find the largest rectangle using red tiles as corners where ALL tiles in the rectangle (including interior) must be red or green. Green tiles are those on the polygon boundary (edges connecting consecutive red tiles) and all tiles inside the closed polygon loop formed by the red tiles.

## Implementation Overview

### Phase 1: Input Parsing (US1)

**Input Format**

- Each line contains a red tile coordinate in "x,y" format
- x and y are non-negative integers
- Example:
  ```
  2,5
  11,1
  7,3
  ```

**Core Functions**

1. **validate_input(lines: list[str]) -> None**

   - Validates that input is non-empty
   - Checks each line is properly formatted as "x,y"
   - Ensures all coordinates are non-negative integers
   - Raises ValueError on any malformed input
   - Example:
     ```python
     validate_input(["2,5", "11,1"])  # OK
     validate_input([])  # Raises: Input cannot be empty
     validate_input(["2,5,3"])  # Raises: invalid format
     ```

2. **parse_coordinates(lines: list[str]) -> list[tuple[int, int]]**
   - Parses validated input lines into (x, y) tuples
   - Returns list of coordinate tuples
   - Handles whitespace in input
   - Example:
     ```python
     parse_coordinates(["2,5", "11,1"])
     # Returns: [(2, 5), (11, 1)]
     ```

**Error Handling**

- Empty input: Raises "Input cannot be empty"
- Empty lines: Raises "Line X is empty"
- Malformed format: Raises "Line X has invalid format"
- Non-integer coordinates: Raises "Line X contains non-integer coordinates"
- Negative coordinates: Raises "Line X has negative coordinates"

### Phase 2: Rectangle Area Calculation (US2)

**Core Function**

3. **calculate_rectangle_area(corner1: tuple[int, int], corner2: tuple[int, int]) -> int**
   - Calculates area given two opposite corner coordinates
   - Formula: |x1 - x2| × |y1 - y2|
   - Order-invariant (corner1 and corner2 can be any opposite corners)
   - Example:
     ```python
     calculate_rectangle_area((2, 5), (11, 1))
     # |2-11| × |5-1| = 9 × 4 = 36
     ```

### Phase 3: Find Largest Rectangle (US3)

**Core Function**

4. **find_largest_rectangle(coordinates: list[tuple[int, int]]) -> int**
   - Generates all distinct pairs of red tiles using itertools.combinations
   - Calculates area for each pair
   - Tracks and returns maximum area
   - Raises ValueError if fewer than 2 tiles provided
   - Example:
     ```python
     find_largest_rectangle([(2, 5), (11, 1), (7, 3)])
     # Pairs: (2,5)-(11,1)=36, (2,5)-(7,3)=6, (11,1)-(7,3)=8
     # Returns: 36
     ```

**Main Solution**

5. **solve_part1(coordinates: list[tuple[int, int]]) -> int**
   - Entry point for Part 1
   - Returns the maximum rectangle area

## Testing

### Test Structure

- **TestValidateInput**: 6 tests for input validation
- **TestParseCoordinates**: 3 tests for coordinate parsing
- **TestCalculateRectangleArea**: 5 tests for area calculation
- **TestFindLargestRectangle**: 4 tests for largest rectangle logic
- **TestSolvePart1**: 2 tests for main solution function

### Running Tests

```bash
# All tests
uv run pytest day-09/test_solution.py -v

# Specific test class
uv run pytest day-09/test_solution.py::TestParseCoordinates -v

# Specific test
uv run pytest day-09/test_solution.py::TestParseCoordinates::test_parse_coordinates_valid -v
```

### Test Coverage

- Input validation (empty, malformed, non-integer, negative)
- Coordinate parsing (valid, with whitespace)
- Area calculation (basic, zero width/height, same point, order-invariant)
- Largest rectangle (basic, two tiles, insufficient tiles, collinear)

## Usage

```powershell
# Run tests (RED phase)
uv run pytest day-09/test_solution.py -v

# Run solution (GREEN phase)
uv run python day-09/solution.py

# Run linting
uv run ruff check day-09/solution.py

# Fix linting issues
uv run ruff check day-09/solution.py --fix
```

## Notes

- Part 1: ✅ COMPLETE - Parse coordinates → Calculate areas → Find maximum
- Part 2: [ ] To be implemented

## Progress

- [x] Phase 1 - Setup (T001-T003)
- [x] Phase 2 - Foundational (T004-T006)
- [x] Phase 3 - US1 Parsing (T007-T010)
- [x] Phase 4 - US2 Rectangle Area (T011-T014)
- [x] Phase 5 - US3 Find Largest (T015-T018)
- [x] Final Polish (T019-T021)

## Test Summary

### Part 1

All 21 tests passing (solution.py):

- ✅ TestValidateInput: 6 tests
- ✅ TestParseCoordinates: 3 tests
- ✅ TestCalculateRectangleArea: 5 tests
- ✅ TestFindLargestRectangle: 4 tests
- ✅ TestSolvePart1: 2 tests
- ✅ test_part2: 1 test (stub)

### Part 2

All 24 tests passing (solution_part2.py):

- ✅ Parsing & Validation: 5 tests
- ✅ Winding Detection: 3 tests
- ✅ Turn Classification: 4 tests
- ✅ Edge Index: 3 tests
- ✅ Ray Segment Generation: 3 tests
- ✅ Initial Ray State: 2 tests
- ✅ Rectangle Validation: 3 tests
- ✅ Integration (solve_part2): 1 test

Code quality:

- ✅ Ruff linting: All checks passed
- ✅ Type hints: Complete
- ✅ Docstrings: Comprehensive with examples
- ✅ TDD approach: Strict RED-GREEN-REFACTOR workflow followed

## Running Part 2

```bash
# On example input (should output 24)
uv run python day-09/solution_part2.py < day-09/test_input.txt

# On actual puzzle input
uv run python day-09/solution_part2.py < day-09/input.txt
```

**Note**: The Part 2 solution works correctly on the example input but may be slow on large inputs due to the point-in-polygon validation for every rectangle tile. Future optimization could use scanline algorithms or precomputed interior masks.

- ✅ Edge cases: Handled and tested
