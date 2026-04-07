import { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

interface ConstellationMapProps {
  visible?: boolean;
  opacity?: number;
  position?: [number, number, number];
}

type ConstellationDef = {
  name: string;
  stars: [number, number][];
  lines: [number, number][];
  offset: [number, number, number];
};

const constellations: ConstellationDef[] = [
  {
    name: 'Aries',
    stars: [[-0.4, 0.3], [0.0, 0.5], [0.3, 0.2], [0.5, -0.1]],
    lines: [[0, 1], [1, 2], [2, 3]],
    offset: [-4, 3, -8],
  },
  {
    name: 'Scorpio',
    stars: [[-0.5, 0.3], [-0.2, 0.1], [0.0, -0.1], [0.2, -0.3], [0.4, -0.2], [0.5, 0.0], [0.6, 0.3]],
    lines: [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6]],
    offset: [5, -2, -10],
  },
  {
    name: 'Leo',
    stars: [[-0.3, 0.5], [0.0, 0.6], [0.2, 0.4], [0.1, 0.1], [-0.1, -0.1], [-0.4, 0.0], [-0.3, 0.5]],
    lines: [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 0]],
    offset: [-6, -1, -12],
  },
  {
    name: 'Orion',
    stars: [
      [-0.2, 0.6], [0.2, 0.6],   // shoulders
      [-0.3, -0.5], [0.3, -0.5],  // feet
      [-0.1, 0.0], [0.0, 0.0], [0.1, 0.0], // belt
    ],
    lines: [[0, 1], [0, 4], [1, 6], [4, 5], [5, 6], [4, 2], [6, 3]],
    offset: [3, 4, -14],
  },
  {
    name: 'Cassiopeia',
    stars: [[-0.6, 0.0], [-0.3, 0.4], [0.0, 0.1], [0.3, 0.5], [0.6, 0.1]],
    lines: [[0, 1], [1, 2], [2, 3], [3, 4]],
    offset: [0, 5, -9],
  },
  {
    name: 'UrsaMajor',
    stars: [
      [-0.6, 0.2], [-0.4, 0.4], [-0.1, 0.4], [0.1, 0.2], // bowl
      [0.3, 0.1], [0.5, 0.2], [0.7, 0.0],                  // handle
    ],
    lines: [[0, 1], [1, 2], [2, 3], [3, 0], [3, 4], [4, 5], [5, 6]],
    offset: [-2, -4, -11],
  },
];

function Constellation({
  def,
  globalOpacity,
}: {
  def: ConstellationDef;
  globalOpacity: number;
}) {
  const groupRef = useRef<THREE.Group>(null);
  const twinkleRef = useRef<THREE.Points>(null);
  const timeOffset = useMemo(() => Math.random() * 100, []);

  const starPositions = useMemo(() => {
    const arr = new Float32Array(def.stars.length * 3);
    def.stars.forEach(([x, y], i) => {
      arr[i * 3] = x;
      arr[i * 3 + 1] = y;
      arr[i * 3 + 2] = 0;
    });
    return arr;
  }, [def.stars]);

  const linePositions = useMemo(() => {
    const points: number[] = [];
    def.lines.forEach(([a, b]) => {
      const [ax, ay] = def.stars[a];
      const [bx, by] = def.stars[b];
      points.push(ax, ay, 0, bx, by, 0);
    });
    return new Float32Array(points);
  }, [def.stars, def.lines]);

  useFrame(({ clock, pointer }) => {
    if (!groupRef.current) return;
    const t = clock.getElapsedTime() + timeOffset;

    // Subtle parallax with mouse
    groupRef.current.position.x = def.offset[0] + pointer.x * 0.15;
    groupRef.current.position.y = def.offset[1] + pointer.y * 0.15;
    groupRef.current.position.z = def.offset[2];

    // Twinkle effect on star sizes
    if (twinkleRef.current) {
      const mat = twinkleRef.current.material as THREE.PointsMaterial;
      mat.size = 0.08 + Math.sin(t * 1.5) * 0.02;
      mat.opacity = globalOpacity * (0.7 + Math.sin(t * 2.3) * 0.3);
    }
  });

  return (
    <group ref={groupRef} position={def.offset}>
      {/* Star dots */}
      <points ref={twinkleRef}>
        <bufferGeometry>
          <bufferAttribute
            attach="attributes-position"
            args={[starPositions, 3]}
            count={def.stars.length}
          />
        </bufferGeometry>
        <pointsMaterial
          color="var(--aged-gold-dim)"
          size={0.08}
          transparent
          opacity={globalOpacity}
          sizeAttenuation
          depthWrite={false}
          blending={THREE.AdditiveBlending}
        />
      </points>

      {/* Connecting lines */}
      <lineSegments>
        <bufferGeometry>
          <bufferAttribute
            attach="attributes-position"
            args={[linePositions, 3]}
            count={linePositions.length / 3}
          />
        </bufferGeometry>
        <lineBasicMaterial
          color="var(--aged-gold-dim)"
          transparent
          opacity={globalOpacity * 0.2}
          depthWrite={false}
          blending={THREE.AdditiveBlending}
        />
      </lineSegments>
    </group>
  );
}

export default function ConstellationMap({
  visible = true,
  opacity = 1,
  position = [0, 0, 0],
}: ConstellationMapProps) {
  if (!visible) return null;

  return (
    <group position={position}>
      {constellations.map((def) => (
        <Constellation key={def.name} def={def} globalOpacity={opacity} />
      ))}
    </group>
  );
}
