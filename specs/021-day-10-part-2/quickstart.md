# Quickstart Guide: Day 10 Part 2

**Phase**: Phase 1 (Design & Quickstart)  
**Date**: 2025-12-12  
**Spec Reference**: [spec.md](../spec.md)  
**Data Model Reference**: [data-model.md](../data-model.md)  
**Research Reference**: [research.md](../research.md)

---

## TDD Test Plan

This document outlines the complete test suite structure using Red-Green-Refactor TDD methodology.

### Test Execution Order (Red-Green-Refactor Cycle)

```
Phase 1: PARSER TESTS (Red-Green-Refactor)
├─ Test 1: Parse first example line
├─ Test 2: Parse second example line
├─ Test 3: Parse third example line
├─ Test 4: Parse full three-line input
└─ Test 5: Error handling (invalid format)

Phase 2: SOLVER TESTS (Red-Green-Refactor)
├─ Test 6: Solve first machine (expect 10)
├─ Test 7: Solve second machine (expect 12)
├─ Test 8: Solve third machine (expect 11)
└─ Test 9: Aggregate all (expect 33)

Phase 3: INTEGRATION TESTS (Red-Green-Refactor)
├─ Test 10: End-to-end pipeline
├─ Test 11: Performance benchmark
└─ Test 12: Edge cases
```

---

## Test Definitions

### PARSER TESTS

#### Test 1: Parse First Example Line

**Test Name**: `test_parse_first_example_line`

**Given**: Input line
```
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
```

**When**: Calling `parse_line(line, machine_id=0)`

**Then**: Expect Machine object with:
```python
assert machine.machine_id == 0
assert machine.num_buttons == 6
assert machine.num_counters == 4
assert machine.buttons[0].affected_counter_indices == [0]  # or whatever (3) means
assert machine.buttons[1].affected_counter_indices == [1, 3]
assert machine.counters[0].target_value == 3
assert machine.counters[1].target_value == 5
assert machine.counters[2].target_value == 4
assert machine.counters[3].target_value == 7
```

**Acceptance**: Parse correctly identifies 6 buttons and 4 counters with correct targets

---

#### Test 2: Parse Second Example Line

**Test Name**: `test_parse_second_example_line`

**Given**: Input line
```
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
```

**When**: Calling `parse_line(line, machine_id=1)`

**Then**: Expect Machine object with:
```python
assert machine.machine_id == 1
assert machine.num_buttons == 5
assert machine.num_counters == 5
assert machine.counters[0].target_value == 7
assert machine.counters[1].target_value == 5
assert machine.counters[2].target_value == 12
assert machine.counters[3].target_value == 7
assert machine.counters[4].target_value == 2
```

**Acceptance**: Correctly handles multi-counter buttons and variable-length targets

---

#### Test 3: Parse Third Example Line

**Test Name**: `test_parse_third_example_line`

**Given**: Input line
```
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
```

**When**: Calling `parse_line(line, machine_id=2)`

**Then**: Expect Machine object with:
```python
assert machine.machine_id == 2
assert machine.num_buttons == 4
assert machine.num_counters == 6
assert machine.buttons[0].affected_counter_indices == [0, 1, 2, 3, 4]
assert machine.buttons[3].affected_counter_indices == [1, 2]
assert machine.counters[2].target_value == 11
assert machine.counters[5].target_value == 5
```

**Acceptance**: Handles 6-counter machine with 4 buttons of varying sizes

---

#### Test 4: Parse Full Three-Line Input

**Test Name**: `test_parse_full_input`

**Given**: Input text with all three example lines:
```
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
```

**When**: Calling `parse_input(text)`

**Then**: Expect PuzzleInput object with:
```python
puzzle = parse_input(text)
assert puzzle.num_machines == 3
assert puzzle.machines[0].machine_id == 0
assert puzzle.machines[1].machine_id == 1
assert puzzle.machines[2].machine_id == 2
assert puzzle.machines[0].num_buttons == 6
assert puzzle.machines[1].num_buttons == 5
assert puzzle.machines[2].num_buttons == 4
```

**Acceptance**: Correctly parses multi-line input into separate machines

---

#### Test 5: Error Handling - Invalid Format

**Test Name**: `test_parse_invalid_format`

**Given**: Malformed input line
```
[.##.] (3) (1,3) MISSING_TARGETS
```

**When**: Calling `parse_line(line, machine_id=0)`

