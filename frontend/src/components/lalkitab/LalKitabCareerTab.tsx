import { useState, useEffect } from 'react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';
import { Briefcase, TrendingUp, Clock, Loader2, Bookmark, BookmarkCheck } from 'lucide-react';
import { pickLang } from './safe-render';

interface Props {
  kundliId: string;
}

interface CareerData {
  tenth_house_planets: string[];
  primary_planet: string | null;
  career_options: string[];
  career_options_en: string[];
  nature: string;
  suitability: string;
  favourable_ages: number[];
  sun_house: number;
  saturn_house: number;
  mercury_house: number;
  advice: { hi: string; en: string };
}

const PLANET_HI: Record<string, string> = {
  sun: 'सूर्य', moon: 'चंद्र', mars: 'मंगल', mercury: 'बुध',
  jupiter: 'गुरु', venus: 'शुक्र', saturn: 'शनि', rahu: 'राहु', ketu: 'केतु',
};

export default function LalKitabCareerTab({ kundliId }: Props) {
  const { t, language } = useTranslation();
  const isHi = language === 'hi';

  const [data, setData] = useState<CareerData | null>(null);
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
        prediction_type: 'career',
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
    api.get(`/api/lalkitab/predictions/career/${kundliId}`)
      .then((res: any) => setData(res))
      .catch(() => setError(t('auto.failedToLoadCareerPr')))
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
            <Briefcase className="w-5 h-5" />
            {t('auto.careerPredictions')}
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
          {t('auto.careerAnalysisBasedO')}
        </p>
      </div>

      {data && (
        <>
          {/* Suitability badge */}
          <div className={`card-sacred rounded-xl border p-5 ${
            data.suitability === 'business'
              ? 'border-blue-300/30 bg-blue-500/5'
              : 'border-green-300/30 bg-green-500/5'
          }`}>
            <div className="flex items-center gap-4">
              <div className={`w-14 h-14 rounded-full flex items-center justify-center ${
                data.suitability === 'business' ? 'bg-blue-500/15' : 'bg-green-500/15'
              }`}>
                <TrendingUp className={`w-7 h-7 ${data.suitability === 'business' ? 'text-blue-600' : 'text-green-600'}`} />
              </div>
              <div>
                <h3 className={`text-lg font-sans font-bold ${data.suitability === 'business' ? 'text-blue-700' : 'text-green-700'}`}>
                  {data.suitability === 'business'
                    ? (t('auto.businessSuited'))
                    : (t('auto.jobSuited'))}
                </h3>
                <p className="text-sm text-foreground/70 mt-0.5">
                  {pickLang(data?.advice, isHi)}
                </p>
              </div>
            </div>
          </div>

          {/* 10th house */}
          <div className="card-sacred rounded-xl border border-sacred-gold/20 p-5">
            <h3 className="font-sans font-semibold text-sacred-gold mb-3">
              {t('auto.10thHousePlanets')}
            </h3>
            {Array.isArray(data.tenth_house_planets) && data.tenth_house_planets.filter(Boolean).length > 0 ? (
              <div className="flex flex-wrap gap-2">
                {data.tenth_house_planets.filter(Boolean).map((raw: any, idx: number) => {
                  const p = String(raw || '');
                  return (
                    <span key={`${p || 'p'}-${idx}`} className="px-3 py-1 rounded-full bg-sacred-gold/10 text-sacred-gold-dark text-sm font-medium">
                      {isHi ? (PLANET_HI[p] ?? p) : (p.charAt(0).toUpperCase() + p.slice(1))}
                    </span>
                  );
                })}
              </div>
            ) : (
              <p className="text-sm text-gray-500">
                {t('auto.noPlanetIn10thHouse')}
              </p>
            )}
          </div>

          {/* Career options */}
          <div className="card-sacred rounded-xl border border-sacred-gold/20 p-5">
            <h3 className="font-sans font-semibold text-sacred-gold mb-4 flex items-center gap-2">
              <Briefcase className="w-4 h-4" />
              {t('auto.suitableCareerOption')}
            </h3>
            <div className="grid gap-2 sm:grid-cols-2">
              {(isHi ? data.career_options : data.career_options_en).map((c, i) => (
                <div key={i} className="flex items-center gap-2 p-3 rounded-lg bg-sacred-gold/5 border border-sacred-gold/15">
                  <span className="w-6 h-6 rounded-full bg-sacred-gold/20 text-sacred-gold text-xs font-bold flex items-center justify-center shrink-0">
                    {i + 1}
                  </span>
                  <span className="text-sm text-foreground">{c}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Favourable ages */}
          <div className="card-sacred rounded-xl border border-sacred-gold/20 p-5">
            <h3 className="font-sans font-semibold text-sacred-gold mb-3 flex items-center gap-2">
              <Clock className="w-4 h-4" />
              {t('auto.favourableAgePeriods')}
            </h3>
            <div className="flex flex-wrap gap-3">
              {data.favourable_ages.map((age) => (
                <div key={age} className="flex flex-col items-center px-5 py-3 rounded-xl bg-sacred-gold/10 border border-sacred-gold/20">
                  <span className="text-2xl font-bold text-sacred-gold">{age}</span>
                  <span className="text-xs text-gray-500 mt-0.5">{t('auto.years')}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Key planet positions */}
          <div className="card-sacred rounded-xl border border-sacred-gold/20 p-5">
            <h3 className="font-sans font-semibold text-sacred-gold mb-3">
              {t('auto.keyPlanetPositions')}
            </h3>
            <div className="grid grid-cols-3 gap-3">
              {[
                { planet: 'sun', house: data.sun_house, hi: 'सूर्य' },
                { planet: 'saturn', house: data.saturn_house, hi: 'शनि' },
                { planet: 'mercury', house: data.mercury_house, hi: 'बुध' },
              ].map(({ planet, house, hi }) => (
                <div key={planet} className="text-center p-3 rounded-xl bg-sacred-gold/5 border border-sacred-gold/15">
                  <p className="text-xs text-gray-500 mb-1">{isHi ? hi : (planet || "").charAt(0).toUpperCase() + planet.slice(1)}</p>
                  <p className="text-xl font-bold text-sacred-gold">{house}</p>
                  <p className="text-xs text-gray-400">{t('auto.house')}</p>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
}
