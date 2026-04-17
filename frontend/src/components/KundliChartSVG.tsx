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
  language?: string;
}

const PLANET_ABBR: Record<string, string> = {
  Sun: 'Su', Moon: 'Mo', Mars: 'Ma', Mercury: 'Me',
  Jupiter: 'Ju', Venus: 'Ve', Saturn: 'Sa', Rahu: 'Ra', Ketu: 'Ke',
};

const PLANET_ABBR_HI: Record<string, string> = {
  Sun: 'सू', Moon: 'चं', Mars: 'मं', Mercury: 'बु',
  Jupiter: 'गु', Venus: 'शु', Saturn: 'श', Rahu: 'रा', Ketu: 'के',
};

const GOLD_MED = '#C4611F';
const DARK = '#1a1a2e';
const GOLD = '#8B4513';
const MALEFIC = new Set(['Sun', 'Mars', 'Saturn', 'Rahu', 'Ketu']);

// Zodiac sign images — same orange images as transit wheel
const SIGN_IMAGES = [
  '/images/zodiac-orange/zodiac-aries-orange.png',
  '/images/zodiac-orange/zodiac-taurus-orange.png',
  '/images/zodiac-orange/zodiac-gemini-orange.png',
  '/images/zodiac-orange/zodiac-cancer-orange.png',
  '/images/zodiac-orange/zodiac-leo-orange.png',
  '/images/zodiac-orange/zodiac-virgo-orange.png',
  '/images/zodiac-orange/zodiac-libra-orange.png',
  '/images/zodiac-orange/zodiac-scorpio-orange.png',
  '/images/zodiac-orange/zodiac-sagittarius-orange.png',
  '/images/zodiac-orange/zodiac-capricorn-orange.png',
  '/images/zodiac-orange/zodiac-aquarius-orange.png',
  '/images/zodiac-orange/zodiac-pisces-orange.png',
];

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

// Sign-indexed planet centers (index 0 = Aries position, 1 = Taurus position, etc.)
// Signs are fixed in North Indian chart; only the HOUSE NUMBER rotates with lagna.
const SIGN_CENTERS: { x: number; y: number }[] = [
  { x: pct(50),   y: pct(28) },    // 0  Aries       — top diamond
  { x: pct(28),   y: pct(14) },    // 1  Taurus      — top-left corner
  { x: pct(15),   y: pct(28) },    // 2  Gemini      — left-upper
  { x: pct(28),   y: pct(50) },    // 3  Cancer      — left diamond
  { x: pct(15),   y: pct(72) },    // 4  Leo         — left-lower
  { x: pct(28),   y: pct(86) },    // 5  Virgo       — bottom-left corner
  { x: pct(50),   y: pct(72) },    // 6  Libra       — bottom diamond
  { x: pct(72),   y: pct(86) },    // 7  Scorpio     — bottom-right corner
  { x: pct(87.5), y: pct(72) },    // 8  Sagittarius — right-lower
  { x: pct(72),   y: pct(50) },    // 9  Capricorn   — right diamond
  { x: pct(87.5), y: pct(28) },    // 10 Aquarius    — right-upper
  { x: pct(72),   y: pct(14) },    // 11 Pisces      — top-right corner
];

// House-number label positions (indexed by SIGN position, not house number)
const HOUSE_NUM_POS: { x: number; y: number }[] = [
  { x: pct(50),   y: pct(45) },    // Aries       pos
  { x: pct(12),   y: pct(8) },     // Taurus      pos
  { x: pct(8),    y: pct(12) },    // Gemini      pos
  { x: pct(45),   y: pct(50) },    // Cancer      pos
  { x: pct(8),    y: pct(88) },    // Leo         pos
  { x: pct(12),   y: pct(92) },    // Virgo       pos
  { x: pct(50),   y: pct(55) },    // Libra       pos
  { x: pct(88),   y: pct(92) },    // Scorpio     pos
  { x: pct(92),   y: pct(88) },    // Sagittarius pos
  { x: pct(55),   y: pct(50) },    // Capricorn   pos
  { x: pct(92),   y: pct(12) },    // Aquarius    pos
  { x: pct(88),   y: pct(8) },     // Pisces      pos
];

function ascMarkerPos(degInSign: number): { x: number; y: number } {
  const t = Math.min(1, Math.max(0, degInSign / 30)) * 0.15;
  return { x: M + (EI - M) * t, y: SI + (M - SI) * t };
}

// North Indian: each position is a fixed sign. Position 0=Aries, 1=Taurus...
// The HOUSE number at position i = ((i - lagnaSignIndex + 12) % 12) + 1
const SIGNS_ORDER = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces'];

