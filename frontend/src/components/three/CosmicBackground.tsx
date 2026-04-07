import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { Stars } from '@react-three/drei';
import { useRef, useMemo, useState, useEffect, useCallback } from 'react';
import * as THREE from 'three';

/* ------------------------------------------------------------------ */
/*  StarField – 3 000+ custom particles with twinkling                */
/* ------------------------------------------------------------------ */

function StarField() {
  const meshRef = useRef<THREE.Points>(null);
  const count = 3500;

  const { positions, colors, sizes, phases } = useMemo(() => {
    const pos = new Float32Array(count * 3);
    const col = new Float32Array(count * 3);
    const siz = new Float32Array(count);
    const pha = new Float32Array(count);

    const palette = [
      new THREE.Color('#ffffff'),
      new THREE.Color('var(--aged-gold-dim)'),
      new THREE.Color('#aac8ff'),
    ];

    for (let i = 0; i < count; i++) {
      // Random position inside sphere of radius 50
      const r = 50 * Math.cbrt(Math.random());
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);

      pos[i * 3] = r * Math.sin(phi) * Math.cos(theta);
      pos[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
      pos[i * 3 + 2] = r * Math.cos(phi);

      const c = palette[Math.floor(Math.random() * palette.length)];
      col[i * 3] = c.r;
      col[i * 3 + 1] = c.g;
      col[i * 3 + 2] = c.b;

      siz[i] = 0.01 + Math.random() * 0.04;
      pha[i] = Math.random() * Math.PI * 2;
    }

    return { positions: pos, colors: col, sizes: siz, phases: pha };
  }, []);

  useFrame(({ clock }) => {
    if (!meshRef.current) return;
    meshRef.current.rotation.y += 0.0001;

    // Twinkling via size attribute
    const geo = meshRef.current.geometry;
    const sizeAttr = geo.getAttribute('size') as THREE.BufferAttribute;
    const arr = sizeAttr.array as Float32Array;
    const t = clock.getElapsedTime();
    for (let i = 0; i < count; i++) {
      arr[i] = sizes[i] * (0.7 + 0.3 * Math.sin(t * 2 + phases[i]));
    }
    sizeAttr.needsUpdate = true;
  });

  return (
    <points ref={meshRef}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          args={[positions, 3]}
        />
        <bufferAttribute
          attach="attributes-color"
          args={[colors, 3]}
        />
        <bufferAttribute
          attach="attributes-size"
          args={[sizes.slice(), 1]}
        />
      </bufferGeometry>
      <pointsMaterial
        vertexColors
        size={0.04}
        sizeAttenuation
        transparent
        opacity={0.9}
        depthWrite={false}
      />
    </points>
  );
}

/* ------------------------------------------------------------------ */
/*  NebulaClouds – large translucent spheres                          */
/* ------------------------------------------------------------------ */

const nebulaData = [
  { color: '#2d1b69', opacity: 0.06, scale: 12, position: [-8, 4, -20] as [number, number, number], speed: 0.3 },
  { color: '#4a0040', opacity: 0.05, scale: 10, position: [10, -3, -25] as [number, number, number], speed: 0.25 },
  { color: '#1a1200', opacity: 0.08, scale: 15, position: [0, -6, -30] as [number, number, number], speed: 0.35 },
  { color: '#2d1b69', opacity: 0.03, scale: 8, position: [6, 8, -18] as [number, number, number], speed: 0.2 },
];

function NebulaCloud({
  color,
  opacity,
  scale,
  position,
  speed,
}: (typeof nebulaData)[number]) {
  const meshRef = useRef<THREE.Mesh>(null);

  useFrame(({ clock }) => {
    if (!meshRef.current) return;
    const t = clock.getElapsedTime() * speed;
    meshRef.current.position.x = position[0] + Math.sin(t) * 0.5;
    meshRef.current.position.y = position[1] + Math.cos(t * 0.7) * 0.4;
  });

  return (
    <mesh ref={meshRef} position={position} scale={scale}>
      <sphereGeometry args={[1, 16, 16]} />
      <meshBasicMaterial
        color={color}
        transparent
        opacity={opacity}
        depthWrite={false}
        side={THREE.DoubleSide}
      />
    </mesh>
  );
}

function NebulaClouds() {
  return (
    <>
      {nebulaData.map((data, i) => (
        <NebulaCloud key={i} {...data} />
      ))}
    </>
  );
}

/* ------------------------------------------------------------------ */
/*  CosmicDust – tiny gold-tinted floating particles                  */
/* ------------------------------------------------------------------ */

