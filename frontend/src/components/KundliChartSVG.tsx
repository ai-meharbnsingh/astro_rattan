/**
 * KundliChartSVG — Live North Indian Kundli Chart
 *
 * Symbols:  ^Retro  vCombust  +Vargottama  Exalted(green)  Debilitated(red)
 * Benefic = green planet color, Malefic = red, Neutral = amber
 * ASC marker = pulsing saffron dot on diamond edge
 */
import { useState, useEffect } from 'react';

interface PlanetEntry {
  planet: string;
  sign: string;
  house: number;
  sign_degree: number;
  is_retrograde?: boolean;
  is_combust?: boolean;
  is_vargottama?: boolean;
  is_exalted?: boolean;
  is_debilitated?: boolean;
}

export interface KundliChartSVGProps {
  planets: PlanetEntry[];
  ascendantSign: string;
  ascendantDegree?: number;
  className?: string;
}

const PLANET_ABBR: Record<string, string> = {
  Sun: 'Su', Moon: 'Mo', Mars: 'Ma', Mercury: 'Me',
  Jupiter: 'Ju', Venus: 'Ve', Saturn: 'Sa', Rahu: 'Ra', Ketu: 'Ke',
};

// Benefic = green, Malefic = red, Neutral = amber
const BENEFIC = new Set(['Jupiter', 'Venus', 'Moon', 'Mercury']);
const MALEFIC = new Set(['Sun', 'Mars', 'Saturn', 'Rahu', 'Ketu']);

function planetColor(p: PlanetEntry): string {
  if (p.is_exalted) return '#059669';      // green-600 — exalted
  if (p.is_debilitated) return '#DC2626';  // red-600 — debilitated
  if (BENEFIC.has(p.planet)) return '#16A34A';  // green-600 — benefic
  if (MALEFIC.has(p.planet)) return '#DC2626';  // red-600 — malefic
  return '#D97706'; // amber-600 — neutral
}

// Build suffix symbols: ^Retro vCombust +Vargottama
function statusSymbols(p: PlanetEntry): string {
  let s = '';
  if (p.is_retrograde) s += '^';
  if (p.is_combust) s += 'v';
  if (p.is_vargottama) s += '+';
  return s;
}

const S = 20;
const E = 380;
const M = 200;

const HOUSE_CENTERS: { x: number; y: number }[] = [
  { x: 200, y: 75 },   { x: 88,  y: 58 },   { x: 42,  y: 145 },
  { x: 88,  y: 200 },  { x: 42,  y: 255 },  { x: 88,  y: 342 },
  { x: 200, y: 325 },  { x: 312, y: 342 },  { x: 358, y: 255 },
  { x: 312, y: 200 },  { x: 358, y: 145 },  { x: 312, y: 58 },
];

const HOUSE_NUMBER_POS: { x: number; y: number }[] = [
  { x: 200, y: 36 },   { x: 65,  y: 36 },   { x: 28,  y: 110 },
  { x: 65,  y: 170 },  { x: 28,  y: 225 },  { x: 65,  y: 300 },
  { x: 200, y: 366 },  { x: 335, y: 300 },  { x: 372, y: 225 },
  { x: 335, y: 170 },  { x: 372, y: 110 },  { x: 335, y: 36 },
];

const LINE_COLOR = 'currentColor';

function ascMarkerPos(degInSign: number): { x: number; y: number } {
  const frac = Math.min(1, Math.max(0, degInSign / 30));
  const t = frac * 0.15;
  return { x: M + (E - 5 - M) * t, y: (S + 5) + (M - S - 5) * t };
}

