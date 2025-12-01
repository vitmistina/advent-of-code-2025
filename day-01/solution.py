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
    Count how many times position 0 is crossed during rotation.

    This counts intermediate crossings DURING the rotation, not including
    the start or end positions.

    Time complexity: O(1)
    Space complexity: O(1)

    Args:
        start_position: Current dial position (0-99)
        direction: 'L' for left (decrease) or 'R' for right (increase)
        distance: Number of clicks to rotate

    Returns:
        Number of times position 0 is crossed during rotation

    Examples:
        >>> count_zero_crossings_during_rotation(50, 'R', 1000)
        10
        >>> count_zero_crossings_during_rotation(99, 'R', 1)
        1
        >>> count_zero_crossings_during_rotation(50, 'L', 60)
        1
    """
    if distance == 0:
        return 0

    if direction not in ("L", "R"):
        raise ValueError(f"Direction must be 'L' or 'R', got: {direction}")

    start_position = start_position % 100

    if direction == "R":
        # Right rotation: count how many times we pass through 0 DURING rotation
        # Not including the final position
        end_position = (start_position + distance) % 100
        total_crossings = (start_position + distance) // 100

        # If we start at 0, the first "crossing" is just the starting position
        if start_position == 0 and total_crossings > 0:
            total_crossings -= 1

        # If we end at 0, don't count it (it's the end position, not during)
        if end_position == 0 and total_crossings > 0:
            total_crossings -= 1

        return total_crossings
    else:  # 'L'
        # Left rotation: count how many times we cross 0 going backward
        # Not including start or end positions
        if start_position == 0:
            return 0
        if distance < start_position:
            return 0

        # Calculate end position
        end_position = (start_position - distance) % 100

        # First crossing happens when we reach 0 from above
        remaining_after_first_cross = distance - start_position
        additional_crossings = remaining_after_first_cross // 100
        total_crossings = 1 + additional_crossings

        # If we end exactly at 0, don't count it (it's the end position, not during)
        if end_position == 0:
            total_crossings -= 1

        return total_crossings


def solve_part2(rotations: list[tuple[str, int]]) -> int:
    """
    Solve Part 2: Count all clicks where dial points at 0.

    Counts both:
    1. Zero crossings DURING rotations (intermediate positions)
    2. Zero end-positions AFTER rotations (final positions)

    Time complexity: O(n) where n = number of rotations
    Space complexity: O(1)

    Args:
        rotations: List of (direction, distance) tuples

    Returns:
        Total number of times the dial pointed at 0 (during + after rotations)

    Example:
        >>> rotations = [('L', 68), ('R', 48), ('L', 55)]
        >>> solve_part2(rotations)
        # Returns count of all zero crossings
    """
    position = 50  # Dial starts at 50
    total_zero_count = 0

    for direction, distance in rotations:
        # Count zeros crossed DURING rotation
        during_count = count_zero_crossings_during_rotation(position, direction, distance)
        total_zero_count += during_count

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
