import { useState } from 'react';
import { useTranslation } from '@/lib/i18n';

/**
 * Interactive SVG compass rose for Vastu entrance direction selection.
 * 8 main directions with inner pada ring showing 32 sub-divisions.
 */

interface Props {
  value: string;
  onChange: (direction: string) => void;
  mode?: 'select' | 'display';
  highlightedPada?: string;  // e.g. "N5" for result display
  onPadaClick?: (padaCode: string, midDegrees: number) => void;  // fired when a specific pada is clicked
}

interface DirInfo {
  code: string;
  en: string;
  hi: string;
  angle: number;     // center angle in degrees (0=N, clockwise)
}

const DIRECTIONS: DirInfo[] = [
  { code: 'N',  en: 'North',     hi: 'उत्तर',  angle: 0 },
  { code: 'NE', en: 'Northeast', hi: 'ईशान',   angle: 45 },
  { code: 'E',  en: 'East',      hi: 'पूर्व',   angle: 90 },
  { code: 'SE', en: 'Southeast', hi: 'आग्नेय', angle: 135 },
  { code: 'S',  en: 'South',     hi: 'दक्षिण',  angle: 180 },
  { code: 'SW', en: 'Southwest', hi: 'नैऋत्य', angle: 225 },
  { code: 'W',  en: 'West',      hi: 'पश्चिम',  angle: 270 },
  { code: 'NW', en: 'Northwest', hi: 'वायव्य', angle: 315 },
];

// 32 Padas — 8 per cardinal direction
const PADA_DIRECTIONS = ['N', 'E', 'S', 'W'];
const PADA_SCORES: Record<string, number> = {
  N1: 4, N2: 4, N3: 4, N4: 5, N5: 5, N6: 5, N7: 4, N8: 3,
  E1: 4, E2: 5, E3: 5, E4: 5, E5: 4, E6: 3, E7: 2, E8: 2,
  S1: 1, S2: 1, S3: 1, S4: 4, S5: 1, S6: 3, S7: 1, S8: 1,
  W1: 3, W2: 1, W3: 1, W4: 5, W5: 1, W6: 1, W7: 4, W8: 5,
};

const PADA_NAMES: Record<string, { en: string; hi: string }> = {
  N1: { en: 'Mukhya', hi: 'मुख्य' }, N2: { en: 'Bhallata', hi: 'भल्लाट' },
  N3: { en: 'Soma', hi: 'सोम' }, N4: { en: 'Diti', hi: 'दिति' },
  N5: { en: 'Aditi', hi: 'अदिति' }, N6: { en: 'Kubera', hi: 'कुबेर' },
  N7: { en: 'Isha', hi: 'ईश' }, N8: { en: 'Parjanya', hi: 'पर्जन्य' },
  E1: { en: 'Shikhi', hi: 'शिखी' }, E2: { en: 'Jayant', hi: 'जयन्त' },
  E3: { en: 'Aditya', hi: 'आदित्य' }, E4: { en: 'Surya', hi: 'सूर्य' },
  E5: { en: 'Satya', hi: 'सत्य' }, E6: { en: 'Bhrisha', hi: 'भृश' },
  E7: { en: 'Akasha', hi: 'आकाश' }, E8: { en: 'Anil', hi: 'अनिल' },
  S1: { en: 'Vitatha', hi: 'वितथ' }, S2: { en: 'Grihakshata', hi: 'गृहक्षत' },
  S3: { en: 'Yama', hi: 'यम' }, S4: { en: 'Gandharva', hi: 'गंधर्व' },
  S5: { en: 'Bhringaraja', hi: 'भृंगराज' }, S6: { en: 'Mriga', hi: 'मृग' },
  S7: { en: 'Nairuti', hi: 'नैऋति' }, S8: { en: 'Papayakshma', hi: 'पापयक्ष्मा' },
  W1: { en: 'Dauvarika', hi: 'दौवारिक' }, W2: { en: 'Shosha', hi: 'शोष' },
  W3: { en: 'Nairuti-W', hi: 'नैऋति-प' }, W4: { en: 'Varuna', hi: 'वरुण' },
  W5: { en: 'Asura', hi: 'असुर' }, W6: { en: 'Roga', hi: 'रोग' },
  W7: { en: 'Naga', hi: 'नाग' }, W8: { en: 'Pushpadant', hi: 'पुष्पदंत' },
};

