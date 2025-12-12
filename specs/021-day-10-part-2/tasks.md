# Tasks: Day 10 Part 2 - Joltage Configuration Optimization

**Input**: Design documents from `/specs/021-day-10-part-2/`  
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅, quickstart.md ✅

**TDD Workflow**: RED → GREEN → REFACTOR (strict enforcement per Constitution Principle IV)

**Organization**: Tasks organized by user story for independent implementation and testing

---

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: User story label (US1, US2, US3, US4, US5) - only for story-specific tasks
- Include exact file paths in descriptions

---

## Phase 1: Setup (Project Infrastructure)

**Purpose**: Verify existing infrastructure is ready for Part 2 implementation

- [ ] T001 Verify Day 10 folder structure exists with `solution.py`, `input.txt`, `test_input.txt`
- [ ] T002 Verify NumPy is available in environment (run `uv run python -c "import numpy; print(numpy.__version__)"`)
- [ ] T003 Verify pytest is available (run `uv run pytest --version`)

**Checkpoint**: Infrastructure ready - proceed to TDD implementation

---

## Phase 2: Foundational (Core Utilities)

**Purpose**: Shared parsing utilities - MUST complete before user story work begins

**⚠️ CRITICAL**: These foundational components are blocking prerequisites for all user stories

- [ ] T004 Verify `parse_input()` and `parse_line()` functions work correctly in `day-10/solution.py`
- [ ] T005 Verify test input contains joltage targets in curly braces format `{3,5,4,7}`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 4 - Input Parser Extracts Machine Definitions (Priority: P1) 🎯

**Goal**: Ensure parsing correctly extracts button definitions and joltage requirements from input format

**Independent Test**: Parse test_input.txt lines and verify button lists and targets match expected values

**Why this comes first**: Without correct parsing, all subsequent calculations will fail. This is the data ingestion layer.

### RED: Write Failing Tests for Parsing (User Story 4)

- [ ] T006 [US4] Create `day-10/test_solution_part2.py` with test for parsing first example line
- [ ] T007 [US4] Add test to verify `parse_line()` extracts buttons `[[3], [1,3], [2], [2,3], [0,2], [0,1]]` and targets `[3,5,4,7]`
- [ ] T008 [US4] Add test for second example line with buttons and targets `{7,5,12,7,2}`
- [ ] T009 [US4] Add test for third example line with 4 buttons and 6 targets
- [ ] T010 [US4] Run tests with `uv run pytest day-10/test_solution_part2.py::test_parse -v` - verify they PASS (parsing already works from Part 1)

**Checkpoint**: Parsing validation complete - existing Part 1 parser handles joltage targets correctly

---

## Phase 4: User Story 3 - Algorithm Developer Optimizes Button Press Strategy (Priority: P1) 🎯 MVP Core

**Goal**: Implement core integer linear programming solver that finds minimum button presses

**Independent Test**: Given button matrix B and target vector t, return solution x that minimizes sum(x) with B·x = t and x ≥ 0

**Why P1**: This is the algorithmic heart of Part 2 - all other stories depend on this working correctly

### RED: Write Failing Tests for Core Algorithm (User Story 3)

- [ ] T011 [P] [US3] Add test `test_build_button_matrix_structure()` in `day-10/test_solution_part2.py` verifying matrix construction
- [ ] T012 [P] [US3] Add test `test_verify_solution_accepts_valid()` checking solution validation with simple 2x2 case
- [ ] T013 [P] [US3] Add test `test_verify_solution_rejects_invalid()` ensuring invalid solutions are rejected
- [ ] T014 [US3] Run tests with `uv run pytest day-10/test_solution_part2.py -k verify -v` - verify they FAIL with ImportError

### GREEN: Implement Core Algorithm (User Story 3)

