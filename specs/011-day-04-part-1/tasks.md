# Tasks: Day 4 Part 1 - Accessible Paper Rolls Counter

**Feature Branch**: `011-day-04-part-1`  
**Input**: Design documents from `/specs/011-day-04-part-1/`  
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

**TDD Approach**: Following constitution Principle IV (NON-NEGOTIABLE), all tasks follow RED-GREEN-REFACTOR cycle.

**Tests**: Included per TDD requirements - tests MUST be written FIRST and verified to FAIL before implementation.

**Organization**: Tasks grouped by user story to enable independent implementation and testing.

---

## Format: `- [ ] [ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- File paths follow day-04/ structure per Constitution Principle II

---

## Phase 1: Setup (Project Infrastructure)

**Purpose**: Initialize Day 4 solution structure

- [x] T001 Create day-04/ folder and download puzzle input via meta runner
- [x] T002 Create day-04/solution.py skeleton with imports and constants
- [x] T003 Create day-04/test_solution.py skeleton with pytest imports

**Checkpoint**: Day 4 folder structure ready for TDD workflow

---

## Phase 2: Foundational (Shared Utilities)

**Purpose**: Core helper functions needed by all user stories

**⚠️ CRITICAL**: These utilities are used across all user stories

- [x] T004 Implement parse_grid(input_data) in day-04/solution.py
- [x] T005 [P] Implement is_valid_position(grid, row, col) in day-04/solution.py
- [x] T006 [P] Define DIRECTIONS constant in day-04/solution.py

**Checkpoint**: Foundation ready - user story implementation can begin

---

## Phase 3: User Story 1 - Parse Grid and Identify Paper Rolls (Priority: P1) 🎯 MVP

**Goal**: Read grid and identify all paper roll positions with coordinates

**Independent Test**: Provide sample grid, verify all '@' positions identified correctly

### RED Phase: Write Tests First

- [x] T007 [US1] Write test_parse_grid_basic() in day-04/test_solution.py - verify grid parsing
- [x] T008 [US1] Write test_parse_grid_empty() in day-04/test_solution.py - verify empty grid handling
- [x] T009 [US1] Write test_identify_paper_rolls() in day-04/test_solution.py - verify '@' positions found
- [x] T010 [US1] Run tests - VERIFY ALL FAIL (RED phase validation)

### GREEN Phase: Implement to Pass Tests

- [x] T011 [US1] Complete parse_grid() implementation to handle multiline input in day-04/solution.py
- [x] T012 [US1] Add grid validation (strip whitespace, split lines) in day-04/solution.py
- [x] T013 [US1] Run tests - VERIFY ALL PASS (GREEN phase validation)

### REFACTOR Phase: Clean Up

- [x] T014 [US1] Refactor parse_grid() for clarity if needed - keep tests green
- [x] T015 [US1] Add docstring examples to parse_grid() in day-04/solution.py

**Checkpoint**: Grid parsing works independently - can read and identify paper rolls

---

## Phase 4: User Story 2 - Count Adjacent Paper Rolls (Priority: P2)

**Goal**: For each paper roll, count neighbors in all 8 directions

**Independent Test**: Provide grid with known adjacency counts, verify each position's count matches

### RED Phase: Write Tests First

- [x] T016 [US2] Write test_count_adjacent_zero() in day-04/test_solution.py - roll with no neighbors
- [x] T017 [US2] Write test_count_adjacent_edge() in day-04/test_solution.py - roll at grid edge
- [x] T018 [US2] Write test_count_adjacent_corner() in day-04/test_solution.py - roll at grid corner
- [x] T019 [US2] Write test_count_adjacent_full() in day-04/test_solution.py - roll with 8 neighbors
- [x] T020 [US2] Write test_is_valid_position_bounds() in day-04/test_solution.py - boundary checking
- [x] T021 [US2] Run tests - VERIFY ALL FAIL (RED phase validation)

### GREEN Phase: Implement to Pass Tests

- [x] T022 [US2] Complete is_valid_position() with bounds checking in day-04/solution.py
- [x] T023 [US2] Implement count_adjacent_rolls() using DIRECTIONS constant in day-04/solution.py
- [x] T024 [US2] Add loop through 8 directions with boundary validation in day-04/solution.py
- [x] T025 [US2] Run tests - VERIFY ALL PASS (GREEN phase validation)

### REFACTOR Phase: Clean Up

- [x] T026 [US2] Refactor count_adjacent_rolls() for readability if needed - keep tests green
- [x] T027 [US2] Add comprehensive docstrings with direction diagram in day-04/solution.py

**Checkpoint**: Adjacency counting works independently - can count neighbors correctly for any position

---

## Phase 5: User Story 3 - Determine Accessibility and Count Results (Priority: P3)

**Goal**: Identify accessible rolls (< 4 neighbors) and return total count

