import { useState, useCallback, useMemo } from 'react';
import { useTranslation } from '@/lib/i18n';

// --- Data types ---
export interface PlanetData {
  planet: string;
  sign: string;
  house: number;
  nakshatra: string;
  sign_degree: number;
  status: string;
  is_retrograde?: boolean;
  is_combust?: boolean;
  is_vargottama?: boolean;
}

export interface ChartData {
  planets: PlanetData[];
  houses?: { number: number; sign: string }[];
  ascendant?: { longitude: number; sign: string; sign_degree?: number };
}

interface InteractiveKundliProps {
  chartData: ChartData;
  onPlanetClick?: (planet: PlanetData) => void;
  onHouseClick?: (house: number, sign: string, planets: PlanetData[]) => void;
  compact?: boolean; // Hide North/South toggle, always show North Indian
}

type ChartStyle = 'north' | 'south';

// --- Constants ---
const ZODIAC_SIGNS = [
  'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
  'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces',
];

// Zodiac numbers instead of symbols (1-12)
const ZODIAC_NUMBERS: Record<string, number> = {
  Aries: 1, Taurus: 2, Gemini: 3, Cancer: 4,
  Leo: 5, Virgo: 6, Libra: 7, Scorpio: 8,
  Sagittarius: 9, Capricorn: 10, Aquarius: 11, Pisces: 12,
};

const PLANET_ABBREVIATIONS: Record<string, string> = {
  Sun: 'Su', Moon: 'Mo', Mars: 'Ma', Mercury: 'Me', Jupiter: 'Ju',
  Venus: 'Ve', Saturn: 'Sa', Rahu: 'Ra', Ketu: 'Ke',
  Ascendant: 'La', Lagna: 'La',
  Uranus: 'Ur', Neptune: 'Ne', Pluto: 'Pl',
};

const PLANET_ABBREVIATIONS_HI: Record<string, string> = {
  Sun: 'सू', Moon: 'चं', Mars: 'मं', Mercury: 'बु', Jupiter: 'गु',
  Venus: 'शु', Saturn: 'श', Rahu: 'रा', Ketu: 'के',
  Ascendant: 'ल', Lagna: 'ल',
  Uranus: 'Ur', Neptune: 'Ne', Pluto: 'Pl',
};

const ZODIAC_ABBREVIATIONS: Record<string, string> = {
  Aries: 'Ari', Taurus: 'Tau', Gemini: 'Gem', Cancer: 'Can',
  Leo: 'Leo', Virgo: 'Vir', Libra: 'Lib', Scorpio: 'Sco',
  Sagittarius: 'Sag', Capricorn: 'Cap', Aquarius: 'Aqu', Pisces: 'Pis',
};

const BENEFIC_PLANETS = ['Jupiter', 'Venus', 'Moon', 'Mercury'];
const MALEFIC_PLANETS = ['Saturn', 'Mars', 'Rahu', 'Ketu', 'Sun'];

const HOUSE_SIGNIFICANCE: Record<number, string> = {
  1: 'Self, Personality, Appearance',
  2: 'Wealth, Family, Speech',
  3: 'Courage, Siblings, Communication',
  4: 'Home, Mother, Comfort',
  5: 'Children, Education, Creativity',
  6: 'Health, Enemies, Service',
  7: 'Marriage, Partnership, Business',
  8: 'Longevity, Transformation, Occult',
  9: 'Fortune, Dharma, Higher Learning',
  10: 'Career, Status, Authority',
  11: 'Gains, Aspirations, Friends',
  12: 'Losses, Moksha, Foreign Lands',
};

const PLANET_ASPECTS: Record<string, number[]> = {
  Sun: [7], Moon: [7], Mercury: [7], Venus: [7],
  Mars: [4, 7, 8], Jupiter: [5, 7, 9], Saturn: [3, 7, 10],
  Rahu: [5, 7, 9], Ketu: [5, 7, 9],
};

// JHora-style per-planet colors
const PLANET_COLORS: Record<string, string> = {
  Sun: '#E65100',      // deep orange
  Moon: '#1565C0',     // blue
  Mars: '#C62828',     // red
  Mercury: '#2E7D32',  // green
  Jupiter: '#F9A825',  // golden yellow
  Venus: '#E91E63',    // pink
  Saturn: '#1565C0',   // blue
  Rahu: '#616161',     // grey
  Ketu: '#795548',     // brown
  Ascendant: 'var(--aged-gold-dim)',
  Lagna: 'var(--aged-gold-dim)',
  Uranus: '#00838F',
  Neptune: '#4527A0',
  Pluto: '#37474F',
};

function getPlanetColor(planet: string): string {
  return PLANET_COLORS[planet] || '#3D2B1F';
}

// Build planet label with status symbols (AstroSage style)
// * Retrograde  ^ Combust  □ Vargottama  ↑ Exalted  ↓ Debilitated
function getPlanetLabel(p: PlanetData, lang?: string): string {
  const abbrMap = lang === 'hi' ? PLANET_ABBREVIATIONS_HI : PLANET_ABBREVIATIONS;
  const abbr = abbrMap[p.planet] || PLANET_ABBREVIATIONS[p.planet] || p.planet.slice(0, 2);
  let suffix = '';
  const s = p.status?.toLowerCase() || '';
  if (p.is_retrograde || s.includes('retrograde')) suffix += '*';
  if (p.is_combust || s.includes('combust')) suffix += '^';
  if (p.is_vargottama || s.includes('vargottama')) suffix += '\u25A1';
  if (s.includes('exalted')) suffix += '\u2191';
  if (s.includes('debilitated')) suffix += '\u2193';
  return abbr + suffix;
}

function getStrength(status: string, t?: (k: string) => string): { label: string; color: string } {
  const s = status?.toLowerCase() || '';
  const tr = t || ((k: string) => k);
  if (s.includes('exalted')) return { label: tr('planet.exalted'), color: '#22C55E' };
  if (s.includes('debilitated')) return { label: tr('planet.debilitated'), color: '#EF4444' };
  if (s.includes('own')) return { label: tr('planet.ownSign'), color: '#3B82F6' };
  return { label: status || tr('planet.transiting'), color: '#6B5B4F' };
}

/*
 * South Indian kundli layout -- 4x4 grid with 12 outer cells.
 * 
 * In South Indian charts, House 1 (Lagna) position depends on the ascendant sign.
 * The chart is a fixed 4x4 grid where houses are arranged anti-clockwise.
 * 
 * Standard arrangement (House 1 can be in any of the 4 corner/edge positions):
 *   [12] [ 1] [ 2] [ 3]
 *   [11] [  ] [  ] [ 4]
 *   [10] [  ] [  ] [ 5]
 *   [ 9] [ 8] [ 7] [ 6]
 * 
 * House 1 is at top-center (row 0, col 1), then moving anti-clockwise:
 * 1->2 (left), 2->3 (left-down), 3->4 (down), etc.
 */