export default function KundliChartSVG({ planets, ascendantDegree, className }: KundliChartSVGProps) {
  const [tick, setTick] = useState(0);
  useEffect(() => {
    const id = setInterval(() => setTick(t => t + 1), 1000);
    return () => clearInterval(id);
  }, []);

  const baseDeg = ascendantDegree ?? 0;
  const liveDeg = (baseDeg + tick * 0.004167) % 360;
  const marker = ascMarkerPos(liveDeg % 30);

  const planetsByHouse: Record<number, PlanetEntry[]> = {};
  for (const p of planets) {
    if (p.house >= 1 && p.house <= 12) {
      if (!planetsByHouse[p.house]) planetsByHouse[p.house] = [];
      planetsByHouse[p.house].push(p);
    }
  }

  return (
    <svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg"
      className={`text-sacred-gold/25 ${className || ''}`} style={{ width: '100%', height: '100%' }}>

      {/* Structure */}
      <rect x={S} y={S} width={E-S} height={E-S} fill="none" stroke={LINE_COLOR} strokeWidth="2.5" />
      <rect x={S+5} y={S+5} width={E-S-10} height={E-S-10} fill="none" stroke={LINE_COLOR} strokeWidth="1" />
      <polygon points={`${M},${S+5} ${E-5},${M} ${M},${E-5} ${S+5},${M}`} fill="none" stroke={LINE_COLOR} strokeWidth="1.5" />
      <line x1={S+5} y1={S+5} x2={M} y2={M} stroke={LINE_COLOR} strokeWidth="0.8" />
      <line x1={E-5} y1={S+5} x2={M} y2={M} stroke={LINE_COLOR} strokeWidth="0.8" />
      <line x1={S+5} y1={E-5} x2={M} y2={M} stroke={LINE_COLOR} strokeWidth="0.8" />
      <line x1={E-5} y1={E-5} x2={M} y2={M} stroke={LINE_COLOR} strokeWidth="0.8" />

      {/* ASC — pulsing marker */}
      <circle cx={marker.x} cy={marker.y} r={4} fill="#FF9933" opacity={0.8 + 0.2 * Math.sin(tick * 0.5)}>
        <animate attributeName="r" values="3;5;3" dur="2s" repeatCount="indefinite" />
      </circle>
      <text x={marker.x + 8} y={marker.y - 2} fontSize="7" fontFamily="monospace" fontWeight="700" fill="#FF9933" opacity="0.8">
        ASC {liveDeg.toFixed(1)}°
      </text>

      {/* House numbers */}
      {HOUSE_NUMBER_POS.map((pos, i) => (
        <text key={`h-${i}`} x={pos.x} y={pos.y} textAnchor="middle" dominantBaseline="central"
          fontSize="9" fill="currentColor" fontFamily="sans-serif" opacity="0.5" className="text-foreground/30">
          {i + 1}
        </text>
      ))}

      {/* Planets with status symbols */}
      {Array.from({ length: 12 }, (_, i) => i + 1).map((house) => {
        const hp = planetsByHouse[house] || [];
        if (!hp.length) return null;
        const c = HOUSE_CENTERS[house - 1];
        const lh = hp.length > 3 ? 11 : 13;
        const sy = c.y - ((hp.length - 1) * lh) / 2;

        return hp.map((p, pi) => {
          const abbr = PLANET_ABBR[p.planet] || p.planet.slice(0, 2);
          const color = planetColor(p);
          const symbols = statusSymbols(p);
          const label = symbols ? `${abbr}${symbols}` : abbr;

          return (
            <text key={`p-${house}-${pi}`} x={c.x} y={sy + pi * lh} textAnchor="middle"
              dominantBaseline="central" fontSize="10" fontWeight="700" fontFamily="sans-serif" fill={color}>
              {label}
            </text>
          );
        });
      })}

      {/* Legend — bottom right corner */}
      <g transform="translate(285, 390)" opacity="0.6">
        <text x="0" y="0" fontSize="6" fontFamily="sans-serif" fill="#059669">^Retro</text>
        <text x="30" y="0" fontSize="6" fontFamily="sans-serif" fill="#DC2626">vCombust</text>
        <text x="65" y="0" fontSize="6" fontFamily="sans-serif" fill="#D97706">+Vargottama</text>
      </g>
    </svg>
  );
}
