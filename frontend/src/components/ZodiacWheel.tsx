import { useTranslation } from '@/lib/i18n';

/* ── Sign data ─────────────────────────────────────────────── */
const SIGNS = [
  { en: 'CAPRICORN',   hi: 'मकर',     glyph: '\u2651\uFE0E', monthEn: 'JAN.',  monthHi: 'जन.' },
  { en: 'AQUARIUS',    hi: 'कुंभ',    glyph: '\u2652\uFE0E', monthEn: 'FEB.',  monthHi: 'फर.' },
  { en: 'PISCES',      hi: 'मीन',     glyph: '\u2653\uFE0E', monthEn: 'MAR.',  monthHi: 'मार्च' },
  { en: 'ARIES',       hi: 'मेष',     glyph: '\u2648\uFE0E', monthEn: 'APRIL', monthHi: 'अप्रैल' },
  { en: 'TAURUS',      hi: 'वृषभ',    glyph: '\u2649\uFE0E', monthEn: 'MAY',   monthHi: 'मई' },
  { en: 'GEMINI',      hi: 'मिथुन',   glyph: '\u264A\uFE0E', monthEn: 'JUNE',  monthHi: 'जून' },
  { en: 'CANCER',      hi: 'कर्क',    glyph: '\u264B\uFE0E', monthEn: 'JULY',  monthHi: 'जुला.' },
  { en: 'LEO',         hi: 'सिंह',    glyph: '\u264C\uFE0E', monthEn: 'AUG.',  monthHi: 'अग.' },
  { en: 'VIRGO',       hi: 'कन्या',   glyph: '\u264D\uFE0E', monthEn: 'SEPT.', monthHi: 'सित.' },
  { en: 'LIBRA',       hi: 'तुला',    glyph: '\u264E\uFE0E', monthEn: 'OCT.',  monthHi: 'अक्टू.' },
  { en: 'SCORPIO',     hi: 'वृश्चिक', glyph: '\u264F\uFE0E', monthEn: 'NOV.',  monthHi: 'नव.' },
  { en: 'SAGITTARIUS', hi: 'धनु',     glyph: '\u2650\uFE0E', monthEn: 'DEC.',  monthHi: 'दिस.' },
];

