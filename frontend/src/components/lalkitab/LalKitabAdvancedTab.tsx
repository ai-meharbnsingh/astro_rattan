import { useState, useEffect, useMemo } from 'react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';
import { 
  Zap, 
  ShieldAlert, 
  EyeOff, 
  HandMetal, 
  Loader2, 
  AlertTriangle,
  History,
  Scale,
  Moon
} from 'lucide-react';
import { translatePlanet, translateSign } from '@/lib/backend-translations';
import LalKitabDiagnosticChart from './LalKitabDiagnosticChart';

interface Props {
  kundliId: string;
  chartData: any;
}

export default function LalKitabAdvancedTab({ kundliId, chartData }: Props) {
  const { t, language } = useTranslation();
  const isHi = language === 'hi';

  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const planetPositions = useMemo(() => {
    return Object.entries(chartData?.planetPositions || {}).map(([planet, house]) => ({
      planet,
      house: house as number
    }));
  }, [chartData]);

  useEffect(() => {
    if (!kundliId) return;
    setLoading(true);
    api.get(`/api/lalkitab/advanced/${kundliId}`)
      .then(setData)
      .catch(() => setError(isHi ? 'उन्नत विश्लेषण लोड करने में विफल' : 'Failed to load advanced analysis'))
      .finally(() => setLoading(false));
  }, [kundliId, isHi]);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-20">
        <Loader2 className="w-10 h-10 animate-spin text-sacred-gold mb-4" />
        <p className="text-sacred-gold">{t('common.loading')}</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 rounded-xl bg-red-50 border border-red-200 text-red-700 text-center">
        {error}
      </div>
    );
  }

  if (!data) return null;

  // Calculate Karmic Confidence Score
  let score = 80;
  score -= (data.karmic_debts.length * 8);
  if (data.teva_type.is_andha) score -= 20;
  if (data.teva_type.is_ratondha) score -= 10;
  if (data.teva_type.is_dharmi) score += 20;
  
  data.masnui_planets.forEach((m: any) => {
    if (['Jupiter', 'Sun', 'Moon'].includes(m.masnui_planet)) score += 5;
    if (['Rahu', 'Saturn'].includes(m.masnui_planet)) score -= 5;
  });

  const finalScore = Math.max(10, Math.min(100, score));
  const scoreColor = finalScore >= 75 ? 'text-green-600' : finalScore >= 45 ? 'text-sacred-gold-dark' : 'text-red-600';
  const scoreBg = finalScore >= 75 ? 'bg-green-500' : finalScore >= 45 ? 'bg-sacred-gold' : 'bg-red-500';
  const scoreLabel = finalScore >= 75 ? t('lk.advanced.highConfidence') : finalScore >= 45 ? t('lk.advanced.midConfidence') : t('lk.advanced.lowConfidence');

  return (
    <div className="space-y-8">
      {/* Karmic Confidence Meter */}
      <div className="card-sacred p-6 rounded-2xl border border-sacred-gold/30 bg-gradient-to-br from-white to-sacred-gold/5 relative overflow-hidden">
        <div className="absolute -right-10 -bottom-10 opacity-5">
          <Scale className="w-48 h-48" />
        </div>
        
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 relative z-10">
          <div className="flex-1">
            <h2 className="text-2xl font-sans font-bold text-sacred-gold mb-1">
              {t('lk.advanced.karmicScore')}
            </h2>
            <p className="text-sm text-cosmic-text/60 max-w-md">
              {t('lk.advanced.scoreDesc')}
            </p>
          </div>

          <div className="flex flex-col items-center md:items-end gap-2">
            <div className="flex items-end gap-2">
              <span className={`text-5xl font-sans font-black tracking-tighter ${scoreColor}`}>
                {finalScore}%
              </span>
              <span className={`text-sm font-bold uppercase mb-2 ${scoreColor}`}>
                {scoreLabel}
              </span>
            </div>
            <div className="w-64 h-3 bg-gray-200 rounded-full overflow-hidden border border-gray-100 shadow-inner">
              <div 
                className={`h-full transition-all duration-1000 ease-out ${scoreBg}`}
                style={{ width: `${finalScore}%` }}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Header */}
      <div>
        <h2 className="text-2xl font-sans font-bold text-sacred-gold mb-2">
          {t('lk.advanced.title')}
        </h2>
        <p className="text-cosmic-text/70">{t('lk.advanced.desc')}</p>
      </div>

      {/* Teva Typology */}
      <div className="grid md:grid-cols-3 gap-4">
        <div className={`p-5 rounded-xl border flex flex-col justify-between ${data.teva_type.is_andha ? 'bg-red-500/5 border-red-200' : 'bg-gray-50 border-gray-100'}`}>
          <div>
            <div className="flex items-center gap-3 mb-3">
              <EyeOff className={`w-6 h-6 ${data.teva_type.is_andha ? 'text-red-600' : 'text-gray-400'}`} />
              <h3 className="font-sans font-bold text-lg">{t('lk.advanced.andhaTeva')}</h3>
            </div>
            <p className="text-xs text-cosmic-text/80 leading-relaxed mb-4">
              {isHi ? data.teva_type.description.andha.hi : data.teva_type.description.andha.en}
            </p>
          </div>
          {data.teva_type.is_andha && (
            <div className="mt-2 scale-90 origin-top">
              <LalKitabDiagnosticChart type="andha" planetPositions={planetPositions} />
            </div>
          )}
        </div>

        <div className={`p-5 rounded-xl border flex flex-col justify-between ${data.teva_type.is_ratondha ? 'bg-orange-500/5 border-orange-200' : 'bg-gray-50 border-gray-100'}`}>
          <div>
            <div className="flex items-center gap-3 mb-3">
              <Moon className={`w-6 h-6 ${data.teva_type.is_ratondha ? 'text-orange-600' : 'text-gray-400'}`} />
              <h3 className="font-sans font-bold text-lg">{t('lk.advanced.ratondhaTeva')}</h3>
            </div>
            <p className="text-xs text-cosmic-text/80 leading-relaxed mb-4">
              {isHi ? data.teva_type.description.ratondha.hi : data.teva_type.description.ratondha.en}
            </p>
          </div>
          {data.teva_type.is_ratondha && (
            <div className="mt-2 scale-90 origin-top">
              <LalKitabDiagnosticChart type="andha" planetPositions={planetPositions} />
            </div>
          )}
        </div>

        <div className={`p-5 rounded-xl border flex flex-col justify-between ${data.teva_type.is_dharmi ? 'bg-green-500/5 border-green-200' : 'bg-gray-50 border-gray-100'}`}>
          <div>
            <div className="flex items-center gap-3 mb-3">
              <HandMetal className={`w-6 h-6 ${data.teva_type.is_dharmi ? 'text-green-600' : 'text-gray-400'}`} />
              <h3 className="font-sans font-bold text-lg">{t('lk.advanced.dharmiTeva')}</h3>
            </div>
            <p className="text-xs text-cosmic-text/80 leading-relaxed mb-4">
              {isHi ? data.teva_type.description.dharmi.hi : data.teva_type.description.dharmi.en}
            </p>
          </div>
          {data.teva_type.is_dharmi && (
            <div className="mt-2 scale-90 origin-top">
              <LalKitabDiagnosticChart type="dharmi" planetPositions={planetPositions} dharmiData={data.teva_type} />
            </div>
          )}
        </div>
      </div>

      {/* Masnui Grah */}
      <section>
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-4">
          <div className="flex items-center gap-2">
            <Zap className="w-5 h-5 text-sacred-gold" />
            <h3 className="text-xl font-sans font-bold text-cosmic-text">{t('lk.advanced.masnuiGrah')}</h3>
          </div>
          {data.masnui_planets.length > 0 && (
            <span className="text-[10px] font-bold text-sacred-gold-dark bg-sacred-gold/10 px-2 py-1 rounded border border-sacred-gold/20 uppercase tracking-widest animate-pulse">
              ALCHEMICAL SYNTHESIS ACTIVE
            </span>
          )}
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          {data.masnui_planets.length > 0 && (
            <div className="lg:col-span-1 p-4 rounded-2xl bg-sacred-gold/5 border border-sacred-gold/20 flex flex-col items-center">
              <p className="text-[10px] font-bold text-sacred-gold uppercase tracking-widest mb-4">Visual Alchemy Map</p>
              <LalKitabDiagnosticChart type="masnui" planetPositions={planetPositions} masnuiData={data.masnui_planets} />
              <p className="text-[10px] text-cosmic-text/50 mt-4 text-center px-4 italic">
                Glowing circles indicate synthetic planets formed by alchemical conjunctions.
              </p>
            </div>
          )}

          <div className={`grid gap-4 ${data.masnui_planets.length > 0 ? 'lg:col-span-2 sm:grid-cols-2' : 'sm:grid-cols-2 lg:grid-cols-3 w-full'}`}>
            {data.masnui_planets.map((m: any, i: number) => (
              <div key={i} className="card-sacred p-4 rounded-xl border border-sacred-gold/20 bg-white/40">
                <div className="flex justify-between items-start mb-2">
                  <span className="text-xs font-bold text-sacred-gold-dark uppercase tracking-wider">{t('lk.kundli.house')} {m.house}</span>
                  <span className="px-2 py-0.5 rounded bg-sacred-gold/10 text-sacred-gold-dark text-[10px] font-bold">MASNUI</span>
                </div>
                <p className="text-sm font-bold text-cosmic-text mb-1">
                  {m.formed_by.map((p: string) => translatePlanet(p, language)).join(' + ')}
                </p>
                <div className="flex items-center gap-2 mb-3">
                  <span className="text-xs text-cosmic-text/60">→</span>
                  <span className="text-lg font-bold text-sacred-gold-dark">{translatePlanet(m.masnui_planet, language)}</span>
                </div>
                <p className="text-xs text-cosmic-text/70 italic border-t border-sacred-gold/10 pt-2">
                  {t('lk.advanced.affectedDomain')}: {isHi ? m.affected_domain.hi : m.affected_domain.en}
                </p>
              </div>
            ))}
            {data.masnui_planets.length === 0 && (
              <div className="col-span-full py-10 text-center border border-dashed border-gray-200 rounded-xl">
                <p className="text-gray-400 italic">{isHi ? 'कोई मसनुई ग्रह नहीं मिला' : 'No artificial planets detected'}</p>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* Karmic Debts */}
      <section>
        <div className="flex items-center gap-2 mb-4">
          <History className="w-5 h-5 text-sacred-gold" />
          <h3 className="text-xl font-sans font-bold text-cosmic-text">{t('lk.advanced.karmicDebts')}</h3>
        </div>
        <div className="space-y-4">
          {data.karmic_debts.map((debt: any, i: number) => (
            <div key={i} className="p-5 rounded-xl border border-red-200 bg-red-500/5 relative overflow-hidden">
              <div className="absolute top-0 right-0 p-2 opacity-10">
                <Scale className="w-12 h-12" />
              </div>
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-4">
                <div>
                  <h4 className="text-lg font-bold text-red-800">{isHi ? debt.name.hi : debt.name.en}</h4>
                  <p className="text-xs font-semibold text-red-600/70">{t('lk.advanced.type')}: {isHi ? debt.type.hi : debt.type.en}</p>
                  <p className="text-xs font-semibold text-red-600/70">{t('lk.advanced.reason')}: {isHi ? debt.reason.hi : debt.reason.en}</p>
                </div>
                <span className="px-3 py-1 rounded-full bg-red-600 text-white text-xs font-bold self-start">{isHi ? 'सक्रिय' : 'ACTIVE DEBT'}</span>
              </div>
              <div className="bg-white/60 p-3 rounded-lg border border-red-100 mb-3">
                <p className="text-xs font-bold text-red-800 mb-1 uppercase tracking-tighter">{t('lk.advanced.manifestation')}</p>
                <p className="text-sm text-cosmic-text leading-relaxed">{isHi ? debt.manifestation.hi : debt.manifestation.en}</p>
              </div>
              <div className="bg-green-600/5 p-3 rounded-lg border border-green-600/20">
                <p className="text-xs font-bold text-green-800 mb-1 uppercase tracking-tighter">{t('lk.advanced.remedy')}</p>
                <p className="text-sm text-cosmic-text leading-relaxed font-medium">{isHi ? debt.remedy.hi : debt.remedy.en}</p>
              </div>
            </div>
          ))}
          {data.karmic_debts.length === 0 && (
            <div className="py-10 text-center border border-dashed border-gray-200 rounded-xl bg-green-500/5">
              <p className="text-green-700 font-medium italic">{isHi ? 'बधाई! कोई गंभीर कर्मिक ऋण नहीं मिला' : 'Congratulations! No severe karmic debts detected'}</p>
            </div>
          )}
        </div>
      </section>

      {/* Prohibitions */}
      <section>
        <div className="flex items-center gap-2 mb-4">
          <ShieldAlert className="w-5 h-5 text-red-600" />
          <h3 className="text-xl font-sans font-bold text-cosmic-text">{t('lk.advanced.prohibitions')}</h3>
        </div>
        <p className="text-sm text-cosmic-text/70 mb-4">{t('lk.advanced.prohibitionDesc')}</p>
        <div className="grid gap-4">
          {data.prohibitions.map((p: any, i: number) => (
            <div key={i} className="flex gap-4 p-4 rounded-xl border border-orange-200 bg-orange-50">
              <div className="shrink-0">
                <div className="w-10 h-10 rounded-full bg-orange-200 flex items-center justify-center text-orange-700 font-bold">
                  {p.house}
                </div>
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-bold text-cosmic-text">
                    {isHi 
                      ? `${p.house}${t('lk.advanced.inHouse')} ${translatePlanet(p.planet, language)}` 
                      : `${translatePlanet(p.planet, language)} ${t('lk.advanced.inHouse')} ${p.house}`
                    }
                  </span>
                </div>
                <div className="flex flex-wrap gap-2 items-center mb-3">
                  <span className="text-sm font-bold text-red-700 uppercase tracking-tight">{t('lk.advanced.forbidden')}:</span>
                  <span className="text-sm bg-white px-2 py-0.5 rounded border border-orange-300 font-medium text-orange-800">{isHi ? p.forbidden.hi : p.forbidden.en}</span>
                </div>
                <div className="flex items-start gap-2 text-xs">
                  <AlertTriangle className="w-3 h-3 text-red-600 mt-0.5" />
                  <span className="text-cosmic-text/70"><strong className="text-red-600">{t('lk.advanced.backlashRisk')}:</strong> {isHi ? p.backlash_risk.hi : p.backlash_risk.en}</span>
                </div>
              </div>
            </div>
          ))}
          {data.prohibitions.length === 0 && (
            <div className="py-10 text-center border border-dashed border-gray-200 rounded-xl">
              <p className="text-gray-400 italic">{isHi ? 'कोई विशिष्ट वर्जना नहीं मिली' : 'No specific prohibitions found'}</p>
            </div>
          )}
        </div>
      </section>
    </div>
  );
}
