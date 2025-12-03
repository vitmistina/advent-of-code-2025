# Tasks: Day 03 Part 2 - Maximize Joltage with 12 Batteries

## Phase 1: Setup

- [x] T001 Create day-03/solution.py for part 2 implementation
- [x] T002 Create day-03/test_solution.py for part 2 tests
- [x] T003 Create day-03/input.txt and day-03/test_input.txt for puzzle and sample input
- [x] T004 Create day-03/README.md for notes and explanations

## Phase 2: Foundational

- [x] T005 Implement function stub for solve_part2(input_text: str) -> int in day-03/solution.py
- [x] T006 [P] Add docstrings and PEP8 compliance to day-03/solution.py

## Phase 3: User Story 1 (P1) [US1]

- [x] T007 [US1] Implement monotonic stack algorithm to select 12 digits in day-03/solution.py
- [x] T008 [P] [US1] Implement error handling for banks with <12 digits in day-03/solution.py
- [x] T009 [P] [US1] Implement parsing of input and summing logic in day-03/solution.py
- [x] T010 [P] [US1] Add acceptance test cases (examples, edge cases) to day-03/test_solution.py
- [x] T011 [P] [US1] Add test for error/edge case (bank <12 digits) to day-03/test_solution.py
- [x] T012 [P] [US1] Add test for all-identical digits and multiple max selections to day-03/test_solution.py
- [x] T013 [US1] Document independent test criteria and usage in day-03/README.md

## Final Phase: Polish & Cross-Cutting

- [x] T014 [P] Refactor for clarity, ruff/PEP8, add comments in day-03/solution.py
- [x] T015 [P] Update day-03/README.md with final notes and edge case explanations

## Dependencies

- Phase 1 → Phase 2 → Phase 3 (US1) → Final Phase
- Within Phase 3, T007 must be completed before T008–T013 (which are parallelizable)

## Parallel Execution Examples

- T006 can be done in parallel with T005
- T008, T009, T010, T011, T012 can be done in parallel after T007
- T014 and T015 can be done in parallel after all US1 tasks

## Implementation Strategy

- MVP: Complete T001–T013 (core logic, tests, and documentation for US1)
- Deliver incrementally: implement and test monotonic stack, then add error handling and edge case tests
- Each user story phase is independently testable via day-03/test_solution.py

---

**Format validation:** All tasks follow strict checklist format: checkbox, TaskID, [P] if parallel, [US1] for user story, and file paths.
