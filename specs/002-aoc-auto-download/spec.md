# Feature Specification: Automatic AOC Task & Input Download

**Feature Branch**: `002-aoc-auto-download`  
**Created**: 2024-11-28  
**Status**: Draft  
**Input**: User description: "CLI will download the input.txt (e.g. from https://adventofcode.com/2021/day/1/input) and it will download task.md (subtree of https://adventofcode.com/2021/day/1, look for <article class="day-desc"> in the HTML)"

## User Scenarios & Testing _(mandatory)_

### User Story 1 - Download Puzzle Input to File (Priority: P1)

The user runs the CLI command to scaffold a new day, and the tool automatically downloads the puzzle input from adventofcode.com and saves it to `day-XX/input.txt`, handling authentication and rate limiting gracefully.

**Why this priority**: This is the core value - eliminating manual copy-paste of puzzle inputs, which is the most repetitive daily task.

**Independent Test**: Run the CLI with a valid session token for a published day; verify that `day-XX/input.txt` exists and contains the actual puzzle input matching what appears on the website.

**Acceptance Scenarios**:

1. **Given** a valid `AOC_SESSION` token and an available puzzle day, **When** the user runs the scaffold command for that day, **Then** the CLI downloads the puzzle input via the `/input` endpoint and saves it to `day-XX/input.txt`.
2. **Given** rate limiting (429 response) from the AOC server, **When** the CLI attempts to download input, **Then** it retries with exponential backoff and jitter, up to the configured maximum retries.
3. **Given** a missing or invalid session token, **When** the CLI attempts to download input, **Then** it falls back to dry-run mode and prints manual download instructions with the correct URL.

---

### User Story 2 - Extract Task Description to Markdown (Priority: P2)

The user runs the CLI command, and the tool downloads the puzzle HTML page, extracts all `<article class="day-desc">` elements (Part 1 and Part 2 descriptions), converts them to clean Markdown, and saves them to `day-XX/task.md`.

**Why this priority**: Having the task description locally enables offline work and provides context for specs/tasks generation without needing to reference the browser.

**Independent Test**: Run the CLI for a day that has both Part 1 and Part 2 published; verify that `day-XX/task.md` exists, contains both part descriptions in Markdown format, preserves formatting (headers, code blocks, lists, emphasis), and is readable without HTML tags.

**Acceptance Scenarios**:

1. **Given** a puzzle day with Part 1 published, **When** the CLI downloads the page, **Then** it extracts the first `<article class="day-desc">` element, converts it to Markdown, and saves it to `day-XX/task.md` with a "Part 1" heading.
2. **Given** a puzzle day with both Part 1 and Part 2 published, **When** the CLI downloads the page, **Then** it extracts both `<article class="day-desc">` elements, converts them to Markdown, and saves them sequentially to `day-XX/task.md` with "Part 1" and "Part 2" headings.
3. **Given** HTML content with code examples in `<code>` or `<pre>` tags, **When** converting to Markdown, **Then** the CLI preserves code formatting using Markdown code blocks with appropriate indentation.
4. **Given** HTML content with emphasis (`<em>`) and strong (`<strong>`) tags, **When** converting to Markdown, **Then** the CLI converts them to `*italic*` and `**bold**` respectively.

---

### User Story 3 - Handle Download Failures Gracefully (Priority: P3)

When the CLI cannot download input or task description due to network errors, rate limiting, or puzzle unavailability, it provides clear, actionable guidance for manual download without failing the entire scaffold operation.

**Why this priority**: Ensures the CLI remains usable even when automated downloads fail, maintaining a good user experience.

**Independent Test**: Simulate network failure or use a future date; verify the CLI prints helpful manual download instructions and continues with the rest of the scaffold process.

**Acceptance Scenarios**:

1. **Given** a network timeout or connection error, **When** the CLI attempts to download, **Then** it retries up to the maximum attempts, then prints manual download instructions with the exact URL and file path.
2. **Given** a puzzle that is not yet published (404 response), **When** the CLI attempts to download, **Then** it immediately skips retries and prints a message indicating the puzzle is not yet available.
3. **Given** rate limiting that persists beyond maximum retries, **When** the CLI exhausts retry attempts, **Then** it prints the manual download URL and continues with local file scaffolding.

---

### Edge Cases

- What happens when only Part 1 is published (before Part 2 unlocks)?
  - CLI extracts only the first `<article class="day-desc">` and saves it as Part 1; when re-run after Part 2 unlocks, it should append Part 2 (or use a flag to update).
- How does the system handle malformed HTML or missing `<article class="day-desc">` elements?

  - CLI saves the raw HTML or a warning message to `task.md` indicating manual extraction is needed, and logs the issue clearly.

