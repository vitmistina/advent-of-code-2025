# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

**Primary Requirement**: Find the largest rectangle in a grid using two red tiles as opposite corners, based on coordinates parsed from input.

**Technical Approach**: Parse input file for red tile coordinates in "x,y" format, store as tuples in a list, and use itertools.combinations to evaluate all distinct pairs. For each pair, calculate area as |x1-x2| × |y1-y2|, track the maximum area found, and return it. Halt and raise error on malformed or empty input. Use pytest for test files and inline asserts for quick checks. Follow PEP8, ruff, and AoC repo standards.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.10+
**Primary Dependencies**: None (standard library), uv, ruff, pytest
**Storage**: Files (input.txt, test_input.txt)
**Testing**: pytest, assert
**Target Platform**: Local (Windows, Linux, Mac)
**Project Type**: Single (day-09/)
**Performance Goals**: <5s for full input
**Constraints**: UV used as runner, PEP8, ruff, <200ms p95 (implied), <100MB memory (implied)
**Scale/Scope**: 1 puzzle/day, 8-1000 tiles typical

## Constitution Check

_GATE: Must pass before Phase 0 research. Re-check after Phase 1 design._

- Must use Python 3.10+ features
- Must use uv as runner
- Must follow PEP8 style guide
- Must use ruff for linting
- Must use pytest or assert for tests
- Must include docstrings for all functions and modules
- Must separate solution and test files
- Must use Git for version control
- Must use uv for dependencies
- Must use clear, conventional commit messages
- Must update README progress tracker

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

<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
# [REMOVE IF UNUSED] Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [REMOVE IF UNUSED] Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [REMOVE IF UNUSED] Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure: feature modules, UI flows, platform tests]
```

**Structure Decision**: [Document the selected structure and reference the real

Use the standard AoC day folder structure:

```text
day-09/
├── solution.py
├── test_solution.py
├── input.txt
├── test_input.txt
├── README.md
```

This matches the repo's constitution and supports clean separation of solution, tests, and inputs.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation                  | Why Needed         | Simpler Alternative Rejected Because |
| -------------------------- | ------------------ | ------------------------------------ |
| [e.g., 4th project]        | [current need]     | [why 3 projects insufficient]        |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient]  |
