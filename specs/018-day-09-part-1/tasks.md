# Tasks: AoC Day 9 Part 1 - Largest Red Tile Rectangle

## Phase 1: Setup

- [x] T001 Create `day-09/` folder and initial files (`solution.py`, `test_solution.py`, `input.txt`, `test_input.txt`, `README.md`)
- [x] T002 Initialize Python environment (Python 3.10+, uv, ruff, pytest) in project root
- [x] T003 Add progress tracker entry to main `README.md` for Day 9

## Phase 2: Foundational

- [x] T004 Implement input validation utility in `day-09/solution.py`
- [x] T005 [P] Add pytest configuration to `day-09/test_solution.py`
- [x] T006 [P] Add ruff linting config to project root

## Phase 3: [US1] Parse Red Tile Coordinates (P1)

- [x] T007 [US1] Implement function to parse red tile coordinates from `input.txt` in `day-09/solution.py`
- [x] T008 [P] [US1] Add tests for coordinate parsing in `day-09/test_solution.py`
- [x] T009 [US1] Integrate error handling for malformed/empty input in `day-09/solution.py`
- [x] T010 [P] [US1] Document parsing logic in `day-09/README.md`

## Phase 4: [US2] Calculate Rectangle Area (P1)

- [x] T011 [US2] Implement rectangle area calculation function in `day-09/solution.py`
- [x] T012 [P] [US2] Add tests for rectangle area calculation in `day-09/test_solution.py`
- [x] T013 [US2] Ensure calculation works for any order of corners in `day-09/solution.py`
- [x] T014 [P] [US2] Document area calculation logic in `day-09/README.md`

## Phase 5: [US3] Find Largest Rectangle (P1)

- [x] T015 [US3] Implement logic to find largest rectangle from all pairs in `day-09/solution.py`
- [x] T016 [P] [US3] Add tests for largest rectangle logic in `day-09/test_solution.py`
- [x] T017 [US3] Integrate edge case handling (fewer than 2 tiles, multiple max rectangles) in `day-09/solution.py`
- [x] T018 [P] [US3] Document largest rectangle logic in `day-09/README.md`

## Final Phase: Polish & Cross-Cutting

- [x] T019 Run ruff and pytest for final lint/test in `day-09/`
- [x] T020 Update all docstrings and comments in `day-09/solution.py`
- [x] T021 Finalize `day-09/README.md` with usage and test instructions

---

### Dependencies

- US1 → US2 → US3 (must parse before calculate, must calculate before find largest)
- Setup and Foundational tasks must be completed before user stories

### Parallel Execution Examples

- T005, T006 (pytest and ruff config) can run in parallel
- T008, T010 (parsing tests and docs) can run in parallel after parsing logic
- T012, T014 (area tests and docs) can run in parallel after area logic
- T016, T018 (largest rectangle tests and docs) can run in parallel after main logic

### Task Count

- Total: 21 tasks
- US1: 4 tasks
- US2: 4 tasks
- US3: 4 tasks
- Parallel opportunities: 8 tasks

### Independent Test Criteria

- US1: Parsing tested by loading input and verifying tuples
- US2: Area calculation tested by providing pairs and checking results
- US3: Largest rectangle logic tested by running on example input and verifying output

### Suggested MVP Scope

- Complete all US1 tasks (T007–T010) for a minimal, testable increment

### Format Validation

- All tasks follow strict checklist format: checkbox, sequential ID, [P] for parallel, [USx] for story, file path included
