import { useEffect, useMemo, useState } from 'react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';
import { useLalKitab } from './LalKitabContext';
import { Calendar, Star } from 'lucide-react';

interface Period {
  planet: string;
  age_start: number;
  age_end: number;
}

interface AgeActivationResponse {
  kundli_id: string;
  birth_date: string;
  as_of: string;
  age_years: number | null;
  periods: Period[];
  active: Period | null;
}

export default function LalKitabYearlyTab() {
  const { t, language } = useTranslation();
  const isHi = language === 'hi';
  const { kundliId, fullData } = useLalKitab();
  const [data, setData] = useState<AgeActivationResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Map planet->house from consolidated positions (authoritative LK house derivation).
  const planetHouse = useMemo(() => {
    const m: Record<string, number> = {};
    for (const p of (fullData?.positions || [])) {
      const planet = (p?.planet || '').toString();
      const house = Number(p?.house || 0);
      if (planet && house) m[planet] = house;
    }
    return m;
  }, [fullData]);

  useEffect(() => {
    if (!kundliId) { setData(null); return; }
    setError(null);
    api.get(`/api/lalkitab/age-activation/${kundliId}`)
      .then((res: any) => setData(res as AgeActivationResponse))
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
    <div className="space-y-6">
      <div>
        <h2 className="font-sans text-2xl text-sacred-gold flex items-center gap-2">
          <Calendar className="w-6 h-6" />
          {t('lk.yearly.title')}
        </h2>
        <p className="text-gray-500 mt-1">{t('lk.yearly.desc')}</p>
      </div>

      {error && (
        <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-red-700 text-sm">
          {error}
        </div>
      )}

      {data && (
        <>
          <div className="rounded-xl p-6 border border-sacred-gold/20 bg-sacred-gold/5 text-center">
            <p className="text-sm text-sacred-gold/70 mb-1">{t('lk.yearly.currentAge')}</p>
            <p className="text-5xl font-sans font-bold text-sacred-gold">{data.age_years ?? '--'}</p>
            {data.active && (
              <p className="text-sm text-gray-500 mt-2">
                {t('auto.activePlanet')}: <span className="text-sacred-gold font-medium">{data.active.planet}</span>
                {planetHouse[data.active.planet] ? (
                  <span className="text-gray-500"> · {isHi ? 'भाव' : 'House'} {planetHouse[data.active.planet]}</span>
                ) : null}
              </p>
            )}
          </div>

          {data.active && (
            <div className="card-sacred rounded-xl p-5 border border-sacred-gold/30 bg-sacred-gold/5">
              <div className="flex items-start gap-3">
                <Star className="w-5 h-5 text-sacred-gold mt-0.5 shrink-0" />
                <div>
                  <h3 className="font-sans text-lg text-sacred-gold mb-1">
                    {data.active.planet} — {t('lk.yearly.ageRange')}: {data.active.age_start}–{data.active.age_end}
                  </h3>
                  <p className="text-sm text-foreground/80">
                    {isHi ? 'यह समय-चक्र बैकएंड से वास्तविक उम्र के आधार पर गणना किया गया है।' : 'This timing cycle is calculated on the backend from your real age.'}
                  </p>
                </div>
              </div>
            </div>
          )}

          <div className="relative">
            {(data.periods || []).map((p, idx) => {
              const isActive = !!(data.active && data.active.planet === p.planet);
              const isLast = idx === (data.periods || []).length - 1;
              return (
                <div key={`${p.planet}-${idx}`} className="relative flex gap-4">
                  <div className="flex flex-col items-center">
                    <div className={`w-4 h-4 rounded-full shrink-0 z-10 ${isActive ? 'bg-sacred-gold shadow-lg shadow-sacred-gold/30' : 'bg-card border border-sacred-gold/20'}`} />
                    {!isLast && <div className={`w-0.5 flex-1 min-h-[2rem] ${isActive ? 'bg-sacred-gold/40' : 'bg-sacred-gold/10'}`} />}
                  </div>

                  <div className={`pb-6 flex-1 rounded-xl px-4 py-3 mb-2 transition-all ${isActive ? 'border border-sacred-gold/30 bg-sacred-gold/5' : 'border border-transparent'}`}>
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className={`font-sans text-base font-semibold ${isActive ? 'text-sacred-gold' : 'text-gray-600'}`}>
                        {p.planet}
                      </span>
                      <span className={`text-sm px-2 py-0.5 rounded-full ${isActive ? 'bg-sacred-gold/20 text-sacred-gold' : 'bg-card text-gray-600'}`}>
                        {t('lk.yearly.ageRange')}: {p.age_start}–{p.age_end}
                      </span>
                      {planetHouse[p.planet] ? (
                        <span className="text-xs text-muted-foreground">
                          {isHi ? 'भाव' : 'House'} {planetHouse[p.planet]}
                        </span>
                      ) : null}
                      {isActive && (
                        <span className="ml-auto text-sm px-2 py-0.5 rounded-full bg-green-500/15 text-green-600 font-medium">
                          {t('auto.active')}
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </>
      )}
    </div>
  );
}

