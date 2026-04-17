import { useState, useEffect, useCallback } from 'react';
import { api } from '@/lib/api';
import {
  Loader2, Users, UserPlus, Trash2, Link2,
  TrendingUp, TrendingDown, ChevronDown, ChevronUp, X,
} from 'lucide-react';

// ─── Types ───────────────────────────────────────────────────────────────────

interface SavedKundli {
  id: string;
  person_name: string;
  birth_date: string;
  birth_time: string;
  birth_place: string;
}

interface CrossWakingItem {
  member_planet: string;
  member_planet_hi: string;
  member_house: number;
  wakes_house: number;
  effect: 'positive' | 'negative' | 'neutral';
  text_en: string;
  text_hi: string;
}

interface FamilyMember {
  link_id: string;
  kundli_id: string;
  name: string;
  relation: string;
  birth_date: string;
  harmony_score: number;
  shared_planets: string[];
  support_planets: string[];
  tension_planets: string[];
  theme: { en: string; hi: string } | null;
  cross_waking_narratives: CrossWakingItem[];
}

interface FamilyData {
  kundli_id: string;
  linked_members: FamilyMember[];
  family_harmony: number;
  dominant_planet: string | null;
  family_theme: { en: string; hi: string } | null;
}

interface Props { kundliId?: string; language: string; }

// ─── Constants ────────────────────────────────────────────────────────────────

const PLANET_DOT: Record<string, string> = {
  Sun: 'bg-orange-500', Moon: 'bg-blue-300', Mars: 'bg-red-500',
  Mercury: 'bg-green-500', Jupiter: 'bg-yellow-500', Venus: 'bg-pink-400',
  Saturn: 'bg-gray-500', Rahu: 'bg-purple-600', Ketu: 'bg-amber-700',
};

const RELATION_ICON: Record<string, string> = {
  father: '👨', mother: '👩', spouse: '💑', son: '👦', daughter: '👧',
  brother: '🧑', sister: '👧', grandfather: '👴', grandmother: '👵', other: '👤',
};

const RELATIONS = [
  'father', 'mother', 'spouse', 'son', 'daughter',
  'brother', 'sister', 'grandfather', 'grandmother', 'other',
];

// ─── Sub-components ──────────────────────────────────────────────────────────

function HarmonyBar({ score }: { score: number }) {
  const color = score >= 70 ? 'bg-green-500' : score >= 40 ? 'bg-yellow-500' : 'bg-red-500';
  return (
    <div className="flex items-center gap-2 min-w-[80px]">
      <div className="flex-1 bg-gray-100 rounded-full h-1.5">
        <div className={`h-1.5 rounded-full transition-all ${color}`} style={{ width: `${score}%` }} />
      </div>
      <span className="text-xs font-semibold tabular-nums w-6 text-right">{score}</span>
    </div>
  );
}

// ─── Cross-Waking Section ─────────────────────────────────────────────────────

