import { useState, useMemo } from 'react';
import { useTranslation } from '@/lib/i18n';
import {
  Calendar,
  ArrowRight,
  Sparkles,
  Heart,
  Gift,
  Home,
  Zap,
} from 'lucide-react';
import type { LalKitabChartData } from './lalkitab-data';
import { PLANETS, REMEDIES, PLANET_EFFECTS_IN_HOUSES } from './lalkitab-data';

interface Props {
  chartData: LalKitabChartData;
  birthDate: string;
}

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

function getPlanetAbbr(key: string): string {
  const abbrs: Record<string, string> = {
    Sun: 'Su',
    Moon: 'Mo',
    Mars: 'Ma',
    Mercury: 'Me',
    Jupiter: 'Ju',
    Venus: 'Ve',
    Saturn: 'Sa',
    Rahu: 'Ra',
    Ketu: 'Ke',
  };
  return abbrs[key] ?? key.slice(0, 2);
}

/** Build the current year and +/- 5 years range. */
function getYearRange(): number[] {
  const current = new Date().getFullYear();
  const years: number[] = [];
  for (let y = current - 5; y <= current + 5; y++) {
    years.push(y);
  }
  return years;
}

export default function LalKitabVarshphalTab({ chartData, birthDate }: Props) {
  const { t, language } = useTranslation();
  const isHi = language === 'hi';

  const currentYear = new Date().getFullYear();
  const [selectedYear, setSelectedYear] = useState<number>(currentYear);
  const yearRange = useMemo(() => getYearRange(), []);
  const birthYear = new Date(birthDate).getFullYear();

  // Compute annual planet positions: shift each planet by (selectedYear - birthYear) % 12 houses
  const annualPositions = useMemo(() => {
    const shift = ((selectedYear - birthYear) % 12 + 12) % 12; // always positive
    const positions: Record<string, number> = {};
    for (const planet of PLANETS) {
      const birthHouse = chartData.planetPositions[planet.key];
      if (birthHouse == null) continue;
      // Shift forward, wrap around 1-12
      positions[planet.key] = ((birthHouse - 1 + shift) % 12) + 1;
    }
    return positions;
  }, [selectedYear, birthYear, chartData.planetPositions]);

  // Build house-to-planets maps for mini charts
  const birthHousePlanets = useMemo(() => {
    const map: Record<number, string[]> = {};
    for (let i = 1; i <= 12; i++) map[i] = [];
    for (const planet of PLANETS) {
      const h = chartData.planetPositions[planet.key];
      if (h != null) map[h].push(planet.key);
    }
    return map;
  }, [chartData.planetPositions]);

  const annualHousePlanets = useMemo(() => {
    const map: Record<number, string[]> = {};
    for (let i = 1; i <= 12; i++) map[i] = [];
    for (const planet of PLANETS) {
      const h = annualPositions[planet.key];
      if (h != null) map[h].push(planet.key);
    }
    return map;
  }, [annualPositions]);

  // Planet comparison: birth house vs annual house
  const planetComparison = useMemo(() => {
    return PLANETS.map((planet) => {
      const birthHouse = chartData.planetPositions[planet.key] ?? null;
      const annualHouse = annualPositions[planet.key] ?? null;
      const changed = birthHouse !== annualHouse;
      const effects = annualHouse != null ? PLANET_EFFECTS_IN_HOUSES[planet.key]?.[annualHouse] : null;
      return { planet, birthHouse, annualHouse, changed, effects };
    }).filter((c) => c.birthHouse != null);
  }, [chartData.planetPositions, annualPositions]);

  // Yearly remedies — based on annual positions, pick 3-5 relevant ones
  const yearlyRemedies = useMemo(() => {
    const collected: { planet: string; house: number; remedy: any }[] = [];

    for (const planet of PLANETS) {
      const annualHouse = annualPositions[planet.key];
      if (annualHouse == null) continue;
      const planetRemedies = REMEDIES[planet.key]?.[annualHouse];
      if (!planetRemedies) continue;

      for (const r of planetRemedies) {
        collected.push({ planet: planet.key, house: annualHouse, remedy: r });
      }
    }

    // Prioritize urgent, then daily
    const priority: Record<string, number> = { urgent: 0, daily: 1, weekly: 2, general: 3 };
    collected.sort(
      (a, b) => (priority[a.remedy.category] ?? 9) - (priority[b.remedy.category] ?? 9),
    );

    return collected.slice(0, 5);
  }, [annualPositions]);

  // Mini chart houses order: 4x3 grid
  const miniGridHouses = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];

  const renderMiniChart = (
    title: string,
    housePlanets: Record<number, string[]>,
  ) => (
    <div className="card-sacred rounded-2xl p-5 border border-sacred-gold/20">
      <h4 className="font-sacred text-base font-semibold text-sacred-gold mb-3 text-center">
        {title}
      </h4>
      <div className="grid grid-cols-4 gap-1">
        {miniGridHouses.map((houseNum) => {
          const planets = housePlanets[houseNum] ?? [];
          return (
            <div
              key={houseNum}
              className="flex flex-col items-center justify-center rounded-md border border-sacred-gold/15 bg-cosmic-card/40 p-1.5 min-h-[44px]"
            >
              <span className="text-[9px] font-medium text-sacred-gold-dark/60">
                {houseNum}
              </span>
              {planets.length > 0 && (
                <div className="flex flex-wrap gap-0.5 justify-center mt-0.5">
                  {planets.map((pKey) => (
                    <span
                      key={pKey}
                      className="text-[8px] font-semibold text-cosmic-text bg-sacred-gold/10 rounded px-1 py-px leading-tight"
                    >
                      {getPlanetAbbr(pKey)}
                    </span>
                  ))}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );

  return (
    <div className="space-y-8">
      {/* ─── Header ─── */}
      <div className="text-center space-y-2">
        <h2 className="text-2xl font-sacred font-bold text-sacred-gold flex items-center justify-center gap-2">
          <Calendar className="w-6 h-6" />
          {t('lk.varshphal.title')}
        </h2>
        <p className="text-sm text-cosmic-text/70">{t('lk.varshphal.desc')}</p>
      </div>

      {/* ─── Year Selector ─── */}
      <div className="flex items-center justify-center gap-3">
        <label className="text-sm font-medium text-sacred-gold">
          {t('lk.varshphal.selectYear')}
        </label>
        <select
          value={selectedYear}
          onChange={(e) => setSelectedYear(Number(e.target.value))}
          className="rounded-xl bg-cosmic-card border border-sacred-gold/20 text-cosmic-text px-4 py-3 focus:outline-none focus:border-sacred-gold/50 transition-colors"
        >
          {yearRange.map((y) => (
            <option key={y} value={y}>
              {y}
            </option>
          ))}
        </select>
      </div>

      {/* ─── Side-by-side Comparison Charts ─── */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {renderMiniChart(t('lk.varshphal.birthChart'), birthHousePlanets)}
        {renderMiniChart(t('lk.varshphal.annualChart'), annualHousePlanets)}
      </div>

      {/* ─── Yearly Predictions ─── */}
      <div className="card-sacred rounded-2xl p-6 border border-sacred-gold/20">
        <h3 className="font-sacred text-lg font-semibold text-sacred-gold mb-4">
          {isHi ? 'वार्षिक फलादेश' : 'Yearly Predictions'} — {selectedYear}
        </h3>

        <div className="space-y-3">
          {planetComparison.map(({ planet, birthHouse, annualHouse, changed, effects }) => (
            <div
              key={planet.key}
              className={`rounded-xl p-4 border transition-all ${
                changed
                  ? 'bg-sacred-gold/10 border-sacred-gold/30'
                  : 'bg-cosmic-card/30 border-sacred-gold/10'
              }`}
            >
              {/* Planet row */}
              <div className="flex items-center justify-between mb-2">
                <span className="font-medium text-cosmic-text">
                  {getPlanetLabel(planet.key, language)}
                </span>
                <div className="flex items-center gap-2 text-sm text-cosmic-text/70">
                  <span>
                    {isHi ? 'भाव' : 'H'}{birthHouse}
                  </span>
                  <ArrowRight className="w-4 h-4 text-sacred-gold/60" />
                  <span
                    className={changed ? 'font-semibold text-sacred-gold' : ''}
                  >
                    {isHi ? 'भाव' : 'H'}{annualHouse}
                  </span>
                  {changed && (
                    <span className="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-sacred-gold/20 text-sacred-gold">
                      {isHi ? 'बदलाव' : 'Changed'}
                    </span>
                  )}
                </div>
              </div>

              {/* Effects of annual position */}
              {effects && (
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 mt-2">
                  <div className="bg-green-500/5 border border-green-500/15 rounded-lg p-3">
                    <p className="text-[10px] font-semibold text-green-400 uppercase tracking-wide mb-1">
                      {isHi ? 'शुभ' : 'Good'}
                    </p>
                    <p className="text-xs text-cosmic-text/70 leading-relaxed">
                      {isHi ? effects.good.hi : effects.good.en}
                    </p>
                  </div>
                  <div className="bg-red-500/5 border border-red-500/15 rounded-lg p-3">
                    <p className="text-[10px] font-semibold text-red-400 uppercase tracking-wide mb-1">
                      {isHi ? 'अशुभ' : 'Bad'}
                    </p>
                    <p className="text-xs text-cosmic-text/70 leading-relaxed">
                      {isHi ? effects.bad.hi : effects.bad.en}
                    </p>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* ─── Yearly Remedies ─── */}
      <div className="card-sacred rounded-2xl p-6 border border-sacred-gold/20">
        <h3 className="font-sacred text-lg font-semibold text-sacred-gold mb-4 flex items-center gap-2">
          <Sparkles className="w-5 h-5" />
          {t('lk.varshphal.yearlyRemedies')}
        </h3>

        {yearlyRemedies.length === 0 ? (
          <p className="text-sm text-cosmic-text/50 italic text-center py-4">
            {isHi ? 'इस वर्ष के लिए कोई विशेष उपाय नहीं' : 'No specific remedies for this year'}
          </p>
        ) : (
          <div className="space-y-3">
            {yearlyRemedies.map((item, idx) => {
              const TypeIcon =
                typeIcons[item.remedy.type as keyof typeof typeIcons] ?? Sparkles;
              const remedyText = isHi ? item.remedy.hi : item.remedy.en;
              const planetLabel = getPlanetLabel(item.planet, language);

              return (
                <div
                  key={idx}
                  className="flex items-start gap-3 p-4 rounded-xl bg-sacred-gold/5 border border-sacred-gold/10"
                >
                  <TypeIcon className="w-4 h-4 text-sacred-gold mt-0.5 shrink-0" />
                  <div className="min-w-0">
                    <p className="text-xs text-sacred-gold font-medium mb-0.5">
                      {planetLabel} — {isHi ? 'भाव' : 'House'} {item.house}
                    </p>
                    <p className="text-sm text-cosmic-text/80 leading-snug">
                      {remedyText}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
