# Quickstart Guide: Day 1 Dial Visualization

**Feature**: 006-dial-visualization  
**Date**: 2025-12-01  
**For**: Developers implementing or using the dial visualization

## Overview

This guide helps you get started with the Day 1 Dial Visualization feature, whether you're implementing it, testing it, or just using it to understand the puzzle.

---

## For Users

### Running the Visualization

1. **Start a local web server** (required if not using embedded mode):

   ```powershell
   cd day-01/visualization
   python -m http.server 8000
   # Or with UV:
   uv run -m http.server 8000
   ```

2. **Open in browser**:

   ```powershell
   start http://localhost:8000
   ```

   Or manually navigate to: `http://localhost:8000/index.html`

3. **Load puzzle input**:

   - Click "Choose File" button
   - Select `../input.txt` (actual puzzle input) or `../test_input.txt` (sample)
   - Or use embedded test input (pre-loaded)

4. **Select mode**:

   - **Part 1**: Counts only when dial lands on 0 after rotation
   - **Part 2**: Counts every time dial crosses 0 during rotation

5. **Start animation**:

   - Click "Play from Start" button
   - Watch the dial rotate and counter increment

6. **Adjust speed** (optional):

   - Use slider or enter value in speed input field
   - Range: 0.1x (slow motion) to 10x (fast forward)

7. **Controls**:
   - **Play from Start**: Reset and restart animation
   - **Pause/Resume**: Pause or continue current animation
   - **Speed**: Adjust playback speed on the fly

### Expected Results

**With test_input.txt** (sample from puzzle):

- **Part 1**: Counter should reach **3**
- **Part 2**: Counter should reach **6**

**With input.txt** (actual puzzle):

- **Part 1**: Counter should match your submitted answer
- **Part 2**: Counter should match your submitted answer

---

## For Developers

### Project Setup

1. **Navigate to feature branch**:

   ```powershell
   git checkout 006-dial-visualization
   ```

2. **Create directory structure**:

   ```powershell
   mkdir -p day-01/visualization
   cd day-01/visualization
   ```

3. **Create initial files**:

   ```powershell
   # Create main HTML file
   New-Item -Path "index.html" -ItemType File

   # Create JavaScript modules
   New-Item -Path "dial-animation.js" -ItemType File
   New-Item -Path "audio-manager.js" -ItemType File
   New-Item -Path "ui-controls.js" -ItemType File

   # Create stylesheet (optional)
   New-Item -Path "styles.css" -ItemType File

   # Create README
   New-Item -Path "README.md" -ItemType File
   ```

### Development Workflow

**Recommended Order**:

1. **Phase 1: Static Rendering**

   ```javascript
   // Step 1.1: Set up HTML structure
   // - Canvas element
   // - Control buttons
   // - Input fields

   // Step 1.2: Implement drawDial()
   // - Draw circle
   // - Draw 100 segment ticks
   // - Draw numbers
   // Test: Verify static dial renders correctly

   // Step 1.3: Implement drawPointer()
   // - Draw line from center to edge
   // Test: Manually set position, verify pointer draws at correct angle
   ```

2. **Phase 2: Input Parsing**

   ```javascript
   // Step 2.1: Implement parseInput()
   // - Parse rotation format
   // - Validate input
   // Test: Parse test_input.txt, verify array output

   // Step 2.2: Implement applyRotation()
   // - Port from Python solution
   // Test: Verify modulo math works correctly
   ```

3. **Phase 3: Basic Animation**

   ```javascript
   // Step 3.1: Set up animation loop
   // - requestAnimationFrame
   // - Time-based updates

   // Step 3.2: Animate single rotation
   // - Smooth pointer movement
   // Test: Apply one rotation, verify smooth animation

   // Step 3.3: Animate full sequence
   // - Iterate through all rotations
   // Test: Load test input, verify all rotations execute
   ```

4. **Phase 4: Counter Display**

   ```javascript
   // Step 4.1: Implement drawCounter()
   // - Display count on canvas

   // Step 4.2: Implement Part 1 logic
   // - Increment on zero landing
   // Test: Verify counter=3 for test_input.txt Part 1
   ```

5. **Phase 5: Audio Feedback**

   ```javascript
   // Step 5.1: Implement initAudio()
   // - Create AudioContext
   // - Check browser support

   // Step 5.2: Implement playClickSound()
   // - Generate click sound with oscillator
   // Test: Verify click plays on zero events
   ```

6. **Phase 6: Speed Controls**

   ```javascript
   // Step 6.1: Implement handleSpeedChange()
   // - Update animation config
   // - Apply to deltaTime calculation
   // Test: Verify animation speeds up/slows down

   // Step 6.2: Sync slider and input field
   // Test: Change slider updates field, change field updates slider
   ```

7. **Phase 7: Part 2 Support**

   ```javascript
   // Step 7.1: Port countZeroCrossingsDuringRotation()
   // - Implement mathematical formula
   // Test: Verify with known examples

   // Step 7.2: Update animation logic for Part 2
   // - Count during rotation, not just at end
   // Test: Verify counter=6 for test_input.txt Part 2
   ```

