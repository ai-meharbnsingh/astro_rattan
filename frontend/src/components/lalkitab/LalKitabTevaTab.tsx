import { useEffect, useMemo, useState } from 'react';
import { useTranslation } from '@/lib/i18n';
import { Info, FileSearch } from 'lucide-react';
import KundliChartSVG, { type PlanetEntry } from '@/components/KundliChartSVG';
import { api } from '@/lib/api';
import { pickLang } from './safe-render';
import { useLalKitab } from './LalKitabContext';
import { toLkPlanetList } from './lalkitab-core';
// P1.1 — Modified Analytical Tewa planet-state classifier
import { classifyPlanetStates, legendEntries, type PlanetStateTag } from './planet-state';
import { Heading } from '@/components/ui/heading';

interface Props {
  apiResult?: any;
}

type TevaType = 'andha' | 'ratondha' | 'dharmi' | 'nabalig' | 'khali';

const PLANET_HI: Record<string, string> = {
  Sun: 'सूर्य', Moon: 'चंद्र', Mars: 'मंगल', Mercury: 'बुध',
  Jupiter: 'गुरु', Venus: 'शुक्र', Saturn: 'शनि', Rahu: 'राहु', Ketu: 'केतु',
};

const TEVA_CONFIG: Record<TevaType, { color: string; bgColor: string; borderColor: string }> = {
  andha:    { color: 'text-red-700',         bgColor: 'bg-red-500/8',          borderColor: 'border-red-300/40' },
  ratondha: { color: 'text-red-700',         bgColor: 'bg-red-500/8',          borderColor: 'border-red-300/40' },
  dharmi:   { color: 'text-green-700',       bgColor: 'bg-green-500/8',        borderColor: 'border-green-300/40' },
  nabalig:  { color: 'text-orange-700',      bgColor: 'bg-orange-500/8',       borderColor: 'border-orange-300/40' },
  khali:    { color: 'text-amber-800',       bgColor: 'bg-amber-400/10',       borderColor: 'border-amber-300/40' },
};

function pickPrimaryType(active: string[] | undefined | null): TevaType | null {
  if (!active || active.length === 0) return null;
  const known: TevaType[] = ['andha', 'ratondha', 'dharmi', 'nabalig', 'khali'];
  for (const k of known) {
    if (active.includes(k)) return k;
  }
  return null;
}

