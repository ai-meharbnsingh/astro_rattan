import { useTranslation } from '@/lib/i18n';

const SIGNS = [
  { en: 'CAPRICORN',   hi: 'मकर',     symbol: '\u2651\uFE0E', monthEn: 'JAN',  monthHi: 'जन' },
  { en: 'AQUARIUS',    hi: 'कुंभ',    symbol: '\u2652\uFE0E', monthEn: 'FEB',  monthHi: 'फर' },
  { en: 'PISCES',      hi: 'मीन',     symbol: '\u2653\uFE0E', monthEn: 'MAR',  monthHi: 'मार्च' },
  { en: 'ARIES',       hi: 'मेष',     symbol: '\u2648\uFE0E', monthEn: 'APR',  monthHi: 'अप्रै' },
  { en: 'TAURUS',      hi: 'वृषभ',    symbol: '\u2649\uFE0E', monthEn: 'MAY',  monthHi: 'मई' },
  { en: 'GEMINI',      hi: 'मिथुन',   symbol: '\u264A\uFE0E', monthEn: 'JUNE', monthHi: 'जून' },
  { en: 'CANCER',      hi: 'कर्क',    symbol: '\u264B\uFE0E', monthEn: 'JULY', monthHi: 'जुला' },
  { en: 'LEO',         hi: 'सिंह',    symbol: '\u264C\uFE0E', monthEn: 'AUG',  monthHi: 'अग' },
  { en: 'VIRGO',       hi: 'कन्या',   symbol: '\u264D\uFE0E', monthEn: 'SEP',  monthHi: 'सित' },
  { en: 'LIBRA',       hi: 'तुला',    symbol: '\u264E\uFE0E', monthEn: 'OCT',  monthHi: 'अक्टू' },
  { en: 'SCORPIO',     hi: 'वृश्चिक', symbol: '\u264F\uFE0E', monthEn: 'NOV',  monthHi: 'नव' },
  { en: 'SAGITTARIUS', hi: 'धनु',     symbol: '\u2650\uFE0E', monthEn: 'DEC',  monthHi: 'दिस' },
];

// Compact SVG line-art paths for each zodiac animal/figure (30x30 viewBox)
const SIGN_ART: Record<string, string> = {
  ARIES:       'M8,22 C8,12 5,6 10,3 C13,1 15,5 15,10 M15,10 C15,5 17,1 20,3 C25,6 22,12 22,22 M15,10 L15,28',
  TAURUS:      'M5,10 C5,4 10,1 15,4 C20,1 25,4 25,10 M5,10 L5,18 C5,24 10,28 15,28 C20,28 25,24 25,18 L25,10 M12,18 A1.5,1.5 0 1,0 12,19 M18,18 A1.5,1.5 0 1,0 18,19',
  GEMINI:      'M9,5 L9,25 M9,5 C9,5 12,3 15,5 C18,3 21,5 21,5 M9,25 C9,25 12,27 15,25 C18,27 21,25 21,25 M21,5 L21,25 M9,12 L21,12 M9,18 L21,18',
  CANCER:      'M5,15 C5,8 12,5 15,10 C18,5 25,8 25,15 M5,15 C5,22 12,25 15,20 C18,25 25,22 25,15 M9,12 A2,2 0 1,0 9,13 M21,18 A2,2 0 1,0 21,19',
  LEO:         'M8,25 C8,18 5,15 8,10 C10,7 14,8 15,12 C16,8 20,7 22,10 C25,15 22,18 22,22 M15,12 L15,20 M10,20 C10,20 12,24 15,24 C18,24 20,20 20,20 M6,6 A4,4 0 1,0 6,7',
  VIRGO:       'M8,5 L8,25 M8,12 C12,8 14,12 14,16 L14,25 M14,12 C18,8 20,12 20,16 L20,25 M20,16 C22,14 25,16 24,20 C23,24 20,25 20,25',
  LIBRA:       'M5,24 L25,24 M7,24 L7,16 L12,12 M23,24 L23,16 L18,12 M12,12 L18,12 M15,12 L15,6 M10,6 L20,6 M10,6 C10,3 20,3 20,6',
  SCORPIO:     'M6,8 L6,22 M6,14 C8,10 10,12 12,16 L12,22 M12,14 C14,10 16,12 18,16 L18,22 M18,22 L22,18 M22,18 L20,16 M22,18 L24,16',
  SAGITTARIUS: 'M6,26 L24,4 M18,4 L24,4 L24,10 M6,16 L20,16 M20,12 L20,20',
  CAPRICORN:   'M6,8 C6,4 10,4 12,8 L12,20 C12,24 16,26 18,22 C20,18 22,20 22,24 M12,12 C16,8 20,10 18,14',
  AQUARIUS:    'M4,12 C8,8 12,16 16,12 C20,8 24,16 28,12 M4,20 C8,16 12,24 16,20 C20,16 24,24 28,20',
  PISCES:      'M8,5 C4,10 4,20 8,25 M22,5 C26,10 26,20 22,25 M5,15 L25,15',
};

const gold = '#B8862E';
const goldMed = 'rgba(184,134,55,0.6)';
const goldFaint = 'rgba(184,134,55,0.3)';

