import { useState, useMemo, useEffect } from 'react';
import { useTranslation } from '@/lib/i18n';
import type { LalKitabChartData } from './lalkitab-data';
import { PLANETS, REMEDIES } from './lalkitab-data';
import { CheckCircle2, Circle, Flame, BookOpen, RotateCcw } from 'lucide-react';
import { apiFetch } from '@/lib/api';

interface Props {
  chartData: LalKitabChartData;
  kundliId?: string;
}

interface JournalEntry {
  date: string;
  note: string;
}

const STORAGE_KEY = 'lk_tracker_v1';
const JOURNAL_KEY = 'lk_journal_v1';

function todayStr(): string {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

function loadDoneMap(): Record<string, string[]> {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
  } catch {
    return {};
  }
}

function saveDoneMap(m: Record<string, string[]>) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(m));
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

export default function LalKitabRemediesTrackerTab({ chartData, kundliId }: Props) {
  const { t, language } = useTranslation();
  const isHi = language === 'hi';

  const [doneMap, setDoneMap] = useState<Record<string, string[]>>(loadDoneMap);
  const [journalEntries, setJournalEntries] = useState<JournalEntry[]>(loadJournal);
  const [journalNote, setJournalNote] = useState('');
  const today = todayStr();

  // Load from API on mount — API wins for synced data
  useEffect(() => {
    if (!kundliId) return;
    apiFetch(`/api/lalkitab/tracker/${kundliId}`)
      .then((res) => res.json())
      .then((data: { done_map: Record<string, string[]>; journal: JournalEntry[] }) => {
        if (data.done_map) {
          const merged = { ...loadDoneMap(), ...data.done_map };
          setDoneMap(merged);
          saveDoneMap(merged);
        }
        if (data.journal?.length) {
          setJournalEntries(data.journal);
          saveJournal(data.journal);
        }
      })
      .catch(() => {/* silent — localStorage already loaded */});
  }, [kundliId]);

  // Collect all remedies for this chart
  const allRemedies = useMemo(() => {
    const list: { id: string; planet: string; house: number; en: string; hi: string; category: string; type: string }[] = [];
    for (const planet of PLANETS) {
      const house = chartData.planetPositions[planet.key];
      if (!house) continue;
      const planetRemedies = REMEDIES[planet.key]?.[house];
      if (!planetRemedies) continue;
      planetRemedies.forEach((r, idx) => {
        list.push({
          id: `${planet.key}_${house}_${idx}`,
          planet: planet.key,
          house,
          en: r.en,
          hi: r.hi,
          category: r.category,
          type: r.type,
        });
      });
    }
    return list;
  }, [chartData]);

  const todayDone = doneMap[today] || [];

  const toggleDone = (id: string) => {
    // Optimistic localStorage update
    setDoneMap((prev) => {
      const dayList = prev[today] || [];
      const next = dayList.includes(id) ? dayList.filter((x) => x !== id) : [...dayList, id];
      const updated = { ...prev, [today]: next };
      saveDoneMap(updated);
      return updated;
    });

    // Sync to API in background
    if (kundliId) {
      apiFetch(`/api/lalkitab/tracker/${kundliId}/toggle`, {
        method: 'POST',
        body: JSON.stringify({ date: today, remedy_id: id }),
      })
        .then((res) => res.json())
        .then((data: { date: string; completed_ids: string[] }) => {
          // Reconcile with server's authoritative list
          setDoneMap((prev) => {
            const updated = { ...prev, [data.date]: data.completed_ids };
            saveDoneMap(updated);
            return updated;
          });
        })
        .catch(() => {/* keep optimistic state */});
    }
  };

  const resetToday = () => {
    setDoneMap((prev) => {
      const updated = { ...prev, [today]: [] };
      saveDoneMap(updated);
      return updated;
    });
    if (kundliId) {
      // Toggle each done item off on the server
      const todayIds = [...(doneMap[today] || [])];
      todayIds.forEach((id) => {
        apiFetch(`/api/lalkitab/tracker/${kundliId}/toggle`, {
          method: 'POST',
          body: JSON.stringify({ date: today, remedy_id: id }),
        }).catch(() => {});
      });
    }
  };

  // Streak: count consecutive days with at least one done
  const streak = useMemo(() => {
    let count = 0;
    const d = new Date();
    while (true) {
      const key = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
      const done = doneMap[key];
      if (!done || done.length === 0) break;
      count++;
      d.setDate(d.getDate() - 1);
    }
    return count;
  }, [doneMap]);

  // Weekly compliance
  const weeklyCompliance = useMemo(() => {
    let doneCount = 0;
    const d = new Date();
    for (let i = 0; i < 7; i++) {
      const key = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
      if (doneMap[key]?.length) doneCount++;
      d.setDate(d.getDate() - 1);
    }
    return Math.round((doneCount / 7) * 100);
  }, [doneMap]);

  const saveJournalEntry = () => {
    if (!journalNote.trim()) return;
    const entry: JournalEntry = { date: today, note: journalNote.trim() };
    const updated = [entry, ...journalEntries].slice(0, 30);
    setJournalEntries(updated);
    saveJournal(updated);
    setJournalNote('');

    // Sync to API in background
    if (kundliId) {
      apiFetch(`/api/lalkitab/tracker/${kundliId}/journal`, {
        method: 'POST',
        body: JSON.stringify({ date: today, note: entry.note }),
      }).catch(() => {});
    }
  };

  const getPlanetLabel = (key: string) => {
    const p = PLANETS.find((pl) => pl.key === key);
    return p ? (isHi ? p.hi : p.en) : key;
  };

  const categoryBadge: Record<string, string> = {
    daily: 'bg-green-500/10 text-green-700',
    weekly: 'bg-blue-500/10 text-blue-700',
    urgent: 'bg-red-500/10 text-red-600',
    general: 'bg-gray-500/10 text-gray-600',
  };

  if (allRemedies.length === 0) {
    return (
      <div className="text-center py-16 text-gray-500">
        <BookOpen className="w-10 h-10 mx-auto mb-3 opacity-30" />
        <p>{t('lk.tracker.noRemedies')}</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-xl font-sans font-semibold text-sacred-gold flex items-center gap-2 mb-1">
          <Flame className="w-5 h-5" />
          {t('lk.tracker.title')}
        </h2>
        <p className="text-sm text-gray-500">{t('lk.tracker.desc')}</p>
      </div>

      {/* Stats row */}
      <div className="grid grid-cols-3 gap-3">
        <div className="card-sacred rounded-xl p-4 border border-sacred-gold/20 text-center">
          <p className="text-2xl font-bold text-sacred-gold">{streak}</p>
          <p className="text-xs text-gray-500 mt-0.5">{t('lk.tracker.streak')}</p>
          <p className="text-xs text-gray-400">{t('lk.tracker.days')}</p>
        </div>
        <div className="card-sacred rounded-xl p-4 border border-sacred-gold/20 text-center">
          <p className="text-2xl font-bold text-cosmic-text">{weeklyCompliance}%</p>
          <p className="text-xs text-gray-500 mt-0.5">{t('lk.tracker.compliance')}</p>
        </div>
        <div className="card-sacred rounded-xl p-4 border border-sacred-gold/20 text-center">
          <p className="text-2xl font-bold text-green-500">{todayDone.length}</p>
          <p className="text-xs text-gray-500 mt-0.5">{t('lk.tracker.totalDone')}</p>
          <p className="text-xs text-gray-400">{isHi ? 'आज' : 'today'}</p>
        </div>
      </div>

      {/* Today's remedies */}
      <div className="card-sacred rounded-xl p-5 border border-sacred-gold/20">
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-sans font-semibold text-sacred-gold">{t('lk.tracker.todayRemedies')}</h3>
          {todayDone.length > 0 && (
            <button
              onClick={resetToday}
              className="flex items-center gap-1 text-xs text-gray-400 hover:text-gray-600 transition-colors"
            >
              <RotateCcw className="w-3 h-3" />
              {t('lk.tracker.resetDay')}
            </button>
          )}
        </div>
        <div className="space-y-2">
          {allRemedies.map((remedy) => {
            const isDone = todayDone.includes(remedy.id);
            return (
              <button
                key={remedy.id}
                onClick={() => toggleDone(remedy.id)}
                className={`w-full flex items-start gap-3 p-3 rounded-xl border text-left transition-all ${
                  isDone
                    ? 'bg-green-500/8 border-green-300/30'
                    : 'bg-white/30 border-gray-200/40 hover:border-sacred-gold/20 hover:bg-sacred-gold/5'
                }`}
              >
                {isDone ? (
                  <CheckCircle2 className="w-4 h-4 text-green-500 mt-0.5 shrink-0" />
                ) : (
                  <Circle className="w-4 h-4 text-gray-300 mt-0.5 shrink-0" />
                )}
                <div className="flex-1 min-w-0">
                  <p className={`text-sm leading-snug ${isDone ? 'line-through text-gray-400' : 'text-cosmic-text'}`}>
                    {isHi ? remedy.hi : remedy.en}
                  </p>
                  <div className="flex flex-wrap gap-1.5 mt-1">
                    <span className="text-xs text-sacred-gold-dark">
                      {getPlanetLabel(remedy.planet)} {isHi ? `· भाव ${remedy.house}` : `· H${remedy.house}`}
                    </span>
                    <span className={`text-xs px-1.5 py-0.5 rounded-full ${categoryBadge[remedy.category] || ''}`}>
                      {t(`lk.remedies.${remedy.category}`)}
                    </span>
                  </div>
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Journal */}
      <div className="card-sacred rounded-xl p-5 border border-sacred-gold/20">
        <h3 className="font-sans font-semibold text-sacred-gold mb-4 flex items-center gap-2">
          <BookOpen className="w-4 h-4" />
          {t('lk.tracker.journal')}
        </h3>
        <textarea
          value={journalNote}
          onChange={(e) => setJournalNote(e.target.value)}
          placeholder={t('lk.tracker.addNote')}
          rows={3}
          className="w-full px-3 py-2.5 rounded-xl border border-sacred-gold/20 bg-white/40 text-sm text-cosmic-text placeholder:text-gray-400 resize-none focus:outline-none focus:border-sacred-gold/50"
        />
        <button
          onClick={saveJournalEntry}
          disabled={!journalNote.trim()}
          className="mt-2 px-4 py-2 rounded-xl bg-sacred-gold text-white text-sm font-medium hover:bg-sacred-gold-dark disabled:opacity-40 disabled:cursor-not-allowed transition-all"
        >
          {t('lk.tracker.saveNote')}
        </button>

        {/* Journal entries */}
        {journalEntries.length > 0 && (
          <div className="mt-4 space-y-3">
            <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide">
              {t('lk.tracker.journalEntries')}
            </p>
            {journalEntries.slice(0, 5).map((entry, idx) => (
              <div key={idx} className="p-3 rounded-xl bg-sacred-gold/5 border border-sacred-gold/10">
                <p className="text-xs text-gray-400 mb-1">{entry.date}</p>
                <p className="text-sm text-cosmic-text/80 leading-snug">{entry.note}</p>
              </div>
            ))}
          </div>
        )}
        {journalEntries.length === 0 && (
          <p className="text-xs text-gray-400 mt-3 text-center">{t('lk.tracker.noEntries')}</p>
        )}
      </div>
    </div>
  );
}
