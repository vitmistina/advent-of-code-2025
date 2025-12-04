"""Debug script to verify the solution."""

from solution import solve_part1, parse_grid, count_adjacent_rolls, is_accessible

# Test the example from description
test_input = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""

result = solve_part1(test_input)
print(f"Example result: {result} (expected: 13)")

# Now let's visualize which ones are accessible
grid = parse_grid(test_input)
print("\nVisualization of accessible rolls:")
for r, row in enumerate(grid):
    line = ""
    for c, val in enumerate(row):
        if val == "@":
            adj = count_adjacent_rolls(grid, r, c)
            if is_accessible(adj):
                line += "x"
            else:
                line += "@"
        else:
            line += "."
    print(line)

# Check with actual input
print("\n" + "=" * 50)
with open("input.txt") as f:
    actual_input = f.read()

actual_result = solve_part1(actual_input)
print(f"Actual input result: {actual_result}")

# Let's check grid dimensions
actual_grid = parse_grid(actual_input)
print(f"Grid dimensions: {len(actual_grid)} x {len(actual_grid[0])}")
print(f"Total @ symbols: {sum(row.count('@') for row in actual_grid)}")
