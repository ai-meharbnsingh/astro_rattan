import { useState } from 'react';
import { useTranslation } from '@/lib/i18n';
import type { LalKitabChartData } from './lalkitab-data';
import { PLANETS, REMEDIES } from './lalkitab-data';
import { Heart, Gift, Home, Zap, Filter } from 'lucide-react';

interface Props {
  chartData: LalKitabChartData;
}

const typeIcons = {
  feeding: Heart,
  donation: Gift,
  household: Home,
  action: Zap,
} as const;

const categoryBadgeStyles: Record<string, string> = {
  daily: 'bg-green-500/10 text-green-600',
  weekly: 'bg-blue-500/10 text-blue-600',
  urgent: 'bg-red-500/10 text-red-600',
  general: 'bg-gray-500/10 text-gray-600',
};

const filterCategories = ['all', 'daily', 'weekly', 'urgent', 'general'] as const;

export default function LalKitabRemediesTab({ chartData }: Props) {
  const { t, language } = useTranslation();
  const [activeFilter, setActiveFilter] = useState<string>('all');

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-xl font-sans font-semibold text-sacred-gold mb-1">
          {t('lk.remedies.title')}
        </h2>
        <p className="text-sm text-cosmic-text/60">
          {t('lk.remedies.desc')}
        </p>
      </div>

      {/* Filter bar */}
      <div className="flex flex-wrap items-center gap-2">
        <Filter className="w-5 h-5 text-sacred-gold" />
        {filterCategories.map((category) => (
          <button
            key={category}
            onClick={() => setActiveFilter(category)}
            className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
              activeFilter === category
                ? 'bg-sacred-gold text-cosmic-bg'
                : 'bg-cosmic-card border border-sacred-gold/20 text-cosmic-text/70'
            }`}
          >
            {category === 'all'
              ? 'All'
              : t(`lk.remedies.${category}`)}
          </button>
        ))}
      </div>

      {/* Remedies per planet */}
      <div className="space-y-6">
        {PLANETS.map((planet) => {
          const houseNumber = chartData.planetPositions[planet.key];
          if (houseNumber == null) return null;

          const planetRemedies = REMEDIES[planet.key]?.[houseNumber];
          if (!planetRemedies || planetRemedies.length === 0) return null;

          const filtered =
            activeFilter === 'all'
              ? planetRemedies
              : planetRemedies.filter((r) => r.category === activeFilter);

          if (filtered.length === 0) return null;

          const planetName = language === 'hi' ? planet.hi : planet.en;

          return (
            <div key={planet.key} className="space-y-4">
              {/* Section header */}
              <h3 className="text-lg font-sans font-semibold text-sacred-gold">
                {planetName} — {language === 'hi' ? 'भाव' : 'House'} {houseNumber}
              </h3>

              {/* Remedy cards */}
              <div className="grid gap-4">
                {filtered.map((remedy, idx) => {
                  const TypeIcon = typeIcons[remedy.type];
                  const typeLabel = t(`lk.remedies.${remedy.type}`);
                  const badgeStyle = categoryBadgeStyles[remedy.category];
                  const categoryLabel = t(`lk.remedies.${remedy.category}`);
                  const remedyText = language === 'hi' ? remedy.hi : remedy.en;

                  return (
                    <div
                      key={idx}
                      className="card-sacred rounded-xl p-4 border border-sacred-gold/20"
                    >
                      <div className="flex items-start gap-4">
                        {/* Type icon */}
                        <div className="mt-0.5">
                          <TypeIcon className="w-5 h-5 text-sacred-gold" />
                        </div>

                        <div className="flex-1 min-w-0">
                          {/* Type label and category badge */}
                          <div className="flex items-center gap-2 mb-1">
                            <span className="text-sm font-medium text-cosmic-text">
                              {typeLabel}
                            </span>
                            <span
                              className={`px-2 py-0.5 rounded-full text-xs font-medium ${badgeStyle}`}
                            >
                              {categoryLabel}
                            </span>
                          </div>

                          {/* Remedy text */}
                          <p className="text-sm text-cosmic-text/80">
                            {remedyText}
                          </p>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
