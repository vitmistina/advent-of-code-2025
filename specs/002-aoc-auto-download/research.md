# Research: Automatic AOC Task & Input Download

**Feature**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)  
**Phase**: 0 - Research & Technology Decisions  
**Date**: 2024-11-28

## Overview

This document consolidates research findings for implementing automatic download of Advent of Code puzzle inputs and task descriptions, including HTML-to-Markdown conversion.

## Technology Decisions

### HTML Parsing Library

**Decision**: Use BeautifulSoup4

**Rationale**:

- Industry-standard for HTML parsing in Python
- Lenient parser handles malformed HTML gracefully
- Simple API for CSS selector queries (`soup.find_all('article', class_='day-desc')`)
- Well-documented with extensive community support
- Lightweight dependency (~50KB)

**Alternatives Considered**:

- **lxml**: Faster but stricter parsing; would fail on malformed HTML
- **html.parser** (stdlib): Basic but limited CSS selector support
- **Parsel**: Overkill for our simple extraction needs

**Implementation Note**: Will use `html.parser` as the BeautifulSoup backend to avoid extra C dependencies.

---

### HTML-to-Markdown Conversion

**Decision**: Use html2text

**Rationale**:

- Purpose-built for HTML → Markdown conversion
- Preserves semantic meaning (headers, emphasis, code blocks, lists)
- Handles HTML entities automatically (`&lt;` → `<`)
- Configurable output (can disable link reference style)
- Mature library (10+ years, well-maintained)

**Alternatives Considered**:

- **markdownify**: Similar features, but html2text has better code block handling
- **Custom regex-based conversion**: Fragile and error-prone for nested HTML
- **pandoc Python wrapper**: Heavy dependency for simple use case

**Configuration**:

```python
import html2text
h = html2text.HTML2Text()
h.ignore_links = False  # Preserve links
h.body_width = 0        # No line wrapping
h.unicode_snob = True   # Use Unicode instead of ASCII
```

---

### Integration with Existing AoCClient

**Decision**: Extend `AoCClient` class with new methods

**Rationale**:

- Existing retry/backoff logic is already implemented
- Session management already handles authentication
- Dry-run mode already supported
- Consistent error handling patterns

**New Methods**:

1. `extract_task_description(html: str) -> list[str]` - Extract article elements
2. `convert_to_markdown(html: str) -> str` - Convert HTML to Markdown
3. `save_task_file(day: int, content: str, overwrite: bool = False) -> bool` - Write task.md

**Best Practice**: Keep methods focused (single responsibility); compose them in `scaffold.py`

---

### File Overwrite Strategy

**Decision**: Skip by default, require explicit `--force` or `--update` flag

**Rationale**:

- Prevents accidental loss of manual edits
- Matches existing scaffold behavior for other files
- Supports "update after Part 2 unlocks" use case
- User-friendly: clear message when file exists

**Implementation**:

```python
if filepath.exists() and not overwrite:
    print(f"⏭️  Skipped {filepath} (already exists, use --force to overwrite)")
    return False
```

---

### Error Handling for Missing HTML Elements

**Decision**: Save warning message to task.md when `<article class="day-desc">` not found

**Rationale**:

- Degrades gracefully rather than failing
- Provides actionable feedback to user
- Allows scaffold process to continue
- Easy to detect and fix manually

**Warning Message Format**:

```markdown
# Task Description Unavailable

⚠️ Could not extract task description from HTML.

**Possible reasons**:

- Puzzle not yet published
- HTML structure changed
- Network error during download

**Manual action required**:
Visit https://adventofcode.com/{year}/day/{day} and copy the description manually.
```

---

### Testing Strategy

**Decision**: Use pytest with mocked HTTP responses and fixture HTML files

**Test Coverage**:

1. **Unit Tests** (test_aoc_client.py):

   - Extract single `<article>` (Part 1 only)
   - Extract multiple `<article>` elements (Part 1 & 2)
   - Handle missing `<article>` elements
   - Convert various HTML elements to Markdown (headers, code, lists, emphasis)
   - Decode HTML entities

