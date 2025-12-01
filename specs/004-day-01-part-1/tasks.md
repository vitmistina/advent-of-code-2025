---
description: "Task list for Day 1 Part 1 implementation"
---

# Tasks: Day 1 Part 1 - Secret Entrance

**Input**: Design documents from `/specs/004-day-01-part-1/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

**TDD Approach**: This feature follows strict Test-Driven Development (RED-GREEN-REFACTOR). All tests MUST be written first and verified to FAIL before implementation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [ID] [P?] [Story] Description`

- **Checkbox**: `- [ ]` for markdown task lists
- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Solution code**: `day-01/solution.py`
- **Tests**: `day-01/test_solution.py`
- **Input files**: `day-01/input.txt`, `day-01/test_input.txt`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

**Status**: ✅ Already complete (scaffolded by meta runner)

- [x] T001 Create day-01/ folder structure
- [x] T002 Create solution.py with function stubs
- [x] T003 Create test_solution.py with pytest fixtures
- [x] T004 Download input.txt and test_input.txt
- [x] T005 Download description.md

**Checkpoint**: ✅ Day folder scaffolded and ready for TDD

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: None - this is a standalone solution with no shared infrastructure needed

**Note**: Advent of Code daily puzzles don't require foundational infrastructure. We proceed directly to user stories.

**Checkpoint**: ✅ Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Count Zero Positions (Priority: P1) 🎯 MVP

**Goal**: Implement core functionality to count how many times the dial points at 0 after applying rotation instructions

**Independent Test**: Provide sample input from puzzle, verify it returns 3

### RED Phase - Write Failing Tests First ⚠️

**CRITICAL**: These tests MUST be written first and verified to FAIL before any implementation

- [ ] T006 [P] [US1] Write test_parse_input_sample in day-01/test_solution.py
  - Test parsing the 10-line sample input
  - Verify first rotation is ('L', 68)
  - Verify last rotation is ('L', 82)
  - **Run and verify it FAILS** ❌

- [ ] T007 [P] [US1] Write test_parse_input_empty in day-01/test_solution.py
  - Test parsing empty input
  - Verify returns empty list
  - **Run and verify it FAILS** ❌

- [ ] T008 [P] [US1] Write test_apply_rotation_left in day-01/test_solution.py
  - Test left rotation: 50 → L68 → 82
  - Test left rotation: 82 → L30 → 52
  - Test wraparound: 5 → L10 → 95
  - **Run and verify it FAILS** ❌

- [ ] T009 [P] [US1] Write test_apply_rotation_right in day-01/test_solution.py
  - Test right rotation: 52 → R48 → 0
  - Test right rotation: 95 → R60 → 55
  - Test wraparound: 99 → R1 → 0
  - **Run and verify it FAILS** ❌

- [ ] T010 [P] [US1] Write test_apply_rotation_zero_distance in day-01/test_solution.py
  - Test no movement: 50 → L0 → 50
  - Test no movement: 50 → R0 → 50
  - **Run and verify it FAILS** ❌

- [ ] T011 [US1] Write test_solve_part1_sample in day-01/test_solution.py
  - Test with full sample input (10 rotations)
  - Verify result is 3
  - **Run and verify it FAILS** ❌

- [ ] T012 [P] [US1] Write test_solve_part1_empty in day-01/test_solution.py
  - Test with empty rotation list
  - Verify result is 0
  - **Run and verify it FAILS** ❌

- [ ] T013 [P] [US1] Write test_solve_part1_no_zeros in day-01/test_solution.py
  - Test with rotations that never land on 0
  - Example: [('L', 10), ('R', 5)]
  - Verify result is 0
  - **Run and verify it FAILS** ❌

**Checkpoint**: ✅ All tests written and FAILING (RED phase complete)

### GREEN Phase - Implement to Pass Tests

- [ ] T014 [US1] Implement parse_input() in day-01/solution.py
  - Parse multi-line string into list of (direction, distance) tuples
  - Handle empty lines (skip them)
  - Extract direction from line[0], distance from int(line[1:])
  - **Run tests - T006, T007 should now PASS** ✅

- [ ] T015 [US1] Implement apply_rotation() in day-01/solution.py
  - Left rotation: `(position - distance) % 100`
  - Right rotation: `(position + distance) % 100`
  - Handle wraparound via modulo arithmetic
  - **Run tests - T008, T009, T010 should now PASS** ✅

