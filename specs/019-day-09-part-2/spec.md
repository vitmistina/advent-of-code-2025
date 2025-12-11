# Feature Specification: Day 9 Part 2 - Largest Red-Green Rectangle (Optimized Ray Tracing)

**Feature Branch**: `019-day-09-part-2`  
**Created**: December 10, 2025  
**Status**: Ready for Planning  
**Input**: User description: "Solve Day 9 Part 2: Find largest rectangle using red and green tiles with optimized ray tracing algorithm"

## User Scenarios & Testing _(mandatory)_

### User Story 1 - Parse Loop and Classify Convex vs Concave Turns (Priority: P1)

The puzzle solver needs to parse the ordered list of red tile coordinates, validate that each consecutive pair is axis-aligned, and label each vertex as either a convex (+90° clockwise) or concave (-90° counter-clockwise) turn. During parsing the solver must also compute the polygon winding (clockwise/counter-clockwise) so that "right" and "left" turns are interpreted consistently regardless of the input ordering.

**Why this priority**: Accurate direction deltas, winding detection, and convex/concave classification provide the geometric primitives used by later ray tracing steps; removing the unnecessary J/L/F/7 taxonomy simplifies the implementation while keeping all required information.

**Independent Test**: Can be fully tested by parsing the example input with 8 red tiles and verifying axis alignment, signed area / winding, and turn classification (considering wraparound from last to first).

**Acceptance Scenarios**:

1. **Given** the example puzzle input with 8 red tile coordinates, **When** parsing the coordinates, **Then** all coordinates are correctly extracted and wrapped: (7,1), (11,1), (11,7), (9,7), (9,5), (2,5), (2,3), (7,3)

2. **Given** red tile at (7,1) with previous (7,3) and next (11,1), **When** computing the turn, **Then** it is marked as convex (+90°) assuming clockwise winding

3. **Given** red tile at (9,5) with previous (9,7) and next (2,5), **When** computing the turn, **Then** it is marked as concave (-90°)

4. **Given** the full list, **When** summing the signed area, **Then** the solver identifies the traversal as clockwise (negative area) and stores that orientation for subsequent logic

5. **Given** verbose mode enabled, **When** parsing completes, **Then** output displays each red tile with its coordinate, incoming/outgoing directions, turn sign (convex/concave), and the detected winding direction

---

### User Story 2 - Precompute Green Edge Tiles into Directional Sets (Priority: P1)

The puzzle solver needs to precompute all green edge tiles (connecting consecutive red tiles) and organize them into two sets: horizontal edges and vertical edges. The edge computation must handle wraparound from the last red tile to the first red tile.

**Why this priority**: Precomputed edge sets enable efficient ray tracing without iterating over every grid position, which is critical for performance with long edges.

**Independent Test**: Can be fully tested by computing edges from example input and verifying horizontal and vertical sets contain the correct green tile positions along each edge segment.

**Acceptance Scenarios**:

1. **Given** red tiles at (7,1) and (11,1) connected horizontally, **When** computing green edges, **Then** all intermediate tiles (8,1), (9,1), (10,1) are added to the horizontal edge set
2. **Given** red tiles at (11,1) and (11,7) connected vertically, **When** computing green edges, **Then** all intermediate tiles (11,2), (11,3), (11,4), (11,5), (11,6) are added to the vertical edge set
3. **Given** the last red tile and first red tile, **When** computing edges, **Then** the wraparound edge is correctly computed and added to the appropriate edge set
4. **Given** verbose mode enabled, **When** edge computation completes, **Then** output displays the count of horizontal and vertical green edge tiles

---

### User Story 3 - Cast Rays with Formal Start Rules and Boundary Handling (Priority: P1)

For each candidate rectangle defined by two red tile corners, the puzzle solver needs to cast rays from each corner in the two directions perpendicular to that corner. Each ray uses a prefiltered combination of the appropriate edge set (horizontal or vertical) and includes both convex and concave corners, but concave corners only affect the ray when approached from their blocking side. Rays operate on half-open segments so that touching a boundary tile counts as leaving the valid region.

**Ray Starting Logic**: Each ray starts from the tile adjacent to the rectangle corner after stepping one unit in the ray direction. The solver first checks whether that half-open interval intersects a perpendicular boundary segment; if so the ray state is immediately "outside", otherwise it begins "inside". This removes ambiguity about "starting on the corner" and guarantees deterministic toggling.

