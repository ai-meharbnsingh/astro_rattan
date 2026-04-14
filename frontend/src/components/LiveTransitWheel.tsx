import { useState, useEffect, useCallback, useMemo } from 'react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';

const toRad = (deg: number) => (deg * Math.PI) / 180;
const CX = 300;
const CY = 300;

const SIGNS = [
  { en: 'Aries',       hi: 'मेष',     glyph: '\u2648\uFE0E', dates: 'Mar 21-Apr 19', datesHi: '21 मार्च-19 अप्रै', gender: '\u2642', elemIcon: '\u{1F525}', img: '/images/zodiac-orange/zodiac-aries-orange.png' },
  { en: 'Taurus',      hi: 'वृषभ',    glyph: '\u2649\uFE0E', dates: 'Apr 20-May 20', datesHi: '20 अप्रै-20 मई',    gender: '\u2640', elemIcon: '\u{1F30D}', img: '/images/zodiac-orange/zodiac-taurus-orange.png' },
  { en: 'Gemini',      hi: 'मिथुन',   glyph: '\u264A\uFE0E', dates: 'May 21-Jun 20', datesHi: '21 मई-20 जून',      gender: '\u2642', elemIcon: '\u{1F4A8}', img: '/images/zodiac-orange/zodiac-gemini-orange.png' },
  { en: 'Cancer',      hi: 'कर्क',    glyph: '\u264B\uFE0E', dates: 'Jun 21-Jul 22', datesHi: '21 जून-22 जुला',    gender: '\u2640', elemIcon: '\u{1F4A7}', img: '/images/zodiac-orange/zodiac-cancer-orange.png' },
  { en: 'Leo',         hi: 'सिंह',    glyph: '\u264C\uFE0E', dates: 'Jul 23-Aug 22', datesHi: '23 जुला-22 अग',     gender: '\u2642', elemIcon: '\u{1F525}', img: '/images/zodiac-orange/zodiac-leo-orange.png' },
  { en: 'Virgo',       hi: 'कन्या',   glyph: '\u264D\uFE0E', dates: 'Aug 23-Sep 22', datesHi: '23 अग-22 सित',     gender: '\u2640', elemIcon: '\u{1F30D}', img: '/images/zodiac-orange/zodiac-virgo-orange.png' },
  { en: 'Libra',       hi: 'तुला',    glyph: '\u264E\uFE0E', dates: 'Sep 23-Oct 22', datesHi: '23 सित-22 अक्टू',  gender: '\u2642', elemIcon: '\u{1F4A8}', img: '/images/zodiac-orange/zodiac-libra-orange.png' },
  { en: 'Scorpio',     hi: 'वृश्चिक', glyph: '\u264F\uFE0E', dates: 'Oct 23-Nov 21', datesHi: '23 अक्टू-21 नव',   gender: '\u2640', elemIcon: '\u{1F4A7}', img: '/images/zodiac-orange/zodiac-scorpio-orange.png' },
  { en: 'Sagittarius', hi: 'धनु',     glyph: '\u2650\uFE0E', dates: 'Nov 22-Dec 21', datesHi: '22 नव-21 दिस',     gender: '\u2642', elemIcon: '\u{1F525}', img: '/images/zodiac-orange/zodiac-sagittarius-orange.png' },
  { en: 'Capricorn',   hi: 'मकर',     glyph: '\u2651\uFE0E', dates: 'Dec 22-Jan 19', datesHi: '22 दिस-19 जन',     gender: '\u2640', elemIcon: '\u{1F30D}', img: '/images/zodiac-orange/zodiac-capricorn-orange.png' },
  { en: 'Aquarius',    hi: 'कुंभ',    glyph: '\u2652\uFE0E', dates: 'Jan 20-Feb 18', datesHi: '20 जन-18 फर',      gender: '\u2642', elemIcon: '\u{1F4A8}', img: '/images/zodiac-orange/zodiac-aquarius-orange.png' },
  { en: 'Pisces',      hi: 'मीन',     glyph: '\u2653\uFE0E', dates: 'Feb 19-Mar 20', datesHi: '19 फर-20 मार्च',   gender: '\u2640', elemIcon: '\u{1F4A7}', img: '/images/zodiac-orange/zodiac-pisces-orange.png' },
];

