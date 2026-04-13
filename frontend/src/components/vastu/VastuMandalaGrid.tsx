import { useState } from 'react';
import { useTranslation } from '@/lib/i18n';
import { X } from 'lucide-react';

/**
 * Interactive 9x9 Vastu Purusha Mandala SVG grid.
 * 45 Devtas placed in their traditional grid positions.
 * Color-coded by nature, clickable for detail popover.
 */

interface DevtaCell {
  id: number;
  name: string;
  name_hi: string;
  zone: string;
  zone_hi: string;
  direction: string;
  direction_hi: string;
  element: string;
  element_hi: string;
  nature: string;
  energy_type: string;
  body_part: string;
  body_part_hi: string;
  mantra: string;
  description_en: string;
  description_hi: string;
}

interface Props {
  zones: Record<string, { devtas: DevtaCell[] }>;
}

// Build grid map from zones data
function buildGridMap(zones: Props['zones']): Map<string, DevtaCell> {
  const map = new Map<string, DevtaCell>();

  // Hardcoded grid positions matching data.py DEVTAS_45 grid_positions
  // row,col → devta id
  const GRID: Record<string, number> = {
    // Row 0 (top = NW → N → NE)
    '0,0': 34, '0,1': 36, '0,2': 41, '0,3': 40, '0,4': 38, '0,5': 39, '0,6': 13, '0,7': 10,
    // Row 1
    '1,0': 35, '1,1': 37, '1,6': 12, '1,7': 11,
    // Row 2
    '2,0': 33, '2,1': 42, '2,7': 43, '2,8': 15,
    // Row 3
    '3,0': 32, '3,3': 4, '3,4': 7, '3,5': 3, '3,8': 14,
    // Row 4
    '4,0': 30, '4,3': 9, '4,4': 6, '4,5': 8, '4,8': 16,
    // Row 5
    '5,0': 31, '5,3': 2, '5,4': 1, '5,5': 5, '5,8': 17,
    // Row 6
    '6,0': 27, '6,1': 29, '6,6': 21, '6,7': 19,
    // Row 7
    '7,0': 26, '7,1': 28, '7,3': 45, '7,4': 44, '7,5': 25, '7,6': 20, '7,7': 18,
    // Row 8
    '8,3': 23, '8,4': 22, '8,5': 24,
  };

  // Flatten all devtas from zones
  const allDevtas: DevtaCell[] = [];
  for (const zone of Object.values(zones)) {
    allDevtas.push(...zone.devtas);
  }

  for (const [key, id] of Object.entries(GRID)) {
    const devta = allDevtas.find(d => d.id === id);
    if (devta) map.set(key, devta);
  }
  return map;
}

const NATURE_COLORS: Record<string, { fill: string; stroke: string; text: string }> = {
  supreme:  { fill: '#78350f', stroke: '#d97706', text: '#fbbf24' },  // amber
  positive: { fill: '#064e3b', stroke: '#059669', text: '#34d399' },  // emerald
  neutral:  { fill: '#1e3a5f', stroke: '#3b82f6', text: '#93c5fd' },  // blue
  negative: { fill: '#4c0519', stroke: '#e11d48', text: '#fb7185' },  // red
  fierce:   { fill: '#431407', stroke: '#ea580c', text: '#fb923c' },  // orange
};

const EMPTY_CELL = { fill: '#0f172a', stroke: '#1e293b', text: '#475569' };

// Direction labels for the grid edges
const DIR_LABELS = [
  { x: 0, y: -12, text: 'NW / वायव्य', anchor: 'start' },
  { x: 225, y: -12, text: 'N / उत्तर', anchor: 'middle' },
  { x: 450, y: -12, text: 'NE / ईशान', anchor: 'end' },
  { x: -8, y: 230, text: 'W', anchor: 'end', rotate: -90 },
  { x: 458, y: 230, text: 'E', anchor: 'start', rotate: 90 },
  { x: 0, y: 468, text: 'SW / नैऋत्य', anchor: 'start' },
  { x: 225, y: 468, text: 'S / दक्षिण', anchor: 'middle' },
  { x: 450, y: 468, text: 'SE / आग्नेय', anchor: 'end' },
];

