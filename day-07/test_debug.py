from .solution import simulate_beams

# Test grid 1: Simple S moving down
grid1 = ["S..", "...", ".^.", "..."]
result1 = simulate_beams(grid1, (0, 0))
print(f"Grid1 result: {result1}")
print("Grid1:")
for i, row in enumerate(grid1):
    print(f"  Row {i}: {row}")
print(f"Starting at (0, 0) which is '{grid1[0][0]}'")
print(f"Moving down to (1, 0): '{grid1[1][0]}'")
print(f"Moving down to (2, 0): '{grid1[2][0]}' <- This is a splitter")
print()

# Test grid 2:
grid2 = ["S....", ".....", ".^.^.", "....."]
result2 = simulate_beams(grid2, (0, 0))
print(f"Grid2 result: {result2}")
print("Grid2:")
for i, row in enumerate(grid2):
    print(f"  Row {i}: {row}")
print(f"Starting at (0, 0) which is '{grid2[0][0]}'")
print(f"Moving down to (1, 0): '{grid2[1][0]}'")
print(f"Moving down to (2, 0): '{grid2[2][0]}' <- This is a splitter")