const HOUSE_GRID: { house: number; row: number; col: number }[] = [
  { house: 12, row: 0, col: 0 },
  { house: 1,  row: 0, col: 1 },
  { house: 2,  row: 0, col: 2 },
  { house: 3,  row: 0, col: 3 },
  { house: 4,  row: 1, col: 3 },
  { house: 5,  row: 2, col: 3 },
  { house: 6,  row: 3, col: 3 },
  { house: 7,  row: 3, col: 2 },
  { house: 8,  row: 3, col: 1 },
  { house: 9,  row: 3, col: 0 },
  { house: 10, row: 2, col: 0 },
  { house: 11, row: 1, col: 0 },
];

const CELL_SIZE = 100;
const GRID_PADDING = 8;

/*
 * North Indian kundli layout -- diamond (rotated square) inside a square.
 *
 * The outer square has midpoints on each side. Lines connect adjacent midpoints
 * to form an inner diamond. Additional lines from corners to the center of the
 * opposite diamond edge create the 12 triangular house regions.
 *
 * ANTI-CLOCKWISE arrangement:
 *   House 1  = top center (Lagna -- always here)
 *   House 2  = upper-right triangle
 *   House 3  = right-upper triangle
 *   House 4  = right center
 *   House 5  = right-bottom triangle
 *   House 6  = bottom-right triangle
 *   House 7  = bottom center
 *   House 8  = bottom-left triangle
 *   House 9  = left-bottom triangle
 *   House 10 = left center
 *   House 11 = left-upper triangle
 *   House 12 = upper-left triangle
 *
 * Coordinate system: 416x416 viewBox, origin at top-left.
 */
const NI_SIZE = 416;
const NI_PAD = 8;
const NI_INNER = NI_SIZE - NI_PAD * 2; // 400
const NI_HALF = NI_INNER / 2; // 200

// Key points (relative to padding origin)
// Corners of outer square
const TL = { x: NI_PAD, y: NI_PAD };
const TR = { x: NI_PAD + NI_INNER, y: NI_PAD };
const BL = { x: NI_PAD, y: NI_PAD + NI_INNER };
const BR = { x: NI_PAD + NI_INNER, y: NI_PAD + NI_INNER };

// Midpoints of sides (diamond vertices)
const MT = { x: NI_PAD + NI_HALF, y: NI_PAD };           // mid top
const MR = { x: NI_PAD + NI_INNER, y: NI_PAD + NI_HALF }; // mid right
const MB = { x: NI_PAD + NI_HALF, y: NI_PAD + NI_INNER }; // mid bottom
const ML = { x: NI_PAD, y: NI_PAD + NI_HALF };           // mid left

// Center
const CC = { x: NI_PAD + NI_HALF, y: NI_PAD + NI_HALF };

/*
 * Each house is a polygon (triangle or quadrilateral). We store:
 *   - house number
 *   - polygon points as SVG path string
 *   - centroid for placing house number, sign symbol, and planets
 */
interface NorthHouse {
  house: number;
  points: string; // SVG polygon points attribute
  cx: number;     // centroid x
  cy: number;     // centroid y
}

function pts(...coords: { x: number; y: number }[]): string {
  return coords.map((c) => `${c.x},${c.y}`).join(' ');
}

function centroid(...coords: { x: number; y: number }[]): { x: number; y: number } {
  const n = coords.length;
  return {
    x: coords.reduce((s, c) => s + c.x, 0) / n,
    y: coords.reduce((s, c) => s + c.y, 0) / n,
  };
}