export default function VastuMandalaGrid({ zones }: Props) {
  const { language } = useTranslation();
  const isHi = language === 'hi';
  const [selected, setSelected] = useState<DevtaCell | null>(null);

  const gridMap = buildGridMap(zones);

  const [hovered, setHovered] = useState<string | null>(null);

  const cellSize = 62;
  const gap = 0;
  const gridPx = 9 * cellSize;

  return (
    <div className="space-y-4">
      {/* Legend */}
      <div className="flex flex-wrap gap-3 justify-center text-sm">
        {Object.entries(NATURE_COLORS).map(([nature, c]) => (
          <div key={nature} className="flex items-center gap-1.5">
            <div className="w-3 h-3 rounded" style={{ background: c.fill, border: `1px solid ${c.stroke}` }} />
            <span className="text-cosmic-text capitalize">{nature}</span>
          </div>
        ))}
        <div className="flex items-center gap-1.5">
          <div className="w-3 h-3 rounded" style={{ background: EMPTY_CELL.fill, border: `1px solid ${EMPTY_CELL.stroke}` }} />
          <span className="text-cosmic-text">{isHi ? 'खाली' : 'Empty'}</span>
        </div>
      </div>

      {/* SVG Grid */}
      <div className="overflow-x-auto">
        <div className="min-w-[560px] mx-auto" style={{ maxWidth: gridPx + 50 }}>
          <svg
            viewBox={`-25 -25 ${gridPx + 50} ${gridPx + 50}`}
            className="w-full"
            style={{ maxHeight: 640 }}
          >
            {/* Direction labels */}
            {DIR_LABELS.map((lbl, i) => (
              <text
                key={i}
                x={lbl.x}
                y={lbl.y}
                textAnchor={lbl.anchor as any}
                fill="#d97706"
                fontSize="11"
                fontWeight="700"
                transform={lbl.rotate ? `rotate(${lbl.rotate}, ${lbl.x}, ${lbl.y})` : undefined}
              >
                {lbl.text}
              </text>
            ))}

            {/* Grid cells */}
            {Array.from({ length: 9 }, (_, r) =>
              Array.from({ length: 9 }, (_, c) => {
                const key = `${r},${c}`;
                const devta = gridMap.get(key);
                const colors = devta ? (NATURE_COLORS[devta.nature] || NATURE_COLORS.neutral) : EMPTY_CELL;
                const x = c * cellSize;
                const y = r * cellSize;
                const isCenter = r >= 3 && r <= 5 && c >= 3 && c <= 5;
                const isSelected = selected?.id === devta?.id;
                const isHov = hovered === key && !!devta;

                return (
                  <g
                    key={key}
                    onMouseEnter={() => devta && setHovered(key)}
                    onMouseLeave={() => setHovered(null)}
                  >
                    <rect
                      x={x + 0.5}
                      y={y + 0.5}
                      width={cellSize - 1}
                      height={cellSize - 1}
                      rx={4}
                      fill={isHov ? colors.stroke : colors.fill}
                      stroke={isSelected ? '#fbbf24' : isHov ? '#fbbf24' : colors.stroke}
                      strokeWidth={isSelected ? 2.5 : isHov ? 1.5 : isCenter && devta ? 1.5 : 0.5}
                      opacity={devta ? 1 : 0.25}
                      className={devta ? 'cursor-pointer transition-all duration-150' : ''}
                      onClick={() => devta && setSelected(devta)}
                    />
                    {devta && (
                      <>
                        <text
                          x={x + cellSize / 2}
                          y={y + 18}
                          textAnchor="middle"
                          fill={isHov ? '#fff' : colors.text}
                          fontSize={devta.name.length > 8 ? 8 : 10}
                          fontWeight="700"
                          className="pointer-events-none select-none"
                        >
                          {devta.name}
                        </text>
                        <text
                          x={x + cellSize / 2}
                          y={y + 32}
                          textAnchor="middle"
                          fill={isHov ? '#fde68a' : colors.text}
                          fontSize={devta.name_hi.length > 6 ? 8 : 9}
                          fontWeight="600"
                          opacity={0.85}
                          className="pointer-events-none select-none"
                        >
                          {devta.name_hi}
                        </text>
                        <text
                          x={x + cellSize / 2}
                          y={y + cellSize - 10}
                          textAnchor="middle"
                          fill={colors.text}
                          fontSize="8"
                          opacity={0.5}
                          className="pointer-events-none select-none"
                        >
                          {isHi ? devta.element_hi : devta.element}
                        </text>
                      </>
                    )}
                  </g>
                );
              })
            )}

            {/* Brahma Sthana border */}
            <rect
              x={3 * cellSize - 1}
              y={3 * cellSize - 1}
              width={3 * cellSize + 2}
              height={3 * cellSize + 2}
              rx={5}
              fill="none"
              stroke="#d97706"
              strokeWidth={2.5}
              strokeDasharray="8 4"
              opacity={0.7}
            />
            <text
              x={4.5 * cellSize}
              y={3 * cellSize - 6}
              textAnchor="middle"
              fill="#d97706"
              fontSize="10"
              fontWeight="700"
            >
              {isHi ? 'ब्रह्म स्थान' : 'Brahma Sthana'}
            </text>
          </svg>
        </div>
      </div>

      {/* Selected Devta Detail */}
      {selected && (
        <div className="bg-white/5 border border-sacred-gold/30 rounded-xl p-5 relative">
          <button
            onClick={() => setSelected(null)}
            className="absolute top-3 right-3 text-cosmic-text/40 hover:text-white"
          >
            <X className="w-4 h-4" />
          </button>
          <div className="flex items-center gap-3 mb-3">
            <div
              className="w-3 h-3 rounded"
              style={{
                background: (NATURE_COLORS[selected.nature] || NATURE_COLORS.neutral).fill,
                border: `2px solid ${(NATURE_COLORS[selected.nature] || NATURE_COLORS.neutral).stroke}`,
              }}
            />
            <h4 className="text-lg font-bold text-cosmic-text">{selected.name}</h4>
            <span className="text-sm text-cosmic-text/60">{selected.name_hi}</span>
            <span className="ml-auto text-sm px-2 py-0.5 rounded bg-white/10 text-cosmic-text capitalize">{selected.nature}</span>
          </div>
          <p className="text-sm text-cosmic-text leading-relaxed mb-3">
            {isHi ? selected.description_hi : selected.description_en}
          </p>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-sm">
            <div>
              <p className="text-cosmic-text/50">{isHi ? 'क्षेत्र' : 'Zone'}</p>
              <p className="font-semibold text-cosmic-text">{isHi ? selected.zone_hi : selected.zone}</p>
            </div>
            <div>
              <p className="text-cosmic-text/50">{isHi ? 'दिशा' : 'Direction'}</p>
              <p className="font-semibold text-cosmic-text">{isHi ? selected.direction_hi : selected.direction}</p>
            </div>
            <div>
              <p className="text-cosmic-text/50">{isHi ? 'तत्व' : 'Element'}</p>
              <p className="font-semibold text-cosmic-text">{isHi ? selected.element_hi : selected.element}</p>
            </div>
            <div>
              <p className="text-cosmic-text/50">{isHi ? 'शरीर अंग' : 'Body Part'}</p>
              <p className="font-semibold text-cosmic-text">{isHi ? selected.body_part_hi : selected.body_part}</p>
            </div>
          </div>
          <p className="text-sm text-sacred-gold/60 italic mt-3">{selected.mantra}</p>
        </div>
      )}
    </div>
  );
}
