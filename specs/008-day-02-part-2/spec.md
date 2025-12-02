# Feature Specification: Day 2 Part 2 - Invalid Product ID Detection (Extended Pattern)

**Feature Branch**: `008-day-02-part-2`  
**Created**: December 2, 2025  
**Status**: Draft  
**Input**: User description: "Solve Day 2 Part 2 - identify invalid product IDs with repeated digit sequences (at least twice) in given ranges"

## User Scenarios & Testing _(mandatory)_

### User Story 1 - Identify Invalid IDs with Any Repeated Pattern (Priority: P1)

A gift shop clerk needs to identify all invalid product IDs across multiple ID ranges where an invalid ID is defined as any number composed entirely of a digit sequence repeated at least twice (e.g., "111" is "1" three times, "565656" is "56" three times, "12341234" is "1234" two times).

**Why this priority**: This is the core requirement - without this capability, the clerk cannot clean up the corrupted database entries caused by the young Elf's patterns.

**Independent Test**: Can be fully tested by providing comma-separated ID ranges and verifying that the sum of all invalid IDs matches the expected total, delivering immediate value for database cleanup.

**Acceptance Scenarios**:

1. **Given** the range "11-22", **When** checking for invalid IDs, **Then** the system identifies "11" and "22" as invalid (both are single digits repeated twice)

2. **Given** the range "95-115", **When** checking for invalid IDs, **Then** the system identifies "99" (9 repeated twice) and "111" (1 repeated three times) as invalid

3. **Given** the range "998-1012", **When** checking for invalid IDs, **Then** the system identifies "999" (9 repeated three times) and "1010" (10 repeated twice) as invalid

4. **Given** the range "1188511880-1188511890", **When** checking for invalid IDs, **Then** the system identifies "1188511885" as invalid (118851 repeated twice)

5. **Given** the range "222220-222224", **When** checking for invalid IDs, **Then** the system identifies "222222" as invalid (222 repeated twice, or 22 repeated three times, or 2 repeated six times)

6. **Given** the range "1698522-1698528", **When** checking for invalid IDs, **Then** the system identifies no invalid IDs

7. **Given** the range "446443-446449", **When** checking for invalid IDs, **Then** the system identifies "446446" as invalid (446 repeated twice)

8. **Given** the range "38593856-38593862", **When** checking for invalid IDs, **Then** the system identifies "38593859" as invalid

9. **Given** the range "565653-565659", **When** checking for invalid IDs, **Then** the system identifies "565656" as invalid (56 repeated three times)

10. **Given** the range "824824821-824824827", **When** checking for invalid IDs, **Then** the system identifies "824824824" as invalid (824 repeated three times)

11. **Given** the range "2121212118-2121212124", **When** checking for invalid IDs, **Then** the system identifies "2121212121" as invalid (21 repeated five times)

12. **Given** the complete example input "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124", **When** summing all invalid IDs, **Then** the total is 4174379265

---

### User Story 2 - Process Multiple Ranges Efficiently (Priority: P2)

A clerk needs to process an entire list of ID ranges (provided as comma-separated values on a single line) and receive a single sum of all invalid IDs found across all ranges.

**Why this priority**: The clerk has many ranges to check and needs an efficient way to process them all at once rather than checking each range individually.

**Independent Test**: Can be tested by providing multi-range input and verifying the aggregated sum matches expected output.

**Acceptance Scenarios**:

1. **Given** multiple ranges separated by commas on a single line, **When** the system processes the input, **Then** it correctly parses each range and checks all IDs within those ranges

2. **Given** ranges with varying sizes (small like "11-22" and large like "1188511880-1188511890"), **When** the system processes them, **Then** all ranges are checked regardless of size

3. **Given** a list of ranges including some with no invalid IDs, **When** summing results, **Then** those ranges contribute 0 to the total

---

### Edge Cases

- What happens when a range contains only valid IDs (e.g., "1698522-1698528")? (Answer: No invalid IDs are found, contributes 0 to sum)
- How does the system handle IDs that can be interpreted as multiple different repeated patterns (e.g., "222222" could be "2" six times, "22" three times, or "222" twice)? (Answer: Any valid interpretation makes it invalid - system identifies it as invalid)
- What happens with single-digit ranges like "1-9"? (Answer: All single digits 1-9 are valid; they don't form repeated patterns)
- How does the system handle two-digit numbers where both digits are the same (e.g., "11", "22", "99")? (Answer: These are invalid as they represent a single digit repeated twice)
- What about numbers with leading zeros conceptually (e.g., a pattern like "0101")? (Answer: Per rules, numbers don't have leading zeros; "0101" is not a valid ID representation, but "101" is valid)

## Requirements _(mandatory)_

### Functional Requirements

- **FR-001**: System MUST accept input as comma-separated ID ranges on a single line, where each range is formatted as "start-end"

- **FR-002**: System MUST parse each range to extract the start ID and end ID as integers

- **FR-003**: System MUST check every integer within each range (inclusive of start and end) to determine if it is invalid

- **FR-004**: System MUST identify an ID as invalid if and only if it consists entirely of some digit sequence repeated at least twice (e.g., "111" = "1" × 3, "565656" = "56" × 3, "12341234" = "1234" × 2)

- **FR-005**: System MUST treat numbers as having no leading zeros (e.g., "101" is valid, "0101" is not a valid number representation)

- **FR-006**: System MUST sum all invalid IDs found across all ranges

- **FR-007**: System MUST output the final sum as an integer

- **FR-008**: System MUST correctly identify invalid IDs for all pattern lengths (single digit repeated multiple times, two digits repeated multiple times, etc.)

- **FR-009**: System MUST handle large ID ranges efficiently (e.g., ranges spanning millions of IDs like "1188511880-1188511890")

- **FR-010**: System MUST produce the sum 4174379265 when given the example input

### Key Entities

- **ID Range**: Represents a continuous span of product IDs, defined by a start integer and end integer (inclusive)
- **Product ID**: An integer value within a range that may be valid or invalid based on pattern-matching rules
- **Invalid ID**: A product ID that consists entirely of a digit sequence repeated at least twice
- **Digit Sequence**: A substring of digits that, when repeated, forms the complete number

## Success Criteria _(mandatory)_

### Measurable Outcomes

- **SC-001**: System correctly identifies all 13 invalid IDs from the example ranges (11, 22, 99, 111, 999, 1010, 1188511885, 222222, 446446, 38593859, 565656, 824824824, 2121212121)

- **SC-002**: System produces the exact sum of 4174379265 for the complete example input

- **SC-003**: System processes all ranges in the example input (11 ranges total) and checks all IDs within those ranges

- **SC-004**: System correctly distinguishes between Part 1 rules (exactly twice) and Part 2 rules (at least twice), identifying additional invalid IDs in Part 2 (e.g., "111", "565656", "824824824", "2121212121")
