from pathlib import Path
from solution import parse_input, count_zero_crossings_during_rotation, apply_rotation

test_input = Path(__file__).parent / "test_input.txt"
rotations = parse_input(test_input.read_text())

position = 50
total = 0
for i, (direction, distance) in enumerate(rotations):
    during = count_zero_crossings_during_rotation(position, direction, distance)
    new_pos = apply_rotation(position, direction, distance)
    end = 1 if new_pos == 0 else 0
    total += during + end
    print(f'{i+1}. {direction}{distance:3d}: {position:2d} -> {new_pos:2d}, during={during}, end={end}, total={total}')
    position = new_pos

print(f'\nFinal total: {total}')
print(f'Expected: 6')
