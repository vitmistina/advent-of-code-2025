import {
  AnimationConfig,
  DialState,
  parseInput,
  startAnimation,
  resetAnimation,
  pauseAnimation,
  resumeAnimation,
} from "./dial-animation.js";
import { playClickSound } from "./audio-manager.js";

const TEST_INPUT = `L68\nL30\nR48\nL5\nR60\nL55\nL1\nL99\nR14\nL82`;

function syncSpeedLabel() {
  const label = document.getElementById("speedLabel");
  const slider = document.getElementById("speedSlider");
  label.textContent = `${Number(slider.value).toFixed(1)}x`;
}

export function handleSpeedChange() {
  const slider = document.getElementById("speedSlider");
  const input = document.getElementById("speedInput");
  const v = Number(slider.value);
  AnimationConfig.speed = v;
  input.value = String(v);
  syncSpeedLabel();
}

export function handleSpeedInputChange() {
  const input = document.getElementById("speedInput");
  let v = Number(input.value);
  if (Number.isNaN(v)) v = 1.0;
  v = Math.max(0.1, Math.min(10.0, v));
  AnimationConfig.speed = v;
  const slider = document.getElementById("speedSlider");
  slider.value = String(v);
  syncSpeedLabel();
}

export function handlePlayFromStart() {
  resetAnimation();
  // start with current mode
  const rotations = window.loadedRotations || [];
  startAnimation(rotations, AnimationConfig.mode);
}

export function handleModeChange() {
  const part1 = document.getElementById("modePart1");
  AnimationConfig.mode = part1.checked ? "part1" : "part2";
}

export function handleFileUpload(file) {
  const reader = new FileReader();
  reader.onload = (e) => {
    try {
      const text = e.target.result;
      const rotations = parseInput(text);
      window.loadedRotations = rotations;
    } catch (err) {
      const msg = document.getElementById("errorMsg");
      msg.textContent = "Failed to parse input file.";
    }
  };
  reader.readAsText(file);
}

window.addEventListener("DOMContentLoaded", () => {
  // Wire events
  document
    .getElementById("speedSlider")
    .addEventListener("input", handleSpeedChange);
  document
    .getElementById("speedInput")
    .addEventListener("change", handleSpeedInputChange);
  document
    .getElementById("playFromStartBtn")
    .addEventListener("click", handlePlayFromStart);
  document
    .getElementById("pauseBtn")
    .addEventListener("click", () => pauseAnimation());
  document
    .getElementById("resumeBtn")
    .addEventListener("click", () => resumeAnimation());
  document
    .getElementById("modePart1")
    .addEventListener("change", handleModeChange);
  document
    .getElementById("modePart2")
    .addEventListener("change", handleModeChange);
  document.getElementById("fileInput").addEventListener("change", (ev) => {
    const file = ev.target.files[0];
    if (file) handleFileUpload(file);
  });
  document.getElementById("loadTestInputBtn").addEventListener("click", () => {
    const rotations = parseInput(TEST_INPUT);
    window.loadedRotations = rotations;
  });

  // Preload test input
  window.loadedRotations = parseInput(TEST_INPUT);
  syncSpeedLabel();
});
