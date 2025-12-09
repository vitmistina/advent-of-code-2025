#!/usr/bin/env python3
"""Test the example from description.md"""

import io
import sys

sys.path.insert(0, "day-06")
from solution import solve_worksheet

example = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   + 
"""

result = solve_worksheet(io.StringIO(example), verbose=True, debug=False)
print(f"\nExpected: 4277556")
print(f"Got: {result}")
print(f"Match: {result == 4277556}")