export default function LalKitabTevaTab({ apiResult }: Props) {
  const { t, language } = useTranslation();
  const isHi = language === 'hi';
  const { kundliId, fullData, chartData } = useLalKitab();

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');
  const [advanced, setAdvanced] = useState<any | null>(null);

  // Prefer consolidated fullData, otherwise load advanced.
  useEffect(() => {
    const adv = fullData?.advanced;
    if (adv) { setAdvanced(adv); return; }
    if (!kundliId) { setAdvanced(null); return; }
    let cancelled = false;
    setLoading(true);
    setError('');
    api.get(`/api/lalkitab/advanced/${kundliId}`)
      .then((res) => { if (!cancelled) setAdvanced(res); })
      .catch(() => { if (!cancelled) setError(isHi ? 'तेवा डेटा लोड नहीं हो पाया।' : 'Failed to load Teva data.'); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [kundliId, fullData?.advanced, isHi]);

  const teva = (advanced?.teva_type || fullData?.advanced?.teva_type) ?? null;
  const activeTypes: string[] = Array.isArray(teva?.active_types) ? teva.active_types : [];
  const primary = pickPrimaryType(activeTypes);
  const cfg = primary ? TEVA_CONFIG[primary] : TEVA_CONFIG.khali;

  // P1.3 — 35-Sala / 36-Sala Chakar cycle (ascendant-lord driven).
  const chakar = (advanced?.chakar_cycle || fullData?.advanced?.chakar_cycle) ?? null;

  const labelKeyByType: Record<string, string> = {
    andha: 'lk.teva.andha',
    ratondha: 'lk.teva.ratondha',
    dharmi: 'lk.teva.dharmi',
    nabalig: 'lk.teva.nabalig',
    khali: 'lk.teva.khali',
  };
  const tevaLabel = primary ? t(labelKeyByType[primary] || 'lk.teva.type') : (isHi ? 'अज्ञात' : 'Unknown');

  const planets: PlanetEntry[] = useMemo(() => {
    const planetsRaw = apiResult?.chart_data?.planets;
    if (!planetsRaw) return [];
    return toLkPlanetList(planetsRaw).map(p => ({
      ...p,
      house: p.house,
    }));
  }, [apiResult]);

  // P1.1 — classify each planet into a dominant LK state so the chart
  // renderer can colour-code planets consistently. Falls back to 'normal'
  // for every planet if `advanced` hasn't loaded yet.
  const planetStateTags = useMemo(
    () => classifyPlanetStates(advanced),
    [advanced],
  );
  // Note: KundliChartSVG does not yet support per-planet state tag objects like InteractiveKundli,
  // but it does color malefic/benefic/exalted/debilitated correctly.
  const hasAnyState = Object.values(planetStateTags).some(t => t.state !== 'normal');
  // Counts per state for the legend ("Blind · 2" etc.)
  const statesInChart = useMemo(() => {
    const counts: Record<string, number> = {};
    for (const tag of Object.values(planetStateTags)) {
      if (tag.state !== 'normal') {
        counts[tag.state] = (counts[tag.state] ?? 0) + 1;
      }
    }
    return counts;
  }, [planetStateTags]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
          <FileSearch className="w-6 h-6" />
          {t('lk.teva.title')}
        </Heading>
        <p className="text-sm text-gray-500">{t('lk.teva.desc')}</p>
      </div>

      {!!error && (
        <div className="p-4 rounded-xl border border-red-200 bg-red-50 text-red-800 text-sm">
          {error}
        </div>
      )}

      {/* Teva type card */}
      <div className={`rounded-xl border p-6 ${cfg.bgColor} ${cfg.borderColor}`}>
        <p className="text-xs font-semibold uppercase tracking-wider text-gray-500 mb-2">
          {t('lk.teva.type')}
        </p>
        <h3 className={`text-2xl font-sans font-bold mb-3 ${cfg.color}`}>{tevaLabel}</h3>

        {loading && (
          <p className="text-sm text-foreground/70">{isHi ? 'लोड हो रहा है...' : 'Loading...'}</p>
        )}

        {!loading && teva && activeTypes.length > 0 && (
          <div className="space-y-3">
            <div className="flex flex-wrap gap-2">
              {activeTypes.map((ty) => (
                <span
                  key={ty}
                  className="text-xs px-2 py-1 rounded-full border border-sacred-gold/30 bg-white/40 text-sacred-gold-dark font-semibold"
                >
                  {t(labelKeyByType[ty] || 'lk.teva.type')}
                </span>
              ))}
              {/* P1.3 — Chakar cycle chip (35-Sala / 36-Sala) */}
              {chakar && (chakar.cycle_length === 35 || chakar.cycle_length === 36) && (
                <span
                  key="chakar-cycle"
                  className={`text-xs px-2 py-1 rounded-full border font-semibold cursor-help ${
                    chakar.cycle_length === 36
                      ? 'border-purple-300/60 bg-purple-500/10 text-purple-800'
                      : 'border-sacred-gold/30 bg-white/40 text-sacred-gold-dark'
                  }`}
                  title={isHi ? chakar.reason_hi : chakar.reason_en}
                >
                  {isHi
                    ? `चक्र: ${chakar.cycle_length}-साला`
                    : `Chakar: ${chakar.cycle_length}-Sala`}
                  {chakar.ascendant_lord && (
                    <span className="opacity-60 ml-1">
                      · {isHi
                          ? (chakar.ascendant_lord_hi || chakar.ascendant_lord)
                          : chakar.ascendant_lord}
                    </span>
                  )}
                </span>
              )}
            </div>
            {/* P1.3 — 36-Sala "shadow year" explanation (only when 36-cycle) */}
            {chakar && chakar.cycle_length === 36 && (chakar.shadow_year_en || chakar.shadow_year_hi) && (
              <div className="mt-2 p-3 rounded-lg border border-purple-200/60 bg-purple-500/5">
                <p className="text-[11px] font-bold text-purple-800 uppercase tracking-wide mb-1">
                  {isHi ? '36-साला छाया वर्ष' : '36-Sala Shadow Year'}
                </p>
                <p className="text-xs text-purple-900/80 leading-relaxed">
                  {isHi ? chakar.shadow_year_hi : chakar.shadow_year_en}
                </p>
              </div>
            )}
            {activeTypes.map((ty) => {
              const desc = teva?.description?.[ty];
              const text = pickLang(desc, isHi);
              if (!text) return null;
              return (
                <p key={`desc-${ty}`} className="text-sm text-foreground/80 leading-relaxed">
                  {text}
                </p>
              );
            }).filter(Boolean)}
          </div>
        )}

        {!loading && (!teva || activeTypes.length === 0) && (
          <p className="text-sm text-foreground/70">
            {isHi ? 'तेवा प्रकार उपलब्ध नहीं है।' : 'Teva type not available.'}
          </p>
        )}
      </div>

      {/* NOTE: Planet classification (blind/righteous/underage) was previously fabricated client-side.
          In strict mode we do not render those until a backend section provides authoritative lists. */}

      {/* Kundli chart — P1.1 Modified Analytical Tewa with per-planet LK
          state colour coding (Andhe/Masnui/Soye/Kayam/Jage) driven by the
          backend /advanced endpoint. */}
      {planets.length > 0 ? (
        <div className="card-sacred rounded-xl border border-sacred-gold/20 p-5">
          <h3 className="font-sans font-semibold text-sacred-gold mb-3 text-sm">
            {t('auto.lalKitabKundliTevaCh')}
          </h3>
          <div className="flex justify-center">
            <div className="w-full max-w-[420px] aspect-square">
              <KundliChartSVG
                planets={planets}
                ascendantSign="Aries" // Lal Kitab is ALWAYS fixed to Aries Lagna
                language={language}
                showRashiNumbers={true}
                showHouseNumbers={false}
                rashiNumberPlacement="center"
                showAscendantMarker={false}
              />
            </div>
          </div>
          {/* P1.1 — legend for the LK state colours. Rendered only when at
              least one planet has a non-normal state so charts with clean
              readings stay visually quiet. */}
          {hasAnyState && (
            <div className="mt-4 pt-3 border-t border-sacred-gold/10">
              <p className="text-[10px] font-bold text-sacred-gold uppercase tracking-widest mb-2">
                {isHi ? 'ग्रह अवस्था रंग-संकेत' : 'Planet State Legend'}
              </p>
              <div className="flex flex-wrap gap-2">
                {legendEntries().map((entry) => {
                  const count = statesInChart[entry.state] ?? 0;
                  if (count === 0) return null;
                  return (
                    <span
                      key={entry.state}
                      className={`inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full border text-[10px] font-semibold ${entry.bgClass} ${entry.textClass} ${entry.borderClass}`}
                      title={isHi ? entry.descHi : entry.descEn}
                    >
                      <span
                        className="w-2 h-2 rounded-full"
                        style={{ backgroundColor: entry.hexColour }}
                        aria-hidden="true"
                      />
                      {isHi ? entry.labelHi : entry.labelEn}
                      <span className="opacity-60">· {count}</span>
                    </span>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      ) : (
        <div className="card-sacred rounded-xl border border-sacred-gold/20 p-5">
          <h3 className="font-sans font-semibold text-sacred-gold mb-4 text-sm">
            {t('auto.planetPositionsLalKi')}
          </h3>
          <div className="grid grid-cols-3 sm:grid-cols-5 gap-2">
            {Object.entries(chartData?.planetPositions || {}).map(([planet, house]: [string, any]) => (
              <div key={planet} className="flex flex-col items-center p-2 rounded-lg bg-sacred-gold/5 border border-sacred-gold/10">
                <span className="text-xs font-semibold text-sacred-gold-dark">
                  {isHi ? (PLANET_HI[planet] ?? planet) : planet}
                </span>
                <span className="text-lg font-bold text-foreground">{Number(house) || 0}</span>
                <span className="text-xs text-gray-400">{t('auto.h')}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
