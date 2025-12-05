from dataclasses import dataclass


@dataclass
class FreshRange:
    start: int
    end: int

    def __post_init__(self):
        if self.start > self.end:
            raise ValueError(f"Invalid FreshRange: start ({self.start}) > end ({self.end})")


def merge_ranges(ranges: list[FreshRange]) -> list[tuple[int, int]]:
    """
    Merge overlapping and adjacent FreshRange intervals into sorted, disjoint
    list of (start, end) tuples. Runs in O(R log R) time where R is the number
    of ranges.
    """
    if not ranges:
        return []
    # Sort ranges by start
    sorted_ranges = sorted(ranges, key=lambda r: r.start)
    merged = []
    for r in sorted_ranges:
        if not merged:
            merged.append((r.start, r.end))
        else:
            last_start, last_end = merged[-1]
            if r.start <= last_end + 1:
                merged[-1] = (last_start, max(last_end, r.end))
            else:
                merged.append((r.start, r.end))
    return merged


def parse_database(data: str) -> tuple[list[FreshRange], list[int]]:
    """
    Parse the database string into a list of FreshRange objects and a list of ingredient IDs.
    Splits input on first blank line (\n\n). Raises ValueError for malformed input.
    """
    if not isinstance(data, str):
        raise ValueError("Input data must be a string.")
    
    # Split on blank line if it exists
    parts = data.strip().split("\n\n", 1)
    header = parts[0]
    ids_section = parts[1] if len(parts) > 1 else ""
    
    ranges = []
    for line in header.strip().splitlines():
        if not line.strip():
            continue
        try:
            start, end = map(int, line.strip().split("-"))
            ranges.append(FreshRange(start, end))
        except ValueError as e:
            raise ValueError(f"Malformed range line: '{line}'") from e
    ids_list = []
    for line in ids_section.strip().splitlines():
        if not line.strip():
            continue
        try:
            ids_list.append(int(line.strip()))
        except ValueError as e:
            raise ValueError(f"Malformed ingredient ID line: '{line}'") from e
    return ranges, ids_list


def is_fresh(ingredient_id: int, merged_ranges: list[tuple[int, int]]) -> bool:
    """
    Determine if an ingredient ID is fresh by checking if it falls within any merged range.
    Uses binary search for O(log R) lookup where R is the number of merged ranges.

    Args:
        ingredient_id: The ingredient ID to check
        merged_ranges: Sorted, disjoint list of (start, end) tuples representing fresh ranges

    Returns:
        True if the ingredient is fresh (within any range), False otherwise
    """
    if not merged_ranges:
        return False

    # Binary search for the range that might contain ingredient_id
    left, right = 0, len(merged_ranges) - 1

    while left <= right:
        mid = (left + right) // 2
        start, end = merged_ranges[mid]

        if start <= ingredient_id <= end:
            return True
        elif ingredient_id < start:
            right = mid - 1
        else:
            left = mid + 1

    return False


def solve_part1(data: str) -> int:
    """
    Solve Day 5 Part 1: Count how many available ingredients are fresh.

    Integrates parsing, range merging, and freshness checking to determine
    the count of fresh ingredients from the database.

    Time complexity: O(R log R + I log R) where R is the number of ranges
    and I is the number of ingredient IDs.

    Args:
        data: The database string containing fresh ranges and ingredient IDs

    Returns:
        The count of fresh ingredients
    """
    # Parse the database
    ranges, ingredient_ids = parse_database(data)

    # Merge overlapping ranges
    merged = merge_ranges(ranges)

    # Count fresh ingredients
    count = 0
    for ingredient_id in ingredient_ids:
        if is_fresh(ingredient_id, merged):
            count += 1

    return count


def parse_ranges_part2(data: str) -> list[FreshRange]:
    """
    Parse only the fresh ID ranges from the input, ignoring available IDs section.
    For Part 2, we only care about ranges (before the blank line).

    Args:
        data: The database string containing fresh ranges and available IDs

    Returns:
        A list of FreshRange objects

    Raises:
        ValueError: If ranges section is malformed
    """
    if not isinstance(data, str):
        raise ValueError("Input data must be a string.")
    
    # Split on blank line if it exists, otherwise use entire input as ranges
    parts = data.strip().split("\n\n", 1)
    header = parts[0]
    
    ranges = []
    for line in header.strip().splitlines():
        if not line.strip():
            continue
        try:
            start, end = map(int, line.strip().split("-"))
            ranges.append(FreshRange(start, end))
        except ValueError as e:
            raise ValueError(f"Malformed range line: '{line}'") from e
    return ranges


def solve_part2(data: str) -> int:
    """
    Solve Day 5 Part 2: Count all unique ingredient IDs that are fresh.

    Calculates the total count of unique fresh IDs across all merged ranges.
    The available IDs section is completely ignored.

    Time complexity: O(R log R) where R is the number of ranges.

    Args:
        data: The database string containing fresh ranges and available IDs

    Returns:
        The count of all unique fresh ingredient IDs across all ranges
    """
    # Parse only ranges (ignore available IDs)
    ranges = parse_ranges_part2(data)

    # Merge overlapping ranges into disjoint intervals
    merged = merge_ranges(ranges)

    # Sum the count of IDs in each merged range
    total_count = 0
    for start, end in merged:
        total_count += end - start + 1

    return total_count


if __name__ == "__main__":
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(description="Advent of Code 2025 - Day 5")
    parser.add_argument("--part", type=int, choices=[1, 2], default=1, help="Which part to solve")
    parser.add_argument("--test", action="store_true", help="Use test input instead of real input")
    args = parser.parse_args()

    # Determine input file
    day_dir = Path(__file__).parent
    input_file = day_dir / ("test_input.txt" if args.test else "input.txt")

    # Load input
    with open(input_file) as f:
        data = f.read()

    # Solve
    if args.part == 1:
        result = solve_part1(data)
        print(f"Part 1: {result}")
    else:
        result = solve_part2(data)
        print(f"Part 2: {result}")
