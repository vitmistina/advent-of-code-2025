# Feature Specification: Day 1 Part 2 Solution

**Feature Branch**: `005-day-01-part-2`  
**Created**: December 1, 2025  
**Status**: Draft  
**Input**: User description: "Count how many times any click causes the dial to point at 0 during or after rotations (password method 0x434C49434B)"

## User Scenarios & Testing _(mandatory)_

### User Story 1 - Count All Zero Crossings (Priority: P1)

As a user, I want to count every time the dial points at 0 during any click (not just at the end of rotations), so I can use password method 0x434C49434B to unlock the door.

**Why this priority**: This is the core requirement for Part 2 and the only way to solve the puzzle using the new password method.

**Independent Test**: Can be fully tested by providing the sample input and verifying the correct count of all zero crossings (both during and after rotations) is returned.

**Acceptance Scenarios**:

1. **Given** the dial starts at 50, **When** the user provides the sample input with password method 0x434C49434B, **Then** the system returns 6 as the result (3 at end of rotations + 3 during rotations).

2. **Given** the dial starts at 50 and is rotated L68, **When** counting all clicks during rotation, **Then** the dial crosses 0 once during the rotation (at position 0) and ends at 82, contributing 1 to the total count.

3. **Given** the dial is at 82 and is rotated L30, **When** counting all clicks during rotation, **Then** the dial does not cross 0 during rotation and ends at 52, contributing 0 to the total count.

4. **Given** the dial is at 52 and is rotated R48, **When** counting all clicks during rotation, **Then** the dial does not cross 0 during rotation but ends at 0, contributing 1 to the total count (end position only).

5. **Given** the dial is at 0 and is rotated L5, **When** counting all clicks during rotation, **Then** the dial does not cross 0 again during rotation (starts at 0, moves away) and ends at 95, contributing 0 to the total count.

6. **Given** the dial is at 95 and is rotated R60, **When** counting all clicks during rotation, **Then** the dial crosses 0 once during the rotation and ends at 55, contributing 1 to the total count.

7. **Given** the dial is at 55 and is rotated L55, **When** counting all clicks during rotation, **Then** the dial does not cross 0 during rotation but ends at 0, contributing 1 to the total count (end position only).

8. **Given** the dial is at 0 and is rotated L1, **When** counting all clicks during rotation, **Then** the dial does not cross 0 again during rotation (starts at 0, moves away) and ends at 99, contributing 0 to the total count.

9. **Given** the dial is at 99 and is rotated L99, **When** counting all clicks during rotation, **Then** the dial does not cross 0 during rotation but ends at 0, contributing 1 to the total count (end position only).

10. **Given** the dial is at 0 and is rotated R14, **When** counting all clicks during rotation, **Then** the dial does not cross 0 again during rotation (starts at 0, moves away) and ends at 14, contributing 0 to the total count.

11. **Given** the dial is at 14 and is rotated L82, **When** counting all clicks during rotation, **Then** the dial crosses 0 once during the rotation (at position 0) and ends at 32, contributing 1 to the total count.

12. **Given** the complete sample sequence is processed, **When** counting all zero crossings (during + after rotations), **Then** the total count is 6 (positions after: 3, positions during: 3).

---

### User Story 2 - Handle Multi-Wrap Rotations (Priority: P2)

As a user, I want the system to correctly count multiple zero crossings when a single rotation wraps around the dial multiple times, so that large rotation distances are accurately processed.

**Why this priority**: Ensures correctness for edge cases where a single rotation crosses 0 multiple times (e.g., R1000 from position 50 crosses 0 ten times).

**Independent Test**: Can be tested by providing a rotation that wraps multiple times and verifying the count of zero crossings during that rotation.

**Acceptance Scenarios**:

1. **Given** the dial is at position 50, **When** the user provides rotation R1000, **Then** the system counts 10 zero crossings during the rotation (1000 clicks, wrapping through 0 ten times) before ending at 50.

