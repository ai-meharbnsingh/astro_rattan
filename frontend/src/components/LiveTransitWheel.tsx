import { useState, useEffect, useCallback } from 'react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';

const toRad = (deg: number) => (deg * Math.PI) / 180;
const CX = 300;
const CY = 300;

const SIGNS = [
  { en: 'Aries',       hi: 'मेष',     glyph: '\u2648\uFE0E', dates: 'Mar 21-Apr 19', datesHi: '21 मार्च-19 अप्रै', gender: '\u2642', elemIcon: '\u{1F525}', img: '/images/zodiac/aries.jpg' },
  { en: 'Taurus',      hi: 'वृषभ',    glyph: '\u2649\uFE0E', dates: 'Apr 20-May 20', datesHi: '20 अप्रै-20 मई',    gender: '\u2640', elemIcon: '\u{1F30D}', img: '/images/zodiac/taurus.jpg' },
  { en: 'Gemini',      hi: 'मिथुन',   glyph: '\u264A\uFE0E', dates: 'May 21-Jun 20', datesHi: '21 मई-20 जून',      gender: '\u2642', elemIcon: '\u{1F4A8}', img: '/images/zodiac/gemini.jpg' },
  { en: 'Cancer',      hi: 'कर्क',    glyph: '\u264B\uFE0E', dates: 'Jun 21-Jul 22', datesHi: '21 जून-22 जुला',    gender: '\u2640', elemIcon: '\u{1F4A7}', img: '/images/zodiac/cancer.jpg' },
  { en: 'Leo',         hi: 'सिंह',    glyph: '\u264C\uFE0E', dates: 'Jul 23-Aug 22', datesHi: '23 जुला-22 अग',     gender: '\u2642', elemIcon: '\u{1F525}', img: '/images/zodiac/leo.jpg' },
  { en: 'Virgo',       hi: 'कन्या',   glyph: '\u264D\uFE0E', dates: 'Aug 23-Sep 22', datesHi: '23 अग-22 सित',     gender: '\u2640', elemIcon: '\u{1F30D}', img: '/images/zodiac/virgo.jpg' },
  { en: 'Libra',       hi: 'तुला',    glyph: '\u264E\uFE0E', dates: 'Sep 23-Oct 22', datesHi: '23 सित-22 अक्टू',  gender: '\u2642', elemIcon: '\u{1F4A8}', img: '/images/zodiac/libra.jpg' },
  { en: 'Scorpio',     hi: 'वृश्चिक', glyph: '\u264F\uFE0E', dates: 'Oct 23-Nov 21', datesHi: '23 अक्टू-21 नव',   gender: '\u2640', elemIcon: '\u{1F4A7}', img: '/images/zodiac/scorpio.jpg' },
  { en: 'Sagittarius', hi: 'धनु',     glyph: '\u2650\uFE0E', dates: 'Nov 22-Dec 21', datesHi: '22 नव-21 दिस',     gender: '\u2642', elemIcon: '\u{1F525}', img: '/images/zodiac/sagittarius.jpg' },
  { en: 'Capricorn',   hi: 'मकर',     glyph: '\u2651\uFE0E', dates: 'Dec 22-Jan 19', datesHi: '22 दिस-19 जन',     gender: '\u2640', elemIcon: '\u{1F30D}', img: '/images/zodiac/capricorn.jpg' },
  { en: 'Aquarius',    hi: 'कुंभ',    glyph: '\u2652\uFE0E', dates: 'Jan 20-Feb 18', datesHi: '20 जन-18 फर',      gender: '\u2642', elemIcon: '\u{1F4A8}', img: '/images/zodiac/aquarius.jpg' },
  { en: 'Pisces',      hi: 'मीन',     glyph: '\u2653\uFE0E', dates: 'Feb 19-Mar 20', datesHi: '19 फर-20 मार्च',   gender: '\u2640', elemIcon: '\u{1F4A7}', img: '/images/zodiac/pisces.jpg' },
];

const PLANET_ABBR: Record<string,string> = { Sun:'Su',Moon:'Mo',Mars:'Ma',Mercury:'Me',Jupiter:'Ju',Venus:'Ve',Saturn:'Sa',Rahu:'Ra',Ketu:'Ke' };
const PLANET_HI: Record<string,string> = { Sun:'सू',Moon:'चं',Mars:'मं',Mercury:'बु',Jupiter:'गु',Venus:'शु',Saturn:'श',Rahu:'रा',Ketu:'के' };
const PLANET_FULL_HI: Record<string,string> = { Sun:'सूर्य',Moon:'चंद्र',Mars:'मंगल',Mercury:'बुध',Jupiter:'बृहस्पति',Venus:'शुक्र',Saturn:'शनि',Rahu:'राहु',Ketu:'केतु' };
const MALEFIC = new Set(['Mars','Saturn','Rahu','Ketu']);

