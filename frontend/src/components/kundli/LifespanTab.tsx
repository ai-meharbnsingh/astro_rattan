import { useState, useEffect } from 'react';
import { Loader2, HeartPulse, AlertTriangle, ShieldCheck, BookOpen, CheckCircle2 } from 'lucide-react';
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

interface LifespanData {
  kundli_id?: string;
  person_name?: string;
  balarishta: BalarishtaData;
  ayu_class: AyuClass;
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

export default function LifespanTab({ kundliId, language, t }: Props) {
  const [data, setData] = useState<LifespanData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const isHi = language === 'hi';

  useEffect(() => {
    if (!kundliId) return;
    let cancelled = false;
    setLoading(true);
    setError('');
    (async () => {
      try {
        const res = await api.get<LifespanData>(`/api/kundli/${kundliId}/ayu-classification`);
        if (!cancelled) setData(res);
      } catch (err: any) {
        if (!cancelled) setError(err?.message || 'Failed to load lifespan data');
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
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

  const { balarishta, ayu_class } = data;
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

      {/* AYU Category Card */}
      <div className={`rounded-xl border-2 p-6 ${CATEGORY_COLOR[ayu_class.category] || CATEGORY_COLOR.Madhyayu}`}>
        <div className="flex items-start justify-between gap-4 mb-4">
          <div>
            <p className="text-xs font-semibold uppercase tracking-wider opacity-70">
              {t(CATEGORY_KEY_MAP[ayu_class.category] || 'auto.madhyayu')}
            </p>
            <h3 className="text-2xl font-bold mt-1">{categoryName}</h3>
          </div>
          <div className="text-right">
            <p className="text-[11px] uppercase tracking-wider opacity-70">{t('auto.yearsRange')}</p>
            <p className="text-lg font-semibold">{ayu_class.years_range}</p>
          </div>
        </div>

        <p className="text-sm leading-relaxed mb-4">{reasoning}</p>

        {ayu_class.matched_rules.length > 0 && (
          <div>
            <p className="text-[11px] font-semibold uppercase tracking-wider opacity-70 mb-2">
              {t('auto.reasoningFactors')}
            </p>
            <ul className="space-y-1">
              {ayu_class.matched_rules.map((rule, i) => (
                <li key={i} className="text-sm flex items-start gap-1.5">
                  <CheckCircle2 className="w-3.5 h-3.5 shrink-0 mt-0.5 opacity-70" />
                  <span>{rule}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        <div className="flex items-center gap-1.5 mt-4 pt-3 border-t border-current/20 text-[11px] opacity-70">
          <BookOpen className="w-3 h-3" />
          <span className="italic">{ayu_class.sloka_ref}</span>
        </div>
      </div>

      {/* Score bars */}
      <div className="grid grid-cols-2 gap-4">
        <div className="p-4 rounded-lg border border-sacred-gold/25 bg-gradient-to-br from-emerald-50 to-white">
          <p className="text-xs font-semibold text-emerald-800 mb-2">
            {t('auto.dirghayu')} {isHi ? 'संकेतक' : 'Score'}
          </p>
          <p className="text-2xl font-bold text-emerald-900">{ayu_class.dirghayu_score}</p>
          <div className="w-full h-1.5 rounded-full bg-emerald-100 mt-2 overflow-hidden">
            <div
              className="h-full bg-emerald-500"
              style={{ width: `${Math.min(100, ayu_class.dirghayu_score * 12)}%` }}
            />
          </div>
        </div>
        <div className="p-4 rounded-lg border border-sacred-gold/25 bg-gradient-to-br from-orange-50 to-white">
          <p className="text-xs font-semibold text-orange-800 mb-2">
            {t('auto.alpayu')} {isHi ? 'संकेतक' : 'Score'}
          </p>
          <p className="text-2xl font-bold text-orange-900">{ayu_class.alpayu_score}</p>
          <div className="w-full h-1.5 rounded-full bg-orange-100 mt-2 overflow-hidden">
            <div
              className="h-full bg-orange-500"
              style={{ width: `${Math.min(100, ayu_class.alpayu_score * 15)}%` }}
            />
          </div>
        </div>
      </div>

      {/* Balarishta */}
      {balarishta.has_risk ? (
        <div className={`rounded-xl border-2 p-5 ${RISK_COLOR[balarishta.risk_level] || RISK_COLOR.low}`}>
          <div className="flex items-start gap-3 mb-3">
            <AlertTriangle className="w-5 h-5 shrink-0 mt-0.5" />
            <div className="flex-1">
              <h3 className="font-bold">{t('auto.balarishtaRisk')}</h3>
              <p className="text-xs mt-0.5 opacity-80">
                {t('auto.riskLevel')}: <span className="font-semibold">{t(RISK_KEY_MAP[balarishta.risk_level])}</span>
              </p>
            </div>
          </div>
          {balarishta.factors.length > 0 && (
            <div>
              <p className="text-[11px] font-semibold uppercase tracking-wider opacity-70 mb-2">
                {t('auto.riskFactors')}
              </p>
              <ul className="space-y-1">
                {balarishta.factors.map((f, i) => (
                  <li key={i} className="text-sm flex items-start gap-1.5">
                    <span className="mt-0.5 shrink-0">•</span>
                    <span>{f}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
          {balarishta.remedies_recommended && (
            <p className="text-xs mt-3 pt-3 border-t border-current/20 font-medium">
              {t('auto.remediesRecommended')}
            </p>
          )}
          <div className="flex items-center gap-1.5 mt-3 pt-2 border-t border-current/20 text-[11px] opacity-70">
            <BookOpen className="w-3 h-3" />
            <span className="italic">{balarishta.sloka_ref}</span>
          </div>
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