- [ ] T015 [US3] Create `day-10/solution_part2.py` with imports (NumPy, fractions, solution.py)
- [ ] T016 [P] [US3] Implement `build_button_matrix(buttons, num_counters)` function returning NumPy array
- [ ] T017 [P] [US3] Implement `verify_solution(B, t, x)` function checking B·x = t and x ≥ 0
- [ ] T018 [US3] Run tests with `uv run pytest day-10/test_solution_part2.py -k "build_button_matrix or verify" -v` - verify they PASS
- [ ] T019 [US3] Implement `gaussian_elimination_integer(B, t)` using Fraction for exact arithmetic, return (aug_matrix, pivot_cols, free_cols)
- [ ] T020 [US3] Implement `solve_integer_linear_system(B, t)` with free variable enumeration and back-substitution
- [ ] T021 [US3] Add bounds calculation in `solve_integer_linear_system()` using `min(sum(t), 20)` cap

### REFACTOR: Optimize Algorithm Performance (User Story 3)

- [ ] T022 [US3] Add performance monitoring (timing) to `solve_integer_linear_system()` with verbose flag
- [ ] T023 [US3] Add docstrings to all functions with type hints and complexity notes

**Checkpoint**: Core solver algorithm complete and validated with basic tests

---

## Phase 5: User Story 1 - Factory Technician Configures Single Machine (Priority: P1) 🎯 MVP Validation

**Goal**: Solve individual machine examples and verify against known expected results (10, 12, 11 presses)

**Independent Test**: Each example machine returns exact expected minimum press count

**Why P1**: This validates the algorithm works correctly on known test cases before running on full input

### RED: Write Failing Tests for Example Machines (User Story 1)

- [ ] T024 [P] [US1] Add `test_example_1_machine()` in `day-10/test_solution_part2.py` expecting 10 presses
- [ ] T025 [P] [US1] Add `test_example_2_machine()` expecting 12 presses
- [ ] T026 [P] [US1] Add `test_example_3_machine()` expecting 11 presses
- [ ] T027 [P] [US1] Add `test_zero_target_case()` for edge case with all targets = 0
- [ ] T028 [US1] Run tests with `uv run pytest day-10/test_solution_part2.py -k example -v` - verify they FAIL

### GREEN: Make Example Tests Pass (User Story 1)

- [ ] T029 [US1] Debug and fix `solve_integer_linear_system()` if example 1 fails (expected: 10 presses)
- [ ] T030 [US1] Debug and fix enumeration bounds if example 2 fails (expected: 12 presses)
- [ ] T031 [US1] Debug and fix back-substitution logic if example 3 fails (expected: 11 presses)
- [ ] T032 [US1] Run tests with `uv run pytest day-10/test_solution_part2.py -k example -v` - verify ALL PASS

**Checkpoint**: Algorithm correctly solves all three example machines independently

---

## Phase 6: User Story 2 - Factory Manager Processes Multiple Machines (Priority: P1) 🎯 MVP Aggregation

**Goal**: Process complete input file with multiple machines and aggregate total minimum presses

**Independent Test**: Parse test_input.txt with 3 machines and verify total = 33 (10 + 12 + 11)

**Why P1**: Essential for solving the actual puzzle - ties together parsing and solving across all machines

### RED: Write Failing Tests for Aggregation (User Story 2)

- [ ] T033 [US2] Add `test_all_examples_aggregate()` in `day-10/test_solution_part2.py` expecting total = 33
- [ ] T034 [US2] Run test with `uv run pytest day-10/test_solution_part2.py -k aggregate -v` - verify it FAILS

### GREEN: Implement Aggregation (User Story 2)

- [ ] T035 [US2] Implement `solve_part2(machines)` function in `day-10/solution_part2.py` that iterates over machines
- [ ] T036 [US2] Add button matrix construction from `machine['buttons']` and targets from `machine['jolts']`
- [ ] T037 [US2] Add error handling for infeasible systems (log warning, continue)
- [ ] T038 [US2] Add summation of total presses across all machines
- [ ] T039 [US2] Add `main()` function that reads `input.txt` and prints result
- [ ] T040 [US2] Run test with `uv run pytest day-10/test_solution_part2.py -k aggregate -v` - verify it PASSES

