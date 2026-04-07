import { useRef, useState, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import { Float, Billboard, Text } from '@react-three/drei';
import * as THREE from 'three';

interface ArmillarySphereProps {
  interactive?: boolean;
  scale?: number;
}

const ZODIAC_SYMBOLS = ['♈','♉','♊','♋','♌','♍','♎','♏','♐','♑','♒','♓'];

const goldMaterial = new THREE.MeshStandardMaterial({
  color: new THREE.Color('var(--aged-gold-dim)'),
  metalness: 0.9,
  roughness: 0.2,
});

const darkGoldMaterial = new THREE.MeshStandardMaterial({
  color: new THREE.Color('var(--aged-gold-dim)'),
  metalness: 0.9,
  roughness: 0.2,
});

const innerRingMaterial = new THREE.MeshStandardMaterial({
  color: new THREE.Color('var(--aged-gold-dim)'),
  metalness: 0.85,
  roughness: 0.25,
});

const centralSphereMaterial = new THREE.MeshStandardMaterial({
  color: new THREE.Color('var(--aged-gold-dim)'),
  emissive: new THREE.Color('var(--aged-gold-dim)'),
  emissiveIntensity: 0.5,
  metalness: 0.7,
  roughness: 0.3,
});

const auraMaterial = new THREE.MeshBasicMaterial({
  color: new THREE.Color('var(--aged-gold-dim)'),
  transparent: true,
  opacity: 0.03,
  side: THREE.DoubleSide,
});

export default function ArmillarySphere({ interactive = false, scale = 1 }: ArmillarySphereProps) {
  const groupRef = useRef<THREE.Group>(null);
  const eclipticRef = useRef<THREE.Mesh>(null);
  const equatorialRef = useRef<THREE.Mesh>(null);
  const inner1Ref = useRef<THREE.Mesh>(null);
  const inner2Ref = useRef<THREE.Mesh>(null);
  const inner3Ref = useRef<THREE.Mesh>(null);
  const [hovered, setHovered] = useState(false);
  const [dragging, setDragging] = useState(false);
  const dragStart = useRef<{ x: number; y: number } | null>(null);
  const rotationOffset = useRef<{ x: number; y: number }>({ x: 0, y: 0 });

  const zodiacPositions = useMemo(() => {
    return ZODIAC_SYMBOLS.map((symbol, i) => {
      const angle = (i / 12) * Math.PI * 2;
      const radius = 1.85;
      const tilt = 23.5 * (Math.PI / 180);
      const x = Math.cos(angle) * radius;
      const y = Math.sin(angle) * radius * Math.sin(tilt);
      const z = Math.sin(angle) * radius * Math.cos(tilt);
      return { symbol, position: [x, y, z] as [number, number, number] };
    });
  }, []);

  useFrame((_state, delta) => {
    if (!groupRef.current) return;

    const speed = hovered ? 0.004 : 0.002;

    if (!dragging) {
      groupRef.current.rotation.y += speed;
    }

    if (eclipticRef.current) {
      eclipticRef.current.rotation.z += delta * 0.1;
    }
    if (equatorialRef.current) {
      equatorialRef.current.rotation.z -= delta * 0.08;
    }
    if (inner1Ref.current) {
      inner1Ref.current.rotation.z += delta * 0.12;
    }
    if (inner2Ref.current) {
      inner2Ref.current.rotation.z -= delta * 0.06;
    }
    if (inner3Ref.current) {
      inner3Ref.current.rotation.z += delta * 0.09;
    }
  });

  const handlePointerDown = (e: THREE.Event & { point: THREE.Vector3; clientX?: number; clientY?: number }) => {
    if (!interactive) return;
    e.stopPropagation();
    setDragging(true);
    const evt = e as unknown as { clientX: number; clientY: number };
    dragStart.current = { x: evt.clientX, y: evt.clientY };
  };

  const handlePointerMove = (e: THREE.Event & { clientX?: number; clientY?: number }) => {
    if (!interactive || !dragging || !dragStart.current || !groupRef.current) return;
    const evt = e as unknown as { clientX: number; clientY: number };
    const dx = (evt.clientX - dragStart.current.x) * 0.005;
    const dy = (evt.clientY - dragStart.current.y) * 0.005;
    groupRef.current.rotation.y = rotationOffset.current.y + dx;
    groupRef.current.rotation.x = rotationOffset.current.x + dy;
  };

  const handlePointerUp = () => {
    if (!interactive || !groupRef.current) return;
    setDragging(false);
    rotationOffset.current = {
      x: groupRef.current.rotation.x,
      y: groupRef.current.rotation.y,
    };
    dragStart.current = null;
  };

  return (
    <Float speed={1.5} rotationIntensity={0} floatIntensity={0.3} floatingRange={[-0.1, 0.1]}>
      <group
        ref={groupRef}
        scale={scale}
        onPointerOver={() => setHovered(true)}
        onPointerOut={() => {
          setHovered(false);
          if (dragging) handlePointerUp();
        }}
        onPointerDown={handlePointerDown}
        onPointerMove={handlePointerMove}
        onPointerUp={handlePointerUp}
      >
        {/* Outer Ring (Meridian) - vertical */}
        <mesh rotation={[0, 0, 0]} material={goldMaterial}>
          <torusGeometry args={[2, 0.03, 16, 100]} />
        </mesh>

        {/* Ecliptic Ring - tilted 23.5 degrees */}
        <mesh
          ref={eclipticRef}
          rotation={[23.5 * (Math.PI / 180), 0, 0]}
          material={goldMaterial}
        >
          <torusGeometry args={[1.8, 0.025, 16, 100]} />
        </mesh>

        {/* Equatorial Ring - horizontal */}
        <mesh
          ref={equatorialRef}
          rotation={[Math.PI / 2, 0, 0]}
          material={darkGoldMaterial}
        >
          <torusGeometry args={[1.6, 0.025, 16, 100]} />
        </mesh>

        {/* Inner Ring 1 */}
        <mesh
          ref={inner1Ref}
          rotation={[Math.PI / 4, Math.PI / 6, 0]}
          material={innerRingMaterial}
        >
          <torusGeometry args={[1.4, 0.02, 16, 80]} />
        </mesh>

        {/* Inner Ring 2 */}
        <mesh
          ref={inner2Ref}
          rotation={[-Math.PI / 5, Math.PI / 3, Math.PI / 8]}
          material={innerRingMaterial}
        >
          <torusGeometry args={[1.4, 0.02, 16, 80]} />
        </mesh>

        {/* Inner Ring 3 */}
        <mesh
          ref={inner3Ref}
          rotation={[Math.PI / 3, -Math.PI / 4, Math.PI / 6]}
          material={innerRingMaterial}
        >
          <torusGeometry args={[1.4, 0.02, 16, 80]} />
        </mesh>

        {/* Central Sphere (Earth/Sun) */}
        <mesh material={centralSphereMaterial}>
          <sphereGeometry args={[0.3, 32, 32]} />
        </mesh>

        {/* Point light inside for glow */}
        <pointLight color="var(--aged-gold-dim)" intensity={2} distance={5} />

        {/* Zodiac Symbols around the ecliptic ring */}
        {zodiacPositions.map(({ symbol, position }, i) => (
          <Billboard key={i} follow lockX={false} lockY={false} lockZ={false} position={position}>
            <Text
              fontSize={0.15}
              color="var(--aged-gold-dim)"
              anchorX="center"
              anchorY="middle"
              outlineWidth={0.005}
              outlineColor="var(--aged-gold-dim)"
            >
              {symbol}
              <meshBasicMaterial
                color="var(--aged-gold-dim)"
                toneMapped={false}
              />
            </Text>
          </Billboard>
        ))}

        {/* Golden aura sphere */}
        <mesh material={auraMaterial}>
          <sphereGeometry args={[2.5, 32, 32]} />
        </mesh>
      </group>
    </Float>
  );
}
