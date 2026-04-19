import { useState, useEffect } from 'react';
import { Loader2, TrendingUp, Compass, Sparkles, Gauge, BookOpen, Info } from 'lucide-react';
import { api } from '@/lib/api';
import { Heading } from '@/components/ui/heading';
import { translatePlanet, translateSign } from '@/lib/backend-translations';

// ───────────────────────────────────────────────────────────────
// Types
// ───────────────────────────────────────────────────────────────
interface HouseStrength {
  house: number;
  sign: string;
  sav_bindus: number;
  status: 'strong' | 'moderate' | 'weak';
  interpretation_en: string;
  interpretation_hi: string;
  sloka_ref: string;
}

interface PlanetStrength {
  planet: string;
  sign: string;
  bindus_in_transit_sign: number;
  threshold: number;
  assessment: 'favorable' | 'unfavorable';
  interpretation_en: string;
  interpretation_hi: string;
  sloka_ref: string;
}

interface SpecialCombo {
  combo: string;
  label_en: string;
  label_hi: string;
  houses: number[];
  total_bindus: number;
  threshold: number;
  achieved: boolean;
  effect_en: string;
  effect_hi: string;
  sloka_ref: string;
}

interface TransitRec {
  planet: string;
  strongest_rasi: string;
  strongest_bindus: number;
  weakest_rasi: string;
  weakest_bindus: number;
  guidance_en: string;
  guidance_hi: string;
  sloka_ref: string;
}

interface PhalaData {
  kundli_id?: string;
  person_name?: string;
  house_strengths: HouseStrength[];
  planet_strengths: PlanetStrength[];
  special_combinations: SpecialCombo[];
  transit_recommendations: TransitRec[];
  overall_score: number;
  sloka_ref: string;
}

// ───────────────────────────────────────────────────────────────
// Style helpers
// ───────────────────────────────────────────────────────────────
const STATUS_BAR: Record<HouseStrength['status'], string> = {
  strong:   'bg-emerald-500',
  moderate: 'bg-amber-500',
  weak:     'bg-red-500',
};

const STATUS_TEXT: Record<HouseStrength['status'], string> = {
  strong:   'text-emerald-700',
  moderate: 'text-amber-700',
  weak:     'text-red-700',
};

const STATUS_BORDER: Record<HouseStrength['status'], string> = {
  strong:   'border-emerald-300 bg-emerald-50',
  moderate: 'border-amber-300 bg-amber-50',
  weak:     'border-red-300 bg-red-50',
};

const COMBO_COLOR_OK    = 'border-emerald-300 bg-emerald-50 text-emerald-900';
const COMBO_COLOR_MISS  = 'border-amber-300 bg-amber-50 text-amber-900';
const COMBO_COLOR_BAD   = 'border-red-300 bg-red-50 text-red-900';

interface Props {
  kundliId: string;
  language: string;
  t: (key: string) => string;
}

// Maximum SAV bindus per sign (theoretical) — 7 planets × 8 = 56, but most signs cap ~48
const SAV_SIGN_MAX = 56;

