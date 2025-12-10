# Quickstart Guide: AoC Day 8 Part 1 - Circuit Analysis

**Feature**: 016-day-08-part-1  
**Branch**: `016-day-08-part-1`  
**Last Updated**: December 10, 2025

## Overview

This guide helps you implement the Day 8 Part 1 solution using Test-Driven Development (TDD). The solution uses a dictionary-based grouping approach to connect 3D junction boxes into circuits based on Euclidean distance.

## Prerequisites

- Python 3.10+
- UV package manager
- pytest (already in project dependencies)
- Files already created by meta runner:
  - `day-08/input.txt` (full puzzle input)
  - `day-08/test_input.txt` (example with 20 junction boxes)
  - `day-08/description.md` (challenge description)

## TDD Workflow (RED → GREEN → REFACTOR)

### Phase 0: Setup Test File

**Task**: Create `day-08/test_solution.py` with imports and test structure.

```python
"""Tests for Day 8 Part 1: Circuit Analysis."""

import pytest
from solution import (
    parse_input,
    euclidean_distance,
    compute_all_distances,
    find_circuit,
    process_connections,
    get_three_largest_sizes,
    solve_part1,
)

# Test data fixture
@pytest.fixture
def example_input():
    """Load the example input from test_input.txt."""
    with open("test_input.txt", "r") as f:
        return f.read()

@pytest.fixture
def sample_points():
    """Small known dataset for unit tests."""
    return [
        (0, 0, 0),    # ID 0
        (3, 4, 0),    # ID 1
        (0, 0, 5),    # ID 2
    ]
```

### Phase 1: RED - Test Parsing

**Task**: Write test for `parse_input()` - MUST FAIL first.

```python
def test_parse_input(example_input):
    """Test parsing of junction box coordinates."""
    points = parse_input(example_input)

    # Example has 20 junction boxes
    assert len(points) == 20

    # First point from example: 162,817,812
    assert points[0] == (162, 817, 812)

    # Second point from example: 425,690,689
    assert points[1] == (425, 690, 689)

    # All points should be 3-tuples of integers
    for point in points:
        assert len(point) == 3
        assert all(isinstance(coord, int) for coord in point)
```

**Run test** (should FAIL): `uv run pytest day-08/test_solution.py::test_parse_input -v`

### Phase 2: GREEN - Implement Parsing

**Task**: Implement `parse_input()` in `day-08/solution.py` to pass the test.

```python
"""Day 8 Part 1: Circuit Analysis."""

from typing import List, Tuple

JunctionBox = Tuple[int, int, int]

def parse_input(input_data: str) -> List[JunctionBox]:
    """Parse input into list of (x, y, z) tuples.

    Args:
        input_data: Newline-separated lines of "X,Y,Z" coordinates

    Returns:
        List of (x, y, z) tuples, indexed by line number (ID = index)
    """
    points = []
    for line in input_data.strip().split('\n'):
        x, y, z = map(int, line.split(','))
        points.append((x, y, z))
    return points
```

**Run test** (should PASS): `uv run pytest day-08/test_solution.py::test_parse_input -v`

### Phase 3: RED - Test Distance Calculation

**Task**: Write test for `euclidean_distance()`.

```python
def test_euclidean_distance(sample_points):
    """Test Euclidean distance calculation."""
    # Distance from (0,0,0) to (3,4,0) should be 5
    dist = euclidean_distance(sample_points[0], sample_points[1])
    assert abs(dist - 5.0) < 0.0001  # Float comparison with tolerance

    # Distance from (0,0,0) to (0,0,5) should be 5
    dist = euclidean_distance(sample_points[0], sample_points[2])
    assert abs(dist - 5.0) < 0.0001

    # Distance to self should be 0
    dist = euclidean_distance(sample_points[0], sample_points[0])
    assert abs(dist - 0.0) < 0.0001
```

**Run test** (should FAIL): `uv run pytest day-08/test_solution.py::test_euclidean_distance -v`

### Phase 4: GREEN - Implement Distance Calculation

```python
import math

def euclidean_distance(point_a: JunctionBox, point_b: JunctionBox) -> float:
    """Calculate Euclidean distance between two 3D points.

    Formula: sqrt((x₂-x₁)² + (y₂-y₁)² + (z₂-z₁)²)
    """
    dx = point_b[0] - point_a[0]
    dy = point_b[1] - point_a[1]
    dz = point_b[2] - point_a[2]
    return math.sqrt(dx*dx + dy*dy + dz*dz)
```

