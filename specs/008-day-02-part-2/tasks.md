---
description: "Task breakdown for Day 2 Part 2 - Invalid Product ID Detection (Extended Pattern)"
---

# Tasks: Day 2 Part 2 - Invalid Product ID Detection (Extended Pattern)

**Input**: Design documents from `specs/008-day-02-part-2/`  
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md  
**Feature Branch**: `008-day-02-part-2`

**Tests**: This feature follows TDD (Test-Driven Development) with RED-GREEN-REFACTOR cycle. All test tasks are marked as **RED phase** and must be completed before implementation.

**Organization**: Tasks are organized by TDD phases to ensure proper test-driven development workflow. Part 1 backward compatibility is verified throughout.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[US1]**: User Story 1 - Identify Invalid IDs with Any Repeated Pattern (P1)
- **[US2]**: User Story 2 - Process Multiple Ranges Efficiently (P2)
- Include exact file paths in descriptions

---

## Phase 1: Setup & Verification (Pre-implementation)

**Purpose**: Verify Part 1 foundation is solid before extending with Part 2

- [X] T001 Verify Part 1 tests pass by running `uv run pytest day-02/test_solution.py::test_solve_part1_example -v`
- [X] T002 Verify Part 1 solution executes by running `uv run python day-02/solution.py --part 1`
- [X] T003 Verify input file exists at `day-02/input.txt` (reused from Part 1)
- [X] T004 Review Part 1 functions to identify reusable components (parse_input, range structure)

**Checkpoint**: Part 1 baseline verified - safe to extend with Part 2

---

## Phase 2: User Story 1 - Identify Invalid IDs with Any Repeated Pattern (Priority: P1) 🎯 MVP

**Goal**: Implement core Part 2 logic to detect invalid IDs where digit patterns are repeated at least twice (vs exactly twice in Part 1)

**Independent Test**: Can be fully tested with individual ranges (11-22, 95-115, etc.) and verified against expected invalid ID lists from spec

### RED Phase: Write Failing Tests for User Story 1

> **CRITICAL**: Write these tests FIRST, ensure they FAIL before implementation

- [X] T005 [P] [US1] Write test `test_is_invalid_id_part2()` in `day-02/test_solution.py` to verify pattern detection with ≥2 repetitions (tests for 11, 111, 565656, 824824824, 2121212121, and valid cases)
- [X] T006 [P] [US1] Write test `test_check_range_part2_range_11_22()` in `day-02/test_solution.py` to verify range 11-22 produces [11, 22]
- [X] T007 [P] [US1] Write test `test_check_range_part2_range_95_115()` in `day-02/test_solution.py` to verify range 95-115 produces [99, 111]
- [X] T008 [P] [US1] Write test `test_check_range_part2_range_998_1012()` in `day-02/test_solution.py` to verify range 998-1012 produces [999, 1010]
- [X] T009 [P] [US1] Write test `test_check_range_part2_range_1188511880_1188511890()` in `day-02/test_solution.py` to verify range 1188511880-1188511890 produces [1188511885]
- [X] T010 [P] [US1] Write test `test_check_range_part2_range_222220_222224()` in `day-02/test_solution.py` to verify range 222220-222224 produces [222222]
- [X] T011 [P] [US1] Write test `test_check_range_part2_range_1698522_1698528()` in `day-02/test_solution.py` to verify range 1698522-1698528 produces [] (no invalids)
- [X] T012 [P] [US1] Write test `test_check_range_part2_range_446443_446449()` in `day-02/test_solution.py` to verify range 446443-446449 produces [446446]
- [X] T013 [P] [US1] Write test `test_check_range_part2_range_38593856_38593862()` in `day-02/test_solution.py` to verify range 38593856-38593862 produces [38593859]
- [X] T014 [P] [US1] Write test `test_check_range_part2_range_565653_565659()` in `day-02/test_solution.py` to verify range 565653-565659 produces [565656]
- [X] T015 [P] [US1] Write test `test_check_range_part2_range_824824821_824824827()` in `day-02/test_solution.py` to verify range 824824821-824824827 produces [824824824]
- [X] T016 [P] [US1] Write test `test_check_range_part2_range_2121212118_2121212124()` in `day-02/test_solution.py` to verify range 2121212118-2121212124 produces [2121212121]
- [X] T017 [US1] Run all Part 2 tests with `uv run pytest day-02/test_solution.py -k part2 -v` and verify they FAIL (expected: NameError or assertion failures)

