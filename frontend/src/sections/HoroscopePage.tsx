import { useState, useEffect, useRef } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Calendar, Loader2, Sun, Moon, Star, Sparkles, Users, Orbit } from 'lucide-react';
import { api } from '@/lib/api';
import { useTranslation } from '@/lib/i18n';
import DailyTab from '@/components/horoscope/DailyTab';
import WeeklyTab from '@/components/horoscope/WeeklyTab';
import AllSignsTab from '@/components/horoscope/AllSignsTab';
import TransitInsightsTab from '@/components/horoscope/TransitInsightsTab';

// ============================================================
// Zodiac sign data
// ============================================================
const SIGNS = [
  { id: 'aries', en: 'Aries', hi: 'मेष', emoji: '\u2648' },
  { id: 'taurus', en: 'Taurus', hi: 'वृषभ', emoji: '\u2649' },
  { id: 'gemini', en: 'Gemini', hi: 'मिथुन', emoji: '\u264A' },
  { id: 'cancer', en: 'Cancer', hi: 'कर्क', emoji: '\u264B' },
  { id: 'leo', en: 'Leo', hi: 'सिंह', emoji: '\u264C' },
  { id: 'virgo', en: 'Virgo', hi: 'कन्या', emoji: '\u264D' },
  { id: 'libra', en: 'Libra', hi: 'तुला', emoji: '\u264E' },
  { id: 'scorpio', en: 'Scorpio', hi: 'वृश्चिक', emoji: '\u264F' },
  { id: 'sagittarius', en: 'Sagittarius', hi: 'धनु', emoji: '\u2650' },
  { id: 'capricorn', en: 'Capricorn', hi: 'मकर', emoji: '\u2651' },
  { id: 'aquarius', en: 'Aquarius', hi: 'कुंभ', emoji: '\u2652' },
  { id: 'pisces', en: 'Pisces', hi: 'मीन', emoji: '\u2653' },
];

// Helper: local date as YYYY-MM-DD
const getLocalDateString = () => {
  const now = new Date();
  return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;
};

