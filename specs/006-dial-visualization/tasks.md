---
description: "Task list for Day 1 Dial Visualization implementation"
---

# Tasks: Day 1 Dial Visualization

**Input**: Design documents from `/specs/006-dial-visualization/`  
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

**Tests**: Manual testing via browser with known inputs (test_input.txt). Automated tests are NOT included (visual features require manual validation).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Convention

All files in: `day-01/visualization/`

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Create directory structure and basic HTML skeleton

- [x] T001 Create day-01/visualization/ directory
- [x] T002 Create day-01/visualization/index.html with basic HTML5 structure
- [x] T003 [P] Create day-01/visualization/dial-animation.js (empty file)
- [x] T004 [P] Create day-01/visualization/audio-manager.js (empty file)
- [x] T005 [P] Create day-01/visualization/ui-controls.js (empty file)
- [x] T006 [P] Create day-01/visualization/styles.css (empty file)
- [x] T007 Add canvas element to index.html (800x800px, id="dialCanvas")
- [x] T008 Add UI controls skeleton to index.html (buttons, sliders, inputs)
- [x] T009 Link all JavaScript modules to index.html

**Checkpoint**: Directory structure ready, HTML skeleton loads in browser

---

## Phase 2: Foundational (Core Parsing & Logic)

**Purpose**: Port core algorithm from Python, implement parsing - BLOCKS all user stories

**⚠️ CRITICAL**: These functions are used by ALL user stories

- [ ] T010 Implement parseInput() in dial-animation.js (port from day-01/solution.py)
- [ ] T011 Implement applyRotation() in dial-animation.js (port from day-01/solution.py)
- [ ] T012 Test parseInput() in browser console with test_input.txt content
- [ ] T013 Test applyRotation() in browser console with known values
- [ ] T014 Add input validation to parseInput() (error handling for invalid format)
- [x] T010 Implement parseInput() in dial-animation.js (port from day-01/solution.py)
- [x] T011 Implement applyRotation() in dial-animation.js (port from day-01/solution.py)
- [ ] T012 Test parseInput() in browser console with test_input.txt content
- [ ] T013 Test applyRotation() in browser console with known values
- [x] T014 Add input validation to parseInput() (error handling for invalid format)

**Checkpoint**: Core functions work correctly - can parse input and calculate rotations

---

## Phase 3: User Story 1 - Visual Dial Animation (Priority: P1) 🎯 MVP

**Goal**: Display circular dial with 100 numbered segments and animate pointer moving through rotations

**Independent Test**: Load test_input.txt, verify dial renders correctly and pointer animates through all rotations

### Implementation for User Story 1

- [ ] T015 [P] [US1] Implement initCanvas() in dial-animation.js (set up canvas context, calculate center/radius)
- [ ] T016 [US1] Implement drawDial() in dial-animation.js (draw circle outline, 100 segment tick marks)
- [ ] T017 [US1] Add segment numbering to drawDial() (major ticks: 0,10,20...90 in 16px bold, minor ticks: 10px)
- [ ] T018 [US1] Test drawDial() renders correctly (manually call from browser console)
- [ ] T019 [P] [US1] Implement positionToAngle() helper in dial-animation.js (converts 0-99 to degrees)
- [ ] T020 [P] [US1] Implement drawPointer() in dial-animation.js (draw line/arrow from center to position)
- [x] T015 [P] [US1] Implement initCanvas() in dial-animation.js (set up canvas context, calculate center/radius)
- [x] T019 [P] [US1] Implement positionToAngle() helper in dial-animation.js (converts 0-99 to degrees)
- [x] T020 [P] [US1] Implement drawPointer() in dial-animation.js (draw line/arrow from center to position)
- [ ] T021 [US1] Test drawPointer() at various positions (0, 25, 50, 75, 99)
- [ ] T022 [US1] Implement basic animation state management (DialState object with position, rotationIndex, isAnimating)
- [ ] T023 [US1] Implement startAnimation() in dial-animation.js (initialize state, prepare rotation sequence)
- [ ] T024 [US1] Implement updateAnimationFrame() with requestAnimationFrame loop (time-based animation)
- [ ] T025 [US1] Add rotation execution logic to updateAnimationFrame() (process one rotation at a time)
- [ ] T026 [US1] Add smooth pointer movement during rotation (interpolate between positions)
- [ ] T027 [US1] Test full animation with test_input.txt (verify pointer moves through all 10 rotations)
- [ ] T028 [US1] Add visual highlighting for current position (larger font, different color)
- [ ] T029 [US1] Add visual highlighting for position 0 (special color)

