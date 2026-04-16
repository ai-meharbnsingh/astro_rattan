import { AlertTriangle, CheckCircle2, Sparkles, Sunrise, Compass, Clover, CircleAlert, Clock } from 'lucide-react';
import type { FullPanchangData } from '@/sections/Panchang';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/table";

/* ------------------------------------------------------------------ */
/*  Extended API types (new fields not yet in FullPanchangData)        */
/* ------------------------------------------------------------------ */
interface SpecialYogaEntry {
  active: boolean;
  type?: string;
  name?: string;
  name_hindi?: string;
  nakshatra?: string;
}
interface DirectionsData {
  disha_shool?: { direction: string; direction_hindi: string; name: string; name_hindi: string };
  baana?: { element: string; element_hindi: string; direction: string; direction_hindi: string };
  anandadi_yoga?: { name: string; name_hindi: string; auspicious: boolean; index: number };
  lucky?: { color: string; color_hindi: string; number: number; direction: string; direction_hindi: string };
}
interface EkadashiParana {
  name: string; name_hindi: string; start: string; end: string; note: string; note_hindi: string;
}
interface PanchakaRahita {
  active?: boolean;
  [key: string]: any;
}
interface ExtPanchang extends FullPanchangData {
  special_yogas?: Record<string, SpecialYogaEntry>;
  directions?: DirectionsData;
  ekadashi_parana?: EkadashiParana | null;
  misc?: { panchaka_rahita?: PanchakaRahita | null; astronomical?: Record<string, any> };
  nivas?: {
    chandra_vasa?: { direction: string; direction_hindi: string; name: string; name_hindi: string };
    agnivasa?: { location: string; location_hindi: string; name: string; name_hindi: string };
    rahu_vasa?: { direction: string; direction_hindi: string; name: string; name_hindi: string };
    shivavasa?: { location: string; location_hindi: string; name: string; name_hindi: string };
    homahuti?: { planet: string; planet_hindi: string; name: string; name_hindi: string };
    kumbha_chakra?: { body_part: string; body_part_hindi: string; auspicious: boolean; name: string; name_hindi: string };
  };
  tamil?: {
    tamil_yoga?: { name: string; name_hindi: string; auspicious: boolean };
    jeevanama?: { status: string; status_hindi: string; favorable: boolean };
    netrama?: { status: string; status_hindi: string; favorable: boolean };
  };
}

interface Props {
  panchang: FullPanchangData;
  language: string;
  t: (key: string) => string;
}

