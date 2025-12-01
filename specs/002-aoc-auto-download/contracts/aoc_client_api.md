# API Contracts: AoCClient Extensions

**Feature**: Automatic AOC Task & Input Download  
**Date**: 2024-11-28

This document defines the contracts (interfaces) for new methods added to the `AoCClient` class.

---

## Method: `extract_task_description`

### Purpose

Extract task description HTML from `<article class="day-desc">` elements in the page HTML.

### Signature

```python
def extract_task_description(self, html: str) -> list[str]:
    """
    Extract task descriptions from AOC HTML page.

    Args:
        html: Full HTML content from puzzle page

    Returns:
        List of HTML strings, one per <article class="day-desc"> element.
        Empty list if no articles found.
    """
```

### Input Contract

- **html**: String containing valid HTML (may be malformed; parser handles gracefully)
- **html** must not be None or empty string

### Output Contract

- Returns list of strings (0, 1, or 2 elements typically)
- Each string contains the inner HTML of one `<article class="day-desc">` element
- Order preserved (first article = Part 1, second = Part 2)
- Returns empty list `[]` if no articles found

### Behavior

- **Success Case**: 1-2 article elements found → returns list of HTML strings
- **No Articles**: No matching elements → returns `[]`
- **Malformed HTML**: Parser handles gracefully → returns best-effort extraction

### Examples

**Input** (simplified):

```html
<main>
  <article class="day-desc">
    <h2>--- Day 1: Title ---</h2>
    <p>Description for Part 1</p>
  </article>
  <article class="day-desc">
    <h2>--- Part Two ---</h2>
    <p>Description for Part 2</p>
  </article>
</main>
```

**Output**:

```python
[
    '<h2>--- Day 1: Title ---</h2>\n<p>Description for Part 1</p>',
    '<h2>--- Part Two ---</h2>\n<p>Description for Part 2</p>'
]
```

---

## Method: `convert_html_to_markdown`

### Purpose

Convert HTML content to clean Markdown format, preserving structure and formatting.

### Signature

```python
def convert_html_to_markdown(self, html: str) -> str:
    """
    Convert HTML to Markdown with proper formatting.

    Args:
        html: HTML string to convert

    Returns:
        Markdown-formatted string
    """
```

### Input Contract

- **html**: String containing HTML (may include entities like `&lt;`)
- **html** must not be None; empty string is valid (returns empty string)

### Output Contract

- Returns string in Markdown format
- Preserves structure: headers, lists, code blocks, emphasis, links
- HTML entities decoded (e.g., `&lt;` → `<`)
- No line wrapping (body_width = 0)
- Consistent formatting

### Conversion Rules

| HTML Element                    | Markdown Output     |
| ------------------------------- | ------------------- |
| `<h2>Text</h2>`                 | `## Text`           |
| `<h3>Text</h3>`                 | `### Text`          |
| `<em>text</em>`                 | `*text*`            |
| `<strong>text</strong>`         | `**text**`          |
| `<code>inline</code>`           | `` `inline` ``      |
| `<pre><code>block</code></pre>` | ` ```\nblock\n``` ` |
| `<ul><li>item</li></ul>`        | `- item`            |
| `<ol><li>item</li></ol>`        | `1. item`           |
| `<a href="url">text</a>`        | `[text](url)`       |
| `&lt;`, `&gt;`, `&amp;`         | `<`, `>`, `&`       |

### Behavior

- **Normal HTML**: Converts to clean Markdown
- **Nested Elements**: Preserves nesting (e.g., bold within list item)
- **Empty Input**: Returns empty string
- **Malformed HTML**: Best-effort conversion; no exceptions raised

### Examples

**Input**:

```html
<h2>--- Day 1: Example ---</h2>
<p>This is <strong>important</strong> and <em>emphasized</em>.</p>
<pre><code>example_code()</code></pre>
```

**Output**:

```markdown
## --- Day 1: Example ---

This is **important** and _emphasized_.
```

example_code()

```

```

---

## Method: `save_task_file`

### Purpose

