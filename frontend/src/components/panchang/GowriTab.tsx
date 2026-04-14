import { useMemo } from 'react';
import { Moon, Sun, CheckCircle2, XCircle } from 'lucide-react';
import type { FullPanchangData } from '@/sections/Panchang';

interface Props {
  panchang: FullPanchangData;
  language: string;
  t: (key: string) => string;
  timezoneOffset: number;
}

export default function GowriTab({ panchang, language, t, timezoneOffset }: Props) {
  const gowriPanchang = panchang.gowri_panchang || [];
  const toMinutes = (time: string) => {
    const [h, m] = String(time || '').split(':').map(Number);
    if (Number.isNaN(h) || Number.isNaN(m)) return -1;
    return h * 60 + m;
  };
  const isInTimeRange = (current: number, start: string, end: string) => {
    const startM = toMinutes(start);
    const endM = toMinutes(end);
    if (startM < 0 || endM < 0 || startM === endM) return false;
    if (startM < endM) return current >= startM && current < endM;
    return current >= startM || current < endM;
  };

  // Memoize day/night separation and current gowri calculation
  const { dayGowri, nightGowri, currentGowri } = useMemo(() => {
    // Separate day and night gowri
    const day = gowriPanchang.filter(g => g.type === 'Day' || g.type === 'दिन');
    const night = gowriPanchang.filter(g => g.type === 'Night' || g.type === 'रात्रि');

    // Find current gowri period (based on panchang location time, not browser local time)
    const currentTimeAtLocation = new Date(Date.now() + ((timezoneOffset + new Date().getTimezoneOffset()) * 60 * 1000));
    const currentMinutes = currentTimeAtLocation.getHours() * 60 + currentTimeAtLocation.getMinutes();

    const current = gowriPanchang.find((g) => isInTimeRange(currentMinutes, g.start, g.end));

    return { dayGowri: day, nightGowri: night, currentGowri: current };
  }, [gowriPanchang, timezoneOffset]);

  const getQualityStyle = (quality: string) => {
    if (quality.toLowerCase().includes('good') || quality === 'शुभ') {
      return { color: 'text-green-500', bg: 'bg-green-500/10', icon: CheckCircle2 };
    }
    return { color: 'text-red-500', bg: 'bg-red-500/10', icon: XCircle };
  };

  const renderRow = (period: typeof gowriPanchang[0], index: number) => {
    const style = getQualityStyle(period.quality);
    const isCurrent = currentGowri?.start === period.start && currentGowri?.end === period.end && currentGowri?.type === period.type;

    return (
      <tr
        key={`${period.type}-${index}`}
        className={`border-b border-cosmic-border/50 last:border-0 ${isCurrent ? 'bg-amber-500/15 border-l-2 border-l-amber-500' : ''}`}
      >
        <td className="px-2 py-1">
          <span className={`font-medium ${isCurrent ? 'text-sacred-gold' : 'text-cosmic-text-primary'}`}>
            {language === 'hi' ? period.name_hindi || period.name : period.name}
          </span>
          {isCurrent && (
            <span className="ml-1 px-1.5 py-0.5 text-xs bg-sacred-gold text-cosmic-bg rounded-full">
              {language === 'hi' ? 'अभी' : 'Now'}
            </span>
          )}
        </td>
        <td className="px-2 py-1">
          <span className={`inline-block px-1.5 py-0.5 rounded text-xs font-medium ${style.bg} ${style.color}`}>
            {language === 'hi' ? period.quality_hindi || period.quality : period.quality}
          </span>
        </td>
        <td className="px-2 py-1 text-cosmic-text-secondary">
          {period.start} - {period.end}
        </td>
      </tr>
    );
  };

  const renderTable = (periods: typeof gowriPanchang, icon: typeof Sun, title: string) => (
    <div className="flex-1 min-w-0">
      <h3 className="font-bold text-cosmic-text-primary mb-1 flex items-center gap-1">
        {icon === Sun
          ? <Sun className="h-4 w-4 text-orange-500" />
          : <Moon className="h-4 w-4 text-indigo-400" />}
        {title}
      </h3>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="bg-sacred-gold/15">
              <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold">
                {language === 'hi' ? 'नाम' : 'Name'}
              </th>
              <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold">
                {language === 'hi' ? 'फल' : 'Quality'}
              </th>
              <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold">
                {language === 'hi' ? 'समय' : 'Time'}
              </th>
            </tr>
          </thead>
          <tbody>
            {periods.map((period, index) => renderRow(period, index))}
          </tbody>
        </table>
      </div>
    </div>
  );

  return (
    <div className="space-y-3">
      {/* Current Gowri compact banner */}
      {currentGowri && (
        <div className="flex items-center gap-3 p-2 rounded-lg border border-sacred-gold/30 bg-sacred-gold/10">
          <Moon className="h-8 w-8 text-sacred-gold flex-shrink-0" />
          <div className="flex-1 min-w-0">
            <p className="text-xs text-cosmic-text-secondary">
              {language === 'hi' ? 'वर्तमान गौरी पंचांग' : 'Current Gowri Panchang'}
            </p>
            <span className="font-bold text-cosmic-text-primary">
              {language === 'hi' ? currentGowri.name_hindi || currentGowri.name : currentGowri.name}
            </span>
            <span className="mx-2 text-sacred-gold">{currentGowri.start} - {currentGowri.end}</span>
            <span className={`text-xs font-medium ${getQualityStyle(currentGowri.quality).color}`}>
              ({language === 'hi' ? currentGowri.quality_hindi || currentGowri.quality : currentGowri.quality})
            </span>
          </div>
        </div>
      )}

      {/* Day + Night side by side (stack on mobile) */}
      <div className="rounded-lg border border-cosmic-border overflow-hidden">
        <div className="flex flex-col md:flex-row divide-y md:divide-y-0 md:divide-x divide-cosmic-border">
          {dayGowri.length > 0 && (
            <div className="p-2">
              {renderTable(dayGowri, Sun, language === 'hi' ? 'दिन का गौरी पंचांग' : 'Day Gowri Panchang')}
            </div>
          )}
          {nightGowri.length > 0 && (
            <div className="p-2">
              {renderTable(nightGowri, Moon, language === 'hi' ? 'रात्रि का गौरी पंचांग' : 'Night Gowri Panchang')}
            </div>
          )}
        </div>
      </div>

      {/* Info */}
      <div className="rounded-lg border border-cosmic-border p-2">
        <h4 className="font-semibold text-cosmic-text-primary mb-1">
          {language === 'hi' ? 'गौरी पंचांग के बारे में' : 'About Gowri Panchang'}
        </h4>
        <p className="text-sm text-cosmic-text-secondary leading-relaxed">
          {language === 'hi'
            ? 'गौरी पंचांग दिन और रात को 8-8 भागों में बांटता है। प्रत्येक अवधि एक देवता द्वारा शासित होती है। शुभ अवधि में कार्य करने से सफलता मिलती है।'
            : 'Gowri Panchang divides day and night into 8 periods each. Each period is ruled by a deity. Work done during auspicious periods yields success.'}
        </p>
      </div>
    </div>
  );
}
