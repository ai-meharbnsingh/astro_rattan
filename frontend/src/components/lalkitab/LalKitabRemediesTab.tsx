import { useState, useEffect } from 'react';
import { useTranslation } from '@/lib/i18n';
import type { LalKitabChartData } from './lalkitab-data';
import { PLANETS, REMEDIES } from './lalkitab-data';
import { api } from '@/lib/api';
import { Heart, Gift, Home, Zap, Filter, Database, Loader2, Clock, BadgeCheck, ShieldCheck } from 'lucide-react';
import { translateBackend, translatePlanet } from '@/lib/backend-translations';

interface Props {
  chartData: LalKitabChartData;
  kundliId: string;
}

interface MasterRemedy {
  planet: string;
  house: number;
  remedy_text: string;
  remedy_type: string;
  duration_days: number;
  instructions: string | null;
  caution: string | null;
}

const PLANET_HI: Record<string, string> = {
  sun: 'सूर्य', moon: 'चंद्र', mars: 'मंगल', mercury: 'बुध',
  jupiter: 'गुरु', venus: 'शुक्र', saturn: 'शनि', rahu: 'राहु', ketu: 'केतु',
};

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

export default function LalKitabRemediesTab({ chartData, kundliId }: Props) {
  const { t, language } = useTranslation();
  const isHi = language === 'hi';
  const [activeFilter, setActiveFilter] = useState<string>('all');
  const [masterRemedies, setMasterRemedies] = useState<MasterRemedy[]>([]);
  const [masterLoading, setMasterLoading] = useState(false);
  const [validatedRemedies, setValidatedRemedies] = useState<any[]>([]);
  const [validatedLoading, setValidatedLoading] = useState(false);
  const [validatedError, setValidatedError] = useState('');

  useEffect(() => {
    if (!kundliId) { setMasterRemedies([]); setValidatedRemedies([]); return; }
    setMasterLoading(true);
    api.get(`/api/lalkitab/remedies/master/${kundliId}`)
      .then((res: any) => setMasterRemedies(Array.isArray(res?.remedies) ? res.remedies : []))
      .catch(() => setMasterRemedies([]))
      .finally(() => setMasterLoading(false));

    // Fetch validated remedies
    setValidatedLoading(true);
    api.post('/api/kp-lalkitab/lk-validated-remedies', { kundli_id: kundliId })
      .then((res: any) => setValidatedRemedies(Array.isArray(res?.remedies) ? res.remedies : []))
      .catch(() => setValidatedError(isHi ? 'सत्यापित उपाय लोड करने में विफल' : 'Failed to load validated remedies'))
      .finally(() => setValidatedLoading(false));
  }, [kundliId]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-xl font-semibold text-sacred-gold mb-1">
          {t('lk.remedies.title')}
        </h2>
        <p className="text-sm text-gray-500">
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
                ? 'bg-sacred-gold text-background'
                : 'bg-card border border-sacred-gold/20 text-gray-600'
            }`}
          >
            {category === 'all'
              ? t('common.all')
              : t(`lk.remedies.${category}`)}
          </button>
        ))}
      </div>

      {/* ─── Validated Remedies (from LK analysis) ─── */}
      <div className="pt-2">
        <div className="flex items-center gap-2 mb-1">
          <BadgeCheck className="w-5 h-5 text-green-600" />
          <h2 className="text-xl font-semibold text-sacred-gold">
            {isHi ? 'सत्यापित उपाय' : 'Validated Remedies'}
          </h2>
        </div>
        <p className="text-sm text-gray-500 mb-4">
          {isHi
            ? 'लाल किताब नियमों से सत्यापित — ये उपाय आपकी कुंडली के अनुसार प्रमाणित हैं।'
            : 'Verified against Lal Kitab rules — these remedies are validated for your chart.'}
        </p>

        {validatedLoading && (
          <div className="flex items-center justify-center py-10">
            <Loader2 className="w-6 h-6 animate-spin text-sacred-gold" />
          </div>
        )}

        {validatedError && !validatedLoading && (
          <div className="p-3 rounded-xl bg-red-50 border border-red-200 text-red-700 text-sm text-center mb-4">
            {validatedError}
          </div>
        )}

        {!validatedLoading && !validatedError && validatedRemedies.length === 0 && kundliId && (
          <p className="text-sm text-gray-400 text-center py-6 mb-4">
            {isHi ? 'कोई सत्यापित उपाय नहीं मिले।' : 'No validated remedies found.'}
          </p>
        )}

        {!validatedLoading && validatedRemedies.length > 0 && (
          <div className="grid gap-4 mb-6">
            {validatedRemedies.map((r: any, idx: number) => {
              const isFullyValidated = r.validated === true || r.validated === 'full';
              return (
                <div key={idx} className="card-sacred rounded-xl border border-green-200/50 bg-green-500/5 p-4">
                  {/* Top row: name + planet + validated badge */}
                  <div className="flex flex-wrap items-center gap-2 mb-3">
                    <span className="text-sm font-bold text-foreground">
                      {isHi ? r.name_hi : r.name_en}
                    </span>
                    {r.for_planet && (
                      <span className="px-2.5 py-1 rounded-full bg-sacred-gold/15 text-sacred-gold-dark text-xs font-semibold">
                        {translatePlanet(r.for_planet, language)}
                      </span>
                    )}
                    <span className={`ml-auto flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-bold ${
                      isFullyValidated
                        ? 'bg-green-200 text-green-800 border border-green-300'
                        : 'bg-amber-200 text-amber-800 border border-amber-300'
                    }`}>
                      <ShieldCheck className="w-3 h-3" />
                      {isFullyValidated
                        ? (isHi ? 'सत्यापित' : 'Validated')
                        : (isHi ? 'आंशिक सत्यापित' : 'Partially Validated')}
                    </span>
                  </div>

                  {/* Procedure */}
                  <p className="text-sm text-foreground leading-relaxed mb-2">
                    {isHi ? r.procedure_hi : r.procedure_en}
                  </p>

                  {/* Condition */}
                  {r.condition && (
                    <p className="text-xs text-foreground/60 italic">
                      <span className="font-semibold">{isHi ? 'शर्त:' : 'Condition:'}</span> {r.condition}
                    </p>
                  )}
                </div>
              );
            })}
          </div>
        )}
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
              <h3 className="text-lg font-semibold text-sacred-gold">
                {planetName} — {t('auto.house')} {houseNumber}
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
                            <span className="text-sm font-medium text-foreground">
                              {typeLabel}
                            </span>
                            <span
                              className={`px-2 py-0.5 rounded-full text-sm font-medium ${badgeStyle}`}
                            >
                              {categoryLabel}
                            </span>
                          </div>

                          {/* Remedy text */}
                          <p className="text-sm text-foreground/80">
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

      {/* ─── Position-Based Remedies from DB ─── */}
      <div className="pt-4 border-t border-sacred-gold/20">
        <div className="flex items-center gap-2 mb-1">
          <Database className="w-5 h-5 text-sacred-gold" />
          <h2 className="text-xl font-semibold text-sacred-gold">
            {t('lk.remedies.positionBased')}
          </h2>
        </div>
        <p className="text-sm text-gray-500 mb-4">{t('lk.remedies.positionDesc')}</p>

        {masterLoading && (
          <div className="flex items-center justify-center py-10">
            <Loader2 className="w-6 h-6 animate-spin text-sacred-gold" />
          </div>
        )}

        {!masterLoading && masterRemedies.length === 0 && kundliId && (
          <p className="text-sm text-gray-400 text-center py-6">
            {t('auto.noPositionBasedRemed')}
          </p>
        )}

        {!masterLoading && masterRemedies.length > 0 && (
          <div className="grid gap-4">
            {masterRemedies.map((r, idx) => (
              <div key={idx} className="card-sacred rounded-xl border border-sacred-gold/20 p-4">
                {/* Planet + house badge row */}
                <div className="flex items-center gap-2 mb-3">
                  <span className="px-2.5 py-1 rounded-full bg-sacred-gold/15 text-sacred-gold-dark text-xs font-semibold">
                    {isHi ? (PLANET_HI[r.planet] ?? r.planet) : r.planet.charAt(0).toUpperCase() + r.planet.slice(1)}
                  </span>
                  <span className="px-2.5 py-1 rounded-full bg-foreground/8 text-foreground text-xs font-medium">
                    {t('auto.houseRHouse')}
                  </span>
                  <span className="px-2 py-0.5 rounded-full bg-blue-500/10 text-blue-600 text-xs border border-blue-300/30">
                    {t(`lk.remedies.${r.remedy_type}`) !== `lk.remedies.${r.remedy_type}`
                      ? t(`lk.remedies.${r.remedy_type}`)
                      : translateBackend(r.remedy_type, language)}
                  </span>
                </div>

                {/* Remedy text */}
                <p className="text-sm text-foreground leading-relaxed mb-3">{r.remedy_text}</p>

                {/* Duration + instructions + caution */}
                <div className="space-y-1.5">
                  <div className="flex items-center gap-1.5 text-xs text-gray-500">
                    <Clock className="w-3.5 h-3.5" />
                    <span>{t('lk.remedies.duration')}: <strong>{r.duration_days} {t('lk.remedies.days')}</strong></span>
                  </div>
                  {r.instructions && (
                    <p className="text-xs text-gray-600">
                      <span className="font-medium">{t('lk.remedies.instructions')}:</span> {r.instructions}
                    </p>
                  )}
                  {r.caution && (
                    <p className="text-xs text-orange-600">
                      <span className="font-medium">{t('lk.remedies.caution')}:</span> {r.caution}
                    </p>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