const RING_R: Record<string, number> = {
  Sun: 206, Moon: 194, Venus: 206, Mercury: 194,
  Mars: 182, Jupiter: 170, Saturn: 182,
  Rahu: 170, Ketu: 170,
};

interface TransitPlanet { planet: string; sign: string; longitude: number; sign_degree: number; is_retrograde: boolean; }
interface TooltipData { planet: string; sign: string; degree: number; retrograde: boolean; x: number; y: number; }
interface SkyData { planets: TransitPlanet[]; lagna_sign: string; lagna_longitude: number; }

const R_OUTER = 270;
const R_SIGN_NAME = 258;
const R_DATE = 245;
const R_DATE_RING = 244;
const R_IMG = 218;
const R_GENDER = 130; // Moved closer to center
const R_GENDER_RING = 140; // Outer circle for gender symbols — reduced to avoid planet overlap
const R_GLYPH_RING = 112;
const R_GLYPH = 96;
const R_ELEM = 75;
const R_ELEM_RING = 85; // Circle outside elements, between elements and glyphs
const R_SIGN_NUM = 52; // Sign numbers (1-12), inside inner ring near center
const R_INNER = 60;
const R_CENTER = 42;

const GOLD = '#8B4513';
const GOLD_MED = '#C4611F';
const DARK = '#1a1a2e';

function signIdx(sign: string) { return Math.max(0, SIGNS.findIndex(s => s.en.toLowerCase() === sign.toLowerCase())); }
function absAngle(p: TransitPlanet) {
  // Keep planets away from exact sign divider boundaries so symbols/labels don't sit on lines.
  const safeDeg = Math.max(3, Math.min(27, p.sign_degree));
  return signIdx(p.sign) * 30 + safeDeg - 90;
}
function arcRot(midDeg: number) { const t = ((midDeg + 90) % 360 + 360) % 360; return (t > 90 && t < 270) ? t + 180 : t; }

