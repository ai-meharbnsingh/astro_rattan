import { useState, useEffect, useCallback } from 'react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';

const toRad = (deg: number) => (deg * Math.PI) / 180;
const CX = 300;
const CY = 300;

const SIGNS_EN = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces'];
const SIGNS_HI = ['मेष','वृषभ','मिथुन','कर्क','सिंह','कन्या','तुला','वृश्चिक','धनु','मकर','कुंभ','मीन'];
const SIGNS_SHORT = ['Ari','Tau','Gem','Can','Leo','Vir','Lib','Sco','Sag','Cap','Aqu','Pis'];
const GLYPHS = ['\u2648','\u2649','\u264A','\u264B','\u264C','\u264D','\u264E','\u264F','\u2650','\u2651','\u2652','\u2653'];
const SIGN_DEGS = ['0-30','30-60','60-90','90-120','120-150','150-180','180-210','210-240','240-270','270-300','300-330','330-360'];

const PLANET_ABBR: Record<string,string> = { Sun:'Su',Moon:'Mo',Mars:'Ma',Mercury:'Me',Jupiter:'Ju',Venus:'Ve',Saturn:'Sa',Rahu:'Ra',Ketu:'Ke' };
const PLANET_HI: Record<string,string> = { Sun:'सू',Moon:'चं',Mars:'मं',Mercury:'बु',Jupiter:'गु',Venus:'शु',Saturn:'श',Rahu:'रा',Ketu:'के' };
const PLANET_FULL_HI: Record<string,string> = { Sun:'सूर्य',Moon:'चंद्र',Mars:'मंगल',Mercury:'बुध',Jupiter:'बृहस्पति',Venus:'शुक्र',Saturn:'शनि',Rahu:'राहु',Ketu:'केतु' };
const MALEFIC = new Set(['Mars','Saturn','Rahu','Ketu']);

// Ring assignments — separate fast/slow/nodes
const RING_A = new Set(['Sun','Moon','Venus','Mercury']);  // r=230 fast
const RING_B = new Set(['Mars','Jupiter','Saturn']);        // r=195 slow
// RING_C = Rahu, Ketu                                     // r=160 nodes
// Spread planets across 5 sub-rings to avoid clustering
const RING_R: Record<string, number> = {
  Sun: 238, Moon: 215, Venus: 238, Mercury: 215,
  Mars: 190, Jupiter: 170, Saturn: 190,
  Rahu: 148, Ketu: 148,
};

interface TransitPlanet {
  planet: string; sign: string; longitude: number;
  sign_degree: number; is_retrograde: boolean;
}
interface TooltipData {
  planet: string; sign: string; degree: number;
  retrograde: boolean; x: number; y: number;
}
interface SkyData {
  planets: TransitPlanet[];
  lagna_sign: string;
  lagna_longitude: number;
}

const R_LABEL = 288;
const R_OUTER = 270;
const R_OUTER_IN = 255;
const R_RING_A = 230;
const R_RING_B = 195;
const R_RING_C = 160;
const R_INNER = 130;
const R_CENTER = 50;

const GOLD = '#8B4513';
const GOLD_MED = '#C4611F';
const DARK = '#1a1a2e';

function signIdx(sign: string): number {
  return Math.max(0, SIGNS_EN.findIndex(s => s.toLowerCase() === sign.toLowerCase()));
}
function absAngle(p: TransitPlanet): number {
  return signIdx(p.sign) * 30 + p.sign_degree - 90;
}
function arcRot(midDeg: number): number {
  const t = ((midDeg + 90) % 360 + 360) % 360;
  return (t > 90 && t < 270) ? t + 180 : t;
}

/** De-overlap planets on same ring: ensure min 18deg separation */
function deOverlap(items: { planet: string; angle: number; ring: number }[]): { planet: string; angle: number; ring: number }[] {
  // Group by ring
  const byRing = new Map<number, typeof items>();
  for (const it of items) {
    const arr = byRing.get(it.ring) || [];
    arr.push(it);
    byRing.set(it.ring, arr);
  }
  const result: typeof items = [];
  for (const [ring, group] of byRing) {
    group.sort((a, b) => a.angle - b.angle);
    for (let i = 1; i < group.length; i++) {
      let diff = group[i].angle - group[i - 1].angle;
      if (diff < 18) {
        const shift = (18 - diff) / 2;
        group[i - 1].angle -= shift;
        group[i].angle += shift;
      }
    }
    result.push(...group);
  }
  return result;
}

