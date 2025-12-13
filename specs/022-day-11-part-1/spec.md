# Feature Specification: Day 11 Part 1 - Reactor Path Finding

**Feature Branch**: `022-day-11-part-1`  
**Created**: December 13, 2025  
**Status**: Draft  
**Input**: User description: "Find all paths from 'you' device to 'out' device in a reactor device network"

## User Scenarios & Testing _(mandatory)_

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.

  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Parse Device Configuration (Priority: P1)

An operations engineer needs to load and understand the reactor's device configuration from a structured input file. Each device is defined with its name and the list of devices its outputs connect to. The system must correctly parse and represent this device network so that path analysis can be performed.

**Why this priority**: This is the foundation - without parsing the input correctly, no path analysis is possible. This is the first critical step in the solution.

**Independent Test**: Can be fully tested by loading any valid device configuration file and verifying that all devices and their connections are correctly extracted and represented in memory.

**Acceptance Scenarios**:

1. **Given** a device configuration with single connections (`you: bbb`), **When** parsing, **Then** the system correctly identifies that device "you" connects to device "bbb"

2. **Given** a device configuration with multiple connections (`bbb: ddd eee`), **When** parsing, **Then** the system correctly identifies that device "bbb" has two outputs connecting to "ddd" and "eee" respectively

3. **Given** a complete device configuration:

   ```
   aaa: you hhh
   you: bbb ccc
   bbb: ddd eee
   ccc: ddd eee fff
   ddd: ggg
   eee: out
   fff: out
   ggg: out
   hhh: ccc fff iii
   iii: out
   ```

   **When** parsing, **Then** the system correctly creates all device connections (10 devices total with proper output mappings)

4. **Given** a device that appears in the configuration multiple times (e.g., `out` as a destination in multiple lines), **When** parsing, **Then** the system correctly handles the device without duplication

5. **Given** a configuration where devices appear only as destinations (like `out` or intermediate devices), **When** parsing, **Then** the system correctly recognizes these devices exist even if they aren't defined as sources

---

### User Story 2 - Build Complete Device Network Graph (Priority: P1)

An operations engineer needs the system to build a complete graph representation of the device network so that connectivity analysis can be performed. The system must identify all devices in the network and establish the proper relationships between them based on the configuration.

**Why this priority**: Without building the complete graph, we cannot determine what devices are reachable or perform path analysis. This is essential before any pathfinding can begin.

**Independent Test**: Can be fully tested by verifying that the graph structure contains all unique devices and all edges (connections) are properly established and bidirectionally consistent.

**Acceptance Scenarios**:

1. **Given** a parsed device configuration, **When** building the network graph, **Then** all unique devices are identified (including those that only appear as destinations)

2. **Given** the example configuration, **When** building the graph, **Then** the complete set of 10 devices {you, bbb, ccc, ddd, eee, fff, ggg, out, aaa, hhh, iii} is present in the graph

3. **Given** a device with no outputs (terminal device like `out`), **When** building the graph, **Then** the system correctly represents it as a node with no outgoing edges

4. **Given** a device with exactly one output, **When** building the graph, **Then** the connection is properly stored

5. **Given** a device with multiple outputs, **When** building the graph, **Then** all output connections are properly established and retrievable

6. **Given** the example configuration, **When** building the graph and querying connections, **Then** device "bbb" correctly lists its outputs as ["ddd", "eee"]

---

### User Story 3 - Find Single Path from Source to Target (Priority: P1)

An operations engineer needs the system to find at least one valid path from the "you" device to the "out" device, proving that a connection exists and the pathfinding algorithm works correctly.

**Why this priority**: Before finding all paths, we need to verify the basic pathfinding capability works. This is the foundation for the complete path enumeration.

**Independent Test**: Can be fully tested by verifying that at least one valid path from "you" to "out" can be discovered and that the path follows valid device connections.

**Acceptance Scenarios**:

1. **Given** a device graph with a connection chain (you → bbb → ddd → ggg → out), **When** finding a path from "you" to "out", **Then** at least one valid path is returned

2. **Given** the example device configuration, **When** finding a path from "you" to "out", **Then** a valid path such as [you, bbb, ddd, ggg, out] is returned

3. **Given** a path chain of length 2 (you → eee → out), **When** finding a path, **Then** the path [you, eee, out] is correctly identified

4. **Given** a starting device that is not "you", **When** attempting to find a path from "you", **Then** the path correctly starts from "you"

5. **Given** a device graph where "you" is directly connected to "out" (if applicable), **When** finding a path, **Then** the direct path [you, out] is correctly identified

---

### User Story 4 - Enumerate All Paths with Backtracking (Priority: P1)

