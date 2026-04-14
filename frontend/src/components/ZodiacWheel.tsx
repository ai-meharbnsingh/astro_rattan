import { useTranslation } from '@/lib/i18n';

const SIGNS = [
  { en: 'CAPRICORN',   hi: 'मकर',     symbol: '\u2651', monthEn: 'JAN',  monthHi: 'जन' },
  { en: 'AQUARIUS',    hi: 'कुंभ',    symbol: '\u2652', monthEn: 'FEB',  monthHi: 'फर' },
  { en: 'PISCES',      hi: 'मीन',     symbol: '\u2653', monthEn: 'MAR',  monthHi: 'मार्च' },
  { en: 'ARIES',       hi: 'मेष',     symbol: '\u2648', monthEn: 'APR',  monthHi: 'अप्रै' },
  { en: 'TAURUS',      hi: 'वृषभ',    symbol: '\u2649', monthEn: 'MAY',  monthHi: 'मई' },
  { en: 'GEMINI',      hi: 'मिथुन',   symbol: '\u264A', monthEn: 'JUNE', monthHi: 'जून' },
  { en: 'CANCER',      hi: 'कर्क',    symbol: '\u264B', monthEn: 'JULY', monthHi: 'जुला' },
  { en: 'LEO',         hi: 'सिंह',    symbol: '\u264C', monthEn: 'AUG',  monthHi: 'अग' },
  { en: 'VIRGO',       hi: 'कन्या',   symbol: '\u264D', monthEn: 'SEP',  monthHi: 'सित' },
  { en: 'LIBRA',       hi: 'तुला',    symbol: '\u264E', monthEn: 'OCT',  monthHi: 'अक्टू' },
  { en: 'SCORPIO',     hi: 'वृश्चिक', symbol: '\u264F', monthEn: 'NOV',  monthHi: 'नव' },
  { en: 'SAGITTARIUS', hi: 'धनु',     symbol: '\u2650', monthEn: 'DEC',  monthHi: 'दिस' },
];

const gold = '#B8862E';
const goldLight = 'rgba(184,134,55,0.7)';
const goldFaint = 'rgba(184,134,55,0.3)';
const goldGlow = 'rgba(184,134,55,0.5)';