**Checkpoint**: All Part 2 tests written and failing - ready for GREEN phase

### GREEN Phase: Implement Solution for User Story 1

> **CRITICAL**: Implement ONLY enough code to pass tests, no more

- [X] T018 [US1] Implement `is_invalid_id_part2(num: int) -> bool` in `day-02/solution.py` with divisor-based pattern matching algorithm (iterate pattern_len from 1 to n//2, check if pattern\*repetitions == s and repetitions >= 2)
- [X] T019 [US1] Implement `check_range_part2(start: int, end: int) -> list[int]` in `day-02/solution.py` to iterate range and collect invalid IDs using is_invalid_id_part2()
- [X] T020 [US1] Run `uv run pytest day-02/test_solution.py::test_is_invalid_id_part2 -v` and verify test PASSES
- [X] T021 [US1] Run all individual range tests (T006-T016) with `uv run pytest day-02/test_solution.py -k check_range_part2 -v` and verify all PASS

**Checkpoint**: Core Part 2 pattern detection implemented and all User Story 1 tests passing

### REFACTOR Phase: Optimize and Clean User Story 1

- [X] T022 [US1] Add comprehensive docstrings to `is_invalid_id_part2()` and `check_range_part2()` in `day-02/solution.py`
- [X] T023 [US1] Add type hints to all Part 2 functions in `day-02/solution.py`
- [X] T024 [US1] Run `ruff check day-02/solution.py` and fix any linting issues
- [X] T025 [US1] Re-run all Part 2 tests with `uv run pytest day-02/test_solution.py -k part2 -v` to verify refactoring didn't break anything

**Checkpoint**: User Story 1 complete - pattern detection works for individual ranges

---

## Phase 3: User Story 2 - Process Multiple Ranges Efficiently (Priority: P2)

**Goal**: Aggregate results across multiple comma-separated ranges and produce final sum

**Independent Test**: Can be tested by providing multi-range input string and verifying the aggregated sum matches expected output (4174379265)

### RED Phase: Write Failing Tests for User Story 2

- [X] T026 [US2] Write test `test_solve_part2_example()` in `day-02/test_solution.py` to verify complete example input produces sum 4174379265
- [X] T027 [US2] Write test `test_solve_part2_multiple_ranges()` in `day-02/test_solution.py` to verify multi-range aggregation (test with subset of ranges)
- [X] T028 [US2] Write test `test_solve_part2_empty_input()` in `day-02/test_solution.py` to verify empty string input returns 0
- [X] T029 [US2] Run Part 2 integration tests with `uv run pytest day-02/test_solution.py::test_solve_part2_example -v` and verify they FAIL

**Checkpoint**: Integration tests written and failing - ready to implement solve_part2()

### GREEN Phase: Implement Solution for User Story 2

- [X] T030 [US2] Implement `solve_part2(input_data: str) -> int` in `day-02/solution.py` to parse ranges (reuse parse_input), call check_range_part2() for each range, and sum all invalid IDs
- [X] T031 [US2] Run `uv run pytest day-02/test_solution.py::test_solve_part2_example -v` and verify test PASSES with expected sum 4174379265
- [X] T032 [US2] Run all User Story 2 tests with `uv run pytest day-02/test_solution.py -k solve_part2 -v` and verify all PASS

**Checkpoint**: Multi-range aggregation working - User Story 2 complete

### REFACTOR Phase: Optimize and Clean User Story 2

- [X] T033 [US2] Add comprehensive docstring to `solve_part2()` in `day-02/solution.py` explaining input format, algorithm, and return value
- [X] T034 [US2] Review performance: run `uv run python day-02/solution.py --part 2` and verify completes in <5 seconds
- [X] T035 [US2] Run complete test suite with `uv run pytest day-02/test_solution.py -v` and verify all tests PASS (Part 1 + Part 2)

**Checkpoint**: All user stories implemented and tested - solution complete

---

## Phase 4: Integration & Backward Compatibility Verification

**Purpose**: Ensure Part 1 remains unaffected and Part 2 integrates cleanly

- [X] T036 Verify Part 1 tests still pass by running `uv run pytest day-02/test_solution.py::test_solve_part1_example -v`
- [X] T037 Verify Part 1 solution still produces correct output with `uv run python day-02/solution.py --part 1`
- [X] T038 Run full test suite with `uv run pytest day-02/test_solution.py -v` and verify 100% pass rate
- [X] T039 Update CLI in `day-02/solution.py` to support `--part 2` argument if not already implemented

**Checkpoint**: Full backward compatibility verified - Part 1 and Part 2 both working

---

## Phase 5: Documentation & Polish

**Purpose**: Update documentation to reflect Part 2 completion

- [X] T040 [P] Update `day-02/README.md` to document Part 2 completion, approach (divisor-based pattern matching), and results
- [X] T041 [P] Verify all functions in `day-02/solution.py` have docstrings and type hints
- [X] T042 Run final linting check with `ruff check day-02/` and fix any remaining issues
- [X] T043 Run quickstart validation: follow steps in `specs/008-day-02-part-2/quickstart.md` and verify all examples work
- [X] T044 Create git commit: `git commit -m "feat: solve day 2 part 2 - extended pattern detection (at least twice)"`

**Checkpoint**: Feature complete, documented, and ready for submission

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - verifies baseline
- **User Story 1 (Phase 2)**: Depends on Setup completion - implements core pattern detection
  - RED phase MUST complete before GREEN phase
  - GREEN phase MUST complete before REFACTOR phase
- **User Story 2 (Phase 3)**: Depends on User Story 1 GREEN phase (needs check_range_part2)
  - RED phase MUST complete before GREEN phase
  - GREEN phase MUST complete before REFACTOR phase
- **Integration (Phase 4)**: Depends on both User Stories completing
- **Documentation (Phase 5)**: Depends on Integration verification passing

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Setup - No dependencies on other stories
  - Implements: Pattern detection algorithm, range checking
  - Deliverable: Individual range validation working
- **User Story 2 (P2)**: Depends on User Story 1 completing GREEN phase
  - Needs: check_range_part2() function from US1
  - Implements: Multi-range aggregation, final sum calculation
  - Deliverable: Complete solution with example sum validation

### Within Each User Story

**User Story 1**:

1. RED phase (T005-T017): Write all tests first
   - All test tasks (T005-T016) can run in parallel (marked [P])
   - T017 verification must run after all tests written
2. GREEN phase (T018-T021): Implement in order
   - T018: Core pattern detector (blocks T019)
   - T019: Range checker (uses T018)
   - T020-T021: Verification tasks (run after implementation)
3. REFACTOR phase (T022-T025): Clean up in order

**User Story 2**:

1. RED phase (T026-T029): Write integration tests
   - T026-T028 can run in parallel (marked [P] candidates)
   - T029 verification runs after tests written
2. GREEN phase (T030-T032): Implement aggregation
   - T030: Solve function (blocks T031-T032)
   - T031-T032: Verification tasks
3. REFACTOR phase (T033-T035): Optimize and verify

### Parallel Opportunities

- **Setup Phase**: All verification tasks (T001-T003) can run in parallel, T004 review after
- **US1 RED Phase**: All test writing tasks (T005-T016) can run in parallel - 12 independent test files
- **US1 GREEN Phase**: Sequential - T018 must complete before T019
- **US2 RED Phase**: Test tasks (T026-T028) can run in parallel
- **Documentation Phase**: Tasks T040-T041 can run in parallel (README vs docstrings)

---

## Parallel Example: User Story 1 RED Phase

```bash
# Launch all test writing tasks together (T005-T016):
Task: "Write test test_is_invalid_id_part2() in day-02/test_solution.py"
Task: "Write test test_check_range_part2_range_11_22() in day-02/test_solution.py"
Task: "Write test test_check_range_part2_range_95_115() in day-02/test_solution.py"
Task: "Write test test_check_range_part2_range_998_1012() in day-02/test_solution.py"
# ... (all 12 test tasks can be written independently)

# Then run verification:
Task: "Run all Part 2 tests and verify they FAIL"
```

---

## Implementation Strategy

### TDD First (RED-GREEN-REFACTOR)

1. Complete Phase 1: Setup verification
2. **RED Phase for US1**: Write ALL tests first (T005-T017) → Tests must FAIL
3. **GREEN Phase for US1**: Implement minimum code (T018-T021) → Tests must PASS
4. **REFACTOR Phase for US1**: Clean up (T022-T025) → Tests stay green
5. **RED Phase for US2**: Write integration tests (T026-T029) → Tests must FAIL
6. **GREEN Phase for US2**: Implement aggregation (T030-T032) → Tests must PASS
7. **REFACTOR Phase for US2**: Optimize (T033-T035) → Tests stay green
8. Verify backward compatibility (Phase 4)
9. Polish and document (Phase 5)

### Incremental Delivery

1. Complete Setup (Phase 1) → Foundation verified
2. Complete User Story 1 → Pattern detection works for single ranges (MVP!)
   - Test with individual range: `check_range_part2(11, 22)` → `[11, 22]`
3. Complete User Story 2 → Full solution with multi-range aggregation
   - Test with complete example → `4174379265`
4. Complete Integration → Part 1 compatibility verified
5. Complete Documentation → Feature ready for submission

### Checkpoint Strategy

Stop at any checkpoint to validate:

- **After Phase 1**: Part 1 baseline solid
- **After US1 RED**: All single-range tests fail appropriately
- **After US1 GREEN**: Pattern detection working
- **After US1 REFACTOR**: Code clean, single ranges validated
- **After US2 GREEN**: Complete solution with example sum
- **After Phase 4**: Full backward compatibility verified

---

## Notes

- **[P] tasks**: Can be parallelized (different test cases, different concerns)
- **[US1]/[US2] labels**: Map tasks to specific user stories for traceability
- **TDD enforced**: RED phase MUST complete before GREEN phase (non-negotiable per Constitution Principle IV)
- **Part 1 preservation**: Verified at multiple checkpoints (T001-T002, T036-T037)
- **Example validation**: Expected sum 4174379265 validated in T026, T031
- **Performance target**: <5 seconds for actual input (verified in T034)
- **Commit strategy**: Single feature commit after all phases complete (T044)

---

## Success Metrics

From spec.md Success Criteria:

- **SC-001**: System correctly identifies all 13 invalid IDs from example ranges
  - Validated by: T006-T016 (individual range tests)
- **SC-002**: System produces exact sum of 4174379265 for complete example input
  - Validated by: T026, T031 (solve_part2_example test)
- **SC-003**: System processes all 11 ranges in example input
  - Validated by: T030-T032 (multi-range aggregation)
- **SC-004**: Part 1 tests remain green (backward compatibility)
  - Validated by: T036-T038 (integration verification)

---

## Total Tasks: 44

- Phase 1 (Setup): 4 tasks
- Phase 2 (User Story 1): 21 tasks
  - RED: 13 tasks (T005-T017)
  - GREEN: 4 tasks (T018-T021)
  - REFACTOR: 4 tasks (T022-T025)
- Phase 3 (User Story 2): 10 tasks
  - RED: 4 tasks (T026-T029)
  - GREEN: 3 tasks (T030-T032)
  - REFACTOR: 3 tasks (T033-T035)
- Phase 4 (Integration): 4 tasks (T036-T039)
- Phase 5 (Documentation): 5 tasks (T040-T044)

**Parallel Opportunities**: 15 tasks marked [P] (34% can run in parallel)

**MVP Scope**: Phase 1 + Phase 2 (User Story 1 complete) = 25 tasks  
**Complete Feature**: All 44 tasks

---

## References

- **Specification**: `specs/008-day-02-part-2/spec.md`
- **Implementation Plan**: `specs/008-day-02-part-2/plan.md`
- **Algorithm Research**: `specs/008-day-02-part-2/research.md`
- **Data Model**: `specs/008-day-02-part-2/data-model.md`
- **API Contracts**: `specs/008-day-02-part-2/contracts/api-contract.md`
- **TDD Workflow Guide**: `specs/008-day-02-part-2/quickstart.md`
- **AoC Constitution**: `.specify/constitution.md`
