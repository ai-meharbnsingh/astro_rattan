import { useState, useEffect, useCallback } from 'react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';

const toRad = (deg: number) => (deg * Math.PI) / 180;
const CX = 300;
const CY = 300;

/* ── Sign data ── */
const SIGNS = [
  { en: 'Aries',       hi: 'मेष',     glyph: '\u2648\uFE0E', month: 'Apr',  monthHi: 'अप्रै', gender: '\u2642', element: 'Fire',  elementHi: 'अग्नि', elemColor: '#e25822', img: '/images/zodiac/aries.jpg' },
  { en: 'Taurus',      hi: 'वृषभ',    glyph: '\u2649\uFE0E', month: 'May',  monthHi: 'मई',    gender: '\u2640', element: 'Earth', elementHi: 'पृथ्वी', elemColor: '#6b8e23', img: '/images/zodiac/taurus.jpg' },
  { en: 'Gemini',      hi: 'मिथुन',   glyph: '\u264A\uFE0E', month: 'Jun',  monthHi: 'जून',   gender: '\u2642', element: 'Air',   elementHi: 'वायु',  elemColor: '#4682b4', img: '/images/zodiac/gemini.jpg' },
  { en: 'Cancer',      hi: 'कर्क',    glyph: '\u264B\uFE0E', month: 'Jul',  monthHi: 'जुला',  gender: '\u2640', element: 'Water', elementHi: 'जल',    elemColor: '#1e90ff', img: '/images/zodiac/cancer.jpg' },
  { en: 'Leo',         hi: 'सिंह',    glyph: '\u264C\uFE0E', month: 'Aug',  monthHi: 'अग',    gender: '\u2642', element: 'Fire',  elementHi: 'अग्नि', elemColor: '#e25822', img: '/images/zodiac/leo.jpg' },
  { en: 'Virgo',       hi: 'कन्या',   glyph: '\u264D\uFE0E', month: 'Sep',  monthHi: 'सित',   gender: '\u2640', element: 'Earth', elementHi: 'पृथ्वी', elemColor: '#6b8e23', img: '/images/zodiac/virgo.jpg' },
  { en: 'Libra',       hi: 'तुला',    glyph: '\u264E\uFE0E', month: 'Oct',  monthHi: 'अक्टू', gender: '\u2642', element: 'Air',   elementHi: 'वायु',  elemColor: '#4682b4', img: '/images/zodiac/libra.jpg' },
  { en: 'Scorpio',     hi: 'वृश्चिक', glyph: '\u264F\uFE0E', month: 'Nov',  monthHi: 'नव',    gender: '\u2640', element: 'Water', elementHi: 'जल',    elemColor: '#1e90ff', img: '/images/zodiac/scorpio.jpg' },
  { en: 'Sagittarius', hi: 'धनु',     glyph: '\u2650\uFE0E', month: 'Dec',  monthHi: 'दिस',   gender: '\u2642', element: 'Fire',  elementHi: 'अग्नि', elemColor: '#e25822', img: '/images/zodiac/sagittarius.jpg' },
  { en: 'Capricorn',   hi: 'मकर',     glyph: '\u2651\uFE0E', month: 'Jan',  monthHi: 'जन',    gender: '\u2640', element: 'Earth', elementHi: 'पृथ्वी', elemColor: '#6b8e23', img: '/images/zodiac/capricorn.jpg' },
  { en: 'Aquarius',    hi: 'कुंभ',    glyph: '\u2652\uFE0E', month: 'Feb',  monthHi: 'फर',    gender: '\u2642', element: 'Air',   elementHi: 'वायु',  elemColor: '#4682b4', img: '/images/zodiac/aquarius.jpg' },
  { en: 'Pisces',      hi: 'मीन',     glyph: '\u2653\uFE0E', month: 'Mar',  monthHi: 'मार्च', gender: '\u2640', element: 'Water', elementHi: 'जल',    elemColor: '#1e90ff', img: '/images/zodiac/pisces.jpg' },
];

