import { useTranslation } from '@/lib/i18n';

/**
 * SarvatobhadraChakra — Pure SVG 9x9 Sarvatobhadra Chakra Grid
 *
 * Renders the 9x9 SBC grid with:
 *   - Color-coded cells (nakshatras=saffron, signs=green, vowels=blue, days=purple)
 *   - Planet glyphs placed in cells
 *   - Vedha lines drawn between connected cells
 *   - Responsive sizing via viewBox
 */

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface SBCCell {
  type: 'nakshatra' | 'sign' | 'vowel' | 'day' | 'empty';
  name: string;
  row: number;
  col: number;
  natal_planets?: string[];
  transit_planets?: string[];
}

interface VedhaEntry {
  transit_planet: string;
  transit_nakshatra: string;
  transit_cell: [number, number];
  natal_planet: string;
  natal_nakshatra: string;
  natal_cell: [number, number];
  vedha_type: 'diagonal' | 'row' | 'column';
  effect: 'auspicious' | 'inauspicious';
}

export interface SarvatobhadraChakraProps {
  grid: SBCCell[][];
  vedhas?: VedhaEntry[];
  showVedhaLines?: boolean;
  className?: string;
}

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const GRID_SIZE = 9;
const CELL_SIZE = 60;
const PADDING = 20;
const TOTAL_SIZE = GRID_SIZE * CELL_SIZE + PADDING * 2;

/** Cell background colors by type */
const CELL_COLORS: Record<string, { bg: string; text: string; border: string }> = {
  nakshatra: { bg: '#FFF3E0', text: '#E65100', border: '#FFB74D' },  // saffron
  sign:      { bg: '#E8F5E9', text: '#1B5E20', border: '#81C784' },  // green
  vowel:     { bg: '#E3F2FD', text: '#0D47A1', border: '#64B5F6' },  // blue
  day:       { bg: '#F3E5F5', text: '#4A148C', border: '#BA68C8' },  // purple
  empty:     { bg: '#FAFAFA', text: '#9E9E9E', border: '#E0E0E0' },  // gray
};

/** Planet abbreviations */
const PLANET_ABBR: Record<string, string> = {
  Sun: 'Su', Moon: 'Mo', Mars: 'Ma', Mercury: 'Me',
  Jupiter: 'Ju', Venus: 'Ve', Saturn: 'Sa',
  Rahu: 'Ra', Ketu: 'Ke',
};

/** Planet colors */
const PLANET_COLORS: Record<string, string> = {
  Sun: '#E65100', Moon: '#546E7A', Mars: '#C62828', Mercury: '#2E7D32',
  Jupiter: '#F9A825', Venus: '#AD1457', Saturn: '#1565C0',
  Rahu: '#6A1B9A', Ketu: '#78909C',
};

/** Vedha line colors */
const VEDHA_COLORS = {
  auspicious: '#2E7D32',
  inauspicious: '#C62828',
};

