# Tasks: Day 6 Part 2 - Cephalopod Math (Right-to-Left Columns)

## Feature: Day 6 Part 2 - Cephalopod Math (Right-to-Left Columns)

### Phase 1: Setup

- [X] T001 Create solution_part2.py in day-06/ for Part 2 implementation
- [X] T002 [P] Create test_solution_part2.py in day-06/ for Part 2 tests

### Phase 2: Foundational

- [X] T003 Implement columnar parsing utility in day-06/parser.py (right-to-left columns)
- [X] T004 [P] Implement grouping logic for problems (space columns as separators) in day-06/parser.py
- [X] T005 [P] Implement number extraction from columns (top-to-bottom digits) in day-06/parser.py
- [X] T006 [P] Implement operator extraction from bottom of columns in day-06/parser.py

### Phase 3: [US1] Solve Cephalopod Math Worksheet (Priority: P1)

- [X] T007 [US1] Implement Problem dataclass reuse/adaptation in day-06/solution_part2.py
- [X] T008 [US1] Implement evaluate_problem logic reuse/adaptation in day-06/solution_part2.py
- [X] T009 [US1] Implement solve_worksheet pipeline for Part 2 in day-06/solution_part2.py
- [X] T010 [P] [US1] Implement verbose/debug output for Part 2 in day-06/solution_part2.py
- [X] T011 [P] [US1] Implement error handling for malformed input in day-06/solution_part2.py
- [X] T012 [P] [US1] Add acceptance criteria tests for example worksheet in test_solution_part2.py
- [X] T013 [P] [US1] Add acceptance criteria tests for edge cases in test_solution_part2.py

### Phase 4: [US2] Handle Edge Formatting (Priority: P2)

- [X] T014 [US2] Add tests for variable spacing/alignment in test_solution_part2.py
- [X] T015 [P] [US2] Add tests for missing numbers/operators/columns in test_solution_part2.py

### Final Phase: Polish & Cross-Cutting Concerns

- [X] T016 Refactor shared logic between solution.py and solution_part2.py into day-06/utils.py
- [X] T017 [P] Add docstrings and comments to all new/changed files
- [X] T018 [P] Update README.md in day-06/ with Part 2 instructions and examples

## Dependencies

- Foundational tasks (T003-T006) must be completed before US1 implementation (T007-T013)
- US1 must be completed before US2 (T014-T015)
- Polish tasks (T016-T018) can be done in parallel after main implementation

## Parallel Execution Examples

- T002, T004, T005, T006 can be done in parallel
- T010, T011, T012, T013 can be done in parallel after pipeline is ready
- T015, T017, T018 can be done in parallel after main tests

## Implementation Strategy

- MVP: Complete all US1 tasks (T007-T013) for a working solution and acceptance criteria
- Incremental delivery: Add edge case handling (US2), refactor, and polish
