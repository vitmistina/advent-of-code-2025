"""Advent of Code 2025 - Day 11 Solution.

This solution implements a pathfinding algorithm to find and count all distinct
paths from device "you" to device "out" in a directed graph of reactor devices.
"""

from pathlib import Path


def parse_device_config(config_text: str) -> dict[str, list[str]]:
    """Parse device configuration into a dictionary of connections.

    Args:
        config_text: Configuration text where each line is formatted as
                    'device: output1 output2 ...'

    Returns:
        Dictionary mapping device names to lists of output device names.
        Includes all devices appearing in the configuration, even if they
        only appear as destinations (with empty output lists).
    """
    connections = {}
    devices = set()

    # First pass: parse all connections and collect all device names
    for line in config_text.strip().split("\n"):
        if not line.strip():
            continue

        parts = line.split(":")
        if len(parts) != 2:
            continue

        source = parts[0].strip()
        destinations_str = parts[1].strip()

        devices.add(source)

        if destinations_str:
            destinations = destinations_str.split()
            connections[source] = destinations
            devices.update(destinations)
        else:
            connections[source] = []

    # Ensure all devices have an entry in connections dict
    for device in devices:
        if device not in connections:
            connections[device] = []

    return connections


def build_graph(connections: dict[str, list[str]]) -> dict[str, list[str]]:
    """Build a directed graph from device connections.

    Args:
        connections: Dictionary mapping device names to output lists

    Returns:
        Adjacency list representation of the graph (same as input in this case,
        since connections is already in the required format)
    """
    return connections


def find_single_path(graph: dict[str, list[str]], start: str, end: str) -> list[str] | None:
    """Find a single path from start to end using DFS.

    Args:
        graph: Adjacency list dictionary
        start: Starting device name
        end: Target device name

    Returns:
        A path from start to end as a list of device names, or None if no path exists
    """
    visited = set()

    def dfs(node: str, path: list[str]) -> list[str] | None:
        if node == end:
            return path

        visited.add(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                result = dfs(neighbor, path + [neighbor])
                if result:
                    return result

        visited.remove(node)
        return None

    return dfs(start, [start])


def find_all_paths(graph: dict[str, list[str]], start: str, end: str) -> list[list[str]]:
    """Find all paths from start to end using DFS with backtracking.

    Args:
        graph: Adjacency list dictionary
        start: Starting device name
        end: Target device name

    Returns:
        List of all paths from start to end, where each path is a list of device names
    """
    paths = []

    def dfs(node: str, path: list[str], visited: set[str]) -> None:
        if node == end:
            paths.append(path[:])
            return

        visited.add(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                path.append(neighbor)
                dfs(neighbor, path, visited)
                path.pop()

        visited.remove(node)

    visited = {start}
    dfs(start, [start], visited)

    return paths


def display_paths(paths: list[list[str]]) -> list[str]:
    """Format paths for display.

    Args:
        paths: List of paths, where each path is a list of device names

    Returns:
        List of formatted path strings (e.g., "you → bbb → ddd → out")
    """
    return [" → ".join(path) for path in paths]


def solve_part1(input_text: str) -> int:
    """Solve Part 1 of the puzzle.

    Counts the total number of distinct paths from device "you" to device "out".

    Args:
        input_text: The puzzle input as text

    Returns:
        The count of distinct paths
    """
    connections = parse_device_config(input_text)
    graph = build_graph(connections)

    # Check if required devices exist
    if "you" not in graph or "out" not in graph:
        return 0

    paths = find_all_paths(graph, "you", "out")
    return len(paths)


def solve_part2(data) -> int:
    """Solve Part 2 of the puzzle.

    TODO: Implement Part 2 solution
    """
    return 0


def main():
    """Main entry point."""
    input_file = Path(__file__).parent / "input.txt"
    input_text = input_file.read_text()

    part1_answer = solve_part1(input_text)
    print(f"Part 1: {part1_answer}")

    part2_answer = solve_part2(input_text)
    print(f"Part 2: {part2_answer}")


if __name__ == "__main__":
    main()
