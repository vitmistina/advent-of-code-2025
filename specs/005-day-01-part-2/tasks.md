---
description: "Task list for Day 1 Part 2 - Zero Crossing Count Implementation"
---

# Tasks: Day 1 Part 2 Solution

**Input**: Design documents from `/specs/005-day-01-part-2/`  
**Prerequisites**: plan.md ✓, spec.md ✓, research.md ✓, data-model.md ✓, contracts/ ✓

**Tests**: Tests are REQUIRED per Constitution Principle IV (TDD - NON-NEGOTIABLE)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

This is a single-project solution following Advent of Code structure:

- **Solution**: `day-01/solution.py`
- **Tests**: `day-01/test_solution.py`
- **Inputs**: `day-01/input.txt`, `day-01/test_input.txt`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Verify existing Part 1 infrastructure is ready for Part 2 extension

- [x] T001 Verify day-01/ folder exists with solution.py, test_solution.py, input.txt
- [x] T002 Verify Part 1 functions (parse_input, apply_rotation, solve_part1) are implemented
- [x] T003 Verify test_input.txt contains sample input from puzzle description

**Note**: All setup tasks are already complete from Part 1. No new infrastructure needed.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: No foundational tasks needed - Part 1 infrastructure is sufficient

**⚠️ SKIP**: This phase is not applicable for Advent of Code solution extensions

**Checkpoint**: Foundation ready (already complete from Part 1) - user story implementation can begin

---

## Phase 3: User Story 1 - Count All Zero Crossings (Priority: P1) 🎯 MVP

**Goal**: Implement Part 2 solution that counts all zero crossings (during + after rotations) and returns 6 for sample input

**Independent Test**: Run `uv run pytest day-01/test_solution.py::test_solve_part2_sample_input -v` and verify result is 6

### RED: Write Failing Tests for User Story 1 (TDD Phase 1)

> **CRITICAL**: Write these tests FIRST, ensure they FAIL before any implementation

