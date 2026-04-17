import { useState, useEffect } from 'react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';
import { Coins, TrendingUp, PiggyBank, Loader2, Bookmark, BookmarkCheck } from 'lucide-react';

interface Props {
  kundliId: string;
}

interface IncomeSource {
  hi: string;
  en: string;
}

interface WealthData {
  wealth_score: number;
  wealth_potential_hi: string;
  wealth_potential_en: string;
  jupiter_house: number;
  venus_house: number;
  second_house_planets: string[];
  eleventh_house_planets: string[];
  income_sources: IncomeSource[];
  investment_advice: { hi: string; en: string };
  savings_tip: { hi: string; en: string };
}

const PLANET_HI: Record<string, string> = {
  sun: 'सूर्य', moon: 'चंद्र', mars: 'मंगल', mercury: 'बुध',
  jupiter: 'गुरु', venus: 'शुक्र', saturn: 'शनि', rahu: 'राहु', ketu: 'केतु',
};

function scoreColor(score: number) {
  if (score >= 80) return { bar: 'bg-green-500', badge: 'bg-green-500/15 text-green-700', text: 'text-green-700' };
  if (score >= 60) return { bar: 'bg-sacred-gold', badge: 'bg-sacred-gold/15 text-sacred-gold-dark', text: 'text-sacred-gold-dark' };
  if (score >= 45) return { bar: 'bg-orange-400', badge: 'bg-orange-400/15 text-orange-700', text: 'text-orange-700' };
  return { bar: 'bg-red-400', badge: 'bg-red-400/15 text-red-700', text: 'text-red-700' };
}

