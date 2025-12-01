# Implementation Plan: Day 1 Part 1 - Secret Entrance

**Branch**: `004-day-01-part-1` | **Date**: 2025-12-01 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/004-day-01-part-1/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement a solution to count the number of times a circular dial (numbered 0-99) points at position 0 after applying a sequence of rotation instructions. The dial starts at position 50 and rotations are specified as direction (L/R) and distance. Technical approach uses simple modular arithmetic for circular wrapping and iterative processing of rotation instructions.

## Technical Context

**Language/Version**: Python 3.10+  
**Primary Dependencies**: pytest (dev), no runtime dependencies beyond stdlib  
**Storage**: File-based input (input.txt, test_input.txt)  
**Testing**: pytest with TDD approach (RED-GREEN-REFACTOR)  
**Target Platform**: Cross-platform Python (Windows/Linux/macOS)
**Project Type**: Single script solution (Advent of Code daily challenge)  
**Performance Goals**: Process 10,000+ rotations in under 2 seconds  
**Constraints**: Must handle circular wraparound correctly (0-99), must validate input format  
**Scale/Scope**: Single-day puzzle, ~100-200 lines of code, 12+ test cases

## Constitution Check

_GATE: Must pass before Phase 0 research. Re-check after Phase 1 design._

### ✅ Principle I: Clean Python Code

- **Status**: PASS
- **Evidence**: Using Python 3.10+, PEP8 via Ruff, type hints in function signatures

### ✅ Principle II: Structured Organization

- **Status**: PASS
- **Evidence**: day-01/ folder exists with solution.py, input.txt, test_input.txt, test_solution.py

### ✅ Principle III: Function-Based Solutions

- **Status**: PASS
- **Evidence**: Separate functions planned: parse_input(), solve_part1(), apply_rotation()

### ✅ Principle IV: Test-Driven Development (NON-NEGOTIABLE)

- **Status**: PASS
- **Evidence**: TDD workflow enforced via tasks.md (to be generated in Phase 2)
- **Note**: RED-GREEN-REFACTOR cycle will be explicit in task breakdown

### ✅ Principle V: Automation First

- **Status**: PASS
- **Evidence**: Meta runner already downloaded input.txt and test_input.txt, CLI ready for submission

### ✅ Principle VI: AoC Compliance & Rate Limiting

- **Status**: PASS
- **Evidence**: Manual submission only, no auto-submit, session token in .env

### ✅ Principle VII: Documentation & Progress Tracking

- **Status**: PASS
- **Evidence**: README.md will be updated after solution complete

### ✅ Principle VIII: Specification-Driven Workflow

- **Status**: PASS
- **Evidence**: spec.md created, plan.md (this file) in progress, tasks.md will follow

### ✅ Principle IX: Delightful CLI

- **Status**: PASS
- **Evidence**: Meta runner CLI already provides friendly UX with progress indicators

**GATE RESULT**: ✅ ALL CHECKS PASS - Proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/004-day-01-part-1/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
│   └── api-contract.md  # Function signatures and data structures
├── checklists/          # Already exists
│   └── requirements.md
└── spec.md              # Already exists
```

### Source Code (repository root)

```text
day-01/
├── solution.py          # Main solution (already scaffolded)
├── input.txt            # Actual puzzle input (already downloaded)
├── test_input.txt       # Sample input from puzzle (already created)
├── test_solution.py     # Tests (already scaffolded)
├── description.md       # Puzzle description (already downloaded)
└── README.md            # Optional notes (created if needed)

