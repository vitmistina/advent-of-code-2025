# Research: Day 1 Dial Visualization

**Feature**: 006-dial-visualization  
**Date**: 2025-12-01  
**Status**: Complete

## Overview

This document captures all research findings and technology decisions made during Phase 0 of the planning process for the Day 1 Dial Visualization feature.

## Research Questions & Answers

### 1. Canvas Rendering Performance

**Question**: What's the best approach to render 100 dial segments with smooth 60 FPS animation?

**Research Findings**:

- **HTML5 Canvas**: Industry standard for 2D graphics, direct pixel manipulation
- **requestAnimationFrame**: Browser-optimized animation loop (60 FPS on most devices)
- **Performance**: Can easily handle 100 static arcs + 1 rotating pointer at 60 FPS
- **Optimization**: Pre-calculate arc positions, only redraw on frame update

**Decision**: Use HTML5 Canvas with requestAnimationFrame

**Rationale**: Canvas provides direct pixel control needed for smooth animation. requestAnimationFrame synchronizes with browser refresh rate ensuring optimal frame pacing. For 100 segments, performance overhead is negligible.

**Alternatives Considered**:
| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| SVG | Declarative, scalable | Too slow for dynamic updates | ❌ Rejected |
| WebGL | Maximum performance | Overkill for 2D circles | ❌ Rejected |
| CSS animations | Simple syntax | Insufficient control over rotation logic | ❌ Rejected |
| HTML5 Canvas | Direct control, fast | Manual drawing required | ✅ **Selected** |

---

### 2. Audio Click Implementation

**Question**: How to generate/play click sounds with <50ms latency for zero crossings?

**Research Findings**:

- **Web Audio API**: Provides low-latency audio playback (<20ms typical)
- **AudioBuffer**: Pre-loaded audio eliminates file I/O during animation
- **Sound Generation**:
  - **Option A**: Programmatic (oscillator with gain envelope for "click" sound)
  - **Option B**: Pre-recorded .wav file (requires HTTP server or base64 embed)

**Decision**: Use Web Audio API with programmatic click sound generation

**Rationale**:

- Web Audio API achieves <50ms latency requirement
- Programmatic sound generation eliminates external dependencies
- AudioContext provides precise timing control for synchronization

**Implementation Approach**:

```javascript
// Generate click sound: short sine wave burst with exponential decay
function createClickSound(audioContext) {
  const oscillator = audioContext.createOscillator();
  const gainNode = audioContext.createGain();

  oscillator.frequency.value = 800; // 800 Hz click
  gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
  gainNode.gain.exponentialRampToValueAtTime(
    0.01,
    audioContext.currentTime + 0.05
  );

  oscillator.connect(gainNode);
  gainNode.connect(audioContext.destination);

  oscillator.start();
  oscillator.stop(audioContext.currentTime + 0.05);
}
```

**Alternatives Considered**:
| Option | Latency | Dependencies | Verdict |
|--------|---------|--------------|---------|
| `<audio>` element | 100-300ms | None | ❌ Too slow |
| Web Audio API | <20ms | None | ✅ **Selected** |
| External .mp3 | Variable | HTTP server | ❌ Adds complexity |

---

### 3. Animation Speed Control

**Question**: How to implement variable speed without breaking visual smoothness or audio sync?

**Research Findings**:

- **Time-based animation**: Track elapsed time, not frame count
- **Delta time**: Calculate time since last frame, multiply by speed factor
- **Audio synchronization**: Queue audio events based on simulation time, not wall-clock time

**Decision**: Implement time-based animation with deltaTime and speed multiplier

**Rationale**:

- Maintains smooth visuals independent of frame rate variations
- Speed changes don't cause visual jitter or audio desync
- Industry-standard approach (used in game engines)

**Implementation Approach**:

```javascript
let lastFrameTime = performance.now();
let speed = 1.0; // User-adjustable multiplier (0.1 to 10)

function animationLoop(currentTime) {
  const deltaTime = (currentTime - lastFrameTime) / 1000; // Convert to seconds
  const adjustedDelta = deltaTime * speed; // Apply speed multiplier

  updateAnimation(adjustedDelta); // Progress animation by adjusted time
  render(); // Draw current state

  lastFrameTime = currentTime;
  requestAnimationFrame(animationLoop);
}
```

**Alternatives Considered**:
| Option | Smoothness | Control | Verdict |
|--------|------------|---------|---------|
| Frame-based (fixed steps) | Inconsistent across devices | Simple | ❌ Rejected |
| Time-based with deltaTime | Smooth on all devices | Moderate complexity | ✅ **Selected** |
| CSS transition-duration | Limited | Very simple | ❌ Insufficient control |

---

### 4. Input File Loading

**Question**: How to load day-01/input.txt from browser without server?

**Research Findings**:

- **Browser Security**: Cannot directly read files from file system
- **FileReader API**: Allows user-selected file upload
- **Local Server**: Simple HTTP server enables fetch() API
- **Embedded Data**: Can include test input as JavaScript constant

