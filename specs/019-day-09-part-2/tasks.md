# Tasks: Day 9 Part 2 - Largest Red-Green Rectangle (Optimized Ray Tracing)

**Input**: Design documents from `/specs/019-day-09-part-2/`  
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅, quickstart.md ✅

**Tests**: Tests are REQUIRED per Constitution Principle IV (TDD is NON-NEGOTIABLE)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story. All tasks follow the strict TDD workflow: RED → GREEN → REFACTOR.

---

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and file structure

- [ ] T001 Verify day-09/ folder structure exists with **init**.py, input.txt, test_input.txt
- [ ] T002 Create day-09/solution_part2.py with module docstring and imports
- [ ] T003 Create day-09/test_solution_part2.py with module docstring and pytest imports

---

## Phase 2: User Story 1 - Parse Loop and Classify Convex vs Concave Turns (Priority: P1) 🎯

**Goal**: Parse red tile coordinates, validate axis alignment, detect winding, and classify each vertex as convex or concave

**Independent Test**: Can be fully tested by parsing the example input (8 red tiles) and verifying axis alignment, signed area/winding, and turn classification with wraparound

### Part A: Parsing & Validation (RED → GREEN → REFACTOR)

- [ ] T004 [US1] **RED**: Write test_parse_coordinates_valid in day-09/test_solution_part2.py
- [ ] T005 [US1] **RED**: Write test_parse_coordinates_with_whitespace in day-09/test_solution_part2.py
- [ ] T006 [US1] **RED**: Write test_parse_coordinates_empty_input in day-09/test_solution_part2.py
- [ ] T007 [US1] **RED**: Write test_validate_axis_alignment_valid in day-09/test_solution_part2.py
- [ ] T008 [US1] **RED**: Write test_validate_axis_alignment_invalid in day-09/test_solution_part2.py
- [ ] T009 [US1] **RED**: Run tests and verify ALL FAIL (no implementation exists)
- [ ] T010 [US1] **GREEN**: Implement parse_coordinates() function in day-09/solution_part2.py
- [ ] T011 [US1] **GREEN**: Implement validate_axis_alignment() function in day-09/solution_part2.py
- [ ] T012 [US1] **GREEN**: Run tests and verify ALL PASS
- [ ] T013 [US1] **REFACTOR**: Add docstring examples, clean up validation logic

### Part B: Winding Detection (RED → GREEN → REFACTOR)

- [ ] T014 [US1] **RED**: Write test_compute_signed_area_clockwise in day-09/test_solution_part2.py
- [ ] T015 [US1] **RED**: Write test_compute_signed_area_ccw in day-09/test_solution_part2.py
- [ ] T016 [US1] **RED**: Write test_is_clockwise_example in day-09/test_solution_part2.py
- [ ] T017 [US1] **RED**: Run tests and verify ALL FAIL
- [ ] T018 [US1] **GREEN**: Implement compute_signed_area() function in day-09/solution_part2.py
- [ ] T019 [US1] **GREEN**: Implement is_clockwise() function in day-09/solution_part2.py
- [ ] T020 [US1] **GREEN**: Run tests and verify ALL PASS
- [ ] T021 [US1] **REFACTOR**: Optimize for integer coordinates if needed

### Part C: Turn Classification (RED → GREEN → REFACTOR)

- [ ] T022 [US1] **RED**: Write test_compute_direction_vector in day-09/test_solution_part2.py
- [ ] T023 [US1] **RED**: Write test_classify_turn_convex in day-09/test_solution_part2.py
- [ ] T024 [US1] **RED**: Write test_classify_turn_concave in day-09/test_solution_part2.py
- [ ] T025 [US1] **RED**: Write test_classify_all_vertices_example in day-09/test_solution_part2.py
- [ ] T026 [US1] **RED**: Run tests and verify ALL FAIL
- [ ] T027 [US1] **GREEN**: Implement compute_direction_vector() function in day-09/solution_part2.py
- [ ] T028 [US1] **GREEN**: Implement classify_turn() function in day-09/solution_part2.py
- [ ] T029 [US1] **GREEN**: Implement classify_all_vertices() function in day-09/solution_part2.py
- [ ] T030 [US1] **GREEN**: Run tests and verify ALL PASS
- [ ] T031 [US1] **REFACTOR**: Clean up classification logic, ensure wraparound is correct

**Checkpoint US1**: At this point, User Story 1 should be fully functional - parsing, winding detection, and turn classification all working independently

---

## Phase 3: User Story 2 - Precompute Green Edge Tiles into Directional Sets (Priority: P1)

**Goal**: Precompute all green edge tiles (connecting consecutive red tiles) and organize them into horizontal and vertical edge sets indexed by coordinate

