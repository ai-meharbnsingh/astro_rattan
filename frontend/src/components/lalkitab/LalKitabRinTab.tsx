import { useState, useEffect } from 'react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';
import { Scale, AlertCircle, CheckCircle2, Loader2, ArrowUpCircle, Ban, Layers } from 'lucide-react';
import { pickLang } from './safe-render';
import SourceBadge from './SourceBadge';

interface Props {
  kundliId: string;
}

interface Debt {
  id: string;
  debt_type: string;
  planet: string;
  description: string;
  indication: string;
  remedy: string;
  active: boolean;
  activation_status?: 'active' | 'latent' | 'passive';
  activation_house?: number;
  activation_urgency?: 'high' | 'medium' | 'low';
  // P1.10 — dasha-aware activation overlay
  activating_planet?: string | null;
  dasha_active?: boolean;
  dasha_upgrade?: boolean;
  dasha_context?: { en?: string; hi?: string } | null;
  next_activation_window?: {
    planet?: string;
    age?: number;
    year?: number;
    en?: string;
    hi?: string;
  } | null;
  // P2.9 — compound debt priority overlay
  priority_rank?: number;
  priority_score?: number;
  priority_boosts?: Array<{ kind: string; delta: number; reason_en?: string; reason_hi?: string }>;
  canon_name?: string;
  cluster_activator?: string;
  cluster_size?: number;
  blocked_by?: string;
  blocked_reason?: { en?: string; hi?: string };
}

interface CompoundCluster {
  activator: string;
  debts: string[];
  member_count: number;
  combined_score: number;
  note_en: string;
  note_hi: string;
}

interface CompoundBlock {
  blocker: string;
  blocks: string[];
  reason_en: string;
  reason_hi: string;
}

interface CompoundAnalysis {
  ranked: Debt[];
  clusters: CompoundCluster[];
  blocked_relationships: CompoundBlock[];
  recommended_order_en: string;
  recommended_order_hi: string;
  source: string;
}

const PLANET_HI: Record<string, string> = {
  sun: 'सूर्य', moon: 'चंद्र', mars: 'मंगल', mercury: 'बुध',
  jupiter: 'गुरु', venus: 'शुक्र', saturn: 'शनि', rahu: 'राहु', ketu: 'केतु',
};

// English translations for the debt types (DB data is Hindi-only).
// P1.7–P1.9 appends 4 new Rin types (Deva / Rishi / Nri / Bhoot) — the
// Hindi key 'देव ऋण' is shared with the legacy Dev Rin entry; the
// updated copy reflects the expanded Deva Rin canon.
const DEBT_EN: Record<string, { type: string; description: string; indication: string; remedy: string }> = {
  'पितृ ऋण':      { type: "Pitru Rin (Father's Debt)",          description: 'Karmic debt related to father or ancestors',          indication: 'Sun afflicted, conflict with father, eye problems',           remedy: 'Keep Gangajal in a copper vessel, seek father\'s blessings' },
  'मातृ ऋण':      { type: "Matru Rin (Mother's Debt)",           description: 'Karmic debt related to mother',                       indication: 'Moon afflicted, conflict with mother, mental stress',          remedy: 'Keep a square piece of silver, serve and care for mother' },
  'भ्रातृ ऋण':    { type: "Bhratu Rin (Sibling's Debt)",         description: 'Karmic debt related to brothers and sisters',         indication: 'Mars afflicted, disputes with brothers, blood ailments',      remedy: 'Donate red lentils (masoor dal), respect siblings' },
  'देव ऋण':       { type: "Deva Rin (Divine / Guru's Debt)",     description: 'Past-life obligation to a spiritual teacher, divine blessing, or the dharmic path', indication: "Spiritual blockage, guru disputes, children's education stalls", remedy: 'Donate yellow clothes on Thursdays, feed Brahmins, worship the Peepal tree' },
  'स्त्री ऋण':   { type: "Stri Rin (Women's Debt)",             description: 'Karmic debt related to women',                        indication: 'Venus afflicted, marital problems',                           remedy: 'Serve a cow, respect and honour your wife' },
  'शत्रु ऋण':    { type: "Shatru Rin (Enemy's Debt)",           description: 'Karmic debt related to enemies or past actions',      indication: 'Saturn afflicted, delayed success, physical pain',            remedy: 'Donate oil on Saturdays, feed roti to a black dog' },
  'पितामह ऋण':   { type: "Pitamah Rin (Grandfather's Debt)",    description: 'Karmic debt to ancestors or maternal grandfather',    indication: 'Rahu afflicted, hidden enemies, addiction tendencies',        remedy: 'Drop 400g lead into flowing water, respect maternal grandfather' },
  'प्रपितामह ऋण':{ type: "Prapitamah Rin (Great-Grandfather's Debt)", description: 'Karmic debt to great-grandparents or ancestors', indication: 'Ketu afflicted, spiritual confusion, fear of untimely events', remedy: 'Feed jaggery to monkeys, apply saffron tilak' },
  // P1.8 — Rishi Rin (sage-tradition / knowledge debt)
  'ऋषि ऋण':     { type: "Rishi Rin (Sage-Tradition Debt)",      description: 'Debt of disconnection from the sage tradition and ancestral wisdom', indication: 'Learning blockages, ancestral wisdom disconnect, publishing / research stalls', remedy: 'Donate books, practise silent reading at dawn, wear green on Wednesdays' },
  // P1.9a — Nri Rin (humanity / service debt)
  'नृ ऋण':       { type: "Nri Rin (Humanity / Service Debt)",    description: 'Karmic debt of service owed to unknown people and humanity at large', indication: 'Public-service obstacles, loneliness in a crowd, karmic relationships with unknown people', remedy: 'Feed 7 beggars on Saturdays, donate to strangers, volunteer silently' },
  // P1.9b — Bhoot Rin (elemental / ancestral-element debt)
  'भूत ऋण':     { type: "Bhoot Rin (Elemental / Ancestral-Element Debt)", description: 'Unresolved debt linked to the five elements or the souls of departed ancestors', indication: 'Unexplained anxiety, ancestral-home disputes, water / fire accidents', remedy: "Offer Ganga jal to the Peepal tree, keep a black-and-white cloth in the home's NE corner, immerse 400 g of lead in flowing water" },
};

