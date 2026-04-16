/**
 * KundliChartSVG — Professional North Indian Kundli Chart (Diamond-in-Square)
 *
 * Fully transparent background with clean geometric lines.
 * Matches the traditional North Indian chart layout.
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

// North Indian chart geometry (viewBox 400x400)
// Outer square: (20,20) to (380,380)
// Diamond midpoints: top(200,20), right(380,200), bottom(200,380), left(20,200)
// Center: (200,200)
const S = 20;   // start
const E = 380;  // end
const M = 200;  // midpoint
const Q1 = 110; // quarter from start (for inner dividers)
const Q3 = 290; // quarter from end

/**
 * House center positions for planet text placement.
 * Houses 1-12 flow clockwise from top-center (North Indian layout).
 */
const HOUSE_CENTERS: { x: number; y: number }[] = [
  { x: 200, y: 75 },   // House 1  — top center diamond
  { x: 88,  y: 58 },   // House 2  — top-left triangle
  { x: 42,  y: 145 },  // House 3  — left-top triangle
  { x: 88,  y: 200 },  // House 4  — left center diamond
  { x: 42,  y: 255 },  // House 5  — left-bottom triangle
  { x: 88,  y: 342 },  // House 6  — bottom-left triangle
  { x: 200, y: 325 },  // House 7  — bottom center diamond
  { x: 312, y: 342 },  // House 8  — bottom-right triangle
  { x: 358, y: 255 },  // House 9  — right-bottom triangle
  { x: 312, y: 200 },  // House 10 — right center diamond
  { x: 358, y: 145 },  // House 11 — right-top triangle
  { x: 312, y: 58 },   // House 12 — top-right triangle
];

/** House number label positions (subtle, in corner of each house) */
const HOUSE_NUMBER_POS: { x: number; y: number }[] = [
  { x: 200, y: 36 },   // 1
  { x: 65,  y: 36 },   // 2
  { x: 28,  y: 110 },  // 3
  { x: 65,  y: 170 },  // 4
  { x: 28,  y: 225 },  // 5
  { x: 65,  y: 300 },  // 6
  { x: 200, y: 366 },  // 7
  { x: 335, y: 300 },  // 8
  { x: 372, y: 225 },  // 9
  { x: 335, y: 170 },  // 10
  { x: 372, y: 110 },  // 11
  { x: 335, y: 36 },   // 12
];

const LINE_COLOR = 'currentColor';

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
      className={`text-sacred-gold/25 ${className || ''}`}
      style={{ width: '100%', height: '100%' }}
    >
      {/* ============================================= */}
      {/* CHART STRUCTURE — all lines use currentColor  */}
      {/* The parent className sets the line opacity     */}
      {/* ============================================= */}

      {/* Outer square — double border effect */}
      <rect
        x={S} y={S} width={E - S} height={E - S}
        fill="none" stroke={LINE_COLOR} strokeWidth="2.5"
      />
      <rect
        x={S + 5} y={S + 5} width={E - S - 10} height={E - S - 10}
        fill="none" stroke={LINE_COLOR} strokeWidth="1"
      />

      {/* Inner diamond — connects midpoints of each side */}
      <polygon
        points={`${M},${S + 5} ${E - 5},${M} ${M},${E - 5} ${S + 5},${M}`}
        fill="none" stroke={LINE_COLOR} strokeWidth="1.5"
      />

      {/* ---- Traditional North Indian: NO center box ---- */}
      {/* The diamond + 4 corner-to-center diagonals create all 12 houses */}

      {/* Top-left corner to center — divides houses 2 and 3 */}
      <line x1={S + 5} y1={S + 5} x2={M} y2={M} stroke={LINE_COLOR} strokeWidth="0.8" />

      {/* Top-right corner to center — divides houses 11 and 12 */}
      <line x1={E - 5} y1={S + 5} x2={M} y2={M} stroke={LINE_COLOR} strokeWidth="0.8" />

      {/* Bottom-left corner to center — divides houses 5 and 6 */}
      <line x1={S + 5} y1={E - 5} x2={M} y2={M} stroke={LINE_COLOR} strokeWidth="0.8" />

      {/* Bottom-right corner to center — divides houses 8 and 9 */}
      <line x1={E - 5} y1={E - 5} x2={M} y2={M} stroke={LINE_COLOR} strokeWidth="0.8" />

      {/* ============================================= */}
      {/* TEXT CONTENT — house numbers, Asc, planets    */}
      {/* ============================================= */}

      {/* House Numbers — subtle reference */}
      {HOUSE_NUMBER_POS.map((pos, i) => (
        <text
          key={`hnum-${i}`}
          x={pos.x}
          y={pos.y}
          textAnchor="middle"
          dominantBaseline="central"
          fontSize="9"
          fill="currentColor"
          fontFamily="sans-serif"
          opacity="0.5"
          className="text-foreground/30"
        >
          {i + 1}
        </text>
      ))}

      {/* Ascendant marker */}
      <text
        x={M}
        y={52}
        textAnchor="middle"
        dominantBaseline="central"
        fontSize="10"
        fontFamily="sans-serif"
        fontStyle="italic"
        fontWeight="600"
        className="fill-sacred-gold/60"
      >
        Asc
      </text>

      {/* Planets in each house */}
      {Array.from({ length: 12 }, (_, i) => i + 1).map((house) => {
        const housePlanets = planetsByHouse[house] || [];
        if (housePlanets.length === 0) return null;

        const center = HOUSE_CENTERS[house - 1];
        const count = housePlanets.length;
        const lineH = count > 3 ? 12 : 14;
        const startY = center.y - ((count - 1) * lineH) / 2;

        return housePlanets.map((p, pIdx) => {
          const abbr = PLANET_ABBR[p.planet] || p.planet.slice(0, 2);
          const color = PLANET_COLORS[p.planet] || '#4B5563';
          const yPos = startY + pIdx * lineH;

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
                  <tspan fill="#DC2626" fontSize="8">(R)</tspan>
                </>
              ) : (
                abbr
              )}
            </text>
          );
        });
      })}

      {/* Ascendant sign in center */}
      <text
        x={M}
        y={M}
        textAnchor="middle"
        dominantBaseline="central"
        fontSize="11"
        fontFamily="sans-serif"
        fontWeight="600"
        className="fill-sacred-gold/50"
      >
        {ascendantSign || ''}
      </text>
    </svg>
  );
}
