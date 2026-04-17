import { useMemo } from 'react';
import { Sun, Moon, Clock } from 'lucide-react';
import type { FullPanchangData } from '@/sections/Panchang';
import { Heading } from "@/components/ui/heading";
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/table";

interface Props {
  panchang: FullPanchangData;
  language: string;
  t: (key: string) => string;
  timezoneOffset: number;
  minuteTick: number;
}

const CHOGHADIYA_QUALITY: Record<string, { label: string; labelHi: string; color: string; bg: string; border: string; bestFor: string; bestForHi: string }> = {
  'Amrit': { label: 'Best',         labelHi: 'सर्वश्रेष्ठ', color: 'text-green-600',   bg: 'bg-green-500/15',   border: 'border-green-500/30',  bestFor: 'All auspicious activities',           bestForHi: 'सभी शुभ कार्य' },
  'Shubh': { label: 'Good',         labelHi: 'अच्छा',       color: 'text-green-500',   bg: 'bg-green-500/10',   border: 'border-green-500/20',  bestFor: 'Marriage, travel, auspicious work',   bestForHi: 'विवाह, यात्रा, शुभ कार्य' },
  'Labh':  { label: 'Gain',         labelHi: 'लाभदायक',     color: 'text-emerald-500', bg: 'bg-emerald-500/10', border: 'border-emerald-500/20', bestFor: 'Business, trade, financial gains',    bestForHi: 'व्यापार, लाभ, क्रय-विक्रय' },
  'Char':  { label: 'Neutral',      labelHi: 'सामान्य',     color: 'text-blue-500',    bg: 'bg-blue-500/10',    border: 'border-blue-500/20',   bestFor: 'Travel, movement, vehicle purchase',  bestForHi: 'यात्रा, वाहन, गमन' },
  'Udveg': { label: 'Inauspicious', labelHi: 'अशुभ',        color: 'text-orange-500',  bg: 'bg-orange-500/10',  border: 'border-orange-500/20', bestFor: 'Government work only',                bestForHi: 'केवल सरकारी कार्य' },
  'Kaal':  { label: 'Inauspicious', labelHi: 'अशुभ',        color: 'text-red-600',     bg: 'bg-red-500/10',     border: 'border-red-500/20',    bestFor: 'Avoid all new work',                  bestForHi: 'नया कार्य वर्जित' },
  'Rog':   { label: 'Inauspicious', labelHi: 'अशुभ',        color: 'text-red-500',     bg: 'bg-red-500/10',     border: 'border-red-500/20',    bestFor: 'Medical treatment only',              bestForHi: 'केवल चिकित्सा कार्य' },
};

const CHOGHADIYA_HINDI: Record<string, string> = {
  'Amrit': 'अमृत', 'Shubh': 'शुभ', 'Labh': 'लाभ', 'Char': 'चर',
  'Udveg': 'उद्वेग', 'Kaal': 'काल', 'Rog': 'रोग',
};

type ChoghadiyaPeriod = { name: string; quality: string; start: string; end: string; name_hindi?: string; vaar_vela?: boolean; kaal_vela?: boolean; kaal_ratri?: boolean };

