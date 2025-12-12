# Implementation Plan: Day 10 Part 2 - Joltage Configuration Optimization

**Branch**: `021-day-10-part-2` | **Date**: 2025-12-12 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/021-day-10-part-2/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Extend Day 10 Part 1 (indicator light toggle system solved with GF(2) linear algebra) to Part 2 (joltage counter increment system solved with non-negative integer linear programming). Both parts use the same button matrix B but different fields: Part 1 operates mod 2 (toggles), Part 2 operates over non-negative integers (increments). The core requirement is finding minimum button presses to reach exact joltage targets starting from 0, where each button increments specific counters by +1.

**Technical Approach** (from research.md):

- **Algorithm**: Gaussian elimination with free variable enumeration over integers
- **Matrix Construction**: Build B where B[i,j] = 1 if button j affects counter i
- **Solving**: Row-reduce [B|t] to identify pivot/free variables, enumerate free variable assignments, back-substitute for pivot variables, minimize L1 norm
- **Optimization**: Smart bounds from LP relaxation to reduce enumeration space
- **Validation**: Verify B·x = t exactly with x ≥ 0 and x ∈ ℤ

**Key Decision**: Use NumPy-only implementation (no additional MILP dependencies) for small-scale systems with k ≤ 15 free variables, expected performance <0.1s per machine.

## Technical Context

**Language/Version**: Python 3.10+  
**Primary Dependencies**: NumPy for matrix operations, SciPy for linear programming optimization  
**Storage**: File-based input (`day-10/input.txt`, `day-10/test_input.txt`)  
**Testing**: pytest with test-driven development (TDD) workflow  
**Target Platform**: Local development environment (Windows/Linux/macOS)  
**Project Type**: Single project (Advent of Code challenge)  
**Performance Goals**: <1 second per machine, <10 seconds total for full puzzle input  
**Constraints**: Non-negative integer solutions only, exact target matching required  
**Scale/Scope**: ~3-5 machines in example, potentially 100+ in actual puzzle input

## Constitution Check

_GATE: Must pass before Phase 0 research. Re-check after Phase 1 design._

### Principle I: Clean Python Code

✅ **PASS** - Solution will use Python 3.10+ with type hints, PEP8 compliance via Ruff

### Principle II: Structured Organization

✅ **PASS** - Day 10 folder already exists with required structure (`day-10/solution.py`, `input.txt`, `test_input.txt`, test files)

### Principle III: Function-Based Solutions

✅ **PASS** - Part 2 will follow existing pattern: `solve_part2(input_data)` function with docstrings

### Principle IV: Test-Driven Development (NON-NEGOTIABLE)

✅ **PASS** - TDD workflow will be enforced:

- RED: Write `test_solution_part2.py` with failing tests based on 3 examples (10, 12, 11 expected)
- GREEN: Implement `solve_part2()` and `solution_part2.py` to pass tests
- REFACTOR: Optimize linear programming approach

### Principle V: Automation First

✅ **PASS** - Meta runner already downloaded inputs. Manual submission required (AoC compliant).

### Principle VI: AoC Compliance & Rate Limiting

✅ **PASS** - No new network interactions. Manual submission only.

### Principle VII: Documentation & Progress Tracking

✅ **PASS** - Progress will be tracked in main README.md upon completion

### Principle VIII: Specification-Driven Workflow

✅ **PASS** - Using Specify framework: spec.md → plan.md → tasks.md workflow

### Principle IX: Delightful CLI

✅ **PASS** - Will use existing meta runner for execution with `uv run`

### Code Structure Requirements

✅ **PASS** - UV-based execution, Git versioning on branch `021-day-10-part-2`

**GATE STATUS**: ✅ **ALL CLEAR** - Proceed to Phase 0 Research

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
day-10/
├── solution.py              # Part 1 implementation (existing)
├── solution_part2.py        # Part 2 implementation (NEW)
├── test_solution.py         # Part 1 tests (existing)
├── test_solution_part2.py   # Part 2 tests (NEW)
├── input.txt                # Actual puzzle input (existing)
├── test_input.txt           # Example machines (existing)
├── description.md           # Problem description (existing)
└── README.md                # Notes and explanations (optional)
```

**Structure Decision**: Day 10 follows Advent of Code standard structure with separate files for each part. Part 2 extends Part 1 by reusing parsing logic while implementing new solver algorithm for integer linear programming. All code resides in `day-10/` folder per Constitution Principle II.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**Status**: No violations identified. All constitution principles are satisfied.

---

## Post-Design Constitution Re-Check

_Re-evaluated after Phase 1 design completion_

### Principle I: Clean Python Code

✅ **PASS** - Design uses type hints, NumPy idioms, modular functions with docstrings

### Principle II: Structured Organization

✅ **PASS** - Files organized in `day-10/` folder, clear separation between Part 1 and Part 2

### Principle III: Function-Based Solutions

✅ **PASS** - Core API defined: `solve_part2()`, `solve_integer_linear_system()`, `build_button_matrix()`

### Principle IV: Test-Driven Development (NON-NEGOTIABLE)

✅ **PASS** - Quickstart explicitly enforces RED-GREEN-REFACTOR: write tests first, verify failures, implement

### Principle V: Automation First

✅ **PASS** - Reuses existing meta runner, no new automation needed

### Principle VI: AoC Compliance & Rate Limiting

✅ **PASS** - Manual submission only, no network interactions

### Principle VII: Documentation & Progress Tracking

✅ **PASS** - Documentation artifacts generated (research, data-model, contracts, quickstart)

### Principle VIII: Specification-Driven Workflow

✅ **PASS** - Full workflow executed: spec.md → plan.md (with research, data-model, contracts, quickstart)

### Principle IX: Delightful CLI

✅ **PASS** - Uses `uv run` commands throughout quickstart

### Code Structure Requirements

✅ **PASS** - UV runtime, dependency management verified, Git branch `021-day-10-part-2`

**FINAL GATE STATUS**: ✅ **ALL CLEAR** - Proceed to Phase 2 (Task Generation with `/speckit.tasks` command)

---

## Implementation Readiness

### Ready for Development

- ✅ Technical unknowns resolved (research.md)
- ✅ Data model defined (data-model.md)
- ✅ API contracts specified (contracts/solver-api.md)
- ✅ Implementation guide provided (quickstart.md)
- ✅ Agent context updated for Copilot assistance

### Next Steps

1. Run `/speckit.tasks` command to generate task breakdown from this plan
2. Execute tasks in TDD order (RED → GREEN → REFACTOR)
3. Solve actual puzzle and submit answer manually
4. Update progress tracker in README.md

| Violation                  | Why Needed         | Simpler Alternative Rejected Because |
| -------------------------- | ------------------ | ------------------------------------ |
| [e.g., 4th project]        | [current need]     | [why 3 projects insufficient]        |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient]  |
