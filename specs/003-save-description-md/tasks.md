# Tasks: Save description.md for both AoC parts

**Input**: Design documents from `/specs/003-save-description-md/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Tests are included as this is a TDD project following Constitution Principle IV.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and test fixtures

- [x] T001 Verify project structure matches plan.md (cli/, tests/, day-XX/ structure)
- [x] T002 [P] Verify all dependencies installed (requests, beautifulsoup4, html2text, python-dotenv)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 Review existing AoCClient methods (download_description, extract_task_description, convert_html_to_markdown)
- [x] T004 [P] Create test fixtures for Part 1 + Part 2 HTML in tests/fixtures/ (can reuse sample_aoc_page.html)
- [x] T005 [P] Create test helper function for mocking download responses in tests/test_aoc_client.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Save Description on Download (Priority: P1) 🎯 MVP

**Goal**: Save downloaded puzzle description to `description.md` on successful download

**Independent Test**: Run `uv run -m cli.meta_runner download --day 1`, verify `day-01/description.md` exists and contains Markdown content

### Tests for User Story 1 (RED Phase - Write tests FIRST)

> **⚠️ CRITICAL: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T006 [P] [US1] Write test `test_save_description_creates_file` in tests/test_aoc_client.py (verify file created on success)
- [x] T007 [P] [US1] Write test `test_save_description_correct_content` in tests/test_aoc_client.py (verify Markdown content matches expected)
- [x] T008 [P] [US1] Write test `test_save_description_creates_folder` in tests/test_aoc_client.py (verify day folder created if missing)
- [x] T009 [US1] Run tests to verify they FAIL (pytest tests/test_aoc_client.py -v -k "test_save_description")

### Implementation for User Story 1 (GREEN Phase)

- [x] T010 [US1] Modify `cmd_download()` in cli/meta_runner.py: After successful description download, extract articles using `client.extract_task_description(desc_content)`
- [x] T011 [US1] Modify `cmd_download()` in cli/meta_runner.py: Join articles with `"\n\n"` separator
- [x] T012 [US1] Modify `cmd_download()` in cli/meta_runner.py: Convert combined HTML to Markdown using `client.convert_html_to_markdown()`
- [x] T013 [US1] Modify `cmd_download()` in cli/meta_runner.py: Create day folder with `Path(f"day-{day:02d}").mkdir(parents=True, exist_ok=True)`
- [x] T014 [US1] Modify `cmd_download()` in cli/meta_runner.py: Write Markdown to `day-{day:02d}/description.md` with UTF-8 encoding
- [x] T015 [US1] Modify `cmd_download()` in cli/meta_runner.py: Add success message "✅ Description saved to day-XX/description.md"
- [x] T016 [US1] Run tests to verify they PASS (pytest tests/test_aoc_client.py -v -k "test_save_description")

### Refactor for User Story 1 (REFACTOR Phase)

- [x] T017 [US1] Add error handling: wrap file write in try-except for OSError
- [x] T018 [US1] Ensure code follows PEP8 (run ruff check cli/meta_runner.py)
- [x] T019 [US1] Add inline comments explaining the description save workflow
- [x] T020 [US1] Run full test suite to ensure no regressions (pytest tests/ -v)

**Checkpoint**: At this point, User Story 1 should be fully functional - descriptions save on first download

---

## Phase 4: User Story 2 - Overwrite Description After Part 2 Unlock (Priority: P2)

**Goal**: Support re-downloading to update `description.md` with Part 2 content

**Independent Test**: Download day 1, manually edit `description.md` to remove Part 2, re-download, verify Part 2 is restored

### Tests for User Story 2 (RED Phase - Write tests FIRST)

> **⚠️ CRITICAL: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T021 [P] [US2] Write test `test_save_description_overwrites_existing` in tests/test_aoc_client.py (verify existing file is overwritten)
- [x] T022 [P] [US2] Write test `test_save_description_part2_update` in tests/test_aoc_client.py (verify Part 1-only file updated to Part 1+2)
- [x] T023 [US2] Run tests to verify they FAIL (pytest tests/test_aoc_client.py -v -k "test_save_description_overwrite or test_save_description_part2")

### Implementation for User Story 2 (GREEN Phase)

- [x] T024 [US2] Verify `cmd_download()` in cli/meta_runner.py: File write uses mode "w" (overwrites by default - should already be implemented from US1)
- [x] T025 [US2] Test with fixture `sample_part1_only.html`: Verify single article converted correctly
- [x] T026 [US2] Test with fixture `sample_aoc_page.html`: Verify two articles joined and converted correctly
- [x] T027 [US2] Run tests to verify they PASS (pytest tests/test_aoc_client.py -v -k "test_save_description_overwrite or test_save_description_part2")

### Refactor for User Story 2 (REFACTOR Phase)

- [x] T028 [US2] Add test case for idempotency (downloading same content twice produces same file)
- [x] T029 [US2] Run full test suite to ensure no regressions (pytest tests/ -v)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work - re-downloads update the file

---

## Phase 5: User Story 3 - Handle Download Failures Gracefully (Priority: P3)

**Goal**: Ensure no file is created or modified when download fails

**Independent Test**: Mock a failed download (HTTP 404), verify no `description.md` created and clear error shown

### Tests for User Story 3 (RED Phase - Write tests FIRST)

> **⚠️ CRITICAL: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T030 [P] [US3] Write test `test_save_description_failure_no_write` in tests/test_aoc_client.py (verify no file created on download failure)
- [x] T031 [P] [US3] Write test `test_save_description_failure_preserves_existing` in tests/test_aoc_client.py (verify existing file unchanged on download failure)
- [x] T032 [P] [US3] Write test `test_save_description_empty_content` in tests/test_aoc_client.py (verify no file created if content is empty)
- [x] T033 [US3] Run tests to verify they FAIL (pytest tests/test_aoc_client.py -v -k "test_save_description_failure or test_save_description_empty")

### Implementation for User Story 3 (GREEN Phase)

- [x] T034 [US3] Verify `cmd_download()` in cli/meta_runner.py: File write only happens inside `if desc_success:` block (should already be implemented from US1)
- [x] T035 [US3] Add validation in `cmd_download()`: Check that `desc_content` is non-empty before writing
- [x] T036 [US3] Add validation in `cmd_download()`: Check that `extract_task_description()` returns non-empty list
- [x] T037 [US3] Update error message on download failure to be clear and actionable
- [x] T038 [US3] Run tests to verify they PASS (pytest tests/test_aoc_client.py -v -k "test_save_description_failure or test_save_description_empty")

### Refactor for User Story 3 (REFACTOR Phase)

- [x] T039 [US3] Add error handling for file write failures (OSError) with clear error message
- [x] T040 [US3] Add error handling for permission errors with actionable message
- [x] T041 [US3] Ensure error messages never leak session token (use never_log_secret utility)
- [x] T042 [US3] Run full test suite to ensure no regressions (pytest tests/ -v)

**Checkpoint**: All user stories should now be independently functional - error handling is robust

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T043 [P] Add test for Unicode characters in description (verify UTF-8 encoding preserved)
- [ ] T044 [P] Add integration test for full `download` command flow in tests/test_cli_integration.py (if file doesn't exist, create it)
- [ ] T045 Update quickstart.md examples with real output from running the command
- [x] T046 Run full test suite with coverage (pytest tests/ --cov=cli --cov-report=term-missing)
- [x] T047 Verify Ruff linting passes (ruff check cli/)
- [ ] T048 Manual validation: Run `uv run -m cli.meta_runner download --day 1` and verify all acceptance scenarios
- [x] T049 Manual validation: Test dry-run mode (--dry-run flag) and verify no files created
- [ ] T050 Update main README.md with description.md feature (if README has a features section)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories SHOULD proceed sequentially (P1 → P2 → P3) since they build on each other
  - However, tests for all stories can be written in parallel after Foundational
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after US1 implementation - Builds on the file-writing logic
- **User Story 3 (P3)**: Can start after US1 implementation - Builds on the conditional logic

### Within Each User Story (TDD Workflow)

1. **RED**: Write tests first (T006-T009, T021-T023, T030-T033)
2. **Verify tests FAIL**: Run tests to ensure they fail before implementation
3. **GREEN**: Implement minimum code to pass tests (T010-T016, T024-T027, T034-T038)
4. **Verify tests PASS**: Run tests to ensure implementation works
5. **REFACTOR**: Clean up code while keeping tests green (T017-T020, T028-T029, T039-T042)

### Parallel Opportunities

- **Phase 1 (Setup)**: All tasks marked [P] can run in parallel
- **Phase 2 (Foundational)**: Tasks T004 and T005 can run in parallel after T003
- **Within User Stories**: All test-writing tasks marked [P] can run in parallel (different test files)
- **Refactoring**: Some refactor tasks can run in parallel if they touch different aspects

---

## Parallel Example: User Story 1 Tests

```bash
# Launch all test-writing tasks for User Story 1 together (RED phase):
Task T006: "Write test test_save_description_creates_file"
Task T007: "Write test test_save_description_correct_content"
Task T008: "Write test test_save_description_creates_folder"

