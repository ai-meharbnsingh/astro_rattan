import { useState, useCallback, useMemo } from 'react';
import { useTranslation } from '@/lib/i18n';
import { pickLang } from '@/components/lalkitab/safe-render';

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
  hideCombust?: boolean; // Lal Kitab context — combustion is Vedic-only, don't render "^"
  /**
   * P1.1 Modified Analytical Tewa — per-planet LK state colour override.
   * When supplied, each planet label is rendered in the state's hexColour
   * instead of the default PLANET_COLORS map. Tooltip shows state label.
   * Map key is planet name (e.g. "Sun", "Mars"). Map value is { hexColour,
   * state, labelEn, labelHi } — the shape emitted by planet-state.ts.
   */
  planetStates?: Record<string, {
    hexColour: string;
    state: string;
    labelEn: string;
    labelHi: string;
    descEn?: string;
    descHi?: string;
  }>;
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

const _ZODIAC_ABBREVIATIONS: Record<string, string> = {
  Aries: 'Ari', Taurus: 'Tau', Gemini: 'Gem', Cancer: 'Can',
  Leo: 'Leo', Virgo: 'Vir', Libra: 'Lib', Scorpio: 'Sco',
  Sagittarius: 'Sag', Capricorn: 'Cap', Aquarius: 'Aqu', Pisces: 'Pis',
};

const _BENEFIC_PLANETS = ['Jupiter', 'Venus', 'Moon', 'Mercury'];
const _MALEFIC_PLANETS = ['Saturn', 'Mars', 'Rahu', 'Ketu', 'Sun'];