**Checkpoint**: Dial renders beautifully, pointer animates smoothly through rotation sequence

---

## Phase 4: User Story 2 - Solution Counter Display (Priority: P2)

**Goal**: Display live counter that increments when dial lands on position 0 (Part 1 logic)

**Independent Test**: Load test_input.txt, run Part 1 animation, verify counter displays 3 at completion

### Implementation for User Story 2

- [ ] T030 [P] [US2] Implement drawCounter() in dial-animation.js (display counter on canvas)
- [ ] T031 [US2] Add zeroCount property to DialState
- [ ] T032 [US2] Implement Part 1 counting logic in updateAnimationFrame() (increment when position === 0 after rotation)
- [ ] T033 [US2] Call drawCounter() in render loop with current count
- [ ] T034 [US2] Test with test_input.txt (counter should reach 3)
- [ ] T035 [US2] Add counter label display (show "Part 1: {count}" or similar)
- [ ] T036 [US2] Style counter display (large font, prominent position, easy to read)
- [ ] T037 [US2] Add visual effect when counter increments (flash/highlight)

**Checkpoint**: Counter displays correctly and shows accurate Part 1 solution (3 for test input)

---

## Phase 5: User Story 3 - Audio Click Feedback (Priority: P3)

**Goal**: Play click sound whenever dial crosses or lands on position 0

**Independent Test**: Load test_input.txt, run animation, hear 3 clicks (Part 1) or 6 clicks (Part 2)

### Implementation for User Story 3

- [ ] T038 [P] [US3] Implement initAudio() in audio-manager.js (create AudioContext, check browser support)
- [ ] T039 [P] [US3] Implement createClickSound() in audio-manager.js (generate oscillator with gain envelope)
- [ ] T040 [P] [US3] Implement playClickSound() in audio-manager.js (play synthesized click)
- [ ] T041 [US3] Add audioManager initialization to index.html on page load
- [ ] T042 [US3] Add click sound trigger in updateAnimationFrame() when position === 0
- [ ] T043 [US3] Test audio plays on zero events (browser console should show no errors)
- [ ] T044 [US3] Add graceful degradation for browsers without Web Audio API support
- [ ] T045 [US3] Add visual indicator when audio not supported (show warning message)
- [ ] T046 [US3] Optimize click timing to avoid overlap (queue events if rapid succession)
- [x] T042 [US3] Add click sound trigger in updateAnimationFrame() when position === 0
- [ ] T043 [US3] Test audio plays on zero events (browser console should show no errors)
- [x] T044 [US3] Add graceful degradation for browsers without Web Audio API support
- [ ] T045 [US3] Add visual indicator when audio not supported (show warning message)
- [ ] T046 [US3] Optimize click timing to avoid overlap (queue events if rapid succession)

**Checkpoint**: Click sounds play synchronized with zero events, graceful fallback if audio unavailable

---

## Phase 6: User Story 4 - Adjustable Animation Speed (Priority: P4)

**Goal**: Allow users to control animation playback speed via slider or input

**Independent Test**: Adjust speed to 0.5x (slow), 2x (fast), 10x (very fast), verify animation speed changes accordingly

### Implementation for User Story 4

- [ ] T047 [P] [US4] Add speed slider to index.html (range 0.1 to 10, step 0.1, default 1.0)
- [ ] T048 [P] [US4] Add speed display label showing current speed value
- [ ] T049 [US4] Implement handleSpeedChange() in ui-controls.js (update AnimationConfig.speed)
- [ ] T050 [US4] Add event listener for speed slider change
- [ ] T051 [US4] Update updateAnimationFrame() to use speed multiplier (deltaTime \* speed)
- [ ] T052 [US4] Test speed changes during animation (verify smooth transition)
- [ ] T053 [US4] Test extreme speeds (0.1x very slow, 10x very fast)
- [ ] T054 [US4] Add visual feedback when speed changes (highlight slider briefly)

