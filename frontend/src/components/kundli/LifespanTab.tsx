import { useState, useEffect } from 'react';
import { Loader2, HeartPulse, AlertTriangle, ShieldCheck, BookOpen, CheckCircle2, ChevronDown, ChevronUp, Sun, Moon, Compass, Scale, Info } from 'lucide-react';
import { api } from '@/lib/api';
import { Heading } from '@/components/ui/heading';

interface BalarishtaData {
  has_risk: boolean;
  risk_level: 'low' | 'moderate' | 'high' | 'severe';
  factors: string[];
  remedies_recommended: boolean;
  sloka_ref: string;
  cancelled: boolean;
}

interface AyuClass {
  category: 'Alpayu' | 'Madhyayu' | 'Dirghayu' | 'Purnayu';
  category_en: string;
  category_hi: string;
  years_range: string;
  reasoning_en: string;
  reasoning_hi: string;
  matched_rules: string[];
  dirghayu_score: number;
  alpayu_score: number;
  sloka_ref: string;
}

interface Harana {
  name: string;
  name_hi: string;
  reason: string;
  fraction: string;
  reduction_years: number;
}

interface MethodResult {
  raw: number;
  after_haranas: number;
  haranas: Harana[];
  breakdown?: Array<{ planet: string; [k: string]: any }>;
  notes?: string[];
}

interface LifespanResolution {
  pindayu_years: number;
  nisargayu_years: number;
  amsayu_years: number;
  method_used: 'majority' | 'average' | 'weighted';
  final_estimate_years: number;
  confidence: 'high' | 'moderate' | 'low';
  resolution_reason_en: string;
  resolution_reason_hi: string;
  sloka_ref: string;
}

interface LifespanPayload {
  pindayu: MethodResult;
  nisargayu: MethodResult;
  amsayu: MethodResult;
  selected_method: 'pindayu' | 'nisargayu' | 'amsayu';
  selection_reason_en: string;
  selection_reason_hi: string;
  final_years: number;
  classification: 'Alpayu' | 'Madhyayu' | 'Dirghayu' | 'Purnayu';
  lifespan_resolution?: LifespanResolution;
  sloka_ref: string;
}

interface ApiResponse {
  kundli_id?: string;
  person_name?: string;
  lifespan: LifespanPayload;
  ayu_class: AyuClass;
  balarishta: BalarishtaData;
}

interface Props {
  kundliId: string;
  language: string;
  t: (key: string) => string;
}

const CATEGORY_KEY_MAP: Record<string, string> = {
  Alpayu: 'auto.alpayu',
  Madhyayu: 'auto.madhyayu',
  Dirghayu: 'auto.dirghayu',
  Purnayu: 'auto.purnayu',
};

const CATEGORY_COLOR: Record<string, string> = {
  Alpayu: 'bg-orange-100 text-orange-800 border-orange-300',
  Madhyayu: 'bg-sacred-gold/15 text-sacred-gold-dark border-sacred-gold/40',
  Dirghayu: 'bg-emerald-100 text-emerald-800 border-emerald-300',
  Purnayu: 'bg-violet-100 text-violet-800 border-violet-400',
};

const RISK_COLOR: Record<string, string> = {
  low: 'bg-emerald-100 text-emerald-800 border-emerald-300',
  moderate: 'bg-amber-100 text-amber-800 border-amber-300',
  high: 'bg-orange-100 text-orange-800 border-orange-300',
  severe: 'bg-red-100 text-red-800 border-red-300',
};

const RISK_KEY_MAP: Record<string, string> = {
  low: 'auto.riskLow',
  moderate: 'auto.riskModerate',
  high: 'auto.riskHigh',
  severe: 'auto.riskSevere',
};

const METHOD_META: Record<string, { key: string; icon: any; color: string }> = {
  pindayu:   { key: 'auto.pindayu',   icon: Sun,     color: 'text-amber-600' },
  nisargayu: { key: 'auto.nisargayu', icon: Moon,    color: 'text-indigo-500' },
  amsayu:    { key: 'auto.amsayu',    icon: Compass, color: 'text-emerald-600' },
};

