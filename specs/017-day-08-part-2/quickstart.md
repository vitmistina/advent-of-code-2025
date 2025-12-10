# Quickstart: AoC Day 8 Part 2 - Complete Circuit Formation

**Feature**: 017-day-08-part-2  
**Date**: December 10, 2025  
**Phase**: 1 (Design)

## Overview

This guide walks through implementing Day 8 Part 2 using Test-Driven Development (TDD) with the Union-Find algorithm.

**Goal**: Find the connection that unifies all junction boxes into one circuit, then return the product of the connecting boxes' X coordinates.

**Key Difference from Part 1**: Part 1 connects exactly N pairs; Part 2 connects pairs until all boxes form ONE circuit.

---

## Prerequisites

- Part 1 solution completed (`day-08/solution.py`)
- Input files downloaded:
  - `day-08/input.txt` (full puzzle input)
  - `day-08/test_input.txt` (example with 20 boxes)
- Development environment ready: `uv run` configured

---

## Development Workflow

### Phase 1: Setup & Test File Creation (RED)

**Goal**: Create test file with failing test based on example

1. **Create test file**:

   ```bash
   cd day-08
   # Create test_solution_part2.py
   ```

2. **Write example test** (based on spec acceptance criteria):

   ```python
   """Tests for Day 8 Part 2: Complete Circuit Formation."""

   from pathlib import Path
   import pytest
   from solution_part2 import solve_part2


   def test_example_final_connection():
       """Test example: final connection should produce 25272."""
       test_input = Path(__file__).parent / "test_input.txt"
       input_data = test_input.read_text()

       result = solve_part2(input_data)

       assert result == 25272, (
           f"Expected final connection to produce 216 × 117 = 25272, "
           f"got {result}"
       )
   ```

3. **Verify test FAILS** (RED phase):

   ```bash
   uv run pytest day-08/test_solution_part2.py -v
   # Should fail: ModuleNotFoundError or ImportError
   ```

   **Critical**: Test MUST fail initially to validate it's testing real functionality.

---

### Phase 2: Minimal Implementation (GREEN)

**Goal**: Write minimum code to make test pass

1. **Create solution file**:

   ```bash
   # Create day-08/solution_part2.py
   ```

2. **Import reusable code from Part 1**:

   ```python
   """Day 8 Part 2: Complete Circuit Formation with Union-Find.

   Finds the connection that unifies all junction boxes into one circuit.
   Returns product of X coordinates of the final connecting pair.
   """

   from pathlib import Path
   # Reuse from Part 1
   from solution import (
       JunctionBox,
       DistancePair,
       parse_input,
       euclidean_distance,
       compute_all_distances,
   )
   ```

3. **Implement UnionFind class**:

   ```python
   class UnionFind:
       """Union-Find data structure with path compression and union-by-rank."""

       def __init__(self, n: int):
           """Initialize n disjoint sets."""
           self.parent = list(range(n))  # Each element is its own parent
           self.rank = [0] * n           # Tree depth estimate
           self.num_components = n       # Count of disjoint circuits

       def find(self, x: int) -> int:
           """Find root of x's set with path compression."""
           if self.parent[x] != x:
               self.parent[x] = self.find(self.parent[x])  # Path compression
           return self.parent[x]

       def union(self, x: int, y: int) -> bool:
           """Unite sets containing x and y.

           Returns:
               True if sets were merged, False if already in same set
           """
           root_x = self.find(x)
           root_y = self.find(y)

           if root_x == root_y:
               return False  # Already connected

           # Union-by-rank: attach smaller tree under larger
           if self.rank[root_x] < self.rank[root_y]:
               self.parent[root_x] = root_y
           elif self.rank[root_x] > self.rank[root_y]:
               self.parent[root_y] = root_x
           else:
               self.parent[root_y] = root_x
               self.rank[root_x] += 1

           self.num_components -= 1
           return True

       def is_fully_connected(self) -> bool:
           """Check if all elements are in one component."""
           return self.num_components == 1
   ```

