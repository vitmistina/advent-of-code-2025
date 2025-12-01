# Quickstart: Save description.md for both AoC parts

**Feature**: Save description.md for both AoC parts  
**Date**: December 1, 2025  
**Branch**: `003-save-description-md`

## Overview

This feature automatically saves Advent of Code puzzle descriptions to `description.md` files when using the `download` command. The description is saved in Markdown format for easy offline reference.

## Quick Start

### 1. Download a puzzle with description

```bash
# Download puzzle description and input for day 1
uv run -m cli.meta_runner download --day 1

# Output:
# 📥 Downloading inputs for 2025 Day 01...
# 📄 Downloading puzzle description...
# ✅ Description saved to day-01/description.md
# 📥 Downloading puzzle input...
# ✅ Input saved to day-01/input.txt
```

### 2. View the saved description

```bash
# On Windows
notepad day-01\description.md

# On Linux/Mac
cat day-01/description.md
```

### 3. Re-download after unlocking Part 2

After solving Part 1, re-run the download command to update `description.md` with Part 2:

```bash
uv run -m cli.meta_runner download --day 1

# The file will be overwritten with both Part 1 and Part 2
```

## Use Cases

### Use Case 1: First-time download (Part 1 only)

**Scenario**: You haven't started day 1 yet.

```bash
uv run -m cli.meta_runner download --day 1
```

**Result**:

- `day-01/description.md` created with Part 1 description
- `day-01/input.txt` created with puzzle input

**File content** (`day-01/description.md`):

```markdown
# Day 1: Historian Hysteria

The historians have lost track of time...

[Part 1 task description]

For example:
...
```

---

### Use Case 2: Re-download after Part 2 unlocks

**Scenario**: You solved Part 1 and want to get the Part 2 description.

```bash
# Run the same command again
uv run -m cli.meta_runner download --day 1
```

**Result**:

- `day-01/description.md` overwritten with Part 1 + Part 2
- `day-01/input.txt` unchanged (same input used)

**File content** (`day-01/description.md`):

```markdown
# Day 1: Historian Hysteria

The historians have lost track of time...

[Part 1 task description]

## Part Two

Now that you've helped them...

[Part 2 task description]
```

---

### Use Case 3: Download fails (network error)

**Scenario**: Your internet connection drops during download.

```bash
uv run -m cli.meta_runner download --day 1
```

**Output**:

```
📥 Downloading inputs for 2025 Day 01...
📄 Downloading puzzle description...
⚠️  Description download failed: Network error: Connection timeout
📥 Downloading puzzle input...
✅ Input saved to day-01/input.txt
```

**Result**:

- `day-01/description.md` **NOT created** (or preserved if existed before)
- `day-01/input.txt` created (if input download succeeded)
- Clear error message shown

---

### Use Case 4: Dry-run mode

**Scenario**: You want to see what would be downloaded without making requests.

```bash
uv run -m cli.meta_runner download --day 1 --dry-run
```

**Output**:

```
📥 Downloading inputs for 2025 Day 01...
📄 Downloading puzzle description...
🔍 DRY RUN: Would download description for 2025 day 1
📋 Manual access: https://adventofcode.com/2025/day/1
📥 Downloading puzzle input...
🔍 DRY RUN: Would download input for 2025 day 1
...
```

**Result**:

- No files created
- No network requests made
- Instructions for manual download shown

---

## File Structure

After running `download --day 1`:

```
advent-of-code-2025/
├── day-01/
│   ├── description.md   ← NEW: Puzzle description in Markdown
│   ├── input.txt        ← Existing: Puzzle input
│   ├── test_input.txt   ← Created by scaffold command
│   ├── solution.py      ← Created by scaffold command
│   └── test_solution.py ← Created by scaffold command
└── ...
```

## All-in-one Command

Use the `all` command to scaffold, download, and generate spec in one step:

```bash
uv run -m cli.meta_runner all --day 1

# This runs:
# 1. scaffold --day 1
# 2. download --day 1    ← Creates description.md
# 3. specify --day 1
```

## Workflow Integration

### Recommended TDD Workflow

1. **Scaffold the day**:

   ```bash
   uv run -m cli.meta_runner scaffold --day 1
   ```

2. **Download puzzle and description**:

   ```bash
   uv run -m cli.meta_runner download --day 1
   ```

3. **Read description**:

   ```bash
   # Windows
   notepad day-01\description.md

   # Linux/Mac
   less day-01/description.md
   ```

4. **Generate spec** (if using Specify):

   ```bash
   uv run -m cli.meta_runner specify --day 1
   ```

5. **Write tests** (RED):

   - Edit `day-01/test_solution.py`
   - Use examples from `description.md`

6. **Run tests** (verify they FAIL):

   ```bash
   uv run pytest day-01/test_solution.py -v
   ```

7. **Implement solution** (GREEN):

   - Edit `day-01/solution.py`

8. **Re-run tests** (verify they PASS):

   ```bash
   uv run pytest day-01/test_solution.py -v
   ```

9. **Submit Part 1 manually**, then **re-download for Part 2**:

   ```bash
   uv run -m cli.meta_runner download --day 1
   # description.md now includes Part 2
   ```

10. **Repeat steps 5-8 for Part 2**

## Troubleshooting

### Problem: "Description download failed: Puzzle not yet available"

**Cause**: The puzzle for that day hasn't been released yet (puzzles unlock at midnight EST).

**Solution**: Wait until the puzzle is released, or use `--dry-run` to see when it will be available.

---

### Problem: "Description download failed: Rate limit exceeded"

**Cause**: You've made too many requests to the AoC server.

**Solution**: Wait a few minutes before retrying. The CLI implements exponential backoff, but excessive requests may still trigger rate limiting.

---

### Problem: `description.md` is empty or corrupted

**Cause**: This should never happen (file is only written on success), but could indicate a bug.

**Solution**: Delete `description.md` and re-run the download command. If the problem persists, download manually from the AoC website.

---

### Problem: "Permission denied" when writing file

**Cause**: File system permissions prevent writing to the day folder.

**Solution**: Check folder permissions, or run from a location where you have write access.

---

## Advanced Usage

### Specify a different year

```bash
uv run -m cli.meta_runner download --day 1 --year 2024
```

### Force re-download (when implemented)

```bash
# Future enhancement
uv run -m cli.meta_runner download --day 1 --force
```

## Testing

### Run tests for this feature

```bash
# Run all tests
uv run pytest tests/ -v

# Run specific test file
uv run pytest tests/test_aoc_client.py -v

# Run with coverage
uv run pytest tests/ --cov=cli --cov-report=term-missing
```

### Verify file creation manually

```bash
# Download for day 1
uv run -m cli.meta_runner download --day 1

# Check if file exists
ls day-01/description.md  # Linux/Mac
dir day-01\description.md  # Windows

# View file content
cat day-01/description.md  # Linux/Mac
type day-01\description.md  # Windows
```

## Related Commands

- `scaffold --day N` - Create day folder and template files
- `specify --day N` - Generate spec from description (reads `description.txt` - naming alignment TBD)
- `all --day N` - Run scaffold + download + specify in sequence

## Next Steps

1. Start using `description.md` for offline reference
2. Consider integrating with `specify` command (update to read from `description.md`)
3. Provide feedback on UX and error messages
