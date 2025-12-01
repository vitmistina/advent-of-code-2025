// Core animation and dial logic
import { playClickSound } from "./audio-manager.js";

export const AnimationConfig = {
  speed: 1.0,
  mode: "part1",
};

export const DialState = {
  position: 50,
  rotations: [],
  rotationIndex: 0,
  zeroCount: 0,
  isAnimating: false,
};

let ctx;
let canvas;
let lastFrameTime = performance.now();

export function initCanvas() {
  canvas = document.getElementById("dialCanvas");
  ctx = canvas.getContext("2d");
  drawDial();
  drawPointer(DialState.position);
}

export function parseInput(inputText) {
  const lines = inputText
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => line.length > 0);

  const rotations = [];
  const re = /^[LR]\d+$/;
  for (const line of lines) {
    if (!re.test(line)) {
      throw new Error(`Invalid instruction format: ${line}`);
    }
    const direction = line[0];
    const distance = parseInt(line.slice(1), 10);
    rotations.push({ direction, distance });
  }
  return rotations;
}
let currentRotationProgress = 0; // 0..1 progress within the current rotation
const degreesPerSegment = 360 / 100; // 3.6° per segment
const rotationRate = 180; // degrees per second base, scaled by speed
let currentRotationStartPos = null;
let currentRotationLastCrossings = 0;

export function applyRotation(position, direction, distance) {
  const mod = 100;
  if (direction === "R") {
    return (position + distance) % mod;
  } else {
    const delta = distance % mod;
    return (position - delta + mod) % mod;
  }
}

