# Implementation Plan: Day 9 Part 2 - Largest Red-Green Rectangle (Optimized Ray Tracing)

**Branch**: `019-day-09-part-2` | **Date**: December 11, 2025 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/019-day-09-part-2/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement an optimized rectangle validation algorithm for Day 9 Part 2 that finds the largest rectangle using red and green tiles. The solution parses a closed loop of red tile coordinates, precomputes green edge tiles into directional sets, and uses ray tracing with edge-only validation to identify valid rectangles. The key optimization is filtering edges by coordinate (x or y) to avoid scanning every grid position, enabling efficient rectangle validation on large grids.

## Technical Context

**Language/Version**: Python 3.10+  
**Primary Dependencies**: Python standard library (itertools, pathlib), pytest for testing  
**Storage**: File-based input (input.txt, test_input.txt) in day-09/ folder  
**Testing**: pytest with test files in day-09/ folder (test_solution_part2.py)  
**Target Platform**: Cross-platform CLI (Windows/Linux/macOS)  
**Project Type**: Single-file solution within day-09/ folder structure  
**Performance Goals**: Complete execution on actual puzzle input in under 10 seconds  
**Constraints**: <200ms for example input, avoid O(grid_size²) naive approaches  
**Scale/Scope**: Handle grids up to thousands of coordinates with efficient ray tracing

## Constitution Check

_GATE: Must pass before Phase 0 research. Re-check after Phase 1 design._

### Principle Compliance

✅ **I. Clean Python Code**: Solution will use Python 3.10+ features, follow PEP8, and use Ruff for linting  
✅ **II. Structured Organization**: Solution will reside in existing day-09/ folder with solution_part2.py  
✅ **III. Function-Based Solutions**: Solution will implement solve_part2(input_data) with full docstrings  
✅ **IV. Test-Driven Development**: TDD cycle (RED-GREEN-REFACTOR) will be strictly enforced with tests written first  
✅ **V. Automation First**: Meta runner already handles input download; manual submission required  
✅ **VI. AoC Compliance**: No automated submissions; respects rate limits  
✅ **VII. Documentation & Progress**: README will be updated with progress  
✅ **VIII. Specification-Driven Workflow**: This plan follows Specify framework workflow  
✅ **IX. Delightful CLI**: Execution via `uv run day-09/solution_part2.py`

**Initial Gate Status**: ✅ PASSED - No constitution violations detected

**Justification for Deviations**: None - this feature complies with all constitution principles

### Post-Design Constitution Re-Evaluation

**Re-evaluated After**: Phase 1 design completion (research, data model, contracts, quickstart)

✅ **I. Clean Python Code**:

- Research confirms use of type hints (Coordinate = Tuple[int, int])
- API contracts specify full PEP8 compliance
- All functions include comprehensive docstrings with examples

✅ **II. Structured Organization**:

- solution_part2.py and test_solution_part2.py clearly defined
- Follows existing day-09/ folder structure
- All files co-located per constitution requirements

✅ **III. Function-Based Solutions**:

- solve_part2(input_data) defined as main entry point
- 15+ supporting functions with clear separation of concerns
- EdgeIndex class for data structure encapsulation

✅ **IV. Test-Driven Development**:

- Quickstart.md enforces strict RED-GREEN-REFACTOR workflow
- Tests defined before implementation in 7 progressive phases
- Each phase includes failing test → implementation → refactor cycle

✅ **V. Automation First**:

- Solution uses existing meta runner infrastructure
- Input/description already downloaded for day-09
- Manual submission workflow preserved

✅ **VI. AoC Compliance**:

- No automated submission in design
- Rate limiting not applicable (reusing existing inputs)
- Session token handling by existing infrastructure

✅ **VII. Documentation & Progress**:

- Plan, research, data-model, contracts, quickstart all generated
- README.md update included in validation checklist
- Progress tracking via constitution compliance

✅ **VIII. Specification-Driven Workflow**:

- Full spec → plan → research → design workflow completed
- Constitution check enforced at both gates
- Tasks phase deferred to /speckit.tasks command

✅ **IX. Delightful CLI**:

- Execution via standard `uv run day-09/solution_part2.py`
- Test execution via `uv run pytest day-09/test_solution_part2.py`
- Follows established project patterns

**Post-Design Gate Status**: ✅ PASSED - Design maintains full constitution compliance

**Design Quality Assessment**:

