import { useTranslation } from '@/lib/i18n';

const SIGNS = [
  { en: 'CAPRICORN',   hi: 'मकर',     glyph: '\u2651\uFE0E', monthEn: 'JAN.',  monthHi: 'जन.',   img: '/images/zodiac/capricorn.png' },
  { en: 'AQUARIUS',    hi: 'कुंभ',    glyph: '\u2652\uFE0E', monthEn: 'FEB.',  monthHi: 'फर.',   img: '/images/zodiac/aquarius.png' },
  { en: 'PISCES',      hi: 'मीन',     glyph: '\u2653\uFE0E', monthEn: 'MAR.',  monthHi: 'मार्च', img: '/images/zodiac/pisces.png' },
  { en: 'ARIES',       hi: 'मेष',     glyph: '\u2648\uFE0E', monthEn: 'APRIL', monthHi: 'अप्रैल', img: '/images/zodiac/aries.png' },
  { en: 'TAURUS',      hi: 'वृषभ',    glyph: '\u2649\uFE0E', monthEn: 'MAY',   monthHi: 'मई',    img: '/images/zodiac/taurus.png' },
  { en: 'GEMINI',      hi: 'मिथुन',   glyph: '\u264A\uFE0E', monthEn: 'JUNE',  monthHi: 'जून',   img: '/images/zodiac/gemini.png' },
  { en: 'CANCER',      hi: 'कर्क',    glyph: '\u264B\uFE0E', monthEn: 'JULY',  monthHi: 'जुला.', img: '/images/zodiac/cancer.png' },
  { en: 'LEO',         hi: 'सिंह',    glyph: '\u264C\uFE0E', monthEn: 'AUG.',  monthHi: 'अग.',   img: '/images/zodiac/leo.png' },
  { en: 'VIRGO',       hi: 'कन्या',   glyph: '\u264D\uFE0E', monthEn: 'SEPT.', monthHi: 'सित.',  img: '/images/zodiac/virgo.png' },
  { en: 'LIBRA',       hi: 'तुला',    glyph: '\u264E\uFE0E', monthEn: 'OCT.',  monthHi: 'अक्टू.', img: '/images/zodiac/libra.png' },
  { en: 'SCORPIO',     hi: 'वृश्चिक', glyph: '\u264F\uFE0E', monthEn: 'NOV.',  monthHi: 'नव.',   img: '/images/zodiac/scorpio.png' },
  { en: 'SAGITTARIUS', hi: 'धनु',     glyph: '\u2650\uFE0E', monthEn: 'DEC.',  monthHi: 'दिस.',  img: '/images/zodiac/sagittarius.png' },
];

const gold = '#B8862E';
const goldMed = 'rgba(184,134,55,0.6)';
const goldFaint = 'rgba(184,134,55,0.3)';

/** Text rotation tangent to circle, flipped on bottom half so always readable from outside */
function arcRot(midDeg: number): number {
  const t = ((midDeg + 90) % 360 + 360) % 360;
  return (t > 90 && t < 270) ? t + 180 : t;
}

