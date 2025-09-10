export function colorForIndex(i: number): string {
  const palette = [
    "#06B6D4",
    "#7C3AED",
    "#F59E0B",
    "#10B981",
    "#3B82F6",
    "#EF4444",
  ];
  return palette[i % palette.length];
}

export function colorForValue(
  v: number,
  min: number,
  max: number
): [number, number, number] {
  // Blue (low) -> Yellow (mid) -> Red (high)
  const t = clamp((v - min) / Math.max(max - min, 1e-9), 0, 1);
  // simple 3-point gradient
  if (t < 0.5) {
    const k = t / 0.5; // 0..1
    return lerpRGB([0.2, 0.4, 1], [1, 0.9, 0], k);
  }
  const k = (t - 0.5) / 0.5;
  return lerpRGB([1, 0.9, 0], [1, 0.2, 0.2], k);
}

function clamp(x: number, a: number, b: number) {
  return Math.max(a, Math.min(b, x));
}
function lerp(a: number, b: number, t: number) {
  return a + (b - a) * t;
}
function lerpRGB(a: number[], b: number[], t: number) {
  return [lerp(a[0], b[0], t), lerp(a[1], b[1], t), lerp(a[2], b[2], t)] as [
    number,
    number,
    number
  ];
}