import { useState, useEffect, useMemo } from 'react';

// --- Types ---
interface PlanetPosition {
  name: string;
  sign: string;
  degree: number;
  nakshatra: string;
  retrograde: boolean;
}

interface PlanetaryPositionsProps {
  planets?: PlanetPosition[];
}

// --- Constants ---
const ZODIAC_SIGNS = [
  'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
  'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces',
];

const ZODIAC_SYMBOLS: Record<string, string> = {
  Aries: '\u2648', Taurus: '\u2649', Gemini: '\u264A', Cancer: '\u264B',
  Leo: '\u264C', Virgo: '\u264D', Libra: '\u264E', Scorpio: '\u264F',
  Sagittarius: '\u2650', Capricorn: '\u2651', Aquarius: '\u2652', Pisces: '\u2653',
};

const PLANET_COLORS: Record<string, string> = {
  Sun: '#FF8C00',
  Moon: '#E8E8E8',
  Mars: '#DC143C',
  Mercury: '#32CD32',
  Jupiter: 'var(--aged-gold-dim)',
  Venus: '#FF69B4',
  Saturn: '#8B8682',
  Rahu: '#4B0082',
  Ketu: '#8B4513',
};

const PLANET_SYMBOLS: Record<string, string> = {
  Sun: '\u2609', Moon: '\u263D', Mars: '\u2642', Mercury: '\u263F',
  Jupiter: '\u2643', Venus: '\u2640', Saturn: '\u2644', Rahu: '\u260A', Ketu: '\u260B',
};

const DEFAULT_PLANETS: PlanetPosition[] = [
  { name: 'Sun', sign: 'Pisces', degree: 12.4, nakshatra: 'Uttara Bhadrapada', retrograde: false },
  { name: 'Moon', sign: 'Cancer', degree: 22.1, nakshatra: 'Ashlesha', retrograde: false },
  { name: 'Mars', sign: 'Gemini', degree: 8.7, nakshatra: 'Ardra', retrograde: false },
  { name: 'Mercury', sign: 'Pisces', degree: 25.3, nakshatra: 'Revati', retrograde: true },
  { name: 'Jupiter', sign: 'Taurus', degree: 18.9, nakshatra: 'Rohini', retrograde: false },
  { name: 'Venus', sign: 'Aquarius', degree: 5.2, nakshatra: 'Dhanishta', retrograde: false },
  { name: 'Saturn', sign: 'Pisces', degree: 2.8, nakshatra: 'Purva Bhadrapada', retrograde: false },
  { name: 'Rahu', sign: 'Pisces', degree: 20.1, nakshatra: 'Revati', retrograde: true },
  { name: 'Ketu', sign: 'Virgo', degree: 20.1, nakshatra: 'Hasta', retrograde: true },
];

function signToAngle(sign: string, degree: number): number {
  const signIdx = ZODIAC_SIGNS.indexOf(sign);
  if (signIdx < 0) return 0;
  return (signIdx * 30 + degree) * (Math.PI / 180);
}

