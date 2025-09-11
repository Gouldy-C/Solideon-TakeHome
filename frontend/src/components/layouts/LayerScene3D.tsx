import { useMemo, useState } from "react";
import { Canvas } from "@react-three/fiber";
import { Line, OrbitControls } from "@react-three/drei";
import { ToggleGroup, ToggleGroupItem } from "..//ui/toggle-group";
import type { Waypoint } from "../../lib/types";

type Props = {
  waypoints: Waypoint[];
  pointRadius?: number;
  lineWidth?: number;
};

export function LayerScene3D({
  waypoints,
  pointRadius = 0.1,
  lineWidth = 20,
}: Props) {
  const [modes, setModes] = useState<string[]>(["points", "lines"]);
  const renderPoints = modes.includes("points");
  const renderLines = modes.includes("lines");

  const sorted = useMemo(() => {
    return [...(waypoints ?? [])].sort((a, b) => {
      const sa = typeof a.seq === "number" ? a.seq : 0;
      const sb = typeof b.seq === "number" ? b.seq : 0;
      return sa - sb;
    });
  }, [waypoints]);

  const points = useMemo<[number, number, number][]>(() => {
    return sorted.map((w) => [
      Number(w.x) || 0,
      Number(w.z) || 0,
      Number(w.y) || 0,
    ]);
  }, [sorted]);

  const { center, maxSpan, radius } = useMemo(() => {
    return computeBounds(points);
  }, [points]);

  const offset: [number, number, number] = [-center[0], -center[1], -center[2]];

  const gridSize = Math.max(2, Math.ceil(maxSpan * 20));
  const gridDivs = 100;

  const fov = 50;
  const distance = computeCameraDistance(radius, fov, 1.2);

  return (
    <div className="relative h-full w-full">
      <Canvas
        className="h-full w-full bg-gray-950"
        camera={{
          position: [distance, 400, distance],
          fov,
          near: 0.1,
          far: Math.max(1000, maxSpan * 5000),
        }}
        
      >
        <ambientLight intensity={0.7} />
        <directionalLight position={[5, 10, 5]} intensity={0.9} />

        <group position={offset}>
          {points.length >= 2 && renderLines && (
            <Line
              points={points}
              color="gray"
              lineWidth={lineWidth}
              dashed={false}
            />
          )}

          {renderPoints && (
            <group>
              {points.map((p, i) => (
                <mesh position={p} key={i}>
                  <sphereGeometry args={[pointRadius, 16, 16]} />
                  <meshStandardMaterial color="white" />
                </mesh>
              ))}
            </group>
          )}

          <gridHelper
            args={[gridSize, gridDivs, "#334155", "#334155"]}
            position={offset}
          />
        </group>

        <OrbitControls makeDefault target={[0, 0, 0]} />
      </Canvas>

      <div className="absolute right-2 top-2 z-10 bg-background/50 rounded-md">
        <ToggleGroup
          type="multiple"
          variant="outline"
          size="sm"
          value={modes}
          onValueChange={(vals) => setModes(vals)}
        >
          <ToggleGroupItem value="points" aria-label="Toggle points visibility" className="p-3 cursor-pointer">
            Points
          </ToggleGroupItem>
          <ToggleGroupItem value="lines" aria-label="Toggle lines visibility" className="p-3 cursor-pointer">
            Lines
          </ToggleGroupItem>
        </ToggleGroup>
      </div>
    </div>
  );
}

function computeBounds(pts: Array<[number, number, number]>) {
  if (!pts.length) {
    return {
      min: [-0.5, -0.5, -0.5] as [number, number, number],
      max: [0.5, 0.5, 0.5] as [number, number, number],
      center: [0, 0, 0] as [number, number, number],
      size: [1, 1, 1] as [number, number, number],
      maxSpan: 1,
      radius: Math.sqrt(3) / 2, // ~0.866
    };
  }

  const min: [number, number, number] = [Infinity, Infinity, Infinity];
  const max: [number, number, number] = [-Infinity, -Infinity, -Infinity];

  for (const [x, y, z] of pts) {
    if (x < min[0]) min[0] = x;
    if (y < min[1]) min[1] = y;
    if (z < min[2]) min[2] = z;
    if (x > max[0]) max[0] = x;
    if (y > max[1]) max[1] = y;
    if (z > max[2]) max[2] = z;
  }

  const size: [number, number, number] = [
    Math.max(max[0] - min[0], 1e-6),
    Math.max(max[1] - min[1], 1e-6),
    Math.max(max[2] - min[2], 1e-6),
  ];
  const center: [number, number, number] = [
    (min[0] + max[0]) / 2,
    (min[1] + max[1]) / 2,
    (min[2] + max[2]) / 2,
  ];
  const maxSpan = Math.max(size[0], size[1], size[2]);

  const radius =
    0.5 * Math.sqrt(size[0] * size[0] + size[1] * size[1] + size[2] * size[2]);

  return { min, max, center, size, maxSpan, radius };
}

function computeCameraDistance(
  radius: number,
  fovDeg: number,
  marginMultiplier = 1.2
) {
  const fov = (fovDeg * Math.PI) / 180;
  const dist = radius / Math.tan(fov / 2);
  return Math.max(2, dist * marginMultiplier);
}
