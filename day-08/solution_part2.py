"""Part 2 solution for AoC Day 8: Complete Circuit Formation.

Reuses parsing and distance functions from Part 1 (solution.py).
"""

from .solution import compute_all_distances, parse_input


class UnionFind:
    """Union-Find with path compression and union-by-rank for circuit tracking."""

    def __init__(self, n: int) -> None:
        """Initialize Union-Find structure for n elements.

        Args:
            n: Number of elements (junction boxes)
        """
        self.parent = list(range(n))  # Each element is its own parent initially
        self.rank = [0] * n  # Rank for union-by-rank optimization
        self.num_components = n  # Track number of disjoint circuits

    def find(self, x: int) -> int:
        """Find root of element x with path compression.

        Path compression: Make all nodes on path point directly to root.
        This flattens the tree structure for O(α(n)) amortized time.

        Args:
            x: Element to find root of

        Returns:
            Root element of x's component
        """
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """Unite components containing x and y using union-by-rank.

        Union-by-rank: Attach smaller tree under root of larger tree.
        This keeps tree depth logarithmic for efficient future finds.

        Args:
            x: First element
            y: Second element

        Returns:
            True if components were merged, False if already in same component
        """
        xroot = self.find(x)
        yroot = self.find(y)
        if xroot == yroot:
            return False  # Already in same component
        # Union-by-rank: attach smaller rank tree under higher rank tree
        if self.rank[xroot] < self.rank[yroot]:
            self.parent[xroot] = yroot
        elif self.rank[xroot] > self.rank[yroot]:
            self.parent[yroot] = xroot
        else:
            self.parent[yroot] = xroot
            self.rank[xroot] += 1  # Same rank: increment after merge
        self.num_components -= 1
        return True

    def is_fully_connected(self) -> bool:
        """Check if all elements are in a single component.

        Returns:
            True if all elements form one connected component
        """
        return self.num_components == 1


def solve_part2(input_data: str) -> int:
    """Find the connection that unifies all circuits.

    Processes junction box pairs by increasing Euclidean distance until all boxes
    form one circuit. Returns the product of X coordinates of the final connecting pair.

    Args:
        input_data: String containing junction box coordinates (one per line, X,Y,Z format)

    Returns:
        Product of X coordinates of the two boxes whose connection unified all circuits

    Raises:
        ValueError: If circuit never unifies (should not happen with valid input)
    """
    # Parse junction box coordinates (reuse Part 1 parsing)
    points = parse_input(input_data)

    # Compute all pairwise distances and sort by distance (reuse Part 1 distance logic)
    distances = compute_all_distances(points)

    # Initialize UnionFind to track circuit membership
    uf = UnionFind(len(points))

    # Process connections in distance order
    for _dist, idx1, idx2 in distances:
        # Check if boxes are already in same circuit (skip redundant connections)
        if uf.find(idx1) == uf.find(idx2):
            continue

        # Before merging, check if we're about to unite the final two circuits
        if uf.num_components == 2:
            # This connection unifies all circuits - calculate result
            x1 = points[idx1][0]
            x2 = points[idx2][0]
            return x1 * x2

        # Merge circuits
        uf.union(idx1, idx2)

    # Should never reach here with valid input
    raise ValueError("Circuit never unified - invalid input or logic error")


def main() -> None:
    """Main entry point for Part 2 solution."""
    from pathlib import Path

    input_file = Path(__file__).parent / "input.txt"
    input_data = input_file.read_text()
    result = solve_part2(input_data)
    print(f"Part 2: {result}")


if __name__ == "__main__":
    main()
