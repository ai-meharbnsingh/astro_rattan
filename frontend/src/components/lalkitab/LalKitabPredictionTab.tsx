import { useMemo, useState, useEffect, useCallback } from 'react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';
import { useLalKitab } from './LalKitabContext';
import { Star, Info, ThumbsUp, Meh } from 'lucide-react';

interface StudioArea {
  key: string;
  title_en: string;
  title_hi: string;
  score: number;
  confidence: 'high' | 'moderate' | 'low' | 'speculative';
  is_positive: boolean;
  positive_en: string;
  positive_hi: string;
  caution_en: string;
  caution_hi: string;
  remedy_en: string;
  remedy_hi: string;
  trace: Array<{ planet: string; house: number }>;
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
        <h2 className="text-xl font-sans font-semibold text-sacred-gold flex items-center gap-2 mb-1">
          <Info className="w-5 h-5" />
          {t('lk.studio.title')}
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

        return (
          <div key={a.key} className={`rounded-2xl border p-5 ${cfg.border} ${cfg.bg}`}>
            <div className="flex items-start justify-between gap-4 mb-3">
              <div>
                <h3 className="text-lg font-sans font-bold text-sacred-gold">
                  {isHi ? a.title_hi : a.title_en}
                </h3>
                <div className="flex items-center gap-2 mt-1">
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

