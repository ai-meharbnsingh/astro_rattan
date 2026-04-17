import { useState, useEffect, useCallback } from 'react';
import { api } from '@/lib/api';
import { Loader2, Plus, CheckCircle2, XCircle, RotateCcw, Trash2, Calendar, X } from 'lucide-react';

// ─── Types ───────────────────────────────────────────────────────────────────

interface TrackerEntry {
  id: string;
  remedy_title: string;
  remedy_description: string;
  planet: string | null;
  started_at: string;
  target_days: number;
  completed_days: number;
  check_ins: string[];
  status: 'active' | 'completed' | 'broken' | 'paused';
  progress_pct: number;
}

interface Props { kundliId?: string; language: string; }

// ─── Constants ────────────────────────────────────────────────────────────────

const PLANETS = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu'];
const PLANET_COLOR: Record<string, string> = {
  Sun: 'bg-orange-100 text-orange-700', Moon: 'bg-blue-100 text-blue-700',
  Mars: 'bg-red-100 text-red-700', Mercury: 'bg-green-100 text-green-700',
  Jupiter: 'bg-yellow-100 text-yellow-800', Venus: 'bg-pink-100 text-pink-700',
  Saturn: 'bg-gray-100 text-gray-700', Rahu: 'bg-purple-100 text-purple-700',
  Ketu: 'bg-amber-100 text-amber-700',
};
const STATUS_COLOR: Record<string, string> = {
  active: 'text-green-600 bg-green-50 border-green-200',
  completed: 'text-blue-600 bg-blue-50 border-blue-200',
  broken: 'text-red-600 bg-red-50 border-red-200',
  paused: 'text-yellow-600 bg-yellow-50 border-yellow-200',
};
const STATUS_LABEL_EN: Record<string, string> = {
  active: 'Active', completed: 'Completed', broken: 'Broken — Reset', paused: 'Paused',
};
const STATUS_LABEL_HI: Record<string, string> = {
  active: 'सक्रिय', completed: 'पूर्ण', broken: 'टूटा — रीसेट', paused: 'रोका',
};

// ─── Add Tracker Modal ────────────────────────────────────────────────────────

interface AddModalProps {
  kundliId: string;
  language: string;
  onClose: () => void;
  onCreated: () => void;
}

