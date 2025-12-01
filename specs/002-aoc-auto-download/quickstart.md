# Quickstart: Automatic AOC Task & Input Download

**Feature**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)  
**Date**: 2024-11-28

## Overview

This guide demonstrates how to use the automatic download feature to fetch puzzle inputs and task descriptions from Advent of Code.

## Prerequisites

1. **AOC Session Token**: Obtain your session cookie from adventofcode.com

   - Log in to adventofcode.com
   - Open browser DevTools (F12)
   - Go to Application/Storage → Cookies
   - Copy the value of the `session` cookie

2. **Environment Setup**: Add token to `.env` file in repo root

   ```bash
   echo "AOC_SESSION=your_session_token_here" >> .env
   ```

3. **Dependencies Installed**: Ensure new packages are added
   ```bash
   uv add beautifulsoup4 html2text
   uv sync
   ```

---

## Basic Usage

### Scaffold a New Day with Auto-Download

Run the CLI scaffold command for a specific day:

```bash
uv run -m cli.meta_runner scaffold --day 1
```

**Expected Output**:

```
🎄 Scaffolding day 1...
📥 Downloading puzzle input...
✅ Saved input to day-01/input.txt
📥 Downloading task description...
✅ Extracted Part 1 description
✅ Saved task to day-01/task.md
✅ Created day-01/solution.py
✅ Created day-01/test_solution.py
✅ Created day-01/README.md

🎉 Day 1 scaffolded successfully!
```

**What Gets Created**:

- `day-01/input.txt` - Your personal puzzle input (downloaded)
- `day-01/task.md` - Puzzle description in Markdown (extracted from HTML)
- `day-01/solution.py` - Starter solution file (templated)
- `day-01/test_solution.py` - Starter test file (templated)
- `day-01/README.md` - Notes file (templated)

---

## Advanced Usage

### Dry-Run Mode (No Downloads)

Test scaffold without making actual HTTP requests:

```bash
uv run -m cli.meta_runner scaffold --day 1 --dry-run
```

**Output**:

```
🎄 Scaffolding day 1 (DRY RUN)...
🔍 DRY RUN: Would download input for 2024 day 1
📋 Manual download: https://adventofcode.com/2024/day/1/input
   1. Log in to adventofcode.com
   2. Navigate to the URL above
   3. Save the content to day-01/input.txt
🔍 DRY RUN: Would download description for 2024 day 1
📋 Manual access: https://adventofcode.com/2024/day/1
```

---

### Update Existing Day (After Part 2 Unlocks)

Re-run scaffold with `--force` to overwrite existing files:

```bash
uv run -m cli.meta_runner scaffold --day 1 --force
```

**Alternative**: Use `--update` flag (if implemented) to append Part 2:

```bash
uv run -m cli.meta_runner scaffold --day 1 --update
```

**Behavior**:

- `--force`: Overwrites `input.txt` and `task.md` completely
- `--update`: Appends Part 2 to existing `task.md` if only Part 1 exists

---

### Specify a Different Year

Override the default year from `.env`:

```bash
uv run -m cli.meta_runner scaffold --day 1 --year 2023
```

**Note**: Ensure your session token has access to the specified year's puzzles.

---

## File Outputs

### input.txt Example

```
3   4
4   3
2   5
1   3
3   9
3   3
```

This is your unique, user-specific puzzle input.

---

### task.md Example

````markdown
# Part 1

## --- Day 1: Historian Hysteria ---

The Chief Historian is missing! The Elves think he went to check on one of the historical locations...

**Example:**

```
3   4
4   3
2   5
```

The first list is `[3, 4, 2, 1, 3, 3]` and the second list is `[4, 3, 5, 3, 9, 3]`.

**What is the total distance between your lists?**

---

# Part 2

## --- Part Two ---

The Elves notice something interesting about the lists...

[Additional description appears here after Part 2 unlocks]
````

---

## Troubleshooting

### Problem: "Rate limit exceeded"

**Symptom**:

```
❌ Rate limit exceeded after 5 attempts.
📋 Please download manually:
   https://adventofcode.com/2024/day/1/input
   Save to: day-01/input.txt
```

**Solution**:

- Wait a few minutes and retry
- Or download manually via the URL provided

---

### Problem: "Puzzle not yet available"

**Symptom**:

```
❌ Puzzle not yet available for day 25
```

**Solution**:

- Wait until the puzzle unlocks (midnight EST)
- Or use a different day number

---

### Problem: "Authentication failed"

**Symptom**:

```
❌ Authentication failed; check AOC_SESSION
```

**Solution**:

- Verify `.env` contains correct session token
- Re-copy session cookie from browser (may have expired)
- Ensure no extra whitespace in `.env` file

---

### Problem: Missing task.md content

**Symptom**:

```
⚠️  Could not extract task description from HTML
```

**Content of task.md**:

```markdown
# Task Description Unavailable

⚠️ Could not extract task description from HTML.
...
```

**Solution**:

- Check if puzzle is published on adventofcode.com
- Verify HTML structure hasn't changed (rare)
- Manually copy description from website

---

## Testing

### Run Tests

Verify the feature works correctly:

```bash
# Run all tests
uv run pytest

# Run only download-related tests
uv run pytest tests/test_aoc_client.py tests/test_scaffold.py -v
```

### Expected Test Output

```
tests/test_aoc_client.py::test_extract_single_article PASSED
tests/test_aoc_client.py::test_extract_multiple_articles PASSED
tests/test_aoc_client.py::test_html_to_markdown_conversion PASSED
tests/test_aoc_client.py::test_handle_missing_articles PASSED
tests/test_scaffold.py::test_scaffold_with_downloads PASSED
tests/test_scaffold.py::test_scaffold_dry_run PASSED
tests/test_scaffold.py::test_scaffold_skip_existing_files PASSED
```

---

## Integration with Specify Workflow

After scaffolding with auto-download:

1. **Generate Spec** (if using Specify for the puzzle):

   ```bash
   uv run specify --input day-01/task.md --output specs/day-01/spec.md
   ```

2. **Generate Tasks**:

   ```bash
   uv run tasks --spec specs/day-01/spec.md --output specs/day-01/tasks.md
   ```

3. **Follow TDD Workflow**:
   - RED: Write tests first
   - GREEN: Implement solution
   - REFACTOR: Clean up code

---

## Summary

The automatic download feature eliminates manual copy-paste steps:

✅ **Before**: Copy input from browser → paste into file → copy description → paste into notes  
✅ **After**: Run one command → both files populated automatically

**Next Steps**: See [tasks.md](tasks.md) for implementation tasks (generated via `/speckit.tasks` command).
