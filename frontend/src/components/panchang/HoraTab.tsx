import { useMemo } from 'react';
import { Clock, Sun, Moon, AlertCircle } from 'lucide-react';
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

export default function HoraTab({ panchang, language, t, timezoneOffset, minuteTick }: Props) {
  const horaTable = panchang.hora_table || [];

  const toMinutes = (time: string): number => {
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

  // Memoize current Hora calculation to avoid running on every render
  const currentHora = useMemo(() => {
    // Calculate current time at the panchang location (not browser local time)
    const currentTimeAtLocation = new Date(Date.now() + ((timezoneOffset + new Date().getTimezoneOffset()) * 60 * 1000));
    const currentMinutes = currentTimeAtLocation.getHours() * 60 + currentTimeAtLocation.getMinutes();

    return horaTable.find((h) => isInTimeRange(currentMinutes, h.start, h.end));
  }, [horaTable, timezoneOffset, minuteTick]);

  const sunriseMin = toMinutes(panchang.sunrise || '');
  const sunsetMin = toMinutes(panchang.sunset || '');
  const hasValidSunWindow = sunriseMin >= 0 && sunsetMin >= 0 && sunriseMin !== sunsetMin;
  const isDayStart = (startTime: string) => {
    const mins = toMinutes(startTime);
    if (mins < 0) return false;
    if (!hasValidSunWindow) return false;
    if (sunriseMin < sunsetMin) return mins >= sunriseMin && mins < sunsetMin;
    return mins >= sunriseMin || mins < sunsetMin;
  };

  const dayHora = hasValidSunWindow
    ? horaTable.filter((h) => isDayStart(h.start))
    : horaTable.slice(0, Math.ceil(horaTable.length / 2));
  const nightHora = hasValidSunWindow
    ? horaTable.filter((h) => !isDayStart(h.start))
    : horaTable.slice(Math.ceil(horaTable.length / 2));

  // Get quality color
  const getQualityColor = (type: string) => {
    if (type.toLowerCase().includes('good') || type === 'शुभ') return 'text-green-500 bg-green-500/10';
    if (type.toLowerCase().includes('bad') || type === 'अशुभ') return 'text-red-500 bg-red-500/10';
    return 'text-yellow-500 bg-yellow-500/10';
  };

  // Get lord icon
  const getLordIcon = (lord: string) => {
    const sunPlanets = ['Sun', 'सूर्य', 'Mars', 'मंगल', 'Jupiter', 'गुरु', 'Saturn', 'शनि'];
    return sunPlanets.includes(lord) ? Sun : Moon;
  };

  return (
    <div className="space-y-3">
      {/* Current Hora */}
      {currentHora && (
        <div className="flex items-center gap-3 p-2 rounded-lg border border-sacred-gold/30 bg-sacred-gold/10">
          <Clock className="h-8 w-8 text-sacred-gold flex-shrink-0" />
          <div className="flex-1 min-w-0">
            <p className="text-xs text-muted-foreground">
              {t('auto.currentHora')}
            </p>
            <span className="font-bold text-foreground">
              {language === 'hi' ? currentHora.hora_hindi || currentHora.hora : currentHora.hora}
            </span>
            <span className="mx-2 text-sacred-gold">{currentHora.start} - {currentHora.end}</span>
            <Text variant="muted" as="span">
              {t('auto.lord')}: {language === 'hi' ? currentHora.lord_hindi || currentHora.lord : currentHora.lord}
            </Text>
          </div>
          <span className={`px-2 py-1 rounded-full text-xs font-semibold ${getQualityColor(currentHora.type)}`}>
            {language === 'hi' ? currentHora.type_hindi || currentHora.type : currentHora.type}
          </span>
        </div>
      )}

      {/* Day + Night tables side-by-side */}
      <div className="rounded-lg border overflow-hidden">
        <div className="flex flex-col md:flex-row divide-y md:divide-y-0 md:divide-x divide-border">
          <div className="flex-1 p-2">
            <h3 className="font-bold text-foreground mb-1 flex items-center gap-1">
              <Sun className="h-4 w-4 text-orange-500" />
              {t('auto.dayHora')}
            </h3>
            <Table className="w-full table-fixed text-xs sm:text-sm">
              <TableHeader>
                <TableRow className="bg-sacred-gold/15">
                  <TableHead className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[25%]">{t('auto.hora')}</TableHead>
                  <TableHead className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[23%]">{t('auto.lord')}</TableHead>
                  <TableHead className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[30%]">{t('auto.time')}</TableHead>
                  <TableHead className="text-center px-2 py-1 text-sacred-gold-dark font-semibold w-[22%]">{t('auto.result')}</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {dayHora.map((hora, index) => {
                  const isCurrent = currentHora?.start === hora.start && currentHora?.end === hora.end;
                  const LordIcon = getLordIcon(hora.lord);
                  return (
                    <TableRow key={`day-${index}`} className={`border-b border/50 last:border-0 ${isCurrent ? 'bg-sacred-gold/10' : ''}`}>
                      <TableCell className="px-2 py-1">
                        <div className="flex items-center gap-1">
                          <LordIcon className={`h-3 w-3 ${hora.type.toLowerCase().includes('good') ? 'text-yellow-500' : 'text-slate-400'}`} />
                          <span className={`font-medium whitespace-normal break-words ${isCurrent ? 'text-sacred-gold' : 'text-foreground'}`}>
                            {language === 'hi' ? hora.hora_hindi || hora.hora : hora.hora}
                          </span>
                        </div>
                      </TableCell>
                      <TableCell className="px-2 py-1 text-muted-foreground whitespace-normal break-words">{language === 'hi' ? hora.lord_hindi || hora.lord : hora.lord}</TableCell>
                      <TableCell className="px-2 py-1 text-muted-foreground whitespace-normal break-words">{hora.start} - {hora.end}</TableCell>
                      <TableCell className="px-2 py-1 text-center">
                        <span className={`inline-flex items-center px-1.5 py-0.5 rounded-full text-[10px] sm:text-xs font-medium ${getQualityColor(hora.type)}`}>
                          {language === 'hi' ? hora.type_hindi || hora.type : hora.type}
                        </span>
                      </TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          </div>

          <div className="flex-1 p-2">
            <h3 className="font-bold text-foreground mb-1 flex items-center gap-1">
              <Moon className="h-4 w-4 text-indigo-400" />
              {t('auto.nightHora')}
            </h3>
            <Table className="w-full table-fixed text-xs sm:text-sm">
              <TableHeader>
                <TableRow className="bg-sacred-gold/15">
                  <TableHead className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[25%]">{t('auto.hora')}</TableHead>
                  <TableHead className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[23%]">{t('auto.lord')}</TableHead>
                  <TableHead className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[30%]">{t('auto.time')}</TableHead>
                  <TableHead className="text-center px-2 py-1 text-sacred-gold-dark font-semibold w-[22%]">{t('auto.result')}</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {nightHora.map((hora, index) => {
                  const isCurrent = currentHora?.start === hora.start && currentHora?.end === hora.end;
                  const LordIcon = getLordIcon(hora.lord);
                  return (
                    <TableRow key={`night-${index}`} className={`border-b border/50 last:border-0 ${isCurrent ? 'bg-sacred-gold/10' : ''}`}>
                      <TableCell className="px-2 py-1">
                        <div className="flex items-center gap-1">
                          <LordIcon className={`h-3 w-3 ${hora.type.toLowerCase().includes('good') ? 'text-yellow-500' : 'text-slate-400'}`} />
                          <span className={`font-medium whitespace-normal break-words ${isCurrent ? 'text-sacred-gold' : 'text-foreground'}`}>
                            {language === 'hi' ? hora.hora_hindi || hora.hora : hora.hora}
                          </span>
                        </div>
                      </TableCell>
                      <TableCell className="px-2 py-1 text-muted-foreground whitespace-normal break-words">{language === 'hi' ? hora.lord_hindi || hora.lord : hora.lord}</TableCell>
                      <TableCell className="px-2 py-1 text-muted-foreground whitespace-normal break-words">{hora.start} - {hora.end}</TableCell>
                      <TableCell className="px-2 py-1 text-center">
                        <span className={`inline-flex items-center px-1.5 py-0.5 rounded-full text-[10px] sm:text-xs font-medium ${getQualityColor(hora.type)}`}>
                          {language === 'hi' ? hora.type_hindi || hora.type : hora.type}
                        </span>
                      </TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          </div>
        </div>
      </div>

      {/* Hora Info */}
      <div className="rounded-lg border p-2">
        <div className="flex items-start gap-2">
          <AlertCircle className="h-4 w-4 text-sacred-gold mt-0.5 flex-shrink-0" />
          <div>
            <Heading as={4} variant={4}>
              {t('auto.aboutHora')}
            </Heading>
            <p className="text-sm text-muted-foreground leading-relaxed">
              {t('auto.horaIs124thPartOfADa')}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}