function AddTrackerModal({ kundliId, language, onClose, onCreated }: AddModalProps) {
  const hi = language === 'hi';
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [planet, setPlanet] = useState('');
  const [targetDays, setTargetDays] = useState(43);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

  const handleCreate = async () => {
    if (!title.trim()) { setError(hi ? 'उपाय का नाम दर्ज करें' : 'Enter a remedy title'); return; }
    setSaving(true);
    setError('');
    try {
      await api.post(`/api/lalkitab/remedy-tracker/${kundliId}`, {
        remedy_title: title.trim(),
        remedy_description: description.trim(),
        planet: planet || null,
        target_days: targetDays,
      });
      onCreated();
    } catch {
      setError(hi ? 'ट्रैकर बनाने में विफल' : 'Failed to create tracker');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center bg-black/50 px-4">
      <div className="bg-background rounded-2xl shadow-xl w-full max-w-md p-5 space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="font-bold text-foreground text-base">
            {hi ? 'नया उपाय ट्रैकर' : 'New Remedy Tracker'}
          </h3>
          <button onClick={onClose}><X className="w-5 h-5 text-muted-foreground" /></button>
        </div>

        <div className="space-y-3">
          <div>
            <label className="text-xs font-semibold text-muted-foreground block mb-1">
              {hi ? 'उपाय का नाम *' : 'Remedy Title *'}
            </label>
            <input
              value={title}
              onChange={e => setTitle(e.target.value)}
              placeholder={hi ? 'उदा. शनि को काले तिल खिलाएं' : 'e.g. Feed black sesame to crows'}
              className="w-full border border-border rounded-xl px-3 py-2 text-sm bg-background focus:outline-none focus:border-sacred-gold"
            />
          </div>
          <div>
            <label className="text-xs font-semibold text-muted-foreground block mb-1">
              {hi ? 'विस्तार (वैकल्पिक)' : 'Description (optional)'}
            </label>
            <textarea
              value={description}
              onChange={e => setDescription(e.target.value)}
              rows={2}
              className="w-full border border-border rounded-xl px-3 py-2 text-sm bg-background focus:outline-none focus:border-sacred-gold resize-none"
            />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-xs font-semibold text-muted-foreground block mb-1">
                {hi ? 'ग्रह' : 'Planet'}
              </label>
              <select
                value={planet}
                onChange={e => setPlanet(e.target.value)}
                className="w-full border border-border rounded-xl px-3 py-2 text-sm bg-background focus:outline-none focus:border-sacred-gold"
              >
                <option value="">{hi ? 'सभी' : 'Any'}</option>
                {PLANETS.map(p => <option key={p} value={p}>{p}</option>)}
              </select>
            </div>
            <div>
              <label className="text-xs font-semibold text-muted-foreground block mb-1">
                {hi ? 'दिन' : 'Days'}
              </label>
              <select
                value={targetDays}
                onChange={e => setTargetDays(Number(e.target.value))}
                className="w-full border border-border rounded-xl px-3 py-2 text-sm bg-background focus:outline-none focus:border-sacred-gold"
              >
                <option value={11}>11 {hi ? 'दिन' : 'days'}</option>
                <option value={21}>21 {hi ? 'दिन' : 'days'}</option>
                <option value={40}>40 {hi ? 'दिन' : 'days'}</option>
                <option value={43}>43 {hi ? 'दिन' : 'days'} (LK Standard)</option>
                <option value={108}>108 {hi ? 'दिन' : 'days'}</option>
              </select>
            </div>
          </div>
        </div>

        {error && <p className="text-xs text-red-600 bg-red-50 rounded-lg px-3 py-2">{error}</p>}

        <div className="flex gap-3">
          <button onClick={onClose} className="flex-1 py-2.5 rounded-xl border border-border text-sm text-foreground hover:bg-muted/30">
            {hi ? 'रद्द करें' : 'Cancel'}
          </button>
          <button
            onClick={handleCreate}
            disabled={saving}
            className="flex-1 py-2.5 rounded-xl bg-sacred-gold text-white text-sm font-semibold hover:bg-sacred-gold/90 disabled:opacity-50 flex items-center justify-center gap-2"
          >
            {saving ? <Loader2 className="w-4 h-4 animate-spin" /> : <Plus className="w-4 h-4" />}
            {hi ? 'शुरू करें' : 'Start'}
          </button>
        </div>
      </div>
    </div>
  );
}

// ─── Progress Circle ──────────────────────────────────────────────────────────

function ProgressRing({ pct, status }: { pct: number; status: string }) {
  const r = 22;
  const circ = 2 * Math.PI * r;
  const fill = (pct / 100) * circ;
  const color = status === 'completed' ? '#3b82f6' : status === 'broken' ? '#ef4444' : '#c45a00';
  return (
    <svg width="56" height="56" viewBox="0 0 56 56">
      <circle cx="28" cy="28" r={r} fill="none" stroke="#e5e7eb" strokeWidth="4" />
      <circle
        cx="28" cy="28" r={r} fill="none"
        stroke={color} strokeWidth="4"
        strokeDasharray={`${fill} ${circ - fill}`}
        strokeLinecap="round"
        transform="rotate(-90 28 28)"
        style={{ transition: 'stroke-dasharray 0.5s ease' }}
      />
      <text x="28" y="33" textAnchor="middle" fontSize="11" fontWeight="bold" fill={color}>
        {pct}%
      </text>
    </svg>
  );
}

// ─── Main Component ───────────────────────────────────────────────────────────

export default function LalKitabRemedyTrackerTab({ kundliId, language }: Props) {
  const hi = language === 'hi';
  const [trackers, setTrackers] = useState<TrackerEntry[]>([]);
  const [loading, setLoading] = useState(false);
  const [showAdd, setShowAdd] = useState(false);
  const [actionId, setActionId] = useState<string | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);

  const load = useCallback(() => {
    if (!kundliId) return;
    setLoading(true);
    setLoadError(null);
    api.get(`/api/lalkitab/remedy-tracker/${kundliId}`)
      .then((d: { trackers: TrackerEntry[] }) => setTrackers(d.trackers))
      .catch((err) => {
        console.error('Failed to load remedy trackers:', err);
        const msg = err instanceof Error ? err.message : (typeof err === 'string' ? err : 'Unknown error');
        setLoadError(msg);
      })
      .finally(() => setLoading(false));
  }, [kundliId]);

  useEffect(() => { load(); }, [load]);

  const checkin = async (trackerId: string, missed = false) => {
    setActionId(trackerId);
    try {
      await api.post(`/api/lalkitab/remedy-tracker/${trackerId}/checkin`, { missed });
      load();
    } catch (err) {
      console.error('Failed to check in remedy:', err);
      const msg = err instanceof Error ? err.message : (typeof err === 'string' ? err : 'Unknown error');
      setLoadError(msg);
    }
    setActionId(null);
  };

  const deleteTracker = async (trackerId: string) => {
    setActionId(trackerId);
    try {
      await api.delete(`/api/lalkitab/remedy-tracker/${trackerId}`);
      load();
    } catch (err) {
      console.error('Failed to delete tracker:', err);
      const msg = err instanceof Error ? err.message : (typeof err === 'string' ? err : 'Unknown error');
      setLoadError(msg);
    }
    setActionId(null);
  };

  if (!kundliId) return (
    <div className="text-center py-10 text-muted-foreground text-sm">
      {hi ? 'ट्रैकर के लिए कुंडली सहेजें।' : 'Save a Kundli to use Remedy Tracker.'}
    </div>
  );

  if (loading) return (
    <div className="flex justify-center py-16">
      <Loader2 className="w-8 h-8 animate-spin text-sacred-gold" />
    </div>
  );

  const today = new Date().toISOString().slice(0, 10);

  return (
    <div className="space-y-4">
      {loadError && (
        <div className="p-3 mb-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-800">
          {hi ? 'डेटा लोड करने में त्रुटि' : 'Failed to load data'}: {loadError}
        </div>
      )}
      {/* Header */}
      <div className="flex items-start justify-between gap-3">
        <div>
          <div className="flex items-center gap-2 mb-0.5">
            <span className="text-2xl">📿</span>
            <h3 className="font-bold text-foreground text-base">
              {hi ? '43-दिन उपाय ट्रैकर' : '43-Day Remedy Tracker'}
            </h3>
          </div>
          <p className="text-xs text-muted-foreground">
            {hi
              ? 'लाल किताब उपायों की श्रृंखला ट्रैक करें — एक दिन भी न चूकें'
              : 'Track your Lal Kitab remedy chains — do not miss a single day'}
          </p>
        </div>
        <button
          onClick={() => setShowAdd(true)}
          className="shrink-0 flex items-center gap-1.5 bg-sacred-gold text-white text-xs font-semibold px-3 py-2 rounded-xl hover:bg-sacred-gold/90"
        >
          <Plus className="w-3.5 h-3.5" />
          {hi ? 'नया' : 'New'}
        </button>
      </div>

      {/* LK rule note */}
      <div className="bg-amber-50 border border-amber-100 rounded-xl p-3 text-xs text-amber-800">
        <span className="font-semibold">{hi ? 'लाल किताब नियम: ' : 'LK Rule: '}</span>
        {hi
          ? '43-दिन की श्रृंखला — एक दिन भी चूकने पर पूरी श्रृंखला टूट जाती है और दिन 0 से फिर शुरू करें।'
          : 'A 43-day unbroken chain. Miss one day → the chain breaks and you must restart from Day 0.'}
      </div>

      {trackers.length === 0 ? (
        <div className="border border-dashed border-border rounded-xl p-8 text-center">
          <Calendar className="w-10 h-10 text-muted-foreground/40 mx-auto mb-3" />
          <p className="text-sm font-semibold text-foreground mb-1">
            {hi ? 'कोई उपाय ट्रैकर नहीं' : 'No remedy trackers yet'}
          </p>
          <p className="text-xs text-muted-foreground mb-4">
            {hi
              ? 'अपना पहला 43-दिन का उपाय शुरू करें'
              : 'Start your first 43-day remedy chain'}
          </p>
          <button
            onClick={() => setShowAdd(true)}
            className="inline-flex items-center gap-1.5 bg-sacred-gold text-white text-sm font-semibold px-4 py-2 rounded-xl hover:bg-sacred-gold/90"
          >
            <Plus className="w-4 h-4" />
            {hi ? 'उपाय शुरू करें' : 'Start a Remedy'}
          </button>
        </div>
      ) : (
        <div className="space-y-3">
          {trackers.map(t => {
            const checkedToday = t.check_ins.includes(today);
            const isActive = t.status === 'active';
            const isBusy = actionId === t.id;
            return (
              <div key={t.id} className={`rounded-xl border p-4 ${STATUS_COLOR[t.status]?.replace('text-', 'border-') ?? 'border-border'} bg-card`}>
                {/* Top row */}
                <div className="flex items-start gap-3 mb-3">
                  <ProgressRing pct={t.progress_pct} status={t.status} />
                  <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between gap-2">
                      <h4 className="font-bold text-sm text-foreground leading-tight">{t.remedy_title}</h4>
                      <button
                        onClick={() => deleteTracker(t.id)}
                        disabled={isBusy}
                        className="p-1 rounded-lg text-muted-foreground hover:text-red-500 hover:bg-red-50 transition-colors shrink-0"
                      >
                        {isBusy ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Trash2 className="w-3.5 h-3.5" />}
                      </button>
                    </div>
                    {t.planet && (
                      <span className={`inline-block text-xs font-semibold px-1.5 py-0.5 rounded-full mt-1 ${PLANET_COLOR[t.planet] ?? 'bg-muted text-muted-foreground'}`}>
                        {t.planet}
                      </span>
                    )}
                    <div className="flex items-center gap-2 mt-1">
                      <span className={`text-xs font-semibold px-1.5 py-0.5 rounded-full border ${STATUS_COLOR[t.status]}`}>
                        {hi ? STATUS_LABEL_HI[t.status] : STATUS_LABEL_EN[t.status]}
                      </span>
                      <span className="text-xs text-muted-foreground">
                        {t.completed_days}/{t.target_days} {hi ? 'दिन' : 'days'}
                      </span>
                    </div>
                  </div>
                </div>

                {/* Progress bar */}
                <div className="w-full bg-gray-100 rounded-full h-1.5 mb-3">
                  <div
                    className={`h-1.5 rounded-full transition-all ${
                      t.status === 'completed' ? 'bg-blue-500' : t.status === 'broken' ? 'bg-red-500' : 'bg-sacred-gold'
                    }`}
                    style={{ width: `${t.progress_pct}%` }}
                  />
                </div>

                {/* Description */}
                {t.remedy_description && (
                  <p className="text-xs text-muted-foreground mb-3">{t.remedy_description}</p>
                )}

                {/* Action buttons */}
                {isActive && (
                  <div className="flex gap-2">
                    <button
                      onClick={() => checkin(t.id, false)}
                      disabled={isBusy || checkedToday}
                      className={`flex-1 flex items-center justify-center gap-1.5 py-2 rounded-xl text-xs font-semibold transition-colors ${
                        checkedToday
                          ? 'bg-green-100 text-green-700 cursor-default'
                          : 'bg-green-600 text-white hover:bg-green-700 disabled:opacity-50'
                      }`}
                    >
                      <CheckCircle2 className="w-3.5 h-3.5" />
                      {checkedToday
                        ? (hi ? 'आज किया ✓' : 'Done today ✓')
                        : (hi ? 'आज किया' : 'Done today')}
                    </button>
                    <button
                      onClick={() => checkin(t.id, true)}
                      disabled={isBusy}
                      className="flex items-center justify-center gap-1.5 px-3 py-2 rounded-xl text-xs font-semibold border border-red-200 text-red-600 hover:bg-red-50 transition-colors disabled:opacity-50"
                    >
                      <XCircle className="w-3.5 h-3.5" />
                      {hi ? 'चूक गया' : 'Missed'}
                    </button>
                  </div>
                )}
                {t.status === 'broken' && (
                  <button
                    onClick={() => checkin(t.id, false)}
                    disabled={isBusy}
                    className="w-full flex items-center justify-center gap-1.5 py-2 rounded-xl text-xs font-semibold bg-sacred-gold text-white hover:bg-sacred-gold/90 disabled:opacity-50"
                  >
                    <RotateCcw className="w-3.5 h-3.5" />
                    {hi ? 'फिर से शुरू करें' : 'Restart from Day 1'}
                  </button>
                )}
                {t.status === 'completed' && (
                  <div className="flex items-center justify-center gap-2 py-2 bg-blue-50 rounded-xl">
                    <CheckCircle2 className="w-4 h-4 text-blue-500" />
                    <span className="text-xs font-bold text-blue-700">
                      {hi ? `${t.target_days} दिन पूर्ण! शुभ है।` : `${t.target_days}-day chain complete! Blessed.`}
                    </span>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}

      {showAdd && (
        <AddTrackerModal
          kundliId={kundliId}
          language={language}
          onClose={() => setShowAdd(false)}
          onCreated={() => { setShowAdd(false); load(); }}
        />
      )}
    </div>
  );
}