# These write to same file but different test functions - can be done in parallel by different devs
# or sequentially by one dev
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T002)
2. Complete Phase 2: Foundational (T003-T005) ← CRITICAL
3. Complete Phase 3: User Story 1 (T006-T020) ← TDD: RED → GREEN → REFACTOR
4. **STOP and VALIDATE**: Test with `uv run -m cli.meta_runner download --day 1`
5. Verify `day-01/description.md` created with correct content
6. **MVP COMPLETE** - Can use immediately for daily AoC workflow

### Incremental Delivery

1. Complete Setup + Foundational (T001-T005) → Foundation ready
2. Add User Story 1 (T006-T020) → Test independently → **MVP DEPLOYED**
3. Add User Story 2 (T021-T029) → Test re-download workflow → Feature enhanced
4. Add User Story 3 (T030-T042) → Test error scenarios → Production-ready
5. Add Polish (T043-T050) → Full quality assurance → Feature complete

### Time Estimates (for one developer, TDD approach)

- Phase 1 (Setup): 10 minutes
- Phase 2 (Foundational): 30 minutes
- Phase 3 (US1): 2-3 hours (RED: 30m, GREEN: 1.5h, REFACTOR: 30m)
- Phase 4 (US2): 1 hour (mostly validation, logic exists)
- Phase 5 (US3): 1.5 hours (error handling and edge cases)
- Phase 6 (Polish): 1 hour (testing and documentation)
- **Total: ~6-7 hours** for complete, tested implementation

---

## Notes

- This is a TDD project (Constitution Principle IV NON-NEGOTIABLE)
- All tests MUST be written first and verified to fail
- Implementation MUST be minimum code to pass tests
- Refactoring MUST keep tests green
- Each user story delivers independent value
- User Story 1 alone is a viable MVP
- File paths assume single-project structure from plan.md
- Use `uv run` for all command executions (Constitution runtime policy)
- Never log session tokens (use `never_log_secret` utility)