**Checkpoint**: Full pipeline works - parse → solve → aggregate across all machines

---

## Phase 7: User Story 5 - Test Validation Against Examples (Priority: P2)

**Goal**: Comprehensive test suite confirms solution works on all provided examples

**Independent Test**: All tests pass, total coverage of examples achieved

**Why P2**: Quality assurance before running on actual puzzle input

### GREEN: Final Validation (User Story 5)

- [ ] T041 [US5] Run full test suite with `uv run pytest day-10/test_solution_part2.py -v` - verify ALL PASS
- [ ] T042 [US5] Run test with coverage: `uv run pytest day-10/test_solution_part2.py --cov=solution_part2 -v`
- [ ] T043 [US5] Verify test output confirms: example 1 = 10, example 2 = 12, example 3 = 11, total = 33

**Checkpoint**: All tests green - solution ready for actual puzzle input

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements and documentation before submission

- [ ] T044 [P] Add module docstring to `day-10/solution_part2.py` explaining integer LP approach
- [x] T045 [P] Add inline comments explaining Gaussian elimination steps in `gaussian_elimination_integer()`
- [x] T046 Run linting with `uv run ruff check day-10/solution_part2.py` and fix any issues
- [x] T047 Run formatting with `uv run ruff format day-10/solution_part2.py`
- [x] T048 Run actual puzzle: `uv run python day-10/solution_part2.py` and capture result (Answer: 20298)
- [ ] T049 Manually submit Part 2 answer to Advent of Code website
- [x] T050 Update `README.md` progress tracker with Day 10 Part 2 completion ⭐

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup) → Phase 2 (Foundational) → Phase 3 (US4 Parsing)
                                         → Phase 4 (US3 Algorithm)
                                         → Phase 5 (US1 Examples)
                                         → Phase 6 (US2 Aggregation)
                                         → Phase 7 (US5 Validation)
                                         → Phase 8 (Polish)
```

### User Story Dependencies

- **US4 (Parsing)**: Independent, validates existing Part 1 parser works for Part 2
- **US3 (Algorithm)**: Core solver, no dependencies on other stories
- **US1 (Examples)**: Depends on US3 (needs solver to test examples)
- **US2 (Aggregation)**: Depends on US3 (needs solver) and US4 (needs parsing)
- **US5 (Validation)**: Depends on all previous stories being complete

### TDD Within Each User Story

1. **RED**: Write tests FIRST for the story
2. **Verify tests FAIL**: Run tests and confirm ImportError or assertion failures
3. **GREEN**: Implement minimum code to make tests pass
4. **Verify tests PASS**: Run tests and confirm all green
5. **REFACTOR**: Clean up code while keeping tests green

### Critical Path (MVP)

```
T001-T005 (Setup + Foundational)
  ↓
T006-T010 (US4: Validate parsing)
  ↓
T011-T023 (US3: Core algorithm - RED/GREEN/REFACTOR)
  ↓
T024-T032 (US1: Example validation)
  ↓
T033-T040 (US2: Aggregation)
  ↓
T041-T043 (US5: Final validation)
  ↓
T044-T050 (Polish & submission)
```

### Parallel Opportunities

**Within US3 (Algorithm):**

- T011, T012, T013 (all test writing) can run in parallel
- T016, T017 (build_button_matrix and verify_solution) can run in parallel

**Within US1 (Examples):**

- T024, T025, T026, T027 (all test writing) can run in parallel

**Within Phase 8 (Polish):**

- T044, T045 (documentation) can run in parallel with T046, T047 (linting)

---

## Parallel Example: User Story 3 (Algorithm Core)

```bash
# Launch RED phase tests together:
Task T011: "Add test test_build_button_matrix_structure"
Task T012: "Add test test_verify_solution_accepts_valid"
Task T013: "Add test test_verify_solution_rejects_invalid"

