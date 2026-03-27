import { useState, useEffect } from 'react';
import { api } from '../lib/api';
import { useAuth } from '../hooks/useAuth';
import {
  Calendar, ChevronLeft, ChevronRight, Sun, Moon, Star, Sparkles,
  Clock, ArrowRight, Compass, Hash, Palette, Activity, Loader2, X
} from 'lucide-react';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface PanchangSummary {
  tithi: { name: string; number: number; paksha: string };
  nakshatra: { name: string; pada: number; lord: string };
  yoga: { name: string; number: number };
  karana: { name: string; number: number };
  sunrise: string;
  sunset: string;
  rahu_kaal?: { start: string; end: string };
  choghadiya?: Array<{ name: string; quality: string; start: string; end: string }>;
}

interface Festival {
  name: string;
  description: string | null;
  category: string | null;
}

interface MuhuratWindow {
  name: string;
  quality: string;
  start: string;
  end: string;
}

interface Transit {
  transiting_planet: string;
  natal_planet: string;
  aspect: string;
  transiting_sign: string;
  natal_sign: string;
  nature: string;
  intensity?: string;
  description: string;
  date?: string;
}

interface CalendarDay {
  day: number;
  date: string;
  day_type: 'festival' | 'auspicious' | 'inauspicious' | 'neutral';
  panchang: PanchangSummary;
  festivals: Festival[];
  muhurat_windows: MuhuratWindow[];
  personalized_transits?: Transit[];
}

interface MonthData {
  year: number;
  month: number;
  month_name: string;
  days_in_month: number;
  days: CalendarDay[];
}

interface TodaySnapshot {
  date: string;
  day_of_week: string;
  planetary_positions: Record<string, { longitude: number; sign: string; degree: number }>;
  panchang: PanchangSummary;
  festivals: Festival[];
  lucky: { number: number; color: string; direction: string };
  suggested_activities: string[];
  personalized_transits?: Transit[];
}