const PLANET_ABBR: Record<string,string> = { Sun:'Su',Moon:'Mo',Mars:'Ma',Mercury:'Me',Jupiter:'Ju',Venus:'Ve',Saturn:'Sa',Rahu:'Ra',Ketu:'Ke' };
const PLANET_HI: Record<string,string> = { Sun:'सू',Moon:'चं',Mars:'मं',Mercury:'बु',Jupiter:'गु',Venus:'शु',Saturn:'श',Rahu:'रा',Ketu:'के' };
const PLANET_FULL_HI: Record<string,string> = { Sun:'सूर्य',Moon:'चंद्र',Mars:'मंगल',Mercury:'बुध',Jupiter:'बृहस्पति',Venus:'शुक्र',Saturn:'शनि',Rahu:'राहु',Ketu:'केतु' };
const MALEFIC = new Set(['Mars','Saturn','Rahu','Ketu']);

// Vedic dignity data
const EXALTED: Record<string,string> = { Sun:'Aries',Moon:'Taurus',Mars:'Capricorn',Mercury:'Virgo',Jupiter:'Cancer',Venus:'Pisces',Saturn:'Libra' };
const DEBILITATED: Record<string,string> = { Sun:'Libra',Moon:'Scorpio',Mars:'Cancer',Mercury:'Pisces',Jupiter:'Capricorn',Venus:'Virgo',Saturn:'Aries' };
// Vargottama: same sign in D1 and D9 (Navamsa). Simplified: degrees 0-3.33 in fire signs, etc.
function isVargottama(sign: string, deg: number): boolean {
  const fireIdx = [0,4,8]; const earthIdx = [1,5,9]; const airIdx = [2,6,10]; const waterIdx = [3,7,11];
  const si = SIGNS.findIndex(s => s.en.toLowerCase() === sign.toLowerCase());
  const navamsaPada = Math.floor(deg / 3.333);
  // Vargottama if navamsa falls in same sign — simplified: pada 0 for movable, pada 4 for fixed, pada 8 for dual
  return navamsaPada === 0 && fireIdx.includes(si) || navamsaPada === 4 && earthIdx.includes(si) || navamsaPada === 8 && airIdx.includes(si);
}
// Combust: planet within certain degrees of Sun
function isCombust(planet: string, sunLong: number, planetLong: number): boolean {
  if (planet === 'Sun' || planet === 'Rahu' || planet === 'Ketu') return false;
  const combustDeg: Record<string,number> = { Moon:12, Mars:17, Mercury:14, Jupiter:11, Venus:10, Saturn:15 };
  const diff = Math.abs(sunLong - planetLong);
  const dist = Math.min(diff, 360 - diff);
  return dist <= (combustDeg[planet] || 10);
}

function getPlanetStatus(p: { planet: string; sign: string; sign_degree: number; longitude: number; is_retrograde: boolean }, sunLong: number): string[] {
  const symbols: string[] = [];
  if (p.is_retrograde) symbols.push('*');
  if (isCombust(p.planet, sunLong, p.longitude)) symbols.push('^');
  if (isVargottama(p.sign, p.sign_degree)) symbols.push('v');
  if (EXALTED[p.planet]?.toLowerCase() === p.sign.toLowerCase()) symbols.push('+');
  if (DEBILITATED[p.planet]?.toLowerCase() === p.sign.toLowerCase()) symbols.push('-');
  return symbols;
}

const RING_R: Record<string, number> = {
  Sun: 206, Moon: 194, Venus: 206, Mercury: 194,
  Mars: 182, Jupiter: 170, Saturn: 182,
  Rahu: 170, Ketu: 170,
};

interface TransitPlanet { planet: string; sign: string; longitude: number; sign_degree: number; is_retrograde: boolean; }
interface TooltipData { planet: string; sign: string; degree: number; retrograde: boolean; x: number; y: number; }
interface SkyData { planets: TransitPlanet[]; lagna_sign: string; lagna_longitude: number; }