**Decision**: Implement multiple options for maximum flexibility:

1. **FileReader API** with file input dialog (works standalone)
2. **Embedded test input** as JavaScript constant (demo/testing)
3. **Optional**: Fetch API if served via local server

**Rationale**:

- FileReader provides standalone functionality (no server required)
- Embedded test input enables immediate testing
- Fetch API adds convenience when developing with local server

**Implementation Approach**:

```javascript
// Option 1: File upload
document.getElementById("fileInput").addEventListener("change", (event) => {
  const file = event.target.files[0];
  const reader = new FileReader();
  reader.onload = (e) => {
    const inputText = e.target.result;
    loadRotations(parseInput(inputText));
  };
  reader.readAsText(file);
});

// Option 2: Embedded test input
const TEST_INPUT = `L68
L30
R48
L5
R60
L55
L1
L99
R14
L82`;

// Option 3: Fetch (if served via HTTP)
async function loadFromFile(filepath) {
  const response = await fetch(filepath);
  const text = await response.text();
  return parseInput(text);
}
```

**Alternatives Considered**:
| Option | Standalone | UX | Verdict |
|--------|------------|-----|---------|
| File upload only | ✅ Yes | Requires user action | ✅ **Included** |
| Embedded only | ✅ Yes | Limited to test data | ✅ **Included** |
| Fetch only | ❌ Needs server | Seamless | ✅ **Optional** |
| Electron/Node.js | ✅ Yes | Heavy dependency | ❌ Rejected |

---

### 5. Part 1 vs Part 2 Counting Logic

**Question**: How to accurately count zero crossings during rotation (Part 2)?

**Research Findings**:

- **Part 1**: Count only when rotation **ends** at position 0
- **Part 2**: Count **every time** dial crosses 0 during rotation
- **Existing Algorithm**: Python solution in day-01/solution.py already implements correct logic

**Decision**: Port `count_zero_crossings_during_rotation()` from Python to JavaScript

**Python Algorithm (to port)**:

```python
def count_zero_crossings_during_rotation(start_position: int, direction: str, distance: int) -> int:
    if distance == 0:
        return 0

    start_position = start_position % 100

    if direction == "R":
        # Right rotation: (start + distance) // 100
        return (start_position + distance) // 100
    else:  # 'L'
        if start_position == 0:
            return distance // 100
        if distance < start_position:
            return 0
        remaining_after_first = distance - start_position
        additional_crossings = remaining_after_first // 100
        return 1 + additional_crossings
```

**JavaScript Port**:

```javascript
function countZeroCrossingsDuringRotation(startPosition, direction, distance) {
  if (distance === 0) return 0;

  startPosition = startPosition % 100;

  if (direction === "R") {
    return Math.floor((startPosition + distance) / 100);
  } else {
    // 'L'
    if (startPosition === 0) {
      return Math.floor(distance / 100);
    }
    if (distance < startPosition) {
      return 0;
    }
    const remainingAfterFirst = distance - startPosition;
    const additionalCrossings = Math.floor(remainingAfterFirst / 100);
    return 1 + additionalCrossings;
  }
}
```

**Rationale**:

- Algorithm is already proven correct (passes all tests)
- Direct port minimizes introduction of bugs
- Mathematical approach is more efficient than simulating every click

**Alternatives Considered**:
| Option | Accuracy | Performance | Verdict |
|--------|----------|-------------|---------|
| Simulate every click | 100% | O(distance) - too slow for large rotations | ❌ Rejected |
| Mathematical formula | 100% | O(1) - instant | ✅ **Selected** |
| Approximate/estimate | Variable | O(1) | ❌ Incorrect results |

---

### 6. Segment Numbering Display

**Question**: Should all 100 numbers be visible, or only key positions?

**Research Findings**:

- **Visual Clutter**: Displaying all 100 numbers at same size is hard to read
- **Context vs Clarity**: Need balance between showing position and avoiding overwhelm
- **UI Design Patterns**: Common pattern is to emphasize multiples (0, 10, 20, etc.)

**Decision**: Implement tiered labeling system:

1. **Major ticks** (0, 10, 20, ..., 90): Large font, bold
2. **Minor ticks** (all others): Small font or tick marks only
3. **Current position**: Highlighted with color/size change

**Visual Design**:

```
     90
 80      0/100

70           10

60           20

 50      30
     40

Major numbers: 16px bold
Minor numbers: 10px regular
Current position: 20px bold + color highlight
```

**Rationale**:

- Provides full context without overwhelming user
- Major ticks (every 10) easy to read for orientation
- Current position emphasis shows exactly where dial points

**Alternatives Considered**:
| Option | Readability | Context | Verdict |
|--------|-------------|---------|---------|
| All 100 numbers same size | Poor | Full | ❌ Too cluttered |
| Only current position | Excellent | Minimal | ❌ Loses context |
| Every 10th number only | Good | Moderate | ❌ Missing detail |
| Tiered labeling | Excellent | Full | ✅ **Selected** |

---

## Technology Stack Summary

### Selected Technologies