function CrossWakingSection({ items, isHi }: { items: CrossWakingItem[]; isHi: boolean }) {
  const [open, setOpen] = useState(false);
  if (!items || items.length === 0) return null;

  const borderColor: Record<string, string> = {
    positive: 'border-l-green-500',
    negative: 'border-l-red-500',
    neutral:  'border-l-gray-300',
  };
  const bgColor: Record<string, string> = {
    positive: 'bg-green-50/60',
    negative: 'bg-red-50/60',
    neutral:  'bg-gray-50/60',
  };

  return (
    <div className="mt-3">
      <button
        onClick={() => setOpen(o => !o)}
        className="flex items-center gap-1.5 text-xs font-semibold text-muted-foreground hover:text-foreground transition-colors w-full text-left"
      >
        {open
          ? <ChevronUp className="w-3.5 h-3.5 shrink-0" />
          : <ChevronDown className="w-3.5 h-3.5 shrink-0" />}
        {isHi
          ? `क्रॉस-वेकिंग पैटर्न (${items.length})`
          : `Cross-Waking Patterns (${items.length})`}
      </button>

      {open && (
        <div className="mt-2 space-y-1.5">
          {items.map((item, idx) => (
            <div
              key={idx}
              className={`border-l-4 rounded-r-lg px-3 py-2 ${borderColor[item.effect] ?? 'border-l-gray-300'} ${bgColor[item.effect] ?? 'bg-gray-50/60'}`}
            >
              <div className="flex items-center gap-1.5 mb-0.5">
                <span className={`w-2 h-2 rounded-full shrink-0 ${PLANET_DOT[item.member_planet] ?? 'bg-gray-400'}`} />
                <span className="text-xs font-semibold text-foreground">
                  {isHi ? item.member_planet_hi : item.member_planet}
                </span>
                <span className="text-xs text-muted-foreground">
                  {isHi ? `भाव ${item.member_house} → भाव ${item.wakes_house}` : `H${item.member_house} → H${item.wakes_house}`}
                </span>
              </div>
              <p className="text-xs text-muted-foreground leading-relaxed">
                {isHi ? item.text_hi : item.text_en}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// ─── Add Member Modal ─────────────────────────────────────────────────────────

interface AddModalProps {
  kundliId: string;
  existingIds: string[];
  language: string;
  onClose: () => void;
  onLinked: () => void;
}

function AddMemberModal({ kundliId, existingIds, language, onClose, onLinked }: AddModalProps) {
  const hi = language === 'hi';
  const [kundlis, setKundlis] = useState<SavedKundli[]>([]);
  const [loadingList, setLoadingList] = useState(true);
  const [selected, setSelected] = useState('');
  const [relation, setRelation] = useState('');
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    api.get('/api/kundli')
      .then((data: SavedKundli[]) => {
        // Filter out already linked + self
        const filtered = data.filter(k => k.id !== kundliId && !existingIds.includes(k.id));
        setKundlis(filtered);
      })
      .catch(() => setError(hi ? 'कुंडली सूची लोड नहीं हुई' : 'Could not load kundli list'))
      .finally(() => setLoadingList(false));
  }, [kundliId, existingIds, hi]);

  const handleLink = async () => {
    if (!selected || !relation) {
      setError(hi ? 'कुंडली और रिश्ता चुनें' : 'Please select a kundli and relation');
      return;
    }
    setSaving(true);
    setError('');
    try {
      await api.post(`/api/lalkitab/family/${kundliId}/link`, {
        member_kundli_id: selected,
        relation,
      });
      onLinked();
    } catch {
      setError(hi ? 'लिंक नहीं हो सका' : 'Failed to link. Please try again.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center bg-black/50 px-4">
      <div className="bg-background rounded-2xl shadow-xl w-full max-w-md p-5 space-y-4">
        {/* Header */}
        <div className="flex items-center justify-between">
          <h3 className="font-bold text-foreground text-base">
            {hi ? 'परिवार सदस्य जोड़ें' : 'Add Family Member'}
          </h3>
          <button onClick={onClose} className="text-muted-foreground hover:text-foreground transition-colors">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Kundli picker */}
        <div>
          <label className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-1.5 block">
            {hi ? 'सदस्य की कुंडली चुनें' : 'Select Member\'s Kundli'}
          </label>
          {loadingList ? (
            <div className="flex justify-center py-4">
              <Loader2 className="w-5 h-5 animate-spin text-sacred-gold" />
            </div>
          ) : kundlis.length === 0 ? (
            <p className="text-sm text-muted-foreground bg-muted/30 rounded-lg p-3 text-center">
              {hi
                ? 'कोई उपलब्ध कुंडली नहीं। पहले परिवार के सदस्य की कुंडली बनाएं।'
                : 'No available kundlis. Create a kundli for the family member first.'}
            </p>
          ) : (
            <div className="space-y-1.5 max-h-48 overflow-y-auto">
              {kundlis.map(k => (
                <button
                  key={k.id}
                  onClick={() => setSelected(k.id)}
                  className={`w-full text-left rounded-xl border p-3 transition-all ${
                    selected === k.id
                      ? 'border-sacred-gold bg-sacred-gold/5'
                      : 'border-border hover:border-sacred-gold/40'
                  }`}
                >
                  <div className="font-semibold text-sm text-foreground">{k.person_name}</div>
                  <div className="text-xs text-muted-foreground mt-0.5">
                    {k.birth_date} · {k.birth_place}
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Relation selector */}
        <div>
          <label className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-1.5 block">
            {hi ? 'रिश्ता' : 'Relation'}
          </label>
          <div className="relative">
            <select
              value={relation}
              onChange={e => setRelation(e.target.value)}
              className="w-full border border-border rounded-xl px-3 py-2.5 text-sm bg-background appearance-none pr-8 focus:outline-none focus:border-sacred-gold"
            >
              <option value="">{hi ? '— रिश्ता चुनें —' : '— Select relation —'}</option>
              {RELATIONS.map(r => (
                <option key={r} value={r}>
                  {RELATION_ICON[r]} {r.charAt(0).toUpperCase() + r.slice(1)}
                </option>
              ))}
            </select>
            <ChevronDown className="w-4 h-4 text-muted-foreground absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none" />
          </div>
        </div>

        {error && (
          <p className="text-xs text-red-600 bg-red-50 rounded-lg px-3 py-2">{error}</p>
        )}

        {/* Actions */}
        <div className="flex gap-3">
          <button
            onClick={onClose}
            className="flex-1 py-2.5 rounded-xl border border-border text-sm text-foreground hover:bg-muted/30 transition-colors"
          >
            {hi ? 'रद्द करें' : 'Cancel'}
          </button>
          <button
            onClick={handleLink}
            disabled={saving || !selected || !relation}
            className="flex-1 py-2.5 rounded-xl bg-sacred-gold text-white text-sm font-semibold hover:bg-sacred-gold/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {saving ? <Loader2 className="w-4 h-4 animate-spin" /> : <Link2 className="w-4 h-4" />}
            {hi ? 'जोड़ें' : 'Link'}
          </button>
        </div>
      </div>
    </div>
  );
}

// ─── Main Component ───────────────────────────────────────────────────────────

export default function LalKitabFamilyTab({ kundliId, language }: Props) {
  const hi = language === 'hi';
  const [data, setData] = useState<FamilyData | null>(null);
  const [loading, setLoading] = useState(false);
  const [showAddModal, setShowAddModal] = useState(false);
  const [removingId, setRemovingId] = useState<string | null>(null);

  const load = useCallback(() => {
    if (!kundliId) return;
    setLoading(true);
    api.get(`/api/lalkitab/family/${kundliId}`)
      .then(setData)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [kundliId]);

  useEffect(() => { load(); }, [load]);

  const handleRemove = async (linkId: string) => {
    if (!kundliId) return;
    setRemovingId(linkId);
    try {
      await api.delete(`/api/lalkitab/family/${kundliId}/link/${linkId}`);
      load();
    } catch {
      // silent
    } finally {
      setRemovingId(null);
    }
  };

  if (!kundliId) return (
    <div className="text-center py-10 text-muted-foreground text-sm">
      {hi ? 'परिवार विश्लेषण के लिए कुंडली सहेजें।' : 'Save a Kundli to use Family Linking.'}
    </div>
  );

  if (loading) return (
    <div className="flex justify-center py-16">
      <Loader2 className="w-8 h-8 animate-spin text-sacred-gold" />
    </div>
  );

  const members = data?.linked_members ?? [];
  const existingIds = members.map(m => m.kundli_id);

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-start justify-between gap-3">
        <div>
          <div className="flex items-center gap-2 mb-0.5">
            <span className="text-2xl">👨‍👩‍👧‍👦</span>
            <h3 className="font-bold text-foreground text-base">
              {hi ? 'ग्रह-गस्ती — परिवार लिंकिंग' : 'Grah-Gasti — Family Linking'}
            </h3>
          </div>
          <p className="text-xs text-muted-foreground">
            {hi
              ? 'परिवार की कुंडलियाँ जोड़कर ग्रह प्रभाव देखें'
              : 'Link family charts to reveal cross-chart planetary interactions'}
          </p>
        </div>
        <button
          onClick={() => setShowAddModal(true)}
          className="shrink-0 flex items-center gap-1.5 bg-sacred-gold text-white text-xs font-semibold px-3 py-2 rounded-xl hover:bg-sacred-gold/90 transition-colors"
        >
          <UserPlus className="w-3.5 h-3.5" />
          {hi ? 'जोड़ें' : 'Add'}
        </button>
      </div>

      {/* Family harmony panel */}
      {members.length > 0 && data && (
        <div className="card-sacred rounded-xl p-4 bg-sacred-gold/5 border border-sacred-gold/20">
          <div className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-3">
            {hi ? 'पारिवारिक सौहार्द' : 'Family Harmony'}
          </div>
          <div className="flex items-center gap-3 mb-2">
            <div className="text-4xl font-bold text-sacred-gold">{data.family_harmony}</div>
            <div className="flex-1">
              <HarmonyBar score={data.family_harmony} />
              {data.family_theme && (
                <p className="text-xs text-muted-foreground mt-1 italic">
                  "{hi ? data.family_theme.hi : data.family_theme.en}"
                </p>
              )}
            </div>
          </div>
          {data.dominant_planet && (
            <div className="flex items-center gap-2 text-xs text-foreground">
              <span className={`w-2.5 h-2.5 rounded-full ${PLANET_DOT[data.dominant_planet] ?? 'bg-gray-400'}`} />
              <span>
                {hi
                  ? `${data.dominant_planet} आपके परिवार का प्रमुख ग्रह है`
                  : `${data.dominant_planet} is the dominant planet across your family`}
              </span>
            </div>
          )}
        </div>
      )}

      {/* Member cards */}
      {members.length > 0 ? (
        <div className="space-y-3">
          <div className="text-xs font-semibold text-muted-foreground px-1">
            {hi ? `${members.length} सदस्य जुड़े हुए हैं` : `${members.length} member(s) linked`}
          </div>
          {members.map((member) => (
            <div key={member.link_id} className="border border-border bg-card rounded-xl p-4">
              {/* Member header */}
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-2">
                  <span className="text-xl">{RELATION_ICON[member.relation] ?? '👤'}</span>
                  <div>
                    <div className="font-bold text-foreground text-sm">{member.name}</div>
                    <div className="text-xs text-muted-foreground capitalize">
                      {member.relation} · {member.birth_date}
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <div className="text-right">
                    <div className="text-xs text-muted-foreground mb-1">{hi ? 'सौहार्द' : 'Harmony'}</div>
                    <HarmonyBar score={member.harmony_score} />
                  </div>
                  <button
                    onClick={() => handleRemove(member.link_id)}
                    disabled={removingId === member.link_id}
                    className="ml-1 p-1.5 rounded-lg text-muted-foreground hover:text-red-500 hover:bg-red-50 transition-colors disabled:opacity-40"
                    title={hi ? 'हटाएं' : 'Remove'}
                  >
                    {removingId === member.link_id
                      ? <Loader2 className="w-3.5 h-3.5 animate-spin" />
                      : <Trash2 className="w-3.5 h-3.5" />}
                  </button>
                </div>
              </div>

              {/* Per-member theme */}
              {member.theme && (
                <p className="text-xs text-muted-foreground italic mb-3 px-0.5">
                  "{hi ? member.theme.hi : member.theme.en}"
                </p>
              )}

              {/* Shared planets */}
              {member.shared_planets.length > 0 && (
                <div className="mb-2">
                  <div className="flex items-center gap-1 text-xs font-semibold text-muted-foreground mb-1">
                    <Link2 className="w-3 h-3" />
                    {hi ? 'साझा ग्रह' : 'Shared planets'}
                  </div>
                  <div className="flex flex-wrap gap-1">
                    {member.shared_planets.map(p => (
                      <span key={p} className="flex items-center gap-1 text-xs bg-sacred-gold/10 text-sacred-gold px-1.5 py-0.5 rounded-full">
                        <span className={`w-1.5 h-1.5 rounded-full ${PLANET_DOT[p] ?? 'bg-gray-400'}`} />
                        {p}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Support & tension */}
              {(member.support_planets.length > 0 || member.tension_planets.length > 0) && (
                <div className="grid grid-cols-2 gap-2 mt-2">
                  {member.support_planets.length > 0 && (
                    <div className="bg-green-50 rounded-lg p-2">
                      <div className="flex items-center gap-1 text-xs font-semibold text-green-700 mb-1">
                        <TrendingUp className="w-3 h-3" />
                        {hi ? 'सहयोग ग्रह' : 'Support'}
                      </div>
                      <div className="flex flex-wrap gap-1">
                        {member.support_planets.map(p => (
                          <span key={p} className="text-xs text-green-600">{p}</span>
                        ))}
                      </div>
                    </div>
                  )}
                  {member.tension_planets.length > 0 && (
                    <div className="bg-red-50 rounded-lg p-2">
                      <div className="flex items-center gap-1 text-xs font-semibold text-red-700 mb-1">
                        <TrendingDown className="w-3 h-3" />
                        {hi ? 'तनाव ग्रह' : 'Tension'}
                      </div>
                      <div className="flex flex-wrap gap-1">
                        {member.tension_planets.map(p => (
                          <span key={p} className="text-xs text-red-600">{p}</span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Cross-waking narratives */}
              <CrossWakingSection
                items={member.cross_waking_narratives ?? []}
                isHi={hi}
              />
            </div>
          ))}
        </div>
      ) : (
        /* Empty state */
        <div className="border border-dashed border-border rounded-xl p-8 text-center">
          <Users className="w-10 h-10 text-muted-foreground/40 mx-auto mb-3" />
          <p className="text-sm font-semibold text-foreground mb-1">
            {hi ? 'कोई परिवार सदस्य नहीं जुड़ा' : 'No family members linked yet'}
          </p>
          <p className="text-xs text-muted-foreground mb-4">
            {hi
              ? 'परिवार के सदस्यों की कुंडली बनाएं और यहाँ जोड़ें'
              : 'Create Kundlis for family members and link them here to see cross-chart planetary analysis'}
          </p>
          <button
            onClick={() => setShowAddModal(true)}
            className="inline-flex items-center gap-1.5 bg-sacred-gold text-white text-sm font-semibold px-4 py-2 rounded-xl hover:bg-sacred-gold/90 transition-colors"
          >
            <UserPlus className="w-4 h-4" />
            {hi ? 'पहला सदस्य जोड़ें' : 'Add First Member'}
          </button>
        </div>
      )}

      {/* How it works note */}
      <div className="bg-muted/30 rounded-xl p-3 text-xs text-muted-foreground space-y-1">
        <p className="font-semibold text-foreground">{hi ? 'यह कैसे काम करता है:' : 'How it works:'}</p>
        <p>1. {hi ? 'परिवार के सदस्य की कुंडली बनाएं (Kundli सेक्शन में)' : 'Create a Kundli for a family member (in the Kundli section)'}</p>
        <p>2. {hi ? '"जोड़ें" बटन दबाकर उन्हें चुनें और रिश्ता बताएं' : 'Click "Add" above, select their Kundli, set the relation'}</p>
        <p>3. {hi ? 'ग्रह-गस्ती इंजन क्रॉस-चार्ट हार्मनी की गणना करेगा' : 'The Grah-Gasti engine calculates cross-chart harmony'}</p>
      </div>

      {/* Add modal */}
      {showAddModal && (
        <AddMemberModal
          kundliId={kundliId}
          existingIds={existingIds}
          language={language}
          onClose={() => setShowAddModal(false)}
          onLinked={() => { setShowAddModal(false); load(); }}
        />
      )}
    </div>
  );
}