function scoreColor(score: number): string {
  if (score >= 5) return '#d97706';  // gold
  if (score >= 4) return '#059669';  // emerald
  if (score >= 3) return '#3b82f6';  // blue
  if (score >= 2) return '#ea580c';  // orange
  return '#e11d48';                  // red
}

function polarToXY(cx: number, cy: number, r: number, angleDeg: number): { x: number; y: number } {
  const rad = ((angleDeg - 90) * Math.PI) / 180;  // -90 so 0° = top
  return { x: cx + r * Math.cos(rad), y: cy + r * Math.sin(rad) };
}

function arcPath(cx: number, cy: number, r: number, startAngle: number, endAngle: number): string {
  const start = polarToXY(cx, cy, r, startAngle);
  const end = polarToXY(cx, cy, r, endAngle);
  const sweep = endAngle - startAngle;
  const largeArc = sweep > 180 ? 1 : 0;
  return `M ${start.x} ${start.y} A ${r} ${r} 0 ${largeArc} 1 ${end.x} ${end.y}`;
}

function sectorPath(
  cx: number, cy: number, rInner: number, rOuter: number,
  startAngle: number, endAngle: number
): string {
  const outerStart = polarToXY(cx, cy, rOuter, startAngle);
  const outerEnd = polarToXY(cx, cy, rOuter, endAngle);
  const innerEnd = polarToXY(cx, cy, rInner, endAngle);
  const innerStart = polarToXY(cx, cy, rInner, startAngle);
  const sweep = endAngle - startAngle;
  const largeArc = sweep > 180 ? 1 : 0;
  return [
    `M ${outerStart.x} ${outerStart.y}`,
    `A ${rOuter} ${rOuter} 0 ${largeArc} 1 ${outerEnd.x} ${outerEnd.y}`,
    `L ${innerEnd.x} ${innerEnd.y}`,
    `A ${rInner} ${rInner} 0 ${largeArc} 0 ${innerStart.x} ${innerStart.y}`,
    'Z',
  ].join(' ');
}