const NORTH_HOUSES: NorthHouse[] = (() => {
  // House 1: top center triangle -- MT, CC split into top diamond triangle
  // The top diamond region is the triangle: MT -> CC -> (need to split into two)
  // Actually the standard layout:
  //   - The diamond edges connect MT-MR-MB-ML.
  //   - Lines from each corner (TL, TR, BR, BL) to the CENTER (CC) divide the
  //     corner regions. But the standard North Indian chart draws lines from
  //     corners to the center, AND the diamond edges.
  //
  // The 12 regions:
  //   Top section (above MT-to-MT horizontal through diamond top edge):
  //     House 1:  triangle MT -> CC (via top-right diamond edge direction)
  //               Actually: triangle formed by MT, midpoint-of-MT-MR...
  //
  // Let me use the CORRECT standard layout:
  // Lines drawn:
  //   1) Outer square: TL-TR-BR-BL
  //   2) Diamond: MT-MR-MB-ML
  //   3) Diagonals: TL-BR and TR-BL (these pass through CC)
  //
  // This creates exactly 12 regions:

  // The square is divided by:
  //   - Two diagonals: TL-BR and TR-BL (crossing at CC)
  //   - Four diamond edges: MT-MR, MR-MB, MB-ML, ML-MT
  //
  // This yields 12 triangular/trapezoidal regions.
  // Houses go ANTI-CLOCKWISE: 1(top) → 2(top-left) → 3(left-top) → ... → 12(top-right)

  const houses: NorthHouse[] = [];

  // House 1 (top center): MT, TR-BL line intersection at CC...
  // No -- the diagonals TL-BR and TR-BL both pass through CC.
  // The diamond edges also pass through... no, MT-MR connects midpoints.
  //
  // Let me just define the 12 triangles explicitly:

  // Top quadrant (above horizontal center line, between diamond edges and top border):
  //   House 1:  MT, CC, ... The top diamond region is triangle MT-MR-ML
  //             but that's the entire top half of diamond.
  //
  // OK, I'll use the definitive geometry:
  //
  // The diagonals (TL-BR, TR-BL) divide the square into 4 triangles.
  // Each triangle is then subdivided by a diamond edge into 3 sub-triangles.
  // Wait, each large triangle gets split into 3? No -- 2 sub-regions each
  // from the diamond edge, but with 4 large triangles that's only 8.
  // Actually each large triangle is split into 3 by TWO diamond edges passing
  // through it.
  //
  // Let me just list the 12 triangles by their 3 vertices:
  //
  // TOP large triangle (TL, TR, CC -- wait no, the diagonal TL-BR and TR-BL
  // create 4 triangles with vertices at CC):
  //   Top:    TL, TR, CC
  //   Right:  TR, BR, CC
  //   Bottom: BR, BL, CC
  //   Left:   BL, TL, CC
  //
  // Now each is subdivided by diamond edges:
  //   Top triangle (TL, TR, CC) has MT on segment TL-TR.
  //     Diamond edges from MT go to ML and MR.
  //     ML is on segment TL-BL (left side), MR is on TR-BR (right side).
  //     But within triangle TL-TR-CC, the edge MT-ML exits via TL-CC side?
  //     No: ML is on the left edge of the square, not inside this triangle.
  //
  //     Within triangle TL-TR-CC:
  //       MT is on edge TL-TR.
  //       The diamond edge MT-MR: MR is on edge TR-BR, which is NOT an edge
  //       of this triangle. But the line MT-MR passes through interior.
  //       Similarly MT-ML: ML is on edge TL-BL, NOT an edge of this triangle.
  //       The line MT-ML passes through interior too.
  //
  //     So triangle TL-TR-CC is split by lines MT-MR and MT-ML?
  //     No, only one of those stays inside this triangle region.
  //
  //     Actually MT-MR goes from top-mid to right-mid. In triangle TL-TR-CC,
  //     this line enters at MT (on TL-TR edge) and exits at... where does it
  //     cross edge TR-CC or TL-CC?
  //
  //     TR = (408, 8), CC = (208, 208). The line TR-CC has slope
  //     (208-8)/(208-408) = 200/(-200) = -1. Equation: y - 8 = -(x - 408),
  //     so y = -x + 416.
  //
  //     MT = (208, 8), MR = (408, 208). Line MT-MR: slope = (208-8)/(408-208) = 1.
  //     Equation: y - 8 = (x - 208), so y = x - 200.
  //
  //     Intersection of y = -x + 416 and y = x - 200:
  //     -x + 416 = x - 200 => 616 = 2x => x = 308, y = 108.
  //     So MT-MR crosses TR-CC at (308, 108).
  //
  //     Similarly MT-ML goes from (208, 8) to (8, 208). Slope = (208-8)/(8-208) = -1.
  //     Equation: y - 8 = -(x - 208), so y = -x + 216.
  //     Line TL-CC: TL=(8,8), CC=(208,208). Slope = 1. y - 8 = x - 8, so y = x.
  //     Intersection: -x + 216 = x => 216 = 2x => x = 108, y = 108.
  //     So MT-ML crosses TL-CC at (108, 108).
  //
  // So triangle TL-TR-CC is divided into 3 sub-triangles:
  //   1. TL, MT, (108,108)         -- House 12
  //   2. MT, (308,108), (108,108)  -- House 1
  //   3. (308,108), TR, (108,108)  -- wait, that doesn't work.
  //
  // Let me re-examine. The two cutting lines within triangle TL-TR-CC are:
  //   MT to (108,108)  [portion of MT-ML inside this triangle]
  //   MT to (308,108)  [portion of MT-MR inside this triangle]
  //
  // These two lines emanate from MT and go to points on TL-CC and TR-CC respectively.
  // This creates 3 sub-triangles:
  //   Sub-tri A: TL, MT, P1=(108,108)              -- this is House 12
  //   Sub-tri B: MT, P2=(308,108), P1=(108,108)    -- wait, P1 and P2 are on different
  //              edges. The region between the two cut lines is: MT, P2, CC, P1? No...
  //
  //   Actually the 3 sub-triangles from vertex MT with cuts to P1 and P2:
  //   Sub-tri A: TL, MT, P1         -- between edge TL-MT and cut MT-P1
  //   Sub-tri B: MT, P2, P1         -- between the two cuts (this is wrong, P1 and P2
  //              are not connected by an edge of the original triangle)
  //
  // Hmm, I need to think about this differently. Within triangle TL-TR-CC:
  //   - P1 = (108, 108) is on edge TL-CC
  //   - P2 = (308, 108) is on edge TR-CC
  //   - Both cut lines go to MT on edge TL-TR
  //
  //   The three sub-regions are:
  //   A: polygon TL, MT, P1              (triangle)  -- House 12
  //   B: polygon MT, TR, P2              (triangle)  -- House 2
  //   C: polygon P1, MT, P2 (+ the CC vertex? No, P1-P2 is a straight line cutting
  //      off the bottom. But P1 and P2 are connected to CC via the original edges.)
  //      Actually: polygon MT, P2, CC, P1  -- this is wrong because MT,P2,CC,P1
  //      would include area outside.
  //
  //   No wait: P1 is on TL-CC, P2 is on TR-CC. The region below both cuts (closer to CC)
  //   is: P1, P2, CC. And the region between cut MT-P1 and the left edge TL-P1 is
  //   triangle TL, MT, P1. The region between cut MT-P2 and right edge TR-P2 is
  //   triangle MT, TR, P2. The middle region is quadrilateral P1, MT, P2, CC?
  //   No: from P1, going along cut to MT, then along cut to P2, then along edge P2-CC,
  //   then along edge CC-P1. That's a quadrilateral P1-MT-P2-CC with vertices at
  //   (108,108), (208,8), (308,108), (208,208). But wait, is CC=(208,208) inside
  //   the original triangle TL-TR-CC? Yes, CC is a vertex of it.
  //
  //   So the three sub-regions of triangle TL(8,8)-TR(408,8)-CC(208,208):
  //   A: TL(8,8), MT(208,8), P1(108,108)                    -- House 12
  //   B: MT(208,8), TR(408,8), P2(308,108)                   -- House 2
  //   C: P1(108,108), MT(208,8), P2(308,108), CC(208,208)    -- House 1
  //
  // House 1 is the top-center trapezoid (actually a rhombus/kite). Perfect!
  // This matches the standard North Indian chart where Lagna is the
  // top-center diamond shape.

  // Let me compute all intersection points:
  const P_TL_CC_x_MT_ML = { x: NI_PAD + NI_HALF / 2, y: NI_PAD + NI_HALF / 2 };
  // = (108, 108)
  const P_TR_CC_x_MT_MR = { x: NI_PAD + NI_HALF + NI_HALF / 2, y: NI_PAD + NI_HALF / 2 };
  // = (308, 108)
  const P_TR_CC_x_MR_MB = { x: NI_PAD + NI_HALF + NI_HALF / 2, y: NI_PAD + NI_HALF + NI_HALF / 2 };
  // = (308, 308)
  const P_BL_CC_x_MB_ML = { x: NI_PAD + NI_HALF / 2, y: NI_PAD + NI_HALF + NI_HALF / 2 };
  // = (108, 308)

  // Shorthand aliases:
  const P1 = P_TL_CC_x_MT_ML;  // (108, 108) -- on TL-CC diagonal, where MT-ML crosses
  const P2 = P_TR_CC_x_MT_MR;  // (308, 108) -- on TR-CC diagonal, where MT-MR crosses
  const P3 = P_TR_CC_x_MR_MB;  // (308, 308) -- on TR-CC diagonal (lower), where MR-MB crosses
  // Wait, P_TR_CC is the line from TR to CC. But MR-MB crosses... let me recalc.
  //
  // Actually for the right large triangle (TR, BR, CC):
  //   MR is on edge TR-BR. Diamond edges from MR go to MT and MB.
  //   Line MR-MT: already computed, crosses TR-CC at P2=(308,108).
  //   Line MR-MB: MR=(408,208), MB=(208,408). Slope=(408-208)/(208-408)=-1.
  //     y - 208 = -(x - 408), y = -x + 616.
  //   Line TR-CC: y = -x + 416. Intersection: -x+616 = -x+416 => 616=416, no solution!
  //   These are parallel (both slope -1). So MR-MB does NOT cross TR-CC.
  //
  //   Instead, MR-MB crosses BR-CC.
  //   Line BR-CC: BR=(408,408), CC=(208,208). Slope = (208-408)/(208-408) = 1.
  //     y - 408 = (x - 408), y = x.
  //   Line MR-MB: y = -x + 616. Intersection: x = -x + 616 => 2x = 616 => x = 308, y = 308.
  //   So MR-MB crosses BR-CC at (308, 308).
  //
  // For the right large triangle TR(408,8)-BR(408,408)-CC(208,208):
  //   MR(408,208) is on edge TR-BR.
  //   Cut 1: MR to P2(308,108) -- portion of MR-MT line inside this triangle, hitting TR-CC
  //   Cut 2: MR to (308,308) -- portion of MR-MB line inside this triangle, hitting BR-CC
  //
  //   Sub-regions:
  //   A: TR(408,8), MR(408,208), P2(308,108)           -- House 3 (was 2? Let me check)
  //   B: P2(308,108), MR(408,208), (308,308), CC(208,208) -- House 4 (center-right trapezoid)
  //   C: MR(408,208), BR(408,408), (308,308)            -- House 5

  // Let me recalculate P3 and P4 properly:
  const iP3 = { x: NI_PAD + NI_HALF + NI_HALF / 2, y: NI_PAD + NI_HALF + NI_HALF / 2 };
  // = (308, 308) -- on BR-CC diagonal, where MR-MB crosses

  // For bottom large triangle BR(408,408)-BL(8,408)-CC(208,208):
  //   MB(208,408) is on edge BR-BL.
  //   Line MB-MR: already computed, crosses BR-CC at (308,308).
  //   Line MB-ML: MB=(208,408), ML=(8,208). Slope=(208-408)/(8-208)=(-200)/(-200)=1.
  //     y - 408 = (x - 208), y = x + 200.
  //   Line BL-CC: BL=(8,408), CC=(208,208). Slope=(208-408)/(208-8)=(-200)/(200)=-1.
  //     y - 408 = -(x - 8), y = -x + 416.
  //   Intersection: x + 200 = -x + 416 => 2x = 216 => x = 108, y = 308.
  //   So MB-ML crosses BL-CC at (108, 308).

  const iP4 = { x: NI_PAD + NI_HALF / 2, y: NI_PAD + NI_HALF + NI_HALF / 2 };
  // = (108, 308) -- on BL-CC diagonal, where MB-ML crosses

  // For left large triangle BL(8,408)-TL(8,8)-CC(208,208):
  //   ML(8,208) is on edge BL-TL.
  //   Line ML-MB: crosses BL-CC at (108,308) = iP4.
  //   Line ML-MT: crosses TL-CC at (108,108) = P1.
  //
  //   Sub-regions:
  //   A: TL(8,8), ML(8,208), P1(108,108)                    -- House 11
  //   B: P1(108,108), ML(8,208), iP4(108,308), CC(208,208)  -- House 10 (center-left)
  //   C: ML(8,208), BL(8,408), iP4(108,308)                 -- House 9

  // Summary of all 12 houses (ANTI-clockwise from top):
  // Standard North Indian (ANTI-clockwise from House 1 at top):
  //     1  = top center (Lagna)
  //     2  = top-left        (anti-clockwise from 1)
  //     3  = left-top
  //     4  = left center
  //     5  = left-bottom
  //     6  = bottom-left
  //     7  = bottom center
  //     8  = bottom-right
  //     9  = right-bottom
  //     10 = right center
  //     11 = right-top
  //     12 = top-right       (anti-clockwise back to 1)

  // Top large triangle (TL, TR, CC) subdivisions (anti-clockwise):
  //   House 2:  TL, MT, P1           (top-left corner triangle)
  //   House 1:  P1, MT, P2, CC       (top center trapezoid -- Lagna)
  //   House 12: MT, TR, P2           (top-right corner triangle)

  // Right large triangle (TR, BR, CC) subdivisions:
  //   House 11: TR, MR, P2           (right-top corner triangle)
  //   House 10: P2, MR, iP3, CC      (right center trapezoid)
  //   House 9:  MR, BR, iP3          (right-bottom corner triangle)

  // Bottom large triangle (BR, BL, CC) subdivisions:
  //   House 8:  BR, MB, iP3          (bottom-right corner triangle)
  //   House 7:  iP3, MB, iP4, CC     (bottom center trapezoid)
  //   House 6:  MB, BL, iP4          (bottom-left corner triangle)

  // Left large triangle (BL, TL, CC) subdivisions:
  //   House 5:  BL, ML, iP4          (left-bottom corner triangle)
  //   House 4:  iP4, ML, P1, CC      (left center trapezoid)
  //   House 3:  ML, TL, P1           (left-top corner triangle)

  const makeTri = (h: number, a: {x:number;y:number}, b: {x:number;y:number}, c: {x:number;y:number}): NorthHouse => {
    const cen = centroid(a, b, c);
    return { house: h, points: pts(a, b, c), cx: cen.x, cy: cen.y };
  };

  const makeQuad = (h: number, a: {x:number;y:number}, b: {x:number;y:number}, c: {x:number;y:number}, d: {x:number;y:number}): NorthHouse => {
    const cen = centroid(a, b, c, d);
    return { house: h, points: pts(a, b, c, d), cx: cen.x, cy: cen.y };
  };

  /*
   * ANTI-CLOCKWISE arrangement for North Indian Chart
   * House 1 at top center, then anti-clockwise: 1 -> 2 -> 3 -> 4...
   * 
   *   House Positions (Anti-clockwise from House 1):
   *   Top-Left:     House 2
   *   Top-Center:   House 1 (Lagna)
   *   Top-Right:    House 12
   *   Right-Top:    House 11
   *   Right-Center: House 10
   *   Right-Bottom: House 9
   *   Bottom-Right: House 8
   *   Bottom-Center:House 7
   *   Bottom-Left:  House 6
   *   Left-Bottom:  House 5
   *   Left-Center:  House 4
   *   Left-Top:     House 3
   */

  // TOP row (left to right: 2, 1, 12) — anti-clockwise from Lagna
  houses.push(makeTri(2, TL, MT, P1));       // Top-left triangle
  houses.push(makeQuad(1, P1, MT, P2, CC));  // Top-center (Lagna)
  houses.push(makeTri(12, MT, TR, P2));      // Top-right triangle

  // RIGHT side (top to bottom: 11, 10, 9)
  houses.push(makeTri(11, TR, MR, P2));          // Right-top triangle
  houses.push(makeQuad(10, P2, MR, iP3, CC));   // Right-center
  houses.push(makeTri(9, MR, BR, iP3));          // Right-bottom triangle

  // BOTTOM row (right to left: 8, 7, 6)
  houses.push(makeTri(8, BR, MB, iP3));          // Bottom-right triangle
  houses.push(makeQuad(7, iP3, MB, iP4, CC));   // Bottom-center
  houses.push(makeTri(6, MB, BL, iP4));          // Bottom-left triangle

  // LEFT side (bottom to top: 5, 4, 3)
  houses.push(makeTri(5, BL, ML, iP4));          // Left-bottom triangle
  houses.push(makeQuad(4, iP4, ML, P1, CC));     // Left-center
  houses.push(makeTri(3, ML, TL, P1));           // Left-top triangle

  return houses;
})();

