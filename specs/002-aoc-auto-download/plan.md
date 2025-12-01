# Implementation Plan: Automatic AOC Task & Input Download

**Branch**: `002-aoc-auto-download` | **Date**: 2024-11-28 | **Spec**: [spec.md](spec.md)  
**Input**: Feature specification from `specs/002-aoc-auto-download/spec.md`

## Summary

This feature extends the existing CLI to automatically download puzzle inputs from `https://adventofcode.com/{year}/day/{day}/input` and extract task descriptions from the HTML page (`<article class="day-desc">` elements), converting them to Markdown and saving as `task.md`. The implementation will add HTML parsing and Markdown conversion capabilities to the existing `AoCClient` class and integrate with the scaffold workflow.

## Technical Context

**Language/Version**: Python 3.10+  
**Primary Dependencies**: requests (existing), python-dotenv (existing), beautifulsoup4 (new), html2text (new)  
**Storage**: Local filesystem (`day-XX/input.txt`, `day-XX/task.md`)  
**Testing**: pytest with fixtures for mocked HTTP responses  
**Target Platform**: Cross-platform CLI (Windows/macOS/Linux)  
**Project Type**: Single project (CLI tool)  
**Performance Goals**: Complete download + parse + save in < 5 seconds total (network latency < 2s assumed)  
**Constraints**: Must respect AOC rate limits (exponential backoff), must handle partial failures gracefully  
**Scale/Scope**: Single-user tool, ~25 days per year, small files (< 100KB per day)

## Constitution Check

_GATE: Must pass before Phase 0 research. Re-check after Phase 1 design._

### ✅ Principle I: Clean Python Code

- **Status**: PASS
- **Evidence**: Using Python 3.10+ features, will follow PEP8, Ruff configured in `pyproject.toml`

### ✅ Principle II: Structured Organization

- **Status**: PASS
- **Evidence**: Maintains `day-XX/` folder structure; adds `task.md` alongside existing `input.txt`, `solution.py`, etc.

### ✅ Principle III: Function-Based Solutions

- **Status**: PASS
- **Evidence**: New functions will be added to `AoCClient` class (e.g., `extract_task_description()`, `convert_html_to_markdown()`); all functions will include docstrings

### ✅ Principle IV: Test-Driven Development

- **Status**: PASS
- **Evidence**: Tests will be written first for HTML extraction and Markdown conversion; will use pytest with mocked HTTP responses

### ✅ Principle V: Automation First

- **Status**: PASS - **THIS IS THE FEATURE IMPLEMENTING THIS PRINCIPLE**
- **Evidence**: This feature IS the automation for downloading inputs and task descriptions; complies with manual submission requirement

### ✅ Principle VI: AoC Compliance & Rate Limiting

- **Status**: PASS
- **Evidence**: Leverages existing `AoCClient` retry/backoff logic; no auto-submission; respects dry-run mode

### ✅ Principle VII: Documentation & Progress Tracking

- **Status**: PASS
- **Evidence**: No changes to `README.md` structure; feature documents itself through generated `task.md` files

### ✅ Principle VIII: Specification-Driven Workflow

- **Status**: PASS
- **Evidence**: This feature created via Specify framework; spec.md exists; tasks.md will be generated in Phase 2

### ✅ Principle IX: Delightful CLI

- **Status**: PASS
- **Evidence**: Maintains friendly console output conventions; adds helpful messages for download status; graceful error handling with actionable guidance

### Code Structure Requirements

- **Status**: PASS
- **UV Dependency Management**: Existing; will add beautifulsoup4 and html2text via `uv add`
- **Runtime Execution**: All commands use `uv run` (existing pattern)
- **Git Version Control**: Using feature branch `002-aoc-auto-download`
- **Specify Integration**: This plan demonstrates compliance

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

```text
cli/
├── __init__.py          # Existing
├── __main__.py          # Existing - CLI entry point
├── aoc_client.py        # MODIFY - Add HTML extraction & Markdown conversion
├── scaffold.py          # MODIFY - Integrate downloads into scaffolding
├── meta_runner.py       # Existing - orchestration
├── utils.py             # Existing - shared utilities
└── specify_integration.py  # Existing - Specify framework integration

tests/
├── test_aoc_client.py   # NEW - Tests for HTML parsing & Markdown conversion
├── test_scaffold.py     # MODIFY - Add tests for download integration
├── test_cli_help.py     # Existing
├── test_backoff.py      # Existing
└── fixtures/
    └── sample_aoc_page.html  # NEW - Sample HTML for testing

day-XX/                  # Example day folder (scaffolded output)
├── solution.py          # Existing
├── test_solution.py     # Existing
├── input.txt            # POPULATED by this feature
├── task.md              # NEW - Created by this feature
└── README.md            # Existing
```