export default function ZodiacWheel() {
  const { language } = useTranslation();
  const cx = 200;
  const cy = 200;

  const outerR = 192;
  const monthR = 180;
  const ringR = 168;
  const nameR = 153;
  const symbolRingR = 135;
  const symbolR = 108;
  const innerRingR = 80;
  const coreR = 48;

  const ticks: JSX.Element[] = [];
  for (let i = 0; i < 72; i++) {
    const a = (i * 5 * Math.PI) / 180;
    const r1 = outerR;
    const r2 = i % 6 === 0 ? outerR - 6 : outerR - 3;
    ticks.push(
      <line key={`t${i}`}
        x1={cx + r1 * Math.cos(a)} y1={cy + r1 * Math.sin(a)}
        x2={cx + r2 * Math.cos(a)} y2={cy + r2 * Math.sin(a)}
        stroke={goldFaint} strokeWidth={i % 6 === 0 ? 1 : 0.5}
      />
    );
  }

  const segments = SIGNS.map((sign, i) => {
    const startDeg = i * 30 - 90;
    const midDeg = startDeg + 15;
    const startRad = (startDeg * Math.PI) / 180;
    const midRad = (midDeg * Math.PI) / 180;

    // Divider line
    const dx1 = cx + innerRingR * Math.cos(startRad);
    const dy1 = cy + innerRingR * Math.sin(startRad);
    const dx2 = cx + outerR * Math.cos(startRad);
    const dy2 = cy + outerR * Math.sin(startRad);

    // Month text
    const mx = cx + monthR * Math.cos(midRad);
    const my = cy + monthR * Math.sin(midRad);
    const monthFlip = midDeg > 90 && midDeg < 270;
    const monthTextRot = monthFlip ? midDeg + 180 : midDeg;

    // Sign name
    const nx = cx + nameR * Math.cos(midRad);
    const ny = cy + nameR * Math.sin(midRad);
    const nameFlip = midDeg > 90 && midDeg < 270;
    const nameTextRot = nameFlip ? midDeg + 180 : midDeg;

    // Zodiac art position
    const artX = cx + symbolR * Math.cos(midRad);
    const artY = cy + symbolR * Math.sin(midRad);

    const signName = language === 'hi' ? sign.hi : sign.en;
    const monthName = language === 'hi' ? sign.monthHi : sign.monthEn;
    const nameFontSize = language === 'hi' ? 8 : (signName.length > 9 ? 5.5 : 6.5);
    const artPath = SIGN_ART[sign.en] || '';

    return (
      <g key={sign.en}>
        <line x1={dx1} y1={dy1} x2={dx2} y2={dy2} stroke={goldFaint} strokeWidth={0.8} />

        {/* Month name */}
        <text x={mx} y={my}
          textAnchor="middle" dominantBaseline="central"
          fill={goldMed} fontSize="7" fontWeight="700" letterSpacing="1"
          transform={`rotate(${monthTextRot},${mx},${my})`}
        >{monthName}</text>

        {/* Sign name */}
        <text x={nx} y={ny}
          textAnchor="middle" dominantBaseline="central"
          fill={gold} fontSize={nameFontSize} fontWeight="600" letterSpacing="0.5"
          transform={`rotate(${nameTextRot},${nx},${ny})`}
        >{signName}</text>

        {/* Zodiac line-art illustration */}
        <g transform={`translate(${artX - 15},${artY - 15}) scale(1)`}>
          {/* Disc background for 3D depth */}
          <circle cx={15} cy={15} r={16} fill="rgba(184,134,55,0.06)" stroke={goldFaint} strokeWidth={0.5} />
          <path
            d={artPath}
            fill="none"
            stroke={gold}
            strokeWidth={1.4}
            strokeLinecap="round"
            strokeLinejoin="round"
            style={{ filter: `drop-shadow(0 0 3px rgba(184,134,55,0.4))` }}
          />
        </g>
      </g>
    );
  });

  // Sun rays
  const sunRays: JSX.Element[] = [];
  for (let i = 0; i < 24; i++) {
    const a = (i * 15 * Math.PI) / 180;
    const r1 = i % 2 === 0 ? coreR - 4 : coreR - 10;
    const r2 = 14;
    sunRays.push(
      <line key={`sr${i}`}
        x1={cx + r2 * Math.cos(a)} y1={cy + r2 * Math.sin(a)}
        x2={cx + r1 * Math.cos(a)} y2={cy + r1 * Math.sin(a)}
        stroke={i % 2 === 0 ? gold : goldMed}
        strokeWidth={i % 2 === 0 ? 1.5 : 0.8}
      />
    );
  }

  return (
    <div className="relative w-full max-w-[420px] mx-auto" style={{ perspective: '900px' }}>
      <div className="absolute inset-[-15%] rounded-full bg-sacred-gold/8 blur-3xl" />
      <div style={{ transform: 'rotateX(14deg)', transformStyle: 'preserve-3d' }}>
        <svg
          viewBox="0 0 400 400"
          className="w-full h-full animate-spin-slow"
          style={{ filter: 'drop-shadow(0 0 20px rgba(184,134,55,0.2))' }}
        >
          <circle cx={cx} cy={cy} r={outerR} fill="none" stroke={gold} strokeWidth={2} />
          {ticks}
          <circle cx={cx} cy={cy} r={ringR} fill="none" stroke={goldFaint} strokeWidth={0.8} />
          <circle cx={cx} cy={cy} r={symbolRingR} fill="none" stroke={goldFaint} strokeWidth={0.8} />
          <circle cx={cx} cy={cy} r={innerRingR} fill="none" stroke={gold} strokeWidth={1.2} />
          <circle cx={cx} cy={cy} r={coreR} fill="none" stroke={gold} strokeWidth={1.2} />
          {segments}
          {sunRays}
          <circle cx={cx} cy={cy} r={12} fill="none" stroke={gold} strokeWidth={1} />
          <circle cx={cx} cy={cy} r={6} fill={gold} opacity={0.6} />
          <circle cx={cx} cy={cy} r={3} fill={gold} opacity={0.9} />
        </svg>
      </div>
    </div>
  );
}
