# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context

backend/

|-----------|------------|-------------------------------------|

# Implementation Plan: Day 03 Part 2 - Maximize Joltage with 12 Batteries

**Branch**: `010-day-03-part-2-spec` | **Date**: December 3, 2025 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/010-day-03-part-2-spec/spec.md`

## Summary

Select exactly 12 digits from each battery bank (string of digits, up to 100 long) to form the largest possible 12-digit number, preserving order. Sum across all banks. Must avoid brute-force; use monotonic stack (optimal subsequence selection) for O(n) per bank.

## Technical Context

**Language/Version**: Python 3.10+
**Primary Dependencies**: None (stdlib only)
**Storage**: N/A (in-memory)
**Testing**: pytest, assert statements
**Target Platform**: Any (cross-platform, AoC CLI)
**Project Type**: Single script per day (see day-03/)
**Performance Goals**: <100ms per bank, scales to n=100
**Constraints**: No brute-force, must handle large banks efficiently
**Scale/Scope**: Up to 100 banks, each with up to 100 digits

## Constitution Check

GATE: Must use clean, readable, efficient Python (see constitution-input.md)

- Use functions with docstrings
- PEP8 style
- At least one test per part
- No brute-force (O(n^k) forbidden)
- Use monotonic stack or DP (O(nk) max)

## Project Structure

### Documentation (this feature)

```text
specs/010-day-03-part-2-spec/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
day-03/
├── solution.py          # Main solution script (part 2 function)
├── input.txt            # Puzzle input
├── test_input.txt       # Sample input for testing
├── test_solution.py     # Tests for part 2
└── README.md            # Notes/explanations
```

**Structure Decision**: Use AoC day folder structure (see constitution-input.md)

## Complexity Tracking

No violations. Brute-force rejected for performance. Monotonic stack chosen for optimality and simplicity.
│ └── api/