8. **Phase 8: Polish**

   ```javascript
   // Step 8.1: Improve visual styling
   // - Colors, fonts, layout
   // - Responsive canvas

   // Step 8.2: Add error handling
   // - Invalid files
   // - Unsupported browser

   // Step 8.3: Add loading states
   // - Show "Loading..." during file read
   // - Disable controls when appropriate
   ```

### Testing Checklist

**Manual Testing Steps**:

- [ ] Static dial renders with 100 segments
- [ ] Numbers are visible and correctly positioned
- [ ] Pointer draws at correct angle for known positions
- [ ] Test input parses without errors
- [ ] Single rotation animates smoothly
- [ ] Full sequence completes without crashes
- [ ] Counter increments at correct times (Part 1)
- [ ] Counter displays final value correctly
- [ ] Click sound plays on zero events
- [ ] Speed slider changes animation speed
- [ ] Speed input field validates correctly
- [ ] Play from Start resets dial and counter
- [ ] Pause/Resume works mid-animation
- [ ] Part 2 mode counts correctly (counter=6 for test)
- [ ] Actual input completes successfully
- [ ] Works in Chrome, Firefox, Safari, Edge
- [ ] Graceful degradation if audio not supported
- [ ] Error messages display for invalid files

### Code Style Guidelines

**JavaScript**:

```javascript
// Use ES6+ features
const rotations = parseInput(inputText);
const { position, zeroCount } = dialState;

// Descriptive function names
function calculateAngleFromPosition(position) {
  return (position * 3.6 - 90) % 360;
}

// JSDoc comments for public functions
/**
 * Apply rotation to dial position.
 * @param {number} position - Current position (0-99)
 * @param {string} direction - 'L' or 'R'
 * @param {number} distance - Clicks to rotate
 * @returns {number} New position
 */
function applyRotation(position, direction, distance) {
  // Implementation
}

// Constants in UPPER_CASE
const SEGMENT_COUNT = 100;
const DEFAULT_SPEED = 1.0;
const MIN_SPEED = 0.1;
const MAX_SPEED = 10.0;
```

**HTML**:

```html
<!-- Semantic structure -->
<main id="visualization">
  <canvas id="dialCanvas" width="800" height="800"></canvas>
  <section id="controls">
    <button id="playBtn">Play from Start</button>
    <input
      type="range"
      id="speedSlider"
      min="0.1"
      max="10"
      step="0.1"
      value="1"
    />
  </section>
</main>
```

**CSS**:

```css
/* Use CSS variables for theming */
:root {
  --bg-color: #1a1a1a;
  --dial-color: #ffffff;
  --pointer-color: #ff4444;
  --zero-color: #44ff44;
}

/* Responsive canvas */
#dialCanvas {
  max-width: 100%;
  height: auto;
}
```

### Debugging Tips

**Common Issues**:

| Issue                      | Likely Cause                   | Solution                                   |
| -------------------------- | ------------------------------ | ------------------------------------------ |
| Canvas is blank            | Forgot to call render function | Check drawDial() is called                 |
| Pointer at wrong position  | Angle calculation off          | Verify: `(position * 3.6 - 90) % 360`      |
| Counter doesn't increment  | Zero check logic wrong         | Log position after each rotation           |
| Animation jerky            | Not using deltaTime            | Use time-based animation, not frame-based  |
| Audio not playing          | AudioContext not initialized   | Check browser console for errors           |
| File upload fails          | CORS policy                    | Use local web server, not file:// protocol |
| Speed control doesn't work | Not applying to deltaTime      | Multiply: `deltaTime * speed`              |

**Debug Logging**:

```javascript
// Add logging for key events
function applyRotation(position, direction, distance) {
  const newPosition =
    direction === "L"
      ? (position - distance) % 100
      : (position + distance) % 100;

  console.log(`Rotation ${direction}${distance}: ${position} → ${newPosition}`);

  if (newPosition === 0) {
    console.log("🎯 ZERO LANDING");
  }

  return newPosition;
}
```

**Browser DevTools**:

- Use **Console** to check for errors and log output
- Use **Network** tab to verify file loads
- Use **Performance** tab to check frame rate
- Use **Elements** tab to inspect canvas rendering

---

## Architecture Overview

### File Structure

```
day-01/visualization/
├── index.html              # Main page
├── dial-animation.js       # Core animation logic
├── audio-manager.js        # Web Audio API wrapper
├── ui-controls.js          # User interaction handlers
├── styles.css              # Visual styling (optional)
└── README.md               # User-facing documentation
```

### Module Responsibilities

**index.html**:

- Canvas element
- UI controls (buttons, sliders, inputs)
- Script imports
- Initial setup

**dial-animation.js**:

- `parseInput()` - Input parsing
- `applyRotation()` - Rotation logic
- `countZeroCrossingsDuringRotation()` - Part 2 logic
- `solvePart1()` / `solvePart2()` - Solution functions
- `startAnimation()` - Animation initialization
- `updateAnimationFrame()` - Frame updates
- `drawDial()` / `drawPointer()` / `drawCounter()` - Rendering

**audio-manager.js**:

