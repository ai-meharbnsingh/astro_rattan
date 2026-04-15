import { AlertTriangle, CheckCircle2, Sparkles, Sunrise } from 'lucide-react';
import type { FullPanchangData } from '@/sections/Panchang';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/table";

interface Props {
  panchang: FullPanchangData;
  language: string;
  t: (key: string) => string;
}

export default function MuhuratTab({ panchang, language, t }: Props) {
  // Inauspicious periods
  const inauspiciousPeriods = [
    {
      key: 'rahu_kaal',
      name: t('auto.rahuKaal'),
      period: panchang.rahu_kaal,
      desc: t('auto.inauspiciousAvoidNew')
    },
    {
      key: 'gulika_kaal',
      name: t('auto.gulikaKaal'),
      period: panchang.gulika_kaal,
      desc: t('auto.mixedResults')
    },
    {
      key: 'yamaganda',
      name: t('auto.yamaganda'),
      period: panchang.yamaganda,
      desc: t('auto.yamaTimeAvoidTravel')
    },
    {
      key: 'dur_muhurtam',
      name: t('auto.durMuhurtam'),
      period: panchang.dur_muhurtam,
      desc: t('auto.highlyInauspicious')
    },
    {
      key: 'varjyam',
      name: t('auto.varjyam'),
      period: panchang.varjyam,
      desc: t('auto.prohibitedTime')
    },
  ].filter(p => p.period && (p.period.start !== '--:--' || p.period.end !== '--:--'));

  // Auspicious periods
  const auspiciousPeriods = [
    {
      key: 'brahma_muhurat',
      name: t('auto.brahmaMuhurat'),
      period: panchang.brahma_muhurat,
      desc: t('auto.mostAuspiciousMedita')
    },
    {
      key: 'abhijit_muhurat',
      name: t('auto.abhijitMuhurat'),
      period: panchang.abhijit_muhurat,
      desc: t('auto.victoryTimeAnyWorkSu')
    },
    {
      key: 'vijaya_muhurta',
      name: t('auto.vijayaMuhurta'),
      period: panchang.vijaya_muhurta,
      desc: t('auto.timeForVictory')
    },
    {
      key: 'godhuli_muhurta',
      name: t('auto.godhuliMuhurta'),
      period: panchang.godhuli_muhurta,
      desc: t('auto.whenCowsReturnAuspic')
    },
    {
      key: 'nishita_muhurta',
      name: t('auto.nishitaMuhurta'),
      period: panchang.nishita_muhurta,
      desc: t('auto.auspiciousNightTime')
    },
  ].filter(p => p.period && (p.period.start !== '--:--' || p.period.end !== '--:--'));

  // Special Yogas
  const specialYogas = [
    { key: 'ravi_yoga', name: t('auto.raviYoga'), data: panchang.ravi_yoga },
    { key: 'amrit_siddhi', name: t('auto.amritSiddhi'), data: panchang.amrit_siddhi },
    { key: 'sarvartha_siddhi', name: t('auto.sarvarthaSiddhi'), data: panchang.sarvartha_siddhi },
    { key: 'tripushkar', name: t('auto.tripushkar'), data: panchang.tripushkar },
    { key: 'dwipushkar', name: t('auto.dwipushkar'), data: panchang.dwipushkar },
  ].filter(y => y.data && (y.data.active || (y.data.start && y.data.end)));

  const sandhyaRows = [
    {
      key: 'pratah_sandhya',
      name: t('auto.pratahSandhya'),
      period: panchang.pratah_sandhya,
      desc: t('auto.timeForGayatriJapa'),
    },
    {
      key: 'sayahna_sandhya',
      name: t('auto.sayahnaSandhya'),
      period: panchang.sayahna_sandhya,
      desc: t('auto.timeForSandhyaJapa'),
    },
  ].filter(s => s.period && (s.period.start !== '--:--' || s.period.end !== '--:--'));

  return (
    <div className="space-y-3">
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-3">
        <div className="rounded-lg border border-green-500/30 p-2">
          <h3 className="font-bold text-foreground mb-1 flex items-center gap-1">
            <CheckCircle2 className="h-4 w-4" />
            {t('auto.auspiciousMuhuratsGo')}
          </h3>
          <Table className="w-full table-fixed text-xs sm:text-sm">
            <TableHeader>
              <TableRow className="bg-green-500/15">
                <TableHead className="text-left px-2 py-1 text-green-700 font-semibold w-[28%]">{t('auto.muhurta')}</TableHead>
                <TableHead className="text-left px-2 py-1 text-green-700 font-semibold w-[18%]">{t('auto.start')}</TableHead>
                <TableHead className="text-left px-2 py-1 text-green-700 font-semibold w-[18%]">{t('auto.end')}</TableHead>
                <TableHead className="text-left px-2 py-1 text-green-700 font-semibold w-[36%]">{t('auto.notes')}</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {auspiciousPeriods.map((period) => (
                <TableRow key={period.key} className="border-b border/50 last:border-0 align-top">
                  <TableCell className="px-2 py-1 font-medium text-foreground whitespace-normal break-words">{period.name}</TableCell>
                  <TableCell className="px-2 py-1 text-foreground">{period.period?.start || '--'}</TableCell>
                  <TableCell className="px-2 py-1 text-foreground">{period.period?.end || '--'}</TableCell>
                  <TableCell className="px-2 py-1 text-muted-foreground whitespace-normal break-words">{period.desc}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>

        <div className="rounded-lg border border-red-500/30 p-2">
          <h3 className="font-bold text-foreground mb-1 flex items-center gap-1">
            <AlertTriangle className="h-4 w-4" />
            {t('auto.inauspiciousTimesAvo')}
          </h3>
          <Table className="w-full table-fixed text-xs sm:text-sm">
            <TableHeader>
              <TableRow className="bg-red-500/15">
                <TableHead className="text-left px-2 py-1 text-red-700 font-semibold w-[28%]">{t('auto.period')}</TableHead>
                <TableHead className="text-left px-2 py-1 text-red-700 font-semibold w-[18%]">{t('auto.start')}</TableHead>
                <TableHead className="text-left px-2 py-1 text-red-700 font-semibold w-[18%]">{t('auto.end')}</TableHead>
                <TableHead className="text-left px-2 py-1 text-red-700 font-semibold w-[36%]">{t('auto.notes')}</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {inauspiciousPeriods.map((period) => (
                <TableRow key={period.key} className="border-b border/50 last:border-0 align-top">
                  <TableCell className="px-2 py-1 font-medium text-foreground whitespace-normal break-words">{period.name}</TableCell>
                  <TableCell className="px-2 py-1 text-foreground">{period.period?.start || '--'}</TableCell>
                  <TableCell className="px-2 py-1 text-foreground">{period.period?.end || '--'}</TableCell>
                  <TableCell className="px-2 py-1 text-muted-foreground whitespace-normal break-words">{period.desc}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-3">
        {specialYogas.length > 0 && (
          <div className="rounded-lg border border-sacred-gold/30 p-2">
            <h3 className="font-bold text-foreground mb-1 flex items-center gap-1">
              <Sparkles className="h-4 w-4" />
              {t('auto.specialYogas')}
            </h3>
            <Table className="w-full table-fixed text-xs sm:text-sm">
              <TableHeader>
                <TableRow className="bg-sacred-gold/15">
                  <TableHead className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[30%]">{t('auto.yoga')}</TableHead>
                  <TableHead className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[20%]">{t('auto.start')}</TableHead>
                  <TableHead className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[20%]">{t('auto.end')}</TableHead>
                  <TableHead className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[30%]">{t('auto.status')}</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {specialYogas.map((yoga) => (
                  <TableRow key={yoga.key} className="border-b border/50 last:border-0 align-top">
                    <TableCell className="px-2 py-1 font-medium text-foreground whitespace-normal break-words">{yoga.name}</TableCell>
                    <TableCell className="px-2 py-1 text-foreground">{yoga.data?.start || '--'}</TableCell>
                    <TableCell className="px-2 py-1 text-foreground">{yoga.data?.end || '--'}</TableCell>
                    <TableCell className="px-2 py-1 text-green-600 whitespace-normal break-words">
                      {t('auto.activeToday')}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        )}

        {sandhyaRows.length > 0 && (
          <div className="rounded-lg border p-2">
            <h3 className="font-bold text-foreground mb-1 flex items-center gap-1">
              <Sunrise className="h-4 w-4 text-orange-500" />
              {t('auto.sandhyaTimes')}
            </h3>
            <Table className="w-full table-fixed text-xs sm:text-sm">
              <TableHeader>
                <TableRow className="bg-sacred-gold/15">
                  <TableHead className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[28%]">{t('auto.period')}</TableHead>
                  <TableHead className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[18%]">{t('auto.start')}</TableHead>
                  <TableHead className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[18%]">{t('auto.end')}</TableHead>
                  <TableHead className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[36%]">{t('auto.notes')}</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {sandhyaRows.map((row) => (
                  <TableRow key={row.key} className="border-b border/50 last:border-0 align-top">
                    <TableCell className="px-2 py-1 font-medium text-foreground whitespace-normal break-words">{row.name}</TableCell>
                    <TableCell className="px-2 py-1 text-foreground">{row.period?.start || '--'}</TableCell>
                    <TableCell className="px-2 py-1 text-foreground">{row.period?.end || '--'}</TableCell>
                    <TableCell className="px-2 py-1 text-muted-foreground whitespace-normal break-words">{row.desc}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        )}
      </div>
    </div>
  );
}