interface TransitTimeline {
  kundli_id: string;
  days_ahead: number;
  total_transits: number;
  transits: Transit[];
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

const DAY_TYPE_COLORS: Record<string, string> = {
  festival: 'bg-sacred-gold/20 border-sacred-gold/50 text-sacred-gold',
  auspicious: 'bg-green-500/15 border-green-500/40 text-green-400',
  inauspicious: 'bg-red-500/15 border-red-500/40 text-red-400',
  neutral: 'bg-cosmic-bg border-sacred-gold/10 text-cosmic-text',
};

const DAY_TYPE_DOT: Record<string, string> = {
  festival: 'bg-sacred-gold',
  auspicious: 'bg-green-400',
  inauspicious: 'bg-red-400',
  neutral: 'bg-cosmic-text/30',
};

const PLANET_COLORS: Record<string, string> = {
  Sun: 'text-yellow-400',
  Moon: 'text-slate-200',
  Mars: 'text-red-400',
  Mercury: 'text-green-400',
  Jupiter: 'text-amber-400',
  Venus: 'text-pink-300',
  Saturn: 'text-blue-400',
  Rahu: 'text-purple-400',
  Ketu: 'text-orange-400',
};

const WEEKDAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

function getFirstDayOffset(year: number, month: number): number {
  const d = new Date(year, month - 1, 1);
  return (d.getDay() + 6) % 7; // Monday = 0
}

// ---------------------------------------------------------------------------
// Sub-components
// ---------------------------------------------------------------------------

function TodaySection({ snapshot }: { snapshot: TodaySnapshot | null }) {
  if (!snapshot) {
    return (
      <div className="card-sacred rounded-2xl p-6 border border-sacred-gold/20 animate-pulse">
        <div className="h-6 bg-sacred-gold/10 rounded w-48 mb-4" />
        <div className="h-4 bg-sacred-gold/10 rounded w-full mb-2" />
        <div className="h-4 bg-sacred-gold/10 rounded w-3/4" />
      </div>
    );
  }

  const p = snapshot.panchang;

  return (
    <div className="card-sacred rounded-2xl p-6 border border-sacred-gold/20">
      <div className="flex items-center gap-3 mb-4">
        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-sacred-gold to-sacred-saffron flex items-center justify-center">
          <Sun className="w-5 h-5 text-white" />
        </div>
        <div>
          <h2 className="font-sacred font-bold text-lg text-sacred-gold">Today's Cosmic Snapshot</h2>
          <p className="text-xs text-cosmic-text/60">{snapshot.day_of_week}, {snapshot.date}</p>
        </div>
      </div>

      {/* Festivals */}
      {snapshot.festivals.length > 0 && (
        <div className="mb-4 flex flex-wrap gap-2">
          {snapshot.festivals.map((f, i) => (
            <span key={i} className="px-3 py-1 rounded-full bg-sacred-gold/20 text-sacred-gold text-xs font-medium">
              <Sparkles className="w-3 h-3 inline mr-1" />{f.name}
            </span>
          ))}
        </div>
      )}

      {/* Panchang row */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-4">
        <div className="bg-cosmic-bg/50 rounded-xl p-3 border border-sacred-gold/10">
          <p className="text-[10px] uppercase tracking-wider text-cosmic-text/40 mb-1">Tithi</p>
          <p className="text-sm font-medium text-cosmic-text">{p.tithi.paksha} {p.tithi.name}</p>
        </div>
        <div className="bg-cosmic-bg/50 rounded-xl p-3 border border-sacred-gold/10">
          <p className="text-[10px] uppercase tracking-wider text-cosmic-text/40 mb-1">Nakshatra</p>
          <p className="text-sm font-medium text-cosmic-text">{p.nakshatra.name} (Pada {p.nakshatra.pada})</p>
        </div>
        <div className="bg-cosmic-bg/50 rounded-xl p-3 border border-sacred-gold/10">
          <p className="text-[10px] uppercase tracking-wider text-cosmic-text/40 mb-1">Sunrise</p>
          <p className="text-sm font-medium text-cosmic-text">{p.sunrise}</p>
        </div>
        <div className="bg-cosmic-bg/50 rounded-xl p-3 border border-sacred-gold/10">
          <p className="text-[10px] uppercase tracking-wider text-cosmic-text/40 mb-1">Sunset</p>
          <p className="text-sm font-medium text-cosmic-text">{p.sunset}</p>
        </div>
      </div>

      {/* Lucky attributes */}
      <div className="grid grid-cols-3 gap-3 mb-4">
        <div className="bg-cosmic-bg/50 rounded-xl p-3 border border-sacred-gold/10 text-center">
          <Hash className="w-4 h-4 mx-auto text-sacred-gold mb-1" />
          <p className="text-[10px] uppercase tracking-wider text-cosmic-text/40">Lucky Number</p>
          <p className="text-lg font-sacred font-bold text-sacred-gold">{snapshot.lucky.number}</p>
        </div>
        <div className="bg-cosmic-bg/50 rounded-xl p-3 border border-sacred-gold/10 text-center">
          <Palette className="w-4 h-4 mx-auto text-sacred-gold mb-1" />
          <p className="text-[10px] uppercase tracking-wider text-cosmic-text/40">Lucky Color</p>
          <p className="text-sm font-medium text-cosmic-text">{snapshot.lucky.color}</p>
        </div>
        <div className="bg-cosmic-bg/50 rounded-xl p-3 border border-sacred-gold/10 text-center">
          <Compass className="w-4 h-4 mx-auto text-sacred-gold mb-1" />
          <p className="text-[10px] uppercase tracking-wider text-cosmic-text/40">Lucky Direction</p>
          <p className="text-sm font-medium text-cosmic-text">{snapshot.lucky.direction}</p>
        </div>
      </div>

      {/* Suggested activities */}
      <div className="mb-4">
        <p className="text-xs uppercase tracking-wider text-cosmic-text/40 mb-2">Suggested Activities</p>
        <div className="flex flex-wrap gap-2">
          {snapshot.suggested_activities.map((a, i) => (
            <span key={i} className="px-3 py-1 rounded-full bg-green-500/10 text-green-400 text-xs border border-green-500/20">
              {a}
            </span>
          ))}
        </div>
      </div>

      {/* Planetary positions */}
      <div>
        <p className="text-xs uppercase tracking-wider text-cosmic-text/40 mb-2">Current Planetary Positions</p>
        <div className="grid grid-cols-3 sm:grid-cols-5 gap-2">
          {Object.entries(snapshot.planetary_positions).map(([name, pos]) => (
            <div key={name} className="bg-cosmic-bg/50 rounded-lg p-2 border border-sacred-gold/10 text-center">
              <p className={`text-xs font-medium ${PLANET_COLORS[name] || 'text-cosmic-text'}`}>{name}</p>
              <p className="text-[10px] text-cosmic-text/60">{pos.sign}</p>
              <p className="text-[10px] text-cosmic-text/40">{pos.degree.toFixed(1)}°</p>
            </div>
          ))}
        </div>
      </div>

      {/* Personalized transits */}
      {snapshot.personalized_transits && snapshot.personalized_transits.length > 0 && (
        <div className="mt-4">
          <p className="text-xs uppercase tracking-wider text-cosmic-text/40 mb-2">Transits Affecting Your Chart</p>
          <div className="space-y-2">
            {snapshot.personalized_transits.slice(0, 5).map((t, i) => (
              <div
                key={i}
                className={`flex items-center gap-2 px-3 py-2 rounded-lg border text-xs ${
                  t.nature === 'favorable'
                    ? 'bg-green-500/10 border-green-500/20 text-green-400'
                    : 'bg-red-500/10 border-red-500/20 text-red-400'
                }`}
              >
                <Activity className="w-3.5 h-3.5 flex-shrink-0" />
                <span>{t.description}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}


function DayDetailPanel({ day, onClose }: { day: CalendarDay; onClose: () => void }) {
  return (
    <div className="card-sacred rounded-2xl p-5 border border-sacred-gold/20 mt-4 animate-in slide-in-from-top-2">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-sacred font-bold text-sacred-gold">
          {new Date(day.date + 'T00:00:00').toLocaleDateString('en-IN', {
            weekday: 'long', year: 'numeric', month: 'long', day: 'numeric',
          })}
        </h3>
        <button onClick={onClose} className="p-1 text-cosmic-text/40 hover:text-sacred-gold transition-colors">
          <X className="w-4 h-4" />
        </button>
      </div>

      {/* Festivals */}
      {day.festivals.length > 0 && (
        <div className="mb-4">
          <p className="text-xs uppercase tracking-wider text-cosmic-text/40 mb-2">Festivals</p>
          {day.festivals.map((f, i) => (
            <div key={i} className="bg-sacred-gold/10 rounded-lg p-3 border border-sacred-gold/20 mb-2">
              <p className="text-sm font-medium text-sacred-gold">{f.name}</p>
              {f.description && <p className="text-xs text-cosmic-text/60 mt-1">{f.description}</p>}
            </div>
          ))}
        </div>
      )}

      {/* Panchang */}
      <div className="mb-4">
        <p className="text-xs uppercase tracking-wider text-cosmic-text/40 mb-2">Panchang</p>
        <div className="grid grid-cols-2 gap-2">
          <div className="bg-cosmic-bg/50 rounded-lg p-2 border border-sacred-gold/10">
            <p className="text-[10px] text-cosmic-text/40">Tithi</p>
            <p className="text-xs font-medium text-cosmic-text">{day.panchang.tithi.paksha} {day.panchang.tithi.name}</p>
          </div>
          <div className="bg-cosmic-bg/50 rounded-lg p-2 border border-sacred-gold/10">
            <p className="text-[10px] text-cosmic-text/40">Nakshatra</p>
            <p className="text-xs font-medium text-cosmic-text">{day.panchang.nakshatra.name}</p>
          </div>
          <div className="bg-cosmic-bg/50 rounded-lg p-2 border border-sacred-gold/10">
            <p className="text-[10px] text-cosmic-text/40">Yoga</p>
            <p className="text-xs font-medium text-cosmic-text">{day.panchang.yoga.name}</p>
          </div>
          <div className="bg-cosmic-bg/50 rounded-lg p-2 border border-sacred-gold/10">
            <p className="text-[10px] text-cosmic-text/40">Karana</p>
            <p className="text-xs font-medium text-cosmic-text">{day.panchang.karana.name}</p>
          </div>
          <div className="bg-cosmic-bg/50 rounded-lg p-2 border border-sacred-gold/10">
            <p className="text-[10px] text-cosmic-text/40">Sunrise</p>
            <p className="text-xs font-medium text-cosmic-text">{day.panchang.sunrise}</p>
          </div>
          <div className="bg-cosmic-bg/50 rounded-lg p-2 border border-sacred-gold/10">
            <p className="text-[10px] text-cosmic-text/40">Sunset</p>
            <p className="text-xs font-medium text-cosmic-text">{day.panchang.sunset}</p>
          </div>
        </div>
      </div>

      {/* Muhurat Windows */}
      {day.muhurat_windows.length > 0 && (
        <div className="mb-4">
          <p className="text-xs uppercase tracking-wider text-cosmic-text/40 mb-2">Auspicious Windows</p>
          <div className="space-y-1">
            {day.muhurat_windows.map((w, i) => (
              <div key={i} className="flex items-center justify-between px-3 py-2 bg-green-500/10 rounded-lg border border-green-500/20">
                <div className="flex items-center gap-2">
                  <Clock className="w-3.5 h-3.5 text-green-400" />
                  <span className="text-xs font-medium text-green-400">{w.name}</span>
                  <span className="text-[10px] text-green-400/60">({w.quality})</span>
                </div>
                <span className="text-xs text-cosmic-text/60">{w.start} - {w.end}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Personalized Transits */}
      {day.personalized_transits && day.personalized_transits.length > 0 && (
        <div>
          <p className="text-xs uppercase tracking-wider text-cosmic-text/40 mb-2">Transits Affecting You</p>
          <div className="space-y-1">
            {day.personalized_transits.map((t, i) => (
              <div
                key={i}
                className={`flex items-center gap-2 px-3 py-2 rounded-lg border text-xs ${
                  t.nature === 'favorable'
                    ? 'bg-green-500/10 border-green-500/20 text-green-400'
                    : 'bg-red-500/10 border-red-500/20 text-red-400'
                }`}
              >
                <Activity className="w-3.5 h-3.5 flex-shrink-0" />
                <span>{t.description}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}


function TransitsTimeline({ transits }: { transits: Transit[] }) {
  if (transits.length === 0) {
    return (
      <div className="card-sacred rounded-2xl p-6 border border-sacred-gold/20 text-center">
        <Star className="w-8 h-8 text-sacred-gold/30 mx-auto mb-2" />
        <p className="text-sm text-cosmic-text/50">No major transits found for the next 30 days.</p>
        <p className="text-xs text-cosmic-text/30 mt-1">Save a kundli to see personalized transit predictions.</p>
      </div>
    );
  }

  return (
    <div className="card-sacred rounded-2xl p-6 border border-sacred-gold/20">
      <h3 className="font-sacred font-bold text-sacred-gold mb-4 flex items-center gap-2">
        <Activity className="w-5 h-5" />
        Upcoming Transits (30 Days)
      </h3>
      <div className="space-y-3">
        {transits.map((t, i) => (
          <div key={i} className="flex items-start gap-3">
            <div className="flex flex-col items-center">
              <div className={`w-3 h-3 rounded-full ${t.nature === 'favorable' ? 'bg-green-400' : 'bg-red-400'}`} />
              {i < transits.length - 1 && <div className="w-0.5 h-8 bg-sacred-gold/10" />}
            </div>
            <div className="flex-1 pb-3">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-xs text-cosmic-text/40">{t.date}</span>
                <span className={`text-[10px] px-2 py-0.5 rounded-full ${
                  t.nature === 'favorable'
                    ? 'bg-green-500/15 text-green-400'
                    : 'bg-red-500/15 text-red-400'
                }`}>
                  {t.nature}
                </span>
              </div>
              <p className="text-sm text-cosmic-text">{t.description}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}


// ---------------------------------------------------------------------------
// Main Component
// ---------------------------------------------------------------------------

export default function CosmicCalendarPage() {
  const { isAuthenticated } = useAuth();
  const today = new Date();
  const [year, setYear] = useState(today.getFullYear());
  const [month, setMonth] = useState(today.getMonth() + 1);
  const [monthData, setMonthData] = useState<MonthData | null>(null);
  const [todaySnapshot, setTodaySnapshot] = useState<TodaySnapshot | null>(null);
  const [transitData, setTransitData] = useState<Transit[]>([]);
  const [selectedDay, setSelectedDay] = useState<CalendarDay | null>(null);
  const [loadingMonth, setLoadingMonth] = useState(true);
  const [loadingToday, setLoadingToday] = useState(true);
  const [loadingTransits, setLoadingTransits] = useState(false);

  useEffect(() => {
    fetchToday();
    fetchTransits();
  }, []);

  useEffect(() => {
    fetchMonth();
  }, [year, month]);

  async function fetchMonth() {
    setLoadingMonth(true);
    setSelectedDay(null);
    try {
      const data = await api.get(`/api/cosmic-calendar/month?year=${year}&month=${month}`);
      setMonthData(data);
    } catch {
      setMonthData(null);
    } finally {
      setLoadingMonth(false);
    }
  }

  async function fetchToday() {
    setLoadingToday(true);
    try {
      const data = await api.get('/api/cosmic-calendar/today');
      setTodaySnapshot(data);
    } catch {
      setTodaySnapshot(null);
    } finally {
      setLoadingToday(false);
    }
  }

  async function fetchTransits() {
    if (!isAuthenticated) return;
    setLoadingTransits(true);
    try {
      // Get user's first kundli
      const kundlis = await api.get('/api/kundli');
      const list = kundlis.kundlis || kundlis || [];
      if (Array.isArray(list) && list.length > 0) {
        const kundliId = list[0].id;
        const data = await api.get(`/api/cosmic-calendar/transits?kundli_id=${kundliId}`);
        setTransitData(data.transits || []);
      }
    } catch {
      setTransitData([]);
    } finally {
      setLoadingTransits(false);
    }
  }

  function goToPrevMonth() {
    if (month === 1) {
      setMonth(12);
      setYear(year - 1);
    } else {
      setMonth(month - 1);
    }
  }

  function goToNextMonth() {
    if (month === 12) {
      setMonth(1);
      setYear(year + 1);
    } else {
      setMonth(month + 1);
    }
  }

  function goToToday() {
    setYear(today.getFullYear());
    setMonth(today.getMonth() + 1);
  }

  const todayDateStr = today.toISOString().split('T')[0];
  const firstDayOffset = getFirstDayOffset(year, month);

  return (
    <div className="min-h-screen bg-cosmic-bg pt-28 pb-16 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Page header */}
        <div className="text-center mb-8">
          <h1 className="font-sacred text-3xl sm:text-4xl font-bold text-sacred-gold mb-2">
            Cosmic Calendar
          </h1>
          <p className="text-cosmic-text/60 text-sm max-w-xl mx-auto">
            Your personalized Vedic calendar with panchang, festivals, auspicious timings, and planetary transits.
          </p>
        </div>

        <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
          {/* Left column: Today's snapshot */}
          <div className="xl:col-span-1 space-y-6">
            {loadingToday ? (
              <div className="card-sacred rounded-2xl p-6 border border-sacred-gold/20 flex items-center justify-center min-h-[200px]">
                <Loader2 className="w-6 h-6 text-sacred-gold animate-spin" />
              </div>
            ) : (
              <TodaySection snapshot={todaySnapshot} />
            )}

            {/* Transits Timeline */}
            {isAuthenticated && (
              loadingTransits ? (
                <div className="card-sacred rounded-2xl p-6 border border-sacred-gold/20 flex items-center justify-center min-h-[100px]">
                  <Loader2 className="w-6 h-6 text-sacred-gold animate-spin" />
                </div>
              ) : (
                <TransitsTimeline transits={transitData} />
              )
            )}
          </div>

          {/* Right column: Calendar grid */}
          <div className="xl:col-span-2">
            <div className="card-sacred rounded-2xl p-4 sm:p-6 border border-sacred-gold/20">
              {/* Month navigation */}
              <div className="flex items-center justify-between mb-6">
                <button
                  onClick={goToPrevMonth}
                  className="p-2 rounded-lg hover:bg-sacred-gold/10 text-cosmic-text/60 hover:text-sacred-gold transition-colors"
                >
                  <ChevronLeft className="w-5 h-5" />
                </button>

                <div className="flex items-center gap-3">
                  <h2 className="font-sacred font-bold text-xl text-sacred-gold">
                    {monthData?.month_name || ''} {year}
                  </h2>
                  {(year !== today.getFullYear() || month !== today.getMonth() + 1) && (
                    <button
                      onClick={goToToday}
                      className="px-3 py-1 rounded-full text-xs btn-sacred"
                    >
                      Today
                    </button>
                  )}
                </div>

                <button
                  onClick={goToNextMonth}
                  className="p-2 rounded-lg hover:bg-sacred-gold/10 text-cosmic-text/60 hover:text-sacred-gold transition-colors"
                >
                  <ChevronRight className="w-5 h-5" />
                </button>
              </div>

              {/* Legend */}
              <div className="flex flex-wrap gap-3 mb-4">
                <div className="flex items-center gap-1.5">
                  <div className="w-2.5 h-2.5 rounded-full bg-sacred-gold" />
                  <span className="text-[10px] text-cosmic-text/50">Festival</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <div className="w-2.5 h-2.5 rounded-full bg-green-400" />
                  <span className="text-[10px] text-cosmic-text/50">Auspicious</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <div className="w-2.5 h-2.5 rounded-full bg-red-400" />
                  <span className="text-[10px] text-cosmic-text/50">Inauspicious</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <div className="w-2.5 h-2.5 rounded-full bg-cosmic-text/30" />
                  <span className="text-[10px] text-cosmic-text/50">Neutral</span>
                </div>
              </div>

              {/* Weekday headers */}
              <div className="grid grid-cols-7 gap-1 mb-1">
                {WEEKDAYS.map((d) => (
                  <div key={d} className="text-center text-[10px] uppercase tracking-wider text-cosmic-text/40 py-1 font-medium">
                    {d}
                  </div>
                ))}
              </div>

              {/* Calendar grid */}
              {loadingMonth ? (
                <div className="flex items-center justify-center min-h-[300px]">
                  <Loader2 className="w-8 h-8 text-sacred-gold animate-spin" />
                </div>
              ) : monthData ? (
                <div className="grid grid-cols-7 gap-1">
                  {/* Empty cells for offset */}
                  {Array.from({ length: firstDayOffset }).map((_, i) => (
                    <div key={`empty-${i}`} className="aspect-square" />
                  ))}

                  {/* Day cells */}
                  {monthData.days.map((day) => {
                    const isToday = day.date === todayDateStr;
                    const isSelected = selectedDay?.date === day.date;
                    return (
                      <button
                        key={day.day}
                        onClick={() => setSelectedDay(isSelected ? null : day)}
                        className={`aspect-square rounded-lg border p-1 sm:p-1.5 flex flex-col items-center justify-start transition-all text-left hover:scale-105 ${
                          DAY_TYPE_COLORS[day.day_type]
                        } ${isToday ? 'ring-2 ring-sacred-gold ring-offset-1 ring-offset-cosmic-bg' : ''} ${
                          isSelected ? 'scale-105 shadow-lg shadow-sacred-gold/20' : ''
                        }`}
                      >
                        <span className={`text-xs sm:text-sm font-medium ${isToday ? 'text-sacred-gold font-bold' : ''}`}>
                          {day.day}
                        </span>
                        <div className="flex items-center gap-0.5 mt-0.5">
                          <div className={`w-1.5 h-1.5 rounded-full ${DAY_TYPE_DOT[day.day_type]}`} />
                          {day.festivals.length > 0 && (
                            <Sparkles className="w-2.5 h-2.5 text-sacred-gold" />
                          )}
                        </div>
                        <p className="text-[8px] sm:text-[9px] text-cosmic-text/40 truncate w-full text-center mt-0.5 hidden sm:block">
                          {day.panchang.tithi.name}
                        </p>
                      </button>
                    );
                  })}
                </div>
              ) : (
                <div className="text-center py-12 text-cosmic-text/50 text-sm">
                  Failed to load calendar data.
                </div>
              )}

              {/* Selected day detail panel */}
              {selectedDay && (
                <DayDetailPanel day={selectedDay} onClose={() => setSelectedDay(null)} />
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