**Why this priority**: Precise start rules and consistent boundary toggling are the backbone of the edge-only validation strategy; without them the algorithm can misclassify rectangles that skim concave pockets.

**Independent Test**: Can be fully tested by casting rays for known rectangles and verifying the ordered list of segment tuples (start, end, in/out) against hand-derived expectations, including cases that touch concave corners.

**Acceptance Scenarios**:

1. **Given** a convex corner at (11,1) whose outgoing edge runs downward, **When** casting a ray downward from (11,2), **Then** the ray starts "inside" because the half-open interval [2, ?) does not cross a perpendicular edge

2. **Given** a convex corner at (7,1) that is adjacent to a vertical barrier to its left, **When** casting a ray leftward from (6,1), **Then** the initial interval immediately intersects that barrier and the ray starts "outside"

3. **Given** a concave corner at (9,5), **When** casting a ray along the concave pocket, **Then** the ray stays "inside" until it reaches the next convex boundary even though it runs adjacent to the concave tiles

4. **Given** consecutive edge crossings at adjacent tiles, **When** computing segments, **Then** zero-width "outside" segments are ignored so that hugging the boundary does not invalidate an otherwise interior ray

5. **Given** a ray traveling down at x=11 from (11,1) to (11,7), **When** filtering edges, **Then** only horizontal edges with x=11 and all corners sharing x=11 are considered, regardless of convexity

6. **Given** a ray that encounters no edge crossings, **When** generating segments, **Then** the entire ray is one "inside" segment from start to end

7. **Given** verbose mode enabled, **When** ray casting for a rectangle, **Then** output displays filtered edge count, ray direction, start state, and segment boundaries for each ray

---

### User Story 4 - Validate Rectangles via Boundary Segments and Find Maximum Area (Priority: P1)

The puzzle solver needs to enumerate all possible rectangles formed by pairs of red tiles, validate each using the ray segment data collected along the four rectangle edges (reject rectangles whose edges cross into "outside" segments), calculate valid rectangle areas, and identify the maximum. Because the polygon is guaranteed to be a simple, hole-free loop whose interior is entirely green, checking the edges is sufficient: if every boundary segment stays inside, no gray tiles can "leak" into the rectangle interior. The solver must still avoid iterating over every tile along each edge.

**Why this priority**: This combines all previous components into the final solution—finding the largest valid rectangle while leveraging the simple-polygon guarantee.

**Independent Test**: Can be fully tested by running on the example input and verifying the maximum area is 24, with step-by-step output showing which rectangles are valid/invalid.

**Acceptance Scenarios**:

1. **Given** a rectangle between red tiles (9,5) and (2,3), **When** checking ray segments, **Then** all four rectangle edges fall within "inside" segments, making it valid with area 24
2. **Given** all possible red tile pairs in the example (28 combinations), **When** evaluating each rectangle, **Then** only rectangles without "outside" segment crossings are marked valid
3. **Given** all valid rectangles, **When** comparing areas, **Then** the maximum area of 24 is correctly identified
4. **Given** verbose mode enabled, **When** rectangle validation runs, **Then** output displays each candidate rectangle with its validity status and area

---

### User Story 5 - Execute Final Solution with Minimal Output (Priority: P1)

The puzzle solver needs to run in production mode (no verbose output) on the actual puzzle input and produce only the final answer as a single integer, without overloading the terminal with intermediate outputs.

**Why this priority**: This is the ultimate success criterion - the solution must work efficiently on the actual input and provide a clean answer for submission.

**Independent Test**: Can be fully tested by running the solution on actual puzzle input and verifying it produces the correct answer in reasonable time with minimal terminal output.

**Acceptance Scenarios**:

1. **Given** the actual puzzle input for Day 9 Part 2, **When** running the solution in production mode, **Then** only the final maximum rectangle area is printed
2. **Given** the solution result, **When** submitting to Advent of Code, **Then** the answer is accepted as correct
3. **Given** the solution implementation with large input, **When** executed, **Then** it completes in under 10 seconds without memory issues

---

### Edge Cases

- What happens when a ray is cast along a coordinate where no edges exist?
  - Answer: The filtered edge set will be empty, and the entire ray segment is marked as "inside" (starting assumption since ray starts from a red tile inside the polygon).
- How are corner tiles handled when they align with a ray direction?
  - Answer: Corners are included in the filtered set based on their type - only corners that represent edges perpendicular to the ray direction are included.
