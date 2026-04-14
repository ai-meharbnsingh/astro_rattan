import { useState, useEffect, useCallback } from 'react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';

const toRad = (deg: number) => (deg * Math.PI) / 180;
const CX = 300;
const CY = 300;

const SIGNS_EN = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces'];
const SIGNS_HI = ['मेष','वृषभ','मिथुन','कर्क','सिंह','कन्या','तुला','वृश्चिक','धनु','मकर','कुंभ','मीन'];
const GLYPHS = ['\u2648','\u2649','\u264A','\u264B','\u264C','\u264D','\u264E','\u264F','\u2650','\u2651','\u2652','\u2653'];

const PLANET_ABBR: Record<string, string> = {
  Sun: 'Su', Moon: 'Mo', Mars: 'Ma', Mercury: 'Me',
  Jupiter: 'Ju', Venus: 'Ve', Saturn: 'Sa', Rahu: 'Ra', Ketu: 'Ke',
};
const PLANET_HI: Record<string, string> = {
  Sun: 'सू', Moon: 'चं', Mars: 'मं', Mercury: 'बु',
  Jupiter: 'गु', Venus: 'शु', Saturn: 'श', Rahu: 'रा', Ketu: 'के',
};
const MALEFIC = new Set(['Mars', 'Saturn', 'Rahu', 'Ketu']);

interface TransitPlanet {
  planet: string;
  sign: string;
  longitude: number;
  sign_degree: number;
  is_retrograde: boolean;
}

interface TooltipData {
  planet: string;
  sign: string;
  degree: number;
  retrograde: boolean;
  x: number;
  y: number;
}

// Ring radii
const R_OUTER = 290;
const R_SIGN_TEXT = 272;
const R_SIGN_RING = 255;
const R_TRANSIT = 230;
const R_INNER_RING = 205;
const R_CENTER_BG = 160;
const R_OM = 45;

const GOLD = '#8B4513';
const GOLD_MED = '#C4611F';
const DARK = '#1a1a2e';

function signIndex(sign: string): number {
  const idx = SIGNS_EN.findIndex(s => s.toLowerCase() === sign.toLowerCase());
  return idx >= 0 ? idx : 0;
}

function planetAngle(planet: TransitPlanet): number {
  return signIndex(planet.sign) * 30 + planet.sign_degree - 90;
}

function arcRot(midDeg: number): number {
  const t = ((midDeg + 90) % 360 + 360) % 360;
  return (t > 90 && t < 270) ? t + 180 : t;
}