**Independent Test**: Provide example grid, verify total accessible count is 13

### RED Phase: Write Tests First

- [x] T028 [US3] Write test_is_accessible_threshold() in day-04/test_solution.py - verify < 4 logic
- [x] T029 [US3] Write test_is_accessible_boundary_cases() in day-04/test_solution.py - test 0, 3, 4, 8 neighbors
- [x] T030 [US3] Write test_example_grid() in day-04/test_solution.py - full example expecting 13
- [x] T031 [US3] Write test_single_roll() in day-04/test_solution.py - single '@' should be accessible
- [x] T032 [US3] Write test_all_accessible() in day-04/test_solution.py - grid where all rolls accessible
- [x] T033 [US3] Run tests - VERIFY ALL FAIL (RED phase validation)

### GREEN Phase: Implement to Pass Tests

- [x] T034 [US3] Implement is_accessible(adjacent_count) with < 4 threshold in day-04/solution.py
- [x] T035 [US3] Implement solve_part1(input_data) main function in day-04/solution.py
- [x] T036 [US3] Add loop through grid to find all '@' positions in day-04/solution.py
- [x] T037 [US3] Integrate count_adjacent_rolls() and is_accessible() in solve_part1() in day-04/solution.py
- [x] T038 [US3] Add accessible counter and return statement in day-04/solution.py
- [x] T039 [US3] Run tests - VERIFY ALL PASS (GREEN phase validation)

### REFACTOR Phase: Clean Up

- [x] T040 [US3] Refactor solve_part1() for clarity (extract functions if complex) - keep tests green
- [x] T041 [US3] Optimize grid traversal if needed (profile first) - keep tests green
- [x] T042 [US3] Add comprehensive docstring to solve_part1() in day-04/solution.py

**Checkpoint**: Full solution works - all user stories integrated and testable independently

---

## Phase 6: Integration & Execution

**Purpose**: Add command-line execution and validate against actual input

- [x] T043 Add **main** block to read input.txt and call solve_part1() in day-04/solution.py
- [x] T044 Add formatted output (Part 1: {result}) in day-04/solution.py
- [x] T045 Run `uv run day-04/solution.py` and verify output is numeric
- [x] T046 Run full test suite `uv run pytest day-04/test_solution.py -v` - all tests pass

**Checkpoint**: Solution ready for submission

---

## Phase 7: Polish & Documentation

**Purpose**: Final cleanup and documentation

- [x] T047 [P] Run ruff format on day-04/ to ensure PEP8 compliance
- [x] T048 [P] Run ruff check on day-04/ and fix any linting issues
- [x] T049 [P] Create day-04/README.md with approach notes (optional)
- [x] T050 Verify all functions have docstrings with examples
- [x] T051 Update main README.md progress tracker for Day 4 Part 1 ✅
- [x] T052 Run quickstart.md validation steps from specs/011-day-04-part-1/quickstart.md

**Checkpoint**: Code clean, documented, and ready to commit

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup) → Phase 2 (Foundational) → User Stories (3, 4, 5) → Integration (6) → Polish (7)
                                              ↓
                                    (Can run in parallel if desired)