**Then**: Expect `ValueError` with message containing "Invalid format" or similar

**Acceptance**: Parser rejects malformed input with clear error message

---

### SOLVER TESTS

#### Test 6: Solve First Machine (Expect 10)

**Test Name**: `test_solve_first_machine`

**Given**: Machine object from Test 1 (or directly constructed)
```python
machine = Machine(
    machine_id=0,
    buttons=[...],  # 6 buttons as parsed from first example
    counters=[...]  # 4 counters with targets [3, 5, 4, 7]
)
```

**When**: Calling `solve_machine(machine)`

**Then**: Expect Solution object with:
```python
solution = solve_machine(machine)
assert solution is not None
assert solution.total_presses == 10
assert all(p >= 0 for p in solution.press_counts)

# Verify solution is correct
is_valid, final_values = solution.verify(machine.buttons, machine.target_vector)
assert is_valid == True
assert final_values == [3, 5, 4, 7]
```

**Acceptance**: Solver finds minimum press count of exactly 10

---

#### Test 7: Solve Second Machine (Expect 12)

**Test Name**: `test_solve_second_machine`

**Given**: Machine object from Test 2

**When**: Calling `solve_machine(machine)`

**Then**: Expect Solution object with:
```python
solution = solve_machine(machine)
assert solution.total_presses == 12

is_valid, final_values = solution.verify(machine.buttons, machine.target_vector)
assert is_valid == True
assert final_values == [7, 5, 12, 7, 2]
```

**Acceptance**: Solver finds minimum press count of exactly 12

---

#### Test 8: Solve Third Machine (Expect 11)

**Test Name**: `test_solve_third_machine`

**Given**: Machine object from Test 3

**When**: Calling `solve_machine(machine)`

**Then**: Expect Solution object with:
```python
solution = solve_machine(machine)
assert solution.total_presses == 11

is_valid, final_values = solution.verify(machine.buttons, machine.target_vector)
assert is_valid == True
assert final_values == [10, 11, 11, 5, 10, 5]
```

**Acceptance**: Solver finds minimum press count of exactly 11

---

#### Test 9: Aggregate All Machines (Expect 33)

**Test Name**: `test_solve_aggregate_all`

**Given**: PuzzleInput from Test 4 (all three machines)

**When**: Calling `solve_all(puzzle)`

**Then**: Expect PuzzleResult object with:
```python
result = solve_all(puzzle)
assert result.per_machine_results == [10, 12, 11]  # In order
assert result.total_minimum_presses == 33
assert sum(result.per_machine_results) == 33
```

**Acceptance**: Aggregate correctly sums machine results to 33

---

### INTEGRATION TESTS

#### Test 10: End-to-End Pipeline

**Test Name**: `test_end_to_end_pipeline`

**Given**: Raw input text (all three example machines)

**When**: Calling:
```python
puzzle = parse_input(input_text)
result = solve_all(puzzle)
answer = result.total_minimum_presses
```

**Then**: Expect:
```python
assert answer == 33
```

**Acceptance**: Full pipeline (parse → solve → result) works end-to-end

---

#### Test 11: Performance Benchmark

**Test Name**: `test_performance_benchmark`

**Given**: Three example machines

**When**: Measuring execution time of `solve_all(puzzle)`

**Then**: Expect:
```python
import time
start = time.time()
result = solve_all(puzzle)
elapsed = time.time() - start
assert elapsed < 1.0, f"Took {elapsed}s, expected < 1s"
```

**Acceptance**: Solver completes in under 1 second for examples

---

#### Test 12: Edge Cases

**Test Name**: `test_edge_case_zero_target`

**Given**: Machine with target of 0
```python
machine = Machine(
    machine_id=0,
    buttons=[Button(0, [0])],
    counters=[Counter(0, 0)]
)
```

**When**: Calling `solve_machine(machine)`

**Then**: Expect:
```python
solution = solve_machine(machine)
assert solution is not None
assert solution.total_presses == 0
assert solution.press_counts == [0]
```

**Acceptance**: Handles zero-target machines correctly (no presses needed)

---

## Red-Green-Refactor Cycle

### Phase 1: RED (Write Tests First)

1. Write all test cases above in `day-10/test_solution_part2.py`
2. Run tests: **ALL FAIL** (RED state)
3. Verify tests are meaningful (not trivially wrong)

```bash
$ pytest day-10/test_solution_part2.py -v
# Expected: All tests FAIL
# E.g., "ModuleNotFoundError: No module named 'solution_part2'"
```