Save task description content to `day-XX/task.md` file.

### Signature

```python
def save_task_file(
    self,
    day: int,
    content: str,
    overwrite: bool = False
) -> tuple[bool, str]:
    """
    Save task description to file.

    Args:
        day: Day number (1-25)
        content: Markdown content to write
        overwrite: If True, overwrite existing file

    Returns:
        Tuple of (success, message)
    """
```

### Input Contract

- **day**: Integer in range 1-25
- **content**: String (may be empty)
- **overwrite**: Boolean (default False)

### Output Contract

- Returns tuple: `(bool, str)`
  - First element: `True` if file written, `False` if skipped or error
  - Second element: Message describing outcome

### Behavior

| Scenario           | overwrite | Result     | Message                                      |
| ------------------ | --------- | ---------- | -------------------------------------------- |
| File doesn't exist | False     | Write file | "✅ Saved task to day-XX/task.md"            |
| File doesn't exist | True      | Write file | "✅ Saved task to day-XX/task.md"            |
| File exists        | False     | Skip       | "⏭️ Skipped day-XX/task.md (already exists)" |
| File exists        | True      | Overwrite  | "✅ Overwrote task in day-XX/task.md"        |
| Invalid day        | Any       | Error      | "❌ Invalid day: must be 1-25"               |

### File Format

- Path: `day-{day:02d}/task.md` (e.g., `day-01/task.md`)
- Encoding: UTF-8
- Content: Raw Markdown string (no additional formatting)

### Examples

**Usage**:

```python
success, msg = client.save_task_file(
    day=1,
    content="# Part 1\n\nDescription here...",
    overwrite=False
)
print(msg)  # "✅ Saved task to day-01/task.md"
```

---

## Integration Contract

### Scaffold Workflow Integration

The new methods integrate into the scaffold workflow as follows:

```python
# In scaffold_day() function:

# 1. Download input (existing)
client = AoCClient(session_token, dry_run)
success, content = client.download_input(year, day)
if success:
    save_to_file(f"day-{day:02d}/input.txt", content)

# 2. Download and process task description (NEW)
success, html = client.download_description(year, day)
if success:
    # Extract article elements
    articles = client.extract_task_description(html)

    if articles:
        # Convert to Markdown
        parts = []
        for i, article_html in enumerate(articles, start=1):
            markdown = client.convert_html_to_markdown(article_html)
            parts.append(f"# Part {i}\n\n{markdown}")

        # Combine and save
        full_content = "\n\n---\n\n".join(parts)
        client.save_task_file(day, full_content, overwrite=force_flag)
    else:
        # No articles found - save warning
        warning = generate_warning_message(year, day)
        client.save_task_file(day, warning, overwrite=force_flag)
```

### Error Handling Contract

All methods follow consistent error handling:

1. **Never raise exceptions for expected failures** (e.g., no articles found)
2. **Return success/failure indicators** in return values
3. **Provide actionable error messages** for logging/display
4. **Degrade gracefully** when data is missing or malformed

---

## Testing Contract

### Test Coverage Requirements

Each method must have tests covering:

1. **extract_task_description**:

   - Single article (Part 1 only)
   - Two articles (Part 1 + Part 2)
   - No articles (empty list)
   - Malformed HTML (best-effort extraction)

2. **convert_html_to_markdown**:

   - Headers (h2, h3)
   - Emphasis (em, strong)
   - Code (inline and blocks)
   - Lists (ordered and unordered)
   - Links
   - HTML entities

3. **save_task_file**:
   - New file creation
   - Skip existing file
   - Overwrite existing file
   - Invalid day number

### Test Fixtures

Required fixture files in `tests/fixtures/`:

- `sample_aoc_page.html` - Full AOC page with 2 articles
- `sample_part1_only.html` - Page with only Part 1
- `sample_no_articles.html` - Page without article tags

---

## Versioning

**Version**: 1.0.0 (initial implementation)

**Breaking Changes**: None (new methods only, no modifications to existing AoCClient interface)

**Compatibility**: Python 3.10+ (matches project requirements)