- [ ] T016 [US1] Implement solve_part1() in day-01/solution.py
  - Initialize position to 50, zero_count to 0
  - Iterate through rotations
  - Apply each rotation, increment count if position == 0
  - Return zero_count
  - **Run tests - T011, T012, T013 should now PASS** ✅

- [ ] T017 [US1] Verify all User Story 1 tests pass
  - Run: `uv run pytest day-01/test_solution.py -v`
  - All 8 tests (T006-T013) should be GREEN ✅

**Checkpoint**: ✅ All User Story 1 tests passing (GREEN phase complete)

### REFACTOR Phase - Clean Up Code

- [ ] T018 [US1] Add type hints to all functions in day-01/solution.py
  - parse_input(input_text: str) -> list[tuple[str, int]]
  - apply_rotation(position: int, direction: str, distance: int) -> int
  - solve_part1(rotations: list[tuple[str, int]]) -> int
  - **Run tests - all should still PASS** ✅

- [ ] T019 [US1] Add comprehensive docstrings in day-01/solution.py
  - Document parameters, return values, behavior
  - Include example usage in docstrings
  - **Run tests - all should still PASS** ✅

- [ ] T020 [US1] Run linting and formatting in day-01/
  - `uv run ruff check day-01/solution.py`
  - `uv run ruff format day-01/solution.py`
  - Fix any issues raised
  - **Run tests - all should still PASS** ✅

- [ ] T021 [US1] Test with actual puzzle input
  - Run: `uv run day-01/solution.py`
  - Verify output looks reasonable (integer result)
  - Don't submit yet - wait for User Story 2 (error handling)

**Checkpoint**: ✅ User Story 1 complete, fully functional and testable independently

---

## Phase 4: User Story 2 - Handle Invalid Input (Priority: P2)

**Goal**: Add robust error handling for malformed input

**Independent Test**: Provide invalid input, verify clear error message is returned

### RED Phase - Write Failing Tests First ⚠️

- [ ] T022 [P] [US2] Write test_parse_input_invalid_direction in day-01/test_solution.py
  - Test with invalid direction (e.g., "X10")
  - Verify raises ValueError with message about invalid direction
  - **Run and verify it FAILS** ❌

- [ ] T023 [P] [US2] Write test_parse_input_invalid_distance in day-01/test_solution.py
  - Test with non-numeric distance (e.g., "L10A")
  - Verify raises ValueError with message about invalid distance
  - **Run and verify it FAILS** ❌

- [ ] T024 [P] [US2] Write test_parse_input_empty_line_handling in day-01/test_solution.py
  - Test with mixed empty and valid lines
  - Verify empty lines are skipped, valid lines parsed
  - **Run and verify it FAILS** ❌

- [ ] T025 [P] [US2] Write test_apply_rotation_invalid_direction in day-01/test_solution.py
  - Test with invalid direction (e.g., 'X')
  - Verify raises ValueError
  - **Run and verify it FAILS** ❌

**Checkpoint**: ✅ All error handling tests written and FAILING (RED phase complete)

### GREEN Phase - Implement Error Handling

- [ ] T026 [US2] Add input validation to parse_input() in day-01/solution.py
  - Check direction in ('L', 'R'), raise ValueError if not
  - Wrap int() conversion in try/except, raise ValueError if fails
  - Include line content in error messages
  - **Run tests - T022, T023, T024 should now PASS** ✅

- [ ] T027 [US2] Add validation to apply_rotation() in day-01/solution.py
  - Check direction in ('L', 'R'), raise ValueError if not
  - Include direction value in error message
  - **Run tests - T025 should now PASS** ✅

- [ ] T028 [US2] Verify all User Story 2 tests pass
  - Run: `uv run pytest day-01/test_solution.py -v`
  - All new tests (T022-T025) should be GREEN ✅
  - All User Story 1 tests should still be GREEN ✅

**Checkpoint**: ✅ User Story 2 complete - error handling works independently

### REFACTOR Phase - Clean Up Error Handling

- [ ] T029 [US2] Improve error messages in day-01/solution.py
  - Make messages descriptive and user-friendly
  - Include context (what was expected, what was received)
  - **Run tests - all should still PASS** ✅

