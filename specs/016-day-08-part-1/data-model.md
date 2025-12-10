# Data Model: AoC Day 8 Part 1 - Circuit Analysis

**Date**: December 10, 2025  
**Feature**: 016-day-08-part-1  
**Phase**: 1 (Design & Contracts)

## Entity Definitions

### 1. JunctionBox (Point3D)

**Description**: Represents a single junction box location in 3D space.

**Representation**: Python tuple `(x: int, y: int, z: int)`

**Attributes**:

- `x`: X-coordinate (integer)
- `y`: Y-coordinate (integer)
- `z`: Z-coordinate (integer)
- Implicit `id`: Array index in the points list (0-based auto-increment)

**Validation Rules**:

- All coordinates must be integers
- No explicit range constraints (based on puzzle input)
- ID is assigned automatically based on order in input file (line 0 → ID 0, line 1 → ID 1, etc.)

**State Transitions**: None (immutable coordinates)

**Example**:

```python
# First line in input: "162,817,812"
point_0 = (162, 817, 812)  # ID = 0

# Second line in input: "425,690,689"
point_1 = (425, 690, 689)  # ID = 1
```

---

### 2. DistancePair

**Description**: Represents the Euclidean distance between two junction boxes, used for sorting and connection selection.

**Representation**: Python tuple `(distance: float, id_a: int, id_b: int)`

**Attributes**:

- `distance`: Euclidean distance between the two points (float, computed via `math.sqrt`)
- `id_a`: ID of first junction box (smaller index)
- `id_b`: ID of second junction box (larger index)

**Validation Rules**:

- `distance >= 0` (always non-negative)
- `0 <= id_a < id_b < num_points` (IDs are valid and ordered)
- Distance calculated as: `sqrt((x₂-x₁)² + (y₂-y₁)² + (z₂-z₁)²)`

**State Transitions**: None (computed once, immutable)

**Relationships**:

- References two `JunctionBox` entities by ID
- Used to determine connection priority (sorted by distance ascending)

**Example**:

```python
# Distance between point_0 (162,817,812) and point_1 (425,690,689)
# Calculation: sqrt((425-162)^2 + (690-817)^2 + (689-812)^2)
#            = sqrt(69169 + 16129 + 15129)
#            = sqrt(100427)
#            ≈ 316.9

distance_pair = (316.9, 0, 1)
```

---

### 3. Circuit

**Description**: A group of connected junction boxes forming an independent circuit.

**Representation**: Python set of integers `{id1, id2, id3, ...}`

**Attributes**:

- `members`: Set of junction box IDs (integers) that belong to this circuit
- `size`: Count of members in the set (computed via `len()`)
- Implicit `name`: Dictionary key (e.g., "circuit_0", "circuit_1")

**Validation Rules**:

- Each junction box can belong to at most one circuit
- Circuit size >= 1 (every point either forms a singleton circuit or joins others)
- No duplicate IDs within a circuit (set enforces uniqueness)

**State Transitions**:

1. **Created**: New circuit formed when two unassigned points are connected
2. **Grown**: Existing circuit adds an unassigned point
3. **Merged**: Two circuits combine when a connection bridges them

**Relationships**:

- Contains multiple `JunctionBox` entities (by ID reference)
- Circuits are mutually exclusive (no overlap)

**Example**:

```python
# After processing some connections:
circuits = {
    "circuit_0": {0, 1, 4, 7, 9},      # 5 members
    "circuit_1": {2, 3, 5, 8},         # 4 members
    "circuit_2": {6, 10},              # 2 members
    # ... more circuits or singleton points
}
```

---

### 4. CircuitCollection

**Description**: The complete set of all circuits after processing connections.

**Representation**: Python dictionary `{circuit_name: set_of_ids}`

**Attributes**:

- `circuits`: Dictionary mapping circuit names (strings) to sets of IDs
- `sizes`: Computed list of circuit sizes (sorted descending for answer calculation)

**Validation Rules**:

- Every junction box ID (0 to num_points-1) appears in exactly one circuit
- Sum of all circuit sizes equals total number of junction boxes
- At least one circuit exists (in worst case, all points form one circuit)

**Operations**:

- `find_circuit(point_id)`: Returns circuit name containing point_id, or None if unassigned
- `merge_circuits(circuit_a, circuit_b)`: Combines two circuits and removes the second
- `add_to_circuit(circuit_name, point_id)`: Adds a point to an existing circuit
- `create_circuit(point_a, point_b)`: Creates a new circuit with two points
- `get_three_largest()`: Returns sizes of three largest circuits (sorted descending)

