import { useState, useEffect, useRef, useCallback, useMemo } from 'react';
import { Play, Pause, SkipForward, SkipBack, RotateCcw } from 'lucide-react';
import { api } from '@/lib/api';
import { translatePlanetAbbr } from '@/lib/backend-translations';
import { Button } from '@/components/ui/button';
import { Heading } from '@/components/ui/heading';

/* ------------------------------------------------------------------ */
/*  Types                                                              */
/* ------------------------------------------------------------------ */

interface NatalPlanet {
  planet: string;
  sign: string;
  longitude: number;
}

interface TransitSnapshot {
  date: string;   // ISO or YYYY-MM-DD
  planets: Array<{
    planet: string;
    sign: string;
    longitude: number;
    is_retrograde?: boolean;
  }>;
}

interface ChartAnimationProps {
  kundliId: string;
  natalPlanets: NatalPlanet[];
  lagnaLongitude: number;
  language: string;
  t: (key: string) => string;
}

/* ------------------------------------------------------------------ */
/*  Constants                                                          */
/* ------------------------------------------------------------------ */

const ZODIAC_SIGNS = [
  'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
  'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces',
];

const SIGN_COLORS = [
  '#FEE2E2', '#FEF3C7', '#D1FAE5', '#DBEAFE', '#F3E8FF', '#FCE7F3',
  '#FEE2E2', '#FEF3C7', '#D1FAE5', '#DBEAFE', '#F3E8FF', '#FCE7F3',
];

const PLANET_COLORS: Record<string, string> = {
  Sun: '#E65100', Moon: '#546E7A', Mars: '#C62828', Mercury: '#2E7D32',
  Jupiter: '#F9A825', Venus: '#AD1457', Saturn: '#1565C0',
  Rahu: '#6A1B9A', Ketu: '#78909C',
};

type SpeedMode = 'day' | 'week' | 'month';

const SPEED_MS: Record<SpeedMode, number> = {
  day: 80,    // ~80ms per day = fast visual
  week: 80,   // same interval but jumps 7 days
  month: 80,  // same interval but jumps 30 days
};

const SPEED_DAYS: Record<SpeedMode, number> = {
  day: 1,
  week: 7,
  month: 30,
};

/** Aspect orbs: if transit-to-natal is within orb, highlight */
const ASPECT_ANGLES = [0, 60, 90, 120, 180];
const ASPECT_ORB = 5; // degrees

/* ------------------------------------------------------------------ */
/*  Geometry helpers                                                    */
/* ------------------------------------------------------------------ */

function polarToXY(cx: number, cy: number, r: number, angleDeg: number) {
  const rad = (angleDeg * Math.PI) / 180;
  return { x: cx + r * Math.cos(rad), y: cy + r * Math.sin(rad) };
}

/* ------------------------------------------------------------------ */
/*  Interpolation helpers                                              */
/* ------------------------------------------------------------------ */

function toDateNum(d: string): number {
  return new Date(d).getTime();
}

function formatDate(d: Date): string {
  return d.toISOString().slice(0, 10);
}

/** Linear interpolation of a longitude value, wrapping at 360 */
function lerpLon(a: number, b: number, t: number): number {
  let diff = ((b - a + 540) % 360) - 180; // shortest arc
  return ((a + diff * t) % 360 + 360) % 360;
}

/** Generate dates from start to end at step interval */
function generateDates(start: string, end: string, stepDays: number): string[] {
  const dates: string[] = [];
  const s = new Date(start);
  const e = new Date(end);
  for (let d = new Date(s); d <= e; d.setDate(d.getDate() + stepDays)) {
    dates.push(formatDate(d));
  }
  return dates;
}

/* ------------------------------------------------------------------ */
/*  Component                                                          */
/* ------------------------------------------------------------------ */

