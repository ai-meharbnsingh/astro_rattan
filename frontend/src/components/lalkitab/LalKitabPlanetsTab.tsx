import { useEffect, useMemo, useState } from 'react';
import { Star, ChevronDown, ChevronUp, ShieldCheck, Zap, BookOpen } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';
import { pickLang } from './safe-render';
import { useLalKitab } from './LalKitabContext';
import { LK_PLANETS } from './lalkitab-core';

interface EnrichedRemedyRow {
  planet: string;
  planet_hi?: string;
  lk_house: number;
  sign?: string;
  dignity?: string;
  strength?: number;
  has_remedy?: boolean;
  urgency?: string;
  remedy_en?: string;
  remedy_hi?: string;
}

export default function LalKitabPlanetsTab() {
  const { t, language } = useTranslation();
  const isHi = language === 'hi';
  const { kundliId, fullData } = useLalKitab();
  const [expanded, setExpanded] = useState<string | null>(null);
  const [interpretations, setInterpretations] = useState<any[]>([]);
  const [loadError, setLoadError] = useState<string | null>(null);

  useEffect(() => {
    if (!kundliId) return;
    setLoadError(null);
    // Fetch LK house interpretations (bilingual) used in expanded view.
    api.post('/api/lalkitab/lk-interpretations', { kundli_id: kundliId })
      .then((res: any) => setInterpretations(Array.isArray(res?.interpretations) ? res.interpretations : []))
      .catch((err) => {
        console.error('Failed to load LK interpretations:', err);
        const msg = err instanceof Error ? err.message : (typeof err === 'string' ? err : 'Unknown error');
        setLoadError(msg);
      });
  }, [kundliId]);

  const byPlanetHouse = useMemo(() => {
    const m: Record<string, number> = {};
    for (const p of (fullData?.positions || [])) {
      const planet = (p?.planet || '').toString();
      const house = Number(p?.house || 0);
      if (planet && house) m[planet] = house;
    }
    return m;
  }, [fullData]);

  const remedyByPlanet = useMemo(() => {
    const m: Record<string, EnrichedRemedyRow | null> = {};
    const rows: EnrichedRemedyRow[] = fullData?.remedies?.remedies || [];
    for (const r of rows) {
      if (r?.planet) m[r.planet] = r;
    }
    return m;
  }, [fullData]);

  const kayamSet = useMemo(() => {
    const s = new Set<string>();
    const ks = fullData?.technical?.kayam;
    if (Array.isArray(ks)) {
      for (const x of ks) {
        const p = (x?.planet || '').toString();
        if (p) s.add(p);
      }
    }
    return s;
  }, [fullData]);

  const planetStatuses = useMemo(() => {
    // technical.planet_statuses is backend-derived and stable; if missing, empty.
    return fullData?.technical?.planet_statuses || {};
  }, [fullData]);

  const toggle = (p: string) => setExpanded((prev) => (prev === p ? null : p));

  const findInterp = (planet: string, house: number) => {
    const key = `${planet.toLowerCase()}_${house}`;
    return interpretations.find((it: any) => (it?.key || '').toString() === key) || null;
  };

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
        <h2 className="text-2xl text-sacred-gold">{t('lk.planets.title')}</h2>
        <p className="text-gray-600 text-sm">{t('lk.planets.desc')}</p>
      </div>

      {loadError && (
        <div className="p-3 mb-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-800">
          {isHi ? 'डेटा लोड करने में त्रुटि' : 'Failed to load data'}: {loadError}
        </div>
      )}

      <div className="flex flex-wrap justify-center gap-4 py-2 border-y border-sacred-gold/10">
        <div className="flex items-center gap-1.5 text-xs text-foreground/70">
          <Zap className="w-3.5 h-3.5 text-green-500" />
          <span>{t('lk.planets.active')}</span>
        </div>
        <div className="flex items-center gap-1.5 text-xs text-foreground/70">
          <ShieldCheck className="w-3.5 h-3.5 text-sacred-gold" />
          <span>{t('lk.planets.stable')}</span>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {LK_PLANETS.map((planetKey) => {
          const planet = planetKey as string;
          const house = byPlanetHouse[planet] || 0;
          const rr = remedyByPlanet[planet] || null;
          const isKayam = kayamSet.has(planet);
          const status = planetStatuses?.[planet] || null;
          const isSleeping = status?.sleeping_status === 'sleeping';
          const isExpanded = expanded === planet;
          const interp = house ? findInterp(planet, house) : null;

          return (
            <div
              key={planet}
              className={`card-sacred rounded-xl border p-5 transition-all ${
                isExpanded ? 'border-sacred-gold/40 bg-sacred-gold/5' : 'border-sacred-gold/20'
              }`}
            >
              <button type="button" onClick={() => toggle(planet)} className="w-full text-left">
                <div className="flex items-start justify-between gap-3">
                  <div className="min-w-0">
                    <div className="flex items-center gap-2">
                      <Star className="w-4 h-4 text-sacred-gold" />
                      <h3 className="font-sans font-semibold text-sacred-gold truncate">
                        {isHi ? (rr?.planet_hi || planet) : planet}
                      </h3>
                    </div>
                    <p className="text-xs text-muted-foreground mt-1">
                      {house ? (isHi ? `भाव ${house}` : `House ${house}`) : (isHi ? 'भाव अज्ञात' : 'House unknown')}
                      {rr?.sign ? ` · ${rr.sign}` : ''}
                    </p>
                  </div>

                  <div className="flex flex-col items-end gap-1">
                    {isSleeping ? (
                      <span className="mt-1 flex items-center gap-1 text-[10px] font-bold text-orange-700 bg-orange-50 px-1.5 py-0.5 rounded border border-orange-200">
                        {t('lk.planets.sleeping')}
                      </span>
                    ) : (
                      <span className="mt-1 flex items-center gap-1 text-[10px] font-bold text-green-700 bg-green-50 px-1.5 py-0.5 rounded border border-green-200">
                        <Zap className="w-2.5 h-2.5" />
                        {t('lk.planets.active')}
                      </span>
                    )}
                    {isKayam && (
                      <span className="mt-1 flex items-center gap-1 text-[10px] font-bold text-sacred-gold-dark bg-sacred-gold/10 px-1.5 py-0.5 rounded border border-sacred-gold/20">
                        <ShieldCheck className="w-2.5 h-2.5" />
                        {t('auto.kAYAM')}
                      </span>
                    )}
                    {isExpanded ? (
                      <ChevronUp className="w-4 h-4 text-sacred-gold/60" />
                    ) : (
                      <ChevronDown className="w-4 h-4 text-sacred-gold/60" />
                    )}
                  </div>
                </div>
              </button>

              {isExpanded && (
                <div className="mt-4 space-y-4 border-t border-sacred-gold/10 pt-4">
                  <div className="grid gap-2">
                    <div className="rounded-lg border border-border/40 bg-card p-3">
                      <div className="text-[10px] font-bold text-gray-400 uppercase tracking-widest">
                        {isHi ? 'शक्ति' : 'Strength'}
                      </div>
                      <div className="text-sm text-foreground mt-1">
                        {rr?.strength != null ? `${rr.strength}` : '--'}
                        {rr?.dignity ? <span className="text-xs text-muted-foreground"> · {rr.dignity}</span> : null}
                      </div>
                      {rr?.has_remedy && (
                        <div className="text-xs text-muted-foreground mt-1">
                          {isHi ? 'उपाय:' : 'Remedy:'} {isHi ? rr.remedy_hi : rr.remedy_en}
                        </div>
                      )}
                    </div>
                  </div>

                  <div className="rounded-lg border border-border/40 bg-card p-3">
                    <div className="flex items-center gap-2 mb-2">
                      <BookOpen className="w-4 h-4 text-sacred-gold" />
                      <div className="text-sm font-semibold text-sacred-gold">
                        {isHi ? 'भाव व्याख्या' : 'House Interpretation'}
                      </div>
                    </div>
                    {interp ? (
                      <div className="text-sm text-foreground/80 leading-relaxed">
                        {pickLang(interp, isHi)}
                      </div>
                    ) : (
                      <div className="text-xs text-muted-foreground">
                        {isHi ? 'इस ग्रह/भाव के लिए व्याख्या उपलब्ध नहीं।' : 'No interpretation available for this planet/house.'}
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
