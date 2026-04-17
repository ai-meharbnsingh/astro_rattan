import { useEffect, useMemo, useState } from 'react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';
import { useLalKitab } from './LalKitabContext';
import { LayoutGrid, AlertTriangle, CheckCircle, Sparkles, Clock } from 'lucide-react';

interface AgeActivationResponse {
  age_years: number | null;
  active: { planet: string; age_start: number; age_end: number } | null;
}

export default function LalKitabDashboardTab({ onNavigateTab }: { onNavigateTab?: (tab: string) => void }) {
  const { t, language } = useTranslation();
  const isHi = language === 'hi';
  const { kundliId, fullData } = useLalKitab();
  const [ageData, setAgeData] = useState<AgeActivationResponse | null>(null);

  useEffect(() => {
    if (!kundliId) { setAgeData(null); return; }
    api.get(`/api/lalkitab/age-activation/${kundliId}`)
      .then((res: any) => setAgeData(res as AgeActivationResponse))
      .catch(() => { /* non-blocking */ });
  }, [kundliId]);

  const occupancy = useMemo(() => {
    const byHouse: Record<number, string[]> = {};
    for (let h = 1; h <= 12; h++) byHouse[h] = [];
    for (const p of (fullData?.positions || [])) {
      const house = Number(p?.house || 0);
      const planet = (p?.planet || '').toString();
      if (house >= 1 && house <= 12 && planet) byHouse[house].push(planet);
    }
    const empty = Object.values(byHouse).filter((ps) => ps.length === 0).length;
    const total = Object.values(byHouse).reduce((a, ps) => a + ps.length, 0);
    return { empty, total, byHouse };
  }, [fullData]);

  const doshas = useMemo(() => {
    const list = Array.isArray(fullData?.doshas) ? fullData.doshas : [];
    const detected = list.filter((d: any) => d?.detected);
    return { total: list.length, detected, detectedCount: detected.length, highCount: detected.filter((d: any) => d?.severity === 'high').length };
  }, [fullData]);

  const quickRemedies = useMemo(() => {
    const rows = (fullData?.remedies?.remedies || []).filter((r: any) => r?.has_remedy);
    const order: Record<string, number> = { high: 0, medium: 1, low: 2 };
    return rows.slice().sort((a: any, b: any) => (order[a?.urgency] ?? 9) - (order[b?.urgency] ?? 9)).slice(0, 6);
  }, [fullData]);

  if (!kundliId) {
    return (
      <div className="text-center py-10 text-muted-foreground text-sm">
        {isHi ? 'कुंडली चुनें या बनाएं।' : 'Select or generate a Kundli.'}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="text-center space-y-2">
        <h2 className="text-2xl font-sans font-bold text-sacred-gold flex items-center justify-center gap-2">
          <LayoutGrid className="w-6 h-6" />
          {t('lk.dashboard.title')}
        </h2>
        <p className="text-sm text-gray-600">{t('lk.dashboard.desc')}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card-sacred rounded-xl p-6 border border-sacred-gold/20">
          <h3 className="font-sans text-lg font-semibold text-sacred-gold mb-4">{t('lk.dashboard.kundliView')}</h3>
          <div className="grid grid-cols-2 gap-3">
            <div className="text-center p-3 rounded-xl bg-sacred-gold/5 border border-sacred-gold/10">
              <p className="text-2xl font-sans font-bold text-foreground">{occupancy.total}</p>
              <p className="text-sm text-gray-500">{isHi ? 'ग्रह' : t('table.planets')}</p>
            </div>
            <div className="text-center p-3 rounded-xl bg-sacred-gold/5 border border-sacred-gold/10">
              <p className="text-2xl font-sans font-bold text-foreground">{occupancy.empty}</p>
              <p className="text-sm text-gray-500">{isHi ? 'खाली भाव' : t('lk.kundli.empty')}</p>
            </div>
          </div>

          {ageData?.active && (
            <div className="mt-4 p-4 rounded-xl border border-sacred-gold/20 bg-sacred-gold/5">
              <div className="flex items-center gap-2 text-sm text-sacred-gold">
                <Clock className="w-4 h-4" />
                <span className="font-semibold">
                  {t('auto.activePlanet')}: {ageData.active.planet}
                </span>
                <span className="text-xs text-muted-foreground">
                  ({isNaN(Number(ageData.active.age_start)) ? 0 : ageData.active.age_start}–{isNaN(Number(ageData.active.age_end)) ? 0 : ageData.active.age_end})
                </span>
              </div>
              <div className="text-xs text-muted-foreground mt-1">
                {t('lk.yearly.currentAge')}: {ageData.age_years ?? '--'}
              </div>
            </div>
          )}
        </div>

        <div className="card-sacred rounded-xl p-6 border border-sacred-gold/20">
          <h3 className="font-sans text-lg font-semibold text-sacred-gold mb-4">{t('lk.dosha.title')}</h3>
          <div className="flex items-center justify-between rounded-xl p-4 border border-sacred-gold/10 bg-sacred-gold/5">
            <div className="text-sm text-foreground">
              {t('lk.dosha.detected')}: <span className="font-semibold">{doshas.detectedCount}</span>
              <span className="text-muted-foreground"> / {doshas.total}</span>
            </div>
            {doshas.detectedCount > 0 ? (
              <AlertTriangle className="w-5 h-5 text-red-500" />
            ) : (
              <CheckCircle className="w-5 h-5 text-green-500" />
            )}
          </div>
          {doshas.highCount > 0 && (
            <div className="mt-3 text-xs text-red-600 font-medium">
              {isHi ? 'उच्च-गंभीरता दोष' : 'High severity'}: {doshas.highCount}
            </div>
          )}

          <button
            onClick={() => onNavigateTab?.('analysis')}
            className="mt-4 text-xs px-3 py-1.5 rounded-full border border-sacred-gold/30 text-sacred-gold hover:border-sacred-gold/60 transition-all"
          >
            {isHi ? 'पूरा विश्लेषण देखें' : 'View full analysis'}
          </button>
        </div>
      </div>

      <div className="card-sacred rounded-xl p-6 border border-sacred-gold/20">
        <div className="flex items-center gap-2 mb-3">
          <Sparkles className="w-4 h-4 text-sacred-gold" />
          <h3 className="font-sans text-lg font-semibold text-sacred-gold">{isHi ? 'त्वरित उपाय' : 'Quick Remedies'}</h3>
        </div>

        {quickRemedies.length === 0 ? (
          <div className="text-sm text-muted-foreground">
            {isHi ? 'कोई तत्काल उपाय नहीं।' : 'No immediate remedies.'}
          </div>
        ) : (
          <div className="grid gap-3 md:grid-cols-2">
            {quickRemedies.map((r: any) => (
              <div key={`${r.planet}-${r.lk_house}`} className="rounded-xl border border-border/40 bg-card p-4">
                <div className="flex items-center justify-between gap-2">
                  <div className="text-sm font-semibold text-foreground">
                    {isHi ? (r.planet_hi || r.planet) : r.planet} · {isHi ? `भाव ${r.lk_house}` : `H${r.lk_house}`}
                  </div>
                  {r.urgency && (
                    <span className={`text-[10px] px-2 py-0.5 rounded-full border font-bold ${
                      r.urgency === 'high' ? 'border-red-200 bg-red-50 text-red-700' :
                      r.urgency === 'medium' ? 'border-amber-200 bg-amber-50 text-amber-700' :
                      'border-gray-200 bg-gray-50 text-gray-700'
                    }`}>
                      {r.urgency}
                    </span>
                  )}
                </div>
                <p className="text-sm text-foreground/80 mt-2 leading-relaxed">
                  {isHi ? r.remedy_hi : r.remedy_en}
                </p>
              </div>
            ))}
          </div>
        )}

        <button
          onClick={() => onNavigateTab?.('upay')}
          className="mt-4 text-xs px-3 py-1.5 rounded-full border border-sacred-gold/30 text-sacred-gold hover:border-sacred-gold/60 transition-all"
        >
          {isHi ? 'सभी उपाय देखें' : 'View all remedies'}
        </button>
      </div>
    </div>
  );
}