```

- **Setup (Phase 1)**: Start immediately
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational completion
  - US1 (Parse Grid) → Independent
  - US2 (Count Adjacent) → Independent (uses Foundational utilities)
  - US3 (Accessibility) → Depends on US1 and US2 being complete
- **Integration (Phase 6)**: Depends on all user stories
- **Polish (Phase 7)**: Depends on Integration

### Within Each User Story (TDD Cycle)

```
RED (write tests) → Verify FAIL → GREEN (implement) → Verify PASS → REFACTOR (optimize) → Keep GREEN
```

1. **RED**: Write all test functions for the story
2. **Verify RED**: Run tests, confirm they FAIL
3. **GREEN**: Implement minimum code to pass
4. **Verify GREEN**: Run tests, confirm they PASS
5. **REFACTOR**: Clean code while keeping tests green

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - no dependencies
- **User Story 2 (P2)**: Can start after Foundational - no dependencies
- **User Story 3 (P3)**: Requires US1 (grid parsing) and US2 (adjacency counting) complete

### Parallel Opportunities

#### Within Foundational Phase (Phase 2)

```bash
# These can run in parallel (different concerns):
T005: is_valid_position() implementation
T006: DIRECTIONS constant definition
```

#### Within User Story 1 (Phase 3)

```bash
# RED Phase - write tests in parallel:
T007: test_parse_grid_basic()
T008: test_parse_grid_empty()
T009: test_identify_paper_rolls()
```

#### Within User Story 2 (Phase 4)

```bash
# RED Phase - write tests in parallel:
T016: test_count_adjacent_zero()
T017: test_count_adjacent_edge()
T018: test_count_adjacent_corner()
T019: test_count_adjacent_full()
T020: test_is_valid_position_bounds()
```

#### Within User Story 3 (Phase 5)

```bash
# RED Phase - write tests in parallel:
T028: test_is_accessible_threshold()
T029: test_is_accessible_boundary_cases()
T030: test_example_grid()
T031: test_single_roll()
T032: test_all_accessible()
```

#### Within Polish Phase (Phase 7)

```bash
# These can run in parallel (different files/concerns):
T047: ruff format
T048: ruff check
T049: README.md creation
```

---

## Implementation Strategy

### MVP First (Recommended for AoC Time Constraints)

```
1. Phase 1: Setup (5 min) - T001-T003
2. Phase 2: Foundational (5 min) - T004-T006
3. Phase 3: US1 Complete (10 min) - T007-T015
4. Phase 4: US2 Complete (10 min) - T016-T027
5. Phase 5: US3 Complete (15 min) - T028-T042
6. Phase 6: Integration (5 min) - T043-T046
7. Phase 7: Polish (5 min) - T047-T052
TOTAL: ~55 minutes
```

**Validation Points**:

- After Phase 2: Foundation utilities tested
- After Phase 3: Can parse grid correctly
- After Phase 4: Can count adjacencies correctly
- After Phase 5: Full solution gives correct answer on example
- After Phase 6: Ready to run on actual input and submit

### TDD Discipline Checkpoints

**RED Phase Validation** (Critical):

- T010: Verify US1 tests FAIL ❌
- T021: Verify US2 tests FAIL ❌
- T033: Verify US3 tests FAIL ❌

**GREEN Phase Validation** (Critical):

- T013: Verify US1 tests PASS ✅
- T025: Verify US2 tests PASS ✅
- T039: Verify US3 tests PASS ✅

**REFACTOR Phase** (Keep tests green):

- T014-T015: US1 cleanup
- T026-T027: US2 cleanup
- T040-T042: US3 cleanup

---

## Task Count Summary

| Phase        | Task Count   | Estimated Time | Can Parallelize             |
| ------------ | ------------ | -------------- | --------------------------- |
| Setup        | 3            | 5 min          | No (sequential)             |
| Foundational | 3            | 5 min          | Partial (T005-T006)         |
| US1 (P1)     | 9            | 10 min         | Tests (T007-T009)           |
| US2 (P2)     | 12           | 10 min         | Tests (T016-T020)           |
| US3 (P3)     | 15           | 15 min         | Tests (T028-T032)           |
| Integration  | 4            | 5 min          | No (sequential)             |
| Polish       | 6            | 5 min          | Partial (T047-T049)         |
| **TOTAL**    | **52 tasks** | **~55 min**    | **15 tasks** parallelizable |

---

## Test Coverage Breakdown

### User Story 1 Tests (Grid Parsing)

- Empty grid handling
- Basic grid parsing
- Paper roll position identification

### User Story 2 Tests (Adjacency Counting)

- Zero neighbors case
- Edge position handling
- Corner position handling
- Full neighbors (8 adjacent)
- Boundary validation

### User Story 3 Tests (Accessibility)

- Threshold logic (< 4)
- Boundary cases (0, 3, 4, 8 neighbors)
- Full example grid (13 expected)
- Single roll edge case
- All accessible grid case

**Total Test Functions**: 13 tests across 3 user stories

---

## Success Criteria (from spec.md)

- ✅ **SC-001**: Correctly identifies all 37 paper rolls in example grid
- ✅ **SC-002**: Produces correct answer of 13 accessible rolls for example
- ✅ **SC-003**: Correctly counts adjacent rolls for edge positions
- ✅ **SC-004**: Correctly counts adjacent rolls for corner positions
- ✅ **SC-005**: Handles full puzzle input in < 1 second
- ✅ **SC-006**: All test scenarios pass including edge cases

**Validation**: All criteria tested through user story test cases

---

## Notes

- All tasks follow TDD RED-GREEN-REFACTOR cycle (Constitution Principle IV)
- [P] tasks can run in parallel (different files, no dependencies)
- [Story] label maps task to user story for traceability
- Each user story independently testable
- Tests MUST fail before implementation (RED phase)
- Commit after each user story phase completion
- Use `uv run` for all executions (Constitution Principle V)
- Manual submission to AoC after validation (Constitution Principle VI)

---

## References

- **Specification**: `specs/011-day-04-part-1/spec.md`
- **Implementation Plan**: `specs/011-day-04-part-1/plan.md`
- **Data Model**: `specs/011-day-04-part-1/data-model.md`
- **Contracts**: `specs/011-day-04-part-1/contracts/function-interface.md`
- **Quickstart Guide**: `specs/011-day-04-part-1/quickstart.md`
- **Research Notes**: `specs/011-day-04-part-1/research.md`
- **Constitution**: `.specify/memory/constitution.md`
