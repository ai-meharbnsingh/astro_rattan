import { useMemo, useState, useEffect } from 'react';
import { useTranslation } from '@/lib/i18n';
import type { LalKitabChartData } from './lalkitab-data';
import {
  PREDICTION_AREAS,
  computeAreaScore,
  scoreToConfidence,
} from './lalkitab-data';
import {
  Star,
  Info,
  Clock,
  ThumbsUp,
  Meh
} from 'lucide-react';

interface Props {
  chartData: LalKitabChartData;
}

const STORAGE_KEY_PREFIX = 'lk_prediction_feedback_';
const confidenceConfig: Record<
  string,
  { border: string; bg: string; badge: string; bar: string; icon: typeof Star }
> = {
  high: {
    border: 'border-green-300/30',
    bg: 'bg-green-500/5',
    badge: 'bg-green-500/10 text-green-700 border-green-300/30',
    bar: 'bg-green-500',
    icon: Star,
  },
  moderate: {
    border: 'border-sacred-gold/30',
    bg: 'bg-sacred-gold/5',
    badge: 'bg-sacred-gold/10 text-sacred-gold-dark border-sacred-gold/30',
    bar: 'bg-sacred-gold',
    icon: Star,
  },
  low: {
    border: 'border-orange-300/30',
    bg: 'bg-orange-500/5',
    badge: 'bg-orange-500/10 text-orange-700 border-orange-300/30',
    bar: 'bg-orange-500',
    icon: Star,
  },
  speculative: {
    border: 'border-gray-300/30',
    bg: 'bg-gray-500/5',
    badge: 'bg-gray-500/10 text-gray-700 border-gray-300/30',
    bar: 'bg-gray-500',
    icon: Star,
  },
};

const areaIcons: Record<string, typeof Star> = {};

const PLANET_LABELS: Record<string, { en: string; hi: string }> = {
  Sun: { en: 'Sun', hi: 'सूर्य' },
  Moon: { en: 'Moon', hi: 'चंद्र' },
  Mars: { en: 'Mars', hi: 'मंगल' },
  Mercury: { en: 'Mercury', hi: 'बुध' },
  Jupiter: { en: 'Jupiter', hi: 'गुरु' },
  Venus: { en: 'Venus', hi: 'शुक्र' },
  Saturn: { en: 'Saturn', hi: 'शनि' },
  Rahu: { en: 'Rahu', hi: 'राहु' },
  Ketu: { en: 'Ketu', hi: 'केतु' },
};

function getPlanetLabel(key: string, language: string): string {
  const p = PLANET_LABELS[key];
  if (!p) return key;
  return language === 'hi' ? p.hi : p.en;
}

