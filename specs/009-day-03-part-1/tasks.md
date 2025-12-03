# Tasks: Day 3 Part 1 - Battery Bank Joltage Calculator

**Input**: Design documents from `/specs/009-day-03-part-1/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: This feature follows TDD (Test-Driven Development) as mandated by Constitution Principle IV. All test tasks use RED-GREEN-REFACTOR cycle.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for Day 3

- [ ] T001 Verify day-03/ folder structure exists with input.txt and test_input.txt
- [ ] T002 Verify Python environment configured (Python 3.10+, pytest installed)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before user story implementation

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T003 Create day-03/solution.py with module docstring and imports
- [ ] T004 Create day-03/test_solution.py with module docstring and imports

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Calculate Maximum Joltage from Battery Banks (Priority: P1) 🎯 MVP

**Goal**: Determine total power output from battery banks by calculating maximum joltage per bank and summing them

**Independent Test**: Provide battery bank data (lines of digits) and verify calculated total output joltage matches expected results (example: 4 banks → 357 total joltage)

### RED Phase: Write Failing Tests (User Story 1)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T005 [P] [US1] Write test_max_joltage() in day-03/test_solution.py with 4 core examples (987654321111111→98, 811111111111119→89, 234234234234278→78, 818181911112111→92)
- [x] T006 [P] [US1] Write test_max_joltage_edge_cases() in day-03/test_solution.py with edge cases (two-digit bank, all same digits, ascending, descending)
- [x] T007 [P] [US1] Write test_parse_input() in day-03/test_solution.py to verify multi-line parsing and whitespace handling
- [x] T008 [P] [US1] Write test_parse_input_empty() in day-03/test_solution.py to verify empty input handling
- [x] T009 [P] [US1] Write test_solve_part1() in day-03/test_solution.py with full example (4 banks → 357)
- [x] T010 [US1] Run pytest to verify all tests FAIL (RED phase complete) using: uv run pytest day-03/test_solution.py -v

### GREEN Phase: Implement Minimum Code (User Story 1)

- [x] T011 [P] [US1] Implement parse_input() function in day-03/solution.py to split input by newlines and strip whitespace
- [x] T012 [P] [US1] Implement max_joltage() function in day-03/solution.py using greedy algorithm (find max in bank[:-1], then max after that position)
- [x] T013 [US1] Implement solve_part1() function in day-03/solution.py to sum max_joltage() for all banks
- [x] T014 [US1] Implement main() function in day-03/solution.py to read input.txt and print result
- [x] T015 [US1] Run pytest to verify all tests PASS (GREEN phase complete) using: uv run pytest day-03/test_solution.py -v

### REFACTOR Phase: Optimize and Clean (User Story 1)

- [x] T016 [US1] Add comprehensive docstrings to all functions in day-03/solution.py (parse_input, max_joltage, solve_part1, main)
- [x] T017 [US1] Add type hints to all function signatures in day-03/solution.py
- [x] T018 [US1] Run ruff format and ruff check on day-03/ using: uv run ruff format day-03/ && uv run ruff check day-03/
- [x] T019 [US1] Verify tests still pass after refactoring using: uv run pytest day-03/test_solution.py -v

### Validation (User Story 1)

- [x] T020 [US1] Test solution with test_input.txt to verify output is 357 using: cd day-03 && uv run solution.py

- [x] T021 [US1] Run solution with actual input.txt to get puzzle answer using: cd day-03 && uv run solution.py

**Checkpoint**: User Story 1 complete - All tests passing, solution produces correct answer for test input (357)

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements and documentation

- [ ] T022 Update README.md in repository root with Day 3 Part 1 completion status
- [ ] T023 Verify all Constitution principles satisfied (clean code, TDD cycle followed, documentation complete)
- [ ] T024 Run quickstart.md validation checklist to ensure all steps completed

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS user story
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion
  - **RED Phase**: Must complete before GREEN phase (tests must fail first)
  - **GREEN Phase**: Must complete before REFACTOR phase (tests must pass)
  - **REFACTOR Phase**: Must maintain passing tests
- **Polish (Phase 4)**: Depends on User Story 1 completion

### Within User Story 1

**RED Phase (T005-T010)**:

- T005, T006, T007, T008, T009 are [P] - can write all tests in parallel
- T010 must wait for all tests to be written (verify they FAIL)

**GREEN Phase (T011-T015)**:

- T011 and T012 are [P] - can implement parse_input() and max_joltage() in parallel
- T013 depends on T011 (parse_input must exist)
- T014 depends on T013 (solve_part1 must exist)
- T015 must wait for T011-T014 (verify they PASS)

**REFACTOR Phase (T016-T019)**:

- T016 and T017 can be done together
- T018 depends on T016-T017 (code must be complete before linting)
- T019 depends on T018 (verify tests still pass after cleanup)

**Validation (T020-T021)**:

- T020 must happen before T021 (verify test input works first)

### Parallel Opportunities

```bash
# RED Phase - Write all tests in parallel:
T005: "Write test_max_joltage() in day-03/test_solution.py"
T006: "Write test_max_joltage_edge_cases() in day-03/test_solution.py"
T007: "Write test_parse_input() in day-03/test_solution.py"
T008: "Write test_parse_input_empty() in day-03/test_solution.py"
T009: "Write test_solve_part1() in day-03/test_solution.py"