tests/                   # Root-level tests (not used for day solutions)
cli/                     # Meta runner (already exists)
```

**Structure Decision**: Using standard Advent of Code structure per Constitution Principle II. Day-01 folder is already created and scaffolded by meta runner. All source code resides in day-01/ with tests co-located.

## Complexity Tracking

**No violations to justify** - This implementation follows all Constitution principles without exceptions.

## Phase 0: Research & Discovery

### Research Tasks

1. **Circular Dial Arithmetic**

   - **Question**: How to implement circular wraparound for 0-99 range?
   - **Answer**: Use modulo 100 arithmetic. For left rotation: `(position - distance) % 100`. For right rotation: `(position + distance) % 100`. Python's modulo handles negatives correctly.
   - **Rationale**: Modulo provides clean, efficient circular arithmetic without conditional logic.

2. **Input Parsing Patterns**

   - **Question**: What's the most Pythonic way to parse "L68" style rotation instructions?
   - **Answer**: Use regex `r'^([LR])(\d+)$'` or simple string slicing: `direction = line[0]`, `distance = int(line[1:])`.
   - **Rationale**: String slicing is clearer and faster for this simple format. Regex adds unnecessary complexity.

3. **Performance Optimization**

   - **Question**: Can we optimize the rotation loop for 10,000+ instructions?
   - **Answer**: Not needed - O(n) iteration with O(1) modulo operations is already optimal. Early optimization would violate TDD.
   - **Rationale**: Premature optimization is unnecessary. Simple implementation will easily meet <2s requirement.

4. **Edge Case Handling**
   - **Question**: How should we handle empty lines, invalid directions, or non-numeric distances?
   - **Answer**:
     - Empty lines: Filter out during parsing (`if line.strip()`)
     - Invalid direction: Raise ValueError with clear message
     - Non-numeric: Raise ValueError with clear message
   - **Rationale**: Fail-fast with informative errors supports debugging and meets FR-004.

### Technology Choices

| Technology | Choice                | Rationale                            | Alternatives Considered                       |
| ---------- | --------------------- | ------------------------------------ | --------------------------------------------- |
| Language   | Python 3.10+          | Required by Constitution             | N/A                                           |
| Testing    | pytest                | Constitution standard, good fixtures | unittest (too verbose)                        |
| Parsing    | String slicing        | Simple, fast, clear                  | regex (overkill), split() (less safe)         |
| Validation | ValueError exceptions | Pythonic, clear error messages       | Return None (unclear), logging (insufficient) |

### Design Decisions

1. **Function Decomposition**:

   - `parse_input(text: str) -> list[tuple[str, int]]`: Parse rotation instructions
   - `apply_rotation(position: int, direction: str, distance: int) -> int`: Apply one rotation
   - `solve_part1(rotations: list[tuple[str, int]]) -> int`: Count zeros after rotations

2. **Data Representation**:

   - Rotation: `tuple[str, int]` where first element is 'L' or 'R', second is distance
   - Dial position: `int` (0-99)
   - Zero count: `int`

3. **Error Handling Strategy**:
   - Parsing errors raise `ValueError` with descriptive message
   - Invalid positions or operations raise `ValueError`
   - Empty input returns empty list (not an error)

## Phase 1: Design & Contracts

**Status**: ✅ COMPLETE

### Data Model

See [data-model.md](data-model.md) for complete entity definitions.

**Key Entities**:

- **Rotation**: Direction (L/R) + Distance (int >= 0)
- **DialState**: Current position (0-99) + zero count (int >= 0)
- **ParsedInput**: List of rotation tuples

**Data Representation**:

```python
Rotation = tuple[str, int]  # ('L', 68)
Position = int  # 0-99
ParsedInput = list[Rotation]
```

### API Contracts

See [contracts/api-contract.md](contracts/api-contract.md) for complete function signatures.

**Core Functions**:

```python
def parse_input(input_text: str) -> list[tuple[str, int]]:
    """Parse rotation instructions from puzzle input."""

def apply_rotation(position: int, direction: str, distance: int) -> int:
    """Apply a single rotation to the dial and return new position."""

def solve_part1(rotations: list[tuple[str, int]]) -> int:
    """Count how many times dial points at 0 after rotations."""
