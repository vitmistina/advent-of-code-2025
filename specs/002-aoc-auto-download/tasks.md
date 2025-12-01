# Tasks: Automatic AOC Task & Input Download

**Feature**: Automatic download of puzzle inputs and task descriptions from Advent of Code  
**Branch**: `002-aoc-auto-download`  
**Input**: Design documents from `specs/002-aoc-auto-download/`

**Organization**: Tasks are grouped by user story (P1, P2, P3) to enable independent implementation and testing.

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: User story label (US1, US2, US3)
- All task descriptions include exact file paths

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Install dependencies and prepare project for new feature

- [x] T001 Install beautifulsoup4 package via `uv add beautifulsoup4`
- [x] T002 Install html2text package via `uv add html2text`
- [x] T003 Run `uv sync` to ensure all dependencies are installed
- [x] T004 [P] Create tests/fixtures/ directory for test HTML samples

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core utilities needed by all user stories

- [x] T005 [P] Create sample AOC HTML fixture in tests/fixtures/sample_aoc_page.html with 2 article elements
- [x] T006 [P] Create sample Part 1 only fixture in tests/fixtures/sample_part1_only.html with 1 article element
- [x] T007 [P] Create sample missing articles fixture in tests/fixtures/sample_no_articles.html

**Checkpoint**: Test fixtures ready - user story implementation can begin

---

## Phase 3: User Story 1 - Download Puzzle Input to File (Priority: P1) 🎯 MVP

**Goal**: Automatically download puzzle input from AOC and save to `day-XX/input.txt`

**Independent Test**: Run CLI scaffold with valid session token; verify `input.txt` exists and contains actual puzzle data

### Tests for User Story 1 (TDD - Write FIRST)

> **RED Phase**: Write these tests FIRST, ensure they FAIL before implementation

- [x] T008 [P] [US1] Write test for successful input download in tests/test_scaffold.py
- [x] T009 [P] [US1] Write test for input download with rate limiting (429) in tests/test_scaffold.py
- [x] T010 [P] [US1] Write test for input download with missing session token in tests/test_scaffold.py
- [x] T011 [US1] Run tests to verify they FAIL (RED phase complete)

### Implementation for User Story 1

> **GREEN Phase**: Implement minimum code to make tests pass

- [x] T012 [US1] Verify AoCClient.download_input() already handles downloads correctly
- [x] T013 [US1] Update scaffold_day() in cli/scaffold.py to call download_input() and save to file
- [x] T014 [US1] Add file existence check in scaffold_day() to skip if input.txt already exists
- [x] T015 [US1] Add --force flag support to scaffold_day() to overwrite existing input.txt
- [x] T016 [US1] Run tests to verify they PASS (GREEN phase complete)

### Refactor for User Story 1

> **REFACTOR Phase**: Clean up code while keeping tests green

- [x] T017 [US1] Extract file-saving logic to helper function if needed
- [x] T018 [US1] Add docstrings to all new/modified functions
- [x] T019 [US1] Run ruff linter and fix any issues
- [x] T020 [US1] Verify all tests still pass after refactoring

**Checkpoint**: User Story 1 complete - puzzle inputs download automatically

---

## Phase 4: User Story 2 - Extract Task Description to Markdown (Priority: P2)

**Goal**: Download HTML, extract `<article class="day-desc">`, convert to Markdown, save to `day-XX/task.md`

**Independent Test**: Run CLI for a day with Part 1+2; verify `task.md` has both parts in clean Markdown

### Tests for User Story 2 (TDD - Write FIRST)

> **RED Phase**: Write these tests FIRST, ensure they FAIL before implementation