# After RED, launch GREEN phase implementations in parallel:
Task T016: "Implement build_button_matrix() in solution_part2.py"
Task T017: "Implement verify_solution() in solution_part2.py"
```

---

## Implementation Strategy

### MVP First (Critical User Stories Only)

1. ✅ Complete Phase 1: Setup (T001-T003)
2. ✅ Complete Phase 2: Foundational (T004-T005)
3. 🎯 Complete Phase 3: US4 Parsing validation (T006-T010)
4. 🎯 Complete Phase 4: US3 Algorithm core (T011-T023) ← **MOST CRITICAL**
5. 🎯 Complete Phase 5: US1 Example validation (T024-T032)
6. 🎯 Complete Phase 6: US2 Aggregation (T033-T040)
7. **STOP and VALIDATE**: Run full test suite - all must be green
8. Polish and submit (T044-T050)

### TDD Discipline Checkpoints

- **After T010**: Parsing tests pass (existing functionality verified)
- **After T014**: Algorithm tests fail (RED confirmed)
- **After T023**: Algorithm tests pass (GREEN achieved)
- **After T028**: Example tests fail (RED confirmed)
- **After T032**: Example tests pass (GREEN achieved)
- **After T034**: Aggregate test fails (RED confirmed)
- **After T040**: Aggregate test passes (GREEN achieved)
- **After T043**: ALL tests green (full validation)

---

## Execution Commands

### Test Commands (TDD workflow)

```bash
# Run all Part 2 tests
uv run pytest day-10/test_solution_part2.py -v

# Run specific test patterns
uv run pytest day-10/test_solution_part2.py -k "example" -v
uv run pytest day-10/test_solution_part2.py -k "verify" -v
uv run pytest day-10/test_solution_part2.py -k "aggregate" -v

# Run with coverage
uv run pytest day-10/test_solution_part2.py --cov=solution_part2 --cov-report=term-missing -v

# Run single test
uv run pytest day-10/test_solution_part2.py::test_example_1_machine -v
```

### Linting Commands

```bash
# Check for issues
uv run ruff check day-10/solution_part2.py

# Auto-fix issues
uv run ruff check --fix day-10/solution_part2.py

# Format code
uv run ruff format day-10/solution_part2.py
```

### Execution Commands

```bash
# Run Part 2 solution
uv run python day-10/solution_part2.py

# Run with verbose output (if implemented)
uv run python day-10/solution_part2.py --verbose
```

---

## Notes

- **TDD is NON-NEGOTIABLE**: Tests must be written first and verified to fail before implementation
- **[P] tasks**: Different files, can run in parallel if team capacity allows
- **[Story] labels**: Map tasks to user stories from spec.md for traceability
- **File paths**: All tasks include exact paths to ensure clarity
- **UV runtime**: All Python commands use `uv run` per Constitution requirement
- **Checkpoints**: Each phase ends with validation before proceeding
- **RED-GREEN-REFACTOR**: Explicitly enforced in task organization (RED tasks before GREEN tasks)

---

## Expected Timeline

- **Setup + Foundational**: 5 minutes (verification only)
- **US4 Parsing**: 10 minutes (validation tests)
- **US3 Algorithm**: 60-90 minutes (core solver implementation)
- **US1 Examples**: 30 minutes (example validation and debugging)
- **US2 Aggregation**: 20 minutes (simple aggregation logic)
- **US5 Validation**: 10 minutes (run full test suite)
- **Polish**: 20 minutes (documentation and cleanup)

**Total Estimated Time**: 2.5-3 hours

---

## Success Criteria

✅ All tests pass: `uv run pytest day-10/test_solution_part2.py -v`  
✅ Example results match: 10, 12, 11 → total 33  
✅ Actual puzzle answer accepted by AoC  
✅ Code follows PEP8 via Ruff  
✅ TDD workflow documented (tests committed before implementation)  
✅ README.md updated with Day 10 Part 2 ⭐
