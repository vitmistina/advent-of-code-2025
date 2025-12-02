# Implementation Plan: Day 2 Part 2 - Invalid Product ID Detection (Extended Pattern)

**Branch**: `008-day-02-part-2` | **Date**: December 2, 2025 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/008-day-02-part-2/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Extend the Day 2 Part 1 solution to detect invalid product IDs using updated pattern rules. Part 2 identifies IDs where any digit sequence is repeated at least twice (vs exactly twice in Part 1). Examples include "111" (1×3), "565656" (56×3), "824824824" (824×3), and "2121212121" (21×5). The solution must identify all invalid IDs across ranges and sum them to produce 4174379265 for the example input.

## Technical Context

**Language/Version**: Python 3.10+  
**Primary Dependencies**: None (stdlib only, following AoC Constitution)  
**Storage**: File-based input (`day-02/input.txt`, `day-02/test_input.txt`)  
**Testing**: pytest with test-driven development (RED-GREEN-REFACTOR cycle)  
**Target Platform**: Local execution via `uv run`  
**Project Type**: Single script solution (Advent of Code day structure)  
**Performance Goals**: Process actual puzzle input in under 10 seconds  
**Constraints**: Must handle ranges efficiently; O(n) pattern checking where n = digit count  
**Scale/Scope**: Day 2 Part 2 - extends existing Part 1 solution

## Constitution Check

_GATE: Must pass before Phase 0 research. Re-check after Phase 1 design._

### ✅ Principle I: Clean Python Code

- Using Python 3.10+ with type hints
- Following PEP8 via Ruff linting
- Prioritizing readability with clear pattern-matching logic

### ✅ Principle II: Structured Organization

- Solution in existing `day-02/` folder
- Updates: `solution.py` (add `solve_part2()`), `test_solution.py` (add Part 2 tests)
- Spec in `specs/008-day-02-part-2/`

### ✅ Principle III: Function-Based Solutions

- Implements `solve_part2(input_data)` function
- Extends `is_invalid_id()` with optional `part` parameter or creates `is_invalid_id_part2()`
- All functions include docstrings
- Clear separation of pattern detection logic

### ✅ Principle IV: Test-Driven Development (NON-NEGOTIABLE)

- **RED**: Write Part 2 tests first using puzzle examples (11-22 → [11, 22], 95-115 → [99, 111], etc.)
- **GREEN**: Implement minimum code to pass Part 2 tests
- **REFACTOR**: Clean up while maintaining both Part 1 and Part 2 tests green
- Tests in existing `day-02/test_solution.py`

### ✅ Principle V: Automation First

- Input already downloaded (reuses `day-02/input.txt`)
- Test input examples documented in spec
- Manual submission after local execution

### ✅ Principle VI: AoC Compliance

- No automated submissions
- Respects rate limits (no new downloads needed)
- Session token in `.env`

### ✅ Principle VII: Documentation & Progress

- README.md will be updated with Part 2 completion
- Spec documents updated pattern rules and all 12 test scenarios

### ✅ Principle VIII: Specification-Driven Workflow

- Spec created from Part 2 challenge description
- Tasks will be generated from spec
- TDD workflow enforced (Part 1 tests remain green)

### ✅ Principle IX: Delightful CLI

- Meta runner provides clear output
- Uses `uv run` for execution

**GATE STATUS**: ✅ PASSED - All constitutional requirements met

### Post-Design Re-evaluation

_Re-checked after Phase 1 (Design & Contracts) completion_

**Design Artifacts Reviewed**:

- ✅ research.md - Algorithm decisions documented (divisor-based pattern matching, O(n²) complexity)
- ✅ data-model.md - Entity model extends Part 1 with PatternMatch entity
- ✅ contracts/api-contract.md - Function signatures defined for Part 2 (`solve_part2`, `is_invalid_id_part2`, `check_range_part2`)
- ✅ quickstart.md - TDD workflow guide created with RED-GREEN-REFACTOR phases

**Constitutional Compliance Verification**:

- ✅ No additional dependencies introduced (stdlib only, divisor iteration uses built-in range)
- ✅ File structure matches Principle II (extends day-02/ folder, no new directories)
- ✅ Function-based design maintained (3 new functions, Part 1 functions preserved)
- ✅ TDD workflow documented in quickstart (strict RED→GREEN→REFACTOR→VERIFY cycle)
- ✅ No complexity violations introduced (simple algorithm, no external libs, no architectural patterns)

**Design Decisions Validated**:

1. **Pattern Detection Algorithm**: Divisor-based string matching chosen

   - Justification: Clear, efficient enough for AoC constraints (O(n²) acceptable)
   - Alternative regex rejected for readability

2. **Backward Compatibility**: Part 1 functions remain unchanged

   - Justification: Separate `_part2` suffixed functions prevent breaking changes
   - Part 1 tests continue to pass without modification

3. **Code Reuse**: `parse_input()` reused from Part 1

   - Justification: Same input format, no changes needed
   - Reduces duplication and testing burden

4. **Test Organization**: Separate test functions for Part 1 and Part 2
   - Justification: Clear separation, easy to verify no regressions
   - Shared test data where applicable (EXAMPLE_INPUT)