# GREEN Phase - Implement independent functions in parallel:
T011: "Implement parse_input() in day-03/solution.py"
T012: "Implement max_joltage() in day-03/solution.py"
```

---

## Implementation Strategy

### TDD Workflow (RED-GREEN-REFACTOR)

1. **Complete Phase 1 (Setup)**: Verify environment (T001-T002)
2. **Complete Phase 2 (Foundational)**: Create empty files (T003-T004)
3. **RED Phase**: Write ALL tests first, ensure they FAIL (T005-T010)
4. **GREEN Phase**: Implement minimal code to pass tests (T011-T015)
5. **REFACTOR Phase**: Clean up code while keeping tests green (T016-T019)
6. **Validation**: Verify with test and actual inputs (T020-T021)
7. **Polish**: Update documentation (T022-T024)

### Time Estimates

| Phase          | Tasks        | Estimated Time  |
| -------------- | ------------ | --------------- |
| Setup          | T001-T002    | 2 minutes       |
| Foundational   | T003-T004    | 3 minutes       |
| RED Phase      | T005-T010    | 10 minutes      |
| GREEN Phase    | T011-T015    | 15 minutes      |
| REFACTOR Phase | T016-T019    | 5 minutes       |
| Validation     | T020-T021    | 5 minutes       |
| Polish         | T022-T024    | 5 minutes       |
| **Total**      | **24 tasks** | **~45 minutes** |

### MVP Scope

**Minimum Viable Product = User Story 1 Only**

This is a single-story feature (Day 3 Part 1 puzzle). The MVP IS the complete feature:

- Input parsing (parse_input)
- Maximum joltage calculation (max_joltage)
- Total output calculation (solve_part1)
- Executable solution (main)
- Full test coverage

**Success Criteria**:

- ✅ All tests pass (8 test functions)
- ✅ Test input produces 357
- ✅ Actual input produces valid puzzle answer
- ✅ Code follows TDD cycle (RED→GREEN→REFACTOR)
- ✅ All Constitution principles satisfied

---

## Task Summary

**Total Tasks**: 24

- **Setup**: 2 tasks
- **Foundational**: 2 tasks
- **User Story 1**: 17 tasks
  - RED Phase: 6 tasks (5 test files + 1 verification)
  - GREEN Phase: 5 tasks (3 functions + main + verification)
  - REFACTOR Phase: 4 tasks (docs + types + lint + verify)
  - Validation: 2 tasks
- **Polish**: 3 tasks

**Parallel Opportunities Identified**: 9 tasks marked [P]

- 5 test tasks can run in parallel (RED phase)
- 2 implementation tasks can run in parallel (GREEN phase)
- 2 documentation tasks can run together (REFACTOR phase)

**Independent Test Criteria**:

- Test with 4-bank example produces total joltage of 357
- Each bank independently calculates correct maximum joltage
- Edge cases (2-digit, same digits, ascending, descending) handled correctly

**Format Validation**: ✅ All tasks follow checklist format (checkbox, ID, optional [P], required [Story] for US1, description with file path)

---

## Notes

- All tasks follow strict checkbox format: `- [ ] [ID] [P?] [Story?] Description`
- [P] indicates parallelizable tasks (different files or independent work)
- [US1] label indicates task belongs to User Story 1 (only story in this feature)
- TDD cycle enforced: RED (write failing tests) → GREEN (implement) → REFACTOR (clean)
- Each phase has clear success criteria and checkpoint
- Solution uses greedy O(n) algorithm per research.md
- No external dependencies beyond pytest (stdlib only)
- Manual puzzle submission to Advent of Code after validation
