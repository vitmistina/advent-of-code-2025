````markdown
# Tasks: Day 5 Part 1 - Fresh Ingredient ID Validation

**Input**: Design documents from `/specs/012-day-05-part-1/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/freshness.openapi.yaml

**Tests**: Included per AoC constitution (TDD Non-Negotiable - Principle IV)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: AoC repository with per-day subdirectories
- Day 05 artifacts in `day-05/` folder
- Shared CLI tooling in `cli/`
- Tests in `day-05/test_solution.py` per puzzle conventions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Ensure day-05 directory structure and input files are ready

- [x] T001 Download day 5 inputs and description using `uv run -m cli.meta_runner download --day 5`
- [x] T002 [P] Verify `day-05/input.txt` and `day-05/test_input.txt` exist and contain expected format
- [x] T003 [P] Verify `day-05/description.md` exists for reference

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core data structures and algorithms that ALL user stories depend on

**⚠️ CRITICAL**: No user story implementation can begin until this phase is complete

- [x] T004 Implement `FreshRange` dataclass with `start` and `end` fields in `day-05/solution.py`
- [x] T005 [P] Implement range validation logic in `FreshRange` to reject `start > end` in `day-05/solution.py`
- [x] T006 Implement `merge_ranges(ranges: list[FreshRange]) -> list[tuple[int, int]]` function in `day-05/solution.py`
- [x] T007 [P] Add docstrings to `merge_ranges` explaining O(R log R) complexity in `day-05/solution.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 3 - Parse Database Format (Priority: P1) 🎯 MVP Component

**Goal**: Correctly parse the database format into structured ranges and ingredient IDs

**Independent Test**: Parse a formatted database string and verify ranges and IDs are extracted correctly

### Tests for User Story 3

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

[X] T008 [P] [US3] Write test for parsing ranges on first lines in `day-05/test_solution.py`
[X] T009 [P] [US3] Write test for inclusive range interpretation `10-14` in `day-05/test_solution.py`
[X] T010 [P] [US3] Write test for handling overlapping ranges in `day-05/test_solution.py`
[X] T011 [P] [US3] Write test for parsing available IDs after blank line in `day-05/test_solution.py`

### Implementation for User Story 3

[X] T012 [US3] Implement `parse_database(data: str) -> tuple[list[FreshRange], list[int]]` in `day-05/solution.py`
[X] T013 [US3] Add parsing logic to split input on blank line `\n\n` in `day-05/solution.py`
[X] T014 [US3] Add range parsing logic to extract `start-end` format in `day-05/solution.py`
[X] T015 [US3] Add ingredient ID parsing to extract integers from second section in `day-05/solution.py`
[X] T016 [US3] Add error handling for malformed input in `day-05/solution.py`
[X] T017 [US3] Run tests and verify all US3 tests pass

**Checkpoint**: At this point, User Story 3 should be fully functional and testable independently

---

## Phase 4: User Story 1 - Validate Single Ingredient Against Fresh Ranges (Priority: P1) 🎯 MVP Component

**Goal**: Determine if a single ingredient ID is fresh by checking against fresh ranges

**Independent Test**: Provide a single ingredient ID and ranges, verify correct fresh/spoiled determination

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T018 [P] [US1] Write test for ingredient ID `5` is fresh in ranges `[3-5, 10-14, 16-20, 12-18]` in `day-05/test_solution.py`
- [x] T019 [P] [US1] Write test for ingredient ID `1` is spoiled in ranges `[3-5, 10-14, 16-20, 12-18]` in `day-05/test_solution.py`
- [x] T020 [P] [US1] Write test for ingredient ID `17` is fresh (overlapping ranges) in `day-05/test_solution.py`
- [x] T021 [P] [US1] Write test for ingredient ID `32` is spoiled in `day-05/test_solution.py`
- [x] T022 [P] [US1] Write test for ingredient ID `11` is fresh in `day-05/test_solution.py`
- [x] T023 [P] [US1] Write test for ingredient ID `8` is spoiled in `day-05/test_solution.py`

### Implementation for User Story 1

- [x] T024 [US1] Implement `is_fresh(ingredient_id: int, merged_ranges: list[tuple[int, int]]) -> bool` in `day-05/solution.py`
- [x] T025 [US1] Add binary search or two-pointer logic for O(log R) membership check in `day-05/solution.py`
- [x] T026 [US1] Add docstrings explaining the freshness determination algorithm in `day-05/solution.py`
- [x] T027 [US1] Run tests and verify all US1 tests pass

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 5: User Story 2 - Process Complete Database and Count Fresh Ingredients (Priority: P1) 🎯 MVP

**Goal**: Process complete database and count how many available ingredients are fresh

**Independent Test**: Provide complete database, verify count matches expected result

### Tests for User Story 2

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T028 [P] [US2] Write test for example database counting 3 fresh ingredients (5, 11, 17) in `day-05/test_solution.py`
- [x] T029 [P] [US2] Write test for empty available ingredients list returning count 0 in `day-05/test_solution.py`
- [x] T030 [P] [US2] Write test for all IDs fresh scenario in `day-05/test_solution.py`
- [x] T031 [P] [US2] Write test for no IDs fresh scenario in `day-05/test_solution.py`