- `initAudio()` - AudioContext setup
- `playClickSound()` - Sound generation

**ui-controls.js**:

- `handleSpeedChange()` - Speed control
- `handleFileUpload()` - File input
- `handleModeChange()` - Part 1/2 toggle
- Event listeners

### State Management

**Global State** (or module-level state):

```javascript
let dialState = {
  position: 50,
  zeroCount: 0,
  rotationIndex: 0,
  isAnimating: false,
};

let animationConfig = {
  speed: 1.0,
  mode: "part1",
  audioEnabled: true,
  degreesPerSecond: 360,
};

let rotationSequence = [];
let audioManager = null;
let canvasContext = null;
```

**Update Pattern**:

```javascript
// Don't mutate directly in render loop
function updateAnimationFrame(currentTime) {
    // Calculate new state
    const newPosition = applyRotation(...);
    const newCount = calculateNewCount(...);

    // Update state atomically
    dialState = {
        ...dialState,
        position: newPosition,
        zeroCount: newCount
    };

    // Render based on new state
    render(dialState);
}
```

---

## Performance Considerations

### Optimization Checklist

- [ ] Pre-calculate segment positions (do once, not every frame)
- [ ] Use `requestAnimationFrame` (not `setInterval`)
- [ ] Clear canvas only when needed (not entire screen every frame)
- [ ] Avoid object allocation in animation loop
- [ ] Use integer positions (avoid floating point when possible)
- [ ] Batch canvas operations (save/restore context once)
- [ ] Throttle speed input changes (debounce)

### Expected Performance

| Metric           | Target | Notes                            |
| ---------------- | ------ | -------------------------------- |
| Frame rate       | 60 FPS | Achieved with Canvas + RAF       |
| Frame time       | <16ms  | Budget per frame at 60 FPS       |
| Memory usage     | <50MB  | Canvas buffer + state objects    |
| Input processing | <10ms  | Parse 1000 rotation instructions |
| Audio latency    | <50ms  | Web Audio API spec               |

---

## Deployment

### Production Checklist

Before merging to main:

- [ ] All manual tests pass
- [ ] Test on Chrome, Firefox, Safari, Edge
- [ ] README.md updated with usage instructions
- [ ] Main README.md mentions visualization tool
- [ ] Code is linted and formatted
- [ ] No console.log() statements in production code
- [ ] Error messages are user-friendly
- [ ] Loading states implemented
- [ ] Fallbacks for unsupported features

### Hosting Options

**Option 1: GitHub Pages** (Recommended)

```powershell
# Push to gh-pages branch
git checkout -b gh-pages
git push origin gh-pages
# Access at: https://username.github.io/advent-of-code-2025/day-01/visualization/
```

**Option 2: Local Server**

```powershell
# Quick local server
cd day-01/visualization
python -m http.server 8000
```

**Option 3: Standalone HTML**

```html
<!-- Embed all CSS/JS inline for single-file distribution -->
<!DOCTYPE html>
<html>
  <head>
    <style>
      /* inline CSS */
    </style>
  </head>
  <body>
    <canvas id="dialCanvas"></canvas>
    <script>
      /* inline JS */
    </script>
  </body>
</html>
```

---

## Troubleshooting

### Common Problems

**"Canvas is not supported"**

- Solution: Use modern browser (Chrome 90+, Firefox 88+, Safari 14+)

**"Audio not working"**

- Check: Browser supports Web Audio API
- Check: User hasn't muted tab/browser
- Check: AudioContext initialized on user interaction (click button first)

**"File won't load"**

- Check: Using local web server (not `file://` protocol)
- Check: File path is correct (`../input.txt`)
- Alternative: Use file upload dialog

**"Animation is slow"**

- Check: Frame rate in Performance DevTools
- Reduce: Canvas size or segment detail
- Simplify: Rendering (fewer draw calls per frame)

**"Counter value is wrong"**

- Verify: Algorithm matches Python solution
- Test: With test_input.txt (known answers)
- Log: Each rotation and counter increment

---

## Resources

### Documentation

- **Specification**: `../spec.md`
- **Data Model**: `../data-model.md`
- **API Contracts**: `../contracts/api-contract.md`
- **Implementation Plan**: `../plan.md`

### External References

- [HTML5 Canvas API](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API)
- [Web Audio API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API)
- [requestAnimationFrame](https://developer.mozilla.org/en-US/docs/Web/API/window/requestAnimationFrame)
- [FileReader API](https://developer.mozilla.org/en-US/docs/Web/API/FileReader)

### Related Code

- **Python Solution**: `../solution.py` (contains algorithms to port)
- **Python Tests**: `../test_solution.py` (test cases for validation)
- **Puzzle Description**: `../description.md` (original problem statement)

---

## Next Steps

1. **Start Implementation**: Follow development workflow above
2. **Test Incrementally**: Verify each phase before moving to next
3. **Validate Results**: Check against known answers (test_input.txt)
4. **Polish & Deploy**: Add finishing touches and ship!

**Questions?** Refer to spec.md or check existing Day 1 Python solution for algorithm reference.

**Happy coding! 🎨🔊**
