# Feature Specification: Day 4 Part 1 - Accessible Paper Rolls Counter

**Feature Branch**: `011-day-04-part-1`  
**Created**: 2025-12-04  
**Status**: Draft  
**Input**: User description: "Solve Day 4 Part 1: Count accessible paper rolls on a grid where a roll is accessible if fewer than 4 rolls exist in its 8 adjacent positions"

## User Scenarios & Testing _(mandatory)_

### User Story 1 - Parse Grid and Identify Paper Rolls (Priority: P1)

As a solver, I need the system to read a grid representation and identify the positions of all paper rolls so that I can determine which ones are accessible.

**Why this priority**: This is the foundation requirement - without reading the grid and identifying paper rolls, no further analysis can occur. This represents the minimum viable functionality.

**Independent Test**: Can be fully tested by providing a sample grid input and verifying that all paper roll positions (@) are correctly identified and their coordinates are accurate.

**Acceptance Scenarios**:

1. **Given** a grid with paper rolls marked as '@' and empty spaces as '.', **When** the system parses the grid, **Then** all paper roll positions are correctly identified with their row and column coordinates
2. **Given** a grid with mixed '@' and '.' characters, **When** the system processes the grid, **Then** empty positions are ignored and only paper rolls are tracked
3. **Given** an empty grid (all '.'), **When** the system parses it, **Then** zero paper rolls are identified

---

### User Story 2 - Count Adjacent Paper Rolls (Priority: P2)

As a solver, I need the system to count the number of paper rolls in the 8 adjacent positions (horizontally, vertically, and diagonally) for each paper roll so that accessibility can be determined.

**Why this priority**: This is the core calculation logic. It builds on P1 and enables the final count, but can be tested independently by checking adjacency counts for specific positions.

**Independent Test**: Can be tested independently by providing a grid and verifying the adjacency count for each paper roll position matches the expected count of neighboring '@' symbols in all 8 directions.

**Acceptance Scenarios**:

1. **Given** a paper roll at position (r, c), **When** the system counts adjacent rolls, **Then** all 8 positions (N, NE, E, SE, S, SW, W, NW) are checked
2. **Given** a paper roll at the edge of the grid, **When** counting adjacent rolls, **Then** positions outside the grid boundaries are treated as empty (not paper rolls)
3. **Given** a paper roll at a corner position, **When** counting adjacent rolls, **Then** only the 3 valid adjacent positions within the grid are checked
4. **Given** a paper roll surrounded by 8 other paper rolls, **When** counting adjacent rolls, **Then** the count is 8

---

### User Story 3 - Determine Accessibility and Count Results (Priority: P3)

As a solver, I need the system to identify which paper rolls are accessible (fewer than 4 adjacent rolls) and provide the total count so that I can answer the puzzle question.

**Why this priority**: This is the final output step that delivers the answer. It depends on P1 and P2 but can be tested independently by verifying the accessibility rule and final count.

**Independent Test**: Can be tested independently by providing adjacency counts for each roll and verifying that only rolls with fewer than 4 neighbors are counted as accessible, and the total is accurate.

**Acceptance Scenarios**:

1. **Given** a paper roll with 0 adjacent rolls, **When** determining accessibility, **Then** it is marked as accessible
2. **Given** a paper roll with 3 adjacent rolls, **When** determining accessibility, **Then** it is marked as accessible
3. **Given** a paper roll with 4 adjacent rolls, **When** determining accessibility, **Then** it is NOT marked as accessible
4. **Given** a paper roll with 8 adjacent rolls, **When** determining accessibility, **Then** it is NOT marked as accessible
5. **Given** the complete grid from the example, **When** counting all accessible rolls, **Then** the result is 13

---

### Test Scenario - Example Grid

**Input Grid**:

```
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
```

**Expected Output**: 13 accessible paper rolls

**Expected Accessible Positions** (marked with 'x' in visual representation):

