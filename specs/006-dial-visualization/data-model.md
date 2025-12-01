# Data Model: Day 1 Dial Visualization

**Feature**: 006-dial-visualization  
**Date**: 2025-12-01  
**Status**: Complete

## Overview

This document defines the data structures and entities used in the Day 1 Dial Visualization application. All structures are defined in JavaScript (ES6+) using JSDoc notation for type clarity.

---

## Core Entities

### 1. Rotation

Represents a single rotation instruction from the puzzle input.

**Structure**:

```javascript
/**
 * @typedef {Object} Rotation
 * @property {'L'|'R'} direction - Left (counterclockwise) or Right (clockwise)
 * @property {number} distance - Number of clicks to rotate (non-negative integer)
 */
```

**Alternative Representation** (tuple):

```javascript
/**
 * @typedef {['L'|'R', number]} RotationTuple
 * [direction, distance]
 */
```

**Examples**:

```javascript
{direction: 'L', distance: 68}
{direction: 'R', distance: 48}
['L', 68]  // Tuple format
['R', 48]  // Tuple format
```

**Validation Rules**:

- `direction` MUST be exactly 'L' or 'R' (case-sensitive)
- `distance` MUST be >= 0
- `distance` MUST be an integer

**Relationships**:

- Many Rotations form a RotationSequence
- Each Rotation is processed to update DialState

---

### 2. DialState

Represents the current state of the safe dial at any point in time.

**Structure**:

```javascript
/**
 * @typedef {Object} DialState
 * @property {number} position - Current dial position (0-99)
 * @property {number} zeroCount - Number of times dial has pointed at 0
 * @property {number} rotationIndex - Index of current rotation being executed
 * @property {boolean} isAnimating - Whether animation is currently playing
 */
```

**Examples**:

```javascript
// Initial state
{
    position: 50,
    zeroCount: 0,
    rotationIndex: 0,
    isAnimating: false
}

// Mid-animation state
{
    position: 23,
    zeroCount: 2,
    rotationIndex: 5,
    isAnimating: true
}
```

**State Transitions**:

```
IDLE (position=50, count=0)
  → ANIMATING (position changing, count incrementing)
  → PAUSED (position frozen, count static)
  → ANIMATING (resume)
  → COMPLETE (final position, final count)
  → RESET (back to IDLE)
```

**Invariants**:

- `position` MUST always be in range [0, 99]
- `zeroCount` MUST always be >= 0
- `rotationIndex` MUST be in range [0, rotations.length]
- If `isAnimating` is true, rendering loop must be active

---

### 3. AnimationConfig

Stores user-configurable animation settings.

**Structure**:

```javascript
/**
 * @typedef {Object} AnimationConfig
 * @property {number} speed - Animation speed multiplier (0.1 to 10.0)
 * @property {'part1'|'part2'} mode - Counting mode
 * @property {boolean} audioEnabled - Whether click sounds are enabled
 * @property {number} degreesPerSecond - Base rotation speed (affected by speed multiplier)
 */
```

**Examples**:

```javascript
// Default configuration
{
    speed: 1.0,
    mode: 'part1',
    audioEnabled: true,
    degreesPerSecond: 360  // One full rotation per second at 1x speed
}

// Fast playback
{
    speed: 5.0,
    mode: 'part2',
    audioEnabled: false,  // Disabled at high speed to avoid audio spam
    degreesPerSecond: 360
}
```

**Validation Rules**:

- `speed` MUST be in range [0.1, 10.0]
- `mode` MUST be exactly 'part1' or 'part2'
- `audioEnabled` MUST be boolean
- `degreesPerSecond` MUST be > 0

**Mode Behaviors**:
| Mode | Count Behavior |
|------|----------------|
| `part1` | Increment counter only when rotation **ends** at position 0 |
| `part2` | Increment counter for every **crossing** of position 0 during rotation |

---

### 4. UIState

Tracks the current state of the user interface.

**Structure**:

```javascript
/**
 * @typedef {Object} UIState
 * @property {'idle'|'playing'|'paused'|'complete'} playbackState
 * @property {boolean} fileLoaded - Whether input file has been loaded
 * @property {string|null} fileName - Name of loaded file (null if none)
 * @property {string|null} errorMessage - Current error message (null if none)
 * @property {boolean} audioSupported - Whether Web Audio API is available
 */
```

**State Machine**:

