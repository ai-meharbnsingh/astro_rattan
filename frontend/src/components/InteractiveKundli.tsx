import { useState, useCallback, useMemo } from 'react';

// --- Data types ---
export interface PlanetData {
  planet: string;
  sign: string;
  house: number;
  nakshatra: string;
  sign_degree: number;
  status: string;
}

export interface ChartData {
  planets: PlanetData[];
  houses?: { number: number; sign: string }[];
}

interface InteractiveKundliProps {
  chartData: ChartData;
  onPlanetClick?: (planet: PlanetData) => void;
  onHouseClick?: (house: number, sign: string, planets: PlanetData[]) => void;
}

// --- Constants ---
const ZODIAC_SIGNS = [
  'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
  'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces',
];

const ZODIAC_SYMBOLS: Record<string, string> = {
  Aries: '\u2648', Taurus: '\u2649', Gemini: '\u264A', Cancer: '\u264B',
  Leo: '\u264C', Virgo: '\u264D', Libra: '\u264E', Scorpio: '\u264F',
  Sagittarius: '\u2650', Capricorn: '\u2651', Aquarius: '\u2652', Pisces: '\u2653',
};

const PLANET_ABBREVIATIONS: Record<string, string> = {
  Sun: 'Su', Moon: 'Mo', Mars: 'Ma', Mercury: 'Me', Jupiter: 'Ju',
  Venus: 'Ve', Saturn: 'Sa', Rahu: 'Ra', Ketu: 'Ke',
  Ascendant: 'As', Lagna: 'As',
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

function getPlanetColor(planet: string): string {
  if (BENEFIC_PLANETS.includes(planet)) return '#D4AF37'; // gold
  if (MALEFIC_PLANETS.includes(planet)) return '#9B59B6'; // purple
  return '#C0C0C0'; // silver
}

function getStrength(status: string): { label: string; color: string } {
  const s = status?.toLowerCase() || '';
  if (s.includes('exalted')) return { label: 'Exalted', color: '#22C55E' };
  if (s.includes('debilitated')) return { label: 'Debilitated', color: '#EF4444' };
  if (s.includes('own')) return { label: 'Own Sign', color: '#3B82F6' };
  return { label: status || 'Transiting', color: '#9CA3AF' };
}

/*
 * South Indian kundli layout -- 4x4 grid with 12 outer cells.
 * The house positions in the grid (row, col) for South Indian style:
 *
 *   [12] [ 1] [ 2] [ 3]
 *   [11] [  ] [  ] [ 4]
 *   [10] [  ] [  ] [ 5]
 *   [ 9] [ 8] [ 7] [ 6]
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

export default function InteractiveKundli({ chartData, onPlanetClick, onHouseClick }: InteractiveKundliProps) {
  const [hoveredHouse, setHoveredHouse] = useState<number | null>(null);
  const [hoveredPlanet, setHoveredPlanet] = useState<string | null>(null);
  const [tooltip, setTooltip] = useState<{ x: number; y: number; content: React.ReactNode } | null>(null);

  const planets = chartData.planets || [];

  const planetsByHouse = useMemo(() => {
    const map: Record<number, PlanetData[]> = {};
    for (let i = 1; i <= 12; i++) map[i] = [];
    planets.forEach((p) => {
      const h = p.house || 1;
      if (map[h]) map[h].push(p);
    });
    return map;
  }, [planets]);

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
    const strength = getStrength(p.status);
    const aspects = aspectsFor(p);
    setTooltip({
      x, y,
      content: (
        <div className="space-y-1.5">
          <div className="font-display font-bold text-sacred-gold text-sm">{p.planet}</div>
          <div className="text-xs text-cosmic-text">
            {ZODIAC_SYMBOLS[p.sign] || ''} {p.sign} {p.sign_degree?.toFixed(1)}&deg;
          </div>
          <div className="text-xs text-cosmic-text-muted">Nakshatra: {p.nakshatra || 'N/A'}</div>
          <div className="text-xs text-cosmic-text-muted">House: {p.house}</div>
          <div className="text-xs" style={{ color: strength.color }}>Strength: {strength.label}</div>
          <div className="text-xs text-cosmic-text-muted">Aspects: {aspects.join(', ')}</div>
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
            House {house} {ZODIAC_SYMBOLS[sign] || ''} {sign}
          </div>
          <div className="text-xs text-cosmic-text-muted">{HOUSE_SIGNIFICANCE[house] || ''}</div>
          {housePlanets.length > 0 && (
            <div className="text-xs text-cosmic-text">
              Planets: {housePlanets.map((p) => p.planet).join(', ')}
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

  const svgWidth = CELL_SIZE * 4 + GRID_PADDING * 2;
  const svgHeight = CELL_SIZE * 4 + GRID_PADDING * 2;

  return (
    <div className="relative inline-block">
      {/* Cosmic glow effect behind chart */}
      <div
        className="absolute inset-0 rounded-2xl opacity-40 blur-xl pointer-events-none"
        style={{
          background: 'radial-gradient(circle, rgba(212,175,55,0.3) 0%, rgba(128,0,128,0.15) 50%, transparent 70%)',
          transform: 'scale(1.1)',
        }}
      />

      <svg
        viewBox={`0 0 ${svgWidth} ${svgHeight}`}
        className="w-full max-w-[480px] h-auto relative z-10"
        style={{ filter: 'drop-shadow(0 0 12px rgba(212,175,55,0.25))' }}
      >
        <defs>
          <linearGradient id="kundli-border-grad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#D4AF37" />
            <stop offset="50%" stopColor="#FFD700" />
            <stop offset="100%" stopColor="#B8860B" />
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
          fill="#0F0A1E"
          opacity={0.95}
        />

        {/* Center area label */}
        <text
          x={svgWidth / 2}
          y={svgHeight / 2 - 6}
          textAnchor="middle"
          fill="#D4AF37"
          fontSize={11}
          fontFamily="serif"
          opacity={0.6}
        >
          Rasi Chart
        </text>
        <text
          x={svgWidth / 2}
          y={svgHeight / 2 + 10}
          textAnchor="middle"
          fill="#D4AF37"
          fontSize={9}
          fontFamily="serif"
          opacity={0.4}
        >
          South Indian
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
                fill={isHovered ? 'rgba(212,175,55,0.12)' : 'rgba(15,10,30,0.6)'}
                stroke={isHovered ? '#D4AF37' : 'rgba(212,175,55,0.2)'}
                strokeWidth={isHovered ? 1.5 : 0.5}
                rx={2}
                style={{ transition: 'all 0.2s ease' }}
              />

              {/* House number */}
              <text
                x={x + 8}
                y={y + 14}
                fill="rgba(212,175,55,0.5)"
                fontSize={9}
                fontFamily="monospace"
              >
                {house}
              </text>

              {/* Zodiac symbol */}
              <text
                x={x + CELL_SIZE - 8}
                y={y + 14}
                textAnchor="end"
                fill="rgba(212,175,55,0.4)"
                fontSize={13}
              >
                {ZODIAC_SYMBOLS[sign] || ''}
              </text>

              {/* Zodiac sign name */}
              <text
                x={x + CELL_SIZE / 2}
                y={y + CELL_SIZE - 8}
                textAnchor="middle"
                fill="rgba(212,175,55,0.35)"
                fontSize={8}
                fontFamily="sans-serif"
              >
                {sign}
              </text>

              {/* Planets in this house */}
              {housePlanets.map((p, idx) => {
                const cols = Math.min(housePlanets.length, 3);
                const pRow = Math.floor(idx / cols);
                const pCol = idx % cols;
                const spacing = CELL_SIZE / (cols + 1);
                const px = x + spacing * (pCol + 1);
                const py = y + 28 + pRow * 22;
                const color = getPlanetColor(p.planet);
                const isHoveredPlanet = hoveredPlanet === p.planet;
                const abbr = PLANET_ABBREVIATIONS[p.planet] || p.planet.slice(0, 2);

                return (
                  <g
                    key={p.planet}
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
                      r={isHoveredPlanet ? 11 : 9}
                      fill={isHoveredPlanet ? color : 'rgba(15,10,30,0.8)'}
                      stroke={color}
                      strokeWidth={1.5}
                      filter={isHoveredPlanet ? 'url(#planet-glow)' : undefined}
                      style={{ transition: 'all 0.2s ease' }}
                    />
                    <text
                      x={px}
                      y={py + 3.5}
                      textAnchor="middle"
                      fill={isHoveredPlanet ? '#0F0A1E' : color}
                      fontSize={9}
                      fontWeight="bold"
                      fontFamily="sans-serif"
                      style={{ pointerEvents: 'none', transition: 'fill 0.2s ease' }}
                    >
                      {abbr}
                    </text>
                  </g>
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
              stroke="rgba(212,175,55,0.15)"
              strokeWidth={0.5}
            />
            <line
              x1={GRID_PADDING}
              y1={GRID_PADDING + i * CELL_SIZE}
              x2={GRID_PADDING + CELL_SIZE * 4}
              y2={GRID_PADDING + i * CELL_SIZE}
              stroke="rgba(212,175,55,0.15)"
              strokeWidth={0.5}
            />
          </g>
        ))}
      </svg>

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
