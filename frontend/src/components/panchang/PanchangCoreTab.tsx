import React from 'react';
import type { FullPanchangData } from '@/sections/Panchang';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/table";

// Nakshatra category badge colours (Muhurta Chintamani, Ch. 2)
const NAK_CAT_STYLES: Record<string, string> = {
  sthira:  'bg-blue-100 text-blue-700 border-blue-200',
  chara:   'bg-green-100 text-green-700 border-green-200',
  ugra:    'bg-red-100 text-red-700 border-red-200',
  mishra:  'bg-purple-100 text-purple-700 border-purple-200',
  laghu:   'bg-teal-100 text-teal-700 border-teal-200',
  mridu:   'bg-pink-100 text-pink-700 border-pink-200',
  tikshna: 'bg-orange-100 text-orange-700 border-orange-200',
};

interface Props {
  panchang: FullPanchangData;
  language: string;
  t: (key: string) => string;
}

export default function PanchangCoreTab({ panchang, language, t }: Props) {
  const l = (en: string, hi: string) => language === 'hi' ? hi : en;
  const isHi = language === 'hi';

  // Nakshatra category badge
  const nak = panchang.nakshatra as any;
  const nakCatKey: string = nak?.category || 'mishra';
  const nakCatLabel: string = isHi ? (nak?.category_hi || nakCatKey) : (nak?.category_en || nakCatKey);
  const nakGoodFor: string = isHi ? (nak?.category_good_for_hi || '') : (nak?.category_good_for_en || '');
  const nakBadgeStyle = NAK_CAT_STYLES[nakCatKey] ?? NAK_CAT_STYLES.mishra;

  const coreRows = [
    {
      metric: isHi ? 'तिथि' : t('panchang.tithi'),
      value: isHi ? panchang.tithi.name_hindi || panchang.tithi.name : panchang.tithi.name,
      details: `${t('auto.no')} ${panchang.tithi.number} • ${isHi ? panchang.tithi.paksha_hindi || panchang.tithi.paksha : panchang.tithi.paksha}`,
      endTime: panchang.tithi.end_time || '--',
      badge: null as React.ReactNode,
    },
    {
      metric: isHi ? 'नक्षत्र' : t('panchang.nakshatra'),
      value: isHi ? panchang.nakshatra.name_hindi || panchang.nakshatra.name : panchang.nakshatra.name,
      details: `${t('auto.pada')} ${panchang.nakshatra.pada} • ${t('auto.lord')} ${isHi ? panchang.nakshatra.lord_hindi || panchang.nakshatra.lord : panchang.nakshatra.lord}`,
      endTime: panchang.nakshatra.end_time || '--',
      badge: (
        <span title={nakGoodFor} className={`inline-block text-[10px] font-bold px-1.5 py-0.5 rounded border ${nakBadgeStyle} cursor-help`}>
          {nakCatLabel}
        </span>
      ),
    },
    {
      metric: isHi ? 'योग' : t('panchang.yoga'),
      value: isHi ? panchang.yoga.name_hindi || panchang.yoga.name : panchang.yoga.name,
      details: `${t('auto.no')} ${panchang.yoga.number}`,
      endTime: panchang.yoga.end_time || '--',
      badge: null as React.ReactNode,
    },
    {
      metric: isHi ? 'करण' : t('panchang.karana'),
      value: isHi ? panchang.karana.name_hindi || panchang.karana.name : panchang.karana.name,
      details: `${t('auto.no')} ${panchang.karana.number}`,
      endTime: panchang.karana.end_time || '--',
      badge: null as React.ReactNode,
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
      metric: l('Moonrise', 'चन्द्रोदय'),
      value: panchang.moonrise || '--',
      details: t('auto.moonRise'),
    },
    {
      metric: l('Moonset', 'चन्द्रास्त'),
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
    <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-2">
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
                <TableCell className="px-2 py-1 text-muted-foreground whitespace-normal break-words">
                  <span>{row.details}</span>
                  {row.badge && <span className="ml-1.5 align-middle">{row.badge}</span>}
                </TableCell>
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