```
              ┌─────────┐
              │  IDLE   │ (initial state, no data loaded)
              └────┬────┘
                   │ loadFile()
                   ▼
              ┌─────────┐
         ┌───▶│  IDLE   │ (data loaded, ready to play)
         │    └────┬────┘
         │         │ playFromStart()
         │         ▼
         │    ┌─────────┐
         │    │ PLAYING │◄─┐ resume()
         │    └────┬────┘  │
         │         │        │
         │         │ pause()│
         │         ▼        │
         │    ┌─────────┐  │
         │    │ PAUSED  │──┘
         │    └────┬────┘
         │         │
         │         │ playFromStart()
         │         ▼
         │    ┌─────────┐
         └────│COMPLETE │
              └─────────┘
                   │
                   │ playFromStart()
                   └─► (back to PLAYING)
```

**Examples**:

```javascript
// Initial state (page load)
{
    playbackState: 'idle',
    fileLoaded: false,
    fileName: null,
    errorMessage: null,
    audioSupported: true
}

// After file loaded
{
    playbackState: 'idle',
    fileLoaded: true,
    fileName: 'input.txt',
    errorMessage: null,
    audioSupported: true
}

// Error state
{
    playbackState: 'idle',
    fileLoaded: false,
    fileName: null,
    errorMessage: 'Invalid file format: Expected L/R followed by number',
    audioSupported: true
}
```

---

### 5. RotationSequence

Collection of all rotation instructions for the current puzzle input.

**Structure**:

```javascript
/**
 * @typedef {Object} RotationSequence
 * @property {Rotation[]} rotations - Array of rotation instructions
 * @property {number} totalRotations - Total number of rotations
 * @property {number} totalDistance - Sum of all distances (for statistics)
 */
```

**Examples**:

```javascript
{
    rotations: [
        {direction: 'L', distance: 68},
        {direction: 'L', distance: 30},
        {direction: 'R', distance: 48}
    ],
    totalRotations: 3,
    totalDistance: 146
}
```

**Derived Properties**:

```javascript
// Can be computed from rotations array
const totalDistance = rotations.reduce((sum, r) => sum + r.distance, 0);
const totalRotations = rotations.length;
const maxDistance = Math.max(...rotations.map((r) => r.distance));
```

---

### 6. CanvasContext

Wraps HTML5 Canvas rendering context with visualization-specific properties.

**Structure**:

```javascript
/**
 * @typedef {Object} CanvasContext
 * @property {HTMLCanvasElement} canvas - The canvas DOM element
 * @property {CanvasRenderingContext2D} ctx - 2D rendering context
 * @property {number} width - Canvas width in pixels
 * @property {number} height - Canvas height in pixels
 * @property {number} centerX - X coordinate of center point
 * @property {number} centerY - Y coordinate of center point
 * @property {number} dialRadius - Radius of the dial circle in pixels
 */
```

**Examples**:

```javascript
{
    canvas: <canvas#dialCanvas>,
    ctx: CanvasRenderingContext2D,
    width: 800,
    height: 800,
    centerX: 400,
    centerY: 400,
    dialRadius: 300
}
```

**Geometry Calculations**:

```javascript
// Segment angle (100 segments in 360°)
const segmentAngle = 360 / 100; // 3.6° per segment

// Position to angle conversion (position 0 = top = -90°, clockwise)
function positionToAngle(position) {
  return (position * segmentAngle - 90) % 360;
}

// Angle to canvas coordinates
function angleToCoords(angleDegrees, radius) {
  const angleRadians = (angleDegrees * Math.PI) / 180;
  return {
    x: centerX + radius * Math.cos(angleRadians),
    y: centerY + radius * Math.sin(angleRadians),
  };
}
```

---

### 7. AudioManager

Manages Web Audio API resources and click sound generation.

**Structure**:

```javascript
/**
 * @typedef {Object} AudioManager
 * @property {AudioContext|null} context - Web Audio API context
 * @property {boolean} isSupported - Whether Web Audio API is available
 * @property {boolean} isMuted - User mute preference
 * @property {number} clickFrequency - Frequency of click sound in Hz
 * @property {number} clickDuration - Duration of click sound in seconds
 */
```

**Examples**:

```javascript
{
    context: AudioContext,
    isSupported: true,
    isMuted: false,
    clickFrequency: 800,  // Hz
    clickDuration: 0.05   // 50ms
}

// Unsupported browser
{
    context: null,
    isSupported: false,
    isMuted: true,
    clickFrequency: 800,
    clickDuration: 0.05
}
```

