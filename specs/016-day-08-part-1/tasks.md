---
description: "Task list for Day 8 Part 1 - Circuit Analysis implementation"
---

# Tasks: AoC Day 8 Part 1 - Circuit Analysis

**Input**: Design documents from `/specs/016-day-08-part-1/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: TDD is MANDATORY per Constitution Principle IV. All tests must be written FIRST and FAIL before implementation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **AoC day folder**: `day-08/` for all source and test files
- **Spec folder**: `specs/016-day-08-part-1/` for planning documents

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create test file structure and prepare for TDD workflow

- [x] T001 Create test file day-08/test_solution.py with imports and fixtures
- [x] T002 Create solution file day-08/solution.py with module docstring

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core utilities and type definitions that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 Define type aliases (JunctionBox, DistancePair) in day-08/solution.py
- [x] T004 Create test fixture for example_input in day-08/test_solution.py
- [x] T005 [P] Create test fixture for sample_points in day-08/test_solution.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Parse Junction Box Coordinates (Priority: P1) 🎯 MVP

**Goal**: Load and parse 3D junction box coordinates from input file

**Independent Test**: Verify parsing produces correct list of (x, y, z) tuples matching input line count and values

### Tests for User Story 1 (TDD - Write FIRST, ensure FAIL) ⚠️

- [x] T006 [US1] Write test_parse_input() in day-08/test_solution.py (MUST FAIL)
- [x] T007 [US1] Write test_parse_input_validates_format() in day-08/test_solution.py (MUST FAIL)

### Implementation for User Story 1

- [x] T008 [US1] Implement parse_input() function in day-08/solution.py to pass tests
- [x] T009 [US1] Verify tests now PASS and refactor if needed

**Checkpoint**: At this point, parsing should be fully functional - can load any input file and extract coordinates

---

## Phase 4: User Story 2 - Calculate Euclidean Distances (Priority: P1)

**Goal**: Compute Euclidean distances between all junction box pairs for connection prioritization

**Independent Test**: Verify distance calculation matches formula √((x₂-x₁)² + (y₂-y₁)² + (z₂-z₁)²) for known coordinates

### Tests for User Story 2 (TDD - Write FIRST, ensure FAIL) ⚠️

- [x] T010 [US2] Write test_euclidean_distance() in day-08/test_solution.py (MUST FAIL)
- [x] T011 [US2] Write test_compute_all_distances() in day-08/test_solution.py (MUST FAIL)
- [x] T012 [US2] Write test_distances_sorted() in day-08/test_solution.py (MUST FAIL)

### Implementation for User Story 2

- [x] T013 [US2] Implement euclidean_distance() function in day-08/solution.py
- [x] T014 [US2] Implement compute_all_distances() function in day-08/solution.py
- [x] T015 [US2] Verify tests now PASS and refactor if needed

**Checkpoint**: At this point, can calculate and sort all pairwise distances for any set of junction boxes

---

## Phase 5: User Story 3 - Connect Closest Pairs Using Union-Find (Priority: P1)

**Goal**: Connect junction boxes iteratively by closest distance, forming circuits while skipping already-connected pairs

**Independent Test**: Verify example with 10 connections produces circuit sizes [5, 4, 2, 2, 1, 1, 1, 1, 1, 1, 1]

### Tests for User Story 3 (TDD - Write FIRST, ensure FAIL) ⚠️

- [x] T016 [US3] Write test_find_circuit() in day-08/test_solution.py (MUST FAIL)
- [x] T017 [US3] Write test_process_connections_creates_circuits() in day-08/test_solution.py (MUST FAIL)
- [x] T018 [US3] Write test_process_connections_skips_same_circuit() in day-08/test_solution.py (MUST FAIL)
- [x] T019 [US3] Write test_process_connections_example_10() in day-08/test_solution.py (MUST FAIL)

### Implementation for User Story 3

- [x] T020 [US3] Implement find_circuit() helper function in day-08/solution.py
- [x] T021 [US3] Implement process_connections() function in day-08/solution.py
- [x] T022 [US3] Verify tests now PASS and refactor if needed

**Checkpoint**: At this point, can build circuits from distance pairs with configurable connection count

---

## Phase 6: User Story 4 - Calculate Circuit Sizes and Identify Largest Three (Priority: P1)

**Goal**: Determine final circuit sizes, identify three largest, and compute their product

**Independent Test**: Verify example produces answer of 40 (5 × 4 × 2)

### Tests for User Story 4 (TDD - Write FIRST, ensure FAIL) ⚠️

- [x] T023 [US4] Write test_get_three_largest_sizes() in day-08/test_solution.py (MUST FAIL)
- [x] T024 [US4] Write test_solve_part1_example() in day-08/test_solution.py (MUST FAIL)
- [x] T025 [US4] Write test_solve_part1_full_input() in day-08/test_solution.py (MUST FAIL)

### Implementation for User Story 4

- [x] T026 [US4] Implement get_three_largest_sizes() function in day-08/solution.py
- [x] T027 [US4] Implement solve_part1() main function in day-08/solution.py
- [x] T028 [US4] Verify tests now PASS and refactor if needed

**Checkpoint**: All user stories complete - full solution functional and tested

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T029 [P] Add docstrings to all functions in day-08/solution.py
- [x] T030 [P] Add type hints to all function signatures in day-08/solution.py
- [x] T031 Run Ruff linting on day-08/solution.py and fix any issues
- [x] T032 Run all tests with pytest in verbose mode and verify 100% pass rate
- [x] T033 Test solution with full input.txt and verify answer
- [x] T034 Update main README.md with Day 8 Part 1 completion status

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-6)**: All depend on Foundational phase completion
  - User stories MUST be completed sequentially (US1 → US2 → US3 → US4)
  - Each story builds on previous story's functions
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Foundational (Phase 2) - Provides parse_input()
- **User Story 2 (P1)**: Depends on US1 - Uses parsed points to compute distances
- **User Story 3 (P1)**: Depends on US2 - Uses sorted distances to build circuits
- **User Story 4 (P1)**: Depends on US3 - Uses circuits to compute final answer

### Within Each User Story

1. **RED**: Write tests FIRST - they MUST fail
2. **GREEN**: Implement minimum code to pass tests
3. **REFACTOR**: Clean up code while keeping tests passing
4. Story complete → checkpoint validation → proceed to next story

### Parallel Opportunities

- **Phase 1**: T001 and T002 can run in parallel
- **Phase 2**: T004 and T005 can run in parallel (both are test fixtures)
- **Within each User Story**: All test-writing tasks can be written in parallel (they're in the same file but different test functions)
- **Phase 7 Polish**: T029 and T030 can run in parallel (docstrings and type hints)

---

## Parallel Example: User Story 1

```bash
# Write all tests for User Story 1 together (RED phase):
Task T006: "Write test_parse_input() in day-08/test_solution.py"
Task T007: "Write test_parse_input_validates_format() in day-08/test_solution.py"

