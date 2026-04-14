import { useTranslation } from '@/lib/i18n';

const SIGNS = [
  { en: 'Aries',       hi: 'मेष',     symbol: '\u2648' },
  { en: 'Taurus',      hi: 'वृषभ',    symbol: '\u2649' },
  { en: 'Gemini',      hi: 'मिथुन',   symbol: '\u264A' },
  { en: 'Cancer',      hi: 'कर्क',    symbol: '\u264B' },
  { en: 'Leo',         hi: 'सिंह',    symbol: '\u264C' },
  { en: 'Virgo',       hi: 'कन्या',   symbol: '\u264D' },
  { en: 'Libra',       hi: 'तुला',    symbol: '\u264E' },
  { en: 'Scorpio',     hi: 'वृश्चिक', symbol: '\u264F' },
  { en: 'Sagittarius', hi: 'धनु',     symbol: '\u2650' },
  { en: 'Capricorn',   hi: 'मकर',     symbol: '\u2651' },
  { en: 'Aquarius',    hi: 'कुंभ',    symbol: '\u2652' },
  { en: 'Pisces',      hi: 'मीन',     symbol: '\u2653' },
];

export default function ZodiacWheel() {
  const { language } = useTranslation();
  const cx = 200;
  const cy = 200;
  const outerR = 190;
  const midR = 155;
  const innerR = 110;
  const coreR = 65;

  // Tick marks on outer edge
  const ticks: JSX.Element[] = [];
  for (let i = 0; i < 72; i++) {
    const angle = (i * 5 * Math.PI) / 180;
    const r1 = outerR - 2;
    const r2 = i % 6 === 0 ? outerR - 10 : outerR - 6;
    ticks.push(
      <line
        key={`t${i}`}
        x1={cx + r1 * Math.cos(angle)}
        y1={cy + r1 * Math.sin(angle)}
        x2={cx + r2 * Math.cos(angle)}
        y2={cy + r2 * Math.sin(angle)}
        stroke="rgba(184,134,55,0.4)"
        strokeWidth={i % 6 === 0 ? 1.2 : 0.6}
      />
    );
  }

  // Sign segments: symbols + names
  const segments = SIGNS.map((sign, i) => {
    const startAngle = (i * 30 - 90) * (Math.PI / 180);
    const midAngle = ((i * 30 + 15) - 90) * (Math.PI / 180);

    // Symbol position (between mid and inner rings)
    const symbolR = (midR + innerR) / 2 + 2;
    const sx = cx + symbolR * Math.cos(midAngle);
    const sy = cy + symbolR * Math.sin(midAngle);

    // Name position (between outer and mid rings)
    const nameR = (outerR + midR) / 2 - 2;
    const nx = cx + nameR * Math.cos(midAngle);
    const ny = cy + nameR * Math.sin(midAngle);

    // Divider line from inner to outer
    const x1 = cx + innerR * Math.cos(startAngle);
    const y1 = cy + innerR * Math.sin(startAngle);
    const x2 = cx + outerR * Math.cos(startAngle);
    const y2 = cy + outerR * Math.sin(startAngle);

    const nameRotation = (i * 30 + 15 - 90);
    // Flip text that would appear upside down
    const flipText = nameRotation > 90 && nameRotation < 270;
    const textRotation = flipText ? nameRotation + 180 : nameRotation;

    return (
      <g key={sign.en}>
        <line x1={x1} y1={y1} x2={x2} y2={y2} stroke="rgba(184,134,55,0.35)" strokeWidth={0.8} />
        {/* Symbol */}
        <text
          x={sx} y={sy}
          textAnchor="middle" dominantBaseline="central"
          fill="#B8862E"
          fontSize="22"
          fontWeight="bold"
          style={{ filter: 'drop-shadow(0 0 4px rgba(184,134,55,0.5))' }}
        >
          {sign.symbol}
        </text>
        {/* Name — counter-rotated so always readable */}
        <text
          x={nx} y={ny}
          textAnchor="middle" dominantBaseline="central"
          fill="rgba(184,134,55,0.85)"
          fontSize={language === 'hi' ? '8' : '7.5'}
          fontWeight="600"
          letterSpacing="0.5"
          transform={`rotate(${textRotation},${nx},${ny})`}
        >
          {language === 'hi' ? sign.hi : sign.en.toUpperCase()}
        </text>
      </g>
    );
  });

  // Central mandala star (8-pointed)
  const starPoints = (points: number, outerStar: number, innerStar: number) => {
    const pts: string[] = [];
    for (let i = 0; i < points * 2; i++) {
      const angle = (i * Math.PI) / points - Math.PI / 2;
      const r = i % 2 === 0 ? outerStar : innerStar;
      pts.push(`${cx + r * Math.cos(angle)},${cy + r * Math.sin(angle)}`);
    }
    return pts.join(' ');
  };

  return (
    <div
      className="relative w-full max-w-[420px] mx-auto"
      style={{ perspective: '800px' }}
    >
      {/* Glow background */}
      <div className="absolute inset-0 rounded-full bg-sacred-gold/10 blur-3xl scale-110" />

      {/* 3D tilt container */}
      <div
        style={{ transform: 'rotateX(12deg) rotateZ(-2deg)', transformStyle: 'preserve-3d' }}
      >
        <svg
          viewBox="0 0 400 400"
          className="w-full h-full animate-spin-slow drop-shadow-[0_0_30px_rgba(184,134,55,0.25)]"
          style={{ animationDuration: '60s', animationDirection: 'normal' }}
        >
          {/* Outer ring */}
          <circle cx={cx} cy={cy} r={outerR} fill="none" stroke="rgba(184,134,55,0.3)" strokeWidth={1.5} />
          <circle cx={cx} cy={cy} r={outerR - 1} fill="none" stroke="rgba(184,134,55,0.15)" strokeWidth={0.5} />

          {/* Tick marks */}
          {ticks}

          {/* Middle ring */}
          <circle cx={cx} cy={cy} r={midR} fill="none" stroke="rgba(184,134,55,0.25)" strokeWidth={0.8} />

          {/* Inner ring */}
          <circle cx={cx} cy={cy} r={innerR} fill="none" stroke="rgba(184,134,55,0.3)" strokeWidth={1} />

          {/* Core circle */}
          <circle cx={cx} cy={cy} r={coreR} fill="none" stroke="rgba(184,134,55,0.25)" strokeWidth={0.8} />

          {/* Segments — symbols & names */}
          {segments}

          {/* Central mandala: 8-pointed star */}
          <polygon
            points={starPoints(8, coreR - 5, coreR * 0.4)}
            fill="none"
            stroke="rgba(184,134,55,0.4)"
            strokeWidth={1}
          />
          <polygon
            points={starPoints(8, coreR * 0.55, coreR * 0.25)}
            fill="none"
            stroke="rgba(184,134,55,0.3)"
            strokeWidth={0.8}
          />

          {/* Center dot cluster */}
          <circle cx={cx} cy={cy} r={4} fill="rgba(184,134,55,0.5)" />
          <circle cx={cx} cy={cy} r={8} fill="none" stroke="rgba(184,134,55,0.25)" strokeWidth={0.6} />
          {[0, 45, 90, 135, 180, 225, 270, 315].map((deg) => {
            const a = (deg * Math.PI) / 180;
            return (
              <circle
                key={deg}
                cx={cx + 18 * Math.cos(a)}
                cy={cy + 18 * Math.sin(a)}
                r={2}
                fill="rgba(184,134,55,0.35)"
              />
            );
          })}

          {/* Decorative inner lines — cross pattern */}
          {[0, 45, 90, 135].map((deg) => {
            const a = (deg * Math.PI) / 180;
            return (
              <line
                key={`cl${deg}`}
                x1={cx + coreR * Math.cos(a)}
                y1={cy + coreR * Math.sin(a)}
                x2={cx - coreR * Math.cos(a)}
                y2={cy - coreR * Math.sin(a)}
                stroke="rgba(184,134,55,0.15)"
                strokeWidth={0.5}
              />
            );
          })}
        </svg>
      </div>
    </div>
  );
}
