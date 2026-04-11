import { useState, useMemo } from 'react';
import { useTranslation } from '@/lib/i18n';
import type { LalKitabChartData } from './lalkitab-data';
import { NISHANIYAN_SIGNS, PLANETS } from './lalkitab-data';
import { BookOpen, CheckSquare, Square, Search, AlertTriangle, CheckCircle2, X } from 'lucide-react';

interface Props {
  chartData: LalKitabChartData;
}

type Category = 'all' | 'body' | 'household' | 'behavior' | 'family' | 'recurring';

interface MatchResult {
  signId: string;
  signEn: string;
  signHi: string;
  planet: string;
  ruleId: string;
  natalHouse: number;
  isMatched: boolean;
}

const categoryKeys: { key: Category; labelKey: string }[] = [
  { key: 'all', labelKey: 'common.all' },
  { key: 'body', labelKey: 'lk.nishaniyan.categoryBody' },
  { key: 'household', labelKey: 'lk.nishaniyan.categoryHousehold' },
  { key: 'behavior', labelKey: 'lk.nishaniyan.categoryBehavior' },
  { key: 'family', labelKey: 'lk.nishaniyan.categoryFamily' },
  { key: 'recurring', labelKey: 'lk.nishaniyan.categoryRecurring' },
];

function getPlanetLabel(key: string, language: string): string {
  const p = PLANETS.find((pl) => pl.key === key);
  if (!p) return key;
  return language === 'hi' ? p.hi : p.en;
}

