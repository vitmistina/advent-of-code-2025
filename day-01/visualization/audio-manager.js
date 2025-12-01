let audioContext = null;

export function initAudio() {
  try {
    const Ctx = window.AudioContext || window.webkitAudioContext;
    if (!Ctx) return null;
    audioContext = new Ctx();
    return audioContext;
  } catch {
    return null;
  }
}

export function playClickSound() {
  if (!audioContext) return;
  // Ensure audio is running (browsers may start suspended until user interaction)
  if (audioContext.state === "suspended") {
    audioContext.resume().catch(() => {});
  }
  const oscillator = audioContext.createOscillator();
  const gainNode = audioContext.createGain();

  oscillator.frequency.value = 800;
  const t0 = audioContext.currentTime + 0.001;
  gainNode.gain.setValueAtTime(0.0001, t0);
  gainNode.gain.exponentialRampToValueAtTime(0.3, t0 + 0.005);
  gainNode.gain.exponentialRampToValueAtTime(0.01, t0 + 0.05);

  oscillator.connect(gainNode);
  gainNode.connect(audioContext.destination);

  oscillator.start(t0);
  oscillator.stop(t0 + 0.06);
}

window.addEventListener("DOMContentLoaded", () => {
  initAudio();
});
