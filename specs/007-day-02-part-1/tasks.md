# Tasks: Day 2 Part 1 - Invalid Product ID Detection

**Input**: Design documents from `/specs/007-day-02-part-1/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/api-contract.md

**Tests**: Tests are REQUIRED per Constitution Principle IV (TDD is NON-NEGOTIABLE). Tasks follow RED-GREEN-REFACTOR cycle.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

Using Advent of Code day structure (from plan.md):

- Solution code: `day-02/`
- Test code: `day-02/`
- Spec artifacts: `specs/007-day-02-part-1/`

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Create day-02 folder structure per AoC Constitution

- [x] T001 Verify day-02/ folder exists with input.txt and description.md
- [x] T002 Create test_input.txt from example in description.md with example ranges
- [x] T003 [P] Create empty day-02/solution.py with module docstring
- [x] T004 [P] Create empty day-02/test_solution.py with module docstring

**Checkpoint**: Day 2 folder structure ready for TDD implementation

---

## Phase 2: Foundational (No Blocking Prerequisites)

**Purpose**: No foundational phase needed - AoC projects are self-contained

**⚠️ Note**: For AoC, each user story maps to incremental solution building. User Story 1 is the MVP.

**Checkpoint**: Ready to begin User Story 1 (core functionality)

---

## Phase 3: User Story 1 - Detect Invalid Product IDs in Single Range (Priority: P1) 🎯 MVP

**Goal**: Implement core invalid ID detection for a single range. This is the foundation - a number is invalid if formed by repeating a digit sequence twice (e.g., 55, 6464, 123123).

**Independent Test**: Provide range "11-22" and verify it identifies [11, 22] as invalid IDs.

### RED Phase - Write Failing Tests for User Story 1 ⚠️

> **CRITICAL: Write these tests FIRST, run them to verify they FAIL before any implementation**

- [x] T005 [P] [US1] Write test_is_invalid_id() in day-02/test_solution.py testing pattern detection (55→True, 101→False, 6464→True, 123123→True)
- [x] T006 [P] [US1] Write test_is_invalid_id_edge_cases() in day-02/test_solution.py testing edge cases (11, 22, 99, 1010, single digits)
- [x] T007 [P] [US1] Write test_find_invalid_ids_in_range() in day-02/test_solution.py testing range scanning with examples from spec

**Checkpoint**: Run `uv run pytest day-02/test_solution.py -v` - ALL tests should FAIL (ImportError or assertion failures)

### GREEN Phase - Implement Minimal Solution for User Story 1

- [x] T008 [US1] Implement is_invalid_id(num: int) -> bool in day-02/solution.py using string split approach from research.md
- [x] T009 [US1] Implement find_invalid_ids_in_range(start: int, end: int) -> list[int] in day-02/solution.py iterating through range
- [x] T010 [US1] Add type hints and docstrings to both functions per contracts/api-contract.md

**Checkpoint**: Run `uv run pytest day-02/test_solution.py -v` - Tests for US1 should now PASS

### REFACTOR Phase - Clean Up User Story 1

- [x] T011 [US1] Review is_invalid_id() for clarity and add examples to docstring
- [x] T012 [US1] Verify test coverage for US1 functions - all acceptance scenarios covered

**Checkpoint**: User Story 1 complete - can detect invalid IDs in a single range independently

---

## Phase 4: User Story 2 - Process Multiple Ranges (Priority: P2)

**Goal**: Parse comma-separated input and process multiple ranges. Builds on US1 by adding input parsing layer.

**Independent Test**: Provide "11-22,95-115,998-1012" and verify it identifies [11, 22, 99, 1010] across all ranges.

### RED Phase - Write Failing Tests for User Story 2 ⚠️

- [x] T013 [P] [US2] Write test_parse_ranges() in day-02/test_solution.py testing comma-separated parsing ("11-22,95-115" → [(11,22), (95,115)])
- [x] T014 [P] [US2] Write test_parse_ranges_edge_cases() in day-02/test_solution.py testing single range, whitespace handling, empty input

**Checkpoint**: Run `uv run pytest day-02/test_solution.py::test_parse_ranges* -v` - New tests should FAIL

### GREEN Phase - Implement User Story 2

- [x] T015 [US2] Implement parse_ranges(input_text: str) -> list[tuple[int, int]] in day-02/solution.py per research.md approach
- [x] T016 [US2] Add type hints and docstring to parse_ranges() per contracts/api-contract.md

**Checkpoint**: Run `uv run pytest day-02/test_solution.py -v` - All tests should PASS (US1 + US2)

### REFACTOR Phase - Clean Up User Story 2

- [x] T017 [US2] Review parse_ranges() for edge case handling (empty strings, whitespace)
- [x] T018 [US2] Verify integration: parse_ranges() output works with find_invalid_ids_in_range() from US1

**Checkpoint**: User Stories 1 AND 2 both work - can parse multiple ranges and detect invalid IDs

---

## Phase 5: User Story 3 - Calculate Total Sum of Invalid IDs (Priority: P3)

**Goal**: Integrate all components and sum invalid IDs across all ranges. Final deliverable for Part 1.

**Independent Test**: Full example input produces sum of 1227775554.

### RED Phase - Write Failing Tests for User Story 3 ⚠️

- [x] T019 [US3] Write test_solve_part1_simple() in day-02/test_solution.py testing simple cases ("11-22" → 33)
- [x] T020 [US3] Write test_solve_part1_example() in day-02/test_solution.py testing full example input → 1227775554
- [x] T021 [P] [US3] Write test_solve_part1_edge_cases() in day-02/test_solution.py testing empty input, no invalid IDs

**Checkpoint**: Run `uv run pytest day-02/test_solution.py::test_solve_part1* -v` - New tests should FAIL

### GREEN Phase - Implement User Story 3

- [x] T022 [US3] Implement solve_part1(input_text: str) -> int in day-02/solution.py integrating parse_ranges() + find_invalid_ids_in_range() + sum()
- [x] T023 [US3] Add type hints and docstring to solve_part1() per contracts/api-contract.md
- [x] T024 [US3] Implement main() function in day-02/solution.py reading from input.txt and printing Part 1 result

**Checkpoint**: Run `uv run pytest day-02/test_solution.py -v` - ALL tests should PASS

### REFACTOR Phase - Clean Up User Story 3

- [x] T025 [US3] Review solve_part1() for clarity - ensure integration is clean
- [x] T026 [US3] Add pathlib import and verify main() uses Path(**file**).parent / "input.txt"
- [x] T027 [US3] Verify full example test passes with exact sum 1227775554

**Checkpoint**: All user stories complete - full Part 1 solution ready

---

## Phase 6: Polish & Validation

**Purpose**: Final verification and quality checks

- [x] T028 [P] Run full test suite: `uv run pytest day-02/test_solution.py -v` - verify 100% pass rate
- [x] T029 [P] Run linter: `uv run ruff check day-02/` - verify no issues
- [x] T030 [P] Run formatter: `uv run ruff format day-02/` - ensure PEP8 compliance
- [x] T031 Execute solution: `uv run day-02/solution.py` - verify output format "Part 1: {answer}"
- [x] T032 Verify all functions have docstrings with examples per Constitution Principle III
- [ ] T033 [P] Create day-02/README.md documenting approach and any learnings (optional but recommended)
- [ ] T034 Manual submission: Copy answer from terminal, submit to adventofcode.com/2025/day/2
- [ ] T035 Update main README.md progress tracker with Day 2 Part 1 completion
- [ ] T036 Commit changes: `git add day-02/ specs/007-day-part-1/ && git commit -m "feat: solve day 02 part 1"`

**Checkpoint**: Part 1 complete, tested, formatted, and submitted

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - start immediately
- **Foundational (Phase 2)**: N/A for AoC - no blocking infrastructure needed
- **User Story 1 (Phase 3)**: Depends on Setup - This is the MVP
- **User Story 2 (Phase 4)**: Depends on US1 completion (uses find_invalid_ids_in_range)
- **User Story 3 (Phase 5)**: Depends on US1 + US2 completion (integrates both)
- **Polish (Phase 6)**: Depends on all user stories

### User Story Dependencies

- **User Story 1 (P1)**: Independent - core invalid ID detection logic
- **User Story 2 (P2)**: Builds on US1 - adds input parsing layer
- **User Story 3 (P3)**: Integrates US1 + US2 - complete solution

### Within Each User Story (TDD Cycle)

**CRITICAL ORDER**:

1. **RED**: Write tests FIRST, run to verify they FAIL
2. **GREEN**: Implement minimum code to make tests PASS
3. **REFACTOR**: Clean up code while keeping tests GREEN

### Parallel Opportunities

**Setup Phase**:

- T003 and T004 can run in parallel (creating different files)

**Within Each User Story**:

- All test-writing tasks marked [P] can be written in parallel
- Tests within a story can be executed together after writing
- RED phase tasks can be written in parallel
- GREEN phase tasks must be sequential (one function may depend on another)

**Polish Phase**:

- T028, T029, T030, T033 can all run in parallel (different operations)

---

## Parallel Example: User Story 1 RED Phase

```bash
# Write all US1 tests in parallel (different test functions):
Task T005: "Write test_is_invalid_id() in day-02/test_solution.py"
Task T006: "Write test_is_invalid_id_edge_cases() in day-02/test_solution.py"
Task T007: "Write test_find_invalid_ids_in_range() in day-02/test_solution.py"

