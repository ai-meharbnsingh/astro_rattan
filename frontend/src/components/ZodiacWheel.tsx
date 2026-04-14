import { useTranslation } from '@/lib/i18n';

const toRad = (deg: number) => (deg * Math.PI) / 180;

/* ── Scaled to 600x600 viewBox to prevent clipping ── */
const CX = 300;
const CY = 300;

const SIGNS = [
  { en: 'CAPRICORN',   hi: 'मकर',     glyph: '\u2651\uFE0E', monthEn: 'JAN',   monthHi: 'जन',    img: '/images/zodiac-orange/zodiac-capricorn-orange.png' },
  { en: 'AQUARIUS',    hi: 'कुंभ',    glyph: '\u2652\uFE0E', monthEn: 'FEB',   monthHi: 'फर',    img: '/images/zodiac-orange/zodiac-aquarius-orange.png' },
  { en: 'PISCES',      hi: 'मीन',     glyph: '\u2653\uFE0E', monthEn: 'MAR',   monthHi: 'मार्च', img: '/images/zodiac-orange/zodiac-pisces-orange.png' },
  { en: 'ARIES',       hi: 'मेष',     glyph: '\u2648\uFE0E', monthEn: 'APR',   monthHi: 'अप्रै', img: '/images/zodiac-orange/zodiac-aries-orange.png' },
  { en: 'TAURUS',      hi: 'वृषभ',    glyph: '\u2649\uFE0E', monthEn: 'MAY',   monthHi: 'मई',    img: '/images/zodiac-orange/zodiac-taurus-orange.png' },
  { en: 'GEMINI',      hi: 'मिथुन',   glyph: '\u264A\uFE0E', monthEn: 'JUN',   monthHi: 'जून',   img: '/images/zodiac-orange/zodiac-gemini-orange.png' },
  { en: 'CANCER',      hi: 'कर्क',    glyph: '\u264B\uFE0E', monthEn: 'JUL',   monthHi: 'जुला',  img: '/images/zodiac-orange/zodiac-cancer-orange.png' },
  { en: 'LEO',         hi: 'सिंह',    glyph: '\u264C\uFE0E', monthEn: 'AUG',   monthHi: 'अग',    img: '/images/zodiac-orange/zodiac-leo-orange.png' },
  { en: 'VIRGO',       hi: 'कन्या',   glyph: '\u264D\uFE0E', monthEn: 'SEP',   monthHi: 'सित',   img: '/images/zodiac-orange/zodiac-virgo-orange.png' },
  { en: 'LIBRA',       hi: 'तुला',    glyph: '\u264E\uFE0E', monthEn: 'OCT',   monthHi: 'अक्टू', img: '/images/zodiac-orange/zodiac-libra-orange.png' },
  { en: 'SCORPIO',     hi: 'वृश्चिक', glyph: '\u264F\uFE0E', monthEn: 'NOV',   monthHi: 'नव',    img: '/images/zodiac-orange/zodiac-scorpio-orange.png' },
  { en: 'SAGITTARIUS', hi: 'धनु',     glyph: '\u2650\uFE0E', monthEn: 'DEC',   monthHi: 'दिस',   img: '/images/zodiac-orange/zodiac-sagittarius-orange.png' },
];

/* ── Ring radii (scaled 1.2x from 500-base) ── */
const R_SUN = 72;            // innermost — sun
const R_GLYPH_MID = 115;    // glyph text center
const R_NAME_RING = 158;    // ring line between glyph & name
const R_NAME_MID = 190;     // sign name text center
const R_IMG_RING = 222;     // ring line between name & illustration
const R_IMG_MID = 262;      // illustration center — INSIDE the wheel
const R_MONTH_RING = 302;   // ring line between illustration & month
const R_MONTH_MID = 330;    // month label center
const R_OUTER = 358;        // outer border circle
const R_ARROW_TIP = 376;    // arrowhead tip — just past outer ring

const GOLD = '#8B4513';
const GOLD_MED = '#C4611F';
const GOLD_LIGHT = 'rgba(196,97,31,0.4)';