const PLANET_ABBR: Record<string,string> = { Sun:'Su',Moon:'Mo',Mars:'Ma',Mercury:'Me',Jupiter:'Ju',Venus:'Ve',Saturn:'Sa',Rahu:'Ra',Ketu:'Ke' };
const PLANET_HI: Record<string,string> = { Sun:'सू',Moon:'चं',Mars:'मं',Mercury:'बु',Jupiter:'गु',Venus:'शु',Saturn:'श',Rahu:'रा',Ketu:'के' };
const PLANET_FULL_HI: Record<string,string> = { Sun:'सूर्य',Moon:'चंद्र',Mars:'मंगल',Mercury:'बुध',Jupiter:'बृहस्पति',Venus:'शुक्र',Saturn:'शनि',Rahu:'राहु',Ketu:'केतु' };
const MALEFIC = new Set(['Mars','Saturn','Rahu','Ketu']);

// Planet ring radii — spread across sub-rings inside Ring 3
const RING_R: Record<string, number> = {
  Sun: 205, Moon: 185, Venus: 205, Mercury: 185,
  Mars: 165, Jupiter: 145, Saturn: 165,
  Rahu: 128, Ketu: 128,
};

interface TransitPlanet { planet: string; sign: string; longitude: number; sign_degree: number; is_retrograde: boolean; }
interface TooltipData { planet: string; sign: string; degree: number; retrograde: boolean; x: number; y: number; }
interface SkyData { planets: TransitPlanet[]; lagna_sign: string; lagna_longitude: number; }

/* ── Ring radii ── */
const R_SIGN_NAME = 285;  // Ring 1: sign names
const R_OUTER = 268;      // outer circle
const R_MONTH = 256;      // Ring 2: months
const R_MONTH_RING = 244; // ring line
const R_IMG = 215;        // Ring 3: watermark images center
const R_GLYPH_RING = 112; // ring line
const R_GLYPH = 96;       // Ring 4: zodiac glyphs
const R_ELEM_RING = 78;   // ring line
const R_ELEM = 65;        // Ring 5: elements
const R_CENTER = 45;      // center

const GOLD = '#8B4513';
const GOLD_MED = '#C4611F';
const DARK = '#1a1a2e';