**Checkpoint**: Speed control works smoothly, animation responds to speed changes in real-time

---

## Phase 7: User Story 5 - Play from Start Control (Priority: P5)

**Goal**: Provide button to reset and restart animation from beginning

**Independent Test**: Run animation halfway, click "Play from Start", verify dial resets to position 50 and counter to 0, animation restarts

### Implementation for User Story 5

- [ ] T055 [P] [US5] Add "Play from Start" button to index.html
- [ ] T056 [US5] Implement resetAnimation() in dial-animation.js (reset DialState to initial values)
- [ ] T057 [US5] Implement handlePlayFromStart() in ui-controls.js (call resetAnimation, then startAnimation)
- [ ] T058 [US5] Add event listener for "Play from Start" button click
- [ ] T059 [US5] Test reset during animation (verify state clears correctly)
- [ ] T060 [US5] Test reset after animation completes
- [ ] T061 [US5] Test reset when paused mid-animation
- [ ] T062 [US5] Add visual feedback for button click (disable briefly during reset)

**Checkpoint**: Play from Start button works in all scenarios (running, paused, completed)

---

## Phase 8: User Story 6 - Speed Input Field (Priority: P6)

**Goal**: Allow direct numeric input for precise speed control

**Independent Test**: Type "2.5" in speed field, verify animation speed changes to 2.5x, field and slider stay synchronized

### Implementation for User Story 6

- [ ] T063 [P] [US6] Add numeric input field to index.html (type="number", min=0.1, max=10, step=0.1)
- [ ] T064 [US6] Implement validateSpeed() in ui-controls.js (check range 0.1-10.0)
- [ ] T065 [US6] Implement handleSpeedInputChange() in ui-controls.js (validate, update config, sync slider)
- [ ] T066 [US6] Add event listener for speed input change
- [ ] T067 [US6] Add two-way binding: slider change updates input field
- [ ] T068 [US6] Add two-way binding: input field change updates slider
- [ ] T069 [US6] Test invalid inputs (negative, zero, >10, non-numeric)
- [ ] T070 [US6] Add error display for invalid speed values (show validation message)
- [ ] T071 [US6] Test synchronization between slider and input field

**Checkpoint**: Speed input field works correctly with validation and stays synchronized with slider

---

## Phase 9: Part 2 Support (Extension)

**Goal**: Add Part 2 counting mode (count all zero crossings during rotation, not just landings)

**Independent Test**: Load test_input.txt, switch to Part 2 mode, run animation, verify counter displays 6

### Implementation for Part 2

- [ ] T072 [P] [P2] Port countZeroCrossingsDuringRotation() from Python to dial-animation.js
- [ ] T073 [P2] Test countZeroCrossingsDuringRotation() with known examples (50,R,1000 → 10)
- [ ] T074 [P] [P2] Add mode selector to index.html (radio buttons or toggle: Part 1 / Part 2)
- [ ] T075 [P2] Add mode property to AnimationConfig ('part1' or 'part2')
- [ ] T076 [P2] Implement handleModeChange() in ui-controls.js (update config, reset if needed)
- [ ] T077 [P2] Add event listener for mode selector change
- [ ] T078 [P2] Update updateAnimationFrame() to use Part 2 logic when mode === 'part2'
- [ ] T079 [P2] Update counter label to show current mode ("Part 1: {count}" or "Part 2: {count}")
- [x] T072 [P] [P2] Port countZeroCrossingsDuringRotation() from Python to dial-animation.js
- [ ] T073 [P2] Test countZeroCrossingsDuringRotation() with known examples (50,R,1000 → 10)
- [x] T078 [P2] Update updateAnimationFrame() to use Part 2 logic when mode === 'part2'
- [x] T079 [P2] Update counter label to show current mode ("Part 1: {count}" or "Part 2: {count}")
- [ ] T080 [P2] Test Part 2 with test_input.txt (verify counter reaches 6)
- [x] T081 [P2] Add click sounds for zero crossings in Part 2 (not just landings)
- [ ] T082 [P2] Test mode switching mid-animation (should reset)

