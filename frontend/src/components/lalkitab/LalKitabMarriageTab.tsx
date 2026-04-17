import { useState, useEffect } from 'react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';
import { pickLang } from '@/components/lalkitab/safe-render';
import { Heart, AlertTriangle, CheckCircle2, Loader2, Flame, Bookmark, BookmarkCheck } from 'lucide-react';

interface Props {
  kundliId: string;
}

interface MarriageData {
  is_manglik: boolean;
  manglik_severity: string;
  mars_house: number;
  venus_house: number;
  spouse_description: { hi: string; en: string };
  seventh_house_planets: string[];
  manglik_remedies: string[];
  compatibility_note: { hi: string; en: string };
}

const PLANET_HI: Record<string, string> = {
  sun: 'सूर्य', moon: 'चंद्र', mars: 'मंगल', mercury: 'बुध',
  jupiter: 'गुरु', venus: 'शुक्र', saturn: 'शनि', rahu: 'राहु', ketu: 'केतु',
};

export default function LalKitabMarriageTab({ kundliId }: Props) {
  const { t, language } = useTranslation();
  const isHi = language === 'hi';

  const [data, setData] = useState<MarriageData | null>(null);
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
        prediction_type: 'marriage',
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
    api.get(`/api/lalkitab/predictions/marriage/${kundliId}`)
      .then((res: any) => setData(res))
      .catch(() => setError(t('auto.failedToLoadMarriage')))
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
          <h2 className="text-xl font-semibold text-sacred-gold flex items-center gap-2 mb-1">
            <Heart className="w-5 h-5" />
            {t('auto.marriagePredictions')}
          </h2>
          {data && (
            <button
              onClick={handleSave}
              disabled={saving || saved}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all border disabled:opacity-60
                border-sacred-gold/40 text-sacred-gold hover:bg-sacred-gold/10"
              title={t('auto.savePrediction')}
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
          {t('auto.manglikDoshaVenusPla')}
        </p>
      </div>

      {data && (
        <>
          {/* Manglik card */}
          <div className={`card-sacred rounded-xl border p-6 ${
            data.is_manglik ? 'border-red-300/40 bg-red-500/5' : 'border-green-300/30 bg-green-500/5'
          }`}>
            <div className="flex items-center gap-4 mb-4">
              <div className={`w-16 h-16 rounded-full flex items-center justify-center ${
                data.is_manglik ? 'bg-red-500/15' : 'bg-green-500/15'
              }`}>
                {data.is_manglik
                  ? <Flame className="w-8 h-8 text-red-500" />
                  : <CheckCircle2 className="w-8 h-8 text-green-500" />}
              </div>
              <div>
                <h3 className={`text-lg font-bold ${data.is_manglik ? 'text-red-700' : 'text-green-700'}`}>
                  {data.is_manglik
                    ? (t('auto.manglikDoshaPresent'))
                    : (t('auto.noManglikDosha'))}
                </h3>
                <div className="flex items-center gap-2 mt-1">
                  <span className="text-sm text-gray-600">
                    {t('auto.marsInHouse')} <strong>{data.mars_house}</strong>
                  </span>
                  {data.is_manglik && (
                    <span className={`px-2 py-0.5 rounded-full text-xs font-semibold border ${
                      data.manglik_severity === 'strong'
                        ? 'bg-red-500/15 text-red-700 border-red-300/40'
                        : 'bg-orange-400/15 text-orange-700 border-orange-300/40'
                    }`}>
                      {data.manglik_severity === 'strong'
                        ? (t('auto.strongDosha'))
                        : (t('auto.moderateDosha'))}
                    </span>
                  )}
                </div>
              </div>
            </div>
            <p className="text-sm text-foreground/80 leading-relaxed">
              {isHi ? data.compatibility_note.hi : data.compatibility_note.en}
            </p>
          </div>

          {/* Spouse description */}
          <div className="card-sacred rounded-xl border border-sacred-gold/20 p-5">
            <h3 className="font-semibold text-sacred-gold mb-3 flex items-center gap-2">
              <Heart className="w-4 h-4" />
              {isHi ? 'जीवनसाथी का स्वभाव (शुक्र भाव {0})'.replace('{0}', String(data.venus_house)) : `Spouse Nature (Venus in House ${data.venus_house})`}
            </h3>
            <p className="text-sm text-foreground leading-relaxed">
              {isHi ? data.spouse_description.hi : data.spouse_description.en}
            </p>
          </div>

          {/* 7th house planets */}
          {Array.isArray(data.seventh_house_planets) && data.seventh_house_planets.filter(Boolean).length > 0 && (
            <div className="card-sacred rounded-xl border border-sacred-gold/20 p-5">
              <h3 className="font-semibold text-sacred-gold mb-3">
                {t('auto.planetsIn7thHouse')}
              </h3>
              <div className="flex flex-wrap gap-2">
                {data.seventh_house_planets.filter(Boolean).map((raw: any, idx: number) => {
                  const p = String(raw || '');
                  return (
                    <span key={`${p || 'p'}-${idx}`} className="px-3 py-1 rounded-full bg-sacred-gold/10 text-sacred-gold-dark text-sm font-medium">
                      {isHi ? (PLANET_HI[p] ?? p) : (p.charAt(0).toUpperCase() + p.slice(1))}
                    </span>
                  );
                })}
              </div>
            </div>
          )}

          {/* Manglik remedies */}
          {data.is_manglik && data.manglik_remedies.length > 0 && (
            <div className="card-sacred rounded-xl border border-orange-300/30 p-5 bg-orange-500/5">
              <h3 className="font-semibold text-orange-700 mb-3 flex items-center gap-2">
                <AlertTriangle className="w-4 h-4" />
                {t('auto.manglikDoshaRemedies')}
              </h3>
              <ul className="space-y-2">
                {data.manglik_remedies.map((remedy, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-foreground/80">
                    <span className="w-5 h-5 rounded-full bg-orange-400/15 text-orange-700 text-xs font-bold flex items-center justify-center shrink-0 mt-0.5">
                      {i + 1}
                    </span>
                    {typeof remedy === 'string' ? remedy : (remedy ? pickLang(remedy, isHi) : '')}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </>
      )}
    </div>
  );
}