const _HOUSE_SIGNIFICANCE: Record<number, string> = {
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

// Build planet label with status symbols (Home kundli style)
// * Retrograde  ^ Combust  v Vargottama  + Exalted  - Debilitated
function getPlanetLabel(p: PlanetData, lang?: string, hideCombust: boolean = false): string {
  const abbrMap = lang === 'hi' ? PLANET_ABBREVIATIONS_HI : PLANET_ABBREVIATIONS;
  const abbr = abbrMap[p.planet] || PLANET_ABBREVIATIONS[p.planet] || p.planet.slice(0, 2);
  let suffix = '';
  // Safely handle bilingual status objects
  const statusStr = typeof p.status === 'string' ? p.status : (p.status ? pickLang(p.status, false) : '');
  const s = statusStr?.toLowerCase() || '';
  if (p.is_retrograde || s.includes('retrograde')) suffix += '*';
  // Lal Kitab does NOT use combustion — callers pass hideCombust=true to suppress.
  if (!hideCombust && (p.is_combust || s.includes('combust'))) suffix += '^';
  if (p.is_vargottama || s.includes('vargottama')) suffix += 'v';
  if (s.includes('exalted')) suffix += '+';
  if (s.includes('debilitated')) suffix += '-';
  return abbr + suffix;
}

function getStrength(status: any, t?: (k: string) => string): { label: string; color: string } {
  // Safely handle bilingual status objects
  const statusStr = typeof status === 'string' ? status : (status ? pickLang(status, false) : '');
  const s = statusStr?.toLowerCase() || '';
  const tr = t || ((k: string) => k);
  if (s.includes('exalted')) return { label: tr('planet.exalted'), color: '#22C55E' };
  if (s.includes('debilitated')) return { label: tr('planet.debilitated'), color: '#EF4444' };
  if (s.includes('own')) return { label: tr('planet.ownSign'), color: '#3B82F6' };
  return { label: statusStr || tr('planet.transiting'), color: '#6B5B4F' };
}

/*
 * South Indian kundli layout -- 4x4 grid with 12 outer cells.
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
const IS_TOUCH_DEVICE = typeof window !== 'undefined' && 'ontouchstart' in window;

/*
 * North Indian kundli layout -- diamond (rotated square) inside a square.
 * Coordinate system: 416x416 viewBox, origin at top-left.
 */
const NI_SIZE = 416;
const NI_PAD = 8;
const NI_INNER = NI_SIZE - NI_PAD * 2; // 400
const NI_HALF = NI_INNER / 2; // 200

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

interface NorthHouse {
  house: number;
  points: string; // SVG polygon points attribute
  cx: number;     // sign number x
  cy: number;     // sign number y
  px: number;     // planet center x
  py: number;     // planet center y
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
  const houses: NorthHouse[] = [];

  // Key intersection points for the 416x416 coordinate system
  const P1 = { x: NI_PAD + NI_HALF / 2, y: NI_PAD + NI_HALF / 2 };               // (108, 108)
  const P2 = { x: NI_PAD + NI_HALF + NI_HALF / 2, y: NI_PAD + NI_HALF / 2 };    // (308, 108)
  const iP3 = { x: NI_PAD + NI_HALF + NI_HALF / 2, y: NI_PAD + NI_HALF + NI_HALF / 2 }; // (308, 308)
  const iP4 = { x: NI_PAD + NI_HALF / 2, y: NI_PAD + NI_HALF + NI_HALF / 2 };   // (108, 308)

  const makeTri = (h: number, a: {x:number;y:number}, b: {x:number;y:number}, inner: {x:number;y:number}, labelPos: {x:number;y:number}): NorthHouse => {
    // For planets in triangles, we use a weighted centroid favoring the inner point to avoid edges
    const px = (a.x + b.x + 2 * inner.x) / 4;
    const py = (a.y + b.y + 2 * inner.y) / 4;
    return { house: h, points: pts(a, b, inner), cx: labelPos.x, cy: labelPos.y, px, py };
  };

  const makeQuad = (h: number, a: {x:number;y:number}, b: {x:number;y:number}, c: {x:number;y:number}, d: {x:number;y:number}, labelPos: {x:number;y:number}): NorthHouse => {
    const cen = centroid(a, b, c, d);
    return { house: h, points: pts(a, b, c, d), cx: labelPos.x, cy: labelPos.y, px: cen.x, py: cen.y };
  };

  // TOP large triangle (TL, TR, CC) subdivisions (anti-clockwise):
  // House 2:  TL, MT, P1           (top-left corner triangle)
  houses.push(makeTri(2, TL, MT, P1, { x: TL.x + 22, y: TL.y + 16 }));
  // House 1:  P1, MT, P2, CC       (top center trapezoid -- Lagna)
  houses.push(makeQuad(1, P1, MT, P2, CC, { x: MT.x, y: MT.y + 18 }));
  // House 12: MT, TR, P2           (top-right corner triangle)
  houses.push(makeTri(12, MT, TR, P2, { x: TR.x - 22, y: TR.y + 16 }));

  // RIGHT large triangle (TR, BR, CC) subdivisions:
  // House 11: TR, MR, P2           (right-top corner triangle)
  houses.push(makeTri(11, TR, MR, P2, { x: TR.x - 16, y: TR.y + 36 }));
  // House 10: P2, MR, iP3, CC      (right center trapezoid)
  houses.push(makeQuad(10, P2, MR, iP3, CC, { x: MR.x - 18, y: MR.y }));
  // House 9:  MR, BR, iP3          (right-bottom corner triangle)
  houses.push(makeTri(9, MR, BR, iP3, { x: BR.x - 16, y: BR.y - 36 }));

  // BOTTOM large triangle (BR, BL, CC) subdivisions:
  // House 8:  BR, MB, iP3          (bottom-right corner triangle)
  houses.push(makeTri(8, BR, MB, iP3, { x: BR.x - 22, y: BR.y - 16 }));
  // House 7:  iP3, MB, iP4, CC     (bottom center trapezoid)
  houses.push(makeQuad(7, iP3, MB, iP4, CC, { x: MB.x, y: MB.y - 18 }));
  // House 6:  MB, BL, iP4          (bottom-left corner triangle)
  houses.push(makeTri(6, MB, BL, iP4, { x: BL.x + 22, y: BL.y - 16 }));

  // LEFT large triangle (BL, TL, CC) subdivisions:
  // House 5:  BL, ML, iP4          (left-bottom corner triangle)
  houses.push(makeTri(5, BL, ML, iP4, { x: BL.x + 16, y: BL.y - 36 }));
  // House 4:  iP4, ML, P1, CC      (left center trapezoid)
  houses.push(makeQuad(4, iP4, ML, P1, CC, { x: ML.x + 18, y: ML.y }));
  // House 3:  ML, TL, P1           (left-top corner triangle)
  houses.push(makeTri(3, ML, TL, P1, { x: TL.x + 16, y: TL.y + 36 }));

  return houses;
})();

