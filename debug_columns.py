#!/usr/bin/env python3
"""Debug the example parsing"""

import io
import sys

sys.path.insert(0, "day-06")
from parser import read_lines_as_stream, columns_from_lines

example = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   + 
"""

lines = read_lines_as_stream(io.StringIO(example))
cols = list(columns_from_lines(lines))

print(f"Total columns: {len(cols)}")
print()

for i, col in enumerate(cols):
    values = col.values
    is_sep = col.is_separator
    content = col.content
    print(f"Col {i:2d}: values={repr(values)} sep={is_sep} content={repr(content)}")