/* ── Detailed zodiac animal SVG paths (44×44 viewBox) ────── */
const ART: Record<string, string[]> = {
  // Capricorn — sea-goat: goat body with curling fish tail
  CAPRICORN: [
    'M10,18 C10,14 13,10 17,10 C19,10 21,11 22,13 L24,11 C25,10 27,10 27,12 L25,15',
    'M17,10 C15,8 14,5 16,4 C18,3 19,5 18,7',
    'M22,13 C23,16 22,20 20,24 C18,28 14,30 12,32 C10,34 8,33 9,31 C10,29 13,28 16,30 C19,32 22,30 24,28',
    'M12,14 A1,1 0 1,0 12,15',
  ],
  // Aquarius — water bearer kneeling, pouring from urn
  AQUARIUS: [
    'M18,6 A3,3 0 1,1 18,7',
    'M16,10 L14,16 L10,16 M22,10 L20,16 L24,20',
    'M14,16 L12,24 L10,30 M20,16 L18,24 L16,30',
    'M26,14 L28,12 L30,14 M26,18 L28,16 L30,18 M26,22 L28,20 L30,22',
    'M24,10 C26,8 28,9 27,11 L25,14',
  ],
  // Pisces — two fish swimming in opposite directions connected by cord
  PISCES: [
    'M8,10 C4,10 3,14 6,16 C3,18 4,22 8,22 C12,22 14,19 12,16 C14,13 12,10 8,10Z',
    'M30,10 C34,10 35,14 32,16 C35,18 34,22 30,22 C26,22 24,19 26,16 C24,13 26,10 30,10Z',
    'M12,16 L26,16',
    'M7,14 A1,1 0 1,0 7,15',
    'M31,14 A1,1 0 1,0 31,15',
    'M9,10 L6,8 M9,22 L6,24',
    'M29,10 L32,8 M29,22 L32,24',
  ],
  // Aries — ram with big curling horns
  ARIES: [
    'M18,8 C14,6 10,8 10,12 C10,16 14,16 16,14',
    'M20,8 C24,6 28,8 28,12 C28,16 24,16 22,14',
    'M16,14 C17,16 18,18 19,20 L19,30',
    'M22,14 C21,16 20,18 19,20',
    'M19,30 L15,34 M19,30 L23,34',
    'M17,12 A1,1 0 1,0 17,13',
    'M21,12 A1,1 0 1,0 21,13',
    'M18,16 L19,18 L20,16',
  ],
  // Taurus — bull head with horns and ring
  TAURUS: [
    'M12,14 C8,14 6,18 8,22 C10,26 14,28 19,28 C24,28 28,26 30,22 C32,18 30,14 26,14',
    'M12,14 C10,10 8,6 6,4 C5,3 4,4 5,6 L8,10',
    'M26,14 C28,10 30,6 32,4 C33,3 34,4 33,6 L30,10',
    'M15,20 A2,2 0 1,0 15,21',
    'M23,20 A2,2 0 1,0 23,21',
    'M17,26 C18,28 20,28 21,26',
    'M16,30 C17,32 21,32 22,30',
  ],
  // Gemini — two figures (twins) side by side
  GEMINI: [
    'M12,8 A3,3 0 1,1 12,9',
    'M26,8 A3,3 0 1,1 26,9',
    'M12,12 L12,24 M12,24 L9,30 M12,24 L15,30',
    'M26,12 L26,24 M26,24 L23,30 M26,24 L29,30',
    'M12,14 L8,18 M12,14 L16,18',
    'M26,14 L22,18 M26,14 L30,18',
    'M16,18 L22,18',
    'M12,6 C14,4 24,4 26,6',
  ],
  // Cancer — crab with two claws and legs
  CANCER: [
    'M12,16 C8,14 4,16 6,20 C8,24 14,26 19,26 C24,26 30,24 32,20 C34,16 30,14 26,16',
    'M12,16 L8,10 C6,8 4,10 6,12 L10,14',
    'M26,16 L30,10 C32,8 34,10 32,12 L28,14',
    'M8,10 L6,8 L4,10 M30,10 L32,8 L34,10',
    'M10,24 L8,28 M14,26 L12,30 M24,26 L26,30 M28,24 L30,28',
    'M16,20 A1.5,1.5 0 1,0 16,21',
    'M22,20 A1.5,1.5 0 1,0 22,21',
  ],
  // Leo — lion with flowing mane
  LEO: [
    'M14,10 C8,8 4,12 6,18 C4,14 4,10 8,8 C12,6 18,6 22,8 C26,6 30,8 32,12 C34,16 32,20 28,20',
    'M14,18 C14,14 16,12 19,12 C22,12 24,14 24,18 C24,22 22,24 19,24 C16,24 14,22 14,18Z',
    'M16,17 A1.5,1.5 0 1,0 16,18',
    'M22,17 A1.5,1.5 0 1,0 22,18',
    'M18,20 L19,21 L20,20',
    'M19,24 L19,30 L16,34 M19,30 L22,34',
    'M22,28 C24,26 28,24 30,26 C32,28 30,32 28,30',
  ],
  // Virgo — maiden holding wheat sheaf
  VIRGO: [
    'M19,6 A3.5,3.5 0 1,1 19,7',
    'M19,10 L19,22',
    'M19,22 L15,32 M19,22 L23,32',
    'M19,13 L14,18 L12,16 M19,13 L24,18',
    'M24,18 L28,14 M28,14 L30,12 M28,14 L30,16 M28,14 L26,12',
    'M17,18 C16,20 14,22 14,24',
    'M15,6 C16,4 18,3 19,3 C20,3 22,4 23,6',
  ],
  // Libra — balance scales with pillar
  LIBRA: [
    'M19,10 L19,28',
    'M14,28 L24,28',
    'M10,10 L28,10',
    'M10,10 L8,14 L14,14 L10,10',
    'M28,10 L26,14 L32,14 L28,10',
    'M19,10 L19,6 M17,6 L21,6',
    'M8,14 L8,16 C8,17 10,18 11,17 L14,16 L14,14',
    'M26,14 L26,16 C26,17 28,18 29,17 L32,16 L32,14',
  ],
  // Scorpio — scorpion with curved stinger tail
  SCORPIO: [
    'M10,18 C8,16 8,12 12,12 C16,12 18,14 18,18 C18,14 20,12 24,12 C28,12 30,14 30,18',
    'M30,18 C32,20 34,24 32,28 C30,32 26,34 24,30 L26,28 M24,30 L22,28',
    'M10,18 L8,24 M14,20 L12,26 M18,20 L16,26 M22,20 L20,26',
    'M12,14 A1,1 0 1,0 12,15',
    'M24,14 A1,1 0 1,0 24,15',
    'M10,12 L8,8 C7,6 6,8 8,10 M16,12 L14,8 C13,6 12,8 14,10',
  ],
  // Sagittarius — centaur archer drawing a bow
  SAGITTARIUS: [
    'M22,6 A3,3 0 1,1 22,7',
    'M22,10 L22,18 L18,24 L16,30 M18,24 L22,24 L26,30',
    'M22,12 L16,14 L10,10 M10,10 L8,6',
    'M10,10 L14,8',
    'M8,6 L6,4 M8,6 L10,4 M8,6 L6,8',
    'M22,14 L28,12',
    'M14,20 C12,18 10,20 12,22',
  ],
  // Capricorn is already defined above, we use the sea-goat
  // Aquarius is defined above
  // Pisces is defined above
};

