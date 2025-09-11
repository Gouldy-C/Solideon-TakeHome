export function computeBoundsWithFixedZ(
  pts: Array<[number, number, number]>,
  zThickness = 2
): {
  min: [number, number, number];
  max: [number, number, number];
  center: [number, number, number];
  size: [number, number, number];
} {
  if (!pts.length) {
    return {
      min: [-0.5, -0.5, -1],
      max: [0.5, 0.5, 1],
      center: [0, 0, 0],
      size: [1, 1, zThickness],
    };
  }

  const min: [number, number, number] = [
    Number.POSITIVE_INFINITY,
    Number.POSITIVE_INFINITY,
    Number.POSITIVE_INFINITY,
  ];
  const max: [number, number, number] = [
    Number.NEGATIVE_INFINITY,
    Number.NEGATIVE_INFINITY,
    Number.NEGATIVE_INFINITY,
  ];

  for (const [x, y, z] of pts) {
    if (x < min[0]) min[0] = x;
    if (y < min[1]) min[1] = y;
    if (z < min[2]) min[2] = z;
    if (x > max[0]) max[0] = x;
    if (y > max[1]) max[1] = y;
    if (z > max[2]) max[2] = z;
  }

  const sizeX = Math.max(max[0] - min[0], 1);
  const sizeY = Math.max(max[1] - min[1], 1);

  const center: [number, number, number] = [
    (min[0] + max[0]) / 2,
    (min[1] + max[1]) / 2,
    (min[2] + max[2]) / 2,
  ];

  const size: [number, number, number] = [sizeX, sizeY, zThickness];

  return { min, max, center, size };
}