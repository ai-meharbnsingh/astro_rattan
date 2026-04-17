import { useTranslation } from '@/lib/i18n';
import { translatePlanetAbbr } from '@/lib/backend-translations';

interface PlanetPos {
  planet: string;
  sign: string;
  longitude: number;
  is_retrograde?: boolean;
}

interface Props {
  natalPlanets: PlanetPos[];
  transitPlanets: PlanetPos[];
  lagnaLongitude: number;
  size?: number;
}

const ZODIAC_SIGNS = [
  'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
  'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
];

const SIGN_COLORS = [
  '#FEE2E2', '#FEF3C7', '#D1FAE5', '#DBEAFE', '#F3E8FF', '#FCE7F3',
  '#FEE2E2', '#FEF3C7', '#D1FAE5', '#DBEAFE', '#F3E8FF', '#FCE7F3'
];

export default function ConcentricChart({ natalPlanets, transitPlanets, lagnaLongitude, size = 400 }: Props) {
  const { t, language } = useTranslation();

  const radius = size / 2;
  const outerRing = radius - 15;
  const transitRing = radius - 45;
  const natalRing = radius - 85;
  const innerCircle = radius - 120;

  // Rotation offset to put Lagna at 180 deg (9 o'clock)
  // Direction: Counter-Clockwise
  const getAngle = (lon: number) => {
    // 1. Degrees from Aries 0
    // 2. Adjust for Lagna-at-Left (180 deg)
    // 3. Subtract from 180 because SVG Y is down (so positive angle is clockwise)
    //    but we want counter-clockwise.
    const deg = (lon - lagnaLongitude + 360) % 360;
    return 180 - deg;
  };

  const polarToCartesian = (centerX: number, centerY: number, radius: number, angleInDegrees: number) => {
    const angleInRadians = angleInDegrees * Math.PI / 180.0;
    return {
      x: centerX + (radius * Math.cos(angleInRadians)),
      y: centerY + (radius * Math.sin(angleInRadians))
    };
  };

  const describeArc = (x: number, y: number, radius: number, startAngle: number, endAngle: number) => {
    const start = polarToCartesian(x, y, radius, endAngle);
    const end = polarToCartesian(x, y, radius, startAngle);
    // For CCW, we flip the sweep flag
    return [
      "M", start.x, start.y, 
      "A", radius, radius, 0, 0, 1, end.x, end.y,
      "L", x, y,
      "Z"
    ].join(" ");
  };

  return (
    <div className="w-full max-w-lg mx-auto bg-white rounded-2xl shadow-lg border border-border p-3">
      <svg viewBox={`0 0 ${size} ${size}`} className="w-full h-auto font-sans">
        {/* Zodiac Ring with Correct Rotation */}
        {ZODIAC_SIGNS.map((sign, i) => {
          const startLon = i * 30;
          const endLon = (i + 1) * 30;
          const startAngle = getAngle(startLon);
          const endAngle = getAngle(endLon);
          
          // Labels positions (mid-sign)
          const labelPos = polarToCartesian(radius, radius, outerRing + 10, getAngle(startLon + 15));
          
          return (
            <g key={sign}>
              <path 
                d={describeArc(radius, radius, outerRing, startAngle, endAngle)} 
                fill={SIGN_COLORS[i]} 
                stroke="#3D2B1F" 
                strokeWidth="0.5"
                opacity="0.2"
              />
              <text 
                x={labelPos.x} 
                y={labelPos.y} 
                textAnchor="middle" 
                fontSize="8" 
                fill="#8B7355" 
                fontWeight="bold"
                transform={`rotate(${90 - getAngle(startLon + 15)}, ${labelPos.x}, ${labelPos.y})`}
              >
                {sign.slice(0, 3)}
              </text>
            </g>
          );
        })}

        {/* Ring Dividers */}
        <circle cx={radius} cy={radius} r={outerRing} fill="none" stroke="#3D2B1F" strokeWidth="1" />
        <circle cx={radius} cy={radius} r={transitRing} fill="none" stroke="#3D2B1F" strokeWidth="0.5" strokeDasharray="4,2" />
        <circle cx={radius} cy={radius} r={natalRing} fill="none" stroke="#3D2B1F" strokeWidth="1" />
        <circle cx={radius} cy={radius} r={innerCircle} fill="#FDF6E3" stroke="#3D2B1F" strokeWidth="1" />

        {/* House Division Lines (Every 30 deg starting from Lagna at 180) */}
        {Array.from({ length: 12 }).map((_, i) => {
          const angle = 180 - (i * 30);
          const p1 = polarToCartesian(radius, radius, innerCircle, angle);
          const p2 = polarToCartesian(radius, radius, outerRing, angle);
          const isLagna = i === 0;
          return (
            <g key={`h-${i}`}>
              <line 
                x1={p1.x} y1={p1.y} x2={p2.x} y2={p2.y} 
                stroke={isLagna ? "#D4AF37" : "#3D2B1F"} 
                strokeWidth={isLagna ? 2 : 0.5} 
                opacity={isLagna ? 1 : 0.3} 
              />
              {isLagna && <text x={p2.x - 15} y={p2.y} fontSize="8" fontWeight="black" fill="#D4AF37">ASC</text>}
            </g>
          );
        })}

        {/* Transit Planets (Middle Ring) */}
        {transitPlanets.map((p, _i) => {
          const angle = getAngle(p.longitude);
          const pos = polarToCartesian(radius, radius, transitRing + 15, angle);
          return (
            <g key={`tr-${p.planet}`}>
              <circle cx={pos.x} cy={pos.y} r="10" fill="white" stroke="#D4AF37" strokeWidth="1" />
              <text x={pos.x} y={pos.y + 3} textAnchor="middle" fontSize="9" fontWeight="bold" fill="#3D2B1F">
                {translatePlanetAbbr(p.planet, language)}
              </text>
              {p.is_retrograde && (
                <text x={pos.x + 6} y={pos.y - 5} fontSize="7" fill="#EF4444" fontWeight="bold">R</text>
              )}
            </g>
          );
        })}

        {/* Natal Planets (Inner Ring) */}
        {natalPlanets.map((p, _i) => {
          const angle = getAngle(p.longitude);
          const pos = polarToCartesian(radius, radius, natalRing + 18, angle);
          return (
            <g key={`nt-${p.planet}`}>
              <circle cx={pos.x} cy={pos.y} r="12" fill="#3D2B1F" />
              <text x={pos.x} y={pos.y + 4} textAnchor="middle" fontSize="10" fontWeight="bold" fill="#D4AF37">
                {translatePlanetAbbr(p.planet, language)}
              </text>
            </g>
          );
        })}

        {/* Center Logo/Symbol */}
        <circle cx={radius} cy={radius} r="15" fill="white" stroke="#D4AF37" strokeWidth="2" />
        <text x={radius} y={radius + 4} textAnchor="middle" fontSize="10" fontWeight="bold" fill="#D4AF37">ॐ</text>
      </svg>
      
      <div className="flex justify-center gap-6 mt-3 border-t border-border/10 pt-3">
        <div className="flex items-center gap-2">
          <div className="w-2.5 h-2.5 rounded-full bg-[#3D2B1F]" />
          <span className="text-[10px] font-bold text-foreground/60 uppercase">{t('auto.natal')}</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-2.5 h-2.5 rounded-full bg-white border border-border" />
          <span className="text-[10px] font-bold text-foreground/60 uppercase">{t('auto.transit')}</span>
        </div>
      </div>
    </div>
  );
}
