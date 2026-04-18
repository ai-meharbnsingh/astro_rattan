import { useState, useMemo, useEffect } from 'react';
import { useTranslation } from '@/lib/i18n';
import { Moon, CheckCircle2, RotateCcw, BookOpen, Play, AlertTriangle } from 'lucide-react';
import { apiFetch } from '@/lib/api';
import { pickLang } from './safe-render';

interface JournalEntry {
  date: string;
  note: string;
}

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

interface ChandraTask {
  day: number;
  en: string;
  hi: string;
  category: 'action' | 'donation' | 'meditation' | 'fasting' | 'mantra';
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

  const [state, setState] = useState<ProtocolState>({ startDate: null, completedDays: [] });
  const [tasks, setTasks] = useState<ChandraTask[]>([]);
  const [journalEntries, setJournalEntries] = useState<JournalEntry[]>([]);
  const [journalNote, setJournalNote] = useState('');
  const [syncError, setSyncError] = useState(false);

  const today = todayStr();

  // Load from API on mount — API wins for cross-device sync
  useEffect(() => {
    apiFetch('/api/lalkitab/chandra')
      .then((data: any) => {
        const apiState: ProtocolState = {
          startDate: data?.start_date ?? null,
          completedDays: Array.isArray(data?.completed_days) ? data.completed_days : [],
        };
        setState(apiState);
        setTasks(Array.isArray(data?.tasks) ? data.tasks : []);
        setJournalEntries(Array.isArray(data?.journal) ? data.journal : []);
        setSyncError(false);
      })
      .catch((err) => {
        console.error('Chandra Chaalana sync failed:', err);
        setSyncError(true);
      });
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

  const todayTask = tasks.find((x) => x.day === currentDay);
  const isTodayDone = state.completedDays.includes(today);

  const reload = () => {
    apiFetch('/api/lalkitab/chandra')
      .then((data: any) => {
        setState({
          startDate: data?.start_date ?? null,
          completedDays: Array.isArray(data?.completed_days) ? data.completed_days : [],
        });
        setTasks(Array.isArray(data?.tasks) ? data.tasks : []);
        setJournalEntries(Array.isArray(data?.journal) ? data.journal : []);
        setSyncError(false);
      })
      .catch((err) => {
        console.error('Chandra Chaalana reload failed:', err);
        setSyncError(true);
      });
  };

  const startProtocol = () => {
    apiFetch('/api/lalkitab/chandra/start', {
      method: 'POST',
      body: JSON.stringify({ start_date: today }),
    }).then(() => reload());
  };

  const restartProtocol = () => {
    apiFetch('/api/lalkitab/chandra/start', {
      method: 'POST',
      body: JSON.stringify({ start_date: today }),
    }).then(() => reload())
      .catch((err) => {
        console.error('Chandra Chaalana restart sync failed:', err);
        setSyncError(true);
      });
  };

  const markDayDone = () => {
    if (isTodayDone) return;
    apiFetch('/api/lalkitab/chandra/mark-done', {
      method: 'POST',
      body: JSON.stringify({ date: today }),
    })
      .then((data: any) => {
        const reconciled: ProtocolState = {
          ...state,
          completedDays: Array.isArray(data?.completed_days) ? data.completed_days : state.completedDays,
        };
        setState(reconciled);
        setSyncError(false);
      })
      .catch((err) => {
        console.error('Chandra Chaalana mark-done sync failed:', err);
        setSyncError(true);
      });
  };

  const saveEntry = () => {
    if (!journalNote.trim()) return;
    apiFetch('/api/lalkitab/chandra/journal', {
      method: 'POST',
      body: JSON.stringify({ date: today, note: journalNote.trim() }),
    })
      .then(() => { setJournalNote(''); reload(); })
      .catch((err) => {
        console.error('Chandra Chaalana journal sync failed:', err);
        setSyncError(true);
      });
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
        {syncError && (
          <div className="p-2 mb-2 bg-amber-50 border border-amber-200 rounded text-xs text-amber-800">
            {isHi ? 'सर्वर से सिंक नहीं हो सका' : 'Could not sync with server'}
          </div>
        )}
        <div>
          <h2 className="text-xl font-sans font-semibold text-sacred-gold flex items-center gap-2 mb-1">
            <Moon className="w-5 h-5" />
            {t('lk.43DayProtocol')}
          </h2>
          <p className="text-sm text-gray-500">
            {isHi
              ? '43-दिवसीय आध्यात्मिक अभ्यास ट्रैकर — दैनिक प्रतिबद्धताओं को दर्ज करें'
              : '43-day spiritual practice tracker — record daily commitments'}
          </p>
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

        {/* Preview first 7 days (from backend tasks) */}
        {tasks.length > 0 && (
          <div className="card-sacred rounded-xl p-5 border border-sacred-gold/20">
            <h3 className="font-sans font-semibold text-sacred-gold mb-4">
              {t('auto.previewFirst7Days')}
            </h3>
            <div className="space-y-2">
              {tasks.slice(0, 7).map((task) => (
                <div key={task.day} className="flex items-start gap-3 p-3 rounded-xl bg-sacred-gold/5">
                  <span className="text-xs font-bold text-sacred-gold min-w-[40px]">
                    {isHi ? `दिन ${task.day}` : `Day ${task.day}`}
                  </span>
                  <p className="text-xs text-foreground/80 leading-snug">
                    {pickLang(task, isHi)}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {syncError && (
        <div className="p-2 mb-2 bg-amber-50 border border-amber-200 rounded text-xs text-amber-800">
          {isHi ? 'सर्वर से सिंक नहीं हो सका — स्थानीय डेटा उपयोग में' : 'Could not sync with server — using local data'}
        </div>
      )}
      {/* Header */}
      <div>
        <h2 className="text-xl font-sans font-semibold text-sacred-gold flex items-center gap-2 mb-1">
          <Moon className="w-5 h-5" />
          {t('lk.43DayProtocol')}
        </h2>
        <p className="text-sm text-gray-500">
          {isHi
            ? '43-दिवसीय आध्यात्मिक अभ्यास ट्रैकर — दैनिक प्रतिबद्धताओं को दर्ज करें'
            : '43-day spiritual practice tracker — record daily commitments'}
        </p>
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
              {t(`lk.chandra.category${(todayTask.category || 'general').charAt(0).toUpperCase() + (todayTask.category || 'general').slice(1)}`)}
            </span>
          </div>
          <p className="text-sm text-foreground leading-relaxed mb-4">
            {pickLang(todayTask, isHi)}
          </p>
          {isTodayDone ? (
            <div className="flex items-center gap-2 text-green-600 text-sm font-medium">
              <CheckCircle2 className="w-4 h-4" />
              {t('lk.chandra.toast.complete')}
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
          className="w-full px-3 py-2.5 rounded-xl border border-sacred-gold/20 bg-white/40 text-sm text-foreground placeholder:text-gray-400 resize-none focus:outline-none focus:border-sacred-gold/50"
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
                <p className="text-sm text-foreground/80 leading-snug">{pickLang(entry.note, isHi)}</p>
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
