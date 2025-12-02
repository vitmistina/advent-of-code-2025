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


# ============================================================================
# PART 2 TESTS: Extended Pattern Detection (At Least Twice)
# ============================================================================


# ============================================================================
# Phase 2: User Story 1 - Pattern Detection (RED Phase)
# ============================================================================


def test_is_invalid_id_part2():
    """Test Part 2 pattern detection (at least twice).
    
    Part 2 detects patterns repeated at least 2 times (vs exactly 2 in Part 1).
    Examples: 11 (1×2), 111 (1×3), 565656 (56×3), 824824824 (824×3), 2121212121 (21×5)
    """
    from solution import is_invalid_id_part2
    
    # Part 1 overlap (exactly twice - still invalid in Part 2)
    assert is_invalid_id_part2(11), "11 is invalid (1×2)"
    assert is_invalid_id_part2(22), "22 is invalid (2×2)"
    assert is_invalid_id_part2(1010), "1010 is invalid (10×2)"
    
    # NEW in Part 2 (three or more times)
    assert is_invalid_id_part2(111), "111 is invalid (1×3)"
    assert is_invalid_id_part2(565656), "565656 is invalid (56×3)"
    assert is_invalid_id_part2(824824824), "824824824 is invalid (824×3)"
    assert is_invalid_id_part2(2121212121), "2121212121 is invalid (21×5)"
    
    # Still valid
    assert not is_invalid_id_part2(101), "101 has no repeated pattern"
    assert not is_invalid_id_part2(12345), "12345 has no repeated pattern"


def test_check_range_part2_range_11_22():
    """Test Part 2 range checking: 11-22 should contain [11, 22]."""
    from solution import check_range_part2
    
    result = check_range_part2(11, 22)
    expected = [11, 22]
    assert result == expected, f"Expected {expected}, got {result}"


def test_check_range_part2_range_95_115():
    """Test Part 2 range checking: 95-115 should contain [99, 111]."""
    from solution import check_range_part2
    
    result = check_range_part2(95, 115)
    expected = [99, 111]
    assert result == expected, f"Expected {expected}, got {result}"


def test_check_range_part2_range_998_1012():
    """Test Part 2 range checking: 998-1012 should contain [999, 1010]."""
    from solution import check_range_part2
    
    result = check_range_part2(998, 1012)
    expected = [999, 1010]
    assert result == expected, f"Expected {expected}, got {result}"


def test_check_range_part2_range_1188511880_1188511890():
    """Test Part 2 range checking: 1188511880-1188511890 should contain [1188511885]."""
    from solution import check_range_part2
    
    result = check_range_part2(1188511880, 1188511890)
    expected = [1188511885]
    assert result == expected, f"Expected {expected}, got {result}"


def test_check_range_part2_range_222220_222224():
    """Test Part 2 range checking: 222220-222224 should contain [222222]."""
    from solution import check_range_part2
    
    result = check_range_part2(222220, 222224)
    expected = [222222]
    assert result == expected, f"Expected {expected}, got {result}"


def test_check_range_part2_range_1698522_1698528():
    """Test Part 2 range checking: 1698522-1698528 should contain [] (no invalids)."""
    from solution import check_range_part2
    
    result = check_range_part2(1698522, 1698528)
    expected = []
    assert result == expected, f"Expected {expected}, got {result}"


def test_check_range_part2_range_446443_446449():
    """Test Part 2 range checking: 446443-446449 should contain [446446]."""
    from solution import check_range_part2
    
    result = check_range_part2(446443, 446449)
    expected = [446446]
    assert result == expected, f"Expected {expected}, got {result}"


def test_check_range_part2_range_38593856_38593862():
    """Test Part 2 range checking: 38593856-38593862 should contain [38593859]."""
    from solution import check_range_part2
    
    result = check_range_part2(38593856, 38593862)
    expected = [38593859]
    assert result == expected, f"Expected {expected}, got {result}"


def test_check_range_part2_range_565653_565659():
    """Test Part 2 range checking: 565653-565659 should contain [565656]."""
    from solution import check_range_part2
    
    result = check_range_part2(565653, 565659)
    expected = [565656]
    assert result == expected, f"Expected {expected}, got {result}"


def test_check_range_part2_range_824824821_824824827():
    """Test Part 2 range checking: 824824821-824824827 should contain [824824824]."""
    from solution import check_range_part2
    
    result = check_range_part2(824824821, 824824827)
    expected = [824824824]
    assert result == expected, f"Expected {expected}, got {result}"


def test_check_range_part2_range_2121212118_2121212124():
    """Test Part 2 range checking: 2121212118-2121212124 should contain [2121212121]."""
    from solution import check_range_part2
    
    result = check_range_part2(2121212118, 2121212124)
    expected = [2121212121]
    assert result == expected, f"Expected {expected}, got {result}"


# ============================================================================
# Phase 3: User Story 2 - Multi-Range Aggregation (RED Phase)
# ============================================================================


def test_solve_part2_example():
    """Test Part 2 with complete example input."""
    from solution import solve_part2
    
    example_input = (
        "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,"
        "1698522-1698528,446443-446449,38593856-38593862,565653-565659,"
        "824824821-824824827,2121212118-2121212124"
    )
    
    result = solve_part2(example_input)
    expected = 4174379265
    assert result == expected, f"Expected {expected}, got {result}"


def test_solve_part2_multiple_ranges():
    """Test Part 2 multi-range aggregation with subset."""
    from solution import solve_part2
    
    # Test with first two ranges: [11, 22] + [99, 111] = 243
    result = solve_part2("11-22,95-115")
    expected = 11 + 22 + 99 + 111  # 243
    assert result == expected, f"Expected {expected}, got {result}"


def test_solve_part2_empty_input():
    """Test Part 2 with empty input."""
    from solution import solve_part2
    
    result = solve_part2("")
    expected = 0
    assert result == expected, f"Expected {expected}, got {result}"