/** Short cell labels for display */
function cellLabel(cell: SBCCell): string {
  if (cell.type === 'empty') return '';
  const name = cell.name;
  // Abbreviate long nakshatra names
  if (cell.type === 'nakshatra') {
    const abbrevs: Record<string, string> = {
      'Krittika': 'Krit', 'Rohini': 'Rohi', 'Mrigashira': 'Mrig',
      'Ardra': 'Ardr', 'Punarvasu': 'Puna', 'Pushya': 'Push',
      'Ashlesha': 'Ashl', 'Bharani': 'Bhar', 'Ashwini': 'Ashw',
      'Revati': 'Reva', 'Hasta': 'Hast', 'Abhijit': 'Abhi',
      'Dhanishta': 'Dhan', 'Shatabhisha': 'Shat', 'Chitra': 'Chit',
      'Swati': 'Swat', 'Mula': 'Mula', 'Jyeshtha': 'Jyes',
      'Anuradha': 'Anur', 'Magha': 'Magh',
      'Purva Phalguni': 'P.Pha', 'Uttara Phalguni': 'U.Pha',
      'Vishakha': 'Vish', 'Purva Ashadha': 'P.Ash',
      'Uttara Ashadha': 'U.Ash', 'Shravana': 'Shra',
      'Purva Bhadrapada': 'P.Bhd', 'Uttara Bhadrapada': 'U.Bhd',
    };
    return abbrevs[name] || name.slice(0, 4);
  }
  if (cell.type === 'sign') {
    const signAbbrevs: Record<string, string> = {
      'Aries': 'Ari', 'Taurus': 'Tau', 'Gemini': 'Gem', 'Cancer': 'Can',
      'Leo': 'Leo', 'Virgo': 'Vir', 'Libra': 'Lib', 'Scorpio': 'Sco',
      'Sagittarius': 'Sag', 'Capricorn': 'Cap', 'Aquarius': 'Aqu', 'Pisces': 'Pis',
    };
    return signAbbrevs[name] || name.slice(0, 3);
  }
  if (cell.type === 'day') {
    return name.slice(0, 3); // Sun, Mon, Tue, etc.
  }
  return name; // vowels are already short
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

export default function SarvatobhadraChakra({
  grid,
  vedhas = [],
  showVedhaLines = true,
  className,
}: SarvatobhadraChakraProps) {
  const { t } = useTranslation();

  if (!grid || grid.length !== 9) return null;

  /** Get pixel center of a cell */
  function cellCenter(row: number, col: number): { x: number; y: number } {
    return {
      x: PADDING + col * CELL_SIZE + CELL_SIZE / 2,
      y: PADDING + row * CELL_SIZE + CELL_SIZE / 2,
    };
  }

  return (
    <svg
      viewBox={`0 0 ${TOTAL_SIZE} ${TOTAL_SIZE}`}
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      style={{ width: '100%', height: '100%' }}
    >
      {/* Background */}
      <rect x="0" y="0" width={TOTAL_SIZE} height={TOTAL_SIZE} fill="#FFFDF7" rx="8" />

      {/* Title */}
      <text
        x={TOTAL_SIZE / 2}
        y={12}
        textAnchor="middle"
        fontSize="10"
        fill="#B45309"
        fontFamily="sans-serif"
        fontWeight="600"
      >
        {t('panchang.sarvatobhadraChakra')}
      </text>

      {/* Grid cells */}
      {grid.map((row, r) =>
        row.map((cell, c) => {
          const x = PADDING + c * CELL_SIZE;
          const y = PADDING + r * CELL_SIZE;
          const colors = CELL_COLORS[cell.type] || CELL_COLORS.empty;
          const label = cellLabel(cell);
          const natalPlanets = cell.natal_planets || [];
          const transitPlanets = cell.transit_planets || [];
          const hasPlanets = natalPlanets.length > 0 || transitPlanets.length > 0;

          return (
            <g key={`cell-${r}-${c}`}>
              {/* Cell background */}
              <rect
                x={x}
                y={y}
                width={CELL_SIZE}
                height={CELL_SIZE}
                fill={colors.bg}
                stroke={colors.border}
                strokeWidth="0.8"
                rx="2"
              />

              {/* Highlight center cell */}
              {r === 4 && c === 4 && (
                <rect
                  x={x + 2}
                  y={y + 2}
                  width={CELL_SIZE - 4}
                  height={CELL_SIZE - 4}
                  fill="none"
                  stroke="#B45309"
                  strokeWidth="1.5"
                  strokeDasharray="3,2"
                  rx="2"
                />
              )}

              {/* Cell label */}
              {label && (
                <text
                  x={x + CELL_SIZE / 2}
                  y={y + (hasPlanets ? 12 : CELL_SIZE / 2)}
                  textAnchor="middle"
                  dominantBaseline={hasPlanets ? 'auto' : 'central'}
                  fontSize={cell.type === 'nakshatra' ? '7' : '8'}
                  fill={colors.text}
                  fontFamily="sans-serif"
                  fontWeight="500"
                >
                  {label}
                </text>
              )}

              {/* Natal planets (top half of remaining space) */}
              {natalPlanets.map((planet, idx) => {
                const abbr = PLANET_ABBR[planet] || planet.slice(0, 2);
                const color = PLANET_COLORS[planet] || '#4B5563';
                const pY = y + 22 + idx * 10;
                return (
                  <text
                    key={`n-${r}-${c}-${idx}`}
                    x={x + CELL_SIZE / 2}
                    y={pY}
                    textAnchor="middle"
                    dominantBaseline="central"
                    fontSize="8"
                    fontWeight="700"
                    fontFamily="sans-serif"
                    fill={color}
                  >
                    {abbr}
                  </text>
                );
              })}

              {/* Transit planets (bottom half, italic) */}
              {transitPlanets.map((planet, idx) => {
                const abbr = PLANET_ABBR[planet] || planet.slice(0, 2);
                const color = PLANET_COLORS[planet] || '#4B5563';
                const pY = y + CELL_SIZE - 8 - (transitPlanets.length - 1 - idx) * 10;
                return (
                  <text
                    key={`t-${r}-${c}-${idx}`}
                    x={x + CELL_SIZE / 2}
                    y={pY}
                    textAnchor="middle"
                    dominantBaseline="central"
                    fontSize="7"
                    fontWeight="600"
                    fontStyle="italic"
                    fontFamily="sans-serif"
                    fill={color}
                    opacity="0.85"
                  >
                    {abbr}
                  </text>
                );
              })}
            </g>
          );
        })
      )}

      {/* Vedha lines */}
      {showVedhaLines &&
        vedhas.map((v, idx) => {
          const from = cellCenter(v.transit_cell[0], v.transit_cell[1]);
          const to = cellCenter(v.natal_cell[0], v.natal_cell[1]);
          const color = VEDHA_COLORS[v.effect];
          return (
            <line
              key={`vedha-${idx}`}
              x1={from.x}
              y1={from.y}
              x2={to.x}
              y2={to.y}
              stroke={color}
              strokeWidth="1"
              strokeDasharray={v.vedha_type === 'diagonal' ? '4,2' : '2,2'}
              opacity="0.5"
              markerEnd={`url(#arrow-${v.effect})`}
            />
          );
        })}

      {/* Arrow markers for vedha lines */}
      <defs>
        <marker
          id="arrow-auspicious"
          viewBox="0 0 10 10"
          refX="8"
          refY="5"
          markerWidth="5"
          markerHeight="5"
          orient="auto-start-reverse"
        >
          <path d="M 0 0 L 10 5 L 0 10 z" fill={VEDHA_COLORS.auspicious} opacity="0.5" />
        </marker>
        <marker
          id="arrow-inauspicious"
          viewBox="0 0 10 10"
          refX="8"
          refY="5"
          markerWidth="5"
          markerHeight="5"
          orient="auto-start-reverse"
        >
          <path d="M 0 0 L 10 5 L 0 10 z" fill={VEDHA_COLORS.inauspicious} opacity="0.5" />
        </marker>
      </defs>

      {/* Legend */}
      <g transform={`translate(${PADDING}, ${TOTAL_SIZE - 6})`}>
        {[
          { label: t('auto.nakshatra'), color: CELL_COLORS.nakshatra.bg, border: CELL_COLORS.nakshatra.border },
          { label: t('auto.sign'), color: CELL_COLORS.sign.bg, border: CELL_COLORS.sign.border },
          { label: t('numerology.vowel'), color: CELL_COLORS.vowel.bg, border: CELL_COLORS.vowel.border },
          { label: t('auto.weekday'), color: CELL_COLORS.day.bg, border: CELL_COLORS.day.border },
        ].map((item, i) => (
          <g key={`legend-${i}`} transform={`translate(${i * 100}, 0)`}>
            <rect x="0" y="-5" width="8" height="8" fill={item.color} stroke={item.border} strokeWidth="0.5" />
            <text x="11" y="1" fontSize="7" fill="#666" fontFamily="sans-serif">{item.label}</text>
          </g>
        ))}
      </g>
    </svg>
  );
}
