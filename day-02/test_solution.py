"""Tests for Advent of Code 2025 - Day 02 Part 1.

Test suite for Gift Shop Invalid Product ID Detection.
Following TDD approach: RED-GREEN-REFACTOR.
"""


# ============================================================================
# User Story 1: Detect Invalid Product IDs in Single Range
# ============================================================================


def test_is_invalid_id():
    """Test invalid ID pattern detection.

    Invalid IDs are numbers where a digit sequence is repeated exactly twice.
    Examples: 55 (5+5), 6464 (64+64), 123123 (123+123)
    """
    from solution import is_invalid_id

    # Valid patterns - should return True
    assert is_invalid_id(55), "55 should be invalid (5+5)"
    assert is_invalid_id(6464), "6464 should be invalid (64+64)"
    assert is_invalid_id(123123), "123123 should be invalid (123+123)"
    assert is_invalid_id(1010), "1010 should be invalid (10+10)"
    assert is_invalid_id(99), "99 should be invalid (9+9)"

    # Invalid patterns - should return False
    assert not is_invalid_id(101), "101 has odd length, cannot split evenly"
    assert not is_invalid_id(1234), "1234: first half (12) != second half (34)"


def test_is_invalid_id_edge_cases():
    """Test edge cases for invalid ID detection."""
    from solution import is_invalid_id

    # Two-digit repeats
    assert is_invalid_id(11), "11 should be invalid (1+1)"
    assert is_invalid_id(22), "22 should be invalid (2+2)"

    # Four-digit repeats
    assert is_invalid_id(1212), "1212 should be invalid (12+12)"

    # Single digits (odd length)
    assert not is_invalid_id(5), "Single digit 5 has odd length"
    assert not is_invalid_id(9), "Single digit 9 has odd length"

    # Three digits (odd length)
    assert not is_invalid_id(121), "121 has odd length"


def test_find_invalid_ids_in_range():
    """Test finding invalid IDs within a range."""
    from solution import find_invalid_ids_in_range

    # Example from spec: range 11-22 contains [11, 22]
    result = find_invalid_ids_in_range(11, 22)
    assert result == [11, 22], f"Expected [11, 22], got {result}"

    # Example from spec: range 95-115 contains [99]
    result = find_invalid_ids_in_range(95, 115)
    assert result == [99], f"Expected [99], got {result}"

    # Example from spec: range 998-1012 contains [1010]
    result = find_invalid_ids_in_range(998, 1012)
    assert result == [1010], f"Expected [1010], got {result}"

    # Example from spec: range 1698522-1698528 contains no invalid IDs
    result = find_invalid_ids_in_range(1698522, 1698528)
    assert result == [], f"Expected [], got {result}"

    # Single ID range
    result = find_invalid_ids_in_range(55, 55)
    assert result == [55], f"Expected [55], got {result}"


# ============================================================================
# User Story 2: Process Multiple Ranges
# ============================================================================


def test_parse_ranges():
    """Test comma-separated range parsing."""
    from solution import parse_ranges

    # Basic multi-range parsing
    result = parse_ranges("11-22,95-115")
    expected = [(11, 22), (95, 115)]
    assert result == expected, f"Expected {expected}, got {result}"

    # Three ranges
    result = parse_ranges("11-22,95-115,998-1012")
    expected = [(11, 22), (95, 115), (998, 1012)]
    assert result == expected, f"Expected {expected}, got {result}"

    # Single range
    result = parse_ranges("998-1012")
    expected = [(998, 1012)]
    assert result == expected, f"Expected {expected}, got {result}"


def test_parse_ranges_edge_cases():
    """Test edge cases for range parsing."""
    from solution import parse_ranges

    # With whitespace
    result = parse_ranges("11-22, 95-115")
    expected = [(11, 22), (95, 115)]
    assert result == expected, f"Expected {expected}, got {result}"

    # Empty input
    result = parse_ranges("")
    expected = []
    assert result == expected, f"Expected {expected}, got {result}"

    # Large numbers
    result = parse_ranges("1188511880-1188511890")
    expected = [(1188511880, 1188511890)]
    assert result == expected, f"Expected {expected}, got {result}"


# ============================================================================
# User Story 3: Calculate Total Sum of Invalid IDs
# ============================================================================


def test_solve_part1_simple():
    """Test solve_part1 with simple cases."""
    from solution import solve_part1

    # Single range with 2 invalid IDs: 11 + 22 = 33
    result = solve_part1("11-22")
    expected = 33
    assert result == expected, f"Expected {expected}, got {result}"

    # Two ranges: [11, 22] + [99] = 132
    result = solve_part1("11-22,95-115")
    expected = 132
    assert result == expected, f"Expected {expected}, got {result}"


def test_solve_part1_example():
    """Test solve_part1 with full example from problem description."""
    from solution import solve_part1

    example_input = (
        "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,"
        "1698522-1698528,446443-446449,38593856-38593862,565653-565659,"
        "824824821-824824827,2121212118-2121212124"
    )

    result = solve_part1(example_input)
    expected = 1227775554
    assert result == expected, f"Expected {expected}, got {result}"


def test_solve_part1_edge_cases():
    """Test solve_part1 edge cases."""
    from solution import solve_part1

    # Empty input
    result = solve_part1("")
    expected = 0
    assert result == expected, f"Expected {expected}, got {result}"

    # Range with no invalid IDs
    result = solve_part1("1698522-1698528")
    expected = 0
    assert result == expected, f"Expected {expected}, got {result}"
