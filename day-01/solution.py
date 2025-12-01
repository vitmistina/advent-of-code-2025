"""Advent of Code 2025 - Day 01 Solution."""

from pathlib import Path


def parse_input(input_text: str) -> list[tuple[str, int]]:
    """
    Parse the puzzle input into list of (direction, distance) tuples.

    Args:
        input_text: Multi-line string containing rotation instructions.
                   Each line format: <direction><distance> (e.g., "L68", "R48")

    Returns:
        List of (direction, distance) tuples where:
        - direction: 'L' or 'R'
        - distance: integer number of clicks

    Example:
        >>> parse_input("L68\\nR48")
        [('L', 68), ('R', 48)]
    """
    if not input_text.strip():
        return []

    rotations = []
    for line in input_text.strip().split("\n"):
        if not line.strip():
            continue
        direction = line[0]
        distance = int(line[1:])
        rotations.append((direction, distance))
    return rotations


def apply_rotation(position: int, direction: str, distance: int) -> int:
    """
    Apply a single rotation to the dial and return new position.

    The dial is circular with positions 0-99. Left rotation decreases position,
    right rotation increases position, with wraparound at boundaries.

    Args:
        position: Current dial position (0-99)
        direction: 'L' for left (decrease) or 'R' for right (increase)
        distance: Number of clicks to rotate

    Returns:
        New dial position after rotation (0-99)

    Examples:
        >>> apply_rotation(50, 'L', 68)
        82
        >>> apply_rotation(99, 'R', 1)
        0
        >>> apply_rotation(5, 'L', 10)
        95
    """
    if direction == "L":
        return (position - distance) % 100
    else:  # direction == "R"
        return (position + distance) % 100


def solve_part1(rotations: list[tuple[str, int]]) -> int:
    """
    Solve Part 1: Count how many times dial points at 0 after rotations.

    The dial starts at position 50. For each rotation in sequence:
    1. Apply the rotation to get new position
    2. If new position is 0, increment the count

    Args:
        rotations: List of (direction, distance) tuples

    Returns:
        Number of times the dial pointed at 0 after any rotation

    Example:
        >>> rotations = [('L', 68), ('L', 30), ('R', 48)]
        >>> solve_part1(rotations)
        1
    """
    position = 50  # Dial starts at 50
    zero_count = 0

    for direction, distance in rotations:
        position = apply_rotation(position, direction, distance)
        if position == 0:
            zero_count += 1

    return zero_count


def count_zero_crossings_during_rotation(start_position: int, direction: str, distance: int) -> int:
    """
    Count how many times position 0 is reached during rotation.

    This counts ALL times we hit position 0 during the rotation, INCLUDING
    if we end at position 0.

    Time complexity: O(1)
    Space complexity: O(1)

    Args:
        start_position: Current dial position (0-99)
        direction: 'L' for left (decrease) or 'R' for right (increase)
        distance: Number of clicks to rotate

    Returns:
        Number of times position 0 is reached during rotation

    Examples:
        >>> count_zero_crossings_during_rotation(50, 'R', 1000)
        10
        >>> count_zero_crossings_during_rotation(99, 'R', 1)
        1
        >>> count_zero_crossings_during_rotation(52, 'R', 48)
        1
        >>> count_zero_crossings_during_rotation(0, 'R', 848)
        8
    """
    if distance == 0:
        return 0

    if direction not in ("L", "R"):
        raise ValueError(f"Direction must be 'L' or 'R', got: {direction}")

    start_position = start_position % 100

    if direction == "R":
        # Right rotation: count how many times we hit 0
        # Each time we complete 100 clicks from our starting point, we return to 0
        # Example: start=0, R848 hits 0 at clicks 100,200,300,400,500,600,700,800 = 8 times
        # Formula: (0 + 848) // 100 = 8 ✓

        # Example: start=52, R48 ends at 0 (after 48 clicks). We hit 0 once.
        # Formula: (52 + 48) // 100 = 1 ✓

        total_crossings = (start_position + distance) // 100
        return total_crossings
    else:  # 'L'
        # Left rotation: count how many times we hit 0
        # Special case: if we start at 0, we go 0→99→98→...
        # We hit 0 again after 100 clicks, then every 100 clicks
        # Example: start=0, L241 hits 0 at clicks 100, 200 = 2 times
        # Formula: 241 // 100 = 2 ✓

        if start_position == 0:
            return distance // 100

        # General case: start at position P, go left D clicks
        # Example: start=50, L60 hits 0 once (after 50 clicks)
        # We need to figure out: how many times do we cross 0?
        # Going left from 50: takes 50 clicks to reach 0, then we have 10 more clicks
        # Total crossings: 1
        # Formula: We hit 0 first after start_position clicks (if distance >= start_position)
        #          Then every 100 clicks after that

        if distance < start_position:
            return 0

        # First crossing at start_position clicks, then every 100 after that
        remaining_after_first = distance - start_position
        additional_crossings = remaining_after_first // 100
        total_crossings = 1 + additional_crossings

        return total_crossings

        return total_crossings


def solve_part2(rotations: list[tuple[str, int]]) -> int:
    """
    Solve Part 2: Count all clicks where dial points at 0.

    Counts EVERY CLICK where position is 0:
    - During each rotation (all intermediate positions)
    - After each rotation (final position)

    Time complexity: O(n) where n = number of rotations
    Space complexity: O(1)

    Args:
        rotations: List of (direction, distance) tuples

    Returns:
        Total number of times the dial pointed at 0 (during + after rotations)
    """
    position = 50  # Dial starts at 50
    total_zero_count = 0

    for direction, distance in rotations:
        # Count ALL zeros during rotation (including if we end at 0)
        zero_count = count_zero_crossings_during_rotation(position, direction, distance)
        total_zero_count += zero_count

        # Apply rotation to get new position
        position = apply_rotation(position, direction, distance)

        # Count if ended at 0
        if position == 0:
            total_zero_count += 1

    return total_zero_count


def main():
    """Main entry point."""
    input_file = Path(__file__).parent / "input.txt"
    input_text = input_file.read_text()

    data = parse_input(input_text)

    part1_answer = solve_part1(data)
    print(f"Part 1: {part1_answer}")

    part2_answer = solve_part2(data)
    print(f"Part 2: {part2_answer}")


if __name__ == "__main__":
    main()
