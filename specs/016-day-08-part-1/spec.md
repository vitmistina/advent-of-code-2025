# Feature Specification: AoC Day 8 Part 1 - Circuit Analysis

**Feature Branch**: `016-day-08-part-1`  
**Created**: December 10, 2025  
**Status**: Draft  
**Input**: User description: "Solve AoC Day 8 Part 1: Circuit Analysis using Union-Find"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Parse Junction Box Coordinates (Priority: P1)

A solver needs to read the puzzle input file and extract the 3D coordinates of all junction boxes for processing.

**Why this priority**: Without parsing input, no analysis can be performed. This is the foundational capability that all other features depend on.

**Independent Test**: Can be tested by loading input and verifying all junction boxes are correctly extracted with their X, Y, Z coordinates.

**Acceptance Scenarios**:

1. **Given** a puzzle input file with junction box coordinates, **When** the file is parsed, **Then** all junction boxes are extracted with accurate X, Y, Z values
2. **Given** valid coordinate format (numbers separated by commas), **When** parsed, **Then** coordinates are stored as numeric values ready for distance calculations
3. **Given** an input file, **When** parsed, **Then** the count of junction boxes matches the number of lines in the input

---

### User Story 2 - Calculate Euclidean Distances (Priority: P1)

A solver needs to compute the straight-line (Euclidean) distances between all pairs of junction boxes.

**Why this priority**: Distance calculation is essential for identifying the closest pairs that should be connected. This is critical to the algorithm.

**Independent Test**: Can be tested with known coordinate pairs (e.g., boxes at (0,0,0) and (3,4,0) should have distance 5) and verifying results match expected values.

**Acceptance Scenarios**:

1. **Given** two junction boxes with known coordinates, **When** distance is calculated, **Then** it matches the Euclidean distance formula: √((x₂-x₁)² + (y₂-y₁)² + (z₂-z₁)²)
2. **Given** the example data (162,817,812 and 425,690,689), **When** distance is calculated, **Then** it equals the expected minimum distance
3. **Given** all junction box pairs, **When** distances are calculated, **Then** results can be sorted by distance for connection prioritization

---

### User Story 3 - Connect Closest Pairs Using Union-Find (Priority: P1)

A solver needs to repeatedly connect the two closest junction boxes that aren't already in the same circuit, up to 1000 connections.

**Why this priority**: This is the core algorithm that determines the final circuit sizes. It directly produces the answer.

**Independent Test**: Can be tested with the example data by verifying that after 10 connections, the circuit distribution matches the expected state (one circuit of 5 boxes, one of 4, two of 2, and seven of 1).

**Acceptance Scenarios**:

1. **Given** unpaired junction boxes, **When** the closest pair is selected, **Then** they are connected regardless of whether they're in separate circuits
2. **Given** boxes already in the same circuit, **When** they would be the next closest pair, **Then** they are skipped and the algorithm moves to the next closest unprocessed pair
3. **Given** the requirement to make 1000 connections, **When** executed, **Then** all 1000 closest unique pairs are processed (or fewer if all boxes become connected)
4. **Given** the example with 10 connections, **When** circuits are formed, **Then** resulting sizes are [5, 4, 2, 2, 1, 1, 1, 1, 1, 1, 1]

---

### User Story 4 - Calculate Circuit Sizes and Identify Largest Three (Priority: P1)

A solver needs to determine the size of each circuit after all connections are made, then identify the three largest circuits.

**Why this priority**: This produces the final answer by multiplying the three largest circuit sizes together.

**Independent Test**: Can be tested by creating circuits of known sizes and verifying the three largest are correctly identified and multiplied.

**Acceptance Scenarios**:

1. **Given** connected junction boxes, **When** circuit sizes are calculated, **Then** each box belongs to exactly one circuit
2. **Given** the example after 10 connections with circuits [5, 4, 2, 2, 1, 1, 1, 1, 1, 1, 1], **When** the three largest are identified, **Then** they are [5, 4, 2]
3. **Given** the three largest circuits, **When** multiplied together, **Then** the result is 40 for the example
4. **Given** the full puzzle with 1000 connections, **When** the three largest circuits are multiplied, **Then** the correct answer is produced

---

### Edge Cases

- What happens if two pairs of boxes have identical distances? (Process in consistent order, e.g., by index)
- How does the system handle the case where all junction boxes become part of a single circuit before 1000 connections? (Stop processing and calculate from final state)
- What if the input contains duplicate coordinates? (Treat as separate boxes; they can't be connected to themselves)
- What if fewer than 3 circuits remain? (Include all remaining circuits in the multiplication)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST parse the puzzle input file and extract all junction box coordinates as (X, Y, Z) tuples
- **FR-002**: System MUST calculate the Euclidean distance between every pair of junction boxes using the formula: √((x₂-x₁)² + (y₂-y₁)² + (z₂-z₁)²)
- **FR-003**: System MUST maintain a Union-Find data structure to track which junction boxes belong to the same circuit
- **FR-004**: System MUST identify the closest pair of junction boxes that are not already in the same circuit
- **FR-005**: System MUST connect pairs iteratively, starting with the closest pairs, up to 1000 connections or until all boxes form a single circuit
- **FR-006**: System MUST skip any pair that is already connected (in the same circuit) when determining the next closest pair to connect
- **FR-007**: System MUST calculate the size of each distinct circuit after all connections are made
- **FR-008**: System MUST identify the three largest circuits by size
- **FR-009**: System MUST compute the product of the three largest circuit sizes and return it as the final answer
- **FR-010**: System MUST produce output that can be verified against the example (answer of 40 for the provided example)

### Key Entities *(include if feature involves data)*

- **Junction Box**: Represents a location in 3D space with coordinates (X, Y, Z). Attributes: id, x_coordinate, y_coordinate, z_coordinate
- **Connection**: A link between two junction boxes. Attributes: box1_id, box2_id, distance
- **Circuit**: A group of junction boxes connected through chains of connections. Attributes: boxes (set of box IDs), size (count of boxes)
- **Distance Pair**: A pair of boxes with their calculated distance. Attributes: box1_id, box2_id, distance_value

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Solution correctly produces output of 40 for the provided example with 20 junction boxes
- **SC-002**: Solution can process 1000 connections from a large input set (1000+ junction boxes) in reasonable time (under 5 seconds)
- **SC-003**: Solution correctly identifies and connects the closest pairs: the first connection should be between boxes at (162,817,812) and (425,690,689) in the example
- **SC-004**: After 10 connections in the example, circuit sizes are [5, 4, 2, 2, 1, 1, 1, 1, 1, 1, 1] as specified
- **SC-005**: No junction boxes are lost or duplicated during the connection process; the total count of boxes across all circuits always equals the initial count
- **SC-006**: Solution handles edge case where all boxes become connected before 1000 connections without error

## Assumptions

- Input file format is CSV-style with one junction box per line in the format `X,Y,Z` where X, Y, Z are integers
- Union-Find implementation will use path compression and/or union by rank for efficiency
- Distance calculations use floating-point arithmetic; ties in distances are broken consistently (e.g., by box index order)
- "Circuit" is defined by connectivity: boxes are in the same circuit if there is a path of connections between them
- The puzzle input will contain valid, non-duplicate coordinates