4. **Implement solve_part2**:

   ```python
   def solve_part2(input_data: str) -> int:
       """Solve Part 2: Find connection that completes circuit unification.

       Args:
           input_data: Newline-separated junction box coordinates (X,Y,Z)

       Returns:
           Product of X coordinates of final connecting pair
       """
       # Parse input
       points = parse_input(input_data)
       n = len(points)

       # Compute and sort all distances
       distances = compute_all_distances(points)

       # Initialize Union-Find
       uf = UnionFind(n)

       # Process connections in distance order
       for distance, id_a, id_b in distances:
           # Check if we're about to complete the final connection
           if uf.num_components == 2:
               # Verify these boxes are in different circuits
               if uf.find(id_a) != uf.find(id_b):
                   # This is the final connection!
                   x_a = points[id_a][0]
                   x_b = points[id_b][0]
                   return x_a * x_b

           # Perform the union
           uf.union(id_a, id_b)

       # Should never reach here if input guarantees full connectivity
       raise ValueError("No connection unified all circuits")
   ```

5. **Add main entry point**:

   ```python
   def main():
       """Main entry point."""
       input_file = Path(__file__).parent / "input.txt"
       input_text = input_file.read_text()

       answer = solve_part2(input_text)
       print(f"Part 2: {answer}")


   if __name__ == "__main__":
       main()
   ```

6. **Run test** (GREEN phase):
   ```bash
   uv run pytest day-08/test_solution_part2.py -v
   # Should pass: test_example_final_connection PASSED
   ```

---

### Phase 3: Refactoring (REFACTOR)

**Goal**: Clean up code while keeping tests green

**Potential refactorings**:

1. **Add edge case tests**:

   ```python
   def test_two_boxes():
       """Test minimal case: 2 boxes."""
       input_data = "0,0,0\n10,0,0\n"
       result = solve_part2(input_data)
       # First connection unifies both: 0 × 10 = 0
       assert result == 0


   def test_already_connected():
       """Test case where all boxes already connected (edge case)."""
       # This tests defensive programming, not expected in real input
       input_data = "5,5,5\n6,5,5\n"  # Two very close boxes
       result = solve_part2(input_data)
       assert result == 30  # 5 × 6
   ```

2. **Add type hints validation**:

   ```bash
   uv run mypy day-08/solution_part2.py --strict
   # Fix any type issues
   ```

3. **Run linter**:

   ```bash
   uv run ruff check day-08/solution_part2.py
   uv run ruff format day-08/solution_part2.py
   ```

4. **Add docstring examples**:

   ```python
   def solve_part2(input_data: str) -> int:
       """Solve Part 2: Find connection that completes circuit unification.

       Example:
           >>> input_data = Path("test_input.txt").read_text()
           >>> solve_part2(input_data)
           25272

       Args:
           input_data: Newline-separated junction box coordinates (X,Y,Z)

       Returns:
           Product of X coordinates of final connecting pair
       """
   ```

5. **Keep tests green**:
   ```bash
   uv run pytest day-08/test_solution_part2.py -v
   # All tests should still pass after refactoring
   ```

---

### Phase 4: Full Puzzle Solution

1. **Run against full input**:

   ```bash
   uv run python day-08/solution_part2.py
   # Output: Part 2: [your answer]
   ```

2. **Manual submission**:

   - Copy answer from terminal
   - Go to Advent of Code Day 8
   - Submit Part 2 answer
   - Verify correctness

3. **Update progress**:

   ```bash
   # Commit changes
   git add day-08/solution_part2.py day-08/test_solution_part2.py specs/017-day-08-part-2/
   git commit -m "feat: solve day 08 part 2 with Union-Find"
   git push origin main
   ```

4. **Update README.md**:
   - Mark Day 8 Part 2 as complete
   - Add any learnings about Union-Find algorithm

---

## Testing Strategy

### Test Pyramid

1. **Unit Tests** (Fast, Focused):

   - `test_union_find_initialization()` — verify initial state
   - `test_union_find_union()` — verify merge behavior
   - `test_union_find_find()` — verify path compression
   - `test_union_find_components()` — verify component counting

2. **Integration Tests** (Example-based):

   - `test_example_final_connection()` — verify full solution with example (25272)
   - `test_two_boxes()` — minimal case
   - `test_multiple_circuits()` — verify circuit merging logic

3. **Full Solution Test** (Slow, End-to-End):
   - Run against `input.txt`
   - Verify output matches submitted answer

### Running Tests

```bash
# Run all Part 2 tests
uv run pytest day-08/test_solution_part2.py -v

# Run specific test
uv run pytest day-08/test_solution_part2.py::test_example_final_connection -v

# Run with coverage
uv run pytest day-08/test_solution_part2.py --cov=solution_part2 --cov-report=term-missing

# Run all day-08 tests (Part 1 + Part 2)
uv run pytest day-08/ -v
```

