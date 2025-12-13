# Implementation Plan: Day 11 Part 1 - Reactor Path Finding

**Branch**: `022-day-11-part-1` | **Date**: December 13, 2025 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/022-day-11-part-1/spec.md`

## Summary

**Primary Requirement**: Find and count all distinct paths from device "you" to device "out" in a directed graph of reactor devices.

**Technical Approach**:

1. Parse device configuration into a directed graph representation
2. Implement depth-first search (DFS) with backtracking to enumerate all paths
3. Count unique paths and optionally display them for verification
4. Handle edge cases including disconnected components and empty configurations

## Technical Context

**Language/Version**: Python 3.10+  
**Primary Dependencies**: Standard library only (no external packages required for core logic)  
**Storage**: File input only (input.txt) - no persistent storage needed  
**Testing**: pytest for unit tests  
**Target Platform**: Python CLI tool (cross-platform)  
**Project Type**: Single solution module (follows day-XX/ structure)  
**Performance Goals**: Complete enumeration and path counting in under 1 second for example input  
**Constraints**: Must handle up to ~100 devices without performance degradation  
**Scale/Scope**: Single day solution with Part 1 focus (Part 2 may extend this design)

## Constitution Check

_GATE: Must pass before Phase 0 research. Re-check after Phase 1 design._

**Evaluation Against Advent of Code 2025 Constitution v1.4.0**:

✅ **Principle I - Clean Python Code**: PASS

- Solution will use Python 3.10+ with PEP8 compliance and Ruff linting

✅ **Principle II - Structured Organization**: PASS

- Follows required `day-11/` folder structure with `solution.py`, `input.txt`, `test_input.txt`, `README.md`

✅ **Principle III - Function-Based Solutions**: PASS

- Implementation will use `solve_part1(input_data)` function with docstrings
- Part 2 reserved for future extension

✅ **Principle IV - Test-Driven Development (NON-NEGOTIABLE)**: PASS

- TDD workflow will be enforced: RED → GREEN → REFACTOR
- Tests written FIRST based on puzzle examples, verified to FAIL before implementation
- Test file: `day-11/test_solution.py`

✅ **Principle V - Automation First**: PASS

- Uses meta runner for task setup and input downloads
- Session tokens via `.env`
- Manual answer submission by user

✅ **Principle VI - AoC Compliance & Rate Limiting**: PASS

- No automated submissions
- Respects Advent of Code terms of service

✅ **Principle VII - Documentation & Progress Tracking**: PASS

- README.md in day-11/ for notes
- Main README.md updated with progress

✅ **Principle VIII - Specification-Driven Workflow**: PASS

- Spec phase complete with 7 user stories and 13 functional requirements
- This plan generated from specification
- Task generation phase follows

✅ **Principle IX - Delightful CLI**: PASS

- Uses existing meta_runner CLI infrastructure
- Clear output formatting

**Constitution Gates**: ✅ ALL GATES PASS - No violations requiring justification

## Project Structure

### Documentation (this feature)

```text
specs/022-day-11-part-1/
├── spec.md              # Feature specification (COMPLETE)
├── plan.md              # This file (Implementation plan)
├── research.md          # Phase 0 output (N/A - no unknowns to research)
├── data-model.md        # Phase 1 output (Entity definitions)
├── quickstart.md        # Phase 1 output (Getting started guide)
├── contracts/           # Phase 1 output (API contracts if applicable)
│   └── (N/A for this feature)
├── checklists/
│   └── requirements.md   # Quality checklist (COMPLETE)
└── tasks.md             # Phase 2 output (TDD task breakdown - PENDING)
```

### Source Code (repository root)

```text
day-11/                          # Feature implementation
├── __init__.py                   # Python module marker
├── solution.py                   # Main solution implementation
│   ├── parse_device_config()     # Parse input configuration
│   ├── build_graph()             # Build directed graph structure
│   ├── find_all_paths()          # DFS with backtracking for path enumeration
│   ├── solve_part1()             # Main solution function (entry point)
│   └── [optional display functions]
├── input.txt                     # Actual puzzle input
├── test_input.txt                # Example input from problem description
├── test_solution.py              # Test cases (TDD - written first)
│   ├── test_parse_single_connection()
│   ├── test_parse_multiple_connections()
│   ├── test_build_graph_all_devices()
│   ├── test_find_single_path()
│   ├── test_enumerate_all_paths_example()
│   ├── test_count_paths()
│   ├── test_no_solution()
│   └── [other edge case tests]
├── README.md                     # Notes and learnings
└── __pycache__/                  # Python cache (gitignored)

