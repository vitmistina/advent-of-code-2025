"""Advent of Code 2025 - Day 02 Part 1 Solution.

Gift Shop Invalid Product ID Detection.
"""

from pathlib import Path


def is_invalid_id(num: int) -> bool:
    """Check if number is formed by repeating a digit sequence twice.

    A number is invalid if it consists of a digit sequence repeated exactly
    twice. Examples: 55 (5+5), 6464 (64+64), 123123 (123+123).

    Args:
        num: Integer product ID to validate

    Returns:
        True if ID is invalid (matches pattern), False otherwise

    Examples:
        >>> is_invalid_id(55)
        True
        >>> is_invalid_id(6464)
        True
        >>> is_invalid_id(123123)
        True
        >>> is_invalid_id(101)
        False
        >>> is_invalid_id(1234)
        False
    """
    s = str(num)
    # Must have even length to split evenly
    if len(s) % 2 != 0:
        return False
    # Split in half and compare
    mid = len(s) // 2
    return s[:mid] == s[mid:]


def find_invalid_ids_in_range(start: int, end: int) -> list[int]:
    """Find all invalid IDs in inclusive range [start, end].

    Args:
        start: First ID in range (inclusive)
        end: Last ID in range (inclusive)

    Returns:
        List of invalid product IDs found in range, in ascending order

    Examples:
        >>> find_invalid_ids_in_range(11, 22)
        [11, 22]
        >>> find_invalid_ids_in_range(95, 115)
        [99]
        >>> find_invalid_ids_in_range(998, 1012)
        [1010]
    """
    invalid_ids = []
    for num in range(start, end + 1):
        if is_invalid_id(num):
            invalid_ids.append(num)
    return invalid_ids


def parse_ranges(input_text: str) -> list[tuple[int, int]]:
    """Parse comma-separated ranges into list of (start, end) tuples.

    Args:
        input_text: String containing comma-separated ranges.
                   Format: "start1-end1,start2-end2,..."
                   Example: "11-22,95-115,998-1012"

    Returns:
        List of (start, end) tuples where start and end are integers.
        Example: [(11, 22), (95, 115), (998, 1012)]

    Examples:
        >>> parse_ranges("11-22,95-115")
        [(11, 22), (95, 115)]
        >>> parse_ranges("998-1012")
        [(998, 1012)]
        >>> parse_ranges("")
        []
    """
    if not input_text.strip():
        return []

    ranges = []
    for range_str in input_text.strip().split(","):
        if not range_str.strip():
            continue
        start_str, end_str = range_str.strip().split("-")
        start, end = int(start_str), int(end_str)
        ranges.append((start, end))
    return ranges


def solve_part1(input_text: str) -> int:
    """Solve Part 1: Calculate sum of all invalid IDs from all ranges.

    Args:
        input_text: Comma-separated range input string
                   Example: "11-22,95-115,998-1012"

    Returns:
        Sum of all invalid product IDs found across all ranges

    Examples:
        >>> solve_part1("11-22")
        33
        >>> solve_part1("11-22,95-115,998-1012")
        1142
    """
    ranges = parse_ranges(input_text)
    invalid_ids = []

    for start, end in ranges:
        invalid_ids.extend(find_invalid_ids_in_range(start, end))

    return sum(invalid_ids)


def main():
    """Main entry point."""
    input_file = Path(__file__).parent / "input.txt"
    input_text = input_file.read_text().strip()

    part1_answer = solve_part1(input_text)
    print(f"Part 1: {part1_answer}")


if __name__ == "__main__":
    main()