```
..xx.xx@x.
x@@.@.@.@@
@@@@@.x.@@
@.@@@@..@.
x@.@@@@.@x
.@@@@@@@.@
.@.@.@.@@@
x.@@@.@@@@
.@@@@@@@@.
x.x.@@@.x.
```

**Verification Details**:

- Total paper rolls in grid: 37
- Accessible paper rolls (< 4 neighbors): 13
- Non-accessible paper rolls (≥ 4 neighbors): 24
- Grid dimensions: 10 rows × 10 columns

**Example Accessibility Calculations**:

- Position (0,2) '@': Has 2 neighbors → Accessible (marked 'x')
- Position (0,3) '@': Has 4 neighbors → Not accessible (stays '@')
- Position (1,0) '@': Has 1 neighbor → Accessible (marked 'x')
- Position (2,2) '@': Has 8 neighbors → Not accessible (stays '@')

---

### Edge Cases

- How does the system handle very large grids efficiently?
- What happens with paper rolls at grid boundaries (edges and corners)?
  - Answer: They count only valid adjacent positions within the grid.

## Requirements _(mandatory)_

### Functional Requirements

- **FR-001**: System MUST read a grid input where '@' represents paper rolls and '.' represents empty space
- **FR-002**: System MUST identify all paper roll positions in the grid with their coordinates
- **FR-003**: System MUST examine all 8 adjacent positions (N, NE, E, SE, S, SW, W, NW) for each paper roll
- **FR-004**: System MUST treat positions outside grid boundaries as empty (not containing paper rolls)
- **FR-005**: System MUST count the number of paper rolls in the 8 adjacent positions for each roll
- **FR-006**: System MUST classify a paper roll as "accessible" if fewer than 4 paper rolls exist in its adjacent positions
- **FR-007**: System MUST classify a paper roll as "not accessible" if 4 or more paper rolls exist in its adjacent positions
- **FR-008**: System MUST count the total number of accessible paper rolls across the entire grid
- **FR-009**: System MUST handle grids of any rectangular dimensions
- **FR-010**: System MUST produce the correct answer of 13 for the provided example grid

### Key Entities _(include if feature involves data)_

- **Grid**: A 2D rectangular structure containing positions that are either empty or contain paper rolls
- **Paper Roll**: An object marked with '@' in the grid, located at specific row and column coordinates
- **Adjacent Position**: One of 8 positions (N, NE, E, SE, S, SW, W, NW) surrounding a given position in the grid
- **Accessibility Status**: A boolean classification indicating whether a paper roll can be accessed by forklifts (true if adjacent count < 4)

## Success Criteria _(mandatory)_

### Measurable Outcomes

- **SC-001**: System correctly identifies all 37 paper rolls in the example grid (10x10 grid with the specified pattern)
- **SC-002**: System produces the correct answer of 13 accessible paper rolls for the example input
- **SC-003**: System correctly counts adjacent rolls for edge positions (accounting for boundary conditions)
- **SC-004**: System correctly counts adjacent rolls for corner positions (checking only 3 adjacent positions)
- **SC-005**: System handles the full puzzle input and produces a numeric answer within reasonable time (under 1 second for typical grid sizes)
- **SC-006**: All test scenarios pass including edge cases (empty grid, single roll, all accessible, none accessible)

## Assumptions

- The grid is always rectangular (all rows have the same length)
- Input is well-formed (only contains '@' and '.' characters, plus newlines)
- The threshold for accessibility is strictly "fewer than 4" (meaning 0, 1, 2, or 3 adjacent rolls)
- The 8 adjacent positions include all horizontal, vertical, and diagonal neighbors
- Grid coordinates use standard row-column indexing (0-based or 1-based, to be determined during implementation)
- The example grid is 10x10 based on the provided input
- Performance requirements are reasonable for typical Advent of Code grid sizes (up to hundreds of rows/columns)