- [ ] T030 [US2] Run linting and verify code quality
  - `uv run ruff check day-01/`
  - Fix any new issues
  - **Run tests - all should still PASS** ✅

**Checkpoint**: ✅ User Stories 1 AND 2 both work independently

---

## Phase 5: User Story 3 - Large Input Performance (Priority: P3)

**Goal**: Verify solution handles large inputs efficiently (10,000+ rotations)

**Independent Test**: Generate 10,000 rotations, verify completes in under 2 seconds

### RED Phase - Write Failing Tests First ⚠️

- [ ] T031 [US3] Write test_solve_part1_large_input in day-01/test_solution.py
  - Generate 10,000 valid rotations
  - Time the execution
  - Verify completes in under 2 seconds
  - Verify returns correct count
  - **Run and verify it FAILS or is slow** ❌

**Checkpoint**: ✅ Performance test written and FAILING (RED phase complete)

### GREEN Phase - Verify Performance (Likely Already Passing)

- [ ] T032 [US3] Run performance test
  - `uv run pytest day-01/test_solution.py::test_solve_part1_large_input -v`
  - Likely already passes due to O(n) implementation
  - If fails, profile and optimize
  - **Run tests - T031 should PASS** ✅

**Checkpoint**: ✅ User Story 3 complete - performance validated

### REFACTOR Phase - Document Performance

- [ ] T033 [US3] Add performance notes to docstrings in day-01/solution.py
  - Document O(n) complexity
  - Note modulo operations are O(1)
  - **Run tests - all should still PASS** ✅

**Checkpoint**: ✅ All user stories complete and independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements affecting the complete solution

- [ ] T034 Run complete test suite
  - `uv run pytest day-01/test_solution.py -v`
  - Verify all tests pass (should be 13+ tests total)
  - Check coverage if desired: `uv run pytest day-01/test_solution.py --cov=day-01`

- [ ] T035 Final code review of day-01/solution.py
  - All functions have type hints ✅
  - All functions have docstrings ✅
  - Code is PEP 8 compliant ✅
  - No TODO comments remaining ✅

- [ ] T036 Verify solution with test input
  - `uv run day-01/solution.py` (should use input.txt)
  - Manually check against test_input.txt
  - Verify sample returns 3

- [ ] T037 Run solution against actual input
  - `uv run day-01/solution.py`
  - Get Part 1 answer
  - **Ready for manual submission** 🎯

- [ ] T038 [P] Create day-01/README.md (optional)
  - Document puzzle approach
  - Note circular arithmetic solution
  - Include performance notes

- [ ] T039 [P] Run quickstart.md validation
  - Follow steps in specs/004-day-01-part-1/quickstart.md
  - Verify all commands work
  - Update if anything has changed

- [ ] T040 Update main README.md progress tracker
  - Mark Day 1 Part 1 as complete ✅
  - Add stars earned: ⭐
  - Note completion date

- [ ] T041 Commit and push
  - `git add day-01/`
  - `git commit -m "feat: solve day 01 part 1"`
  - `git push origin 004-day-01-part-1`

- [ ] T042 Submit answer to Advent of Code (MANUAL)
  - Go to https://adventofcode.com/2025/day/1
  - Submit Part 1 answer manually
  - Wait for Part 2 to unlock ⏳

**Checkpoint**: ✅ Day 1 Part 1 complete and submitted!

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: ✅ Already complete - meta runner scaffolded everything
- **Foundational (Phase 2)**: ✅ N/A - no shared infrastructure needed
- **User Story 1 (Phase 3)**: Can start immediately - core functionality
- **User Story 2 (Phase 4)**: Can start after US1 complete - adds error handling
- **User Story 3 (Phase 5)**: Can start after US1 complete - validates performance
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Independent - can start immediately ✅
- **User Story 2 (P2)**: Enhances US1 - adds error handling to existing functions
- **User Story 3 (P3)**: Validates US1 - tests performance of existing implementation

### TDD Workflow (Within Each User Story)

**CRITICAL ORDER**:
1. **RED**: Write all tests FIRST (T006-T013 for US1)
2. **Verify FAIL**: Run tests and confirm they fail ❌
3. **GREEN**: Implement code to make tests pass (T014-T017 for US1)
4. **Verify PASS**: Run tests and confirm they pass ✅
5. **REFACTOR**: Clean up code while keeping tests green (T018-T021 for US1)

