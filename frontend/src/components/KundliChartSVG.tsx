/**
 * KundliChartSVG — Live North Indian Kundli Chart
 *
 * Colors match transit wheel: GOLD_MED(benefic) / DARK(malefic)
 * Symbols: ^Retro  vCombust  +Vargottama
 * Live ASC degree marker ticks every second.
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

// Match transit wheel colors exactly
const GOLD_MED = '#C4611F';  // benefic / exalted
const DARK = '#1a1a2e';      // malefic / debilitated
const GOLD = '#8B4513';      // house numbers, lines

const MALEFIC = new Set(['Sun', 'Mars', 'Saturn', 'Rahu', 'Ketu']);

function planetColor(p: PlanetEntry): string {
  if (p.is_exalted) return '#059669';   // green for exalted
  if (p.is_debilitated) return '#DC2626'; // red for debilitated
  return MALEFIC.has(p.planet) ? DARK : GOLD_MED;
}

function statusSuffix(p: PlanetEntry): string {
  let s = '';
  if (p.is_retrograde) s += '^';
  if (p.is_combust) s += 'v';
  if (p.is_vargottama) s += '+';
  return s;
}

const S = 20, E = 380, M = 200;

// House centers — carefully positioned to avoid overlap
// Diamond houses (1,4,7,10) have more vertical space
// Corner triangle houses (2,3,5,6,8,9,11,12) are tighter
const HOUSE_CENTERS: { x: number; y: number }[] = [
  { x: 200, y: 72 },   // 1  — top diamond
  { x: 82,  y: 55 },   // 2  — top-left triangle
  { x: 40,  y: 120 },  // 3  — left-top triangle
  { x: 82,  y: 200 },  // 4  — left diamond
  { x: 40,  y: 280 },  // 5  — left-bottom triangle
  { x: 82,  y: 345 },  // 6  — bottom-left triangle
  { x: 200, y: 328 },  // 7  — bottom diamond
  { x: 318, y: 345 },  // 8  — bottom-right triangle
  { x: 360, y: 280 },  // 9  — right-bottom triangle
  { x: 318, y: 200 },  // 10 — right diamond
  { x: 360, y: 120 },  // 11 — right-top triangle
  { x: 318, y: 55 },   // 12 — top-right triangle
];

const HOUSE_NUM_POS: { x: number; y: number }[] = [
  { x: 200, y: 34 },  { x: 58,  y: 34 },  { x: 26, y: 105 },
  { x: 58,  y: 168 }, { x: 26,  y: 230 }, { x: 58, y: 300 },
  { x: 200, y: 368 }, { x: 342, y: 300 }, { x: 374, y: 230 },
  { x: 342, y: 168 }, { x: 374, y: 105 }, { x: 342, y: 34 },
];

function ascMarkerPos(degInSign: number): { x: number; y: number } {
  const t = Math.min(1, Math.max(0, degInSign / 30)) * 0.15;
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

  // Group planets by house
  const planetsByHouse: Record<number, PlanetEntry[]> = {};
  for (const p of planets) {
    if (p.house >= 1 && p.house <= 12) {
      if (!planetsByHouse[p.house]) planetsByHouse[p.house] = [];
      planetsByHouse[p.house].push(p);
    }
  }

  return (
    <svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg"
      className={className || ''} style={{ width: '100%', height: '100%' }}>

      {/* Chart lines — match transit wheel stroke style */}
      <rect x={S} y={S} width={E-S} height={E-S} fill="none" stroke={GOLD} strokeWidth="2" opacity="0.4" />
      <rect x={S+4} y={S+4} width={E-S-8} height={E-S-8} fill="none" stroke={GOLD} strokeWidth="0.8" opacity="0.3" />
      <polygon points={`${M},${S+4} ${E-4},${M} ${M},${E-4} ${S+4},${M}`} fill="none" stroke={GOLD} strokeWidth="1.2" opacity="0.4" />
      <line x1={S+4} y1={S+4} x2={M} y2={M} stroke={GOLD} strokeWidth="0.6" opacity="0.3" />
      <line x1={E-4} y1={S+4} x2={M} y2={M} stroke={GOLD} strokeWidth="0.6" opacity="0.3" />
      <line x1={S+4} y1={E-4} x2={M} y2={M} stroke={GOLD} strokeWidth="0.6" opacity="0.3" />
      <line x1={E-4} y1={E-4} x2={M} y2={M} stroke={GOLD} strokeWidth="0.6" opacity="0.3" />

      {/* ASC pulsing marker */}
      <circle cx={marker.x} cy={marker.y} r={4} fill={GOLD_MED} opacity={0.8 + 0.2 * Math.sin(tick * 0.5)}>
        <animate attributeName="r" values="3;5;3" dur="2s" repeatCount="indefinite" />
      </circle>
      <text x={marker.x + 8} y={marker.y - 1} fontSize="8" fontFamily="'Inter',sans-serif" fontWeight="700" fill={GOLD_MED} opacity="0.9">
        ASC {liveDeg.toFixed(1)}°
      </text>

      {/* House numbers — subtle, same as transit wheel */}
      {HOUSE_NUM_POS.map((pos, i) => (
        <text key={`h-${i}`} x={pos.x} y={pos.y} textAnchor="middle" dominantBaseline="central"
          fontSize="10" fontWeight="600" fill={GOLD} opacity="0.5" fontFamily="'Inter',sans-serif">
          {i + 1}
        </text>
      ))}

      {/* Planets — matching transit wheel style: fontSize 13, fontWeight 800 */}
      {Array.from({ length: 12 }, (_, i) => i + 1).map((house) => {
        const hp = planetsByHouse[house] || [];
        if (!hp.length) return null;
        const c = HOUSE_CENTERS[house - 1];

        // Smart layout: spread planets to avoid overlap
        const count = hp.length;
        // For diamond houses (1,4,7,10) — vertical stack
        // For triangle houses — tighter vertical stack with smaller font if crowded
        const isDiamond = [1, 4, 7, 10].includes(house);
        const lineH = count > 4 ? 10 : count > 3 ? 11 : isDiamond ? 14 : 12;
        const fSize = count > 4 ? 10 : 12;
        const startY = c.y - ((count - 1) * lineH) / 2;

        return hp.map((p, pi) => {
          const abbr = PLANET_ABBR[p.planet] || p.planet.slice(0, 2);
          const suffix = statusSuffix(p);
          const color = planetColor(p);
          const label = suffix ? `${abbr}${suffix}` : abbr;

          return (
            <text key={`p-${house}-${pi}`} x={c.x} y={startY + pi * lineH}
              textAnchor="middle" dominantBaseline="central"
              fontSize={fSize} fontWeight="800" fontFamily="'Inter',sans-serif" fill={color}>
              {label}
            </text>
          );
        });
      })}

      {/* Legend — bottom */}
      <text x={M} y={395} textAnchor="middle" fontSize="6.5" fontFamily="'Inter',sans-serif" fill={GOLD} opacity="0.5">
        ^Retro  vCombust  +Vargottama  ●Benefic  ●Malefic
      </text>
    </svg>
  );
}