# Then run together to verify ALL fail:
uv run pytest day-02/test_solution.py -v
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup → Files created
2. Complete Phase 3: User Story 1 (RED-GREEN-REFACTOR) → Core detection works
3. **STOP and VALIDATE**: Test US1 independently with `pytest`
4. Can already detect invalid IDs in single range - partial value delivered!

### Incremental Delivery (Recommended for AoC)

1. Phase 1: Setup → Structure ready
2. Phase 3: US1 complete → Can detect invalid IDs ✓
3. Phase 4: US2 complete → Can parse multiple ranges ✓
4. Phase 5: US3 complete → Full solution, can solve puzzle ✓
5. Phase 6: Polish → Submission ready

### Sequential TDD Strategy (AoC Standard)

Since this is a single-developer AoC challenge:

1. Complete Setup
2. US1: RED (write tests) → GREEN (implement) → REFACTOR (clean)
3. US2: RED → GREEN → REFACTOR
4. US3: RED → GREEN → REFACTOR
5. Polish and submit

Each user story builds on the previous, but maintains independent testability.

---

## Implementation Guidance

### From research.md

**Core Algorithm** (for T008):

```python
def is_invalid_id(num: int) -> bool:
    s = str(num)
    if len(s) % 2 != 0:
        return False
    mid = len(s) // 2
    return s[:mid] == s[mid:]
```

### From contracts/api-contract.md

**Function Signatures**:

- `parse_ranges(input_text: str) -> list[tuple[int, int]]`
- `is_invalid_id(num: int) -> bool`
- `find_invalid_ids_in_range(start: int, end: int) -> list[int]`
- `solve_part1(input_text: str) -> int`
- `main() -> None`

### From data-model.md

**Test Data**:

- Example ranges: 11-22, 95-115, 998-1012, etc.
- Known invalid IDs: 11, 22, 99, 1010, 1188511885, 222222, 446446, 38593859
- Expected sum: 1227775554

### Key Reminders

- ⚠️ **TDD is NON-NEGOTIABLE** (Constitution Principle IV)
- ✅ Write tests FIRST, see them FAIL, then implement
- ✅ Use examples from problem description for test cases
- ✅ Each user story should work independently
- ✅ Commit after each phase completion
- ✅ Follow quickstart.md for detailed workflow

---

## Notes

- All tasks follow strict TDD discipline: RED → GREEN → REFACTOR
- [P] tasks can be parallelized (different test functions, different operations)
- [Story] label tracks which user story each task implements
- Stop at any checkpoint to validate story works independently
- Constitution Principle IV requires seeing tests fail before implementation
- Each user story delivers incremental value even if stopped early
