import { useState, useEffect } from 'react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';
import { Activity, AlertTriangle, CheckCircle2, Shield, Loader2, Bookmark, BookmarkCheck } from 'lucide-react';

interface Props {
  kundliId: string;
}

interface VulnerableArea {
  planet: string;
  house: number;
  area_hi: string;
  area_en: string;
}

interface Precaution {
  hi: string;
  en: string;
}

interface HealthData {
  overall_health: string;
  vulnerable_areas: VulnerableArea[];
  precautions: Precaution[];
  chronic_risk_planets: string[];
  health_house_planets: Record<string, string[]>;
  sun_house: number;
  moon_house: number;
  mars_house: number;
  saturn_house: number;
}

const PLANET_HI: Record<string, string> = {
  sun: 'सूर्य', moon: 'चंद्र', mars: 'मंगल', mercury: 'बुध',
  jupiter: 'गुरु', venus: 'शुक्र', saturn: 'शनि', rahu: 'राहु', ketu: 'केतु',
};

const overallConfig = {
  good:     { cls: 'border-green-300/40 bg-green-500/5',   badge: 'bg-green-500/15 text-green-700', icon: CheckCircle2, hi: 'उत्तम स्वास्थ्य', en: 'Good Health' },
  moderate: { cls: 'border-orange-300/30 bg-orange-500/5', badge: 'bg-orange-400/15 text-orange-700', icon: AlertTriangle, hi: 'सामान्य स्वास्थ्य', en: 'Moderate Health' },
  caution:  { cls: 'border-red-300/40 bg-red-500/5',       badge: 'bg-red-500/15 text-red-700',    icon: AlertTriangle, hi: 'सावधानी आवश्यक', en: 'Caution Required' },
};

