import { useRef, useMemo } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Stars, Float, Text3D, Center } from '@react-three/drei';
import * as THREE from 'three';

// 3D Zodiac Ring Component
function ZodiacRing() {
  const groupRef = useRef<THREE.Group>(null);
  
  useFrame((state) => {
    if (groupRef.current) {
      groupRef.current.rotation.y = state.clock.elapsedTime * 0.1;
      groupRef.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.2) * 0.1;
    }
  });

  const symbols = useMemo(() => [
    '♈', '♉', '♊', '♋', '♌', '♍', 
    '♎', '♏', '♐', '♑', '♒', '♓'
  ], []);

  return (
    <group ref={groupRef}>
      {/* Central glowing sphere */}
      <mesh>
        <sphereGeometry args={[0.8, 32, 32]} />
        <meshStandardMaterial 
          color="#ffd700" 
          emissive="#d4af37"
          emissiveIntensity={0.5}
          metalness={0.8}
          roughness={0.2}
        />
      </mesh>
      
      {/* Inner glow */}
      <mesh>
        <sphereGeometry args={[1.2, 32, 32]} />
        <meshBasicMaterial 
          color="#ffd700" 
          transparent 
          opacity={0.1}
        />
      </mesh>

      {/* Zodiac symbols in a ring */}
      {symbols.map((symbol, i) => {
        const angle = (i / symbols.length) * Math.PI * 2;
        const radius = 2.5;
        const x = Math.cos(angle) * radius;
        const z = Math.sin(angle) * radius;
        
        return (
          <Float 
            key={i}
            speed={2} 
            rotationIntensity={0.5} 
            floatIntensity={0.5}
          >
            <group position={[x, 0, z]} rotation={[0, -angle + Math.PI/2, 0]}>
              <mesh>
                <boxGeometry args={[0.3, 0.3, 0.05]} />
                <meshStandardMaterial 
                  color="#1a1a1a"
                  metalness={0.9}
                  roughness={0.1}
                />
              </mesh>
              {/* Glow behind symbol */}
              <mesh position={[0, 0, -0.02]}>
                <planeGeometry args={[0.4, 0.4]} />
                <meshBasicMaterial 
                  color="#d4af37" 
                  transparent 
                  opacity={0.3}
                />
              </mesh>
            </group>
          </Float>
        );
      })}

      {/* Outer ring */}
      <mesh rotation={[Math.PI/2, 0, 0]}>
        <torusGeometry args={[2.5, 0.02, 16, 100]} />
        <meshBasicMaterial color="#d4af37" transparent opacity={0.5} />
      </mesh>
      
      {/* Second outer ring */}
      <mesh rotation={[Math.PI/2, 0, 0]} position={[0, 0, 0]}>
        <torusGeometry args={[3.2, 0.01, 16, 100]} />
        <meshBasicMaterial color="#ffd700" transparent opacity={0.3} />
      </mesh>
    </group>
  );
}

// Floating particles
function Particles() {
  const count = 200;
  const positions = useMemo(() => {
    const positions = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      positions[i * 3] = (Math.random() - 0.5) * 20;
      positions[i * 3 + 1] = (Math.random() - 0.5) * 20;
      positions[i * 3 + 2] = (Math.random() - 0.5) * 20;
    }
    return positions;
  }, []);

  const pointsRef = useRef<THREE.Points>(null);

  useFrame((state) => {
    if (pointsRef.current) {
      pointsRef.current.rotation.y = state.clock.elapsedTime * 0.05;
    }
  });

  return (
    <points ref={pointsRef}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={count}
          array={positions}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial
        size={0.05}
        color="#d4af37"
        transparent
        opacity={0.8}
        sizeAttenuation
      />
    </points>
  );
}

// Main 3D Scene
export default function ZodiacScene() {
  return (
    <div className="fixed inset-0 z-0">
      <Canvas
        camera={{ position: [0, 0, 8], fov: 50 }}
        gl={{ antialias: true, alpha: true }}
        style={{ background: 'transparent' }}
      >
        {/* Lighting */}
        <ambientLight intensity={0.3} />
        <pointLight position={[10, 10, 10]} intensity={1} color="#ffd700" />
        <pointLight position={[-10, -10, -10]} intensity={0.5} color="#d4af37" />
        
        {/* 3D Elements */}
        <ZodiacRing />
        <Particles />
        <Stars 
          radius={50} 
          depth={50} 
          count={1000} 
          factor={4} 
          saturation={0} 
          fade 
          speed={0.5}
          color="#d4af37"
        />
      </Canvas>
    </div>
  );
}