export default function LalKitabPredictionTab({ chartData }: Props) {
  const { t, language } = useTranslation();
  const isHi = language === 'hi';

  const [feedback, setFeedback] = useState<Record<string, string>>({});

  // Load feedback from localStorage
  useEffect(() => {
    const stored = localStorage.getItem(`${STORAGE_KEY_PREFIX}`);
    if (stored) {
      try {
        setFeedback(JSON.parse(stored));
      } catch (e) {
        /* ignored — corrupt localStorage entry */
      }
    }
  }, []);

  const saveFeedback = (areaKey: string, value: string) => {
    const next = { ...feedback, [areaKey]: value };
    setFeedback(next);
    localStorage.setItem(`${STORAGE_KEY_PREFIX}`, JSON.stringify(next));
  };

  const predictions = useMemo(
    () =>
      PREDICTION_AREAS.map((area) => {
        const score = computeAreaScore(area, chartData.planetPositions, chartData.houses, chartData.planetLongitudes);
        const confidence = scoreToConfidence(score);
        const isPositive = score >= 55;
        return { area, score, confidence, isPositive };
      }),
    [chartData],
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-xl font-semibold text-sacred-gold flex items-center gap-2 mb-1">
          <Star className="w-5 h-5" />
          {t('lk.studio.title')}
        </h2>
        <p className="text-sm text-gray-500">{t('lk.studio.desc')}</p>
      </div>

      {/* Formula note */}
      <div className="flex items-start gap-3 p-4 rounded-xl border border-sacred-gold/20 bg-sacred-gold/5">
        <Info className="w-4 h-4 text-sacred-gold mt-0.5 shrink-0" />
        <p className="text-xs text-gray-600">{t('lk.studio.formula')}</p>
      </div>

      {/* Prediction cards grid */}
      <div className="grid gap-4 md:grid-cols-2">
        {predictions.map(({ area, score, confidence, isPositive }) => {
          const cfg = confidenceConfig[confidence] ?? confidenceConfig.speculative;
          const Icon = areaIcons[area.key] ?? Star;
          const StatusIcon = cfg.icon;
          const userRating = feedback[area.key];

          // Planets implicated in this area
          const implicated = area.primaryPlanets.map((pKey) => {
            const house = chartData.planetPositions[pKey];
            return { key: pKey, house };
          });

          return (
            <div
              key={area.key}
              className={`card-sacred rounded-xl border p-5 flex flex-col h-full transition-all ${cfg.border} ${cfg.bg}`}
            >
              <div className="flex-1">
                {/* Card header */}
                <div className="flex items-start justify-between gap-3 mb-4">
                  <div className="flex items-center gap-2">
                    <div className="w-9 h-9 rounded-xl bg-sacred-gold/10 flex items-center justify-center shrink-0">
                      <Icon className="w-4 h-4 text-sacred-gold" />
                    </div>
                    <div>
                      <p className="font-semibold text-foreground text-sm">
                        {isHi ? area.hi : area.en}
                      </p>
                      <span
                        className={`inline-block text-xs px-2 py-0.5 rounded-full border font-medium mt-0.5 ${cfg.badge}`}
                      >
                        {t(`lk.studio.${confidence}`)}
                      </span>
                    </div>
                  </div>
                  <div className="text-right shrink-0">
                    <p className="text-xl font-bold text-foreground">{score}</p>
                    <p className="text-[10px] text-gray-400 uppercase font-bold tracking-widest">Score</p>
                  </div>
                </div>

                {/* Score bar */}
                <div className="w-full bg-gray-200/60 rounded-full h-1.5 mb-4">
                  <div
                    className={`h-1.5 rounded-full transition-all duration-1000 ${cfg.bar}`}
                    style={{ width: `${score}%` }}
                  />
                </div>

                {/* Tone badge */}
                <div className={`flex items-start gap-2 mb-4 p-3 rounded-lg ${isPositive ? 'bg-green-500/8' : 'bg-orange-400/8'}`}>
                  <StatusIcon className={`w-4 h-4 shrink-0 mt-0.5 ${isPositive ? 'text-green-600' : 'text-orange-500'}`} />
                  <p className="text-xs font-medium text-foreground/80 leading-relaxed">
                    <span className={`font-bold ${isPositive ? 'text-green-600' : 'text-orange-600'} uppercase tracking-tight`}>
                      {isPositive ? t('lk.studio.positive') : t('lk.studio.caution')}:{' '}
                    </span>
                    {isPositive
                      ? (isHi ? area.positiveHi : area.positiveEn)
                      : (isHi ? area.cautionHi : area.cautionEn)}
                  </p>
                </div>

                {/* Remedy */}
                <div className="mb-4">
                  <p className="text-xs font-bold text-sacred-gold uppercase tracking-widest mb-1.5">
                    {t('lk.studio.actionLabel')}
                  </p>
                  <p className="text-sm text-foreground/70 leading-snug">
                    {isHi ? area.remedyHi : area.remedyEn}
                  </p>
                </div>

                {/* Why — planet trace */}
                <div className="mb-6">
                  <p className="text-xs font-bold text-sacred-gold uppercase tracking-widest mb-2">
                    {t('lk.studio.whyLabel')}
                  </p>
                  <div className="flex flex-wrap gap-1.5">
                    {implicated.map(({ key, house }) => (
                      <span
                        key={key}
                        className="text-[10px] px-2 py-0.5 rounded bg-sacred-gold/10 text-sacred-gold-dark font-bold"
                      >
                        {getPlanetLabel(key, language)} {t('auto.hHouse')}
                      </span>
                    ))}
                    <span className="text-[10px] px-2 py-0.5 rounded bg-gray-100 text-gray-500 font-medium">
                      {isHi
                        ? `मुख्य भाव: ${area.primaryHouses.join(', ')}`
                        : `Key Houses: ${area.primaryHouses.join(', ')}`}
                    </span>
                  </div>
                </div>
              </div>

              {/* Feedback Section */}
              <div className="mt-auto pt-4 border-t border-sacred-gold/10">
                <p className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-3">
                  {t('lk.prediction.feedbackTitle')}
                </p>
                <div className="flex gap-2">
                  <button
                    onClick={() => saveFeedback(area.key, 'happened')}
                    className={`flex-1 flex items-center justify-center gap-1.5 py-2 rounded-lg text-[10px] font-bold transition-all border ${
                      userRating === 'happened'
                        ? 'bg-green-600 text-white border-green-600 shadow-md'
                        : 'bg-white/50 text-gray-500 border-gray-200 hover:border-green-300'
                    }`}
                  >
                    <ThumbsUp className="w-3 h-3" />
                    {t('lk.prediction.happened')}
                  </button>
                  <button
                    onClick={() => saveFeedback(area.key, 'partially')}
                    className={`flex-1 flex items-center justify-center gap-1.5 py-2 rounded-lg text-[10px] font-bold transition-all border ${
                      userRating === 'partially'
                        ? 'bg-sacred-gold text-white border-sacred-gold shadow-md'
                        : 'bg-white/50 text-gray-500 border-gray-200 hover:border-sacred-gold/30'
                    }`}
                  >
                    <Meh className="w-3 h-3" />
                    {t('lk.prediction.partially')}
                  </button>
                  <button
                    onClick={() => saveFeedback(area.key, 'not_yet')}
                    className={`flex-1 flex items-center justify-center gap-1.5 py-2 rounded-lg text-[10px] font-bold transition-all border ${
                      userRating === 'not_yet'
                        ? 'bg-gray-600 text-white border-gray-600 shadow-md'
                        : 'bg-white/50 text-gray-500 border-gray-200 hover:border-gray-400'
                    }`}
                  >
                    <Clock className="w-3 h-3" />
                    {t('lk.prediction.notYet')}
                  </button>
                </div>
                {userRating && (
                  <p className="text-[10px] text-green-600 font-bold mt-2 text-center animate-pulse">
                    ✓ {t('lk.prediction.ratingSaved')}
                  </p>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