export default function LiveTransitWheel() {
  const { language } = useTranslation();
  const hi = language === 'hi';

  const [planets, setPlanets] = useState<TransitPlanet[]>([]);
  const [skyDate, setSkyDate] = useState('');
  const [skyTime, setSkyTime] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [currentTime, setCurrentTime] = useState(new Date());
  const [tooltip, setTooltip] = useState<TooltipData | null>(null);

  const fetchSky = useCallback(async () => {
    try {
      const data = await api.get('/api/kundli/current-sky');
      setPlanets(data.planets || []);
      setSkyDate(data.date || '');
      setSkyTime(data.time || '');
      setError(false);
    } catch {
      setError(true);
    }
    setLoading(false);
  }, []);

  // Fetch on mount + every 60s
  useEffect(() => {
    fetchSky();
    const iv = setInterval(fetchSky, 60000);
    return () => clearInterval(iv);
  }, [fetchSky]);

  // Live clock
  useEffect(() => {
    const iv = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(iv);
  }, []);

  const timeStr = currentTime.toLocaleTimeString(hi ? 'hi-IN' : 'en-IN', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  const dateStr = currentTime.toLocaleDateString(hi ? 'hi-IN' : 'en-IN', { day: 'numeric', month: 'short', year: 'numeric' });

  // Zodiac sign ticks
  const ticks: JSX.Element[] = [];
  for (let i = 0; i < 360; i += 3) {
    const a = toRad(i);
    const isMajor = i % 30 === 0;
    const r2 = isMajor ? R_OUTER - 8 : R_OUTER - 3;
    ticks.push(
      <line key={`t${i}`}
        x1={CX + R_OUTER * Math.cos(a)} y1={CY + R_OUTER * Math.sin(a)}
        x2={CX + r2 * Math.cos(a)} y2={CY + r2 * Math.sin(a)}
        stroke="rgba(196,97,31,0.3)" strokeWidth={isMajor ? 1.2 : 0.4}
      />
    );
  }

  // Sign labels + dividers
  const signElements = SIGNS_EN.map((sign, i) => {
    const startDeg = i * 30 - 90;
    const midDeg = startDeg + 15;
    const startRad = toRad(startDeg);
    const midRad = toRad(midDeg);

    const lx1 = CX + R_INNER_RING * Math.cos(startRad);
    const ly1 = CY + R_INNER_RING * Math.sin(startRad);
    const lx2 = CX + R_OUTER * Math.cos(startRad);
    const ly2 = CY + R_OUTER * Math.sin(startRad);

    const tx = CX + R_SIGN_TEXT * Math.cos(midRad);
    const ty = CY + R_SIGN_TEXT * Math.sin(midRad);
    const rot = arcRot(midDeg);

    const gx = CX + (R_SIGN_RING - 16) * Math.cos(midRad);
    const gy = CY + (R_SIGN_RING - 16) * Math.sin(midRad);

    const label = hi ? SIGNS_HI[i] : sign.slice(0, 3).toUpperCase();

    return (
      <g key={sign}>
        <line x1={lx1} y1={ly1} x2={lx2} y2={ly2} stroke={GOLD_MED} strokeWidth={0.8} />
        <text x={tx} y={ty} textAnchor="middle" dominantBaseline="central"
          fill={GOLD} fontSize="10" fontWeight="700" fontFamily="'Inter',sans-serif"
          transform={`rotate(${rot},${tx},${ty})`}>{label}</text>
        <text x={gx} y={gy} textAnchor="middle" dominantBaseline="central"
          fill={GOLD_MED} fontSize="14"
          fontFamily="'Segoe UI Symbol','Noto Sans Symbols 2',serif"
        >{GLYPHS[i]}</text>
      </g>
    );
  });

  // Planet dots (transit ring)
  const planetDots = planets.map((p, i) => {
    const angle = planetAngle(p);
    const rad = toRad(angle);
    const px = CX + R_TRANSIT * Math.cos(rad);
    const py = CY + R_TRANSIT * Math.sin(rad);
    const isMalefic = MALEFIC.has(p.planet);
    const abbr = hi ? PLANET_HI[p.planet] || p.planet.slice(0, 2) : PLANET_ABBR[p.planet] || p.planet.slice(0, 2);

    return (
      <g key={p.planet}
        className="transit-dot"
        style={{ animationDelay: `${i * 0.1}s` }}
        onMouseEnter={() => setTooltip({ planet: p.planet, sign: p.sign, degree: p.sign_degree, retrograde: p.is_retrograde, x: px, y: py })}
        onMouseLeave={() => setTooltip(null)}
      >
        <circle cx={px} cy={py} r={18}
          fill={isMalefic ? '#a83232' : GOLD_MED}
          stroke={GOLD} strokeWidth={1.5}
          style={{ transition: 'cx 1s ease, cy 1s ease' }}
        />
        <text x={px} y={py} textAnchor="middle" dominantBaseline="central"
          fill="white" fontSize="9" fontWeight="600" fontFamily="'Inter',sans-serif"
        >{abbr}</text>
        {p.is_retrograde && (
          <text x={px + 12} y={py - 12} fill="#ff4444" fontSize="8" fontWeight="bold">R</text>
        )}
      </g>
    );
  });

  // Sun rays for center
  const sunRays: JSX.Element[] = [];
  for (let i = 0; i < 32; i++) {
    const a = toRad(i * 11.25);
    const long = i % 2 === 0;
    sunRays.push(
      <line key={`sr${i}`}
        x1={CX + 14 * Math.cos(a)} y1={CY + 14 * Math.sin(a)}
        x2={CX + (long ? R_OM - 3 : R_OM - 12) * Math.cos(a)}
        y2={CY + (long ? R_OM - 3 : R_OM - 12) * Math.sin(a)}
        stroke={long ? GOLD_MED : 'rgba(196,97,31,0.4)'}
        strokeWidth={long ? 1.5 : 0.7}
      />
    );
  }

  return (
    <div className="relative w-full max-w-[500px] mx-auto">
      {/* Tooltip */}
      {tooltip && (
        <div className="absolute z-20 pointer-events-none"
          style={{
            left: `${(tooltip.x / 600) * 100}%`,
            top: `${(tooltip.y / 600) * 100}%`,
            transform: 'translate(-50%, -120%)',
          }}>
          <div className="bg-white border border-[#C4611F] rounded-lg px-3 py-2 shadow-lg text-xs" style={{ fontFamily: 'Inter, sans-serif' }}>
            <p className="font-semibold text-[#1a1a2e]">{tooltip.planet}</p>
            <p className="text-[#8B4513]">{tooltip.sign} {tooltip.degree.toFixed(1)}&deg;</p>
            {tooltip.retrograde && <p className="text-red-600 font-semibold">{hi ? 'वक्री' : 'Retrograde'} &#x21BA;</p>}
            <p className="text-gray-500">{MALEFIC.has(tooltip.planet) ? (hi ? 'पापी' : 'Malefic') : (hi ? 'शुभ' : 'Benefic')}</p>
          </div>
        </div>
      )}

      <div className="chakra-float" style={{ transformStyle: 'preserve-3d' }}>
        <svg viewBox="0 0 600 600" className="w-full h-full" style={{
          filter: 'drop-shadow(6px 12px 20px rgba(139,69,19,0.35)) drop-shadow(0px 4px 8px rgba(196,97,31,0.2))',
          overflow: 'visible',
        }}>
          {/* Rings */}
          <circle cx={CX} cy={CY} r={R_OUTER} fill="none" stroke={GOLD} strokeWidth={2.5} />
          {ticks}
          <circle cx={CX} cy={CY} r={R_SIGN_RING} fill="none" stroke="rgba(196,97,31,0.3)" strokeWidth={0.8} />
          <circle cx={CX} cy={CY} r={R_INNER_RING} fill="none" stroke={GOLD} strokeWidth={1} />

          {/* Inner gradient fill */}
          <defs>
            <radialGradient id="innerGrad" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stopColor="#FAF7F2" />
              <stop offset="100%" stopColor="#F0E8D8" stopOpacity={0.5} />
            </radialGradient>
          </defs>
          <circle cx={CX} cy={CY} r={R_INNER_RING} fill="url(#innerGrad)" />

          {/* Sign labels + dividers */}
          {signElements}

          {/* Transit planet dots */}
          {!loading && planetDots}

          {/* Center sun area */}
          <circle cx={CX} cy={CY} r={R_OM} fill="#FAF7F2" stroke={GOLD_MED} strokeWidth={1.5} />
          {sunRays}

          {/* Center content */}
          {loading ? (
            <text x={CX} y={CY} textAnchor="middle" dominantBaseline="central"
              fill={GOLD_MED} fontSize="10" fontFamily="'Inter',sans-serif">
              {hi ? 'लोड हो रहा...' : 'Loading...'}
            </text>
          ) : (
            <>
              <text x={CX} y={CY - 14} textAnchor="middle" fill={GOLD_MED} fontSize="9" fontFamily="'Inter',sans-serif">
                {dateStr}
              </text>
              <text x={CX} y={CY + 4} textAnchor="middle" fill={GOLD_MED} fontSize="20" fontWeight="bold">
                {hi ? 'ॐ' : 'ॐ'}
              </text>
              <text x={CX} y={CY + 20} textAnchor="middle" fill={GOLD} fontSize="10" fontWeight="600" fontFamily="'Inter',sans-serif">
                {timeStr}
              </text>
            </>
          )}

          {/* Error overlay */}
          {error && !loading && (
            <text x={CX} y={CY + 38} textAnchor="middle" fill="#a83232" fontSize="8" fontFamily="'Inter',sans-serif">
              {hi ? 'लाइव डेटा अनुपलब्ध' : 'Live data unavailable'}
            </text>
          )}
        </svg>
      </div>

      {/* Legend */}
      <div className="flex flex-wrap justify-center gap-4 mt-4 text-xs" style={{ fontFamily: 'Inter, sans-serif', color: GOLD }}>
        <div className="flex items-center gap-1.5">
          <span className="w-3 h-3 rounded-full" style={{ background: GOLD_MED }} />
          {hi ? 'शुभ ग्रह' : 'Benefic'}
        </div>
        <div className="flex items-center gap-1.5">
          <span className="w-3 h-3 rounded-full" style={{ background: '#a83232' }} />
          {hi ? 'पापी ग्रह' : 'Malefic'}
        </div>
        <div className="flex items-center gap-1.5">
          <span className="text-red-600 font-bold">R</span>
          {hi ? 'वक्री' : 'Retrograde'}
        </div>
      </div>
    </div>
  );
}
