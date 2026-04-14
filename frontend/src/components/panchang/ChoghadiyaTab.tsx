import { useMemo } from 'react';
import { Sun, Moon, Clock } from 'lucide-react';
import type { FullPanchangData } from '@/sections/Panchang';

interface Props {
  panchang: FullPanchangData;
  language: string;
  t: (key: string) => string;
  timezoneOffset: number;
}

const CHOGHADIYA_QUALITY: Record<string, { label: string; labelHi: string; color: string; bg: string; border: string }> = {
  'Amrit':  { label: 'Best',          labelHi: 'सर्वश्रेष्ठ',     color: 'text-green-600',  bg: 'bg-green-500/15',  border: 'border-green-500/30' },
  'Shubh':  { label: 'Good',          labelHi: 'अच्छा',           color: 'text-green-500',  bg: 'bg-green-500/10',  border: 'border-green-500/20' },
  'Labh':   { label: 'Gain',          labelHi: 'लाभदायक',         color: 'text-emerald-500', bg: 'bg-emerald-500/10', border: 'border-emerald-500/20' },
  'Char':   { label: 'Neutral',       labelHi: 'सामान्य',          color: 'text-blue-500',   bg: 'bg-blue-500/10',   border: 'border-blue-500/20' },
  'Udveg':  { label: 'Inauspicious',  labelHi: 'अशुभ',            color: 'text-orange-500', bg: 'bg-orange-500/10', border: 'border-orange-500/20' },
  'Kaal':   { label: 'Inauspicious',  labelHi: 'अशुभ',            color: 'text-red-600',    bg: 'bg-red-500/10',    border: 'border-red-500/20' },
  'Rog':    { label: 'Inauspicious',  labelHi: 'अशुभ',            color: 'text-red-500',    bg: 'bg-red-500/10',    border: 'border-red-500/20' },
};

const CHOGHADIYA_HINDI: Record<string, string> = {
  'Amrit': 'अमृत', 'Shubh': 'शुभ', 'Labh': 'लाभ', 'Char': 'चर',
  'Udveg': 'उद्वेग', 'Kaal': 'काल', 'Rog': 'रोग',
};

type ChoghadiyaPeriod = { name: string; quality: string; start: string; end: string; name_hindi?: string };

