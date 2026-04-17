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
  // Optional: if not provided, we derive house from sign + ascendantSign.
  house?: number;
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

// House position centers for North Indian chart (house 1 fixed at the top).
// We rotate signs (not house positions) based on ascendantSign.
const HOUSE_CENTERS: { x: number; y: number }[] = [
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

// Number label positions (indexed by house position 1..12 in the layout).
// We render *rashi* numbers (Aries=1..Pisces=12) that rotate with Lagna,
// matching the main Kundli (InteractiveKundli) North-Indian chart behavior.
const NUMBER_LABEL_POS: { x: number; y: number }[] = [
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

// Zodiac order (index 0=Aries, ..., 11=Pisces)
const SIGNS_ORDER = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces'];

function normalizeSignName(raw: string | null | undefined): string | null {
  if (!raw) return null;
  const s = String(raw).trim().toLowerCase();
  if (!s) return null;
  // Common casing/spacing issues handled here; keep it conservative.
  for (const canon of SIGNS_ORDER) {
    if (canon.toLowerCase() === s) return canon;
  }
  return null;
}

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
  const ascCanon = normalizeSignName(ascendantSign);
  const lagnaSignIdx = ascCanon ? SIGNS_ORDER.indexOf(ascCanon) : -1;

  // Group planets by HOUSE POSITION (0-11) so we render a true North-Indian
  // chart: house positions are fixed; signs rotate based on ascendantSign.
  const planetsByHousePos: Record<number, PlanetEntry[]> = {};
  for (const pl of planets) {
    let houseNum = Number(pl.house || 0);
    if (!(houseNum >= 1 && houseNum <= 12)) {
      const plSignCanon = normalizeSignName(pl.sign);
      const signIdx = plSignCanon ? SIGNS_ORDER.indexOf(plSignCanon) : -1;
      if (signIdx < 0 || lagnaSignIdx < 0) continue;
      houseNum = ((signIdx - lagnaSignIdx + 12) % 12) + 1;
    }
    const posIdx = houseNum - 1;
    if (!planetsByHousePos[posIdx]) planetsByHousePos[posIdx] = [];
    planetsByHousePos[posIdx].push(pl);
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
        // i is the house position (0..11). In a North-Indian house-fixed chart,
        // the sign in house (i+1) is (lagnaSignIdx + i) in zodiac order.
        const signIdx = lagnaSignIdx >= 0 ? (lagnaSignIdx + i) % 12 : i;
        return (
          <image key={`sign-img-${i}`}
            href={SIGN_IMAGES[signIdx]}
            x={pos.x - imgSize / 2} y={pos.y - imgSize / 2}
            width={imgSize} height={imgSize}
            opacity="0.15"
          />
        );
      })}

      {/* Rashi numbers (1..12) — rotate with Lagna (Aries=1..Pisces=12). */}
      {NUMBER_LABEL_POS.map((pos, i) => {
        const signIdx = lagnaSignIdx >= 0 ? (lagnaSignIdx + i) % 12 : i;
        const rashiNum = signIdx + 1;
        return (
          <text
            key={`rashi-${i}`}
            x={pos.x}
            y={pos.y}
            textAnchor="middle"
            dominantBaseline="central"
            fontSize="12"
            fontWeight="700"
            fill={GOLD}
            opacity="0.5"
            fontFamily="'Inter',sans-serif"
          >
            {rashiNum}
          </text>
        );
      })}

      {/* Planets — placed at their HOUSE position (fixed on chart), font 13px/800 */}
      {Array.from({ length: 12 }, (_, i) => i).map((posIdx) => {
        const hp = planetsByHousePos[posIdx] || [];
        if (!hp.length) return null;
        const c = HOUSE_CENTERS[posIdx];
        const count = hp.length;
        const lineH = count > 4 ? 13 : count > 3 ? 14 : 16;
        const startY = c.y - ((count - 1) * lineH) / 2;

        return hp.map((pl, pi) => {
          const abbr = isHi ? (PLANET_ABBR_HI[pl.planet] || pl.planet.slice(0, 2)) : (PLANET_ABBR[pl.planet] || pl.planet.slice(0, 2));
          const suffix = statusSuffix(pl);
          const color = planetColor(pl);

          return (
            <g key={`p-${posIdx}-${pi}`}>
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