- What happens when two red tiles are adjacent (minimal distance)?
  - Answer: The rectangle formed will have minimal area; ray tracing will still work correctly to validate if all edges are inside the polygon.
- What happens when two consecutive edge crossings create a zero-width "outside" segment (e.g., pattern `>||.|` where `|` represents vertical edges)?
  - Answer: When two edges are on consecutive tiles, they create an "outside" segment of width zero (e.g., crossing from inside to outside at position 1, then back to inside at position 2). These zero-width outside segments should be ignored since we're transitioning from green tile to green tile. Only non-zero-width outside segments indicate areas that would invalidate a rectangle. Example: in `>||.|` starting inside, the first two `|` create outside segment of width 0 (ignored), and only the third `|` creates a proper inside→outside transition.

## Requirements _(mandatory)_

### Functional Requirements

- **FR-001**: System MUST parse a list of red tile coordinates in (x,y) format from the puzzle input
- **FR-002**: System MUST validate that consecutive red tiles in the list are aligned either horizontally or vertically (same x or same y coordinate)
- **FR-003**: System MUST treat the list as a closed loop, computing incoming/outgoing direction vectors for every vertex with wraparound
- **FR-004**: System MUST compute the polygon winding via signed area and classify each turn as convex (+90° relative to the detected winding) or concave (-90°)
- **FR-005**: System MUST precompute all green edge tiles between consecutive red tiles (including the wraparound edge) and organize them into horizontal and vertical sets filtered by coordinate
- **FR-006**: System MUST enumerate all possible rectangles formed by pairs of red tiles as opposite corners
- **FR-007**: For each rectangle corner, system MUST cast rays in the two perpendicular directions from that corner (e.g., top-right corner casts down and left)
- **FR-008**: System MUST filter edge sets by shared coordinate (x or y) to avoid iterating over irrelevant tiles, and include both convex and concave corners while respecting their blocking directions
- **FR-009**: System MUST start each ray using the half-open interval that begins one tile away from the corner in the ray direction
- **FR-010**: System MUST determine initial ray state (inside/outside) by checking whether that half-open interval immediately intersects a perpendicular boundary segment
- **FR-011**: System MUST generate ray segments as tuples (start, end, in_or_out) based on edge crossings, toggling state after each crossing and ignoring zero-width outside segments caused by adjacent crossings
- **FR-012**: System MUST validate rectangles by checking whether any of the four edges overlap with a non-zero-width outside segment; if none do, the rectangle is considered entirely inside by the simple-polygon guarantee
- **FR-013**: System MUST calculate the area of each valid rectangle (width × height including corners)
- **FR-014**: System MUST identify and return the maximum area among all valid rectangles
- **FR-015**: System MUST support verbose mode for step-by-step output with visualization (limited to manageable datasets)
- **FR-016**: System MUST support production mode with minimal output (only final answer)
- **FR-017**: System MUST handle the rectangular coordinate system where x increases rightward and y increases downward

### Key Entities _(include if feature involves data)_

- **Red Tile**: A tile explicitly listed in the puzzle input coordinates; stores incoming/outgoing direction vectors plus convex/concave turn metadata; serves as required rectangle corner
- **Green Edge Tile**: A tile on the straight path between consecutive red tiles; precomputed into horizontal or vertical edge sets
- **Turn Direction**: Classification of rotation angle at each red tile - convex (+90° relative to winding) or concave (-90°); both types may intersect rays, but concave corners only block from one side
- **Edge Set**: Precomputed collection of green edge tiles organized by orientation (horizontal or vertical)
- **Ray**: A directional scan from a rectangle corner; uses filtered edge/corner sets to identify inside/outside segments
- **Segment**: A tuple (start, end, in_or_out) representing a continuous region along a ray where tiles are inside or outside the polygon
- **Rectangle**: A region bounded by two red tiles as opposite corners; valid only if all edges fall within "inside" segments

## Success Criteria _(mandatory)_

### Measurable Outcomes