| Component          | Technology            | Version          | Justification                               |
| ------------------ | --------------------- | ---------------- | ------------------------------------------- |
| **Rendering**      | HTML5 Canvas          | Current standard | 60 FPS capability, direct pixel control     |
| **Animation**      | requestAnimationFrame | Browser API      | Optimized timing, smooth frame delivery     |
| **Audio**          | Web Audio API         | Current standard | <20ms latency, programmatic control         |
| **Language**       | JavaScript            | ES6+             | Universal browser support, no transpilation |
| **Styling**        | CSS3                  | Current standard | Modern layout, responsive design            |
| **Module System**  | ES6 Modules or inline | Browser-native   | No build step required                      |
| **Input Handling** | FileReader API        | Current standard | Standalone file upload capability           |

### No Dependencies Required

**Zero external libraries** - entire implementation uses browser-native APIs:

- ✅ No npm packages
- ✅ No CDN links
- ✅ No build tools
- ✅ No transpilation
- ✅ Works offline

**Rationale**: Keeps project simple, fast-loading, and free of dependency management overhead.

---

## Performance Analysis

### Expected Performance Characteristics

| Metric          | Target | Expected | Notes                              |
| --------------- | ------ | -------- | ---------------------------------- |
| Frame rate      | 60 FPS | 60 FPS   | Canvas easily handles 100 segments |
| Audio latency   | <50ms  | <20ms    | Web Audio API specification        |
| Load time       | <2s    | <500ms   | No external resources              |
| Max rotations   | 10,000 | 50,000+  | O(1) mathematical algorithm        |
| Memory usage    | <100MB | <50MB    | Canvas buffer + audio context      |
| Browser support | 90%+   | 95%+     | Modern browsers only               |

### Browser Compatibility

| Browser | Version | Canvas | Web Audio | FileReader | Verdict          |
| ------- | ------- | ------ | --------- | ---------- | ---------------- |
| Chrome  | 90+     | ✅     | ✅        | ✅         | ✅ Supported     |
| Firefox | 88+     | ✅     | ✅        | ✅         | ✅ Supported     |
| Safari  | 14+     | ✅     | ✅        | ✅         | ✅ Supported     |
| Edge    | 90+     | ✅     | ✅        | ✅         | ✅ Supported     |
| IE 11   | -       | ⚠️     | ❌        | ⚠️         | ❌ Not supported |

**Note**: Internet Explorer 11 is explicitly not supported (no Web Audio API). Graceful degradation message will be shown.

---

## Best Practices to Follow

### Code Organization

- Separate concerns: rendering, animation, audio, UI controls
- Modular functions (single responsibility)
- Clear naming conventions
- Comments for complex logic (especially ported algorithms)

### Performance

- Minimize canvas redraws (only on animation frame)
- Pre-calculate static values (segment positions)
- Use efficient data structures (arrays, not objects for hot paths)
- Avoid memory allocation in animation loop

### User Experience

- Show loading states
- Provide visual feedback (hover effects, button states)
- Graceful error handling (missing audio support, invalid files)
- Responsive design (canvas scales with window)
- Accessibility considerations (keyboard controls if time permits)

### Testing

- Manual testing with known inputs
- Test across browsers (Chrome, Firefox, Safari minimum)
- Test edge cases (empty input, very large rotations)
- Validate Part 1 and Part 2 logic against Python solution

---

## Risk Mitigation

### Identified Risks

| Risk                       | Probability | Impact | Mitigation Strategy                                |
| -------------------------- | ----------- | ------ | -------------------------------------------------- |
| Audio not supported        | Low         | Medium | Gracefully degrade, show visual-only mode          |
| Canvas performance issues  | Very Low    | High   | Pre-testing shows no issues expected               |
| File parsing errors        | Medium      | Low    | Robust error handling, validation                  |
| Browser incompatibility    | Low         | Medium | Test on major browsers, show compatibility warning |
| Speed control audio desync | Medium      | Medium | Careful event timing based on simulation time      |

### Fallback Strategies

1. **No Web Audio API**: Show warning, disable audio, continue with visual-only
2. **Old browser**: Show "Please upgrade" message with supported browser list
3. **Invalid input file**: Show error, fallback to embedded test input
4. **Performance issues**: Add "Reduce quality" option (fewer segments, simplified rendering)

---

## Open Questions (Resolved)

All research questions have been answered and decisions made. No blockers remain.

---

## Conclusion

**Research Status**: ✅ COMPLETE

All technical unknowns have been resolved. Technology stack selected, algorithms identified, and implementation approach defined. Ready to proceed to Phase 1 (Design & Contracts).

**Key Takeaways**:

1. Canvas + requestAnimationFrame provides required 60 FPS performance
2. Web Audio API meets <50ms latency requirement
3. Existing Python algorithm can be directly ported to JavaScript
4. Zero external dependencies keeps project simple and fast
5. Multiple input options (upload, embedded, fetch) maximize flexibility

**Next Phase**: Create data model, API contracts, and quickstart documentation.
