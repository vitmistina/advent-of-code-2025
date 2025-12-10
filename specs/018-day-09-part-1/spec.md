# Feature Specification: AoC Day 9 Part 1 - Largest Red Tile Rectangle

**Feature Branch**: `018-day-09-part-1`  
**Created**: 2025-12-10  
**Status**: Draft  
**Input**: User description: "Find the largest rectangle that uses red tiles for two of its opposite corners in a grid"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Parse Red Tile Coordinates (Priority: P1)

The puzzle solver needs to read a list of red tile coordinates from the puzzle input and load them into a structured format that can be used for analysis.

**Why this priority**: This is the foundational step - without parsing the input data correctly, no further analysis is possible. This must work before any rectangle calculations.

**Independent Test**: Can be fully tested by loading the input file and verifying all coordinate pairs are correctly parsed and stored.

**Acceptance Scenarios**:

1. **Given** a puzzle input file with red tile coordinates in "x,y" format, **When** the input is parsed, **Then** each coordinate pair is extracted as a separate entry
2. **Given** coordinates like "7,1" and "11,7", **When** parsed, **Then** they are stored as tuples or coordinate objects with x=7, y=1 and x=11, y=7
3. **Given** the example input from the problem (8 red tiles), **When** parsed, **Then** all 8 coordinates are successfully loaded
4. **Given** empty or malformed input, **When** parsed, **Then** the system returns an error and halts execution

---

### User Story 2 - Calculate Rectangle Area for Any Two Tiles (Priority: P1)

The puzzle solver needs to calculate the area of a rectangle formed by any two red tiles used as opposite corners.

**Why this priority**: This is the core calculation required for the solution. Without the ability to compute rectangle areas, we cannot find the largest one.

**Independent Test**: Can be fully tested by providing any two coordinate pairs and verifying the area calculation is correct.

**Acceptance Scenarios**:

1. **Given** two red tiles at (2,5) and (9,7), **When** calculating rectangle area, **Then** the result is 24
2. **Given** two red tiles at (7,1) and (11,7), **When** calculating rectangle area, **Then** the result is 35
3. **Given** two red tiles at (7,3) and (2,3), **When** calculating rectangle area, **Then** the result is 6
4. **Given** two red tiles at (2,5) and (11,1), **When** calculating rectangle area, **Then** the result is 50
5. **Given** two distinct red tiles, **When** calculating rectangle area, **Then** the formula correctly handles tiles provided in any order (e.g., (2,5) and (11,1) gives same result as (11,1) and (2,5))

---

### User Story 3 - Find Largest Rectangle Across All Possible Pairs (Priority: P1)

The puzzle solver needs to efficiently check all possible pairs of red tiles and identify which pair forms the largest rectangle.

**Why this priority**: This is the final and most critical computation - it determines the answer to the puzzle.

**Independent Test**: Can be fully tested by running against the example input and verifying the result is 50.

**Acceptance Scenarios**:

1. **Given** the example input with 8 red tiles, **When** finding the largest rectangle, **Then** the result is 50
2. **Given** any set of red tiles, **When** finding the largest rectangle, **Then** all possible pairs (combinations of 2 distinct tiles) are evaluated
3. **Given** red tiles, **When** finding the largest rectangle, **Then** the result is the maximum area value only

---

### Edge Cases

- What happens when there are fewer than 2 red tiles? (Cannot form a rectangle)
- What happens when all red tiles are collinear (on the same line)? (All rectangles have zero or minimal area)
- What happens with very large coordinates or many tiles? (Performance and precision)
- What happens when multiple pairs of tiles produce the same maximum area? (Return any one, or all of them?)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST parse puzzle input containing red tile coordinates in "x,y" format
- **FR-002**: System MUST extract all coordinate pairs from the input
- **FR-003**: System MUST store red tile coordinates in a data structure enabling efficient lookup and iteration
- **FR-004**: System MUST calculate the rectangular area formed by any two tiles used as opposite corners using the formula: width × height = |x1 - x2| × |y1 - y2|
- **FR-005**: System MUST evaluate all possible pairs of distinct red tiles (combination algorithm, not permutation)
- **FR-006**: System MUST identify and return only the maximum area value found across all possible pairs
- **FR-007**: System MUST return an error when input is empty or malformed
- **FR-008**: System MUST handle the example input correctly and return area of 50

### Key Entities

- **Red Tile**: A coordinate point (x, y) in the grid, representing a location of a red tile
- **Rectangle**: A shape defined by two opposite corner tiles, with area calculated as width × height

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Parser correctly extracts all red tile coordinates from puzzle input with 100% accuracy
- **SC-002**: Rectangle area calculation produces correct results for all provided examples (areas of 24, 35, 6, 50)
- **SC-003**: Algorithm identifies the largest rectangle area of 50 from the example input
- **SC-004**: Solution completes for the full puzzle input in under 5 seconds (performance requirement)
- **SC-005**: Algorithm explores all possible pairs of tiles (for n tiles, evaluates n(n-1)/2 pairs)

## Assumptions

- Input coordinates are non-negative integers
- Coordinates follow standard Cartesian grid format (x,y)
- A rectangle's area is calculated as the absolute difference in x-coordinates multiplied by the absolute difference in y-coordinates
- Only distinct pairs of red tiles are evaluated (same tile cannot be used as both opposite corners)
- System returns an error and halts when encountering empty or malformed input
- Solution returns the maximum area value only (not the tile coordinates)
