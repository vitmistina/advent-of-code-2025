# Data Model: Automatic AOC Task & Input Download

**Feature**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)  
**Phase**: 1 - Design  
**Date**: 2024-11-28

## Overview

This document defines the data structures and entities for the automatic download feature. All models are described at a conceptual level without implementation details.

## Core Entities

### DownloadResult

Represents the outcome of a download operation (input or description).

**Attributes**:

- `success`: Boolean indicating if the download succeeded
- `content`: String containing the downloaded content (empty if failed)
- `error_message`: String describing the error (empty if succeeded)
- `source_url`: String containing the URL that was accessed
- `target_path`: String representing the destination file path

**Relationships**:

- Returned by download methods in AoCClient
- Consumed by scaffold functions to determine next actions

**State Transitions**:

```
[Pending] → [Downloading] → [Success | Failed]
```

**Validation Rules**:

- If `success` is True, `content` must be non-empty
- If `success` is False, `error_message` must be non-empty
- `source_url` must be a valid AOC URL format
- `target_path` must be a valid file path within `day-XX/` directory

---

### TaskDescription

Represents an extracted and converted puzzle task description.

**Attributes**:

- `part_number`: Integer (1 or 2) indicating which part of the puzzle
- `raw_html`: String containing the original HTML from `<article>` element
- `markdown_content`: String containing the converted Markdown text
- `heading`: String for the part heading (e.g., "Part 1", "Part 2")

**Relationships**:

- One or more TaskDescriptions per puzzle day (1 before Part 2 unlocks, 2 after)
- Aggregated into a single `task.md` file
- Extracted from HTML downloaded via DownloadResult

**Validation Rules**:

- `part_number` must be 1 or 2
- `raw_html` must contain valid HTML (even if malformed, parser handles it)
- `markdown_content` is derived from `raw_html` and cannot be set independently
- `heading` format must be "Part {part_number}" or custom from HTML

---

### PuzzleInput

Represents the downloaded puzzle input data.

**Attributes**:

- `day`: Integer (1-25) identifying the puzzle day
- `year`: Integer identifying the AOC year
- `content`: String containing the raw input data
- `file_path`: String path to the saved input file (e.g., `day-01/input.txt`)
- `downloaded_at`: Timestamp when the input was downloaded

**Relationships**:

- One PuzzleInput per day
- Associated with a DownloadResult that fetched it
- Saved to `day-{day:02d}/input.txt`

**Validation Rules**:

- `day` must be in range 1-25
- `year` must be ≥ 2015 (first year of AOC)
- `content` can be empty only if download failed
- `file_path` must exist after successful download

---

## Data Flow

### Download & Save Flow

```
1. User triggers scaffold command
   ↓
2. AoCClient.download_input(year, day) → DownloadResult
   ↓
3. If DownloadResult.success:
      Save DownloadResult.content to PuzzleInput.file_path
   Else:
      Print DownloadResult.error_message
   ↓
4. AoCClient.download_description(year, day) → DownloadResult
   ↓
5. If DownloadResult.success:
      Extract TaskDescription(s) from HTML
      Convert to Markdown
      Save to day-XX/task.md
   Else:
      Save warning message to task.md
```

### HTML Extraction Flow

```
1. Receive HTML string from DownloadResult
   ↓
2. Parse HTML with BeautifulSoup
   ↓
3. Find all <article class="day-desc"> elements
   ↓
4. For each article (index i):
      Create TaskDescription(
          part_number=i+1,
          raw_html=article.html,
          markdown_content=convert(article.html)
      )
   ↓
5. Aggregate TaskDescriptions into single file:
      # Part 1
      [markdown_content of TaskDescription #1]
      ---
      # Part 2
      [markdown_content of TaskDescription #2]
```

---

## File Structure Mapping

### Input File

**Entity**: PuzzleInput  
**File**: `day-{day:02d}/input.txt`  
**Format**: Plain text (user-specific puzzle input)

### Task Description File

**Entity**: List[TaskDescription]  
**File**: `day-{day:02d}/task.md`  
**Format**: Markdown with sections for Part 1 and Part 2

---

## Error States

### DownloadResult Error States

| State            | Trigger                       | Error Message Pattern                      |
| ---------------- | ----------------------------- | ------------------------------------------ |
| **RateLimited**  | HTTP 429 response             | "Rate limit exceeded after N attempts"     |
| **NotFound**     | HTTP 404 response             | "Puzzle not yet available for day X"       |
| **Unauthorized** | Missing/invalid session token | "Authentication failed; check AOC_SESSION" |
| **NetworkError** | Connection timeout/refused    | "Network error: {exception_message}"       |
| **ServerError**  | HTTP 5xx response             | "Server error ({status_code})"             |

### TaskDescription Error States

| State              | Trigger                               | Handling                                                             |
| ------------------ | ------------------------------------- | -------------------------------------------------------------------- |
| **MissingArticle** | No `<article class="day-desc">` found | Create TaskDescription with warning message in markdown              |
| **MalformedHTML**  | Parser encounters severe errors       | Use lenient parser; log warning; proceed with best-effort extraction |
| **EmptyContent**   | Article exists but contains no text   | Include heading only; add "No description available" message         |

---

## Constraints

### Business Rules

- Only 1-2 TaskDescriptions per day (Part 1 always present, Part 2 optional)
- PuzzleInput is unique per (year, day) combination
- Downloads respect rate limits (max 5 retries with exponential backoff)

### Technical Constraints

- File paths must be relative to repository root
- All file operations use UTF-8 encoding
- Markdown conversion preserves original HTML structure semantics
- No execution of downloaded content (read-only data)

---

## Future Considerations

### Potential Extensions (Out of Scope for This Feature)

- **TestInput extraction**: Parse example inputs from task description (requires NLP/pattern matching)
- **Caching**: Store downloaded HTML to avoid re-fetching on re-runs
- **Diff detection**: Detect when Part 2 is added and auto-update task.md
- **Metadata tracking**: Record download timestamps, response headers, etc.

These are explicitly **not** included in the current feature scope per the specification.
