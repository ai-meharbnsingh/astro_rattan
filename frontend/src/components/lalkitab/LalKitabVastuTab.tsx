import { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import { Loader2, Home, AlertTriangle, CheckCircle2, Compass, Wrench, LayoutGrid } from 'lucide-react';

// ─── Types ───────────────────────────────────────────────────────────────────

interface DirectionEntry {
  house: number;
  direction: { en: string; hi: string };
  zone: { en: string; hi: string };
  planets: string[];
  is_empty: boolean;
}

interface PlanetWarning {
  planet: string;
  house: number;
  direction: { en: string; hi: string };
  zone: { en: string; hi: string };
  warning: { en: string; hi: string };
  fix: { en: string; hi: string };
  is_critical: boolean;
}

interface VastuData {
  directional_map: DirectionEntry[];
  planet_warnings: PlanetWarning[];
  priority_fixes: PlanetWarning[];
  general_layout: { house: number; direction: { en: string; hi: string }; tip: { en: string; hi: string } }[];
  total_warnings: number;
  critical_count: number;
}

interface Props { kundliId?: string; language: string; }

// ─── Planet colors (hex for SVG + CSS) ───────────────────────────────────────

const PLANET_HEX: Record<string, string> = {
  Sun: '#f97316', Moon: '#60a5fa', Mars: '#ef4444',
  Mercury: '#22c55e', Jupiter: '#eab308', Venus: '#ec4899',
  Saturn: '#6b7280', Rahu: '#9333ea', Ketu: '#b45309',
};
const PLANET_CSS: Record<string, string> = {
  Sun: 'text-orange-500', Moon: 'text-blue-400', Mars: 'text-red-500',
  Mercury: 'text-green-500', Jupiter: 'text-yellow-500', Venus: 'text-pink-500',
  Saturn: 'text-gray-500', Rahu: 'text-purple-600', Ketu: 'text-amber-700',
};

// ─── Vastu Score ─────────────────────────────────────────────────────────────

function vastuScore(warnings: PlanetWarning[]): number {
  const deductions = warnings.reduce((acc, w) => acc + (w.is_critical ? 15 : 7), 0);
  return Math.max(0, 100 - deductions);
}

// ─── SVG Compass ─────────────────────────────────────────────────────────────
// H1=East, H4=South, H7=West, H10=North (classical LK mapping)
// 30° per house, clockwise from East (0°)

const CX = 140, CY = 140, OUTER_R = 122, INNER_R = 50, MID_R = 88;

function segPath(i: number, r1: number, r2: number): string {
  const s = ((i) * 30) * Math.PI / 180;
  const e = ((i + 1) * 30) * Math.PI / 180;
  const x1 = CX + r2 * Math.cos(s), y1 = CY + r2 * Math.sin(s);
  const x2 = CX + r2 * Math.cos(e), y2 = CY + r2 * Math.sin(e);
  const xi1 = CX + r1 * Math.cos(s), yi1 = CY + r1 * Math.sin(s);
  const xi2 = CX + r1 * Math.cos(e), yi2 = CY + r1 * Math.sin(e);
  return `M ${xi1} ${yi1} L ${x1} ${y1} A ${r2} ${r2} 0 0 1 ${x2} ${y2} L ${xi2} ${yi2} A ${r1} ${r1} 0 0 0 ${xi1} ${yi1} Z`;
}

function midPoint(i: number, r: number) {
  const a = ((i + 0.5) * 30) * Math.PI / 180;
  return { x: CX + r * Math.cos(a), y: CY + r * Math.sin(a), a };
}

interface CompassProps {
  map: DirectionEntry[];
  warnings: PlanetWarning[];
  hi: boolean;
}

function VastuCompass({ map, warnings, hi }: CompassProps) {
  const warnHouses = new Set(warnings.map(w => w.house));
  const critHouses = new Set(warnings.filter(w => w.is_critical).map(w => w.house));
  const [hovered, setHovered] = useState<number | null>(null);

  // Compass label positions (outside the wheel)
  const compassLabels = [
    { label: 'E', angle: 0, hi: 'पूर्व' },
    { label: 'SE', angle: 45, hi: 'द.पू.' },
    { label: 'S', angle: 90, hi: 'दक्षिण' },
    { label: 'SW', angle: 135, hi: 'द.प.' },
    { label: 'W', angle: 180, hi: 'पश्चिम' },
    { label: 'NW', angle: 225, hi: 'उ.प.' },
    { label: 'N', angle: 270, hi: 'उत्तर' },
    { label: 'NE', angle: 315, hi: 'उ.पू.' },
  ];

  return (
    <div className="relative">
      <svg viewBox="0 0 280 280" className="w-full max-w-[320px] mx-auto">
        {/* Background */}
        <circle cx={CX} cy={CY} r={OUTER_R + 18} fill="#fffbf5" />

        {/* Compass ring labels */}
        {compassLabels.map(({ label, angle, hi: hiLabel }) => {
          const rad = angle * Math.PI / 180;
          const lx = CX + (OUTER_R + 12) * Math.cos(rad);
          const ly = CY + (OUTER_R + 12) * Math.sin(rad);
          return (
            <text key={label} x={lx} y={ly + 3.5} textAnchor="middle" fontSize="8.5"
              fontWeight="600" fill="#9ca3af">
              {hi ? hiLabel : label}
            </text>
          );
        })}

        {/* 12 house segments */}
        {map.map((entry, i) => {
          const isCrit = critHouses.has(entry.house);
          const isWarn = warnHouses.has(entry.house);
          const isHov = hovered === entry.house;

          const fill = isCrit
            ? (isHov ? '#fecaca' : '#fee2e2')
            : isWarn
              ? (isHov ? '#fef08a' : '#fef9c3')
              : entry.is_empty
                ? (isHov ? '#f3f4f6' : '#f9fafb')
                : (isHov ? '#fef3c7' : '#fffbeb');

          const stroke = isCrit ? '#ef4444' : isWarn ? '#ca8a04' : '#e5e7eb';
          const strokeW = isCrit ? 1.5 : isWarn ? 1 : 0.5;

          const mid = midPoint(i, MID_R);
          const labelMid = midPoint(i, MID_R - 16);

          return (
            <g key={entry.house}
              style={{ cursor: 'pointer' }}
              onMouseEnter={() => setHovered(entry.house)}
              onMouseLeave={() => setHovered(null)}
            >
              <path d={segPath(i, INNER_R, OUTER_R)} fill={fill} stroke={stroke} strokeWidth={strokeW} />

              {/* House number */}
              <text x={labelMid.x} y={labelMid.y + 4} textAnchor="middle" fontSize="9.5"
                fontWeight="bold" fill={isCrit ? '#dc2626' : isWarn ? '#92400e' : '#374151'}>
                H{entry.house}
              </text>

              {/* Warning badge */}
              {isCrit && (
                <text x={mid.x} y={mid.y + 4} textAnchor="middle" fontSize="9" fill="#dc2626">⚠</text>
              )}
              {isWarn && !isCrit && (
                <text x={mid.x} y={mid.y + 4} textAnchor="middle" fontSize="9" fill="#ca8a04">!</text>
              )}

              {/* Planet dots */}
              {!isWarn && !isCrit && entry.planets.slice(0, 2).map((p, pi) => {
                const offset = entry.planets.length === 1 ? 0 : (pi === 0 ? -5 : 5);
                const pr = MID_R + 6;
                const pr2 = MID_R - 8;
                const dotR = pi === 0 ? pr : pr2;
                return (
                  <circle key={p}
                    cx={CX + dotR * Math.cos(mid.a) + (entry.planets.length > 1 ? offset * Math.cos(mid.a + Math.PI / 2) : 0)}
                    cy={CY + dotR * Math.sin(mid.a) + (entry.planets.length > 1 ? offset * Math.sin(mid.a + Math.PI / 2) : 0)}
                    r="4.5" fill={PLANET_HEX[p] || '#6b7280'}
                  />
                );
              })}
            </g>
          );
        })}

        {/* Inner center circle */}
        <circle cx={CX} cy={CY} r={INNER_R} fill="white" stroke="#d97706" strokeWidth="1.5" />
        <text x={CX} y={CY - 9} textAnchor="middle" fontSize="8" fill="#92400e" fontWeight="600">
          {hi ? 'आपका' : 'Your'}
        </text>
        <text x={CX} y={CY + 4} textAnchor="middle" fontSize="11" fill="#c45a00" fontWeight="800">
          {hi ? 'घर' : 'Home'}
        </text>
        <text x={CX} y={CY + 16} textAnchor="middle" fontSize="7.5" fill="#d97706">
          {hi ? 'वास्तु' : 'Vastu'}
        </text>

        {/* N arrow */}
        <g transform={`translate(${CX},${CY - OUTER_R - 3}) rotate(0)`}>
          <polygon points="0,-7 3,2 0,0 -3,2" fill="#ef4444" />
        </g>
      </svg>

      {/* Hover tooltip */}
      {hovered !== null && (() => {
        const entry = map.find(m => m.house === hovered);
        if (!entry) return null;
        const warn = warnings.find(w => w.house === hovered);
        return (
          <div className="absolute bottom-0 left-0 right-0 mx-4 bg-white border border-sacred-gold/30 rounded-xl p-3 shadow-lg text-xs pointer-events-none">
            <div className="flex items-center gap-2 mb-1">
              <span className="font-bold text-sacred-gold">H{entry.house}</span>
              <span className="text-muted-foreground">{hi ? entry.direction.hi : entry.direction.en}</span>
              <span className="text-muted-foreground">· {hi ? entry.zone.hi : entry.zone.en}</span>
            </div>
            {entry.planets.length > 0
              ? <div className="flex gap-1">{entry.planets.map(p => <span key={p} className={`font-semibold ${PLANET_CSS[p] ?? ''}`}>{p}</span>)}</div>
              : <span className="text-muted-foreground">{hi ? 'खाली' : 'Empty house'}</span>
            }
            {warn && <p className="mt-1 text-orange-700">{hi ? warn.warning.hi : warn.warning.en}</p>}
          </div>
        );
      })()}
    </div>
  );
}

// ─── 3×3 Home Floor Plan ─────────────────────────────────────────────────────
// Maps LK houses to a Vastu Purush Mandala grid

const GRID_CELLS: { pos: [number, number]; houses: number[]; dir: string; dir_hi: string; icon: string }[] = [
  { pos: [0, 2], houses: [11, 12], dir: 'North-East', dir_hi: 'उत्तर-पूर्व', icon: '↗' },
  { pos: [1, 2], houses: [9, 10], dir: 'North', dir_hi: 'उत्तर', icon: '↑' },
  { pos: [2, 2], houses: [6],     dir: 'North-West', dir_hi: 'उत्तर-पश्चिम', icon: '↖' },
  { pos: [0, 1], houses: [1],     dir: 'East', dir_hi: 'पूर्व', icon: '→' },
  { pos: [1, 1], houses: [],      dir: 'Center', dir_hi: 'केंद्र', icon: '◇' },
  { pos: [2, 1], houses: [5, 7],  dir: 'West', dir_hi: 'पश्चिम', icon: '←' },
  { pos: [0, 0], houses: [2],     dir: 'South-East', dir_hi: 'दक्षिण-पूर्व', icon: '↘' },
  { pos: [1, 0], houses: [3],     dir: 'South', dir_hi: 'दक्षिण', icon: '↓' },
  { pos: [2, 0], houses: [4, 8],  dir: 'South-West', dir_hi: 'दक्षिण-पश्चिम', icon: '↙' },
];

interface FloorPlanProps {
  map: DirectionEntry[];
  warnings: PlanetWarning[];
  hi: boolean;
}

function HomeFloorPlan({ map, warnings, hi }: FloorPlanProps) {
  const warnHouses = new Set(warnings.map(w => w.house));
  const critHouses = new Set(warnings.filter(w => w.is_critical).map(w => w.house));

  return (
    <div className="grid grid-cols-3 gap-1.5">
      {GRID_CELLS.map(cell => {
        const { pos, houses, dir, dir_hi, icon } = cell;
        const isCenter = houses.length === 0;
        const planets = houses.flatMap(h => map.find(m => m.house === h)?.planets ?? []);
        const hasCrit = houses.some(h => critHouses.has(h));
        const hasWarn = houses.some(h => warnHouses.has(h));

        const colStart = pos[0] + 1;
        const rowStart = 3 - pos[1]; // flip Y axis (row 0 = bottom = South, row 2 = top = North)

        const bg = isCenter
          ? 'bg-sacred-gold/5 border-sacred-gold/20'
          : hasCrit
            ? 'bg-red-50 border-red-300'
            : hasWarn
              ? 'bg-yellow-50 border-yellow-300'
              : 'bg-card border-border';

        return (
          <div
            key={dir}
            style={{ gridColumn: colStart, gridRow: rowStart }}
            className={`rounded-xl border p-2.5 min-h-[80px] flex flex-col justify-between ${bg}`}
          >
            <div className="flex items-center justify-between">
              <span className="text-sm font-bold text-muted-foreground/60">{icon}</span>
              {(hasCrit || hasWarn) && (
                <span className={`text-xs font-bold ${hasCrit ? 'text-red-600' : 'text-yellow-600'}`}>
                  {hasCrit ? '⚠' : '!'}
                </span>
              )}
            </div>
            <div>
              {!isCenter && houses.map(h => (
                <span key={h} className="text-xs font-semibold text-muted-foreground/70 mr-1">H{h}</span>
              ))}
              <div className="text-xs font-semibold text-foreground mt-0.5 leading-tight">
                {hi ? dir_hi : dir.split(' ').map(w => w.charAt(0) + w.slice(1)).join(' ')}
              </div>
              {!isCenter && planets.length > 0 && (
                <div className="flex flex-wrap gap-0.5 mt-1">
                  {planets.slice(0, 3).map(p => (
                    <span key={p} className={`text-[10px] font-bold ${PLANET_CSS[p] ?? 'text-foreground'}`}>{p.slice(0, 3)}</span>
                  ))}
                </div>
              )}
              {isCenter && (
                <div className="text-center mt-1">
                  <div className="text-xs text-sacred-gold font-semibold">🏠</div>
                </div>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}

// ─── Main Component ───────────────────────────────────────────────────────────

export default function LalKitabVastuTab({ kundliId, language }: Props) {
  const hi = language === 'hi';
  const [data, setData] = useState<VastuData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);
  const [view, setView] = useState<'compass' | 'floorplan' | 'warnings' | 'tips'>('compass');

  useEffect(() => {
    if (!kundliId) return;
    setLoading(true);
    setError(false);
    api.get(`/api/lalkitab/vastu/${kundliId}`)
      .then(setData)
      .catch(() => setError(true))
      .finally(() => setLoading(false));
  }, [kundliId]);

  if (!kundliId) return (
    <div className="text-center py-10 text-muted-foreground text-sm">
      {hi ? 'वास्तु विश्लेषण के लिए कुंडली सहेजें।' : 'Save a Kundli to view Vastu diagnosis.'}
    </div>
  );

  if (loading) return (
    <div className="space-y-4 animate-pulse">
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-center gap-2">
          <div className="w-9 h-9 rounded-xl bg-muted" />
          <div className="space-y-1.5">
            <div className="h-4 w-32 bg-muted rounded" />
            <div className="h-3 w-48 bg-muted rounded" />
          </div>
        </div>
        <div className="w-16 h-14 bg-muted rounded-xl" />
      </div>
      <div className="flex gap-1 bg-muted/30 rounded-xl p-1">
        {[1, 2, 3, 4].map(n => <div key={n} className="flex-1 h-10 bg-muted rounded-lg" />)}
      </div>
      <div className="h-72 bg-muted rounded-2xl" />
    </div>
  );

  if (error) return (
    <div className="text-center py-10 text-sm text-red-500">
      {hi ? 'वास्तु डेटा लोड नहीं हो सका।' : 'Could not load Vastu data. Please try again.'}
    </div>
  );

  if (!data) return null;

  const score = vastuScore(data.planet_warnings);
  const scoreColor = score >= 70 ? 'text-green-600' : score >= 45 ? 'text-yellow-600' : 'text-red-600';
  const scoreBg = score >= 70 ? 'bg-green-50 border-green-200' : score >= 45 ? 'bg-yellow-50 border-yellow-200' : 'bg-red-50 border-red-200';

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-center gap-2">
          <div className="w-9 h-9 rounded-xl bg-green-100 flex items-center justify-center shrink-0">
            <Home className="w-4.5 h-4.5 text-green-700" />
          </div>
          <div>
            <h3 className="font-bold text-foreground text-base leading-tight">
              {hi ? 'मकान वास्तु' : 'Makaan Vastu'}
            </h3>
            <p className="text-xs text-muted-foreground">
              {hi ? 'लाल किताब आधारित दिशा निदान' : 'Lal Kitab directional home diagnosis'}
            </p>
          </div>
        </div>
        {/* Vastu score */}
        <div className={`shrink-0 rounded-xl border px-3 py-2 text-center ${scoreBg}`}>
          <div className={`text-2xl font-black ${scoreColor}`}>{score}</div>
          <div className={`text-[9px] font-semibold uppercase tracking-wide ${scoreColor}`}>
            {hi ? 'वास्तु स्कोर' : 'Vastu Score'}
          </div>
        </div>
      </div>

      {/* Warning summary */}
      <div className="flex items-center gap-2 flex-wrap">
        <span className={`flex items-center gap-1 text-xs font-semibold px-2 py-1 rounded-full ${data.critical_count > 0 ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}`}>
          {data.critical_count > 0 ? <AlertTriangle className="w-3 h-3" /> : <CheckCircle2 className="w-3 h-3" />}
          {data.critical_count} {hi ? 'गंभीर' : 'critical'}
        </span>
        <span className="flex items-center gap-1 text-xs font-semibold px-2 py-1 rounded-full bg-yellow-100 text-yellow-700">
          {data.total_warnings} {hi ? 'चेतावनी' : 'warnings'}
        </span>
        <span className="flex items-center gap-1 text-xs font-semibold px-2 py-1 rounded-full bg-blue-50 text-blue-700">
          <CheckCircle2 className="w-3 h-3" />
          {12 - data.total_warnings} {hi ? 'स्वच्छ' : 'clear'}
        </span>
      </div>

      {/* View switcher */}
      <div className="flex gap-1 bg-muted/30 rounded-xl p-1">
        {([
          ['compass',   hi ? 'कम्पास' : 'Compass',      Compass],
          ['floorplan', hi ? 'फ्लोर प्लान' : 'Floor Plan', LayoutGrid],
          ['warnings',  hi ? 'चेतावनी' : 'Warnings',    AlertTriangle],
          ['tips',      hi ? 'सुझाव' : 'Tips',            Wrench],
        ] as const).map(([key, label, Icon]) => (
          <button
            key={key}
            onClick={() => setView(key)}
            className={`flex-1 flex flex-col items-center gap-0.5 text-[10px] font-semibold py-1.5 rounded-lg transition-all ${
              view === key ? 'bg-white shadow text-foreground' : 'text-muted-foreground'
            }`}
          >
            <Icon className="w-3.5 h-3.5" />
            <span>{label}</span>
          </button>
        ))}
      </div>

      {/* ── COMPASS VIEW ─────────────────────────────────── */}
      {view === 'compass' && (
        <div className="space-y-3">
          <div className="bg-card rounded-2xl border border-border p-3">
            <VastuCompass map={data.directional_map} warnings={data.planet_warnings} hi={hi} />
            <p className="text-center text-xs text-muted-foreground mt-2">
              {hi
                ? 'खंड पर होवर करें — घर और ग्रह विवरण देखें'
                : 'Hover a segment to see house, zone & planet details'}
            </p>
          </div>

          {/* Legend */}
          <div className="flex flex-wrap items-center gap-x-4 gap-y-1.5 px-1">
            {[
              { color: 'bg-red-200', label: hi ? 'गंभीर चेतावनी' : 'Critical' },
              { color: 'bg-yellow-200', label: hi ? 'चेतावनी' : 'Warning' },
              { color: 'bg-amber-50 border border-border', label: hi ? 'ग्रह उपस्थित' : 'Has planets' },
              { color: 'bg-gray-100', label: hi ? 'खाली' : 'Empty' },
            ].map(({ color, label }) => (
              <div key={label} className="flex items-center gap-1.5">
                <span className={`w-3 h-3 rounded-sm ${color}`} />
                <span className="text-xs text-muted-foreground">{label}</span>
              </div>
            ))}
          </div>

          {/* Planet dot legend */}
          <div className="flex flex-wrap gap-2 px-1">
            {Object.entries(PLANET_HEX).map(([p, hex]) => (
              <div key={p} className="flex items-center gap-1">
                <span className="w-2.5 h-2.5 rounded-full inline-block" style={{ backgroundColor: hex }} />
                <span className="text-xs text-muted-foreground">{p}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ── FLOOR PLAN VIEW ──────────────────────────────── */}
      {view === 'floorplan' && (
        <div className="space-y-3">
          <div className="bg-card rounded-2xl border border-border p-3">
            <p className="text-xs text-muted-foreground text-center mb-3">
              {hi
                ? 'वास्तु पुरुष मंडल — 12 भावों का गृह लेआउट'
                : 'Vastu Purush Mandala — 12 houses mapped to home zones'}
            </p>
            <HomeFloorPlan map={data.directional_map} warnings={data.planet_warnings} hi={hi} />
            {/* Compass markers */}
            <div className="flex justify-between text-[10px] text-muted-foreground mt-2 px-2">
              <span>↙ {hi ? 'दक्षिण-पश्चिम' : 'SW'}</span>
              <span>↓ {hi ? 'दक्षिण' : 'S'}</span>
              <span>↘ {hi ? 'दक्षिण-पूर्व' : 'SE'}</span>
            </div>
            <div className="flex justify-between text-[10px] text-muted-foreground px-2">
              <span>↖ {hi ? 'उत्तर-पश्चिम' : 'NW'}</span>
              <span>↑ {hi ? 'उत्तर' : 'N'}</span>
              <span>↗ {hi ? 'उत्तर-पूर्व' : 'NE'}</span>
            </div>
          </div>

          <div className="bg-amber-50 border border-amber-100 rounded-xl p-3 text-xs text-amber-800">
            <span className="font-semibold">{hi ? 'नोट: ' : 'Note: '}</span>
            {hi
              ? 'लाल किताब में H1=पूर्व, H4=दक्षिण, H7=पश्चिम, H10=उत्तर। यह क्लासिक लग्न आधारित मैपिंग है।'
              : 'In LK: H1=East, H4=South, H7=West, H10=North. This is the classical ascendant-based mapping.'}
          </div>
        </div>
      )}

      {/* ── WARNINGS VIEW ────────────────────────────────── */}
      {view === 'warnings' && (
        <div className="space-y-3">
          {data.planet_warnings.length === 0 ? (
            <div className="text-center py-8 text-muted-foreground text-sm">
              <CheckCircle2 className="w-8 h-8 text-green-500 mx-auto mb-2" />
              {hi ? 'कोई गंभीर वास्तु चेतावनी नहीं।' : 'No planet-specific Vastu warnings for this chart.'}
            </div>
          ) : (
            data.planet_warnings.map((w, i) => (
              <div key={i} className={`rounded-xl p-4 border ${w.is_critical ? 'border-red-200 bg-red-50' : 'border-yellow-200 bg-yellow-50'}`}>
                <div className="flex items-start gap-2 mb-2">
                  <div className={`w-8 h-8 rounded-xl flex items-center justify-center text-xs font-black shrink-0 ${w.is_critical ? 'bg-red-100 text-red-700' : 'bg-yellow-100 text-yellow-700'}`}>
                    H{w.house}
                  </div>
                  <div className="flex-1">
                    <div className="flex flex-wrap items-center gap-1.5 mb-0.5">
                      <span className={`font-bold text-sm ${PLANET_CSS[w.planet] ?? ''}`}>{w.planet}</span>
                      <span className="text-xs text-muted-foreground">{hi ? w.direction.hi : w.direction.en}</span>
                      {w.is_critical && (
                        <span className="text-[10px] font-black text-red-600 bg-red-100 px-1.5 rounded-full uppercase">
                          {hi ? 'गंभीर' : 'CRITICAL'}
                        </span>
                      )}
                    </div>
                    <div className="text-xs text-muted-foreground">{hi ? w.zone.hi : w.zone.en}</div>
                  </div>
                </div>
                <p className="text-xs text-foreground/80 mb-3">{hi ? w.warning.hi : w.warning.en}</p>
                <div className="bg-white/80 rounded-lg p-2.5 border border-green-100">
                  <div className="text-xs font-semibold text-green-700 mb-1 flex items-center gap-1">
                    <Wrench className="w-3 h-3" />
                    {hi ? 'उपाय:' : 'Fix:'}
                  </div>
                  <p className="text-xs text-green-800">{hi ? w.fix.hi : w.fix.en}</p>
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {/* ── TIPS VIEW ────────────────────────────────────── */}
      {view === 'tips' && (
        <div className="space-y-2">
          {data.priority_fixes.length > 0 && (
            <div className="mb-3 p-3 rounded-xl bg-orange-50 border border-orange-100">
              <p className="text-xs font-semibold text-orange-700 mb-2">
                {hi ? 'प्राथमिकता उपाय (शीर्ष 3)' : 'Priority fixes (top 3)'}
              </p>
              {data.priority_fixes.map((fix, i) => (
                <div key={i} className="flex gap-2 mb-1.5 last:mb-0">
                  <span className={`text-xs font-bold shrink-0 ${PLANET_CSS[fix.planet] ?? ''}`}>{fix.planet}</span>
                  <p className="text-xs text-orange-800">{hi ? fix.fix.hi : fix.fix.en}</p>
                </div>
              ))}
            </div>
          )}
          {data.general_layout.map(item => (
            <div key={item.house} className="flex gap-3 p-3 rounded-xl border border-border bg-card">
              <div className="w-8 h-8 rounded-lg bg-sacred-gold/10 text-sacred-gold text-xs font-black flex items-center justify-center shrink-0">
                {item.house}
              </div>
              <div>
                <div className="text-xs font-semibold text-foreground mb-0.5">
                  {hi ? item.direction.hi : item.direction.en}
                </div>
                <p className="text-xs text-muted-foreground">{hi ? item.tip.hi : item.tip.en}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
