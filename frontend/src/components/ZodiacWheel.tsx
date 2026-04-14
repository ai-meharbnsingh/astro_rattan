import { useTranslation } from '@/lib/i18n';

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

/* Detailed zodiac figures — each in a 38×38 viewBox, engraving style */
const ART: Record<string, string[]> = {
  CAPRICORN: [
    // Sea-goat: goat forebody + curling fish tail
    'M12,8 C10,6 8,6 8,9 C8,11 10,12 12,12 L14,11 C15,10 17,9 18,10',
    'M8,9 L6,7 M8,6 L7,4', // horns
    'M9,9 A0.8,0.8 0 1,0 9,10', // eye
    'M12,12 L11,16 L9,20 M14,11 L14,16 L12,20', // front legs
    'M18,10 C20,11 22,14 22,18 C22,22 20,26 16,28 C14,29 12,28 14,26 C16,24 20,24 22,26 C24,28 24,30 22,32',
    'M22,32 C21,34 23,34 24,32', // tail fin
    'M16,28 C14,30 16,32 18,30', // lower fin
  ],
  AQUARIUS: [
    // Water bearer: kneeling figure pouring from urn
    'M20,5 A3,3 0 1,1 20,6', // head
    'M18,9 L16,15 L14,15 M22,9 L20,15 L24,15', // torso + arms
    'M16,15 L14,22 L12,28', // left leg kneeling
    'M20,15 L22,20 L24,22 L26,28', // right leg
    'M14,15 L10,14 L8,12', // left arm to urn
    'M8,12 L6,10 C5,9 4,10 5,12 L7,14 L8,12', // urn
    'M7,14 C6,16 5,18 6,18 M5,18 C4,20 3,22 4,22 M4,22 C3,24 2,26 3,26', // water streams
    'M7,14 C8,16 7,18 8,18 M8,18 C9,20 8,22 9,22', // second stream
  ],
  PISCES: [
    // Two fish swimming in opposite directions, connected
    'M6,10 C3,8 2,12 4,14 C2,16 3,20 6,18 C9,16 10,14 6,10Z', // left fish
    'M6,10 L4,8 M6,18 L4,20', // tail fins
    'M5,12.5 A0.6,0.6 0 1,0 5,13.2', // eye
    'M32,20 C35,22 36,18 34,16 C36,14 35,10 32,12 C29,14 28,16 32,20Z', // right fish
    'M32,20 L34,22 M32,12 L34,10', // tail fins
    'M33,17.5 A0.6,0.6 0 1,0 33,18.2', // eye
    'M10,14 L14,14 C16,14 18,15 20,16 L24,16 L28,16', // connecting cord
  ],
  ARIES: [
    // Ram with large curled horns, woolly body
    'M18,10 C14,8 10,8 8,12 C6,16 10,18 14,16', // left horn curl
    'M20,10 C24,8 28,8 30,12 C32,16 28,18 24,16', // right horn curl
    'M14,16 L16,18 C17,20 18,22 19,22 C20,22 21,20 22,18 L24,16', // face
    'M16,16 A0.7,0.7 0 1,0 16,17', 'M22,16 A0.7,0.7 0 1,0 22,17', // eyes
    'M18,20 L19,21 L20,20', // nose
    'M19,22 L17,28 L15,34 M19,22 L21,28 L23,34', // front legs
    'M17,28 C16,26 12,24 12,28 L14,34 M21,28 C22,26 26,24 26,28 L24,34', // hind legs
    'M12,24 C10,22 8,24 10,26 C12,24 14,22 16,24', // wool texture
  ],
  TAURUS: [
    // Bull: strong body, head down, prominent horns
    'M14,10 C10,8 6,10 6,14 C6,18 10,20 14,20', // left body
    'M24,10 C28,8 32,10 32,14 C32,18 28,20 24,20', // right body
    'M14,20 C16,22 22,22 24,20', // chin
    'M6,10 L4,6 C3,4 2,6 4,8', // left horn
    'M32,10 L34,6 C35,4 36,6 34,8', // right horn
    'M12,14 A1.2,1.2 0 1,0 12,15', 'M26,14 A1.2,1.2 0 1,0 26,15', // eyes
    'M17,18 A1,0.5 0 1,0 17,19 M21,18 A1,0.5 0 1,0 21,19', // nostrils
    'M16,24 C17,26 21,26 22,24', // nose ring
    'M14,20 L12,26 L10,32 M14,20 L16,26 L14,32', // front legs
    'M24,20 L22,26 L24,32 M24,20 L26,26 L28,32', // hind legs
  ],
  GEMINI: [
    // Twins: two identical figures holding hands
    'M12,5 A2.5,2.5 0 1,1 12,6', 'M26,5 A2.5,2.5 0 1,1 26,6', // heads
    'M12,9 L12,20', 'M26,9 L26,20', // torsos
    'M12,20 L9,28 M12,20 L15,28', 'M26,20 L23,28 M26,20 L29,28', // legs
    'M12,12 L8,16', 'M26,12 L30,16', // outer arms
    'M12,12 L16,14 M26,12 L22,14', // inner arms meeting
    'M16,14 L19,15 L22,14', // hands held
    'M10,5 C11,3 13,3 14,5', 'M24,5 C25,3 27,3 28,5', // hair
    'M12,9 C14,8 16,9 16,10', 'M26,9 C24,8 22,9 22,10', // shoulders
  ],
  CANCER: [
    // Crab: round body, two large pincers, legs
    'M12,16 C8,12 6,16 8,20 C10,24 16,26 19,26 C22,26 28,24 30,20 C32,16 30,12 26,16', // shell
    'M12,16 L8,10 L6,8 M6,8 L4,6 L6,6 M6,8 L4,10 L6,10', // left claw
    'M26,16 L30,10 L32,8 M32,8 L34,6 L32,6 M32,8 L34,10 L32,10', // right claw
    'M10,22 L8,26 M14,24 L12,28 M24,24 L26,28 M28,22 L30,26', // legs
    'M16,18 A1,1 0 1,0 16,19', 'M22,18 A1,1 0 1,0 22,19', // eyes
    'M18,22 C19,23 20,22 19,21', // mouth
  ],
  LEO: [
    // Lion: large mane, proud stance, tail curled up
    'M16,8 C10,6 6,10 6,16 C6,20 10,22 14,20', // mane left
    'M22,8 C28,6 32,10 32,16 C32,20 28,22 24,20', // mane right
    'M14,20 C14,16 16,14 19,14 C22,14 24,16 24,20 C24,22 22,24 19,24 C16,24 14,22 14,20', // face
    'M16,8 C18,6 20,6 22,8', // top of mane
    'M16,18 A0.8,0.8 0 1,0 16,19', 'M22,18 A0.8,0.8 0 1,0 22,19', // eyes
    'M18,21 L19,22 L20,21', // nose
    'M17,23 C18,24 20,24 21,23', // mouth
    'M19,24 L17,30 L15,36 M19,24 L21,30 L23,36', // front legs
    'M15,30 C12,28 8,28 8,32 L12,36', // hind body + leg
    'M8,28 C6,26 4,24 2,22 C0,20 2,18 4,20 C6,22 4,24 2,26', // tail curl
  ],
  VIRGO: [
    // Maiden holding wheat sheaf, flowing dress
    'M19,4 A3,3 0 1,1 19,5', // head
    'M17,4 C18,2 20,2 21,4', // hair top
    'M16,4 C14,6 14,8 16,7', // hair left
    'M22,4 C24,6 24,8 22,7', // hair right
    'M19,8 L19,18', // torso
    'M19,18 C16,22 14,28 12,34', // dress left
    'M19,18 C22,22 24,28 26,34', // dress right
    'M12,34 C16,34 22,34 26,34', // dress hem
    'M19,11 L14,16 L12,14', // left arm
    'M19,11 L24,14 L28,10', // right arm holding sheaf
    'M28,10 L30,6 M28,10 L26,6 M28,10 L28,6', // wheat sheaf
    'M30,6 L31,4 M26,6 L25,4 M28,6 L28,3', // wheat tips
  ],
  LIBRA: [
    // Balance scales: ornate pillar with two hanging pans
    'M19,6 L19,26', // central pillar
    'M15,26 L23,26', // base
    'M17,26 L17,28 L21,28 L21,26', // base detail
    'M8,8 L30,8', // beam
    'M19,6 L19,4 C18,3 20,3 19,4', // top ornament
    'M8,8 L6,12 L12,12 L8,8', // left pan triangle
    'M6,12 C6,14 8,15 9,14 L12,14 C12,14 14,13 12,12', // left pan
    'M30,8 L28,12 L34,12 L30,8', // right pan triangle
    'M28,12 C28,14 30,15 31,14 L34,14 C34,14 36,13 34,12', // right pan
    'M8,8 L8,6 M30,8 L30,6', // suspension cords
  ],
  SCORPIO: [
    // Scorpion: segmented body, pincers, curved stinger tail
    'M10,16 C8,14 6,14 6,16 C6,18 8,20 10,20', // left pincer
    'M6,14 L4,12 L2,10 M2,10 L0,9 M2,10 L2,8', // left claw
    'M28,16 C30,14 32,14 32,16 C32,18 30,20 28,20', // right pincer
    'M32,14 L34,12 L36,10 M36,10 L38,9 M36,10 L36,8', // right claw
    'M10,18 L14,18 L18,18 L22,18 L26,18 L28,18', // body segments
    'M10,16 L10,20 M14,16 L14,20 M18,16 L18,20 M22,16 L22,20 M26,16 L26,20', // segment lines
    'M28,18 C30,16 32,12 30,8 C28,4 26,4 26,6', // tail curving up
    'M26,6 L24,4 M26,6 L28,4', // stinger
    'M12,22 L10,26 M16,22 L14,26 M20,22 L18,26 M24,22 L22,26', // legs
  ],
  SAGITTARIUS: [
    // Centaur archer: human torso on horse body, drawing bow
    'M22,4 A2.5,2.5 0 1,1 22,5', // head
    'M22,8 L22,16', // human torso
    'M22,10 L16,14 L10,10', // left arm drawing bow
    'M22,10 L28,8', // right arm
    'M10,10 L8,6', // arrow
    'M8,6 L6,4 M8,6 L10,4 M8,6 L6,8', // arrowhead
    'M10,10 C8,12 8,16 10,14 C12,12 14,14 10,10', // bow curve
    'M22,16 L18,20 L14,24 L10,30', // front horse legs
    'M22,16 L26,20 L30,24 L34,30', // hind horse legs
    'M18,20 C16,18 14,20 16,22', // front knee
    'M26,20 C28,18 30,20 28,22', // hind body
    'M30,24 C32,22 34,20 36,22 C38,24 36,26 34,24', // tail
  ],
};