export default function HoroscopePage() {
  const { t, language } = useTranslation();
  const sectionRef = useRef<HTMLDivElement>(null);

  const [selectedDate, setSelectedDate] = useState(() => getLocalDateString());
  const [selectedSign, setSelectedSign] = useState('aries');
  const [activeTab, setActiveTab] = useState('daily');

  // Data states
  const [dailyData, setDailyData] = useState<any>(null);
  const [weeklyData, setWeeklyData] = useState<any>(null);
  const [allSignsData, setAllSignsData] = useState<any>(null);
  const [transitData, setTransitData] = useState<any>(null);

  // Loading states
  const [dailyLoading, setDailyLoading] = useState(false);
  const [weeklyLoading, setWeeklyLoading] = useState(false);
  const [allSignsLoading, setAllSignsLoading] = useState(false);
  const [transitLoading, setTransitLoading] = useState(false);

  const [currentTime, setCurrentTime] = useState(new Date());

  // Live clock
  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  // Fetch daily horoscope when sign or date changes
  useEffect(() => {
    let cancelled = false;
    const fetchDaily = async () => {
      setDailyLoading(true);
      try {
        const data = await api.get(`/api/horoscope/daily?sign=${selectedSign}&date=${selectedDate}`);
        if (!cancelled && data) setDailyData(data);
      } catch { /* keep previous */ }
      finally { if (!cancelled) setDailyLoading(false); }
    };
    fetchDaily();
    return () => { cancelled = true; };
  }, [selectedSign, selectedDate]);

  // Fetch weekly when sign changes
  useEffect(() => {
    let cancelled = false;
    const fetchWeekly = async () => {
      setWeeklyLoading(true);
      try {
        const data = await api.get(`/api/horoscope/weekly?sign=${selectedSign}`);
        if (!cancelled && data) setWeeklyData(data);
      } catch { /* keep previous */ }
      finally { if (!cancelled) setWeeklyLoading(false); }
    };
    fetchWeekly();
    return () => { cancelled = true; };
  }, [selectedSign]);

  // Fetch all signs on mount and date change
  useEffect(() => {
    let cancelled = false;
    const fetchAll = async () => {
      setAllSignsLoading(true);
      try {
        const data = await api.get(`/api/horoscope/all?period=daily&date=${selectedDate}`);
        if (!cancelled && data) setAllSignsData(data);
      } catch { /* keep previous */ }
      finally { if (!cancelled) setAllSignsLoading(false); }
    };
    fetchAll();
    return () => { cancelled = true; };
  }, [selectedDate]);

  // Fetch transit insights on mount
  useEffect(() => {
    let cancelled = false;
    const fetchTransits = async () => {
      setTransitLoading(true);
      try {
        const data = await api.get('/api/horoscope/transits');
        if (!cancelled && data) setTransitData(data);
      } catch { /* keep previous */ }
      finally { if (!cancelled) setTransitLoading(false); }
    };
    fetchTransits();
    return () => { cancelled = true; };
  }, []);

  // Handle sign selection from AllSignsTab
  const handleSelectFromAll = (sign: string) => {
    setSelectedSign(sign);
    setActiveTab('daily');
  };

  const dateDisplay = new Date(selectedDate + 'T12:00:00').toLocaleDateString(
    language === 'hi' ? 'hi-IN' : 'en-IN',
    { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' },
  );

  return (
    <section ref={sectionRef} id="horoscope" className="relative pt-32 pb-8 bg-transparent">
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

        {/* Date + Time Header */}
        <div className="rounded-xl border border-cosmic-border bg-cosmic-card p-3 mb-4">
          <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
            <span className="font-semibold text-cosmic-text">{dateDisplay}</span>
            <span className="text-sm text-cosmic-text-secondary">{currentTime.toLocaleTimeString(language === 'hi' ? 'hi-IN' : 'en-IN')}</span>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            <input
              type="date"
              value={selectedDate}
              onChange={(e) => setSelectedDate(e.target.value)}
              className="w-full px-2 py-1.5 rounded-lg bg-white border border-cosmic-border text-cosmic-text text-sm focus:border-sacred-gold focus:outline-none"
            />
            <select
              value={selectedSign}
              onChange={(e) => setSelectedSign(e.target.value)}
              className="w-full px-2 py-1.5 rounded-lg bg-white border border-cosmic-border text-cosmic-text text-sm focus:border-sacred-gold focus:outline-none"
            >
              {SIGNS.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.emoji} {language === 'hi' ? s.hi : s.en}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Sign Quick-Select Bar */}
        <div className="rounded-xl border border-cosmic-border bg-cosmic-card p-2 mb-4 overflow-x-auto">
          <div className="flex gap-1 min-w-max">
            {SIGNS.map((s) => (
              <button
                key={s.id}
                onClick={() => setSelectedSign(s.id)}
                className={`flex flex-col items-center gap-0.5 px-2.5 py-1.5 rounded-lg text-xs transition-all whitespace-nowrap ${
                  selectedSign === s.id
                    ? 'bg-sacred-gold text-white shadow-sm'
                    : 'text-cosmic-text-secondary hover:bg-sacred-gold/10'
                }`}
              >
                <span className="text-lg leading-none">{s.emoji}</span>
                <span className="text-[10px]">{language === 'hi' ? s.hi : s.en}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Tab Navigation */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-4 gap-1 h-auto p-1 bg-cosmic-card rounded-xl">
            {[
              { id: 'daily', label: language === 'hi' ? 'दैनिक' : 'Daily', icon: Sun },
              { id: 'weekly', label: language === 'hi' ? 'साप्ताहिक' : 'Weekly', icon: Calendar },
              { id: 'all', label: language === 'hi' ? 'सभी राशि' : 'All Signs', icon: Users },
              { id: 'transits', label: language === 'hi' ? 'गोचर' : 'Transits', icon: Orbit },
            ].map(tab => (
              <TabsTrigger key={tab.id} value={tab.id} className="min-w-0 flex flex-col items-center gap-0.5 py-2 px-1 text-xs data-[state=active]:bg-sacred-gold data-[state=active]:text-white rounded-lg">
                <tab.icon className="w-4 h-4" />
                <span className="hidden sm:block">{tab.label}</span>
              </TabsTrigger>
            ))}
          </TabsList>

          <div className="mt-4">
            <TabsContent value="daily">
              <DailyTab data={dailyData} loading={dailyLoading} language={language} t={t} />
            </TabsContent>
            <TabsContent value="weekly">
              <WeeklyTab data={weeklyData} loading={weeklyLoading} language={language} t={t} />
            </TabsContent>
            <TabsContent value="all">
              <AllSignsTab data={allSignsData} loading={allSignsLoading} language={language} t={t} onSelectSign={handleSelectFromAll} />
            </TabsContent>
            <TabsContent value="transits">
              <TransitInsightsTab data={transitData} loading={transitLoading} language={language} t={t} />
            </TabsContent>
          </div>
        </Tabs>
      </div>
    </section>
  );
}
