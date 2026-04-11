import { useMemo } from 'react';
import { useTranslation } from '@/lib/i18n';
import type { LalKitabChartData } from './lalkitab-data';
import {
  PREDICTION_AREAS,
  PLANETS,
  computeAreaScore,
  scoreToConfidence,
} from './lalkitab-data';
import {
  Briefcase,
  Coins,
  Heart,
  Home,
  Activity,
  Plane,
  Scale,
  Star,
  TrendingUp,
  AlertTriangle,
  Info,
} from 'lucide-react';

interface Props {
  chartData: LalKitabChartData;
}

const areaIcons: Record<string, React.ElementType> = {
  career: Briefcase,
  money: Coins,
  relationship: Heart,
  family: Home,
  health: Activity,
  travel: Plane,
  legal: Scale,
  spiritual: Star,
};

const confidenceConfig = {
  high: {
    bar: 'bg-green-500',
    badge: 'bg-green-500/15 text-green-700 border-green-300/40',
    border: 'border-green-300/30',
    bg: 'bg-green-500/5',
    icon: TrendingUp,
  },
  moderate: {
    bar: 'bg-sacred-gold',
    badge: 'bg-sacred-gold/15 text-sacred-gold-dark border-sacred-gold/40',
    border: 'border-sacred-gold/30',
    bg: 'bg-sacred-gold/5',
    icon: TrendingUp,
  },
  low: {
    bar: 'bg-orange-400',
    badge: 'bg-orange-400/15 text-orange-700 border-orange-300/40',
    border: 'border-orange-300/30',
    bg: 'bg-orange-400/5',
    icon: AlertTriangle,
  },
  speculative: {
    bar: 'bg-gray-400',
    badge: 'bg-gray-400/15 text-gray-600 border-gray-300/40',
    border: 'border-gray-200/50',
    bg: 'bg-gray-50/50',
    icon: Info,
  },
};

function getPlanetLabel(key: string, language: string): string {
  const p = PLANETS.find((pl) => pl.key === key);
  if (!p) return key;
  return language === 'hi' ? p.hi : p.en;
}

export default function LalKitabPredictionTab({ chartData }: Props) {
  const { t, language } = useTranslation();
  const isHi = language === 'hi';

  const predictions = useMemo(
    () =>
      PREDICTION_AREAS.map((area) => {
        const score = computeAreaScore(area, chartData.planetPositions, chartData.houses);
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
        <h2 className="text-xl font-sans font-semibold text-sacred-gold flex items-center gap-2 mb-1">
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
          const cfg = confidenceConfig[confidence];
          const Icon = areaIcons[area.key] ?? Star;
          const StatusIcon = cfg.icon;

          // Planets implicated in this area
          const implicated = area.primaryPlanets.map((pKey) => {
            const house = chartData.planetPositions[pKey];
            return { key: pKey, house };
          });

          return (
            <div
              key={area.key}
              className={`card-sacred rounded-xl border p-5 ${cfg.border} ${cfg.bg}`}
            >
              {/* Card header */}
              <div className="flex items-start justify-between gap-3 mb-4">
                <div className="flex items-center gap-2">
                  <div className="w-9 h-9 rounded-xl bg-sacred-gold/10 flex items-center justify-center shrink-0">
                    <Icon className="w-4 h-4 text-sacred-gold" />
                  </div>
                  <div>
                    <p className="font-sans font-semibold text-cosmic-text text-sm">
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
                  <p className="text-xl font-bold text-cosmic-text">{score}</p>
                  <p className="text-xs text-gray-400">/100</p>
                </div>
              </div>

              {/* Score bar */}
              <div className="w-full bg-gray-200/60 rounded-full h-1.5 mb-4">
                <div
                  className={`h-1.5 rounded-full transition-all ${cfg.bar}`}
                  style={{ width: `${score}%` }}
                />
              </div>

              {/* Tone badge */}
              <div className={`flex items-center gap-2 mb-3 p-2.5 rounded-lg ${isPositive ? 'bg-green-500/8' : 'bg-orange-400/8'}`}>
                <StatusIcon className={`w-3.5 h-3.5 shrink-0 ${isPositive ? 'text-green-600' : 'text-orange-500'}`} />
                <p className="text-xs font-medium text-cosmic-text/80 leading-snug">
                  <span className={`font-semibold ${isPositive ? 'text-green-600' : 'text-orange-600'}`}>
                    {isPositive ? t('lk.studio.positive') : t('lk.studio.caution')}:{' '}
                  </span>
                  {isPositive
                    ? (isHi ? area.positiveHi : area.positiveEn)
                    : (isHi ? area.cautionHi : area.cautionEn)}
                </p>
              </div>

              {/* Remedy */}
              <div className="mb-3">
                <p className="text-xs font-semibold text-sacred-gold mb-1">
                  {t('lk.studio.actionLabel')}
                </p>
                <p className="text-xs text-cosmic-text/70 leading-snug">
                  {isHi ? area.remedyHi : area.remedyEn}
                </p>
              </div>

              {/* Why — planet trace */}
              <div>
                <p className="text-xs font-semibold text-sacred-gold mb-1.5">
                  {t('lk.studio.whyLabel')}
                </p>
                <div className="flex flex-wrap gap-1.5">
                  {implicated.map(({ key, house }) => (
                    <span
                      key={key}
                      className="text-xs px-2 py-0.5 rounded-full bg-sacred-gold/10 text-sacred-gold-dark"
                    >
                      {getPlanetLabel(key, language)} {isHi ? `भाव ${house}` : `H${house}`}
                    </span>
                  ))}
                  <span className="text-xs px-2 py-0.5 rounded-full bg-gray-100 text-gray-500">
                    {isHi
                      ? `मुख्य भाव: ${area.primaryHouses.join(', ')}`
                      : `Key Houses: ${area.primaryHouses.join(', ')}`}
                  </span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
