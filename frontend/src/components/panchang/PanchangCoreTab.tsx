import type { FullPanchangData } from '@/sections/Panchang';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/table";

interface Props {
  panchang: FullPanchangData;
  language: string;
  t: (key: string) => string;
}

export default function PanchangCoreTab({ panchang, language, t }: Props) {
  const coreRows = [
    {
      metric: language === 'hi' ? 'तिथि' : t('panchang.tithi'),
      value: language === 'hi' ? panchang.tithi.name_hindi || panchang.tithi.name : panchang.tithi.name,
      details: `${t('auto.no')} ${panchang.tithi.number} • ${language === 'hi' ? panchang.tithi.paksha_hindi || panchang.tithi.paksha : panchang.tithi.paksha}`,
      endTime: panchang.tithi.end_time || '--',
    },
    {
      metric: language === 'hi' ? 'नक्षत्र' : t('panchang.nakshatra'),
      value: language === 'hi' ? panchang.nakshatra.name_hindi || panchang.nakshatra.name : panchang.nakshatra.name,
      details: `${t('auto.pada')} ${panchang.nakshatra.pada} • ${t('auto.lord')} ${language === 'hi' ? panchang.nakshatra.lord_hindi || panchang.nakshatra.lord : panchang.nakshatra.lord}`,
      endTime: panchang.nakshatra.end_time || '--',
    },
    {
      metric: language === 'hi' ? 'योग' : t('panchang.yoga'),
      value: language === 'hi' ? panchang.yoga.name_hindi || panchang.yoga.name : panchang.yoga.name,
      details: `${t('auto.no')} ${panchang.yoga.number}`,
      endTime: panchang.yoga.end_time || '--',
    },
    {
      metric: language === 'hi' ? 'करण' : t('panchang.karana'),
      value: language === 'hi' ? panchang.karana.name_hindi || panchang.karana.name : panchang.karana.name,
      details: `${t('auto.no')} ${panchang.karana.number}`,
      endTime: panchang.karana.end_time || '--',
    },
  ];

  const sunMoonRows = [
    {
      metric: language === 'hi' ? 'सूर्योदय' : t('panchang.sunrise'),
      value: panchang.sunrise || '--',
      details: t('auto.dayStart'),
    },
    {
      metric: language === 'hi' ? 'सूर्यास्त' : t('panchang.sunset'),
      value: panchang.sunset || '--',
      details: t('auto.dayEnd'),
    },
    {
      metric: 'Moonrise',
      value: panchang.moonrise || '--',
      details: t('auto.moonRise'),
    },
    {
      metric: 'Moonset',
      value: panchang.moonset || '--',
      details: t('auto.moonSet'),
    },
  ];

  const dayRows = [
    {
      metric: t('auto.dayLength'),
      value: panchang.dinamana || '--',
      details: t('auto.totalDaylight'),
    },
    {
      metric: t('auto.nightLength'),
      value: panchang.ratrimana || '--',
      details: t('auto.totalNighttime'),
    },
    {
      metric: t('auto.midDay'),
      value: panchang.madhyahna || '--',
      details: t('auto.middleOfDay'),
    },
    {
      metric: t('auto.weekday'),
      value: language === 'hi' ? panchang.vaar?.name_hindi || panchang.vaar?.name || '--' : panchang.vaar?.name || '--',
      details: t('auto.dayName'),
    },
  ];

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-3">
      <div className="rounded-lg border p-2">
        <Table className="w-full table-fixed text-xs sm:text-sm">
          <TableHeader>
            <TableRow className="bg-sacred-gold/15">
              <TableHead className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[22%]">{t('auto.metric')}</TableHead>
              <TableHead className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[24%]">{t('auto.value')}</TableHead>
              <TableHead className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[34%]">{t('auto.details')}</TableHead>
              <TableHead className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[20%]">{t('auto.ends')}</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {coreRows.map((row) => (
              <TableRow key={row.metric} className="border-b border/50 last:border-0 align-top">
                <TableCell className="px-2 py-1 font-medium text-foreground whitespace-normal break-words">{row.metric}</TableCell>
                <TableCell className="px-2 py-1 text-foreground whitespace-normal break-words">{row.value}</TableCell>
                <TableCell className="px-2 py-1 text-muted-foreground whitespace-normal break-words">{row.details}</TableCell>
                <TableCell className="px-2 py-1 text-sacred-gold whitespace-normal break-words">{row.endTime}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>

      <div className="rounded-lg border p-2">
        <Table className="w-full table-fixed text-xs sm:text-sm">
          <TableHeader>
            <TableRow className="bg-sacred-gold/15">
              <TableHead className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[34%]">{t('auto.metric')}</TableHead>
              <TableHead className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[28%]">{t('auto.value')}</TableHead>
              <TableHead className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[38%]">{t('auto.details')}</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {sunMoonRows.map((row) => (
              <TableRow key={row.metric} className="border-b border/50 last:border-0 align-top">
                <TableCell className="px-2 py-1 font-medium text-foreground whitespace-normal break-words">{row.metric}</TableCell>
                <TableCell className="px-2 py-1 text-foreground whitespace-normal break-words">{row.value}</TableCell>
                <TableCell className="px-2 py-1 text-muted-foreground whitespace-normal break-words">{row.details}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>

      <div className="rounded-lg border p-2">
        <Table className="w-full table-fixed text-xs sm:text-sm">
          <TableHeader>
            <TableRow className="bg-sacred-gold/15">
              <TableHead className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[34%]">{t('auto.metric')}</TableHead>
              <TableHead className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[28%]">{t('auto.value')}</TableHead>
              <TableHead className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[38%]">{t('auto.details')}</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {dayRows.map((row) => (
              <TableRow key={row.metric} className="border-b border/50 last:border-0 align-top">
                <TableCell className="px-2 py-1 font-medium text-foreground whitespace-normal break-words">{row.metric}</TableCell>
                <TableCell className="px-2 py-1 text-foreground whitespace-normal break-words">{row.value}</TableCell>
                <TableCell className="px-2 py-1 text-muted-foreground whitespace-normal break-words">{row.details}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}