- **SC-001**: Parser correctly extracts all red tile coordinates from example input (8 tiles in test case)
- **SC-002**: Corner classification correctly labels each tile as convex or concave based on neighbor directions with wraparound and the detected winding
- **SC-003**: Turn direction classification matches the expected convex (7,1), (11,1), (11,7), (9,7), (2,5), (2,3) and concave (9,5), (7,3) corners in the example input
- **SC-004**: Green edge precomputation correctly identifies all horizontal and vertical edge tiles between consecutive red pairs including wraparound
- **SC-005**: Edge set filtering reduces search space by only selecting edges with matching x or y coordinate for each ray direction
- **SC-006**: Ray filtering correctly incorporates convex corners and recognizes concave corners only when approached from their blocking side
- **SC-007**: Ray tracing generates accurate segment tuples (start, end, in_or_out) for the two perpendicular directions from each rectangle corner
- **SC-008**: Ray tracing correctly determines initial inside/outside state based on whether the half-open starting interval intersects a perpendicular edge
- **SC-009**: Rectangle validation correctly rejects candidates whose edges cross into "outside" segments
- **SC-010**: Maximum rectangle calculation correctly returns area 24 for example input
- **SC-011**: Verbose mode displays step-by-step output including turn metadata (convex/concave), edge counts, ray segments, and rectangle validation results
- **SC-012**: Production mode outputs only the final answer without intermediate visualization
- **SC-013**: Solution completes execution on actual input in under 10 seconds without memory issues
- **SC-014**: Solution produces correct answer when executed on actual puzzle input (verified by Advent of Code submission)

## Assumptions

- Puzzle input is well-formed (coordinates are integers, proper format)
- Red tile coordinates form a simple, closed loop with no self-intersections or holes; all tiles strictly inside that loop are green
- Consecutive red tiles are always aligned horizontally or vertically
- The solver detects the polygon winding (and asserts it matches the expected clockwise direction in the provided data); all turn signs are interpreted relative to that detected winding
- Grid size is large enough to make naive approaches inefficient, necessitating optimized ray tracing
- Rays start at the tile adjacent to the corner in the ray direction, modeled as a half-open interval so touching a boundary counts as leaving the interior
- Initial ray state (inside/outside) is determined by whether that initial half-open interval immediately intersects a perpendicular edge
- Concave (left-hand) corners remain part of the boundary; rays recognize them when approached from the blocking side instead of ignoring them outright
- Edge crossings alternate between inside and outside states; consecutive crossings at adjacent tiles create zero-width outside segments that are ignored
- No edge cases exist where multiple edges overlap at the same coordinate along a ray (aside from the deliberate zero-width cases above)

## Technical Approach Notes

### Turn Classification and Winding Detection

For each red tile, the solver computes the vector from the previous tile (incoming edge) and the vector to the next tile (outgoing edge). Using these vectors and the signed area (winding), the solver determines whether the turn is convex (+90° relative to the winding) or concave (-90°). This retains all meaningful geometric information without introducing additional corner labels.

Example from the test input (7,1) with previous (7,3) and next (11,1): incoming vector = Up, outgoing vector = Right. Given a clockwise loop, the rotation is +90°, so the corner is convex. At (9,5), the rotation is -90°, so it is concave.

### Ray Filtering Strategy

For each ray direction from a rectangle corner, the system selects the appropriate edge set (horizontal edges for vertical rays, vertical edges for horizontal rays) filtered by the ray's fixed coordinate. All corners on that coordinate are also considered. Convex corners always behave as blockers. Concave corners only affect the ray when it approaches from the side where the polygon boundary protrudes inward; otherwise the ray simply glides along the interior.

Each rectangle corner casts rays in its two perpendicular directions. Because the algorithm models rays as half-open intervals, it consistently treats touching a boundary as invalid while allowing rays that run adjacent to concave regions without toggling state unnecessarily. When a ray encounters a corner tile that belongs to both a horizontal and a vertical edge, the perpendicular edge is processed first (flipping the state), then the parallel edge is considered only if the ray keeps traveling along that direction. All events along a coordinate are sorted, so crossings are applied in strictly increasing order of distance from the ray origin.

**Initial Ray State**: The ray's initial inside/outside state is determined as follows:

- Use the winding detected in User Story 1 to establish the inward normal. For clockwise loops, the interior is always to the right of each directed edge; for counter-clockwise loops it is to the left.
- Compute the ray direction vector (dx, dy) and the inward normal of the outgoing edge at the corner: `inward = (dy, -dx)` for clockwise winding, `inward = (-dy, dx)` otherwise.
- Check if the first unit step in the ray direction immediately intersects an edge whose outward normal opposes the ray; if so the half-open interval is already outside and the ray starts "outside". Otherwise it starts "inside".
- Because every corner stores both incoming and outgoing direction vectors, the algorithm can consistently choose the outward normal regardless of how the polygon was listed in the input.