**State Transitions**:

1. **Initialization**: Empty dictionary `{}`
2. **Growth**: Circuits added as connections are processed
3. **Consolidation**: Circuits may merge when connections bridge them
4. **Finalization**: Final state after all connections processed

**Example**:

```python
# Final state for the example (20 points, 10 connections)
circuits = {
    "circuit_0": {0, 1, 4, 7, 9},              # size 5
    "circuit_1": {2, 3, 5, 8},                 # size 4
    "circuit_2": {6, 10},                      # size 2
    "circuit_3": {11, 14},                     # size 2
    "circuit_4": {12},                         # size 1 (singleton)
    "circuit_5": {13},                         # size 1
    "circuit_6": {15},                         # size 1
    "circuit_7": {16},                         # size 1
    "circuit_8": {17},                         # size 1
    "circuit_9": {18},                         # size 1
    "circuit_10": {19},                        # size 1
}

# Circuit sizes: [5, 4, 2, 2, 1, 1, 1, 1, 1, 1, 1]
# Three largest: [5, 4, 2]
# Product: 5 * 4 * 2 = 40
```

---

## Data Flow

```
Input File (input.txt)
    ↓
[Parse] → List[JunctionBox] with auto-increment IDs
    ↓
[Compute Distances] → List[DistancePair]
    ↓
[Sort by Distance] → Sorted List[DistancePair]
    ↓
[Process N Connections] → CircuitCollection (dict of circuits)
    ↓
[Extract Sizes] → List[int] (circuit sizes)
    ↓
[Sort Descending] → Sorted List[int]
    ↓
[Take Top 3] → [size1, size2, size3]
    ↓
[Multiply] → Final Answer (int)
```

---

## Type Signatures (Python)

```python
from typing import List, Tuple, Dict, Set, Optional

# Type aliases for clarity
JunctionBox = Tuple[int, int, int]  # (x, y, z)
PointID = int
DistancePair = Tuple[float, PointID, PointID]  # (distance, id_a, id_b)
Circuit = Set[PointID]
CircuitName = str
CircuitCollection = Dict[CircuitName, Circuit]

def parse_input(input_data: str) -> List[JunctionBox]:
    """Parse input into list of 3D points."""
    ...

def euclidean_distance(point_a: JunctionBox, point_b: JunctionBox) -> float:
    """Calculate Euclidean distance between two points."""
    ...

def compute_all_distances(points: List[JunctionBox]) -> List[DistancePair]:
    """Compute all pairwise distances and return sorted list."""
    ...

def find_circuit(point_id: PointID, circuits: CircuitCollection) -> Optional[CircuitName]:
    """Find which circuit contains the given point ID."""
    ...

def process_connections(
    distances: List[DistancePair],
    num_points: int,
    num_connections: int
) -> CircuitCollection:
    """Process N closest connections and build circuits."""
    ...

def get_three_largest_sizes(circuits: CircuitCollection) -> List[int]:
    """Extract and return the three largest circuit sizes."""
    ...

def solve_part1(input_data: str, num_connections: int = 1000) -> int:
    """Main solver function."""
    ...
```

---

## Memory & Performance Estimates

**For N = 1000 junction boxes**:

- `List[JunctionBox]`: 1000 tuples × 24 bytes = ~24 KB
- `List[DistancePair]`: ~500,000 pairs × 32 bytes = ~16 MB
- `CircuitCollection`: Up to 1000 sets × (overhead + IDs) = ~100 KB
- **Total peak memory**: ~20 MB (well within acceptable limits)

**Time Complexity**:

- Parsing: O(N)
- Distance computation: O(N²)
- Sorting: O(N² log N)
- Connection processing: O(K × N) where K = num_connections (worst case if many lookups)
- Final calculation: O(N log N)
- **Overall**: O(N² log N) ≈ 6M operations for N=1000 → well under 1 second

---

## Validation & Testing

**Unit Tests**:

- `test_parse_input()`: Verify parsing of example input (20 lines → 20 points)
- `test_euclidean_distance()`: Verify known distances (e.g., (0,0,0) to (3,4,0) = 5.0)
- `test_find_circuit()`: Verify circuit lookup logic
- `test_process_connections()`: Verify circuit building with small example
- `test_get_three_largest()`: Verify correct extraction of top 3 sizes

**Integration Test**:

- `test_example_solution()`: Full example (20 points, 10 connections) → answer = 40

**Edge Cases**:

- Single point: Should form one circuit of size 1
- All points connected before num_connections: Should handle gracefully
- Ties in distances: Should process deterministically (by ID order)