const R_OUTERMOST = 298; // outermost circle — closer to signs
const R_SIGN_NAME = 280;
const R_OUTER = 270; // second circle — slightly bigger
const R_DATE = 256;
const R_DATE_RING = 244;
const R_IMG = 193;
const R_GENDER = 130; // Moved closer to center
const R_GENDER_RING = 143; // Outer circle for gender symbols
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
const WHEEL_LINE = 'rgba(139,69,19,0.52)';
const WHEEL_STROKE_W = 0.7;

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

  const [fetchedAt, setFetchedAt] = useState<number>(Date.now());
  const [viewMode, setViewMode] = useState<'transit' | 'kundli'>('transit');

  const fetchSky = useCallback(async () => {
    try { const d = await api.get('/api/kundli/current-sky'); setSkyData(d); setFetchedAt(Date.now()); setError(false); } catch { setError(true); }
    setLoading(false);
  }, []);

  useEffect(() => { fetchSky(); const iv = setInterval(fetchSky, 60000); return () => clearInterval(iv); }, [fetchSky]);
  useEffect(() => { const iv = setInterval(() => setCurrentTime(new Date()), 5000); return () => clearInterval(iv); }, []);

  const timeStr = currentTime.toLocaleTimeString(hi ? 'hi-IN' : 'en-IN', { hour:'2-digit', minute:'2-digit', second:'2-digit' });
  const planets = skyData?.planets || [];
  // ASC moves ~0.25°/min (360°/24h). Interpolate between API fetches for smooth 5s updates.
  const elapsedSec = (currentTime.getTime() - fetchedAt) / 1000;
  const lagnaLong = (skyData?.lagna_longitude || 0) + (elapsedSec * (360 / 86400));
  const lagnaAngle = lagnaLong - 90;

  // Build kundli house data from sky data
  const SIGN_NAMES = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces'];
  const ascSignIdx = Math.floor(lagnaLong / 30) % 12;
  const kundliHouses = useMemo(() => {
    if (!skyData) return [];
    return Array.from({ length: 12 }, (_, i) => {
      const signIdx = (ascSignIdx + i) % 12;
      const sign = SIGN_NAMES[signIdx];
      const housePlanets = planets.filter(p => {
        const pIdx = SIGN_NAMES.findIndex(s => s.toLowerCase() === p.sign.toLowerCase());
        return ((pIdx - ascSignIdx + 12) % 12) === i;
      });
      return { house: i + 1, sign, signNum: signIdx + 1, planets: housePlanets };
    });
  }, [skyData, planets, ascSignIdx]);

  // Ticks
  const ticks: JSX.Element[] = [];
  for (let i = 0; i < 360; i += 5) {
    const a = toRad(i);
    const r2 = R_OUTER - 4;
    ticks.push(<line key={`t${i}`} x1={CX+R_OUTER*Math.cos(a)} y1={CY+R_OUTER*Math.sin(a)} x2={CX+r2*Math.cos(a)} y2={CY+r2*Math.sin(a)} stroke={WHEEL_LINE} strokeWidth={WHEEL_STROKE_W} />);
  }

  // Segments
  const clipDefs = SIGNS.map((_, i) => {
    const midRad = toRad(i * 30 + 15 - 90);
    return <clipPath key={`wc${i}`} id={`wc${i}`}><circle cx={CX + R_IMG * Math.cos(midRad)} cy={CY + R_IMG * Math.sin(midRad)} r={28} /></clipPath>;
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
    const lx2 = CX + R_OUTERMOST * Math.cos(startRad);
    const ly2 = CY + R_OUTERMOST * Math.sin(startRad);

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
        <line x1={lx1} y1={ly1} x2={lx2} y2={ly2} stroke={WHEEL_LINE} strokeWidth={WHEEL_STROKE_W} />

        {/* Ring 1: Sign name + degree span (uniform for all signs) */}
        <text x={nx} y={ny} textAnchor="middle" dominantBaseline="central"
          fill={GOLD} fontSize="13" fontWeight="700" fontFamily="'Inter',sans-serif"
          transform={`rotate(${rot},${nx},${ny})`}>{`${signLabel} ${degStart}°-${degEnd}°`}</text>

        {/* Ring 2: Date range */}
        <text x={dx} y={dy} textAnchor="middle" dominantBaseline="central"
          fill={GOLD_MED} fontSize="12" fontWeight="700" fontFamily="'Inter',sans-serif"
          transform={`rotate(${rot},${dx},${dy})`}>{hi ? sign.datesHi : sign.dates}</text>

        {/* Ring 3: Watermark zodiac animal sketch — saffron monochrome */}
        <image href={sign.img} x={ix-28} y={iy-28} width={56} height={56}
          preserveAspectRatio="xMidYMid slice" opacity={0.30}
          clipPath={`url(#wc${i})`} />

        {/* Gender symbol — inside, visible */}
        <text x={gndx} y={gndy} textAnchor="middle" dominantBaseline="central"
          fill={GOLD_MED} opacity={1} fontSize="16" fontWeight="700">{sign.gender}</text>

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

  // Planet positions — clamp angle to stay 5° inside sign boundaries (never cross divider lines)
  const DOT_MIN_DIST = 48;
  const LANE_MIN = 162;
  const LANE_MAX = 214;
  const SIGN_PAD = 5; // degrees padding from sign boundary
  let dotPos = planets.map(p => {
    const baseRadius = Math.max(LANE_MIN, Math.min(LANE_MAX, RING_R[p.planet] || 180));
    const si = signIdx(p.sign);
    const signStart = si * 30 - 90;
    // Clamp degree within sign: min SIGN_PAD, max 30-SIGN_PAD
    const clampedDeg = Math.max(SIGN_PAD, Math.min(30 - SIGN_PAD, p.sign_degree));
    const angle = toRad(signStart + clampedDeg);
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

  const sunLong = planets.find(p => p.planet === 'Sun')?.longitude || 0;

  const planetDots = dotPos.map(({ planet: p, angle, radius }, i) => {
    const px = CX + radius * Math.cos(angle);
    const py = CY + radius * Math.sin(angle);
    const isMalefic = MALEFIC.has(p.planet);
    const abbr = hi ? PLANET_HI[p.planet] : PLANET_ABBR[p.planet];
    const degText = `${p.sign_degree.toFixed(1)}\u00B0`;
    const textColor = isMalefic ? DARK : GOLD_MED;
    const status = getPlanetStatus(p, sunLong);
    const statusStr = status.join('');

    return (
      <g key={p.planet} className="transit-dot" style={{ animationDelay: `${i * 0.08}s` }}
        onMouseEnter={() => setTooltip({ planet: p.planet, sign: p.sign, degree: p.sign_degree, retrograde: p.is_retrograde, x: px, y: py })}
        onMouseLeave={() => setTooltip(null)} cursor="pointer">
        <text x={px} y={py - 4} textAnchor="middle" dominantBaseline="central"
          fill={textColor} fontSize="13" fontWeight="800" fontFamily="'Inter',sans-serif"
          style={{ transition: 'all 1s ease' }}>{abbr}{statusStr ? ` ${statusStr}` : ''}</text>
        <text x={px} y={py + 10} textAnchor="middle" dominantBaseline="central"
          fill={textColor} opacity={0.75} fontSize="9" fontWeight="600" fontFamily="'Inter',sans-serif">{degText}</text>
      </g>
    );
  });

  // ASC — placed on outermost circle
  const ascRad = toRad(lagnaAngle);
  const ascX = CX + R_OUTERMOST * Math.cos(ascRad);
  const ascY = CY + R_OUTERMOST * Math.sin(ascRad);
  const ascLabelR = R_OUTERMOST + 30;
  const ascLabelX = CX + ascLabelR * Math.cos(ascRad);
  const ascLabelY = CY + ascLabelR * Math.sin(ascRad);
  const ascDegText = `${(lagnaLong % 30).toFixed(1)}°`;

  const ascMarker = (
    <g>
      <line x1={CX} y1={CY} x2={ascX} y2={ascY} stroke={GOLD_MED} strokeWidth={2} strokeDasharray="5,4" opacity={0.6} />
      <polygon points={`${ascX},${ascY} ${ascX+12*Math.cos(ascRad+0.35)},${ascY+12*Math.sin(ascRad+0.35)} ${ascX+12*Math.cos(ascRad-0.35)},${ascY+12*Math.sin(ascRad-0.35)}`} fill={GOLD_MED} />
      <text x={ascLabelX} y={ascLabelY} textAnchor="middle" dominantBaseline="central"
        fill={GOLD_MED} fontSize="11" fontWeight="700" fontFamily="'Inter',sans-serif">{ascDegText}</text>
    </g>
  );

  return (
    <div className="relative w-full mx-auto" style={{ maxWidth: '760px', padding: '0px' }}>
      {/* Toggle Button */}
      <div className="flex justify-center mb-2">
        <div className="inline-flex rounded-lg border border-sacred-gold/30 overflow-hidden text-xs">
          <button
            onClick={() => setViewMode('transit')}
            className={`px-4 py-1.5 font-semibold transition-all ${
              viewMode === 'transit'
                ? 'bg-sacred-gold/20 text-sacred-gold-dark'
                : 'text-gray-500 hover:bg-sacred-gold/5'
            }`}
          >
            {hi ? 'गोचर' : 'Transit'}
          </button>
          <button
            onClick={() => setViewMode('kundli')}
            className={`px-4 py-1.5 font-semibold transition-all ${
              viewMode === 'kundli'
                ? 'bg-sacred-gold/20 text-sacred-gold-dark'
                : 'text-gray-500 hover:bg-sacred-gold/5'
            }`}
          >
            {hi ? 'कुंडली' : 'Kundli'}
          </button>
        </div>
      </div>

      {/* Kundli Chart View — North Indian style, same aesthetic as transit wheel */}
      {viewMode === 'kundli' && skyData && (() => {
        // Use exact same coordinate system as InteractiveKundli
        const S = 416; // same viewBox as InteractiveKundli
        const P = 8;   // same padding
        const W = S - 2 * P; // 400 inner width
        const H2 = W / 2;   // 200
        // Corners
        const tl = { x: P, y: P };
        const tr = { x: P + W, y: P };
        const bl = { x: P, y: P + W };
        const br = { x: P + W, y: P + W };
        // Midpoints (diamond vertices)
        const mt = { x: P + H2, y: P };
        const mr = { x: P + W, y: P + H2 };
        const mb = { x: P + H2, y: P + W };
        const ml = { x: P, y: P + H2 };
        const cc = { x: P + H2, y: P + H2 };
        // Intersection points (where diamond edges cross diagonals)
        const q = H2 / 2;
        const p1 = { x: P + q, y: P + q };          // TL-CC ∩ MT-ML
        const p2 = { x: P + H2 + q, y: P + q };     // TR-CC ∩ MT-MR
        const p3 = { x: P + H2 + q, y: P + H2 + q };// BR-CC ∩ MR-MB
        const p4 = { x: P + q, y: P + H2 + q };     // BL-CC ∩ MB-ML

        // Centroid from vertices (same as InteractiveKundli)
        const cen = (...v: {x:number;y:number}[]) => ({
          cx: v.reduce((s,p)=>s+p.x,0)/v.length,
          cy: v.reduce((s,p)=>s+p.y,0)/v.length,
        });

        // 12 houses with computed centroids — exact same geometry as InteractiveKundli
        const houses: { h: number; cx: number; cy: number; trap: boolean }[] = [
          // Top: 2(tri), 1(quad), 12(tri)
          { h: 1,  ...cen(p1, mt, p2, cc),  trap: true },
          { h: 2,  ...cen(tl, mt, p1),       trap: false },
          { h: 12, ...cen(mt, tr, p2),        trap: false },
          // Right: 11(tri), 10(quad), 9(tri)
          { h: 11, ...cen(tr, mr, p2),        trap: false },
          { h: 10, ...cen(p2, mr, p3, cc),   trap: true },
          { h: 9,  ...cen(mr, br, p3),        trap: false },
          // Bottom: 8(tri), 7(quad), 6(tri)
          { h: 8,  ...cen(br, mb, p3),        trap: false },
          { h: 7,  ...cen(p3, mb, p4, cc),   trap: true },
          { h: 6,  ...cen(mb, bl, p4),        trap: false },
          // Left: 5(tri), 4(quad), 3(tri)
          { h: 5,  ...cen(bl, ml, p4),        trap: false },
          { h: 4,  ...cen(p4, ml, p1, cc),   trap: true },
          { h: 3,  ...cen(ml, tl, p1),        trap: false },
        ];

        const pAbbr = (name: string) => hi ? (PLANET_HI[name] || name.slice(0,2)) : (PLANET_ABBR[name] || name.slice(0,2));
        const sunLong = planets.find(p => p.planet === 'Sun')?.longitude || 0;
        const pStatus = (pl: TransitPlanet) => getPlanetStatus(pl, sunLong).join('');

        return (
          <div className="chakra-float" style={{ transformStyle: 'preserve-3d' }}>
            <svg viewBox={`0 0 ${S} ${S}`} className="w-full h-full" style={{
              overflow: 'visible',
              transform: 'scale(0.85)',
              transformOrigin: 'center center',
              filter: 'drop-shadow(4px 8px 16px rgba(139,69,19,0.25)) drop-shadow(0 2px 6px rgba(196,97,31,0.12))',
            }}>
              {/* Outer square */}
              <rect x={P} y={P} width={W} height={W} fill="none" stroke={WHEEL_LINE} strokeWidth={WHEEL_STROKE_W} />
              {/* Inner diamond */}
              <polygon points={`${mt.x},${mt.y} ${mr.x},${mr.y} ${mb.x},${mb.y} ${ml.x},${ml.y}`} fill="none" stroke={WHEEL_LINE} strokeWidth={WHEEL_STROKE_W} />
              {/* Diagonals */}
              <line x1={tl.x} y1={tl.y} x2={br.x} y2={br.y} stroke={WHEEL_LINE} strokeWidth={WHEEL_STROKE_W} />
              <line x1={tr.x} y1={tr.y} x2={bl.x} y2={bl.y} stroke={WHEEL_LINE} strokeWidth={WHEEL_STROKE_W} />

              {/* House contents — EXACT same layout as InteractiveKundli (same 416px viewBox) */}
              {houses.map(nh => {
                const hData = kundliHouses[nh.h - 1];
                if (!hData) return null;
                const hPlanets = hData.planets;
                const count = hPlanets.length;

                // EXACT InteractiveKundli values (lines 1091-1108)
                const maxCols = nh.trap
                  ? (count > 4 ? 3 : count > 2 ? 2 : count)
                  : (count > 3 ? 3 : count > 1 ? 2 : 1);
                const cols = Math.min(count, maxCols);
                const spacing = nh.trap
                  ? (count > 4 ? 26 : 32)
                  : (count > 3 ? 22 : count > 2 ? 24 : 28);
                const rowHeight = count > 4 ? 16 : count > 3 ? 18 : 20;
                const fontSize = nh.trap
                  ? (count > 4 ? 13 : 15)
                  : (count > 3 ? 12 : count > 2 ? 13 : 14);

                return (
                  <g key={nh.h}>
                    {/* Rashi number (same as InteractiveKundli line 1074-1085) */}
                    <text x={nh.cx} y={nh.cy - (count > 0 ? 12 : 0) + 5}
                      textAnchor="middle" dominantBaseline="central"
                      fill={GOLD} fontSize={nh.trap ? 20 : 16} fontWeight="bold" fontFamily="'Inter',sans-serif"
                      opacity={0.35}>{hData.signNum}</text>

                    {/* Planets — EXACT InteractiveKundli grid (lines 1088-1129) */}
                    {hPlanets.map((pl, idx) => {
                      const sym = pStatus(pl);
                      const label = `${pAbbr(pl.planet)}${sym} ${pl.sign_degree.toFixed(0)}°`;
                      const pCol = idx % cols;
                      const pRow = Math.floor(idx / cols);
                      const startX = nh.cx - ((cols - 1) * spacing) / 2;
                      const px = startX + pCol * spacing;
                      const baseY = nh.cy + (nh.trap ? 14 : 8) - (count > 0 ? 2 : 0);
                      const py = baseY + pRow * rowHeight;
                      return (
                        <text key={pl.planet} x={px} y={py}
                          textAnchor="middle" dominantBaseline="central"
                          fill={MALEFIC.has(pl.planet) ? DARK : GOLD_MED}
                          fontSize={fontSize} fontWeight="700" fontFamily="'Inter',sans-serif">
                          {label}
                        </text>
                      );
                    })}
                  </g>
                );
              })}

              {/* Center — Om + time */}
              <text x={cc.x} y={cc.y - 6} textAnchor="middle" fill={GOLD_MED} fontSize="18" fontWeight="bold">ॐ</text>
              <text x={cc.x} y={cc.y + 10} textAnchor="middle" fill={GOLD} fontSize="9" fontWeight="600" fontFamily="'Inter',sans-serif">{timeStr}</text>
              {/* ASC label */}
              <text x={cc.x} y={P - 6} textAnchor="middle" fill={GOLD_MED} fontSize="9" fontWeight="700" fontFamily="'Inter',sans-serif">
                ASC {(lagnaLong % 30).toFixed(1)}° {hi ? SIGNS[ascSignIdx]?.hi : SIGNS[ascSignIdx]?.en}
              </text>
            </svg>
          </div>
        );
      })()}

      {/* Transit Wheel View */}
      {viewMode === 'transit' && <div className="relative w-full pb-2">
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
            overflow: 'visible',
            transform: 'scale(0.85)',
            transformOrigin: 'center center',
            filter: 'drop-shadow(4px 8px 16px rgba(139,69,19,0.25)) drop-shadow(0 2px 6px rgba(196,97,31,0.12))',
          }}>
            <defs>{clipDefs}</defs>

          <circle cx={CX} cy={CY} r={R_OUTERMOST} fill="none" stroke={WHEEL_LINE} strokeWidth={WHEEL_STROKE_W} />
          <circle cx={CX} cy={CY} r={R_OUTER} fill="none" stroke={WHEEL_LINE} strokeWidth={WHEEL_STROKE_W} />
          {ticks}
          <circle cx={CX} cy={CY} r={R_DATE_RING} fill="none" stroke={WHEEL_LINE} strokeWidth={WHEEL_STROKE_W} />
          <circle cx={CX} cy={CY} r={R_GENDER_RING} fill="none" stroke={WHEEL_LINE} strokeWidth={WHEEL_STROKE_W} />
          <circle cx={CX} cy={CY} r={R_GLYPH_RING} fill="none" stroke={WHEEL_LINE} strokeWidth={WHEEL_STROKE_W} />
          <circle cx={CX} cy={CY} r={R_ELEM_RING} fill="none" stroke={WHEEL_LINE} strokeWidth={WHEEL_STROKE_W} />
          <circle cx={CX} cy={CY} r={R_INNER} fill="none" stroke={WHEEL_LINE} strokeWidth={WHEEL_STROKE_W} />

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
      </div>}

      {/* Legend — bottom */}
      <div className="rounded-lg bg-sacred-gold/5 px-3 py-1 mt-2 text-sm" style={{ fontFamily:'Inter,sans-serif', color: GOLD }}>
        <div className="flex flex-wrap justify-center gap-x-4 gap-y-1">
            <span className="flex items-center gap-1"><span className="font-bold" style={{ color: GOLD_MED }}>*</span>{hi?'वक्री':'Retro'}</span>
            <span className="flex items-center gap-1"><span className="font-bold" style={{ color: GOLD_MED }}>^</span>{hi?'अस्त':'Combust'}</span>
            <span className="flex items-center gap-1"><span className="font-bold" style={{ color: GOLD_MED }}>v</span>{hi?'वर्गोत्तम':'Vargottama'}</span>
            <span className="flex items-center gap-1"><span className="font-bold" style={{ color: GOLD_MED }}>+</span>{hi?'उच्च':'Exalted'}</span>
            <span className="flex items-center gap-1"><span className="font-bold" style={{ color: GOLD_MED }}>-</span>{hi?'नीच':'Debilitated'}</span>
        </div>
        <div className="flex flex-wrap justify-center gap-x-4 gap-y-1 mt-0.5">
            <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full" style={{ background:GOLD_MED }} />{hi?'शुभ':'Benefic'}</span>
            <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full" style={{ background:DARK }} />{hi?'पापी':'Malefic'}</span>
            <span className="flex items-center gap-1"><span className="w-2 h-2" style={{ background:GOLD_MED, clipPath:'polygon(50% 0%,0% 100%,100% 100%)' }} />ASC</span>
        </div>
      </div>
    </div>
  );
}