export default function VastuCompass({ value, onChange, mode = 'select', highlightedPada, onPadaClick }: Props) {
  const { language } = useTranslation();
  const isHi = language === 'hi';
  const [hoveredPada, setHoveredPada] = useState<string | null>(null);

  const cx = 200, cy = 200;
  const rOuter = 175;
  const rMid = 130;
  const rInner = 90;
  const rCenter = 50;

  return (
    <div className="relative">
      <svg viewBox="0 0 400 400" className="w-full max-w-[400px] mx-auto">
        {/* Background circle */}
        <circle cx={cx} cy={cy} r={rOuter + 5} fill="#0f172a" stroke="#1e293b" strokeWidth={1} />

        {/* Pada ring — 32 sectors (8 per cardinal direction) */}
        {PADA_DIRECTIONS.map(dir => {
          const dirInfo = DIRECTIONS.find(d => d.code === dir)!;
          const baseAngle = dirInfo.angle - 45; // each cardinal spans 90°, centered on its angle
          return Array.from({ length: 8 }, (_, i) => {
            const padaCode = `${dir}${i + 1}`;
            const score = PADA_SCORES[padaCode] || 3;
            const startA = baseAngle + i * (90 / 8);
            const endA = startA + (90 / 8);
            const isHighlighted = highlightedPada === padaCode;
            const isHovered = hoveredPada === padaCode;
            const midAngle = (startA + endA) / 2;
            const labelPos = polarToXY(cx, cy, (rMid + rOuter) / 2, midAngle);

            return (
              <g key={padaCode}>
                <path
                  d={sectorPath(cx, cy, rMid, rOuter, startA, endA)}
                  fill={isHighlighted || isHovered ? scoreColor(score) : `${scoreColor(score)}33`}
                  stroke={isHighlighted ? '#fbbf24' : '#1e293b'}
                  strokeWidth={isHighlighted ? 2 : 0.5}
                  opacity={isHighlighted || isHovered ? 1 : 0.6}
                  className="cursor-pointer transition-opacity"
                  onMouseEnter={() => setHoveredPada(padaCode)}
                  onMouseLeave={() => setHoveredPada(null)}
                  onClick={() => {
                    if (mode === 'select') {
                      onChange(dir);
                      // Compute the mid-degree of this pada (normalize to 0-360)
                      const midDeg = ((midAngle % 360) + 360) % 360;
                      onPadaClick?.(padaCode, Math.round(midDeg * 100) / 100);
                    }
                  }}
                />
                <text
                  x={labelPos.x}
                  y={labelPos.y + 1}
                  textAnchor="middle"
                  dominantBaseline="middle"
                  fill={isHighlighted || isHovered ? '#fff' : '#94a3b8'}
                  fontSize="7"
                  fontWeight={isHighlighted ? '700' : '400'}
                  className="pointer-events-none select-none"
                >
                  {i + 1}
                </text>
              </g>
            );
          });
        })}

        {/* Main direction sectors */}
        {DIRECTIONS.map(dir => {
          const halfSpan = 22.5;
          const startA = dir.angle - halfSpan;
          const endA = dir.angle + halfSpan;
          const isActive = value === dir.code;
          const labelPos = polarToXY(cx, cy, (rInner + rMid) / 2, dir.angle);
          const namePos = polarToXY(cx, cy, rInner - 14, dir.angle);

          return (
            <g key={dir.code}>
              <path
                d={sectorPath(cx, cy, rInner, rMid, startA, endA)}
                fill={isActive ? '#78350f' : '#1e293b'}
                stroke={isActive ? '#d97706' : '#334155'}
                strokeWidth={isActive ? 2 : 0.5}
                className="cursor-pointer"
                onClick={() => onChange(dir.code)}
              />
              <text
                x={labelPos.x}
                y={labelPos.y - 2}
                textAnchor="middle"
                dominantBaseline="middle"
                fill={isActive ? '#fbbf24' : '#e2e8f0'}
                fontSize="11"
                fontWeight="700"
                className="pointer-events-none select-none"
              >
                {dir.code}
              </text>
              <text
                x={labelPos.x}
                y={labelPos.y + 10}
                textAnchor="middle"
                dominantBaseline="middle"
                fill={isActive ? '#fbbf24' : '#94a3b8'}
                fontSize="7"
                className="pointer-events-none select-none"
              >
                {isHi ? dir.hi : dir.en}
              </text>
            </g>
          );
        })}

        {/* Center — Brahma circle */}
        <circle cx={cx} cy={cy} r={rCenter} fill="#1c1917" stroke="#d97706" strokeWidth={1.5} />
        <text x={cx} y={cy - 6} textAnchor="middle" fill="#d97706" fontSize="10" fontWeight="700" className="select-none">
          {isHi ? 'ब्रह्म' : 'Brahma'}
        </text>
        <text x={cx} y={cy + 8} textAnchor="middle" fill="#a16207" fontSize="8" className="select-none">
          {isHi ? 'स्थान' : 'Sthana'}
        </text>

        {/* North pointer */}
        <polygon
          points={`${cx},${cy - rOuter - 10} ${cx - 6},${cy - rOuter + 2} ${cx + 6},${cy - rOuter + 2}`}
          fill="#e11d48"
          stroke="#f43f5e"
          strokeWidth={0.5}
        />
      </svg>

      {/* Hover tooltip */}
      {hoveredPada && (
        <div className="absolute top-2 left-1/2 -translate-x-1/2 bg-black/90 border border-white/20 rounded-lg px-3 py-2 text-center z-10">
          <p className="text-xs font-bold text-cosmic-text">{hoveredPada}</p>
          {PADA_NAMES[hoveredPada] && (
            <p className="text-[10px] text-sacred-gold">
              {isHi ? PADA_NAMES[hoveredPada].hi : PADA_NAMES[hoveredPada].en}
            </p>
          )}
          <div className="flex items-center gap-1 justify-center mt-0.5">
            {Array.from({ length: 5 }, (_, i) => (
              <div
                key={i}
                className="w-2 h-2 rounded-full"
                style={{
                  background: i < (PADA_SCORES[hoveredPada] || 0) ? scoreColor(PADA_SCORES[hoveredPada]) : '#334155',
                }}
              />
            ))}
          </div>
          <p className="text-[10px] text-cosmic-text/60 mt-0.5">
            {(PADA_SCORES[hoveredPada] || 0) >= 4 ? (isHi ? 'शुभ' : 'Auspicious')
              : (PADA_SCORES[hoveredPada] || 0) >= 3 ? (isHi ? 'सामान्य' : 'Neutral')
              : (isHi ? 'अशुभ' : 'Challenging')}
          </p>
        </div>
      )}
    </div>
  );
}
