# Feature Specification: Meta Runner & CLI (AoC 2025)

**Feature Branch**: `001-meta-cli`  
**Created**: 2025-11-28  
**Status**: Draft  
**Input**: User description: "Specify meta functions and CLI for Advent of Code 2025 per Constitution 1.3.0, including automation-first meta runner, compliance, and delightful CLI."

## Clarifications

### Session 2025-11-28

- Q: What is the default behavior when `AOC_SESSION` is missing? → A: Prompt for token interactively (masked)
- Q: How do we select the Advent of Code year? → A: Non-secret `.env` setting `AOC_YEAR` (overrideable by CLI flag)
- Q: What level of observability should the CLI implement? → A: No observability beyond console prints

## User Scenarios & Testing _(mandatory)_

### User Story 1 - Download & Scaffold Day (Priority: P1)

The user starts a new AoC day and runs a single CLI command to fetch the puzzle description, download `input.txt`, create `day-XX/` with required files, and generate `specs/day-XX/spec.md` plus `specs/day-XX/tasks.md` via Specify.

**Why this priority**: This enables the core daily workflow and sets up TDD quickly with minimal manual steps.

**Independent Test**: Execute the CLI with a target day in a fresh repo; verify created files, populated inputs, and generated spec/tasks without needing any other features.

**Acceptance Scenarios**:

1. **Given** a valid `AOC_SESSION` in `.env`, **When** the user runs the CLI for `day-01`, **Then** the tool creates `day-01/` with `solution.py`, `test_solution.py`, `input.txt`, `test_input.txt`, and initializes `specs/day-01/spec.md` and `specs/day-01/tasks.md` from puzzle examples.
2. **Given** missing `input.txt`, **When** the CLI runs with network enabled, **Then** it downloads the puzzle input with rate-limited requests and exponential backoff.

---

### User Story 2 - Generate Spec & Tasks From Description (Priority: P2)

The user converts the puzzle description into a structured specification and a TDD task list using Specify commands integrated in the CLI flow.

**Why this priority**: Ensures disciplined TDD and consistent documentation per constitution.

**Independent Test**: Provide a sample description, run spec/tasks generation, and confirm spec sections and task breakdown exist and are complete.

**Acceptance Scenarios**:

1. **Given** a downloaded puzzle description, **When** the CLI triggers `specify` and `tasks`, **Then** `specs/day-XX/spec.md` contains P1/P2 stories with acceptance criteria and `specs/day-XX/tasks.md` includes RED→GREEN→REFACTOR tasks.

---

### User Story 3 - Manual Submission Guidance (Priority: P3)

After computing answers locally, the CLI displays results and clear steps for manual submission without automating website interactions.

**Why this priority**: Complies with AoC rules and avoids risky automation while keeping UX smooth.

**Independent Test**: Run solution on `input.txt`; verify outputs and that the CLI presents manual submission instructions (no auto-post).

**Acceptance Scenarios**:

1. **Given** a computed answer for Part 1/2, **When** the CLI finishes execution, **Then** it prints the answer(s), links to the submission page, and reiterates manual submission policy.

### Edge Cases

- Missing or invalid `AOC_SESSION` in `.env` → CLI prompts interactively to paste the token with masked input; if declined or non-interactive, it runs in dry-run mode and prints secure setup guidance.
- Network throttling or 429 responses → CLI must back off and retry with exponential strategy, up to a safe cap, then suggest manual retrieval.

  Clarification: Backoff MUST include jitter; max retries MUST be capped; once exceeded, CLI MUST print manual retrieval guidance and exit gracefully.

- Puzzle description without clear examples → CLI must leave placeholders for `test_input.txt` and prompt the user to add examples.
- Absent `AOC_YEAR` → CLI defaults to latest published year and prints which year is active; `--year` flag takes precedence over `.env`.
- Non-interactive environment or masked prompt declined → CLI MUST fall back to dry-run, print secure setup guidance, and exit with code 2.

## Requirements _(mandatory)_

### Functional Requirements

