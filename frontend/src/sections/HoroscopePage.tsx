import { useState, useEffect, useRef } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Calendar, CalendarDays, CalendarCheck, Sun, Star, Users, Orbit, ChevronDown } from 'lucide-react';
import { api } from '@/lib/api';
import { useTranslation } from '@/lib/i18n';
import { useAuth } from '@/hooks/useAuth';
import DailyTab from '@/components/horoscope/DailyTab';
import WeeklyTab from '@/components/horoscope/WeeklyTab';
import MonthlyTab from '@/components/horoscope/MonthlyTab';
import YearlyTab from '@/components/horoscope/YearlyTab';
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

const BIRTH_PARAMS_KEY = 'astrorattan_birth_params';

interface BirthParams {
  birth_date: string;
  birth_time: string;
  birth_lat: string;
  birth_lon: string;
}

function loadBirthParams(): BirthParams | null {
  try {
    const raw = localStorage.getItem(BIRTH_PARAMS_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

export default function HoroscopePage() {
  const { t, language } = useTranslation();
  const { user } = useAuth();
  const sectionRef = useRef<HTMLDivElement>(null);

  const [selectedDate, setSelectedDate] = useState(() => getLocalDateString());
  const [selectedSign, setSelectedSign] = useState('aries');
  const [activeTab, setActiveTab] = useState('daily');
  const [showPersonalize, setShowPersonalize] = useState(false);
  const [birthParams, setBirthParams] = useState<BirthParams>(() => {
    const saved = loadBirthParams();
    if (saved) return saved;
    return { birth_date: user?.date_of_birth || '', birth_time: '', birth_lat: '', birth_lon: '' };
  });

  // Data states
  const [dailyData, setDailyData] = useState<any>(null);
  const [weeklyData, setWeeklyData] = useState<any>(null);
  const [monthlyData, setMonthlyData] = useState<any>(null);
  const [yearlyData, setYearlyData] = useState<any>(null);
  const [tomorrowData, setTomorrowData] = useState<any>(null);
  const [allSignsData, setAllSignsData] = useState<any>(null);
  const [transitData, setTransitData] = useState<any>(null);

  // Loading states
  const [dailyLoading, setDailyLoading] = useState(false);
  const [tomorrowLoading, setTomorrowLoading] = useState(false);
  const [weeklyLoading, setWeeklyLoading] = useState(false);
  const [monthlyLoading, setMonthlyLoading] = useState(false);
  const [yearlyLoading, setYearlyLoading] = useState(false);
  const [allSignsLoading, setAllSignsLoading] = useState(false);
  const [transitLoading, setTransitLoading] = useState(false);

  const [currentTime, setCurrentTime] = useState(new Date());
  const [detectedSign, setDetectedSign] = useState<{ moon_sign: string; moon_sign_hindi: string; nakshatra: string } | null>(null);

  // Persist birth params to localStorage
  const saveBirthParams = (params: BirthParams) => {
    setBirthParams(params);
    localStorage.setItem(BIRTH_PARAMS_KEY, JSON.stringify(params));
  };

  // Auto-detect Moon sign (Rashi) when birth date + coords are available
  useEffect(() => {
    const { birth_date, birth_lat, birth_lon, birth_time } = birthParams;
    if (!birth_date || !birth_lat || !birth_lon) { setDetectedSign(null); return; }
    let cancelled = false;
    const params = new URLSearchParams({ birth_date, birth_lat, birth_lon });
    if (birth_time) params.append('birth_time', birth_time.length === 5 ? birth_time + ':00' : birth_time);
    api.get(`/api/horoscope/natal-sign?${params.toString()}`)
      .then((data: any) => { if (!cancelled && data?.moon_sign) setDetectedSign(data); })
      .catch(() => {});
    return () => { cancelled = true; };
  }, [birthParams.birth_date, birthParams.birth_lat, birthParams.birth_lon, birthParams.birth_time]);

  // Build birth query string (only when all required fields are filled)
  const birthQuery = (() => {
    const { birth_date, birth_time, birth_lat, birth_lon } = birthParams;
    if (!birth_date || !birth_lat || !birth_lon) return '';
    const params = new URLSearchParams({ birth_date });
    if (birth_time) params.append('birth_time', birth_time.length === 5 ? birth_time + ':00' : birth_time);
    params.append('birth_lat', birth_lat);
    params.append('birth_lon', birth_lon);
    return '&' + params.toString();
  })();

  // Live clock
  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  // Fetch daily horoscope when sign, date, or birth params change
  useEffect(() => {
    let cancelled = false;
    const fetchDaily = async () => {
      setDailyLoading(true);
      try {
        const data = await api.get(`/api/horoscope/daily?sign=${selectedSign}&date=${selectedDate}${birthQuery}`);
        if (!cancelled && data) setDailyData(data);
      } catch { /* keep previous */ }
      finally { if (!cancelled) setDailyLoading(false); }
    };
    fetchDaily();
    return () => { cancelled = true; };
  }, [selectedSign, selectedDate, birthQuery]);

  // Fetch tomorrow's horoscope when sign or birth params change
  useEffect(() => {
    let cancelled = false;
    const fetchTomorrow = async () => {
      setTomorrowLoading(true);
      try {
        const data = await api.get(`/api/horoscope/tomorrow?sign=${selectedSign}${birthQuery}`);
        if (!cancelled && data) setTomorrowData(data);
      } catch { /* keep previous */ }
      finally { if (!cancelled) setTomorrowLoading(false); }
    };
    fetchTomorrow();
    return () => { cancelled = true; };
  }, [selectedSign, birthQuery]);

  // Fetch weekly when sign or birth params change
  useEffect(() => {
    let cancelled = false;
    const fetchWeekly = async () => {
      setWeeklyLoading(true);
      try {
        const data = await api.get(`/api/horoscope/weekly?sign=${selectedSign}${birthQuery}`);
        if (!cancelled && data) setWeeklyData(data);
      } catch { /* keep previous */ }
      finally { if (!cancelled) setWeeklyLoading(false); }
    };
    fetchWeekly();
    return () => { cancelled = true; };
  }, [selectedSign, birthQuery]);

  // Fetch monthly when sign or birth params change
  useEffect(() => {
    let cancelled = false;
    const fetchMonthly = async () => {
      setMonthlyLoading(true);
      try {
        const data = await api.get(`/api/horoscope/monthly?sign=${selectedSign}${birthQuery}`);
        if (!cancelled && data) setMonthlyData(data);
      } catch { /* keep previous */ }
      finally { if (!cancelled) setMonthlyLoading(false); }
    };
    fetchMonthly();
    return () => { cancelled = true; };
  }, [selectedSign, birthQuery]);

  // Fetch yearly when sign or birth params change
  useEffect(() => {
    let cancelled = false;
    const fetchYearly = async () => {
      setYearlyLoading(true);
      try {
        const data = await api.get(`/api/horoscope/yearly?sign=${selectedSign}${birthQuery}`);
        if (!cancelled && data) setYearlyData(data);
      } catch { /* keep previous */ }
      finally { if (!cancelled) setYearlyLoading(false); }
    };
    fetchYearly();
    return () => { cancelled = true; };
  }, [selectedSign, birthQuery]);

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
        <div className="rounded-xl border border-border bg-card p-3 mb-4">
          <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
            <span className="font-semibold text-foreground">{dateDisplay}</span>
            <span className="text-sm text-muted-foreground">{currentTime.toLocaleTimeString(language === 'hi' ? 'hi-IN' : 'en-IN')}</span>
          </div>
          <input
            type="date"
            value={selectedDate}
            onChange={(e) => setSelectedDate(e.target.value)}
            className="input-sacred"
          />
        </div>

        {/* Personalize with birth data */}
        <div className="rounded-xl border border-border bg-card mb-4 overflow-hidden">
          <button
            onClick={() => setShowPersonalize(v => !v)}
            className="w-full flex items-center justify-between px-4 py-2.5 text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
          >
            <span className="flex items-center gap-2">
              <Star className="w-4 h-4 text-sacred-gold" />
              {birthQuery ? (language === 'hi' ? 'व्यक्तिगत राशिफल (जन्म डेटा सक्रिय)' : 'Personalized Reading (birth data active)') : (language === 'hi' ? 'व्यक्तिगत राशिफल जोड़ें' : 'Personalize with Birth Data')}
            </span>
            <ChevronDown className={`w-4 h-4 transition-transform ${showPersonalize ? 'rotate-180' : ''}`} />
          </button>
          {showPersonalize && (
            <div className="px-4 pb-4 grid grid-cols-2 sm:grid-cols-4 gap-3 border-t border-border pt-3">
              <div>
                <label className="block text-xs text-muted-foreground mb-1">{language === 'hi' ? 'जन्म तिथि' : 'Birth Date'}</label>
                <input
                  type="date"
                  value={birthParams.birth_date}
                  onChange={e => saveBirthParams({ ...birthParams, birth_date: e.target.value })}
                  className="input-sacred"
                />
              </div>
              <div>
                <label className="block text-xs text-muted-foreground mb-1">{language === 'hi' ? 'जन्म समय' : 'Birth Time'}</label>
                <input
                  type="time"
                  value={birthParams.birth_time}
                  onChange={e => saveBirthParams({ ...birthParams, birth_time: e.target.value })}
                  className="input-sacred"
                />
              </div>
              <div>
                <label className="block text-xs text-muted-foreground mb-1">{language === 'hi' ? 'अक्षांश' : 'Latitude'}</label>
                <input
                  type="number"
                  step="0.0001"
                  placeholder="28.6139"
                  value={birthParams.birth_lat}
                  onChange={e => saveBirthParams({ ...birthParams, birth_lat: e.target.value })}
                  className="input-sacred"
                />
              </div>
              <div>
                <label className="block text-xs text-muted-foreground mb-1">{language === 'hi' ? 'देशांतर' : 'Longitude'}</label>
                <input
                  type="number"
                  step="0.0001"
                  placeholder="77.2090"
                  value={birthParams.birth_lon}
                  onChange={e => saveBirthParams({ ...birthParams, birth_lon: e.target.value })}
                  className="input-sacred"
                />
              </div>
              {birthQuery && (
                <div className="col-span-2 sm:col-span-4">
                  <button
                    onClick={() => saveBirthParams({ birth_date: '', birth_time: '', birth_lat: '', birth_lon: '' })}
                    className="text-xs text-muted-foreground hover:text-destructive transition-colors"
                  >
                    {language === 'hi' ? 'साफ़ करें' : 'Clear personalization'}
                  </button>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Auto-detected Rashi banner */}
        {detectedSign && detectedSign.moon_sign !== selectedSign && (
          <div className="rounded-xl border border-sacred-gold/40 bg-sacred-gold/5 px-4 py-2.5 mb-3 flex items-center justify-between gap-3">
            <p className="text-xs text-foreground">
              {language === 'hi'
                ? `जन्म डेटा से राशि: ${detectedSign.moon_sign_hindi} (${detectedSign.nakshatra})`
                : `Detected Rashi: ${detectedSign.moon_sign.charAt(0).toUpperCase() + detectedSign.moon_sign.slice(1)} (${detectedSign.nakshatra})`}
            </p>
            <button
              onClick={() => setSelectedSign(detectedSign.moon_sign)}
              className="text-xs font-semibold text-sacred-gold-dark hover:underline whitespace-nowrap"
            >
              {language === 'hi' ? 'इसे चुनें' : 'Use this'}
            </button>
          </div>
        )}

        {/* Sign Tabs — equally spaced grid of 12 */}
        <div className="rounded-xl border border-border bg-card p-2 mb-4">
          <div className="grid grid-cols-6 sm:grid-cols-12 gap-1">
            {SIGNS.map((s) => (
              <button
                key={s.id}
                onClick={() => setSelectedSign(s.id)}
                className={`flex flex-col items-center gap-0.5 py-2 rounded-lg text-xs transition-all ${
                  selectedSign === s.id
                    ? 'bg-sacred-gold/[0.08] text-sacred-gold-dark shadow-sm border border-sacred-gold/30'
                    : 'text-muted-foreground hover:bg-sacred-gold/10'
                }`}
              >
                <img
                  src={`/images/zodiac-orange/zodiac-${s.id}-orange.png`}
                  alt={s.en}
                  className="w-10 h-10 object-contain"
                />
                <span className="text-[10px]">{language === 'hi' ? s.hi : s.en}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Tab Navigation */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-7 h-auto p-1 bg-card rounded-xl">
            {[
              { id: 'daily', label: t('auto.daily'), icon: Sun },
              { id: 'tomorrow', label: language === 'hi' ? 'कल' : 'Tomorrow', icon: CalendarCheck },
              { id: 'weekly', label: t('auto.weekly'), icon: Calendar },
              { id: 'monthly', label: t('auto.monthly'), icon: CalendarDays },
              { id: 'yearly', label: t('auto.yearly'), icon: Star },
              { id: 'all', label: t('auto.allSigns'), icon: Users },
              { id: 'transits', label: t('auto.transits'), icon: Orbit },
            ].map(tab => (
              <TabsTrigger key={tab.id} value={tab.id} className="flex-1 flex flex-col items-center gap-0.5 py-2 text-xs data-[state=active]:bg-sacred-gold data-[state=active]:text-white rounded-lg">
                <tab.icon className="w-4 h-4" />
                <span>{tab.label}</span>
              </TabsTrigger>
            ))}
          </TabsList>

          <div className="mt-4">
            <TabsContent value="daily">
              <DailyTab data={dailyData} loading={dailyLoading} language={language} t={t} />
            </TabsContent>
            <TabsContent value="tomorrow">
              <DailyTab data={tomorrowData} loading={tomorrowLoading} language={language} t={t} />
            </TabsContent>
            <TabsContent value="weekly">
              <WeeklyTab data={weeklyData} loading={weeklyLoading} language={language} t={t} />
            </TabsContent>
            <TabsContent value="monthly">
              <MonthlyTab data={monthlyData} loading={monthlyLoading} language={language} t={t} />
            </TabsContent>
            <TabsContent value="yearly">
              <YearlyTab data={yearlyData} loading={yearlyLoading} language={language} t={t} />
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
