import { useState, useEffect, useMemo, useCallback } from 'react';
import { useTranslation } from '@/lib/i18n';
import { Navigation, AlertTriangle, Info, Zap, RefreshCw } from 'lucide-react';
import { pickLang } from './safe-render';
import { apiFetch } from '@/lib/api';
import type { LalKitabChartLite } from './lalkitab-core';

interface ApproxTransit {
  planet: string;
  lkHouse: number;
  speedNote: 'slow' | 'medium' | 'fast';
  en: string;
  hi: string;
}

interface Props {
  chartData: LalKitabChartLite;
  apiResult?: any;
}

interface LiveTransit {
  planet: string;
  sign: string;
  sign_degree: number;
  nakshatra: string | null;
  retrograde: boolean;
  lk_house: number;
  speed_note: 'slow' | 'medium' | 'fast';
}

const speedColors: Record<string, string> = {
  slow: 'bg-purple-500/10 text-purple-700 border-purple-300/30',
  medium: 'bg-orange-500/10 text-orange-700 border-orange-300/30',
  fast: 'bg-blue-500/10 text-blue-700 border-blue-300/30',
};

const speedDots: Record<string, string> = {
  slow: 'bg-purple-500',
  medium: 'bg-orange-400',
  fast: 'bg-blue-400',
};

const PLANET_ABBR: Record<string, string> = {
  Sun: 'Su', Moon: 'Mo', Mars: 'Ma', Mercury: 'Me',
  Jupiter: 'Ju', Venus: 'Ve', Saturn: 'Sa', Rahu: 'Ra', Ketu: 'Ke',
};

const SIGN_HI: Record<string, string> = {
  Aries: 'मेष', Taurus: 'वृष', Gemini: 'मिथुन', Cancer: 'कर्क',
  Leo: 'सिंह', Virgo: 'कन्या', Libra: 'तुला', Scorpio: 'वृश्चिक',
  Sagittarius: 'धनु', Capricorn: 'मकर', Aquarius: 'कुंभ', Pisces: 'मीन',
};

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

function mapLiveTransit(t: LiveTransit): ApproxTransit {
  const deg = typeof t.sign_degree === 'number' ? t.sign_degree.toFixed(1) : '?';
  const retro = t.retrograde ? ' (R)' : '';
  const nak = t.nakshatra ? ` · ${t.nakshatra}` : '';
  const nakHi = t.nakshatra ? ` · ${t.nakshatra}` : '';
  const planetLabel = PLANET_LABELS[t.planet];
  return {
    planet: t.planet,
    lkHouse: t.lk_house,
    speedNote: t.speed_note,
    en: `${t.planet} in ${t.sign}${retro} ${deg}°${nak}`,
    hi: `${pickLang(planetLabel, true)} ${SIGN_HI[t.sign] || t.sign} में${t.retrograde ? ' (वक्री)' : ''} ${deg}°${nakHi}`,
  };
}