export default function ChoghadiyaTab({ panchang, language, t, timezoneOffset }: Props) {
  const dayChoghadiya = panchang.choghadiya || [];
  const nightChoghadiya = panchang.night_choghadiya || [];

  // Find current active period across both day and night
  const currentPeriodKey = useMemo(() => {
    const now = new Date(Date.now() + ((timezoneOffset + new Date().getTimezoneOffset()) * 60 * 1000));
    const currentTime = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;

    const allPeriods = [...dayChoghadiya, ...nightChoghadiya];
    const found = allPeriods.find(c => currentTime >= c.start && currentTime < c.end);
    return found ? `${found.start}-${found.end}` : null;
  }, [dayChoghadiya, nightChoghadiya, timezoneOffset]);

  const renderRow = (period: ChoghadiyaPeriod) => {
    const q = CHOGHADIYA_QUALITY[period.name] || { label: '?', labelHi: '?', color: 'text-gray-500', bg: 'bg-gray-500/10', border: 'border-gray-500/20' };
    const key = `${period.start}-${period.end}`;
    const isCurrent = key === currentPeriodKey;

    return (
      <tr
        key={key}
        className={`border-b border-cosmic-border/50 last:border-0 ${isCurrent ? 'bg-amber-500/15 border-l-2 border-l-amber-500' : ''}`}
      >
        <td className="px-2 py-1">
          <span className={`font-medium ${isCurrent ? 'text-sacred-gold' : 'text-cosmic-text-primary'}`}>
            {language === 'hi' ? period.name_hindi || CHOGHADIYA_HINDI[period.name] || period.name : period.name}
          </span>
          {isCurrent && (
            <span className="ml-1 px-1.5 py-0.5 text-xs bg-sacred-gold text-cosmic-bg rounded-full">
              {language === 'hi' ? 'अभी' : 'Now'}
            </span>
          )}
        </td>
        <td className="px-2 py-1">
          <span className={`inline-block px-1.5 py-0.5 rounded text-xs font-medium ${q.bg} ${q.color}`}>
            {language === 'hi' ? q.labelHi : q.label}
          </span>
        </td>
        <td className="px-2 py-1 text-cosmic-text-secondary">
          {period.start} - {period.end}
        </td>
      </tr>
    );
  };

  const renderTable = (periods: ChoghadiyaPeriod[], icon: typeof Sun, title: string) => (
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
                {language === 'hi' ? 'फल' : 'Type'}
              </th>
              <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold">
                {language === 'hi' ? 'समय' : 'Time'}
              </th>
            </tr>
          </thead>
          <tbody>
            {periods.map(renderRow)}
          </tbody>
        </table>
      </div>
    </div>
  );

  return (
    <div className="space-y-3">
      {/* Current Choghadiya compact banner */}
      {currentPeriodKey && (() => {
        const allPeriods = [...dayChoghadiya, ...nightChoghadiya];
        const current = allPeriods.find(c => `${c.start}-${c.end}` === currentPeriodKey);
        if (!current) return null;
        const q = CHOGHADIYA_QUALITY[current.name];
        return (
          <div className="flex items-center gap-3 p-2 rounded-lg border border-sacred-gold/30 bg-sacred-gold/10">
            <Clock className="h-8 w-8 text-sacred-gold flex-shrink-0" />
            <div className="flex-1 min-w-0">
              <p className="text-xs text-cosmic-text-secondary">
                {language === 'hi' ? 'वर्तमान चौघड़िया' : 'Current Choghadiya'}
              </p>
              <span className="font-bold text-cosmic-text-primary">
                {language === 'hi' ? current.name_hindi || CHOGHADIYA_HINDI[current.name] || current.name : current.name}
              </span>
              <span className="mx-2 text-sacred-gold">{current.start} - {current.end}</span>
              {q && <span className={`text-xs font-medium ${q.color}`}>({language === 'hi' ? q.labelHi : q.label})</span>}
            </div>
          </div>
        );
      })()}

      {/* Day + Night side by side (stack on mobile) */}
      <div className="rounded-lg border border-cosmic-border overflow-hidden">
        <div className="flex flex-col md:flex-row divide-y md:divide-y-0 md:divide-x divide-cosmic-border">
          {dayChoghadiya.length > 0 && (
            <div className="flex-1 p-2">
              {renderTable(dayChoghadiya, Sun, language === 'hi' ? 'दिन के चौघड़िया' : 'Day Choghadiya')}
            </div>
          )}
          {nightChoghadiya.length > 0 && (
            <div className="flex-1 p-2">
              {renderTable(nightChoghadiya, Moon, language === 'hi' ? 'रात्रि के चौघड़िया' : 'Night Choghadiya')}
            </div>
          )}
        </div>
      </div>

      {/* Compact Legend */}
      <div className="rounded-lg border border-cosmic-border p-2">
        <h4 className="font-semibold text-cosmic-text-primary mb-1 text-sm">
          {language === 'hi' ? 'चौघड़िया का अर्थ' : 'Choghadiya Meanings'}
        </h4>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-1 text-xs">
          <div className="flex items-center gap-1 px-1.5 py-1 rounded bg-green-500/10">
            <span className="w-2 h-2 rounded-full bg-green-500 flex-shrink-0" />
            <span className="text-cosmic-text-primary font-medium">
              {language === 'hi' ? 'अमृत, शुभ, लाभ' : 'Amrit, Shubh, Labh'}
            </span>
            <span className="text-cosmic-text-secondary ml-auto">{language === 'hi' ? 'शुभ' : 'Good'}</span>
          </div>
          <div className="flex items-center gap-1 px-1.5 py-1 rounded bg-blue-500/10">
            <span className="w-2 h-2 rounded-full bg-blue-500 flex-shrink-0" />
            <span className="text-cosmic-text-primary font-medium">
              {language === 'hi' ? 'चर' : 'Char'}
            </span>
            <span className="text-cosmic-text-secondary ml-auto">{language === 'hi' ? 'यात्रा' : 'Travel'}</span>
          </div>
          <div className="flex items-center gap-1 px-1.5 py-1 rounded bg-orange-500/10">
            <span className="w-2 h-2 rounded-full bg-orange-500 flex-shrink-0" />
            <span className="text-cosmic-text-primary font-medium">
              {language === 'hi' ? 'रोग, उद्वेग' : 'Rog, Udveg'}
            </span>
            <span className="text-cosmic-text-secondary ml-auto">{language === 'hi' ? 'सावधान' : 'Caution'}</span>
          </div>
          <div className="flex items-center gap-1 px-1.5 py-1 rounded bg-red-500/10">
            <span className="w-2 h-2 rounded-full bg-red-600 flex-shrink-0" />
            <span className="text-cosmic-text-primary font-medium">
              {language === 'hi' ? 'काल' : 'Kaal'}
            </span>
            <span className="text-cosmic-text-secondary ml-auto">{language === 'hi' ? 'टालें' : 'Avoid'}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