**Structure Decision**: Single project structure (existing pattern). This feature extends the `cli/` package with new methods in `aoc_client.py` for HTML extraction and Markdown conversion. The `scaffold.py` module will be updated to call these methods during the scaffolding process. Tests follow the existing pattern in `tests/` directory.

## Complexity Tracking

> No constitution violations - this section is not applicable.

**All constitution checks PASS**. No complexity justification needed.

---

## Phase Outputs Summary

### ✅ Phase 0: Research (Complete)

**Output**: [research.md](research.md)

**Key Decisions**:

- **HTML Parsing**: BeautifulSoup4 with html.parser backend
- **Markdown Conversion**: html2text library with clean configuration
- **Integration**: Extend existing `AoCClient` class
- **Testing**: pytest with mocked responses and fixture HTML files

**Unknowns Resolved**:

- ✅ HTML structure: `<article class="day-desc">` elements
- ✅ Part 2 handling: Re-run with `--update` or `--force` flag
- ✅ Conversion library: html2text
- ✅ Test strategy: Mocked HTTP with fixtures

---

### ✅ Phase 1: Design & Contracts (Complete)

**Outputs**:

1. [data-model.md](data-model.md) - Entity definitions (DownloadResult, TaskDescription, PuzzleInput)
2. [quickstart.md](quickstart.md) - User guide with examples
3. [contracts/aoc_client_api.md](contracts/aoc_client_api.md) - API contracts for new methods

**Key Entities**:

- **DownloadResult**: Outcome of HTTP requests (success, content, error_message)
- **TaskDescription**: Extracted puzzle description (part_number, raw_html, markdown_content)
- **PuzzleInput**: Downloaded input data (day, year, content, file_path)

**API Contracts**:

- `extract_task_description(html: str) -> list[str]`
- `convert_html_to_markdown(html: str) -> str`
- `save_task_file(day: int, content: str, overwrite: bool) -> tuple[bool, str]`

---

### 🔄 Phase 2: Tasks (Pending)

**Command**: Run `/speckit.tasks` to generate [tasks.md](tasks.md)

**Expected Content**:

- TDD task breakdown (RED → GREEN → REFACTOR)
- Tasks organized by user story priority (P1, P2, P3)
- Explicit ordering for test-first workflow

**Next Action**: User should run `/speckit.tasks` when ready to begin implementation.

---

### ✅ Phase 2: Tasks (Complete)

**Output**: [tasks.md](tasks.md)

**Content**:

- 75 tasks organized by user story (P1, P2, P3)
- TDD workflow: RED → GREEN → REFACTOR for each story
- Parallel execution opportunities identified
- MVP path defined (Phases 1-3 = 20 tasks)

**Task Breakdown**:

- Setup & Foundation: 7 tasks
- User Story 1 (P1): 13 tasks
- User Story 2 (P2): 27 tasks
- User Story 3 (P3): 17 tasks
- Polish: 11 tasks

**Next Action**: Begin implementation following task order (start with T001)

---

## Implementation Checklist

### Dependencies

- [ ] Run `uv add beautifulsoup4 html2text`
- [ ] Run `uv sync` to install new packages

### Code Changes

- [ ] Extend `cli/aoc_client.py` with new methods
- [ ] Update `cli/scaffold.py` to call download methods
- [ ] Create `tests/test_aoc_client.py` with comprehensive tests
- [ ] Update `tests/test_scaffold.py` with integration tests
- [ ] Create `tests/fixtures/sample_aoc_page.html` for testing

### Testing

- [ ] Write tests FIRST (RED phase)
- [ ] Verify all tests fail initially
- [ ] Implement methods to make tests pass (GREEN phase)
- [ ] Refactor for clean code (REFACTOR phase)
- [ ] Achieve >90% code coverage for new code

### Integration

- [ ] Test full scaffold workflow with downloads
- [ ] Test dry-run mode
- [ ] Test file overwrite behavior
- [ ] Test error handling (rate limiting, missing articles, etc.)

### Documentation

- [ ] Update main README.md if needed
- [ ] Ensure all new functions have docstrings
- [ ] Add inline comments for complex logic

---

## Ready for Implementation

**Status**: ✅ **All Planning Complete - Ready to Code**

**Branch**: `002-aoc-auto-download`

**Generated Artifacts**:

- ✅ `plan.md` - This file
- ✅ `research.md` - Technology decisions and best practices
- ✅ `data-model.md` - Entity definitions
- ✅ `quickstart.md` - User guide
- ✅ `contracts/aoc_client_api.md` - API contracts
- ✅ `tasks.md` - **75 tasks with TDD workflow**
- ✅ Agent context updated (GitHub Copilot)

**Next Steps**:

1. Install dependencies: `uv add beautifulsoup4 html2text && uv sync`
2. Start with T001 from tasks.md
3. Follow TDD workflow: RED (write failing tests) → GREEN (implement) → REFACTOR (clean up)