// JHora visual constants
const JHORA_BG = '#F5E6B8';       // warm golden background
const JHORA_LINE = '#3D2B1F';      // dark brown lines
const JHORA_LINE_W = 2.2;          // line thickness
const JHORA_CURVE = 28;            // bezier curve inward offset for concave arcs

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

// --- Planet rendering ---
interface PlanetBadgeProps {
  planet: PlanetData;
  px: number;
  py: number;
  hoveredPlanet: string | null;
  setHoveredPlanet: (p: string | null) => void;
  showPlanetTooltip: (p: PlanetData, x: number, y: number) => void;
  hideTooltip: () => void;
  onPlanetClick?: (p: PlanetData) => void;
  hideCombust?: boolean;
  stateTag?: {
    hexColour: string;
    state: string;
    labelEn: string;
    labelHi: string;
    descEn?: string;
    descHi?: string;
  };
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
  hideCombust,
  stateTag,
}: PlanetBadgeProps) {
  const { language: lang } = useTranslation();
  const defaultColor = getPlanetColor(p.planet);
  const useStateColor = !!stateTag && stateTag.state !== 'normal';
  const color = useStateColor ? stateTag!.hexColour : defaultColor;
  const isHovered = hoveredPlanet === p.planet;
  const label = getPlanetLabel(p, lang, hideCombust);
  const stateLabel = useStateColor
    ? ` — ${lang === 'hi' ? stateTag!.labelHi : stateTag!.labelEn}`
    : '';

  return (
    <g
      role="img"
      aria-label={`${p.planet}${stateLabel}`}
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
      {useStateColor && (
        <circle
          cx={px}
          cy={py}
          r={15}
          fill="none"
          stroke={color}
          strokeWidth={1.5}
          strokeDasharray="2 2"
          opacity={0.6}
        />
      )}
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
        fontFamily="var(--, Inter, sans-serif)"
        style={{ pointerEvents: 'none', transition: 'fill 0.2s ease' }}
      >
        {label}
      </text>
    </g>
  );
}

