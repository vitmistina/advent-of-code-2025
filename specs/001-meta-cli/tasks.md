# Tasks: Meta Runner & CLI (AoC 2025)

Feature: Meta Runner & CLI (AoC 2025)
Feature Dir: `specs/001-meta-cli`

## Phase 1: Setup

- [x] T001 Create project structure per plan at `cli/`
- [x] T002 Configure UV and sync dependencies in `.uv/` and `pyproject.toml`
- [x] T003 Create CLI package init in `cli/__init__.py`
- [x] T004 Add `.env` handling utilities in `cli/utils.py`
- [x] T005 Prepare Specify integration commands in `cli/specify_integration.py`
- [x] T006 Update quickstart with commands in `specs/001-meta-cli/quickstart.md`

## Phase 2: Foundational

- [x] T007 Implement rate-limited HTTP client in `cli/aoc_client.py`
- [x] T008 Implement scaffold helpers in `cli/scaffold.py`
- [x] T009 Wire argparse CLI entry in `cli/meta_runner.py`
- [x] T010 Add TDD messaging utilities in `cli/utils.py`

## Phase 3: [US1] Download & Scaffold Day (P1)

[X] T011 [US1] Create Day entity with paths in `cli/utils.py`
[X] T012 [P] [US1] Implement `scaffold --day` command in `cli/meta_runner.py`
[X] T013 [US1] Implement idempotent writes for `day-XX/` in `cli/scaffold.py`, including support for multi-part test inputs (`test_input_N.txt`)
[X] T014 [P] [US1] Implement `download --day --year --dry-run` in `cli/aoc_client.py`, ensuring dry-run prints manual retrieval guidance and avoids network actions

## Phase 4: [US2] Generate Spec & Tasks (P2)

[X] T021a [US2] If puzzle description lacks clear examples, generate placeholder `test_input.txt` and prompt user with actionable instructions

## Phase 5: [US3] Manual Submission Guidance (P3)

- [x] T022 [US3] Print Part 1/2 answers in `cli/meta_runner.py`
- [x] T023 [P] [US3] Display submission link and policy reminder in `cli/utils.py`
- [x] T024 [US3] Block auto-post; show steps in `cli/meta_runner.py`

## Final Phase: Polish & Cross-Cutting

- [x] T025 Add `--dry-run` flag handling in `cli/meta_runner.py`
- [x] T026 Improve `--help` ergonomics in `cli/meta_runner.py`
- [x] T027 Add progress notes reminders in `cli/utils.py`
- [x] T028 Security: never log `AOC_SESSION` in `cli/utils.py`
- [x] T029 Update progress tracker in `README.md`
- [x] T030 Confirm year handling from `.env` and `--year` in `cli/utils.py`
      [X] T031a Add measurable CLI UX: validate all error/success messages are actionable and friendly (user review or test)
      [X] T031b Add performance timing: measure and log wall-clock time for scaffold+download; target <30s
      [X] T031c Add test: all CLI flags and help output are discoverable and usable within 5 seconds by a new user

### Runtime & Validation Additions

- [x] T031 Validate `uv run` usage across quickstart and `--help` examples; replace any non-`uv run` Python invocations.
- [x] T032 Ensure all developer commands in docs use `uv run` consistently (quickstart, README, help output).
- [x] T033 Test `--dry-run` prevents any network actions and prints manual retrieval guidance.
- [x] T034 Verify `AOC_SESSION` never appears in logs/output; implement input masking and add a simple scan step.
- [x] T035 Measure scaffold+download timing in a warm environment; target < 30s and document results.
- [x] T036 Confirm TDD fail-first: ensure `day-XX/test_solution.py` tests fail (RED) before implementation (GREEN), then refactor while maintaining green.
      [X] T037 Validate multi-part test input support: ensure CLI generates and recognizes `test_input_N.txt` files as needed
      [X] T038 Validate actionable prompts: when examples are missing, CLI provides clear, actionable instructions for user to add test inputs

## Dependencies

- US1 → US2 → US3
- Foundational must complete before US1

## Parallel Execution Examples

- T012 and T014 can proceed in parallel
- T019 and T020 can proceed in parallel
- T023 can proceed in parallel with T022

## Implementation Strategy

- MVP: Complete Phase 3 (US1) first
- Incremental: Add US2, then US3

Note: Phases are organizational (Setup/Foundational/US1/US2/US3) and do not imply a separate “planning phase”; AoC skips planning per Constitution VIII.