const gold = '#B8862E';
const goldMed = 'rgba(184,134,55,0.6)';
const goldFaint = 'rgba(184,134,55,0.3)';

/**
 * Compute rotation so text runs tangent to the circle (along the arc),
 * flipped on the bottom half so it's always readable from outside.
 */
function arcTextRotation(midDeg: number): number {
  const tangent = ((midDeg + 90) % 360 + 360) % 360;
  const flip = tangent > 90 && tangent < 270;
  return flip ? tangent + 180 : tangent;
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

    // Month text — along the arc
    const mx = cx + monthR * Math.cos(midRad);
    const my = cy + monthR * Math.sin(midRad);
    const mRot = arcTextRotation(midDeg);

    // Art center
    const ax = cx + artR * Math.cos(midRad);
    const ay = cy + artR * Math.sin(midRad);

    // Sign name — along the arc
    const nx = cx + nameR * Math.cos(midRad);
    const ny = cy + nameR * Math.sin(midRad);
    const nRot = arcTextRotation(midDeg);

    // Glyph
    const gx = cx + glyphR * Math.cos(midRad);
    const gy = cy + glyphR * Math.sin(midRad);

    const signName = language === 'hi' ? sign.hi : sign.en;
    const monthName = language === 'hi' ? sign.monthHi : sign.monthEn;
    const nameFontSize = language === 'hi' ? 7.5 : (signName.length > 9 ? 5 : 6);
    const artPaths = ART[sign.en] || [];

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

        {/* Zodiac illustration */}
        <g transform={`translate(${ax - 19},${ay - 19}) scale(1)`}>
          {artPaths.map((d, j) => (
            <path key={j} d={d}
              fill="none" stroke={gold} strokeWidth={1.1}
              strokeLinecap="round" strokeLinejoin="round"
            />
          ))}
        </g>

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
      <div style={{ transform: 'rotateX(12deg)', transformStyle: 'preserve-3d' }}>
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