- [x] T021 [P] [US2] Write test for extracting single article (Part 1) in tests/test_aoc_client.py
- [x] T022 [P] [US2] Write test for extracting two articles (Part 1 & 2) in tests/test_aoc_client.py
- [x] T023 [P] [US2] Write test for extracting zero articles (empty list) in tests/test_aoc_client.py
- [x] T024 [P] [US2] Write test for HTML to Markdown conversion (headers) in tests/test_aoc_client.py
- [x] T025 [P] [US2] Write test for HTML to Markdown conversion (emphasis/strong) in tests/test_aoc_client.py
- [x] T026 [P] [US2] Write test for HTML to Markdown conversion (code blocks) in tests/test_aoc_client.py
- [x] T027 [P] [US2] Write test for HTML to Markdown conversion (inline code) in tests/test_aoc_client.py
- [x] T028 [P] [US2] Write test for HTML to Markdown conversion (lists) in tests/test_aoc_client.py
- [x] T029 [P] [US2] Write test for HTML to Markdown conversion (links) in tests/test_aoc_client.py
- [x] T030 [P] [US2] Write test for HTML entity decoding (&lt; &gt; &amp;) in tests/test_aoc_client.py
- [x] T031 [P] [US2] Write test for save_task_file() creating new file in tests/test_aoc_client.py
- [x] T032 [P] [US2] Write test for save_task_file() skipping existing file in tests/test_aoc_client.py
- [x] T033 [P] [US2] Write test for save_task_file() overwriting with force flag in tests/test_aoc_client.py
- [x] T034 [US2] Run all US2 tests to verify they FAIL (RED phase complete)

### Implementation for User Story 2

> **GREEN Phase**: Implement minimum code to make tests pass

- [x] T035 [P] [US2] Implement extract_task_description() method in cli/aoc_client.py using BeautifulSoup
- [x] T036 [P] [US2] Implement convert_html_to_markdown() method in cli/aoc_client.py using html2text
- [x] T037 [P] [US2] Configure html2text converter (body_width=0, ignore_links=False, unicode_snob=True)
- [x] T038 [US2] Implement save_task_file() method in cli/aoc_client.py
- [x] T039 [US2] Update scaffold_day() in cli/scaffold.py to download description and extract articles
- [x] T040 [US2] Update scaffold_day() to convert each article to Markdown with Part headings
- [x] T041 [US2] Update scaffold_day() to combine parts with separator (---) and save to task.md
- [x] T042 [US2] Run all US2 tests to verify they PASS (GREEN phase complete)

### Refactor for User Story 2

> **REFACTOR Phase**: Clean up code while keeping tests green

- [x] T043 [US2] Add comprehensive docstrings to extract_task_description(), convert_html_to_markdown(), save_task_file()
- [x] T044 [US2] Extract HTML parsing logic to helper method if complex
- [x] T045 [US2] Add type hints to all new methods
- [x] T046 [US2] Run ruff linter and fix any issues
- [x] T047 [US2] Verify all tests still pass after refactoring

**Checkpoint**: User Story 2 complete - task descriptions extract and convert to Markdown

---

## Phase 5: User Story 3 - Handle Download Failures Gracefully (Priority: P3)

**Goal**: Provide clear manual download instructions when automatic download fails

**Independent Test**: Simulate network failure; verify CLI prints helpful instructions and continues scaffolding

### Tests for User Story 3 (TDD - Write FIRST)

> **RED Phase**: Write these tests FIRST, ensure they FAIL before implementation

- [x] T048 [P] [US3] Write test for network timeout with retry in tests/test_aoc_client.py
- [x] T049 [P] [US3] Write test for 404 response (puzzle not available) in tests/test_aoc_client.py
- [x] T050 [P] [US3] Write test for exhausted retries printing manual URL in tests/test_scaffold.py
- [x] T051 [P] [US3] Write test for missing articles warning message in task.md in tests/test_aoc_client.py
- [x] T052 [P] [US3] Write test for scaffold continuing after download failure in tests/test_scaffold.py
- [x] T053 [US3] Run all US3 tests to verify they FAIL (RED phase complete)

### Implementation for User Story 3

> **GREEN Phase**: Implement minimum code to make tests pass

- [x] T054 [US3] Add warning message generation when extract_task_description() returns empty list
- [x] T055 [US3] Update save_task_file() to save warning message when no articles found
- [x] T056 [US3] Ensure scaffold_day() continues even if download_input() fails
- [x] T057 [US3] Ensure scaffold_day() continues even if download_description() fails
- [x] T058 [US3] Update error messages to include exact URLs and file paths per FR-009
- [x] T059 [US3] Run all US3 tests to verify they PASS (GREEN phase complete)