# Run tests to verify they FAIL:
uv run pytest day-08/test_solution.py::test_parse_input -v
uv run pytest day-08/test_solution.py::test_parse_input_validates_format -v

# Implement solution (GREEN phase):
Task T008: "Implement parse_input() function in day-08/solution.py"

# Verify tests now PASS:
uv run pytest day-08/test_solution.py -v
```

---

## Implementation Strategy

### MVP First (All User Stories Required)

**NOTE**: For this AoC problem, all 4 user stories must be completed to produce the final answer. Each story represents a necessary step in the algorithm pipeline:

1. Complete Phase 1: Setup → Test and solution files created
2. Complete Phase 2: Foundational → Type definitions and fixtures ready
3. Complete Phase 3: User Story 1 → Can parse input ✓
4. Complete Phase 4: User Story 2 → Can calculate distances ✓
5. Complete Phase 5: User Story 3 → Can build circuits ✓
6. Complete Phase 6: User Story 4 → **MVP COMPLETE** - Produces final answer ✓
7. **VALIDATE**: Run with example (expect 40) and full input
8. Complete Phase 7: Polish → Production-ready solution

### Incremental Validation

After each user story completes, run partial integration tests:

1. **After US1**: Verify parse_input() works with test_input.txt and input.txt
2. **After US2**: Verify compute_all_distances() produces correct count (N\*(N-1)/2 pairs)
3. **After US3**: Verify process_connections() with 10 connections produces expected circuit distribution
4. **After US4**: Verify solve_part1() produces answer of 40 for example

### TDD Workflow (MANDATORY)

For each user story:

1. **RED**: Write test(s), run them, watch them FAIL
2. **GREEN**: Write minimal implementation to pass tests
3. **REFACTOR**: Clean up code while keeping tests green
4. **CHECKPOINT**: Validate story independently before moving to next

---

## Notes

- **[P]** tasks = different files or different test functions, no dependencies
- **[Story]** label maps task to specific user story for traceability
- **TDD is non-negotiable** per Constitution Principle IV - tests MUST be written first
- Each user story builds on previous stories (pipeline architecture)
- Stop at any checkpoint to validate story independently
- Example answer: 40 (circuits [5, 4, 2, 2, 1, 1, 1, 1, 1, 1, 1] → 5 × 4 × 2 = 40)
- Full input uses 1000 connections (example uses 10)
- Commit after each task or logical group (e.g., after each user story)

---

## Task Count Summary

- **Phase 1 (Setup)**: 2 tasks
- **Phase 2 (Foundational)**: 3 tasks
- **Phase 3 (US1)**: 4 tasks (2 tests + 2 implementation)
- **Phase 4 (US2)**: 6 tasks (3 tests + 3 implementation)
- **Phase 5 (US3)**: 7 tasks (4 tests + 3 implementation)
- **Phase 6 (US4)**: 6 tasks (3 tests + 3 implementation)
- **Phase 7 (Polish)**: 6 tasks

**Total**: 34 tasks

**Parallel Opportunities**: 7 tasks can run in parallel (marked with [P])

**Critical Path**: Setup → Foundational → US1 → US2 → US3 → US4 → Polish (sequential due to pipeline dependencies)
