# Tasks: Day 7 Part 1 - Tachyon Beam Split Counter

**Input**: Design documents from `/specs/001-day-07-part-1/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create day-07/ directory structure (solution.py, test_solution.py)
- [x] T002 Verify test_input.txt exists in day-07/ with the exact example from description.md
- [x] T003 Verify input.txt exists in day-07/ (downloaded from AoC)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Define direction constants (DOWN, LEFT, RIGHT) in day-07/solution.py
- [x] T005 Implement parse_grid(filename) function in day-07/solution.py to read grid and find 'S'
- [x] T006 Create beam state representation using (row, col, direction) tuples in day-07/solution.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Count Beam Splits (Priority: P1) 🎯 MVP

**Goal**: Implement core beam simulation to count splits on test_input.txt

**Independent Test**: test_input.txt returns 21 splits

### Implementation for User Story 1

- [x] T007 [US1] Implement simulate_beams(grid, start_pos) skeleton with queue initialization in day-07/solution.py
- [x] T008 [US1] Implement BFS loop: dequeue beam, check visited set, mark visited in day-07/solution.py
- [x] T009 [US1] Implement beam movement: calculate next position, check bounds in day-07/solution.py
- [x] T010 [US1] Implement empty space handling: continue beam in same direction in day-07/solution.py
- [x] T011 [US1] Implement splitter logic: increment split_count, emit LEFT and RIGHT beams in day-07/solution.py
- [x] T012 [US1] Implement count_splits(filename) main entry point in day-07/solution.py
- [x] T013 [US1] Add main block to run solution on input files in day-07/solution.py

**Checkpoint**: User Story 1 complete - solution counts splits correctly

---

## Phase 4: User Story 2 - Support for test_input.txt (Priority: P2)

**Goal**: Create integration test using test_input.txt

**Independent Test**: Integration test passes with result of 21

### Implementation for User Story 2

- [x] T014 [US2] Create test_example_input() test function in day-07/test_solution.py
- [x] T015 [US2] Implement assertion: count_splits("day-07/test_input.txt") == 21 in day-07/test_solution.py
- [x] T016 [US2] Add test runner main block in day-07/test_solution.py

**Checkpoint**: Integration test passes, validates solution against known example

---

## Phase 5: User Story 3 - Handle Multiple Beams and Overlaps (Priority: P3)

**Goal**: Ensure beam merging works correctly for overlapping beams

**Independent Test**: Merged beam scenarios return correct split counts

### Implementation for User Story 3

- [x] T017 [P] [US3] Create test_merged_beams() unit test in day-07/test_solution.py
- [x] T018 [P] [US3] Create test_no_splitters() edge case test in day-07/test_solution.py
- [x] T019 [US3] Verify visited set properly merges beams with same (row, col, direction) in day-07/solution.py
- [x] T020 [US3] Verify split counting: 2 splitters = 2 splits even if middle beam shared in day-07/solution.py

**Checkpoint**: All beam merging scenarios handled correctly

---

## Phase 6: User Story 4 - Main Input Solution (Priority: P1)

**Goal**: Run solution on main puzzle input (input.txt) for AoC submission

**Independent Test**: Solution runs on input.txt and outputs an integer

### Implementation for User Story 4

- [x] T021 [US4] Verify count_splits works with "day-07/input.txt" path in day-07/solution.py
- [x] T022 [US4] Run solution on input.txt and capture result for AoC submission
- [x] T023 [US4] Document the answer in day-07/README.md

**Checkpoint**: Main puzzle solved, answer ready for submission

---

## Phase 7: User Story 5 - Splitter Module Behavior (Priority: P2)

**Goal**: Validate splitter logic with unit tests

**Independent Test**: Splitter unit tests pass

### Implementation for User Story 5

- [x] T024 [P] [US5] Create test_single_split() unit test in day-07/test_solution.py
- [x] T025 [P] [US5] Create test_multiple_splitters_same_row() unit test in day-07/test_solution.py
- [x] T026 [US5] Verify splitter emits exactly LEFT and RIGHT beams (not DOWN) in day-07/solution.py
- [x] T027 [US5] Verify original beam stops at splitter position in day-07/solution.py

**Checkpoint**: Splitter behavior validated and correct

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T028 [P] Add docstrings to all functions in day-07/solution.py
- [x] T029 [P] Create or update day-07/README.md with usage instructions
- [x] T030 Add type hints to function signatures in day-07/solution.py
- [x] T031 Run all tests and verify they pass
- [x] T032 Validate against quickstart.md scenarios

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can proceed in parallel (if staffed)
  - Or sequentially in priority order (US1 → US4 → US2 → US5 → US3)
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - Core implementation
- **User Story 2 (P2)**: Depends on US1 being complete - Tests US1 functionality
- **User Story 3 (P3)**: Can start after Foundational, enhanced by US1 - Tests edge cases
- **User Story 4 (P1)**: Depends on US1 being complete - Uses US1 to solve main puzzle
- **User Story 5 (P2)**: Can start after Foundational, enhanced by US1 - Validates US1 logic

### Within Each User Story

- US1: Sequential implementation of simulation logic (T007 → T008 → T009 → T010 → T011 → T012 → T013)
- US2: Sequential test creation (T014 → T015 → T016)
- US3: Tests can run in parallel (T017, T018), then verification (T019, T020)
- US4: Sequential execution (T021 → T022 → T023)
- US5: Tests can run in parallel (T024, T025), then verification (T026, T027)

### Parallel Opportunities

- Setup tasks (T001, T002, T003) can be verified in parallel
- Foundational tasks are sequential (each builds on previous)
- Once US1 is complete:
  - US2 can start (create tests)
  - US4 can start (run on input.txt)
  - US5 can start (validate splitter logic)
  - US3 can start (edge case tests)
- Within US3: T017 and T018 can run in parallel
- Within US5: T024 and T025 can run in parallel
- Polish tasks: T028 and T029 can run in parallel

---

## Parallel Example: After US1 Complete

```bash
# These can all be worked on simultaneously:
Task T014: Create integration test (US2)
Task T021: Run on input.txt (US4)
Task T024: Create splitter unit test (US5)
Task T017: Create merged beams test (US3)
```

---

## Implementation Strategy

### MVP First (User Story 1 + 4 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (core simulation)
4. Complete Phase 6: User Story 4 (solve main puzzle)
5. **STOP and VALIDATE**: Submit answer to AoC
6. Return to add tests and polish

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test manually with test_input.txt → Should get 21 (MVP!)
3. Add User Story 4 → Run on input.txt → Submit to AoC
4. Add User Story 2 → Integration tests pass → Automated validation
5. Add User Story 5 → Unit tests pass → Logic validated
6. Add User Story 3 → Edge cases pass → Robust solution
7. Polish → Clean, documented, complete

### Test-Driven Approach (Optional)

1. Complete Setup + Foundational
2. Create all tests first (US2, US3, US5) - they will fail
3. Implement US1 until tests pass
4. Run US4 to solve puzzle
5. Polish

---

## Summary

- **Total Tasks**: 32
- **Task Count per User Story**:
  - Setup: 3 tasks
  - Foundational: 3 tasks
  - US1 (Count Beam Splits): 7 tasks
  - US2 (test_input.txt support): 3 tasks
  - US3 (Handle Overlaps): 4 tasks
  - US4 (Main Input): 3 tasks
  - US5 (Splitter Behavior): 4 tasks
  - Polish: 5 tasks
- **Parallel Opportunities**: 6 tasks can run in parallel
- **Independent Test Criteria**: Each user story has clear validation criteria
- **Suggested MVP Scope**: US1 + US4 (core simulation + solve puzzle) = 10 tasks

---

## Format Validation

✅ All tasks follow checklist format: `- [ ] [TaskID] [P?] [Story?] Description with file path`
✅ All tasks have unique IDs (T001-T032)
✅ All user story tasks have [Story] labels
✅ All parallelizable tasks have [P] marker
✅ All tasks include specific file paths