---

## Data Flow

### Input → State → Rendering

```
┌─────────────┐
│ Input File  │
│ (text)      │
└──────┬──────┘
       │
       │ parseInput()
       ▼
┌─────────────────┐
│RotationSequence │
│                 │
│ [Rotation[]]    │
└────────┬────────┘
         │
         │ Animation Loop
         ▼
┌─────────────────┐      ┌─────────────┐
│   DialState     │─────▶│  Rendering  │
│                 │      │  (Canvas)   │
│ position: 42    │      └─────────────┘
│ zeroCount: 3    │             │
│ rotationIndex: 5│             │
└─────────────────┘             │
         │                      │
         │ Zero crossing?       │
         ▼                      ▼
┌─────────────────┐      ┌─────────────┐
│  AudioManager   │      │  UI Update  │
│                 │      │             │
│  playClick()    │      │ Counter: 3  │
└─────────────────┘      └─────────────┘
```

---

## Validation & Constraints

### Input Validation

**Rotation parsing**:

```javascript
function validateRotation(line) {
  const match = line.match(/^([LR])(\d+)$/);
  if (!match) {
    throw new Error(
      `Invalid rotation format: "${line}". Expected L/R followed by number.`
    );
  }
  const direction = match[1];
  const distance = parseInt(match[2], 10);
  if (distance < 0) {
    throw new Error(`Distance must be non-negative: ${distance}`);
  }
  return { direction, distance };
}
```

**Position validation**:

```javascript
function validatePosition(position) {
  if (!Number.isInteger(position) || position < 0 || position > 99) {
    throw new Error(
      `Position must be integer in range [0, 99], got: ${position}`
    );
  }
}
```

**Speed validation**:

```javascript
function validateSpeed(speed) {
  if (typeof speed !== "number" || speed < 0.1 || speed > 10.0) {
    throw new Error(`Speed must be in range [0.1, 10.0], got: ${speed}`);
  }
}
```

---

## Type Definitions (Complete Reference)

```javascript
/**
 * Complete type definitions for Day 1 Dial Visualization
 */

/** @typedef {'L'|'R'} Direction */
/** @typedef {number} Distance */
/** @typedef {number} Position */ // 0-99
/** @typedef {'part1'|'part2'} Mode */
/** @typedef {'idle'|'playing'|'paused'|'complete'} PlaybackState */

/** @typedef {Object} Rotation
 * @property {Direction} direction
 * @property {Distance} distance
 */

/** @typedef {Object} DialState
 * @property {Position} position
 * @property {number} zeroCount
 * @property {number} rotationIndex
 * @property {boolean} isAnimating
 */

/** @typedef {Object} AnimationConfig
 * @property {number} speed
 * @property {Mode} mode
 * @property {boolean} audioEnabled
 * @property {number} degreesPerSecond
 */

/** @typedef {Object} UIState
 * @property {PlaybackState} playbackState
 * @property {boolean} fileLoaded
 * @property {string|null} fileName
 * @property {string|null} errorMessage
 * @property {boolean} audioSupported
 */

/** @typedef {Object} RotationSequence
 * @property {Rotation[]} rotations
 * @property {number} totalRotations
 * @property {number} totalDistance
 */

/** @typedef {Object} CanvasContext
 * @property {HTMLCanvasElement} canvas
 * @property {CanvasRenderingContext2D} ctx
 * @property {number} width
 * @property {number} height
 * @property {number} centerX
 * @property {number} centerY
 * @property {number} dialRadius
 */

/** @typedef {Object} AudioManager
 * @property {AudioContext|null} context
 * @property {boolean} isSupported
 * @property {boolean} isMuted
 * @property {number} clickFrequency
 * @property {number} clickDuration
 */
```

---

## Summary

**Data Model Status**: ✅ COMPLETE

All entities defined with:

- Clear structure and properties
- Validation rules
- State transitions
- Examples
- Type definitions

**Key Entities**:

1. **Rotation** - Single instruction (L/R + distance)
2. **DialState** - Current position and counter
3. **AnimationConfig** - User settings
4. **UIState** - Interface state machine
5. **RotationSequence** - Full input data
6. **CanvasContext** - Rendering context
7. **AudioManager** - Sound system

**Ready for**: API contract definition and implementation
