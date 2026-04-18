import { useMemo, useState, useEffect, useCallback } from 'react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';
import { useLalKitab } from './LalKitabContext';
import { Star, Info, ThumbsUp, Meh, AlertTriangle, TrendingUp, Scale, Shield } from 'lucide-react';
import { pickLang } from './safe-render';
import SourceBadge from './SourceBadge';

type StudioLabel = 'STRONG' | 'MODERATE' | 'NEEDS ATTENTION';

interface BilingualText {
  en?: string;
  hi?: string;
}

interface StudioArea {
  key: string;
  title_en: string;
  title_hi: string;
  score: number;
  confidence: 'high' | 'moderate' | 'low' | 'speculative';
  label?: StudioLabel | string;
  is_positive: boolean;
  positive_en: string;
  positive_hi: string;
  caution_en: string;
  caution_hi: string;
  remedy_en: string;
  remedy_hi: string;
  trace: Array<{ planet: string; house: number }>;
  // 3-part cause structure (backend Codex R4-P5)
  primary_cause?: BilingualText;
  secondary_modifier?: BilingualText;
  supporting_factor?: BilingualText;
  weakest_planet?: string | null;
  weakest_house?: number | null;
  weakest_dignity?: string | null;
  strongest_planet?: string | null;
  strongest_house?: number | null;
  strongest_dignity?: string | null;
}

const labelConfig: Record<string, { bg: string; text: string; border: string; icon: typeof Star; en: string; hi: string }> = {
  STRONG: {
    bg: 'bg-green-600',
    text: 'text-white',
    border: 'border-green-700',
    icon: TrendingUp,
    en: 'STRONG',
    hi: 'सशक्त',
  },
  MODERATE: {
    bg: 'bg-amber-500',
    text: 'text-white',
    border: 'border-amber-600',
    icon: Scale,
    en: 'MODERATE',
    hi: 'मध्यम',
  },
  'NEEDS ATTENTION': {
    bg: 'bg-red-600',
    text: 'text-white',
    border: 'border-red-700',
    icon: AlertTriangle,
    en: 'NEEDS ATTENTION',
    hi: 'ध्यान आवश्यक',
  },
};

function getLabelConfig(label: string | undefined, score: number) {
  if (label && labelConfig[label]) return labelConfig[label];
  // Fallback derivation matching backend thresholds
  if (score >= 70) return labelConfig.STRONG;
  if (score >= 55) return labelConfig.MODERATE;
  return labelConfig['NEEDS ATTENTION'];
}

interface StudioResponse {
  kundli_id: string;
  areas: StudioArea[];
}

const STORAGE_KEY_PREFIX = 'lk_prediction_feedback_';

const confidenceConfig: Record<string, { border: string; bg: string; badge: string; bar: string; icon: typeof Star }> = {
  high: {
    border: 'border-green-300/30',
    bg: 'bg-green-500/5',
    badge: 'bg-green-500/10 text-green-700 border-green-300/30',
    bar: 'bg-green-500',
    icon: Star,
  },
  moderate: {
    border: 'border-sacred-gold/30',
    bg: 'bg-sacred-gold/5',
    badge: 'bg-sacred-gold/10 text-sacred-gold-dark border-sacred-gold/30',
    bar: 'bg-sacred-gold',
    icon: Star,
  },
  low: {
    border: 'border-orange-300/30',
    bg: 'bg-orange-500/5',
    badge: 'bg-orange-500/10 text-orange-700 border-orange-300/30',
    bar: 'bg-orange-500',
    icon: Star,
  },
  speculative: {
    border: 'border-gray-300/30',
    bg: 'bg-gray-500/5',
    badge: 'bg-gray-500/10 text-gray-700 border-gray-300/30',
    bar: 'bg-gray-500',
    icon: Star,
  },
};

