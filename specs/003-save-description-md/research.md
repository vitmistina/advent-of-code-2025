# Phase 0: Research - Save description.md for both AoC parts

**Feature**: Save description.md for both AoC parts  
**Date**: December 1, 2025  
**Status**: Complete

## Overview

This document captures research findings and decisions made during Phase 0 planning for saving puzzle descriptions to `description.md` files.

## Research Tasks

### 1. HTML to Markdown Conversion Strategy

**Question**: What's the best approach for converting AoC HTML descriptions to Markdown?

**Decision**: Use existing `html2text` library already in dependencies

**Rationale**:

- Already imported in `aoc_client.py`
- `AoCClient.convert_html_to_markdown()` method exists
- Configured for clean output (no line wrapping, keeps links, Unicode support)
- Proven to work with AoC HTML structure

**Alternatives considered**:

- BeautifulSoup custom parsing → Rejected: More complex, reinvents the wheel
- Pandoc → Rejected: External dependency, overkill for this use case

### 2. File Format Choice

**Question**: Should we save as `.md` or `.txt`?

**Decision**: Use `description.md` (Markdown format)

**Rationale**:

- Better rendering in editors and GitHub
- Semantic alignment with content (formatted text with headings)
- Consistent with project's documentation practices
- Enables future enhancements (syntax highlighting, links)

**Alternatives considered**:

- `description.txt` → Rejected: Less semantic, harder to read
- `description.html` → Rejected: Harder to read in plain text editors

### 3. Overwrite Behavior

**Question**: How should we handle re-downloads after Part 2 unlocks?

**Decision**: Always overwrite `description.md` on successful download

**Rationale**:

- AoC puzzle pages update in place (Part 2 is added to the same URL)
- Users need the complete description including Part 2
- No value in keeping Part 1-only version
- Consistent with existing `input.txt` behavior (always writes on success)

**Alternatives considered**:

- Append to file → Rejected: Would duplicate Part 1 content
- Versioned files (description_part1.md, description_part2.md) → Rejected: Over-engineered, splits context

### 4. Error Handling Strategy

**Question**: What should happen if description download fails?

**Decision**: Do not create or modify `description.md` on failure

**Rationale**:

- Prevents partial/corrupted files
- Preserves existing valid description if re-download fails
- Consistent with constitution (error handling)
- User gets clear error message to try again or download manually

**Implementation**:

- Check success flag from `client.download_description()`
- Only write file if `desc_success == True`
- Print clear error message if failed

### 5. HTML Extraction Method

**Question**: Do we need to modify the HTML extraction logic?

**Decision**: Use existing `AoCClient.extract_task_description()` and `convert_html_to_markdown()`

**Rationale**:

- `extract_task_description()` already extracts `<article class="day-desc">` elements
- Returns list of HTML strings (one per part)
- Can be joined and converted to Markdown
- Handles both Part 1-only and Part 1+2 scenarios

**Implementation approach**:

```python
articles_html = client.extract_task_description(desc_content)
combined_html = "\n\n".join(articles_html)
markdown = client.convert_html_to_markdown(combined_html)
```

### 6. Integration Point in CLI

**Question**: Where should the file-writing logic be added?

**Decision**: Modify `cmd_download()` in `meta_runner.py`

**Rationale**:

- Already has description download logic
- Has access to `day` variable for folder path
- Follows existing pattern (same place where `input.txt` is saved)
- Maintains single responsibility per command

**Code location**: `cli/meta_runner.py`, function `cmd_download()`, after line where `desc_success, desc_content = client.download_description(year, day)`

## Technical Constraints Identified

1. **Network reliability**: Downloads can fail; must handle gracefully
2. **Rate limiting**: AoC may rate-limit; already handled by backoff in `AoCClient`
3. **File system permissions**: Writing may fail; need try-except around file operations
4. **Encoding**: Must use UTF-8 for proper character rendering (AoC uses Unicode)

## Best Practices Applied

1. **DRY Principle**: Reuse existing methods (`extract_task_description`, `convert_html_to_markdown`)
2. **Fail-safe**: Only write on success, never partial files
3. **User feedback**: Clear messages for success and failure cases
4. **Consistency**: Match existing patterns in `cmd_download()` for `input.txt`
5. **Testing**: Add pytest tests with fixtures for HTML responses

## Dependencies Verified

All required dependencies already present in `pyproject.toml`:

- `requests` - HTTP client
- `beautifulsoup4>=4.14.3` - HTML parsing
- `html2text>=2025.4.15` - HTML to Markdown conversion
- `python-dotenv` - Environment variable management

**No new dependencies required.**

## Open Questions

None - all clarifications resolved.
