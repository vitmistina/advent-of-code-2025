#!/usr/bin/env python3
import io
import sys
sys.path.insert(0, 'day-06')

from parser import (
    read_lines_as_stream,
    columns_from_lines,
    problem_column_groups_part2,
    extract_problem_part2,
)

worksheet = "342 1 53\n4*+ 6 2\n    *   +\n"
print(f"Input worksheet:\n{repr(worksheet)}\n")

lines = list(read_lines_as_stream(io.StringIO(worksheet)))
print("Lines:")
for i, line in enumerate(lines):
    print(f"  {i}: {repr(line)}")

cols = list(columns_from_lines(read_lines_as_stream(io.StringIO(worksheet))))
print(f"\nColumns ({len(cols)} total):")
for col in cols:
    print(f"  Col {col.index}: values={col.values}, separator={col.is_separator}")

print("\nProblem groups:")
groups = list(problem_column_groups_part2(columns_from_lines(read_lines_as_stream(io.StringIO(worksheet)))))
for i, group in enumerate(groups):
    print(f"  Group {i}: cols {group.start_column}-{group.end_column}")
    for col in group.columns:
        print(f"    Col {col.index}: {col.values}")
    
    try:
        problem = extract_problem_part2(group)
        print(f"    Problem: operands={problem.operands}, operation={problem.operation}")
    except Exception as e:
        print(f"    Error: {e}")