const gold = '#B8862E';
const goldMed = 'rgba(184,134,55,0.65)';
const goldFaint = 'rgba(184,134,55,0.3)';

export default function ZodiacWheel() {
  const { language } = useTranslation();
  const cx = 200;
  const cy = 200;

  /* Ring radii — from outside in:
     outerR → monthR → artRingOuter → nameR → glyphR → artRingInner → coreR */
  const outerR = 195;
  const monthR = 183;      // month text
  const artRingOuter = 170; // divider ring
  const artR = 142;         // animal illustration center
  const nameR = 112;        // sign name text
  const nameRingR = 100;    // divider ring
  const glyphR = 82;        // glyph center
  const innerRingR = 65;    // inner ring
  const coreR = 45;         // sun area

  // Tick marks
  const ticks: JSX.Element[] = [];
  for (let i = 0; i < 360; i += 3) {
    const a = (i * Math.PI) / 180;
    const r1 = outerR;
    const isMajor = i % 30 === 0;
    const isMid = i % 15 === 0;
    const r2 = isMajor ? outerR - 8 : isMid ? outerR - 5 : outerR - 3;
    ticks.push(
      <line key={`t${i}`}
        x1={cx + r1 * Math.cos(a)} y1={cy + r1 * Math.sin(a)}
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

    // Divider lines from inner ring to outer
    const lx1 = cx + innerRingR * Math.cos(startRad);
    const ly1 = cy + innerRingR * Math.sin(startRad);
    const lx2 = cx + artRingOuter * Math.cos(startRad);
    const ly2 = cy + artRingOuter * Math.sin(startRad);

    // Month text (outer ring) — rotated along circle
    const mx = cx + monthR * Math.cos(midRad);
    const my = cy + monthR * Math.sin(midRad);
    const mFlip = midDeg > 90 && midDeg < 270;
    const mRot = mFlip ? midDeg + 180 : midDeg;

    // Animal art position
    const ax = cx + artR * Math.cos(midRad);
    const ay = cy + artR * Math.sin(midRad);

    // Sign name text
    const nx = cx + nameR * Math.cos(midRad);
    const ny = cy + nameR * Math.sin(midRad);
    const nFlip = midDeg > 90 && midDeg < 270;
    const nRot = nFlip ? midDeg + 180 : midDeg;

    // Glyph position
    const gx = cx + glyphR * Math.cos(midRad);
    const gy = cy + glyphR * Math.sin(midRad);

    const signName = language === 'hi' ? sign.hi : sign.en;
    const monthName = language === 'hi' ? sign.monthHi : sign.monthEn;
    const nameFontSize = language === 'hi' ? 7.5 : (signName.length > 9 ? 5 : 6);
    const artPaths = ART[sign.en] || [];

    return (
      <g key={sign.en}>
        {/* Divider line */}
        <line x1={lx1} y1={ly1} x2={lx2} y2={ly2} stroke={goldMed} strokeWidth={0.8} />

        {/* Month name — outer */}
        <text x={mx} y={my}
          textAnchor="middle" dominantBaseline="central"
          fill={gold} fontSize="9" fontWeight="800" letterSpacing="0.5"
          fontFamily="'Inter', sans-serif"
          transform={`rotate(${mRot},${mx},${my})`}
        >{monthName}</text>

        {/* Animal illustration */}
        <g transform={`translate(${ax - 19},${ay - 19}) scale(1)`}>
          {artPaths.map((d, j) => (
            <path key={j} d={d}
              fill="none" stroke={gold} strokeWidth={1.2}
              strokeLinecap="round" strokeLinejoin="round"
            />
          ))}
        </g>

        {/* Sign name */}
        <text x={nx} y={ny}
          textAnchor="middle" dominantBaseline="central"
          fill={gold} fontSize={nameFontSize} fontWeight="700" letterSpacing="0.3"
          fontFamily="'Inter', sans-serif"
          transform={`rotate(${nRot},${nx},${ny})`}
        >{signName}</text>

        {/* Glyph symbol */}
        <text x={gx} y={gy}
          textAnchor="middle" dominantBaseline="central"
          fill={gold} fontSize="14" fontWeight="bold"
          fontFamily="'Segoe UI Symbol', 'Noto Sans Symbols 2', serif"
          style={{ filter: 'drop-shadow(0 0 2px rgba(184,134,55,0.4))' }}
        >{sign.glyph}</text>
      </g>
    );
  });

  // Sun rays
  const sunRays: JSX.Element[] = [];
  for (let i = 0; i < 32; i++) {
    const a = (i * 11.25 * Math.PI) / 180;
    const long = i % 2 === 0;
    const r1 = long ? coreR - 3 : coreR - 8;
    const r2 = 12;
    sunRays.push(
      <line key={`sr${i}`}
        x1={cx + r2 * Math.cos(a)} y1={cy + r2 * Math.sin(a)}
        x2={cx + r1 * Math.cos(a)} y2={cy + r1 * Math.sin(a)}
        stroke={long ? gold : goldMed}
        strokeWidth={long ? 1.5 : 0.7}
      />
    );
  }

  return (
    <div className="relative w-full max-w-[440px] mx-auto" style={{ perspective: '900px' }}>
      <div className="absolute inset-[-10%] rounded-full bg-sacred-gold/5 blur-3xl" />
      <div style={{ transform: 'rotateX(12deg)', transformStyle: 'preserve-3d' }}>
        <svg
          viewBox="0 0 400 400"
          className="w-full h-full animate-spin-slow"
          style={{ filter: 'drop-shadow(0 0 24px rgba(184,134,55,0.15))' }}
        >
          {/* Rings — outside in */}
          <circle cx={cx} cy={cy} r={outerR} fill="none" stroke={gold} strokeWidth={2.5} />
          {ticks}
          <circle cx={cx} cy={cy} r={artRingOuter} fill="none" stroke={gold} strokeWidth={1.2} />
          <circle cx={cx} cy={cy} r={nameRingR} fill="none" stroke={goldFaint} strokeWidth={0.8} />
          <circle cx={cx} cy={cy} r={innerRingR} fill="none" stroke={gold} strokeWidth={1.2} />
          <circle cx={cx} cy={cy} r={coreR} fill="none" stroke={gold} strokeWidth={1.5} />

          {segments}

          {/* Central sun */}
          {sunRays}
          <circle cx={cx} cy={cy} r={10} fill={gold} opacity={0.8} />
          <circle cx={cx} cy={cy} r={6} fill="white" opacity={0.3} />
        </svg>
      </div>
    </div>
  );
}
