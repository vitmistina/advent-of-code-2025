# API Contract: Description File Operations

**Feature**: Save description.md for both AoC parts  
**Date**: December 1, 2025  
**Version**: 1.0.0

## Overview

This document defines the internal API contract for saving puzzle descriptions to `description.md` files in the CLI meta runner.

## Function Contracts

### 1. cmd_download (Modified)

**Location**: `cli/meta_runner.py`

**Signature**:

```python
def cmd_download(args) -> int
```

**Input**:

- `args.day`: int (1-25)
- `args.year`: int | None (defaults to current AoC year)
- `args.dry_run`: bool (default: False)

**Output**:

- Returns: `0` if any download succeeded, `1` if all failed

**Behavior**:

1. Validate day number
2. Get session token
3. Create AoCClient instance
4. Download description:
   - On success: Extract articles, convert to Markdown, save to `description.md`
   - On failure: Print error, do NOT create/modify file
5. Download input (existing behavior)
6. Return exit code

**Side Effects**:

- Creates/overwrites `day-{day:02d}/description.md` on successful description download
- Prints progress messages to stdout

**Error Handling**:

- Network errors: Caught by AoCClient, error message printed
- File write errors: Must catch and print clear error message
- Invalid day: Returns 1 before any downloads

**Example Usage**:

```python
# Called by CLI dispatcher
args = argparse.Namespace(day=1, year=2025, dry_run=False)
exit_code = cmd_download(args)
```

---

### 2. AoCClient.download_description (Existing, No Changes)

**Location**: `cli/aoc_client.py`

**Signature**:

```python
def download_description(self, year: int, day: int) -> tuple[bool, str]
```

**Input**:

- `year`: int - AoC year
- `day`: int - Day number (1-25)

**Output**:

- `(True, html_content)` on success
- `(False, error_message)` on failure

**Behavior**:

- Makes HTTP GET to `https://adventofcode.com/{year}/day/{day}`
- Implements retry logic with exponential backoff
- Returns HTML content on success (HTTP 200)
- Returns error message on failure (404, 429, 500, network error)

**No changes required - existing implementation is sufficient.**

---

### 3. AoCClient.extract_task_description (Existing, No Changes)

**Location**: `cli/aoc_client.py`

**Signature**:

```python
def extract_task_description(self, html_content: str) -> list[str]
```

**Input**:

- `html_content`: str - Full HTML page from AoC

**Output**:

- List of HTML strings, each containing one `<article class="day-desc">` element
- Empty list if no articles found

**Behavior**:

- Uses BeautifulSoup to parse HTML
- Finds all `<article class="day-desc">` elements
- Returns list of article HTML strings

**No changes required - existing implementation is sufficient.**

---

### 4. AoCClient.convert_html_to_markdown (Existing, No Changes)

**Location**: `cli/aoc_client.py`

**Signature**:

```python
def convert_html_to_markdown(self, html_content: str) -> str
```

**Input**:

- `html_content`: str - HTML to convert

**Output**:

- str - Markdown-formatted text

**Behavior**:

- Uses html2text library
- Configured with no line wrapping, keeps links, Unicode support
- Returns clean Markdown

**No changes required - existing implementation is sufficient.**

---

## File System Contract

### Description File

**Path Pattern**: `day-{day:02d}/description.md`

**Format**: UTF-8 encoded Markdown text

**Write Conditions**:

- MUST create parent directory if not exists (`mkdir -p` semantics)
- MUST write only on successful download (`desc_success == True`)
- MUST overwrite existing file (if any)
- MUST NOT write partial content on error
- MUST use UTF-8 encoding explicitly

**Read Conditions**:

- File may not exist (first download)
- File may exist from previous download
- Used by `cmd_specify()` to generate spec (reads `description.txt` - note different name, will need alignment)

**Permissions**: Standard user read/write

---

## Error Responses

### Download Failures

| Scenario                        | AoCClient Response                              | cmd_download Behavior                                    |
| ------------------------------- | ----------------------------------------------- | -------------------------------------------------------- |
| HTTP 404 (puzzle not available) | `(False, "Puzzle not yet available for day N")` | Print error, skip file write, continue to input download |
| HTTP 429 (rate limit)           | `(False, "Rate limit exceeded...")`             | Print error, skip file write, continue to input download |
| HTTP 500 (server error)         | `(False, "HTTP 500...")`                        | Print error, skip file write, continue to input download |
| Network error                   | `(False, "Network error: ...")`                 | Print error, skip file write, continue to input download |
| Dry run                         | `(False, "DRY RUN: Would download...")`         | Print dry-run message, skip file write                   |
| No session token                | `(False, "DRY RUN: Would download...")`         | Print dry-run message, skip file write                   |

### File System Failures

| Scenario          | Detection              | Response                                     |
| ----------------- | ---------------------- | -------------------------------------------- |
| Permission denied | `OSError` during write | Catch exception, print clear error, return 1 |
| Disk full         | `OSError` during write | Catch exception, print clear error, return 1 |
| Invalid path      | `OSError` during mkdir | Catch exception, print clear error, return 1 |

---

## Integration Flow

```
User runs: uv run -m cli.meta_runner download --day 1

    ↓
main() parses args
    ↓
cmd_download(args) called
    ↓
validate_day(1) → True
    ↓
get_session_token() → "abc123..."
    ↓
AoCClient(token, dry_run=False)
    ↓
client.download_description(2025, 1) → (True, "<html>...</html>")
    ↓
client.extract_task_description(html) → ["<article>Part 1</article>", "<article>Part 2</article>"]
    ↓
"\n\n".join(articles) → "<article>Part 1</article>\n\n<article>Part 2</article>"
    ↓
client.convert_html_to_markdown(combined_html) → "# Day 1\n\n..."
    ↓
Path("day-01").mkdir(parents=True, exist_ok=True)
    ↓
(day-01/description.md).write_text(markdown, encoding="utf-8")
    ↓
Print: "✅ Description saved to day-01/description.md"
    ↓
[Continue to input download...]
    ↓
return 0
```

---

## Backward Compatibility

### Breaking Changes

None - this is a new feature.

### New Behavior

- `cmd_download()` now creates `description.md` in addition to `input.txt`
- `cmd_specify()` should eventually read from `description.md` instead of `description.txt` (alignment issue noted)

### Deprecations

None.

---

## Testing Contract

### Unit Tests Required

**File**: `tests/test_aoc_client.py` (modifications)

**Test Cases**:

1. `test_save_description_success` - Verify file created with correct content
2. `test_save_description_overwrite` - Verify existing file is overwritten
3. `test_save_description_part2_update` - Verify Part 2 appends correctly
4. `test_save_description_failure_no_write` - Verify no file on download failure
5. `test_save_description_unicode` - Verify UTF-8 encoding preserved

**Fixtures**:

- Use existing `sample_aoc_page.html` (has Part 1 + Part 2)
- Use existing `sample_part1_only.html` (has Part 1 only)

### Integration Tests

**File**: `tests/test_cli_integration.py` (new or extend existing)

**Test Cases**:

1. End-to-end download command with mocked HTTP
2. Verify file system changes after command execution

---

## Notes

### Known Issues

- `cmd_specify()` currently reads from `description.txt`, but this feature creates `description.md`
- Should align naming in future iteration or update `cmd_specify()` to read from `description.md`

### Future Enhancements

- Add `--force` flag to re-download even if file exists
- Add checksum verification for cached descriptions
- Support downloading specific parts only