tests/                           # Project-level test directory (existing)
├── (day-11 tests also in day-11/test_solution.py)
```

**Structure Decision**: Single project structure per Principle II. Each day is self-contained in its folder with co-located tests, inputs, and documentation. All Python execution via `uv run`.

## Complexity Tracking

> No violations - Constitution Check passed all gates. Research phase completed with detailed analysis.

| Item                        | Status       | Details                                     |
| --------------------------- | ------------ | ------------------------------------------- |
| **Input Scale**             | ✅ Analyzed  | 576 devices, 1,642 edges (27x example size) |
| **Branching Factor**        | ✅ Analyzed  | Avg 2.85 (low), max 24 (manageable)         |
| **Path Count**              | ✅ Estimated | 100-10,000 realistic, ~35,000 worst-case    |
| **Algorithm Performance**   | ✅ Confirmed | 50-600ms expected (well under 1s)           |
| **Cycle Risk**              | ✅ Mitigated | Visited set prevents infinite loops         |
| **Optimization Need**       | ✅ Assessed  | NOT REQUIRED (baseline sufficient)          |
| **Architecture Complexity** | ✅ Low       | Simple DFS, no complex patterns             |
| **Dependency Complexity**   | ✅ None      | Standard library only                       |

---

## Implementation Phases

### Phase 0: Research (COMPLETE ✅)

**Deliverable**: `research.md` - Computational complexity analysis

**Key Findings**:

- **Input Scale**: 575 lines → 576 devices, 1,642 edges (27x larger than example)
- **Branching Factor**: 2.85 average (low, mostly binary)
- **You's Outputs**: 10 initial branches
- **Out's Inputs**: 18 convergence points
- **Estimated Paths**: 100-10,000 (realistic), ~35,000 worst-case
- **Expected Runtime**: 50-600ms (well under 1s target)
- **Algorithm**: DFS with backtracking is ideal
- **Complexity**: O(V + E + P) where P = path count
- **Optimization**: Baseline DFS sufficient, no aggressive optimization needed
- **Risk Level**: LOW - straightforward algorithm, no architectural issues

**Rationale**: Analysis confirms DFS with visited set tracking is the right approach. No unknowns remain that would affect implementation strategy.

### Phase 1: Design & Data Model

**Deliverables** (to be generated):

- `data-model.md` - Entity definitions and relationships
- `quickstart.md` - Getting started guide for developers
- `contracts/` - Input/output format specifications (if applicable)

**Key Design Decisions** (informed by research.md):

1. **Graph Representation**:

   - Use adjacency list dictionary: `{device_name: [output_devices]}`
   - Efficient for DFS traversal with O(1) lookup
   - Supports devices with 0 to 24 outputs (observed range)
   - **Research Confirmed**: Average 2.85 outputs per device supports simple dict approach

2. **Path Enumeration Algorithm**:

   - Depth-first search (DFS) with backtracking
   - **Visited set for cycle safety**: Track nodes in current path to prevent infinite loops
   - Accumulate paths during recursion and return at base case
   - Time complexity: O(V + E + paths_found) = O(576 + 1,642 + estimated_paths)
   - **Research Confirmed**: With ~2.85 branching factor, 100-10,000 paths expected
   - Estimated runtime: 50-600ms (well under 1s target)

3. **Data Structures**:

   - Simple dictionaries for configuration data (no need for classes)
   - Functions for parsing and pathfinding (functional style per Principle III)
   - Visit set (current path): `set()` for O(1) membership testing

4. **Input Parsing**:

   - Line-by-line parsing: `device_name: output1 output2 ...`
   - Handle edge cases: empty outputs, missing devices, duplicates
   - **Research Data**: 575 input lines create 576 unique devices with 1,642 total edges
   - Deduplicate outputs using set during parsing

5. **Implementation Priority**:
   - Start with baseline DFS (no optimization)
   - Add visited set for cycle safety (minimal overhead)
   - Skip aggressive optimization (research shows not needed)
   - Measure actual performance on real input before optimizing

### Phase 2: TDD Task Breakdown (NEXT STEP)

**Will be generated by `/speckit.tasks` command**:

Tasks will be organized by user story and follow RED → GREEN → REFACTOR cycle:

**Part 1 Tasks** (from 5 P1 user stories):

- RED: Write tests for device parsing
- GREEN: Implement parse_device_config()
- REFACTOR: Optimize parsing
- RED: Write tests for graph building
- GREEN: Implement build_graph()
- REFACTOR: Optimize graph structure
- RED: Write tests for single path finding
- GREEN: Implement basic pathfinding
- REFACTOR: Clean up code
- RED: Write tests for path enumeration
- GREEN: Implement full DFS backtracking
- REFACTOR: Optimize performance
- RED: Write tests for path counting
- GREEN: Implement count function
- REFACTOR: Final cleanup

**Part 2 Tasks** (P2 user stories):

- RED: Write tests for path display
- GREEN: Implement display function
- REFACTOR: Format output nicely
- RED: Write tests for edge cases (no solution)
- GREEN: Handle edge cases
- REFACTOR: Improve error messages

### Phase 3: Development Workflow

**Per Constitution Principle VIII**, implementation follows this order:

1. ✅ **Spec Phase** (COMPLETE): Transform requirements into user stories
2. ➡️ **Tasks Phase** (NEXT): Generate task list with TDD breakdowns
3. **Execution Phase** (AFTER tasks):
   - RED: Write all test cases based on acceptance scenarios from spec
   - Verify all tests FAIL before writing implementation
   - GREEN: Implement solution functions incrementally
   - REFACTOR: Optimize and clean up while keeping tests green
   - Run full test suite to confirm all pass
4. **Verification Phase**:
   - Test against actual puzzle input
   - Prepare answer for manual submission
5. **Closure Phase**:
   - Commit to feature branch
   - Update main README.md
   - Mark feature complete

---

## Success Metrics

✅ **SC-001**: Parse example configuration correctly → identify 10 devices  
✅ **SC-002**: Enumerate exactly 5 paths in example → all paths valid and distinct  
✅ **SC-003**: Count correctly → return 5 for example input  
✅ **SC-004**: Handle disconnected components → return 0 when no path exists  
✅ **SC-005**: Performance → complete enumeration in <1 second  
✅ **SC-006**: Code quality → 100% test coverage, PEP8 compliant, well-documented

---

## Next Steps

1. ✅ **Feature branch created**: `022-day-11-part-1`
2. ✅ **Specification complete**: `spec.md` with 7 user stories, 13 FRs, 10 success criteria
3. ✅ **Plan created**: This document outlines implementation approach
4. ➡️ **NEXT: Generate task list** → Run `/speckit.tasks` command to create `tasks.md`
5. ➡️ **NEXT: Execute RED phase** → Write test cases in `day-11/test_solution.py`
6. ➡️ **NEXT: Execute GREEN phase** → Implement `day-11/solution.py`
7. ➡️ **NEXT: Verification** → Run against puzzle input and verify count
8. ➡️ **NEXT: Commit & close** → Feature completion

---

**Status**: Ready for task generation and TDD execution