2. **Given** the dial is at position 0, **When** the user provides rotation R100, **Then** the system counts 1 zero crossing (lands on 0 at the end) for a total of 1.

3. **Given** the dial is at position 50, **When** the user provides rotation L150, **Then** the system counts 2 zero crossings during the rotation (crosses 0 twice while going left 150 clicks) before ending at position 0, plus 1 for ending at 0, total 3.

---

### User Story 3 - Maintain Backward Compatibility (Priority: P3)

As a user, I want to still be able to use the Part 1 method (count only end positions), so I can verify both password methods work correctly.

**Why this priority**: Supports validation and ensures Part 1 solution remains functional while Part 2 is implemented.

**Independent Test**: Can be tested by running Part 1 logic separately and verifying it still returns the original answer.

**Acceptance Scenarios**:

1. **Given** the sample input, **When** using Part 1 method (count only end positions at 0), **Then** the system returns 3.

2. **Given** the sample input, **When** using Part 2 method (count all clicks at 0), **Then** the system returns 6.

3. **Given** any input, **When** running both methods, **Then** Part 2 count >= Part 1 count (since Part 2 includes all Part 1 counts plus additional during-rotation counts).

---

### Edge Cases

- What happens when the rotation distance is 0? (Should not add any counts, dial stays at current position)
- What happens when starting at position 0? (Should not double-count the starting position when rotating away)
- How does the system handle rotations that wrap exactly N times (e.g., R100, R200)? (Each complete wrap crosses 0 once)
- What if the dial starts at 0 and rotates to 0? (Count depends on whether 0 is crossed during rotation)
- How does direction affect zero crossing count? (Left and right rotations wrap differently but should count zeros the same way)
- What happens with very large distances (e.g., R10000)? (Should correctly count all crossings without overflow)

## Requirements _(mandatory)_

### Functional Requirements

- **FR-001**: System MUST count every click where the dial points at position 0, including both during rotations and at the end of rotations.

- **FR-002**: System MUST correctly handle rotations where the dial wraps around multiple times (e.g., R1000 crosses 0 ten times from position 50).

- **FR-003**: System MUST NOT double-count position 0 when the dial starts at 0 and rotates away (starting position is not counted).

- **FR-004**: System MUST count position 0 when the dial ends at 0 after a rotation (end position counts).

- **FR-005**: System MUST handle both left (L) and right (R) rotations when counting zero crossings during rotation.

- **FR-006**: System MUST maintain backward compatibility with Part 1 solution (solve_part1 function should remain unchanged).

- **FR-007**: System MUST process the same input format as Part 1 (sequence of rotation instructions, one per line).

- **FR-008**: For rotations that cross 0 during the rotation, system MUST calculate how many times 0 is crossed based on start position, direction, and distance.

### Key Entities _(include if feature involves data)_

- **Rotation Instruction**: Represents a single rotation with direction (L or R) and distance (integer >= 0) - same as Part 1.

- **Zero Crossing**: Represents each instance where the dial points at 0, which can occur:

  - During a rotation (intermediate positions)
  - At the end of a rotation (final position)

- **Dial State**: Represents the current position of the dial (0-99) and tracks:
  - Total count of all zero crossings (Part 2)
  - Count of zero end-positions (Part 1, for backward compatibility)

## Success Criteria _(mandatory)_

### Measurable Outcomes

- **SC-001**: Users receive the correct count of all zero crossings for the sample input, matching the puzzle description (6 total: 3 at end + 3 during rotations).

- **SC-002**: System correctly counts multiple zero crossings for single rotations with large distances (e.g., R1000 from position 50 returns 10 crossings).

- **SC-003**: Part 1 solution remains functional and returns correct answer (3 for sample input) when solve_part1 is called.

- **SC-004**: Part 2 solution returns count >= Part 1 count for any input (since all end-position zeros are included in total crossings).

- **SC-005**: System processes rotations in under 2 seconds even with very large distances (e.g., 10,000 rotations with distances up to 10,000).

- **SC-006**: 100% of acceptance scenarios in User Scenarios & Testing are independently verifiable.
