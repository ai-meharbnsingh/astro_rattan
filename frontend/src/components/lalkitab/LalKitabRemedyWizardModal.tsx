/**
 * P2.4 — Remedy Wizard modal.
 *
 * Three steps:
 *   1. Intent picker — 9 cards (bilingual)
 *   2. Loading — "Analysing your chart..."
 *   3. Results — top 3 ranked remedies with match_reason highlighted,
 *               plus the full ranked list below
 *
 * Backend: POST /api/lalkitab/remedy-wizard  {kundli_id, intent}
 */

import { useState, useEffect, useCallback } from 'react';
import { api } from '@/lib/api';
import {
  Wallet, Heart, Briefcase, Activity, Baby, Flame, Home as HomeIcon, Swords, Scale,
  Loader2, AlertTriangle, Sparkles, HelpCircle, Lightbulb, ArrowLeft, Wand2, X,
} from 'lucide-react';
import SourceBadge from './SourceBadge';

type WizardStep = 'pick' | 'loading' | 'result';

interface IntentCard {
  id: string;
  label_en: string;
  label_hi: string;
  desc_en: string;
  desc_hi: string;
  icon: string;
  focus_planets: string[];
  focus_houses: number[];
}

interface RankedRemedy {
  planet: string;
  planet_hi: string;
  sign: string;
  lk_house: number;
  dignity: string;
  strength: number;
  has_remedy: boolean;
  urgency: 'high' | 'medium' | 'low';
  material?: string;
  day?: string;
  remedy_en: string;
  remedy_hi: string;
  problem_en: string;
  problem_hi: string;
  reason_en: string;
  reason_hi: string;
  how_en: string;
  how_hi: string;
  match_reason_en: string;
  match_reason_hi: string;
  relevance_score: number;
  matches_focus_planet?: boolean;
  matches_focus_house?: boolean;
  matches_avoid?: boolean;
  afflictions?: string[];
}

interface WizardResult {
  intent: string;
  intent_label_en: string;
  intent_label_hi: string;
  focus_planets: string[];
  focus_houses: number[];
  avoid: Array<{ planet: string; house: number }>;
  ranked_remedies: RankedRemedy[];
  top_picks: RankedRemedy[];
  source: string;
}

interface Props {
  kundliId: string;
  isHi: boolean;
  open: boolean;
  onClose: () => void;
}

const ICON_MAP: Record<string, React.ComponentType<{ className?: string }>> = {
  Wallet, Heart, Briefcase, Activity, Baby, Flame, Home: HomeIcon, Swords, Scale,
};

const URGENCY_BADGE: Record<string, string> = {
  high:   'bg-red-100 text-red-700 border-red-200',
  medium: 'bg-amber-100 text-amber-700 border-amber-200',
  low:    'bg-gray-100 text-gray-600 border-gray-200',
};

function IntentIcon({ name, className }: { name: string; className?: string }) {
  const Cmp = ICON_MAP[name] ?? Wand2;
  return <Cmp className={className} />;
}

