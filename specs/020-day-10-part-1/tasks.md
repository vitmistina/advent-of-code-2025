# Tasks: AoC Day 10 Part 1 — Factory Machine Initialization

**Input**: Design documents from `specs/020-day-10-part-1/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md

**Tests**: Tests are OPTIONAL; this feature uses TDD per Constitution. Include RED tests for Part 1.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basics

- [ ] T001 Ensure day folder structure is consistent in `day-10/`
- [ ] T002 [P] Add docstring stubs in `day-10/solution.py` for `solve_part1(input_data)`
- [ ] T003 [P] Create parsing helper stub in `day-10/parser.py` (if needed)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core prerequisites before implementing stories

- [ ] T004 [P] Validate `day-10/test_input.txt` contains 3 example lines
- [ ] T005 [P] Validate `day-10/input.txt` is present and non-empty (160 lines)
- [ ] T006 Set up basic pytest config (reuse repo settings) for `day-10/test_solution.py`

Checkpoint: Foundation ready — proceed to user stories.

---

## Phase 3: User Story 1 — Parse Machine Configuration (Priority: P1) 🎯 MVP

**Goal**: Parse indicator diagram, button lists, and joltage (ignored) per line
**Independent Test**: Provide one line; verify parsed components match expected structures

### Tests (RED)

- [ ] T007 [P] [US1] Add unit tests in `day-10/test_solution.py` for parsing the three description examples
- [ ] T008 [P] [US1] Add unit test to validate index bounds and handling of spaces

### Implementation

- [ ] T009 [P] [US1] Implement `parse_line(line: str) -> (target:list[int], buttons:list[list[int]], jolts:list[int])` in `day-10/parser.py`
- [ ] T010 [US1] Implement `parse_input(text: str)` to return list of machines in `day-10/parser.py`
- [ ] T011 [US1] Wire parsing into `day-10/solution.py` for Part 1 flow

Checkpoint: Parsing works independently.

---

## Phase 4: User Story 2 — Model Machine State (Priority: P1)

**Goal**: Represent lights and simulate toggling via button operations
**Independent Test**: Initialize off-state, apply button sequences, check final state

### Tests (RED)

- [ ] T012 [P] [US2] Add unit tests for toggle behavior (even presses cancel; sequences from description)

### Implementation

- [ ] T013 [P] [US2] Implement `apply_button(state: list[int], indices: list[int]) -> list[int]` in `day-10/solution.py`
- [ ] T014 [US2] Implement `apply_sequence(state, buttons, counts)` in `day-10/solution.py`

Checkpoint: State modeling validated independently.

---

## Phase 5: User Story 3 — Minimum Presses per Machine (Priority: P1)

**Goal**: Compute minimal button presses from all-off to target per machine
**Independent Test**: Verify known examples return 2, 3, and 2 respectively

### Tests (RED)

- [ ] T015 [P] [US3] Add unit tests asserting min presses for the three sample machines (2, 3, 2)
- [ ] T016 [P] [US3] Add unit test for zero-press case (target all-off)

### Implementation

- [ ] T017 [US3] Implement GF(2) elimination helper: `min_presses(buttons, target) -> int` in `day-10/solution.py`
- [ ] T018 [US3] Integrate solver with parsed machine and return count

Checkpoint: Single-machine optimization works independently.

---

## Phase 6: User Story 4 — Sum Across Machines (Priority: P1)

**Goal**: Aggregate minimal presses for all machines in input
**Independent Test**: Provide multi-line input; verify sum equals expected

### Tests (RED)

- [ ] T019 [P] [US4] Add unit test that sums [2, 3, 2] to 7
- [ ] T020 [P] [US4] Add unit test for empty input → 0

### Implementation

- [ ] T021 [US4] Implement `solve_part1(input_text: str) -> int` to call parser + per-machine solver and sum
- [ ] T022 [US4] Add CLI entry path in `day-10/solution.py` to print result when run directly

Checkpoint: Part 1 end-to-end.

---

## Final Phase: Polish & Cross-Cutting

- [ ] T023 [P] Add README note in `day-10/README.md` summarizing approach and complexity
- [ ] T024 [P] Light refactor for clarity; keep tests green
- [ ] T025 Validate performance against full input (<= 30s)

---

## Dependencies & Execution Order

- Setup → Foundational → Stories (US1 → US2 → US3 → US4) → Polish
- Stories are independently testable; US3 depends on US1 for parsing; US4 depends on US3.

## Parallel Opportunities

- Parsing tests and implementation (T007–T011) can run in parallel across different files
- Modeling tests and implementation (T012–T014) are parallelizable
- Solver tests (T015–T016) and GF(2) helper (T017) can be parallelized
- Aggregation tests (T019–T020) and final integration (T021–T022) parallelizable post-foundation

## Implementation Strategy

- MVP: Complete US1 fully, validate parsing
- Then US3 to enable computing answers; US2 supports simulation but solver is primary
- Finally US4 for aggregation and completion
