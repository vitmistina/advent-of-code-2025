# Data Model: Day 4 Part 1 - Accessible Paper Rolls Counter

**Feature**: Count accessible paper rolls on a grid  
**Date**: 2025-12-04  
**Version**: 1.0

## Entities

### 1. Grid

**Description**: A 2D rectangular structure representing the warehouse floor layout

**Implementation**: List of strings (each string is a row)

**Fields**:

- `rows`: List[str] - Each element is a row of the grid
- `height`: int - Number of rows (derived: `len(rows)`)
- `width`: int - Number of columns (derived: `len(rows[0])` if rows exist)

**Validation Rules**:

- Grid must be rectangular (all rows same length)
- Grid must contain only '@' (paper roll) and '.' (empty space) characters
- Grid may be empty (0 rows) - edge case

**State Transitions**: None (immutable after parsing)

**Example**:

```python
# Internal representation
grid = [
    "..@@.@@@@.",
    "@@@.@.@.@@",
    # ... more rows
]
height = 10
width = 10
```

---

### 2. Position

**Description**: A coordinate location in the grid

**Implementation**: Tuple of integers (row, col)

**Fields**:

- `row`: int - Zero-based row index (0 to height-1)
- `col`: int - Zero-based column index (0 to width-1)

**Validation Rules**:

- Row must be >= 0 and < grid height
- Column must be >= 0 and < grid width
- Out-of-bounds positions are considered empty (not containing paper rolls)

**Example**:

```python
position = (0, 2)  # Row 0, Column 2
```

---

### 3. PaperRoll

**Description**: A paper roll entity located at a specific position in the grid

**Implementation**: Implicit (identified by '@' character at position)

**Fields**:

- `position`: Position (row, col) - Location of the paper roll
- `adjacent_count`: int - Number of paper rolls in adjacent positions (computed)
- `is_accessible`: bool - Accessibility status (computed: adjacent_count < 4)

**Derived Properties**:

- `adjacent_count`: Computed by checking 8 surrounding positions
- `is_accessible`: True if adjacent_count < 4, False otherwise

**Validation Rules**:

- Position must contain '@' character in grid
- Adjacent count must be between 0 and 8 (inclusive)

**State Transitions**: None (properties computed on-demand)

**Example**:

```python
# Logical representation (not stored as object)
paper_roll = {
    'position': (0, 2),
    'adjacent_count': 2,
    'is_accessible': True  # 2 < 4
}
```

---

### 4. Direction

**Description**: One of 8 possible adjacent positions relative to a center position

**Implementation**: Tuple of offset values (delta_row, delta_col)

**Values** (constant):

```python
DIRECTIONS = [
    (-1, -1),  # Northwest
    (-1,  0),  # North
    (-1,  1),  # Northeast
    ( 0, -1),  # West
    ( 0,  1),  # East
    ( 1, -1),  # Southwest
    ( 1,  0),  # South
    ( 1,  1),  # Southeast
]
```

**Usage**: Applied to a position to get adjacent position

```python
adjacent_row = row + direction[0]
adjacent_col = col + direction[1]
```

---

### 5. AccessibilityResult

**Description**: The final output containing the count of accessible paper rolls

**Implementation**: Integer value

**Fields**:

- `count`: int - Total number of accessible paper rolls in the grid

**Validation Rules**:

- Count must be >= 0
- Count must be <= total number of paper rolls in grid

**Example**:

```python
result = 13  # For the example grid
```

---

## Data Flow

```
Input String (multiline)
    ↓
[Parse into Grid]
    ↓
Grid (List[str])
    ↓
[Find all '@' positions] → List[Position]
    ↓
[For each Position]
    ↓
[Count adjacent '@' in 8 directions] → adjacent_count
    ↓
[Check if adjacent_count < 4] → is_accessible
    ↓
[Sum all is_accessible] → AccessibilityResult
    ↓
Output: int (count)
```

---

## Function Signatures

Based on the data model, the following functions are required:

```python
def parse_grid(input_data: str) -> List[str]:
    """Parse input string into grid representation.

    Args:
        input_data: Multiline string containing grid

    Returns:
        List of strings, each representing a row
    """
    pass

def is_valid_position(grid: List[str], row: int, col: int) -> bool:
    """Check if position is within grid boundaries.

    Args:
        grid: The grid representation
        row: Row index to check
        col: Column index to check

    Returns:
        True if position is valid, False otherwise
    """
    pass

def count_adjacent_rolls(grid: List[str], row: int, col: int) -> int:
    """Count paper rolls in 8 adjacent positions.

    Args:
        grid: The grid representation
        row: Row index of center position
        col: Column index of center position

    Returns:
        Number of adjacent paper rolls (0-8)
    """
    pass

def is_accessible(adjacent_count: int) -> bool:
    """Determine if a paper roll is accessible.

    Args:
        adjacent_count: Number of adjacent paper rolls

    Returns:
        True if accessible (< 4 neighbors), False otherwise
    """
    pass

def solve_part1(input_data: str) -> int:
    """Solve Day 4 Part 1: Count accessible paper rolls.

    Args:
        input_data: Multiline string containing grid

    Returns:
        Count of accessible paper rolls
    """
    pass
```

---

## Constraints & Invariants

1. **Grid Rectangularity**: All rows must have the same length
2. **Character Set**: Grid contains only '@' and '.' characters (and whitespace for parsing)
3. **Accessibility Threshold**: A roll is accessible iff adjacent_count < 4 (strictly less than)
4. **Direction Count**: Always check exactly 8 directions for each paper roll
5. **Boundary Handling**: Out-of-bounds positions are treated as empty (not paper rolls)
6. **Immutability**: Grid data is not modified during processing

---

## Example Walkthrough

**Input**:

```
..@@.@@@@.
@@@.@.@.@@
```

**Parsing**:

```python
grid = ["..@@.@@@@.", "@@@.@.@.@@"]
height = 2
width = 10
```

**Paper Roll at (0, 2)**:

- Position: (0, 2)
- Adjacent positions to check:
  - (-1, 1), (-1, 2), (-1, 3): Out of bounds → 0 rolls
  - (0, 1): '.' → 0 rolls
  - (0, 3): '@' → 1 roll ✓
  - (1, 1), (1, 2), (1, 3): '@', '@', '@' → 3 rolls ✓
- Adjacent count: 1 + 3 = 4
- Is accessible: False (4 is NOT < 4)

**Paper Roll at (0, 3)**:

- Adjacent positions: (0,2)='@', (0,4)='.', (1,2)='@', (1,3)='.', (1,4)='@'
- Adjacent count: 3
- Is accessible: True (3 < 4) ✓

---

## Testing Considerations

From the data model, the following test cases should be created:

1. **Grid Parsing**: Verify grid is correctly split into rows
2. **Position Validation**: Test boundary checks (corners, edges, valid interior)
3. **Adjacent Counting**:
   - Roll with 0 neighbors
   - Roll with 1-3 neighbors (accessible)
   - Roll with 4-8 neighbors (not accessible)
   - Rolls at edges and corners
4. **Accessibility Logic**: Verify threshold at 3 vs 4 neighbors
5. **Full Integration**: Example grid expecting 13 accessible rolls