export default function LiveTransitWheel() {
  const { language } = useTranslation();
  const hi = language === 'hi';

  const [skyData, setSkyData] = useState<SkyData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [currentTime, setCurrentTime] = useState(new Date());
  const [tooltip, setTooltip] = useState<TooltipData | null>(null);

  const fetchSky = useCallback(async () => {
    try {
      const data = await api.get('/api/kundli/current-sky');
      setSkyData(data);
      setError(false);
    } catch { setError(true); }
    setLoading(false);
  }, []);

  useEffect(() => { fetchSky(); const iv = setInterval(fetchSky, 60000); return () => clearInterval(iv); }, [fetchSky]);
  useEffect(() => { const iv = setInterval(() => setCurrentTime(new Date()), 1000); return () => clearInterval(iv); }, []);

  const timeStr = currentTime.toLocaleTimeString(hi ? 'hi-IN' : 'en-IN', { hour:'2-digit', minute:'2-digit', second:'2-digit' });
  const planets = skyData?.planets || [];
  const lagnaLong = skyData?.lagna_longitude || 0;
  const lagnaAngle = lagnaLong - 90;

  // Prepare planet positions with ring assignment + de-overlap
  const positioned = deOverlap(
    planets.map(p => ({ planet: p.planet, angle: absAngle(p), ring: RING_R[p.planet] || R_RING_C }))
  );
  const posMap = new Map(positioned.map(p => [p.planet, p]));

  /* ── Ticks ── */
  const ticks: JSX.Element[] = [];
  for (let i = 0; i < 360; i += 5) {
    const a = toRad(i);
    const isMajor = i % 30 === 0;
    const isMid = i % 10 === 0;
    const r2 = isMajor ? R_OUTER - 12 : isMid ? R_OUTER - 6 : R_OUTER - 3;
    ticks.push(
      <line key={`t${i}`}
        x1={CX + R_OUTER * Math.cos(a)} y1={CY + R_OUTER * Math.sin(a)}
        x2={CX + r2 * Math.cos(a)} y2={CY + r2 * Math.sin(a)}
        stroke="rgba(139,69,19,0.2)" strokeWidth={isMajor ? 1.2 : 0.4}
      />
    );
  }

  /* ── Sign labels + dividers ── */
  const signEls = SIGNS_EN.map((sign, i) => {
    const startDeg = i * 30 - 90;
    const midDeg = startDeg + 15;
    const startRad = toRad(startDeg);
    const midRad = toRad(midDeg);

    const lx1 = CX + R_INNER * Math.cos(startRad);
    const ly1 = CY + R_INNER * Math.sin(startRad);
    const lx2 = CX + R_OUTER * Math.cos(startRad);
    const ly2 = CY + R_OUTER * Math.sin(startRad);

    const tx = CX + R_LABEL * Math.cos(midRad);
    const ty = CY + R_LABEL * Math.sin(midRad);
    const rot = arcRot(midDeg);
    const label = hi ? SIGNS_HI[i] : SIGNS_SHORT[i];

    // Watermark glyph inside segment (between inner and outer ring)
    const wmR = (R_INNER + R_OUTER) / 2;
    const wmx = CX + wmR * Math.cos(midRad);
    const wmy = CY + wmR * Math.sin(midRad);

    // Degree number at outer rim for start of each sign
    const degLabelR = R_OUTER + 14;
    const dlx = CX + degLabelR * Math.cos(startRad);
    const dly = CY + degLabelR * Math.sin(startRad);
    const dlRot = arcRot(startDeg);
    const degNum = i * 30;

    return (
      <g key={sign}>
        <line x1={lx1} y1={ly1} x2={lx2} y2={ly2} stroke="rgba(139,69,19,0.15)" strokeWidth={0.7} />
        {/* Sign name outside */}
        <text x={tx} y={ty - 6} textAnchor="middle" dominantBaseline="central"
          fill={GOLD} fontSize="14" fontWeight="700" fontFamily="'Inter',sans-serif"
          transform={`rotate(${rot},${tx},${ty - 6})`}>{label}</text>
        {/* Watermark zodiac glyph inside segment */}
        <text x={wmx} y={wmy} textAnchor="middle" dominantBaseline="central"
          fill="rgba(139,69,19,0.08)" fontSize="36"
          fontFamily="'Segoe UI Symbol','Noto Sans Symbols 2',serif"
        >{GLYPHS[i]}</text>
      </g>
    );
  });

  /* ── Planet positions with pixel-level collision resolution ── */
  const DOT_R = 26;
  const MIN_DIST = DOT_R * 2 + 6; // 58px min between dot centers

  // Calculate initial pixel positions
  let dotPositions = planets.map((p) => {
    const pos = posMap.get(p.planet);
    const ring = pos?.ring || R_RING_C;
    const angle = pos?.angle || absAngle(p);
    const rad = toRad(angle);
    return { planet: p, x: CX + ring * Math.cos(rad), y: CY + ring * Math.sin(rad) };
  });

  // Resolve overlaps — 10 iterations with strong push
  for (let iter = 0; iter < 10; iter++) {
    for (let i = 0; i < dotPositions.length; i++) {
      for (let j = i + 1; j < dotPositions.length; j++) {
        const dx = dotPositions[i].x - dotPositions[j].x;
        const dy = dotPositions[i].y - dotPositions[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < MIN_DIST && dist > 0) {
          const angle = Math.atan2(dy, dx);
          const push = (MIN_DIST - dist) / 2 + 8;
          dotPositions[i].x += Math.cos(angle) * push;
          dotPositions[i].y += Math.sin(angle) * push;
          dotPositions[j].x -= Math.cos(angle) * push;
          dotPositions[j].y -= Math.sin(angle) * push;
        }
      }
    }
  }

  const planetDots = dotPositions.map(({ planet: p, x: px, y: py }, i) => {
    const isMalefic = MALEFIC.has(p.planet);
    const abbr = hi ? PLANET_HI[p.planet] : PLANET_ABBR[p.planet];
    const degText = `${Math.floor(p.sign_degree)}\u00B0`;

    return (
      <g key={p.planet} className="transit-dot" style={{ animationDelay: `${i * 0.08}s` }}
        onMouseEnter={() => setTooltip({ planet: p.planet, sign: p.sign, degree: p.sign_degree, retrograde: p.is_retrograde, x: px, y: py })}
        onMouseLeave={() => setTooltip(null)}
        cursor="pointer"
      >
        {/* Main dot — red ring if retrograde */}
        <circle cx={px} cy={py} r={DOT_R}
          fill={isMalefic ? DARK : GOLD_MED}
          stroke={p.is_retrograde ? '#FF3333' : (isMalefic ? '#a83232' : GOLD)}
          strokeWidth={p.is_retrograde ? 3 : 1.5}
          style={{ transition: 'all 1s ease' }}
        />
        {/* Planet abbreviation */}
        <text x={px} y={py - 5} textAnchor="middle" dominantBaseline="central"
          fill="white" fontSize="11" fontWeight="700" fontFamily="'Inter',sans-serif"
        >{abbr}</text>
        {/* Degree */}
        <text x={px} y={py + 8} textAnchor="middle" dominantBaseline="central"
          fill="rgba(255,255,255,0.85)" fontSize="10" fontFamily="'Inter',sans-serif"
        >{degText}</text>
        {/* Retrograde ℞ symbol above dot */}
        {p.is_retrograde && (
          <text x={px} y={py - DOT_R - 8} textAnchor="middle" dominantBaseline="central"
            fill="#FF3333" fontSize="12" fontWeight="700">{'\u211E'}</text>
        )}
      </g>
    );
  });

  /* ── Ascendant marker ── */
  const ascRad = toRad(lagnaAngle);
  const ascX = CX + R_OUTER * Math.cos(ascRad);
  const ascY = CY + R_OUTER * Math.sin(ascRad);
  const ascLabelX = CX + (R_LABEL + 8) * Math.cos(ascRad);
  const ascLabelY = CY + (R_LABEL + 8) * Math.sin(ascRad);
  const ascDeg = Math.floor(lagnaLong % 30);

  const ascMarker = (
    <g>
      {/* Dashed line from center to ASC */}
      <line x1={CX} y1={CY} x2={ascX} y2={ascY}
        stroke={GOLD_MED} strokeWidth={2} strokeDasharray="5,4" opacity={0.7} />
      {/* Dot at rim */}
      <circle cx={ascX} cy={ascY} r={6} fill={GOLD_MED} />
      {/* Triangle pointing inward — larger */}
      <polygon
        points={`${ascX},${ascY} ${ascX + 12 * Math.cos(ascRad + 0.35)},${ascY + 12 * Math.sin(ascRad + 0.35)} ${ascX + 12 * Math.cos(ascRad - 0.35)},${ascY + 12 * Math.sin(ascRad - 0.35)}`}
        fill={GOLD_MED}
      />
      {/* Label */}
      <text x={ascLabelX} y={ascLabelY} textAnchor="middle" dominantBaseline="central"
        fill={GOLD_MED} fontSize="13" fontWeight="700" fontFamily="'Inter',sans-serif"
        transform={`rotate(${arcRot(lagnaAngle + 90)},${ascLabelX},${ascLabelY})`}
      >ASC {ascDeg}&deg;</text>
    </g>
  );

  return (
    <div className="relative w-full max-w-[460px] mx-auto" style={{ padding: '12px' }}>
      {/* Tooltip */}
      {tooltip && (
        <div className="absolute z-20 pointer-events-none"
          style={{ left: `${((tooltip.x + 16) / 600) * 100}%`, top: `${(tooltip.y / 600) * 100}%`, transform: 'translate(-50%,-130%)' }}>
          <div className="bg-white border border-[#C4611F] rounded-lg px-3 py-2 shadow-lg text-xs" style={{ fontFamily:'Inter,sans-serif', minWidth: '120px' }}>
            <p className="font-bold" style={{ color: DARK }}>{tooltip.planet} ({hi ? PLANET_FULL_HI[tooltip.planet] : tooltip.planet})</p>
            <p style={{ color: GOLD }}>{tooltip.sign} ({hi ? SIGNS_HI[signIdx(tooltip.sign)] : tooltip.sign})</p>
            <p style={{ color: GOLD_MED }}>{tooltip.degree.toFixed(1)}&deg;</p>
            <p className="text-gray-500">{MALEFIC.has(tooltip.planet) ? (hi ? 'पापी' : 'Malefic') : (hi ? 'शुभ' : 'Benefic')} &middot; {tooltip.retrograde ? (hi ? 'वक्री' : 'Retrograde') : (hi ? 'मार्गी' : 'Direct')}</p>
          </div>
        </div>
      )}

      <div className="chakra-float" style={{ transformStyle: 'preserve-3d' }}>
        <svg viewBox="0 0 600 600" className="w-full h-full" style={{
          overflow: 'visible',
          filter: 'drop-shadow(4px 8px 16px rgba(139,69,19,0.25)) drop-shadow(0 2px 6px rgba(196,97,31,0.12))',
        }}>
          {/* Rings */}
          <circle cx={CX} cy={CY} r={R_OUTER} fill="none" stroke={GOLD} strokeWidth={2} />
          <circle cx={CX} cy={CY} r={R_OUTER_IN} fill="none" stroke="rgba(139,69,19,0.12)" strokeWidth={0.5} />
          {ticks}

          {/* Three orbital rings — dashed for clarity */}
          <circle cx={CX} cy={CY} r={R_RING_A} fill="none" stroke="rgba(139,69,19,0.1)" strokeWidth={0.6} strokeDasharray="3,4" />
          <circle cx={CX} cy={CY} r={R_RING_B} fill="none" stroke="rgba(139,69,19,0.12)" strokeWidth={0.6} strokeDasharray="3,4" />
          <circle cx={CX} cy={CY} r={R_RING_C} fill="none" stroke="rgba(139,69,19,0.1)" strokeWidth={0.6} strokeDasharray="3,4" />

          <circle cx={CX} cy={CY} r={R_INNER} fill="none" stroke="rgba(139,69,19,0.18)" strokeWidth={0.8} />

          {/* Inner fill */}
          <defs>
            <radialGradient id="iBg" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stopColor="#FAF7F2" />
              <stop offset="100%" stopColor="#F0E8D8" stopOpacity={0.3} />
            </radialGradient>
          </defs>
          <circle cx={CX} cy={CY} r={R_INNER} fill="url(#iBg)" />

          {/* Center */}
          <circle cx={CX} cy={CY} r={R_CENTER} fill="#FAF7F2" stroke="rgba(139,69,19,0.2)" strokeWidth={0.8} />

          {/* Signs */}
          {signEls}

          {/* Ascendant */}
          {!loading && skyData && ascMarker}

          {/* Planets */}
          {!loading && planetDots}

          {/* Center content */}
          {loading ? (
            <text x={CX} y={CY} textAnchor="middle" dominantBaseline="central"
              fill={GOLD_MED} fontSize="8" fontFamily="'Inter',sans-serif">
              {hi ? 'लोड हो रहा...' : 'Loading...'}
            </text>
          ) : (
            <>
              <text x={CX} y={CY - 5} textAnchor="middle" fill={GOLD_MED} fontSize="28" fontWeight="bold">ॐ</text>
              <text x={CX} y={CY + 18} textAnchor="middle" fill={GOLD} fontSize="13" fontWeight="600" fontFamily="'Inter',sans-serif">{timeStr}</text>
            </>
          )}
          {error && !loading && (
            <text x={CX} y={CY + 22} textAnchor="middle" fill="#a83232" fontSize="6">
              {hi ? 'अनुपलब्ध' : 'Unavailable'}
            </text>
          )}
        </svg>
      </div>

      {/* Legend */}
      <div className="flex flex-wrap justify-center gap-3 mt-3 text-[10px]" style={{ fontFamily:'Inter,sans-serif', color: GOLD }}>
        <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-full" style={{ background: GOLD_MED }} />{hi ? 'शुभ' : 'Benefic'}</span>
        <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-full" style={{ background: DARK }} />{hi ? 'पापी' : 'Malefic'}</span>
        <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-full bg-red-600" /><span className="text-red-600 font-bold">R</span> {hi ? 'वक्री' : 'Retro'}</span>
        <span className="flex items-center gap-1"><span className="w-2.5 h-2.5" style={{ background: GOLD_MED, clipPath: 'polygon(50% 0%, 0% 100%, 100% 100%)' }} />ASC</span>
      </div>
    </div>
  );
}