// JHora visual constants
const JHORA_BG = '#F5E6B8';       // warm golden background
const JHORA_LINE = '#3D2B1F';      // dark brown lines
const JHORA_LINE_W = 2.2;          // line thickness
const JHORA_CURVE = 28;            // bezier curve inward offset for concave arcs

// Sign name positions for each house — placed at OUTER EDGES near corners/borders
// house -> { x, y } for the sign label
const NORTH_SIGN_POSITIONS: Record<number, { x: number; y: number }> = {
  1:  { x: CC.x,        y: NI_PAD + 16 },              // top center, near top border
  2:  { x: NI_PAD + 24, y: NI_PAD + 16 },              // top-left corner
  12: { x: NI_PAD + NI_INNER - 24, y: NI_PAD + 16 },   // top-right corner
  3:  { x: NI_PAD + 16, y: NI_PAD + NI_HALF / 2 },     // left-top
  4:  { x: NI_PAD + 16, y: CC.y },                      // left center
  5:  { x: NI_PAD + 16, y: NI_PAD + NI_HALF + NI_HALF / 2 }, // left-bottom
  6:  { x: NI_PAD + 24, y: NI_PAD + NI_INNER - 6 },    // bottom-left corner
  7:  { x: CC.x,        y: NI_PAD + NI_INNER - 6 },    // bottom center
  8:  { x: NI_PAD + NI_INNER - 24, y: NI_PAD + NI_INNER - 6 }, // bottom-right corner
  9:  { x: NI_PAD + NI_INNER - 16, y: NI_PAD + NI_HALF + NI_HALF / 2 }, // right-bottom
  10: { x: NI_PAD + NI_INNER - 16, y: CC.y },           // right center
  11: { x: NI_PAD + NI_INNER - 16, y: NI_PAD + NI_HALF / 2 }, // right-top
};


