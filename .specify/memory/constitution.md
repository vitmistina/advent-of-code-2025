<!--
SYNC IMPACT REPORT
==================
Version Change: 1.0.0 → 1.1.0
Modified Principles:
  - Principle IV: "Testing Required" → "Test-Driven Development (NON-NEGOTIABLE)"
    - Added mandatory Red-Green-Refactor cycle
    - Tests MUST be written BEFORE implementation
    - Tests MUST fail before implementation begins
Added Sections: None
Removed Sections: None

Templates Status:
  ✅ plan-template.md - Reviewed, no updates needed (constitution check placeholder intact)
  ✅ spec-template.md - Reviewed, aligns with TDD requirements
  ✅ tasks-template.md - Reviewed, already includes "Tests written → User approved → Tests fail → Then implement" pattern
  ⚠️ No commands directory found - skipped

Follow-up TODOs: None
-->

# Advent of Code 2025 Constitution

## Core Principles

### I. Clean Python Code

All solutions MUST use Python 3.10+ features where appropriate and strictly follow PEP8 style guide. Code MUST prioritize readability and efficiency. Ruff MUST be used for linting and formatting.

**Rationale**: Advent of Code is an opportunity to practice clean code principles in a time-constrained environment. Using modern Python features and consistent style makes solutions easier to review, learn from, and maintain.

### II. Structured Organization

Each day's challenge MUST reside in its own folder named `day-XX/` (e.g., `day-01/`). Each folder MUST contain:

- `solution.py` — main solution script
- `input.txt` — puzzle input
- `test_input.txt` — sample input for testing
- `test_input_N.txt` — (optional) additional sample inputs for different parts, where N is a numeric ID
- `README.md` — (optional) notes or explanations

**Rationale**: Consistent structure enables quick navigation, reduces cognitive load when switching between days, and ensures all necessary files are co-located for each challenge.

### III. Function-Based Solutions

Every solution MUST implement separate functions for each part (e.g., `solve_part1(input_data)`, `solve_part2(input_data)`). All functions and modules MUST include docstrings.

**Rationale**: Function-based design enforces separation of concerns, makes testing straightforward, and provides clear entry points for each puzzle part.

### IV. Test-Driven Development (NON-NEGOTIABLE)

**Red-Green-Refactor cycle MUST be strictly enforced**:

1. **RED**: Write tests FIRST based on puzzle examples - tests MUST fail initially
2. **GREEN**: Implement minimum code to make tests pass
3. **REFACTOR**: Clean up code while keeping tests green

Each solution MUST include at least one test per part using pytest or simple assert statements. Test files MUST be named `test_solution.py` and placed in the same folder as the solution. Tests MUST be written and verified to fail BEFORE any solution implementation begins.

**Rationale**: TDD ensures solutions are testable from the start, prevents over-engineering, and provides immediate feedback. The Red-Green-Refactor cycle enforces discipline in a time-pressured environment and ensures test validity - a passing test that was never seen failing cannot be trusted.

### V. Automation First

A meta runner script at the root level MUST handle:

- Downloading task descriptions
- Downloading `input.txt` (if not present)
- Providing prompt templates to parse task descriptions into `test_input.txt` (with support for multiple test input files for different parts)
- Running solutions
- Validating answers against the Advent of Code website

Session tokens MUST be stored in a `.env` file for authentication.

**Rationale**: Automation reduces manual steps, prevents errors from copy-paste mistakes, and allows focus on problem-solving rather than infrastructure.

### VI. Documentation & Progress Tracking

The main `README.md` MUST be kept current with:

- Progress tracker showing which days are solved
- Special notes or learnings from challenges

**Rationale**: Documentation captures insights and patterns discovered during problem-solving, provides motivation through visible progress, and helps identify knowledge gaps.

## Code Structure Requirements

**Project Root**: Contains the meta runner script and main `README.md`

**Day Folders**: `day-XX/` structure as defined in Principle II

**Dependency Management**: UV MUST be used for Python package management

**Version Control**: Git MUST be used; commits pushed directly to main branch are permitted for this project
**Workflow Order** (TDD-enforced):

1. Run meta runner to download task and generate test inputs (might need user to run a prompt template to parse the day's task)
2. **RED**: Write test cases using sample inputs - verify tests FAIL
3. **GREEN**: Implement solution functions to make tests pass
4. **REFACTOR**: Clean up code while maintaining green tests
5. Run solution against actual input
6. Submit via automated validation
7. Commit with clear message
8. Update progress trackertions
9. Validate against tests
10. Run solution against actual input
11. Submit via automated validation
12. Commit with clear message
13. Update progress tracker

**No Pull Requests Required**: Direct commits to main are acceptable given the solo, time-sensitive nature of Advent of Code challenges.

**No Code Review Gates**: Speed is prioritized during the competition period; refactoring and cleanup may occur after initial solutions.

## Governance

**Complexity Justification**: If a solution requires deviation from these principles (e.g., skipping TDD for extreme time pressure), the reason MUST be documented in the day's `README.md`. Note: Principle IV (TDD) is marked NON-NEGOTIABLE and deviations should be exceptional.

**Enforcement**: Pre-commit hooks MAY be used to enforce linting (Ruff) and test execution. Manual validation is acceptable during active competition. TDD compliance is enforced through workflow discipline.

**Version**: 1.1.0 | **Ratified**: 2025-11-28 | **Last Amended**: 2025-11-28
**Complexity Justification**: If a solution requires deviation from these principles (e.g., skipping tests for extreme time pressure), the reason MUST be documented in the day's `README.md`.

**Enforcement**: Pre-commit hooks MAY be used to enforce linting (Ruff) and test execution. Manual validation is acceptable during active competition.

**Version**: 1.0.0 | **Ratified**: 2025-11-28 | **Last Amended**: 2025-11-28