**Never skip the RED phase** - if a test passes before implementation, it's not testing the right thing!

### Parallel Opportunities

**Within RED Phase**:
- All test-writing tasks marked [P] can be written in parallel
- T006, T007, T008, T009, T010, T012, T013 (US1 tests)
- T022, T023, T024, T025 (US2 tests)

**Within REFACTOR Phase**:
- T018 (type hints) and T019 (docstrings) can be done in parallel if desired
- T034 and T038, T039 (documentation) can be done in parallel

**Across User Stories** (if multiple developers):
- Once US1 is complete, US2 and US3 can proceed in parallel
- US2 enhances error handling
- US3 validates performance
- Both are independent enhancements to US1

---

## Parallel Example: User Story 1 RED Phase

```bash
# All these tests can be written simultaneously (different test functions):
Task T006: "Write test_parse_input_sample in day-01/test_solution.py"
Task T007: "Write test_parse_input_empty in day-01/test_solution.py"
Task T008: "Write test_apply_rotation_left in day-01/test_solution.py"
Task T009: "Write test_apply_rotation_right in day-01/test_solution.py"
Task T010: "Write test_apply_rotation_zero_distance in day-01/test_solution.py"
Task T012: "Write test_solve_part1_empty in day-01/test_solution.py"
Task T013: "Write test_solve_part1_no_zeros in day-01/test_solution.py"

# Then run once to verify all fail:
uv run pytest day-01/test_solution.py -v  # All should be RED ❌
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

**Recommended for AoC speed**:
1. ✅ Complete Phase 1: Setup (already done)
2. Complete Phase 3: User Story 1 (core functionality)
   - RED: Write tests (T006-T013)
   - GREEN: Implement (T014-T017)
   - REFACTOR: Clean up (T018-T021)
3. **STOP and VALIDATE**: Run solution, get answer, submit
4. Then add US2 and US3 if time permits (good practice but not required for submission)

### Complete Implementation (All Stories)

**Recommended for practice and robustness**:
1. ✅ Complete Phase 1: Setup (already done)
2. Complete Phase 3: User Story 1 (TDD: RED → GREEN → REFACTOR)
3. Complete Phase 4: User Story 2 (error handling)
4. Complete Phase 5: User Story 3 (performance validation)
5. Complete Phase 6: Polish and submit

### Time Estimates (With TDD)

- **User Story 1** (core): 30-45 minutes
  - RED: 10 minutes (write 8 tests)
  - GREEN: 15-20 minutes (implement 3 functions)
  - REFACTOR: 5-10 minutes (type hints, docstrings, formatting)
- **User Story 2** (error handling): 15-20 minutes
  - RED: 5 minutes (write 4 tests)
  - GREEN: 10 minutes (add validation)
  - REFACTOR: 5 minutes (improve messages)
- **User Story 3** (performance): 10 minutes
  - RED: 5 minutes (write 1 test)
  - GREEN: 2 minutes (verify already fast)
  - REFACTOR: 3 minutes (document)
- **Polish**: 10-15 minutes

**Total**: 65-90 minutes for complete implementation with full TDD

**MVP to submission**: 30-45 minutes (just US1)

---

## Notes

- ✅ All tasks follow TDD strictly (Constitution Principle IV - NON-NEGOTIABLE)
- ✅ Each user story is independently testable (can stop after any story)
- ✅ Tests written first, verified to fail, then implementation
- ✅ File paths are explicit (day-01/solution.py, day-01/test_solution.py)
- ✅ [P] markers indicate parallelizable tasks
- ✅ [Story] markers (US1, US2, US3) trace tasks to requirements
- ⚠️ Part 2 not included - will be revealed after Part 1 submission
- ⚠️ Remember: MANUAL submission only (Constitution Principle VI)

---

## Quick Reference Commands

```bash
# Run all tests
uv run pytest day-01/test_solution.py -v

# Run specific test
uv run pytest day-01/test_solution.py::test_solve_part1_sample -v

# Run solution
uv run day-01/solution.py

# Lint and format
uv run ruff check day-01/
uv run ruff format day-01/

# Run with coverage
uv run pytest day-01/test_solution.py --cov=day-01 --cov-report=term-missing
```

**Ready to start?** Begin with Task T006 - write your first failing test! 🚀
