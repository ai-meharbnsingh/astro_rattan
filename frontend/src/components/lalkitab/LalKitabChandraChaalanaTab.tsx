import { useState, useMemo, useEffect } from 'react';
import { useTranslation } from '@/lib/i18n';
import { CHANDRA_CHAALANA_TASKS } from './lalkitab-data';
import { Moon, CheckCircle2, RotateCcw, BookOpen, Play, AlertTriangle } from 'lucide-react';
import { apiFetch } from '@/lib/api';

interface JournalEntry {
  date: string;
  note: string;
}

const STORAGE_KEY = 'lk_chandra_v1';
const JOURNAL_KEY = 'lk_chandra_journal_v1';

function todayStr(): string {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

interface ProtocolState {
  startDate: string | null;
  completedDays: string[]; // list of ISO dates marked complete
}

function loadState(): ProtocolState {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null') || { startDate: null, completedDays: [] };
  } catch {
    return { startDate: null, completedDays: [] };
  }
}

function saveState(s: ProtocolState) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(s));
}

function loadJournal(): JournalEntry[] {
  try {
    return JSON.parse(localStorage.getItem(JOURNAL_KEY) || '[]');
  } catch {
    return [];
  }
}

function saveJournal(j: JournalEntry[]) {
  localStorage.setItem(JOURNAL_KEY, JSON.stringify(j));
}

const categoryColors: Record<string, string> = {
  action: 'bg-blue-500/10 text-blue-700',
  donation: 'bg-green-500/10 text-green-700',
  meditation: 'bg-purple-500/10 text-purple-700',
  fasting: 'bg-orange-500/10 text-orange-700',
  mantra: 'bg-sacred-gold/15 text-sacred-gold-dark',
};