export default function LalKitabNishaniyaTab({ chartData }: Props) {
  const { t, language } = useTranslation();
  const isHi = language === 'hi';

  const [checked, setChecked] = useState<Set<string>>(new Set());
  const [matched, setMatched] = useState<MatchResult[] | null>(null);
  const [activeCategory, setActiveCategory] = useState<Category>('all');

  const filteredSigns = useMemo(
    () =>
      activeCategory === 'all'
        ? NISHANIYAN_SIGNS
        : NISHANIYAN_SIGNS.filter((s) => s.category === activeCategory),
    [activeCategory],
  );

  const toggle = (id: string) => {
    setMatched(null);
    setChecked((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const clearAll = () => {
    setChecked(new Set());
    setMatched(null);
  };

  const matchRules = () => {
    const results: MatchResult[] = [];
    for (const id of checked) {
      const sign = NISHANIYAN_SIGNS.find((s) => s.id === id);
      if (!sign) continue;
      const natalHouse = chartData.planetPositions[sign.planet] ?? 0;
      const isMatched = natalHouse > 0 && sign.badHouses.includes(natalHouse);
      results.push({
        signId: sign.id,
        signEn: sign.en,
        signHi: sign.hi,
        planet: sign.planet,
        ruleId: sign.ruleId,
        natalHouse,
        isMatched,
      });
    }
    // matched first, then unmatched
    results.sort((a, b) => Number(b.isMatched) - Number(a.isMatched));
    setMatched(results);
  };

  const matchedCount = matched ? matched.filter((r) => r.isMatched).length : 0;
  const confidencePct =
    matched && matched.length > 0
      ? Math.round((matchedCount / matched.length) * 100)
      : 0;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-xl font-sans font-semibold text-sacred-gold flex items-center gap-2 mb-1">
          <BookOpen className="w-5 h-5" />
          {t('lk.nishaniyan.title')}
        </h2>
        <p className="text-sm text-gray-500">{t('lk.nishaniyan.desc')}</p>
      </div>

      {/* Category filter */}
      <div className="flex flex-wrap gap-2">
        {categoryKeys.map(({ key, labelKey }) => (
          <button
            key={key}
            onClick={() => setActiveCategory(key)}
            className={`px-3 py-1.5 rounded-full text-xs font-medium transition-all ${
              activeCategory === key
                ? 'bg-sacred-gold text-white shadow-sm'
                : 'bg-sacred-gold/10 text-sacred-gold hover:bg-sacred-gold/20'
            }`}
          >
            {t(labelKey)}
          </button>
        ))}
      </div>

      {/* Signs checklist */}
      <div className="card-sacred rounded-xl p-5 border border-sacred-gold/20">
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-sans font-semibold text-sacred-gold">
            {t('lk.nishaniyan.selectSigns')}
          </h3>
          {checked.size > 0 && (
            <span className="text-xs text-gray-500">
              {checked.size} {t('lk.nishaniyan.checkedCount')}
            </span>
          )}
        </div>

        <div className="grid gap-2 sm:grid-cols-2">
          {filteredSigns.map((sign) => {
            const isChecked = checked.has(sign.id);
            return (
              <button
                key={sign.id}
                onClick={() => toggle(sign.id)}
                className={`flex items-start gap-3 p-3 rounded-xl border text-left transition-all ${
                  isChecked
                    ? 'bg-sacred-gold/10 border-sacred-gold/40'
                    : 'bg-white/30 border-gray-200/50 hover:border-sacred-gold/20 hover:bg-sacred-gold/5'
                }`}
              >
                {isChecked ? (
                  <CheckSquare className="w-4 h-4 text-sacred-gold mt-0.5 shrink-0" />
                ) : (
                  <Square className="w-4 h-4 text-gray-400 mt-0.5 shrink-0" />
                )}
                <span className="text-sm text-cosmic-text leading-snug">
                  {isHi ? sign.hi : sign.en}
                </span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Action buttons */}
      <div className="flex flex-wrap gap-3">
        <button
          onClick={matchRules}
          disabled={checked.size === 0}
          className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-sacred-gold text-white font-medium text-sm hover:bg-sacred-gold-dark disabled:opacity-40 disabled:cursor-not-allowed transition-all"
        >
          <Search className="w-4 h-4" />
          {t('lk.nishaniyan.matchBtn')}
        </button>
        {checked.size > 0 && (
          <button
            onClick={clearAll}
            className="flex items-center gap-2 px-4 py-2.5 rounded-xl border border-gray-300 text-gray-600 text-sm hover:bg-gray-50 transition-all"
          >
            <X className="w-4 h-4" />
            {t('lk.nishaniyan.clearBtn')}
          </button>
        )}
      </div>

      {/* Help text when nothing selected */}
      {checked.size === 0 && matched === null && (
        <div className="text-center py-8 text-gray-500 text-sm">
          {t('lk.nishaniyan.selectFirst')}
        </div>
      )}

      {/* Results */}
      {matched !== null && (
        <div className="space-y-4">
          {/* Confidence score */}
          {matched.length > 0 && (
            <div className="card-sacred rounded-xl p-5 border border-sacred-gold/20">
              <div className="flex items-center justify-between mb-3">
                <h3 className="font-sans font-semibold text-sacred-gold">
                  {t('lk.nishaniyan.confidence')}
                </h3>
                <span className="text-2xl font-bold text-sacred-gold">{confidencePct}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2.5">
                <div
                  className={`h-2.5 rounded-full transition-all ${
                    confidencePct >= 70
                      ? 'bg-green-500'
                      : confidencePct >= 40
                        ? 'bg-orange-400'
                        : 'bg-red-400'
                  }`}
                  style={{ width: `${confidencePct}%` }}
                />
              </div>
              <p className="text-xs text-gray-500 mt-2">
                {matchedCount} / {matched.length} {isHi ? 'नियम आपकी कुंडली से मिले' : 'rules matched your chart'}
              </p>
            </div>
          )}

          {/* Match list */}
          <div className="card-sacred rounded-xl p-5 border border-sacred-gold/20">
            <h3 className="font-sans font-semibold text-sacred-gold mb-4">
              {t('lk.nishaniyan.matched')}
            </h3>

            {matched.length === 0 ? (
              <p className="text-sm text-gray-500 text-center py-4">
                {t('lk.nishaniyan.noMatch')}
              </p>
            ) : (
              <div className="space-y-3">
                {matched.map((result) => (
                  <div
                    key={result.signId}
                    className={`p-4 rounded-xl border ${
                      result.isMatched
                        ? 'bg-red-500/5 border-red-300/30'
                        : 'bg-green-500/5 border-green-300/30'
                    }`}
                  >
                    <div className="flex items-start gap-3">
                      {result.isMatched ? (
                        <AlertTriangle className="w-4 h-4 text-red-500 mt-0.5 shrink-0" />
                      ) : (
                        <CheckCircle2 className="w-4 h-4 text-green-500 mt-0.5 shrink-0" />
                      )}
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-cosmic-text leading-snug">
                          {isHi ? result.signHi : result.signEn}
                        </p>
                        <div className="flex flex-wrap gap-x-4 gap-y-1 mt-2">
                          <span className="text-xs text-gray-500">
                            <span className="font-medium text-sacred-gold">{t('lk.nishaniyan.planet')}:</span>{' '}
                            {getPlanetLabel(result.planet, language)}{' '}
                            {isHi ? `(भाव ${result.natalHouse})` : `(House ${result.natalHouse})`}
                          </span>
                          <span className="text-xs text-gray-400">
                            {t('lk.nishaniyan.ruleId')}: {result.ruleId}
                          </span>
                        </div>
                        <p
                          className={`text-xs mt-1.5 font-medium ${result.isMatched ? 'text-red-500' : 'text-green-600'}`}
                        >
                          {result.isMatched
                            ? t('lk.nishaniyan.found')
                            : t('lk.nishaniyan.noPlanet')}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
