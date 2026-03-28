import { useEffect, useMemo, useRef } from 'react';

// SVG Zodiac Icons - Pure Gold
const ZodiacIcons: Record<string, JSX.Element> = {
  aries: <svg viewBox="0 0 100 100" fill="currentColor"><path d="M30,85 V75 C30,65 35,60 45,60 H55 C65,60 70,65 70,75 V85 H80 V75 C80,60 72,52 62,50 C68,46 72,40 72,32 C72,18 62,8 50,8 C38,8 28,18 28,32 C28,40 32,46 38,50 C28,52 20,60 20,75 V85 H30 M50,18 C56,18 62,24 62,32 C62,40 56,46 50,46 C44,46 38,40 38,32 C38,24 44,18 50,18 Z"/></svg>,
  taurus: <svg viewBox="0 0 100 100" fill="currentColor"><path d="M50,15 C30,15 15,30 15,50 C15,65 25,77 38,82 C28,85 20,92 20,100 H30 C30,92 38,88 50,88 C62,88 70,92 70,100 H80 C80,92 72,85 62,82 C75,77 85,65 85,50 C85,30 70,15 50,15 M50,25 C64,25 75,36 75,50 C75,64 64,75 50,75 C36,75 25,64 25,50 C25,36 36,25 50,25 Z"/></svg>,
  gemini: <svg viewBox="0 0 100 100" fill="currentColor"><path d="M25,10 V20 H40 V80 H25 V90 H75 V80 H60 V20 H75 V10 H25 M48,20 H52 V80 H48 V20 Z"/></svg>,
  cancer: <svg viewBox="0 0 100 100" fill="currentColor"><path d="M50,15 C30,15 15,30 15,50 C15,65 25,77 38,82 C28,85 22,92 22,100 H32 C32,92 40,88 50,88 C60,88 68,92 68,100 H78 C78,92 72,85 62,82 C75,77 85,65 85,50 C85,30 70,15 50,15 M50,25 C64,25 75,36 75,50 C75,64 64,75 50,75 C36,75 25,64 25,50 C25,36 36,25 50,25 Z"/></svg>,
  leo: <svg viewBox="0 0 100 100" fill="currentColor"><path d="M50,10 C30,10 15,25 15,45 C15,60 25,72 38,77 C30,80 25,88 25,98 C25,100 26,102 28,102 C30,102 32,100 32,98 C32,88 40,82 50,82 C60,82 68,88 68,98 C68,100 70,102 72,102 C74,102 75,100 75,98 C75,88 70,80 62,77 C75,72 85,60 85,45 C85,25 70,10 50,10 M50,20 C64,20 75,31 75,45 C75,59 64,70 50,70 C36,70 25,59 25,45 C25,31 36,20 50,20 Z"/></svg>,
  virgo: <svg viewBox="0 0 100 100" fill="currentColor"><path d="M20,10 V20 H35 V50 C35,60 28,65 25,75 V100 H35 V75 C35,70 40,65 45,62 V100 H55 V45 C55,40 60,35 65,32 V100 H75 V32 C75,22 70,15 62,12 V10 H52 V28 C52,28 50,32 48,35 V10 H20 M78,10 V35 C78,45 85,50 88,55 V100 H98 V55 C98,45 90,38 88,28 V10 H78 Z"/></svg>,
  libra: <svg viewBox="0 0 100 100" fill="currentColor"><path d="M10,80 V90 H90 V80 H10 M25,10 V25 C25,40 35,48 48,52 V55 H30 V65 H70 V55 H52 V52 C65,48 75,40 75,25 V10 H60 V25 C60,35 55,42 50,42 C45,42 40,35 40,25 V10 H25 Z"/></svg>,
  scorpio: <svg viewBox="0 0 100 100" fill="currentColor"><path d="M25,10 V25 C25,40 35,48 48,52 V58 C35,58 25,68 25,85 V100 H35 V85 C35,75 40,68 48,65 V100 H58 V65 L78,55 V100 H88 V55 C88,40 78,32 68,28 V10 H58 V42 C58,32 53,25 48,22 V10 H25 M62,10 H68 V48 L62,52 V10 Z"/></svg>,
  sagittarius: <svg viewBox="0 0 100 100" fill="currentColor"><path d="M50,10 L40,20 L65,45 L15,95 L25,105 L75,55 L100,80 L105,70 L105,10 H50 M90,20 L80,30 L70,20 H90 V40 L80,30 L90,20 Z"/></svg>,
  capricorn: <svg viewBox="0 0 100 100" fill="currentColor"><path d="M20,10 V25 C20,45 35,55 48,58 V55 C38,52 30,42 30,25 V10 H20 M52,10 V25 C52,42 62,52 72,55 V100 H82 V55 C82,35 68,25 58,22 V10 H52 M88,10 V100 H98 V10 H88 Z"/></svg>,
  aquarius: <svg viewBox="0 0 100 100" fill="currentColor"><path d="M5,40 L15,50 L25,40 L35,50 L45,40 L55,50 L65,40 L75,50 L85,40 L95,50 L100,45 L85,30 L75,40 L65,30 L55,40 L45,30 L35,40 L25,30 L15,40 L5,30 V40 M5,65 L15,75 L25,65 L35,75 L45,65 L55,75 L65,65 L75,75 L85,65 L95,75 L100,70 L85,55 L75,65 L65,55 L55,65 L45,55 L35,65 L25,55 L15,65 L5,55 V65 Z"/></svg>,
  pisces: <svg viewBox="0 0 100 100" fill="currentColor"><path d="M15,10 C15,35 30,55 50,62 C70,55 85,35 85,10 H75 C75,30 65,45 50,52 C35,45 25,30 25,10 H15 M15,90 C15,65 30,45 50,38 C70,45 85,65 85,90 H75 C75,70 65,55 50,48 C35,55 25,70 25,90 H15 Z"/></svg>,
  sun: <svg viewBox="0 0 100 100" fill="currentColor"><circle cx="50" cy="50" r="18"/><path d="M50,10 V20 M50,80 V90 M10,50 H20 M80,50 H90 M22,22 L29,29 M71,71 L78,78 M22,78 L29,71 M71,29 L78,22" stroke="currentColor" strokeWidth="6" strokeLinecap="round"/></svg>,
  moon: <svg viewBox="0 0 100 100" fill="currentColor"><path d="M50,10 C28,10 10,28 10,50 C10,72 28,90 50,90 C52,90 54,89 56,89 C42,84 32,68 32,50 C32,30 44,14 60,9 C57,9 54,10 50,10 Z"/></svg>,
  mercury: <svg viewBox="0 0 100 100" fill="currentColor"><path d="M50,15 C32,15 18,29 18,47 C18,62 28,75 42,80 V100 H48 V82 H52 V100 H58 V80 C72,75 82,62 82,47 C82,29 68,15 50,15 M50,25 C62,25 72,35 72,47 C72,59 62,69 50,69 C38,69 28,59 28,47 C28,35 38,25 50,25 Z"/></svg>,
  venus: <svg viewBox="0 0 100 100" fill="currentColor"><circle cx="50" cy="38" r="20"/><path d="M50,58 V100 M35,78 H65" stroke="currentColor" strokeWidth="6" strokeLinecap="round"/></svg>,
  mars: <svg viewBox="0 0 100 100" fill="currentColor"><circle cx="40" cy="60" r="20"/><path d="M65,15 V45 M65,15 H95 M65,15 L95,45" stroke="currentColor" strokeWidth="6" strokeLinecap="round" fill="none"/></svg>,
  jupiter: <svg viewBox="0 0 100 100" fill="currentColor"><path d="M30,10 C30,25 40,35 50,35 C60,35 70,25 70,10 H60 C60,20 55,25 50,25 C45,25 40,20 40,10 H30 M20,45 C20,65 35,80 50,80 C65,80 80,65 80,45 H70 C70,60 60,70 50,70 C40,70 30,60 30,45 H20 M10,85 V100 H90 V95 H20 V85 H10 Z"/></svg>,
  saturn: <svg viewBox="0 0 100 100" fill="currentColor"><path d="M50,15 C32,15 18,29 18,47 C18,62 28,75 42,80 V100 H58 V80 C72,75 82,62 82,47 C82,29 68,15 50,15 M50,25 C62,25 72,35 72,47 C72,59 62,69 50,69 C38,69 28,59 28,47 C28,35 38,25 50,25 M5,55 V65 H20 V55 H5 M80,55 V65 H95 V55 H80 Z"/></svg>,
  star4: <svg viewBox="0 0 100 100" fill="currentColor"><path d="M50,5 L60,40 L95,50 L60,60 L50,95 L40,60 L5,50 L40,40 Z"/></svg>,
  star5: <svg viewBox="0 0 100 100" fill="currentColor"><path d="M50,0 L61,35 L98,35 L68,57 L79,92 L50,70 L21,92 L32,57 L2,35 L39,35 Z"/></svg>
};

