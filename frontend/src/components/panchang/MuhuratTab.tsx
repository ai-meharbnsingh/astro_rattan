import { AlertTriangle, CheckCircle2, Sparkles, Sunrise } from 'lucide-react';
import type { FullPanchangData } from '@/sections/Panchang';

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
          <h3 className="font-bold text-cosmic-text-primary mb-1 flex items-center gap-1">
            <CheckCircle2 className="h-4 w-4" />
            {t('auto.auspiciousMuhuratsGo')}
          </h3>
          <table className="w-full table-fixed text-xs sm:text-sm">
            <thead>
              <tr className="bg-green-500/15">
                <th className="text-left px-2 py-1 text-green-700 font-semibold w-[28%]">{t('auto.muhurta')}</th>
                <th className="text-left px-2 py-1 text-green-700 font-semibold w-[18%]">{t('auto.start')}</th>
                <th className="text-left px-2 py-1 text-green-700 font-semibold w-[18%]">{t('auto.end')}</th>
                <th className="text-left px-2 py-1 text-green-700 font-semibold w-[36%]">{t('auto.notes')}</th>
              </tr>
            </thead>
            <tbody>
              {auspiciousPeriods.map((period) => (
                <tr key={period.key} className="border-b border-cosmic-border/50 last:border-0 align-top">
                  <td className="px-2 py-1 font-medium text-cosmic-text-primary whitespace-normal break-words">{period.name}</td>
                  <td className="px-2 py-1 text-cosmic-text-primary">{period.period?.start || '--'}</td>
                  <td className="px-2 py-1 text-cosmic-text-primary">{period.period?.end || '--'}</td>
                  <td className="px-2 py-1 text-cosmic-text-secondary whitespace-normal break-words">{period.desc}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="rounded-lg border border-red-500/30 p-2">
          <h3 className="font-bold text-cosmic-text-primary mb-1 flex items-center gap-1">
            <AlertTriangle className="h-4 w-4" />
            {t('auto.inauspiciousTimesAvo')}
          </h3>
          <table className="w-full table-fixed text-xs sm:text-sm">
            <thead>
              <tr className="bg-red-500/15">
                <th className="text-left px-2 py-1 text-red-700 font-semibold w-[28%]">{t('auto.period')}</th>
                <th className="text-left px-2 py-1 text-red-700 font-semibold w-[18%]">{t('auto.start')}</th>
                <th className="text-left px-2 py-1 text-red-700 font-semibold w-[18%]">{t('auto.end')}</th>
                <th className="text-left px-2 py-1 text-red-700 font-semibold w-[36%]">{t('auto.notes')}</th>
              </tr>
            </thead>
            <tbody>
              {inauspiciousPeriods.map((period) => (
                <tr key={period.key} className="border-b border-cosmic-border/50 last:border-0 align-top">
                  <td className="px-2 py-1 font-medium text-cosmic-text-primary whitespace-normal break-words">{period.name}</td>
                  <td className="px-2 py-1 text-cosmic-text-primary">{period.period?.start || '--'}</td>
                  <td className="px-2 py-1 text-cosmic-text-primary">{period.period?.end || '--'}</td>
                  <td className="px-2 py-1 text-cosmic-text-secondary whitespace-normal break-words">{period.desc}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-3">
        {specialYogas.length > 0 && (
          <div className="rounded-lg border border-sacred-gold/30 p-2">
            <h3 className="font-bold text-cosmic-text-primary mb-1 flex items-center gap-1">
              <Sparkles className="h-4 w-4" />
              {t('auto.specialYogas')}
            </h3>
            <table className="w-full table-fixed text-xs sm:text-sm">
              <thead>
                <tr className="bg-sacred-gold/15">
                  <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[30%]">{t('auto.yoga')}</th>
                  <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[20%]">{t('auto.start')}</th>
                  <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[20%]">{t('auto.end')}</th>
                  <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[30%]">{t('auto.status')}</th>
                </tr>
              </thead>
              <tbody>
                {specialYogas.map((yoga) => (
                  <tr key={yoga.key} className="border-b border-cosmic-border/50 last:border-0 align-top">
                    <td className="px-2 py-1 font-medium text-cosmic-text-primary whitespace-normal break-words">{yoga.name}</td>
                    <td className="px-2 py-1 text-cosmic-text-primary">{yoga.data?.start || '--'}</td>
                    <td className="px-2 py-1 text-cosmic-text-primary">{yoga.data?.end || '--'}</td>
                    <td className="px-2 py-1 text-green-600 whitespace-normal break-words">
                      {t('auto.activeToday')}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {sandhyaRows.length > 0 && (
          <div className="rounded-lg border border-cosmic-border p-2">
            <h3 className="font-bold text-cosmic-text-primary mb-1 flex items-center gap-1">
              <Sunrise className="h-4 w-4 text-orange-500" />
              {t('auto.sandhyaTimes')}
            </h3>
            <table className="w-full table-fixed text-xs sm:text-sm">
              <thead>
                <tr className="bg-sacred-gold/15">
                  <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[28%]">{t('auto.period')}</th>
                  <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[18%]">{t('auto.start')}</th>
                  <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[18%]">{t('auto.end')}</th>
                  <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[36%]">{t('auto.notes')}</th>
                </tr>
              </thead>
              <tbody>
                {sandhyaRows.map((row) => (
                  <tr key={row.key} className="border-b border-cosmic-border/50 last:border-0 align-top">
                    <td className="px-2 py-1 font-medium text-cosmic-text-primary whitespace-normal break-words">{row.name}</td>
                    <td className="px-2 py-1 text-cosmic-text-primary">{row.period?.start || '--'}</td>
                    <td className="px-2 py-1 text-cosmic-text-primary">{row.period?.end || '--'}</td>
                    <td className="px-2 py-1 text-cosmic-text-secondary whitespace-normal break-words">{row.desc}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
