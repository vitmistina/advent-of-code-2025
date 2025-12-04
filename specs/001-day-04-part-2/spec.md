# Feature Specification: Day 4 Part 2 - Printing Department

**Feature Branch**: `001-day-04-part-2`  
**Created**: 2025-12-04  
**Status**: Draft  
**Input**: User description: "Create AoC Day 4 Part 2 spec"

## User Scenarios & Testing _(mandatory)_

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.

  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Flag initial forklift-accessible rolls (Priority: P1)

The Elves need a quick way to highlight every roll of paper that a forklift can reach before any removals happen so they can prioritize the easiest targets.

**Why this priority**: Discovering the accessible set is the baseline task and must be verified before attempting the iterative removal described in Part Two.

**Independent Test**: Run the adjacency check on the example grid and confirm the count and positions match the 13 rolls marked with `x` in the description.

**Acceptance Scenarios**:

1. **Given** the 10×10 sample diagram from the problem statement, **When** each roll of paper is evaluated by counting the rolls in the eight surrounding cells, **Then** exactly 13 rolls are flagged as accessible and the sample map with `x` marks is reproducible.
2. **Given** a roll that has four or more adjacent `@` characters, **When** its neighbors are inspected, **Then** it is excluded from the accessible set in this initial pass and remains in the grid.

---

### User Story 2 - Remove accessible rolls iteratively (Priority: P2)

Once the accessible roll set is known, the forklifts remove all such rolls, re-evaluate the remaining grid, and keep repeating until no new rolls become accessible.

**Why this priority**: Part Two asks for the total number of rolls that can be removed by continually freeing up more rolls; this iterative loop is the core of the feature.

**Independent Test**: Progress through the removal sequence shown in the example, ensuring each iteration honors the accessibility rule and that the process ends when no rolls have fewer than four neighbors.

**Acceptance Scenarios**:

1. **Given** the sample diagram, **When** the forklifts remove every roll that is accessible at the start of each iteration and stop when none remain, **Then** the total number of removed rolls is 43 and the final grid contains no more _removeable_ `@` characters, matching the provided step-by-step removes.
2. **Given** multiple rolls qualify as accessible simultaneously, **When** they are all removed in the same iteration, **Then** no roll is removed while still surrounded by four or more neighbors in that iteration. (it _might_ become eligible in the next iteration)

---

### User Story 3 - Report results for the real input (Priority: P3)

After verifying the sample behavior, the solution must ingest the official puzzle input and deliver the required counts without manual intervention.

**Why this priority**: Completing the challenge requires reliably processing the actual Day 4 input after sample-based validation.

**Independent Test**: Run the solution against the stored input, then compare the returned counts to the known (or eventually confirmed) answers for Day 4 Part 1 and Part 2.

**Acceptance Scenarios**:

1. **Given** the official Day 4 input file, **When** the algorithm executes the adjacency scan followed by the removal loop, **Then** the CLI prints two integers: the initial accessible roll count and the total rolls removed, formatted according to the existing output conventions.

---

### Edge Cases

- How is the removal process handled when cascading accessibility occurs (removing one roll unlocks multiple new rolls)?
  - Answer: In the next iteration, all newly accessible rolls are identified and removed together.
- What is the expected failure mode when the input grid rows have inconsistent widths (malformed but rectangular assumption broken)?
  - Answer: Won't happen

### Functional Requirements

- **FR-001**: System MUST read the Day 4 diagram as a rectangular grid of characters where `@` represents a paper roll and `.` represents empty space.
- **FR-002**: System MUST determine whether a given roll is accessible by counting the paper rolls in the eight surrounding cells and treating fewer than four neighbors as accessible.
- **FR-003**: System MUST remove every accessible roll in the current pass, update the grid, and repeat the evaluation until no accessible rolls remain.
- **FR-004**: System MUST report two counts: the number of rolls accessible in the first pass and the cumulative number of rolls removed after the loop terminates.
- **FR-005**: System MUST support the provided sample diagram as an automated regression test so that the accessible count is 13 and the total removed count is 43.

### Key Entities _(include if feature involves data)_

- **PaperRoll**: Represents a single `@` cell, including its coordinates and current access state (blocked vs. accessible) based on adjacent roll counts.
- **GridState**: Represents the full layout, tracks which cells contain paper or are empty, and exposes neighbors for each cell to support the adjacency evaluation and iterative removal.

## Success Criteria _(mandatory)_

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: Running the adjacency check on the sample diagram produces one pass with exactly 13 accessible rolls before any removals occur.
- **SC-002**: Repeating the removal loop on the sample diagram removes 43 rolls in total and leaves a grid without any `@` characters.
- **SC-003**: For any valid puzzle input, the process halts when no rolls have fewer than four neighbors, ensuring the algorithm terminates gracefully.
- **SC-004**: The CLI or reporting output exposes both the initial accessible count and the total removed count so that the elves can confidently deliver both Part 1 and Part 2 answers.

## Assumptions

- The grid is rectangular; all rows contain the same number of columns.
- The input only uses `@`, `.`, and whitespace/newline characters.
- The sample diagram provided in the description remains the canonical regression test for this feature.
- The existing CLI/runner supplies the puzzle input as a newline-delimited text block so this spec only covers the evaluation and removal logic.