---

### Phase 2: GREEN (Implement Minimum Code)

1. Create `day-10/solution_part2.py` with stub functions
2. Implement parser first (Test 1-5)
3. Implement solver next (Test 6-9)
4. Integrate (Test 10-12)
5. Run tests after each section: they should PASS

```bash
$ pytest day-10/test_solution_part2.py::test_parse_first_example_line -v
# After implementation: PASS

$ pytest day-10/test_solution_part2.py -v
# After full implementation: All tests PASS (GREEN state)
```

---

### Phase 3: REFACTOR (Clean Code)

1. Optimize solver performance (if needed)
2. Improve code readability
3. Add docstrings and comments
4. Run tests: **ALL STILL PASS**

```bash
$ pytest day-10/test_solution_part2.py -v
# After refactoring: All tests still PASS
```

---

## Test File Template

```python
# day-10/test_solution_part2.py

import pytest
from solution_part2 import parse_line, parse_input, solve_machine, solve_all, Solution

# Constants for examples
EXAMPLE_1_LINE = "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"
EXAMPLE_2_LINE = "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}"
EXAMPLE_3_LINE = "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"

EXAMPLE_FULL_INPUT = f"""{EXAMPLE_1_LINE}
{EXAMPLE_2_LINE}
{EXAMPLE_3_LINE}"""

class TestParser:
    """Tests for parse_line() and parse_input()"""
    
    def test_parse_first_example_line(self):
        """Test parsing first example line"""
        # TODO: Implement after RED phase
        pass
    
    def test_parse_second_example_line(self):
        """Test parsing second example line"""
        pass
    
    def test_parse_third_example_line(self):
        """Test parsing third example line"""
        pass
    
    def test_parse_full_input(self):
        """Test parsing full three-line input"""
        pass
    
    def test_parse_invalid_format(self):
        """Test error handling for invalid format"""
        pass


class TestSolver:
    """Tests for solve_machine() and solve_all()"""
    
    def test_solve_first_machine(self):
        """Test solving first machine (expect 10)"""
        # TODO: Implement after GREEN phase
        pass
    
    def test_solve_second_machine(self):
        """Test solving second machine (expect 12)"""
        pass
    
    def test_solve_third_machine(self):
        """Test solving third machine (expect 11)"""
        pass
    
    def test_solve_aggregate_all(self):
        """Test aggregate solution (expect 33)"""
        pass


class TestIntegration:
    """End-to-end integration tests"""
    
    def test_end_to_end_pipeline(self):
        """Test full parse → solve → result pipeline"""
        pass
    
    def test_performance_benchmark(self):
        """Test performance (< 1 second)"""
        pass
    
    def test_edge_case_zero_target(self):
        """Test machine with zero target"""
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

---

## Implementation Checklist

- [ ] Write all test cases (RED phase)
- [ ] Run tests, verify all fail
- [ ] Implement parse_line() → tests 1-5 pass
- [ ] Implement solve_machine() → tests 6-9 pass
- [ ] Implement solve_all() → test 9 passes
- [ ] Integrate → test 10 passes
- [ ] Performance check → test 11 passes
- [ ] Edge cases → test 12 passes
- [ ] Refactor for readability
- [ ] Add docstrings
- [ ] Run full test suite: all green ✓
- [ ] Verify Part 1 still works (no regression)
- [ ] Update README.md
- [ ] Commit with message "feat(day-10): Implement Part 2 solution with TDD"

---

## Running the Solution

### Development (with tests):
```bash
cd day-10
pytest test_solution_part2.py -v
```

### Verify examples:
```bash
python -c "from solution_part2 import main; print(main('test_input.txt'))"
# Expected output: 33
```

### Solve actual puzzle:
```bash
uv run -m cli.meta_runner solve --day 10 --part 2
# Or manually:
python -c "from solution_part2 import main; print(main('input.txt'))"
```

---

## Success Criteria

✅ All parser tests pass (correctly extracts buttons and targets)  
✅ All solver tests pass (finds minimum presses: 10, 12, 11)  
✅ Aggregate test passes (33 = 10 + 12 + 11)  
✅ End-to-end test passes (full pipeline works)  
✅ Performance test passes (< 1 second)  
✅ Zero-target edge case passes  
✅ All code has docstrings  
✅ Code passes ruff linting  
✅ Part 1 tests still pass (no regression)  
✅ README updated with solution notes  

