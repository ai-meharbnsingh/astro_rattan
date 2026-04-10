import { useMemo } from 'react';
import { useTranslation } from '@/lib/i18n';
import {
  LayoutGrid,
  AlertTriangle,
  CheckCircle,
  Sparkles,
  Clock,
  Heart,
  Gift,
  Home,
  Zap,
} from 'lucide-react';
import type { LalKitabChartData } from './lalkitab-data';
import { PLANETS, AGE_PLANET_ACTIVATION, REMEDIES } from './lalkitab-data';

interface Props {
  chartData: LalKitabChartData;
  birthDate: string;
}

interface DoshaResult {
  key: string;
  nameEn: string;
  nameHi: string;
  detected: boolean;
  severity: 'high' | 'medium' | 'low';
  descEn: string;
  descHi: string;
  remedyEn: string;
  remedyHi: string;
}

const severityStyles: Record<DoshaResult['severity'], { badge: string; label: string }> = {
  high: { badge: 'bg-red-500/20 text-red-500', label: 'High' },
  medium: { badge: 'bg-orange-500/20 text-orange-500', label: 'Medium' },
  low: { badge: 'bg-yellow-500/20 text-yellow-600', label: 'Low' },
};

const typeIcons = {
  feeding: Heart,
  donation: Gift,
  household: Home,
  action: Zap,
} as const;

function getPlanetLabel(key: string, language: string): string {
  const planet = PLANETS.find((p) => p.key === key);
  if (!planet) return key;
  return language === 'hi' ? planet.hi : planet.en;
}

/** Return the planet dot color based on its key. */
function getPlanetDotColor(key: string): string {
  const colors: Record<string, string> = {
    Sun: 'bg-orange-400',
    Moon: 'bg-blue-300',
    Mars: 'bg-red-500',
    Mercury: 'bg-green-400',
    Jupiter: 'bg-yellow-400',
    Venus: 'bg-pink-400',
    Saturn: 'bg-indigo-400',
    Rahu: 'bg-gray-400',
    Ketu: 'bg-gray-600',
  };
  return colors[key] ?? 'bg-sacred-gold';
}

function calculateAge(birthDate: string): number {
  const birth = new Date(birthDate);
  const today = new Date();
  let age = today.getFullYear() - birth.getFullYear();
  const monthDiff = today.getMonth() - birth.getMonth();
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
    age--;
  }
  return age;
}

