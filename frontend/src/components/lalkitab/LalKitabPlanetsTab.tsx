import { useEffect, useMemo, useState } from 'react';
import { Star, ChevronDown, ChevronUp, ShieldCheck, Zap, BookOpen } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';
import { Heading } from '@/components/ui/heading';
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

      {/* Astrology Theory Section — General educational summary */}
      <AstrologyTheorySection language={language} />
    </div>
  );
}

function AstrologyTheorySection({ language }: { language: string }) {
  const hi = language === 'hi';
  const l = (en: string, hiStr: string) => (hi ? hiStr : en);

  return (
    <div className="mt-12 space-y-6 pb-10">
      <div className="rounded-xl border border-sacred-gold/30 bg-sacred-gold/5 p-6 overflow-hidden">
        <Heading as={3} variant={3} className="text-sacred-gold-dark mb-4 flex items-center gap-2">
          <BookOpen className="w-5 h-5" />
          {l('Understanding Your Lal Kitab Planets', 'लाल किताब ग्रहों को समझना')}
        </Heading>
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <div className="bg-white/40 p-4 rounded-lg border border-sacred-gold/10">
            <h5 className="font-bold text-sacred-gold-dark text-xs uppercase mb-2">{l('The Actors (Planets)', 'अभिनेता (ग्रह)')}</h5>
            <p className="text-xs text-foreground/70 leading-relaxed">
              {l('In Lal Kitab, planets are the living forces. They can be "Sleeping" (inactive) or "Kayam" (stable and strong).', 'लाल किताब में ग्रह जीवित शक्तियां हैं। वे "सोए हुए" (निष्क्रिय) या "कायम" (स्थिर और मजबूत) हो सकते हैं।')}
            </p>
          </div>
          <div className="bg-white/40 p-4 rounded-lg border border-sacred-gold/10">
            <h5 className="font-bold text-sacred-gold-dark text-xs uppercase mb-2">{l('The Fixed Stage (Houses)', 'निश्चित मंच (भाव)')}</h5>
            <p className="text-xs text-foreground/70 leading-relaxed">
              {l('Lal Kitab uses a fixed house system. Each house has a permanent nature regardless of the sign.', 'लाल किताब एक निश्चित भाव प्रणाली का उपयोग करती है। प्रत्येक भाव का स्वभाव स्थायी होता है, चाहे राशि कोई भी हो।')}
            </p>
          </div>
          <div className="bg-white/40 p-4 rounded-lg border border-sacred-gold/10">
            <h5 className="font-bold text-sacred-gold-dark text-xs uppercase mb-2">{l('The Remedies (Upay)', 'उपाय (लाल किताब)')}</h5>
            <p className="text-xs text-foreground/70 leading-relaxed">
              {l('Planets here are judged by their behavior. If an actor is "Malefic", specific logic-based remedies are given.', 'यहाँ ग्रहों को उनके व्यवहार से आंका जाता है। यदि कोई ग्रह "अशुभ" है, तो विशिष्ट तर्क-आधारित उपाय दिए जाते हैं।')}
            </p>
          </div>
        </div>

        <div className="space-y-4">
          <h4 className="text-sm font-bold text-primary border-b border-sacred-gold/20 pb-1.5 uppercase tracking-wide">
            {l('Core Lal Kitab Concepts', 'लाल किताब के मूल सिद्धांत')}
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="text-xs">
              <span className="font-bold text-sacred-gold-dark">{l('Sleeping Planet:', 'सोया हुआ ग्रह:')}</span>{' '}
              <span className="text-foreground/70">{l('A planet that is not activated. It needs a specific action or time to start giving results.', 'एक ऐसा ग्रह जो सक्रिय नहीं है। इसे परिणाम देना शुरू करने के लिए एक विशिष्ट कार्य या समय की आवश्यकता होती है।')}</span>
            </div>
            <div className="text-xs">
              <span className="font-bold text-sacred-gold-dark">{l('Kayam Grah:', 'कायम ग्रह:')}</span>{' '}
              <span className="text-foreground/70">{l('A planet that is stable, independent, and giving its own results without interference.', 'एक ऐसा ग्रह जो स्थिर, स्वतंत्र है और बिना किसी हस्तक्षेप के अपना परिणाम दे रहा है।')}</span>
            </div>
          </div>
        </div>

        <div className="mt-8 pt-4 border-t border-sacred-gold/20">
          <p className="text-[11px] text-foreground/50 italic text-center">
            {l(
              'Lal Kitab is unique because it focuses on practical "Logic" and simple remedies over complex calculations.',
              'लाल किताब अद्वितीय है क्योंकि यह जटिल गणनाओं के बजाय व्यावहारिक "तर्क" और सरल उपायों पर ध्यान केंद्रित करती है।'
            )}
          </p>
        </div>
      </div>
    </div>
  );
}
