# Day 11 - Reactor Path Finding

## Puzzle Description

This puzzle involves finding paths through a directed graph of reactor devices. Given a configuration of connected devices, the goal is to identify and count all distinct paths from device "you" to device "out".

### Problem Summary

- **Input**: Device configuration where each line specifies a device and its output connections
- **Format**: `device_name: output1 output2 output3 ...`
- **Task**: Find all unique paths from "you" to "out"
- **Expected Paths for Example**: 5

## Implementation Status

### Part 1: ✅ COMPLETE

- **Status**: Implemented and tested
- **Result**: **791 paths**
- **Tests**: 37 passing

### Part 2: ⏳ NOT YET IMPLEMENTED

## Functions Implemented

- `parse_device_config(config_text)` - Parse device configuration
- `build_graph(connections)` - Build graph representation
- `find_single_path(graph, start, end)` - Find one path using DFS
- `find_all_paths(graph, start, end)` - Find all paths using DFS with backtracking
- `display_paths(paths)` - Format paths for display
- `solve_part1(input_text)` - Main solution function
- `solve_part2(input_text)` - Placeholder for Part 2

## Code Quality

- ✅ All tests passing (37/37)
- ✅ No lint errors (Ruff clean)
- ✅ Type hints throughout (Python 3.10+)
- ✅ 100% docstring coverage (PEP 257)

## Usage

```bash
# Run all tests
uv run pytest day-11/test_solution.py -v

# Run solution with real input
uv run python day-11/solution.py

# Run specific test class
uv run pytest day-11/test_solution.py::TestEnumerateAllPaths -v
```

## Performance

| Metric                  | Actual | Target   | Status  |
| ----------------------- | ------ | -------- | ------- |
| Real Input (791 paths)  | <200ms | <1,000ms | ✅ PASS |
| Example Input (5 paths) | <1ms   | <100ms   | ✅ PASS |

---

**Status**: ✅ COMPLETE | **Answer**: 791 | **Date**: December 13, 2025
