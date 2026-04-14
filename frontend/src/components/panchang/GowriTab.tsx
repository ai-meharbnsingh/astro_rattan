import { useMemo } from 'react';
import { Moon, Sun, Clock } from 'lucide-react';
import type { FullPanchangData } from '@/sections/Panchang';

interface Props {
  panchang: FullPanchangData;
  language: string;
  t: (key: string) => string;
  timezoneOffset: number;
  minuteTick: number;
}

type GowriPeriod = {
  type: string;
  name: string;
  name_hindi?: string;
  quality: string;
  quality_hindi?: string;
  start: string;
  end: string;
};

const GOWRI_TYPE_INFO = {
  good: {
    label: 'Auspicious',
    labelHi: 'शुभ',
    color: 'text-green-600',
    bg: 'bg-green-500/15',
    dot: 'bg-green-500',
  },
  neutral: {
    label: 'Neutral',
    labelHi: 'सामान्य',
    color: 'text-blue-500',
    bg: 'bg-blue-500/10',
    dot: 'bg-blue-500',
  },
  bad: {
    label: 'Inauspicious',
    labelHi: 'अशुभ',
    color: 'text-red-600',
    bg: 'bg-red-500/10',
    dot: 'bg-red-600',
  },
} as const;

export default function GowriTab({ panchang, language, t, timezoneOffset, minuteTick }: Props) {
  const gowriPanchang: GowriPeriod[] = panchang.gowri_panchang || [];
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
  const getTypeBucket = (quality: string) => {
    const q = String(quality || '').toLowerCase();
    if (q.includes('good') || q.includes('auspicious') || q.includes('benefic') || q === 'शुभ') return 'good';
    if (q.includes('neutral') || q === 'सामान्य') return 'neutral';
    return 'bad';
  };

  const { dayGowri, nightGowri, currentPeriodKey } = useMemo(() => {
    const day = gowriPanchang.filter(g => g.type === 'Day' || g.type === 'दिन');
    const night = gowriPanchang.filter(g => g.type === 'Night' || g.type === 'रात्रि');

    const currentTimeAtLocation = new Date(Date.now() + ((timezoneOffset + new Date().getTimezoneOffset()) * 60 * 1000));
    const currentMinutes = currentTimeAtLocation.getHours() * 60 + currentTimeAtLocation.getMinutes();
    const current = gowriPanchang.find((g) => isInTimeRange(currentMinutes, g.start, g.end));

    return {
      dayGowri: day,
      nightGowri: night,
      currentPeriodKey: current ? `${current.start}-${current.end}-${current.type}` : null,
    };
  }, [gowriPanchang, timezoneOffset, minuteTick]);
  const currentGowri = useMemo(
    () => gowriPanchang.find((g) => `${g.start}-${g.end}-${g.type}` === currentPeriodKey),
    [gowriPanchang, currentPeriodKey]
  );

  const renderRow = (period: GowriPeriod, index: number) => {
    const bucket = getTypeBucket(period.quality);
    const style = GOWRI_TYPE_INFO[bucket];
    const isCurrent = `${period.start}-${period.end}-${period.type}` === currentPeriodKey;

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
              {t('auto.now')}
            </span>
          )}
        </td>
        <td className="px-2 py-1">
          <span className={`inline-block px-1.5 py-0.5 rounded text-xs font-medium ${style.bg} ${style.color}`}>
            {language === 'hi' ? style.labelHi : style.label}
          </span>
        </td>
        <td className="px-2 py-1 text-cosmic-text-secondary">
          {period.start} - {period.end}
        </td>
      </tr>
    );
  };

  const renderTable = (periods: GowriPeriod[], icon: typeof Sun, title: string) => (
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
                {t('auto.name')}
              </th>
              <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold">
                {t('auto.type')}
              </th>
              <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold">
                {t('auto.time')}
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
          <Clock className="h-8 w-8 text-sacred-gold flex-shrink-0" />
          <div className="flex-1 min-w-0">
            <p className="text-xs text-cosmic-text-secondary">
              {t('auto.currentGowriPanchang')}
            </p>
            <span className="font-bold text-cosmic-text-primary">
              {language === 'hi' ? currentGowri.name_hindi || currentGowri.name : currentGowri.name}
            </span>
            <span className="mx-2 text-sacred-gold">{currentGowri.start} - {currentGowri.end}</span>
            <span className={`text-xs font-medium ${GOWRI_TYPE_INFO[getTypeBucket(currentGowri.quality)].color}`}>
              ({language === 'hi' ? GOWRI_TYPE_INFO[getTypeBucket(currentGowri.quality)].labelHi : GOWRI_TYPE_INFO[getTypeBucket(currentGowri.quality)].label})
            </span>
          </div>
        </div>
      )}

      {/* Day + Night side by side (stack on mobile) */}
      <div className="rounded-lg border border-cosmic-border overflow-hidden">
        <div className="flex flex-col md:flex-row divide-y md:divide-y-0 md:divide-x divide-cosmic-border">
          {dayGowri.length > 0 && (
            <div className="p-2">
              {renderTable(dayGowri, Sun, t('auto.dayGowriPanchang'))}
            </div>
          )}
          {nightGowri.length > 0 && (
            <div className="p-2">
              {renderTable(nightGowri, Moon, t('auto.nightGowriPanchang'))}
            </div>
          )}
        </div>
      </div>

      {/* Compact Legend */}
      <div className="rounded-lg border border-cosmic-border p-2">
        <h4 className="font-semibold text-cosmic-text-primary mb-1 text-sm">
          {t('auto.gowriMeanings')}
        </h4>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-1 text-xs">
          <div className={`flex items-center gap-1 px-1.5 py-1 rounded ${GOWRI_TYPE_INFO.good.bg}`}>
            <span className={`w-2 h-2 rounded-full ${GOWRI_TYPE_INFO.good.dot} flex-shrink-0`} />
            <span className="text-cosmic-text-primary font-medium">{language === 'hi' ? GOWRI_TYPE_INFO.good.labelHi : GOWRI_TYPE_INFO.good.label}</span>
            <span className="text-cosmic-text-secondary ml-auto">{t('auto.favorable')}</span>
          </div>
          <div className={`flex items-center gap-1 px-1.5 py-1 rounded ${GOWRI_TYPE_INFO.neutral.bg}`}>
            <span className={`w-2 h-2 rounded-full ${GOWRI_TYPE_INFO.neutral.dot} flex-shrink-0`} />
            <span className="text-cosmic-text-primary font-medium">{language === 'hi' ? GOWRI_TYPE_INFO.neutral.labelHi : GOWRI_TYPE_INFO.neutral.label}</span>
            <span className="text-cosmic-text-secondary ml-auto">{t('auto.average')}</span>
          </div>
          <div className={`flex items-center gap-1 px-1.5 py-1 rounded ${GOWRI_TYPE_INFO.bad.bg}`}>
            <span className={`w-2 h-2 rounded-full ${GOWRI_TYPE_INFO.bad.dot} flex-shrink-0`} />
            <span className="text-cosmic-text-primary font-medium">{language === 'hi' ? GOWRI_TYPE_INFO.bad.labelHi : GOWRI_TYPE_INFO.bad.label}</span>
            <span className="text-cosmic-text-secondary ml-auto">{t('auto.avoid')}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
