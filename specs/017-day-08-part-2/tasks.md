# Tasks: AoC Day 8 Part 2 - Complete Circuit Formation

**Feature**: 017-day-08-part-2  
**Generated**: December 10, 2025  
**Input**: Design documents from `specs/017-day-08-part-2/`

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

Single project structure - Advent of Code daily challenge:

- Solution code: `day-08/`
- Tests: `day-08/`
- Specifications: `specs/017-day-08-part-2/`

---

## Phase 1: Setup

**Purpose**: Test file creation and initial structure

- [x] T001 Create test file day-08/test_solution_part2.py with import statements
- [x] T002 Write example test for final connection (25272) in day-08/test_solution_part2.py
- [x] T003 Verify test FAILS with ModuleNotFoundError (RED phase validation)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core UnionFind data structure that ALL user stories depend on

**⚠️ CRITICAL**: UnionFind must be complete before any user story implementation can begin

- [x] T004 Create day-08/solution_part2.py with module docstring and imports from solution.py
- [x] T005 Implement UnionFind.**init**() in day-08/solution_part2.py
- [x] T006 Implement UnionFind.find() with path compression in day-08/solution_part2.py
- [x] T007 Implement UnionFind.union() with union-by-rank in day-08/solution_part2.py
- [x] T008 Implement UnionFind.is_fully_connected() in day-08/solution_part2.py

**Checkpoint**: UnionFind class complete - user story implementation can now begin

---

## Phase 3: User Story 3 - Process Connections in Distance Order (Priority: P2)

**Goal**: Ensure junction box pairs are processed by increasing Euclidean distance, reusing Part 1's distance calculation and sorting logic.

**Independent Test**: Verify distances are calculated correctly using Euclidean formula and sorted in ascending order before processing.

### Implementation for User Story 3

- [x] T009 [US3] Import parse_input from solution.py in day-08/solution_part2.py
- [x] T010 [US3] Import euclidean_distance from solution.py in day-08/solution_part2.py
- [x] T011 [US3] Import compute_all_distances from solution.py in day-08/solution_part2.py
- [x] T012 [US3] Verify distance calculation reuse by adding comment documenting Part 1 dependency

**Checkpoint**: Distance ordering infrastructure ready - can now track circuit membership

---

## Phase 4: User Story 2 - Track Circuit Membership During Connection Process (Priority: P2)

**Goal**: Accurately track which junction boxes belong to which circuit, skip redundant connections, and correctly merge circuits.

**Independent Test**: Process a sequence of connections and verify circuit membership is updated correctly after each merge.

### Implementation for User Story 2

- [x] T013 [US2] Add circuit membership validation logic in solve_part2() using UnionFind.find()
- [x] T014 [US2] Implement connection skipping when find(a) == find(b) in day-08/solution_part2.py
- [x] T015 [US2] Implement circuit merging via UnionFind.union() in day-08/solution_part2.py
- [x] T016 [US2] Add num_components tracking to monitor circuit count in day-08/solution_part2.py

**Checkpoint**: Circuit tracking complete - can now implement final connection detection

---

## Phase 5: User Story 1 - Find Final Connection to Unite All Circuits (Priority: P1) 🎯 MVP

**Goal**: Identify the exact pair of junction boxes whose connection unifies all circuits into one, then calculate the product of their X coordinates.

**Independent Test**: Process example input (20 boxes) and verify final connection produces 216 × 117 = 25272.

### Implementation for User Story 1

- [ ] T017 [US1] Implement solve_part2() function signature with input_data parameter in day-08/solution_part2.py
- [ ] T018 [US1] Add points parsing using parse_input() in solve_part2()
- [ ] T019 [US1] Add distance computation using compute_all_distances() in solve_part2()
- [ ] T020 [US1] Initialize UnionFind with len(points) in solve_part2()
- [ ] T021 [US1] Implement main processing loop iterating over sorted distances in solve_part2()
- [ ] T022 [US1] Add detection logic for num_components == 2 transition in solve_part2()
- [ ] T023 [US1] Calculate X-coordinate product for final connecting pair in solve_part2()
- [ ] T024 [US1] Add error handling for case where circuit never unifies in solve_part2()
- [ ] T025 [US1] Implement main() entry point with input file reading in day-08/solution_part2.py
- [ ] T026 [US1] Add if **name** == "**main**" block in day-08/solution_part2.py
- [ ] T027 [US1] Run test_solution_part2.py and verify it PASSES (GREEN phase)

**Checkpoint**: Core Part 2 solution complete and example test passes

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Code quality, documentation, and validation

