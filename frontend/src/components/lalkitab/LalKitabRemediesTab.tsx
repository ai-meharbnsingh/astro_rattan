import { useState, useEffect } from 'react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';
import SourceBadge from './SourceBadge';
import { pickLang } from '@/components/lalkitab/safe-render';
import { AlertTriangle, HelpCircle, Lightbulb, Sparkles, Loader2, ChevronDown, ChevronUp, Clock, ShieldCheck, BadgeCheck } from 'lucide-react';

interface Props {
  kundliId: string;
}

interface EnrichedRemedy {
  planet: string;
  planet_hi: string;
  sign: string;
  lk_house: number;
  dignity: string;
  strength: number;
  has_remedy: boolean;
  urgency: 'high' | 'medium' | 'low';
  material: string;
  day: string;
  remedy_en: string;
  remedy_hi: string;
  problem_en: string;
  problem_hi: string;
  reason_en: string;
  reason_hi: string;
  how_en: string;
  how_hi: string;
  // P0 safety layer — LK 4.08 / 4.09 / 2.12 / 4.14
  savdhaniyan?: {
    precautions?: Array<{
      en?: string; hi?: string; severity?: string;
      category?: string; lk_ref?: string;
    }>;
    time_rule?: string;
    reversal_risk?: boolean;
    lk_refs?: string[];
  };
  time_rule?: string;
  reversal_risk?: boolean;
  andhe_grah_warning?: {
    kind: string;
    severity?: string;
    reasons?: string[];
    en?: string;
    hi?: string;
    lk_ref?: string;
    adjacent_to_blind?: string[];
  };
  // P1.11 — LK 1952 remedy tier (trial / remedy / good_conduct)
  classification?: 'trial' | 'remedy' | 'good_conduct' | string;
  classification_en?: string;
  classification_hi?: string;
  classification_desc_en?: string;
  classification_desc_hi?: string;
}

interface ValidatedRemedy {
  name_en: string;
  name_hi: string;
  procedure_en: string;
  procedure_hi: string;
  condition?: string;
  validated?: boolean | string;
  for_planet?: string;
}

const URGENCY_STYLES: Record<string, string> = {
  high:   'border-red-300 bg-red-50/60',
  medium: 'border-amber-200 bg-amber-50/40',
  low:    'border-border bg-card',
};

const URGENCY_BADGE: Record<string, string> = {
  high:   'bg-red-100 text-red-700 border-red-200',
  medium: 'bg-amber-100 text-amber-700 border-amber-200',
  low:    'bg-gray-100 text-gray-600 border-gray-200',
};

const DAY_COLORS: Record<string, string> = {
  Sunday: 'text-orange-600', Monday: 'text-blue-500', Tuesday: 'text-red-600',
  Wednesday: 'text-green-600', Thursday: 'text-yellow-600', Friday: 'text-pink-500',
  Saturday: 'text-gray-700',
};

// P1.11 — LK 1952 remedy-tier badge styling
const CLASSIFICATION_STYLES: Record<string, string> = {
  trial:        'bg-cyan-100 text-cyan-800 border-cyan-300',
  remedy:       'bg-sacred-gold/15 text-sacred-gold-dark border-sacred-gold/40',
  good_conduct: 'bg-violet-100 text-violet-800 border-violet-300',
};

