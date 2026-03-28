import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { useRef, useMemo, useEffect } from 'react';
import * as THREE from 'three';

/* ------------------------------------------------------------------ */
/*  CosmicSymbols – Real zodiac & planetary symbols scattered        */
/* ------------------------------------------------------------------ */

function CosmicSymbols() {
  const groupRef = useRef<THREE.Group>(null);
  
  const symbols = useMemo(() => {
    // Real cosmic symbols
    const cosmicGlyphs = [
      '♈', '♉', '♊', '♋', '♌', '♍', // Zodiac
      '♎', '♏', '♐', '♑', '♒', '♓',
      '☉', '☽', '☿', '♀', '♂', '♃', // Planets
      '♄', '♅', '♆', '☊', '☋',
      '✦', '✧', '✪', '✯', '✶'       // Stars
    ];
    
    const items = [];
    
    // Create 35 symbols scattered EVERYWHERE
    for (let i = 0; i < 35; i++) {
      // True random scatter - entire screen area
      const angle = Math.random() * Math.PI * 2;
      const radius = 15 + Math.random() * 50; // Spread from 15 to 65 units
      
      const x = Math.cos(angle) * radius * (0.5 + Math.random() * 0.5);
      const y = (Math.random() - 0.5) * 60; // Full height spread
      const z = -5 - Math.random() * 50;    // Depth variation
      
      items.push({
        position: [x, y, z] as [number, number, number],
        glyph: cosmicGlyphs[i % cosmicGlyphs.length],
        scale: 0.4 + Math.random() * 0.8,
        rotation: [0, 0, (Math.random() - 0.5) * 0.5],
        floatSpeed: 0.2 + Math.random() * 0.3,
        floatOffset: Math.random() * Math.PI * 2,
        opacity: 0.15 + Math.random() * 0.25
      });
    }
    return items;
  }, []);

  useFrame(({ clock }) => {
    if (!groupRef.current) return;
    const t = clock.getElapsedTime();
    
    groupRef.current.children.forEach((child, i) => {
      const symbol = symbols[i];
      if (symbol) {
        // Gentle floating
        const floatY = Math.sin(t * symbol.floatSpeed + symbol.floatOffset) * 0.4;
        child.position.y = symbol.position[1] + floatY;
        
        // Very slow rotation
        child.rotation.z = symbol.rotation[2] + Math.sin(t * 0.1 + i) * 0.05;
      }
    });
  });

  // Create text sprites for symbols
  return (
    <group ref={groupRef}>
      {symbols.map((sym, i) => (
        <SymbolSprite 
          key={i}
          glyph={sym.glyph}
          position={sym.position}
          scale={sym.scale}
          rotation={sym.rotation}
          opacity={sym.opacity}
        />
      ))}
    </group>
  );
}

// Helper component to create text sprite
function SymbolSprite({ 
  glyph, 
  position, 
  scale, 
  rotation, 
  opacity 
}: { 
  glyph: string; 
  position: [number, number, number]; 
  scale: number; 
  rotation: [number, number, number];
  opacity: number;
}) {
  const meshRef = useRef<THREE.Mesh>(null);
  
  const texture = useMemo(() => {
    const canvas = document.createElement('canvas');
    canvas.width = 128;
    canvas.height = 128;
    const ctx = canvas.getContext('2d')!;
    
    // Clear
    ctx.clearRect(0, 0, 128, 128);
    
    // Draw glow
    ctx.shadowColor = '#9A7B0A';
    ctx.shadowBlur = 20;
    
    // Draw symbol
    ctx.font = '80px serif';
    ctx.fillStyle = `rgba(212, 175, 55, ${opacity})`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(glyph, 64, 64);
    
    const tex = new THREE.CanvasTexture(canvas);
    tex.needsUpdate = true;
    return tex;
  }, [glyph, opacity]);

  return (
    <mesh ref={meshRef} position={position} rotation={rotation}>
      <planeGeometry args={[scale * 2, scale * 2]} />
      <meshBasicMaterial 
        map={texture} 
        transparent 
        opacity={opacity}
        side={THREE.DoubleSide}
        depthWrite={false}
      />
    </mesh>
  );
}