**Run test** (should PASS): `uv run pytest day-08/test_solution.py::test_euclidean_distance -v`

### Phase 5: RED - Test Distance Computation

**Task**: Write test for `compute_all_distances()`.

```python
def test_compute_all_distances(sample_points):
    """Test pairwise distance computation."""
    distances = compute_all_distances(sample_points)

    # 3 points → 3 pairs: (0,1), (0,2), (1,2)
    assert len(distances) == 3

    # Should be sorted by distance
    assert distances[0][0] <= distances[1][0] <= distances[2][0]

    # First two distances should be 5.0 (tied)
    assert abs(distances[0][0] - 5.0) < 0.0001
    assert abs(distances[1][0] - 5.0) < 0.0001

    # Each entry should be (distance, id_a, id_b) with id_a < id_b
    for dist, id_a, id_b in distances:
        assert id_a < id_b
```

**Run test** (should FAIL)

### Phase 6: GREEN - Implement Distance Computation

```python
from typing import List

DistancePair = Tuple[float, int, int]

def compute_all_distances(points: List[JunctionBox]) -> List[DistancePair]:
    """Compute all pairwise distances and return sorted list.

    Returns:
        List of (distance, id_a, id_b) tuples, sorted by distance ascending
    """
    distances = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            dist = euclidean_distance(points[i], points[j])
            distances.append((dist, i, j))
    distances.sort()  # Sort by distance (first element of tuple)
    return distances
```

**Run test** (should PASS)

### Phase 7: RED - Test Circuit Finding

**Task**: Write test for `find_circuit()`.

```python
def test_find_circuit():
    """Test circuit lookup functionality."""
    circuits = {
        "circuit_0": {0, 1, 4},
        "circuit_1": {2, 3},
    }

    # Points in circuits
    assert find_circuit(0, circuits) == "circuit_0"
    assert find_circuit(1, circuits) == "circuit_0"
    assert find_circuit(2, circuits) == "circuit_1"

    # Unassigned point
    assert find_circuit(5, circuits) is None
```

**Run test** (should FAIL)

### Phase 8: GREEN - Implement Circuit Finding

```python
from typing import Dict, Set, Optional

CircuitName = str
Circuit = Set[int]
CircuitCollection = Dict[CircuitName, Circuit]

def find_circuit(point_id: int, circuits: CircuitCollection) -> Optional[CircuitName]:
    """Find which circuit contains the given point ID.

    Returns:
        Circuit name (string key) if found, None if point is unassigned
    """
    for circuit_name, members in circuits.items():
        if point_id in members:
            return circuit_name
    return None
```

**Run test** (should PASS)

### Phase 9: RED - Test Connection Processing

**Task**: Write test for `process_connections()`.

```python
def test_process_connections(sample_points):
    """Test circuit building with connections."""
    # Compute distances for 3 points
    distances = compute_all_distances(sample_points)

    # Connect first 2 pairs (distances are tied at 5.0)
    circuits = process_connections(distances, num_points=3, num_connections=2)

    # All 3 points should be connected (one circuit or two circuits)
    all_members = set()
    for members in circuits.values():
        all_members.update(members)
    assert all_members == {0, 1, 2}

    # Should have created circuits
    assert len(circuits) >= 1
```

**Run test** (should FAIL)

### Phase 10: GREEN - Implement Connection Processing

```python
def process_connections(
    distances: List[DistancePair],
    num_points: int,
    num_connections: int
) -> CircuitCollection:
    """Process N closest connections and build circuits.

    Args:
        distances: Sorted list of (distance, id_a, id_b) tuples
        num_points: Total number of junction boxes
        num_connections: Number of connections to make

    Returns:
        Dictionary mapping circuit names to sets of point IDs
    """
    circuits = {}
    next_circuit_id = 0
    connections_made = 0

    for distance, point_a, point_b in distances:
        if connections_made >= num_connections:
            break

        circuit_a = find_circuit(point_a, circuits)
        circuit_b = find_circuit(point_b, circuits)

        # Skip if both already in same circuit
        if circuit_a is not None and circuit_a == circuit_b:
            continue

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
        else:
            # Merge two circuits
            circuits[circuit_a].update(circuits[circuit_b])
            del circuits[circuit_b]

        connections_made += 1

    # Add any unconnected points as singleton circuits
    all_connected = set()
    for members in circuits.values():
        all_connected.update(members)

    for point_id in range(num_points):
        if point_id not in all_connected:
            circuits[f"circuit_{next_circuit_id}"] = {point_id}
            next_circuit_id += 1

    return circuits
```