export default function AshtakvargaPhalaTab({ kundliId, language, t }: Props) {
  const [data, setData] = useState<PhalaData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const isHi = language === 'hi';

  useEffect(() => {
    if (!kundliId) return;
    let cancelled = false;
    setLoading(true);
    setError('');
    (async () => {
      try {
        const res = await api.get<PhalaData>(`/api/kundli/${kundliId}/ashtakvarga-phala`);
        if (!cancelled) setData(res);
      } catch (err: any) {
        if (!cancelled) setError(err?.message || 'Failed to load ashtakvarga-phala');
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => { cancelled = true; };
  }, [kundliId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-8 h-8 animate-spin text-sacred-gold" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 rounded-lg bg-red-50 border border-red-200 text-red-700 text-sm">
        {error}
      </div>
    );
  }

  if (!data) return null;

  const statusLabel = (s: HouseStrength['status']): string => {
    if (s === 'strong') return t('auto.strengthStrong');
    if (s === 'moderate') return t('auto.strengthModerate');
    return t('auto.strengthWeak');
  };

  const score = data.overall_score ?? 0;
  const scoreColor = score >= 70 ? 'text-emerald-700' : score >= 50 ? 'text-amber-700' : 'text-red-700';
  const scoreBar = score >= 70 ? 'bg-emerald-500' : score >= 50 ? 'bg-amber-500' : 'bg-red-500';

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
          <Sparkles className="w-6 h-6" />
          {t('auto.ashtakvargaPhala')}
        </Heading>
        <p className="text-sm text-muted-foreground">{t('auto.ashtakvargaPhalaDesc')}</p>
      </div>

      {/* Overall Score */}
      <div className="p-4 rounded-xl border border-sacred-gold/30 bg-gradient-to-r from-sacred-gold/5 to-transparent">
        <div className="flex items-center gap-3 mb-2">
          <Gauge className="w-5 h-5 text-sacred-gold-dark" />
          <h3 className="text-base font-bold text-sacred-gold-dark">{t('auto.overallAshtakvargaScore')}</h3>
        </div>
        <div className="flex items-baseline gap-2 mb-2">
          <span className={`text-4xl font-bold ${scoreColor}`}>{score}</span>
          <span className="text-muted-foreground">/ 100</span>
        </div>
        <div className="w-full h-3 bg-gray-200 rounded-full overflow-hidden">
          <div className={`h-full ${scoreBar} transition-all`} style={{ width: `${score}%` }} />
        </div>
        <p className="text-[11px] italic text-muted-foreground mt-2 flex items-center gap-1">
          <BookOpen className="w-3 h-3" />{data.sloka_ref}
        </p>
      </div>

      {/* House Strengths */}
      <section>
        <h3 className="text-lg font-bold text-sacred-gold-dark mb-3 flex items-center gap-2">
          <TrendingUp className="w-5 h-5" />
          {t('auto.houseStrength')}
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          {data.house_strengths.map((h) => {
            const pct = Math.min(100, Math.round((h.sav_bindus / SAV_SIGN_MAX) * 100));
            return (
              <div key={h.house} className={`rounded-lg border p-3 ${STATUS_BORDER[h.status]}`}>
                <div className="flex items-center justify-between gap-2 mb-1">
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-bold">
                      {t('auto.house')} {h.house}
                    </span>
                    <span className="text-xs text-muted-foreground">
                      {translateSign(h.sign, language)}
                    </span>
                  </div>
                  <span className={`text-xs font-semibold uppercase tracking-wider px-2 py-0.5 rounded bg-white/60 ${STATUS_TEXT[h.status]}`}>
                    {statusLabel(h.status)}
                  </span>
                </div>
                <div className="flex items-center gap-2 mb-1">
                  <div className="flex-1 h-2 bg-white/80 rounded-full overflow-hidden">
                    <div className={`h-full ${STATUS_BAR[h.status]}`} style={{ width: `${pct}%` }} />
                  </div>
                  <span className="text-xs font-semibold tabular-nums">
                    {h.sav_bindus}
                  </span>
                </div>
                <p className="text-[11px] leading-snug opacity-90">
                  {isHi ? h.interpretation_hi : h.interpretation_en}
                </p>
              </div>
            );
          })}
        </div>
        <p className="text-[11px] italic text-muted-foreground mt-2 flex items-center gap-1">
          <BookOpen className="w-3 h-3" />{t('auto.savBindus')} · Adh. 24 sloka 2
        </p>
      </section>

      {/* Planet Transit Strengths */}
      <section>
        <h3 className="text-lg font-bold text-sacred-gold-dark mb-3 flex items-center gap-2">
          <Compass className="w-5 h-5" />
          {t('auto.transitRecommendations')}
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {data.planet_strengths.map((p) => {
            const favorable = p.assessment === 'favorable';
            const border = favorable ? 'border-emerald-300 bg-emerald-50' : 'border-red-300 bg-red-50';
            return (
              <div key={p.planet} className={`rounded-lg border p-3 ${border}`}>
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-bold text-sm">
                    {translatePlanet(p.planet, language)}
                  </h4>
                  <span className={`text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded ${favorable ? 'bg-emerald-200 text-emerald-900' : 'bg-red-200 text-red-900'}`}>
                    {favorable ? t('auto.transitFavorable') : t('auto.transitUnfavorable')}
                  </span>
                </div>
                <p className="text-xs mb-1">
                  <span className="font-semibold">{translateSign(p.sign, language)}</span>
                  {' · '}
                  <span className="tabular-nums">{p.bindus_in_transit_sign}</span>
                  {' / '}
                  <span className="text-muted-foreground">{p.threshold}</span>
                </p>
                <p className="text-[11px] leading-snug opacity-90">
                  {isHi ? p.interpretation_hi : p.interpretation_en}
                </p>
                <p className="text-[10px] italic text-muted-foreground mt-2 flex items-center gap-1">
                  <BookOpen className="w-3 h-3" />{p.sloka_ref}
                </p>
              </div>
            );
          })}
        </div>
      </section>

      {/* Special Combinations */}
      <section>
        <h3 className="text-lg font-bold text-sacred-gold-dark mb-3 flex items-center gap-2">
          <Sparkles className="w-5 h-5" />
          {t('auto.specialCombinations')}
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {data.special_combinations.map((c) => {
            const isDusthana = c.combo === 'dusthana_obstacles';
            // For dusthana, "achieved" = affliction (bad); for others, achieved = good.
            let colorCls = COMBO_COLOR_MISS;
            if (isDusthana) {
              colorCls = c.achieved ? COMBO_COLOR_BAD : COMBO_COLOR_OK;
            } else {
              colorCls = c.achieved ? COMBO_COLOR_OK : COMBO_COLOR_MISS;
            }
            return (
              <div key={c.combo} className={`rounded-xl border-2 p-4 ${colorCls}`}>
                <div className="flex items-start justify-between gap-2 mb-2">
                  <h4 className="font-bold">{isHi ? c.label_hi : c.label_en}</h4>
                  <span className="text-[10px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded bg-white/60 tabular-nums">
                    {c.total_bindus} / {c.threshold}
                  </span>
                </div>
                <p className="text-xs opacity-80 mb-2">
                  {t('auto.house')}: {c.houses.join(' + ')}
                </p>
                <p className="text-xs leading-relaxed mb-2">
                  {isHi ? c.effect_hi : c.effect_en}
                </p>
                <div className="flex items-center gap-1.5 mt-2 pt-2 border-t border-current/15 text-[10px] opacity-70">
                  <BookOpen className="w-3 h-3" />
                  <span className="italic">{c.sloka_ref}</span>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* Transit Recommendations (strongest / weakest per planet) */}
      <section>
        <h3 className="text-lg font-bold text-sacred-gold-dark mb-3 flex items-center gap-2">
          <Info className="w-5 h-5" />
          {t('auto.bestWorstTransitRasi')}
        </h3>
        <div className="overflow-x-auto rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <table className="table-sacred w-full text-sm border-collapse">
            <thead>
              <tr className="border-b border-sacred-gold/30 bg-sacred-gold/5">
                <th className="text-left p-2 font-semibold">{t('auto.planet')}</th>
                <th className="text-left p-2 font-semibold text-emerald-700">
                  {t('auto.strongestTransit')}
                </th>
                <th className="text-left p-2 font-semibold text-red-700">
                  {t('auto.weakestTransit')}
                </th>
                <th className="text-left p-2 font-semibold">{t('auto.guidance')}</th>
              </tr>
            </thead>
            <tbody>
              {data.transit_recommendations.map((r) => (
                <tr key={r.planet} className="border-b border-sacred-gold/15">
                  <td className="p-2 font-semibold">{translatePlanet(r.planet, language)}</td>
                  <td className="p-2 text-emerald-700">
                    {translateSign(r.strongest_rasi, language)}{' '}
                    <span className="text-xs tabular-nums">({r.strongest_bindus})</span>
                  </td>
                  <td className="p-2 text-red-700">
                    {translateSign(r.weakest_rasi, language)}{' '}
                    <span className="text-xs tabular-nums">({r.weakest_bindus})</span>
                  </td>
                  <td className="p-2 text-xs leading-snug opacity-90">
                    {isHi ? r.guidance_hi : r.guidance_en}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="text-[11px] italic text-muted-foreground mt-2 flex items-center gap-1">
          <BookOpen className="w-3 h-3" />Phaladeepika Adh. 24
        </p>
      </section>
    </div>
  );
}
