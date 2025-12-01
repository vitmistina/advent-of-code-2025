# Phase 1: Data Model - Save description.md for both AoC parts

**Feature**: Save description.md for both AoC parts  
**Date**: December 1, 2025  
**Status**: Complete

## Overview

This document defines the data entities and their relationships for saving puzzle descriptions to `description.md` files.

## Entities

### 1. Puzzle Description File

**Entity Name**: `description.md`

**Purpose**: Stores the complete puzzle description (Part 1 and Part 2 if unlocked) in Markdown format for offline reference

**Location**: `day-{day:02d}/description.md` (e.g., `day-01/description.md`)

**Format**: Markdown text file, UTF-8 encoded

**Content Structure**:

```markdown
[Article 1: Part 1 description]

[Article 2: Part 2 description (if unlocked)]
```

**Lifecycle**:

1. Created on first successful download
2. Overwritten on subsequent successful downloads (e.g., after Part 2 unlocks)
3. Preserved if download fails (no partial writes)

**Validation Rules**:

- Must be valid UTF-8 text
- Must not be empty (download must succeed)
- Must be writable to filesystem

**Relationships**:

- Belongs to a specific day folder (`day-{day:02d}/`)
- Sibling to `input.txt`, `test_input.txt`, `solution.py`
- Source content fetched from AoC website

---

### 2. Download Response

**Entity Name**: DownloadResult (conceptual - exists as tuple in code)

**Purpose**: Represents the result of a description download operation

**Structure**:

```python
(success: bool, content: str)
# success: True if HTTP 200 received
# content: HTML string if success=True, error message if success=False
```

**States**:

- **Success**: `(True, "<html>...</html>")`
- **Failure**: `(False, "Error message")`

**Validation Rules**:

- `success` must be `True` before writing to file
- `content` must be non-empty HTML string when `success=True`

**Relationships**:

- Returned by `AoCClient.download_description()`
- Consumed by `cmd_download()` to determine file write

---

### 3. Article Collection

**Entity Name**: Articles (intermediate data)

**Purpose**: Extracted HTML article elements from AoC page

**Structure**:

```python
List[str]  # Each string is one <article class="day-desc">...</article>
```

**Cardinality**:

- 1 article: Part 1 only (before solving Part 1)
- 2 articles: Part 1 + Part 2 (after unlocking Part 2)

**Processing Flow**:

```
HTML page → extract_task_description() → List[articles]
→ join("\n\n") → combined HTML
→ convert_html_to_markdown() → Markdown string
→ write to description.md
```

**Validation Rules**:

- List must not be empty (indicates malformed page)
- Each article must be valid HTML string

---

## Data Flow

```
┌─────────────────────┐
│ AoC Website         │
│ (HTML page)         │
└──────────┬──────────┘
           │ HTTP GET
           ▼
┌─────────────────────┐
│ AoCClient           │
│ download_description│
└──────────┬──────────┘
           │ (success, html_content)
           ▼
┌─────────────────────┐
│ extract_task_       │
│ description()       │
└──────────┬──────────┘
           │ List[article_html]
           ▼
┌─────────────────────┐
│ Join articles       │
│ with "\n\n"         │
└──────────┬──────────┘
           │ combined_html
           ▼
┌─────────────────────┐
│ convert_html_to_    │
│ markdown()          │
└──────────┬──────────┘
           │ markdown_text
           ▼
┌─────────────────────┐
│ Write to            │
│ description.md      │
└─────────────────────┘
```

## State Transitions

### Description File States

1. **Non-existent** → **Part 1 Only**

   - Trigger: First successful download before solving Part 1
   - Action: Create `description.md` with Part 1 content

2. **Part 1 Only** → **Part 1 + Part 2**

   - Trigger: Re-download after unlocking Part 2
   - Action: Overwrite `description.md` with full content

3. **Any State** → **Same State** (preserved)

   - Trigger: Download failure
   - Action: No file modification, error message displayed

4. **Part 1 + Part 2** → **Part 1 + Part 2** (idempotent)
   - Trigger: Re-download when both parts already present
   - Action: Overwrite with same content (no user-visible change)

## Field Definitions

### description.md Content

| Field           | Type     | Required    | Description                                              |
| --------------- | -------- | ----------- | -------------------------------------------------------- |
| Heading         | Text     | Yes         | Day number and title (e.g., "Day 1: Historian Hysteria") |
| Part 1 Story    | Markdown | Yes         | Narrative context for Part 1                             |
| Part 1 Task     | Markdown | Yes         | What to compute for Part 1                               |
| Part 1 Examples | Markdown | Conditional | Sample inputs/outputs (if provided by AoC)               |
| Part 2 Story    | Markdown | Conditional | Narrative for Part 2 (after unlock)                      |
| Part 2 Task     | Markdown | Conditional | What to compute for Part 2 (after unlock)                |
| Part 2 Examples | Markdown | Conditional | Sample inputs/outputs for Part 2                         |

### File Metadata

| Attribute    | Value            | Description                                      |
| ------------ | ---------------- | ------------------------------------------------ |
| Encoding     | UTF-8            | Character encoding                               |
| Line Endings | Platform-default | `\n` on Unix, `\r\n` on Windows (Python handles) |
| Extension    | `.md`            | Markdown format                                  |
| Permissions  | User read/write  | Standard file permissions                        |

## Constraints

1. **Atomicity**: File write must be atomic (success or no change)
2. **Encoding**: Must preserve Unicode characters (UTF-8)
3. **Idempotency**: Re-downloading same content has no side effects
4. **Overwrite semantics**: New content always replaces old (no append)
5. **Error isolation**: Download failure does not corrupt existing file

## Examples

### Example 1: Part 1 Only

```markdown
# Day 1: Historian Hysteria

The historians have lost track of time...

[Part 1 task description]

For example:

- Input: `3 4\n4 3\n2 5`
- Output: `11`
```

### Example 2: Part 1 + Part 2

```markdown
# Day 1: Historian Hysteria

The historians have lost track of time...

[Part 1 task description]

## Part Two

Now that you've helped them with Part 1...

[Part 2 task description]

For example:

- Input: `3 4\n4 3\n2 5`
- Output: `31`
```
