import { useMemo, useState } from 'react';
import { useTranslation } from '@/lib/i18n';
import { useLalKitab } from './LalKitabContext';
import { ChevronDown, ChevronUp, Home, Sparkles } from 'lucide-react';

export default function LalKitabHousesTab() {
  const { t, language } = useTranslation();
  const isHi = language === 'hi';
  const { fullData } = useLalKitab();
  const [expandedHouse, setExpandedHouse] = useState<number | null>(null);

  const byHouse = useMemo(() => {
    const map: Record<number, string[]> = {};
    for (let h = 1; h <= 12; h++) map[h] = [];
    for (const p of (fullData?.positions || [])) {
      const house = Number(p?.house || 0);
      const planet = (p?.planet || '').toString();
      if (house >= 1 && house <= 12 && planet) map[house].push(planet);
    }
    return map;
  }, [fullData]);

  const remedyByHouse = useMemo(() => {
    const map: Record<number, any[]> = {};
    const list = fullData?.remedies?.remedies || [];
    for (const r of list) {
      const h = Number(r?.lk_house || 0);
      if (!h) continue;
      if (!map[h]) map[h] = [];
      map[h].push(r);
    }
    return map;
  }, [fullData]);

  const toggle = (house: number) => setExpandedHouse((prev) => (prev === house ? null : house));

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-semibold text-sacred-gold mb-1">{t('lk.houses.title')}</h2>
        <p className="text-sm text-gray-500">{t('lk.houses.desc')}</p>
      </div>

      <div className="grid gap-4">
        {Array.from({ length: 12 }, (_, i) => i + 1).map((house) => {
          const planets = byHouse[house] || [];
          const remedies = (remedyByHouse[house] || []).filter((r) => r?.has_remedy);
          const urgent = remedies.filter((r) => r?.urgency === 'high');
          const isExpanded = expandedHouse === house;
          return (
            <div key={house} className="card-sacred rounded-xl border border-sacred-gold/20 overflow-hidden transition-all">
              <button
                type="button"
                onClick={() => toggle(house)}
                className="w-full flex items-center justify-between p-4 text-left"
              >
                <div className="flex items-center gap-4">
                  <div className="flex items-center gap-2">
                    <Home className="w-5 h-5 text-sacred-gold/60" />
                    <span className="text-2xl font-bold text-sacred-gold">{house}</span>
                  </div>

                  <div className="flex flex-col gap-1">
                    <span className="text-sm text-foreground">
                      {planets.length ? (isHi ? 'ग्रह:' : 'Planets:') : (isHi ? 'खाली' : 'Empty')}
                    </span>
                    <div className="flex flex-wrap gap-1">
                      {planets.map((p) => (
                        <span key={p} className="bg-sacred-gold/10 text-sacred-gold px-2 py-0.5 rounded-full text-sm font-medium">
                          {isHi ? ({Sun:'सूर्य', Moon:'चंद्र', Mars:'मंगल', Mercury:'बुध', Jupiter:'गुरु', Venus:'शुक्र', Saturn:'शनि', Rahu:'राहु', Ketu:'केतु'}[p] || p) : p}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  {urgent.length > 0 && (
                    <span className="text-xs px-2 py-0.5 rounded-full border border-red-200 bg-red-50 text-red-700 font-semibold">
                      {isHi ? 'अत्यावश्यक' : 'Urgent'}: {urgent.length}
                    </span>
                  )}
                  {isExpanded ? <ChevronUp className="w-5 h-5 text-sacred-gold/60" /> : <ChevronDown className="w-5 h-5 text-sacred-gold/60" />}
                </div>
              </button>

              {isExpanded && (
                <div className="px-4 pb-4 space-y-4 border-t border-sacred-gold/10 pt-4">
                  <div className="flex items-center gap-2">
                    <Sparkles className="w-4 h-4 text-sacred-gold" />
                    <h4 className="text-sm font-semibold text-sacred-gold">
                      {isHi ? 'उपाय (इस भाव के ग्रह)' : 'Remedies (planets in this house)'}
                    </h4>
                  </div>

                  {remedies.length === 0 ? (
                    <p className="text-sm text-gray-600 italic">
                      {isHi ? 'इस भाव के लिए कोई उपाय नहीं मिला।' : 'No remedies found for this house.'}
                    </p>
                  ) : (
                    <div className="space-y-2">
                      {remedies.slice(0, 8).map((r: any) => (
                        <div key={`${r.planet}-${r.lk_house}`} className="rounded-xl border border-border/40 bg-card p-4">
                          <div className="flex items-center justify-between gap-2">
                            <div className="text-sm font-semibold text-foreground">
                              {isHi ? (r.planet_hi || r.planet) : r.planet}
                            </div>
                            {r.urgency && (
                              <span className={`text-[10px] px-2 py-0.5 rounded-full border font-bold ${
                                r.urgency === 'high' ? 'border-red-200 bg-red-50 text-red-700' :
                                r.urgency === 'medium' ? 'border-amber-200 bg-amber-50 text-amber-700' :
                                'border-gray-200 bg-gray-50 text-gray-700'
                              }`}>
                                {isHi
                                  ? ({high:'उच्च', medium:'मध्यम', low:'निम्न'}[r.urgency] || r.urgency)
                                  : r.urgency.charAt(0).toUpperCase() + r.urgency.slice(1)}
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
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