- What happens if `day-XX/input.txt` or `day-XX/task.md` already exist?

  - CLI skips download and prints a message that the file exists, unless a `--force` or `--update` flag is provided to overwrite.

- How does the system handle HTML entities (e.g., `&lt;`, `&gt;`, `&amp;`) in the task description?

  - CLI decodes HTML entities during HTML-to-Markdown conversion to produce clean, readable text.

- What happens when the session token expires mid-download?
  - CLI detects authentication failure (usually 400/401 response), prints a message to update the token, and provides manual download instructions.

## Scope & Boundaries

### In Scope

- Downloading puzzle input files from adventofcode.com
- Extracting and converting task descriptions to Markdown
- Graceful error handling and retry logic for network operations
- Automatic file creation for `input.txt` and `task.md`

### Out of Scope

- Automatic extraction of test inputs from puzzle examples (manual step remains)
- Auto-submission of answers to adventofcode.com (manual only per constitution)
- Parsing or interpretation of puzzle requirements for automated test generation
- Download of puzzle leaderboards, statistics, or community solutions

## Dependencies & Assumptions

### Dependencies

- Existing `AoCClient` class with HTTP request handling, retry logic, and backoff
- Valid AOC session token for authenticated downloads
- Network connectivity to adventofcode.com

### Assumptions

- Puzzle HTML structure remains consistent (uses `<article class="day-desc">` for descriptions)
- Session tokens have reasonable expiration periods (days to weeks, not hours)
- Users understand they need to obtain their session token from browser cookies
- Markdown conversion is sufficient for offline readability (no rich HTML rendering needed)

## Requirements _(mandatory)_

### Functional Requirements

- **FR-001**: CLI MUST download puzzle input from `https://adventofcode.com/{year}/day/{day}/input` using the authenticated session token and save it to `day-{day:02d}/input.txt`.

- **FR-002**: CLI MUST download the puzzle HTML page from `https://adventofcode.com/{year}/day/{day}` and extract all `<article class="day-desc">` elements.

- **FR-003**: CLI MUST convert extracted HTML content to Markdown format, preserving:

  - Headers (h2 → `## Header`, h3 → `### Header`, etc.)
  - Emphasis (`<em>` → `*text*`, `<strong>` → `**text**`)
  - Code blocks (`<pre><code>` → triple backticks)
  - Inline code (`<code>` → single backticks)
  - Lists (ordered and unordered)
  - Links (`<a href="...">` → `[text](url)`)

- **FR-004**: CLI MUST save extracted and converted task descriptions to `day-{day:02d}/task.md`, with Part 1 and Part 2 separated by clear headings.

- **FR-005**: CLI MUST decode HTML entities (e.g., `&lt;`, `&gt;`, `&amp;`, `&nbsp;`) to their Unicode equivalents during Markdown conversion.

- **FR-006**: CLI MUST skip download if `day-{day:02d}/input.txt` or `day-{day:02d}/task.md` already exist, unless a force/update flag is provided.

- **FR-007**: CLI MUST handle missing `<article class="day-desc">` elements by saving a warning message to `task.md` and logging the issue clearly to console.

- **FR-008**: CLI MUST distinguish between Part 1 and Part 2 descriptions by extracting multiple `<article class="day-desc">` elements in sequence and labeling them appropriately in the Markdown file.

- **FR-009**: When download fails (network error, rate limit exceeded, puzzle unavailable), CLI MUST print the exact URL for manual download and the target file path.

- **FR-010**: CLI MUST use the existing `AoCClient` class for all HTTP operations, leveraging its built-in retry logic, backoff, and dry-run mode.

### Key Entities _(include if feature involves data)_

- **Puzzle Input**: The unique, user-specific input data for a given day and year; downloaded from the `/input` endpoint; stored as plain text in `day-XX/input.txt`.

- **Task Description**: The puzzle description HTML containing one or more `<article class="day-desc">` elements; extracted and converted to Markdown; stored in `day-XX/task.md` with Part 1/Part 2 headings.

- **Download Result**: Represents the outcome of a download operation; attributes include `success` (boolean), `content` (string), `error_message` (string), and `target_path` (file path).

## Success Criteria _(mandatory)_

### Measurable Outcomes

- **SC-001**: Users can scaffold a new day and have both `input.txt` and `task.md` populated automatically in under 5 seconds (assuming network latency < 2s per request).

- **SC-002**: 95% of downloads succeed on the first attempt when a valid session token is provided and the puzzle is published.

- **SC-003**: When downloads fail, 100% of failure messages include the exact manual download URL and target file path.

- **SC-004**: Converted `task.md` files are readable in Markdown preview with no visible HTML tags or malformed formatting in 98% of cases.

- **SC-005**: Users can update an existing day's files (re-download after Part 2 unlocks) using a single flag without manual file deletion.