export default function LiveTransitWheel() {
  const { language } = useTranslation();
  const hi = language === 'hi';

  const [skyData, setSkyData] = useState<SkyData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [currentTime, setCurrentTime] = useState(new Date());
  const [tooltip, setTooltip] = useState<TooltipData | null>(null);

  const fetchSky = useCallback(async () => {
    try { const d = await api.get('/api/kundli/current-sky'); setSkyData(d); setError(false); } catch { setError(true); }
    setLoading(false);
  }, []);

  useEffect(() => { fetchSky(); const iv = setInterval(fetchSky, 60000); return () => clearInterval(iv); }, [fetchSky]);
  useEffect(() => { const iv = setInterval(() => setCurrentTime(new Date()), 1000); return () => clearInterval(iv); }, []);

  const timeStr = currentTime.toLocaleTimeString(hi ? 'hi-IN' : 'en-IN', { hour:'2-digit', minute:'2-digit', second:'2-digit' });
  const planets = skyData?.planets || [];
  const lagnaLong = skyData?.lagna_longitude || 0;
  const lagnaAngle = lagnaLong - 90;

  // Ticks
  const ticks: JSX.Element[] = [];
  for (let i = 0; i < 360; i += 5) {
    const a = toRad(i);
    const isMajor = i % 30 === 0;
    const r2 = isMajor ? R_OUTER - 10 : R_OUTER - 3;
    ticks.push(<line key={`t${i}`} x1={CX+R_OUTER*Math.cos(a)} y1={CY+R_OUTER*Math.sin(a)} x2={CX+r2*Math.cos(a)} y2={CY+r2*Math.sin(a)} stroke="rgba(139,69,19,0.2)" strokeWidth={isMajor?1.2:0.4} />);
  }

  // Segments
  const clipDefs = SIGNS.map((_, i) => {
    const midRad = toRad(i * 30 + 15 - 90);
    return <clipPath key={`wc${i}`} id={`wc${i}`}><circle cx={CX + R_IMG * Math.cos(midRad)} cy={CY + R_IMG * Math.sin(midRad)} r={18} /></clipPath>;
  });

  const segEls = SIGNS.map((sign, i) => {
    const startDeg = i * 30 - 90;
    const midDeg = startDeg + 15;
    const startRad = toRad(startDeg);
    const midRad = toRad(midDeg);
    const rot = arcRot(midDeg);

    // Divider line — from CENTER to OUTER
    const lx1 = CX + R_CENTER * Math.cos(startRad);
    const ly1 = CY + R_CENTER * Math.sin(startRad);
    const lx2 = CX + R_OUTER * Math.cos(startRad);
    const ly2 = CY + R_OUTER * Math.sin(startRad);

    const nx = CX + R_SIGN_NAME * Math.cos(midRad);
    const ny = CY + R_SIGN_NAME * Math.sin(midRad);
    const dx = CX + R_DATE * Math.cos(midRad);
    const dy = CY + R_DATE * Math.sin(midRad);
    const ix = CX + R_IMG * Math.cos(midRad);
    const iy = CY + R_IMG * Math.sin(midRad);
    const gndx = CX + R_GENDER * Math.cos(midRad);
    const gndy = CY + R_GENDER * Math.sin(midRad);
    const gx = CX + R_GLYPH * Math.cos(midRad);
    const gy = CY + R_GLYPH * Math.sin(midRad);
    const ex = CX + R_ELEM * Math.cos(midRad);
    const ey = CY + R_ELEM * Math.sin(midRad);
    const snx = CX + R_SIGN_NUM * Math.cos(midRad);
    const sny = CY + R_SIGN_NUM * Math.sin(midRad);

    const degStart = i * 30;
    const degEnd = (i + 1) * 30;
    const signLabel = hi ? sign.hi : sign.en.slice(0, 3);

    return (
      <g key={sign.en}>
        {/* Divider — full extent from center to outer */}
        <line x1={lx1} y1={ly1} x2={lx2} y2={ly2} stroke="rgba(139,69,19,0.15)" strokeWidth={0.7} />

        {/* Ring 1: Sign name + degree span (uniform for all signs) */}
        <text x={nx} y={ny} textAnchor="middle" dominantBaseline="central"
          fill={GOLD} fontSize="13" fontWeight="700" fontFamily="'Inter',sans-serif"
          transform={`rotate(${rot},${nx},${ny})`}>{`${signLabel} ${degStart}°-${degEnd}°`}</text>

        {/* Ring 2: Date range */}
        <text x={dx} y={dy} textAnchor="middle" dominantBaseline="central"
          fill={GOLD_MED} fontSize="12" fontWeight="700" fontFamily="'Inter',sans-serif"
          transform={`rotate(${rot},${dx},${dy})`}>{hi ? sign.datesHi : sign.dates}</text>

        {/* Ring 3: Watermark animal — grayscale */}
        <image href={sign.img} x={ix-18} y={iy-18} width={36} height={36}
          preserveAspectRatio="xMidYMid slice" opacity={0.08}
          clipPath={`url(#wc${i})`}
          style={{ filter: 'grayscale(1) brightness(0.8)' }} />

        {/* Gender symbol — inside, visible */}
        <text x={gndx} y={gndy} textAnchor="middle" dominantBaseline="central"
          fill={GOLD_MED} opacity={0.25} fontSize="16" fontWeight="bold">{sign.gender}</text>

        {/* Ring 4: Zodiac glyph */}
        <text x={gx} y={gy} textAnchor="middle" dominantBaseline="central"
          fill={GOLD_MED} fontSize="18" fontWeight="bold"
          fontFamily="'Segoe UI Symbol','Noto Sans Symbols 2',serif">{sign.glyph}</text>

        {/* Ring 5: Element symbol (not text) */}
        <text x={ex} y={ey} textAnchor="middle" dominantBaseline="central"
          fontSize="14" opacity={0.5}>{sign.elemIcon}</text>

        {/* Ring 6: Sign number (1-12) */}
        <text x={snx} y={sny} textAnchor="middle" dominantBaseline="central"
          fill={GOLD} fontSize="10" fontWeight="600" opacity={0.7}>{i + 1}</text>
      </g>
    );
  });

  // Planet positions — place at MIDPOINT of sign (not on divider lines)
  const DOT_MIN_DIST = 48;
  const LANE_MIN = 162;
  const LANE_MAX = 214;
  let dotPos = planets.map(p => {
    const baseRadius = Math.max(LANE_MIN, Math.min(LANE_MAX, RING_R[p.planet] || 180));
    const angle = toRad(absAngle(p));
    return { planet: p, angle, radius: baseRadius, baseRadius };
  });

  // Collision resolve
  for (let iter = 0; iter < 16; iter++) {
    for (let i = 0; i < dotPos.length; i++) {
      for (let j = i + 1; j < dotPos.length; j++) {
        const ix = CX + dotPos[i].radius * Math.cos(dotPos[i].angle);
        const iy = CY + dotPos[i].radius * Math.sin(dotPos[i].angle);
        const jx = CX + dotPos[j].radius * Math.cos(dotPos[j].angle);
        const jy = CY + dotPos[j].radius * Math.sin(dotPos[j].angle);
        const ddx = ix - jx;
        const ddy = iy - jy;
        const dist = Math.sqrt(ddx * ddx + ddy * ddy);
        if (dist < DOT_MIN_DIST && dist > 0) {
          const push = (DOT_MIN_DIST - dist) / 2 + 4;
          if (dotPos[i].radius <= dotPos[j].radius) {
            dotPos[i].radius -= push * 0.45;
            dotPos[j].radius += push * 0.55;
          } else {
            dotPos[i].radius += push * 0.55;
            dotPos[j].radius -= push * 0.45;
          }
        }
      }
    }
    // Keep all planet labels in the middle lane and near their home ring.
    for (let k = 0; k < dotPos.length; k++) {
      const minR = Math.max(LANE_MIN, dotPos[k].baseRadius - 20);
      const maxR = Math.min(LANE_MAX, dotPos[k].baseRadius + 20);
      dotPos[k].radius = Math.max(minR, Math.min(maxR, dotPos[k].radius));
    }
  }

  const planetDots = dotPos.map(({ planet: p, angle, radius }, i) => {
    const px = CX + radius * Math.cos(angle);
    const py = CY + radius * Math.sin(angle);
    const isMalefic = MALEFIC.has(p.planet);
    const abbr = hi ? PLANET_HI[p.planet] : PLANET_ABBR[p.planet];
    const degText = `${p.sign_degree.toFixed(1)}\u00B0`;
    const textColor = isMalefic ? DARK : GOLD_MED;

    return (
      <g key={p.planet} className="transit-dot" style={{ animationDelay: `${i * 0.08}s` }}
        onMouseEnter={() => setTooltip({ planet: p.planet, sign: p.sign, degree: p.sign_degree, retrograde: p.is_retrograde, x: px, y: py })}
        onMouseLeave={() => setTooltip(null)} cursor="pointer">
        <text x={px} y={py - 4} textAnchor="middle" dominantBaseline="central"
          fill={textColor} fontSize="13" fontWeight="800" fontFamily="'Inter',sans-serif"
          style={{ transition: 'all 1s ease' }}>{abbr}</text>
        <text x={px} y={py + 10} textAnchor="middle" dominantBaseline="central"
          fill={textColor} opacity={0.75} fontSize="9" fontWeight="600" fontFamily="'Inter',sans-serif">{degText}</text>
        {/* Retrograde — ALWAYS show ℞ when is_retrograde is true */}
        {p.is_retrograde && (
          <text x={px + 12} y={py - 7} textAnchor="middle"
            fill="#FF3333" fontSize="13" fontWeight="800">{'\u211E'}</text>
        )}
      </g>
    );
  });

  // ASC
  const ascRad = toRad(lagnaAngle);
  const ascX = CX + R_OUTER * Math.cos(ascRad);
  const ascY = CY + R_OUTER * Math.sin(ascRad);
  const ascLX = CX + (R_SIGN_NAME + 10) * Math.cos(ascRad);
  const ascLY = CY + (R_SIGN_NAME + 10) * Math.sin(ascRad);
  const ascDeg = Math.floor(lagnaLong % 30);

  const ascMarker = (
    <g>
      <line x1={CX} y1={CY} x2={ascX} y2={ascY} stroke={GOLD_MED} strokeWidth={2} strokeDasharray="5,4" opacity={0.6} />
      <circle cx={ascX} cy={ascY} r={6} fill={GOLD_MED} />
      <polygon points={`${ascX},${ascY} ${ascX+12*Math.cos(ascRad+0.35)},${ascY+12*Math.sin(ascRad+0.35)} ${ascX+12*Math.cos(ascRad-0.35)},${ascY+12*Math.sin(ascRad-0.35)}`} fill={GOLD_MED} />
      <text x={ascLX} y={ascLY} textAnchor="middle" dominantBaseline="central"
        fill={GOLD_MED} fontSize="12" fontWeight="700" fontFamily="'Inter',sans-serif"
        transform={`rotate(${arcRot(lagnaAngle+90)},${ascLX},${ascLY})`}>ASC {ascDeg}&deg;</text>
    </g>
  );

  return (
    <div className="relative w-full max-w-[520px] mx-auto" style={{ padding: '16px' }}>
      {tooltip && (
        <div className="absolute z-20 pointer-events-none"
          style={{ left: `${((tooltip.x+16)/600)*100}%`, top: `${(tooltip.y/600)*100}%`, transform: 'translate(-50%,-130%)' }}>
          <div className="bg-white border border-[#C4611F] rounded-lg px-3 py-2 shadow-lg text-xs" style={{ fontFamily:'Inter,sans-serif', minWidth:'130px' }}>
            <p className="font-bold" style={{ color: MALEFIC.has(tooltip.planet)?DARK:GOLD_MED }}>{tooltip.planet} ({hi?PLANET_FULL_HI[tooltip.planet]:tooltip.planet})</p>
            <p style={{ color: GOLD }}>{tooltip.sign} ({hi?SIGNS[signIdx(tooltip.sign)].hi:tooltip.sign})</p>
            <p style={{ color: GOLD_MED }}>{tooltip.degree.toFixed(1)}&deg;</p>
            <p className="text-gray-500">{MALEFIC.has(tooltip.planet)?(hi?'पापी':'Malefic'):(hi?'शुभ':'Benefic')} · {tooltip.retrograde?(hi?'वक्री ℞':'Retro ℞'):(hi?'मार्गी':'Direct')}</p>
          </div>
        </div>
      )}

      <div className="chakra-float" style={{ transformStyle: 'preserve-3d' }}>
        <svg viewBox="0 0 600 600" className="w-full h-full" style={{
          overflow: 'hidden',
          filter: 'drop-shadow(4px 8px 16px rgba(139,69,19,0.25)) drop-shadow(0 2px 6px rgba(196,97,31,0.12))',
        }}>
          <defs>{clipDefs}</defs>

          <circle cx={CX} cy={CY} r={R_OUTER} fill="none" stroke={GOLD} strokeWidth={2} />
          {ticks}
          <circle cx={CX} cy={CY} r={R_DATE_RING} fill="none" stroke="rgba(139,69,19,0.12)" strokeWidth={0.5} />
          <circle cx={CX} cy={CY} r={R_GENDER_RING} fill="none" stroke="rgba(139,69,19,0.15)" strokeWidth={0.6} />
          <circle cx={CX} cy={CY} r={R_GLYPH_RING} fill="none" stroke="rgba(139,69,19,0.15)" strokeWidth={0.8} />
          <circle cx={CX} cy={CY} r={R_GLYPH_RING + 14} fill="none" stroke="rgba(139,69,19,0.1)" strokeWidth={0.5} />
          <circle cx={CX} cy={CY} r={R_ELEM_RING} fill="none" stroke="rgba(139,69,19,0.18)" strokeWidth={0.7} />
          <circle cx={CX} cy={CY} r={R_INNER} fill="none" stroke="rgba(139,69,19,0.12)" strokeWidth={0.6} />

          <defs>
            <radialGradient id="iBg2" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stopColor="#FAF7F2" />
              <stop offset="100%" stopColor="#F0E8D8" stopOpacity={0.3} />
            </radialGradient>
          </defs>
          <circle cx={CX} cy={CY} r={R_INNER} fill="url(#iBg2)" />
          <circle cx={CX} cy={CY} r={R_CENTER} fill="#FAF7F2" stroke="rgba(139,69,19,0.2)" strokeWidth={1} />

          {segEls}
          {!loading && skyData && ascMarker}
          {!loading && planetDots}

          {loading ? (
            <text x={CX} y={CY} textAnchor="middle" dominantBaseline="central" fill={GOLD_MED} fontSize="9">{hi?'लोड हो रहा...':'Loading...'}</text>
          ) : (
            <>
              <text x={CX} y={CY-6} textAnchor="middle" fill={GOLD_MED} fontSize="22" fontWeight="bold">ॐ</text>
              <text x={CX} y={CY+14} textAnchor="middle" fill={GOLD} fontSize="10" fontWeight="600" fontFamily="'Inter',sans-serif">{timeStr}</text>
            </>
          )}
        </svg>
      </div>

      <div className="flex flex-wrap justify-center gap-3 mt-3 text-[10px]" style={{ fontFamily:'Inter,sans-serif', color: GOLD }}>
        <span className="flex items-center gap-1"><span className="font-bold" style={{ color:GOLD_MED }}>Su 14&deg;</span> {hi?'शुभ':'Benefic'}</span>
        <span className="flex items-center gap-1"><span className="font-bold" style={{ color:DARK }}>Ma 8&deg;</span> {hi?'पापी':'Malefic'}</span>
        <span className="flex items-center gap-1"><span className="text-red-600 font-bold">{'\u211E'}</span> {hi?'वक्री':'Retro'}</span>
        <span className="flex items-center gap-1"><span className="w-2.5 h-2.5" style={{ background:GOLD_MED, clipPath:'polygon(50% 0%,0% 100%,100% 100%)' }} />ASC</span>
      </div>
    </div>
  );
}
