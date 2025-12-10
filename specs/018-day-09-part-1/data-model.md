# Data Model: AoC Day 9 Part 1 - Largest Red Tile Rectangle

## Entities

### Red Tile

- **Description**: A coordinate point (x, y) in the grid, representing a location of a red tile.
- **Fields**:
  - `x`: int (non-negative)
  - `y`: int (non-negative)
- **Validation**:
  - Both `x` and `y` must be integers >= 0
  - Must be parsed from input in "x,y" format

### Rectangle

- **Description**: A shape defined by two opposite corner tiles, with area calculated as width × height.
- **Fields**:
  - `corner1`: Red Tile
  - `corner2`: Red Tile
  - `area`: int (calculated as |x1 - x2| × |y1 - y2|)
- **Validation**:
  - `corner1` and `corner2` must be distinct
  - Area must be >= 0

## Relationships

- Each Rectangle is formed by a unique pair of Red Tiles.
- The largest Rectangle is the one with the maximum area among all possible pairs.

## State Transitions

- **Initial**: Parse all Red Tiles from input
- **Intermediate**: Generate all possible Rectangle pairs
- **Final**: Identify and return the largest Rectangle area

## Edge Cases

- Fewer than 2 Red Tiles: Cannot form a rectangle (error)
- Collinear tiles: Rectangle area may be zero or minimal
- Multiple pairs with same max area: Return any one

## Example

- Input: "2,5", "11,1" → Red Tiles: (2,5), (11,1)
- Rectangle area: |2-11| × |5-1| = 9 × 4 = 36

## Validation Rules

- Input must be non-empty and well-formed
- All coordinates must be non-negative integers
- Only distinct pairs of Red Tiles are considered
