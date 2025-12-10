from typing import Literal


# --- Move class and type definitions above main() ---
Coordinate = tuple[int, int]  # (row, col)


class Cell:
    def __init__(self, coord: Coordinate, kind: Literal["start", "splitter", "empty"]):
        self.coord = coord
        self.kind = kind


class ManifoldDiagram:
    allowed_chars = {"S", "^", ".", " "}

    def __init__(self, rows: list[str]):
        self.rows = [row.rstrip() for row in rows]
        self.height = len(self.rows)
        self.width = max((len(row) for row in self.rows), default=0)
        self.start: Coordinate | None = None
        self.splitters: set[Coordinate] = set()
        self.walkable: set[Coordinate] = set()
        self._parse()

    def _parse(self):
        found_start = False
        for r, row in enumerate(self.rows):
            for c, ch in enumerate(row):
                if ch not in self.allowed_chars:
                    raise ValueError(f"Invalid character '{ch}' at ({r},{c})")
                if ch == "S":
                    if found_start:
                        raise ValueError("Multiple start positions 'S' found")
                    self.start = (r, c)
                    found_start = True
                    self.walkable.add((r, c))
                elif ch == "^":
                    self.splitters.add((r, c))
                    self.walkable.add((r, c))
                elif ch == ".":
                    self.walkable.add((r, c))
        if not found_start:
            raise ValueError("No start position 'S' found in diagram")
        if self.height == 0 or all(not row.strip() for row in self.rows):
            raise ValueError("Diagram must contain at least one non-whitespace row")

    def cell_kind(self, coord: Coordinate) -> str | None:
        if coord == self.start:
            return "start"
        elif coord in self.splitters:
            return "splitter"
        elif coord in self.walkable:
            return "empty"
        return None


# --- MVP: Single Splitter Timeline Counter ---
def count_timelines(diagram: "ManifoldDiagram") -> int:
    memo = {}

    def in_bounds(coord):
        r, c = coord
        return 0 <= r < diagram.height and 0 <= c < diagram.width

    def dfs(coord):
        if coord in memo:
            return memo[coord]
        if not in_bounds(coord) or coord not in diagram.walkable:
            return 0
        if coord[0] == diagram.height - 1:
            memo[coord] = 1
            return 1
        kind = diagram.cell_kind(coord)
        if coord[0] == diagram.height - 1:
            memo[coord] = 1
            return 1
        total = 0
        kind = diagram.cell_kind(coord)
        if kind == "splitter":
            # Split diagonally left and right
            for dcol in (-1, 1):
                next_coord = (coord[0] + 1, coord[1] + dcol)
                if in_bounds(next_coord) and next_coord in diagram.walkable:
                    total += dfs(next_coord)
        else:
            # Only move straight down
            next_coord = (coord[0] + 1, coord[1])
            if in_bounds(next_coord) and next_coord in diagram.walkable:
                total += dfs(next_coord)
        # If no moves were possible, timeline ends here
        if total == 0:
            total = 1
        memo[coord] = total
        return total

    return dfs(diagram.start)


# For test import
__all__ = ["ManifoldDiagram", "count_timelines"]
# Quantum Tachyon Manifold Timelines - Day 7 Part 2


def main():
    import os

    input_path = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(input_path, encoding="utf-8") as f:
        rows = [line.rstrip("\n") for line in f]
    diagram = ManifoldDiagram(rows)
    result = count_timelines(diagram)
    print("\n=== Quantum Timeline Count ===")
    print(f"Input: {input_path}")
    print(f"Timelines: {result}")
    print("=============================")


if __name__ == "__main__":
    main()
