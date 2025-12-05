# Feature Specification: Day 5 Part 1 - Fresh Ingredient ID Validation

**Feature Branch**: `012-day-05-part-1`  
**Created**: December 5, 2025  
**Status**: Draft  
**Input**: Identify which ingredient IDs are fresh based on range validation rules

## User Scenarios & Testing _(mandatory)_

### User Story 1 - Validate Single Ingredient Against Fresh Ranges (Priority: P1)

An Elf needs to determine if a single available ingredient ID is fresh by checking if it falls within any of the defined fresh ID ranges. This is the core requirement that enables the entire solution.

**Why this priority**: This is the fundamental operation that all other functionality depends on. Without being able to validate a single ingredient, the solution cannot work.

**Independent Test**: Can be tested by providing a single ingredient ID, a set of ranges, and verifying the correct fresh/spoiled determination is returned.

**Acceptance Scenarios**:

1. **Given** fresh ranges `[3-5, 10-14, 16-20, 12-18]` and ingredient ID `5`, **When** validating, **Then** return `fresh` because `5` is within range `3-5`
2. **Given** fresh ranges `[3-5, 10-14, 16-20, 12-18]` and ingredient ID `1`, **When** validating, **Then** return `spoiled` because `1` is not in any range
3. **Given** fresh ranges `[3-5, 10-14, 16-20, 12-18]` and ingredient ID `17`, **When** validating, **Then** return `fresh` because `17` is within both range `16-20` and range `12-18`
4. **Given** fresh ranges `[3-5, 10-14, 16-20, 12-18]` and ingredient ID `32`, **When** validating, **Then** return `spoiled` because `32` is not in any range
5. **Given** fresh ranges `[3-5, 10-14, 16-20, 12-18]` and ingredient ID `11`, **When** validating, **Then** return `fresh` because `11` is within range `10-14`
6. **Given** fresh ranges `[3-5, 10-14, 16-20, 12-18]` and ingredient ID `8`, **When** validating, **Then** return `spoiled` because `8` is not in any range

---

### User Story 2 - Process Complete Database and Count Fresh Ingredients (Priority: P1)

An Elf needs to process the complete database consisting of fresh ranges and available ingredient IDs, then count how many available ingredients are fresh.

**Why this priority**: This is the main deliverable that answers the puzzle question. Without this, the individual validations have no purpose.

**Independent Test**: Can be tested by providing a complete database file with ranges and available IDs, executing the solution, and verifying the count of fresh ingredients matches the expected result.

**Acceptance Scenarios**:

1. **Given** database with ranges `[3-5, 10-14, 16-20, 12-18]` and available IDs `[1, 5, 8, 11, 17, 32]`, **When** processing, **Then** return count of `3` fresh ingredients (IDs: 5, 11, 17)
2. **Given** an empty available ingredients list, **When** processing, **Then** return count of `0`
3. **Given** fresh ranges and all available IDs fall within ranges, **When** processing, **Then** return count equal to the total number of available IDs
4. **Given** fresh ranges and no available IDs fall within ranges, **When** processing, **Then** return count of `0`

---

### User Story 3 - Parse Database Format (Priority: P1)

An Elf needs to correctly parse the database format: fresh ID ranges separated from available ingredient IDs by a blank line, and correctly interpret inclusive range notation.

**Why this priority**: Without correct parsing, the validation logic cannot operate on the input data. This must work reliably to ensure the solution is accurate.

**Independent Test**: Can be tested by parsing a formatted database string and verifying that ranges and available IDs are extracted correctly.

**Acceptance Scenarios**:

1. **Given** input with ranges on first lines, blank line, then IDs, **When** parsing, **Then** extract ranges into one collection and IDs into another
2. **Given** range `10-14`, **When** parsing, **Then** interpret as inclusive: 10, 11, 12, 13, 14 are all valid
3. **Given** ranges `[10-14, 16-20]` with overlap, **When** parsing, **Then** handle overlapping ranges correctly (no duplicates in the fresh set)
4. **Given** database with `3-5` and available ID `4`, **When** parsing and validating, **Then** correctly identify `4` as fresh

---

### Edge Cases

- What happens when a range is a single number (e.g., `5-5`)?
- How does the system handle ranges that wrap around or are specified in reverse (e.g., `14-10`)?
- What happens when an available ingredient ID is negative or zero?
- How does the system handle very large range values or ingredient IDs?

## Requirements _(mandatory)_

### Functional Requirements

- **FR-001**: System MUST parse fresh ID ranges from the input database in the format `START-END`
- **FR-002**: System MUST interpret ranges as inclusive (both START and END are valid IDs)
- **FR-003**: System MUST parse available ingredient IDs from the input database (one per line after blank line separator)
- **FR-004**: System MUST determine if an ingredient ID is fresh by checking if it falls within ANY of the fresh ranges
- **FR-005**: System MUST count the total number of fresh ingredient IDs from the available list
- **FR-006**: System MUST handle overlapping ranges correctly (an ID fresh in any range is considered fresh)
- **FR-007**: System MUST return the count of fresh ingredients as the solution

### Key Entities

- **Fresh Range**: A pair of inclusive ingredient IDs (start and end) that defines which ingredients are fresh. Multiple ranges can overlap.
- **Available Ingredient ID**: An individual ingredient ID that needs to be checked against fresh ranges to determine if it's fresh or spoiled.
- **Ingredient Status**: Either "fresh" (ID exists in at least one fresh range) or "spoiled" (ID does not exist in any fresh range)

## Success Criteria _(mandatory)_

### Measurable Outcomes

- **SC-001**: Solution correctly identifies 3 fresh ingredients (IDs 5, 11, 17) and 3 spoiled ingredients (IDs 1, 8, 32) from the example database
- **SC-002**: Solution processes the complete puzzle input and returns an integer count of fresh ingredients
- **SC-003**: All acceptance scenarios execute without errors and produce expected results
- **SC-004**: Solution handles databases with up to 1000 ranges and 1000+ available IDs efficiently

## Assumptions

- Ranges are provided in `START-END` format where START ≤ END
- Ranges and available IDs are positive integers
- The database format is well-formed (valid separator, no malformed lines)
- Each available ingredient ID should be counted once, regardless of how many ranges it falls into
