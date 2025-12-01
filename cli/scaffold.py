"""Scaffolding functions for creating day folders and files."""

from datetime import datetime
from pathlib import Path

from cli.aoc_client import AoCClient


def _download_puzzle_input(day: int, session_token: str | None, year: int | None) -> str:
    """
    Download puzzle input from Advent of Code.

    Args:
        day: Day number (1-25)
        session_token: AOC session token (optional)
        year: AOC year (optional, defaults to current year)

    Returns:
        Downloaded input content, or empty string if download failed
    """
    if not (session_token or year):
        return ""

    actual_year = year if year else datetime.now().year
    client = AoCClient(session_token, dry_run=session_token is None)
    success, content = client.download_input(actual_year, day)

    if success:
        print(f"✅ Downloaded input for day {day}")
        return content
    else:
        print(content)  # Print error/dry-run message
        return ""


def _download_task_description(
    day: int, day_dir: str, session_token: str | None, year: int | None, force: bool = False
) -> None:
    """
    Download and save task description from Advent of Code.

    Args:
        day: Day number (1-25)
        day_dir: Directory where task.md should be saved
        session_token: AOC session token (optional)
        year: AOC year (optional, defaults to current year)
        force: If True, overwrite existing task.md
    """
    if not year:
        return

    actual_year = year if year else datetime.now().year
    client = AoCClient(session_token, dry_run=False)

    # Download HTML description
    success, html_content = client.download_description(actual_year, day)

    if not success:
        print(html_content)  # Print error message
        return

    # Extract article elements
    articles = client.extract_task_description(html_content)

    if not articles:
        warning_msg = (
            f"⚠️  No task description found for day {day}\n"
            f"📋 Manual access: {client.BASE_URL}/{actual_year}/day/{day}\n"
            f"   The puzzle may not be available yet, or the HTML structure has changed."
        )
        print(warning_msg)
        # Save warning to task.md
        client.save_task_file(day_dir, warning_msg, force=force)
        return

    # Convert each article to Markdown and combine
    markdown_parts = []
    for i, article_html in enumerate(articles, start=1):
        markdown = client.convert_html_to_markdown(article_html)
        if i == 1:
            markdown_parts.append(markdown)
        else:
            markdown_parts.append(f"\n---\n\n{markdown}")

    combined_markdown = "".join(markdown_parts)

    # Save to file
    saved = client.save_task_file(day_dir, combined_markdown, force=force)

    if saved:
        print(f"✅ Downloaded task description for day {day} ({len(articles)} part(s))")
    else:
        print("⏭️  Skipped task.md (already exists)")


def scaffold_day(
    day: int,
    overwrite: bool = False,
    session_token: str | None = None,
    year: int | None = None,
) -> list[str]:
    """
    Create folder structure and files for a given day.

    Args:
        day: Day number (1-25)
        overwrite: If True, overwrite existing files
        session_token: AOC session token for downloads (optional)
        year: AOC year (optional, defaults to current year)

    Returns:
        List of created file paths
    """
    day_folder = Path(f"day-{day:02d}")
    day_folder.mkdir(parents=True, exist_ok=True)

    created_files = []

    # Download input if session token or year provided
    input_content = _download_puzzle_input(day, session_token, year)

    # Download task description if year provided
    _download_task_description(day, str(day_folder), session_token, year, force=overwrite)

    # Define files to create
    files = {
        "solution.py": _get_solution_template(day),
        "test_solution.py": _get_test_template(day),
        "input.txt": input_content,
        "test_input.txt": _get_test_input_placeholder(),
        "README.md": _get_readme_template(day),
    }

    for filename, content in files.items():
        filepath = day_folder / filename

        # Check if file exists
        if filepath.exists() and not overwrite:
            print(f"⏭️  Skipped {filepath} (already exists)")
            continue

        # Write file
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        created_files.append(str(filepath))
        print(f"✅ Created {filepath}")

    return created_files


def scaffold_multi_test_inputs(day: int, count: int) -> list[str]:
    """
    Create multiple test input files for puzzles with multiple examples.

    Args:
        day: Day number (1-25)
        count: Number of test input files to create (2, 3, ...)

    Returns:
        List of created file paths
    """
    day_folder = Path(f"day-{day:02d}")
    day_folder.mkdir(parents=True, exist_ok=True)

    created_files = []

    for n in range(2, count + 1):
        filepath = day_folder / f"test_input_{n}.txt"

        if filepath.exists():
            print(f"⏭️  Skipped {filepath} (already exists)")
            continue

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(_get_test_input_placeholder(n))

        created_files.append(str(filepath))
        print(f"✅ Created {filepath}")

    return created_files


def _get_solution_template(day: int) -> str:
    """Generate solution.py template."""
    return f'''"""Advent of Code 2025 - Day {day:02d} Solution."""

from pathlib import Path


def parse_input(input_text: str):
    """Parse the puzzle input."""
    lines = input_text.strip().split("\\n")
    # TODO: Parse input according to puzzle requirements
    return lines


def solve_part1(data) -> int:
    """Solve Part 1 of the puzzle."""
    # TODO: Implement Part 1 solution
    return 0


def solve_part2(data) -> int:
    """Solve Part 2 of the puzzle."""
    # TODO: Implement Part 2 solution
    return 0


def main():
    """Main entry point."""
    input_file = Path(__file__).parent / "input.txt"
    input_text = input_file.read_text()
    
    data = parse_input(input_text)
    
    part1_answer = solve_part1(data)
    print(f"Part 1: {{part1_answer}}")
    
    part2_answer = solve_part2(data)
    print(f"Part 2: {{part2_answer}}")


if __name__ == "__main__":
    main()
'''


def _get_test_template(day: int) -> str:
    """Generate test_solution.py template."""
    return f'''"""Tests for Advent of Code 2025 - Day {day:02d}."""

from pathlib import Path

import pytest

from .solution import parse_input, solve_part1, solve_part2


@pytest.fixture
def test_input():
    """Load test input."""
    test_file = Path(__file__).parent / "test_input.txt"
    return test_file.read_text()


@pytest.fixture
def parsed_test_data(test_input):
    """Parse test input."""
    return parse_input(test_input)


def test_parse_input(test_input):
    """Test input parsing."""
    data = parse_input(test_input)
    assert data is not None
    # TODO: Add specific parsing assertions


def test_part1(parsed_test_data):
    """Test Part 1 with example input."""
    result = solve_part1(parsed_test_data)
    # TODO: Replace with expected answer from puzzle
    expected = 0
    assert result == expected, f"Expected {{expected}}, got {{result}}"


def test_part2(parsed_test_data):
    """Test Part 2 with example input."""
    result = solve_part2(parsed_test_data)
    # TODO: Replace with expected answer from puzzle
    expected = 0
    assert result == expected, f"Expected {{expected}}, got {{result}}"
'''


def _get_test_input_placeholder(number: int = 1) -> str:
    """Generate test input placeholder."""
    suffix = f" #{number}" if number > 1 else ""
    return f"""# TODO: Add example input{suffix} from puzzle description
# This file should contain the sample input provided in the puzzle.
# Update this once you read the puzzle!
"""


def _get_readme_template(day: int) -> str:
    """Generate README.md template."""
    return f"""# Day {day:02d}

## Puzzle Description

[Add puzzle description here or link to adventofcode.com]

## Notes

- Part 1: 
- Part 2: 

## Usage

```powershell
# Run tests (RED phase)
uv run pytest day-{day:02d}/test_solution.py -v

# Run solution (GREEN phase)
uv run python day-{day:02d}/solution.py
```
"""