interface SymbolData {
  id: number;
  type: string;
  left: number;
  top: number;
  size: number;
  delay: number;
  duration: number;
  opacity: number;
  rotate: number;
}

export default function CosmicBackground() {
  const containerRef = useRef<HTMLDivElement>(null);
  const symbolElsRef = useRef<Map<number, HTMLDivElement>>(new Map());
  const mouseRef = useRef({ x: -1000, y: -1000 });

  const symbols = useMemo<SymbolData[]>(() => {
    const items: SymbolData[] = [];
    const iconKeys = Object.keys(ZodiacIcons);
    
    for (let i = 0; i < 32; i++) {
      const left = Math.random() * 100;
      const top = Math.random() * 100;
      const inCenterX = left > 30 && left < 70;
      const inCenterY = top > 25 && top < 75;
      
      items.push({
        id: i,
        type: iconKeys[i % iconKeys.length],
        left,
        top,
        size: 28 + Math.random() * 24,
        delay: Math.random() * 4,
        duration: 5 + Math.random() * 3,
        opacity: inCenterX && inCenterY ? 0.15 : 0.45 + Math.random() * 0.25,
        rotate: Math.random() * 360
      });
    }
    
    return items;
  }, []);

  // Parallax effect
  useEffect(() => {
    let rafId: number;
    
    const handleMouseMove = (e: MouseEvent) => {
      const rect = containerRef.current?.getBoundingClientRect();
      if (rect) {
        mouseRef.current = { x: e.clientX - rect.left, y: e.clientY - rect.top };
      }
    };

    const animate = () => {
      const mx = mouseRef.current.x;
      const my = mouseRef.current.y;
      
      symbolElsRef.current.forEach((el, id) => {
        const rect = el.getBoundingClientRect();
        const ex = rect.left + rect.width / 2;
        const ey = rect.top + rect.height / 2;
        const dx = mx - ex;
        const dy = my - ey;
        const dist = Math.sqrt(dx * dx + dy * dy);
        
        // Parallax: move symbols away from mouse
        let tx = 0, ty = 0;
        if (dist < 250 && dist > 0) {
          const force = (1 - dist / 250) * 20;
          tx = -(dx / dist) * force;
          ty = -(dy / dist) * force;
        }
        
        el.style.transform = `translate3d(${tx}px, ${ty}px, 0)`;
      });
      
      rafId = requestAnimationFrame(animate);
    };

    const container = containerRef.current;
    container?.addEventListener('mousemove', handleMouseMove, { passive: true });
    rafId = requestAnimationFrame(animate);
    
    return () => {
      container?.removeEventListener('mousemove', handleMouseMove);
      cancelAnimationFrame(rafId);
    };
  }, []);

  return (
    <div ref={containerRef} className="fixed inset-0 z-0 overflow-hidden bg-[#F5F0E8]">
      {/* Symbols with floating animation */}
      {symbols.map((s) => (
        <div
          key={s.id}
          ref={(el) => { if (el) symbolElsRef.current.set(s.id, el); }}
          className="absolute will-change-transform"
          style={{
            left: `${s.left}%`,
            top: `${s.top}%`,
            width: `${s.size}px`,
            height: `${s.size}px`,
            opacity: s.opacity,
            color: '#9A7B0A',
            filter: 'drop-shadow(0 0 10px rgba(212,175,55,0.4)) drop-shadow(0 0 20px rgba(212,175,55,0.2))',
            pointerEvents: 'none'
          }}
        >
          <div style={{
            width: '100%',
            height: '100%',
            animation: `float ${s.duration}s ease-in-out infinite`,
            animationDelay: `${s.delay}s`,
            transform: `rotate(${s.rotate}deg)`
          }}>
            {ZodiacIcons[s.type]}
          </div>
        </div>
      ))}

      {/* Stars */}
      {Array.from({ length: 30 }).map((_, i) => (
        <div
          key={`star-${i}`}
          className="absolute w-[2px] h-[2px] bg-[#9A7B0A] rounded-full pointer-events-none"
          style={{
            left: `${Math.random() * 100}%`,
            top: `${Math.random() * 100}%`,
            boxShadow: '0 0 6px #9A7B0A',
            opacity: 0.3 + Math.random() * 0.5,
            animation: `pulse ${3 + Math.random() * 3}s ease-in-out infinite`,
            animationDelay: `${Math.random() * 4}s`
          }}
        />
      ))}

      {/* Vignette */}
      <div 
        className="absolute inset-0 pointer-events-none"
        style={{
          background: 'radial-gradient(ellipse at center, transparent 0%, rgba(139,69,19,0.03) 60%, rgba(139,69,19,0.08) 100%)'
        }}
      />

      <style>{`
        @keyframes float {
          0%, 100% { transform: translate3d(0, 0, 0) rotate(var(--r, 0deg)); }
          50% { transform: translate3d(0, -12px, 0) rotate(calc(var(--r, 0deg) + 3deg)); }
        }
        @keyframes pulse {
          0%, 100% { opacity: 0.3; transform: scale(1); }
          50% { opacity: 0.7; transform: scale(1.3); }
        }
      `}</style>
    </div>
  );
}
