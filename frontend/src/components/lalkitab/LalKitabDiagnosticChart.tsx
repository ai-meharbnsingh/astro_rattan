import { useMemo } from 'react';
import { useTranslation } from '@/lib/i18n';
import { translatePlanetAbbr } from '@/lib/backend-translations';

interface PlanetPos {
  planet: string;
  house: number;
}

interface MasnuiPlanet {
  house: number;
  formed_by: string[];
  masnui_planet: string;
  affected_domain: { en: string; hi: string };
}

interface Props {
  type: 'andha' | 'masnui' | 'dharmi';
  planetPositions: PlanetPos[];
  masnuiData?: MasnuiPlanet[];
  dharmiData?: { is_dharmi: boolean };
}

const NI_SIZE = 400;
const NI_PAD = 10;
const NI_INNER = NI_SIZE - NI_PAD * 2; // 380

// Key points
const TL = { x: NI_PAD, y: NI_PAD };
const TR = { x: NI_PAD + NI_INNER, y: NI_PAD };
const BL = { x: NI_PAD, y: NI_PAD + NI_INNER };
const BR = { x: NI_PAD + NI_INNER, y: NI_PAD + NI_INNER };
const MT = { x: NI_PAD + NI_INNER / 2, y: NI_PAD };
const MR = { x: NI_PAD + NI_INNER, y: NI_PAD + NI_INNER / 2 };
const MB = { x: NI_PAD + NI_INNER / 2, y: NI_PAD + NI_INNER };
const ML = { x: NI_PAD, y: NI_PAD + NI_INNER / 2 };
const CC = { x: NI_PAD + NI_INNER / 2, y: NI_PAD + NI_INNER / 2 };

// Intersections for trapezoids
const P1 = { x: NI_PAD + NI_INNER / 4, y: NI_PAD + NI_INNER / 4 };
const P2 = { x: NI_PAD + (NI_INNER * 3) / 4, y: NI_PAD + NI_INNER / 4 };
const P3 = { x: NI_PAD + (NI_INNER * 3) / 4, y: NI_PAD + (NI_INNER * 3) / 4 };
const P4 = { x: NI_PAD + NI_INNER / 4, y: NI_PAD + (NI_INNER * 3) / 4 };

const pts = (...coords: { x: number; y: number }[]) => coords.map(c => `${c.x},${c.y}`).join(' ');

const HOUSE_POLYGONS: Record<number, string> = {
  1: pts(P1, MT, P2, CC),
  2: pts(TL, MT, P1),
  3: pts(ML, TL, P1),
  4: pts(P4, ML, P1, CC),
  5: pts(BL, ML, P4),
  6: pts(MB, BL, P4),
  7: pts(P3, MB, P4, CC),
  8: pts(BR, MB, P3),
  9: pts(MR, BR, P3),
  10: pts(P2, MR, P3, CC),
  11: pts(TR, MR, P2),
  12: pts(MT, TR, P2),
};

const HOUSE_CENTROIDS: Record<number, { x: number; y: number }> = {
  1: { x: 200, y: 130 },
  2: { x: 100, y: 50 },
  3: { x: 50, y: 100 },
  4: { x: 130, y: 200 },
  5: { x: 50, y: 300 },
  6: { x: 100, y: 350 },
  7: { x: 200, y: 270 },
  8: { x: 300, y: 350 },
  9: { x: 350, y: 300 },
  10: { x: 270, y: 200 },
  11: { x: 350, y: 100 },
  12: { x: 300, y: 50 },
};

const PLANET_COLORS: Record<string, string> = {
  Sun: '#E65100', Moon: '#1565C0', Mars: '#C62828',
  Mercury: '#2E7D32', Jupiter: '#F9A825', Venus: '#E91E63',
  Saturn: '#1565C0', Rahu: '#616161', Ketu: '#795548',
};