An operations engineer needs the system to systematically find every possible path from the "you" device to the "out" device by exploring all branches of the device network. The system must use backtracking to explore alternative routes when multiple outputs are available.

**Why this priority**: This is the core requirement of the feature. Without complete path enumeration, the feature is not complete. This directly answers the user's question: "How many different paths lead from you to out?"

**Independent Test**: Can be fully tested by manually verifying the count of paths and validating that each path is valid and distinct.

**Acceptance Scenarios**:

1. **Given** the example device configuration with 5 documented paths, **When** enumerating all paths from "you" to "out", **Then** exactly 5 distinct paths are found:

   - Path 1: you → bbb → ddd → ggg → out
   - Path 2: you → bbb → eee → out
   - Path 3: you → ccc → ddd → ggg → out
   - Path 4: you → ccc → eee → out
   - Path 5: you → ccc → fff → out

2. **Given** a simple linear path (you → out), **When** enumerating paths, **Then** exactly 1 path is found: [you, out]

3. **Given** a configuration with a single branching point (you → a, a → out, a → b, b → out), **When** enumerating paths, **Then** exactly 2 paths are found:

   - you → a → out
   - you → a → b → out

4. **Given** a configuration with multiple branching points:

   ```
   you: a b
   a: x
   b: x
   x: out
   ```

   **When** enumerating paths, **Then** exactly 2 paths are found:

   - you → a → x → out
   - you → b → x → out

5. **Given** a complex branching structure like the example with 5 paths, **When** enumerating all paths, **Then** every path in the enumeration:

   - Starts with "you" device
   - Ends with "out" device
   - Follows valid device connections throughout
   - Is unique and never duplicated

6. **Given** the example configuration, **When** enumerating paths, **Then** device "ccc" appears in exactly 3 of the 5 paths (as an intermediate node)

7. **Given** the example configuration, **When** enumerating paths, **Then** device "ggg" appears in exactly 2 of the 5 paths (as a connection point between ddd and out)

---

### User Story 5 - Count Total Distinct Paths (Priority: P1)

An operations engineer needs the system to count and report the total number of distinct paths from "you" to "out" so they can provide the final answer to the Elf team.

**Why this priority**: The entire goal is to answer the question "How many different paths lead from you to out?" - the count is the primary deliverable.

**Independent Test**: Can be fully tested by verifying the count matches manual enumeration and that the count accurately represents the number of paths found.

**Acceptance Scenarios**:

1. **Given** the example device configuration, **When** counting all paths, **Then** the count is exactly 5

2. **Given** a single linear path (you → out), **When** counting paths, **Then** the count is 1

3. **Given** a simple branching (you → a → out, you → b → out), **When** counting paths, **Then** the count is 2

4. **Given** the complex example configuration with multiple levels of branching, **When** counting paths, **Then** the count accurately reflects all possible path combinations

5. **Given** no valid path exists from "you" to "out", **When** counting paths, **Then** the count is 0

6. **Given** multiple paths have been enumerated, **When** displaying the count to the user, **Then** the result is presented clearly as a single integer value

---

### User Story 6 - Display Enumerated Paths for Verification (Priority: P2)

An operations engineer needs to see the actual enumerated paths (not just the count) so they can manually verify that the pathfinding algorithm is working correctly and understand which device combinations create valid routes.

**Why this priority**: While the count is the required answer, showing the paths allows for verification and debugging. This is valuable for validation but not strictly required for the answer.

**Independent Test**: Can be tested by verifying that displayed paths are complete, valid, and match manual tracing through the device configuration.

**Acceptance Scenarios**:

1. **Given** all paths have been enumerated from "you" to "out", **When** displaying paths, **Then** each path is shown as a sequence of device names in order

2. **Given** the example configuration with 5 paths, **When** displaying paths, **Then** each path clearly shows:

   - you → bbb → ddd → ggg → out
   - you → bbb → eee → out
   - you → ccc → ddd → ggg → out
   - you → ccc → eee → out
   - you → ccc → fff → out

3. **Given** displayed paths, **When** manually tracing each path, **Then** every consecutive device pair exists as a valid connection in the device configuration

4. **Given** multiple paths with different lengths, **When** displaying, **Then** shorter paths (fewer hops) and longer paths (more hops) are all shown equally

5. **Given** paths displayed to the engineer, **When** reviewing them, **Then** no path appears more than once in the enumeration

---

### User Story 7 - Handle Device Network with No Solution (Priority: P2)

An operations engineer needs the system to gracefully handle configurations where no path exists from "you" to "out", providing clear feedback that the reactor has no valid communication route.

**Why this priority**: Edge case handling ensures robustness. If "you" and "out" are disconnected, the system should handle this gracefully rather than crashing or hanging.

