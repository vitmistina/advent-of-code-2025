# Data Model: Meta Runner & CLI (AoC 2025)

## Entities

### Day

- number: int (1–25)
- folder: string (`day-XX/`)
- files:
  - solutionPath: `day-XX/solution.py`
  - testPath: `day-XX/test_solution.py`
  - inputPath: `day-XX/input.txt`
  - testInputPath: `day-XX/test_input.txt`
- specPath: `specs/day-XX/spec.md`
- tasksPath: `specs/day-XX/tasks.md`

Validation:

- `1 <= number <= 25`
- folder exists after scaffold
- required files created; overwrite only with confirmation

### MetaRunResult

- downloaded: boolean
- createdFiles: list<string>
- specPath: string
- tasksPath: string
- messages: list<string>

State Transitions:

- INIT → SCAFFOLDED → DOWNLOADED → SPEC_GENERATED → TASKS_GENERATED → READY_FOR_TDD
- On errors: remain in last successful state; provide guidance

## Relationships

- Day 1:N Meta actions (scaffold, download, spec, tasks)
- MetaRunResult references Day paths

## Rules

- Enforce TDD flow messaging (RED→GREEN→REFACTOR)
- AoC compliance: never auto-submit; show manual steps
- Dry-run bypasses network, still scaffolds and generates placeholders