export default function ZodiacWheel() {
  const { language } = useTranslation();
  const cx = 200;
  const cy = 200;

  const outerR = 195;
  const monthR = 182;
  const artRingOuter = 168;
  const artR = 140;
  const nameRingR = 112;
  const nameR = 100;
  const glyphR = 80;
  const innerRingR = 65;
  const coreR = 44;
  const imgSize = 44; // image render size in SVG units

  // Tick marks
  const ticks: JSX.Element[] = [];
  for (let i = 0; i < 360; i += 3) {
    const a = (i * Math.PI) / 180;
    const isMajor = i % 30 === 0;
    const isMid = i % 15 === 0;
    const r2 = isMajor ? outerR - 8 : isMid ? outerR - 5 : outerR - 3;
    ticks.push(
      <line key={`t${i}`}
        x1={cx + outerR * Math.cos(a)} y1={cy + outerR * Math.sin(a)}
        x2={cx + r2 * Math.cos(a)} y2={cy + r2 * Math.sin(a)}
        stroke={goldFaint} strokeWidth={isMajor ? 1.2 : 0.4}
      />
    );
  }

  const segments = SIGNS.map((sign, i) => {
    const startDeg = i * 30 - 90;
    const midDeg = startDeg + 15;
    const startRad = (startDeg * Math.PI) / 180;
    const midRad = (midDeg * Math.PI) / 180;

    // Divider lines
    const lx1 = cx + innerRingR * Math.cos(startRad);
    const ly1 = cy + innerRingR * Math.sin(startRad);
    const lx2 = cx + artRingOuter * Math.cos(startRad);
    const ly2 = cy + artRingOuter * Math.sin(startRad);

    // Month text — tangent to arc
    const mx = cx + monthR * Math.cos(midRad);
    const my = cy + monthR * Math.sin(midRad);
    const mRot = arcRot(midDeg);

    // Image center
    const ax = cx + artR * Math.cos(midRad);
    const ay = cy + artR * Math.sin(midRad);

    // Sign name — tangent to arc
    const nx = cx + nameR * Math.cos(midRad);
    const ny = cy + nameR * Math.sin(midRad);
    const nRot = arcRot(midDeg);

    // Glyph
    const gx = cx + glyphR * Math.cos(midRad);
    const gy = cy + glyphR * Math.sin(midRad);

    const signName = language === 'hi' ? sign.hi : sign.en;
    const monthName = language === 'hi' ? sign.monthHi : sign.monthEn;
    const nameFontSize = language === 'hi' ? 7.5 : (signName.length > 9 ? 5 : 6.5);

    return (
      <g key={sign.en}>
        <line x1={lx1} y1={ly1} x2={lx2} y2={ly2} stroke={goldMed} strokeWidth={0.7} />

        {/* Month — along arc */}
        <text x={mx} y={my}
          textAnchor="middle" dominantBaseline="central"
          fill={gold} fontSize="9.5" fontWeight="800" letterSpacing="0.8"
          fontFamily="'Inter', sans-serif"
          transform={`rotate(${mRot},${mx},${my})`}
        >{monthName}</text>

        {/* Zodiac engraving image — counter-rotated so figure stays upright */}
        <image
          href={sign.img}
          x={ax - imgSize / 2}
          y={ay - imgSize / 2}
          width={imgSize}
          height={imgSize}
          style={{
            filter: 'sepia(0.3) brightness(0.85) contrast(1.1)',
            opacity: 0.85,
          }}
          preserveAspectRatio="xMidYMid meet"
        />

        {/* Sign name — along arc */}
        <text x={nx} y={ny}
          textAnchor="middle" dominantBaseline="central"
          fill={gold} fontSize={nameFontSize} fontWeight="700" letterSpacing="0.3"
          fontFamily="'Inter', sans-serif"
          transform={`rotate(${nRot},${nx},${ny})`}
        >{signName}</text>

        {/* Glyph */}
        <text x={gx} y={gy}
          textAnchor="middle" dominantBaseline="central"
          fill={gold} fontSize="14" fontWeight="bold"
          fontFamily="'Segoe UI Symbol','Noto Sans Symbols 2',serif"
          style={{ filter: 'drop-shadow(0 0 2px rgba(184,134,55,0.35))' }}
        >{sign.glyph}</text>
      </g>
    );
  });

  // Sun rays
  const sunRays: JSX.Element[] = [];
  for (let i = 0; i < 32; i++) {
    const a = (i * 11.25 * Math.PI) / 180;
    const long = i % 2 === 0;
    sunRays.push(
      <line key={`sr${i}`}
        x1={cx + 11 * Math.cos(a)} y1={cy + 11 * Math.sin(a)}
        x2={cx + (long ? coreR - 3 : coreR - 9) * Math.cos(a)}
        y2={cy + (long ? coreR - 3 : coreR - 9) * Math.sin(a)}
        stroke={long ? gold : goldMed}
        strokeWidth={long ? 1.5 : 0.7}
      />
    );
  }

  return (
    <div className="relative w-full max-w-[440px] mx-auto" style={{ perspective: '900px' }}>
      <div className="absolute inset-[-10%] rounded-full bg-sacred-gold/5 blur-3xl" />
      <div style={{ transformStyle: 'preserve-3d' }}>
        <svg
          viewBox="0 0 400 400"
          className="w-full h-full animate-spin-slow"
          style={{ filter: 'drop-shadow(0 0 24px rgba(184,134,55,0.15))' }}
        >
          <circle cx={cx} cy={cy} r={outerR} fill="none" stroke={gold} strokeWidth={2.5} />
          {ticks}
          <circle cx={cx} cy={cy} r={artRingOuter} fill="none" stroke={gold} strokeWidth={1} />
          <circle cx={cx} cy={cy} r={nameRingR} fill="none" stroke={goldFaint} strokeWidth={0.8} />
          <circle cx={cx} cy={cy} r={innerRingR} fill="none" stroke={gold} strokeWidth={1.2} />
          <circle cx={cx} cy={cy} r={coreR} fill="none" stroke={gold} strokeWidth={1.5} />
          {segments}
          {sunRays}
          <circle cx={cx} cy={cy} r={9} fill={gold} opacity={0.8} />
          <circle cx={cx} cy={cy} r={5} fill="white" opacity={0.25} />
        </svg>
      </div>
    </div>
  );
}