export default function LifespanTab({ kundliId, language, t }: Props) {
  const [data, setData] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [expandedMethod, setExpandedMethod] = useState<string | null>(null);
  const [avPindayu, setAvPindayu] = useState<any>(null);
  const isHi = language === 'hi';

  useEffect(() => {
    if (!kundliId) return;
    let cancelled = false;
    setLoading(true);
    setError('');
    (async () => {
      try {
        try {
          const res = await api.get<ApiResponse>(`/api/kundli/${kundliId}/lifespan`);
          if (!cancelled) setData(res);
        } catch {
          const fallback = await api.get<any>(`/api/kundli/${kundliId}/ayu-classification`);
          if (!cancelled) setData({ ...fallback, lifespan: null as any });
        }
      } catch (err: any) {
        if (!cancelled) setError(err?.message || 'Failed to load lifespan data');
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => { cancelled = true; };
  }, [kundliId]);

  useEffect(() => {
    if (!kundliId) return;
    let cancelled = false;
    api.get<any>(`/api/kundli/${kundliId}/pindayu`)
      .then(res => { if (!cancelled) setAvPindayu(res); })
      .catch(() => {});
    return () => { cancelled = true; };
  }, [kundliId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-8 h-8 animate-spin text-sacred-gold" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 rounded-lg bg-red-50 border border-red-200 text-red-700 text-sm">
        {error}
      </div>
    );
  }

  if (!data) return null;

  const { balarishta, ayu_class, lifespan } = data;
  const categoryName = isHi ? ayu_class.category_hi : ayu_class.category_en;
  const reasoning = isHi ? ayu_class.reasoning_hi : ayu_class.reasoning_en;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
          <HeartPulse className="w-6 h-6" />
          {t('auto.lifespan')}
        </Heading>
        <p className="text-sm text-muted-foreground">{t('auto.lifespanDesc')}</p>
      </div>

      {/* Final lifespan hero */}
      {lifespan && (
        <div className={`rounded-xl border-2 p-6 ${CATEGORY_COLOR[lifespan.classification] || CATEGORY_COLOR.Madhyayu}`}>
          <div className="flex items-start justify-between gap-4 flex-wrap">
            <div>
              <p className="text-xs font-semibold uppercase tracking-wider opacity-70">
                {t('auto.finalLifespan')}
              </p>
              <div className="flex items-baseline gap-3 mt-1">
                <span className="text-5xl font-bold">{lifespan.final_years.toFixed(1)}</span>
                <span className="text-lg">{t('auto.years')}</span>
              </div>
              <p className="text-sm mt-2">
                <span className="font-semibold">{t(CATEGORY_KEY_MAP[lifespan.classification])}</span>
              </p>
            </div>
            <div className="text-sm text-right">
              <p className="font-semibold">{t('auto.selectedMethod')}</p>
              <p className="opacity-80">
                {t(METHOD_META[lifespan.selected_method]?.key || 'auto.pindayu')}
              </p>
              <p className="text-xs mt-1 opacity-70 max-w-xs">
                {isHi ? lifespan.selection_reason_hi : lifespan.selection_reason_en}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-1.5 mt-4 pt-3 border-t border-current/20 text-[11px] opacity-70">
            <BookOpen className="w-3 h-3" />
            <span className="italic">{lifespan.sloka_ref}</span>
          </div>
        </div>
      )}

      {/* 3 methods comparison */}
      {lifespan && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {(['pindayu', 'nisargayu', 'amsayu'] as const).map((method) => {
            const m = lifespan[method];
            const isSelected = lifespan.selected_method === method;
            const meta = METHOD_META[method];
            const Icon = meta.icon;
            const expanded = expandedMethod === method;

            return (
              <div
                key={method}
                className={`rounded-xl border-2 p-4 transition-all ${
                  isSelected
                    ? 'border-sacred-gold bg-sacred-gold/10 shadow-md'
                    : 'border-sacred-gold/20 bg-white'
                }`}
              >
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <Icon className={`w-5 h-5 ${meta.color}`} />
                    <span className="text-sm font-semibold text-foreground">
                      {t(meta.key)}
                    </span>
                  </div>
                  {isSelected && (
                    <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-sacred-gold-dark text-white">
                      {t('auto.selected')}
                    </span>
                  )}
                </div>

                <div className="grid grid-cols-2 gap-2 mb-3">
                  <div>
                    <p className="text-[10px] text-muted-foreground uppercase tracking-wider">
                      {t('auto.rawYears')}
                    </p>
                    <p className="text-lg font-semibold text-foreground">{m.raw.toFixed(1)}</p>
                  </div>
                  <div>
                    <p className="text-[10px] text-muted-foreground uppercase tracking-wider">
                      {t('auto.afterHaranas')}
                    </p>
                    <p className="text-lg font-semibold text-sacred-gold-dark">
                      {m.after_haranas.toFixed(1)}
                    </p>
                  </div>
                </div>

                {(m.haranas.length > 0 || (m.breakdown && m.breakdown.length > 0) || (m.notes && m.notes.length > 0)) && (
                  <button
                    type="button"
                    onClick={() => setExpandedMethod(expanded ? null : method)}
                    className="w-full flex items-center justify-center gap-1 text-xs text-sacred-gold-dark hover:text-sacred-gold pt-2 border-t border-sacred-gold/15"
                  >
                    {expanded ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
                    {t('auto.details')}
                  </button>
                )}

                {expanded && (
                  <div className="mt-3 space-y-3 text-xs">
                    {m.haranas.length > 0 && (
                      <div>
                        <p className="font-semibold text-foreground mb-1">{t('auto.haranasApplied')}</p>
                        <ul className="space-y-1">
                          {m.haranas.map((h, i) => (
                            <li key={i} className="text-muted-foreground">
                              <span className="font-medium text-foreground">
                                {isHi ? h.name_hi : h.name}
                              </span>{' '}
                              ({h.fraction}) — <span className="text-red-600">−{h.reduction_years}y</span>
                              <p className="pl-2 text-[10px]">{h.reason}</p>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                    {m.breakdown && m.breakdown.length > 0 && (
                      <div>
                        <p className="font-semibold text-foreground mb-1">{t('auto.methodBreakdown')}</p>
                        <ul className="space-y-0.5">
                          {m.breakdown.map((b, i) => (
                            <li key={i} className="flex justify-between text-muted-foreground">
                              <span className="font-medium text-foreground">{b.planet}</span>
                              <span>{b.contribution?.toFixed?.(1) ?? b.contribution} y</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                    {m.notes && m.notes.length > 0 && (
                      <ul className="list-disc pl-4 text-muted-foreground space-y-0.5">
                        {m.notes.map((n, i) => (
                          <li key={i}>{n}</li>
                        ))}
                      </ul>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}

      {/* Feature 5: Lifespan Resolution — Adhyaya 13 */}
      {lifespan?.lifespan_resolution && (
        <section className="rounded-xl border-2 border-sacred-gold/40 bg-sacred-gold/5 p-5">
          <h3 className="font-semibold text-sacred-gold-dark mb-3 flex items-center gap-2">
            <Scale className="w-5 h-5" />
            {isHi ? 'आयुर्दाय विरोधाभास निराकरण (अ. 13)' : 'Lifespan Conflict Resolution (Adh. 13)'}
          </h3>
          {/* Three-system comparison table */}
          <div className="overflow-x-auto rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden mb-4">
            <table className="table-sacred w-full text-sm">
              <thead>
                <tr className="border-b border-sacred-gold/20">
                  <th className="text-left py-1 pr-4 text-muted-foreground font-medium text-xs uppercase tracking-wide">
                    {isHi ? 'विधि' : 'Method'}
                  </th>
                  <th className="text-right py-1 px-3 text-muted-foreground font-medium text-xs uppercase tracking-wide">
                    {isHi ? 'वर्ष' : 'Years'}
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr className="border-t border-sacred-gold/10">
                  <td className="py-1.5 pr-4 font-medium text-foreground flex items-center gap-1.5">
                    <Sun className="w-3.5 h-3.5 text-amber-500" /> {isHi ? 'पिण्डायु' : 'Pindayu'}
                  </td>
                  <td className="py-1.5 px-3 text-right font-semibold text-foreground">
                    {lifespan.lifespan_resolution.pindayu_years.toFixed(1)}
                  </td>
                </tr>
                <tr className="border-t border-sacred-gold/10">
                  <td className="py-1.5 pr-4 font-medium text-foreground">
                    <span className="flex items-center gap-1.5"><Moon className="w-3.5 h-3.5 text-indigo-500" /> {isHi ? 'निसर्गायु' : 'Nisargayu'}</span>
                  </td>
                  <td className="py-1.5 px-3 text-right font-semibold text-foreground">
                    {lifespan.lifespan_resolution.nisargayu_years.toFixed(1)}
                  </td>
                </tr>
                <tr className="border-t border-sacred-gold/10">
                  <td className="py-1.5 pr-4 font-medium text-foreground">
                    <span className="flex items-center gap-1.5"><Compass className="w-3.5 h-3.5 text-emerald-500" /> {isHi ? 'अंशायु' : 'Amsayu'}</span>
                  </td>
                  <td className="py-1.5 px-3 text-right font-semibold text-foreground">
                    {lifespan.lifespan_resolution.amsayu_years.toFixed(1)}
                  </td>
                </tr>
                <tr className="border-t-2 border-sacred-gold/40 bg-sacred-gold/10">
                  <td className="py-2 pr-4 font-bold text-sacred-gold-dark">
                    {isHi ? 'अंतिम अनुमान' : 'Final Estimate'}
                    <span className="ml-2 text-[10px] font-normal text-muted-foreground uppercase tracking-wide">
                      ({lifespan.lifespan_resolution.method_used})
                    </span>
                  </td>
                  <td className="py-2 px-3 text-right font-bold text-sacred-gold-dark text-lg">
                    {lifespan.lifespan_resolution.final_estimate_years.toFixed(1)}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          {/* Confidence badge */}
          <div className="flex items-center gap-2 mb-3">
            <span className={`text-xs font-semibold uppercase tracking-wider px-2 py-0.5 rounded ${
              lifespan.lifespan_resolution.confidence === 'high'
                ? 'bg-emerald-600 text-white'
                : lifespan.lifespan_resolution.confidence === 'moderate'
                ? 'bg-amber-500 text-white'
                : 'bg-orange-600 text-white'
            }`}>
              {isHi
                ? lifespan.lifespan_resolution.confidence === 'high' ? 'उच्च विश्वास' : lifespan.lifespan_resolution.confidence === 'moderate' ? 'मध्यम विश्वास' : 'निम्न विश्वास'
                : `${lifespan.lifespan_resolution.confidence.charAt(0).toUpperCase() + lifespan.lifespan_resolution.confidence.slice(1)} Confidence`
              }
            </span>
          </div>
          {/* Resolution reason */}
          <p className="text-xs text-foreground/80 leading-relaxed">
            {isHi ? lifespan.lifespan_resolution.resolution_reason_hi : lifespan.lifespan_resolution.resolution_reason_en}
          </p>
          <div className="flex items-center gap-1.5 mt-3 text-[10px] text-muted-foreground italic">
            <BookOpen className="w-3 h-3" />
            <span>{lifespan.lifespan_resolution.sloka_ref}</span>
          </div>
        </section>
      )}

      {/* Ashtakavarga Pindayu */}
      {avPindayu && (
        <div className="rounded-xl border-2 border-sacred-gold/30 bg-sacred-gold/5 p-5">
          <div className="flex items-center justify-between mb-3 flex-wrap gap-2">
            <h3 className="font-semibold text-sacred-gold-dark flex items-center gap-2">
              <Sun className="w-5 h-5" />
              {isHi ? 'अष्टकवर्ग पिण्डायु' : 'Ashtakavarga Pindayu'}
            </h3>
            {avPindayu.classification && (
              <span className={`text-xs font-bold px-2 py-0.5 rounded border ${CATEGORY_COLOR[avPindayu.classification] || CATEGORY_COLOR.Madhyayu}`}>
                {t(CATEGORY_KEY_MAP[avPindayu.classification] || 'auto.madhyayu')}
              </span>
            )}
          </div>
          {avPindayu.total_years != null && (
            <div className="flex items-baseline gap-2 mb-3">
              <span className="text-3xl font-bold text-sacred-gold-dark">{avPindayu.total_years.toFixed(1)}</span>
              <span className="text-sm text-muted-foreground">{t('auto.years')}</span>
            </div>
          )}
          {avPindayu.planet_contributions && (avPindayu.planet_contributions as any[]).length > 0 && (
            <div className="overflow-x-auto rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
              <table className="table-sacred w-full text-xs">
                <thead>
                  <tr className="border-b border-sacred-gold/20">
                    <th className="text-left py-1 pr-3 text-muted-foreground font-medium">{isHi ? 'ग्रह' : 'Planet'}</th>
                    <th className="text-center py-1 px-2 text-muted-foreground font-medium">{isHi ? 'भाव' : 'House'}</th>
                    <th className="text-center py-1 px-2 text-muted-foreground font-medium">{isHi ? 'बिंदु' : 'Bindus'}</th>
                    <th className="text-right py-1 pl-3 text-muted-foreground font-medium">{isHi ? 'वर्ष' : 'Years'}</th>
                  </tr>
                </thead>
                <tbody>
                  {(avPindayu.planet_contributions as any[]).map((pc: any, i: number) => (
                    <tr key={i} className="border-t border-sacred-gold/10">
                      <td className="py-1 pr-3 font-medium text-foreground">{pc.planet}</td>
                      <td className="py-1 px-2 text-center text-muted-foreground">{pc.house}</td>
                      <td className="py-1 px-2 text-center text-muted-foreground">{pc.bindus}</td>
                      <td className="py-1 pl-3 text-right font-semibold text-sacred-gold-dark">{pc.years?.toFixed(1)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {/* Ayu classification (from rule-based method) */}
      <div className={`rounded-xl border-2 p-5 ${CATEGORY_COLOR[ayu_class.category] || CATEGORY_COLOR.Madhyayu}`}>
        <div className="flex items-start justify-between gap-4 mb-3 flex-wrap">
          <div>
            <p className="text-xs font-semibold uppercase tracking-wider opacity-70">
              {t(CATEGORY_KEY_MAP[ayu_class.category] || 'auto.madhyayu')}
            </p>
            <h3 className="text-xl font-bold mt-1">{categoryName}</h3>
          </div>
          <div className="text-right">
            <p className="text-[11px] uppercase tracking-wider opacity-70">{t('auto.yearsRange')}</p>
            <p className="text-lg font-semibold">{ayu_class.years_range}</p>
          </div>
        </div>
        <p className="text-sm leading-relaxed mb-3">{reasoning}</p>
        {ayu_class.matched_rules.length > 0 && (
          <ul className="space-y-1">
            {ayu_class.matched_rules.map((rule, i) => (
              <li key={i} className="text-xs flex items-start gap-1.5">
                <CheckCircle2 className="w-3 h-3 shrink-0 mt-0.5 opacity-70" />
                <span>{rule}</span>
              </li>
            ))}
          </ul>
        )}
      </div>

      {/* Balarishta */}
      {balarishta.has_risk ? (
        <div className={`rounded-xl border-2 p-5 ${RISK_COLOR[balarishta.risk_level] || RISK_COLOR.low}`}>
          <div className="flex items-start gap-3 mb-3">
            <AlertTriangle className="w-5 h-5 shrink-0 mt-0.5" />
            <div>
              <h3 className="font-bold">{t('auto.balarishtaRisk')}</h3>
              <p className="text-xs mt-0.5 opacity-80">
                {t('auto.riskLevel')}:{' '}
                <span className="font-semibold">{t(RISK_KEY_MAP[balarishta.risk_level])}</span>
              </p>
            </div>
          </div>
          {balarishta.factors.length > 0 && (
            <ul className="space-y-1">
              {balarishta.factors.map((f, i) => (
                <li key={i} className="text-sm flex items-start gap-1.5">
                  <span className="mt-0.5 shrink-0">•</span>
                  <span>{f}</span>
                </li>
              ))}
            </ul>
          )}
          {balarishta.remedies_recommended && (
            <p className="text-xs mt-3 pt-3 border-t border-current/20 font-medium">
              {t('auto.remediesRecommended')}
            </p>
          )}
        </div>
      ) : balarishta.cancelled ? (
        <div className="rounded-xl border-2 border-emerald-300 bg-emerald-50 p-5 text-emerald-800">
          <div className="flex items-start gap-3">
            <ShieldCheck className="w-5 h-5 shrink-0 mt-0.5" />
            <div>
              <h3 className="font-bold">{t('auto.balarishtaRisk')}</h3>
              <p className="text-sm mt-1">{t('auto.balarishtaCancelled')}</p>
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
}
