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
  Moon,
  Building2,
  Swords,
  Shield,
  ArrowRight,
  CheckCircle2,
  XCircle
} from 'lucide-react';
import { translatePlanet } from '@/lib/backend-translations';
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

  // LK Analysis state (bunyaad, takkar, enemy_presence)
  const [analysisData, setAnalysisData] = useState<any>(null);
  const [analysisLoading, setAnalysisLoading] = useState(false);
  const [analysisError, setAnalysisError] = useState('');

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
      .catch(() => setError(t('auto.failedToLoadAdvanced')))
      .finally(() => setLoading(false));
  }, [kundliId, isHi]);

  // Fetch LK Analysis (bunyaad, takkar, enemy_presence)
  useEffect(() => {
    if (!kundliId) return;
    setAnalysisLoading(true);
    api.post('/api/kp-lalkitab/lk-analysis', { kundli_id: kundliId })
      .then(setAnalysisData)
      .catch(() => setAnalysisError(t('lk.advanced.loadingAnalysis')))
      .finally(() => setAnalysisLoading(false));
  }, [kundliId]);

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
  
  // Use new masnui structure
  const masnuiList = data.masnui_planets?.masnui_planets || data.masnui_planets || [];
  masnuiList.forEach((m: any) => {
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
            <p className="text-sm text-foreground/60 max-w-md">
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
        <p className="text-foreground/70">{t('lk.advanced.desc')}</p>
      </div>

      {/* Teva Typology */}
      <div className="grid md:grid-cols-3 gap-4">
        <div className={`p-5 rounded-xl border flex flex-col justify-between ${data.teva_type.is_andha ? 'bg-red-500/5 border-red-200' : 'bg-gray-50 border-gray-100'}`}>
          <div>
            <div className="flex items-center gap-3 mb-3">
              <EyeOff className={`w-6 h-6 ${data.teva_type.is_andha ? 'text-red-600' : 'text-gray-400'}`} />
              <h3 className="font-sans font-bold text-lg">{t('lk.advanced.andhaTeva')}</h3>
            </div>
            <p className="text-xs text-foreground/80 leading-relaxed mb-4">
              {isHi ? data.teva_type.description.andha.hi : data.teva_type.description.andha.en}
            </p>
          </div>
          {data.teva_type.is_andha && (
            <div className="mt-2">
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
            <p className="text-xs text-foreground/80 leading-relaxed mb-4">
              {isHi ? data.teva_type.description.ratondha.hi : data.teva_type.description.ratondha.en}
            </p>
          </div>
          {data.teva_type.is_ratondha && (
            <div className="mt-2">
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
            <p className="text-xs text-foreground/80 leading-relaxed mb-4">
              {isHi ? data.teva_type.description.dharmi.hi : data.teva_type.description.dharmi.en}
            </p>
          </div>
          {data.teva_type.is_dharmi && (
            <div className="mt-2">
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
            <h3 className="text-xl font-sans font-bold text-foreground">{t('lk.advanced.masnuiGrah')}</h3>
          </div>
          {masnuiList.length > 0 && (
            <span className="text-[10px] font-bold text-sacred-gold-dark bg-sacred-gold/10 px-2 py-1 rounded border border-sacred-gold/20 uppercase tracking-widest animate-pulse">
              {t('lk.advanced.badge')}
            </span>
          )}
        </div>

        {/* Psychological Profile */}
        {data.masnui_planets?.psychological_profile && (
          <div className="mb-6 p-4 rounded-xl bg-purple-50 border border-purple-200">
            <h4 className="font-bold text-purple-800 mb-2 text-sm uppercase tracking-wider">
              {t('auto.psychologicalProfile')}
            </h4>
            <p className="text-sm text-foreground mb-2">
              {isHi 
                ? data.masnui_planets.psychological_profile.dominant_quality?.hi 
                : data.masnui_planets.psychological_profile.dominant_quality?.en}
            </p>
            <p className="text-xs text-foreground/70">
              <span className="font-semibold">{t('auto.behavioralTendencies')}</span>
              {isHi 
                ? data.masnui_planets.psychological_profile.behavioral_tendencies?.hi 
                : data.masnui_planets.psychological_profile.behavioral_tendencies?.en}
            </p>
            <p className="text-xs text-foreground/70 mt-1">
              <span className="font-semibold">{t('auto.relationshipApproach')}</span>
              {isHi 
                ? data.masnui_planets.psychological_profile.relationship_approach?.hi 
                : data.masnui_planets.psychological_profile.relationship_approach?.en}
            </p>
          </div>
        )}

        {/* House Override Warnings */}
        {data.masnui_planets?.house_overrides && Object.keys(data.masnui_planets.house_overrides).length > 0 && (
          <div className="mb-6 space-y-3">
            <h4 className="font-bold text-sacred-brown text-sm uppercase tracking-wider">
              {t('auto.houseOverrideEffects')}
            </h4>
            {Object.entries(data.masnui_planets.house_overrides).map(([houseNum, override]: [string, any]) => (
              <div key={houseNum} className="p-4 rounded-xl bg-amber-50 border border-amber-200">
                <div className="flex items-center gap-2 mb-2">
                  <span className="px-2 py-0.5 bg-amber-200 text-amber-800 text-xs font-bold rounded">
                    {t('auto.houseHouseNum')}
                  </span>
                  <span className="text-sm font-bold text-amber-800">
                    {isHi ? override.house_name?.hi : override.house_name?.en}
                  </span>
                </div>
                <p className="text-xs text-foreground mb-2">
                  <span className="font-semibold">{t('auto.effects')}</span>
                  {isHi ? override.effects?.hi : override.effects?.en}
                </p>
                <p className="text-xs text-amber-700 italic">
                  <span className="font-semibold">{t('auto.predictiveNote')}</span>
                  {isHi ? override.predictive_note?.hi : override.predictive_note?.en}
                </p>
              </div>
            ))}
          </div>
        )}

        {/* Predictive Notes */}
        {data.masnui_planets?.predictive_notes && data.masnui_planets.predictive_notes.length > 0 && (
          <div className="mb-6 p-4 rounded-xl bg-blue-50 border border-blue-200">
            <h4 className="font-bold text-blue-800 mb-3 text-sm uppercase tracking-wider">
              {t('auto.predictiveNotes')}
            </h4>
            <ul className="space-y-2">
              {data.masnui_planets.predictive_notes.map((note: any, i: number) => (
                <li key={i} className="text-xs text-foreground flex items-start gap-2">
                  <span className="text-blue-500 mt-0.5">•</span>
                  <span>{isHi ? note.note?.hi : note.note?.en}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        <div className="grid lg:grid-cols-5 gap-6">
          {masnuiList.length > 0 && (
            <div className="lg:col-span-2 p-4 rounded-2xl bg-sacred-gold/5 border border-sacred-gold/20 flex flex-col items-center">
              <p className="text-[10px] font-bold text-sacred-gold uppercase tracking-widest mb-4">{t('lk.advanced.mapTitle')}</p>
              <LalKitabDiagnosticChart type="masnui" planetPositions={planetPositions} masnuiData={masnuiList} />
              <p className="text-[10px] text-foreground/50 mt-4 text-center px-4 italic">
                {t('lk.advanced.mapDesc')}
              </p>
            </div>
          )}

          <div className={`grid gap-4 ${masnuiList.length > 0 ? 'lg:col-span-3 sm:grid-cols-2' : 'sm:grid-cols-2 lg:grid-cols-3 w-full'}`}>
            {masnuiList.map((m: any, i: number) => (
              <div key={i} className="card-sacred p-4 rounded-xl border border-sacred-gold/20 bg-white/40">
                <div className="flex justify-between items-start mb-2">
                  <span className="text-xs font-bold text-sacred-gold-dark uppercase tracking-wider">{t('lk.kundli.house')} {m.house}</span>
                  <span className="px-2 py-0.5 rounded bg-sacred-gold/10 text-sacred-gold-dark text-[10px] font-bold">MASNUI</span>
                </div>
                <p className="text-sm font-bold text-foreground mb-1">
                  {m.formed_by.map((p: string) => translatePlanet(p, language)).join(' + ')}
                </p>
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-xs text-foreground/60">→</span>
                  <span className="text-lg font-bold text-sacred-gold-dark">{translatePlanet(m.masnui_planet, language)}</span>
                </div>
                {m.quality && (
                  <span className={`text-[10px] px-1.5 py-0.5 rounded ${
                    m.quality === 'Khali Hawai' ? 'bg-gray-200 text-gray-700' :
                    m.quality === 'Challenging' ? 'bg-red-100 text-red-700' :
                    m.quality === 'Mixed' ? 'bg-yellow-100 text-yellow-700' :
                    'bg-green-100 text-green-700'
                  }`}>
                    {m.quality}
                  </span>
                )}
                <p className="text-xs text-foreground/70 italic border-t border-sacred-gold/10 pt-2 mt-2">
                  {t('lk.advanced.affectedDomain')}: {isHi ? m.affected_domain.hi : m.affected_domain.en}
                </p>
                {m.house_override && (
                  <p className="text-xs text-amber-700 mt-2">
                    <span className="font-semibold">{t('auto.houseOverride')}</span>
                    {t('auto.houseMHouseoverride')}
                  </p>
                )}
              </div>
            ))}
            {masnuiList.length === 0 && (
              <div className="col-span-full py-10 text-center border border-dashed border-gray-200 rounded-xl">
                <p className="text-gray-400 italic">{t('auto.noArtificialPlanetsD')}</p>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* Hora-Based Debt Analysis */}
      {data.karmic_debts_hora_analysis && (
        <section className="p-5 rounded-xl border border-purple-200 bg-purple-50">
          <div className="flex items-center gap-2 mb-4">
            <svg className="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <h3 className="text-xl font-sans font-bold text-purple-900">
              {t('auto.horaPlanetaryHourDeb')}
            </h3>
          </div>
          
          {data.karmic_debts_hora_analysis.hora_analysis ? (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-white p-3 rounded-lg border border-purple-100">
                  <span className="text-xs text-purple-600 uppercase font-bold">{t('auto.dayLord')}</span>
                  <p className="text-lg font-bold text-purple-900">{data.karmic_debts_hora_analysis.hora_analysis.day_lord}</p>
                  <p className="text-xs text-purple-600">{data.karmic_debts_hora_analysis.hora_analysis.weekday_name}</p>
                </div>
                <div className="bg-white p-3 rounded-lg border border-purple-100">
                  <span className="text-xs text-purple-600 uppercase font-bold">{t('auto.horaLord')}</span>
                  <p className="text-lg font-bold text-purple-900">{data.karmic_debts_hora_analysis.hora_analysis.hora_lord}</p>
                  <p className="text-xs text-purple-600">
                    {t('auto.DataKarmicdebtshoraa')}
                  </p>
                </div>
              </div>

              {/* Base Debt from Hora */}
              {data.karmic_debts_hora_analysis.hora_analysis.base_debt && (
                <div className="bg-white p-4 rounded-lg border border-purple-100">
                  <h4 className="font-bold text-purple-800 mb-2">
                    {t('auto.horaBasedDebt')}
                    {isHi ? data.karmic_debts_hora_analysis.hora_analysis.base_debt.debt_hi : data.karmic_debts_hora_analysis.hora_analysis.base_debt.debt}
                  </h4>
                  <p className="text-sm text-foreground">
                    {isHi ? data.karmic_debts_hora_analysis.hora_analysis.base_debt.description.hi : data.karmic_debts_hora_analysis.hora_analysis.base_debt.description.en}
                  </p>
                </div>
              )}

              {/* Conflict Modifications */}
              {data.karmic_debts_hora_analysis.conflicts_resolved && data.karmic_debts_hora_analysis.conflicts_resolved.length > 0 && (
                <div className="bg-amber-50 p-4 rounded-lg border border-amber-200">
                  <h4 className="font-bold text-amber-800 mb-2">
                    {t('auto.conflictModification')}
                  </h4>
                  {data.karmic_debts_hora_analysis.conflicts_resolved.map((conflict: any, idx: number) => (
                    <div key={idx} className="mb-2">
                      <p className="text-sm font-semibold text-amber-900">
                        {conflict.type === 'modification' 
                          ? (t('auto.modifiedConflictFrom'))
                          : (t('auto.intensityEnhancement'))
                        }
                      </p>
                      <p className="text-xs text-amber-700">
                        {isHi ? conflict.reason?.hi : conflict.reason?.en}
                      </p>
                    </div>
                  ))}
                </div>
              )}

              {/* Time Sensitivity Warning */}
              {data.karmic_debts_hora_analysis.time_sensitivity_warning && (
                <div className="bg-yellow-50 p-3 rounded-lg border border-yellow-200">
                  <p className="text-sm text-yellow-800">
                    <span className="font-bold">{t('auto.timeSensitivity')}</span>
                    {isHi ? data.karmic_debts_hora_analysis.time_sensitivity_warning.message.hi : data.karmic_debts_hora_analysis.time_sensitivity_warning.message.en}
                  </p>
                </div>
              )}

              {/* Hora Influence Summary */}
              {data.karmic_debts_hora_analysis.hora_influence && (
                <div className="text-sm text-foreground bg-white/50 p-3 rounded">
                  <p>
                    <span className="font-semibold">{t('auto.horaInfluence')}</span>
                    {data.karmic_debts_hora_analysis.hora_influence.added_new_debt 
                      ? (t('auto.newDebtAddedBasedOnH'))
                      : (t('auto.horaDebtAlreadyIdent'))
                    }
                  </p>
                </div>
              )}
            </div>
          ) : (
            <p className="text-sm text-foreground italic">
              {t('auto.horaAnalysisCouldNot')}
            </p>
          )}
        </section>
      )}

      {/* Karmic Debts */}
      <section>
        <div className="flex items-center gap-2 mb-4">
          <History className="w-5 h-5 text-sacred-gold" />
          <h3 className="text-xl font-sans font-bold text-foreground">{t('lk.advanced.karmicDebts')}</h3>
        </div>
        <div className="space-y-4">
          {data.karmic_debts.map((debt: any, i: number) => (
            <div key={i} className={`p-5 rounded-xl border relative overflow-hidden ${
              debt.is_hora_based 
                ? 'border-purple-200 bg-purple-50' 
                : 'border-red-200 bg-red-500/5'
            }`}>
              <div className="absolute top-0 right-0 p-2 opacity-10">
                <Scale className="w-12 h-12" />
              </div>
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-4">
                <div>
                  <div className="flex items-center gap-2">
                    <h4 className="text-lg font-bold text-red-800">{isHi ? debt.name.hi : debt.name.en}</h4>
                    {debt.is_hora_based && (
                      <span className="px-2 py-0.5 rounded bg-purple-200 text-purple-800 text-[10px] font-bold">
                        {t('auto.hORABASED')}
                      </span>
                    )}
                    {debt.is_modified && (
                      <span className="px-2 py-0.5 rounded bg-amber-200 text-amber-800 text-[10px] font-bold">
                        {t('auto.mODIFIED')}
                      </span>
                    )}
                  </div>
                  <p className="text-xs font-semibold text-red-600/70">{t('lk.advanced.type')}: {isHi ? debt.type.hi : debt.type.en}</p>
                  {debt.source && (
                    <p className="text-xs text-purple-600 italic">
                      {isHi ? debt.source.hi : debt.source.en}
                    </p>
                  )}
                  <p className="text-xs font-semibold text-red-600/70">{t('lk.advanced.reason')}: {isHi ? debt.reason.hi : debt.reason.en}</p>
                </div>
                <span className="px-3 py-1 rounded-full bg-red-600 text-white text-xs font-bold self-start">{t('auto.aCTIVEDEBT')}</span>
              </div>
              <div className="bg-white/60 p-3 rounded-lg border border-red-100 mb-3">
                <p className="text-xs font-bold text-red-800 mb-1 uppercase tracking-tighter">{t('lk.advanced.manifestation')}</p>
                <p className="text-sm text-foreground leading-relaxed">{isHi ? debt.manifestation.hi : debt.manifestation.en}</p>
              </div>
              {debt.remedy && (
                <div className="bg-green-600/5 p-3 rounded-lg border border-green-600/20">
                  <p className="text-xs font-bold text-green-800 mb-1 uppercase tracking-tighter">{t('lk.advanced.remedy')}</p>
                  <p className="text-sm text-foreground leading-relaxed font-medium">{isHi ? debt.remedy.hi : debt.remedy.en}</p>
                </div>
              )}
            </div>
          ))}
          {data.karmic_debts.length === 0 && (
            <div className="py-10 text-center border border-dashed border-gray-200 rounded-xl bg-green-500/5">
              <p className="text-green-700 font-medium italic">{t('auto.congratulationsNoSev')}</p>
            </div>
          )}
        </div>
      </section>

      {/* Prohibitions */}
      <section>
        <div className="flex items-center gap-2 mb-4">
          <ShieldAlert className="w-5 h-5 text-red-600" />
          <h3 className="text-xl font-sans font-bold text-foreground">{t('lk.advanced.prohibitions')}</h3>
        </div>
        <p className="text-sm text-foreground/70 mb-4">{t('lk.advanced.prohibitionDesc')}</p>
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
                  <span className="font-bold text-foreground">
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
                  <span className="text-foreground/70"><strong className="text-red-600">{t('lk.advanced.backlashRisk')}:</strong> {isHi ? p.backlash_risk.hi : p.backlash_risk.en}</span>
                </div>
              </div>
            </div>
          ))}
          {data.prohibitions.length === 0 && (
            <div className="py-10 text-center border border-dashed border-gray-200 rounded-xl">
              <p className="text-gray-400 italic">{t('auto.noSpecificProhibitio')}</p>
            </div>
          )}
        </div>
      </section>

      {/* ═══════════════════════════════════════════════════════════════
          LK ANALYSIS: Bunyaad + Takkar + Enemy Siege
          ═══════════════════════════════════════════════════════════════ */}

      {analysisLoading && (
        <div className="flex flex-col items-center justify-center py-12">
          <Loader2 className="w-8 h-8 animate-spin text-sacred-gold mb-3" />
          <p className="text-sacred-gold text-sm">{t('lk.advanced.loadingAnalysis')}</p>
        </div>
      )}

      {analysisError && !analysisLoading && (
        <div className="p-4 rounded-xl bg-red-50 border border-red-200 text-red-700 text-sm text-center">
          {analysisError}
        </div>
      )}

      {analysisData && !analysisLoading && (
        <>
          {/* ── BUNYAAD (Foundation) Section ── */}
          <section>
            <div className="flex items-center gap-2 mb-2">
              <Building2 className="w-5 h-5 text-sacred-gold" />
              <h3 className="text-xl font-sans font-bold text-foreground">
                {t('lk.advanced.bunyaadTitle')}
              </h3>
            </div>
            <p className="text-sm text-foreground/60 mb-4">
              {t('lk.advanced.bunyaadDesc')}
            </p>

            {/* Collapsed Planets Banner */}
            {analysisData.bunyaad?.collapsed_planets && analysisData.bunyaad.collapsed_planets.length > 0 && (
              <div className="mb-4 p-3 rounded-xl bg-red-500/10 border border-red-300 flex items-center gap-3">
                <XCircle className="w-5 h-5 text-red-600 shrink-0" />
                <div>
                  <p className="text-sm font-bold text-red-800">
                    {t('lk.advanced.collapsedFoundations')}
                  </p>
                  <div className="flex flex-wrap gap-1.5 mt-1">
                    {analysisData.bunyaad.collapsed_planets.map((p: string) => (
                      <span key={p} className="px-2 py-0.5 rounded bg-red-200 text-red-800 text-xs font-bold">
                        {translatePlanet(p, language)}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* Strong Foundations Badge Row */}
            {analysisData.bunyaad?.strong_foundations && analysisData.bunyaad.strong_foundations.length > 0 && (
              <div className="mb-4 flex flex-wrap items-center gap-2">
                <span className="text-xs font-bold text-green-700 uppercase tracking-wider">
                  {t('lk.advanced.strongFoundations')}
                </span>
                {analysisData.bunyaad.strong_foundations.map((p: string) => (
                  <span key={p} className="px-2 py-0.5 rounded bg-green-100 text-green-800 text-xs font-bold border border-green-200">
                    {translatePlanet(p, language)}
                  </span>
                ))}
              </div>
            )}

            {/* Planet Bunyaad Cards */}
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {analysisData.bunyaad?.planets && Object.entries(analysisData.bunyaad.planets).map(([planet, info]: [string, any]) => {
                const statusColor = info.bunyaad_status === 'strong'
                  ? 'bg-green-100 text-green-800 border-green-200'
                  : info.bunyaad_status === 'afflicted'
                    ? 'bg-red-100 text-red-800 border-red-200'
                    : 'bg-gray-100 text-gray-600 border-gray-200';
                const statusLabel = info.bunyaad_status === 'strong'
                  ? t('lk.advanced.foundation.strong')
                  : info.bunyaad_status === 'afflicted'
                    ? t('lk.advanced.foundation.afflicted')
                    : t('lk.advanced.foundation.empty');

                return (
                  <div key={planet} className="card-sacred p-4 rounded-xl border border-sacred-gold/20 bg-white/40">
                    <div className="flex justify-between items-start mb-2">
                      <span className="text-sm font-bold text-sacred-gold-dark">
                        {translatePlanet(planet, language)}
                      </span>
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold border ${statusColor}`}>
                        {statusLabel}
                      </span>
                    </div>
                    <div className="grid grid-cols-2 gap-2 text-xs mb-2">
                      <div>
                        <span className="text-foreground/50 font-semibold">{t('lk.advanced.pakkaGhar')}</span>
                        <p className="font-bold text-foreground">{info.pakka_ghar}</p>
                      </div>
                      <div>
                        <span className="text-foreground/50 font-semibold">{t('lk.advanced.bunyaadHouse')}</span>
                        <p className="font-bold text-foreground">{info.bunyaad_house}</p>
                      </div>
                    </div>
                    {info.enemies_in_bunyaad && info.enemies_in_bunyaad.length > 0 && (
                      <div className="mb-2">
                        <span className="text-[10px] text-red-600 font-bold uppercase tracking-wider">
                          {t('lk.advanced.enemiesInBunyaad')}
                        </span>
                        <div className="flex flex-wrap gap-1 mt-0.5">
                          {info.enemies_in_bunyaad.map((e: string) => (
                            <span key={e} className="text-[10px] text-red-600 bg-red-50 px-1.5 py-0.5 rounded border border-red-100">
                              {translatePlanet(e, language)}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                    <p className="text-xs text-foreground/70 italic border-t border-sacred-gold/10 pt-2 mt-2">
                      {isHi ? info.interpretation_hi : info.interpretation_en}
                    </p>
                  </div>
                );
              })}
            </div>
          </section>

          {/* ── TAKKAR (Collision) Section ── */}
          <section>
            <div className="flex items-center gap-2 mb-2">
              <Swords className="w-5 h-5 text-red-600" />
              <h3 className="text-xl font-sans font-bold text-foreground">
                {t('lk.advanced.takkarTitle')}
              </h3>
            </div>
            <p className="text-sm text-foreground/60 mb-4">
              {t('lk.advanced.takkarDesc')}
            </p>

            {/* Summary Row */}
            <div className="flex flex-wrap gap-3 mb-4">
              {analysisData.takkar?.destructive_count != null && (
                <span className="px-3 py-1 rounded-full bg-red-100 text-red-800 text-xs font-bold border border-red-200">
                  {t('lk.advanced.takkar.destructive')}: {analysisData.takkar.destructive_count}
                </span>
              )}
              {analysisData.takkar?.mild_count != null && (
                <span className="px-3 py-1 rounded-full bg-amber-100 text-amber-800 text-xs font-bold border border-amber-200">
                  {t('lk.advanced.takkar.mild')}: {analysisData.takkar.mild_count}
                </span>
              )}
              {analysisData.takkar?.most_attacked_planet && (
                <span className="px-3 py-1 rounded-full bg-red-500/10 text-red-700 text-xs font-bold border border-red-300">
                  {t('lk.advanced.takkar.mostAttacked')}: {translatePlanet(analysisData.takkar.most_attacked_planet, language)}
                </span>
              )}
            </div>

            {/* Safe Planets */}
            {analysisData.takkar?.safe_planets && analysisData.takkar.safe_planets.length > 0 && (
              <div className="mb-4 flex flex-wrap items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-green-600" />
                <span className="text-xs font-bold text-green-700 uppercase tracking-wider">
                  {t('lk.advanced.safePlanets')}
                </span>
                {analysisData.takkar.safe_planets.map((p: string) => (
                  <span key={p} className="px-2 py-0.5 rounded bg-green-100 text-green-800 text-xs font-bold border border-green-200">
                    {translatePlanet(p, language)}
                  </span>
                ))}
              </div>
            )}

            {/* Collision Cards */}
            <div className="space-y-3">
              {analysisData.takkar?.collisions && analysisData.takkar.collisions.length > 0 ? (
                analysisData.takkar.collisions.map((c: any, i: number) => {
                  const isDestructive = c.severity === 'destructive';
                  return (
                    <div
                      key={i}
                      className={`p-4 rounded-xl border ${
                        isDestructive
                          ? 'border-red-200 bg-red-500/5'
                          : 'border-amber-200 bg-amber-500/5'
                      }`}
                    >
                      <div className="flex items-center gap-3 mb-2">
                        <span className={`text-sm font-bold ${isDestructive ? 'text-red-800' : 'text-amber-800'}`}>
                          {translatePlanet(c.attacker, language)}
                        </span>
                        <ArrowRight className={`w-4 h-4 ${isDestructive ? 'text-red-500' : 'text-amber-500'}`} />
                        <span className={`text-sm font-bold ${isDestructive ? 'text-red-800' : 'text-amber-800'}`}>
                          {translatePlanet(c.receiver, language)}
                        </span>
                        <span className={`ml-auto px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                          isDestructive
                            ? 'bg-red-200 text-red-800'
                            : 'bg-amber-200 text-amber-800'
                        }`}>
                          {isDestructive ? t('lk.advanced.takkar.destructive') : t('lk.advanced.takkar.mild')}
                        </span>
                      </div>
                      {c.axis && (
                        <p className="text-xs text-foreground/60 mb-1">
                          <span className="font-semibold">{t('lk.advanced.takkar.axis')}:</span> {c.axis}
                        </p>
                      )}
                      <p className="text-xs text-foreground/70 italic">
                        {isHi ? c.interpretation_hi : c.interpretation_en}
                      </p>
                    </div>
                  );
                })
              ) : (
                <div className="py-10 text-center border border-dashed border-gray-200 rounded-xl bg-green-500/5">
                  <p className="text-green-700 font-medium italic">
                    {t('lk.advanced.noCollisions')}
                  </p>
                </div>
              )}
            </div>
          </section>

          {/* ── ENEMY SIEGE Section ── */}
          <section>
            <div className="flex items-center gap-2 mb-2">
              <Shield className="w-5 h-5 text-orange-600" />
              <h3 className="text-xl font-sans font-bold text-foreground">
                {t('lk.advanced.enemySiegeTitle')}
              </h3>
            </div>
            <p className="text-sm text-foreground/60 mb-4">
              {t('lk.advanced.enemySiegeDesc')}
            </p>

            {/* Highlight Row */}
            <div className="flex flex-wrap gap-3 mb-4">
              {analysisData.enemy_presence?.most_besieged && (
                <span className="px-3 py-1 rounded-full bg-red-100 text-red-800 text-xs font-bold border border-red-200">
                  {t('lk.advanced.mostBesieged')}: {translatePlanet(analysisData.enemy_presence.most_besieged, language)}
                </span>
              )}
              {analysisData.enemy_presence?.least_besieged && (
                <span className="px-3 py-1 rounded-full bg-green-100 text-green-800 text-xs font-bold border border-green-200">
                  {t('lk.advanced.leastBesieged')}: {translatePlanet(analysisData.enemy_presence.least_besieged, language)}
                </span>
              )}
            </div>

            {/* Siege Cards */}
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {analysisData.enemy_presence?.planets && Object.entries(analysisData.enemy_presence.planets).map(([planet, info]: [string, any]) => {
                const siegeLevel = info.enemy_siege_level || 'none';
                const siegeStyles: Record<string, string> = {
                  severe: 'bg-red-200 text-red-800 border-red-300',
                  moderate: 'bg-orange-200 text-orange-800 border-orange-300',
                  mild: 'bg-amber-100 text-amber-800 border-amber-200',
                  none: 'bg-green-100 text-green-800 border-green-200',
                };
                const siegeLabelMap: Record<string, string> = {
                  severe: t('lk.advanced.siege.severe'),
                  moderate: t('lk.advanced.siege.moderate'),
                  mild: t('lk.advanced.siege.mild'),
                  none: t('lk.advanced.siege.none'),
                };

                return (
                  <div key={planet} className="card-sacred p-4 rounded-xl border border-sacred-gold/20 bg-white/40">
                    <div className="flex justify-between items-start mb-2">
                      <span className="text-sm font-bold text-sacred-gold-dark">
                        {translatePlanet(planet, language)}
                      </span>
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold border ${siegeStyles[siegeLevel] || siegeStyles.none}`}>
                        {siegeLabelMap[siegeLevel] || siegeLevel}
                      </span>
                    </div>
                    <div className="grid grid-cols-2 gap-2 text-xs mb-2">
                      <div>
                        <span className="text-foreground/50 font-semibold">{t('lk.advanced.totalEnemies')}</span>
                        <p className="font-bold text-foreground">{info.total_enemies ?? 0}</p>
                      </div>
                      <div>
                        <span className="text-foreground/50 font-semibold">{t('lk.advanced.inPakkaGhar')}</span>
                        <p className="font-bold text-foreground">{info.enemies_in_pakka_ghar ?? 0}</p>
                      </div>
                    </div>
                    <p className="text-xs text-foreground/70 italic border-t border-sacred-gold/10 pt-2 mt-2">
                      {isHi ? info.interpretation_hi : info.interpretation_en}
                    </p>
                  </div>
                );
              })}
            </div>
          </section>
        </>
      )}
    </div>
  );
}
