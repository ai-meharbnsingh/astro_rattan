import { useMemo } from 'react';
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

export default function ConcentricChart({ natalPlanets, transitPlanets, size = 500 }: Props) {
  const { language } = useTranslation();
  
  const radius = size / 2;
  const outerRing = radius - 20;
  const transitRing = radius - 60;
  const natalRing = radius - 110;
  const innerCircle = radius - 150;

  const polarToCartesian = (centerX: number, centerY: number, radius: number, angleInDegrees: number) => {
    const angleInRadians = (angleInDegrees - 90) * Math.PI / 180.0;
    return {
      x: centerX + (radius * Math.cos(angleInRadians)),
      y: centerY + (radius * Math.sin(angleInRadians))
    };
  };

  const describeArc = (x: number, y: number, radius: number, startAngle: number, endAngle: number) => {
    const start = polarToCartesian(x, y, radius, endAngle);
    const end = polarToCartesian(x, y, radius, startAngle);
    const largeArcFlag = endAngle - startAngle <= 180 ? "0" : "1";
    return [
      "M", start.x, start.y, 
      "A", radius, radius, 0, largeArcFlag, 0, end.x, end.y,
      "L", x, y,
      "Z"
    ].join(" ");
  };

  return (
    <div className="w-full max-w-xl mx-auto bg-white rounded-2xl shadow-xl border border-sacred-gold p-4">
      <svg viewBox={`0 0 ${size} ${size}`} className="w-full h-auto font-sans">
        {/* Zodiac Outer Ring */}
        {ZODIAC_SIGNS.map((sign, i) => {
          const startAngle = i * 30;
          const endAngle = (i + 1) * 30;
          const labelPos = polarToCartesian(radius, radius, outerRing + 10, startAngle + 15);
          
          return (
            <g key={sign}>
              <path 
                d={describeArc(radius, radius, outerRing, startAngle, endAngle)} 
                fill={SIGN_COLORS[i]} 
                stroke="#3D2B1F" 
                strokeWidth="0.5"
                opacity="0.3"
              />
              <text 
                x={labelPos.x} 
                y={labelPos.y} 
                textAnchor="middle" 
                fontSize="10" 
                fill="#8B7355" 
                fontWeight="bold"
                transform={`rotate(${startAngle + 15}, ${labelPos.x}, ${labelPos.y})`}
              >
                {sign.slice(0, 3)}
              </text>
            </g>
          );
        })}

        {/* Ring Dividers */}
        <circle cx={radius} cy={radius} r={outerRing} fill="none" stroke="#3D2B1F" strokeWidth="1" />
        <circle cx={radius} cy={radius} r={transitRing} fill="none" stroke="#3D2B1F" strokeWidth="0.5" strokeDasharray="4,4" />
        <circle cx={radius} cy={radius} r={natalRing} fill="none" stroke="#3D2B1F" strokeWidth="1" />
        <circle cx={radius} cy={radius} r={innerCircle} fill="#FDF6E3" stroke="#3D2B1F" strokeWidth="1" />

        {/* Labels for Rings */}
        <text x={radius} y={radius - 125} textAnchor="middle" fontSize="10" fill="#8B7355" fontWeight="bold" opacity="0.5">TRANSIT</text>
        <text x={radius} y={radius - 85} textAnchor="middle" fontSize="10" fill="#8B7355" fontWeight="bold" opacity="0.5">NATAL</text>

        {/* Transit Planets (Middle Ring) */}
        {transitPlanets.map((p, i) => {
          const pos = polarToCartesian(radius, radius, transitRing + 20, p.longitude);
          return (
            <g key={`tr-${p.planet}`}>
              <circle cx={pos.x} cy={pos.y} r="12" fill="white" stroke="#D4AF37" strokeWidth="1" shadow-sm="true" />
              <text x={pos.x} y={pos.y + 4} textAnchor="middle" fontSize="10" fontWeight="bold" fill="#3D2B1F">
                {translatePlanetAbbr(p.planet, language)}
              </text>
              {p.is_retrograde && (
                <text x={pos.x + 8} y={pos.y - 6} fontSize="8" fill="#EF4444" fontWeight="bold">R</text>
              )}
            </g>
          );
        })}

        {/* Natal Planets (Inner Ring) */}
        {natalPlanets.map((p, i) => {
          const pos = polarToCartesian(radius, radius, natalRing + 25, p.longitude);
          return (
            <g key={`nt-${p.planet}`}>
              <circle cx={pos.x} cy={pos.y} r="14" fill="#3D2B1F" />
              <text x={pos.x} y={pos.y + 5} textAnchor="middle" fontSize="11" fontWeight="bold" fill="#D4AF37">
                {translatePlanetAbbr(p.planet, language)}
              </text>
            </g>
          );
        })}

        {/* Center Logo/Symbol */}
        <circle cx={radius} cy={radius} r="20" fill="white" stroke="#D4AF37" strokeWidth="2" />
        <text x={radius} y={radius + 5} textAnchor="middle" fontSize="12" fontWeight="bold" fill="#D4AF37">ॐ</text>
      </svg>
      
      <div className="flex justify-center gap-6 mt-4 border-t border-sacred-gold/10 pt-4">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-[#3D2B1F]" />
          <span className="text-xs font-bold text-cosmic-text/60">NATAL</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-white border border-sacred-gold" />
          <span className="text-xs font-bold text-cosmic-text/60">TRANSIT</span>
        </div>
      </div>
    </div>
  );
}
