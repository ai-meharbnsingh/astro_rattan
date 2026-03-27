import { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import { Billboard, Text } from '@react-three/drei';
import * as THREE from 'three';

interface ZodiacWheelProps {
  size?: number;
  tilt?: number;
  rotationSpeed?: number;
}

const zodiacSymbols = [
  '\u2648', // Aries
  '\u2649', // Taurus
  '\u264A', // Gemini
  '\u264B', // Cancer
  '\u264C', // Leo
  '\u264D', // Virgo
  '\u264E', // Libra
  '\u264F', // Scorpio
  '\u2650', // Sagittarius
  '\u2651', // Capricorn
  '\u2652', // Aquarius
  '\u2653', // Pisces
];

function SegmentLines({ size, count }: { size: number; count: number }) {
  const positions = useMemo(() => {
    const pts: number[] = [];
    for (let i = 0; i < count; i++) {
      const angle = (i / count) * Math.PI * 2;
      const innerR = size * 0.55;
      const outerR = size * 0.9;
      pts.push(
        Math.cos(angle) * innerR,
        Math.sin(angle) * innerR,
        0,
        Math.cos(angle) * outerR,
        Math.sin(angle) * outerR,
        0,
      );
    }
    return new Float32Array(pts);
  }, [size, count]);

  return (
    <lineSegments>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          args={[positions, 3]}
          count={positions.length / 3}
        />
      </bufferGeometry>
      <lineBasicMaterial
        color="#ffd700"
        transparent
        opacity={0.3}
        depthWrite={false}
      />
    </lineSegments>
  );
}

export default function ZodiacWheel({
  size = 2,
  tilt = 0.5,
  rotationSpeed = 0.1,
}: ZodiacWheelProps) {
  const groupRef = useRef<THREE.Group>(null);
  const glowRef = useRef<THREE.Mesh>(null);

  useFrame(({ clock }) => {
    if (groupRef.current) {
      groupRef.current.rotation.z = clock.getElapsedTime() * rotationSpeed;
    }
    if (glowRef.current) {
      const mat = glowRef.current.material as THREE.MeshBasicMaterial;
      mat.opacity = 0.12 + Math.sin(clock.getElapsedTime() * 1.2) * 0.04;
    }
  });

  const symbolRadius = size * 0.72;

  return (
    <group rotation={[tilt, 0, 0]}>
      <group ref={groupRef}>
        {/* Outer gold border ring */}
        <mesh>
          <torusGeometry args={[size * 0.9, size * 0.02, 16, 128]} />
          <meshStandardMaterial
            color="#ffd700"
            emissive="#ffd700"
            emissiveIntensity={0.4}
            metalness={0.8}
            roughness={0.2}
          />
        </mesh>

        {/* Inner border ring */}
        <mesh>
          <torusGeometry args={[size * 0.55, size * 0.01, 16, 128]} />
          <meshStandardMaterial
            color="#ffd700"
            emissive="#ffd700"
            emissiveIntensity={0.3}
            metalness={0.8}
            roughness={0.3}
          />
        </mesh>

        {/* Glowing border effect */}
        <mesh ref={glowRef}>
          <torusGeometry args={[size * 0.9, size * 0.08, 16, 128]} />
          <meshBasicMaterial
            color="#ffd700"
            transparent
            opacity={0.12}
            depthWrite={false}
            blending={THREE.AdditiveBlending}
          />
        </mesh>

        {/* Segment divider lines */}
        <SegmentLines size={size} count={12} />

        {/* Zodiac symbols */}
        {zodiacSymbols.map((symbol, i) => {
          const angle = (i / 12) * Math.PI * 2 - Math.PI / 2;
          const x = Math.cos(angle) * symbolRadius;
          const y = Math.sin(angle) * symbolRadius;
          return (
            <Billboard key={i} position={[x, y, 0.01]} follow={false}>
              <Text
                fontSize={size * 0.1}
                color="#ffd700"
                anchorX="center"
                anchorY="middle"
              >
                {symbol}
              </Text>
            </Billboard>
          );
        })}

        {/* Center disc (semi-transparent) */}
        <mesh position={[0, 0, -0.01]}>
          <circleGeometry args={[size * 0.55, 64]} />
          <meshBasicMaterial
            color="#1a0a2e"
            transparent
            opacity={0.5}
            depthWrite={false}
          />
        </mesh>
      </group>

      {/* Ambient lighting */}
      <ambientLight intensity={0.5} />
      <pointLight position={[0, 0, 3]} intensity={0.4} />
    </group>
  );
}
