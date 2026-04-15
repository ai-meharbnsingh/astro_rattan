/**
 * KundliChartSVG — Pure SVG North Indian Kundli Chart
 *
 * Transparent background, sacred gold lines, planet abbreviations with colors,
 * retrograde indicators, ascendant marker. Responsive via viewBox.
 */

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
  className?: string;
}

// --- Constants ---

const PLANET_ABBR: Record<string, string> = {
  Sun: 'Su',
  Moon: 'Mo',
  Mars: 'Ma',
  Mercury: 'Me',
  Jupiter: 'Ju',
  Venus: 'Ve',
  Saturn: 'Sa',
  Rahu: 'Ra',
  Ketu: 'Ke',
};

const PLANET_COLORS: Record<string, string> = {
  Sun: '#E65100',
  Moon: '#546E7A',
  Mars: '#C62828',
  Mercury: '#2E7D32',
  Jupiter: '#F9A825',
  Venus: '#AD1457',
  Saturn: '#1565C0',
  Rahu: '#6A1B9A',
  Ketu: '#78909C',
};

/**
 * North Indian chart house center positions (viewBox 400x400).
 *
 * The chart is an outer square (20,20)-(380,380) with a diamond connecting midpoints.
 * Houses 1-12 flow clockwise from top-center.
 */
const HOUSE_CENTERS: { x: number; y: number }[] = [
  { x: 200, y: 72 },   // House 1  — top center
  { x: 92, y: 72 },    // House 2  — top left
  { x: 52, y: 148 },   // House 3  — left top
  { x: 92, y: 200 },   // House 4  — left center
  { x: 52, y: 255 },   // House 5  — left bottom
  { x: 92, y: 330 },   // House 6  — bottom left
  { x: 200, y: 330 },  // House 7  — bottom center
  { x: 308, y: 330 },  // House 8  — bottom right
  { x: 348, y: 255 },  // House 9  — right bottom
  { x: 308, y: 200 },  // House 10 — right center
  { x: 348, y: 148 },  // House 11 — right top
  { x: 308, y: 72 },   // House 12 — top right
];

/** Small offset position for the house number label (top-left corner of each house area) */
const HOUSE_NUMBER_POS: { x: number; y: number }[] = [
  { x: 200, y: 38 },   // 1
  { x: 68, y: 38 },    // 2
  { x: 28, y: 115 },   // 3
  { x: 68, y: 168 },   // 4
  { x: 28, y: 222 },   // 5
  { x: 68, y: 295 },   // 6
  { x: 200, y: 365 },  // 7
  { x: 332, y: 295 },  // 8
  { x: 372, y: 222 },  // 9
  { x: 332, y: 168 },  // 10
  { x: 372, y: 115 },  // 11
  { x: 332, y: 38 },   // 12
];

const STROKE_COLOR = '#B45309';

export default function KundliChartSVG({ planets, ascendantSign, className }: KundliChartSVGProps) {
  // Group planets by house
  const planetsByHouse: Record<number, PlanetEntry[]> = {};
  for (const p of planets) {
    const h = p.house;
    if (h < 1 || h > 12) continue;
    if (!planetsByHouse[h]) planetsByHouse[h] = [];
    planetsByHouse[h].push(p);
  }

  return (
    <svg
      viewBox="0 0 400 400"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      style={{ width: '100%', height: '100%' }}
    >
      {/* --- Chart Structure --- */}

      {/* Outer square */}
      <rect
        x="20" y="20" width="360" height="360"
        fill="none" stroke={STROKE_COLOR} strokeWidth="1.5"
      />

      {/* Inner diamond — midpoint to midpoint */}
      <polygon
        points="200,20 380,200 200,380 20,200"
        fill="none" stroke={STROKE_COLOR} strokeWidth="1"
      />

      {/* Corner-to-center diagonals that divide the edge triangles into houses */}
      {/* Top-left corner to bottom-right corner */}
      {/* These lines go from each corner to the two opposite midpoints of that corner's triangle */}

      {/* Top row: line from top-left corner to top-right corner through diamond center area */}
      {/* Horizontal divider for top triangle: from left-diamond to right-diamond through ~y=110 */}
      <line x1="110" y1="110" x2="290" y2="110" stroke={STROKE_COLOR} strokeWidth="0.5" opacity="0.35" />

      {/* Bottom row: divider for bottom triangle */}
      <line x1="110" y1="290" x2="290" y2="290" stroke={STROKE_COLOR} strokeWidth="0.5" opacity="0.35" />

      {/* Left column: divider for left triangle */}
      <line x1="110" y1="110" x2="110" y2="290" stroke={STROKE_COLOR} strokeWidth="0.5" opacity="0.35" />

      {/* Right column: divider for right triangle */}
      <line x1="290" y1="110" x2="290" y2="290" stroke={STROKE_COLOR} strokeWidth="0.5" opacity="0.35" />

      {/* --- House Numbers --- */}
      {HOUSE_NUMBER_POS.map((pos, i) => (
        <text
          key={`hnum-${i}`}
          x={pos.x}
          y={pos.y}
          textAnchor="middle"
          dominantBaseline="central"
          fontSize="10"
          fill="#9CA3AF"
          fontFamily="sans-serif"
          opacity="0.6"
        >
          {i + 1}
        </text>
      ))}

      {/* --- Ascendant marker in House 1 --- */}
      <text
        x={200}
        y={55}
        textAnchor="middle"
        dominantBaseline="central"
        fontSize="10"
        fill="#B45309"
        fontFamily="sans-serif"
        fontStyle="italic"
        fontWeight="600"
        opacity="0.8"
      >
        Asc
      </text>

      {/* --- Planets in each house --- */}
      {Array.from({ length: 12 }, (_, i) => i + 1).map((house) => {
        const housePlanets = planetsByHouse[house] || [];
        if (housePlanets.length === 0) return null;

        const center = HOUSE_CENTERS[house - 1];
        const count = housePlanets.length;
        // Stack planets vertically around center; 14px per line
        const lineH = 14;
        const startY = center.y - ((count - 1) * lineH) / 2;

        return housePlanets.map((p, pIdx) => {
          const abbr = PLANET_ABBR[p.planet] || p.planet.slice(0, 2);
          const color = PLANET_COLORS[p.planet] || '#4B5563';
          const yPos = startY + pIdx * lineH;
          const label = p.is_retrograde ? `${abbr}(R)` : abbr;

          return (
            <text
              key={`p-${house}-${pIdx}`}
              x={center.x}
              y={yPos}
              textAnchor="middle"
              dominantBaseline="central"
              fontSize="11"
              fontWeight="600"
              fontFamily="sans-serif"
              fill={color}
            >
              {p.is_retrograde ? (
                <>
                  <tspan fill={color}>{abbr}</tspan>
                  <tspan fill="#DC2626" fontSize="9">(R)</tspan>
                </>
              ) : (
                label
              )}
            </text>
          );
        });
      })}

      {/* --- Ascendant sign label in center diamond --- */}
      <text
        x={200}
        y={200}
        textAnchor="middle"
        dominantBaseline="central"
        fontSize="12"
        fill="#B45309"
        fontFamily="sans-serif"
        fontWeight="600"
        opacity="0.7"
      >
        {ascendantSign || ''}
      </text>
    </svg>
  );
}