**Run test** (should PASS)

### Phase 11: RED - Test Three Largest Extraction

**Task**: Write test for `get_three_largest_sizes()`.

```python
def test_get_three_largest_sizes():
    """Test extraction of three largest circuit sizes."""
    circuits = {
        "circuit_0": {0, 1, 4, 7, 9},      # size 5
        "circuit_1": {2, 3, 5, 8},         # size 4
        "circuit_2": {6, 10},              # size 2
        "circuit_3": {11, 14},             # size 2
        "circuit_4": {12},                 # size 1
    }

    sizes = get_three_largest_sizes(circuits)

    assert sizes == [5, 4, 2]
```

**Run test** (should FAIL)

### Phase 12: GREEN - Implement Three Largest Extraction

```python
def get_three_largest_sizes(circuits: CircuitCollection) -> List[int]:
    """Extract and return the three largest circuit sizes.

    Returns:
        List of three integers, sorted descending
    """
    sizes = [len(members) for members in circuits.values()]
    sizes.sort(reverse=True)
    return sizes[:3]
```

**Run test** (should PASS)

### Phase 13: RED - Test Full Solution (Integration Test)

**Task**: Write integration test using the example.

```python
def test_solve_part1_example(example_input):
    """Test full solution with example input.

    Example has 20 junction boxes, 10 connections → answer = 40
    """
    result = solve_part1(example_input, num_connections=10)

    assert result == 40
```

**Run test** (should FAIL)

### Phase 14: GREEN - Implement Main Solver

```python
def solve_part1(input_data: str, num_connections: int = 1000) -> int:
    """Solve Day 8 Part 1: Circuit Analysis.

    Args:
        input_data: Newline-separated list of X,Y,Z coordinates
        num_connections: Number of closest pairs to connect (default 1000)

    Returns:
        Product of three largest circuit sizes
    """
    # Parse input
    points = parse_input(input_data)

    # Compute and sort all distances
    distances = compute_all_distances(points)

    # Process connections
    circuits = process_connections(distances, len(points), num_connections)

    # Get three largest sizes
    top_three = get_three_largest_sizes(circuits)

    # Calculate product
    return top_three[0] * top_three[1] * top_three[2]
```

**Run test** (should PASS): `uv run pytest day-08/test_solution.py::test_solve_part1_example -v`

### Phase 15: REFACTOR

**Tasks**:

1. Add type hints to all functions (already done above)
2. Add docstrings (already done above)
3. Run linter: `uv run ruff check day-08/solution.py`
4. Run formatter: `uv run ruff format day-08/solution.py`
5. Run all tests: `uv run pytest day-08/test_solution.py -v`

## Running the Solution

### Against Example Input

```bash
uv run pytest day-08/test_solution.py::test_solve_part1_example -v
```

### Against Full Input (via script)

```python
# Add to solution.py:
if __name__ == "__main__":
    with open("input.txt", "r") as f:
        puzzle_input = f.read()

    answer = solve_part1(puzzle_input, num_connections=1000)
    print(f"Day 8 Part 1 Answer: {answer}")
```

```bash
uv run python day-08/solution.py
```

### Using Meta Runner

```bash
uv run -m cli.meta_runner run --day 8
```

## Expected Results

- **Example** (20 boxes, 10 connections): `40`
- **Full Input** (1000 connections): TBD (will be revealed when submitted)

## Debugging Tips

1. **Print circuit sizes during development**:

   ```python
   sizes = [len(members) for members in circuits.values()]
   print(f"Circuit sizes: {sorted(sizes, reverse=True)}")
   ```

2. **Verify first few connections**:

   ```python
   for i, (dist, id_a, id_b) in enumerate(distances[:5]):
       print(f"Connection {i}: Points {id_a} and {id_b}, distance {dist:.2f}")
   ```

3. **Check that all points are accounted for**:
   ```python
   all_members = set()
   for members in circuits.values():
       all_members.update(members)
   assert len(all_members) == len(points)
   ```

## Next Steps

After completing this feature:

1. Run full test suite: `uv run pytest day-08/ -v`
2. Submit answer manually at adventofcode.com
3. Update `README.md` progress tracker
4. Commit: `git commit -m "feat: solve day 8 part 1 - circuit analysis"`
5. (Optional) Add visualization or optimization notes to `day-08/README.md`