**Final Status**: ✅ ALL GATES PASSED - Ready for Phase 2 (Tasks)

## Project Structure

### Documentation (this feature)

```text
specs/008-day-02-part-2/
├── spec.md              # Feature specification (COMPLETED)
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output - algorithm research
├── data-model.md        # Phase 1 output - entities and relationships
├── quickstart.md        # Phase 1 output - developer onboarding
├── checklists/
│   └── requirements.md  # Spec validation checklist (COMPLETED)
├── contracts/           # Phase 1 output - API contracts
│   └── api-contract.md
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
day-02/
├── solution.py          # EXTENDS: Add solve_part2() and updated pattern detection
├── test_solution.py     # EXTENDS: Add Part 2 test cases (11 new scenarios)
├── input.txt            # UNCHANGED: Reuse existing puzzle input
├── test_input.txt       # UNCHANGED: Part 1 examples (Part 2 uses same ranges)
├── description.md       # EXISTS: Contains both Part 1 and Part 2 descriptions
└── README.md            # UPDATE: Document Part 2 completion and approach

cli/
├── meta_runner.py       # UNCHANGED: No changes needed
└── ...

specs/008-day-02-part-2/ # This spec and planning artifacts
```

**Structure Decision**: Extending the existing Day 2 solution following Principle II. Part 2 adds new functions to `solution.py` and new test cases to `test_solution.py`. All Part 1 functionality and tests remain intact. No new files required beyond spec documentation - implements the established Advent of Code pattern where both parts coexist in the same day folder.

## Complexity Tracking

> No constitutional violations - all gates passed. This section is empty per template instructions.

---

## Phase 0: Research & Analysis

### Research Questions

1. **Pattern Detection Algorithm**: How to efficiently check if a number is composed of a repeated digit sequence (at least twice)?

   - Must handle all divisor lengths (1, 2, 3, ... n/2 where n = digit count)
   - Example: "222222" could be "2"×6, "22"×3, or "222"×2
   - Need O(n) or better solution where n = number of digits

2. **Algorithm Optimization**: What's the most efficient approach for checking large ranges?

   - Part 1 used string-based pattern matching
   - Can Part 2 reuse or extend Part 1 logic?
   - Consider: iterate through divisors of string length, check if pattern repeats

3. **Edge Cases**: What special cases need handling?

   - Single digit numbers (always valid in Part 2, like Part 1)
   - Numbers where multiple divisors work (any match makes it invalid)
   - Relationship to Part 1 (Part 2 is superset - includes all Part 1 invalids plus more)

4. **Test Strategy**: How to structure tests for backward compatibility?
   - Part 1 tests must remain green
   - Part 2 tests verify extended pattern detection
   - Shared test helpers vs separate test functions?

### Research Output

_Will be documented in `research.md` with decisions, rationale, and alternatives considered_

---

## Phase 1: Design & Contracts

### Data Model

_Will be documented in `data-model.md` - extends Part 1 model_

**Expected Entities**:

- **IDRange**: Same as Part 1 (start, end integers)
- **ProductID**: Same as Part 1 (integer value, validation state)
- **PatternMatch**: NEW - represents a digit sequence and its repetition count
- **ValidationRule**: Abstraction for Part 1 (exactly twice) vs Part 2 (at least twice)

### API Contracts

_Will be documented in `contracts/api-contract.md`_

**Expected Functions**:

- `solve_part2(input_data: str) -> int` - Main entry point for Part 2
- `is_invalid_id_part2(num: int) -> bool` - Pattern detection with "at least twice" rule
- `find_repeated_pattern(s: str) -> Optional[str]` - Helper to detect any repeated pattern
- Reuse from Part 1: `parse_input()`, `check_range()`

### Quickstart Guide

_Will be documented in `quickstart.md`_

**Expected Content**:

- Setup: Verify Part 1 tests still pass
- TDD Workflow for Part 2:
  - RED: Write test for "111" detection (1×3), verify failure
  - GREEN: Implement pattern divisor iteration
  - Test additional scenarios: "565656", "824824824", "2121212121"
  - REFACTOR: Optimize and clean
- Run Part 2: `uv run day-02/solution.py --part 2`
- Verify: Sum should be 4174379265 for example input

---

## Phase 2: Task Breakdown

_Will be generated by `/speckit.tasks` command - NOT created by `/speckit.plan`_

**Expected Task Categories**:

1. **Phase 0 Research Tasks**: Algorithm investigation, decision documentation
2. **Phase 1 Design Tasks**: Data model, contracts, quickstart creation
3. **RED Tasks**: Write failing Part 2 tests (11 scenarios from spec)
4. **GREEN Tasks**: Implement Part 2 solution to pass tests
5. **REFACTOR Tasks**: Optimize pattern detection, clean up code
6. **Integration Tasks**: Verify Part 1 tests still pass, update README

---

## Success Criteria

From spec.md Success Criteria section:

- **SC-001**: System correctly identifies all 13 invalid IDs from example ranges
- **SC-002**: System produces exact sum of 4174379265 for complete example input
- **SC-003**: System processes all 11 ranges in example input
- **SC-004**: Part 1 tests remain green (backward compatibility verified)
