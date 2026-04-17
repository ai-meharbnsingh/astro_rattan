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

// Tithi type badge (Muhurta Chintamani — 5 types, cycling every 5 tithis)
// 1,6,11=Nanda  2,7,12=Bhadra  3,8,13=Jaya  4,9,14=Rikta  5,10,15=Poorna
const TITHI_TYPES: Record<number, { name: string; nameHi: string; style: string; goodFor: string; goodForHi: string }> = {
  1: { name: 'Nanda',  nameHi: 'नन्दा',  style: 'bg-green-100 text-green-700 border-green-200',  goodFor: 'Joy, happiness, celebrations',    goodForHi: 'आनन्द, उत्सव, शुभ कार्य' },
  2: { name: 'Bhadra', nameHi: 'भद्रा',  style: 'bg-blue-100 text-blue-700 border-blue-200',     goodFor: 'Permanent, lasting activities',   goodForHi: 'स्थायी कार्य, घर निर्माण' },
  3: { name: 'Jaya',   nameHi: 'जया',    style: 'bg-purple-100 text-purple-700 border-purple-200', goodFor: 'Victory, confrontation, battles', goodForHi: 'विजय, प्रतिस्पर्धा, संघर्ष' },
  4: { name: 'Rikta',  nameHi: 'रिक्ता', style: 'bg-red-100 text-red-700 border-red-200',         goodFor: 'Avoid auspicious new work',       goodForHi: 'शुभ कार्य से बचें' },
  5: { name: 'Poorna', nameHi: 'पूर्णा', style: 'bg-amber-100 text-amber-700 border-amber-200',   goodFor: 'Completion, fulfilment',          goodForHi: 'पूर्णता, सिद्धि, तीर्थ' },
};

// Dagdha (burned) Tithi — weekday index (0=Mon…6=Sun) → tithi number to avoid
const DAGDHA_TITHIS: Record<number, number> = { 0: 7, 1: 12, 2: 3, 3: 11, 4: 6, 5: 9, 6: 2 };

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

  // Tithi type badge
  const tithiTypeIdx = ((panchang.tithi.number - 1) % 5) + 1;
  const tithiType = TITHI_TYPES[tithiTypeIdx];
  const tithiTypeBadge = tithiType ? (
    <span
      title={isHi ? tithiType.goodForHi : tithiType.goodFor}
      className={`inline-block text-[10px] font-bold px-1.5 py-0.5 rounded border ${tithiType.style} cursor-help`}
    >
      {isHi ? tithiType.nameHi : tithiType.name}
    </span>
  ) : null;

  // Yoga quality badge
  const yogaData = panchang.yoga as any;
  const yogaBadge = yogaData?.quality === 'bad' || yogaData?.auspicious === false ? (
    <span
      title={`${yogaData?.name || ''} — Yoga Dosha (inauspicious yoga)`}
      className="inline-block text-[10px] font-bold px-1.5 py-0.5 rounded border bg-red-100 text-red-700 border-red-200 cursor-help"
    >
      {isHi ? 'योग दोष' : 'Yoga Dosha'}
    </span>
  ) : (
    <span
      title={`${yogaData?.name || ''} — Shubha (auspicious yoga)`}
      className="inline-block text-[10px] font-bold px-1.5 py-0.5 rounded border bg-green-100 text-green-700 border-green-200 cursor-help"
    >
      {isHi ? 'शुभ' : 'Shubha'}
    </span>
  );

  // Karana quality badge
  const karanaData = panchang.karana as any;
  const karanaBadge = karanaData?.is_vishti === true ? (
    <span
      title="Inauspicious Karana — avoid new work"
      className="inline-block text-[10px] font-bold px-1.5 py-0.5 rounded border bg-red-100 text-red-700 border-red-200 cursor-help"
    >
      {isHi ? 'विष्टि/भद्रा' : 'Vishti/Bhadra'}
    </span>
  ) : karanaData?.type === 'sthira' ? (
    <span
      title={`${karanaData?.name || ''} — Sthira (fixed) Karana`}
      className="inline-block text-[10px] font-bold px-1.5 py-0.5 rounded border bg-slate-100 text-slate-600 border-slate-200 cursor-help"
    >
      {isHi ? 'स्थिर' : 'Sthira'}
    </span>
  ) : (
    <span
      title={`${karanaData?.name || ''} — Chara (moveable) Karana`}
      className="inline-block text-[10px] font-bold px-1.5 py-0.5 rounded border bg-blue-100 text-blue-600 border-blue-200 cursor-help"
    >
      {isHi ? 'चर' : 'Chara'}
    </span>
  );

  // Dagdha Tithi check (burned day — avoid all new auspicious work)
  const vaarNum = panchang.vaar?.number ?? -1;
  const dagdhaTithiNum = DAGDHA_TITHIS[vaarNum];
  const isDagdha = dagdhaTithiNum !== undefined && panchang.tithi.number === dagdhaTithiNum;

  const coreRows = [
    {
      metric: isHi ? 'तिथि' : t('panchang.tithi'),
      value: isHi ? panchang.tithi.name_hindi || panchang.tithi.name : panchang.tithi.name,
      details: `${t('auto.no')} ${panchang.tithi.number} • ${isHi ? panchang.tithi.paksha_hindi || panchang.tithi.paksha : panchang.tithi.paksha}`,
      endTime: panchang.tithi.end_time || '--',
      badge: tithiTypeBadge,
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
      badge: yogaBadge,
    },
    {
      metric: isHi ? 'करण' : t('panchang.karana'),
      value: isHi ? panchang.karana.name_hindi || panchang.karana.name : panchang.karana.name,
      details: `${t('auto.no')} ${panchang.karana.number}`,
      endTime: panchang.karana.end_time || '--',
      badge: karanaBadge,
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
    <div className="space-y-2">
    {/* Dagdha Tithi warning */}
    {isDagdha && (
      <div className="rounded-lg border border-red-500/40 bg-red-500/10 px-3 py-2 flex items-start gap-2">
        <span className="text-red-600 font-bold text-sm flex-shrink-0">⚠</span>
        <div>
          <p className="text-sm font-semibold text-red-700">
            {isHi ? 'दग्ध तिथि — जली हुई तिथि' : 'Dagdha Tithi — Burned Day'}
          </p>
          <p className="text-xs text-red-600/80 mt-0.5">
            {isHi
              ? 'आज दग्ध तिथि है। नए शुभ कार्य प्रारम्भ न करें।'
              : 'Today is a Dagdha (burned) Tithi. Avoid starting new auspicious work.'}
          </p>
        </div>
      </div>
    )}
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
    </div>
  );
}