export default function MuhuratTab({ panchang: _panchang, language, t }: Props) {
  const panchang = _panchang as ExtPanchang;
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

      {/* ============================================================ */}
      {/*  NEW: Special Active Yogas Banner                            */}
      {/* ============================================================ */}
      {(() => {
        const sy = panchang.special_yogas;
        if (!sy) return null;
        const badges: { label: string; color: string }[] = [];
        if (sy.sarvartha_siddhi?.active)
          badges.push({
            label: language === 'hi' ? (sy.sarvartha_siddhi.name_hindi || 'सर्वार्थ सिद्धि योग') : (sy.sarvartha_siddhi.name || 'Sarvartha Siddhi Yoga'),
            color: 'bg-yellow-500/20 text-yellow-700 border-yellow-500/40',
          });
        if (sy.amrit_siddhi?.active)
          badges.push({
            label: language === 'hi' ? (sy.amrit_siddhi.name_hindi || 'अमृत सिद्धि योग') : (sy.amrit_siddhi.name || 'Amrit Siddhi Yoga'),
            color: 'bg-yellow-500/20 text-yellow-700 border-yellow-500/40',
          });
        if (sy.dwipushkar?.active)
          badges.push({
            label: language === 'hi' ? (sy.dwipushkar.name_hindi || 'द्विपुष्कर योग') : (sy.dwipushkar.name || 'Dwipushkar Yoga'),
            color: 'bg-blue-500/20 text-blue-700 border-blue-500/40',
          });
        if (sy.tripushkar?.active)
          badges.push({
            label: language === 'hi' ? (sy.tripushkar.name_hindi || 'त्रिपुष्कर योग') : (sy.tripushkar.name || 'Tripushkar Yoga'),
            color: 'bg-blue-500/20 text-blue-700 border-blue-500/40',
          });
        if (sy.ganda_moola?.active)
          badges.push({
            label: language === 'hi' ? (sy.ganda_moola.name_hindi || 'गण्ड मूल') : (sy.ganda_moola.name || 'Ganda Moola'),
            color: 'bg-red-500/20 text-red-700 border-red-500/40',
          });
        if (badges.length === 0) return null;
        return (
          <div className="flex flex-wrap gap-2">
            {badges.map((b, i) => (
              <span
                key={i}
                className={`inline-flex items-center gap-1 rounded-full border px-3 py-1 text-xs font-semibold ${b.color}`}
              >
                <Sparkles className="h-3 w-3" />
                {b.label}
              </span>
            ))}
          </div>
        );
      })()}

      {/* ============================================================ */}
      {/*  NEW: Anandadi Yoga + Disha Shool + Lucky + Ekadashi Parana  */}
      {/* ============================================================ */}
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-3">
        {/* --- Anandadi Yoga --- */}
        {panchang.directions?.anandadi_yoga && (
          <div className="rounded-lg border p-3">
            <h4 className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-2 flex items-center gap-1">
              <Sparkles className="h-3.5 w-3.5" />
              {language === 'hi' ? 'आनन्दादि योग' : 'Anandadi Yoga'}
            </h4>
            <p className="text-sm font-bold text-foreground">
              {language === 'hi'
                ? panchang.directions.anandadi_yoga.name_hindi
                : panchang.directions.anandadi_yoga.name}
            </p>
            <div className="mt-1 flex items-center gap-2 text-xs">
              <span
                className={`inline-block h-2.5 w-2.5 rounded-full ${
                  panchang.directions.anandadi_yoga.auspicious ? 'bg-green-500' : 'bg-red-500'
                }`}
              />
              <span className={panchang.directions.anandadi_yoga.auspicious ? 'text-green-600' : 'text-red-600'}>
                {panchang.directions.anandadi_yoga.auspicious
                  ? (language === 'hi' ? 'शुभ' : 'Auspicious')
                  : (language === 'hi' ? 'अशुभ' : 'Inauspicious')}
              </span>
              <span className="text-muted-foreground">
                #{panchang.directions.anandadi_yoga.index}
              </span>
            </div>
          </div>
        )}

        {/* --- Disha Shool --- */}
        {panchang.directions?.disha_shool && (
          <div className="rounded-lg border border-red-500/30 bg-red-500/5 p-3">
            <h4 className="text-xs font-semibold text-red-600 uppercase tracking-wide mb-2 flex items-center gap-1">
              <Compass className="h-3.5 w-3.5" />
              {language === 'hi'
                ? (panchang.directions.disha_shool.name_hindi || 'दिशा शूल')
                : (panchang.directions.disha_shool.name || 'Disha Shool')}
            </h4>
            <p className="text-sm font-bold text-red-700">
              {language === 'hi'
                ? panchang.directions.disha_shool.direction_hindi
                : panchang.directions.disha_shool.direction}
            </p>
            <p className="mt-1 text-xs text-red-600/80">
              {language === 'hi' ? 'इस दिशा में यात्रा वर्जित' : 'Avoid travel in this direction'}
            </p>
          </div>
        )}

        {/* --- Lucky Indicators --- */}
        {panchang.directions?.lucky && (
          <div className="rounded-lg border border-sacred-gold/30 bg-sacred-gold/5 p-3">
            <h4 className="text-xs font-semibold text-sacred-gold-dark uppercase tracking-wide mb-2 flex items-center gap-1">
              <Clover className="h-3.5 w-3.5" />
              {language === 'hi' ? 'शुभ संकेत' : 'Lucky Indicators'}
            </h4>
            <div className="space-y-1 text-sm">
              <div className="flex justify-between">
                <span className="text-muted-foreground">{language === 'hi' ? 'रंग' : 'Color'}</span>
                <span className="font-medium text-foreground">
                  {language === 'hi' ? panchang.directions.lucky.color_hindi : panchang.directions.lucky.color}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">{language === 'hi' ? 'अंक' : 'Number'}</span>
                <span className="font-medium text-foreground">{panchang.directions.lucky.number}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">{language === 'hi' ? 'दिशा' : 'Direction'}</span>
                <span className="font-medium text-foreground">
                  {language === 'hi' ? panchang.directions.lucky.direction_hindi : panchang.directions.lucky.direction}
                </span>
              </div>
            </div>
          </div>
        )}

        {/* --- Ekadashi Parana --- */}
        {panchang.ekadashi_parana && (
          <div className="rounded-lg border border-green-500/30 bg-green-500/5 p-3">
            <h4 className="text-xs font-semibold text-green-700 uppercase tracking-wide mb-2 flex items-center gap-1">
              <Clock className="h-3.5 w-3.5" />
              {language === 'hi'
                ? (panchang.ekadashi_parana.name_hindi || 'एकादशी पारण')
                : (panchang.ekadashi_parana.name || 'Ekadashi Parana')}
            </h4>
            <p className="text-sm font-bold text-green-700">
              {panchang.ekadashi_parana.start} &ndash; {panchang.ekadashi_parana.end}
            </p>
            {(panchang.ekadashi_parana.note || panchang.ekadashi_parana.note_hindi) && (
              <p className="mt-1 text-xs text-green-600/80">
                {language === 'hi' ? panchang.ekadashi_parana.note_hindi : panchang.ekadashi_parana.note}
              </p>
            )}
          </div>
        )}
      </div>

      {/* ============================================================ */}
      {/*  NEW: Panchaka Warning Banner                                */}
      {/* ============================================================ */}
      {panchang.misc?.panchaka_rahita?.active && (
        <div className="rounded-lg border border-orange-500/40 bg-orange-500/10 p-3 flex items-start gap-2">
          <CircleAlert className="h-4 w-4 text-orange-600 mt-0.5 flex-shrink-0" />
          <div>
            <p className="text-sm font-semibold text-orange-700">
              {language === 'hi' ? 'पंचक काल सक्रिय' : 'Panchaka Period Active'}
            </p>
            <p className="text-xs text-orange-600/80 mt-0.5">
              {language === 'hi'
                ? 'पंचक काल में शुभ कार्य वर्जित माने जाते हैं'
                : 'Auspicious activities are generally avoided during Panchaka'}
            </p>
          </div>
        </div>
      )}

      {/* ============================================================ */}
      {/*  Tamil Yoga & Status (Jeevanama / Netrama)                   */}
      {/* ============================================================ */}
      {panchang.tamil && (panchang.tamil.tamil_yoga || panchang.tamil.jeevanama || panchang.tamil.netrama) && (
        <div>
          <h3 className="text-sm font-bold text-sacred-gold uppercase tracking-wider mb-2">
            {language === 'hi' ? 'तमिल योग एवं स्थिति' : 'Tamil Yoga & Status'}
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            {/* Tamil Yoga */}
            {panchang.tamil.tamil_yoga && (
              <div className="rounded-lg border p-3 space-y-1">
                <h4 className="text-xs font-semibold text-muted-foreground uppercase tracking-wide">
                  {language === 'hi' ? 'तमिल योग' : 'Tamil Yoga'}
                </h4>
                <p className="text-sm font-bold text-foreground">
                  {language === 'hi' ? panchang.tamil.tamil_yoga.name_hindi : panchang.tamil.tamil_yoga.name}
                </p>
                <div className="flex items-center gap-2 text-xs">
                  <span
                    className={`inline-block h-2.5 w-2.5 rounded-full ${
                      panchang.tamil.tamil_yoga.auspicious ? 'bg-green-500' : 'bg-red-500'
                    }`}
                  />
                  <span className={panchang.tamil.tamil_yoga.auspicious ? 'text-green-600' : 'text-red-600'}>
                    {panchang.tamil.tamil_yoga.auspicious
                      ? (language === 'hi' ? 'शुभ' : 'Auspicious')
                      : (language === 'hi' ? 'अशुभ' : 'Inauspicious')}
                  </span>
                </div>
              </div>
            )}

            {/* Jeevanama */}
            {panchang.tamil.jeevanama && (
              <div className="rounded-lg border p-3 space-y-1">
                <h4 className="text-xs font-semibold text-muted-foreground uppercase tracking-wide">
                  {language === 'hi' ? 'जीवनमा' : 'Jeevanama'}
                </h4>
                <p className="text-sm font-bold text-foreground">
                  {language === 'hi' ? panchang.tamil.jeevanama.status_hindi : panchang.tamil.jeevanama.status}
                </p>
                <div className="flex items-center gap-2 text-xs">
                  <span
                    className={`inline-block h-2.5 w-2.5 rounded-full ${
                      panchang.tamil.jeevanama.favorable ? 'bg-green-500' : 'bg-red-500'
                    }`}
                  />
                  <span className={panchang.tamil.jeevanama.favorable ? 'text-green-600' : 'text-red-600'}>
                    {panchang.tamil.jeevanama.favorable
                      ? (language === 'hi' ? 'अनुकूल' : 'Favorable')
                      : (language === 'hi' ? 'प्रतिकूल' : 'Unfavorable')}
                  </span>
                </div>
              </div>
            )}

            {/* Netrama */}
            {panchang.tamil.netrama && (
              <div className="rounded-lg border p-3 space-y-1">
                <h4 className="text-xs font-semibold text-muted-foreground uppercase tracking-wide">
                  {language === 'hi' ? 'नेत्रमा' : 'Netrama'}
                </h4>
                <p className="text-sm font-bold text-foreground">
                  {language === 'hi' ? panchang.tamil.netrama.status_hindi : panchang.tamil.netrama.status}
                </p>
                <div className="flex items-center gap-2 text-xs">
                  <span
                    className={`inline-block h-2.5 w-2.5 rounded-full ${
                      panchang.tamil.netrama.favorable ? 'bg-green-500' : 'bg-red-500'
                    }`}
                  />
                  <span className={panchang.tamil.netrama.favorable ? 'text-green-600' : 'text-red-600'}>
                    {panchang.tamil.netrama.favorable
                      ? (language === 'hi' ? 'अनुकूल' : 'Favorable')
                      : (language === 'hi' ? 'प्रतिकूल' : 'Unfavorable')}
                  </span>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* ============================================================ */}
      {/*  Nivas & Vasa (Chandra, Rahu, Shiva, Agni, Homahuti, Kumbha) */}
      {/* ============================================================ */}
      {panchang.nivas && (
        <div>
          <h3 className="text-sm font-bold text-sacred-gold uppercase tracking-wider mb-2">
            {language === 'hi' ? 'निवास एवं वास' : 'Nivas & Vasa'}
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-3">
            {/* Chandra Vasa */}
            {panchang.nivas.chandra_vasa && (
              <div className="rounded-lg border p-3 space-y-1">
                <h4 className="text-xs font-semibold text-muted-foreground uppercase tracking-wide">
                  {language === 'hi'
                    ? (panchang.nivas.chandra_vasa.name_hindi || 'चन्द्र वास')
                    : (panchang.nivas.chandra_vasa.name || 'Chandra Vasa')}
                </h4>
                <p className="text-sm font-bold text-foreground">
                  {language === 'hi'
                    ? panchang.nivas.chandra_vasa.direction_hindi
                    : panchang.nivas.chandra_vasa.direction}
                </p>
                <p className="text-xs text-muted-foreground">
                  {language === 'hi' ? 'चन्द्रमा की दिशा' : 'Moon direction'}
                </p>
              </div>
            )}

            {/* Rahu Vasa */}
            {panchang.nivas.rahu_vasa && (
              <div className="rounded-lg border border-red-500/30 bg-red-500/5 p-3 space-y-1">
                <h4 className="text-xs font-semibold text-red-600 uppercase tracking-wide">
                  {language === 'hi'
                    ? (panchang.nivas.rahu_vasa.name_hindi || 'राहु वास')
                    : (panchang.nivas.rahu_vasa.name || 'Rahu Vasa')}
                </h4>
                <p className="text-sm font-bold text-red-700">
                  {language === 'hi'
                    ? panchang.nivas.rahu_vasa.direction_hindi
                    : panchang.nivas.rahu_vasa.direction}
                </p>
                <p className="text-xs text-red-600/80">
                  {language === 'hi' ? 'राहु की दिशा — सावधान' : 'Rahu direction — caution'}
                </p>
              </div>
            )}

            {/* Shivavasa */}
            {panchang.nivas.shivavasa && (
              <div className="rounded-lg border p-3 space-y-1">
                <h4 className="text-xs font-semibold text-muted-foreground uppercase tracking-wide">
                  {language === 'hi'
                    ? (panchang.nivas.shivavasa.name_hindi || 'शिव वास')
                    : (panchang.nivas.shivavasa.name || 'Shivavasa')}
                </h4>
                <p className="text-sm font-bold text-foreground">
                  {language === 'hi'
                    ? panchang.nivas.shivavasa.location_hindi
                    : panchang.nivas.shivavasa.location}
                </p>
                <p className="text-xs text-muted-foreground">
                  {language === 'hi' ? 'शिव का निवास' : "Shiva's abode"}
                </p>
              </div>
            )}

            {/* Agnivasa */}
            {panchang.nivas.agnivasa && (
              <div className="rounded-lg border p-3 space-y-1">
                <h4 className="text-xs font-semibold text-muted-foreground uppercase tracking-wide">
                  {language === 'hi'
                    ? (panchang.nivas.agnivasa.name_hindi || 'अग्नि वास')
                    : (panchang.nivas.agnivasa.name || 'Agnivasa')}
                </h4>
                <p className="text-sm font-bold text-foreground">
                  {language === 'hi'
                    ? panchang.nivas.agnivasa.location_hindi
                    : panchang.nivas.agnivasa.location}
                </p>
                <p className="text-xs text-muted-foreground">
                  {language === 'hi' ? 'अग्नि का स्थान' : 'Fire location'}
                </p>
              </div>
            )}

            {/* Homahuti */}
            {panchang.nivas.homahuti && (
              <div className="rounded-lg border p-3 space-y-1">
                <h4 className="text-xs font-semibold text-muted-foreground uppercase tracking-wide">
                  {language === 'hi'
                    ? (panchang.nivas.homahuti.name_hindi || 'होमाहुति')
                    : (panchang.nivas.homahuti.name || 'Homahuti')}
                </h4>
                <p className="text-sm font-bold text-foreground">
                  {language === 'hi'
                    ? panchang.nivas.homahuti.planet_hindi
                    : panchang.nivas.homahuti.planet}
                </p>
                <p className="text-xs text-muted-foreground">
                  {language === 'hi' ? 'होम हेतु ग्रह' : 'Planet for homa'}
                </p>
              </div>
            )}

            {/* Kumbha Chakra */}
            {panchang.nivas.kumbha_chakra && (
              <div
                className={`rounded-lg border p-3 space-y-1 ${
                  panchang.nivas.kumbha_chakra.auspicious
                    ? 'border-green-500/30 bg-green-500/5'
                    : 'border-red-500/30 bg-red-500/5'
                }`}
              >
                <h4
                  className={`text-xs font-semibold uppercase tracking-wide ${
                    panchang.nivas.kumbha_chakra.auspicious ? 'text-green-700' : 'text-red-600'
                  }`}
                >
                  {language === 'hi'
                    ? (panchang.nivas.kumbha_chakra.name_hindi || 'कुम्भ चक्र')
                    : (panchang.nivas.kumbha_chakra.name || 'Kumbha Chakra')}
                </h4>
                <p
                  className={`text-sm font-bold ${
                    panchang.nivas.kumbha_chakra.auspicious ? 'text-green-700' : 'text-red-700'
                  }`}
                >
                  {language === 'hi'
                    ? panchang.nivas.kumbha_chakra.body_part_hindi
                    : panchang.nivas.kumbha_chakra.body_part}
                </p>
                <div className="flex items-center gap-2 text-xs">
                  <span
                    className={`inline-block h-2.5 w-2.5 rounded-full ${
                      panchang.nivas.kumbha_chakra.auspicious ? 'bg-green-500' : 'bg-red-500'
                    }`}
                  />
                  <span className={panchang.nivas.kumbha_chakra.auspicious ? 'text-green-600' : 'text-red-600'}>
                    {panchang.nivas.kumbha_chakra.auspicious
                      ? (language === 'hi' ? 'शुभ' : 'Auspicious')
                      : (language === 'hi' ? 'अशुभ' : 'Inauspicious')}
                  </span>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}