```

### Quickstart

See [quickstart.md](quickstart.md) for developer onboarding and TDD workflow.

**Quick Start Commands**:

```bash
# Write tests first (RED)
code day-01/test_solution.py

# Run tests (should fail initially)
uv run pytest day-01/test_solution.py -v

# Implement solution (GREEN)
code day-01/solution.py

# Run tests (should pass)
uv run pytest day-01/test_solution.py -v

# Refactor and lint
uv run ruff format day-01/
```

### Agent Context Update

✅ **Completed**: Agent context updated with current technology stack

- Command run: `.specify/scripts/powershell/update-agent-context.ps1 -AgentType copilot`
- Updated: `.github/agents/copilot-instructions.md`
- Added: Python 3.10+, pytest, file-based input

### Constitution Re-Check (Post-Design)

**Re-evaluating all principles after Phase 1 design...**

✅ **All principles still PASS** - No violations introduced during design phase.

**Design validates**:

- Clean Python with type hints and docstrings (Principle I)
- Function-based solution with clear separation (Principle III)
- TDD workflow explicit in quickstart (Principle IV)
- Contracts and data model support all FRs (Principles II, VIII)

## Phase 2: Task Breakdown

**Status**: ⏳ PENDING - Not part of /speckit.plan command

**Next Command**: Run separately after plan approval

```bash
uv run -m cli.meta_runner tasks --feature 004-day-01-part-1
```

**Expected Output**: `specs/004-day-01-part-1/tasks.md` with:

- RED tasks: Write failing tests for each function
- GREEN tasks: Implement functions to pass tests
- REFACTOR tasks: Clean up and optimize code

**Task Structure** (will be generated):

```
User Story 1: Count Zero Positions (P1)
├── RED-1.1: Write test for parse_input with sample
├── RED-1.2: Write test for apply_rotation left/right
├── RED-1.3: Write test for solve_part1 with sample
├── GREEN-1.1: Implement parse_input
├── GREEN-1.2: Implement apply_rotation
├── GREEN-1.3: Implement solve_part1
└── REFACTOR-1.1: Clean up and add type hints
```

## Implementation Notes

**Current Status**: Plan complete, ready for task generation

**Part 1 Focus**:

- Implement only Part 1 (count zeros during rotation sequence)
- Part 2 will be revealed after Part 1 submission
- Expected completion: 1-2 hours with TDD approach

**Key Implementation Points**:

1. Start with tests (TDD RED phase)
2. Implement minimal code to pass (GREEN phase)
3. Refactor while keeping tests green (REFACTOR phase)
4. Verify with sample input (should return 3)
5. Run on actual input and submit manually

## Post-Implementation Checklist

After implementation complete:

1. ✅ All tests pass: `uv run pytest day-01/test_solution.py -v`
2. ✅ Linting passes: `uv run ruff check day-01/`
3. ✅ Test input returns expected result (3)
4. ✅ Run solution: `uv run day-01/solution.py`
5. ✅ Submit answer manually to Advent of Code website
6. ✅ Update main README.md progress tracker
7. ✅ Commit: `git commit -m "feat: solve day 01 part 1"`
8. ✅ Push to GitHub: `git push origin 004-day-01-part-1`
9. ⏳ Wait for Part 2 to unlock
10. ⏳ Repeat process for Part 2

## Summary

**Plan Status**: ✅ COMPLETE (Phases 0 and 1)

**Artifacts Generated**:

- ✅ `plan.md` (this file)
- ✅ `research.md` (all unknowns resolved)
- ✅ `data-model.md` (entities and relationships)
- ✅ `contracts/api-contract.md` (function signatures)
- ✅ `quickstart.md` (developer onboarding)
- ✅ Agent context updated

**Next Action**: Generate tasks.md via `/speckit.tasks` command (separate from this plan)

**Branch**: `004-day-01-part-1`  
**Ready for**: Task generation and TDD implementation