export default function InteractiveKundli({ chartData, onPlanetClick, onHouseClick, compact, hideCombust, planetStates }: InteractiveKundliProps) {
  const { t, language } = useTranslation();
  const [hoveredHouse, setHoveredHouse] = useState<number | null>(null);
  const [hoveredPlanet, setHoveredPlanet] = useState<string | null>(null);
  const [tooltip, setTooltip] = useState<{ x: number; y: number; content: React.ReactNode } | null>(null);
  const [chartStyle, setChartStyle] = useState<ChartStyle>('north');

  const planets = useMemo(() => chartData.planets || [], [chartData.planets]);

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
  if (chartData.houses && chartData.houses.length > 0) {
    const h = chartData.houses.find((hh) => hh.number === house);
    if (h) return h.sign;
  }
  // Fallback: derive from Lagna/Ascendant planet
  const asc = planetsWithLagna.find((p) => p.planet === 'Lagna' || p.planet === 'Ascendant');
  if (asc) {
    const ascIdx = ZODIAC_SIGNS.indexOf(asc.sign);
    if (ascIdx >= 0) {
      const houseOfLagna = asc.house || 1;
      const signIdx = (ascIdx + (house - houseOfLagna) + 12) % 12;
      return ZODIAC_SIGNS[signIdx];
    }
  }
  return ZODIAC_SIGNS[(house - 1) % 12];
}, [chartData.houses, planetsWithLagna]);


  const aspectsFor = useCallback((planet: PlanetData): string[] => {
    const aspects = PLANET_ASPECTS[planet.planet] || [7];
    return aspects.map((offset) => {
      const targetHouse = ((planet.house - 1 + offset) % 12) + 1;
      return `${t('table.house')} ${targetHouse}`;
    });
  }, [t]);

  const showPlanetTooltip = useCallback((p: PlanetData, x: number, y: number) => {
    const strength = getStrength(p.status, t);
    const aspects = aspectsFor(p);
    const adjustedY = IS_TOUCH_DEVICE ? Math.max(0, y - 80) : y;
    setTooltip({
      x, y: adjustedY,
      content: (
        <div className="space-y-1.5">
          <div className="font-bold text-sacred-gold text-sm">{t(`planet.${p.planet}`)}</div>
          <div className="text-sm text-foreground">
            {(() => {
              const signStr = typeof p.sign === 'string' ? p.sign : (p.sign ? pickLang(p.sign, false) : '');
              return `${ZODIAC_NUMBERS[signStr] || ''} ${signStr} ${p.sign_degree?.toFixed(1)}°`;
            })()}
          </div>
          <div className="text-sm text-foreground">{t('table.nakshatra')}: {typeof p.nakshatra === 'string' ? p.nakshatra : (p.nakshatra ? pickLang(p.nakshatra, false) : '') || t('common.noData')}</div>
          <div className="text-sm text-foreground">{t('table.house')}: {p.house}</div>
          <div className="text-sm" style={{ color: strength.color }}>{strength.label}</div>
          <div className="text-sm text-foreground">{t('table.aspects')}: {aspects.join(', ')}</div>
        </div>
      ),
    });
  }, [aspectsFor, t]);

  const showHouseTooltip = useCallback((house: number, x: number, y: number) => {
    const housePlanets = planetsByHouse[house] || [];
    const adjustedY = IS_TOUCH_DEVICE ? Math.max(0, y - 80) : y;
    setTooltip({
      x, y: adjustedY,
      content: (
        <div className="space-y-1.5">
          <div className="font-bold text-sacred-gold text-sm">
            {t('table.house')} {house}
          </div>
          <div className="text-sm text-foreground">{t(`kundli.house${house}`)}</div>
          {housePlanets.length > 0 && (
            <div className="text-sm text-foreground">
              {t('table.planet')}: {housePlanets.map((p) => t(`planet.${p.planet}`)).join(', ')}
            </div>
          )}
        </div>
      ),
    });
  }, [planetsByHouse, t]);

  const hideTooltip = useCallback(() => {
    setTooltip(null);
    setHoveredHouse(null);
    setHoveredPlanet(null);
  }, []);

  const renderSouthIndian = () => {
    const svgWidth = CELL_SIZE * 4 + GRID_PADDING * 2;
    const svgHeight = CELL_SIZE * 4 + GRID_PADDING * 2;

    return (
      <svg
        width="100%"
        viewBox={`0 0 ${svgWidth} ${svgHeight}`}
        className="relative z-10"
        style={compact
          ? { width: '100%', height: '100%' }
          : { width: '100%', height: 'auto', filter: 'drop-shadow(0 0 12px rgba(212,175,55,0.25))' }
        }
      >
        <SvgDefs />
        <rect x={GRID_PADDING - 2} y={GRID_PADDING - 2} width={CELL_SIZE * 4 + 4} height={CELL_SIZE * 4 + 4} rx={6} fill="none" stroke="url(#kundli-border-grad)" strokeWidth={2.5} filter="url(#glow)" />
        <rect x={GRID_PADDING} y={GRID_PADDING} width={CELL_SIZE * 4} height={CELL_SIZE * 4} rx={4} fill="var(--sacred-gray-light)" />
        <text x={svgWidth / 2} y={svgHeight / 2 - 6} textAnchor="middle" fill="var(--aged-gold-dim)" fontSize={13} fontFamily="var(--, Inter, sans-serif)">{t('chart.rasi')}</text>
        <text x={svgWidth / 2} y={svgHeight / 2 + 10} textAnchor="middle" fill="var(--aged-gold-dim)" fontSize={9} fontFamily="var(--, Inter, sans-serif)">{t('chart.southIndian')}</text>
        {HOUSE_GRID.map(({ house, row, col }) => {
          const x = GRID_PADDING + col * CELL_SIZE;
          const y = GRID_PADDING + row * CELL_SIZE;
          const sign = houseSign(house);
          const isHovered = hoveredHouse === house;
          const housePlanets = planetsByHouse[house] || [];
          return (
            <g key={house} style={{ cursor: 'pointer' }} onMouseEnter={(e) => {
                setHoveredHouse(house);
                const rect = (e.target as SVGElement).closest('svg')?.getBoundingClientRect();
                if (rect) showHouseTooltip(house, e.clientX - rect.left, e.clientY - rect.top);
              }} onMouseLeave={hideTooltip} onClick={() => onHouseClick?.(house, sign, housePlanets)}>
              <rect x={x + 1} y={y + 1} width={CELL_SIZE - 2} height={CELL_SIZE - 2} fill={isHovered ? 'rgba(184,134,11,0.08)' : 'rgba(232,224,212,0.5)'} stroke={isHovered ? 'var(--aged-gold-dim)' : 'rgba(184,134,11,0.3)'} strokeWidth={isHovered ? 1.5 : 0.5} rx={2} style={{ transition: 'all 0.2s ease' }} />
              <text x={x + CELL_SIZE / 2} y={y + CELL_SIZE / 2 + 6} textAnchor="middle" fill="var(--aged-gold-dim)" fontSize={28} fontWeight="bold">{house}</text>
              {housePlanets.map((p, idx) => {
                const cols = Math.min(housePlanets.length, 3);
                const pRow = Math.floor(idx / cols);
                const pCol = idx % cols;
                const spacing = CELL_SIZE / (cols + 1);
                const px = x + spacing * (pCol + 1);
                const py = y + 28 + pRow * 22;
                return (
                  <PlanetBadge key={p.planet} planet={p} px={px} py={py} hoveredPlanet={hoveredPlanet} setHoveredPlanet={setHoveredPlanet} showPlanetTooltip={showPlanetTooltip} hideTooltip={hideTooltip} onPlanetClick={onPlanetClick} hideCombust={hideCombust} stateTag={planetStates?.[p.planet]} />
                );
              })}
            </g>
          );
        })}
        {[1, 2, 3].map((i) => (
          <g key={`grid-${i}`}>
            <line x1={GRID_PADDING + i * CELL_SIZE} y1={GRID_PADDING} x2={GRID_PADDING + i * CELL_SIZE} y2={GRID_PADDING + CELL_SIZE * 4} stroke="rgba(184,134,11,1)" strokeWidth={0.5} />
            <line x1={GRID_PADDING} y1={GRID_PADDING + i * CELL_SIZE} x2={GRID_PADDING + CELL_SIZE * 4} y2={GRID_PADDING + i * CELL_SIZE} stroke="rgba(184,134,11,1)" strokeWidth={0.5} />
          </g>
        ))}
      </svg>
    );
  };

  const renderNorthIndian = () => {
    const svgSize = NI_SIZE;
    const cv = JHORA_CURVE;
    const outerPath = [
      `M ${TL.x} ${TL.y}`,
      `Q ${MT.x} ${MT.y + cv} ${TR.x} ${TR.y}`,
      `Q ${MR.x - cv} ${MR.y} ${BR.x} ${BR.y}`,
      `Q ${MB.x} ${MB.y - cv} ${BL.x} ${BL.y}`,
      `Q ${ML.x + cv} ${ML.y} ${TL.x} ${TL.y}`,
      'Z',
    ].join(' ');
    const dcv = cv * 0.4;
    const diamondPath = [
      `M ${MT.x} ${MT.y}`,
      `Q ${(MT.x + MR.x) / 2 - dcv * 0.5} ${(MT.y + MR.y) / 2 + dcv * 0.5} ${MR.x} ${MR.y}`,
      `Q ${(MR.x + MB.x) / 2 - dcv * 0.5} ${(MR.y + MB.y) / 2 - dcv * 0.5} ${MB.x} ${MB.y}`,
      `Q ${(MB.x + ML.x) / 2 + dcv * 0.5} ${(MB.y + ML.y) / 2 - dcv * 0.5} ${ML.x} ${ML.y}`,
      `Q ${(ML.x + MT.x) / 2 + dcv * 0.5} ${(ML.y + MT.y) / 2 + dcv * 0.5} ${MT.x} ${MT.y}`,
      'Z',
    ].join(' ');
    const cBoxW = 30;
    const cBoxH = 22;

    return (
      <svg width="100%" viewBox={`0 0 ${svgSize} ${svgSize}`} className="relative z-10" style={compact ? { width: '100%', height: '100%' } : { width: '100%', height: 'auto', filter: 'drop-shadow(0 2px 8px rgba(61,43,31,0.15))' }}>
        <SvgDefs />
        <rect x={NI_PAD} y={NI_PAD} width={NI_INNER} height={NI_INNER} fill={JHORA_BG} />
        <path d={outerPath} fill="none" stroke={JHORA_LINE} strokeWidth={JHORA_LINE_W} strokeLinejoin="round" />
        <path d={diamondPath} fill="none" stroke={JHORA_LINE} strokeWidth={JHORA_LINE_W} strokeLinejoin="round" />
        <line x1={TL.x} y1={TL.y} x2={BR.x} y2={BR.y} stroke={JHORA_LINE} strokeWidth={JHORA_LINE_W} />
        <line x1={TR.x} y1={TR.y} x2={BL.x} y2={BL.y} stroke={JHORA_LINE} strokeWidth={JHORA_LINE_W} />
        <rect x={CC.x - cBoxW / 2} y={CC.y - cBoxH / 2} width={cBoxW} height={cBoxH} fill={JHORA_BG} stroke={JHORA_LINE} strokeWidth={1.5} rx={2} />
        <circle cx={CC.x - 6} cy={CC.y - 4} r={2} fill={JHORA_LINE} />
        <circle cx={CC.x + 6} cy={CC.y - 4} r={2} fill={JHORA_LINE} />
        <circle cx={CC.x - 6} cy={CC.y + 4} r={2} fill={JHORA_LINE} />
        <circle cx={CC.x + 6} cy={CC.y + 4} r={2} fill={JHORA_LINE} />
        {NORTH_HOUSES.map((nh) => {
          const sign = houseSign(nh.house);
          const isHovered = hoveredHouse === nh.house;
          const housePlanets = planetsByHouse[nh.house] || [];
          const isLagna = nh.house === 1;
          const rashiNum = ZODIAC_NUMBERS[sign] || '';
          return (
            <g key={nh.house} style={{ cursor: 'pointer' }} onMouseEnter={(e) => {
                setHoveredHouse(nh.house);
                const rect = (e.target as SVGElement).closest('svg')?.getBoundingClientRect();
                if (rect) showHouseTooltip(nh.house, e.clientX - rect.left, e.clientY - rect.top);
              }} onMouseLeave={hideTooltip} onClick={() => onHouseClick?.(nh.house, sign, housePlanets)}>
              <polygon points={nh.points} fill={isHovered ? 'rgba(61,43,31,0.06)' : 'transparent'} stroke="none" style={{ transition: 'fill 0.2s ease' }} />
              <text x={nh.cx} y={nh.cy} textAnchor="middle" fill={isLagna ? '#C62828' : JHORA_LINE} fontSize={isLagna ? 15 : 13} fontWeight="800" fontFamily="var(--, Inter, sans-serif)">{rashiNum}</text>
              {housePlanets.map((p, idx) => {
                const count = housePlanets.length;
                const isTrapezoid = [1, 4, 7, 10].includes(nh.house);
                const maxCols = isTrapezoid ? (count > 4 ? 3 : count > 2 ? 2 : count) : (count > 3 ? 3 : count > 1 ? 2 : 1);
                const cols = Math.min(count, maxCols);
                const pRow = Math.floor(idx / cols);
                const pCol = idx % cols;
                const spacing = isTrapezoid ? (count > 4 ? 26 : 32) : (count > 3 ? 22 : count > 2 ? 24 : 28);
                const rowHeight = count > 4 ? 16 : count > 3 ? 18 : 20;
                const fontSize = isTrapezoid ? (count > 4 ? 13 : 15) : (count > 3 ? 12 : count > 2 ? 13 : 14);
                const startX = nh.px - ((cols - 1) * spacing) / 2;
                const px = startX + pCol * spacing;
                const baseY = nh.py + (isTrapezoid ? 14 : 8) - (count > 0 ? 2 : 0);
                const py = baseY + pRow * rowHeight;
                const label = getPlanetLabel(p, language, hideCombust);
                const stateTag = planetStates?.[p.planet];
                const useStateColor = !!stateTag && stateTag.state !== 'normal';
                const planetFill = useStateColor ? stateTag!.hexColour : getPlanetColor(p.planet);
                return (
                  <g key={p.planet} role="img" aria-label={p.planet}>
                    {useStateColor && <circle cx={px} cy={py - fontSize + 2} r={2.5} fill={planetFill} opacity={0.8} />}
                    <text x={px} y={py} textAnchor="middle" fill={planetFill} fontSize={fontSize} fontWeight="bold" fontFamily="var(--, Inter, sans-serif)" style={{ cursor: 'pointer' }} onClick={(e) => { e.stopPropagation(); onPlanetClick?.(p); }}>{label}</text>
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
      {!compact && <div className="flex justify-center gap-1 mb-3 relative z-20">
        <button onClick={() => setChartStyle('north')} className="px-4 py-1.5 text-sm font-semibold rounded-l-md border transition-all duration-200" style={{ background: chartStyle === 'north' ? 'var(--aged-gold-dim)' : 'var(--sacred-gray-light)', color: chartStyle === 'north' ? 'var(--parchment)' : 'var(--ink-light)', borderColor: 'var(--aged-gold-dim)' }}>{t('kundli.northIndian')}</button>
        <button onClick={() => setChartStyle('south')} className="px-4 py-1.5 text-sm font-semibold rounded-r-md border transition-all duration-200" style={{ background: chartStyle === 'south' ? 'var(--aged-gold-dim)' : 'var(--sacred-gray-light)', color: chartStyle === 'south' ? 'var(--parchment)' : 'var(--ink-light)', borderColor: 'var(--aged-gold-dim)' }}>{t('kundli.southIndian')}</button>
      </div>}
      {!compact && <div className="absolute inset-0 rounded-2xl blur-xl pointer-events-none" style={{ background: 'radial-gradient(circle, rgba(212,175,55,0.3) 0%, rgba(128,0,128,0.15) 50%, transparent 70%)', transform: 'scale(1.1)' }} />}
      {chartStyle === 'north' ? renderNorthIndian() : renderSouthIndian()}
      {tooltip && <div className="absolute z-50 pointer-events-none" style={{ left: tooltip.x + 12, top: tooltip.y - 8, maxWidth: 220 }}><div className="bg-background backdrop-blur-sm border border-sacred-gold rounded-lg p-3 shadow-lg">{tooltip.content}</div></div>}
    </div>
  );
}

export function ChartLegend() {
  const { t } = useTranslation();
  return (
    <div className="flex flex-wrap gap-x-4 gap-y-1 justify-center text-sm mt-2 px-2" style={{ color: 'var(--aged-gold)', fontFamily: 'var(--, Inter, sans-serif)' }}>
      <span><strong>*</strong> {t('planet.retrograde')}</span>
      <span><strong>^</strong> {t('planet.combust')}</span>
      <span><strong>v</strong> {t('planet.vargottama')}</span>
      <span><strong>+</strong> {t('planet.exalted')}</span>
      <span><strong>-</strong> {t('planet.debilitated')}</span>
      <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full inline-block" style={{ background: '#C4611F' }} />{t('kundli.benefic')}</span>
      <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full inline-block" style={{ background: '#1a1a2e' }} />{t('kundli.malefic')}</span>
    </div>
  );
}