Example: A ray going left from right-turn corner (9,5) filters vertical edges where y=5, plus right-turn F and 7 corners (which have vertical edges extending "downward"). Left-turn corners like (9,5) itself are ignored. The ray starts at (8,5); because the inward normal for clockwise winding points down/right at that corner, stepping left does not cross a perpendicular barrier, so the state begins "inside".

Example: A ray going downward from convex corner (11,1) inherits the outgoing edge direction `(0, +1)`; for clockwise winding the inward normal points to the right, meaning the adjacent tile `(11,2)` is still interior, so the state begins "inside". Conversely, casting a ray leftward from convex corner (7,1) immediately meets the vertical segment at x=6 whose outward normal points right, so the half-open interval is outside before traveling any distance.

### Segment Generation Logic

Ray segments track inside/outside state as the ray crosses edges:

1. Ray starts at a red tile (inside the polygon) → initial state = "inside"
2. Each edge crossing toggles the state: inside → outside → inside → outside...
3. Segments are recorded as tuples: (start_coord, end_coord, in_or_out)
4. Zero-width "outside" segments (consecutive edge crossings) should be ignored, as they represent transitions through adjacent green tiles
5. Rectangle validation checks if any rectangle edge overlaps with a non-zero-width "outside" segment

Example: For ray pattern `>||.|.` starting inside at position 0:

- Position 1: Cross edge → transition to "outside"
- Position 2: Cross edge → transition to "inside" (creates outside segment of width 0, ignored)
- Position 3: Cross edge → transition to "outside" (creates valid inside segment from 2 to 3)
- Only the final "outside" segment matters for validation

### Concave Corner Walkthrough (Example Input)

```
0 1 2 3 4 5 6 7 8 9 10111213
. . . . . . . . . . . . . .
. . . . . . . # . . . # . .
. . . . . . . . . . . . . .
. . # . . . . # . . . . . .
. . . . . . . . . . . . . .
. . # . . . . . . # . . . .
. . . . . . . . . . . . . .
. . . . . . . . . # . # . .
. . . . . . . . . . . . . .
```

**Horizontal ray leftward from (9,7)**

The ray starts at (8,7). It starts outside.
Expected segments:

- (8 to bounds) outside

**Vertical ray downward from (9,7)**
The ray starts at (9,8). It starts outside. Expected segments:

- (8 to bounds) outside

**Horizontal ray rightward from (9,7)**
The ray starts at (10,7). It starts inside. Then at (11,7) it meets a convex corner, toggling to outside. Expected segments:

- (10 to 11) inside
- (11 to bounds) outside

**Vertical ray upward from (9,7)**
The ray starts at (9,6). It starts inside. Then at (9,5) it meets a concave corner, so it remains inside. Next at (9,1) it meets a horizontal edge, toggling to outside. Expected segments:

- (6 to 1) inside
- (1 to bounds) outside

### Performance Optimization

The key optimization is coordinate filtering:

- Instead of checking every tile along a ray (O(grid_size)), filter edges by shared coordinate
- Example: For a horizontal ray at y=5, only process edges where y=5
- This reduces iteration to O(edges_at_coordinate) which is typically much smaller

### Edge-Only Rectangle Validation Justification

This solver deliberately **embraces** the guarantee from the puzzle text: the red tiles form a simple loop, every tile on that loop is red or green, and every tile strictly inside the loop is green. Given that invariant, an axis-aligned rectangle can only include invalid tiles if one of its four boundary rays crosses from green into gray. To see why:

1. The Jordan-curve guarantee for the red/green loop ensures every horizontal or vertical scan line intersects the boundary an even number of times. If a rectangle edge stays within "inside" segments, that scan line never crosses into gray.
2. Once both edges on a pair of opposite sides (top/bottom or left/right) are confirmed inside, every tile between them is also inside because the interior is completely filled. We never need to sample the billions of interior tiles explicitly; the edge tests propagate the guarantee inward.
3. Concavities (the "U" concern) necessarily pierce at least one of the rectangle edges. The walkthrough above shows that when a pocket intrudes, the ray aligned with the pocket's opening toggles outside immediately, so the rectangle is rejected before checking its area.

Therefore, validating rectangles solely via boundary rays is both correct (given the fill guarantee) and dramatically faster than scanning every tile.

### Verbose vs Production Mode

- **Verbose mode**: Displays corner classifications, edge counts, ray segments for each rectangle, validation status
- **Production mode**: Suppresses all intermediate output, prints only the final maximum area
