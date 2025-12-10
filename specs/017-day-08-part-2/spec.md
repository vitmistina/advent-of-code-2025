# Feature Specification: AoC Day 8 Part 2 - Complete Circuit Formation

**Feature Branch**: `017-day-08-part-2`  
**Created**: December 10, 2025  
**Status**: Draft  
**Input**: User description: "AoC Day 8 Part 2 solution"

## User Scenarios & Testing _(mandatory)_

### User Story 1 - Find Final Connection to Unite All Circuits (Priority: P1)

A solver working on Advent of Code Day 8 Part 2 needs to determine which pair of junction boxes, when connected, causes all junction boxes to form a single unified circuit, and then calculate the product of their X coordinates.

**Why this priority**: This is the core requirement of Part 2 - finding the specific connection that completes the entire circuit and computing the required answer.

**Independent Test**: Can be fully tested by providing junction box coordinates, simulating connections until all boxes are in one circuit, and verifying the X-coordinate product of the final connecting pair matches expected output.

**Acceptance Scenarios**:

1. **Given** a list of 20 junction boxes from the example, **When** the solver connects pairs in order of increasing distance until all form one circuit, **Then** the final connection is between boxes at (216,146,977) and (117,168,530), and the product of X coordinates (216 × 117) equals 25272.

2. **Given** the full puzzle input with many junction boxes, **When** the solver processes connections sequentially by distance, **Then** the system identifies the exact pair that unifies all circuits and computes their X-coordinate product.

3. **Given** junction boxes that form multiple separate circuits, **When** each connection is made, **Then** the system accurately tracks which circuits merge and continues until only one circuit remains.

---

### User Story 2 - Track Circuit Membership During Connection Process (Priority: P2)

A solver needs the system to accurately track which junction boxes belong to which circuit throughout the connection process, so that redundant connections (boxes already in the same circuit) are identified and skipped.

**Why this priority**: Essential for correct operation - the algorithm must avoid counting connections between boxes already in the same circuit and must correctly merge circuits when different circuits connect.

**Independent Test**: Can be tested by tracking circuit membership after each connection and verifying that boxes in the same circuit are not reconnected, and that merging two circuits correctly combines all members.

**Acceptance Scenarios**:

1. **Given** two junction boxes already in the same circuit, **When** they are identified as the next closest pair, **Then** no connection occurs and the circuit count remains unchanged.

2. **Given** two junction boxes in different circuits, **When** they are connected, **Then** all boxes from both circuits merge into a single circuit.

3. **Given** a connection sequence, **When** processing each pair, **Then** the system maintains accurate circuit membership for all junction boxes at every step.

---

### User Story 3 - Process Connections in Distance Order (Priority: P2)

A solver needs junction box pairs to be processed in order of increasing Euclidean distance, so that the algorithm follows the problem's requirement to connect closest pairs first.

**Why this priority**: Critical for correctness - the problem explicitly requires connecting pairs in order of proximity, and the final answer depends on following this sequence.

**Independent Test**: Can be tested by verifying that calculated distances are sorted correctly and pairs are processed in ascending distance order.

**Acceptance Scenarios**:

1. **Given** a list of junction boxes with calculated pairwise distances, **When** the solver processes connections, **Then** each connection uses the shortest remaining distance between boxes not yet in the same circuit.

2. **Given** multiple pairs with different distances, **When** distances are calculated, **Then** Euclidean distance (√((x₂-x₁)² + (y₂-y₁)² + (z₂-z₁)²)) is used for all comparisons.

---

### Edge Cases

- What happens when all junction boxes start in one circuit? (Answer: already complete, no connections needed)
- What happens when there are only 2 junction boxes? (Answer: single connection unifies them)
- How does the system handle very large coordinate values without overflow?
- What if multiple pairs have identical distances? (Process in any stable order)
- How are ties broken when distances are equal? (Use consistent ordering, e.g., by coordinate values)

## Requirements _(mandatory)_

### Functional Requirements

- **FR-001**: System MUST parse input containing junction box 3D coordinates in X,Y,Z format (one per line).

- **FR-002**: System MUST calculate Euclidean distance between all pairs of junction boxes using the formula: √((x₂-x₁)² + (y₂-y₁)² + (z₂-z₁)²).

- **FR-003**: System MUST maintain circuit membership tracking such that each junction box belongs to exactly one circuit at any given time.

- **FR-004**: System MUST process junction box pairs in ascending order of distance.

- **FR-005**: System MUST skip connections between junction boxes that are already in the same circuit.

- **FR-006**: System MUST merge circuits when connecting junction boxes from different circuits, combining all members.

- **FR-007**: System MUST continue connecting pairs until all junction boxes belong to a single unified circuit.

- **FR-008**: System MUST identify the specific pair of junction boxes whose connection completes the final circuit unification.

- **FR-009**: System MUST calculate and output the product of the X coordinates of the two junction boxes in the final connection.

- **FR-010**: System MUST handle the example input correctly, producing 25272 as the answer.

### Key Entities

- **Junction Box**: A point in 3D space represented by X, Y, Z integer coordinates.
- **Circuit**: A set of junction boxes that are electrically connected (directly or indirectly through other boxes).
- **Connection**: A pair of junction boxes connected by a string of lights, enabling electrical flow between them.
- **Distance**: The Euclidean distance between two junction boxes in 3D space.

## Success Criteria _(mandatory)_

### Measurable Outcomes

- **SC-001**: System correctly processes the example input (20 junction boxes) and outputs 25272.

- **SC-002**: System accurately identifies when all junction boxes have unified into a single circuit.

- **SC-003**: System processes the full puzzle input and produces the correct answer within reasonable time (under 60 seconds for typical input sizes).

- **SC-004**: System correctly handles all edge cases including minimal inputs (2 boxes) and large coordinate values.

- **SC-005**: The calculated X-coordinate product matches the expected Advent of Code answer when submitted.
