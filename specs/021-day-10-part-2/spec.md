# Feature Specification: Day 10 Part 2 - Joltage Configuration Optimization

**Feature Branch**: `021-day-10-part-2`  
**Created**: 2025-12-12  
**Status**: Draft  
**Input**: User description: "Day 10 Part 2: Joltage Configuration Optimization"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Factory Technician Configures Single Machine Joltage (Priority: P1)

A factory technician needs to bring a single offline machine online by configuring its joltage counters to exact target levels. The machine has multiple buttons available, and pressing each button increments specific counters. The technician needs to determine the minimum number of button presses required to reach all target joltage levels simultaneously.

**Why this priority**: This is the core MVP - a technician must be able to solve a single machine problem to understand the system before handling multiple machines.

**Independent Test**: Can be fully tested by providing a single machine definition (buttons and target joltage requirements) and verifying the minimum button press count is correctly calculated.

**Acceptance Scenarios**:

1. **Given** a machine with buttons `(3)`, `(1,3)`, `(2)`, `(2,3)`, `(0,2)`, `(0,1)` and joltage targets `{3,5,4,7}`, **When** analyzing for minimum presses, **Then** the system returns `10` as the minimum total presses

2. **Given** a machine with buttons `(0,2,3,4)`, `(2,3)`, `(0,4)`, `(0,1,2)`, `(1,2,3,4)` and joltage targets `{7,5,12,7,2}`, **When** analyzing for minimum presses, **Then** the system returns `12` as the minimum total presses

3. **Given** a machine with buttons `(0,1,2,3,4)`, `(0,3,4)`, `(0,1,2,4,5)`, `(1,2)` and joltage targets `{10,11,11,5,10,5}`, **When** analyzing for minimum presses, **Then** the system returns `11` as the minimum total presses

### User Story 2 - Factory Manager Processes Multiple Machines (Priority: P1)

A factory manager receives a complete list of machines that need to be configured. Each machine has its own set of buttons and joltage requirements. The manager needs to determine the total minimum button presses across all machines to bring the entire factory online.

**Why this priority**: Essential for solving the actual problem - aggregating results across all machines in the input.

**Independent Test**: Can be tested with a multi-machine input file and verifying the sum of minimum presses for each machine equals the expected total.

**Acceptance Scenarios**:

1. **Given** three machines with known minimum presses of 10, 12, and 11 respectively, **When** processing the complete input, **Then** the system returns total minimum presses as `33` (10 + 12 + 11)

2. **Given** a machine definition file with multiple machines, **When** reading and parsing the file, **Then** each machine is correctly extracted with its buttons and joltage requirements

3. **Given** all machines processed, **When** generating output, **Then** both per-machine results and total aggregate result are provided

### User Story 3 - Algorithm Developer Optimizes Button Press Strategy (Priority: P2)

An algorithm developer needs to implement the core optimization logic that finds minimum button presses. The algorithm must handle multiple buttons, each affecting different sets of counters, with non-negative integer constraints and exact target matching.

**Why this priority**: Directly affects solution quality and performance. Part of MVP but distinct from data handling.

**Independent Test**: Can be tested independently with unit tests providing various button/target configurations and verifying minimum press counts.

**Acceptance Scenarios**:

1. **Given** a simple case with 2 buttons and 1 counter where button A increments counter 0 by 1, button B increments counter 0 by 2, and target is counter 0 = 5, **When** solving, **Then** system finds minimum 2 presses (press B twice for 4, press A once for total 5)

2. **Given** independent counters where buttons don't overlap, **When** solving, **Then** each counter is solved independently and results are combined

3. **Given** coupled counters where buttons affect multiple counters, **When** solving, **Then** the algorithm finds the globally optimal solution considering all constraints

### User Story 4 - Input Parser Extracts Machine Definitions (Priority: P1)

A data engineer needs to reliably parse the machine definition format. Each line contains button definitions in parentheses and joltage requirements in curly braces.

**Why this priority**: Critical for ingesting the problem input; without correct parsing, subsequent calculations fail.

**Independent Test**: Can be tested by parsing individual lines and verifying extracted button lists and joltage requirements match expected values.

**Acceptance Scenarios**:

1. **Given** input line `[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}`, **When** parsing, **Then** extract buttons: `[3]`, `[1,3]`, `[2]`, `[2,3]`, `[0,2]`, `[0,1]` and targets: `[3,5,4,7]`

2. **Given** input line `[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}`, **When** parsing, **Then** correctly extract 4 buttons and 6 joltage targets

3. **Given** malformed input with missing sections, **When** parsing, **Then** system provides clear error message identifying the issue

### User Story 5 - Test Validation Against Examples (Priority: P2)

A quality assurance engineer verifies the solution works correctly on the provided examples before running against the actual puzzle input. The problem statement includes three worked examples with known correct answers.

**Why this priority**: Provides confidence in the solution before attempting the actual puzzle.

**Independent Test**: Can validate the solution against three example machines and verify exact answer matches documented results.

**Acceptance Scenarios**:

1. **Given** the first example machine, **When** solving, **Then** result is exactly `10`

2. **Given** the second example machine, **When** solving, **Then** result is exactly `12`

3. **Given** the third example machine, **When** solving, **Then** result is exactly `11`

4. **Given** all three examples processed together, **When** summing results, **Then** total is exactly `33`

### Edge Cases

- What happens when a machine has a target of 0 (already at target)?
- What happens when buttons have overlapping counter effects?
- What if there are more buttons than needed (redundancy)?
- How does the system handle very large target numbers (hundreds or thousands)?
- What happens when a counter receives contributions from multiple buttons?
- Can the system handle machines with single-button, single-counter scenarios?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST parse each machine line to extract button definitions and joltage targets, ignoring indicator light diagrams

- **FR-002**: System MUST represent each button as a list of counter indices it affects (e.g., button `(1,3)` affects counters 1 and 3)

- **FR-003**: System MUST support joltage targets ranging from 0 to arbitrary large integers for each counter

- **FR-004**: System MUST find the minimum number of total button presses required to bring all counters from 0 to their exact target values simultaneously

- **FR-005**: System MUST handle machines with any number of buttons and counters, including buttons that affect overlapping sets of counters

- **FR-006**: System MUST reject non-integer press counts (fractional presses are invalid)

- **FR-007**: System MUST reject negative press counts (cannot press buttons backwards)

- **FR-008**: System MUST calculate per-machine minimum presses and aggregate total across all machines in the input

- **FR-009**: System MUST provide detailed solution breakdown showing which buttons to press and how many times for verification purposes

- **FR-010**: System MUST handle input files containing multiple machine definitions (one per line)

### Key Entities

- **Machine**: Represents a single factory machine with button collection, joltage targets, and solution details

- **Button**: Represents a physical button with identifier, affected counter indices, and press count in optimal solution

- **Counter**: Represents a joltage level tracker with index, target value, and current value during solving

- **PuzzleInput**: Represents the complete problem with collection of machines and total minimum presses

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Parser correctly extracts button definitions and joltage targets for all provided example machines (100% accuracy on three examples)

- **SC-002**: Solver returns minimum press count of exactly `10` for first example machine, `12` for second, `11` for third (0% error rate on examples)

- **SC-003**: Aggregate calculation returns `33` when processing all three examples together (verifies aggregation logic)

- **SC-004**: Solution provides example button press sequences that can be independently verified (each press sequence achieves exact targets)

- **SC-005**: System handles edge cases without crashes: targets of 0, large target numbers (1000+), machines with 5+ buttons and 5+ counters

- **SC-006**: Algorithm completes single machine analysis in under 1 second for realistic machine sizes (up to 20 buttons, 20 counters)

- **SC-007**: Full puzzle input processing completes in under 10 seconds total

- **SC-008**: Solution is correct for the actual Day 10 Part 2 puzzle input (when tested against AoC answer checker)

---

## Assumptions

- Each button must be pressed a non-negative integer number of times
- Button presses are applied simultaneously - order doesn't matter
- Each button press affects its listed counters by exactly +1
- Counters start at 0
- Solution must reach exact target values (no approximation)
- Optimization goal is to minimize total button presses (sum across all buttons)
- Machines in the input are independent (solving one doesn't affect others)
- The joltage level counter system operates independently from the indicator light system (Part 2 ignores lights entirely)
