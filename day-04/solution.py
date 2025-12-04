"""
Day 4 Part 1: Accessible Paper Rolls Counter

Implements grid parsing, adjacency counting, and accessibility logic.

Functions:
    - parse_grid: Parse input string into grid
    - is_valid_position: Check grid boundaries
    - count_adjacent_rolls: Count neighbors
    - is_accessible: Accessibility logic
    - solve_part1: Main solution
"""

# Direction offsets for 8 adjacent positions
DIRECTIONS: list[tuple[int, int]] = [
    (-1, -1),
    (-1, 0),
    (-1, 1),  # NW, N, NE
    (0, -1),
    (0, 1),  # W,     E
    (1, -1),
    (1, 0),
    (1, 1),  # SW, S, SE
]


def parse_grid(input_data: str) -> list[str]:
    """
    Parse input string into grid representation.

    Example:
        >>> parse_grid("@.@\n...\n@.@")
        ['@.@', '...', '@.@']

    Args:
        input_data: Multiline string containing grid

    Returns:
        List of strings, each representing a row
    """
    input_data = input_data.strip()
    if not input_data:
        return []
    lines = [line.strip() for line in input_data.split("\n") if line.strip()]
    if not lines:
        return []
    width = len(lines[0])
    if any(len(line) != width for line in lines):
        raise ValueError("Grid is not rectangular")
    return lines


def is_valid_position(grid: list[str], row: int, col: int) -> bool:
    """Check if position is within grid boundaries.

    Args:
        grid: The grid representation
        row: Row index to check
        col: Column index to check

    Returns:
        True if position is valid, False otherwise
    """
    if not grid:
        return False
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])


def count_adjacent_rolls(grid: list[str], row: int, col: int) -> int:
    """
    Count paper rolls in 8 adjacent positions.

    Example:
        >>> grid = ['@@@', '@@@', '@@@']
        >>> count_adjacent_rolls(grid, 1, 1)
        8

    Args:
        grid: The grid representation
        row: Row index of center position
        col: Column index of center position

    Returns:
        Number of adjacent paper rolls (0-8)
    """
    count = 0
    for dr, dc in DIRECTIONS:
        nr, nc = row + dr, col + dc
        if is_valid_position(grid, nr, nc) and grid[nr][nc] == "@":
            count += 1
    return count


def is_accessible(adjacent_count: int) -> bool:
    """
    Determine if a paper roll is accessible (< 4 neighbors).

    Example:
        >>> is_accessible(3)
        True
        >>> is_accessible(4)
        False

    Args:
        adjacent_count: Number of adjacent paper rolls

    Returns:
        True if accessible (< 4 neighbors), False otherwise
    """
    return adjacent_count < 4


def solve_part1(input_data: str) -> int:
    """
    Solve Day 4 Part 1: Count accessible paper rolls.

    Example:
        >>> input_data = "@.@\n...\n@.@"
        >>> solve_part1(input_data)
        4

    Args:
        input_data: Multiline string containing grid

    Returns:
        Count of accessible paper rolls
    """
    grid = parse_grid(input_data)
    if not grid:
        return 0
    accessible_count = 0
    for row, row_str in enumerate(grid):
        for col, val in enumerate(row_str):
            if val == "@":
                adjacent = count_adjacent_rolls(grid, row, col)
                if is_accessible(adjacent):
                    accessible_count += 1
    return accessible_count


if __name__ == "__main__":
    # Read input and solve
    with open("day-04/input.txt") as f:
        input_data = f.read()
    result = solve_part1(input_data)
    print(f"Part 1: {result}")
