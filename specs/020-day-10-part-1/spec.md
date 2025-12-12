# Feature Specification: AoC Day 10 Part 1 - Factory Machine Initialization

**Feature Branch**: `020-day-10-part-1`  
**Created**: December 11, 2025  
**Status**: Draft  
**Input**: User description: "AoC Day 10 Part 1"

## User Scenarios & Testing _(mandatory)_

### User Story 1 - Parse Machine Configuration (Priority: P1)

As a solver, I need to parse each machine's configuration line to extract the indicator light target state, button wiring, and joltage requirements (ignored for Part 1), so that I can work with the machine data.

**Why this priority**: This is the foundational capability - without parsing, no other functionality is possible. It's the entry point for all problem-solving.

**Independent Test**: Can be fully tested by providing a single machine configuration line and verifying correct extraction of all three components (indicator lights, buttons, joltage).

**Acceptance Scenarios**:

1. **Given** a simple machine configuration `[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}`, **When** parsing the line, **Then** extract 4 indicator lights with target state [off, on, on, off], 6 buttons with their respective toggle indices, and joltage values {3,5,4,7}
2. **Given** a machine with 5 indicator lights `[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}`, **When** parsing, **Then** correctly identify target state [off, off, off, on, off] and 5 buttons
3. **Given** a machine with 6 indicator lights `[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}`, **When** parsing, **Then** correctly identify target state [off, on, on, on, off, on] and 4 buttons
4. **Given** a button wiring `(0,3,4)`, **When** parsing, **Then** extract indices [0, 3, 4] representing the first, fourth, and fifth lights
5. **Given** an indicator light diagram `[.##.]`, **When** parsing, **Then** recognize `.` as off (0/false) and `#` as on (1/true)

---

### User Story 2 - Model Machine State (Priority: P1)

As a solver, I need to track the current state of a machine's indicator lights and apply button presses to toggle lights, so that I can simulate the machine's behavior.

**Why this priority**: This is core logic needed to simulate any solution. Without state tracking and toggle operations, we cannot test if a button sequence solves the problem.

**Independent Test**: Can be fully tested by initializing a machine with all lights off, applying a sequence of button presses, and verifying the final light states match expected values.

**Acceptance Scenarios**:

1. **Given** a machine with 5 lights all initially off `[.....] ` and button `(0,3,4)`, **When** pressing the button once, **Then** lights become `[#..##]` (positions 0, 3, 4 toggle from off to on)
2. **Given** a machine with lights in state `[#....]` and button `(0,3,4)`, **When** pressing the button once, **Then** lights become `[...##]` (position 0 toggles off, positions 3 and 4 toggle on)
3. **Given** a machine with 4 lights `[.##.]` and buttons `(0,2)` and `(0,1)`, **When** pressing `(0,2)` once and `(0,1)` once, **Then** lights reach target state `[.##.]`
4. **Given** any machine state, **When** pressing a button N times where N is even, **Then** the affected lights return to their original state
5. **Given** initial state `[....]` and target `[.##.]`, **When** applying button sequence [(1,3), (2,3), (0,1), (0,1)], **Then** final state matches target (from example: press (1,3) once, (2,3) once, (0,1) twice = 4 presses)

---

### User Story 3 - Find Minimum Button Presses for Single Machine (Priority: P1)

As a solver, I need to determine the minimum number of button presses required to configure a single machine's indicator lights from all-off to the target state, so that I can solve individual machines optimally.

**Why this priority**: This is the core optimization problem for a single machine. It delivers value immediately by solving the fundamental puzzle mechanic.

**Independent Test**: Can be fully tested by providing a single machine configuration and verifying the returned minimum press count matches known examples.

**Acceptance Scenarios**:

1. **Given** machine `[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}`, **When** finding minimum presses, **Then** return 2 (achieved by pressing (0,2) and (0,1) once each)
2. **Given** machine `[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}`, **When** finding minimum presses, **Then** return 3 (achieved by pressing last three buttons once each)
3. **Given** machine `[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}`, **When** finding minimum presses, **Then** return 2 (achieved by pressing (0,3,4) and (0,1,2,4,5) once each)
4. **Given** a machine where target state is all lights off, **When** finding minimum presses, **Then** return 0 (already at target)
5. **Given** a machine with only one button affecting all lights and target state with all lights on, **When** finding minimum presses, **Then** return 1

---

### User Story 4 - Solve Multiple Machines (Priority: P1)

As a solver, I need to calculate the sum of minimum button presses across all machines in the input, so that I can provide the final puzzle answer.

**Why this priority**: This is the final deliverable for Part 1 - the answer format specified by the problem.

**Independent Test**: Can be fully tested by providing a multi-line input with known individual minimums and verifying the total sum.

**Acceptance Scenarios**:

1. **Given** three example machines with minimum presses [2, 3, 2], **When** calculating total, **Then** return 7
2. **Given** actual puzzle input with N machines, **When** calculating total, **Then** sum all individual minimums correctly
3. **Given** input with 1 machine requiring 5 presses, **When** calculating total, **Then** return 5
4. **Given** empty input, **When** calculating total, **Then** return 0

---

### Edge Cases