function RemedyCard({ r, isHi }: { r: EnrichedRemedy; isHi: boolean }) {
  const [open, setOpen] = useState(r.urgency === 'high');
  const style = URGENCY_STYLES[r.urgency] ?? URGENCY_STYLES.low;
  const badge = URGENCY_BADGE[r.urgency] ?? URGENCY_BADGE.low;
  const dayColor = DAY_COLORS[r.day] ?? 'text-foreground';
  const urgencyLabel = r.urgency === 'high'
    ? (isHi ? 'अत्यावश्यक' : 'Urgent')
    : r.urgency === 'medium'
    ? (isHi ? 'सामान्य' : 'Medium')
    : (isHi ? 'वैकल्पिक' : 'Optional');

  return (
    <div className={`rounded-xl border-2 ${style} overflow-hidden`}>
      {/* Header row — always visible */}
      <button
        className="w-full flex items-center gap-3 px-4 py-3 text-left"
        onClick={() => setOpen(o => !o)}
      >
        <div className="flex-1 min-w-0">
          <div className="flex flex-wrap items-center gap-2 mb-0.5">
            <span className="font-semibold text-sm text-foreground">
              {isHi ? r.planet_hi : (typeof r.planet === 'string' ? r.planet : pickLang(r.planet, false))}
            </span>
            <span className="text-xs text-muted-foreground">
              {isHi ? `भाव ${r.lk_house}` : `H${r.lk_house}`} · {typeof r.sign === 'string' ? r.sign : pickLang(r.sign, false)}
            </span>
            {r.classification && (
              <span
                className={`text-[10px] px-2 py-0.5 rounded-full border font-semibold uppercase tracking-wide ${
                  CLASSIFICATION_STYLES[r.classification] ?? CLASSIFICATION_STYLES.remedy
                }`}
                title={isHi ? r.classification_desc_hi : r.classification_desc_en}
              >
                {isHi ? r.classification_hi : r.classification_en}
              </span>
            )}
            <span className={`ml-auto text-xs px-2 py-0.5 rounded-full border font-medium ${badge}`}>
              {urgencyLabel}
            </span>
          </div>
          {/* Problem preview — collapsed state */}
          {!open && (
            <p className="text-xs text-muted-foreground line-clamp-1 mt-0.5">
              {isHi ? r.problem_hi : r.problem_en}
            </p>
          )}
        </div>
        {open ? <ChevronUp className="w-4 h-4 text-muted-foreground shrink-0" /> : <ChevronDown className="w-4 h-4 text-muted-foreground shrink-0" />}
      </button>

      {/* Expanded body */}
      {open && (
        <div className="px-4 pb-4 space-y-3 border-t border-current/10 pt-3">

          {/* 1 — PROBLEM */}
          <div className="flex gap-2.5">
            <AlertTriangle className="w-4 h-4 text-red-500 shrink-0 mt-0.5" />
            <div>
              <p className="text-xs font-semibold text-red-600 uppercase tracking-wide mb-0.5">
                {isHi ? 'समस्या' : 'Problem'}
              </p>
              <p className="text-sm text-foreground leading-relaxed">
                {isHi ? r.problem_hi : r.problem_en}
              </p>
            </div>
          </div>

          {/* 2 — REASON */}
          <div className="flex gap-2.5">
            <HelpCircle className="w-4 h-4 text-amber-500 shrink-0 mt-0.5" />
            <div>
              <p className="text-xs font-semibold text-amber-600 uppercase tracking-wide mb-0.5">
                {isHi ? 'कारण (लाल किताब)' : 'Reason (Lal Kitab)'}
              </p>
              <p className="text-sm text-foreground leading-relaxed">
                {isHi ? r.reason_hi : r.reason_en}
              </p>
            </div>
          </div>

          {/* 2-B — ANDHE GRAH WARNING (LK 4.14) — shown BEFORE remedy */}
          {r.andhe_grah_warning && (r.andhe_grah_warning.en || r.andhe_grah_warning.hi) && (
            <div className="rounded-lg border-2 border-red-400 bg-red-50 p-3">
              <div className="flex items-start gap-2">
                <AlertTriangle className="w-5 h-5 text-red-600 shrink-0 mt-0.5" />
                <div className="flex-1">
                  <p className="text-xs font-bold text-red-700 uppercase tracking-wide mb-1">
                    {isHi ? '⚠ अंधा ग्रह चेतावनी' : '⚠ Blind Planet Warning'}
                    <span className="ml-2 text-[10px] font-normal opacity-75">
                      LK 4.14 · severity: {r.andhe_grah_warning.severity}
                    </span>
                  </p>
                  <p className="text-sm text-red-900 leading-relaxed">
                    {pickLang(r.andhe_grah_warning, isHi)}
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* 2-C — SAVDHANIYAN (LK 4.08 + 4.09) — mandatory precautions */}
          {r.savdhaniyan?.precautions && r.savdhaniyan.precautions.length > 0 && (
            <div className="rounded-lg border border-orange-300 bg-orange-50 p-3">
              <div className="flex items-start gap-2">
                <HelpCircle className="w-5 h-5 text-orange-600 shrink-0 mt-0.5" />
                <div className="flex-1">
                  <p className="text-xs font-bold text-orange-700 uppercase tracking-wide mb-1">
                    {isHi ? '🔔 सावधानियाँ (अनिवार्य)' : '🔔 Savdhaniyan — Mandatory Precautions'}
                    <span className="ml-2 text-[10px] font-normal opacity-75">
                      LK {(r.savdhaniyan.lk_refs || []).join(', ')} · time: {r.time_rule}
                      {r.reversal_risk && ' · reversal-risk'}
                    </span>
                  </p>
                  <ol className="list-decimal list-inside space-y-1 text-xs text-orange-900 leading-relaxed">
                    {r.savdhaniyan.precautions.map((p, i) => (
                      <li key={i}>
                        <span className="font-semibold uppercase text-[10px] mr-1">
                          [{p.severity || 'info'} / {p.category || '—'}]
                        </span>
                        {pickLang(p, isHi)}
                      </li>
                    ))}
                  </ol>
                  <p className="text-[10px] text-orange-700 mt-2 italic">
                    {isHi
                      ? 'लाल किताब 4.08 के अनुसार — सावधानी छूटने पर उपाय उल्टा पड़ सकता है।'
                      : 'Per LK 4.08 — omitting a precaution can silently reverse the remedy.'}
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* 3 — REMEDY */}
          <div className="flex gap-2.5">
            <Sparkles className="w-4 h-4 text-sacred-gold shrink-0 mt-0.5" />
            <div className="flex-1">
              <p className="text-xs font-semibold text-sacred-gold uppercase tracking-wide mb-0.5">
                {isHi ? 'उपाय' : 'Remedy'}
              </p>
              <p className="text-sm text-foreground leading-relaxed">
                {isHi ? r.remedy_hi : r.remedy_en}
              </p>
              <div className="flex flex-wrap gap-2 mt-2">
                {r.material && (
                  <span className="text-xs px-2 py-0.5 rounded bg-sacred-gold/10 text-sacred-gold-dark border border-sacred-gold/20">
                    {isHi ? 'सामग्री:' : 'Material:'} {r.material}
                  </span>
                )}
                {r.day && (
                  <span className={`text-xs px-2 py-0.5 rounded bg-foreground/5 border border-border font-medium ${dayColor}`}>
                    {isHi ? 'दिन:' : 'Day:'} {r.day}
                  </span>
                )}
              </div>
            </div>
          </div>

          {/* 4 — HOW IT WORKS */}
          <div className="flex gap-2.5">
            <Lightbulb className="w-4 h-4 text-blue-500 shrink-0 mt-0.5" />
            <div>
              <p className="text-xs font-semibold text-blue-600 uppercase tracking-wide mb-0.5">
                {isHi ? 'उपाय क्यों काम करता है' : 'Why it works'}
              </p>
              <p className="text-sm text-foreground/80 leading-relaxed italic">
                {isHi ? r.how_hi : r.how_en}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default function LalKitabRemediesTab({ kundliId }: Props) {
  const { t, language } = useTranslation();
  const isHi = language === 'hi';

  const [enriched, setEnriched] = useState<EnrichedRemedy[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filter, setFilter] = useState<'all' | 'urgent' | 'medium'>('all');

  const [validated, setValidated] = useState<ValidatedRemedy[]>([]);
  const [validatedLoading, setValidatedLoading] = useState(false);
  const [master, setMaster] = useState<any[]>([]);
  const [masterLoading, setMasterLoading] = useState(false);

  useEffect(() => {
    if (!kundliId) return;
    setLoading(true);
    api.get(`/api/lalkitab/remedies/enriched/${kundliId}`)
      .then((res: any) => setEnriched(Array.isArray(res?.remedies) ? res.remedies : []))
      .catch(() => setError(isHi ? 'उपाय लोड नहीं हो सके' : 'Could not load remedies'))
      .finally(() => setLoading(false));

    setValidatedLoading(true);
    api.post('/api/lalkitab/lk-validated-remedies', { kundli_id: kundliId })
      .then((res: any) => setValidated(Array.isArray(res?.remedies) ? res.remedies : []))
      .catch((err: any) => {
        console.error('Validated remedies fetch failed:', err);
        setError(isHi ? 'सत्यापित उपाय लोड नहीं हो सके' : 'Could not load validated remedies');
      })
      .finally(() => setValidatedLoading(false));

    // Raw (DB) master remedies list for planet+house matches.
    setMasterLoading(true);
    api.get(`/api/lalkitab/remedies/master/${kundliId}`)
      .then((res: any) => setMaster(Array.isArray(res?.remedies) ? res.remedies : []))
      .catch(() => { /* non-blocking */ })
      .finally(() => setMasterLoading(false));
  }, [kundliId]);

  const filtered = enriched.filter(r => {
    if (filter === 'urgent') return r.urgency === 'high' && r.has_remedy;
    if (filter === 'medium') return r.urgency === 'medium';
    return true;
  });

  const urgentCount = enriched.filter(r => r.urgency === 'high' && r.has_remedy).length;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="rounded-xl border border-sacred-gold/20 bg-card p-5">
        <div className="flex items-center gap-2 mb-1 flex-wrap">
          <Sparkles className="w-4 h-4 text-sacred-gold" />
          <h3 className="font-semibold text-sacred-gold">
            {isHi ? 'लाल किताब उपाय — समस्या · कारण · उपाय · असर' : 'Lal Kitab Remedies — Problem · Reason · Remedy · Why It Works'}
          </h3>
          <SourceBadge source="LK_CANONICAL" size="xs" />
        </div>
        <p className="text-xs text-muted-foreground">
          {isHi
            ? 'प्रत्येक ग्रह के लिए: समस्या क्या है → लाल किताब 1952 के अनुसार कारण → उपाय → उपाय क्यों काम करता है'
            : 'For each planet: what the problem is → LK 1952 reason → the remedy → why the ritual works'}
        </p>
        {urgentCount > 0 && (
          <div className="mt-2 inline-flex items-center gap-1.5 text-xs text-red-600 font-medium">
            <AlertTriangle className="w-3.5 h-3.5" />
            {isHi ? `${urgentCount} अत्यावश्यक उपाय` : `${urgentCount} urgent remedies`}
          </div>
        )}
      </div>

      {/* Filter pills */}
      <div className="flex gap-2 flex-wrap">
        {(['all', 'urgent', 'medium'] as const).map(f => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`text-xs px-3 py-1.5 rounded-full border transition-all ${
              filter === f
                ? 'bg-sacred-gold text-white border-sacred-gold font-semibold'
                : 'border-sacred-gold/30 text-muted-foreground hover:border-sacred-gold/60'
            }`}
          >
            {f === 'all' ? (isHi ? 'सभी' : 'All') : f === 'urgent' ? (isHi ? 'अत्यावश्यक' : 'Urgent') : (isHi ? 'सामान्य' : 'Medium')}
          </button>
        ))}
      </div>

      {/* Main remedy cards */}
      {loading && (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="w-6 h-6 animate-spin text-sacred-gold mr-2" />
          <span className="text-sm text-muted-foreground">{isHi ? 'उपाय लोड हो रहे हैं...' : 'Loading remedies...'}</span>
        </div>
      )}

      {error && !loading && (
        <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-red-700 text-sm">{error}</div>
      )}

      {!loading && !error && (
        <div className="space-y-3">
          {filtered.length === 0 ? (
            <p className="text-sm text-muted-foreground text-center py-8">
              {isHi ? 'इस श्रेणी में कोई उपाय नहीं।' : 'No remedies in this category.'}
            </p>
          ) : (
            filtered.map((r) => <RemedyCard key={`${r.planet}-${r.lk_house}`} r={r} isHi={isHi} />)
          )}
        </div>
      )}

      {/* Validated Remedies section */}
      {(validatedLoading || validated.length > 0) && (
        <div className="pt-4 border-t border-sacred-gold/20">
          <div className="flex items-center gap-2 mb-3 flex-wrap">
            <BadgeCheck className="w-4 h-4 text-green-600" />
            <h3 className="font-semibold text-sacred-gold text-sm">
              {isHi ? 'सत्यापित उपाय (लाल किताब नियमों से)' : 'Validated Remedies (verified against LK rules)'}
            </h3>
            <SourceBadge source="LK_DERIVED" size="xs" />
          </div>

          {validatedLoading && (
            <div className="flex items-center gap-2 py-4">
              <Loader2 className="w-4 h-4 animate-spin text-sacred-gold" />
              <span className="text-xs text-muted-foreground">{isHi ? 'लोड हो रहा है...' : 'Loading...'}</span>
            </div>
          )}

          {!validatedLoading && validated.length > 0 && (
            <div className="space-y-3">
              {validated.map((r, idx) => {
                const isFullyValidated = r.validated === true || r.validated === 'full';
                return (
                  <div key={idx} className="rounded-xl border border-green-200/60 bg-green-500/5 p-4">
                    <div className="flex flex-wrap items-center gap-2 mb-2">
                      <span className="text-sm font-semibold text-foreground">
                        {isHi ? r.name_hi : r.name_en}
                      </span>
                      {r.for_planet && (
                        <span className="px-2 py-0.5 rounded-full bg-sacred-gold/15 text-sacred-gold-dark text-xs font-semibold">
                          {r.for_planet}
                        </span>
                      )}
                      <span className={`ml-auto flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-bold ${
                        isFullyValidated ? 'bg-green-200 text-green-800 border border-green-300' : 'bg-amber-200 text-amber-800 border border-amber-300'
                      }`}>
                        <ShieldCheck className="w-3 h-3" />
                        {isFullyValidated ? (isHi ? 'सत्यापित' : 'Validated') : (isHi ? 'आंशिक' : 'Partial')}
                      </span>
                    </div>
                    <p className="text-sm text-foreground leading-relaxed">
                      {isHi ? r.procedure_hi : r.procedure_en}
                    </p>
                    {r.condition && (
                      <p className="mt-1.5 text-xs text-foreground/60 italic">
                        <span className="font-semibold">{isHi ? 'शर्त:' : 'Condition:'}</span> {r.condition}
                      </p>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </div>
      )}

      {/* Master Remedies (raw DB) */}
      {(masterLoading || master.length > 0) && (
        <div className="pt-4 border-t border-sacred-gold/20">
          <div className="flex items-center gap-2 mb-3 flex-wrap">
            <BadgeCheck className="w-4 h-4 text-sacred-gold" />
            <h3 className="font-semibold text-sacred-gold text-sm">
              {isHi ? 'मास्टर उपाय (डेटाबेस)' : 'Master Remedies (database)'}
            </h3>
            <SourceBadge source="LK_CANONICAL" size="xs" />
          </div>

          {masterLoading && (
            <div className="flex items-center gap-2 py-4">
              <Loader2 className="w-4 h-4 animate-spin text-sacred-gold" />
              <span className="text-xs text-muted-foreground">{isHi ? 'लोड हो रहा है...' : 'Loading...'}</span>
            </div>
          )}

          {!masterLoading && master.length > 0 && (
            <div className="space-y-2">
              {master.slice(0, 80).map((r: any, idx: number) => (
                <div key={idx} className="rounded-xl border border-border/40 bg-card p-4">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="text-sm font-semibold text-foreground">
                      {r.planet} · {isHi ? `भाव ${r.house}` : `H${r.house}`}
                    </span>
                    {r.remedy_type && (
                      <span className="text-[10px] px-2 py-0.5 rounded-full border border-border/40 text-muted-foreground">
                        {r.remedy_type}
                      </span>
                    )}
                    {r.duration_days != null && !isNaN(Number(r.duration_days)) && (
                      <span className="ml-auto text-[10px] px-2 py-0.5 rounded-full border border-border/40 text-muted-foreground">
                        {isHi ? 'दिन' : 'Days'}: {r.duration_days}
                      </span>
                    )}
                  </div>
                  {r.remedy_text && (
                    <p className="text-sm text-foreground/80 mt-2 leading-relaxed">
                      {r.remedy_text}
                    </p>
                  )}
                  {(r.instructions || r.caution) && (
                    <div className="mt-2 text-xs text-muted-foreground space-y-1">
                      {r.instructions && <div>{isHi ? 'निर्देश' : 'Instructions'}: {r.instructions}</div>}
                      {r.caution && <div>{isHi ? 'सावधानी' : 'Caution'}: {r.caution}</div>}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