export default function LalKitabGocharTab({ chartData, apiResult }: Props) {
  const { t, language } = useTranslation();
  const isHi = language === 'hi';

  const [transits, setTransits] = useState<ApproxTransit[]>([]);
  const [asOf, setAsOf] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [loadError, setLoadError] = useState<string | null>(null);

  // Fetch live planet positions
  useEffect(() => {
    let isMounted = true;
    apiFetch('/api/lalkitab/gochar')
      .then(async (res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((data: { transits: LiveTransit[]; as_of: string }) => {
        if (!isMounted) return;
        const live = Array.isArray(data.transits) ? data.transits.map(mapLiveTransit) : [];
        setTransits(live);
        setAsOf(data.as_of || null);
        if (!live.length) {
          setLoadError(t('auto.transitDataIsUnavail'));
        }
      })
      .catch(() => {
        if (!isMounted) return;
        setLoadError(t('auto.unableToLoadLiveTran'));
        setTransits([]);
      })
      .finally(() => {
        if (isMounted) setIsLoading(false);
      });
    return () => {
      isMounted = false;
    };
  }, [language, t]);

  // Lagna sign number (0 = Aries … 11 = Pisces)
  // Transit alerts come ONLY from backend /api/lalkitab/gochar (no client-side heuristics).
  const alerts = useMemo<{ en: string; hi: string }[]>(() => {
    // If the backend ever returns an `alerts` field on the gochar payload, render it here.
    // Until then, no alerts are rendered — previously this component fabricated alerts
    // from hardcoded rules which duplicated (and conflicted with) backend logic.
    return [];
  }, [transits]);

  const lagnaSignNum = useMemo(() => {
    const asc =
      apiResult?.chart_data?.ascendant?.sign_number ??
      apiResult?.ascendant?.sign_number ??
      null;
    return typeof asc === 'number' ? asc : null;
  }, [apiResult]);

  const globalToNatal = useCallback((globalHouse: number): number | null => {
    if (lagnaSignNum === null || globalHouse === 0) return null;
    return ((globalHouse - 1 - lagnaSignNum + 12) % 12) + 1;
  }, [lagnaSignNum]);

  const activatedHouses = useMemo(() => {
    const map: Record<number, string[]> = {};
    for (const transit of transits) {
      if (transit.lkHouse === 0) continue;
      const natalH = lagnaSignNum !== null ? globalToNatal(transit.lkHouse) : transit.lkHouse;
      if (!natalH) continue;
      if (!map[natalH]) map[natalH] = [];
      if (!map[natalH].includes(transit.planet)) map[natalH].push(transit.planet);
    }
    return map;
  }, [lagnaSignNum, transits, globalToNatal]);

  const houseLabel = (n: number) => t('auto.houseN', { n });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <h2 className="text-xl font-sans font-semibold text-sacred-gold flex items-center gap-2 mb-1">
            <Navigation className="w-5 h-5" />
            {t('lk.gochar.title')}
          </h2>
          <p className="text-sm text-gray-500">{t('lk.gochar.desc')}</p>
        </div>
        {asOf && (
          <div className="flex items-center gap-1.5 text-xs text-green-600 bg-green-500/10 border border-green-300/30 rounded-full px-2.5 py-1 shrink-0">
            <RefreshCw className="w-3 h-3" />
            {t('auto.liveAsOf', { asOf })}
          </div>
        )}
      </div>

      {/* Disclaimer / data source notice */}
      <div className="flex items-start gap-3 p-4 rounded-xl border border-blue-300/30 bg-blue-500/5">
        <Info className="w-4 h-4 text-blue-500 mt-0.5 shrink-0" />
        <p className="text-xs text-blue-700">
          {isHi
            ? 'ग्रहों की स्थिति आज की तिथि के अनुसार स्वचालित रूप से गणना की गई है (सायन/लाहिरी)।'
            : 'Planet positions are live-calculated for today using sidereal/Lahiri ayanamsa.'}
        </p>
      </div>

      {/* Transit Alerts (rendered only when backend supplies them) */}
      {alerts.length > 0 && (
        <div className="card-sacred rounded-xl p-5 border border-sacred-gold/20">
          <h3 className="font-sans font-semibold text-sacred-gold mb-4 flex items-center gap-2">
            <AlertTriangle className="w-4 h-4" />
            {t('lk.gochar.alerts')}
          </h3>
          <div className="space-y-3">
            {alerts.map((alert, idx) => (
              <div
                key={idx}
                className="flex items-start gap-3 p-3 rounded-xl bg-orange-500/5 border border-orange-300/20"
              >
                <Zap className="w-4 h-4 text-orange-500 mt-0.5 shrink-0" />
                <p className="text-sm text-foreground/80 leading-snug">
                  {pickLang(alert, isHi)}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Current Transits table */}
      <div className="card-sacred rounded-xl p-5 border border-sacred-gold/20">
        <h3 className="font-sans font-semibold text-sacred-gold mb-4">
          {t('lk.gochar.currentTransits')}
        </h3>
        {isLoading ? (
          <p className="text-sm text-foreground/70">{t('auto.loadingTransits')}</p>
        ) : loadError ? (
          <p className="text-sm text-red-500">{loadError}</p>
        ) : transits.length === 0 ? (
          <p className="text-sm text-foreground/70">{t('auto.noTransitDataAvailab')}</p>
        ) : (
          <div className="space-y-3">
          {transits.map((transit) => {
            const natalH = lagnaSignNum !== null && transit.lkHouse > 0
              ? globalToNatal(transit.lkHouse)
              : transit.lkHouse > 0 ? transit.lkHouse : null;
            const natalPlanets = natalH
              ? Object.entries(chartData.planetPositions)
                  .filter(([, h]) => h === natalH)
                  .map(([p]) => p)
              : [];

            return (
              <div
                key={transit.planet}
                className="rounded-xl border border-sacred-gold/10 bg-sacred-gold/3 overflow-hidden"
              >
                <div className="flex items-center gap-3 p-3">
                  <span className={`w-2.5 h-2.5 rounded-full shrink-0 ${speedDots[transit.speedNote]}`} />

                  <div className="min-w-[70px]">
                    <p className="text-sm font-semibold text-foreground">
                      {getPlanetLabel(transit.planet, language)}
                    </p>
                    <span
                      className={`inline-block text-xs px-1.5 py-0.5 rounded-full border ${speedColors[transit.speedNote]}`}
                    >
                      {t(`lk.gochar.${transit.speedNote}`)}
                    </span>
                  </div>

                  <div className="flex-1 min-w-0">
                    {transit.lkHouse > 0 ? (
                      <div className="flex flex-wrap gap-x-4 gap-y-0.5">
                        <span className="text-xs text-gray-500">
                          <span className="font-medium text-sacred-gold-dark">
                            {t('lk.gochar.globalHouse')}:
                          </span>{' '}
                          {houseLabel(transit.lkHouse)}
                        </span>
                        {natalH && (
                          <span className="text-xs text-gray-500">
                            <span className="font-medium text-sacred-gold-dark">
                              {t('lk.gochar.natalHouse')}:
                            </span>{' '}
                            {houseLabel(natalH)}
                          </span>
                        )}
                      </div>
                    ) : (
                      <span className="text-xs text-gray-400 italic">
                        {t('auto.variable')}
                      </span>
                    )}

                    <p className="text-xs text-gray-500 mt-1 leading-snug">
                      {pickLang(transit, isHi)}
                    </p>

                    {natalPlanets.length > 0 && (
                      <div className="flex flex-wrap gap-1 mt-1.5">
                        {natalPlanets.map((p) => (
                          <span
                            key={p}
                            className="text-xs px-1.5 py-0.5 rounded bg-sacred-gold/15 text-sacred-gold-dark font-medium"
                          >
                            {PLANET_ABBR[p] || p.slice(0, 2)} {t('auto.Natal')}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
          </div>
        )}
      </div>

      {/* Activated Natal Houses summary */}
      {Object.keys(activatedHouses).length > 0 && (
        <div className="card-sacred rounded-xl p-5 border border-sacred-gold/20">
          <h3 className="font-sans font-semibold text-sacred-gold mb-4">
            {t('lk.gochar.activatedHouses')}
          </h3>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
            {Array.from({ length: 12 }, (_, i) => i + 1).map((h) => {
              const transitingPlanets = activatedHouses[h];
              const natalPlanets = Object.entries(chartData.planetPositions)
                .filter(([, hn]) => hn === h)
                .map(([p]) => p);
              if (!transitingPlanets?.length && !natalPlanets.length) return null;
              return (
                <div
                  key={h}
                  className={`p-3 rounded-xl border text-center ${
                    transitingPlanets?.length
                      ? 'border-sacred-gold/30 bg-sacred-gold/8'
                      : 'border-gray-200/50 bg-white/20'
                  }`}
                >
                  <p className="text-sm font-bold text-sacred-gold mb-1">{houseLabel(h)}</p>
                  {transitingPlanets?.length ? (
                    <div className="flex flex-wrap justify-center gap-1">
                      {transitingPlanets.map((p) => (
                        <span
                          key={p}
                          className="text-xs px-1.5 py-0.5 rounded bg-orange-400/20 text-orange-700 font-medium"
                        >
                          {getPlanetLabel(p, language)}
                        </span>
                      ))}
                      <span className="text-xs text-gray-400 w-full mt-1">
                        {t('auto.transit')}
                      </span>
                    </div>
                  ) : (
                    <p className="text-xs text-gray-400">{t('lk.gochar.noNatalPlanets')}</p>
                  )}
                </div>
              );
            }).filter(Boolean)}
          </div>
        </div>
      )}
    </div>
  );
}