- What happens when a button only affects lights that should remain off in target state? (May still be useful in combination)
- What happens with very large numbers of lights (e.g., 50+ lights)? (Algorithm must scale efficiently)

## Requirements _(mandatory)_

### Functional Requirements

- **FR-001**: System MUST parse indicator light diagrams from square brackets `[...]` where `.` represents off and `#` represents on
- **FR-002**: System MUST parse button wiring schematics from parentheses `(...)` where comma-separated integers represent light indices (0-indexed)
- **FR-003**: System MUST parse joltage requirements from curly braces `{...}` but ignore them for Part 1 calculations
- **FR-004**: System MUST initialize all indicator lights to off state before applying button presses
- **FR-005**: System MUST implement toggle operation where pressing a button flips each specified light (off→on or on→off)
- **FR-006**: System MUST support pressing each button an integer number of times (0, 1, 2, 3, ...)
- **FR-007**: System MUST determine the minimum total button presses needed to reach target state for each machine
- **FR-008**: System MUST sum the minimum presses across all machines to produce final answer
- **FR-009**: System MUST handle multiple machines (one per line) in the input
- **FR-010**: System MUST recognize that pressing a button twice returns affected lights to original state
- **FR-011**: System MUST validate that light indices in button wiring are within valid range (0 to num_lights-1)
- **FR-012**: System MUST handle machines with varying numbers of indicator lights (from test examples: 4, 5, 6 lights)
- **FR-013**: System MUST handle machines with varying numbers of buttons (from test examples: 6, 5, 4 buttons)

### Key Entities

- **Machine**: Represents one factory machine with its configuration

  - Initial state: all lights off
  - Target state: desired light configuration from diagram
  - Number of lights: determined by length of indicator diagram
  - Available buttons: list of button wirings

- **Button**: Represents a button wiring schematic

  - Affected lights: set of light indices that toggle when pressed
  - Press count: number of times this button is pressed in a solution

- **Light State**: Represents the current configuration of all indicator lights

  - Binary state for each light: on (true/1) or off (false/0)
  - Position: 0-indexed from left to right in diagram

- **Solution**: Represents a valid button press sequence
  - Press counts: how many times each button is pressed
  - Total presses: sum of all button press counts
  - Final state: resulting light configuration after applying all presses

## Success Criteria _(mandatory)_

### Measurable Outcomes

- **SC-001**: System correctly parses all three example machines from the problem description with 100% accuracy
- **SC-002**: System calculates minimum presses of 2, 3, and 2 for the three example machines respectively
- **SC-003**: System produces final sum of 7 for the example input
- **SC-004**: System solves actual puzzle input and produces correct answer accepted by AoC submission
- **SC-005**: System processes all machines in puzzle input (typically 100-1000 lines) within 30 seconds
- **SC-006**: Solution correctly handles edge case of target state being all-off (returns 0 presses)
- **SC-007**: System validation tests pass for all parsing, state transition, and optimization logic with 100% success rate

## Input Complexity Overview

- Example lines from actual puzzle input `day-10/input.txt`:
  - `[####..##.#] (2,3,5,7,8,9) (0,3,5,6,8) (1,3,7,8) (0,2,3,5) (1,2,3,4,5,6,7,8) (3,5,7) (9) (0,1,3,4,6,7,8) (0,1,2,3,4,5,7,9) (0,1,2,3,4,5,6,9) (5,8) (2,3,5) {47,30,68,91,24,97,20,46,53,53}`
  - `[.#.......] (0,1,2,4,5,6,7) (0,1,2,6,7,8) (0,1) (3,4,6) (1,3,4,5,6,8) (2,4,5) (0,1,2,3,4,5,6) (0,1,2,5,7) (0,1,2,3,4,6,7) (2,3,6,8) (0,1,2,4,6,7,8) {51,53,64,44,60,34,64,38,16}`
  - `[.#.#.#] (0,1,2,3,5) (1,3,5) (2,4,5) (3,4,5) (0,1,2,4) (0,3) {25,18,25,15,25,15}`
- Total number of lines in input: 160
- Observation: Machines vary widely in number of lights (4–10), and buttons per machine range from 2 to 13+, indicating high combinatorial diversity; joltage values are present but ignored.

## Assumptions

- Puzzle input is well-formed (valid syntax for brackets, parentheses, braces)
- Every machine in the puzzle input has a valid solution (can reach target state)
- Light indices in button wiring are always valid (within range 0 to num_lights-1)
- Joltage requirements can be safely ignored for Part 1
- Button press counts are non-negative integers
- Optimal solution exists using linear combination of button presses (this is a system of linear equations over GF(2))
- The problem is equivalent to solving a system of linear equations in modulo 2 arithmetic (Gaussian elimination over binary field)

## Dependencies

- Standard parsing libraries for string manipulation
- Linear algebra solving capability for binary systems (Gaussian elimination mod 2, or similar)
- Test framework for validation

## Out of Scope

- Joltage requirement processing (explicitly ignored per problem statement)
- Part 2 extensions (will be addressed in separate feature)
- Graphical visualization of light states
- Interactive button press simulation UI
- Performance optimization beyond reasonable limits (sub-second for typical inputs)
