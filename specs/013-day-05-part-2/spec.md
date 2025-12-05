# Feature Specification: Day 5 Part 2 - Fresh Ingredient ID Range Coverage

**Feature Branch**: `013-day-05-part-2`  
**Created**: December 5, 2025  
**Status**: Draft  
**Input**: Calculate the total number of unique ingredient IDs that are considered fresh according to fresh ingredient ID ranges, ignoring available IDs

## User Scenarios & Testing _(mandatory)_

### User Story 1 - Calculate Total Fresh Ingredients from Ranges (Priority: P1)

An Elf needs to determine the complete set of all ingredient IDs that are fresh according to the defined fresh ID ranges, regardless of whether those IDs are in the available inventory. This is the primary requirement for Part 2.

**Why this priority**: This is the core deliverable for Part 2 that directly answers the puzzle question. Without this capability, the feature provides no value.

**Independent Test**: Can be tested by providing fresh ID ranges, calculating all fresh IDs across all ranges (accounting for overlaps), and verifying the total count matches expected results.

**Acceptance Scenarios**:

1. **Given** fresh ranges `[3-5, 10-14, 16-20, 12-18]`, **When** calculating all fresh IDs, **Then** return count of `14` fresh IDs (the complete set: 3, 4, 5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20)

2. **Given** fresh ranges `[3-5]` (single range), **When** calculating all fresh IDs, **Then** return count of `3` fresh IDs (3, 4, 5)

3. **Given** fresh ranges `[10-14, 16-20, 12-18]` (overlapping ranges), **When** calculating all fresh IDs, **Then** return count of `11` fresh IDs (10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20) - no duplicates counted

4. **Given** fresh ranges `[1-3, 5-7]` (non-adjacent ranges), **When** calculating all fresh IDs, **Then** return count of `6` fresh IDs (1, 2, 3, 5, 6, 7) with gap at ID 4

5. **Given** fresh ranges `[10-10]` (single-ID range), **When** calculating all fresh IDs, **Then** return count of `1` fresh ID (just 10)

6. **Given** fresh ranges `[1-1, 2-2, 3-3]` (multiple single-ID ranges), **When** calculating all fresh IDs, **Then** return count of `3` fresh IDs (1, 2, 3)

7. **Given** fresh ranges `[1-5, 3-7]` (significantly overlapping ranges), **When** calculating all fresh IDs, **Then** return count of `7` fresh IDs (1, 2, 3, 4, 5, 6, 7) - union removes duplicates

---

### User Story 2 - Parse Fresh Ranges and Ignore Available IDs Section (Priority: P1)

An Elf needs to correctly parse the database format in Part 2, extracting only fresh ID ranges and completely ignoring the available ingredient IDs section (which is irrelevant for Part 2).

**Why this priority**: The database format parsing is essential to the solution. Part 2 explicitly states that the available IDs section is irrelevant, so the solution must handle this distinction correctly.

**Independent Test**: Can be tested by parsing a complete database file and verifying that only fresh ranges are extracted and processed, while available IDs are not used in the calculation.

**Acceptance Scenarios**:

1. **Given** database with ranges `[3-5, 10-14, 16-20, 12-18]`, blank line, and available IDs `[1, 5, 8, 11, 17, 32]`, **When** parsing for Part 2, **Then** extract ranges only and return fresh count of `14` (available IDs are ignored)

2. **Given** database with single range `[5-5]` and any available IDs, **When** parsing for Part 2, **Then** extract range and ignore available IDs section

3. **Given** database with ranges followed by blank line and large available IDs list, **When** parsing for Part 2, **Then** process only ranges and not iterate through available IDs

---

### User Story 3 - Handle Edge Cases in Range Coverage (Priority: P2)

An Elf needs the solution to correctly handle edge cases such as very large ranges, contiguous ranges, and unusual but valid range configurations.

**Why this priority**: Edge cases ensure robustness and correctness across different puzzle input configurations. P2 because common cases work first.

**Independent Test**: Can be tested by providing various edge case range configurations and verifying the fresh ID count is calculated correctly.

**Acceptance Scenarios**:

1. **Given** fresh ranges `[1-100]` (large range), **When** calculating fresh IDs, **Then** return count of `100`

2. **Given** fresh ranges `[1-10, 11-20]` (adjacent/contiguous ranges), **When** calculating fresh IDs, **Then** return count of `20` (1-20 continuous)

3. **Given** fresh ranges `[5-10, 3-7, 8-12]` (multiple overlapping patterns), **When** calculating fresh IDs, **Then** return count of `10` (3-12 complete coverage with overlaps)

4. **Given** fresh ranges with duplicates `[3-5, 3-5]` (identical ranges), **When** calculating fresh IDs, **Then** return count of `3` (3, 4, 5) - no double-counting

---

### Edge Cases

- What happens when ranges have very large ID values (e.g., 1000000-1000010)?
- How does the system handle reverse-ordered ranges (e.g., `14-10` instead of `10-14`)?
- What if the ranges list is empty?
- How does the system handle a single range that covers a very large set of IDs?
- What happens if an ID appears in many overlapping ranges?

## Requirements _(mandatory)_

### Functional Requirements

- **FR-001**: System MUST parse fresh ID ranges from the input database in the format `START-END`
- **FR-002**: System MUST interpret ranges as inclusive (both START and END are valid IDs)
- **FR-003**: System MUST calculate the complete set of all fresh ingredient IDs by merging all ranges
- **FR-004**: System MUST handle overlapping ranges correctly by calculating the union (no duplicate IDs in the final count)
- **FR-005**: System MUST ignore the available ingredient IDs section in Part 2 (blank line and subsequent IDs are not used)
- **FR-006**: System MUST return the total count of unique fresh ingredient IDs across all ranges
- **FR-007**: System MUST handle adjacent and contiguous ranges correctly by merging them into the union

### Key Entities

- **Fresh Range**: A pair of inclusive ingredient IDs (start and end) that defines which ingredients are fresh. Multiple ranges can overlap or be contiguous.
- **Fresh Ingredient ID Set**: The complete union of all ingredient IDs that fall within any fresh range, with no duplicates.
- **Range Union**: The mathematical union of all fresh ranges, representing all IDs that are fresh according to the rules.

## Success Criteria _(mandatory)_

### Measurable Outcomes

- **SC-001**: Solution correctly calculates that ranges `[3-5, 10-14, 16-20, 12-18]` yield 14 total fresh IDs (3, 4, 5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20)
- **SC-002**: Solution correctly identifies IDs in overlapping regions (e.g., ID 17 is in both `16-20` and `12-18`) without double-counting
- **SC-003**: Solution correctly handles non-adjacent ranges by calculating the union (e.g., ranges `[1-3, 5-7]` yield 6 fresh IDs with a gap at 4)
- **SC-004**: Solution processes the complete puzzle input and returns an integer count of total fresh IDs
- **SC-005**: Solution verifies that available ingredient IDs section is completely ignored and does not affect the result
- **SC-006**: All acceptance scenarios execute without errors and produce expected results
- **SC-007**: Solution handles databases with up to 1000 ranges efficiently

## Assumptions

- Ranges are provided in `START-END` format where START ≤ END (ranges are not provided in reverse)
- Ranges and IDs are positive integers
- The database format is well-formed with ranges before the blank line separator
- The fresh ID range section is mandatory; an empty range list is a valid edge case
- The solution focus is on the mathematical union of ranges, not the available IDs from Part 1