- [ ] T004 [US1] Add test_count_zero_crossings_during_rotation() with parameterized test cases in day-01/test_solution.py

  - Include edge cases: zero distance, right rotation (multi-wrap, boundary, no cross), left rotation (cross once, don't reach, from zero, multi-wrap)
  - Expected: ImportError or AttributeError (function doesn't exist yet) - MUST FAIL

- [ ] T005 [US1] Add test_solve_part2_sample_input() in day-01/test_solution.py

  - Parse sample input and call solve_part2()
  - Assert result == 6 (3 during + 3 at end)
  - Expected: ImportError or AttributeError (function doesn't exist yet) - MUST FAIL

- [ ] T006 [US1] Run tests and verify they FAIL with `uv run pytest day-01/test_solution.py::test_count_zero_crossings_during_rotation -v`

  - Document failure output (should show function not found)
  - **GATE**: Do not proceed until tests are confirmed FAILING

- [ ] T007 [US1] Run tests and verify they FAIL with `uv run pytest day-01/test_solution.py::test_solve_part2_sample_input -v`
  - Document failure output (should show function not found)
  - **GATE**: Do not proceed until tests are confirmed FAILING

### GREEN: Implement Minimum Code for User Story 1 (TDD Phase 2)

> **CRITICAL**: Implement ONLY enough code to make tests pass - no more, no less

- [ ] T008 [US1] Implement count_zero_crossings_during_rotation() in day-01/solution.py

  - Add function signature with type hints: (int, str, int) -> int
  - Add comprehensive docstring with examples and complexity (O(1))
  - Implement right rotation formula: (start + distance) // 100
  - Implement left rotation formula: max(0, (distance - start + 99) // 100)
  - Add direction validation (raise ValueError for invalid)
  - Handle zero distance edge case

- [ ] T009 [US1] Implement solve_part2() in day-01/solution.py

  - Add function signature with type hints: (list[tuple[str, int]]) -> int
  - Add docstring with description and complexity (O(n))
  - Initialize position = 50, total_zero_count = 0
  - Loop through rotations:
    - Call count_zero_crossings_during_rotation() and add to total
    - Apply rotation using existing apply_rotation()
    - If position == 0, increment total
  - Return total_zero_count

- [ ] T010 [US1] Update main() in day-01/solution.py to call solve_part2()

  - Add line: `part2_answer = solve_part2(data)`
  - Add line: `print(f"Part 2: {part2_answer}")`
  - Keep existing Part 1 code unchanged

- [ ] T011 [US1] Run test_count_zero_crossings_during_rotation and verify it PASSES

  - Command: `uv run pytest day-01/test_solution.py::test_count_zero_crossings_during_rotation -v`
  - Expected: All parameterized test cases pass
  - **GATE**: If any test fails, fix implementation before proceeding

- [ ] T012 [US1] Run test_solve_part2_sample_input and verify it PASSES
  - Command: `uv run pytest day-01/test_solution.py::test_solve_part2_sample_input -v`
  - Expected: Test passes with result == 6
  - **GATE**: If test fails, fix implementation before proceeding

### REFACTOR: Clean Up Code for User Story 1 (TDD Phase 3)

> **CRITICAL**: Improve code quality while keeping tests GREEN

- [ ] T013 [US1] Run Ruff linter on day-01/solution.py

  - Command: `uv run ruff check day-01/solution.py`
  - Fix any linting errors (PEP8 compliance)

- [ ] T014 [US1] Run Ruff formatter on day-01/solution.py

  - Command: `uv run ruff format day-01/solution.py`
  - Ensure consistent code style

- [ ] T015 [US1] Verify all tests still pass after refactoring
  - Command: `uv run pytest day-01/test_solution.py -v`
  - Expected: All tests pass (Part 1 + Part 2)
  - **GATE**: If any test fails, revert refactoring

**Checkpoint**: User Story 1 complete - Part 2 returns 6 for sample input, all tests pass

---

## Phase 4: User Story 2 - Handle Multi-Wrap Rotations (Priority: P2)

**Goal**: Ensure large rotation distances (multi-wrap scenarios) are correctly handled

**Independent Test**: Run `uv run pytest day-01/test_solution.py::test_multi_wrap_rotations -v` and verify all cases pass

### RED: Write Failing Tests for User Story 2 (TDD Phase 1)

- [ ] T016 [US2] Add test_multi_wrap_rotations() in day-01/test_solution.py

  - Test case 1: position=50, R1000 → expect 10 crossings during
  - Test case 2: position=0, R100 → expect 1 crossing (end only)
  - Test case 3: position=50, L150 → expect 3 total (2 during + 1 end)
  - Use parameterized test with @pytest.mark.parametrize
  - Expected: Tests should PASS (already implemented in US1) or reveal edge cases

- [ ] T017 [US2] Run test and verify behavior
  - Command: `uv run pytest day-01/test_solution.py::test_multi_wrap_rotations -v`
  - If tests PASS: US2 already handled by US1 implementation ✓
  - If tests FAIL: Identify gap in count_zero_crossings_during_rotation()

### GREEN: Fix Any Multi-Wrap Issues (TDD Phase 2)

- [ ] T018 [US2] Fix count_zero_crossings_during_rotation() if needed

  - Only required if T017 revealed failures
  - Verify formula handles large distances (>100)
  - Ensure no integer overflow for distances up to 10,000

- [ ] T019 [US2] Verify multi-wrap tests pass
  - Command: `uv run pytest day-01/test_solution.py::test_multi_wrap_rotations -v`
  - **GATE**: All multi-wrap tests must pass

### REFACTOR: Optimize for Large Distances (TDD Phase 3)

- [ ] T020 [US2] Add performance test for large inputs (optional)

  - Test 10,000 rotations with distances up to 10,000
  - Assert completion time < 2 seconds
  - Validate result is non-negative

- [ ] T021 [US2] Verify all tests still pass
  - Command: `uv run pytest day-01/test_solution.py -v`
  - Expected: All tests pass including performance test

**Checkpoint**: User Story 2 complete - multi-wrap rotations handled correctly, performance validated

---

## Phase 5: User Story 3 - Maintain Backward Compatibility (Priority: P3)

**Goal**: Ensure Part 1 solution still works correctly and Part 2 >= Part 1 invariant holds

**Independent Test**: Run `uv run pytest day-01/test_solution.py::test_part1_compatibility -v` and verify Part 1 unchanged

### RED: Write Failing Tests for User Story 3 (TDD Phase 1)

- [ ] T022 [US3] Add test_part1_unchanged() in day-01/test_solution.py

  - Test solve_part1() with sample input
  - Assert result == 3 (original Part 1 answer)
  - Expected: Should PASS (Part 1 not modified)

- [ ] T023 [US3] Add test_part2_includes_part1() in day-01/test_solution.py

  - Test both solve_part1() and solve_part2() with same input
  - Assert part2_result >= part1_result
  - Test with sample input and multiple custom inputs
  - Expected: Should PASS (mathematical invariant)

- [ ] T024 [US3] Run compatibility tests
  - Command: `uv run pytest day-01/test_solution.py::test_part1_unchanged -v`
  - Command: `uv run pytest day-01/test_solution.py::test_part2_includes_part1 -v`
  - If any test FAILS: Identify backward compatibility issue

### GREEN: Fix Any Compatibility Issues (TDD Phase 2)

- [ ] T025 [US3] Verify solve_part1() implementation unchanged

  - Review code changes - ensure no modifications to solve_part1()
  - Review apply_rotation() - ensure no modifications
  - Review parse_input() - ensure no modifications

- [ ] T026 [US3] Verify Part 2 >= Part 1 invariant

  - If test fails: Debug solve_part2() logic
  - Ensure end-position zeros are counted in Part 2
  - Ensure during-rotation zeros are non-negative

- [ ] T027 [US3] Run all compatibility tests
  - Command: `uv run pytest day-01/test_solution.py -k compatibility -v`
  - **GATE**: All compatibility tests must pass

### REFACTOR: Add Documentation (TDD Phase 3)

- [ ] T028 [US3] Add edge case tests for empty input

  - Test solve_part2([]) == 0
  - Test solve_part1([]) == 0

- [ ] T029 [US3] Verify complete test suite passes
  - Command: `uv run pytest day-01/test_solution.py -v`
  - Expected: All tests pass (US1 + US2 + US3)

**Checkpoint**: User Story 3 complete - backward compatibility verified, invariants validated

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and documentation

- [ ] T030 Run complete test suite with coverage

  - Command: `uv run pytest day-01/test_solution.py --cov=day-01/solution --cov-report=term-missing -v`
  - Verify coverage >= 90% for solution.py

- [ ] T031 Run solution with test input

  - Command: `uv run python day-01/solution.py` (using test_input.txt manually)
  - Verify output: Part 1: 3, Part 2: 6

- [ ] T032 Run solution with actual input

  - Command: `uv run python day-01/solution.py`
  - Verify Part 2 >= Part 1
  - Copy Part 2 answer for manual submission

- [ ] T033 [P] Create day-01/README.md with notes (optional)

  - Document zero crossing algorithm
  - Note performance: O(1) per rotation, O(n) total
  - Include link to research.md for details

- [ ] T034 Update main README.md progress tracker

  - Mark Day 1 Part 2 as complete
  - Add any learnings or insights

- [ ] T035 Final validation using quickstart.md

  - Follow all commands in quickstart.md
  - Verify all steps work as documented
  - Fix any discrepancies

- [ ] T036 Commit changes

  - Command: `git add day-01/ specs/005-day-01-part-2/`
  - Command: `git commit -m "feat: solve day 1 part 2 - count all zero crossings"`

- [ ] T037 Merge to main (after submission)
  - Submit Part 2 answer manually at adventofcode.com
  - After successful submission: `git checkout main && git merge 005-day-01-part-2`
  - Push to remote

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Already complete from Part 1 ✓
- **Foundational (Phase 2)**: Skipped (not applicable) ✓
- **User Story 1 (Phase 3)**: Can start immediately - CORE MVP
- **User Story 2 (Phase 4)**: Can start after US1 - validates edge cases
- **User Story 3 (Phase 5)**: Can start after US1 - validates compatibility
- **Polish (Phase 6)**: Depends on all user stories complete

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies - can start immediately (MVP)
- **User Story 2 (P2)**: Logically depends on US1 (extends same functions) - but tests can be written in parallel
- **User Story 3 (P3)**: Depends on US1 being complete to validate backward compatibility

### Within Each User Story (TDD Cycle)

1. **RED**: Write tests → Run tests → Verify they FAIL
2. **GREEN**: Implement code → Run tests → Verify they PASS
3. **REFACTOR**: Clean code → Run tests → Verify still PASS

**CRITICAL**: Never skip RED phase - tests must fail first to be valid

### Parallel Opportunities

Within User Story 1:

- T004 and T005 can be written in parallel (different test functions)
- T006 and T007 can run in parallel (independent test verification)
- T011 and T012 run sequentially (after implementation)
- T013 and T014 run sequentially (refactoring steps)

Across User Stories (if team has multiple developers):

- After US1 GREEN phase (T008-T010), US2 and US3 tests can be written in parallel
- US2 and US3 can be validated concurrently once US1 is complete

Polish Phase:

- T030, T031, T032 run sequentially (validation steps)
- T033 and T034 can run in parallel (documentation)

---

## Parallel Example: User Story 1 RED Phase

```bash
# Terminal 1: Write test for count_zero_crossings_during_rotation
# T004: day-01/test_solution.py

# Terminal 2: Write test for solve_part2
# T005: day-01/test_solution.py

# After both complete, verify failures:
uv run pytest day-01/test_solution.py::test_count_zero_crossings_during_rotation -v
uv run pytest day-01/test_solution.py::test_solve_part2_sample_input -v
```

---

## Implementation Strategy

### TDD MVP First (Recommended)

1. ✅ Phase 1: Setup (already complete)
2. ✅ Phase 2: Foundational (skipped - not needed)
3. **RED**: T004-T007 → Write tests, verify FAIL
4. **GREEN**: T008-T012 → Implement, verify PASS
5. **REFACTOR**: T013-T015 → Clean, verify PASS
6. **VALIDATE**: Run solution, verify sample returns 6
7. **SUBMIT**: Manual submission at adventofcode.com

### Incremental Delivery

- **MVP (US1)**: Core zero crossing count → Sample input returns 6
- **Edge Cases (US2)**: Multi-wrap validation → Large distances work
- **Validation (US3)**: Backward compatibility → Part 1 still works
- **Polish**: Documentation, final validation → Ready to merge

### TDD Discipline

- **Constitution Principle IV is NON-NEGOTIABLE**
- Tests MUST be written first
- Tests MUST fail before implementation
- Tests MUST pass after implementation
- Tests MUST remain passing after refactoring

---

## Notes

- **[P]** tasks = different files, can run in parallel
- **[Story]** label = traceability to spec.md user stories
- **TDD gates** = do not proceed until phase complete
- All file paths are exact (day-01/solution.py, day-01/test_solution.py)
- Test-first workflow enforced per Constitution Principle IV
- Sample input expected result: 6 (3 during + 3 at end)
- Performance target: <2s for 10k rotations × 10k distance

---

## Success Criteria Validation

After completing all tasks:

- ✅ **SC-001**: Sample input returns 6 (verified by T012)
- ✅ **SC-002**: R1000 from position 50 returns 10 crossings (verified by T016-T019)
- ✅ **SC-003**: Part 1 still returns 3 for sample (verified by T022)
- ✅ **SC-004**: Part 2 >= Part 1 for all inputs (verified by T023)
- ✅ **SC-005**: Performance <2s for large inputs (verified by T020)
- ✅ **SC-006**: 100% acceptance scenarios testable (all user stories have tests)
