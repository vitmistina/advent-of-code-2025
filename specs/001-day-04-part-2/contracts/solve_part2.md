# Algorithm Contract: solve_part2()

**Function**: `solve_part2(input_data: str) -> int`

**Purpose**: Calculate total number of paper rolls that can be removed through iterative forklift access.

---

## Contract

### Input

**Parameter**: `input_data: str`

**Format**: Multiline string representing a rectangular grid

- Each line is a row of the grid
- Characters: `@` (paper roll) or `.` (empty space)
- Grid must be rectangular (all rows same length)

**Example**:

```python
input_data = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@"""
```

**Preconditions**:

- `input_data` is a non-empty string
- After stripping whitespace, contains at least one valid row
- All rows have equal length (rectangular grid)
- Contains only `@`, `.`, and whitespace characters

---

### Output

**Type**: `int`

**Meaning**: Total number of paper rolls removed across all iterations

**Range**: `[0, total_rolls_in_grid]`

- Minimum: 0 (all rolls have ≥ 4 neighbors, none accessible)
- Maximum: N where N is total `@` characters in grid (all rolls eventually removed)

**Example**:

```python
# For the sample input from problem description
result = solve_part2(sample_input)
assert result == 43
```

---

### Behavior

**Algorithm Steps**:

1. **Parse Grid**: Convert input string to grid representation

   ```python
   grid = parse_grid(input_data)
   ```

2. **Initialize Roll Tracker**: Build dictionary of all roll positions with neighbor counts

   ```python
   rolls: dict[tuple[int, int], int] = {}
   for each @ in grid:
       rolls[(row, col)] = count_adjacent_rolls(grid, row, col)
   ```

3. **Iterative Removal Loop**:

   ```python
   total_removed = 0
   while True:
       # Find accessible rolls (< 4 neighbors)
       accessible = {pos for pos, count in rolls.items() if count < 4}

       # Termination check
       if not accessible:
           break

       # Remove accessible rolls and update neighbor counts
       for pos in accessible:
           del rolls[pos]
           for neighbor in get_8_neighbors(pos):
               if neighbor in rolls:
                   rolls[neighbor] -= 1

       total_removed += len(accessible)
   ```

4. **Return Total**: Return cumulative count of removed rolls

---

### Guarantees

**Correctness**:

- Roll is accessible ⟺ has fewer than 4 adjacent paper rolls
- All accessible rolls in an iteration are removed simultaneously
- Neighbor counts are accurately maintained after each removal
- Process terminates when no rolls have < 4 neighbors

**Termination**:

- Loop terminates in finite time (each iteration removes ≥ 1 roll if accessible set non-empty)
- Maximum iterations: N (total rolls) in worst case where one roll removed per iteration
- Typical iterations: O(log N) to O(√N) due to cascading accessibility

**Performance**:

- Time complexity: O(R × K) where R = total rolls, K = average removals per iteration
- Space complexity: O(R × C) where R = rows, C = columns (grid storage)
- No unnecessary grid rescans (dictionary-based tracking)

---

### Side Effects

**None** - Pure function with no external state modification

---

### Error Handling

**Invalid Grid**:

```python
# Non-rectangular grid
ValueError: "Grid is not rectangular"

# Empty input
Returns: 0
```

**Edge Cases**:

- Single roll with no neighbors: Returns 1 (one iteration)
- All rolls isolated (no neighbors): Returns N (one iteration removes all)
- All rolls clustered (all have ≥ 4 neighbors): Returns 0 (no iterations)
- Grid with no rolls: Returns 0

---

### Test Coverage

**Required Tests**:

1. **Sample from problem description**:

   ```python
   def test_example_part2():
       input_data = """..@@.@@@@.
       @@@.@.@.@@
       @@@@@.@.@@
       @.@@@@..@.
       @@.@@@@.@@
       .@@@@@@@.@
       .@.@.@.@@@
       @.@@@.@@@@
       .@@@@@@@@.
       @.@.@@@.@."""
       assert solve_part2(input_data) == 43
   ```

2. **All isolated rolls**:

   ```python
   def test_all_isolated():
       input_data = "@.@\n...\n@.@"
       assert solve_part2(input_data) == 4  # All removed in one iteration
   ```

3. **No accessible rolls**:

   ```python
   def test_no_accessible():
       input_data = "@@@@@\n@@@@@\n@@@@@"
       # All rolls have 8 or close to 8 neighbors
       result = solve_part2(input_data)
       assert result < 25  # Some might remain
   ```

4. **Cascading removals**:

   ```python
   def test_cascading():
       input_data = "@@@\n@.@\n@@@"
       # Center empty, so all 8 rolls have 2-3 neighbors initially
       result = solve_part2(input_data)
       assert result == 8  # All removed, possibly multiple iterations
   ```

5. **Empty grid**:
   ```python
   def test_empty_grid():
       assert solve_part2("") == 0
       assert solve_part2("...\n...\n...") == 0
   ```

---

### Dependencies

**Required Functions** (from Part 1):

- `parse_grid(input_data: str) -> list[str]`
- `count_adjacent_rolls(grid: list[str], row: int, col: int) -> int`
- `DIRECTIONS: list[tuple[int, int]]` (8-direction offsets)

**New Helper** (optional extraction):

```python
def get_neighbors(pos: tuple[int, int]) -> list[tuple[int, int]]:
    """Return 8 neighboring positions for given position."""
    row, col = pos
    return [(row + dr, col + dc) for dr, dc in DIRECTIONS]
```

---

### Integration with Part 1

**Shared Resources**:

- Same `input.txt` and `test_input.txt` files
- Same grid parsing logic
- Same adjacency counting logic

**Differences**:

- Part 1: Single pass, count accessible rolls
- Part 2: Iterative loop, count total removed

**Main Block**:

```python
if __name__ == "__main__":
    with open("day-04/input.txt") as f:
        input_data = f.read()

    part1_result = solve_part1(input_data)
    part2_result = solve_part2(input_data)

    print(f"Part 1: {part1_result}")
    print(f"Part 2: {part2_result}")
```