export default function LalKitabChandraChaalanaTab() {
  const { t, language } = useTranslation();
  const isHi = language === 'hi';

  const [state, setState] = useState<ProtocolState>(loadState);
  const [journalEntries, setJournalEntries] = useState<JournalEntry[]>(loadJournal);
  const [journalNote, setJournalNote] = useState('');

  const today = todayStr();

  // Load from API on mount — API wins for cross-device sync
  useEffect(() => {
    apiFetch('/api/lalkitab/chandra')
      .then((res) => res.json())
      .then((data: { start_date: string | null; completed_days: string[]; journal: JournalEntry[] }) => {
        if (data.start_date !== undefined) {
          const apiState: ProtocolState = {
            startDate: data.start_date,
            completedDays: data.completed_days || [],
          };
          setState(apiState);
          saveState(apiState);
        }
        if (data.journal?.length) {
          setJournalEntries(data.journal);
          saveJournal(data.journal);
        }
      })
      .catch(() => {/* silent — localStorage already loaded */});
  }, []);

  const { currentDay, isMissed, isComplete } = useMemo(() => {
    if (!state.startDate) return { currentDay: 0, isMissed: false, isComplete: false };
    const start = new Date(state.startDate);
    const now = new Date(today);
    const daysSinceStart = Math.floor((now.getTime() - start.getTime()) / 86400000);
    const completedCount = state.completedDays.length;
    const isMissed = completedCount < daysSinceStart; // missed a day
    const currentDay = completedCount + 1;
    const isComplete = completedCount >= 43;
    return { currentDay: Math.min(currentDay, 43), isMissed, isComplete };
  }, [state, today]);

  const todayTask = CHANDRA_CHAALANA_TASKS.find((t) => t.day === currentDay);
  const isTodayDone = state.completedDays.includes(today);

  const startProtocol = () => {
    const s: ProtocolState = { startDate: today, completedDays: [] };
    saveState(s);
    setState(s);
    apiFetch('/api/lalkitab/chandra/start', {
      method: 'POST',
      body: JSON.stringify({ start_date: today }),
    }).catch(() => {});
  };

  const restartProtocol = () => {
    const s: ProtocolState = { startDate: today, completedDays: [] };
    saveState(s);
    setState(s);
    apiFetch('/api/lalkitab/chandra/start', {
      method: 'POST',
      body: JSON.stringify({ start_date: today }),
    }).catch(() => {});
  };

  const markDayDone = () => {
    if (isTodayDone) return;
    // Optimistic update
    const updated: ProtocolState = {
      ...state,
      completedDays: [...state.completedDays, today],
    };
    saveState(updated);
    setState(updated);

    // Sync to API — API reconciles and returns authoritative list
    apiFetch('/api/lalkitab/chandra/mark-done', {
      method: 'POST',
      body: JSON.stringify({ date: today }),
    })
      .then((res) => res.json())
      .then((data: { completed_days: string[] }) => {
        const reconciled: ProtocolState = { ...updated, completedDays: data.completed_days };
        saveState(reconciled);
        setState(reconciled);
      })
      .catch(() => {/* keep optimistic state */});
  };

  const saveEntry = () => {
    if (!journalNote.trim()) return;
    const entry: JournalEntry = { date: today, note: journalNote.trim() };
    const updated = [entry, ...journalEntries].slice(0, 60);
    setJournalEntries(updated);
    saveJournal(updated);
    setJournalNote('');

    apiFetch('/api/lalkitab/chandra/journal', {
      method: 'POST',
      body: JSON.stringify({ date: today, note: entry.note }),
    }).catch(() => {});
  };

  const progressPct = state.startDate ? Math.min(100, Math.round((state.completedDays.length / 43) * 100)) : 0;

  const dayLabel = (n: number) =>
    isHi
      ? t('lk.chandra.dayOf').replace('{n}', String(n))
      : t('lk.chandra.dayOf').replace('{n}', String(n));

  // Not started
  if (!state.startDate) {
    return (
      <div className="space-y-6">
        <div>
          <h2 className="text-xl font-sans font-semibold text-sacred-gold flex items-center gap-2 mb-1">
            <Moon className="w-5 h-5" />
            {t('lk.chandra.title')}
          </h2>
          <p className="text-sm text-gray-500">{t('lk.chandra.desc')}</p>
        </div>

        <div className="card-sacred rounded-xl p-8 border border-sacred-gold/20 text-center">
          <Moon className="w-14 h-14 mx-auto mb-4 text-sacred-gold opacity-70" />
          <h3 className="font-sans text-lg font-semibold text-sacred-gold mb-2">
            {t('lk.chandra.notStarted')}
          </h3>
          <p className="text-sm text-gray-500 mb-6 max-w-sm mx-auto">
            {t('lk.chandra.notStartedDesc')}
          </p>
          <div className="flex items-start gap-3 p-4 rounded-xl bg-orange-500/5 border border-orange-300/20 mb-6 text-left">
            <AlertTriangle className="w-4 h-4 text-orange-500 mt-0.5 shrink-0" />
            <p className="text-xs text-orange-700">{t('lk.chandra.restartInfo')}</p>
          </div>
          <button
            onClick={startProtocol}
            className="flex items-center gap-2 px-6 py-3 rounded-xl bg-sacred-gold text-white font-semibold hover:bg-sacred-gold-dark transition-all mx-auto"
          >
            <Play className="w-4 h-4" />
            {t('lk.chandra.startBtn')}
          </button>
        </div>

        {/* Preview first 7 days */}
        <div className="card-sacred rounded-xl p-5 border border-sacred-gold/20">
          <h3 className="font-sans font-semibold text-sacred-gold mb-4">
            {isHi ? 'पहले 7 दिन की झलक' : 'Preview — First 7 Days'}
          </h3>
          <div className="space-y-2">
            {CHANDRA_CHAALANA_TASKS.slice(0, 7).map((task) => (
              <div key={task.day} className="flex items-start gap-3 p-3 rounded-xl bg-sacred-gold/5">
                <span className="text-xs font-bold text-sacred-gold min-w-[40px]">
                  {isHi ? `दिन ${task.day}` : `Day ${task.day}`}
                </span>
                <p className="text-xs text-cosmic-text/80 leading-snug">
                  {isHi ? task.hi : task.en}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-xl font-sans font-semibold text-sacred-gold flex items-center gap-2 mb-1">
          <Moon className="w-5 h-5" />
          {t('lk.chandra.title')}
        </h2>
        <p className="text-sm text-gray-500">{t('lk.chandra.desc')}</p>
      </div>

      {/* Complete banner */}
      {isComplete && (
        <div className="p-5 rounded-xl bg-green-500/10 border border-green-300/30 text-center">
          <CheckCircle2 className="w-10 h-10 text-green-500 mx-auto mb-2" />
          <p className="font-sans font-semibold text-green-700">{t('lk.chandra.complete')}</p>
          <button
            onClick={restartProtocol}
            className="mt-3 flex items-center gap-2 px-4 py-2 rounded-xl border border-green-400 text-green-700 text-sm hover:bg-green-50 transition-all mx-auto"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            {t('lk.chandra.restartBtn')}
          </button>
        </div>
      )}

      {/* Missed day warning */}
      {!isComplete && isMissed && (
        <div className="p-4 rounded-xl bg-red-500/8 border border-red-300/30 flex items-start gap-3">
          <AlertTriangle className="w-4 h-4 text-red-500 mt-0.5 shrink-0" />
          <div>
            <p className="text-sm font-semibold text-red-600">{t('lk.chandra.missedDay')}</p>
            <p className="text-xs text-red-500/80 mt-0.5">{t('lk.chandra.restartInfo')}</p>
            <button
              onClick={restartProtocol}
              className="mt-2 flex items-center gap-1.5 text-xs text-red-600 font-medium hover:text-red-700"
            >
              <RotateCcw className="w-3 h-3" />
              {t('lk.chandra.restartBtn')}
            </button>
          </div>
        </div>
      )}

      {/* Progress + stats */}
      {!isComplete && !isMissed && (
        <div className="card-sacred rounded-xl p-5 border border-sacred-gold/20">
          <div className="flex items-center justify-between mb-3">
            <div>
              <p className="text-sm font-semibold text-sacred-gold">{t('lk.chandra.progress')}</p>
              <p className="text-xs text-gray-500">
                {dayLabel(currentDay)} &nbsp;·&nbsp;
                {43 - state.completedDays.length} {t('lk.chandra.daysLeft')}
              </p>
            </div>
            <span className="text-xl font-bold text-sacred-gold">{progressPct}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="h-2 rounded-full bg-sacred-gold transition-all"
              style={{ width: `${progressPct}%` }}
            />
          </div>
          {/* Day mini-grid */}
          <div className="flex flex-wrap gap-1 mt-4">
            {Array.from({ length: 43 }, (_, i) => i + 1).map((d) => {
              const isDone = d <= state.completedDays.length;
              const isCurrent = d === currentDay;
              return (
                <div
                  key={d}
                  className={`w-6 h-6 rounded-md flex items-center justify-center text-xs font-bold ${
                    isDone
                      ? 'bg-sacred-gold text-white'
                      : isCurrent
                        ? 'bg-sacred-gold/30 text-sacred-gold border border-sacred-gold'
                        : 'bg-gray-100 text-gray-400'
                  }`}
                >
                  {d}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Today's task */}
      {todayTask && !isComplete && !isMissed && (
        <div className="card-sacred rounded-xl p-5 border border-sacred-gold/30 bg-sacred-gold/5">
          <div className="flex items-center justify-between mb-3">
            <h3 className="font-sans font-semibold text-sacred-gold flex items-center gap-2">
              <Moon className="w-4 h-4" />
              {t('lk.chandra.todayTask')}
            </h3>
            <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${categoryColors[todayTask.category] || ''}`}>
              {t(`lk.chandra.category${todayTask.category.charAt(0).toUpperCase() + todayTask.category.slice(1)}`)}
            </span>
          </div>
          <p className="text-sm text-cosmic-text leading-relaxed mb-4">
            {isHi ? todayTask.hi : todayTask.en}
          </p>
          {isTodayDone ? (
            <div className="flex items-center gap-2 text-green-600 text-sm font-medium">
              <CheckCircle2 className="w-4 h-4" />
              {isHi ? 'आज का दिन पूर्ण हो गया!' : "Today's day marked complete!"}
            </div>
          ) : (
            <button
              onClick={markDayDone}
              className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-sacred-gold text-white font-medium text-sm hover:bg-sacred-gold-dark transition-all"
            >
              <CheckCircle2 className="w-4 h-4" />
              {t('lk.chandra.markDone')}
            </button>
          )}
        </div>
      )}

      {/* Journal */}
      <div className="card-sacred rounded-xl p-5 border border-sacred-gold/20">
        <h3 className="font-sans font-semibold text-sacred-gold mb-4 flex items-center gap-2">
          <BookOpen className="w-4 h-4" />
          {t('lk.chandra.journal')}
        </h3>
        <textarea
          value={journalNote}
          onChange={(e) => setJournalNote(e.target.value)}
          placeholder={t('lk.chandra.journalPlaceholder')}
          rows={3}
          className="w-full px-3 py-2.5 rounded-xl border border-sacred-gold/20 bg-white/40 text-sm text-cosmic-text placeholder:text-gray-400 resize-none focus:outline-none focus:border-sacred-gold/50"
        />
        <button
          onClick={saveEntry}
          disabled={!journalNote.trim()}
          className="mt-2 px-4 py-2 rounded-xl bg-sacred-gold text-white text-sm font-medium hover:bg-sacred-gold-dark disabled:opacity-40 disabled:cursor-not-allowed transition-all"
        >
          {t('lk.chandra.saveEntry')}
        </button>

        {journalEntries.length > 0 ? (
          <div className="mt-4 space-y-3">
            <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide">
              {t('lk.chandra.entries')}
            </p>
            {journalEntries.slice(0, 5).map((entry, idx) => (
              <div key={idx} className="p-3 rounded-xl bg-sacred-gold/5 border border-sacred-gold/10">
                <p className="text-xs text-gray-400 mb-1">{entry.date}</p>
                <p className="text-sm text-cosmic-text/80 leading-snug">{entry.note}</p>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-xs text-gray-400 mt-3 text-center">{t('lk.chandra.noEntries')}</p>
        )}
      </div>
    </div>
  );
}