**Independent Test**: Can be fully tested by computing edges from example input and verifying horizontal and vertical sets contain correct green tile positions along each edge segment

### Edge Index Implementation (RED → GREEN → REFACTOR)

- [ ] T032 [US2] **RED**: Write test_edge_index_horizontal_edges in day-09/test_solution_part2.py
- [ ] T033 [US2] **RED**: Write test_edge_index_vertical_edges in day-09/test_solution_part2.py
- [ ] T034 [US2] **RED**: Write test_edge_index_wraparound in day-09/test_solution_part2.py
- [ ] T035 [US2] **RED**: Run tests and verify ALL FAIL
- [ ] T036 [US2] **GREEN**: Implement EdgeIndex class with **init**() in day-09/solution_part2.py
- [ ] T037 [US2] **GREEN**: Implement EdgeIndex.\_build_index() method in day-09/solution_part2.py
- [ ] T038 [US2] **GREEN**: Implement EdgeIndex.get_edges_at_x() method in day-09/solution_part2.py
- [ ] T039 [US2] **GREEN**: Implement EdgeIndex.get_edges_at_y() method in day-09/solution_part2.py
- [ ] T040 [US2] **GREEN**: Run tests and verify ALL PASS
- [ ] T041 [US2] **REFACTOR**: Optimize edge storage, add verbose output for edge counts

**Checkpoint US2**: At this point, User Story 2 should be fully functional - edge index precomputation working with coordinate-based lookup

---

## Phase 4: User Story 3 - Cast Rays with Formal Start Rules and Boundary Handling (Priority: P1)

**Goal**: For each candidate rectangle corner, cast rays in perpendicular directions using prefiltered edge sets, determine initial ray state, and generate inside/outside segments based on edge crossings

**Independent Test**: Can be fully tested by casting rays for known rectangles and verifying ordered list of segment tuples (start, end, in/out) against hand-derived expectations

### Ray Segment Generation (RED → GREEN → REFACTOR)

- [ ] T042 [US3] **RED**: Write test_generate_ray_segments_no_crossings in day-09/test_solution_part2.py
- [ ] T043 [US3] **RED**: Write test_generate_ray_segments_with_crossings in day-09/test_solution_part2.py
- [ ] T044 [US3] **RED**: Write test_filter_zero_width_segments in day-09/test_solution_part2.py
- [ ] T045 [US3] **RED**: Run tests and verify ALL FAIL
- [ ] T046 [US3] **GREEN**: Implement generate_ray_segments() function in day-09/solution_part2.py
- [ ] T047 [US3] **GREEN**: Implement filter_zero_width_segments() function in day-09/solution_part2.py
- [ ] T048 [US3] **GREEN**: Run tests and verify ALL PASS
- [ ] T049 [US3] **REFACTOR**: Clean up segment generation logic

### Initial Ray State Determination (RED → GREEN → REFACTOR)

- [ ] T050 [US3] **RED**: Write test_determine_initial_ray_state_inside in day-09/test_solution_part2.py
- [ ] T051 [US3] **RED**: Write test_determine_initial_ray_state_outside in day-09/test_solution_part2.py
- [ ] T052 [US3] **RED**: Run tests and verify ALL FAIL
- [ ] T053 [US3] **GREEN**: Implement determine_initial_ray_state() function in day-09/solution_part2.py
- [ ] T054 [US3] **GREEN**: Run tests and verify ALL PASS
- [ ] T055 [US3] **REFACTOR**: Verify boundary check logic for perpendicular edges

**Checkpoint US3**: At this point, User Story 3 should be fully functional - ray casting with proper state determination and segment generation

---

## Phase 5: User Story 4 - Validate Rectangles via Boundary Segments and Find Maximum Area (Priority: P1)

**Goal**: Enumerate all possible rectangles formed by pairs of red tiles, validate each using ray segment data along the four rectangle edges, calculate valid rectangle areas, and identify the maximum

**Independent Test**: Can be fully tested by running on the example input and verifying the maximum area is 24, with step-by-step output showing which rectangles are valid/invalid

### Rectangle Edge Validation (RED → GREEN → REFACTOR)

- [ ] T056 [US4] **RED**: Write test_validate_rectangle_edge_inside in day-09/test_solution_part2.py
- [ ] T057 [US4] **RED**: Write test_validate_rectangle_edge_outside in day-09/test_solution_part2.py
- [ ] T058 [US4] **RED**: Write test_calculate_rectangle_area in day-09/test_solution_part2.py
- [ ] T059 [US4] **RED**: Run tests and verify ALL FAIL
- [ ] T060 [US4] **GREEN**: Implement validate_rectangle_edge() function in day-09/solution_part2.py
- [ ] T061 [US4] **GREEN**: Implement calculate_rectangle_area() function in day-09/solution_part2.py
- [ ] T062 [US4] **GREEN**: Run tests and verify ALL PASS
- [ ] T063 [US4] **REFACTOR**: Optimize edge validation logic

