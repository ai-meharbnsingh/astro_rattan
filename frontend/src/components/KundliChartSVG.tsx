/**
 * KundliChartSVG — Live North Indian Kundli Chart
 *
 * ALL positions as percentages. Font matches transit wheel (13px/800).
 * Symbols: * Retro, ^ Combust, + Vargottama
 * Colors: green=exalted, red=debilitated, GOLD_MED=benefic, DARK=malefic
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

const GOLD_MED = '#C4611F';
const DARK = '#1a1a2e';
const GOLD = '#8B4513';
const MALEFIC = new Set(['Sun', 'Mars', 'Saturn', 'Rahu', 'Ketu']);

function planetColor(p: PlanetEntry): string {
  if (p.is_exalted) return '#059669';
  if (p.is_debilitated) return '#DC2626';
  return MALEFIC.has(p.planet) ? DARK : GOLD_MED;
}

function statusSuffix(p: PlanetEntry): string {
  let s = '';
  if (p.is_retrograde) s += '*';
  if (p.is_combust) s += '^';
  if (p.is_vargottama) s += '+';
  return s;
}

const BOX = 400;
const pct = (v: number) => (v / 100) * BOX;

const S = pct(5);
const E = pct(95);
const M = pct(50);
const SI = pct(6);
const EI = pct(94);

// Planet centers — DEEP inside each house, away from all lines
const HOUSE_CENTERS: { x: number; y: number }[] = [
  { x: pct(50), y: pct(15) },  // 1  — top diamond (high up, clear of center)
  { x: pct(18), y: pct(13) },  // 2  — top-left triangle
  { x: pct(10), y: pct(27) },  // 3  — left-top triangle
  { x: pct(15), y: pct(50) },  // 4  — left diamond (far left, clear of center)
  { x: pct(10), y: pct(73) },  // 5  — left-bottom triangle
  { x: pct(18), y: pct(87) },  // 6  — bottom-left triangle
  { x: pct(50), y: pct(85) },  // 7  — bottom diamond (low, clear of center)
  { x: pct(82), y: pct(87) },  // 8  — bottom-right triangle
  { x: pct(90), y: pct(73) },  // 9  — right-bottom triangle
  { x: pct(85), y: pct(50) },  // 10 — right diamond (far right, clear of center)
  { x: pct(90), y: pct(27) },  // 11 — right-top triangle
  { x: pct(82), y: pct(13) },  // 12 — top-right triangle
];

// House numbers — reference image positions
const HOUSE_NUM_POS: { x: number; y: number }[] = [
  { x: pct(50),   y: pct(45) },    // 1
  { x: pct(28.75),y: pct(22.5) },  // 2
  { x: pct(22.5), y: pct(28.75) }, // 3
  { x: pct(45),   y: pct(50) },    // 4
  { x: pct(22.5), y: pct(71.25) }, // 5
  { x: pct(28.75),y: pct(77.5) },  // 6
  { x: pct(50),   y: pct(55) },    // 7
  { x: pct(71.25),y: pct(77.5) },  // 8
  { x: pct(77.5), y: pct(71.25) }, // 9
  { x: pct(55),   y: pct(50) },    // 10
  { x: pct(77.5), y: pct(28.75) }, // 11
  { x: pct(70),   y: pct(22.5) },  // 12
];

function ascMarkerPos(degInSign: number): { x: number; y: number } {
  const t = Math.min(1, Math.max(0, degInSign / 30)) * 0.15;
  return { x: M + (EI - M) * t, y: SI + (M - SI) * t };
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
  for (const pl of planets) {
    if (pl.house >= 1 && pl.house <= 12) {
      if (!planetsByHouse[pl.house]) planetsByHouse[pl.house] = [];
      planetsByHouse[pl.house].push(pl);
    }
  }

  return (
    <svg viewBox={`0 0 ${BOX} ${BOX}`} xmlns="http://www.w3.org/2000/svg"
      className={className || ''} style={{ width: '100%', height: '100%' }}>

      {/* Outer double border */}
      <rect x={S} y={S} width={E-S} height={E-S} fill="none" stroke={GOLD} strokeWidth="2" opacity="0.4" />
      <rect x={SI} y={SI} width={EI-SI} height={EI-SI} fill="none" stroke={GOLD} strokeWidth="0.8" opacity="0.3" />

      {/* Inner diamond */}
      <polygon points={`${M},${SI} ${EI},${M} ${M},${EI} ${SI},${M}`} fill="none" stroke={GOLD} strokeWidth="1.2" opacity="0.4" />

      {/* Corner-to-center diagonals */}
      <line x1={SI} y1={SI} x2={M} y2={M} stroke={GOLD} strokeWidth="0.6" opacity="0.3" />
      <line x1={EI} y1={SI} x2={M} y2={M} stroke={GOLD} strokeWidth="0.6" opacity="0.3" />
      <line x1={SI} y1={EI} x2={M} y2={M} stroke={GOLD} strokeWidth="0.6" opacity="0.3" />
      <line x1={EI} y1={EI} x2={M} y2={M} stroke={GOLD} strokeWidth="0.6" opacity="0.3" />

      {/* ASC dot */}
      <circle cx={marker.x} cy={marker.y} r={3} fill={GOLD_MED} opacity={0.7}>
        <animate attributeName="r" values="2;4;2" dur="2s" repeatCount="indefinite" />
      </circle>

      {/* House numbers */}
      {HOUSE_NUM_POS.map((pos, i) => (
        <text key={`h-${i}`} x={pos.x} y={pos.y} textAnchor="middle" dominantBaseline="central"
          fontSize="10" fontWeight="600" fill={GOLD} opacity="0.45" fontFamily="'Inter',sans-serif">
          {i + 1}
        </text>
      ))}

      {/* Planets — font 13px/800 matching transit wheel */}
      {Array.from({ length: 12 }, (_, i) => i + 1).map((house) => {
        const hp = planetsByHouse[house] || [];
        if (!hp.length) return null;
        const c = HOUSE_CENTERS[house - 1];
        const count = hp.length;
        const lineH = count > 4 ? 13 : count > 3 ? 14 : 16;
        const startY = c.y - ((count - 1) * lineH) / 2;

        return hp.map((pl, pi) => {
          const abbr = PLANET_ABBR[pl.planet] || pl.planet.slice(0, 2);
          const suffix = statusSuffix(pl);
          const color = planetColor(pl);

          return (
            <g key={`p-${house}-${pi}`}>
              {/* Planet name */}
              <text x={c.x} y={startY + pi * lineH}
                textAnchor="middle" dominantBaseline="central"
                fontSize="13" fontWeight="800" fontFamily="'Inter',sans-serif" fill={color}>
                {abbr}
              </text>
              {/* Status suffix — smaller, right after name */}
              {suffix && (
                <text x={c.x + 16} y={startY + pi * lineH - 2}
                  textAnchor="start" dominantBaseline="central"
                  fontSize="8" fontWeight="700" fontFamily="'Inter',sans-serif" fill={color} opacity="0.8">
                  {suffix}
                </text>
              )}
            </g>
          );
        });
      })}

      {/* Legend */}
      <text x={M} y={pct(98.5)} textAnchor="middle" fontSize="7" fontFamily="'Inter',sans-serif" fill={GOLD} opacity="0.5">
        *Retro  ^Combust  +Vargottama
      </text>
    </svg>
  );
}
