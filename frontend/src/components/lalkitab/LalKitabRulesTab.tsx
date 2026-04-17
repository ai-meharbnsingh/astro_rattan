import { useEffect, useState } from 'react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';
import { useLalKitab } from './LalKitabContext';
import { BookOpen, Layers } from 'lucide-react';

interface RulesResponse {
  kundli_id: string;
  mirror_axis: Array<{
    h1: number;
    h2: number;
    planets_h1: string[];
    planets_h2: string[];
    has_mutual: boolean;
  }>;
  cross_effects: Array<{
    idx: number;
    from_house: number;
    to_house: number;
    trigger_planets: string[];
    has_trigger: boolean;
  }>;
}

export default function LalKitabRulesTab() {
  const { t, language } = useTranslation();
  const isHi = language === 'hi';
  const { kundliId } = useLalKitab();
  const [data, setData] = useState<RulesResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!kundliId) { setData(null); return; }
    setError(null);
    api.get(`/api/lalkitab/rules/${kundliId}`)
      .then((res: any) => setData(res as RulesResponse))
      .catch((e: any) => setError(e instanceof Error ? e.message : (isHi ? 'लोड नहीं हो सका' : 'Failed to load')));
  }, [kundliId]);

  if (!kundliId) {
    return (
      <div className="text-center py-10 text-muted-foreground text-sm">
        {isHi ? 'कुंडली चुनें या बनाएं।' : 'Select or generate a Kundli.'}
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div>
        <h2 className="font-sans text-2xl text-sacred-gold flex items-center gap-2">
          <BookOpen className="w-6 h-6" />
          {t('lk.rules.title')}
        </h2>
        <p className="text-gray-500 mt-1">{t('lk.rules.desc')}</p>
      </div>

      {error && (
        <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-red-700 text-sm">
          {error}
        </div>
      )}

      {/* Mirror House Axis */}
      <section>
        <h3 className="font-sans text-lg text-sacred-gold mb-4">{t('lk.rules.mirrorAxis')}</h3>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {(data?.mirror_axis || []).map((pair) => (
            <div
              key={`${pair.h1}-${pair.h2}`}
              className={`card-sacred rounded-xl border transition-all ${
                pair.has_mutual ? 'border-sacred-gold/40 bg-sacred-gold/5' : 'border-sacred-gold/20'
              }`}
            >
              <div className="flex items-stretch">
                <div className="flex-1 p-4 text-center">
                  <p className="text-sm text-gray-600 mb-1">{t('auto.house')}</p>
                  <p className="text-2xl font-sans font-bold text-sacred-gold">{pair.h1}</p>
                  <div className="mt-2 space-y-1">
                    {pair.planets_h1?.length ? (
                      pair.planets_h1.map((p) => (
                        <span key={p} className="inline-block px-2 py-0.5 rounded-full bg-sacred-gold/10 text-sacred-gold text-sm font-medium mr-1">
                          {p}
                        </span>
                      ))
                    ) : (
                      <span className="text-sm text-gray-500 italic">{t('auto.empty')}</span>
                    )}
                  </div>
                </div>
                <div className="flex items-center justify-center px-2">
                  <span className="text-sacred-gold/60 text-xl">&#10231;</span>
                </div>
                <div className="flex-1 p-4 text-center">
                  <p className="text-sm text-gray-600 mb-1">{t('auto.house')}</p>
                  <p className="text-2xl font-sans font-bold text-sacred-gold">{pair.h2}</p>
                  <div className="mt-2 space-y-1">
                    {pair.planets_h2?.length ? (
                      pair.planets_h2.map((p) => (
                        <span key={p} className="inline-block px-2 py-0.5 rounded-full bg-sacred-gold/10 text-sacred-gold text-sm font-medium mr-1">
                          {p}
                        </span>
                      ))
                    ) : (
                      <span className="text-sm text-gray-500 italic">{t('auto.empty')}</span>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}
          {!error && (data?.mirror_axis || []).length === 0 && (
            <div className="text-sm text-muted-foreground">{isHi ? 'कोई डेटा नहीं।' : 'No data.'}</div>
          )}
        </div>
      </section>

      <div className="border-t border-sacred-gold/10" />

      {/* Cross-House Effects (generic triggers; text is via i18n) */}
      <section>
        <h3 className="font-sans text-lg text-sacred-gold mb-4 flex items-center gap-2">
          <Layers className="w-5 h-5" />
          {t('lk.rules.crossEffect')}
        </h3>
        <div className="space-y-4">
          {(data?.cross_effects || []).map((rule) => (
            <div
              key={rule.idx}
              className={`card-sacred rounded-xl p-4 border border-sacred-gold/20 ${rule.has_trigger ? 'bg-sacred-gold/5' : ''}`}
            >
              <div className="flex items-center gap-3 mb-2 flex-wrap">
                <span className="px-2.5 py-1 rounded-lg bg-sacred-gold/10 text-sacred-gold text-sm font-sans font-medium">
                  {t('auto.house')} {isNaN(Number(rule.from_house)) ? 0 : rule.from_house}
                </span>
                <span className="text-sacred-gold/40">&#10230;</span>
                <span className="px-2.5 py-1 rounded-lg bg-sacred-gold/10 text-sacred-gold text-sm font-sans font-medium">
                  {t('auto.house')} {isNaN(Number(rule.to_house)) ? 0 : rule.to_house}
                </span>
                <span className="text-sm text-gray-500">
                  ({t('lk.rules.cross.domain.' + rule.idx)})
                </span>
              </div>

              <p className="text-sm text-gray-600">{t('lk.rules.cross.' + rule.idx)}</p>

              {rule.has_trigger && (
                <div className="mt-3 pt-3 border-t border-sacred-gold/10">
                  <p className="text-sm text-gray-600 mb-1.5">{t('auto.currentPlanetsInHous')}</p>
                  <div className="flex gap-2 flex-wrap">
                    {rule.trigger_planets.map((p) => (
                      <span key={p} className="inline-block px-2 py-0.5 rounded-full bg-sacred-gold/15 text-sacred-gold text-sm font-medium">
                        {p}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

