from solution import parse_grid, simulate_beams

grid, start_pos = parse_grid("test_input.txt")
print(f"Grid size: {len(grid)} rows x {len(grid[0])} cols")
print(f"Start pos: {start_pos}")
print(f"Start char: {grid[start_pos[0]][start_pos[1]]}")

# Count splitters
splitter_count = sum(row.count("^") for row in grid)
print(f"Total splitters in grid: {splitter_count}")

# Run simulation with the new logic
result = simulate_beams(grid, start_pos)
print(f"\nFinal split count: {result}")
print("Expected: 21")