export default function ChartAnimation({
  kundliId,
  natalPlanets,
  lagnaLongitude,
  language,
  t,
}: ChartAnimationProps) {
  const l = (en: string, hi: string) => (language === 'hi' ? hi : en);

  /* ----- state ----- */
  const today = formatDate(new Date());
  const defaultEnd = formatDate(new Date(Date.now() + 365 * 86400000));

  const [startDate, setStartDate] = useState(today);
  const [endDate, setEndDate] = useState(defaultEnd);
  const [speed, setSpeed] = useState<SpeedMode>('day');
  const [isPlaying, setIsPlaying] = useState(false);
  const [frameIndex, setFrameIndex] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // The pre-fetched snapshots (sparse — one per month)
  const [snapshots, setSnapshots] = useState<TransitSnapshot[]>([]);

  const animRef = useRef<number | null>(null);
  const lastTickRef = useRef<number>(0);

  /* ----- date list for current playback ----- */
  const allDates = useMemo(
    () => generateDates(startDate, endDate, SPEED_DAYS[speed]),
    [startDate, endDate, speed]
  );
  const totalFrames = allDates.length;

  /* ----- fetch transit snapshots (sparse: monthly) ----- */
  const fetchSnapshots = useCallback(async () => {
    if (!kundliId) return;
    setLoading(true);
    setError(null);
    try {
      // Fetch monthly snapshots between start and end
      const months = generateDates(startDate, endDate, 30);
      const results: TransitSnapshot[] = [];

      // Batch in chunks of 6 to avoid overwhelming API
      for (let i = 0; i < months.length; i += 6) {
        const batch = months.slice(i, i + 6);
        const batchResults = await Promise.all(
          batch.map(async (date) => {
            try {
              const res = await api.post(`/api/kundli/${kundliId}/transits`, {
                transit_date: date,
                transit_time: '12:00:00',
              });
              return {
                date,
                planets: (res.transits || []).map((tr: any) => {
                  const signIdx = ZODIAC_SIGNS.indexOf(tr.current_sign);
                  return {
                    planet: tr.planet,
                    sign: tr.current_sign,
                    longitude: signIdx >= 0 ? signIdx * 30 + (tr.sign_degree || 0) : 0,
                    is_retrograde: !!tr.is_retrograde,
                  };
                }),
              } as TransitSnapshot;
            } catch {
              return null;
            }
          })
        );
        results.push(...(batchResults.filter(Boolean) as TransitSnapshot[]));
      }

      setSnapshots(results);
      setFrameIndex(0);
    } catch (err: any) {
      setError(err?.message || 'Failed to load transit data');
    } finally {
      setLoading(false);
    }
  }, [kundliId, startDate, endDate]);

  /* ----- interpolate planets for a given date ----- */
  const interpolateFrame = useCallback(
    (dateStr: string) => {
      if (snapshots.length === 0) return natalPlanets.map(() => ({ planet: '', longitude: 0, is_retrograde: false }));
      if (snapshots.length === 1) return snapshots[0].planets;

      const dateTime = toDateNum(dateStr);

      // Find surrounding snapshots
      let before = snapshots[0];
      let after = snapshots[snapshots.length - 1];
      for (let i = 0; i < snapshots.length - 1; i++) {
        const t0 = toDateNum(snapshots[i].date);
        const t1 = toDateNum(snapshots[i + 1].date);
        if (dateTime >= t0 && dateTime <= t1) {
          before = snapshots[i];
          after = snapshots[i + 1];
          break;
        }
      }

      const range = toDateNum(after.date) - toDateNum(before.date);
      const tFactor = range > 0 ? (dateTime - toDateNum(before.date)) / range : 0;

      // Interpolate each planet
      return before.planets.map((bp) => {
        const ap = after.planets.find((p) => p.planet === bp.planet);
        if (!ap) return bp;
        return {
          planet: bp.planet,
          longitude: lerpLon(bp.longitude, ap.longitude, tFactor),
          is_retrograde: tFactor < 0.5 ? bp.is_retrograde : ap.is_retrograde,
        };
      });
    },
    [snapshots, natalPlanets]
  );

  /* Current frame planets */
  const currentDate = allDates[Math.min(frameIndex, allDates.length - 1)] || today;
  const currentTransitPlanets = useMemo(
    () => interpolateFrame(currentDate),
    [currentDate, interpolateFrame]
  );

  /* ----- detect aspects ----- */
  const activeAspects = useMemo(() => {
    const aspects: Array<{ natal: string; transit: string; angle: number }> = [];
    for (const np of natalPlanets) {
      for (const tp of currentTransitPlanets) {
        if (!tp.planet) continue;
        const diff = Math.abs(((tp.longitude - np.longitude + 180) % 360) - 180);
        for (const aspectAngle of ASPECT_ANGLES) {
          if (Math.abs(diff - aspectAngle) <= ASPECT_ORB) {
            aspects.push({ natal: np.planet, transit: tp.planet, angle: aspectAngle });
          }
        }
      }
    }
    return aspects;
  }, [natalPlanets, currentTransitPlanets]);

  /* ----- animation loop ----- */
  useEffect(() => {
    if (!isPlaying) {
      if (animRef.current) cancelAnimationFrame(animRef.current);
      return;
    }

    const tick = (timestamp: number) => {
      if (timestamp - lastTickRef.current >= SPEED_MS[speed]) {
        lastTickRef.current = timestamp;
        setFrameIndex((prev) => {
          if (prev >= totalFrames - 1) {
            setIsPlaying(false);
            return prev;
          }
          return prev + 1;
        });
      }
      animRef.current = requestAnimationFrame(tick);
    };

    animRef.current = requestAnimationFrame(tick);
    return () => {
      if (animRef.current) cancelAnimationFrame(animRef.current);
    };
  }, [isPlaying, speed, totalFrames]);

  /* ----- SVG rendering ----- */
  const SIZE = 420;
  const CENTER = SIZE / 2;
  const OUTER_R = CENTER - 15;
  const TRANSIT_R = CENTER - 50;
  const NATAL_R = CENTER - 90;
  const INNER_R = CENTER - 125;

  const getAngle = (lon: number) => {
    const deg = (lon - lagnaLongitude + 360) % 360;
    return 180 - deg;
  };

  /* ---------------------------------------------------------------- */
  /*  Render                                                           */
  /* ---------------------------------------------------------------- */

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="bg-muted rounded-xl border border-border p-4">
        <Heading as={4} variant={4} className="mb-1">
          {l('Transit Animation', 'गोचर एनिमेशन')}
        </Heading>
        <p className="text-xs text-foreground/70">
          {l(
            'Watch transit planets move over your birth chart. Aspects are highlighted in real-time.',
            'अपनी जन्म कुंडली पर गोचर ग्रहों की चाल देखें। पहलू वास्तविक समय में हाइलाइट किए जाते हैं।'
          )}
        </p>
      </div>

      {/* Date range + Load */}
      <div className="flex flex-wrap items-end gap-3">
        <div>
          <label className="text-xs font-medium text-foreground/70 block mb-1">{l('Start', 'शुरू')}</label>
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            className="px-3 py-1.5 rounded-lg text-sm border border-border bg-white text-foreground"
          />
        </div>
        <div>
          <label className="text-xs font-medium text-foreground/70 block mb-1">{l('End', 'अंत')}</label>
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            className="px-3 py-1.5 rounded-lg text-sm border border-border bg-white text-foreground"
          />
        </div>
        <Button
          size="sm"
          onClick={() => { setIsPlaying(false); fetchSnapshots(); }}
          disabled={loading}
        >
          {loading ? l('Loading...', 'लोड हो रहा है...') : l('Load Transits', 'गोचर लोड करें')}
        </Button>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-xl p-3 text-sm text-red-700">{error}</div>
      )}

      {/* SVG Chart */}
      <div className="bg-white rounded-2xl shadow-lg border border-border p-3">
        <svg viewBox={`0 0 ${SIZE} ${SIZE}`} className="w-full h-auto font-sans">
          {/* Zodiac ring segments */}
          {ZODIAC_SIGNS.map((sign, i) => {
            const startAngle = getAngle(i * 30);
            const endAngle = getAngle((i + 1) * 30);
            const midAngle = getAngle(i * 30 + 15);
            const labelPos = polarToXY(CENTER, CENTER, OUTER_R + 10, midAngle);

            // Arc path
            const p1 = polarToXY(CENTER, CENTER, OUTER_R, startAngle);
            const p2 = polarToXY(CENTER, CENTER, OUTER_R, endAngle);
            return (
              <g key={sign}>
                <path
                  d={`M ${CENTER} ${CENTER} L ${p1.x} ${p1.y} A ${OUTER_R} ${OUTER_R} 0 0 1 ${p2.x} ${p2.y} Z`}
                  fill={SIGN_COLORS[i]}
                  stroke="#3D2B1F"
                  strokeWidth="0.5"
                  opacity="0.2"
                />
                <text
                  x={labelPos.x}
                  y={labelPos.y}
                  textAnchor="middle"
                  dominantBaseline="central"
                  fontSize="7"
                  fill="#8B7355"
                  fontWeight="bold"
                >
                  {sign.slice(0, 3)}
                </text>
              </g>
            );
          })}

          {/* Ring dividers */}
          <circle cx={CENTER} cy={CENTER} r={OUTER_R} fill="none" stroke="#3D2B1F" strokeWidth="1" />
          <circle cx={CENTER} cy={CENTER} r={TRANSIT_R} fill="none" stroke="#3D2B1F" strokeWidth="0.5" strokeDasharray="4,2" />
          <circle cx={CENTER} cy={CENTER} r={NATAL_R} fill="none" stroke="#3D2B1F" strokeWidth="1" />
          <circle cx={CENTER} cy={CENTER} r={INNER_R} fill="#FDF6E3" stroke="#3D2B1F" strokeWidth="1" />

          {/* House division lines */}
          {Array.from({ length: 12 }).map((_, i) => {
            const angle = 180 - i * 30;
            const p1 = polarToXY(CENTER, CENTER, INNER_R, angle);
            const p2 = polarToXY(CENTER, CENTER, OUTER_R, angle);
            const isLagna = i === 0;
            return (
              <line
                key={`hl-${i}`}
                x1={p1.x} y1={p1.y} x2={p2.x} y2={p2.y}
                stroke={isLagna ? '#D4AF37' : '#3D2B1F'}
                strokeWidth={isLagna ? 2 : 0.5}
                opacity={isLagna ? 1 : 0.3}
              />
            );
          })}

          {/* Aspect lines (transit-to-natal) */}
          {activeAspects.map((asp, idx) => {
            const np = natalPlanets.find((p) => p.planet === asp.natal);
            const tp = currentTransitPlanets.find((p) => p.planet === asp.transit);
            if (!np || !tp) return null;
            const nPos = polarToXY(CENTER, CENTER, NATAL_R + 18, getAngle(np.longitude));
            const tPos = polarToXY(CENTER, CENTER, TRANSIT_R + 15, getAngle(tp.longitude));
            const color = asp.angle === 0 || asp.angle === 120 || asp.angle === 60
              ? '#22C55E'   // benefic aspects: green
              : '#EF4444';  // malefic aspects: red
            return (
              <line
                key={`asp-${idx}`}
                x1={nPos.x} y1={nPos.y} x2={tPos.x} y2={tPos.y}
                stroke={color}
                strokeWidth="1"
                strokeDasharray="3,3"
                opacity="0.6"
              />
            );
          })}

          {/* Natal planets (inner ring — fixed) */}
          {natalPlanets.map((p) => {
            const angle = getAngle(p.longitude);
            const pos = polarToXY(CENTER, CENTER, NATAL_R + 18, angle);
            return (
              <g key={`nt-${p.planet}`}>
                <circle cx={pos.x} cy={pos.y} r="11" fill="#3D2B1F" />
                <text
                  x={pos.x}
                  y={pos.y + 3}
                  textAnchor="middle"
                  fontSize="9"
                  fontWeight="bold"
                  fill="#D4AF37"
                >
                  {translatePlanetAbbr(p.planet, language)}
                </text>
              </g>
            );
          })}

          {/* Transit planets (middle ring — animated) */}
          {currentTransitPlanets.map((p) => {
            if (!p.planet) return null;
            const angle = getAngle(p.longitude);
            const pos = polarToXY(CENTER, CENTER, TRANSIT_R + 15, angle);
            const hasAspect = activeAspects.some((a) => a.transit === p.planet);
            const color = PLANET_COLORS[p.planet] || '#4B5563';
            return (
              <g key={`tr-${p.planet}`}>
                <circle
                  cx={pos.x}
                  cy={pos.y}
                  r="10"
                  fill="white"
                  stroke={hasAspect ? '#D4AF37' : color}
                  strokeWidth={hasAspect ? 2 : 1}
                />
                {hasAspect && (
                  <circle cx={pos.x} cy={pos.y} r="13" fill="none" stroke="#D4AF37" strokeWidth="1" opacity="0.4">
                    <animate attributeName="r" from="10" to="16" dur="1.5s" repeatCount="indefinite" />
                    <animate attributeName="opacity" from="0.6" to="0" dur="1.5s" repeatCount="indefinite" />
                  </circle>
                )}
                <text
                  x={pos.x}
                  y={pos.y + 3}
                  textAnchor="middle"
                  fontSize="8"
                  fontWeight="bold"
                  fill={color}
                >
                  {translatePlanetAbbr(p.planet, language)}
                </text>
                {p.is_retrograde && (
                  <text x={pos.x + 7} y={pos.y - 5} fontSize="6" fill="#EF4444" fontWeight="bold">R</text>
                )}
              </g>
            );
          })}

          {/* Center */}
          <circle cx={CENTER} cy={CENTER} r="15" fill="white" stroke="#D4AF37" strokeWidth="2" />
          <text x={CENTER} y={CENTER + 4} textAnchor="middle" fontSize="10" fontWeight="bold" fill="#D4AF37">
            {'\u0950'}
          </text>
        </svg>

        {/* Current date display */}
        <div className="text-center mt-2">
          <span className="text-sm font-bold text-primary">{currentDate}</span>
          {activeAspects.length > 0 && (
            <span className="ml-3 text-xs text-amber-600 font-medium">
              {activeAspects.length} {l('aspect(s) active', 'पहलू सक्रिय')}
            </span>
          )}
        </div>

        {/* Legend */}
        <div className="flex justify-center gap-4 mt-2 border-t border-border/10 pt-2">
          <div className="flex items-center gap-1">
            <div className="w-2.5 h-2.5 rounded-full bg-[#3D2B1F]" />
            <span className="text-[10px] font-bold text-foreground/60 uppercase">{l('Natal', 'जन्म')}</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-2.5 h-2.5 rounded-full bg-white border border-border" />
            <span className="text-[10px] font-bold text-foreground/60 uppercase">{l('Transit', 'गोचर')}</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-4 h-0.5 bg-green-500" />
            <span className="text-[10px] font-bold text-foreground/60 uppercase">{l('Benefic', 'शुभ')}</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-4 h-0.5 bg-red-500" />
            <span className="text-[10px] font-bold text-foreground/60 uppercase">{l('Malefic', 'पाप')}</span>
          </div>
        </div>
      </div>

      {/* Playback controls */}
      <div className="bg-muted rounded-xl border border-border p-4">
        <div className="flex flex-wrap items-center justify-center gap-3">
          {/* Skip back */}
          <Button
            size="icon-sm"
            variant="outline"
            onClick={() => setFrameIndex(0)}
            disabled={snapshots.length === 0}
            title={l('Reset', 'रीसेट')}
          >
            <RotateCcw className="w-4 h-4" />
          </Button>

          {/* Step back */}
          <Button
            size="icon-sm"
            variant="outline"
            onClick={() => setFrameIndex((p) => Math.max(0, p - 1))}
            disabled={frameIndex <= 0 || snapshots.length === 0}
          >
            <SkipBack className="w-4 h-4" />
          </Button>

          {/* Play / Pause */}
          <Button
            size="sm"
            onClick={() => setIsPlaying((p) => !p)}
            disabled={snapshots.length === 0 || frameIndex >= totalFrames - 1}
            className="px-6"
          >
            {isPlaying ? <Pause className="w-4 h-4 mr-1" /> : <Play className="w-4 h-4 mr-1" />}
            {isPlaying ? l('Pause', 'रुकें') : l('Play', 'चलाएं')}
          </Button>

          {/* Step forward */}
          <Button
            size="icon-sm"
            variant="outline"
            onClick={() => setFrameIndex((p) => Math.min(totalFrames - 1, p + 1))}
            disabled={frameIndex >= totalFrames - 1 || snapshots.length === 0}
          >
            <SkipForward className="w-4 h-4" />
          </Button>

          {/* Speed selector */}
          <div className="flex items-center gap-1 ml-3">
            <span className="text-xs text-foreground/70 font-medium">{l('Speed', 'गति')}:</span>
            {(['day', 'week', 'month'] as SpeedMode[]).map((s) => (
              <button
                key={s}
                onClick={() => setSpeed(s)}
                className={`px-2 py-1 text-[10px] font-bold rounded-md transition-all ${
                  speed === s
                    ? 'bg-primary text-white'
                    : 'bg-white text-primary border border-border hover:bg-muted/10'
                }`}
              >
                {s === 'day' ? l('1 Day', '1 दिन') : s === 'week' ? l('1 Week', '1 सप्ताह') : l('1 Month', '1 माह')}
              </button>
            ))}
          </div>
        </div>

        {/* Progress bar */}
        {totalFrames > 0 && (
          <div className="mt-3">
            <input
              type="range"
              min={0}
              max={totalFrames - 1}
              value={frameIndex}
              onChange={(e) => { setIsPlaying(false); setFrameIndex(parseInt(e.target.value)); }}
              className="w-full h-1.5 bg-border/30 rounded-full appearance-none cursor-pointer accent-primary"
            />
            <div className="flex items-center justify-between text-[10px] text-foreground/50 mt-1">
              <span>{startDate}</span>
              <span>{frameIndex + 1} / {totalFrames}</span>
              <span>{endDate}</span>
            </div>
          </div>
        )}
      </div>

      {/* Active aspects list */}
      {activeAspects.length > 0 && (
        <div className="bg-muted rounded-xl border border-border p-4">
          <Heading as={5} variant={5} className="mb-2">
            {l('Active Aspects', 'सक्रिय पहलू')} — {currentDate}
          </Heading>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2">
            {activeAspects.map((asp, idx) => {
              const isBenefic = asp.angle === 0 || asp.angle === 120 || asp.angle === 60;
              return (
                <div
                  key={idx}
                  className={`flex items-center gap-2 p-2 rounded-lg text-xs border ${
                    isBenefic ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'
                  }`}
                >
                  <span className={`font-bold ${isBenefic ? 'text-green-700' : 'text-red-700'}`}>
                    {translatePlanetAbbr(asp.transit, language)}
                  </span>
                  <span className="text-foreground/50">{asp.angle}&deg;</span>
                  <span className="font-bold text-foreground">
                    {translatePlanetAbbr(asp.natal, language)}
                  </span>
                  <span className={`text-[9px] px-1 rounded ${isBenefic ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                    {asp.angle === 0 ? l('Conjunction', 'युति')
                      : asp.angle === 60 ? l('Sextile', 'षडाश्र')
                      : asp.angle === 90 ? l('Square', 'चतुष्कोण')
                      : asp.angle === 120 ? l('Trine', 'त्रिकोण')
                      : l('Opposition', 'सप्तम')}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