// North Indian position layout (clockwise from top):
// pos 0=top(Aries), 1=top-right-corner, 2=right-upper, 3=right(Cancer),
// 4=right-lower, 5=bottom-right-corner, 6=bottom(Libra), 7=bottom-left-corner,
// 8=left-lower, 9=left(Capricorn), 10=left-upper, 11=top-left-corner
//
// But our HOUSE_NUM_POS and HOUSE_CENTERS use house-based indexing:
// index 0 = house 1 (top), index 1 = house 2 (top-left), etc.
//
// In North Indian, sign positions go: top=Aries, then COUNTER-CLOCKWISE:
// top-left=Taurus, left-upper=Gemini, left=Cancer, left-lower=Leo,
// bottom-left=Virgo, bottom=Libra, bottom-right=Scorpio, right-lower=Sag,
// right=Capricorn, right-upper=Aquarius, top-right=Pisces
const SIGN_AT_POSITION = [
  'Aries',       // pos 0 = top diamond
  'Taurus',      // pos 1 = top-left corner
  'Gemini',      // pos 2 = left-upper
  'Cancer',      // pos 3 = left diamond
  'Leo',         // pos 4 = left-lower
  'Virgo',       // pos 5 = bottom-left corner
  'Libra',       // pos 6 = bottom diamond
  'Scorpio',     // pos 7 = bottom-right corner
  'Sagittarius', // pos 8 = right-lower
  'Capricorn',   // pos 9 = right diamond
  'Aquarius',    // pos 10 = right-upper
  'Pisces',      // pos 11 = top-right corner
];

export default function KundliChartSVG({ planets, ascendantSign, ascendantDegree, className, language = 'en' }: KundliChartSVGProps) {
  const isHi = language === 'hi';
  const [tick, setTick] = useState(0);
  useEffect(() => {
    const id = setInterval(() => setTick(t => t + 1), 1000);
    return () => clearInterval(id);
  }, []);

  const baseDeg = ascendantDegree ?? 0;
  const liveDeg = (baseDeg + tick * 0.004167) % 360;
  const marker = ascMarkerPos(liveDeg % 30);

  // Lagna sign index (0=Aries, 1=Taurus, ..., 11=Pisces). -1 if unknown.
  const lagnaSignIdx = SIGNS_ORDER.indexOf(ascendantSign);

  // Group planets by their SIGN POSITION (0-11) so they render at the fixed
  // sign positions on the North Indian chart. The HOUSE NUMBER is derived
  // from the offset between sign position and lagna position.
  const planetsBySignPos: Record<number, PlanetEntry[]> = {};
  for (const pl of planets) {
    const signIdx = SIGNS_ORDER.indexOf(pl.sign);
    if (signIdx < 0) continue;
    if (!planetsBySignPos[signIdx]) planetsBySignPos[signIdx] = [];
    planetsBySignPos[signIdx].push(pl);
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

      {/* Zodiac sign images — orange, low opacity, at fixed sign positions */}
      {[
        { x: pct(50),   y: pct(28) },   // Aries — top diamond
        { x: pct(28),   y: pct(14) },   // Taurus — top-left corner
        { x: pct(12.5), y: pct(28) },   // Gemini — left-upper
        { x: pct(28),   y: pct(50) },   // Cancer — left diamond
        { x: pct(12.5), y: pct(72) },   // Leo — left-lower
        { x: pct(28),   y: pct(86) },   // Virgo — bottom-left corner
        { x: pct(50),   y: pct(72) },   // Libra — bottom diamond
        { x: pct(72),   y: pct(86) },   // Scorpio — bottom-right corner
        { x: pct(87.5), y: pct(72) },   // Sagittarius — right-lower
        { x: pct(72),   y: pct(50) },   // Capricorn — right diamond
        { x: pct(87.5), y: pct(28) },   // Aquarius — right-upper
        { x: pct(72),   y: pct(14) },   // Pisces — top-right corner
      ].map((pos, i) => {
        const imgSize = 40;
        return (
          <image key={`sign-img-${i}`}
            href={SIGN_IMAGES[i]}
            x={pos.x - imgSize / 2} y={pos.y - imgSize / 2}
            width={imgSize} height={imgSize}
            opacity="0.15"
          />
        );
      })}

      {/* House numbers — rotate with lagna. House 1 always sits at the lagna sign. */}
      {HOUSE_NUM_POS.map((pos, i) => {
        // Position i corresponds to sign index i in SIGNS_ORDER.
        // House at this sign = ((signIdx - lagnaSignIdx + 12) % 12) + 1
        const houseNum = lagnaSignIdx >= 0
          ? ((i - lagnaSignIdx + 12) % 12) + 1
          : i + 1;
        return (
          <text key={`h-${i}`} x={pos.x} y={pos.y} textAnchor="middle" dominantBaseline="central"
            fontSize="10" fontWeight="600" fill={GOLD} opacity="0.45" fontFamily="'Inter',sans-serif">
            {houseNum}
          </text>
        );
      })}

      {/* Planets — placed at their sign position (fixed on chart), font 13px/800 */}
      {Array.from({ length: 12 }, (_, i) => i).map((signIdx) => {
        const hp = planetsBySignPos[signIdx] || [];
        if (!hp.length) return null;
        const c = SIGN_CENTERS[signIdx];
        const count = hp.length;
        const lineH = count > 4 ? 13 : count > 3 ? 14 : 16;
        const startY = c.y - ((count - 1) * lineH) / 2;

        return hp.map((pl, pi) => {
          const abbr = isHi ? (PLANET_ABBR_HI[pl.planet] || pl.planet.slice(0, 2)) : (PLANET_ABBR[pl.planet] || pl.planet.slice(0, 2));
          const suffix = statusSuffix(pl);
          const color = planetColor(pl);

          return (
            <g key={`p-${signIdx}-${pi}`}>
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

    </svg>
  );
}