export default function LalKitabHealthTab({ kundliId }: Props) {
  const { language } = useTranslation();
  const isHi = language === 'hi';

  const [data, setData] = useState<HealthData | null>(null);
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
        prediction_type: 'health',
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
    api.get(`/api/lalkitab/predictions/health/${kundliId}`)
      .then((res: any) => setData(res))
      .catch(() => setError(t('auto.failedToLoadHealthPr')))
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
            <Activity className="w-5 h-5" />
            {t('auto.healthPredictions')}
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
          {t('auto.healthAnalysisBasedO')}
        </p>
      </div>

      {data && (
        <>
          {/* Overall health card */}
          {(() => {
            const cfg = overallConfig[data.overall_health as keyof typeof overallConfig] ?? overallConfig.moderate;
            const StatusIcon = cfg.icon;
            return (
              <div className={`card-sacred rounded-xl border p-5 ${cfg.cls}`}>
                <div className="flex items-center gap-4">
                  <div className={`w-14 h-14 rounded-full flex items-center justify-center ${cfg.badge.replace('text-', 'bg-').replace('-700', '-500/20')}`}>
                    <StatusIcon className="w-7 h-7" />
                  </div>
                  <div>
                    <span className={`inline-block px-3 py-1 rounded-full text-sm font-semibold ${cfg.badge}`}>
                      {isHi ? cfg.hi : cfg.en}
                    </span>
                    <p className="text-xs text-gray-500 mt-1">
                      {t('auto.DataVulnerableareasL')}
                    </p>
                  </div>
                </div>
              </div>
            );
          })()}

          {/* Vulnerable areas */}
          {data.vulnerable_areas.length > 0 && (
            <div className="card-sacred rounded-xl border border-red-300/30 p-5">
              <h3 className="font-sans font-semibold text-red-700 mb-4 flex items-center gap-2">
                <AlertTriangle className="w-4 h-4" />
                {t('auto.vulnerableHealthArea')}
              </h3>
              <div className="grid gap-3 sm:grid-cols-2">
                {data.vulnerable_areas.map((area, i) => (
                  <div key={i} className="p-3 rounded-xl bg-red-500/5 border border-red-300/20">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="px-2 py-0.5 rounded-full bg-sacred-gold/10 text-sacred-gold-dark text-xs font-semibold">
                        {isHi ? (PLANET_HI[area.planet] ?? area.planet) : area.planet.charAt(0).toUpperCase() + area.planet.slice(1)}
                      </span>
                      <span className="text-xs text-gray-500">
                        {t('auto.houseAreaHouse')}
                      </span>
                    </div>
                    <p className="text-sm text-foreground font-medium">
                      {isHi ? area.area_hi : area.area_en}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Chronic risk */}
          {data.chronic_risk_planets.length > 0 && (
            <div className="flex items-start gap-3 p-4 rounded-xl border border-orange-300/30 bg-orange-500/5">
              <AlertTriangle className="w-4 h-4 text-orange-500 mt-0.5 shrink-0" />
              <div>
                <p className="text-sm font-semibold text-orange-700 mb-2">
                  {t('auto.chronicIllnessRisk8t')}
                </p>
                <div className="flex flex-wrap gap-2">
                  {data.chronic_risk_planets.map((p) => (
                    <span key={p} className="px-2.5 py-0.5 rounded-full bg-orange-400/15 text-orange-700 text-xs font-medium">
                      {isHi ? (PLANET_HI[p] ?? p) : p.charAt(0).toUpperCase() + p.slice(1)}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Precautions */}
          {data.precautions.length > 0 && (
            <div className="card-sacred rounded-xl border border-sacred-gold/20 p-5">
              <h3 className="font-sans font-semibold text-sacred-gold mb-4 flex items-center gap-2">
                <Shield className="w-4 h-4" />
                {t('auto.healthPrecautions')}
              </h3>
              <ul className="space-y-3">
                {data.precautions.map((p, i) => (
                  <li key={i} className="flex items-start gap-3">
                    <span className="w-6 h-6 rounded-full bg-sacred-gold/15 text-sacred-gold text-xs font-bold flex items-center justify-center shrink-0 mt-0.5">
                      {i + 1}
                    </span>
                    <p className="text-sm text-foreground/80 leading-relaxed">
                      {isHi ? p.hi : p.en}
                    </p>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Key planet positions */}
          <div className="card-sacred rounded-xl border border-sacred-gold/20 p-5">
            <h3 className="font-sans font-semibold text-sacred-gold mb-3">
              {t('auto.healthRelatedPlanetP')}
            </h3>
            <div className="grid grid-cols-4 gap-3">
              {[
                { key: 'sun',    hi: 'सूर्य', house: data.sun_house },
                { key: 'moon',   hi: 'चंद्र', house: data.moon_house },
                { key: 'mars',   hi: 'मंगल', house: data.mars_house },
                { key: 'saturn', hi: 'शनि',  house: data.saturn_house },
              ].map(({ key, hi, house }) => {
                const isInBadHouse = [6, 8, 12].includes(house);
                return (
                  <div key={key} className={`text-center p-3 rounded-xl border ${
                    isInBadHouse ? 'bg-red-500/5 border-red-300/20' : 'bg-sacred-gold/5 border-sacred-gold/15'
                  }`}>
                    <p className="text-xs text-gray-500 mb-1">{isHi ? hi : key.charAt(0).toUpperCase() + key.slice(1)}</p>
                    <p className={`text-xl font-bold ${isInBadHouse ? 'text-red-600' : 'text-sacred-gold'}`}>{house}</p>
                    <p className="text-xs text-gray-400">{t('auto.house')}</p>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Good health message */}
          {data.overall_health === 'good' && (
            <div className="flex items-center gap-3 p-4 rounded-xl border border-green-300/30 bg-green-500/5">
              <CheckCircle2 className="w-5 h-5 text-green-500 shrink-0" />
              <p className="text-sm text-green-700">
                {t('auto.noMajorHealthAfflict')}
              </p>
            </div>
          )}
        </>
      )}
    </div>
  );
}
