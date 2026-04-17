interface PalmZone {
  zone_id: string; name: string; planet: string;
  svg_cx: number; svg_cy: number; svg_r: number; zone_type: string;
}
interface PalmMark { zone_id: string; mark_type: string; }

interface Props {
  zones: PalmZone[];
  marks: PalmMark[];
  onZoneClick: (zoneId: string) => void;
  selectedZone: string | null;
  language: string;
}

const PLANET_COLOR: Record<string, string> = {
  Jupiter: '#f59e0b', Saturn: '#6b7280', Sun: '#f97316', Mercury: '#22c55e',
  Venus: '#ec4899', Mars_inner: '#ef4444', Mars_outer: '#dc2626',
  Moon: '#93c5fd', Rahu: '#9333ea', Heart: '#f43f5e', Head: '#3b82f6',
  Life: '#10b981', Fate: '#8b5cf6', Sun_line: '#f97316',
};
const MARK_SYMBOL: Record<string, string> = {
  cross: '✕', star: '★', island: '◈', chain: '⊕', dot: '•',
  triangle: '△', square: '□', trident: 'ψ', circle: '○',
};

export default function PalmSVG({ zones, marks, onZoneClick, selectedZone, language }: Props) {
  const getZoneMarks = (zoneId: string) => marks.filter(m => m.zone_id === zoneId);

  return (
    <svg viewBox="0 0 220 300" className="w-full max-w-xs mx-auto" style={{ touchAction: 'manipulation' }}>
      {/* Palm outline */}
      <path
        d="M 60 260 Q 30 240 25 190 Q 20 150 30 120 Q 35 95 45 80 Q 50 60 55 45 Q 60 30 70 28 Q 82 26 85 45 Q 88 55 88 70 Q 90 50 95 35 Q 100 20 110 18 Q 122 16 125 35 Q 128 50 128 68 Q 130 48 135 33 Q 140 18 152 18 Q 164 16 167 35 Q 170 52 168 72 Q 172 52 178 40 Q 184 26 195 30 Q 207 34 210 55 Q 215 80 210 110 Q 205 140 198 170 Q 192 210 185 240 Q 178 260 160 270 Q 130 280 100 278 Q 75 275 60 260 Z"
        fill="#fde8d8" stroke="#d4a896" strokeWidth="1.5"
      />
      {/* Thumb */}
      <path
        d="M 55 45 Q 50 30 42 28 Q 28 26 22 45 Q 16 65 25 85 Q 35 100 50 100"
        fill="#fde8d8" stroke="#d4a896" strokeWidth="1.5"
      />
      {/* Faint anatomical line guides (heart/head/life/fate) */}
      <g opacity="0.25" fill="none" stroke="#8b5e3c" strokeWidth="1" strokeLinecap="round">
        <path d="M 55 108 Q 110 95 195 112" />
        <path d="M 60 145 Q 110 135 175 160" />
        <path d="M 85 90 Q 55 150 60 235" />
        <path d="M 120 265 Q 125 190 122 110" />
      </g>

      {/* Zones */}
      {zones.map((zone) => {
        const zoneMarks = getZoneMarks(zone.zone_id);
        const isSelected = selectedZone === zone.zone_id;
        const color = PLANET_COLOR[zone.planet ?? ''] || PLANET_COLOR[zone.name ?? ''] || '#94a3b8';

        if (zone.zone_type === 'line') {
          return (
            <g key={zone.zone_id}>
              <circle
                cx={zone.svg_cx} cy={zone.svg_cy} r={zone.svg_r || 12}
                fill={isSelected ? color : color + '30'}
                stroke={color} strokeWidth={isSelected ? 2 : 1}
                className="cursor-pointer transition-all"
                onClick={() => onZoneClick(zone.zone_id)}
              />
              {zoneMarks.length > 0 && (
                <text x={zone.svg_cx} y={zone.svg_cy + 4} textAnchor="middle"
                  fontSize="8" fill={color} fontWeight="bold">
                  {MARK_SYMBOL[zoneMarks[0].mark_type] || '•'}
                </text>
              )}
            </g>
          );
        }

        return (
          <g key={zone.zone_id}>
            <circle
              cx={zone.svg_cx} cy={zone.svg_cy} r={zone.svg_r || 18}
              fill={isSelected ? color + '60' : color + '25'}
              stroke={color} strokeWidth={isSelected ? 2.5 : 1.5}
              strokeDasharray={isSelected ? '0' : '3 2'}
              className="cursor-pointer transition-all hover:fill-current"
              onClick={() => onZoneClick(zone.zone_id)}
            />
            <text x={zone.svg_cx} y={zone.svg_cy + 1} textAnchor="middle"
              fontSize="6.5" fill={color} fontWeight="700" className="pointer-events-none"
              style={{ letterSpacing: '-0.2px' }}>
              {(zone.planet ?? '').replace('_inner', ' In').replace('_outer', ' Out').replace('_line', '')}
            </text>
            {zoneMarks.length > 0 && (
              <text x={zone.svg_cx} y={zone.svg_cy + 10} textAnchor="middle"
                fontSize="9" fill={color} fontWeight="bold" className="pointer-events-none">
                {MARK_SYMBOL[zoneMarks[0].mark_type] || '•'}
              </text>
            )}
          </g>
        );
      })}

      {/* Tap hint */}
      <text x="110" y="295" textAnchor="middle" fontSize="7" fill="#94a3b8">
        {language === 'hi' ? 'क्षेत्र पर टैप करें' : 'Tap a zone to add mark'}
      </text>
    </svg>
  );
}