export default function LalKitabWealthTab({ kundliId }: Props) {
  const { t, language } = useTranslation();
  const isHi = language === 'hi';

  const [data, setData] = useState<WealthData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  const handleSave = async () => {
    if (!data || !kundliId || saving || saved) return;
    setSaving(true);
    try {
      await api.post('/api/lalkitab/predictions/save', {
        kundli_id: kundliId,
        prediction_type: 'wealth',
        prediction_data: data,
      });
      setSaved(true);
    } catch { /* ignore */ } finally {
      setSaving(false);
    }
  };

  useEffect(() => {
    setSaved(false);
    if (!kundliId) { setData(null); setError(''); return; }
    setLoading(true);
    setError('');
    api.get(`/api/lalkitab/predictions/wealth/${kundliId}`)
      .then((res: any) => setData(res))
      .catch(() => setError(t('auto.failedToLoadWealthPr')))
      .finally(() => setLoading(false));
  }, [kundliId, isHi]);

  if (loading) return (
    <div className="flex items-center justify-center py-20">
      <Loader2 className="w-8 h-8 animate-spin text-sacred-gold" />
    </div>
  );

  if (error) return (
    <div className="p-4 rounded-xl bg-red-50 border border-red-200 text-red-700 text-sm">{error}</div>
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <div className="flex items-start justify-between">
          <h2 className="text-xl font-sans font-semibold text-sacred-gold flex items-center gap-2 mb-1">
            <Coins className="w-5 h-5" />
            {t('auto.wealthPredictions')}
          </h2>
          {data && (
            <button
              onClick={handleSave}
              disabled={saving || saved}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all border disabled:opacity-60
                border-sacred-gold/40 text-sacred-gold hover:bg-sacred-gold/10"
            >
              {saved
                ? <><BookmarkCheck className="w-4 h-4" />{t('auto.saved')}</>
                : saving
                ? <><Loader2 className="w-4 h-4 animate-spin" />{t('auto.saving')}</>
                : <><Bookmark className="w-4 h-4" />{t('auto.save')}</>}
            </button>
          )}
        </div>
        <p className="text-sm text-gray-500">
          {t('auto.wealthAnalysisBasedO')}
        </p>
      </div>

      {data && (
        <>
          {/* Wealth score card */}
          {(() => {
            const clr = scoreColor(data.wealth_score);
            return (
              <div className="card-sacred rounded-xl border border-sacred-gold/20 p-6">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h3 className="font-sans font-semibold text-sacred-gold">
                      {t('auto.wealthPotentialScore')}
                    </h3>
                    <span className={`inline-block mt-1 px-3 py-1 rounded-full text-sm font-semibold ${clr.badge}`}>
                      {isHi ? data.wealth_potential_hi : data.wealth_potential_en}
                    </span>
                  </div>
                  <div className="text-right">
                    <p className={`text-4xl font-bold ${clr.text}`}>{data.wealth_score}</p>
                    <p className="text-xs text-gray-400">/100</p>
                  </div>
                </div>
                <div className="w-full bg-gray-200/60 rounded-full h-3">
                  <div
                    className={`h-3 rounded-full transition-all ${clr.bar}`}
                    style={{ width: `${data.wealth_score}%` }}
                  />
                </div>
              </div>
            );
          })()}

          {/* Jupiter & Venus positions */}
          <div className="grid grid-cols-2 gap-4">
            {[
              { key: 'jupiter', hi: 'गुरु', house: data.jupiter_house, label: { hi: 'गुरु भाव', en: 'Jupiter House' } },
              { key: 'venus',   hi: 'शुक्र', house: data.venus_house,   label: { hi: 'शुक्र भाव', en: 'Venus House' } },
            ].map(({ key, hi, house, label }) => (
              <div key={key} className="card-sacred rounded-xl border border-sacred-gold/20 p-4 text-center">
                <p className="text-xs text-gray-500 mb-1">{isHi ? label.hi : label.en}</p>
                <p className="text-3xl font-bold text-sacred-gold">{house}</p>
                <p className="text-xs text-gray-400 mt-0.5">{isHi ? hi : (key || "").charAt(0).toUpperCase() + key.slice(1)}</p>
              </div>
            ))}
          </div>

          {/* 2nd and 11th house planets */}
          <div className="grid grid-cols-2 gap-4">
            {[
              { label: { hi: 'द्वितीय भाव (धन)', en: '2nd House (Wealth)' }, planets: data.second_house_planets },
              { label: { hi: 'एकादश भाव (लाभ)', en: '11th House (Gains)' }, planets: data.eleventh_house_planets },
            ].map(({ label, planets }, idx) => (
              <div key={idx} className="card-sacred rounded-xl border border-sacred-gold/20 p-4">
                <p className="text-xs font-semibold text-sacred-gold mb-2">
                {isHi ? label.hi : label.en}
              </p>
                {Array.isArray(planets) && planets.filter(Boolean).length > 0 ? (
                  <div className="flex flex-wrap gap-1.5">
                    {planets.filter(Boolean).map((raw: any, pi: number) => {
                      const p = String(raw || '');
                      return (
                        <span key={`${p || 'p'}-${pi}`} className="px-2 py-0.5 rounded-full bg-sacred-gold/10 text-sacred-gold-dark text-xs font-medium">
                          {isHi ? (PLANET_HI[p] ?? p) : (p.charAt(0).toUpperCase() + p.slice(1))}
                        </span>
                      );
                    })}
                  </div>
                ) : (
                  <p className="text-xs text-gray-400">{t('auto.noPlanets')}</p>
                )}
              </div>
            ))}
          </div>

          {/* Income sources */}
          {data.income_sources.length > 0 && (
            <div className="card-sacred rounded-xl border border-sacred-gold/20 p-5">
              <h3 className="font-sans font-semibold text-sacred-gold mb-4 flex items-center gap-2">
                <TrendingUp className="w-4 h-4" />
                {t('auto.incomeSources')}
              </h3>
              <div className="space-y-2">
                {data.income_sources.map((src, i) => (
                  <div key={i} className="flex items-center gap-3 p-3 rounded-lg bg-sacred-gold/5 border border-sacred-gold/15">
                    <span className="w-6 h-6 rounded-full bg-sacred-gold/20 text-sacred-gold text-xs font-bold flex items-center justify-center shrink-0">
                      {i + 1}
                    </span>
                    <p className="text-sm text-foreground">{isHi ? src.hi : src.en}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Investment advice */}
          <div className="card-sacred rounded-xl border border-blue-300/30 p-5 bg-blue-500/5">
            <h3 className="font-sans font-semibold text-blue-700 mb-2 flex items-center gap-2">
              <Coins className="w-4 h-4" />
              {t('auto.investmentAdvice')}
            </h3>
            <p className="text-sm text-foreground/80 leading-relaxed">
              {isHi ? data.investment_advice.hi : data.investment_advice.en}
            </p>
          </div>

          {/* Savings tip */}
          <div className="card-sacred rounded-xl border border-green-300/30 p-5 bg-green-500/5">
            <h3 className="font-sans font-semibold text-green-700 mb-2 flex items-center gap-2">
              <PiggyBank className="w-4 h-4" />
              {t('auto.savingsTip')}
            </h3>
            <p className="text-sm text-foreground/80 leading-relaxed">
              {isHi ? data.savings_tip.hi : data.savings_tip.en}
            </p>
          </div>
        </>
      )}
    </div>
  );
}
