from .solution_part2 import ManifoldDiagram, count_timelines


def test_invalid_input_missing_start():
    diagram = [".....^..", ".^..^..."]
    try:
        ManifoldDiagram(diagram)
    except ValueError as e:
        assert "No start position" in str(e)
    else:
        raise AssertionError("Expected ValueError for missing start position")


def test_invalid_input_bad_char():
    diagram = ["S..@^..", ".^..^.."]
    try:
        ManifoldDiagram(diagram)
    except ValueError as e:
        assert "Invalid character" in str(e)
    else:
        raise AssertionError("Expected ValueError for invalid character")


def test_full_example():
    with open("day-07/test_input.txt") as f:
        diagram = [line.rstrip("\n") for line in f]
    md = ManifoldDiagram(diagram)
    result = count_timelines(md)
    # Replace 40 with the correct expected value for your full example
    assert result == 40


def test_multiple_splitters():
    diagram = ["..S.", "..^.", ".^..", "...."]
    md = ManifoldDiagram(diagram)
    result = count_timelines(md)
    assert result == 3


def test_no_splitters():
    diagram = ["S", ".", ".", "."]
    md = ManifoldDiagram(diagram)
    result = count_timelines(md)
    assert result == 1


def test_single_splitter():
    diagram = [".S.", ".^.", "..."]
    md = ManifoldDiagram(diagram)
    result = count_timelines(md)
    assert result == 2