function signIdx(sign: string): number { return Math.max(0, SIGNS.findIndex(s => s.en.toLowerCase() === sign.toLowerCase())); }
function absAngle(p: TransitPlanet): number { return signIdx(p.sign) * 30 + p.sign_degree - 90; }
function arcRot(midDeg: number): number {
  const t = ((midDeg + 90) % 360 + 360) % 360;
  return (t > 90 && t < 270) ? t + 180 : t;
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
    try { const d = await api.get('/api/kundli/current-sky'); setSkyData(d); setError(false); } catch { setError(true); }
    setLoading(false);
  }, []);

  useEffect(() => { fetchSky(); const iv = setInterval(fetchSky, 60000); return () => clearInterval(iv); }, [fetchSky]);
  useEffect(() => { const iv = setInterval(() => setCurrentTime(new Date()), 1000); return () => clearInterval(iv); }, []);

  const timeStr = currentTime.toLocaleTimeString(hi ? 'hi-IN' : 'en-IN', { hour:'2-digit', minute:'2-digit', second:'2-digit' });
  const planets = skyData?.planets || [];
  const lagnaLong = skyData?.lagna_longitude || 0;
  const lagnaAngle = lagnaLong - 90;

  /* ── Ticks ── */
  const ticks: JSX.Element[] = [];
  for (let i = 0; i < 360; i += 5) {
    const a = toRad(i);
    const isMajor = i % 30 === 0;
    const r2 = isMajor ? R_OUTER - 10 : R_OUTER - 3;
    ticks.push(<line key={`t${i}`} x1={CX+R_OUTER*Math.cos(a)} y1={CY+R_OUTER*Math.sin(a)} x2={CX+r2*Math.cos(a)} y2={CY+r2*Math.sin(a)} stroke="rgba(139,69,19,0.2)" strokeWidth={isMajor?1.2:0.4} />);
  }

  /* ── 12 sign segments ── */
  const segmentEls = SIGNS.map((sign, i) => {
    const startDeg = i * 30 - 90;
    const midDeg = startDeg + 15;
    const startRad = toRad(startDeg);
    const midRad = toRad(midDeg);
    const rot = arcRot(midDeg);

    // Divider line
    const lx1 = CX + R_ELEM_RING * Math.cos(startRad);
    const ly1 = CY + R_ELEM_RING * Math.sin(startRad);
    const lx2 = CX + R_OUTER * Math.cos(startRad);
    const ly2 = CY + R_OUTER * Math.sin(startRad);

    // Ring 1: sign name
    const nx = CX + R_SIGN_NAME * Math.cos(midRad);
    const ny = CY + R_SIGN_NAME * Math.sin(midRad);

    // Ring 2: month
    const mx = CX + R_MONTH * Math.cos(midRad);
    const my = CY + R_MONTH * Math.sin(midRad);

    // Ring 3: watermark image
    const ix = CX + R_IMG * Math.cos(midRad);
    const iy = CY + R_IMG * Math.sin(midRad);

    // Watermark gender symbol
    const gsx = CX + 170 * Math.cos(midRad);
    const gsy = CY + 170 * Math.sin(midRad);

    // Ring 4: glyph
    const gx = CX + R_GLYPH * Math.cos(midRad);
    const gy = CY + R_GLYPH * Math.sin(midRad);

    // Ring 5: element
    const ex = CX + R_ELEM * Math.cos(midRad);
    const ey = CY + R_ELEM * Math.sin(midRad);

    const signName = hi ? sign.hi : sign.en.slice(0, 3);
    const monthName = hi ? sign.monthHi : sign.month;
    const elemName = hi ? sign.elementHi : sign.element;

    return (
      <g key={sign.en}>
        <line x1={lx1} y1={ly1} x2={lx2} y2={ly2} stroke="rgba(139,69,19,0.15)" strokeWidth={0.7} />

        {/* Ring 1: Sign name */}
        <text x={nx} y={ny} textAnchor="middle" dominantBaseline="central"
          fill={GOLD} fontSize="13" fontWeight="700" fontFamily="'Inter',sans-serif"
          transform={`rotate(${rot},${nx},${ny})`}>{signName}</text>

        {/* Ring 2: Month */}
        <text x={mx} y={my} textAnchor="middle" dominantBaseline="central"
          fill={GOLD_MED} fontSize="9" fontWeight="600" fontFamily="'Inter',sans-serif"
          transform={`rotate(${rot},${mx},${my})`}>{monthName}</text>

        {/* Ring 3: Watermark animal image */}
        <image href={sign.img} x={ix - 22} y={iy - 22} width={44} height={44}
          preserveAspectRatio="xMidYMid slice" opacity={0.12}
          clipPath={`url(#wc${i})`} />

        {/* Watermark gender symbol */}
        <text x={gsx} y={gsy} textAnchor="middle" dominantBaseline="central"
          fill="rgba(139,69,19,0.08)" fontSize="20">{sign.gender}</text>

        {/* Watermark element icon */}
        <text x={ix} y={iy} textAnchor="middle" dominantBaseline="central"
          fill={sign.elemColor} opacity={0.1} fontSize="28">
          {sign.element === 'Fire' ? '🔥' : sign.element === 'Earth' ? '🌍' : sign.element === 'Air' ? '💨' : '💧'}
        </text>

        {/* Ring 4: Zodiac glyph (golden, not purple) */}
        <text x={gx} y={gy} textAnchor="middle" dominantBaseline="central"
          fill={GOLD_MED} fontSize="18" fontWeight="bold"
          fontFamily="'Segoe UI Symbol','Noto Sans Symbols 2',serif">{sign.glyph}</text>

        {/* Ring 5: Element name */}
        <text x={ex} y={ey} textAnchor="middle" dominantBaseline="central"
          fill={sign.elemColor} fontSize="7" fontWeight="600" opacity={0.7}
          fontFamily="'Inter',sans-serif"
          transform={`rotate(${rot},${ex},${ey})`}>{elemName}</text>
      </g>
    );
  });

  /* ── Clip paths for watermark images ── */
  const clipDefs = SIGNS.map((_, i) => {
    const midRad = toRad(i * 30 + 15 - 90);
    const cx = CX + R_IMG * Math.cos(midRad);
    const cy = CY + R_IMG * Math.sin(midRad);
    return <clipPath key={`wc${i}`} id={`wc${i}`}><circle cx={cx} cy={cy} r={20} /></clipPath>;
  });

  /* ── Planet dots (foreground on Ring 3) ── */
  const DOT_R = 22;
  const MIN_DIST = DOT_R * 2 + 10;

  let dotPos = planets.map(p => {
    const ring = RING_R[p.planet] || 150;
    const rad = toRad(absAngle(p));
    return { planet: p, x: CX + ring * Math.cos(rad), y: CY + ring * Math.sin(rad) };
  });

  // Collision resolve — 12 iterations
  for (let iter = 0; iter < 12; iter++) {
    for (let i = 0; i < dotPos.length; i++) {
      for (let j = i + 1; j < dotPos.length; j++) {
        const dx = dotPos[i].x - dotPos[j].x;
        const dy = dotPos[i].y - dotPos[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < MIN_DIST && dist > 0) {
          const a = Math.atan2(dy, dx);
          const push = (MIN_DIST - dist) / 2 + 6;
          dotPos[i].x += Math.cos(a) * push;
          dotPos[i].y += Math.sin(a) * push;
          dotPos[j].x -= Math.cos(a) * push;
          dotPos[j].y -= Math.sin(a) * push;
        }
      }
    }
  }

  const planetDots = dotPos.map(({ planet: p, x: px, y: py }, i) => {
    const isMalefic = MALEFIC.has(p.planet);
    const abbr = hi ? PLANET_HI[p.planet] : PLANET_ABBR[p.planet];
    const degText = `${Math.floor(p.sign_degree)}\u00B0`;
    const textColor = isMalefic ? DARK : GOLD_MED;

    return (
      <g key={p.planet} className="transit-dot" style={{ animationDelay: `${i * 0.08}s` }}
        onMouseEnter={() => setTooltip({ planet: p.planet, sign: p.sign, degree: p.sign_degree, retrograde: p.is_retrograde, x: px, y: py })}
        onMouseLeave={() => setTooltip(null)} cursor="pointer">
        <circle cx={px} cy={py} r={DOT_R}
          fill="white" fillOpacity={0.92}
          stroke={p.is_retrograde ? '#FF3333' : (isMalefic ? DARK : GOLD_MED)}
          strokeWidth={p.is_retrograde ? 2.5 : 1.5}
          style={{ transition: 'all 1s ease' }} />
        <text x={px} y={py - 4} textAnchor="middle" dominantBaseline="central"
          fill={textColor} fontSize="10" fontWeight="700" fontFamily="'Inter',sans-serif">{abbr}</text>
        <text x={px} y={py + 8} textAnchor="middle" dominantBaseline="central"
          fill={textColor} opacity={0.8} fontSize="8" fontFamily="'Inter',sans-serif">{degText}</text>
        {p.is_retrograde && (
          <text x={px} y={py - DOT_R - 6} textAnchor="middle"
            fill="#FF3333" fontSize="11" fontWeight="700">{'\u211E'}</text>
        )}
      </g>
    );
  });

  /* ── ASC marker ── */
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
    <div className="relative w-full max-w-[480px] mx-auto" style={{ padding: '16px' }}>
      {tooltip && (
        <div className="absolute z-20 pointer-events-none"
          style={{ left: `${((tooltip.x+16)/600)*100}%`, top: `${(tooltip.y/600)*100}%`, transform: 'translate(-50%,-130%)' }}>
          <div className="bg-white border border-[#C4611F] rounded-lg px-3 py-2 shadow-lg text-xs" style={{ fontFamily:'Inter,sans-serif', minWidth:'130px' }}>
            <p className="font-bold" style={{ color: MALEFIC.has(tooltip.planet) ? DARK : GOLD_MED }}>{tooltip.planet} ({hi ? PLANET_FULL_HI[tooltip.planet] : tooltip.planet})</p>
            <p style={{ color: GOLD }}>{tooltip.sign} ({hi ? SIGNS[signIdx(tooltip.sign)].hi : tooltip.sign})</p>
            <p style={{ color: GOLD_MED }}>{tooltip.degree.toFixed(1)}&deg;</p>
            <p className="text-gray-500">{MALEFIC.has(tooltip.planet) ? (hi?'पापी':'Malefic') : (hi?'शुभ':'Benefic')} · {tooltip.retrograde ? (hi?'वक्री':'Retro ℞') : (hi?'मार्गी':'Direct')}</p>
          </div>
        </div>
      )}

      <div className="chakra-float" style={{ transformStyle: 'preserve-3d' }}>
        <svg viewBox="0 0 600 600" className="w-full h-full" style={{
          overflow: 'visible',
          filter: 'drop-shadow(4px 8px 16px rgba(139,69,19,0.25)) drop-shadow(0 2px 6px rgba(196,97,31,0.12))',
        }}>
          <defs>{clipDefs}</defs>

          {/* Rings */}
          <circle cx={CX} cy={CY} r={R_OUTER} fill="none" stroke={GOLD} strokeWidth={2} />
          {ticks}
          <circle cx={CX} cy={CY} r={R_MONTH_RING} fill="none" stroke="rgba(139,69,19,0.15)" strokeWidth={0.6} />
          <circle cx={CX} cy={CY} r={R_GLYPH_RING} fill="none" stroke="rgba(139,69,19,0.18)" strokeWidth={0.8} />
          <circle cx={CX} cy={CY} r={R_ELEM_RING} fill="none" stroke="rgba(139,69,19,0.12)" strokeWidth={0.6} />

          {/* Inner gradient fill */}
          <defs>
            <radialGradient id="iBg2" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stopColor="#FAF7F2" />
              <stop offset="100%" stopColor="#F0E8D8" stopOpacity={0.3} />
            </radialGradient>
          </defs>
          <circle cx={CX} cy={CY} r={R_ELEM_RING} fill="url(#iBg2)" />

          {/* Center */}
          <circle cx={CX} cy={CY} r={R_CENTER} fill="#FAF7F2" stroke="rgba(139,69,19,0.2)" strokeWidth={1} />

          {/* Segments */}
          {segmentEls}

          {/* ASC */}
          {!loading && skyData && ascMarker}

          {/* Planet dots ON TOP */}
          {!loading && planetDots}

          {/* Center content */}
          {loading ? (
            <text x={CX} y={CY} textAnchor="middle" dominantBaseline="central" fill={GOLD_MED} fontSize="9">{hi?'लोड हो रहा...':'Loading...'}</text>
          ) : (
            <>
              <text x={CX} y={CY - 6} textAnchor="middle" fill={GOLD_MED} fontSize="22" fontWeight="bold">ॐ</text>
              <text x={CX} y={CY + 14} textAnchor="middle" fill={GOLD} fontSize="10" fontWeight="600" fontFamily="'Inter',sans-serif">{timeStr}</text>
            </>
          )}
        </svg>
      </div>

      {/* Legend */}
      <div className="flex flex-wrap justify-center gap-3 mt-3 text-[10px]" style={{ fontFamily:'Inter,sans-serif', color: GOLD }}>
        <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full border-2" style={{ borderColor: GOLD_MED, background: 'white' }} />{hi?'शुभ':'Benefic'}</span>
        <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full border-2" style={{ borderColor: DARK, background: 'white' }} />{hi?'पापी':'Malefic'}</span>
        <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full border-2 border-red-500 bg-white" /><span className="text-red-600 font-bold">{'\u211E'}</span> {hi?'वक्री':'Retro'}</span>
        <span className="flex items-center gap-1"><span className="w-3 h-3" style={{ background: GOLD_MED, clipPath:'polygon(50% 0%,0% 100%,100% 100%)' }} />ASC</span>
      </div>
    </div>
  );
}
