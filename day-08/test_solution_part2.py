"""Tests for Day 8 Part 2: Complete Circuit Formation."""

import pytest
from .solution_part2 import solve_part2


def test_example_final_connection():
    """Test example: final connection should produce 25272."""
    from pathlib import Path

    test_input = Path(__file__).parent / "test_input.txt"
    input_data = test_input.read_text()
    result = solve_part2(input_data)
    assert result == 25272, f"Expected final connection to produce 216 × 117 = 25272, got {result}"
