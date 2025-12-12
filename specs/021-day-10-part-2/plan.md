# Implementation Plan: Day 10 Part 2 - Joltage Configuration Optimization

**Branch**: `021-day-10-part-2` | **Date**: 2025-12-12 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/021-day-10-part-2/spec.md`

## Summary

**Primary Requirement**: Solve a system of linear equations over non-negative integers to find the minimum total button presses required to bring factory machine joltage counters to exact target levels.

**Technical Approach**: Parse machine definitions to extract button effects and target values, then apply a linear optimization algorithm (likely Gaussian elimination with modular arithmetic or greedy optimization with backtracking) to find the minimum integer solution for each machine independently, aggregating results across all machines.

**Scope**: Parse input format, implement core solver, aggregate results, validate against three provided examples with known answers (10, 12, 11 → 33 total).

## Technical Context

**Language/Version**: Python 3.10+
**Primary Dependencies**: pytest (testing), ruff (linting)
**Storage**: File-based input (`input.txt`), no database required
**Testing**: pytest with red-green-refactor TDD cycle
**Target Platform**: Local CLI execution via `uv run -m cli.meta_runner`
**Project Type**: Single Python module (Advent of Code challenge)
**Performance Goals**: Single machine analysis < 1 second, full puzzle < 10 seconds
**Constraints**: Exact target matching required, integer-only press counts
**Scale/Scope**: Up to ~1000 machines in actual puzzle input, 10-20 buttons per machine

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

✅ **Principle I - Clean Python Code**: Solution MUST use Python 3.10+, follow PEP8, use ruff for linting/formatting. No violations expected.

✅ **Principle II - Structured Organization**: Solution placed in `day-10/` following existing convention with `solution_part2.py`, `test_solution_part2.py`, existing `input.txt` and `test_input.txt`.

✅ **Principle III - Function-Based Solutions**: MUST implement `solve_part2(input_data)` with docstring, imported by main solution entry point.

✅ **Principle IV - Test-Driven Development**: MUST follow red-green-refactor: tests written first using three documented examples (expected: 10, 12, 11), tests fail initially, then implementation makes them pass. Test file: `test_solution_part2.py`.

✅ **Principle V - Automation First**: Leverage existing `uv run -m cli.meta_runner` infrastructure. No new automation required for this feature.

✅ **Principle VI - AoC Compliance**: File-based operation only, no network calls. Fully compliant.

✅ **Principle VII - Documentation & Progress**: Solution integration documented in `day-10/README.md`. Progress tracked in main `README.md`.

✅ **Principle VIII - Specification-Driven Workflow**: This feature uses Specify framework for planning. Specification complete and unambiguous.

**Gate Result**: ✅ **PASS** - No constitution violations. Proceed with Phase 0 research.

## Project Structure

### Documentation (this feature)

```text
specs/021-day-10-part-2/
├── plan.md                          # This file (implementation plan)
├── spec.md                          # Feature specification
├── research.md                      # Phase 0 research (solver algorithm analysis)
├── data-model.md                    # Phase 1 data model (Machine, Button, Counter entities)
├── quickstart.md                    # Phase 1 quickstart guide
├── contracts/                       # Phase 1 API contracts (parsing interface)
│   ├── parser.md                    # Input format specification
│   └── solver.md                    # Solver interface specification
└── checklists/
    └── requirements.md              # Quality checklist (complete)
