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


# ============================================================================
# PART 2: Extended Pattern Detection (At Least Twice)
# ============================================================================


def is_invalid_id_part2(num: int) -> bool:
    """Check if a number is invalid using Part 2 rules.

    A number is invalid if it consists of a digit sequence repeated
    at least twice (e.g., 111 = "1"×3, 565656 = "56"×3).

    Args:
        num: Product ID to check

    Returns:
        True if invalid (repeated pattern ≥2), False otherwise

    Examples:
        >>> is_invalid_id_part2(11)
        True
        >>> is_invalid_id_part2(111)
        True
        >>> is_invalid_id_part2(565656)
        True
        >>> is_invalid_id_part2(101)
        False
    """
    s = str(num)
    n = len(s)

    # Check all possible pattern lengths (1 to n/2)
    for pattern_len in range(1, n // 2 + 1):
        if n % pattern_len == 0:  # Length divisible by pattern
            pattern = s[:pattern_len]
            repetitions = n // pattern_len

            # Check if repeating pattern forms the string
            if pattern * repetitions == s and repetitions >= 2:
                return True  # Found repeated pattern

    return False  # No repeated pattern found


def check_range_part2(start: int, end: int) -> list[int]:
    """Find all invalid IDs in a range using Part 2 rules.

    Args:
        start: First ID in range (inclusive)
        end: Last ID in range (inclusive)

    Returns:
        List of invalid product IDs in the range

    Examples:
        >>> check_range_part2(11, 22)
        [11, 22]
        >>> check_range_part2(95, 115)
        [99, 111]
    """
    invalid = []
    for num in range(start, end + 1):
        if is_invalid_id_part2(num):
            invalid.append(num)
    return invalid


def solve_part2(input_text: str) -> int:
    """Solve Part 2: Sum all invalid product IDs.

    Args:
        input_text: Comma-separated ID ranges (e.g., "11-22,95-115")

    Returns:
        Sum of all invalid product IDs across all ranges

    Examples:
        >>> solve_part2("11-22")
        33
        >>> solve_part2("11-22,95-115")
        243
    """
    ranges = parse_ranges(input_text)  # Reuse Part 1 parser
    total = 0

    for start, end in ranges:
        invalid_ids = check_range_part2(start, end)
        total += sum(invalid_ids)

    return total


def main():
    """Main entry point."""
    import sys

    input_file = Path(__file__).parent / "input.txt"
    input_text = input_file.read_text().strip()

    # Parse --part argument
    part = 1
    if len(sys.argv) > 1 and sys.argv[1] == "--part":
        if len(sys.argv) > 2:
            part = int(sys.argv[2])
    elif len(sys.argv) > 1:
        # Also accept just "--part 2" format
        for i, arg in enumerate(sys.argv[1:]):
            if arg == "--part" and i + 1 < len(sys.argv) - 1:
                part = int(sys.argv[i + 2])

    if part == 1:
        part1_answer = solve_part1(input_text)
        print(f"Part 1: {part1_answer}")
    elif part == 2:
        part2_answer = solve_part2(input_text)
        print(f"Part 2: {part2_answer}")
    else:
        print(f"Unknown part: {part}")
        sys.exit(1)


if __name__ == "__main__":
    main()