export default function ZodiacWheel() {
  const { language } = useTranslation();
  const cx = 200;
  const cy = 200;

  // Ring radii
  const outerR = 192;     // outer edge
  const monthR = 180;     // month text radius
  const ringR = 168;      // ring between months and names
  const nameR = 152;      // sign name text radius
  const symbolRingR = 132; // ring between names and symbols
  const symbolR = 108;    // symbol position radius
  const innerRingR = 82;  // inner ring
  const coreR = 50;       // center mandala

  // Build segments
  const segments = SIGNS.map((sign, i) => {
    const startDeg = i * 30 - 90;
    const midDeg = startDeg + 15;
    const startRad = (startDeg * Math.PI) / 180;
    const midRad = (midDeg * Math.PI) / 180;

    // Divider line from inner ring to outer
    const dx1 = cx + innerRingR * Math.cos(startRad);
    const dy1 = cy + innerRingR * Math.sin(startRad);
    const dx2 = cx + outerR * Math.cos(startRad);
    const dy2 = cy + outerR * Math.sin(startRad);

    // Month text position (outer ring)
    const mx = cx + monthR * Math.cos(midRad);
    const my = cy + monthR * Math.sin(midRad);
    const monthRotDeg = midDeg;
    const monthFlip = monthRotDeg > 90 && monthRotDeg < 270;
    const monthTextRot = monthFlip ? monthRotDeg + 180 : monthRotDeg;

    // Sign name position (middle ring)
    const nx = cx + nameR * Math.cos(midRad);
    const ny = cy + nameR * Math.sin(midRad);
    const nameFlip = midDeg > 90 && midDeg < 270;
    const nameTextRot = nameFlip ? midDeg + 180 : midDeg;

    // Symbol position (inner ring)
    const sx = cx + symbolR * Math.cos(midRad);
    const sy = cy + symbolR * Math.sin(midRad);

    const signName = language === 'hi' ? sign.hi : sign.en;
    const monthName = language === 'hi' ? sign.monthHi : sign.monthEn;
    const nameFontSize = language === 'hi' ? 8 : (signName.length > 9 ? 5.5 : 6.5);

    return (
      <g key={sign.en}>
        {/* Divider line */}
        <line x1={dx1} y1={dy1} x2={dx2} y2={dy2} stroke={goldFaint} strokeWidth={0.8} />

        {/* Month name */}
        <text
          x={mx} y={my}
          textAnchor="middle" dominantBaseline="central"
          fill={goldLight}
          fontSize="7"
          fontWeight="700"
          letterSpacing="1"
          transform={`rotate(${monthTextRot},${mx},${my})`}
        >
          {monthName}
        </text>

        {/* Sign name */}
        <text
          x={nx} y={ny}
          textAnchor="middle" dominantBaseline="central"
          fill={gold}
          fontSize={nameFontSize}
          fontWeight="600"
          letterSpacing="0.5"
          transform={`rotate(${nameTextRot},${nx},${ny})`}
        >
          {signName}
        </text>

        {/* Zodiac symbol */}
        <text
          x={sx} y={sy}
          textAnchor="middle" dominantBaseline="central"
          fill={gold}
          fontSize="26"
          fontWeight="bold"
          style={{ filter: `drop-shadow(0 0 6px ${goldGlow})` }}
        >
          {sign.symbol}
        </text>
      </g>
    );
  });

  // Central sun rays
  const sunRays: JSX.Element[] = [];
  for (let i = 0; i < 24; i++) {
    const a = (i * 15 * Math.PI) / 180;
    const r1 = i % 2 === 0 ? coreR - 4 : coreR - 10;
    const r2 = 14;
    sunRays.push(
      <line
        key={`sr${i}`}
        x1={cx + r2 * Math.cos(a)}
        y1={cy + r2 * Math.sin(a)}
        x2={cx + r1 * Math.cos(a)}
        y2={cy + r1 * Math.sin(a)}
        stroke={i % 2 === 0 ? gold : goldLight}
        strokeWidth={i % 2 === 0 ? 1.5 : 0.8}
      />
    );
  }

  // Tick marks on outer edge
  const ticks: JSX.Element[] = [];
  for (let i = 0; i < 72; i++) {
    const a = (i * 5 * Math.PI) / 180;
    const r1 = outerR;
    const r2 = i % 6 === 0 ? outerR - 6 : outerR - 3;
    ticks.push(
      <line
        key={`t${i}`}
        x1={cx + r1 * Math.cos(a)} y1={cy + r1 * Math.sin(a)}
        x2={cx + r2 * Math.cos(a)} y2={cy + r2 * Math.sin(a)}
        stroke={goldFaint}
        strokeWidth={i % 6 === 0 ? 1 : 0.5}
      />
    );
  }

  return (
    <div className="relative w-full max-w-[420px] mx-auto" style={{ perspective: '900px' }}>
      {/* Glow */}
      <div className="absolute inset-[-15%] rounded-full bg-sacred-gold/8 blur-3xl" />

      {/* 3D tilt wrapper */}
      <div style={{ transform: 'rotateX(14deg)', transformStyle: 'preserve-3d' }}>
        <svg
          viewBox="0 0 400 400"
          className="w-full h-full animate-spin-slow"
          style={{ filter: `drop-shadow(0 0 20px rgba(184,134,55,0.2))` }}
        >
          {/* Outer ring */}
          <circle cx={cx} cy={cy} r={outerR} fill="none" stroke={gold} strokeWidth={2} />
          {ticks}

          {/* Ring between months and names */}
          <circle cx={cx} cy={cy} r={ringR} fill="none" stroke={goldFaint} strokeWidth={0.8} />

          {/* Ring between names and symbols */}
          <circle cx={cx} cy={cy} r={symbolRingR} fill="none" stroke={goldFaint} strokeWidth={0.8} />

          {/* Inner ring */}
          <circle cx={cx} cy={cy} r={innerRingR} fill="none" stroke={gold} strokeWidth={1.2} />

          {/* Core ring */}
          <circle cx={cx} cy={cy} r={coreR} fill="none" stroke={gold} strokeWidth={1.2} />

          {/* Segments */}
          {segments}

          {/* Center sun */}
          {sunRays}
          <circle cx={cx} cy={cy} r={12} fill="none" stroke={gold} strokeWidth={1} />
          <circle cx={cx} cy={cy} r={6} fill={gold} opacity={0.6} />
          <circle cx={cx} cy={cy} r={3} fill={gold} opacity={0.9} />
        </svg>
      </div>
    </div>
  );
}
