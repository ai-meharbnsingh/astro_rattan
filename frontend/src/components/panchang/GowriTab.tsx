import { useMemo } from 'react';
import { Moon, Sun, Clock } from 'lucide-react';
import type { FullPanchangData } from '@/sections/Panchang';
import { Heading } from "@/components/ui/heading";
import { Text } from "@/components/ui/text";
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/table";

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

const GOWRI_PERIOD_DETAILS: Record<string, { en: string; hi: string }> = {
  amrit: { en: 'Best for all auspicious work', hi: 'सर्वश्रेष्ठ, सभी शुभ कार्यों के लिए' },
  shubha: { en: 'Good for important tasks', hi: 'महत्वपूर्ण कार्यों के लिए शुभ' },
  labha: { en: 'Good for gains and finance', hi: 'लाभ और धन संबंधी कार्यों के लिए अच्छा' },
  udvega: { en: 'Avoid new beginnings', hi: 'नए कार्य शुरू करने से बचें' },
  kaala: { en: 'Inauspicious period', hi: 'अशुभ समय' },
  roga: { en: 'Not good for health-related decisions', hi: 'स्वास्थ्य संबंधित निर्णयों के लिए उचित नहीं' },
  chara: { en: 'Suitable for travel and movement', hi: 'यात्रा और गतिशील कार्यों के लिए उपयुक्त' },
  dhana: { en: 'Favorable for money matters', hi: 'धन संबंधी कार्यों के लिए अनुकूल' },
  dhanada: { en: 'Prosperity and wealth gaining', hi: 'समृद्धि और धन वृद्धि के लिए अनुकूल' },
};

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
  const getPeriodDetail = (name: string) => {
    const key = String(name || '').toLowerCase();
    const found = Object.keys(GOWRI_PERIOD_DETAILS).find((k) => key.includes(k));
    if (!found) return language === 'hi' ? 'सामान्य गौरी अवधि' : 'General Gowri period';
    return language === 'hi' ? GOWRI_PERIOD_DETAILS[found].hi : GOWRI_PERIOD_DETAILS[found].en;
  };

  const { dayGowri, nightGowri, currentPeriodKey } = useMemo(() => {
    const day = gowriPanchang.filter((g) => {
      const type = String(g.type || '').toLowerCase();
      return type.includes('day') || type.includes('दिन');
    });
    const night = gowriPanchang.filter((g) => {
      const type = String(g.type || '').toLowerCase();
      return type.includes('night') || type.includes('रात्र');
    });

    // Fallback: some payloads do not include explicit day/night type labels.
    const fallbackDay = day.length > 0 ? day : gowriPanchang.slice(0, Math.ceil(gowriPanchang.length / 2));
    const fallbackNight = night.length > 0 ? night : gowriPanchang.slice(Math.ceil(gowriPanchang.length / 2));

    const currentTimeAtLocation = new Date(Date.now() + ((timezoneOffset + new Date().getTimezoneOffset()) * 60 * 1000));
    const currentMinutes = currentTimeAtLocation.getHours() * 60 + currentTimeAtLocation.getMinutes();
    const current = gowriPanchang.find((g) => isInTimeRange(currentMinutes, g.start, g.end));

    return {
      dayGowri: fallbackDay,
      nightGowri: fallbackNight,
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
      <TableRow
        key={`${period.type}-${index}`}
        className={`border-b border/50 last:border-0 ${isCurrent ? 'bg-amber-500/15 border-l-2 border-l-amber-500' : ''}`}
      >
        <TableCell className="px-2 py-1">
          <span className={`font-medium ${isCurrent ? 'text-sacred-gold' : 'text-foreground'}`}>
            {language === 'hi' ? period.name_hindi || period.name : period.name}
          </span>
          {isCurrent && (
            <span className="ml-1 px-1.5 py-0.5 text-xs bg-sacred-gold text-background rounded-full">
              {t('auto.now')}
            </span>
          )}
        </TableCell>
        <TableCell className="px-2 py-1">
          <span className={`inline-block px-1.5 py-0.5 rounded text-xs font-medium ${style.bg} ${style.color}`}>
            {language === 'hi' ? style.labelHi : style.label}
          </span>
        </TableCell>
        <TableCell className="px-2 py-1 text-muted-foreground">
          {period.start} - {period.end}
        </TableCell>
        <TableCell className="px-2 py-1 text-muted-foreground whitespace-normal break-words">
          {getPeriodDetail(period.name)}
        </TableCell>
      </TableRow>
    );
  };

  const renderTable = (periods: GowriPeriod[], icon: typeof Sun, title: string) => (
    <div className="flex-1 min-w-0">
      <h3 className="font-bold text-foreground mb-1 flex items-center gap-1">
        {icon === Sun
          ? <Sun className="h-4 w-4 text-orange-500" />
          : <Moon className="h-4 w-4 text-indigo-400" />}
        {title}
      </h3>
      <div className="overflow-x-auto">
        <Table className="w-full text-sm">
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
              <TableHead className="text-left px-2 py-1 text-sacred-gold-dark font-semibold">
                {t('auto.details')}
              </TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {periods.map((period, index) => renderRow(period, index))}
          </TableBody>
        </Table>
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
            <p className="text-xs text-muted-foreground">
              {t('auto.currentGowriPanchang')}
            </p>
            <span className="font-bold text-foreground">
              {language === 'hi' ? currentGowri.name_hindi || currentGowri.name : currentGowri.name}
            </span>
            <span className="mx-2 text-sacred-gold">{currentGowri.start} - {currentGowri.end}</span>
            <span className={`text-xs font-medium ${GOWRI_TYPE_INFO[getTypeBucket(currentGowri.quality)].color}`}>
              ({language === 'hi' ? GOWRI_TYPE_INFO[getTypeBucket(currentGowri.quality)].labelHi : GOWRI_TYPE_INFO[getTypeBucket(currentGowri.quality)].label})
            </span>
            <Text variant="small" as="span">
              {getPeriodDetail(currentGowri.name)}
            </Text>
          </div>
        </div>
      )}

      {/* Day + Night side by side (stack on mobile) */}
      <div className="rounded-lg border overflow-hidden">
        <div className="flex flex-col md:flex-row divide-y md:divide-y-0 md:divide-x divide-border">
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
      <div className="rounded-lg border p-2">
        <Heading as={4} variant={4}>
          {t('auto.gowriMeanings')}
        </Heading>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-1 text-xs">
          <div className={`flex items-center gap-1 px-1.5 py-1 rounded ${GOWRI_TYPE_INFO.good.bg}`}>
            <span className={`w-2 h-2 rounded-full ${GOWRI_TYPE_INFO.good.dot} flex-shrink-0`} />
            <span className="text-foreground font-medium">{language === 'hi' ? GOWRI_TYPE_INFO.good.labelHi : GOWRI_TYPE_INFO.good.label}</span>
            <span className="text-muted-foreground ml-auto">{t('auto.favorable')}</span>
          </div>
          <div className={`flex items-center gap-1 px-1.5 py-1 rounded ${GOWRI_TYPE_INFO.neutral.bg}`}>
            <span className={`w-2 h-2 rounded-full ${GOWRI_TYPE_INFO.neutral.dot} flex-shrink-0`} />
            <span className="text-foreground font-medium">{language === 'hi' ? GOWRI_TYPE_INFO.neutral.labelHi : GOWRI_TYPE_INFO.neutral.label}</span>
            <span className="text-muted-foreground ml-auto">{t('auto.average')}</span>
          </div>
          <div className={`flex items-center gap-1 px-1.5 py-1 rounded ${GOWRI_TYPE_INFO.bad.bg}`}>
            <span className={`w-2 h-2 rounded-full ${GOWRI_TYPE_INFO.bad.dot} flex-shrink-0`} />
            <span className="text-foreground font-medium">{language === 'hi' ? GOWRI_TYPE_INFO.bad.labelHi : GOWRI_TYPE_INFO.bad.label}</span>
            <span className="text-muted-foreground ml-auto">{t('auto.avoid')}</span>
          </div>
        </div>
      </div>
    </div>
  );
}