### Rectangle Enumeration and Validation (RED → GREEN → REFACTOR)

- [ ] T064 [US4] **RED**: Write test_enumerate_rectangles in day-09/test_solution_part2.py
- [ ] T065 [US4] **RED**: Write test_validate_rectangle_with_rays in day-09/test_solution_part2.py
- [ ] T066 [US4] **RED**: Run tests and verify ALL FAIL
- [ ] T067 [US4] **GREEN**: Implement enumerate_rectangles() function in day-09/solution_part2.py
- [ ] T068 [US4] **GREEN**: Implement validate_rectangle() function with 4-ray casting in day-09/solution_part2.py
- [ ] T069 [US4] **GREEN**: Run tests and verify ALL PASS
- [ ] T070 [US4] **REFACTOR**: Optimize rectangle validation, add verbose output option

**Checkpoint US4**: At this point, User Story 4 should be fully functional - rectangle validation and maximum area calculation working correctly

---

## Phase 6: User Story 5 - Execute Final Solution with Minimal Output (Priority: P1) 🎯 MVP

**Goal**: Run solution in production mode (no verbose output) on actual puzzle input and produce only the final answer as a single integer

**Independent Test**: Can be fully tested by running the solution on actual puzzle input and verifying it produces the correct answer in reasonable time with minimal terminal output

### Integration and Main Entry Point (RED → GREEN → REFACTOR)

- [ ] T071 [US5] **RED**: Write test_solve_part2_example in day-09/test_solution_part2.py
- [ ] T072 [US5] **RED**: Run test and verify it FAILS
- [ ] T073 [US5] **GREEN**: Implement solve_part2() function in day-09/solution_part2.py
- [ ] T074 [US5] **GREEN**: Integrate all components (parse → winding → classify → edges → rays → validate → max)
- [ ] T075 [US5] **GREEN**: Run test and verify it PASSES with result == 24
- [ ] T076 [US5] **REFACTOR**: Add error handling, clean up integration logic

### CLI Entry Point and Production Execution

- [ ] T077 [US5] Add if **name** == "**main**" block to day-09/solution_part2.py
- [ ] T078 [US5] Add argparse for input file handling (read from stdin or file)
- [ ] T079 [US5] Test on example: `uv run day-09/solution_part2.py < day-09/test_input.txt`
- [ ] T080 [US5] Verify example output is exactly: 24
- [ ] T081 [US5] Run on actual input: `uv run day-09/solution_part2.py < day-09/input.txt`
- [ ] T082 [US5] Verify execution completes in under 10 seconds
- [ ] T083 [US5] Submit answer to Advent of Code website (manual submission)

**Checkpoint US5**: At this point, User Story 5 should be fully functional - complete solution running on actual input with correct answer

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Code quality, documentation, and final validation

- [ ] T084 [P] Run full test suite: `uv run pytest day-09/test_solution_part2.py -v`
- [ ] T085 [P] Verify all tests pass (100% pass rate)
- [ ] T086 [P] Run linter: `uv run ruff check day-09/solution_part2.py`
- [ ] T087 [P] Fix any linting errors
- [ ] T088 [P] Run formatter: `uv run ruff format day-09/solution_part2.py`
- [ ] T089 [P] Verify all functions have type hints
- [ ] T090 [P] Verify all functions have docstrings with examples
- [ ] T091 Add verbose mode flag for debugging (optional enhancement)
- [ ] T092 Add performance timing output (optional enhancement)
- [ ] T093 Update day-09/README.md with Part 2 notes
- [ ] T094 Update main README.md with Day 9 Part 2 completion status
- [ ] T095 Commit with message: `feat: solve day 09 part 2 - optimized ray tracing`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - can start immediately
- **Phase 2 (US1)**: Depends on Phase 1 (Setup)
- **Phase 3 (US2)**: Depends on Phase 1 (Setup) - Independent of US1 but logical to follow
- **Phase 4 (US3)**: Depends on Phase 3 (US2) for EdgeIndex class
- **Phase 5 (US4)**: Depends on Phase 4 (US3) for ray segment generation
- **Phase 6 (US5)**: Depends on Phases 2-5 (all user stories) for integration
- **Phase 7 (Polish)**: Depends on Phase 6 (US5) completion

### Within Each User Story

**TDD Workflow (STRICTLY ENFORCED)**:

1. **RED**: Write tests FIRST - verify tests FAIL
2. **GREEN**: Implement minimal code - verify tests PASS
3. **REFACTOR**: Clean up code - verify tests still PASS

