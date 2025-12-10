"""
Day 7 Part 1: Tachyon Beam Split Counter

This module simulates the movement of tachyon beams through a manifold diagram
and counts the number of times beams are split.

Algorithm: Queue-based BFS with state tracking
- Beams are represented as (row, col, direction) tuples
- A visited set tracks processed states to prevent reprocessing and enable beam merging
- Each splitter encounter counts as one split
"""

from collections import deque

# Direction constants: (delta_row, delta_col)
DOWN = (1, 0)  # Tachyon beams always start moving down
LEFT = (0, -1)  # Emitted from splitter
RIGHT = (0, 1)  # Emitted from splitter


def parse_grid(filename: str) -> tuple[list[str], tuple[int, int]]:
    """
    Parse the grid from an input file and find the starting position 'S'.

    Args:
        filename: Path to the input file

    Returns:
        Tuple of (grid, start_position) where:
        - grid: List of strings, each representing a row
        - start_position: (row, col) tuple for the 'S' character

    Raises:
        ValueError: If no starting position 'S' is found
    """
    with open(filename) as f:
        grid = [line.rstrip("\n") for line in f]

    # Find starting position 'S'
    start_pos = None
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == "S":
                start_pos = (row, col)
                break
        if start_pos:
            break

    if start_pos is None:
        raise ValueError(f"No starting position 'S' found in {filename}")

    return grid, start_pos


def simulate_beams(grid: list[str], start_pos: tuple[int, int]) -> int:
    """
    Simulate tachyon beams moving through the grid and count splits.

    Uses a queue-based BFS approach:
    1. Start with one beam at 'S' moving DOWN
    2. Process each beam: move it one step in its direction
    3. Check the cell at the new position:
       - '.': Continue moving in same direction
       - '^': Split event - increment split count, emit two beams that continue DOWN
               from the left and right columns of the splitter
       - Out of bounds: Discard beam
    4. Track visited states (row, col, direction) to detect beam merging

    When two beams reach the same (row, col, direction), they merge into one
    and are processed only once (the duplicate is skipped).

    The key insight: When a beam hits a splitter '^', it stops.
    Two new beams are created that continue DOWNWARD:
    - One from the column to the left (col - 1)
    - One from the column to the right (col + 1)

    Args:
        grid: List of strings representing the manifold
        start_pos: (row, col) tuple for the starting position 'S'

    Returns:
        Integer count of beam splits (number of times a splitter is encountered)
    """
    # Initialize queue with the starting beam
    queue = deque([(start_pos[0], start_pos[1], DOWN)])
    visited: set[tuple[int, int, tuple[int, int]]] = set()
    split_count = 0

    while queue:
        row, col, direction = queue.popleft()

        # Skip if this state was already processed (beam merging)
        if (row, col, direction) in visited:
            continue
        visited.add((row, col, direction))

        # Move the beam in its current direction
        dr, dc = direction
        new_row = row + dr
        new_col = col + dc

        # Check if the new position is within bounds
        if not (0 <= new_row < len(grid) and 0 <= new_col < len(grid[0])):
            # Beam exits the grid
            continue

        cell = grid[new_row][new_col]

        if cell == "." or cell == "S":
            # Empty space or start: continue moving in the same direction
            queue.append((new_row, new_col, direction))
        elif cell == "^":
            # Splitter: count the split and emit two new beams
            # Both new beams continue DOWNWARD from different columns
            split_count += 1
            queue.append((new_row, new_col - 1, DOWN))  # Left beam
            queue.append((new_row, new_col + 1, DOWN))  # Right beam

    return split_count


def count_splits(filename: str) -> int:
    """
    Count the number of beam splits in a manifold diagram.

    This is the main entry point that:
    1. Parses the input file to extract the grid and starting position
    2. Simulates beam movement and splitting
    3. Returns the total split count

    Args:
        filename: Path to the input file

    Returns:
        Integer count of beam splits
    """
    grid, start_pos = parse_grid(filename)
    return simulate_beams(grid, start_pos)


if __name__ == "__main__":
    # Run on test input
    test_result = count_splits("day-07/test_input.txt")
    print(f"Test input result: {test_result}")

    # Run on main input
    main_result = count_splits("day-07/input.txt")
    print(f"Main input result: {main_result}")