**Independent Test**: Can be tested by providing a configuration where "you" and "out" are in separate, disconnected components of the graph.

**Acceptance Scenarios**:

1. **Given** a configuration where "you" exists but has no outputs, **When** enumerating paths, **Then** the system returns 0 paths (not an error)

2. **Given** a configuration where "you" outputs to device "a", but "a" has no path to "out", **When** enumerating paths, **Then** the system returns 0 paths

3. **Given** a configuration where "out" exists but is unreachable from "you", **When** enumerating paths, **Then** the system returns 0 paths with a clear message

4. **Given** a configuration with a dead-end device (device with no outputs other than "out"), **When** attempting to reach "out" from a different branch, **Then** the system correctly identifies paths that reach "out" and ignores dead-end branches

### Edge Cases

- What happens when the same device appears multiple times in different paths? (Should be counted as separate path occurrences)
- How does the system handle a device that connects to itself or creates cycles? (Should not occur in valid Advent of Code input, but system should not hang)
- What if "you" or "out" devices are not present in the configuration? (Should return 0 paths)
- What if a device is referenced but never defined as a source line? (Should still be included in the graph as a destination node)
- What if the device configuration is empty? (Should return 0 paths)
- What if there are duplicate lines in the configuration? (Should be handled gracefully - ideally deduplicated or merged)

## Requirements _(mandatory)_

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: System MUST parse device configuration from input where each line is formatted as `device_name: output1 output2 ...` with space-separated outputs
- **FR-002**: System MUST correctly handle devices with single outputs (e.g., `iii: out`)
- **FR-003**: System MUST correctly handle devices with multiple outputs (e.g., `ccc: ddd eee fff`)
- **FR-004**: System MUST build a complete directed graph representing all device connections from the parsed configuration
- **FR-005**: System MUST identify all unique devices in the network, including those that only appear as destinations
- **FR-006**: System MUST implement a pathfinding algorithm (e.g., depth-first search with backtracking) to enumerate all paths from source to target
- **FR-007**: System MUST find all distinct paths from "you" device to "out" device following valid device connections
- **FR-008**: System MUST count the total number of distinct paths from "you" to "out"
- **FR-009**: System MUST return path count of 0 when no valid path exists from "you" to "out"
- **FR-010**: System MUST NOT count the same path twice (paths must be unique)
- **FR-011**: System MUST handle configurations with multiple branching points and reconvergence points correctly
- **FR-012**: System MUST optionally display all enumerated paths for verification purposes
- **FR-013**: System MUST handle invalid or malformed input gracefully without crashing

### Key Entities _(include if feature involves data)_

- **Device**: A node in the reactor network with a unique name (string identifier). A device has:

  - **name**: The device's unique identifier (e.g., "you", "out", "bbb")
  - **outputs**: List of devices this device connects to (outgoing edges)

- **DeviceNetwork**: A directed graph representing all device connections. It contains:

  - **devices**: Collection of all Device nodes indexed by name
  - **connections**: Mapping of source device to list of destination devices
  - **source**: The starting device "you"
  - **target**: The destination device "out"

- **Path**: A sequence of device names representing one route from "you" to "out". Example: `["you", "bbb", "ddd", "ggg", "out"]`

- **PathEnumeration**: The result of finding all paths, containing:
  - **paths**: List of all distinct Path objects found
  - **count**: Total number of distinct paths (length of paths list)

## Success Criteria _(mandatory)_

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: System correctly parses the example device configuration without errors and accurately identifies all 10 devices
- **SC-002**: System correctly enumerates exactly 5 paths from "you" to "out" in the example configuration
- **SC-003**: Each enumerated path starts with device "you" and ends with device "out"
- **SC-004**: Each enumerated path contains only valid consecutive device connections that exist in the device configuration
- **SC-005**: All enumerated paths are unique with no duplicates in the enumeration
- **SC-006**: System returns path count of 0 for configurations where "you" and "out" are disconnected
- **SC-007**: System completes path enumeration for the example configuration in under 1 second
- **SC-008**: System can handle device configurations with up to 100 devices without hanging or crashing
- **SC-009**: When multiple valid paths of different lengths exist (e.g., 3-hop vs 5-hop paths), all are correctly included in the enumeration
- **SC-010**: The final answer (path count) correctly solves the Advent of Code Day 11 Part 1 puzzle for provided test inputs

## Assumptions

- Device names are valid non-empty strings containing alphanumeric characters and underscores
- The device network forms a directed acyclic graph (DAG) with no cycles
- Both "you" and "out" devices exist in valid test cases for Part 1
- A path cannot visit the same device twice (no cycles to break)
- Output format for individual paths should be a simple sequence like: `you → bbb → ddd → ggg → out`
- The system will be called once per puzzle input and should return deterministic results