export default function PlanetaryPositions({ planets: propPlanets }: PlanetaryPositionsProps) {
  const planets = propPlanets || DEFAULT_PLANETS;
  const [animOffset, setAnimOffset] = useState(0);
  const [hoveredPlanet, setHoveredPlanet] = useState<string | null>(null);

  // Slow orbital animation effect
  useEffect(() => {
    let frame: number;
    let start: number | null = null;

    const animate = (time: number) => {
      if (!start) start = time;
      const elapsed = (time - start) / 1000;
      setAnimOffset(elapsed * 0.02); // very slow rotation for visual effect
      frame = requestAnimationFrame(animate);
    };

    frame = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(frame);
  }, []);

  const CX = 200;
  const CY = 200;
  const ZODIAC_R = 175;
  const PLANET_R = 130;
  const INNER_R = 85;

  const planetPositions = useMemo(() => {
    return planets.map((p) => {
      const baseAngle = signToAngle(p.sign, p.degree);
      // Add subtle animation offset (planets that are not retrograde move slightly forward)
      const offset = p.retrograde ? -animOffset * 0.3 : animOffset * 0.5;
      const angle = baseAngle + offset - Math.PI / 2; // -90 so 0 deg Aries is at top
      const x = CX + PLANET_R * Math.cos(angle);
      const y = CY + PLANET_R * Math.sin(angle);

      // Trail: a few points behind the current position
      const trail = [1, 2, 3].map((i) => {
        const tAngle = angle - i * 0.03 * (p.retrograde ? -1 : 1);
        return {
          x: CX + PLANET_R * Math.cos(tAngle),
          y: CY + PLANET_R * Math.sin(tAngle),
          opacity: 0.4 - i * 0.12,
        };
      });

      return { ...p, x, y, trail };
    });
  }, [planets, animOffset]);

  return (
    <div className="relative inline-block">
      {/* Cosmic glow */}
      <div
        className="absolute inset-0 rounded-full blur-2xl pointer-events-none"
        style={{
          background: 'radial-gradient(circle, rgba(128,0,128,0.3) 0%, rgba(212,175,55,0.15) 50%, transparent 70%)',
          transform: 'scale(1.15)',
        }}
      />

      <svg viewBox="0 0 400 400" className="w-full max-w-[500px] h-auto relative z-10">
        <defs>
          <radialGradient id="zodiac-bg" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#1A0F2E" />
            <stop offset="100%" stopColor="#0F0A1E" />
          </radialGradient>
          <filter id="pp-glow">
            <feGaussianBlur stdDeviation="3" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
          <filter id="pp-planet-glow">
            <feGaussianBlur stdDeviation="2" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        {/* Background circle */}
        <circle cx={CX} cy={CY} r={ZODIAC_R + 10} fill="url(#zodiac-bg)" />

        {/* Outer zodiac ring */}
        <circle cx={CX} cy={CY} r={ZODIAC_R} fill="none" stroke="var(--aged-gold-dim)" strokeWidth={1}  />
        <circle cx={CX} cy={CY} r={ZODIAC_R - 20} fill="none" stroke="var(--aged-gold-dim)" strokeWidth={0.5}  />

        {/* Planet orbit circle */}
        <circle cx={CX} cy={CY} r={PLANET_R} fill="none" stroke="rgba(212,175,55,1)" strokeWidth={0.5} strokeDasharray="4 4" />

        {/* Inner circle */}
        <circle cx={CX} cy={CY} r={INNER_R} fill="none" stroke="rgba(212,175,55,1)" strokeWidth={0.5} />

        {/* Zodiac sign divisions & labels */}
        {ZODIAC_SIGNS.map((sign, idx) => {
          const startAngle = (idx * 30 - 90) * (Math.PI / 180);
          const midAngle = ((idx * 30 + 15) - 90) * (Math.PI / 180);
          const x1 = CX + (ZODIAC_R - 20) * Math.cos(startAngle);
          const y1 = CY + (ZODIAC_R - 20) * Math.sin(startAngle);
          const x2 = CX + ZODIAC_R * Math.cos(startAngle);
          const y2 = CY + ZODIAC_R * Math.sin(startAngle);
          const labelX = CX + (ZODIAC_R - 10) * Math.cos(midAngle);
          const labelY = CY + (ZODIAC_R - 10) * Math.sin(midAngle);

          return (
            <g key={sign}>
              <line x1={x1} y1={y1} x2={x2} y2={y2} stroke="var(--aged-gold-dim)" strokeWidth={0.5}  />
              <text
                x={labelX}
                y={labelY + 4}
                textAnchor="middle"
                fill="var(--aged-gold-dim)"
                fontSize={11}
                
              >
                {ZODIAC_SYMBOLS[sign]}
              </text>
            </g>
          );
        })}

        {/* Center label */}
        <text x={CX} y={CY - 8} textAnchor="middle" fill="var(--aged-gold-dim)" fontSize={10}  fontFamily="var(--font-sacred, Cormorant Garamond, Georgia, serif)">
          Planetary
        </text>
        <text x={CX} y={CY + 6} textAnchor="middle" fill="var(--aged-gold-dim)" fontSize={10} opacity={0.5} fontFamily="var(--font-sacred, Cormorant Garamond, Georgia, serif)">
          Positions
        </text>
        <text x={CX} y={CY + 20} textAnchor="middle" fill="#9B59B6" fontSize={8}  fontFamily="sans-serif">
          Live Sky
        </text>

        {/* Planet trails and dots */}
        {planetPositions.map((p) => {
          const color = PLANET_COLORS[p.name] || 'var(--aged-gold-dim)';
          const isHovered = hoveredPlanet === p.name;

          return (
            <g key={p.name}>
              {/* Trail */}
              {p.trail.map((t, i) => (
                <circle
                  key={i}
                  cx={t.x}
                  cy={t.y}
                  r={3 - i * 0.5}
                  fill={color}
                  opacity={t.opacity}
                />
              ))}

              {/* Planet dot */}
              <g
                style={{ cursor: 'pointer' }}
                onMouseEnter={() => setHoveredPlanet(p.name)}
                onMouseLeave={() => setHoveredPlanet(null)}
              >
                <circle
                  cx={p.x}
                  cy={p.y}
                  r={isHovered ? 14 : 10}
                  fill={isHovered ? color : '#0F0A1E'}
                  stroke={color}
                  strokeWidth={2}
                  filter={isHovered ? 'url(#pp-planet-glow)' : undefined}
                  style={{ transition: 'all 0.25s ease' }}
                />
                <text
                  x={p.x}
                  y={p.y + 3.5}
                  textAnchor="middle"
                  fill={isHovered ? '#0F0A1E' : color}
                  fontSize={9}
                  fontWeight="bold"
                  fontFamily="sans-serif"
                  style={{ pointerEvents: 'none', transition: 'fill 0.25s ease' }}
                >
                  {PLANET_SYMBOLS[p.name] || p.name.slice(0, 2)}
                </text>

                {/* Retrograde indicator */}
                {p.retrograde && (
                  <text
                    x={p.x + (isHovered ? 16 : 12)}
                    y={p.y - 4}
                    fill="#EF4444"
                    fontSize={8}
                    fontWeight="bold"
                    style={{ pointerEvents: 'none' }}
                  >
                    R
                  </text>
                )}
              </g>
            </g>
          );
        })}
      </svg>

      {/* Tooltip */}
      {hoveredPlanet && (() => {
        const p = planetPositions.find((pp) => pp.name === hoveredPlanet);
        if (!p) return null;
        const color = PLANET_COLORS[p.name] || 'var(--aged-gold-dim)';

        return (
          <div
            className="absolute z-50 pointer-events-none"
            style={{
              left: '50%',
              bottom: 8,
              transform: 'translateX(-50%)',
            }}
          >
            <div className="bg-cosmic-bg backdrop-blur-sm border border-sacred-gold rounded-lg px-4 py-2.5 shadow-lg whitespace-nowrap">
              <div className="flex items-center gap-2 mb-1">
                <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: color }} />
                <span className="font-display font-bold text-sacred-gold text-sm">{p.name}</span>
                {p.retrograde && <span className="text-xs text-red-400 font-bold">Retrograde</span>}
              </div>
              <div className="text-xs text-cosmic-text">
                {ZODIAC_SYMBOLS[p.sign]} {p.sign} {p.degree.toFixed(1)}&deg;
              </div>
              <div className="text-xs text-cosmic-text">Nakshatra: {p.nakshatra}</div>
            </div>
          </div>
        );
      })()}
    </div>
  );
}