**Checkpoint**: Part 2 mode works correctly, test input shows counter=6

---

## Phase 10: File Input & UI Polish

**Purpose**: Add file upload functionality and improve visual design

- [ ] T083 [P] Add file input element to index.html (accept=".txt")
- [ ] T084 Implement handleFileUpload() in ui-controls.js (FileReader API, parse, load rotations)
- [ ] T085 Add event listener for file input change
- [ ] T086 Test file upload with test_input.txt
- [ ] T087 Test file upload with input.txt (actual puzzle input)
- [ ] T088 [P] Add embedded test input as JavaScript constant (fallback/demo mode)
- [ ] T089 [P] Add "Load Test Input" button to use embedded data
- [ ] T090 Add error handling for invalid file formats (show user-friendly message)
- [ ] T091 Add error handling for empty files
- [ ] T092 [P] Implement CSS styling in styles.css (colors, layout, fonts)
- [ ] T093 [P] Make canvas responsive (scale with window size)
- [ ] T094 [P] Add loading state indicator (show "Loading..." during file read)
- [ ] T095 Add pause/resume button to UI
- [ ] T096 Implement pauseAnimation() and resumeAnimation() in dial-animation.js
- [ ] T097 Add event listeners for pause/resume buttons
- [x] T095 Add pause/resume button to UI
- [x] T096 Implement pauseAnimation() and resumeAnimation() in dial-animation.js
- [x] T097 Add event listeners for pause/resume buttons
- [ ] T098 Add visual feedback for button states (disabled, active, hover)

**Checkpoint**: File upload works, UI is polished and user-friendly

---

## Phase 11: Cross-Browser Testing & Polish

**Purpose**: Ensure compatibility and finalize all features

- [ ] T099 Test in Chrome 90+ (verify all features work)
- [ ] T100 Test in Firefox 88+ (verify all features work)
- [ ] T101 Test in Safari 14+ (verify all features work)
- [ ] T102 Test in Edge 90+ (verify all features work)
- [ ] T103 Add browser compatibility check on page load (show warning if unsupported)
- [ ] T104 Add fallback message for IE 11 (not supported)
- [ ] T105 [P] Optimize canvas rendering (minimize redraws, pre-calculate static values)
- [ ] T106 [P] Add comments to all functions (especially ported algorithms)
- [ ] T107 [P] Clean up console.log() statements (remove debugging logs)
- [ ] T108 [P] Create day-01/visualization/README.md with usage instructions
- [ ] T109 Update main README.md to mention visualization tool
- [ ] T110 Run quickstart.md validation (follow user workflow, verify all steps work)

**Checkpoint**: All features work across browsers, documentation complete

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories
- **User Stories (Phases 3-8)**: All depend on Foundational completion
  - Can proceed in priority order: US1 → US2 → US3 → US4 → US5 → US6
  - Or work on multiple in parallel (different files)
- **Part 2 Support (Phase 9)**: Depends on US1 (animation) and US2 (counter)
- **File Input & Polish (Phase 10)**: Can start after US1 complete
- **Testing & Polish (Phase 11)**: Depends on all desired features being complete

### User Story Dependencies

- **US1 (Visual Animation)**: Independent - only depends on Foundational
- **US2 (Counter)**: Depends on US1 (needs animation loop)
- **US3 (Audio)**: Independent - only depends on US1 (needs zero events)
- **US4 (Speed Control)**: Depends on US1 (needs animation loop)
- **US5 (Play from Start)**: Depends on US1 (needs resetAnimation)
- **US6 (Speed Input)**: Depends on US4 (extends speed control)
- **Part 2**: Depends on US1 and US2 (extends counting logic)

### Parallel Opportunities

**Setup Phase**:

- T003, T004, T005, T006 (create files) can run in parallel

**User Story 1**:

- T015, T019, T020 (different functions) can run in parallel
- T016 and T017 are sequential (drawing then numbering)

**User Story 2**:

- T030 can run in parallel with other US2 tasks if only creating skeleton

**User Story 3**:

