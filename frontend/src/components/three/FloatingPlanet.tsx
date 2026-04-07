import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { Float } from '@react-three/drei';
import * as THREE from 'three';

interface FloatingPlanetProps {
  color: string;
  size: number;
  position: [number, number, number];
  hasRing?: boolean;
  orbitRadius?: number;
  rotationSpeed?: number;
}

export default function FloatingPlanet({
  color,
  size,
  position,
  hasRing = false,
  orbitRadius,
  rotationSpeed = 0.3,
}: FloatingPlanetProps) {
  const planetRef = useRef<THREE.Mesh>(null);
  const ringRef = useRef<THREE.Mesh>(null);
  const glowRef = useRef<THREE.Mesh>(null);

  useFrame(({ clock }) => {
    const t = clock.getElapsedTime();
    if (planetRef.current) {
      planetRef.current.rotation.y = t * rotationSpeed;
      planetRef.current.rotation.x = Math.sin(t * 0.2) * 0.1;
    }
    if (ringRef.current) {
      ringRef.current.rotation.z = t * rotationSpeed * 0.5;
    }
    if (glowRef.current) {
      const mat = glowRef.current.material as THREE.MeshBasicMaterial;
      mat.opacity = 0.08 + Math.sin(t * 0.8) * 0.03;
    }
  });

  return (
    <group position={position}>
      {/* Orbit path */}
      {orbitRadius != null && (
        <mesh rotation={[-Math.PI / 2, 0, 0]}>
          <torusGeometry args={[orbitRadius, 0.005, 8, 128]} />
          <meshBasicMaterial
            color="#B45309"
            transparent
            opacity={0.1}
            depthWrite={false}
          />
        </mesh>
      )}

      <Float speed={1.5} rotationIntensity={0.2} floatIntensity={0.5}>
        {/* Planet sphere */}
        <mesh ref={planetRef}>
          <sphereGeometry args={[size, 32, 32]} />
          <meshStandardMaterial
            color={color}
            roughness={0.7}
            metalness={0.3}
            emissive={color}
            emissiveIntensity={0.15}
          />
        </mesh>

        {/* Glow aura */}
        <mesh ref={glowRef}>
          <sphereGeometry args={[size * 1.4, 24, 24]} />
          <meshBasicMaterial
            color={color}
            transparent
            opacity={0.08}
            side={THREE.BackSide}
            depthWrite={false}
            blending={THREE.AdditiveBlending}
          />
        </mesh>

        {/* Ring (like Saturn) */}
        {hasRing && (
          <mesh ref={ringRef} rotation={[Math.PI / 3, 0.2, 0]}>
            <ringGeometry args={[size * 1.3, size * 2, 64]} />
            <meshBasicMaterial
              color={color}
              transparent
              opacity={0.25}
              side={THREE.DoubleSide}
              depthWrite={false}
            />
          </mesh>
        )}
      </Float>

      {/* Ambient + point light for the planet */}
      <ambientLight intensity={0.4} />
      <pointLight position={[3, 3, 3]} intensity={0.6} />
    </group>
  );
}