/* ------------------------------------------------------------------ */
/*  StarField – Very few scattered stars                             */
/* ------------------------------------------------------------------ */

function StarField() {
  const meshRef = useRef<THREE.Points>(null);
  const count = 300;

  const positions = useMemo(() => {
    const pos = new Float32Array(count * 3);
    
    for(let i = 0; i < count * 3; i+=3) {
      // Scattered in wide area
      const angle = Math.random() * Math.PI * 2;
      const radius = 10 + Math.random() * 70;
      
      pos[i] = Math.cos(angle) * radius;
      pos[i+1] = (Math.random() - 0.5) * 80;
      pos[i+2] = -10 - Math.random() * 50;
    }
    return pos;
  }, []);

  useFrame(() => {
    if (!meshRef.current) return;
    meshRef.current.rotation.y += 0.00005;
  });

  return (
    <points ref={meshRef}>
      <bufferGeometry>
        <bufferAttribute attach="attributes-position" args={[positions, 3]} />
      </bufferGeometry>
      <pointsMaterial
        color="#9A7B0A"
        size={0.1}
        sizeAttenuation
        transparent
        opacity={0.5}
      />
    </points>
  );
}

/* ------------------------------------------------------------------ */
/*  ConstellationLines – Connecting some symbols                      */
/* ------------------------------------------------------------------ */

function ConstellationLines() {
  const linesRef = useRef<THREE.LineSegments>(null);
  
  const linePositions = useMemo(() => {
    const positions = [];
    // Create random connections between scattered points
    for (let i = 0; i < 12; i++) {
      const angle1 = Math.random() * Math.PI * 2;
      const r1 = 20 + Math.random() * 40;
      const x1 = Math.cos(angle1) * r1;
      const y1 = (Math.random() - 0.5) * 50;
      const z1 = -15 - Math.random() * 25;
      
      const angle2 = angle1 + (Math.random() - 0.5);
      const r2 = r1 + (Math.random() - 0.5) * 20;
      const x2 = Math.cos(angle2) * r2;
      const y2 = y1 + (Math.random() - 0.5) * 15;
      const z2 = z1 + (Math.random() - 0.5) * 10;
      
      positions.push(x1, y1, z1, x2, y2, z2);
    }
    return new Float32Array(positions);
  }, []);

  return (
    <lineSegments ref={linesRef}>
      <bufferGeometry>
        <bufferAttribute attach="attributes-position" args={[linePositions, 3]} />
      </bufferGeometry>
      <lineBasicMaterial color="#9A7B0A" transparent opacity={0.06} />
    </lineSegments>
  );
}

/* ------------------------------------------------------------------ */
/*  MouseParallax – Camera follows cursor                            */
/* ------------------------------------------------------------------ */

function MouseParallax() {
  const { camera } = useThree();
  const target = useRef({ x: 0, y: 0 });

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      target.current.x = (e.clientX / window.innerWidth - 0.5) * 2;
      target.current.y = (e.clientY / window.innerHeight - 0.5) * 1.5;
    };
    window.addEventListener('mousemove', handler);
    return () => window.removeEventListener('mousemove', handler);
  }, []);

  useFrame(() => {
    camera.position.x += (target.current.x - camera.position.x) * 0.02;
    camera.position.y += (target.current.y - camera.position.y) * 0.02;
  });

  return null;
}

/* ------------------------------------------------------------------ */
/*  ObservatoryBackground – Main export                              */
/* ------------------------------------------------------------------ */

export default function ObservatoryBackground() {
  return (
    <div className="fixed inset-0 z-0" style={{ pointerEvents: 'none' }}>
      <Canvas
        camera={{ position: [0, 0, 25], fov: 75 }}
        gl={{ antialias: true, alpha: true }}
        dpr={[1, 2]}
      >
        <StarField />
        <CosmicSymbols />
        <ConstellationLines />
        <MouseParallax />
      </Canvas>
    </div>
  );
}
