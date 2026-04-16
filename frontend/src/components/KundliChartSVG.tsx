/**
 * KundliChartSVG — Live North Indian Kundli Chart
 *
 * ALL positions defined as percentages (0-100) of box size.
 * Scales perfectly at any resolution.
 * Colors match transit wheel: GOLD_MED(benefic) / DARK(malefic)
 * Symbols: ^Retro  vCombust  +Vargottama
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
  if (p.is_retrograde) s += '^';
  if (p.is_combust) s += 'v';
  if (p.is_vargottama) s += '+';
  return s;
}

// ── ALL POSITIONS AS PERCENTAGES (0-100) ──
// Box = 400x400 viewBox. pct(28.75) = 115px on 400.
// This ensures perfect scaling at ANY size.

const BOX = 400;
const p = (pct: number) => (pct / 100) * BOX; // percentage to pixels

// Outer square edges (5% padding)
const S = p(5);    // 20
const E = p(95);   // 380
const M = p(50);   // 200
// Inner border offset
const SI = p(6);   // 24
const EI = p(94);  // 376

// Planet placement centers (% based)
const HOUSE_CENTERS: { x: number; y: number }[] = [
  { x: p(50), y: p(18) },  // 1  — top diamond
  { x: p(20), y: p(14) },  // 2  — top-left
  { x: p(10), y: p(30) },  // 3  — left-top
  { x: p(20), y: p(50) },  // 4  — left diamond
  { x: p(10), y: p(70) },  // 5  — left-bottom
  { x: p(20), y: p(86) },  // 6  — bottom-left
  { x: p(50), y: p(82) },  // 7  — bottom diamond
  { x: p(80), y: p(86) },  // 8  — bottom-right
  { x: p(90), y: p(70) },  // 9  — right-bottom
  { x: p(80), y: p(50) },  // 10 — right diamond
  { x: p(90), y: p(30) },  // 11 — right-top
  { x: p(80), y: p(14) },  // 12 — top-right
];

// House number positions — from reference image, as percentages
const HOUSE_NUM_POS: { x: number; y: number }[] = [
  { x: p(50),   y: p(45) },    // 1  → center-top
  { x: p(28.75),y: p(22.5) },  // 2  → top-left corner
  { x: p(22.5), y: p(28.75) }, // 3  → left-upper
  { x: p(45),   y: p(50) },    // 4  → center-left
  { x: p(22.5), y: p(71.25) }, // 5  → left-lower
  { x: p(28.75),y: p(77.5) },  // 6  → bottom-left corner
  { x: p(50),   y: p(55) },    // 7  → center-bottom
  { x: p(71.25),y: p(77.5) },  // 8  → bottom-right corner
  { x: p(77.5), y: p(71.25) }, // 9  → right-lower
  { x: p(55),   y: p(50) },    // 10 → center-right
  { x: p(77.5), y: p(28.75) }, // 11 → right-upper
  { x: p(70),   y: p(22.5) },  // 12 → top-right corner
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

      {/* ASC pulsing marker */}
      <circle cx={marker.x} cy={marker.y} r={4} fill={GOLD_MED} opacity={0.8 + 0.2 * Math.sin(tick * 0.5)}>
        <animate attributeName="r" values="3;5;3" dur="2s" repeatCount="indefinite" />
      </circle>
      <text x={marker.x + 8} y={marker.y - 1} fontSize="8" fontFamily="'Inter',sans-serif" fontWeight="700" fill={GOLD_MED} opacity="0.9">
        ASC {liveDeg.toFixed(1)}°
      </text>

      {/* House numbers */}
      {HOUSE_NUM_POS.map((pos, i) => (
        <text key={`h-${i}`} x={pos.x} y={pos.y} textAnchor="middle" dominantBaseline="central"
          fontSize="10" fontWeight="600" fill={GOLD} opacity="0.5" fontFamily="'Inter',sans-serif">
          {i + 1}
        </text>
      ))}

      {/* Planets */}
      {Array.from({ length: 12 }, (_, i) => i + 1).map((house) => {
        const hp = planetsByHouse[house] || [];
        if (!hp.length) return null;
        const c = HOUSE_CENTERS[house - 1];
        const count = hp.length;
        const isDiamond = [1, 4, 7, 10].includes(house);
        const lineH = count > 4 ? 10 : count > 3 ? 11 : isDiamond ? 14 : 12;
        const fSize = count > 4 ? 10 : 12;
        const startY = c.y - ((count - 1) * lineH) / 2;

        return hp.map((pl, pi) => {
          const abbr = PLANET_ABBR[pl.planet] || pl.planet.slice(0, 2);
          const suffix = statusSuffix(pl);
          const color = planetColor(pl);
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

      {/* Legend */}
      <text x={M} y={p(98.5)} textAnchor="middle" fontSize="6.5" fontFamily="'Inter',sans-serif" fill={GOLD} opacity="0.5">
        ^Retro  vCombust  +Vargottama
      </text>
    </svg>
  );
}
