# Implementation Plan: Day 5 Part 1 - Fresh Ingredient ID Validation

**Branch**: `012-day-05-part-1` | **Date**: December 5, 2025 | **Spec**: specs/012-day-05-part-1/spec.md
**Input**: Feature specification from `/specs/012-day-05-part-1/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Determine how many available ingredient IDs are fresh by parsing inclusive ID ranges, merging them into disjoint intervals, and scanning the available IDs with a two-pointer sweep to keep runtime near `O(R log R + I log I)` for Day 5 Part 1.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.10+ (uv-managed virtual environment)  
**Primary Dependencies**: Standard library (pathlib, typing), pytest for local tests, uv tooling; no third-party runtime deps needed  
**Storage**: Local filesystem inputs (`day-05/input.txt`, `day-05/test_input.txt`)  
**Testing**: pytest and direct function-level asserts in `day-05/test_solution.py` executed via `uv run pytest`  
**Target Platform**: Local CLI environment (Windows/macOS/Linux) via `uv run`  
**Project Type**: Single CLI/utility repository with per-day subdirectories  
**Performance Goals**: Process up to 1000 ranges and 1000+ ingredient IDs in ≤ O((R + I) log R) time with minimal memory; strive for O(R log R + I log R) or better  
**Constraints**: Must follow AoC constitution (function-based design, TDD-first, `uv run` for execution, Ruff-compliant code)  
**Scale/Scope**: Single AoC puzzle part (Day 5 Part 1) within `day-05/` folder

## Constitution Check

_GATE: Must pass before Phase 0 research. Re-check after Phase 1 design._

- **Principle I (Clean Python Code)**: Plan maintains Pythonic, PEP8-compliant functions with Ruff enforced — PASS
- **Principle II (Structured Organization)**: Work confined to existing `day-05/` folder with required files — PASS
- **Principle III (Function-Based Solutions)**: Will implement `solve_part1` plus helper functions with docstrings — PASS
- **Principle IV (TDD Non-Negotiable)**: Tasks will enforce RED→GREEN→REFACTOR with pytest before implementation — PASS
- **Principle V (Automation First)**: meta runner/CLI usage unchanged; only puzzle logic touched — PASS
- **Runtime Execution Policy**: All commands executed via `uv run` — PASS

Gate status: ✅ Ready to proceed to Phase 0.

Post-Phase-1 recheck: ✅ Deliverables (research, data model, contracts, quickstart) align with constitution mandates (no new violations introduced).

## Project Structure

### Documentation (this feature)

```text
specs/012-day-05-part-1/
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
day-05/
├── description.md
├── input.txt
├── solution.py
├── test_input.txt
├── test_solution.py
└── README.md

cli/
├── __main__.py
├── meta_runner.py
└── ... (supporting AoC automation utilities)

tests/
└── fixtures/
```

**Structure Decision**: Single-repo CLI workspace where each puzzle lives under `day-XX/`. Day 05 artifacts stay within `day-05/`, while shared tooling remains in `cli/`. Global tests stay under `tests/` per constitution.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation                  | Why Needed         | Simpler Alternative Rejected Because |
| -------------------------- | ------------------ | ------------------------------------ |
| [e.g., 4th project]        | [current need]     | [why 3 projects insufficient]        |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient]  |