### Implementation for User Story 2

- [x] T032 [US2] Implement `solve_part1(data: str) -> int` in `day-05/solution.py`
- [x] T033 [US2] Integrate parsing, merging, and counting logic in `solve_part1` in `day-05/solution.py`
- [x] T034 [US2] Add main execution block to load and solve with both test and real input in `day-05/solution.py`
- [x] T035 [US2] Add CLI argument parsing for `--part 1` support in `day-05/solution.py`
- [x] T036 [US2] Run tests and verify all US2 tests pass
- [x] T037 [US2] Execute solution with test input and verify expected output

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and ensure quality

- [x] T038 [P] Add comprehensive docstrings to all functions in `day-05/solution.py`
- [x] T039 [P] Run Ruff linting and fix any issues with `uv run ruff check day-05`
- [x] T040 [P] Run Ruff formatting with `uv run ruff format day-05`
- [x] T041 Execute full test suite with `uv run pytest day-05/test_solution.py -v`
- [x] T042 Run solution against real input with `uv run day-05/solution.py --part 1`
- [x] T043 [P] Update `day-05/README.md` with solution summary and approach
- [x] T044 Validate quickstart.md workflow by executing all steps in `specs/012-day-05-part-1/quickstart.md`
- [x] T045 [P] Optional: Add performance benchmark to verify O(R log R + I log I) complexity

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-5)**: All depend on Foundational phase completion
  - User stories can proceed in parallel (if different functions)
  - Or sequentially in priority order (US3 → US1 → US2 recommended for logical flow)
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 3 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies, but logically follows US3
- **User Story 2 (P1)**: Depends on US3 (parsing) and US1 (validation) being complete for integration

### Within Each User Story

- Tests MUST be written and FAIL before implementation (TDD)
- Tests within a story marked [P] can run in parallel
- Implementation tasks follow sequential dependencies within each story
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T002, T003)
- Foundational tasks T005 and T007 can run in parallel with T004 and T006 respectively
- All test-writing tasks for each user story can run in parallel
- Polish tasks marked [P] can run in parallel (T038, T039, T040, T043, T045)
- Once Foundational is complete, test writing for all three user stories can begin in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Write test for ingredient ID `5` is fresh in tests"
Task: "Write test for ingredient ID `1` is spoiled in tests"
Task: "Write test for ingredient ID `17` is fresh (overlapping) in tests"
Task: "Write test for ingredient ID `32` is spoiled in tests"
Task: "Write test for ingredient ID `11` is fresh in tests"
Task: "Write test for ingredient ID `8` is spoiled in tests"
```

---

## Implementation Strategy

### Recommended Sequential Approach (Following TDD)

1. **Phase 1: Setup** (T001-T003)
   - Download and verify inputs
2. **Phase 2: Foundational** (T004-T007)
   - Build core data structures
3. **Phase 3: User Story 3 - Parsing** (T008-T017)
   - Write tests → See them fail → Implement parsing → Tests pass
4. **Phase 4: User Story 1 - Validation** (T018-T027)
   - Write tests → See them fail → Implement validation → Tests pass
5. **Phase 5: User Story 2 - Full Solution** (T028-T037)
   - Write tests → See them fail → Implement integration → Tests pass
6. **Phase 6: Polish** (T038-T045)
   - Clean up, document, validate

### MVP Definition

The MVP is the complete Day 5 Part 1 solution, which requires all three P1 user stories:

- **US3**: Parsing (foundation for all other work)
- **US1**: Single ingredient validation (core logic)
- **US2**: Full database processing (final deliverable)

### TDD Workflow Per User Story

For each user story:

1. **RED**: Write all test tasks in parallel → Run tests → Verify failures
2. **GREEN**: Implement tasks sequentially → Run tests → Verify passes
3. **REFACTOR**: Clean up code, add docstrings, ensure Ruff compliance

---

## Format Validation Summary

✅ All tasks follow checklist format: `- [ ] [TaskID] [P?] [Story?] Description with file path`
✅ Task IDs sequential from T001 to T045
✅ [P] markers only on truly parallelizable tasks (different files/no dependencies)
✅ [Story] labels on all user story phase tasks (US1, US2, US3)
✅ Setup and Foundational phases: NO story labels
✅ Polish phase: NO story labels
✅ All implementation tasks include exact file paths

---

## Summary

- **Total Tasks**: 45
- **Setup Phase**: 3 tasks
- **Foundational Phase**: 4 tasks (BLOCKING)
- **User Story 3 (Parsing)**: 10 tasks (4 tests + 6 implementation)
- **User Story 1 (Validation)**: 10 tasks (6 tests + 4 implementation)
- **User Story 2 (Full Solution)**: 10 tasks (4 tests + 6 implementation)
- **Polish Phase**: 8 tasks
- **Parallel Opportunities**: 24 tasks marked [P]
- **MVP Scope**: All three P1 user stories (complete Part 1 solution)
````