export default function LalKitabDiagnosticChart({ type, planetPositions, masnuiData, dharmiData }: Props) {
  const { language } = useTranslation();

  const planetsByHouse = useMemo(() => {
    const map: Record<number, string[]> = {};
    planetPositions.forEach(p => {
      if (!map[p.house]) map[p.house] = [];
      map[p.house].push(p.planet);
    });
    return map;
  }, [planetPositions]);

  return (
    <div className="relative w-full max-w-[260px] mx-auto bg-parchment rounded-xl shadow-inner border border-sacred-gold/20 overflow-hidden">
      <svg viewBox={`0 0 ${NI_SIZE} ${NI_SIZE}`} className="w-full h-auto">
        <defs>
          <filter id="glow-gold">
            <feGaussianBlur stdDeviation="3" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
          <radialGradient id="fog-grad">
            <stop offset="0%" stopColor="#4A5568" stopOpacity="0.6" />
            <stop offset="100%" stopColor="#2D3748" stopOpacity="0.1" />
          </radialGradient>
        </defs>

        {/* Background */}
        <rect width={NI_SIZE} height={NI_SIZE} fill="#FDF6E3" />

        {/* House Highlighting */}
        {type === 'andha' && (
          <polygon points={HOUSE_POLYGONS[10]} fill="url(#fog-grad)" className="animate-pulse" />
        )}

        {/* Grid Lines */}
        <line x1={TL.x} y1={TL.y} x2={BR.x} y2={BR.y} stroke="#3D2B1F" strokeWidth="1.5" />
        <line x1={TR.x} y1={TR.y} x2={BL.x} y2={BL.y} stroke="#3D2B1F" strokeWidth="1.5" />
        <path d={`M ${MT.x} ${MT.y} L ${MR.x} ${MR.y} L ${MB.x} ${MB.y} L ${ML.x} ${ML.y} Z`} fill="none" stroke="#3D2B1F" strokeWidth="1.5" />
        <rect x={NI_PAD} y={NI_PAD} width={NI_INNER} height={NI_INNER} fill="none" stroke="#3D2B1F" strokeWidth="2" />

        {/* House Numbers */}
        {Object.entries(HOUSE_CENTROIDS).map(([h, pos]) => (
          <text key={h} x={pos.x} y={pos.y + 20} textAnchor="middle" fontSize="12" fill="#8B7355" opacity="0.4" fontWeight="bold">
            {h}
          </text>
        ))}

        {/* Protective Beams (Dharmi) */}
        {type === 'dharmi' && dharmiData?.is_dharmi && (
          <g>
            {(() => {
              const jupH = planetPositions.find(p => p.planet === 'Jupiter')?.house;
              const satH = planetPositions.find(p => p.planet === 'Saturn')?.house;
              if (jupH && satH) {
                const p1 = HOUSE_CENTROIDS[jupH];
                const p2 = HOUSE_CENTROIDS[satH];
                return (
                  <line 
                    x1={p1.x} y1={p1.y} x2={p2.x} y2={p2.y} 
                    stroke="#D4AF37" strokeWidth="4" strokeDasharray="8,4" 
                    filter="url(#glow-gold)" opacity="0.6"
                    className="animate-pulse"
                  />
                );
              }
              return null;
            })()}
          </g>
        )}

        {/* Planets */}
        {Object.entries(planetsByHouse).map(([h, planets]) => {
          const houseNum = parseInt(h);
          const centroid = HOUSE_CENTROIDS[houseNum];
          
          return planets.map((p, idx) => {
            const isMasnuiIngredient = type === 'masnui' && masnuiData?.some(m => m.house === houseNum && m.formed_by.includes(p));
            const color = PLANET_COLORS[p] || '#3D2B1F';
            const x = centroid.x + (idx % 2 === 0 ? -12 : 12);
            const y = centroid.y + (idx < 2 ? -8 : 12);

            return (
              <text
                key={`${p}-${h}-${idx}`}
                x={x}
                y={y}
                textAnchor="middle"
                fill={color}
                fontSize="14"
                fontWeight="bold"
                opacity={isMasnuiIngredient ? 0.3 : 1}
              >
                {translatePlanetAbbr(p, language)}
              </text>
            );
          });
        })}

        {/* Masnui Planets Overlay */}
        {type === 'masnui' && masnuiData?.map((m, idx) => {
          const centroid = HOUSE_CENTROIDS[m.house];
          return (
            <g key={`masnui-${idx}`} filter="url(#glow-gold)">
              <circle cx={centroid.x} cy={centroid.y} r="18" fill="white" fillOpacity="0.8" stroke="#D4AF37" strokeWidth="1" />
              <text
                x={centroid.x}
                y={centroid.y + 5}
                textAnchor="middle"
                fill={PLANET_COLORS[m.masnui_planet] || '#D4AF37'}
                fontSize="16"
                fontWeight="black"
              >
                {translatePlanetAbbr(m.masnui_planet, language)}
              </text>
              <text x={centroid.x} y={centroid.y - 12} textAnchor="middle" fontSize="8" fill="#D4AF37" fontWeight="bold">MASNUI</text>
            </g>
          );
        })}
      </svg>
      
      {/* Label Overlay */}
      <div className="absolute top-2 left-2 px-2 py-0.5 rounded bg-black/60 text-[10px] text-white font-bold uppercase tracking-widest backdrop-blur-sm">
        {type === 'andha' ? 'Blindness Map' : type === 'masnui' ? 'Alchemy Map' : 'Protection Map'}
      </div>
    </div>
  );
}