export default function ChoghadiyaTab({ panchang, language, t, timezoneOffset, minuteTick }: Props) {
  const dayChoghadiya = panchang.choghadiya || [];
  const nightChoghadiya = panchang.night_choghadiya || [];
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

  // Find current active period across both day and night
  const currentPeriodKey = useMemo(() => {
    const now = new Date(Date.now() + ((timezoneOffset + new Date().getTimezoneOffset()) * 60 * 1000));
    const currentMinutes = now.getHours() * 60 + now.getMinutes();

    const allPeriods = [...dayChoghadiya, ...nightChoghadiya];
    const found = allPeriods.find(c => isInTimeRange(currentMinutes, c.start, c.end));
    return found ? `${found.start}-${found.end}` : null;
  }, [dayChoghadiya, nightChoghadiya, timezoneOffset, minuteTick, isInTimeRange]);

  const renderRow = (period: ChoghadiyaPeriod) => {
    const q = CHOGHADIYA_QUALITY[period.name] || { label: '?', labelHi: '?', color: 'text-muted-foreground', bg: 'bg-gray-500/10', border: 'border-gray-500/20' };
    const key = `${period.start}-${period.end}`;
    const isCurrent = key === currentPeriodKey;
    const hasVelaFlag = period.vaar_vela || period.kaal_vela || period.kaal_ratri;

    return (
      <TableRow
        key={key}
        className={`border-b border/50 last:border-0 ${hasVelaFlag ? 'bg-red-50/50' : ''} ${isCurrent ? 'bg-amber-500/15 border-l-2 border-l-amber-500' : ''}`}
      >
        <TableCell className="px-2 py-1">
          <div className="flex flex-wrap items-center gap-1">
            <span className={`font-medium ${isCurrent ? 'text-sacred-gold' : 'text-foreground'}`}>
              {language === 'hi' ? period.name_hindi || CHOGHADIYA_HINDI[period.name] || period.name : period.name}
            </span>
            {isCurrent && (
              <span className="px-1.5 py-0.5 text-xs bg-sacred-gold text-background rounded-full">
                {t('auto.now')}
              </span>
            )}
            {period.vaar_vela && (
              <span className="bg-red-100 text-red-700 text-[9px] px-1.5 py-0.5 rounded-full font-medium" title={language === 'hi' ? 'अशुभ उप-काल' : 'Inauspicious sub-period'}>
                {language === 'hi' ? 'वार वेला' : 'Vaar Vela'}
              </span>
            )}
            {period.kaal_vela && (
              <span className="bg-red-100 text-red-700 text-[9px] px-1.5 py-0.5 rounded-full font-medium" title={language === 'hi' ? 'अशुभ उप-काल' : 'Inauspicious sub-period'}>
                {language === 'hi' ? 'काल वेला' : 'Kaal Vela'}
              </span>
            )}
            {period.kaal_ratri && (
              <span className="bg-red-100 text-red-700 text-[9px] px-1.5 py-0.5 rounded-full font-medium" title={language === 'hi' ? 'अशुभ रात्रि काल' : 'Inauspicious night period'}>
                {language === 'hi' ? 'काल रात्रि' : 'Kaal Ratri'}
              </span>
            )}
          </div>
        </TableCell>
        <TableCell className="px-2 py-1">
          <span className={`inline-block px-1.5 py-0.5 rounded text-xs font-medium ${q.bg} ${q.color}`}>
            {language === 'hi' ? q.labelHi : q.label}
          </span>
        </TableCell>
        <TableCell className="px-2 py-1 text-muted-foreground">
          {period.start} - {period.end}
        </TableCell>
      </TableRow>
    );
  };

  const renderTable = (periods: ChoghadiyaPeriod[], icon: typeof Sun, title: string) => (
    <div className="flex-1 min-w-0">
      <h3 className="font-bold text-foreground mb-1 flex items-center gap-1">
        {icon === Sun
          ? <Sun className="h-4 w-4 text-orange-500" />
          : <Moon className="h-4 w-4 text-indigo-400" />}
        {title}
      </h3>
      <div className="overflow-x-auto">
        <Table className="w-full table-fixed text-xs sm:text-sm">
          <TableHeader>
            <TableRow className="bg-sacred-gold/15">
              <TableHead className="text-left px-2 py-1 text-sacred-gold-dark font-semibold">
                {t('auto.name')}
              </TableHead>
              <TableHead className="text-left px-2 py-1 text-sacred-gold-dark font-semibold">
                {t('auto.type')}
              </TableHead>
              <TableHead className="text-left px-2 py-1 text-sacred-gold-dark font-semibold">
                {t('auto.time')}
              </TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {periods.map(renderRow)}
          </TableBody>
        </Table>
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
              <p className="text-xs text-muted-foreground">
                {t('auto.currentChoghadiya')}
              </p>
              <span className="font-bold text-foreground">
                {language === 'hi' ? current.name_hindi || CHOGHADIYA_HINDI[current.name] || current.name : current.name}
              </span>
              <span className="mx-2 text-sacred-gold">{current.start} - {current.end}</span>
              {q && <span className={`text-xs font-medium ${q.color}`}>({language === 'hi' ? q.labelHi : q.label})</span>}
              {q && (
                <p className="text-[11px] text-muted-foreground mt-0.5">
                  {language === 'hi' ? q.bestForHi : q.bestFor}
                </p>
              )}
            </div>
          </div>
        );
      })()}

      {/* Day + Night side by side (stack on mobile) */}
      <div className="rounded-lg border overflow-hidden">
        <div className="flex flex-col md:flex-row divide-y md:divide-y-0 md:divide-x divide-border">
          {dayChoghadiya.length > 0 && (
            <div className="flex-1 p-2">
              {renderTable(dayChoghadiya, Sun, t('auto.dayChoghadiya'))}
            </div>
          )}
          {nightChoghadiya.length > 0 && (
            <div className="flex-1 p-2">
              {renderTable(nightChoghadiya, Moon, t('auto.nightChoghadiya'))}
            </div>
          )}
        </div>
      </div>

      {/* Compact Legend */}
      <div className="rounded-lg border p-2">
        <Heading as={4} variant={4}>
          {t('auto.choghadiyaMeanings')}
        </Heading>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-1 text-xs">
          {Object.entries(CHOGHADIYA_QUALITY).map(([name, q]) => (
            <div key={name} className={`flex items-start gap-2 px-2 py-1.5 rounded ${q.bg}`}>
              <span className={`w-2 h-2 rounded-full flex-shrink-0 mt-1 ${q.color.replace('text-', 'bg-')}`} />
              <div className="min-w-0">
                <span className={`font-semibold ${q.color}`}>{name}</span>
                <span className="text-muted-foreground ml-1.5">
                  {language === 'hi' ? CHOGHADIYA_HINDI[name] || name : ''}
                </span>
                <p className="text-muted-foreground/80 leading-tight">
                  {language === 'hi' ? q.bestForHi : q.bestFor}
                </p>
              </div>
            </div>
          ))}
        </div>
        {/* Vaar Vela / Kaal Vela / Kaal Ratri legend */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-1 text-xs mt-2">
          <div className="flex items-center gap-1.5 px-1.5 py-1 rounded bg-red-50">
            <span className="bg-red-100 text-red-700 text-[9px] px-1.5 py-0.5 rounded-full font-medium flex-shrink-0">
              {language === 'hi' ? 'वार वेला' : 'Vaar Vela'}
            </span>
            <span className="text-muted-foreground">
              {language === 'hi' ? 'अशुभ वार काल' : 'Inauspicious weekday period'}
            </span>
          </div>
          <div className="flex items-center gap-1.5 px-1.5 py-1 rounded bg-red-50">
            <span className="bg-red-100 text-red-700 text-[9px] px-1.5 py-0.5 rounded-full font-medium flex-shrink-0">
              {language === 'hi' ? 'काल वेला' : 'Kaal Vela'}
            </span>
            <span className="text-muted-foreground">
              {language === 'hi' ? 'अशुभ काल' : 'Inauspicious time period'}
            </span>
          </div>
          <div className="flex items-center gap-1.5 px-1.5 py-1 rounded bg-red-50">
            <span className="bg-red-100 text-red-700 text-[9px] px-1.5 py-0.5 rounded-full font-medium flex-shrink-0">
              {language === 'hi' ? 'काल रात्रि' : 'Kaal Ratri'}
            </span>
            <span className="text-muted-foreground">
              {language === 'hi' ? 'अशुभ रात्रि काल' : 'Inauspicious night period'}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}