### Critical Path

The critical path for MVP delivery:

```
Setup (T001-T003)
  → US1 Part A (T004-T013)
  → US1 Part B (T014-T021)
  → US1 Part C (T022-T031)
  → US2 (T032-T041)
  → US3 Segments (T042-T049)
  → US3 Initial State (T050-T055)
  → US4 Edge Validation (T056-T063)
  → US4 Rectangle Validation (T064-T070)
  → US5 Integration (T071-T076)
  → US5 CLI (T077-T083)
  → Polish (T084-T095)
```

### Parallel Opportunities

**Within Setup Phase**:

- T001, T002, T003 can be done together (but sequential is fine for simple setup)

**Within User Story 1**:

- All RED test-writing tasks (T004-T008) can be written together
- All RED test-writing tasks (T014-T016) can be written together
- All RED test-writing tasks (T022-T025) can be written together

**Within User Story 2**:

- All RED test-writing tasks (T032-T034) can be written together

**Within User Story 3**:

- All RED test-writing tasks (T042-T044) can be written together
- All RED test-writing tasks (T050-T051) can be written together

**Within User Story 4**:

- All RED test-writing tasks (T056-T058) can be written together
- All RED test-writing tasks (T064-T065) can be written together

**Within Polish Phase**:

- T084-T090 are all marked [P] and can run in parallel

**Between User Stories**:

- User Stories are intentionally sequential due to dependencies (US2 needs setup, US3 needs US2, etc.)
- However, test writing across stories could be done in advance if desired

---

## Parallel Example: User Story 1 Part A

```bash
# Launch all RED test tasks together for Part A:
Task T004: Write test_parse_coordinates_valid
Task T005: Write test_parse_coordinates_with_whitespace
Task T006: Write test_parse_coordinates_empty_input
Task T007: Write test_validate_axis_alignment_valid
Task T008: Write test_validate_axis_alignment_invalid

# Then verify all fail (T009)
# Then implement functions (T010-T011)
# Then verify all pass (T012)
# Then refactor (T013)
```

---

## Implementation Strategy

### MVP First (Recommended for Advent of Code)

1. **Phase 1**: Setup (T001-T003) → Quick project initialization
2. **Phase 2**: US1 Complete (T004-T031) → Parsing & classification foundation
3. **Phase 3**: US2 Complete (T032-T041) → Edge index optimization
4. **Phase 4**: US3 Complete (T042-T055) → Ray casting mechanics
5. **Phase 5**: US4 Complete (T056-T070) → Rectangle validation
6. **Phase 6**: US5 Complete (T071-T083) → Integration & answer
7. **Phase 7**: Polish (T084-T095) → Quality & documentation

**STOP and VALIDATE** after each phase - ensure tests are green before proceeding.

### TDD Discipline (NON-NEGOTIABLE per Constitution)

- Every implementation task MUST be preceded by failing tests
- Tests must be verified to FAIL before writing implementation
- Tests must be verified to PASS after implementation
- No skipping the RED phase - this validates test correctness

### Quickstart Alignment

Each phase maps directly to phases in `quickstart.md`:

- Phase 2 (US1) → Quickstart Phases 1-3
- Phase 3 (US2) → Quickstart Phase 4
- Phase 4 (US3) → Quickstart Phase 5
- Phase 5 (US4) → Quickstart Phase 6
- Phase 6 (US5) → Quickstart Phase 7

---

## Task Summary

**Total Tasks**: 95  
**Setup**: 3 tasks  
**User Story 1**: 28 tasks (parsing, winding, classification)  
**User Story 2**: 10 tasks (edge index)  
**User Story 3**: 14 tasks (ray casting)  
**User Story 4**: 15 tasks (rectangle validation)  
**User Story 5**: 13 tasks (integration & CLI)  
**Polish**: 12 tasks (quality & documentation)

**Estimated Time**: 4-6 hours for experienced developer following TDD strictly

**Success Criteria**:

- ✅ All 95 tasks completed in order
- ✅ All pytest tests pass (green)
- ✅ Example input produces answer: 24
- ✅ Actual input runs in < 10 seconds
- ✅ Ruff linting passes with no errors
- ✅ Answer accepted by Advent of Code

---

## Notes

- **[P]** marker indicates tasks that can run in parallel (same file operations allowed)
- **[Story]** label (US1-US5) maps task to specific user story for traceability
- **RED-GREEN-REFACTOR** cycle is explicitly enforced in task descriptions
- File paths are concrete: `day-09/solution_part2.py` and `day-09/test_solution_part2.py`
- Each user story checkpoint provides validation opportunity
- Constitution Principle IV (TDD) is strictly enforced throughout
- Quickstart guide provides detailed code examples for each phase