- **FR-001**: CLI MUST scaffold `day-XX/` with `solution.py`, `test_solution.py`, `input.txt`, `test_input.txt`, and optional `README.md` per Constitution Principle II. If the puzzle has multiple sample inputs, CLI MUST support `test_input_N.txt` (N=2,3,...) and generate placeholders as needed.
- **FR-002**: Meta runner MUST download puzzle description and `input.txt` when permitted, using exponential backoff with jitter and a safe max retry cap while respecting rate limits; upon exceeding the cap, it MUST print clear guidance for manual retrieval.
- **FR-003**: CLI MUST generate `specs/day-XX/spec.md` and `specs/day-XX/tasks.md` via Specify, skipping the plan phase.
- **FR-004**: CLI MUST enforce TDD flow: prompt to run RED tests, then GREEN implementation, then REFACTOR, with friendly messages. Initial tests MUST fail (RED) before implementation (GREEN); refactor maintains green.
- **FR-005**: CLI MUST provide manual submission guidance; answers MUST NOT be auto-submitted.
- **FR-006**: CLI MUST support a `--dry-run` mode for any network actions. In dry-run, CLI MUST print manual retrieval guidance and avoid all network requests.
- **FR-007**: CLI MUST avoid logging sensitive data; `AOC_SESSION` MUST never be printed. CLI MUST implement input masking and scan logs/output for accidental leaks.
- **FR-008**: CLI MUST offer ergonomic flags and helpful `--help` output. `--help` MUST list commands and examples; flags MUST include `--day`, `--year`, `--dry-run`; examples MUST be concise and colorized where supported.
- **FR-009**: CLI MUST update progress notes and remind to maintain `README.md` tracker.
- **FR-010**: CLI MUST use UV for dependency management and execute all Python commands via `uv run`. All documentation, examples, and help output MUST consistently use `uv run`.
- **FR-011**: CLI MUST support interactive masked entry of `AOC_SESSION` when missing, and gracefully fall back to dry-run when non-interactive or declined.
- **FR-012**: CLI MUST read non-secret `AOC_YEAR` from `.env` and support `--year` to override it; when neither is provided, default to latest published year.

### Non-Functional & UX Requirements

- **NFR-001**: CLI MUST provide a "delightful" user experience, defined as: (a) all error and success messages are clear, actionable, and friendly; (b) all prompts are colorized and masked where appropriate; (c) all commands complete in under 2s except for network actions; (d) help output is discoverable within 5 seconds.
- **NFR-002**: CLI flags MUST be ergonomic: short and long forms, grouped logically, and discoverable via `--help`.
- **NFR-003**: CLI MUST provide friendly, actionable prompts when puzzle description lacks clear examples, including instructions for the user to add `test_input.txt` or variants.
-

### Observability Clarification

- Logs are limited to user-facing console prints; no structured logging, metrics collection, tracing, or centralized aggregation is required. Ensure no sensitive data (e.g., `AOC_SESSION`) is printed.

### Key Entities

- **Day**: Represents a challenge day; attributes include `number`, `folder`, required files, and associated spec/task paths.
- **Meta Run Result**: Represents outputs of meta actions; attributes include `downloaded`, `createdFiles`, `specPath`, `tasksPath`, `messages`.

## Success Criteria _(mandatory)_

### Measurable Outcomes

- **SC-001**: New day setup completes in under 30 seconds in a warm environment. (Record wall-clock timing for scaffold+download and log the duration; target < 30s.)
- **SC-002**: 95% of runs with valid session tokens complete downloads without manual retries.
- **SC-003**: 100% of generated specs include P1/P2 stories and acceptance criteria; tasks include REDGREENREFACTOR per Constitution.
- **SC-004**: Users can locate answers and manual submission steps within 5 seconds of run completion.
- **SC-005**: No instance of `AOC_SESSION` or sensitive data appears in logs or output (verified by automated scan).
- **SC-006**: All CLI flags and help output are discoverable and usable within 5 seconds by a new user.
- **SC-007**: All error and success messages are actionable and friendly, as validated by user testing or review.

### Acceptance Clarifications

- **FR-006 (Dry-run)**: In dry-run mode, CLI prints clear manual retrieval guidance and does not perform any network actions.
- **FR-008 (Ergonomic Flags)**: `--help` output is colorized (where supported), lists all commands, and provides concise usage examples for each flag.
- **FR-001 (Test Inputs)**: If puzzle description lacks clear examples, CLI generates placeholder `test_input.txt` and prompts user to add examples, with actionable instructions.