// --- Shared SVG Defs ---
function SvgDefs() {
  return (
    <defs>
      <linearGradient id="kundli-border-grad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="var(--aged-gold-dim)" />
        <stop offset="50%" stopColor="var(--aged-gold-dim)" />
        <stop offset="100%" stopColor="var(--aged-gold-dim)" />
      </linearGradient>
      <filter id="glow">
        <feGaussianBlur stdDeviation="2" result="blur" />
        <feMerge>
          <feMergeNode in="blur" />
          <feMergeNode in="SourceGraphic" />
        </feMerge>
      </filter>
      <filter id="planet-glow">
        <feGaussianBlur stdDeviation="1.5" result="blur" />
        <feMerge>
          <feMergeNode in="blur" />
          <feMergeNode in="SourceGraphic" />
        </feMerge>
      </filter>
    </defs>
  );
}


// --- Planet rendering (shared between both styles) ---
interface PlanetBadgeProps {
  planet: PlanetData;
  px: number;
  py: number;
  hoveredPlanet: string | null;
  setHoveredPlanet: (p: string | null) => void;
  showPlanetTooltip: (p: PlanetData, x: number, y: number) => void;
  hideTooltip: () => void;
  onPlanetClick?: (p: PlanetData) => void;
}

function PlanetBadge({
  planet: p,
  px,
  py,
  hoveredPlanet,
  setHoveredPlanet,
  showPlanetTooltip,
  hideTooltip,
  onPlanetClick,
}: PlanetBadgeProps) {
  const { language: lang } = useTranslation();
  const color = getPlanetColor(p.planet);
  const isHovered = hoveredPlanet === p.planet;
  const label = getPlanetLabel(p, lang);

  return (
    <g
      style={{ cursor: 'pointer' }}
      onMouseEnter={(e) => {
        e.stopPropagation();
        setHoveredPlanet(p.planet);
        const rect = (e.target as SVGElement).closest('svg')?.getBoundingClientRect();
        if (rect) showPlanetTooltip(p, e.clientX - rect.left, e.clientY - rect.top);
      }}
      onMouseLeave={() => {
        setHoveredPlanet(null);
        hideTooltip();
      }}
      onClick={(e) => {
        e.stopPropagation();
        onPlanetClick?.(p);
      }}
    >
      <circle
        cx={px}
        cy={py}
        r={isHovered ? 13 : 11}
        fill={isHovered ? color : 'var(--parchment)'}
        stroke={color}
        strokeWidth={2}
        filter={isHovered ? 'url(#planet-glow)' : undefined}
        style={{ transition: 'all 0.2s ease' }}
      />
      <text
        x={px}
        y={py + 4}
        textAnchor="middle"
        fill={isHovered ? 'var(--parchment)' : color}
        fontSize={13}
        fontWeight="bold"
        fontFamily="var(--font-sacred, Cormorant Garamond, Georgia, serif)"
        style={{ pointerEvents: 'none', transition: 'fill 0.2s ease' }}
      >
        {label}
      </text>
    </g>
  );
}