### Refactor for User Story 3

> **REFACTOR Phase**: Clean up code while keeping tests green

- [x] T060 [US3] Extract warning message template to constant or helper function
- [x] T061 [US3] Ensure consistent error message formatting across all failure modes
- [x] T062 [US3] Add docstring examples for error scenarios
- [x] T063 [US3] Run ruff linter and fix any issues
- [x] T064 [US3] Verify all tests still pass after refactoring

**Checkpoint**: User Story 3 complete - all download failures handled gracefully

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements affecting multiple user stories

- [x] T065 [P] Run full test suite with `uv run pytest tests/ -v`
- [x] T066 [P] Check test coverage with `uv run pytest --cov=cli tests/`
- [x] T067 [P] Ensure coverage is >90% for new code in aoc_client.py
- [x] T068 [P] Update CLI help text if new flags added (--force, --update)
- [x] T069 [P] Test full end-to-end workflow: scaffold day 1 with real AOC credentials
- [x] T070 [P] Test dry-run mode: scaffold with --dry-run flag
- [x] T071 Verify all docstrings follow Google/NumPy style
- [x] T072 Run ruff format on all modified files
- [x] T073 Update main README.md with new feature documentation if needed
- [x] T074 Create example task.md output in quickstart.md if not already present
- [x] T075 Final manual test: scaffold a day, verify input.txt and task.md are correct

---

## Dependencies & Parallel Execution

### User Story Dependencies

```
Setup (Phase 1) ────► Foundational (Phase 2)
                           │
                           ├─────► US1 (Phase 3) ─────┐
                           │                           │
                           ├─────► US2 (Phase 4) ─────┼──► Polish (Phase 6)
                           │                           │
                           └─────► US3 (Phase 5) ─────┘

All user stories are INDEPENDENT after Phase 2
```

### Parallel Execution Opportunities

**Within US1** (Phase 3):

- T008, T009, T010 can run in parallel (different test scenarios)

**Within US2** (Phase 4):

- T021-T033 can run in parallel (different test cases)
- T035, T036, T037 can run in parallel (different methods)

**Within US3** (Phase 5):

- T048-T052 can run in parallel (different test scenarios)

**Polish** (Phase 6):

- T065-T070 can run in parallel (independent verification tasks)

---

## Implementation Strategy

### MVP First Approach

**Minimum Viable Product** = Phase 3 (User Story 1) only:

- Downloads puzzle input automatically
- Saves to input.txt
- Handles basic errors

**Value**: Eliminates most repetitive manual step (copy-pasting input)

### Incremental Delivery

1. **Sprint 1**: Phases 1-3 (Setup + Foundation + US1) → **MVP**
2. **Sprint 2**: Phase 4 (US2) → **Enhanced** (task descriptions)
3. **Sprint 3**: Phase 5 (US3) → **Robust** (error handling)
4. **Sprint 4**: Phase 6 (Polish) → **Production Ready**

---

## Validation Checklist

### Before Starting Implementation

- [ ] All dependencies installed (T001-T003)
- [ ] Test fixtures created (T005-T007)
- [ ] Constitution checks reviewed and passed

### After Each User Story

- [ ] All tests for that story pass
- [ ] Ruff linting clean
- [ ] Independent test scenario verified
- [ ] Documentation updated

### Final Validation

- [ ] All 75 tasks completed
- [ ] Test coverage >90% for new code
- [ ] Full end-to-end workflow tested
- [ ] All files formatted and linted
- [ ] README updated (if needed)

---

## Task Count Summary

- **Setup**: 4 tasks
- **Foundation**: 3 tasks
- **User Story 1**: 13 tasks (8 tests + 5 implementation + refactor)
- **User Story 2**: 27 tasks (14 tests + 8 implementation + 5 refactor)
- **User Story 3**: 17 tasks (6 tests + 6 implementation + 5 refactor)
- **Polish**: 11 tasks

**Total**: 75 tasks

**Estimated Effort**:

- MVP (Phases 1-3): ~4-6 hours
- Full Feature (Phases 1-6): ~12-16 hours