```

### Source Code (repository root)

```text
day-10/
├── solution.py                      # Part 1 solution (existing)
├── solution_part2.py                # Part 2 solution (NEW - to implement)
├── test_solution.py                 # Part 1 tests (existing)
├── test_solution_part2.py           # Part 2 tests (NEW - to implement via TDD)
├── test_input.txt                   # Part 1 test input (existing)
├── input.txt                        # Actual puzzle input
├── description.md                   # Problem description
└── README.md                        # Day 10 notes and progress (to update)
```

**Structure Decision**: Single-file solution approach (aligned with existing day folders). Part 2 solution in new `solution_part2.py` file with corresponding tests in `test_solution_part2.py`. Leverages existing parsing infrastructure from Part 1 where applicable.

## Complexity Tracking

No constitution violations requiring justification. All design decisions follow established Advent of Code patterns in this repository.

---

## Implementation Phases

### Phase 0: Research & Analysis

**Goal**: Understand the algorithm space and identify the optimal solver approach.

**Tasks**:

1. **Algorithm Research** - Analyze the mathematical nature of the problem
   - Determine if this is a linear Diophantine equation system
   - Research solution approaches: Gaussian elimination, greedy optimization, constraint solving
   - Evaluate performance characteristics for different algorithms
   - Document findings in `research.md`

2. **Edge Case Analysis** - Identify and document special cases
   - Zero targets (machine already configured)
   - Single button/counter scenarios
   - Large target numbers (hundreds/thousands)
   - Redundant buttons (multiple solutions exist)
   - Infeasible scenarios (impossible to reach target)

3. **Parsing Deep Dive** - Understand the exact input format
   - Extract all parts: indicator lights (ignored), buttons, targets
   - Handle variations in button/target count
   - Test parsing on all three provided examples
   - Document in `research.md`

**Output**: `research.md` containing algorithm evaluation, edge case analysis, and parsing strategy.

---

### Phase 1: Design & Data Model

**Goal**: Define entities, contracts, and implementation approach.

**Tasks**:

1. **Data Model Definition** - Formalize entities from spec
   - Machine: buttons list + targets list + solution
   - Button: indices + press count
   - Counter: index + target + current value
   - Create `data-model.md` with full schema and validation rules

2. **API/Contract Definition** - Define public interfaces
   - `parse_machine(line: str) -> Machine`
   - `solve_machine(machine: Machine) -> int` (returns min presses)
   - `solve_all(machines: List[Machine]) -> int` (returns total)
   - Create `contracts/parser.md` and `contracts/solver.md`

3. **Test Strategy** - Plan test structure using TDD
   - Test 1: Parse first example, verify 6 buttons and 4 targets
   - Test 2: Solve first example, expect 10 presses minimum
   - Test 3: Solve second example, expect 12 presses
   - Test 4: Solve third example, expect 11 presses
   - Test 5: Aggregate three examples, expect 33 total
   - Document in `quickstart.md`

**Output**: `data-model.md`, `contracts/parser.md`, `contracts/solver.md`, `quickstart.md`

---

### Phase 2: Implementation

**Goal**: Build working solution following TDD workflow.

**Tasks**:

1. **Test-Driven Development Cycle**
   - **RED**: Write all tests first (all fail initially)
     - Parser tests (extract buttons and targets)
     - Solver tests (minimum presses for each example)
     - Aggregation tests (sum across machines)
   - **GREEN**: Implement minimum code to pass each test group
     - Start with parser (simplest, enables all other tests)
     - Implement solver core (brute force acceptable if performance OK)
     - Add aggregation logic
   - **REFACTOR**: Optimize while keeping tests green
     - Optimize solver algorithm if needed (< 1 sec per machine)
     - Clean up code style

2. **Code Organization**
   - Create `day-10/solution_part2.py` with `solve_part2(input_data: str) -> int`
   - Create `day-10/test_solution_part2.py` with all TDD tests
   - Update `day-10/solution.py` if needed to integrate Part 2
   - Add module docstrings and function docstrings per Principle III

3. **Validation**
   - Run tests: all should pass (green)
   - Verify Part 1 still works (no regression)
   - Manual verification: run examples, confirm outputs match spec
   - Performance check: measure time on example input

**Output**: Working `solution_part2.py` with 100% passing tests, all spec scenarios validated.

---

### Phase 3: Documentation & Integration

**Goal**: Complete solution documentation and integrate with repository.

**Tasks**:

1. **README Update**
   - Update `day-10/README.md` with Part 2 explanation
   - Document algorithm choice and performance characteristics
   - Add notes on any interesting edge cases encountered
   - Update main repository `README.md` with Day 10 completion status

2. **Code Review Checklist**
   - [ ] All tests passing (green status)
   - [ ] No ruff linting errors
   - [ ] All functions have docstrings
   - [ ] Code follows PEP8
   - [ ] Part 1 integration verified (no regressions)
   - [ ] Performance < 1s per machine confirmed
   - [ ] All three examples produce exact expected results

3. **Final Commit**
   - Stage all changes
   - Create meaningful commit message
   - Push to `021-day-10-part-2` branch

**Output**: Fully integrated, documented solution ready for submission to AoC.

---

## Success Metrics

- ✅ Parser correctly extracts buttons and targets from all example inputs (100% accuracy)
- ✅ Solver finds exact minimum presses: 10, 12, 11 for examples (0% error)
- ✅ Aggregation produces 33 for three examples combined
- ✅ All tests pass (red-green-refactor complete)
- ✅ Performance: < 1 second per machine, < 10 seconds total
- ✅ Zero ruff violations on new code
- ✅ Complete documentation in place

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| Algorithm complexity | Low | High | Research phase identifies optimal approach before coding |
| Large input performance | Medium | Medium | Prototype solver on examples, optimize before full input |
| Parse errors | Low | Medium | Comprehensive TDD tests cover all variations |
| Part 1 regression | Low | Medium | Run full Part 1 test suite after each change |
