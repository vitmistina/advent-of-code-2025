"""Day 8 Part 1: Circuit Analysis - Connecting Junction Boxes with Union-Find.

Solves Advent of Code 2025 Day 8 Part 1 by:
1. Parsing 3D junction box coordinates from input
2. Computing all pairwise Euclidean distances
3. Connecting closest pairs using Union-Find algorithm
4. Computing product of three largest circuit sizes
"""

import math
from pathlib import Path

# Type aliases
JunctionBox = tuple[int, int, int]  # (x, y, z) coordinates
DistancePair = tuple[float, int, int]  # (distance, id_a, id_b)


def parse_input(input_data: str) -> list[JunctionBox]:
    """Parse input into list of (x, y, z) tuples.

    Args:
        input_data: Newline-separated lines of "X,Y,Z" coordinates

    Returns:
        List of (x, y, z) tuples, indexed by junction box ID
    """
    points = []
    for line in input_data.strip().split("\n"):
        if line:
            x, y, z = map(int, line.split(","))
            points.append((x, y, z))
    return points


def euclidean_distance(point_a: JunctionBox, point_b: JunctionBox) -> float:
    """Calculate Euclidean distance between two 3D points.

    Args:
        point_a: First 3D point (x, y, z)
        point_b: Second 3D point (x, y, z)

    Returns:
        Euclidean distance as float
    """
    dx = point_b[0] - point_a[0]
    dy = point_b[1] - point_a[1]
    dz = point_b[2] - point_a[2]
    return math.sqrt(dx * dx + dy * dy + dz * dz)


def compute_all_distances(points: list[JunctionBox]) -> list[DistancePair]:
    """Compute all pairwise distances and return sorted list.

    Args:
        points: List of junction box coordinates

    Returns:
        Sorted list of (distance, id_a, id_b) tuples, ascending by distance
    """
    distances = []
    n = len(points)

    for i in range(n):
        for j in range(i + 1, n):
            dist = euclidean_distance(points[i], points[j])
            distances.append((dist, i, j))

    # Sort by distance (ascending)
    distances.sort(key=lambda x: x[0])

    return distances


def find_circuit(point_id: int, circuits: dict[str, set[int]]) -> str | None:
    """Find which circuit contains the given point ID.

    Args:
        point_id: Junction box ID to search for
        circuits: Dictionary of circuit_name -> set of point IDs

    Returns:
        Circuit name containing the point, or None if not found
    """
    for circuit_name, members in circuits.items():
        if point_id in members:
            return circuit_name
    return None


def process_connections(
    sorted_distances: list[DistancePair], num_points: int, num_connections: int
) -> dict[str, set[int]]:
    """Process connections to build circuits using Union-Find approach.

    Args:
        sorted_distances: List of (distance, id_a, id_b) sorted by distance
        num_points: Total number of junction boxes
        num_connections: Number of closest pairs to process (including skipped pairs)

    Returns:
        Dictionary of circuit_name -> set of point IDs
    """
    circuits: dict[str, set[int]] = {}
    next_circuit_id = 0

    # Process the N closest pairs (count attempts, not actual connections)
    for _distance, point_a, point_b in sorted_distances[:num_connections]:
        circuit_a = find_circuit(point_a, circuits)
        circuit_b = find_circuit(point_b, circuits)

        if circuit_a is None and circuit_b is None:
            # Both unassigned: create new circuit
            circuits[f"circuit_{next_circuit_id}"] = {point_a, point_b}
            next_circuit_id += 1
        elif circuit_a is not None and circuit_b is None:
            # Point B joins circuit A
            circuits[circuit_a].add(point_b)
        elif circuit_a is None and circuit_b is not None:
            # Point A joins circuit B
            circuits[circuit_b].add(point_a)
        elif circuit_a != circuit_b:
            # Merge two circuits
            circuits[circuit_a].update(circuits[circuit_b])
            del circuits[circuit_b]
        # else: both in same circuit, skip (but still counts as one of the N pairs processed)

    # Add singleton circuits for unconnected points
    for point_id in range(num_points):
        if find_circuit(point_id, circuits) is None:
            circuits[f"circuit_{next_circuit_id}"] = {point_id}
            next_circuit_id += 1

    return circuits


def get_three_largest_sizes(circuits: dict[str, set[int]]) -> list[int]:
    """Get sizes of three largest circuits.

    Args:
        circuits: Dictionary of circuit_name -> set of point IDs

    Returns:
        List of three largest circuit sizes in descending order
    """
    sizes = sorted([len(members) for members in circuits.values()], reverse=True)
    return sizes[:3]


def solve_part1(input_data: str, num_connections: int = 1000) -> int:
    """Solve Part 1 of the puzzle.

    Args:
        input_data: Input text containing junction box coordinates
        num_connections: Number of connections to make (default 1000)

    Returns:
        Product of three largest circuit sizes
    """
    # Parse input
    points = parse_input(input_data)

    # Compute all distances
    distances = compute_all_distances(points)

    # Build circuits
    circuits = process_connections(distances, len(points), num_connections)

    # Get three largest sizes
    largest_three = get_three_largest_sizes(circuits)

    # Return product
    return largest_three[0] * largest_three[1] * largest_three[2]


def main():
    """Main entry point."""
    input_file = Path(__file__).parent / "input.txt"
    input_text = input_file.read_text()

    answer = solve_part1(input_text)
    print(f"Part 1: {answer}")


if __name__ == "__main__":
    main()
