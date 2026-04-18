import { Card, CardContent } from '@/components/ui/card';
import { Heading } from '@/components/ui/heading';
import { Badge } from '@/components/ui/badge';
import { AlertCircle, CheckCircle, Clock, Flame, Leaf, Moon } from 'lucide-react';
import { translateBackend } from '@/lib/backend-translations';
import type { FullPanchangData } from '@/sections/Panchang';

interface Props {
  panchang: FullPanchangData;
  language: string;
  t: (key: string) => string;
}

export default function DayDetailPanel({ panchang, language, t }: Props) {
  const isHi = language === 'hi';
  const l = (en: string, hi: string) => isHi ? hi : en;

  const timeBadge = (icon: string, label: string, value: string | undefined) => {
    if (!value || value === '--:--') return null;
    return (
      <div className="flex items-center justify-between p-2 rounded-lg bg-background/50 border border-border/30">
        <span className="text-xs font-medium text-muted-foreground">{icon} {label}</span>
        <span className="font-semibold text-foreground text-sm">{value}</span>
      </div>
    );
  };

  const formatPeriod = (period: any) => {
    if (!period) return null;
    if (typeof period === 'string') return period;
    const s = period.start || '';
    const e = period.end || '';
    return s && e ? `${s} – ${e}` : null;
  };

  return (
    <div className="space-y-3">
      {/* Primary Panchang Elements */}
      <div className="grid grid-cols-2 gap-2">
        <Card className="bg-background/50 border-border/50">
          <CardContent className="p-3">
            <p className="text-[10px] text-muted-foreground font-medium mb-1">
              {l('Tithi', 'तिथि')}
            </p>
            <p className="text-sm font-bold text-foreground">
              {isHi && panchang.tithi?.name_hindi
                ? panchang.tithi.name_hindi
                : panchang.tithi?.name}
            </p>
            {panchang.tithi?.end_time && (
              <p className="text-[9px] text-muted-foreground mt-1">
                {l('Until', 'तक')} {panchang.tithi.end_time}
              </p>
            )}
          </CardContent>
        </Card>

        <Card className="bg-background/50 border-border/50">
          <CardContent className="p-3">
            <p className="text-[10px] text-muted-foreground font-medium mb-1">
              {l('Nakshatra', 'नक्षत्र')}
            </p>
            <p className="text-sm font-bold text-foreground">
              {isHi && panchang.nakshatra?.name_hindi
                ? panchang.nakshatra.name_hindi
                : panchang.nakshatra?.name}
            </p>
            {panchang.nakshatra?.end_time && (
              <p className="text-[9px] text-muted-foreground mt-1">
                {l('Until', 'तक')} {panchang.nakshatra.end_time}
              </p>
            )}
          </CardContent>
        </Card>

        <Card className="bg-background/50 border-border/50">
          <CardContent className="p-3">
            <p className="text-[10px] text-muted-foreground font-medium mb-1">
              {l('Yoga', 'योग')}
            </p>
            <p className="text-sm font-bold text-foreground">
              {isHi && panchang.yoga?.name_hindi
                ? panchang.yoga.name_hindi
                : panchang.yoga?.name}
            </p>
            {panchang.yoga?.end_time && (
              <p className="text-[9px] text-muted-foreground mt-1">
                {l('Until', 'तक')} {panchang.yoga.end_time}
              </p>
            )}
          </CardContent>
        </Card>

        <Card className="bg-background/50 border-border/50">
          <CardContent className="p-3">
            <p className="text-[10px] text-muted-foreground font-medium mb-1">
              {l('Karana', 'करण')}
            </p>
            <p className="text-sm font-bold text-foreground">
              {isHi && panchang.karana?.name_hindi
                ? panchang.karana.name_hindi
                : panchang.karana?.name}
            </p>
            {panchang.karana?.end_time && (
              <p className="text-[9px] text-muted-foreground mt-1">
                {l('Until', 'तक')} {panchang.karana.end_time}
              </p>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Sun & Moon Times */}
      <div className="space-y-2">
        <Heading as={5} variant={5} className="text-muted-foreground">
          ☀️ {l('Sun', 'सूर्य')} & ☽ {l('Moon', 'चंद्र')}
        </Heading>
        <div className="space-y-1">
          {timeBadge('☀↑', l('Sunrise', 'सूर्योदय'), panchang.sunrise)}
          {timeBadge('☀↓', l('Sunset', 'सूर्यास्त'), panchang.sunset)}
          {timeBadge('☽↑', l('Moonrise', 'चंद्रोदय'), panchang.moonrise)}
          {timeBadge('☽↓', l('Moonset', 'चंद्रास्त'), panchang.moonset)}
        </div>
      </div>

      {/* Critical Times */}
      <div className="space-y-2">
        <Heading as={5} variant={5} className="text-muted-foreground">
          ⚠️ {l('Times to Avoid', 'बचने के समय')}
        </Heading>
        <div className="space-y-1">
          {panchang.rahu_kaal && formatPeriod(panchang.rahu_kaal) && (
            <div className="flex items-center justify-between p-2 rounded-lg bg-orange-50/50 border border-orange-200/50">
              <span className="text-xs font-medium text-orange-700">{l('Rahu Kaal', 'राहु काल')}</span>
              <span className="text-xs font-semibold text-orange-700">
                {formatPeriod(panchang.rahu_kaal)}
              </span>
            </div>
          )}
          {panchang.gulika_kaal && formatPeriod(panchang.gulika_kaal) && (
            <div className="flex items-center justify-between p-2 rounded-lg bg-orange-50/50 border border-orange-200/50">
              <span className="text-xs font-medium text-orange-700">{l('Gulika Kaal', 'गुलिका काल')}</span>
              <span className="text-xs font-semibold text-orange-700">
                {formatPeriod(panchang.gulika_kaal)}
              </span>
            </div>
          )}
          {panchang.yamaganda && formatPeriod(panchang.yamaganda) && (
            <div className="flex items-center justify-between p-2 rounded-lg bg-red-50/50 border border-red-200/50">
              <span className="text-xs font-medium text-red-700">{l('Yamaganda', 'यमगंडा')}</span>
              <span className="text-xs font-semibold text-red-700">
                {formatPeriod(panchang.yamaganda)}
              </span>
            </div>
          )}
        </div>
      </div>

      {/* Auspicious Times */}
      <div className="space-y-2">
        <Heading as={5} variant={5} className="text-muted-foreground">
          ✨ {l('Auspicious Times', 'शुभ समय')}
        </Heading>
        <div className="space-y-1">
          {panchang.abhijit_muhurat && formatPeriod(panchang.abhijit_muhurat) && (
            <div className="flex items-center justify-between p-2 rounded-lg bg-green-50/50 border border-green-200/50">
              <span className="text-xs font-medium text-green-700">{l('Abhijit Muhurat', 'अभिजित मुहूर्त')}</span>
              <span className="text-xs font-semibold text-green-700">
                {formatPeriod(panchang.abhijit_muhurat)}
              </span>
            </div>
          )}
          {panchang.brahma_muhurat && formatPeriod(panchang.brahma_muhurat) && (
            <div className="flex items-center justify-between p-2 rounded-lg bg-green-50/50 border border-green-200/50">
              <span className="text-xs font-medium text-green-700">{l('Brahma Muhurat', 'ब्रह्म मुहूर्त')}</span>
              <span className="text-xs font-semibold text-green-700">
                {formatPeriod(panchang.brahma_muhurat)}
              </span>
            </div>
          )}
          {panchang.vijaya_muhurta && formatPeriod(panchang.vijaya_muhurta) && (
            <div className="flex items-center justify-between p-2 rounded-lg bg-blue-50/50 border border-blue-200/50">
              <span className="text-xs font-medium text-blue-700">{l('Vijaya Muhurta', 'विजय मुहूर्त')}</span>
              <span className="text-xs font-semibold text-blue-700">
                {formatPeriod(panchang.vijaya_muhurta)}
              </span>
            </div>
          )}
        </div>
      </div>

      {/* Festivals & Special Yogas */}
      {(panchang.festivals?.length || panchang.special_yogas) && (
        <div className="space-y-2">
          <Heading as={5} variant={5} className="text-muted-foreground">
            🎊 {l('Festivals & Special Days', 'पर्व और विशेष दिन')}
          </Heading>
          <div className="space-y-1">
            {panchang.festivals?.map((festival, idx) => (
              <Badge key={idx} className="inline-block mr-2 mb-2 bg-red-100 text-red-700 hover:bg-red-100">
                {isHi && festival.name_hindi ? festival.name_hindi : festival.name}
              </Badge>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
