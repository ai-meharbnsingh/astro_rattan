import { useState, useEffect, useCallback } from 'react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';

const toRad = (deg: number) => (deg * Math.PI) / 180;
const CX = 300;
const CY = 300;

const SIGNS_EN = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces'];
const SIGNS_HI = ['मेष','वृषभ','मिथुन','कर्क','सिंह','कन्या','तुला','वृश्चिक','धनु','मकर','कुंभ','मीन'];
const SIGNS_SHORT = ['Ari','Tau','Gem','Can','Leo','Vir','Lib','Sco','Sag','Cap','Aqu','Pis'];

const PLANET_ABBR: Record<string, string> = {
  Sun:'Su', Moon:'Mo', Mars:'Ma', Mercury:'Me',
  Jupiter:'Ju', Venus:'Ve', Saturn:'Sa', Rahu:'Ra', Ketu:'Ke',
};
const PLANET_HI: Record<string, string> = {
  Sun:'सू', Moon:'चं', Mars:'मं', Mercury:'बु',
  Jupiter:'गु', Venus:'शु', Saturn:'श', Rahu:'रा', Ketu:'के',
};
const MALEFIC = new Set(['Mars','Saturn','Rahu','Ketu']);

interface TransitPlanet {
  planet: string; sign: string; longitude: number;
  sign_degree: number; is_retrograde: boolean;
}
interface TooltipData {
  planet: string; sign: string; degree: number;
  retrograde: boolean; x: number; y: number;
}

/* ── Ring radii matching reference layout ── */
const R_LABEL = 288;      // sign name text (OUTSIDE outer ring)
const R_OUTER = 270;      // outermost circle
const R_OUTER_IN = 255;   // inner edge of sign band
const R_RING3 = 225;      // 3rd ring
const R_TRANSIT = 200;    // transit planet dots
const R_RING2 = 170;      // 2nd ring
const R_RING1 = 130;      // 1st inner ring
const R_INNER = 90;       // innermost ring
const R_CENTER = 40;      // center circle

const GOLD = '#8B4513';
const GOLD_MED = '#C4611F';
const DARK = '#1a1a2e';

function signIdx(sign: string): number {
  return Math.max(0, SIGNS_EN.findIndex(s => s.toLowerCase() === sign.toLowerCase()));
}
function pAngle(p: TransitPlanet): number {
  return signIdx(p.sign) * 30 + p.sign_degree - 90;
}
function arcRot(midDeg: number): number {
  const t = ((midDeg + 90) % 360 + 360) % 360;
  return (t > 90 && t < 270) ? t + 180 : t;
}

