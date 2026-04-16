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

// Planet centers — inside houses, clear of lines AND edges
const HOUSE_CENTERS: { x: number; y: number }[] = [
  { x: pct(50), y: pct(28) },  // 1  — top diamond
  { x: pct(21), y: pct(18) },  // 2  — top-left corner
  { x: pct(18), y: pct(35) },  // 3  — left-upper
  { x: pct(28), y: pct(50) },  // 4  — left diamond
  { x: pct(18), y: pct(65) },  // 5  — left-lower
  { x: pct(28), y: pct(86) },  // 6  — bottom-left corner
  { x: pct(50), y: pct(72) },  // 7  — bottom diamond
  { x: pct(72), y: pct(86) },  // 8  — bottom-right corner
  { x: pct(82), y: pct(65) },  // 9  — right-lower
  { x: pct(72), y: pct(50) },  // 10 — right diamond
  { x: pct(82), y: pct(35) },  // 11 — right-upper
  { x: pct(78), y: pct(18) },  // 12 — top-right corner
];

// House numbers — reference image positions
const HOUSE_NUM_POS: { x: number; y: number }[] = [
  { x: pct(50),   y: pct(45) },    // 1
  { x: pct(10),   y: pct(7) },     // 2
  { x: pct(7),    y: pct(10) },    // 3
  { x: pct(45),   y: pct(50) },    // 4
  { x: pct(22.5), y: pct(71.25) }, // 5
  { x: pct(28),   y: pct(77.5) },  // 6
  { x: pct(50),   y: pct(55) },    // 7
  { x: pct(71.25),y: pct(77.5) },  // 8
  { x: pct(77.5), y: pct(71.25) }, // 9
  { x: pct(55),   y: pct(50) },    // 10
  { x: pct(77.5), y: pct(28) },    // 11
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

      {/* Single outer box */}
      <rect x={S} y={S} width={E-S} height={E-S} fill="none" stroke={GOLD} strokeWidth="1.5" opacity="0.5" />

      {/* Inner diamond — connects midpoints of each side */}
      <polygon points={`${M},${S} ${E},${M} ${M},${E} ${S},${M}`} fill="none" stroke={GOLD} strokeWidth="1" opacity="0.4" />

      {/* Corner-to-center diagonals — equal triangles */}
      <line x1={S} y1={S} x2={M} y2={M} stroke={GOLD} strokeWidth="0.7" opacity="0.35" />
      <line x1={E} y1={S} x2={M} y2={M} stroke={GOLD} strokeWidth="0.7" opacity="0.35" />
      <line x1={S} y1={E} x2={M} y2={M} stroke={GOLD} strokeWidth="0.7" opacity="0.35" />
      <line x1={E} y1={E} x2={M} y2={M} stroke={GOLD} strokeWidth="0.7" opacity="0.35" />

      {/* No ASC dot — degree shown in table only */}

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