/** Text rotation tangent to arc, flipped for readability from outside */
function arcRot(midDeg: number): number {
  const t = ((midDeg + 90) % 360 + 360) % 360;
  return (t > 90 && t < 270) ? t + 180 : t;
}

export default function ZodiacWheel() {
  const { language } = useTranslation();

  // Tick marks on outer ring
  const ticks: JSX.Element[] = [];
  for (let i = 0; i < 360; i += 3) {
    const a = toRad(i);
    const isMajor = i % 30 === 0;
    const isMid = i % 15 === 0;
    const r2 = isMajor ? R_OUTER - 10 : isMid ? R_OUTER - 6 : R_OUTER - 3;
    ticks.push(
      <line key={`t${i}`}
        x1={CX + R_OUTER * Math.cos(a)} y1={CY + R_OUTER * Math.sin(a)}
        x2={CX + r2 * Math.cos(a)} y2={CY + r2 * Math.sin(a)}
        stroke={GOLD_LIGHT} strokeWidth={isMajor ? 1.4 : 0.5}
      />
    );
  }

  // Section content: dividers, glyphs, names, images, months
  const sections = SIGNS.map((sign, i) => {
    const startDeg = i * 30 - 90;
    const midDeg = startDeg + 15;
    const startRad = toRad(startDeg);
    const midRad = toRad(midDeg);

    // Divider line — from sun to arrow tip
    const lx1 = CX + R_SUN * Math.cos(startRad);
    const ly1 = CY + R_SUN * Math.sin(startRad);
    const lx2 = CX + R_ARROW_TIP * Math.cos(startRad);
    const ly2 = CY + R_ARROW_TIP * Math.sin(startRad);

    // Glyph
    const gx = CX + R_GLYPH_MID * Math.cos(midRad);
    const gy = CY + R_GLYPH_MID * Math.sin(midRad);

    // Sign name
    const nx = CX + R_NAME_MID * Math.cos(midRad);
    const ny = CY + R_NAME_MID * Math.sin(midRad);
    const nRot = arcRot(midDeg);

    // Illustration — INSIDE the wheel between R_IMG_RING and R_MONTH_RING
    const ax = CX + R_IMG_MID * Math.cos(midRad);
    const ay = CY + R_IMG_MID * Math.sin(midRad);

    // Month label
    const mx = CX + R_MONTH_MID * Math.cos(midRad);
    const my = CY + R_MONTH_MID * Math.sin(midRad);
    const mRot = arcRot(midDeg);

    const signName = language === 'hi' ? sign.hi : sign.en;
    const monthName = language === 'hi' ? sign.monthHi : sign.monthEn;
    const nameFontSize = language === 'hi' ? 15 : (signName.length > 9 ? 11 : 13);

    return (
      <g key={sign.en}>
        {/* Divider line with arrowhead */}
        <line
          x1={lx1} y1={ly1} x2={lx2} y2={ly2}
          stroke={GOLD_MED} strokeWidth={1.2}
          markerEnd="url(#arrowhead)"
        />

        {/* Glyph symbol */}
        <text x={gx} y={gy}
          textAnchor="middle" dominantBaseline="central"
          fill={GOLD_MED} fontSize="30" fontWeight="bold"
          fontFamily="'Segoe UI Symbol','Noto Sans Symbols 2',serif"
        >{sign.glyph}</text>

        {/* Sign name — along arc */}
        <text x={nx} y={ny}
          textAnchor="middle" dominantBaseline="central"
          fill={GOLD_MED} fontSize={nameFontSize} fontWeight="700"
          letterSpacing="0.5"
          fontFamily="'Inter',sans-serif"
          transform={`rotate(${nRot},${nx},${ny})`}
        >{signName}</text>

        {/* Zodiac illustration — INSIDE wheel, circular clip */}
        <image
          href={sign.img}
          x={ax - 33} y={ay - 33}
          width={66} height={66}
          preserveAspectRatio="xMidYMid slice"
          clipPath={`url(#imgClip${i})`}
          style={{ filter: 'sepia(0.4) brightness(0.85) contrast(1.1)', opacity: 0.9 }}
        />

        {/* Month label — along arc */}
        <text x={mx} y={my}
          textAnchor="middle" dominantBaseline="central"
          fill={GOLD} fontSize="18" fontWeight="800"
          letterSpacing="1"
          fontFamily="'Inter',sans-serif"
          transform={`rotate(${mRot},${mx},${my})`}
        >{monthName}</text>
      </g>
    );
  });

  // Sun center rays
  const sunRays: JSX.Element[] = [];
  for (let i = 0; i < 36; i++) {
    const a = toRad(i * 10);
    const long = i % 2 === 0;
    sunRays.push(
      <line key={`sr${i}`}
        x1={CX + 16 * Math.cos(a)} y1={CY + 16 * Math.sin(a)}
        x2={CX + (long ? R_SUN - 4 : R_SUN - 16) * Math.cos(a)}
        y2={CY + (long ? R_SUN - 4 : R_SUN - 16) * Math.sin(a)}
        stroke={long ? GOLD_MED : GOLD_LIGHT}
        strokeWidth={long ? 2 : 0.9}
      />
    );
  }

  return (
    <div className="relative w-full max-w-[420px] mx-auto" style={{ overflow: 'visible', padding: '20px' }}>
      {/* Soft glow */}
      <div className="absolute inset-0 rounded-full bg-sacred-gold/5 blur-3xl" />

      {/* 3D float wrapper */}
      <div className="chakra-float" style={{ transformStyle: 'preserve-3d', overflow: 'visible' }}>
        <svg
          viewBox="0 0 600 600"
          className="w-full h-full wheel-spin"
          style={{
            overflow: 'visible',
            filter: 'drop-shadow(8px 16px 24px rgba(139,69,19,0.45)) drop-shadow(0px 4px 8px rgba(196,97,31,0.25)) drop-shadow(-3px -3px 8px rgba(255,210,120,0.15))',
          }}
        >
          <defs>
            {/* Arrowhead marker */}
            <marker id="arrowhead" markerWidth="12" markerHeight="9" refX="10" refY="4.5" orient="auto" markerUnits="userSpaceOnUse">
              <polygon points="0 0, 12 4.5, 0 9" fill={GOLD} />
            </marker>

            {/* Circular clip paths for each illustration */}
            {SIGNS.map((_, i) => {
              const midDeg = i * 30 + 15 - 90;
              const midRad = toRad(midDeg);
              const imgCx = CX + R_IMG_MID * Math.cos(midRad);
              const imgCy = CY + R_IMG_MID * Math.sin(midRad);
              return (
                <clipPath key={`clip${i}`} id={`imgClip${i}`}>
                  <circle cx={imgCx} cy={imgCy} r={31} />
                </clipPath>
              );
            })}
          </defs>

          {/* Ring circles */}
          <circle cx={CX} cy={CY} r={R_OUTER} fill="none" stroke={GOLD} strokeWidth={2.5} />
          {ticks}
          <circle cx={CX} cy={CY} r={R_MONTH_RING} fill="none" stroke={GOLD_LIGHT} strokeWidth={0.8} />
          <circle cx={CX} cy={CY} r={R_IMG_RING} fill="none" stroke={GOLD} strokeWidth={1} />
          <circle cx={CX} cy={CY} r={R_NAME_RING} fill="none" stroke={GOLD_LIGHT} strokeWidth={0.8} />
          <circle cx={CX} cy={CY} r={R_SUN} fill="none" stroke={GOLD} strokeWidth={1.5} />

          {/* 12 sections */}
          {sections}

          {/* Sun center — drawn on top */}
          <circle cx={CX} cy={CY} r={R_SUN} fill="#FAF7F2" stroke={GOLD_MED} strokeWidth={1.5} />
          {sunRays}
          <circle cx={CX} cy={CY} r={14} fill={GOLD_MED} opacity={0.85} />
          <circle cx={CX} cy={CY} r={8} fill="#FAF7F2" opacity={0.4} />
        </svg>
      </div>
    </div>
  );
}
