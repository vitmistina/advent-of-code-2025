# Implementation Plan: Save description.md for both AoC parts

**Branch**: `003-save-description-md` | **Date**: December 1, 2025 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-save-description-md/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Save downloaded puzzle descriptions to `description.md` in the day folder. Support re-downloading after Part 2 unlocks to overwrite with updated content. Handle failures gracefully without creating incomplete files.

## Technical Context

**Language/Version**: Python 3.10+  
**Primary Dependencies**: requests, beautifulsoup4, html2text, python-dotenv  
**Storage**: Local filesystem (day-XX/description.md)  
**Testing**: pytest with fixtures for mocking HTTP responses  
**Target Platform**: Cross-platform CLI (Windows/Linux/macOS)  
**Project Type**: Single project with CLI module  
**Performance Goals**: Download and save within 5 seconds per request  
**Constraints**: Must respect AoC rate limits, handle network failures gracefully  
**Scale/Scope**: 25 days × 2 parts = up to 50 description downloads per year

## Constitution Check

_GATE: Must pass before Phase 0 research. Re-check after Phase 1 design._

### Initial Check (Before Phase 0)

✅ **Principle I (Clean Python)**: Solution uses Python 3.10+, follows PEP8  
✅ **Principle II (Structured Organization)**: Saves to day-XX/description.md per spec  
✅ **Principle III (Function-Based Solutions)**: CLI functions with clear separation  
✅ **Principle IV (TDD)**: Will write tests before implementation (RED-GREEN-REFACTOR)  
✅ **Principle V (Automation First)**: Extends existing download automation  
✅ **Principle VI (AoC Compliance)**: Respects rate limits, no auto-submission  
✅ **Principle VII (Documentation)**: Feature properly specified  
✅ **Principle VIII (Specification-Driven)**: Following speckit workflow  
✅ **Principle IX (Delightful CLI)**: Maintains existing UX patterns

### Post-Design Check (After Phase 1)

✅ **Principle I (Clean Python)**: Design reuses existing methods, follows PEP8 conventions  
✅ **Principle II (Structured Organization)**: `description.md` in `day-XX/` folder aligns with structure  
✅ **Principle III (Function-Based Solutions)**: Modifies existing `cmd_download()`, clear function boundaries  
✅ **Principle IV (TDD)**: Test cases defined in contracts, will implement RED-GREEN-REFACTOR  
✅ **Principle V (Automation First)**: Automated description save integrated with download workflow  
✅ **Principle VI (AoC Compliance)**: Uses existing rate-limited `AoCClient`, respects backoff  
✅ **Principle VII (Documentation)**: Research, data model, contracts, quickstart all complete  
✅ **Principle VIII (Specification-Driven)**: Full spec → plan → research → design workflow followed  
✅ **Principle IX (Delightful CLI)**: Clear success/error messages, maintains emoji-based UX

**No violations detected. No complexity justification needed.**

### Notes

- Minor naming alignment issue identified: `cmd_specify()` reads `description.txt` but this feature creates `description.md`
- Recommended fix: Update `cmd_specify()` in future iteration to read from `description.md`
- Not a constitution violation, just a consistency opportunity

## Project Structure

### Documentation (this feature)

```text
specs/003-save-description-md/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
# Single project structure
cli/
├── __init__.py
├── __main__.py
├── aoc_client.py        # AoCClient class with download methods
├── meta_runner.py       # CLI commands (scaffold, download, specify, all)
├── scaffold.py
├── specify_integration.py
└── utils.py

day-XX/                  # Created per day
├── description.md       # ← NEW: Downloaded puzzle description (Markdown)
├── input.txt           # Downloaded puzzle input
├── test_input.txt      # Sample input from examples
├── solution.py         # Solution implementation
├── test_solution.py    # Tests
└── README.md           # (optional) Notes

tests/
├── test_aoc_client.py   # ← MODIFIED: Add description save tests
├── test_scaffold.py
├── test_utils.py
└── fixtures/
    ├── sample_aoc_page.html          # Existing fixture
    ├── sample_part1_only.html        # Existing fixture
    └── sample_no_articles.html       # Existing fixture
```

**Structure Decision**: Using existing single-project structure. The `cmd_download` function in `meta_runner.py` will be modified to save `description.md` after successful download. The `AoCClient.download_description` method already returns HTML content; we need to add file-writing logic in the command handler.

## Complexity Tracking

**No violations detected - this section is not applicable.**