- T038, T039, T040 (audio-manager.js functions) can run in parallel

**User Story 4**:

- T047, T048 (HTML elements) can run in parallel

**User Story 6**:

- T063 (HTML) can run in parallel with JavaScript implementation

**Phase 10**:

- T083, T088, T089, T092, T093, T094 (different files/concerns) can run in parallel

**Phase 11**:

- T099-T104 (browser testing) can run in parallel
- T105-T109 (documentation and cleanup) can run in parallel

---

## Parallel Example: User Story 1

```bash
# Can work simultaneously (different functions):
Task T015: "Implement initCanvas() in dial-animation.js"
Task T019: "Implement positionToAngle() helper in dial-animation.js"
Task T020: "Implement drawPointer() in dial-animation.js"

# Sequential (same function, build on each other):
Task T016: "Implement drawDial() - basic circle"
Task T017: "Add segment numbering to drawDial()"
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1 (Visual Animation)
4. Complete Phase 4: User Story 2 (Counter Display)
5. **STOP and VALIDATE**: Test with test_input.txt (should see counter=3)
6. This is a functional MVP - dial animates and shows correct answer!

### Incremental Delivery

1. **Foundation** (Phases 1-2) → Can parse and calculate
2. **+ US1** (Phase 3) → Can see dial animate → Demo-able!
3. **+ US2** (Phase 4) → Shows solution → MVP complete!
4. **+ US3** (Phase 5) → Audio feedback → Enhanced experience
5. **+ US4** (Phase 6) → Speed control → User control
6. **+ US5** (Phase 7) → Replay → Convenience feature
7. **+ US6** (Phase 8) → Precise speed → Power user feature
8. **+ Part 2** (Phase 9) → Full puzzle support
9. **+ Polish** (Phases 10-11) → Production ready

### Suggested Working Order

For solo developer (recommended):

1. Phases 1-2 (Setup + Foundation)
2. Phase 3 (US1 - Visual Animation) ← First demo milestone
3. Phase 4 (US2 - Counter) ← MVP milestone
4. Phase 10 (File Input) ← Make it easy to test
5. Phase 9 (Part 2 Support) ← Full feature parity
6. Phases 5-8 (Audio, Speed controls) ← Polish
7. Phase 11 (Testing & Docs) ← Ship it!

---

## Validation Checkpoints

### After Phase 2 (Foundation)

```javascript
// Browser console test
const input = "L68\nR48";
const rotations = parseInput(input);
console.log(rotations); // Should show [{direction: 'L', distance: 68}, {direction: 'R', distance: 48}]

const newPos = applyRotation(50, "L", 68);
console.log(newPos); // Should show 82
```

### After Phase 3 (US1 - Visual Animation)

- Open index.html in browser
- Dial with 100 segments should be visible
- Pointer should animate smoothly through rotations
- All 10 rotations from test input should execute

### After Phase 4 (US2 - Counter)

- Run animation with test_input.txt
- Counter should increment 3 times (when dial lands on 0)
- Final counter value: **3** ✓

### After Phase 9 (Part 2)

- Switch to Part 2 mode
- Run animation with test_input.txt
- Counter should increment 6 times (including during-rotation crossings)
- Final counter value: **6** ✓

### After Phase 11 (Complete)

- All features work in Chrome, Firefox, Safari, Edge
- File upload works with both test and actual inputs
- Speed controls work smoothly (0.1x to 10x)
- Audio clicks synchronized with zero events
- No console errors
- Documentation complete

---

## Notes

- **Manual Testing**: All validation is manual (visual inspection + browser console)
- **No Automated Tests**: Visual features require human observation
- **Browser DevTools**: Use Console for debugging, Performance for FPS monitoring
- **Incremental Commits**: Commit after each phase or logical milestone
- **Test Frequently**: Don't wait until the end - test each function as you build
- **Reference Python Solution**: day-01/solution.py has proven algorithms to port

**Total Tasks**: 110 tasks organized across 11 phases and 6 user stories + Part 2 support

**Estimated Completion**:

- MVP (Phases 1-4): 4-6 hours
- Full Feature (All phases): 12-16 hours
- With polish: 16-20 hours