- [x] T028 [P] Add type hints to all functions in day-08/solution_part2.py
- [x] T029 [P] Add docstrings to solve_part2() and main() in day-08/solution_part2.py
- [x] T030 [P] Add inline comments explaining UnionFind optimizations in day-08/solution_part2.py
- [x] T031 Run Ruff linter on day-08/solution_part2.py and fix any issues
- [x] T032 Run Ruff formatter on day-08/solution_part2.py
- [x] T033 Test with full puzzle input (day-08/input.txt) and verify performance <1 second
- [x] T034 [P] Update day-08/README.md with Part 2 solution summary
- [x] T035 Validate solution follows quickstart.md TDD workflow
- [ ] T036 Manual submission of Part 2 answer to Advent of Code website
- [x] T037 Update main README.md progress tracker with completion status

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - creates test file first (TDD)
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 3 (Phase 3)**: Depends on Foundational (needs UnionFind to exist)
- **User Story 2 (Phase 4)**: Depends on Foundational + User Story 3 (needs distance sorting and UnionFind)
- **User Story 1 (Phase 5)**: Depends on Foundational + User Story 2 + User Story 3 (integrates all components)
- **Polish (Phase 6)**: Depends on User Story 1 completion (MVP must work before polish)

### User Story Dependencies

- **User Story 3 (P2)**: Can start after Foundational - establishes distance ordering (reuses Part 1 code)
- **User Story 2 (P2)**: Depends on User Story 3 - needs sorted distances to track circuit membership correctly
- **User Story 1 (P1)**: Depends on User Stories 2 & 3 - integrates distance ordering and circuit tracking to find final connection

**Note**: Priority numbers (P1, P2) indicate business priority, but technical dependencies dictate actual execution order. US3 and US2 must complete before US1 despite US1 being highest priority.

### Within Each User Story

- **US3**: Sequential import tasks (T009-T012) - no parallelism (all touch same file imports)
- **US2**: Circuit tracking tasks (T013-T016) build on each other sequentially
- **US1**: Core implementation (T017-T027) must be sequential - each builds on previous
- **Polish**: Tasks T028, T029, T030, T034 marked [P] can run in parallel (different concerns)

### Parallel Opportunities

```bash
# Limited parallelism due to single solution file:
# Polish phase offers main parallel opportunities:
Task T028: "Add type hints to all functions"
Task T029: "Add docstrings to solve_part2() and main()"
Task T030: "Add inline comments for UnionFind optimizations"
Task T034: "Update day-08/README.md with Part 2 summary"
# These can be worked on in parallel as they touch different aspects
```

**Reality Check**: Since all implementation touches `day-08/solution_part2.py`, most tasks must be sequential. Main parallelism is during polish (documentation, type hints, comments can be added by different people or in different sessions).

---

## Implementation Strategy

### TDD Workflow (Following quickstart.md)

1. **RED**: Complete Phase 1 (Setup)

   - Create test file
   - Write failing test for example (25272)
   - Verify test FAILS

2. **GREEN**: Complete Phases 2-5 (Foundational + User Stories)

   - Build UnionFind (Phase 2)
   - Reuse distance code (Phase 3)
   - Add circuit tracking (Phase 4)
   - Implement core solver (Phase 5)
   - Verify test PASSES

3. **REFACTOR**: Complete Phase 6 (Polish)
   - Add type hints
   - Improve documentation
   - Optimize if needed
   - Submit answer

### MVP Definition

**MVP = User Story 1 complete** (Phase 5 done)

At this point:

- Example test passes (25272)
- Full puzzle input can be solved
- Answer ready for submission

### Incremental Validation

- **After Phase 1**: Test file exists and fails correctly (RED validated)
- **After Phase 2**: UnionFind class complete (can be unit tested separately if desired)
- **After Phase 3**: Distance calculation verified (reuse confirmed)
- **After Phase 4**: Circuit tracking works (membership updates correctly)
- **After Phase 5**: Example test passes (GREEN achieved) - **STOP and VALIDATE**
- **After Phase 6**: Code polished and production-ready

---

## Summary Statistics

- **Total Tasks**: 37
- **Phase 1 (Setup)**: 3 tasks
- **Phase 2 (Foundational)**: 5 tasks (BLOCKS all user stories)
- **Phase 3 (US3 - Distance Order)**: 4 tasks
- **Phase 4 (US2 - Circuit Tracking)**: 4 tasks
- **Phase 5 (US1 - Final Connection)**: 11 tasks (MVP)
- **Phase 6 (Polish)**: 10 tasks

**Parallel Opportunities**: 4 tasks (T028, T029, T030, T034 in polish phase)

**Critical Path**: Sequential through Setup → Foundational → US3 → US2 → US1 → Polish

**MVP Scope**: Complete through Phase 5 (T001-T027) = 27 tasks

**Estimated Complexity**: O(N² log N) for N junction boxes

- Example (N=20): ~8,000 operations
- Full input (N=1000): ~10,000,000 operations
- Expected runtime: <1 second

---

## Notes

- TDD approach: Test first (Phase 1), implementation second (Phases 2-5), refactor third (Phase 6)
- Code reuse strategy: Import parsing and distance functions from Part 1 (solution.py)
- Single file focus: Most implementation in day-08/solution_part2.py limits parallelism
- Performance validated: Union-Find approach 125x faster than dictionary approach for ~500k checks
- Constitution compliant: Standard library only, TDD workflow, manual submission
- No external dependencies beyond pytest for testing