export function countZeroCrossingsDuringRotation(
  startPosition,
  direction,
  distance
) {
  if (distance === 0) return 0;
  startPosition = ((startPosition % 100) + 100) % 100;
  if (direction === "R") {
    return Math.floor((startPosition + distance) / 100);
  } else {
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

export function positionToAngle(pos) {
  // 0 at top (−90°), clockwise increase
  return (pos * degreesPerSegment - 90) * (Math.PI / 180);
}

export function drawDial() {
  const w = canvas.width;
  const h = canvas.height;
  const cx = w / 2;
  const cy = h / 2;
  const radius = Math.min(cx, cy) - 40;

  ctx.clearRect(0, 0, w, h);

  // Outer circle
  ctx.strokeStyle = "#e6e6e6";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.arc(cx, cy, radius, 0, Math.PI * 2);
  ctx.stroke();

  // Tick marks and numbering
  for (let i = 0; i < 100; i++) {
    const angle = positionToAngle(i);
    const inner = radius - 12;
    const outer = radius;
    const ix = cx + inner * Math.cos(angle);
    const iy = cy + inner * Math.sin(angle);
    const ox = cx + outer * Math.cos(angle);
    const oy = cy + outer * Math.sin(angle);

    ctx.strokeStyle = i % 10 === 0 ? "#ffd866" : "#9aa0a6";
    ctx.lineWidth = i % 10 === 0 ? 2 : 1;
    ctx.beginPath();
    ctx.moveTo(ix, iy);
    ctx.lineTo(ox, oy);
    ctx.stroke();

    if (i % 10 === 0) {
      const labelRadius = radius + 20;
      const lx = cx + labelRadius * Math.cos(angle);
      const ly = cy + labelRadius * Math.sin(angle);
      ctx.fillStyle = "#ffd866";
      ctx.font = "bold 16px system-ui";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(String(i), lx, ly);
    }
  }

  // Highlight position 0
  const zeroAngle = positionToAngle(0);
  const zx = cx + radius * Math.cos(zeroAngle);
  const zy = cy + radius * Math.sin(zeroAngle);
  ctx.fillStyle = "#64ffda";
  ctx.beginPath();
  ctx.arc(zx, zy, 4, 0, Math.PI * 2);
  ctx.fill();
}

export function drawPointer(position) {
  const w = canvas.width;
  const h = canvas.height;
  const cx = w / 2;
  const cy = h / 2;
  const radius = Math.min(cx, cy) - 60;
  const angle = positionToAngle(position);
  const px = cx + radius * Math.cos(angle);
  const py = cy + radius * Math.sin(angle);

  ctx.strokeStyle = position === 0 ? "#64ffda" : "#ff6464";
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.moveTo(cx, cy);
  ctx.lineTo(px, py);
  ctx.stroke();

  // current position label (display as integer for readability)
  ctx.fillStyle = "#ffcc00";
  ctx.font = "bold 20px system-ui";
  ctx.textAlign = "center";
  ctx.textBaseline = "top";
  const dispPos = ((Math.round(position) % 100) + 100) % 100;
  ctx.fillText(`Pos: ${dispPos}`, cx, cy + 8);
}

export function startAnimation(rotations, mode) {
  DialState.rotations = rotations;
  DialState.rotationIndex = 0;
  DialState.zeroCount = 0;
  DialState.isAnimating = true;
  AnimationConfig.mode = mode || AnimationConfig.mode;
  currentRotationStartPos = DialState.position;
  currentRotationLastCrossings = 0;
  lastFrameTime = performance.now();
  requestAnimationFrame(animationLoop);
}

function animationLoop(currentTime) {
  if (!DialState.isAnimating) return;
  const deltaTime = (currentTime - lastFrameTime) / 1000;
  const adjusted = deltaTime * AnimationConfig.speed;
  updateAnimationFrame(adjusted);
  lastFrameTime = currentTime;
  requestAnimationFrame(animationLoop);
}

export function updateAnimationFrame(delta) {
  if (DialState.rotationIndex >= DialState.rotations.length) {
    DialState.isAnimating = false;
    return;
  }

  const { direction, distance } = DialState.rotations[DialState.rotationIndex];
  if (currentRotationStartPos == null)
    currentRotationStartPos = DialState.position;

  const totalDegrees = distance * degreesPerSegment;
  const degThisFrame = rotationRate * AnimationConfig.speed * delta;
  currentRotationProgress += degThisFrame / Math.max(1e-6, totalDegrees || 1);

  // During-rotation audio for Part 2: trigger clicks as zero crossings occur
  if (AnimationConfig.mode === "part2") {
    const traveledSegmentsInt = Math.floor(
      distance * Math.min(currentRotationProgress, 1)
    );
    if (traveledSegmentsInt > 0) {
      const crossingsSoFar = countZeroCrossingsDuringRotation(
        currentRotationStartPos,
        direction,
        traveledSegmentsInt
      );
      const deltaClicks = crossingsSoFar - currentRotationLastCrossings;
      for (let i = 0; i < deltaClicks; i++) {
        playClickSound();
      }
      if (deltaClicks > 0) currentRotationLastCrossings = crossingsSoFar;
    }
  }

  if (currentRotationProgress >= 1 || totalDegrees === 0) {
    const newPos = applyRotation(DialState.position, direction, distance);
    // Finalize Part 2 count
    if (AnimationConfig.mode === "part2") {
      const totalCrossings = countZeroCrossingsDuringRotation(
        currentRotationStartPos,
        direction,
        distance
      );
      DialState.zeroCount += totalCrossings;
    }
    DialState.position = newPos;
    if (AnimationConfig.mode === "part1") {
      if (newPos === 0) {
        DialState.zeroCount += 1;
        playClickSound();
      }
    }
    DialState.rotationIndex += 1;
    currentRotationProgress = 0;
    currentRotationStartPos = null;
    currentRotationLastCrossings = 0;
  } else {
    const directionSign = direction === "R" ? 1 : -1;
    const degreesMoved = totalDegrees * currentRotationProgress * directionSign;
    const segmentsMoved = degreesMoved / degreesPerSegment;
    const visualPos =
      (((DialState.position + segmentsMoved) % 100) + 100) % 100;
    drawDial();
    drawPointer(visualPos);
    drawCounter(DialState.zeroCount);
    return;
  }

  drawDial();
  drawPointer(DialState.position);
  drawCounter(DialState.zeroCount);
}

export function drawCounter(count) {
  ctx.fillStyle = "#e6e6e6";
  ctx.font = "bold 24px system-ui";
  ctx.textAlign = "left";
  ctx.textBaseline = "top";
  ctx.fillText(
    `${AnimationConfig.mode === "part2" ? "Part 2" : "Part 1"}: ${count}`,
    16,
    16
  );
}

export function resetAnimation() {
  DialState.position = 50;
  DialState.rotationIndex = 0;
  DialState.zeroCount = 0;
  DialState.isAnimating = false;
  drawDial();
  drawPointer(DialState.position);
  drawCounter(DialState.zeroCount);
}

export function pauseAnimation() {
  DialState.isAnimating = false;
}

export function resumeAnimation() {
  if (DialState.rotationIndex >= DialState.rotations.length) return;
  if (DialState.isAnimating) return;
  DialState.isAnimating = true;
  lastFrameTime = performance.now();
  requestAnimationFrame(animationLoop);
}

// Initialize on DOM ready
window.addEventListener("DOMContentLoaded", () => {
  initCanvas();
});