export default function LalKitabDashboardTab({ chartData, birthDate }: Props) {
  const { t, language } = useTranslation();
  const isHi = language === 'hi';

  // House counts
  const counts = useMemo(() => {
    let empty = 0;
    let strong = 0;
    let weak = 0;
    let totalPlanets = 0;
    for (const h of chartData.houses) {
      if (h.strength === 'empty') empty++;
      else if (h.strength === 'strong') strong++;
      else if (h.strength === 'weak') weak++;
      totalPlanets += h.planets.length;
    }
    return { empty, strong, weak, totalPlanets };
  }, [chartData.houses]);

  // Doshas
  const doshas: DoshaResult[] = (chartData as any).doshas ?? [];
  const detectedDoshas = useMemo(
    () => doshas.filter((d) => d.detected),
    [doshas],
  );

  // Quick remedies — urgent first, then daily, limited to 5
  const quickRemedies = useMemo(() => {
    const collected: { planet: string; house: number; remedy: any }[] = [];

    for (const planet of PLANETS) {
      const houseNumber = chartData.planetPositions[planet.key];
      if (houseNumber == null) continue;
      const planetRemedies = REMEDIES[planet.key]?.[houseNumber];
      if (!planetRemedies) continue;

      for (const r of planetRemedies) {
        collected.push({ planet: planet.key, house: houseNumber, remedy: r });
      }
    }

    // Sort: urgent first, then daily, then rest
    const priority: Record<string, number> = { urgent: 0, daily: 1, weekly: 2, general: 3 };
    collected.sort(
      (a, b) => (priority[a.remedy.category] ?? 9) - (priority[b.remedy.category] ?? 9),
    );

    return collected.slice(0, 5);
  }, [chartData]);

  // Timeline
  const age = useMemo(() => calculateAge(birthDate), [birthDate]);

  const timelinePeriods = useMemo(() => {
    if (!AGE_PLANET_ACTIVATION || AGE_PLANET_ACTIVATION.length === 0) return [];
    const sorted = [...AGE_PLANET_ACTIVATION].sort((a, b) => a.startAge - b.startAge);
    return sorted;
  }, []);

  const currentPeriodIndex = useMemo(() => {
    return timelinePeriods.findIndex(
      (p) => age >= p.startAge && age <= p.endAge,
    );
  }, [age, timelinePeriods]);

  // House grid for mini chart: rows 1-3, cols 1-4 (3x4 grid = 12 houses)
  const miniGridHouses = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center space-y-2">
        <h2 className="text-2xl font-sans font-bold text-sacred-gold flex items-center justify-center gap-2">
          <LayoutGrid className="w-6 h-6" />
          {t('lk.dashboard.title')}
        </h2>
        <p className="text-sm text-cosmic-text/70">{t('lk.dashboard.desc')}</p>
      </div>

      {/* 2x2 Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* ─── 1. Kundli Overview ─── */}
        <div className="card-sacred rounded-2xl p-6 border border-sacred-gold/20">
          <h3 className="font-sans text-lg font-semibold text-sacred-gold mb-4">
            {t('lk.dashboard.kundliView')}
          </h3>

          {/* Quick stats */}
          <div className="grid grid-cols-2 gap-3 mb-5">
            <div className="text-center p-3 rounded-xl bg-sacred-gold/5 border border-sacred-gold/10">
              <p className="text-2xl font-sans font-bold text-cosmic-text">
                {counts.totalPlanets}
              </p>
              <p className="text-sm text-cosmic-text/60">
                {isHi ? 'ग्रह' : 'Planets'}
              </p>
            </div>
            <div className="text-center p-3 rounded-xl bg-sacred-gold/5 border border-sacred-gold/10">
              <p className="text-2xl font-sans font-bold text-cosmic-text">
                {counts.empty}
              </p>
              <p className="text-sm text-cosmic-text/60">
                {isHi ? 'खाली भाव' : 'Empty'}
              </p>
            </div>
            <div className="text-center p-3 rounded-xl bg-green-500/5 border border-green-300/10">
              <p className="text-2xl font-sans font-bold text-green-400">
                {counts.strong}
              </p>
              <p className="text-sm text-cosmic-text/60">
                {isHi ? 'मजबूत' : 'Strong'}
              </p>
            </div>
            <div className="text-center p-3 rounded-xl bg-red-500/5 border border-red-300/10">
              <p className="text-2xl font-sans font-bold text-red-400">
                {counts.weak}
              </p>
              <p className="text-sm text-cosmic-text/60">
                {isHi ? 'कमजोर' : 'Weak'}
              </p>
            </div>
          </div>

          {/* Mini 3x4 grid */}
          <div className="grid grid-cols-4 gap-1.5">
            {miniGridHouses.map((houseNum) => {
              const house = chartData.houses.find((h) => h.house === houseNum);
              const planets = house?.planets ?? [];
              const planetAbbr: Record<string, string> = { Sun: 'Su', Moon: 'Mo', Mars: 'Ma', Mercury: 'Me', Jupiter: 'Ju', Venus: 'Ve', Saturn: 'Sa', Rahu: 'Ra', Ketu: 'Ke' };
              return (
                <div
                  key={houseNum}
                  className="relative flex flex-col items-center justify-center rounded-md border border-sacred-gold/15 bg-cosmic-card/40 p-2 min-h-[52px]"
                >
                  <span className="text-sm font-bold text-sacred-gold-dark">
                    {houseNum}
                  </span>
                  {planets.length > 0 && (
                    <div className="flex flex-wrap gap-0.5 justify-center mt-1">
                      {planets.map((pKey) => (
                        <span
                          key={pKey}
                          className={`text-sm font-semibold px-1 rounded ${getPlanetDotColor(pKey).replace('bg-', 'text-')}`}
                        >
                          {planetAbbr[pKey] || pKey.slice(0, 2)}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* ─── 2. Problem Summary (Doshas) ─── */}
        <div className="card-sacred rounded-2xl p-6 border border-sacred-gold/20">
          <h3 className="font-sans text-lg font-semibold text-sacred-gold mb-4">
            {t('lk.dashboard.problems')}
          </h3>

          {detectedDoshas.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-8 text-center space-y-3">
              <CheckCircle className="w-10 h-10 text-green-500" />
              <p className="text-green-400 font-medium">
                {isHi ? 'सब ठीक है! कोई दोष नहीं पाया गया।' : 'All Clear! No doshas detected.'}
              </p>
            </div>
          ) : (
            <div className="space-y-3">
              {/* Count summary */}
              <div className="flex items-center gap-2 mb-3">
                <AlertTriangle className="w-5 h-5 text-red-500" />
                <span className="text-sm text-cosmic-text/80">
                  {detectedDoshas.length}{' '}
                  {isHi ? 'दोष पाए गए' : detectedDoshas.length === 1 ? 'dosha detected' : 'doshas detected'}
                </span>
              </div>

              {/* Dosha list */}
              {detectedDoshas.map((dosha) => (
                <div
                  key={dosha.key}
                  className="flex items-center justify-between p-3 rounded-xl border border-red-300/20 bg-red-500/5"
                >
                  <div className="flex items-center gap-2 min-w-0">
                    <AlertTriangle className="w-4 h-4 text-red-400 shrink-0" />
                    <span className="text-sm text-cosmic-text truncate">
                      {isHi ? dosha.nameHi : dosha.nameEn}
                    </span>
                  </div>
                  <span
                    className={`px-2.5 py-0.5 rounded-full text-sm font-semibold shrink-0 ml-2 ${severityStyles[dosha.severity].badge}`}
                  >
                    {dosha.severity === 'high'
                      ? t('lk.dosha.high')
                      : dosha.severity === 'medium'
                        ? t('lk.dosha.medium')
                        : t('lk.dosha.low')}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* ─── 3. Quick Remedies ─── */}
        <div className="card-sacred rounded-2xl p-6 border border-sacred-gold/20">
          <h3 className="font-sans text-lg font-semibold text-sacred-gold mb-4">
            {t('lk.dashboard.remediesList')}
          </h3>

          {quickRemedies.length === 0 ? (
            <p className="text-sm text-cosmic-text/70 italic py-4 text-center">
              {isHi ? 'कोई उपाय उपलब्ध नहीं' : 'No remedies available'}
            </p>
          ) : (
            <div className="space-y-3">
              {quickRemedies.map((item, idx) => {
                const TypeIcon =
                  typeIcons[item.remedy.type as keyof typeof typeIcons] ?? Sparkles;
                const remedyText = isHi ? item.remedy.hi : item.remedy.en;

                return (
                  <div
                    key={idx}
                    className="flex items-start gap-3 p-3 rounded-xl bg-sacred-gold/5 border border-sacred-gold/10"
                  >
                    <TypeIcon className="w-4 h-4 text-sacred-gold mt-0.5 shrink-0" />
                    <p className="text-sm text-cosmic-text/80 leading-snug">
                      {remedyText}
                    </p>
                  </div>
                );
              })}

              {/* View all link */}
              <p className="text-sm text-sacred-gold cursor-pointer hover:text-sacred-gold-dark transition-colors text-center pt-2">
                {isHi ? 'सभी उपाय देखें →' : 'View all remedies →'}
              </p>
            </div>
          )}
        </div>

        {/* ─── 4. Life Timeline ─── */}
        <div className="card-sacred rounded-2xl p-6 border border-sacred-gold/20">
          <h3 className="font-sans text-lg font-semibold text-sacred-gold mb-4 flex items-center gap-2">
            <Clock className="w-5 h-5" />
            {t('lk.dashboard.timeline')}
          </h3>

          <p className="text-sm text-cosmic-text/60 mb-4">
            {isHi ? 'वर्तमान आयु' : 'Current Age'}:{' '}
            <span className="font-semibold text-cosmic-text">{age}</span>
          </p>

          {timelinePeriods.length === 0 ? (
            <p className="text-sm text-cosmic-text/70 italic py-4 text-center">
              {isHi ? 'समयरेखा उपलब्ध नहीं' : 'Timeline data not available'}
            </p>
          ) : (
            <div className="space-y-2">
              {timelinePeriods.map((period, idx) => {
                const isCurrent = idx === currentPeriodIndex;
                const isPrevious = idx === currentPeriodIndex - 1;
                const isNext = idx === currentPeriodIndex + 1;

                // Only show previous, current, and next periods
                if (!isCurrent && !isPrevious && !isNext) return null;

                const planetLabel = getPlanetLabel(period.planet, language);

                return (
                  <div
                    key={idx}
                    className={`flex items-center justify-between p-3 rounded-xl border transition-all ${
                      isCurrent
                        ? 'bg-sacred-gold/15 border-sacred-gold/40'
                        : 'bg-cosmic-card/30 border-sacred-gold/10 opacity-60'
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <span
                        className={`w-2.5 h-2.5 rounded-full ${
                          isCurrent ? 'bg-sacred-gold animate-pulse' : 'bg-cosmic-text/30'
                        }`}
                      />
                      <div>
                        <p
                          className={`text-sm font-medium ${
                            isCurrent ? 'text-sacred-gold' : 'text-cosmic-text/70'
                          }`}
                        >
                          {planetLabel}
                        </p>
                        <p className="text-sm text-cosmic-text/70">
                          {period.startAge}–{period.endAge}{' '}
                          {isHi ? 'वर्ष' : 'years'}
                        </p>
                      </div>
                    </div>

                    {isCurrent && (
                      <span className="px-2.5 py-0.5 rounded-full text-sm font-semibold bg-sacred-gold/20 text-sacred-gold">
                        {isHi ? 'वर्तमान' : 'Active'}
                      </span>
                    )}
                    {isPrevious && (
                      <span className="px-2.5 py-0.5 rounded-full text-sm text-cosmic-text/60">
                        {isHi ? 'पिछला' : 'Previous'}
                      </span>
                    )}
                    {isNext && (
                      <span className="px-2.5 py-0.5 rounded-full text-sm text-cosmic-text/60">
                        {isHi ? 'अगला' : 'Next'}
                      </span>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