function CosmicDust() {
  const meshRef = useRef<THREE.Points>(null);
  const count = 500;

  const { positions, basePosY } = useMemo(() => {
    const pos = new Float32Array(count * 3);
    const baseY = new Float32Array(count);
    for (let i = 0; i < count; i++) {
      pos[i * 3] = (Math.random() - 0.5) * 40;
      pos[i * 3 + 1] = (Math.random() - 0.5) * 40;
      pos[i * 3 + 2] = (Math.random() - 0.5) * 40;
      baseY[i] = pos[i * 3 + 1];
    }
    return { positions: pos, basePosY: baseY };
  }, []);

  useFrame(({ clock }) => {
    if (!meshRef.current) return;
    const posAttr = meshRef.current.geometry.getAttribute(
      'position',
    ) as THREE.BufferAttribute;
    const arr = posAttr.array as Float32Array;
    const t = clock.getElapsedTime();
    for (let i = 0; i < count; i++) {
      // slow upward drift, wrapping around
      arr[i * 3 + 1] = basePosY[i] + ((t * 0.1 + i * 0.02) % 40) - 20;
    }
    posAttr.needsUpdate = true;
  });

  return (
    <points ref={meshRef}>
      <bufferGeometry>
        <bufferAttribute attach="attributes-position" args={[positions, 3]} />
      </bufferGeometry>
      <pointsMaterial
        color="var(--aged-gold-dim)"
        size={0.008}
        sizeAttenuation
        transparent
        opacity={0.4}
        depthWrite={false}
      />
    </points>
  );
}

/* ------------------------------------------------------------------ */
/*  ShootingStar – occasional streak across the sky                   */
/* ------------------------------------------------------------------ */

function ShootingStar() {
  const meshRef = useRef<THREE.Mesh>(null);
  const trailRef = useRef<THREE.Mesh>(null);
  const state = useRef({
    active: false,
    start: new THREE.Vector3(),
    end: new THREE.Vector3(),
    progress: 0,
    nextTime: Math.random() * 5 + 5,
  });

  useFrame(({ clock }) => {
    const t = clock.getElapsedTime();
    const s = state.current;

    if (!s.active) {
      if (t > s.nextTime) {
        s.active = true;
        s.progress = 0;
        // Random start/end high up in the sky
        s.start.set(
          (Math.random() - 0.5) * 30,
          10 + Math.random() * 10,
          -10 - Math.random() * 20,
        );
        s.end.set(
          s.start.x + (Math.random() - 0.5) * 20,
          s.start.y - 15 - Math.random() * 10,
          s.start.z + (Math.random() - 0.5) * 10,
        );
      }
      return;
    }

    s.progress += 0.02;

    if (s.progress >= 1) {
      s.active = false;
      s.nextTime = t + 5 + Math.random() * 5;
      if (meshRef.current) meshRef.current.visible = false;
      if (trailRef.current) trailRef.current.visible = false;
      return;
    }

    const pos = new THREE.Vector3().lerpVectors(s.start, s.end, s.progress);
    const trailPos = new THREE.Vector3().lerpVectors(
      s.start,
      s.end,
      Math.max(0, s.progress - 0.08),
    );

    if (meshRef.current) {
      meshRef.current.visible = true;
      meshRef.current.position.copy(pos);
    }
    if (trailRef.current) {
      trailRef.current.visible = true;
      trailRef.current.position.copy(trailPos);
      // Orient trail towards the head
      trailRef.current.lookAt(pos);
      const opacity = 1 - s.progress;
      (trailRef.current.material as THREE.MeshBasicMaterial).opacity =
        opacity * 0.6;
    }
  });

  return (
    <>
      <mesh ref={meshRef} visible={false}>
        <sphereGeometry args={[0.04, 8, 8]} />
        <meshBasicMaterial color="var(--aged-gold-dim)" transparent opacity={0.9} />
      </mesh>
      <mesh ref={trailRef} visible={false}>
        <cylinderGeometry args={[0.01, 0.03, 1.5, 6]} />
        <meshBasicMaterial
          color="var(--aged-gold-dim)"
          transparent
          opacity={0.5}
          depthWrite={false}
        />
      </mesh>
    </>
  );
}

/* ------------------------------------------------------------------ */
/*  Parallax rig – subtle mouse-follow for the whole scene            */
/* ------------------------------------------------------------------ */

function ParallaxRig() {
  const { camera } = useThree();
  const target = useRef({ x: 0, y: 0 });

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      target.current.x = (e.clientX / window.innerWidth - 0.5) * 0.4;
      target.current.y = (e.clientY / window.innerHeight - 0.5) * 0.4;
    };
    window.addEventListener('mousemove', handler);
    return () => window.removeEventListener('mousemove', handler);
  }, []);

  useFrame(() => {
    camera.position.x += (target.current.x - camera.position.x) * 0.02;
    camera.position.y += (-target.current.y - camera.position.y) * 0.02;
  });

  return null;
}

/* ------------------------------------------------------------------ */
/*  CosmicBackground – the exported wrapper                           */
/* ------------------------------------------------------------------ */

export default function CosmicBackground() {
  return (
    <div className="fixed inset-0 z-0" style={{ pointerEvents: 'none' }}>
      <Canvas
        camera={{ position: [0, 0, 5], fov: 75 }}
        gl={{ antialias: false, alpha: true }}
        dpr={[1, 1.5]}
      >
        <StarField />
        <NebulaClouds />
        <CosmicDust />
        <ShootingStar />
        <ParallaxRig />
      </Canvas>
    </div>
  );
}
