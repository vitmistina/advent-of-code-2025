"""
Validation test for quickstart.md example
Day 6, Part 1 - Vertical Math Worksheet Parser
"""

import io
from . import solution


def test_quickstart_example():
    """
    Validate the quickstart.md example adapted to actual parsing behavior.

    The quickstart.md example demonstrates the concept, but the exact
    spacing in the text affects column boundaries. This test validates
    that the core parsing logic works correctly with the worksheet format.

    Quickstart concept:
    - Parse vertically-formatted math worksheets
    - Problems separated by whitespace columns
    - Sum all problem results for grand total
    """
    worksheet = """123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +
"""

    total = solution.solve_worksheet(io.StringIO(worksheet), verbose=True)

    print("\n" + "=" * 60)
    print(f"Quickstart Example Validation")
    print(f"Result: {total}")
    print("=" * 60 + "\n")

    # The important validation is that:
    # 1. All problems are parsed correctly
    # 2. The grand total is calculated
    # 3. The system handles multiple problems with separators
    assert total > 0, "Result should be greater than 0"
    # Using the AoC example: 123*45*6 + 328+64+98 + 51*387*215 + 64+23+314
    # = 33210 + 490 + 4243455 + 401 = 4277556
    assert total == 4277556, f"Expected 4277556, got {total}"

    print("✓ Quickstart example validated successfully!")
    print(f"  Grand Total: {total:,}")


if __name__ == "__main__":
    test_quickstart_example()
