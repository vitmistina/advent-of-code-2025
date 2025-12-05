# Tasks: Day 5 Part 2 - Fresh Ingredient ID Range Coverage

## Feature: Day 5 Part 2 - Fresh Ingredient ID Range Coverage

---

## Phase 1: Setup

- [X] T001 Create day-05/solution.py if missing
- [X] T002 Create day-05/test_solution.py if missing
- [X] T003 Create/verify input.txt and test_input.txt in day-05/

## Phase 2: Foundational

- [X] T004 [P] Add FreshRange dataclass to day-05/solution.py
- [X] T005 [P] Add merge_ranges() function to day-05/solution.py (reuse from Part 1)

## Phase 3: [US1] Calculate Total Fresh Ingredients from Ranges (P1)

- [X] T006 [P] [US1] Implement parse_ranges_part2() to extract only ranges from input in day-05/solution.py
- [X] T007 [P] [US1] Implement solve_part2(data: str) in day-05/solution.py (sum merged range lengths)
- [X] T008 [P] [US1] Add tests for solve_part2() in day-05/test_solution.py (cover all acceptance scenarios)

## Phase 4: [US2] Parse Fresh Ranges and Ignore Available IDs Section (P1)

- [X] T009 [P] [US2] Add test to verify available IDs section is ignored in day-05/test_solution.py

## Phase 5: [US3] Handle Edge Cases in Range Coverage (P2)

- [X] T010 [P] [US3] Add tests for large, adjacent, duplicate, and empty ranges in day-05/test_solution.py

## Final Phase: Polish & Cross-Cutting

- [X] T011 Add/verify docstrings and comments in day-05/solution.py
- [X] T012 Run ruff and ensure PEP8 compliance in day-05/solution.py and day-05/test_solution.py
- [X] T013 Update day-05/README.md with usage for part 2

## Dependencies

- US1 and US2 can be implemented/tested in parallel after foundational phase
- US3 (edge cases) can be tested in parallel with US1/US2

## Parallel Execution Examples

- T004, T005 can be done in parallel
- T006, T007, T008, T009 can be done in parallel after foundational
- T010 can be done in parallel with T008/T009

## Implementation Strategy

- MVP: Complete Phase 3 (US1) and Phase 4 (US2) for basic correctness
- Incrementally add edge case tests (US3) and polish

---

All tasks follow checklist format and are independently testable.
