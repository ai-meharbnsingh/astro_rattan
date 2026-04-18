import { useEffect, useMemo, useState } from 'react';
import { useTranslation } from '@/lib/i18n';
import { Info } from 'lucide-react';
import InteractiveKundli, { type PlanetData, type ChartData } from '@/components/InteractiveKundli';
import { api } from '@/lib/api';
import { pickLang } from './safe-render';
import { useLalKitab } from './LalKitabContext';
import { toLkPlanetList } from './lalkitab-core';

interface Props {
  apiResult?: any;
}

type TevaType = 'andha' | 'ratondha' | 'dharmi' | 'nabalig' | 'khali';

const PLANET_HI: Record<string, string> = {
  Sun: 'सूर्य', Moon: 'चंद्र', Mars: 'मंगल', Mercury: 'बुध',
  Jupiter: 'गुरु', Venus: 'शुक्र', Saturn: 'शनि', Rahu: 'राहु', Ketu: 'केतु',
};

const ZODIAC_SIGNS = [
  'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
  'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces',
];

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

  const labelKeyByType: Record<string, string> = {
    andha: 'lk.teva.andha',
    ratondha: 'lk.teva.ratondha',
    dharmi: 'lk.teva.dharmi',
    nabalig: 'lk.teva.nabalig',
    khali: 'lk.teva.khali',
  };
  const tevaLabel = primary ? t(labelKeyByType[primary] || 'lk.teva.type') : (isHi ? 'अज्ञात' : 'Unknown');

  const interactiveChartData: ChartData | null = useMemo(() => {
    const planetsRaw = apiResult?.chart_data?.planets;
    if (!planetsRaw) return null;

    // LK context — uses central toLkPlanetList helper
    const planets: PlanetData[] = toLkPlanetList(planetsRaw);

    const asc = apiResult.chart_data?.ascendant;
    const ascSign = asc?.sign || 'Aries';
    const ascIdx = ZODIAC_SIGNS.indexOf(ascSign);
    const houses = Array.from({ length: 12 }, (_, i) => ({
      number: i + 1,
      sign: ZODIAC_SIGNS[(ascIdx + i) % 12],
    }));

    return {
      planets,
      houses,
      ascendant: asc ? { longitude: asc.longitude || 0, sign: ascSign, sign_degree: asc.sign_degree } : undefined,
    };
  }, [apiResult]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-xl font-sans font-semibold text-sacred-gold flex items-center gap-2 mb-1">
          <Info className="w-5 h-5" />
          {t('lk.teva.title')}
        </h2>
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
            </div>
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

      {/* Kundli chart */}
      {interactiveChartData ? (
        <div className="card-sacred rounded-xl border border-sacred-gold/20 p-5">
          <h3 className="font-sans font-semibold text-sacred-gold mb-3 text-sm">
            {t('auto.lalKitabKundliTevaCh')}
          </h3>
          <div className="flex justify-center">
            <div className="w-72 h-72">
              <InteractiveKundli chartData={interactiveChartData} compact hideCombust />
            </div>
          </div>
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