function RankedCard({ r, isHi, highlight }: { r: RankedRemedy; isHi: boolean; highlight?: boolean }) {
  const badge = URGENCY_BADGE[r.urgency] ?? URGENCY_BADGE.low;
  const urgencyLabel = r.urgency === 'high'
    ? (isHi ? 'अत्यावश्यक' : 'Urgent')
    : r.urgency === 'medium'
    ? (isHi ? 'सामान्य' : 'Medium')
    : (isHi ? 'वैकल्पिक' : 'Optional');

  return (
    <div className={`rounded-xl border-2 p-4 ${
      highlight ? 'border-sacred-gold/60 bg-sacred-gold/5' : 'border-border bg-card'
    }`}>
      <div className="flex items-center flex-wrap gap-2 mb-2">
        <span className="font-semibold text-sm text-foreground">
          {isHi ? r.planet_hi : r.planet}
        </span>
        <span className="text-xs text-muted-foreground">
          {isHi ? `भाव ${r.lk_house}` : `H${r.lk_house}`} · {r.sign}
        </span>
        {r.matches_avoid && (
          <span className="text-[10px] px-1.5 py-0.5 rounded bg-red-100 text-red-700 border border-red-200 font-semibold">
            {isHi ? 'बाधा-संयोजन' : 'Obstacle pattern'}
          </span>
        )}
        {r.matches_focus_planet && (
          <span className="text-[10px] px-1.5 py-0.5 rounded bg-violet-100 text-violet-700 border border-violet-200 font-semibold">
            {isHi ? 'केंद्र ग्रह' : 'Focus planet'}
          </span>
        )}
        {r.matches_focus_house && (
          <span className="text-[10px] px-1.5 py-0.5 rounded bg-blue-100 text-blue-700 border border-blue-200 font-semibold">
            {isHi ? 'केंद्र भाव' : 'Focus house'}
          </span>
        )}
        <span className={`ml-auto text-xs px-2 py-0.5 rounded-full border font-medium ${badge}`}>
          {urgencyLabel}
        </span>
      </div>

      {/* MATCH REASON — the wizard's unique value */}
      <div className="flex gap-2 mb-3 rounded-lg bg-sacred-gold/10 border border-sacred-gold/30 p-2.5">
        <Wand2 className="w-4 h-4 text-sacred-gold shrink-0 mt-0.5" />
        <div>
          <p className="text-[10px] font-bold text-sacred-gold uppercase tracking-wide mb-0.5">
            {isHi ? 'यह उपाय क्यों?' : 'Why this remedy?'}
          </p>
          <p className="text-xs text-foreground/80 leading-relaxed">
            {isHi ? r.match_reason_hi : r.match_reason_en}
          </p>
          <p className="text-[10px] text-muted-foreground mt-1">
            {isHi ? 'प्रासंगिकता:' : 'Relevance:'} {r.relevance_score.toFixed(2)}
          </p>
        </div>
      </div>

      <div className="space-y-2.5">
        {/* Problem */}
        <div className="flex gap-2">
          <AlertTriangle className="w-4 h-4 text-red-500 shrink-0 mt-0.5" />
          <div>
            <p className="text-[10px] font-semibold text-red-600 uppercase tracking-wide mb-0.5">
              {isHi ? 'समस्या' : 'Problem'}
            </p>
            <p className="text-sm text-foreground leading-relaxed">
              {isHi ? (r.problem_hi || '—') : (r.problem_en || '—')}
            </p>
          </div>
        </div>

        {/* Reason */}
        <div className="flex gap-2">
          <HelpCircle className="w-4 h-4 text-amber-500 shrink-0 mt-0.5" />
          <div>
            <p className="text-[10px] font-semibold text-amber-600 uppercase tracking-wide mb-0.5">
              {isHi ? 'कारण' : 'Reason'}
            </p>
            <p className="text-sm text-foreground leading-relaxed">
              {isHi ? (r.reason_hi || '—') : (r.reason_en || '—')}
            </p>
          </div>
        </div>

        {/* Remedy */}
        <div className="flex gap-2">
          <Sparkles className="w-4 h-4 text-sacred-gold shrink-0 mt-0.5" />
          <div>
            <p className="text-[10px] font-semibold text-sacred-gold uppercase tracking-wide mb-0.5">
              {isHi ? 'उपाय' : 'Remedy'}
            </p>
            <p className="text-sm text-foreground leading-relaxed">
              {isHi ? (r.remedy_hi || '—') : (r.remedy_en || '—')}
            </p>
            <div className="flex flex-wrap gap-2 mt-1.5">
              {r.material && (
                <span className="text-[10px] px-1.5 py-0.5 rounded bg-sacred-gold/10 text-sacred-gold-dark border border-sacred-gold/20">
                  {isHi ? 'सामग्री:' : 'Material:'} {r.material}
                </span>
              )}
              {r.day && (
                <span className="text-[10px] px-1.5 py-0.5 rounded bg-foreground/5 border border-border">
                  {isHi ? 'दिन:' : 'Day:'} {r.day}
                </span>
              )}
            </div>
          </div>
        </div>

        {/* Why it works */}
        {(r.how_en || r.how_hi) && (
          <div className="flex gap-2">
            <Lightbulb className="w-4 h-4 text-blue-500 shrink-0 mt-0.5" />
            <div>
              <p className="text-[10px] font-semibold text-blue-600 uppercase tracking-wide mb-0.5">
                {isHi ? 'क्यों काम करता है' : 'Why it works'}
              </p>
              <p className="text-sm text-foreground/80 leading-relaxed italic">
                {isHi ? r.how_hi : r.how_en}
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function LalKitabRemedyWizardModal({ kundliId, isHi, open, onClose }: Props) {
  const [step, setStep] = useState<WizardStep>('pick');
  const [intents, setIntents] = useState<IntentCard[]>([]);
  const [intentsLoading, setIntentsLoading] = useState(false);
  const [result, setResult] = useState<WizardResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Load intent catalog on open
  useEffect(() => {
    if (!open) return;
    // Reset state when opening
    setStep('pick');
    setResult(null);
    setError(null);

    if (intents.length === 0) {
      setIntentsLoading(true);
      api.get('/api/lalkitab/remedy-wizard/intents')
        .then((res: any) => setIntents(Array.isArray(res?.intents) ? res.intents : []))
        .catch(() => setError(isHi ? 'इरादे लोड नहीं हो सके' : 'Could not load intents'))
        .finally(() => setIntentsLoading(false));
    }
  }, [open]);

  // Close on Escape
  useEffect(() => {
    if (!open) return;
    const handler = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [open, onClose]);

  const pickIntent = useCallback(async (intentId: string) => {
    if (!kundliId) {
      setError(isHi ? 'कुंडली आईडी अनुपस्थित' : 'Kundli id missing');
      return;
    }
    setStep('loading');
    setError(null);
    try {
      const res: any = await api.post('/api/lalkitab/remedy-wizard', {
        kundli_id: kundliId,
        intent: intentId,
      });
      if (res?.error) {
        setError(res.error);
        setStep('pick');
        return;
      }
      setResult(res as WizardResult);
      setStep('result');
    } catch (e: any) {
      setError(e?.message || (isHi ? 'विश्लेषण विफल' : 'Analysis failed'));
      setStep('pick');
    }
  }, [kundliId, isHi]);

  if (!open) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4 overflow-y-auto"
      onClick={(e) => { if (e.target === e.currentTarget) onClose(); }}
    >
      <div className="relative w-full max-w-4xl bg-card rounded-2xl border-2 border-sacred-gold/40 shadow-2xl max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 z-10 bg-card border-b border-sacred-gold/20 px-5 py-3 flex items-center gap-3">
          <Wand2 className="w-5 h-5 text-sacred-gold" />
          <h2 className="font-semibold text-sacred-gold flex-1">
            {isHi ? 'उपाय विज़र्ड' : 'Remedy Wizard'}
          </h2>
          <SourceBadge source="LK_DERIVED" size="xs" />
          <button
            type="button"
            aria-label={isHi ? 'बंद करें' : 'Close'}
            onClick={onClose}
            className="p-1 rounded-full hover:bg-foreground/10 transition"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        <div className="p-5">
          {error && (
            <div className="mb-4 rounded-xl border border-red-200 bg-red-50 p-3 text-sm text-red-700">
              {error}
            </div>
          )}

          {/* Step 1 — Intent picker */}
          {step === 'pick' && (
            <div>
              <div className="mb-4">
                <h3 className="text-lg font-bold text-foreground mb-1">
                  {isHi ? 'आप क्या सुधारना चाहते हैं?' : 'What do you want to improve?'}
                </h3>
                <p className="text-sm text-muted-foreground">
                  {isHi
                    ? 'अपना उद्देश्य चुनें — हम आपकी कुंडली से उसी उद्देश्य के लिए सबसे प्रासंगिक 3 उपाय निकालेंगे।'
                    : 'Pick your goal — we will surface the 3 most relevant Lal Kitab remedies from your chart for THAT goal.'}
                </p>
              </div>

              {intentsLoading && (
                <div className="flex items-center justify-center py-12">
                  <Loader2 className="w-6 h-6 animate-spin text-sacred-gold mr-2" />
                  <span className="text-sm text-muted-foreground">
                    {isHi ? 'इरादे लोड हो रहे हैं...' : 'Loading intents...'}
                  </span>
                </div>
              )}

              {!intentsLoading && intents.length > 0 && (
                <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                  {intents.map((it) => (
                    <button
                      key={it.id}
                      type="button"
                      onClick={() => pickIntent(it.id)}
                      className="group text-left rounded-xl border-2 border-border hover:border-sacred-gold bg-background hover:bg-sacred-gold/5 p-4 transition"
                    >
                      <div className="flex items-center gap-2 mb-1.5">
                        <div className="w-9 h-9 rounded-full bg-sacred-gold/15 text-sacred-gold flex items-center justify-center group-hover:bg-sacred-gold group-hover:text-white transition">
                          <IntentIcon name={it.icon} className="w-5 h-5" />
                        </div>
                        <span className="font-semibold text-sm text-foreground">
                          {isHi ? it.label_hi : it.label_en}
                        </span>
                      </div>
                      <p className="text-xs text-muted-foreground leading-snug">
                        {isHi ? it.desc_hi : it.desc_en}
                      </p>
                      <p className="text-[10px] text-muted-foreground/80 mt-1.5">
                        {isHi ? 'ग्रह:' : 'Planets:'} {it.focus_planets.join(', ')} ·{' '}
                        {isHi ? 'भाव:' : 'Houses:'} {it.focus_houses.join(', ')}
                      </p>
                    </button>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Step 2 — Loading */}
          {step === 'loading' && (
            <div className="flex flex-col items-center justify-center py-20">
              <Loader2 className="w-10 h-10 animate-spin text-sacred-gold mb-3" />
              <p className="text-sm text-foreground">
                {isHi ? 'आपकी कुंडली का विश्लेषण हो रहा है...' : 'Analysing your chart...'}
              </p>
              <p className="text-xs text-muted-foreground mt-1">
                {isHi ? 'ग्रहों की दशा, भाव, और दुर्बलताएँ जाँच रहे हैं।' : 'Checking planets, houses, and afflictions.'}
              </p>
            </div>
          )}

          {/* Step 3 — Results */}
          {step === 'result' && result && (
            <div>
              <div className="mb-4 flex items-center flex-wrap gap-2">
                <button
                  type="button"
                  onClick={() => setStep('pick')}
                  className="inline-flex items-center gap-1 text-xs px-3 py-1.5 rounded-full border border-sacred-gold/30 text-sacred-gold hover:bg-sacred-gold/10"
                >
                  <ArrowLeft className="w-3.5 h-3.5" />
                  {isHi ? 'दूसरा इरादा चुनें' : 'Switch intent'}
                </button>
                <span className="text-sm text-foreground">
                  {isHi ? 'इरादा:' : 'Intent:'}{' '}
                  <strong>{isHi ? result.intent_label_hi : result.intent_label_en}</strong>
                </span>
                <span className="text-xs text-muted-foreground">
                  · {isHi ? 'ग्रह' : 'planets'}: {result.focus_planets.join(', ')}
                  · {isHi ? 'भाव' : 'houses'}: {result.focus_houses.join(', ')}
                </span>
              </div>

              {/* Top 3 picks */}
              <div className="mb-6">
                <h3 className="text-sm font-bold text-sacred-gold mb-2 flex items-center gap-2">
                  <Sparkles className="w-4 h-4" />
                  {isHi ? 'शीर्ष 3 अनुशंसित उपाय' : 'Top 3 recommended remedies'}
                </h3>
                {result.top_picks.length === 0 ? (
                  <p className="text-sm text-muted-foreground">
                    {isHi ? 'कोई मिलान नहीं।' : 'No matches.'}
                  </p>
                ) : (
                  <div className="space-y-3">
                    {result.top_picks.map((r) => (
                      <RankedCard key={`top-${r.planet}-${r.lk_house}`} r={r} isHi={isHi} highlight />
                    ))}
                  </div>
                )}
              </div>

              {/* Full ranked list below */}
              {result.ranked_remedies.length > result.top_picks.length && (
                <details className="rounded-xl border border-border bg-background overflow-hidden">
                  <summary className="p-3 cursor-pointer text-sm font-semibold text-foreground hover:bg-foreground/5">
                    {isHi
                      ? `सभी ${result.ranked_remedies.length} उपाय (पुनः क्रमित)`
                      : `All ${result.ranked_remedies.length} remedies (re-ranked)`}
                  </summary>
                  <div className="p-3 space-y-3 border-t border-border">
                    {result.ranked_remedies.slice(result.top_picks.length).map((r) => (
                      <RankedCard key={`rest-${r.planet}-${r.lk_house}`} r={r} isHi={isHi} />
                    ))}
                  </div>
                </details>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