export default function LiveTransitWheel() {
  const { language } = useTranslation();
  const hi = language === 'hi';

  const [planets, setPlanets] = useState<TransitPlanet[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [currentTime, setCurrentTime] = useState(new Date());
  const [tooltip, setTooltip] = useState<TooltipData | null>(null);

  const fetchSky = useCallback(async () => {
    try {
      const data = await api.get('/api/kundli/current-sky');
      setPlanets(data.planets || []);
      setError(false);
    } catch { setError(true); }
    setLoading(false);
  }, []);

  useEffect(() => { fetchSky(); const iv = setInterval(fetchSky, 60000); return () => clearInterval(iv); }, [fetchSky]);
  useEffect(() => { const iv = setInterval(() => setCurrentTime(new Date()), 1000); return () => clearInterval(iv); }, []);

  const timeStr = currentTime.toLocaleTimeString(hi ? 'hi-IN' : 'en-IN', { hour:'2-digit', minute:'2-digit', second:'2-digit' });

  /* ── Tick marks on outer ring ── */
  const ticks: JSX.Element[] = [];
  for (let i = 0; i < 360; i += 1) {
    const a = toRad(i);
    const isMajor = i % 30 === 0;
    const isMid = i % 10 === 0;
    if (!isMajor && !isMid && i % 5 !== 0) continue;
    const r2 = isMajor ? R_OUTER - 12 : isMid ? R_OUTER - 7 : R_OUTER - 4;
    ticks.push(
      <line key={`t${i}`}
        x1={CX + R_OUTER * Math.cos(a)} y1={CY + R_OUTER * Math.sin(a)}
        x2={CX + r2 * Math.cos(a)} y2={CY + r2 * Math.sin(a)}
        stroke="rgba(139,69,19,0.25)" strokeWidth={isMajor ? 1.2 : 0.5}
      />
    );
  }

  /* ── Sign labels outside + divider lines ── */
  const signEls = SIGNS_EN.map((sign, i) => {
    const startDeg = i * 30 - 90;
    const midDeg = startDeg + 15;
    const startRad = toRad(startDeg);
    const midRad = toRad(midDeg);

    // Divider line from inner to outer
    const lx1 = CX + R_INNER * Math.cos(startRad);
    const ly1 = CY + R_INNER * Math.sin(startRad);
    const lx2 = CX + R_OUTER * Math.cos(startRad);
    const ly2 = CY + R_OUTER * Math.sin(startRad);

    // Sign name OUTSIDE the outer ring
    const tx = CX + R_LABEL * Math.cos(midRad);
    const ty = CY + R_LABEL * Math.sin(midRad);
    const rot = arcRot(midDeg);
    const label = hi ? SIGNS_HI[i] : SIGNS_SHORT[i];

    return (
      <g key={sign}>
        <line x1={lx1} y1={ly1} x2={lx2} y2={ly2}
          stroke="rgba(139,69,19,0.2)" strokeWidth={0.8} />
        <text x={tx} y={ty} textAnchor="middle" dominantBaseline="central"
          fill={GOLD} fontSize="11" fontWeight="600" fontFamily="'Inter',sans-serif"
          transform={`rotate(${rot},${tx},${ty})`}>{label}</text>
      </g>
    );
  });

  /* ── Planet dots on transit ring ── */
  const planetDots = planets.map((p, i) => {
    const angle = pAngle(p);
    const rad = toRad(angle);
    const px = CX + R_TRANSIT * Math.cos(rad);
    const py = CY + R_TRANSIT * Math.sin(rad);
    const isMalefic = MALEFIC.has(p.planet);
    const abbr = hi ? PLANET_HI[p.planet] || p.planet.slice(0,2) : PLANET_ABBR[p.planet] || p.planet.slice(0,2);

    return (
      <g key={p.planet} className="transit-dot" style={{ animationDelay: `${i * 0.08}s` }}
        onMouseEnter={() => setTooltip({ planet: p.planet, sign: p.sign, degree: p.sign_degree, retrograde: p.is_retrograde, x: px, y: py })}
        onMouseLeave={() => setTooltip(null)}>
        <circle cx={px} cy={py} r={15}
          fill={isMalefic ? DARK : GOLD_MED}
          stroke={isMalefic ? '#a83232' : GOLD}
          strokeWidth={1.5}
          style={{ transition: 'cx 1s ease, cy 1s ease' }}
        />
        <text x={px} y={py + 1} textAnchor="middle" dominantBaseline="central"
          fill="white" fontSize="8" fontWeight="700" fontFamily="'Inter',sans-serif"
        >{abbr}</text>
        {p.is_retrograde && (
          <text x={px + 10} y={py - 10} fill="#ff4444" fontSize="7" fontWeight="bold">R</text>
        )}
      </g>
    );
  });

  return (
    <div className="relative w-full max-w-[460px] mx-auto" style={{ padding: '16px' }}>
      {/* Tooltip */}
      {tooltip && (
        <div className="absolute z-20 pointer-events-none"
          style={{ left: `${((tooltip.x + 16) / 600) * 100}%`, top: `${((tooltip.y) / 600) * 100}%`, transform: 'translate(-50%, -120%)' }}>
          <div className="bg-white border border-[#C4611F] rounded-lg px-3 py-2 shadow-lg text-xs" style={{ fontFamily: 'Inter,sans-serif' }}>
            <p className="font-semibold" style={{ color: DARK }}>{tooltip.planet}</p>
            <p style={{ color: GOLD }}>{tooltip.sign} {tooltip.degree.toFixed(1)}&deg;</p>
            {tooltip.retrograde && <p className="text-red-600 font-semibold">{hi ? 'वक्री' : 'Retrograde'}</p>}
          </div>
        </div>
      )}

      <div className="chakra-float" style={{ transformStyle: 'preserve-3d' }}>
        <svg viewBox="0 0 600 600" className="w-full h-full" style={{
          overflow: 'visible',
          filter: 'drop-shadow(4px 8px 16px rgba(139,69,19,0.3)) drop-shadow(0 2px 6px rgba(196,97,31,0.15))',
        }}>
          {/* ── Concentric rings ── */}
          <circle cx={CX} cy={CY} r={R_OUTER} fill="none" stroke={GOLD} strokeWidth={2} />
          <circle cx={CX} cy={CY} r={R_OUTER_IN} fill="none" stroke="rgba(139,69,19,0.15)" strokeWidth={0.6} />
          {ticks}

          <circle cx={CX} cy={CY} r={R_RING3} fill="none" stroke="rgba(139,69,19,0.12)" strokeWidth={0.6} strokeDasharray="4,3" />
          <circle cx={CX} cy={CY} r={R_RING2} fill="none" stroke="rgba(139,69,19,0.15)" strokeWidth={0.8} />
          <circle cx={CX} cy={CY} r={R_RING1} fill="none" stroke="rgba(139,69,19,0.12)" strokeWidth={0.6} strokeDasharray="4,3" />
          <circle cx={CX} cy={CY} r={R_INNER} fill="none" stroke="rgba(139,69,19,0.2)" strokeWidth={1} />

          {/* Inner fill — subtle gradient */}
          <defs>
            <radialGradient id="innerBg" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stopColor="#FAF7F2" />
              <stop offset="80%" stopColor="#F3EDE0" stopOpacity={0.4} />
              <stop offset="100%" stopColor="#EDE5D4" stopOpacity={0.2} />
            </radialGradient>
          </defs>
          <circle cx={CX} cy={CY} r={R_INNER} fill="url(#innerBg)" />

          {/* Center circle */}
          <circle cx={CX} cy={CY} r={R_CENTER} fill="#FAF7F2" stroke="rgba(139,69,19,0.25)" strokeWidth={1} />
          <circle cx={CX} cy={CY} r={R_CENTER - 8} fill="none" stroke="rgba(139,69,19,0.12)" strokeWidth={0.5} />

          {/* Sign labels + dividers */}
          {signEls}

          {/* Transit planet dots */}
          {!loading && planetDots}

          {/* Center content */}
          {loading ? (
            <text x={CX} y={CY} textAnchor="middle" dominantBaseline="central"
              fill={GOLD_MED} fontSize="8" fontFamily="'Inter',sans-serif">
              {hi ? 'लोड हो रहा...' : 'Loading...'}
            </text>
          ) : (
            <>
              <text x={CX} y={CY - 4} textAnchor="middle" fill={GOLD_MED} fontSize="12" fontWeight="bold">ॐ</text>
              <text x={CX} y={CY + 10} textAnchor="middle" fill={GOLD} fontSize="6.5" fontWeight="600" fontFamily="'Inter',sans-serif">
                {timeStr}
              </text>
            </>
          )}

          {error && !loading && (
            <text x={CX} y={CY + 22} textAnchor="middle" fill="#a83232" fontSize="6" fontFamily="'Inter',sans-serif">
              {hi ? 'लाइव डेटा अनुपलब्ध' : 'Live data unavailable'}
            </text>
          )}
        </svg>
      </div>

      {/* Legend */}
      <div className="flex flex-wrap justify-center gap-4 mt-3 text-[11px]" style={{ fontFamily: 'Inter,sans-serif', color: GOLD }}>
        <div className="flex items-center gap-1.5">
          <span className="w-2.5 h-2.5 rounded-full" style={{ background: GOLD_MED }} />
          {hi ? 'शुभ' : 'Benefic'}
        </div>
        <div className="flex items-center gap-1.5">
          <span className="w-2.5 h-2.5 rounded-full" style={{ background: DARK }} />
          {hi ? 'पापी' : 'Malefic'}
        </div>
        <div className="flex items-center gap-1.5">
          <span className="text-red-600 font-bold text-xs">R</span>
          {hi ? 'वक्री' : 'Retro'}
        </div>
      </div>
    </div>
  );
}
