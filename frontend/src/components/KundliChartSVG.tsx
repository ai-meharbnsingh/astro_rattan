/**
 * KundliChartSVG — Live North Indian Kundli Chart (Diamond-in-Square)
 *
 * Shows house numbers + planets only (no "Asc" label).
 * Live ascendant degree marker ticks every second.
 */
import { useState, useEffect } from 'react';

interface PlanetEntry {
  planet: string;
  sign: string;
  house: number;
  sign_degree: number;
  is_retrograde: boolean;
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

const PLANET_COLORS: Record<string, string> = {
  Sun: '#E65100', Moon: '#546E7A', Mars: '#C62828', Mercury: '#2E7D32',
  Jupiter: '#F9A825', Venus: '#AD1457', Saturn: '#1565C0', Rahu: '#6A1B9A', Ketu: '#78909C',
};

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
  return {
    x: M + (E - 5 - M) * t,
    y: (S + 5) + (M - S - 5) * t,
  };
}

export default function KundliChartSVG({ planets, ascendantDegree, className }: KundliChartSVGProps) {
  const [tick, setTick] = useState(0);

  useEffect(() => {
    const id = setInterval(() => setTick(t => t + 1), 1000);
    return () => clearInterval(id);
  }, []);

  const baseDeg = ascendantDegree ?? 0;
  const liveDeg = (baseDeg + tick * 0.004167) % 360;
  const degInSign = liveDeg % 30;
  const marker = ascMarkerPos(degInSign);

  const planetsByHouse: Record<number, PlanetEntry[]> = {};
  for (const p of planets) {
    if (p.house >= 1 && p.house <= 12) {
      if (!planetsByHouse[p.house]) planetsByHouse[p.house] = [];
      planetsByHouse[p.house].push(p);
    }
  }

  return (
    <svg
      viewBox="0 0 400 400"
      xmlns="http://www.w3.org/2000/svg"
      className={`text-sacred-gold/25 ${className || ''}`}
      style={{ width: '100%', height: '100%' }}
    >
      {/* Outer double border */}
      <rect x={S} y={S} width={E - S} height={E - S} fill="none" stroke={LINE_COLOR} strokeWidth="2.5" />
      <rect x={S + 5} y={S + 5} width={E - S - 10} height={E - S - 10} fill="none" stroke={LINE_COLOR} strokeWidth="1" />

      {/* Inner diamond */}
      <polygon points={`${M},${S + 5} ${E - 5},${M} ${M},${E - 5} ${S + 5},${M}`} fill="none" stroke={LINE_COLOR} strokeWidth="1.5" />

      {/* Corner diagonals */}
      <line x1={S + 5} y1={S + 5} x2={M} y2={M} stroke={LINE_COLOR} strokeWidth="0.8" />
      <line x1={E - 5} y1={S + 5} x2={M} y2={M} stroke={LINE_COLOR} strokeWidth="0.8" />
      <line x1={S + 5} y1={E - 5} x2={M} y2={M} stroke={LINE_COLOR} strokeWidth="0.8" />
      <line x1={E - 5} y1={E - 5} x2={M} y2={M} stroke={LINE_COLOR} strokeWidth="0.8" />

      {/* Live ascendant marker — pulses */}
      <circle cx={marker.x} cy={marker.y} r={4} fill="#FF9933" opacity={0.8 + 0.2 * Math.sin(tick * 0.5)}>
        <animate attributeName="r" values="3;5;3" dur="2s" repeatCount="indefinite" />
      </circle>
      <text x={marker.x + 8} y={marker.y - 2} fontSize="7" fontFamily="monospace" fontWeight="600" fill="#FF9933" opacity="0.7">
        {liveDeg.toFixed(2)}°
      </text>

      {/* House numbers */}
      {HOUSE_NUMBER_POS.map((pos, i) => (
        <text key={`h-${i}`} x={pos.x} y={pos.y} textAnchor="middle" dominantBaseline="central"
          fontSize="9" fill="currentColor" fontFamily="sans-serif" opacity="0.5" className="text-foreground/30">
          {i + 1}
        </text>
      ))}

      {/* Planets */}
      {Array.from({ length: 12 }, (_, i) => i + 1).map((house) => {
        const hp = planetsByHouse[house] || [];
        if (!hp.length) return null;
        const c = HOUSE_CENTERS[house - 1];
        const lh = hp.length > 3 ? 12 : 14;
        const sy = c.y - ((hp.length - 1) * lh) / 2;
        return hp.map((p, pi) => {
          const abbr = PLANET_ABBR[p.planet] || p.planet.slice(0, 2);
          const color = PLANET_COLORS[p.planet] || '#4B5563';
          return (
            <text key={`p-${house}-${pi}`} x={c.x} y={sy + pi * lh} textAnchor="middle"
              dominantBaseline="central" fontSize="11" fontWeight="600" fontFamily="sans-serif" fill={color}>
              {p.is_retrograde ? <><tspan fill={color}>{abbr}</tspan><tspan fill="#DC2626" fontSize="8">(R)</tspan></> : abbr}
            </text>
          );
        });
      })}
    </svg>
  );
}