export default function LalKitabPredictionTab() {
  const { t, language } = useTranslation();
  const isHi = language === 'hi';
  const { kundliId } = useLalKitab();

  const [studio, setStudio] = useState<StudioResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const storageKey = `${STORAGE_KEY_PREFIX}${kundliId || ''}`;
  const [feedback, setFeedback] = useState<Record<string, string>>({});

  useEffect(() => {
    if (!kundliId) return;
    setError(null);
    api.get(`/api/lalkitab/predictions/studio/${kundliId}`)
      .then((res: any) => setStudio(res as StudioResponse))
      .catch((e: any) => setError(e instanceof Error ? e.message : (isHi ? 'लोड नहीं हो सका' : 'Failed to load')));
  }, [kundliId]);

  // Load feedback: API is authoritative; localStorage is optimistic cache
  useEffect(() => {
    if (!kundliId) return;
    try {
      const cached = localStorage.getItem(storageKey);
      if (cached) setFeedback(JSON.parse(cached));
    } catch { /* ignore */ }

    api.get(`/api/lalkitab/predictions/feedback/${kundliId}`)
      .then((res: any) => {
        if (res?.feedback && typeof res.feedback === 'object') {
          setFeedback(res.feedback);
          localStorage.setItem(storageKey, JSON.stringify(res.feedback));
        }
      })
      .catch(() => { /* keep local */ });
  }, [kundliId, storageKey]);

  const saveFeedback = useCallback((areaKey: string, value: string) => {
    if (!kundliId) return;
    const next = { ...feedback, [areaKey]: value };
    setFeedback(next);
    localStorage.setItem(storageKey, JSON.stringify(next));
    api.post('/api/lalkitab/predictions/feedback', { kundli_id: kundliId, feedback: next })
      .catch(() => { /* optimistic */ });
  }, [feedback, kundliId, storageKey]);

  const areas = useMemo(() => (studio?.areas || []).slice().sort((a, b) => b.score - a.score), [studio]);

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
        <h2 className="text-xl font-sans font-semibold text-sacred-gold flex items-center gap-2 mb-1 flex-wrap">
          <Info className="w-5 h-5" />
          {t('lk.studio.title')}
          <SourceBadge source="PRODUCT" size="xs" />
        </h2>
        <p className="text-sm text-gray-500">{t('lk.studio.desc')}</p>
      </div>

      {error && (
        <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-red-700 text-sm">
          {error}
        </div>
      )}

      {areas.map((a) => {
        const cfg = confidenceConfig[a.confidence] || confidenceConfig.speculative;
        const Icon = cfg.icon;
        const userRating = feedback[a.key] || '';
        const isPositive = !!a.is_positive;
        const StatusIcon = isPositive ? ThumbsUp : Meh;
        const trace = a.trace || [];
        const lbl = getLabelConfig(a.label, a.score);
        const LabelIcon = lbl.icon;

        const primaryCause = pickLang(a.primary_cause, isHi);
        const secondaryModifier = pickLang(a.secondary_modifier, isHi);
        const supportingFactor = pickLang(a.supporting_factor, isHi);
        const hasCauseBreakdown = !!(primaryCause || secondaryModifier || supportingFactor);

        return (
          <div key={a.key} className={`rounded-2xl border p-5 ${cfg.border} ${cfg.bg}`}>
            <div className="flex items-start justify-between gap-4 mb-3">
              <div className="flex-1 min-w-0">
                <h3 className="text-lg font-sans font-bold text-sacred-gold">
                  {isHi ? a.title_hi : a.title_en}
                </h3>
                <div className="flex items-center gap-2 mt-2 flex-wrap">
                  <span className={`inline-flex items-center gap-1 text-[11px] px-2.5 py-1 rounded-full border font-bold shadow-sm ${lbl.bg} ${lbl.text} ${lbl.border}`}>
                    <LabelIcon className="w-3 h-3" />
                    {pickLang(lbl, isHi)}
                  </span>
                  <span className={`text-[10px] px-2 py-0.5 rounded-full border font-bold ${cfg.badge}`}>
                    {a.confidence.toUpperCase()}
                  </span>
                  <span className="text-xs text-muted-foreground">
                    {t('lk.studio.score')}: {isNaN(a.score) ? 0 : a.score}/100
                  </span>
                </div>
              </div>
              <Icon className="w-5 h-5 text-sacred-gold shrink-0" />
            </div>

            <div className="h-1.5 rounded-full bg-black/5 overflow-hidden mb-4">
              <div className={`h-1.5 rounded-full transition-all duration-700 ${cfg.bar}`} style={{ width: `${a.score}%` }} />
            </div>

            <div className={`flex items-start gap-2 mb-4 p-3 rounded-lg ${isPositive ? 'bg-green-500/8' : 'bg-orange-400/8'}`}>
              <StatusIcon className={`w-4 h-4 shrink-0 mt-0.5 ${isPositive ? 'text-green-600' : 'text-orange-500'}`} />
              <p className="text-xs font-medium text-foreground/80 leading-relaxed">
                <span className={`font-bold ${isPositive ? 'text-green-600' : 'text-orange-600'} uppercase tracking-tight`}>
                  {isPositive ? t('lk.studio.positive') : t('lk.studio.caution')}:{' '}
                </span>
                {isPositive ? (isHi ? a.positive_hi : a.positive_en) : (isHi ? a.caution_hi : a.caution_en)}
              </p>
            </div>

            {hasCauseBreakdown && (
              <div className="mb-4 space-y-2">
                <p className="text-xs font-bold text-sacred-gold uppercase tracking-widest mb-1.5 flex items-center gap-2 flex-wrap">
                  {isHi ? 'चार्ट विश्लेषण' : 'Chart Analysis'}
                  <SourceBadge source="LK_DERIVED" size="xs" />
                </p>

                {primaryCause && (
                  <div className="rounded-lg border border-red-300/30 bg-red-500/5 p-3">
                    <div className="flex items-center gap-1.5 mb-1">
                      <AlertTriangle className="w-3.5 h-3.5 text-red-600" />
                      <p className="text-[10px] font-bold text-red-700 uppercase tracking-wider">
                        {isHi ? 'प्राथमिक कारण' : 'Primary Cause'}
                      </p>
                    </div>
                    <p className="text-xs text-foreground/80 leading-relaxed">{primaryCause}</p>
                  </div>
                )}

                {secondaryModifier && (
                  <div className="rounded-lg border border-amber-300/30 bg-amber-500/5 p-3">
                    <div className="flex items-center gap-1.5 mb-1">
                      <Scale className="w-3.5 h-3.5 text-amber-600" />
                      <p className="text-[10px] font-bold text-amber-700 uppercase tracking-wider">
                        {isHi ? 'द्वितीयक प्रभाव' : 'Secondary Modifier'}
                      </p>
                    </div>
                    <p className="text-xs text-foreground/80 leading-relaxed">{secondaryModifier}</p>
                  </div>
                )}

                {supportingFactor && (
                  <div className="rounded-lg border border-green-300/30 bg-green-500/5 p-3">
                    <div className="flex items-center gap-1.5 mb-1">
                      <Shield className="w-3.5 h-3.5 text-green-600" />
                      <p className="text-[10px] font-bold text-green-700 uppercase tracking-wider">
                        {isHi ? 'सहायक कारक' : 'Supporting Factor'}
                      </p>
                    </div>
                    <p className="text-xs text-foreground/80 leading-relaxed">{supportingFactor}</p>
                  </div>
                )}
              </div>
            )}

            <div className="mb-4">
              <p className="text-xs font-bold text-sacred-gold uppercase tracking-widest mb-1.5">{t('lk.studio.actionLabel')}</p>
              <p className="text-sm text-foreground/70 leading-snug">{isHi ? a.remedy_hi : a.remedy_en}</p>
            </div>

            <div className="mb-6">
              <p className="text-xs font-bold text-sacred-gold uppercase tracking-widest mb-2">{t('lk.studio.whyLabel')}</p>
              <div className="flex flex-wrap gap-1.5">
                {trace.map((tr) => (
                  <span key={`${tr.planet}-${tr.house}`} className="text-[10px] px-2 py-0.5 rounded bg-sacred-gold/10 text-sacred-gold-dark font-bold">
                    {tr.planet} {isHi ? `भाव ${tr.house}` : `H${tr.house}`}
                  </span>
                ))}
              </div>
            </div>

            <div className="mt-auto pt-4 border-t border-sacred-gold/10">
              <p className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-3">
                {t('lk.prediction.feedbackTitle')}
              </p>
              <div className="flex gap-2">
                <button
                  onClick={() => saveFeedback(a.key, 'happened')}
                  className={`flex-1 flex items-center justify-center gap-1.5 py-2 rounded-lg text-[10px] font-bold transition-all border ${
                    userRating === 'happened'
                      ? 'bg-green-600 text-white border-green-600 shadow-md'
                      : 'bg-white/50 text-gray-500 border-gray-200 hover:border-green-300'
                  }`}
                >
                  <ThumbsUp className="w-3 h-3" />
                  {t('lk.prediction.happened')}
                </button>
                <button
                  onClick={() => saveFeedback(a.key, 'partially')}
                  className={`flex-1 flex items-center justify-center gap-1.5 py-2 rounded-lg text-[10px] font-bold transition-all border ${
                    userRating === 'partially'
                      ? 'bg-sacred-gold text-white border-sacred-gold shadow-md'
                      : 'bg-white/50 text-gray-500 border-gray-200 hover:border-sacred-gold/30'
                  }`}
                >
                  <Star className="w-3 h-3" />
                  {t('lk.prediction.partially')}
                </button>
                <button
                  onClick={() => saveFeedback(a.key, 'not_happened')}
                  className={`flex-1 flex items-center justify-center gap-1.5 py-2 rounded-lg text-[10px] font-bold transition-all border ${
                    userRating === 'not_happened'
                      ? 'bg-gray-800 text-white border-gray-800 shadow-md'
                      : 'bg-white/50 text-gray-500 border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <Meh className="w-3 h-3" />
                  {t('lk.prediction.notHappened')}
                </button>
              </div>
            </div>
          </div>
        );
      })}

      {!error && areas.length === 0 && (
        <div className="text-center py-8 text-sm text-muted-foreground">
          {isHi ? 'कोई डेटा नहीं।' : 'No data.'}
        </div>
      )}
    </div>
  );
}