2. **Integration Tests** (test_scaffold.py):
   - Full scaffold with download enabled
   - Dry-run mode (no actual downloads)
   - File exists → skip download
   - File exists + force flag → overwrite

**Fixtures**:

- `tests/fixtures/sample_aoc_page.html` - Real AOC HTML structure
- `tests/fixtures/sample_part1_only.html` - Page with only Part 1
- `tests/fixtures/sample_malformed.html` - Missing article tags

---

## Best Practices

### AOC Website Structure

**Current Structure** (as of 2024):

```html
<main>
  <article class="day-desc">
    <h2>--- Day 1: Title ---</h2>
    <p>Description...</p>
    <pre><code>Example code</code></pre>
  </article>
  <!-- Part 2 appears after solving Part 1 -->
  <article class="day-desc">
    <h2>--- Part Two ---</h2>
    <p>Additional description...</p>
  </article>
</main>
```

**Extraction Strategy**:

- Use `soup.find_all('article', class_='day-desc')`
- Iterate through results (1 or 2 articles expected)
- Label first as "Part 1", second as "Part 2"

### Markdown Formatting

**Desired Output Structure**:

```markdown
# Part 1

[Converted content from first <article>]

---

# Part 2

[Converted content from second <article>]
```

**Formatting Rules**:

- H2 in HTML → H2 in Markdown (preserve heading levels)
- `<pre><code>` → triple backtick code blocks
- `<code>` → single backtick inline code
- `<em>` → `*italic*`, `<strong>` → `**bold**`
- Preserve list structure (ordered and unordered)

---

## Dependencies

### New Packages to Add

```bash
uv add beautifulsoup4 html2text
```

### Version Constraints

- `beautifulsoup4>=4.12.0` - Latest stable with Python 3.10+ support
- `html2text>=2020.1.16` - Mature version with full feature set

### No Breaking Changes

Existing dependencies (`requests`, `python-dotenv`, `pytest`) remain unchanged.

---

## Performance Considerations

### Expected Timings

- HTTP request to download HTML: ~500ms - 2s (network dependent)
- HTML parsing with BeautifulSoup: <10ms
- Markdown conversion: <5ms
- File I/O (write task.md): <1ms

**Total**: < 3s including network latency (well under 5s goal)

### Memory Usage

- HTML page size: ~50-100KB
- Parsed DOM: ~500KB (temporary)
- Markdown output: ~20-50KB

**Total**: Negligible memory footprint (<1MB peak)

---

## Security Considerations

### Session Token Handling

- ✅ Already implemented in `AoCClient.__init__`
- ✅ Token never logged or printed
- ✅ Stored in `.env` (gitignored)

### HTML Injection Risk

- **Risk**: Malicious HTML in AOC pages could inject unwanted content
- **Mitigation**: html2text escapes HTML by converting to Markdown; no execution risk
- **Additional**: Markdown files are read-only documentation, not executed

---

## Unknowns Resolved

### ✅ Which HTML elements contain task descriptions?

**Answer**: `<article class="day-desc">` elements (1 for Part 1, 2 total after Part 2 unlocks)

### ✅ How to handle Part 2 appearing after Part 1 is solved?

**Answer**: Re-run scaffold with `--update` flag; append Part 2 to existing task.md or overwrite with `--force`

### ✅ What library for HTML → Markdown conversion?

**Answer**: html2text with configuration for clean output (no line wrapping, preserve links)

### ✅ How to test without hitting live AOC servers?

**Answer**: pytest with mocked `requests` responses and fixture HTML files

### ✅ What to do if HTML structure changes?

**Answer**: Graceful degradation - save warning message to task.md and log clear error message

---

## Next Steps

Proceed to **Phase 1: Design & Contracts** to create:

1. `data-model.md` - Define entities (DownloadResult, TaskDescription)
2. `contracts/` - API contracts for AoCClient methods
3. `quickstart.md` - Usage examples for new functionality