const PLANET_COLOR: Record<string, string> = {
  sun:     'bg-orange-400/15 text-orange-700',
  moon:    'bg-blue-400/15 text-blue-700',
  mars:    'bg-red-400/15 text-red-700',
  mercury: 'bg-green-400/15 text-green-700',
  jupiter: 'bg-yellow-400/15 text-yellow-700',
  venus:   'bg-pink-400/15 text-pink-700',
  saturn:  'bg-gray-400/15 text-gray-700',
  rahu:    'bg-purple-400/15 text-purple-700',
  ketu:    'bg-indigo-400/15 text-indigo-700',
};

export default function LalKitabRinTab({ kundliId }: Props) {
  const { t, language } = useTranslation();
  const isHi = language === 'hi';

  const [debts, setDebts] = useState<Debt[]>([]);
  const [afflicted, setAfflicted] = useState<string[]>([]);
  const [compound, setCompound] = useState<CompoundAnalysis | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!kundliId) {
      setDebts([]);
      setAfflicted([]);
      setCompound(null);
      setError('');
      return;
    }
    setLoading(true);
    setError('');
    api.get(`/api/lalkitab/rin-active/${kundliId}`)
      .then((res: any) => {
        setDebts(Array.isArray(res?.debts) ? res.debts : []);
        setAfflicted(Array.isArray(res?.afflicted_planets) ? res.afflicted_planets : []);
        setCompound(res?.compound_analysis || null);
      })
      .catch(() => setError(t('auto.failedToLoadDebtData')))
      .finally(() => setLoading(false));
  }, [kundliId, isHi]);

  const activeDebts = debts.filter((d) => d.active);
  const inactiveDebts = debts.filter((d) => !d.active);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-xl font-sans font-semibold text-sacred-gold flex items-center gap-2 mb-1">
          <Scale className="w-5 h-5" />
          {t('auto.lalKitabRinKarmicDeb')}
        </h2>
        <p className="text-sm text-gray-500">
          {t('auto.pastLifeKarmicDebtsT')}
        </p>
      </div>

      {/* Afflicted planets notice */}
      {!loading && afflicted.length > 0 && (
        <div className="flex items-start gap-3 p-4 rounded-xl border border-red-300/30 bg-red-500/5">
          <AlertCircle className="w-4 h-4 text-red-500 mt-0.5 shrink-0" />
          <div>
            <p className="text-sm font-semibold text-red-700 mb-1">
              {t('auto.afflictedPlanetsIn6t')}
            </p>
            <div className="flex flex-wrap gap-2">
              {afflicted.filter(Boolean).map((raw: any, idx: number) => {
                const p = String(raw || '').toLowerCase();
                const label = p ? (p.charAt(0).toUpperCase() + p.slice(1)) : '';
                return (
                  <span key={`${p || 'p'}-${idx}`} className={`px-2.5 py-0.5 rounded-full text-xs font-semibold ${PLANET_COLOR[p] ?? 'bg-gray-100 text-gray-600'}`}>
                    {isHi ? (PLANET_HI[p] ?? p) : label}
                  </span>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* Summary */}
      {!loading && debts.length > 0 && (
        <div className="flex gap-3">
          <div className="flex-1 p-3 rounded-xl bg-red-500/8 border border-red-300/20 text-center">
            <p className="text-2xl font-bold text-red-600">{activeDebts.length}</p>
            <p className="text-xs text-gray-500 mt-0.5">{t('auto.activeDebts')}</p>
          </div>
          <div className="flex-1 p-3 rounded-xl bg-green-500/8 border border-green-300/20 text-center">
            <p className="text-2xl font-bold text-green-600">{inactiveDebts.length}</p>
            <p className="text-xs text-gray-500 mt-0.5">{t('auto.inactiveDebts')}</p>
          </div>
          <div className="flex-1 p-3 rounded-xl bg-sacred-gold/8 border border-sacred-gold/20 text-center">
            <p className="text-2xl font-bold text-sacred-gold">{debts.length}</p>
            <p className="text-xs text-gray-500 mt-0.5">{t('auto.totalDebts')}</p>
          </div>
        </div>
      )}

      {/* P2.9 — Compound Priority Analysis */}
      {!loading && compound && Array.isArray(compound.ranked) && compound.ranked.length > 0 && (
        <CompoundPrioritySection compound={compound} isHi={isHi} />
      )}

      {/* Loading */}
      {loading && (
        <div className="flex items-center justify-center py-16">
          <Loader2 className="w-8 h-8 animate-spin text-sacred-gold" />
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="p-4 rounded-xl bg-red-50 border border-red-200 text-red-700 text-sm">
          {error}
        </div>
      )}

      {/* Active Debts */}
      {!loading && activeDebts.length > 0 && (
        <div>
          <h3 className="font-sans font-semibold text-red-700 mb-3 flex items-center gap-2">
            <AlertCircle className="w-4 h-4" />
            {t('auto.activeDebtsRemediesR')}
          </h3>
          <div className="space-y-4">
            {activeDebts.map((debt) => (
              <DebtCard key={debt.id} debt={debt} isHi={isHi} />
            ))}
          </div>
        </div>
      )}

      {/* Inactive Debts */}
      {!loading && inactiveDebts.length > 0 && (
        <div>
          <h3 className="font-sans font-semibold text-green-700 mb-3 flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4" />
            {t('auto.inactiveDebtsNotCurr')}
          </h3>
          <div className="space-y-3">
            {inactiveDebts.map((debt) => (
              <DebtCard key={debt.id} debt={debt} isHi={isHi} />
            ))}
          </div>
        </div>
      )}

      {!loading && !error && debts.length === 0 && (
        <div className="text-center py-12 text-gray-400 text-sm">
          {t('auto.noDebtDataAvailable')}
        </div>
      )}
    </div>
  );
}

function DebtCard({ debt, isHi }: { debt: Debt; isHi: boolean }) {
  const { t } = useTranslation();
  const planetKey = String((debt as any)?.planet || '').toLowerCase();
  const PLANET_COLOR: Record<string, string> = {
    sun: 'bg-orange-400/15 text-orange-700', moon: 'bg-blue-400/15 text-blue-700',
    mars: 'bg-red-400/15 text-red-700', mercury: 'bg-green-400/15 text-green-700',
    jupiter: 'bg-yellow-400/15 text-yellow-700', venus: 'bg-pink-400/15 text-pink-700',
    saturn: 'bg-gray-400/15 text-gray-700', rahu: 'bg-purple-400/15 text-purple-700',
    ketu: 'bg-indigo-400/15 text-indigo-700',
  };
  const PLANET_HI: Record<string, string> = {
    sun: 'सूर्य', moon: 'चंद्र', mars: 'मंगल', mercury: 'बुध',
    jupiter: 'गुरु', venus: 'शुक्र', saturn: 'शनि', rahu: 'राहु', ketu: 'केतु',
  };

  return (
    <div
      className={`card-sacred rounded-xl border p-4 ${
        debt.active
          ? 'border-red-300/40 bg-red-500/5'
          : 'border-gray-200/50 bg-white/20'
      }`}
    >
      {/* Title row */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2 flex-wrap">
          <h4 className="font-sans font-semibold text-foreground">{pickLang((debt as any).debt_type ?? (debt as any).type ?? (debt as any).name, isHi)}</h4>
          <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${PLANET_COLOR[planetKey] ?? 'bg-gray-100 text-gray-600'}`}>
            {isHi
              ? (PLANET_HI[planetKey] ?? (debt.planet || ''))
              : (planetKey ? planetKey.charAt(0).toUpperCase() + planetKey.slice(1) : (isHi ? '' : ''))}
          </span>
          {/* Activation status badge */}
          {debt.activation_status === 'active' && (
            <span className="flex items-center gap-1 px-2 py-0.5 rounded-full bg-red-500/10 text-red-700 text-xs font-bold border border-red-300/40">
              {debt.activation_urgency === 'high' && (
                <span className="w-1.5 h-1.5 rounded-full bg-red-600 animate-pulse shrink-0" />
              )}
              {isHi ? 'सक्रिय' : 'ACTIVE'}
            </span>
          )}
          {debt.activation_status === 'latent' && (
            <span className="flex items-center gap-1 px-2 py-0.5 rounded-full bg-yellow-400/10 text-yellow-700 text-xs font-bold border border-yellow-300/40">
              {debt.activation_urgency === 'high' && (
                <span className="w-1.5 h-1.5 rounded-full bg-yellow-500 animate-pulse shrink-0" />
              )}
              {isHi ? 'सुप्त' : 'LATENT'}
            </span>
          )}
          {(!debt.activation_status || debt.activation_status === 'passive') && (
            <span className="flex items-center gap-1 px-2 py-0.5 rounded-full bg-gray-400/10 text-gray-500 text-xs font-bold border border-gray-300/40">
              {isHi ? 'निष्क्रिय' : 'PASSIVE'}
            </span>
          )}
          {/* P1.10 — live-now dasha indicator */}
          {debt.dasha_active && (
            <span className="flex items-center gap-1 px-2 py-0.5 rounded-full bg-orange-500/15 text-orange-700 text-xs font-bold border border-orange-400/50">
              <span className="w-1.5 h-1.5 rounded-full bg-orange-600 animate-pulse shrink-0" />
              {isHi ? 'अभी दशा में' : 'LIVE IN DASHA'}
            </span>
          )}
        </div>
        {debt.active ? (
          <span className="flex items-center gap-1 px-2 py-0.5 rounded-full bg-red-500/10 text-red-700 text-xs font-semibold border border-red-300/30 shrink-0">
            <AlertCircle className="w-3 h-3" />
            {t('auto.active')}
          </span>
        ) : (
          <span className="flex items-center gap-1 px-2 py-0.5 rounded-full bg-green-500/10 text-green-700 text-xs font-medium border border-green-300/30 shrink-0">
            <CheckCircle2 className="w-3 h-3" />
            {t('auto.inactive')}
          </span>
        )}
      </div>

      {/* Description — backend may return a string (legacy) or {hi,en} (new shape) */}
      {(() => {
        const dbtAny = debt as any;
        const debtTypeKey = typeof dbtAny.debt_type === 'string' ? dbtAny.debt_type : '';
        const descFallback = DEBT_EN[debtTypeKey]?.description;
        const descValue = dbtAny.description ?? dbtAny.manifestation;
        const descText = isHi
          ? pickLang(descValue, true)
          : (pickLang(descValue, false) || descFallback || '');
        return descText ? (
          <p className="text-sm text-foreground/80 mb-3 leading-relaxed">{descText}</p>
        ) : null;
      })()}

      {/* Indication — backend `reason` (bilingual) or legacy `indication` string */}
      {(() => {
        const dbtAny = debt as any;
        const debtTypeKey = typeof dbtAny.debt_type === 'string' ? dbtAny.debt_type : '';
        const indFallback = DEBT_EN[debtTypeKey]?.indication;
        const indValue = dbtAny.indication ?? dbtAny.reason;
        const indText = isHi
          ? pickLang(indValue, true)
          : (pickLang(indValue, false) || indFallback || '');
        return indText ? (
          <div className="mb-3 p-3 rounded-lg bg-sacred-gold/5 border border-sacred-gold/15">
            <p className="text-xs font-semibold text-sacred-gold mb-1">
              {t('auto.indication')}
            </p>
            <p className="text-xs text-foreground/70 leading-snug">{indText}</p>
          </div>
        ) : null;
      })()}

      {/* Remedy — backend `remedy` is a {hi,en} object OR a legacy string */}
      {(() => {
        const dbtAny = debt as any;
        const debtTypeKey = typeof dbtAny.debt_type === 'string' ? dbtAny.debt_type : '';
        const remFallback = DEBT_EN[debtTypeKey]?.remedy;
        const remText = isHi
          ? pickLang(dbtAny.remedy, true)
          : (pickLang(dbtAny.remedy, false) || remFallback || '');
        return remText ? (
          <div className="p-3 rounded-lg bg-green-500/5 border border-green-300/20">
            <p className="text-xs font-semibold text-green-700 mb-1">
              {t('auto.remedy')}
            </p>
            <p className="text-xs text-foreground/70 leading-snug">{remText}</p>
          </div>
        ) : null;
      })()}

      {/* P1.10 — Dasha-aware activation context. Only render when backend
          provided the overlay (older responses won't have these fields). */}
      {debt.dasha_context && (
        <div
          className={`mt-3 p-3 rounded-lg border ${
            debt.dasha_active
              ? 'bg-orange-500/8 border-orange-400/40'
              : 'bg-gray-50 border-gray-200'
          }`}
        >
          <p className={`text-xs font-bold mb-1 uppercase tracking-widest ${
            debt.dasha_active ? 'text-orange-700' : 'text-gray-500'
          }`}>
            {isHi ? 'दशा स्थिति' : 'Dasha Status'}
          </p>
          <p className="text-xs text-foreground/80 leading-snug">
            {pickLang(debt.dasha_context, isHi)}
          </p>
        </div>
      )}

      {/* P1.10 — Next activation window (if backend could predict one). */}
      {debt.next_activation_window && !debt.dasha_active && (
        <div className="mt-2 p-2.5 rounded-lg bg-sacred-gold/5 border border-sacred-gold/20">
          <p className="text-[10px] font-bold text-sacred-gold-dark uppercase tracking-widest mb-0.5">
            {isHi ? 'अगली सक्रियता' : 'Next activation'}
          </p>
          <p className="text-xs text-foreground/75 leading-snug">
            {pickLang(debt.next_activation_window, isHi)}
          </p>
        </div>
      )}

      {/* P2.9 — Blocked-by warning (canon gating, e.g. Pitru blocks Deva) */}
      {debt.blocked_by && (
        <div className="mt-2 p-2.5 rounded-lg bg-red-500/8 border border-red-400/40 flex items-start gap-2">
          <Ban className="w-3.5 h-3.5 text-red-600 mt-0.5 shrink-0" />
          <div>
            <p className="text-[10px] font-bold text-red-700 uppercase tracking-widest mb-0.5">
              {isHi ? 'पहले यह उपाय अवरुद्ध' : 'Gated by canon'}
            </p>
            <p className="text-xs text-foreground/80 leading-snug">
              {pickLang(debt.blocked_reason || { hi: `पहले ${debt.blocked_by} का उपाय करें।`, en: `Work ${debt.blocked_by} first.` }, isHi)}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

// ─────────────────────────────────────────────────────────────
// P2.9 — Compound Priority Section
// ─────────────────────────────────────────────────────────────
function CompoundPrioritySection({ compound, isHi }: { compound: CompoundAnalysis; isHi: boolean }) {
  const top3 = (compound.ranked || []).slice(0, 3);
  const rankBadges = ['1️⃣', '2️⃣', '3️⃣'];

  return (
    <div className="rounded-2xl border border-sacred-gold/30 bg-sacred-gold/5 p-5 space-y-4">
      <div>
        <h3 className="text-lg font-sans font-bold text-sacred-gold flex items-center gap-2 flex-wrap mb-1">
          <Layers className="w-5 h-5" />
          {isHi ? 'यौगिक प्राथमिकता' : 'Compound Priority'}
          <SourceBadge source="LK_DERIVED" size="xs" />
        </h3>
        <p className="text-xs text-foreground/70 leading-snug">
          {isHi
            ? 'लाल किताब ऋण-शोधन क्रम के अनुसार, एक साथ उपाय न करें — इस क्रम में करें।'
            : 'Per Lal Kitab Rina-Shodhan Krama: do not remediate all Rins at once — work them in this order.'}
        </p>
      </div>

      {/* Top 3 priority ranking */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        {top3.map((debt, i) => {
          const title = debt.canon_name
            || pickLang((debt as any).name ?? (debt as any).debt_type, isHi)
            || `Debt ${i + 1}`;
          const isBlocked = !!debt.blocked_by;
          return (
            <div
              key={`${debt.canon_name || i}`}
              className={`relative rounded-xl border p-3 ${
                isBlocked
                  ? 'border-red-300/50 bg-red-500/5'
                  : i === 0
                    ? 'border-sacred-gold/50 bg-sacred-gold/10'
                    : 'border-gray-200 bg-white/60'
              }`}
            >
              <div className="flex items-start gap-2 mb-1">
                <span className="text-xl shrink-0" aria-hidden="true">{rankBadges[i]}</span>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-bold text-foreground leading-tight">{title}</p>
                  <div className="flex flex-wrap gap-1 mt-1">
                    {typeof debt.priority_score === 'number' && (
                      <span className="text-[10px] px-1.5 py-0.5 rounded bg-sacred-gold/15 text-sacred-gold-dark font-semibold">
                        {isHi ? 'अंक' : 'Score'}: {debt.priority_score}
                      </span>
                    )}
                    {debt.dasha_active && (
                      <span className="inline-flex items-center gap-0.5 text-[10px] px-1.5 py-0.5 rounded bg-orange-500/15 text-orange-700 font-semibold">
                        <ArrowUpCircle className="w-3 h-3" />
                        {isHi ? 'दशा' : 'Dasha'}
                      </span>
                    )}
                    {debt.cluster_activator && (debt.cluster_size ?? 0) > 1 && (
                      <span className="text-[10px] px-1.5 py-0.5 rounded bg-purple-500/15 text-purple-700 font-semibold">
                        {isHi ? 'समूह' : 'Cluster'}: {debt.cluster_activator}
                      </span>
                    )}
                  </div>
                </div>
              </div>
              {isBlocked && (
                <div className="mt-2 flex items-start gap-1">
                  <Ban className="w-3 h-3 text-red-600 mt-0.5 shrink-0" />
                  <p className="text-[10px] text-red-700 leading-snug">
                    {isHi
                      ? (debt.blocked_reason?.hi || `पहले ${debt.blocked_by}`)
                      : (debt.blocked_reason?.en || `Gated by ${debt.blocked_by}`)}
                  </p>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Blocked relationships banner */}
      {compound.blocked_relationships && compound.blocked_relationships.length > 0 && (
        <div className="rounded-lg border border-red-400/40 bg-red-500/5 p-3">
          <p className="text-[10px] font-bold text-red-700 uppercase tracking-widest mb-1.5 flex items-center gap-1.5">
            <Ban className="w-3.5 h-3.5" />
            {isHi ? 'कैनन अवरोध' : 'Canon Blocks'}
          </p>
          <ul className="space-y-1.5">
            {compound.blocked_relationships.map((b, idx) => (
              <li key={`${b.blocker}-${idx}`} className="text-xs text-foreground/80 leading-snug">
                <span className="font-semibold text-red-700">
                  {b.blocker} {isHi ? 'पहले' : 'first'}:
                </span>{' '}
                {isHi ? b.reason_hi : b.reason_en}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Clusters (planet-shared compound) */}
      {compound.clusters && compound.clusters.length > 0 && (
        <div className="rounded-lg border border-purple-300/40 bg-purple-500/5 p-3">
          <p className="text-[10px] font-bold text-purple-700 uppercase tracking-widest mb-1.5 flex items-center gap-1.5">
            <Layers className="w-3.5 h-3.5" />
            {isHi ? 'संयोजित समूह' : 'Compound Clusters'}
          </p>
          <ul className="space-y-1.5">
            {compound.clusters.map((c, idx) => (
              <li key={`${c.activator}-${idx}`} className="text-xs text-foreground/80 leading-snug">
                <span className="font-semibold text-purple-700">{c.activator}:</span>{' '}
                {isHi ? c.note_hi : c.note_en}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Recommended order — prose paragraph */}
      <div className="rounded-lg border border-sacred-gold/30 bg-white/50 p-3">
        <p className="text-[10px] font-bold text-sacred-gold-dark uppercase tracking-widest mb-1">
          {isHi ? 'अनुशंसित क्रम' : 'Recommended Order'}
        </p>
        <p className="text-xs text-foreground/85 leading-relaxed">
          {isHi ? compound.recommended_order_hi : compound.recommended_order_en}
        </p>
      </div>
    </div>
  );
}
