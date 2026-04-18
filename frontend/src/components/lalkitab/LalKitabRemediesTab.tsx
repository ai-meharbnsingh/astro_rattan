import { useState, useEffect } from 'react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';
import SourceBadge from './SourceBadge';
import { pickLang } from '@/components/lalkitab/safe-render';
import { AlertTriangle, HelpCircle, Lightbulb, Sparkles, Loader2, ChevronDown, ChevronUp, Clock, ShieldCheck, BadgeCheck, Calendar, Compass, Palette, Gem, Wand2 } from 'lucide-react';
// P2.4 — Remedy Wizard (intent → ranked remedies)
import LalKitabRemedyWizardModal from './LalKitabRemedyWizardModal';

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
    // P2.10 — tithi timing sub-bundle (LK_DERIVED)
    tithi_timing?: {
      preferred_paksha?: 'shukla' | 'krishna' | 'either';
      preferred_tithis?: number[];
      forbidden_tithis?: number[];
      forbidden_tithis_detail?: Array<{
        tithi: number; paksha?: string;
        reason_en?: string; reason_hi?: string;
      }>;
      peak_tithi?: number | null;
      peak_tithi_paksha?: string | null;
      peak_tithi_en?: string;
      peak_tithi_hi?: string;
      reason_en?: string;
      reason_hi?: string;
      lk_ref?: string;
      source?: string;
    };
  };
  // P2.11 — direction/colour/material matrix (LK_CANONICAL)
  remedy_matrix?: {
    direction?: { en?: string; hi?: string; bearing_deg?: number | null };
    colour?: {
      primary_en?: string; primary_hi?: string; hex?: string;
      alt_en?: string[]; alt_hi?: string[];
    };
    material?: {
      primary_en?: string; primary_hi?: string;
      alt?: string[]; alt_hi?: string[];
    };
    lk_ref?: string;
    source?: string;
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

                  {/* P2.10 — TITHI TIMING sub-section */}
                  {r.savdhaniyan?.tithi_timing && (r.savdhaniyan.tithi_timing.peak_tithi_en || r.savdhaniyan.tithi_timing.peak_tithi_hi) && (
                    <div className="mt-3 pt-3 border-t border-orange-300/60">
                      <div className="flex items-start gap-2">
                        <Calendar className="w-4 h-4 text-orange-700 shrink-0 mt-0.5" />
                        <div className="flex-1 min-w-0">
                          <p className="text-[11px] font-bold text-orange-800 uppercase tracking-wide mb-1">
                            {isHi ? 'तिथि समय (सर्वोत्तम)' : 'Tithi Timing (Optimal Lunar Day)'}
                            <span className="ml-2 text-[10px] font-normal opacity-75">
                              LK {r.savdhaniyan.tithi_timing.lk_ref || '4.16'} · {r.savdhaniyan.tithi_timing.source || 'LK_DERIVED'}
                            </span>
                          </p>
                          <p className="text-xs text-orange-900 leading-relaxed">
                            <span className="font-semibold">
                              {isHi ? 'चरम तिथि: ' : 'Peak tithi: '}
                            </span>
                            {isHi
                              ? (r.savdhaniyan.tithi_timing.peak_tithi_hi || r.savdhaniyan.tithi_timing.peak_tithi_en)
                              : (r.savdhaniyan.tithi_timing.peak_tithi_en || r.savdhaniyan.tithi_timing.peak_tithi_hi)}
                          </p>
                          {(r.savdhaniyan.tithi_timing.reason_en || r.savdhaniyan.tithi_timing.reason_hi) && (
                            <p className="text-[11px] text-orange-800/80 leading-relaxed mt-1 italic">
                              {isHi ? r.savdhaniyan.tithi_timing.reason_hi : r.savdhaniyan.tithi_timing.reason_en}
                            </p>
                          )}
                          {r.savdhaniyan.tithi_timing.forbidden_tithis && r.savdhaniyan.tithi_timing.forbidden_tithis.length > 0 && (
                            <p className="text-[11px] text-red-700 mt-1">
                              <span className="font-semibold">
                                {isHi ? 'वर्जित तिथियाँ: ' : 'Avoid: '}
                              </span>
                              {r.savdhaniyan.tithi_timing.forbidden_tithis.join(', ')}
                            </p>
                          )}
                        </div>
                      </div>
                    </div>
                  )}
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

              {/* P2.11 — Direction · Colour · Material chip row */}
              {r.remedy_matrix && (r.remedy_matrix.direction?.en || r.remedy_matrix.colour?.primary_en || r.remedy_matrix.material?.primary_en) && (
                <div className="flex flex-wrap gap-2 mt-2">
                  {r.remedy_matrix.direction?.en && (
                    <span
                      className="inline-flex items-center gap-1 text-[11px] px-2 py-0.5 rounded-full bg-sky-50 border border-sky-200 text-sky-800"
                      title={isHi
                        ? `दिशा ${r.remedy_matrix.direction.bearing_deg ?? ''}°`
                        : `Bearing ${r.remedy_matrix.direction.bearing_deg ?? ''}°`}
                    >
                      <Compass className="w-3 h-3" />
                      {isHi ? 'दिशा:' : 'Direction:'}{' '}
                      <span className="font-semibold">
                        {isHi ? r.remedy_matrix.direction.hi : r.remedy_matrix.direction.en}
                      </span>
                    </span>
                  )}
                  {r.remedy_matrix.colour?.primary_en && (
                    <span className="inline-flex items-center gap-1 text-[11px] px-2 py-0.5 rounded-full bg-rose-50 border border-rose-200 text-rose-800">
                      <Palette className="w-3 h-3" />
                      {isHi ? 'रंग:' : 'Colour:'}{' '}
                      {r.remedy_matrix.colour.hex && (
                        <span
                          className="inline-block w-2.5 h-2.5 rounded-full border border-black/10"
                          style={{ backgroundColor: r.remedy_matrix.colour.hex }}
                          aria-hidden
                        />
                      )}
                      <span className="font-semibold">
                        {isHi ? r.remedy_matrix.colour.primary_hi : r.remedy_matrix.colour.primary_en}
                      </span>
                    </span>
                  )}
                  {r.remedy_matrix.material?.primary_en && (
                    <span className="inline-flex items-center gap-1 text-[11px] px-2 py-0.5 rounded-full bg-amber-50 border border-amber-200 text-amber-800">
                      <Gem className="w-3 h-3" />
                      {isHi ? 'धातु:' : 'Material:'}{' '}
                      <span className="font-semibold">
                        {isHi ? r.remedy_matrix.material.primary_hi : r.remedy_matrix.material.primary_en}
                      </span>
                    </span>
                  )}
                </div>
              )}
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
  const [abhimantritItems, setAbhimantritItems] = useState<Record<string, any> | null>(null);
  // P2.4 — Remedy Wizard modal
  const [wizardOpen, setWizardOpen] = useState(false);

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

    // LK 4.20 — Abhimantrit specialty items catalogue
    api.get(`/api/lalkitab/remedies/abhimantrit?kundli_id=${kundliId}`)
      .then((res: any) => setAbhimantritItems(res?.items ?? null))
      .catch(() => { /* non-blocking */ });
  }, [kundliId]);

  const filtered = enriched.filter(r => {
    if (filter === 'urgent') return r.urgency === 'high' && r.has_remedy;
    if (filter === 'medium') return r.urgency === 'medium';
    return true;
  });

  const urgentCount = enriched.filter(r => r.urgency === 'high' && r.has_remedy).length;

  // LK 4.12 — Remedy Conflict Detection
  const detectConflicts = () => {
    const conflicts: Array<{ planets: string[]; reason_en: string; reason_hi: string; severity: 'high' | 'medium' }> = [];
    const activeRemedies = enriched.filter(r => r.has_remedy);

    // Check for same-day conflicts (multiple remedies on the same day might be hard to execute)
    const dayCount: Record<string, EnrichedRemedy[]> = {};
    activeRemedies.forEach(r => {
      if (r.day && r.day !== '') {
        if (!dayCount[r.day]) dayCount[r.day] = [];
        dayCount[r.day].push(r);
      }
    });

    Object.entries(dayCount).forEach(([day, planets]) => {
      if (planets.length > 2) {
        conflicts.push({
          planets: planets.map(p => p.planet),
          reason_en: `${planets.length} remedies scheduled for ${day} — may be difficult to execute together. Consider spacing them out.`,
          reason_hi: `${day} के लिए ${planets.length} उपाय — एक साथ करना मुश्किल हो सकता है। उन्हें अलग-अलग समय पर करने पर विचार करें।`,
          severity: 'medium',
        });
      }
    });

    // Check for opposite material/action keywords (feed vs avoid, speak vs silence, etc.)
    const opposites: Record<string, string[]> = {
      'feed': ['avoid feeding', 'do not feed', 'refrain from feeding'],
      'speak': ['avoid speaking', 'do not speak', 'silence'],
      'donate': ['refuse donation', 'avoid donating'],
      'wear': ['remove', 'not wear', 'avoid wearing'],
    };

    for (const [keyword, oppositeList] of Object.entries(opposites)) {
      const withKeyword = activeRemedies.filter(r =>
        r.remedy_en.toLowerCase().includes(keyword) ||
        r.remedy_hi?.toLowerCase().includes(keyword.replace(/[a-z]/g, '') || '')
      );
      const withOpposite = activeRemedies.filter(r =>
        oppositeList.some(opp => r.remedy_en.toLowerCase().includes(opp.toLowerCase()))
      );

      const conflictingPairs = withKeyword.filter(k =>
        withOpposite.some(o => o.planet !== k.planet)
      );

      if (conflictingPairs.length > 0 && withOpposite.length > 0) {
        conflicts.push({
          planets: [...new Set([...withKeyword.map(p => p.planet), ...withOpposite.map(p => p.planet)])],
          reason_en: `Conflicting action instructions: some remedies ask to "${keyword}" while others ask to avoid it.`,
          reason_hi: `विरोधाभासी निर्देश: कुछ उपाय "${keyword}" करने को कहते हैं जबकि अन्य इससे बचने को कहते हैं।`,
          severity: 'high',
        });
      }
    }

    return conflicts;
  };

  const conflicts = detectConflicts();

  return (
    <div className="space-y-6">
      {/* P2.4 — Remedy Wizard CTA: "Don't know where to start?" */}
      <div className="rounded-xl border-2 border-sacred-gold/40 bg-gradient-to-br from-sacred-gold/10 to-amber-500/5 p-4 flex items-center gap-4 flex-wrap">
        <div className="flex-1 min-w-0">
          <p className="text-sm font-bold text-sacred-gold-dark flex items-center gap-2 mb-1">
            <Wand2 className="w-4 h-4" />
            {isHi ? 'किस उपाय से शुरू करें?' : "Don't know which remedy to start with?"}
          </p>
          <p className="text-xs text-foreground/70">
            {isHi
              ? 'अपनी मंशा बताएँ — विज़र्ड आपकी कुंडली के अनुसार शीर्ष 3 उपाय सुझाएगा।'
              : 'Tell us your intent — the wizard will rank the top 3 remedies for your chart.'}
          </p>
        </div>
        <button
          onClick={() => setWizardOpen(true)}
          className="px-4 py-2 rounded-lg bg-sacred-gold text-white font-semibold text-sm hover:bg-sacred-gold-dark transition-colors flex items-center gap-1.5 shadow-sm"
        >
          <Wand2 className="w-4 h-4" />
          {isHi ? 'विज़र्ड खोलें' : 'Open Wizard'}
        </button>
      </div>
      <LalKitabRemedyWizardModal
        kundliId={kundliId}
        isHi={isHi}
        open={wizardOpen}
        onClose={() => setWizardOpen(false)}
      />

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

      {/* LK 4.12 — Remedy Conflict Detection */}
      {conflicts.length > 0 && (
        <div className="rounded-xl border-2 border-orange-300 bg-orange-50/80 p-4 space-y-3">
          <div className="flex items-start gap-3">
            <AlertTriangle className="w-5 h-5 text-orange-700 shrink-0 mt-0.5" />
            <div className="flex-1">
              <h4 className="font-semibold text-orange-800 text-sm flex items-center gap-2 mb-2">
                {isHi ? '⚠ उपायों में टकराव' : '⚠ Remedy Conflicts Detected'}
                <span className="text-xs px-2 py-0.5 rounded-full bg-orange-100 border border-orange-300 text-orange-700 font-medium">
                  {conflicts.length} {isHi ? 'मुद्दे' : 'issues'}
                </span>
              </h4>
              <div className="space-y-2">
                {conflicts.map((conflict, idx) => {
                  const isHighSeverity = conflict.severity === 'high';
                  return (
                    <div
                      key={idx}
                      className={`rounded-lg border p-3 ${
                        isHighSeverity
                          ? 'border-red-300/60 bg-red-50/60'
                          : 'border-amber-200/60 bg-amber-50/40'
                      }`}
                    >
                      <div className="flex items-start gap-2 mb-1.5">
                        <span className={`text-xs font-bold uppercase ${isHighSeverity ? 'text-red-700' : 'text-amber-700'}`}>
                          {isHighSeverity ? '🔴 Critical' : '🟡 Warning'}
                        </span>
                        <span className="text-xs text-foreground/60">
                          {conflict.planets.join(', ')}
                        </span>
                      </div>
                      <p className={`text-sm leading-relaxed ${isHighSeverity ? 'text-red-900' : 'text-amber-900'}`}>
                        {isHi ? conflict.reason_hi : conflict.reason_en}
                      </p>
                    </div>
                  );
                })}
              </div>
              <p className="text-xs text-orange-700/80 mt-3 italic">
                {isHi
                  ? 'सुझाव: आप उपायों को अलग-अलग समय पर करने पर विचार कर सकते हैं या किसी पारंपरिक ज्योतिषी से सलाह ले सकते हैं।'
                  : 'Suggestion: Consider spacing out the remedies or consult a traditional astrologer for guidance.'}
              </p>
            </div>
          </div>
        </div>
      )}

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

          {/* LK 4.20 — Abhimantrit Items */}
          {abhimantritItems && Object.keys(abhimantritItems).length > 0 && (
            <div className="mt-4 pt-4 border-t border-border space-y-3">
              <h4 className="text-sm font-semibold text-foreground flex items-center gap-2">
                <Gem className="w-4 h-4 text-sacred-gold-dark shrink-0" />
                {isHi ? 'अभिमंत्रित वस्तुएं' : 'Abhimantrit Items'}
                <span className="text-[10px] px-2 py-0.5 rounded-full border border-sacred-gold/40 bg-sacred-gold/10 text-sacred-gold-dark font-medium ml-1">
                  {isHi ? 'प्रीमियम' : 'Specialty'}
                </span>
              </h4>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {Object.entries(abhimantritItems).map(([key, item]: [string, any]) => (
                  <div key={key} className="rounded-lg border border-sacred-gold/30 bg-sacred-gold/5 p-3 space-y-1.5">
                    <div className="flex items-start justify-between gap-2">
                      <p className="font-semibold text-sm text-foreground">
                        {isHi ? item.name_hi : item.name_en}
                      </p>
                      {item.cost_tier && (
                        <span className="text-[10px] px-1.5 py-0.5 rounded border border-border/50 text-muted-foreground shrink-0">
                          {item.cost_tier}
                        </span>
                      )}
                    </div>
                    <p className="text-xs text-muted-foreground">{item.material}</p>
                    {item.wear_method && (
                      <p className="text-xs text-foreground/70">{isHi ? 'धारण विधि' : 'Wear'}: {item.wear_method}</p>
                    )}
                    {item.planet_association && (
                      <p className="text-xs text-foreground/70">{isHi ? 'ग्रह' : 'Planet'}: {item.planet_association}</p>
                    )}
                    {item.ritual_required && (
                      <p className="text-xs text-amber-700 font-medium">{isHi ? '⚑ अभिमंत्रण आवश्यक' : '⚑ Ritual required'}</p>
                    )}
                    {Array.isArray(item.benefits) && item.benefits.length > 0 && (
                      <p className="text-xs text-muted-foreground">{item.benefits.join(' · ')}</p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
