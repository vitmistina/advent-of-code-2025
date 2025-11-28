<!--
SYNC IMPACT REPORT
==================
Version Change: 1.1.0 → 1.2.0
Modified Principles:
  - Principle V: "Automation First" - Clarified meta runner role (downloads only)
  - NEW Principle VII: "Specification-Driven Workflow" - Added Specify framework integration
Added Sections:
  - Specify Framework Workflow (detailed spec → tasks process)
  - Updated Workflow Order with explicit Specify commands
Removed Sections: None

Templates Status:
  ✅ plan-template.md - Reviewed, aligns with new workflow (Advent of Code doesn't use plan phase)
  ✅ spec-template.md - Reviewed, user stories map to puzzle parts
  ✅ tasks-template.md - Reviewed, TDD pattern enforced in task generation
  ⚠️ No commands directory - not applicable

Follow-up TODOs:
  - Create README.md at project root with progress tracker (Principle VI requirement)
  - Create meta runner script (Principle V requirement)
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

- Downloading task descriptions from Advent of Code website
- Downloading `input.txt` (if not present)
- Generating `test_input.txt` from task description examples (with support for multiple test input files for different parts)
- Running solutions against inputs
- Validating answers against the Advent of Code website

Session tokens MUST be stored in a `.env` file for authentication.

**Rationale**: Automation reduces manual steps, prevents errors from copy-paste mistakes, and allows focus on problem-solving. The meta runner handles external integration only; solution planning and task generation are handled by the Specify framework (see Principle VII).

### VI. Documentation & Progress Tracking

The main `README.md` MUST be kept current with:

- Progress tracker showing which days are solved
- Special notes or learnings from challenges

**Rationale**: Documentation captures insights and patterns discovered during problem-solving, provides motivation through visible progress, and helps identify knowledge gaps.

### VII. Specification-Driven Workflow

**Specify framework MUST be used to convert challenge descriptions into executable tasks**:

1. **Spec Phase** (`specify` command): Transform raw challenge description into structured specification with:
   - User stories (Part 1 = P1, Part 2 = P2)
   - Acceptance criteria from puzzle examples
   - Edge cases and requirements
2. **Tasks Phase** (`tasks` command): Generate TDD task list from spec:
   - Tasks organized by user story (Part 1 tasks, Part 2 tasks)
   - RED tasks (write tests first)
   - GREEN tasks (implement solution)
   - REFACTOR tasks (optimize/clean)

**The planning phase is SKIPPED** for Advent of Code since:

- No complex architecture needed
- Structure is predefined (Principle II)
- Technical context is constant (Python 3.10+, pytest)

**Rationale**: Specify framework ensures systematic breakdown of puzzle requirements into testable increments. The spec → tasks flow enforces TDD discipline by making test-first workflow explicit in the task list. Skipping the plan phase keeps overhead minimal for time-sensitive competition.

## Code Structure Requirements

**Project Root**: Contains the meta runner script and main `README.md`

**Day Folders**: `day-XX/` structure as defined in Principle II

**Dependency Management**: UV MUST be used for Python package management

**Version Control**: Git MUST be used; commits pushed directly to main branch are permitted for this project

**Specify Framework Integration**:

- Specifications stored in `specs/day-XX/spec.md`
- Tasks stored in `specs/day-XX/tasks.md`
- Plan phase skipped (not applicable for Advent of Code)
- Constitution check automated via Specify templates

**Workflow Order** (TDD-enforced):

1. Run meta runner to download challenge description and inputs

   - Downloads task from Advent of Code website
   - Creates `day-XX/` folder
   - Downloads `input.txt`
   - Generates `test_input.txt` from puzzle examples

2. **SPEC**: Run `specify` command to create structured specification
   - Input: Raw challenge description
   - Output: `specs/day-XX/spec.md` with:
     - User Story 1 (Part 1) with acceptance criteria
     - User Story 2 (Part 2) with acceptance criteria
     - Edge cases and requirements
3. **TASKS**: Run `tasks` command to generate TDD task breakdown

   - Input: `specs/day-XX/spec.md`
   - Output: `specs/day-XX/tasks.md` with:
     - Part 1 tasks (RED → GREEN → REFACTOR)
     - Part 2 tasks (RED → GREEN → REFACTOR)
     - Tasks explicitly ordered for TDD workflow

4. Execute tasks in order from `tasks.md`:

   - **RED**: Write test cases in `day-XX/test_solution.py` - verify tests FAIL
   - **GREEN**: Implement solution functions in `day-XX/solution.py` to make tests pass
   - **REFACTOR**: Clean up code while maintaining green tests

5. Run solution against actual input using meta runner

6. Submit answer via meta runner automated validation

7. Commit with clear message (e.g., `feat: solve day XX part 1` or `feat: solve day XX complete`)

8. Update progress tracker in main `README.md`

**No Pull Requests Required**: Direct commits to main are acceptable given the solo, time-sensitive nature of Advent of Code challenges.

**No Code Review Gates**: Speed is prioritized during the competition period; refactoring and cleanup may occur after initial solutions.

## Governance

**Complexity Justification**: If a solution requires deviation from these principles (e.g., skipping TDD for extreme time pressure), the reason MUST be documented in the day's `README.md`. Note: Principle IV (TDD) is marked NON-NEGOTIABLE and deviations should be exceptional.

**Enforcement**: Pre-commit hooks MAY be used to enforce linting (Ruff) and test execution. Manual validation is acceptable during active competition. TDD compliance is enforced through workflow discipline.

**Amendment Process**: Constitution updates follow semantic versioning. MINOR version bumps (e.g., adding workflow clarifications) require validation across all Specify templates for consistency.

**Version**: 1.2.0 | **Ratified**: 2025-11-28 | **Last Amended**: 2025-11-28