export default function InteractiveKundli({ chartData, onPlanetClick, onHouseClick, compact }: InteractiveKundliProps) {
  const { t, language } = useTranslation();
  const [hoveredHouse, setHoveredHouse] = useState<number | null>(null);
  const [hoveredPlanet, setHoveredPlanet] = useState<string | null>(null);
  const [tooltip, setTooltip] = useState<{ x: number; y: number; content: React.ReactNode } | null>(null);
  const [chartStyle, setChartStyle] = useState<ChartStyle>('north');

  const planets = chartData.planets || [];

  // Inject Lagna as a pseudo-planet in House 1 if ascendant data is available
  const planetsWithLagna = useMemo(() => {
    const list = [...planets];
    if (chartData.ascendant) {
      const hasLagna = list.some((p) => p.planet === 'Lagna' || p.planet === 'Ascendant');
      if (!hasLagna) {
        list.unshift({
          planet: 'Lagna',
          sign: chartData.ascendant.sign,
          house: 1,
          nakshatra: '',
          sign_degree: chartData.ascendant.sign_degree ?? (chartData.ascendant.longitude % 30),
          status: '',
        });
      }
    }
    return list;
  }, [planets, chartData.ascendant]);

  const planetsByHouse = useMemo(() => {
    const map: Record<number, PlanetData[]> = {};
    for (let i = 1; i <= 12; i++) map[i] = [];
    planetsWithLagna.forEach((p) => {
      const h = p.house || 1;
      if (map[h]) map[h].push(p);
    });
    return map;
  }, [planetsWithLagna]);

  const houseSign = useCallback((house: number): string => {
    if (chartData.houses) {
      const h = chartData.houses.find((hh) => hh.number === house);
      if (h) return h.sign;
    }
    // Fallback: derive from ascendant planet house
    const asc = planets.find((p) => p.planet === 'Ascendant' || p.planet === 'Lagna');
    if (asc) {
      const ascIdx = ZODIAC_SIGNS.indexOf(asc.sign);
      if (ascIdx >= 0) return ZODIAC_SIGNS[(ascIdx + house - 1) % 12];
    }
    return ZODIAC_SIGNS[(house - 1) % 12];
  }, [chartData.houses, planets]);

  const aspectsFor = useCallback((planet: PlanetData): string[] => {
    const aspects = PLANET_ASPECTS[planet.planet] || [7];
    return aspects.map((offset) => {
      const targetHouse = ((planet.house - 1 + offset) % 12) + 1;
      return `House ${targetHouse}`;
    });
  }, []);

  const showPlanetTooltip = useCallback((p: PlanetData, x: number, y: number) => {
    const strength = getStrength(p.status, t);
    const aspects = aspectsFor(p);
    setTooltip({
      x, y,
      content: (
        <div className="space-y-1.5">
          <div className="font-display font-bold text-sacred-gold text-sm">{p.planet}</div>
          <div className="text-xs text-cosmic-text">
            {ZODIAC_NUMBERS[p.sign] || ''} {p.sign} {p.sign_degree?.toFixed(1)}&deg;
          </div>
          <div className="text-xs text-cosmic-text-muted">{t('table.nakshatra')}: {p.nakshatra || 'N/A'}</div>
          <div className="text-xs text-cosmic-text-muted">{t('table.house')}: {p.house}</div>
          <div className="text-xs" style={{ color: strength.color }}>{strength.label}</div>
          <div className="text-xs text-cosmic-text-muted">{t('table.aspects')}: {aspects.join(', ')}</div>
        </div>
      ),
    });
  }, [aspectsFor]);

  const showHouseTooltip = useCallback((house: number, x: number, y: number) => {
    const sign = houseSign(house);
    const housePlanets = planetsByHouse[house] || [];
    setTooltip({
      x, y,
      content: (
        <div className="space-y-1.5">
          <div className="font-display font-bold text-sacred-gold text-sm">
            {t('table.house')} {house}
          </div>
          <div className="text-xs text-cosmic-text-muted">{t(`house.${house}`)}</div>
          {housePlanets.length > 0 && (
            <div className="text-xs text-cosmic-text">
              {t('table.planet')}: {housePlanets.map((p) => p.planet).join(', ')}
            </div>
          )}
        </div>
      ),
    });
  }, [houseSign, planetsByHouse]);

  const hideTooltip = useCallback(() => {
    setTooltip(null);
    setHoveredHouse(null);
    setHoveredPlanet(null);
  }, []);

  // --- South Indian Chart ---
  const renderSouthIndian = () => {
    const svgWidth = CELL_SIZE * 4 + GRID_PADDING * 2;
    const svgHeight = CELL_SIZE * 4 + GRID_PADDING * 2;

    return (
      <svg
        viewBox={`0 0 ${svgWidth} ${svgHeight}`}
        className="relative z-10"
        style={compact
          ? { width: '100%', height: '100%' }
          : { width: '100%', height: 'auto', filter: 'drop-shadow(0 0 12px rgba(212,175,55,0.25))' }
        }
      >
        <SvgDefs />

        {/* Outer gold border */}
        <rect
          x={GRID_PADDING - 2}
          y={GRID_PADDING - 2}
          width={CELL_SIZE * 4 + 4}
          height={CELL_SIZE * 4 + 4}
          rx={6}
          fill="none"
          stroke="url(#kundli-border-grad)"
          strokeWidth={2.5}
          filter="url(#glow)"
        />

        {/* Background fill */}
        <rect
          x={GRID_PADDING}
          y={GRID_PADDING}
          width={CELL_SIZE * 4}
          height={CELL_SIZE * 4}
          rx={4}
          fill="var(--sacred-purple)"
          opacity={0.95}
        />

        {/* Center area label */}
        <text
          x={svgWidth / 2}
          y={svgHeight / 2 - 6}
          textAnchor="middle"
          fill="var(--aged-gold-dim)"
          fontSize={13}
          fontFamily="var(--font-sacred, Cormorant Garamond, Georgia, serif)"
          opacity={0.6}
        >
          {t('chart.rasi')}
        </text>
        <text
          x={svgWidth / 2}
          y={svgHeight / 2 + 10}
          textAnchor="middle"
          fill="var(--aged-gold-dim)"
          fontSize={9}
          fontFamily="var(--font-sacred, Cormorant Garamond, Georgia, serif)"
          opacity={0.4}
        >
          {t('chart.southIndian')}
        </text>

        {/* House cells */}
        {HOUSE_GRID.map(({ house, row, col }) => {
          const x = GRID_PADDING + col * CELL_SIZE;
          const y = GRID_PADDING + row * CELL_SIZE;
          const sign = houseSign(house);
          const isHovered = hoveredHouse === house;
          const housePlanets = planetsByHouse[house] || [];

          return (
            <g
              key={house}
              style={{ cursor: 'pointer' }}
              onMouseEnter={(e) => {
                setHoveredHouse(house);
                const rect = (e.target as SVGElement).closest('svg')?.getBoundingClientRect();
                if (rect) showHouseTooltip(house, e.clientX - rect.left, e.clientY - rect.top);
              }}
              onMouseLeave={hideTooltip}
              onClick={() => onHouseClick?.(house, sign, housePlanets)}
            >
              {/* Cell background */}
              <rect
                x={x + 1}
                y={y + 1}
                width={CELL_SIZE - 2}
                height={CELL_SIZE - 2}
                fill={isHovered ? 'rgba(184,134,11,0.08)' : 'rgba(232,224,212,0.5)'}
                stroke={isHovered ? 'var(--aged-gold-dim)' : 'rgba(184,134,11,0.3)'}
                strokeWidth={isHovered ? 1.5 : 0.5}
                rx={2}
                style={{ transition: 'all 0.2s ease' }}
              />

              {/* House Number - Large */}
              <text
                x={x + CELL_SIZE / 2}
                y={y + CELL_SIZE / 2 + 6}
                textAnchor="middle"
                fill="var(--aged-gold-dim)"
                fontSize={28}
                fontWeight="bold"
                opacity={0.8}
              >
                {house}
              </text>

              {/* Planets in this house */}
              {housePlanets.map((p, idx) => {
                const cols = Math.min(housePlanets.length, 3);
                const pRow = Math.floor(idx / cols);
                const pCol = idx % cols;
                const spacing = CELL_SIZE / (cols + 1);
                const px = x + spacing * (pCol + 1);
                const py = y + 28 + pRow * 22;

                return (
                  <PlanetBadge
                    key={p.planet}
                    planet={p}
                    px={px}
                    py={py}
                    hoveredPlanet={hoveredPlanet}
                    setHoveredPlanet={setHoveredPlanet}
                    showPlanetTooltip={showPlanetTooltip}
                    hideTooltip={hideTooltip}
                    onPlanetClick={onPlanetClick}
                  />
                );
              })}
            </g>
          );
        })}

        {/* Grid lines for inner area */}
        {[1, 2, 3].map((i) => (
          <g key={`grid-${i}`}>
            <line
              x1={GRID_PADDING + i * CELL_SIZE}
              y1={GRID_PADDING}
              x2={GRID_PADDING + i * CELL_SIZE}
              y2={GRID_PADDING + CELL_SIZE * 4}
              stroke="rgba(184,134,11,0.25)"
              strokeWidth={0.5}
            />
            <line
              x1={GRID_PADDING}
              y1={GRID_PADDING + i * CELL_SIZE}
              x2={GRID_PADDING + CELL_SIZE * 4}
              y2={GRID_PADDING + i * CELL_SIZE}
              stroke="rgba(184,134,11,0.25)"
              strokeWidth={0.5}
            />
          </g>
        ))}
      </svg>
    );
  };

  // --- North Indian Chart ---
  const renderNorthIndian = () => {
    const svgSize = NI_SIZE;
    // Curve offset for concave arcs at midpoints
    const cv = JHORA_CURVE;

    // JHora-style outer border with concave curves at midpoints.
    // Each side of the outer square has a concave (inward-dipping) arc
    // where the diamond edge meets the border.
    // We draw the outer border as a path with quadratic bezier curves.
    //
    // Top side: TL -> curve inward at MT -> TR
    //   Control point for top concave arc: (MT.x, MT.y + cv) — pushes midpoint downward
    // Right side: TR -> curve inward at MR -> BR
    //   Control point: (MR.x - cv, MR.y) — pushes midpoint leftward
    // Bottom side: BR -> curve inward at MB -> BL
    //   Control point: (MB.x, MB.y - cv) — pushes midpoint upward
    // Left side: BL -> curve inward at ML -> TL
    //   Control point: (ML.x + cv, ML.y) — pushes midpoint rightward

    const outerPath = [
      `M ${TL.x} ${TL.y}`,
      `Q ${MT.x} ${MT.y + cv} ${TR.x} ${TR.y}`,    // top side: concave arc
      `Q ${MR.x - cv} ${MR.y} ${BR.x} ${BR.y}`,    // right side: concave arc
      `Q ${MB.x} ${MB.y - cv} ${BL.x} ${BL.y}`,    // bottom side: concave arc
      `Q ${ML.x + cv} ${ML.y} ${TL.x} ${TL.y}`,    // left side: concave arc
      'Z',
    ].join(' ');

    // Diamond edges with slight concave curves too (subtler effect)
    const dcv = cv * 0.4; // smaller curve for diamond edges
    // Diamond: MT -> MR -> MB -> ML -> MT
    // Each diamond edge curves slightly inward toward center
    // MT->MR midpoint is at ~(308,108), control goes toward center
    const diamondPath = [
      `M ${MT.x} ${MT.y}`,
      `Q ${(MT.x + MR.x) / 2 - dcv * 0.5} ${(MT.y + MR.y) / 2 + dcv * 0.5} ${MR.x} ${MR.y}`,
      `Q ${(MR.x + MB.x) / 2 - dcv * 0.5} ${(MR.y + MB.y) / 2 - dcv * 0.5} ${MB.x} ${MB.y}`,
      `Q ${(MB.x + ML.x) / 2 + dcv * 0.5} ${(MB.y + ML.y) / 2 - dcv * 0.5} ${ML.x} ${ML.y}`,
      `Q ${(ML.x + MT.x) / 2 + dcv * 0.5} ${(ML.y + MT.y) / 2 + dcv * 0.5} ${MT.x} ${MT.y}`,
      'Z',
    ].join(' ');

    // Center box dimensions
    const cBoxW = 30;
    const cBoxH = 22;

    return (
      <svg
        viewBox={`0 0 ${svgSize} ${svgSize}`}
        className="relative z-10"
        style={compact
          ? { width: '100%', height: '100%' }
          : { width: '100%', height: 'auto', filter: 'drop-shadow(0 2px 8px rgba(61,43,31,0.15))' }
        }
      >
        <SvgDefs />

        {/* Warm golden background fill */}
        <rect
          x={NI_PAD}
          y={NI_PAD}
          width={NI_INNER}
          height={NI_INNER}
          fill={JHORA_BG}
        />

        {/* Outer border with concave curves (JHora signature) */}
        <path
          d={outerPath}
          fill="none"
          stroke={JHORA_LINE}
          strokeWidth={JHORA_LINE_W}
          strokeLinejoin="round"
        />

        {/* Diamond with subtle concave curves */}
        <path
          d={diamondPath}
          fill="none"
          stroke={JHORA_LINE}
          strokeWidth={JHORA_LINE_W}
          strokeLinejoin="round"
        />

        {/* Diagonal lines: TL-BR and TR-BL */}
        <line x1={TL.x} y1={TL.y} x2={BR.x} y2={BR.y} stroke={JHORA_LINE} strokeWidth={JHORA_LINE_W} />
        <line x1={TR.x} y1={TR.y} x2={BL.x} y2={BL.y} stroke={JHORA_LINE} strokeWidth={JHORA_LINE_W} />

        {/* Center rectangular box with 4 dots (JHora style) */}
        <rect
          x={CC.x - cBoxW / 2}
          y={CC.y - cBoxH / 2}
          width={cBoxW}
          height={cBoxH}
          fill={JHORA_BG}
          stroke={JHORA_LINE}
          strokeWidth={1.5}
          rx={2}
        />
        {/* 4 dots inside center box in a 2x2 pattern */}
        <circle cx={CC.x - 6} cy={CC.y - 4} r={2} fill={JHORA_LINE} />
        <circle cx={CC.x + 6} cy={CC.y - 4} r={2} fill={JHORA_LINE} />
        <circle cx={CC.x - 6} cy={CC.y + 4} r={2} fill={JHORA_LINE} />
        <circle cx={CC.x + 6} cy={CC.y + 4} r={2} fill={JHORA_LINE} />

        {/* House regions (interactive polygons) */}
        {NORTH_HOUSES.map((nh) => {
          const sign = houseSign(nh.house);
          const isHovered = hoveredHouse === nh.house;
          const housePlanets = planetsByHouse[nh.house] || [];
          const isTrapezoid = [1, 4, 7, 10].includes(nh.house);
          const signPos = NORTH_SIGN_POSITIONS[nh.house];
          const signAbbr = ZODIAC_ABBREVIATIONS[sign] || sign.slice(0, 3);
          const rashiNum = ZODIAC_NUMBERS[sign] || '';

          // Determine text anchor for sign names based on house position
          let signAnchor: string = 'middle';
          if ([3, 4, 5].includes(nh.house)) signAnchor = 'start';       // left side houses
          if ([9, 10, 11].includes(nh.house)) signAnchor = 'end';       // right side houses

          return (
            <g
              key={nh.house}
              style={{ cursor: 'pointer' }}
              onMouseEnter={(e) => {
                setHoveredHouse(nh.house);
                const rect = (e.target as SVGElement).closest('svg')?.getBoundingClientRect();
                if (rect) showHouseTooltip(nh.house, e.clientX - rect.left, e.clientY - rect.top);
              }}
              onMouseLeave={hideTooltip}
              onClick={() => onHouseClick?.(nh.house, sign, housePlanets)}
            >
              {/* House polygon (hover highlight) */}
              <polygon
                points={nh.points}
                fill={isHovered ? 'rgba(61,43,31,0.06)' : 'transparent'}
                stroke="none"
                style={{ transition: 'fill 0.2s ease' }}
              />

              {/* Sign name hidden — only house numbers shown */}

              {/* Rashi Number inside house */}
              <text
                x={nh.cx}
                y={nh.cy - (housePlanets.length > 0 ? 12 : 0) + 5}
                textAnchor="middle"
                fill={JHORA_LINE}
                fontSize={isTrapezoid ? 20 : 16}
                fontWeight="bold"
                fontFamily="var(--font-sacred, Cormorant Garamond, Georgia, serif)"
                opacity={0.85}
              >
                {rashiNum}
              </text>

              {/* Planets in this house — JHora plain colored text with status symbols */}
              {housePlanets.map((p, idx) => {
                const count = housePlanets.length;
                // Dynamic sizing: scale down for crowded houses
                const maxCols = isTrapezoid
                  ? (count > 4 ? 3 : count > 2 ? 2 : count)
                  : (count > 3 ? 3 : count > 1 ? 2 : 1);
                const cols = Math.min(count, maxCols);
                const pRow = Math.floor(idx / cols);
                const pCol = idx % cols;
                // Tighter spacing for crowded or triangular houses
                const spacing = isTrapezoid
                  ? (count > 4 ? 26 : 32)
                  : (count > 3 ? 22 : count > 2 ? 24 : 28);
                const rowHeight = count > 4 ? 16 : count > 3 ? 18 : 20;
                const fontSize = isTrapezoid
                  ? (count > 4 ? 13 : 15)
                  : (count > 3 ? 12 : count > 2 ? 13 : 14);
                const startX = nh.cx - ((cols - 1) * spacing) / 2;
                const px = startX + pCol * spacing;
                const baseY = nh.cy + (isTrapezoid ? 14 : 8) - (count > 0 ? 2 : 0);
                const py = baseY + pRow * rowHeight;
                const label = getPlanetLabel(p, language);

                return (
                  <g key={p.planet}>
                    {/* Planet abbreviation + status symbols */}
                    <text
                      x={px}
                      y={py}
                      textAnchor="middle"
                      fill={getPlanetColor(p.planet)}
                      fontSize={fontSize}
                      fontWeight="bold"
                      fontFamily="var(--font-sacred, Cormorant Garamond, Georgia, serif)"
                      style={{ cursor: 'pointer' }}
                      onClick={(e) => { e.stopPropagation(); onPlanetClick?.(p); }}
                    >
                      {label}{p.is_retrograde ? 'R' : ''}
                    </text>
                  </g>
                );
              })}
            </g>
          );
        })}
      </svg>
    );
  };

  return (
    <div className={compact ? "relative w-full h-full" : "relative w-full max-w-[800px]"}>
      {/* Chart Style Toggle */}
      {!compact && <div className="flex justify-center gap-1 mb-3 relative z-20">
        <button
          onClick={() => setChartStyle('north')}
          className="px-4 py-1.5 text-xs font-semibold rounded-l-md border transition-all duration-200"
          style={{
            fontFamily: 'var(--font-sacred, Cormorant Garamond, Georgia, serif)',
            background: chartStyle === 'north' ? 'var(--aged-gold-dim)' : 'var(--sacred-purple)',
            color: chartStyle === 'north' ? 'var(--parchment)' : 'var(--ink-light)',
            borderColor: 'var(--aged-gold-dim)',
          }}
        >
          {t('kundli.northIndian')}
        </button>
        <button
          onClick={() => setChartStyle('south')}
          className="px-4 py-1.5 text-xs font-semibold rounded-r-md border transition-all duration-200"
          style={{
            fontFamily: 'var(--font-sacred, Cormorant Garamond, Georgia, serif)',
            background: chartStyle === 'south' ? 'var(--aged-gold-dim)' : 'var(--sacred-purple)',
            color: chartStyle === 'south' ? 'var(--parchment)' : 'var(--ink-light)',
            borderColor: 'var(--aged-gold-dim)',
          }}
        >
          {t('kundli.southIndian')}
        </button>
      </div>}

      {/* Cosmic glow effect behind chart — hidden in compact mode */}
      {!compact && (
        <div
          className="absolute inset-0 rounded-2xl opacity-40 blur-xl pointer-events-none"
          style={{
            background: 'radial-gradient(circle, rgba(212,175,55,0.3) 0%, rgba(128,0,128,0.15) 50%, transparent 70%)',
            transform: 'scale(1.1)',
          }}
        />
      )}

      {chartStyle === 'north' ? renderNorthIndian() : renderSouthIndian()}

      {/* Tooltip overlay */}
      {tooltip && (
        <div
          className="absolute z-50 pointer-events-none"
          style={{
            left: tooltip.x + 12,
            top: tooltip.y - 8,
            maxWidth: 220,
          }}
        >
          <div className="bg-cosmic-bg/95 backdrop-blur-sm border border-sacred-gold/30 rounded-lg p-3 shadow-lg shadow-sacred-gold/10">
            {tooltip.content}
          </div>
        </div>
      )}
    </div>
  );
}

// Legend component for chart status symbols
export function ChartLegend() {
  const { t } = useTranslation();
  return (
    <div className="flex flex-wrap gap-x-4 gap-y-1 justify-center text-xs mt-2 px-2" style={{ color: 'var(--aged-gold)', fontFamily: 'var(--font-sacred, Cormorant Garamond, Georgia, serif)' }}>
      <span><strong>*</strong> {t('planet.retrograde')}</span>
      <span><strong>^</strong> {t('planet.combust')}</span>
      <span><strong>{'\u25A1'}</strong> {t('planet.vargottama')}</span>
      <span><strong>{'\u2191'}</strong> {t('planet.exalted')}</span>
      <span><strong>{'\u2193'}</strong> {t('planet.debilitated')}</span>
    </div>
  );
}