---

## Debugging Tips

### Problem: Test fails with wrong answer

**Diagnosis**:

```python
# Add debug output to solve_part2
for distance, id_a, id_b in distances:
    if uf.num_components == 2:
        print(f"Components=2: checking ({id_a}, {id_b}), distance={distance}")
        print(f"  Point A: {points[id_a]}")
        print(f"  Point B: {points[id_b]}")
        if uf.find(id_a) != uf.find(id_b):
            print(f"  → FINAL CONNECTION: {points[id_a][0]} × {points[id_b][0]}")
```

**Common issues**:

- Not checking `find(id_a) != find(id_b)` when `num_components == 2`
- Processing distances in wrong order (not sorted)
- Off-by-one error in union logic

### Problem: Performance is slow

**Diagnosis**:

```python
import time

start = time.time()
distances = compute_all_distances(points)
print(f"Distance computation: {time.time() - start:.2f}s")

start = time.time()
# ... union-find processing ...
print(f"Union-Find processing: {time.time() - start:.2f}s")
```

**Expected performance** (N=1000):

- Distance computation: < 0.5s
- Union-Find processing: < 0.1s

**If slower**: Check that you're using Union-Find, not dictionary approach

### Problem: UnionFind not merging correctly

**Diagnosis**:

```python
# Test union behavior directly
uf = UnionFind(5)
print(f"Initial components: {uf.num_components}")  # Should be 5

merged = uf.union(0, 1)
print(f"After union(0,1): merged={merged}, components={uf.num_components}")  # merged=True, components=4

merged = uf.union(0, 1)
print(f"After union(0,1) again: merged={merged}, components={uf.num_components}")  # merged=False, components=4
```

---

## Code Reuse from Part 1

**Reusable components**:

- ✅ `parse_input()` — same input format
- ✅ `euclidean_distance()` — same distance formula
- ✅ `compute_all_distances()` — same pair generation & sorting
- ✅ Type aliases: `JunctionBox`, `DistancePair`

**New for Part 2**:

- ❌ Circuit tracking logic (Part 1 uses dictionary, Part 2 uses Union-Find)
- ❌ Connection processing (Part 1 processes N pairs, Part 2 processes until unified)
- ❌ Answer calculation (Part 1 returns product of 3 largest circuits, Part 2 returns X-coordinate product of final pair)

**Import strategy**:

```python
# In solution_part2.py
from solution import (
    JunctionBox,
    DistancePair,
    parse_input,
    euclidean_distance,
    compute_all_distances,
)
```

---

## Success Criteria Checklist

Before considering Part 2 complete:

- ✅ Example test passes (output: 25272)
- ✅ Full input produces correct answer (submitted to AoC)
- ✅ All tests pass: `uv run pytest day-08/test_solution_part2.py -v`
- ✅ Code formatted: `uv run ruff format day-08/solution_part2.py`
- ✅ No linting errors: `uv run ruff check day-08/solution_part2.py`
- ✅ Type hints validated: `uv run mypy day-08/solution_part2.py --strict`
- ✅ Solution runs in < 1 second for full input
- ✅ Code committed to main branch
- ✅ Progress tracker updated in main README.md

---

## Next Steps

After completing Part 2:

1. **Reflect on learnings**:

   - When is Union-Find the right choice?
   - What's the complexity trade-off between dictionary and Union-Find approaches?

2. **Optional optimizations**:

   - Could we avoid computing all N² distances if we know we only need N-1 connections?
   - Could spatial indexing (e.g., k-d tree) help find nearest neighbors faster?

3. **Documentation**:
   - Update `day-08/README.md` with Part 2 solution notes
   - Document algorithm complexity comparison in constitution learnings

---

## Reference

- **Constitution**: `.specify/memory/constitution.md` (Principle IV: TDD is NON-NEGOTIABLE)
- **Spec**: `specs/017-day-08-part-2/spec.md`
- **Research**: `specs/017-day-08-part-2/research.md` (algorithm decision rationale)
- **Data Model**: `specs/017-day-08-part-2/data-model.md` (entity definitions)
- **Part 1 Solution**: `day-08/solution.py` (reusable parsing & distance code)