- **Modularity**: 15+ well-defined functions with single responsibilities
- **Testability**: Each function independently testable per TDD requirements
- **Performance**: Coordinate filtering optimization documented and justified
- **Maintainability**: Clear abstractions (EdgeIndex, Ray, Segment concepts)
- **Documentation**: Comprehensive docstrings, contracts, and implementation guide

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
day-09/
├── __init__.py
├── solution.py           # Part 1 solution (already exists)
├── solution_part2.py     # Part 2 solution (NEW - this feature)
├── test_solution.py      # Part 1 tests (already exists)
├── test_solution_part2.py # Part 2 tests (NEW - this feature)
├── input.txt            # Actual puzzle input (already exists)
├── test_input.txt       # Example input (already exists)
├── description.md       # Challenge description (already exists)
└── README.md            # Notes and explanations (already exists)
```

**Structure Decision**: Following Advent of Code convention (Principle II), this Part 2 solution extends the existing day-09/ folder. The solution_part2.py file will contain the optimized ray tracing algorithm with edge-only validation, while test_solution_part2.py will contain comprehensive TDD tests covering all user stories from the specification.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No complexity violations detected - this feature complies fully with all constitution principles.

---

## Planning Phase Summary

**Status**: ✅ **PLANNING COMPLETE** (Phases 0-1 finished, Phase 2 deferred to /speckit.tasks)

### Artifacts Generated

| Artifact                | Location                                   | Status      | Purpose                                             |
| ----------------------- | ------------------------------------------ | ----------- | --------------------------------------------------- |
| **Feature Spec**        | `specs/019-day-09-part-2/spec.md`          | ✅ Complete | User stories, requirements, success criteria        |
| **Implementation Plan** | `specs/019-day-09-part-2/plan.md`          | ✅ Complete | This file - technical context, constitution gates   |
| **Research Document**   | `specs/019-day-09-part-2/research.md`      | ✅ Complete | Algorithmic decisions, technology choices           |
| **Data Model**          | `specs/019-day-09-part-2/data-model.md`    | ✅ Complete | Entity definitions, relationships, validation rules |
| **API Contracts**       | `specs/019-day-09-part-2/contracts/api.md` | ✅ Complete | Function signatures, contracts, error handling      |
| **Quickstart Guide**    | `specs/019-day-09-part-2/quickstart.md`    | ✅ Complete | Step-by-step TDD implementation guide               |
| **Agent Context**       | `.github/agents/copilot-instructions.md`   | ✅ Updated  | GitHub Copilot context with new tech stack          |

### Key Design Decisions

1. **Winding Detection**: Shoelace formula for O(n) signed area computation
2. **Turn Classification**: 2D cross product for convex/concave determination
3. **Edge Optimization**: Coordinate-indexed edge sets (100x speedup for sparse grids)
4. **Validation Strategy**: Edge-only rectangle validation leveraging simple-polygon guarantee
5. **Data Structure**: EdgeIndex class with horizontal/vertical edge dictionaries
6. **Algorithm Complexity**: O(n² × K) where K = edges per coordinate << total edges

### Technical Stack Confirmed

- **Language**: Python 3.10+ with type hints
- **Testing**: pytest with TDD (RED-GREEN-REFACTOR)
- **Dependencies**: Standard library only (itertools, pathlib)
- **Performance Target**: <10s for actual input, <200ms for examples
- **Code Quality**: Ruff linting, PEP8 compliance, comprehensive docstrings

### Constitution Compliance Verified

✅ All 9 principles verified at both gates (initial + post-design)  
✅ No complexity violations or deviations required  
✅ TDD workflow explicitly enforced in quickstart guide  
✅ Clean code patterns documented in research and contracts

### Research Highlights

**Phase 0 Deliverables**:

- Polygon winding detection algorithm (shoelace formula)
- Turn classification logic (cross product + winding awareness)
- Ray casting with state toggling and segment generation
- Coordinate filtering optimization for edge lookup
- Zero-width segment handling for boundary-hugging rays

**Implementation Patterns**:

- 15+ well-defined functions with clear responsibilities
- EdgeIndex class for O(K) edge lookup vs O(E) naive approach
- Segment-based validation with inside/outside state tracking
- Rectangle enumeration via itertools.combinations
- Comprehensive error handling with descriptive messages

### Next Steps

**Phase 2 - Task Generation** (use `/speckit.tasks` command):

1. Run `/speckit.tasks` to generate `specs/019-day-09-part-2/tasks.md`
2. Tasks will break down implementation into granular TDD steps
3. Each task will reference quickstart guide phases

**Implementation Workflow**:

1. Follow TDD phases in `quickstart.md`
2. Implement functions per API contracts in `contracts/api.md`
3. Validate against data model in `data-model.md`
4. Reference research decisions in `research.md`
5. Run tests continuously: `uv run pytest day-09/test_solution_part2.py`
6. Execute solution: `uv run day-09/solution_part2.py < day-09/input.txt`

**Success Criteria**:

- All pytest tests pass (green)
- Example input produces correct answer (24)
- Actual input completes in <10 seconds
- Ruff linting passes with no errors
- Answer accepted by Advent of Code

---

## Command Execution Report

**Branch**: `019-day-09-part-2`  
**Spec Directory**: `c:\Users\YJ42EK\coding\advent-of-code-2025\specs\019-day-09-part-2`  
**Execution Date**: December 11, 2025

**Phases Completed**:

- ✅ **Setup**: Variables initialized, plan template copied
- ✅ **Phase 0**: Research completed (winding, classification, ray casting, optimization)
- ✅ **Phase 1**: Design artifacts generated (data model, contracts, quickstart)
- ✅ **Phase 1**: Agent context updated (GitHub Copilot)
- ✅ **Constitution Gates**: Both initial and post-design gates passed

**Phase 2 Deferred**: Task generation should be run separately via `/speckit.tasks` command as per specification-driven workflow.

---

**Planning Status**: ✅ **COMPLETE**  
**Ready for**: Task generation (`/speckit.tasks`) and TDD implementation
