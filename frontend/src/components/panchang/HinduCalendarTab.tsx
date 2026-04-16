import { useState, useEffect, useMemo, useCallback } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ChevronLeft, ChevronRight, Sun, Moon, Star, Flame, Calendar, X } from 'lucide-react';
import { api } from '@/lib/api';
import { translateBackend } from '@/lib/backend-translations';
import type { FullPanchangData } from '@/sections/Panchang';

interface Props {
  language: string;
  t: (key: string) => string;
  latitude: string;
  longitude: string;
  locationName?: string;
}

interface DayPanchang {
  date: string;
  tithi: string;
  tithi_hindi?: string;
  nakshatra: string;
  nakshatra_hindi?: string;
  paksha: string;
  paksha_hindi?: string;
  moon_sign?: string;
  moon_sign_hindi?: string;
  sunrise: string;
  sunset: string;
  moonrise?: string;
  moonset?: string;
  festivals: string[];
  festival_details: FestivalDetail[];
}

interface FestivalDetail {
  name: string;
  type?: string;
  description?: string;
  rituals?: string;
}

interface SelectedDayFull {
  panchang: FullPanchangData | null;
  loading: boolean;
}

// ---- helpers (shared with MonthlyCalendarTab) ----

const FIXED_FESTIVALS_BY_MMDD: Record<string, string[]> = {
  '01-14': ['Makar Sankranti', 'Pongal'], '01-26': ['Republic Day'],
  '03-14': ['Holika Dahan'], '03-15': ['Holi'],
  '04-13': ['Baisakhi'], '04-14': ['Ambedkar Jayanti'],
  '08-15': ['Independence Day'], '08-16': ['Krishna Janmashtami'],
  '10-02': ['Gandhi Jayanti', 'Dussehra'], '10-22': ['Diwali'],
  '11-15': ['Guru Nanak Jayanti'], '12-25': ['Christmas'],
};

const uniqStrings = (arr: string[]) => {
  const seen = new Set<string>();
  return arr.filter((s) => {
    const k = s.trim().toLowerCase();
    if (!k || seen.has(k)) return false;
    seen.add(k);
    return true;
  });
};

const normalizeFestivalName = (raw: any) => {
  if (typeof raw === 'string') return raw.trim();
  return String(raw?.name || raw?.title || raw?.festival || '').trim();
};

const normalizeFestivalDetail = (raw: any): FestivalDetail | null => {
  const name = normalizeFestivalName(raw);
  if (!name) return null;
  return {
    name,
    type: typeof raw?.type === 'string' ? raw.type : undefined,
    description: typeof raw?.description === 'string' ? raw.description : undefined,
    rituals: typeof raw?.rituals === 'string' ? raw.rituals : undefined,
  };
};

const generateObservances = (day: DayPanchang) => {
  const tithi = (day.tithi || '').toLowerCase();
  const list: string[] = [];
  if (tithi.includes('ekadashi')) list.push('Ekadashi Vrat');
  if (tithi.includes('pradosh') || tithi.includes('trayodashi')) list.push('Pradosh Vrat');
  if (tithi.includes('amavasya')) list.push('Amavasya');
  if (tithi.includes('purnima')) list.push('Purnima');
  const mmdd = day.date.slice(5, 10);
  return uniqStrings([...list, ...(FIXED_FESTIVALS_BY_MMDD[mmdd] || [])]);
};

const enrichDayFestivals = (day: DayPanchang): DayPanchang => {
  const generated = generateObservances(day);
  const genDetails: FestivalDetail[] = generated.map((name) => ({ name, type: 'observance' }));
  const seen = new Set<string>();
  const allDetails = [...(day.festival_details || []), ...genDetails].filter((d) => {
    const k = d.name.trim().toLowerCase();
    if (!k || seen.has(k)) return false;
    seen.add(k);
    return true;
  });
  return {
    ...day,
    festivals: uniqStrings([...(day.festivals || []), ...generated, ...allDetails.map((f) => f.name)]),
    festival_details: allDetails,
  };
};

const getLocalDateString = () => {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
};

// Moon phase icon based on paksha + tithi
const getMoonIcon = (paksha: string, tithi: string) => {
  const t = tithi.toLowerCase();
  if (t.includes('purnima')) return '🌕';
  if (t.includes('amavasya')) return '🌑';
  if (paksha.toLowerCase().includes('shukla')) {
    if (t.includes('pratipada') || t.includes('dwitiya') || t.includes('tritiya')) return '🌒';
    if (t.includes('chaturthi') || t.includes('panchami') || t.includes('shashthi') || t.includes('saptami')) return '🌓';
    if (t.includes('ashtami') || t.includes('navami') || t.includes('dashami')) return '🌔';
    return '🌔';
  }
  // Krishna
  if (t.includes('pratipada') || t.includes('dwitiya') || t.includes('tritiya')) return '🌖';
  if (t.includes('chaturthi') || t.includes('panchami') || t.includes('shashthi') || t.includes('saptami')) return '🌗';
  if (t.includes('ashtami') || t.includes('navami') || t.includes('dashami')) return '🌘';
  return '🌘';
};

// Festival importance
const isMajorFestival = (name: string) => {
  const l = name.toLowerCase();
  return ['diwali', 'holi', 'dussehra', 'navratri', 'janmashtami', 'shivaratri',
    'ganesh', 'ram navami', 'hanuman jayanti', 'raksha bandhan', 'republic', 'independence',
    'baisakhi', 'guru nanak', 'christmas', 'new year'].some((w) => l.includes(w));
};

const isVrat = (name: string) => {
  const l = name.toLowerCase();
  return ['vrat', 'ekadashi', 'pradosh', 'chaturthi'].some((w) => l.includes(w));
};

// Tithi number: Pratipada=1, Dwitiya=2, ... Chaturdashi=14, Purnima=15/30, Amavasya=30
const TITHI_NUM: Record<string, number> = {
  pratipada: 1, dwitiya: 2, tritiya: 3, chaturthi: 4, panchami: 5,
  shashthi: 6, saptami: 7, ashtami: 8, navami: 9, dashami: 10,
  ekadashi: 11, dwadashi: 12, trayodashi: 13, chaturdashi: 14,
  purnima: 15, amavasya: 30,
};
const getTithiNumber = (tithi: string): number | null => {
  const t = tithi.toLowerCase();
  for (const [key, num] of Object.entries(TITHI_NUM)) {
    if (t.includes(key)) return num;
  }
  return null;
};

// Helper to safely format a time period
const fmtPeriod = (period: any): string => {
  if (!period) return '';
  if (typeof period === 'string') return period;
  const s = period.start || period.begin || '';
  const e = period.end || '';
  if (!s && !e) return '';
  return `${s} to ${e}`;
};

export default function HinduCalendarTab({ language, t, latitude, longitude, locationName }: Props) {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [monthlyData, setMonthlyData] = useState<DayPanchang[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedDay, setSelectedDay] = useState<DayPanchang | null>(null);
  const [selectedDayFull, setSelectedDayFull] = useState<SelectedDayFull>({ panchang: null, loading: false });
  const [lightboxOpen, setLightboxOpen] = useState(false);

  // Open lightbox for a day
  const openLightbox = useCallback((dayData: DayPanchang) => {
    setSelectedDay(dayData);
    setLightboxOpen(true);
  }, []);

  // Close lightbox
  const closeLightbox = useCallback(() => {
    setLightboxOpen(false);
  }, []);

  // Escape key closes lightbox + body scroll lock
  useEffect(() => {
    if (!lightboxOpen) return;
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') closeLightbox(); };
    document.addEventListener('keydown', onKey);
    document.body.style.overflow = 'hidden';
    return () => {
      document.removeEventListener('keydown', onKey);
      document.body.style.overflow = '';
    };
  }, [lightboxOpen, closeLightbox]);

  const year = currentDate.getFullYear();
  const month = currentDate.getMonth();

  const monthNames = language === 'hi'
    ? ['जनवरी', 'फरवरी', 'मार्च', 'अप्रैल', 'मई', 'जून', 'जुलाई', 'अगस्त', 'सितंबर', 'अक्टूबर', 'नवंबर', 'दिसंबर']
    : ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

  const weekdaysFull = language === 'hi'
    ? ['रवि', 'सोम', 'मंगल', 'बुध', 'गुरु', 'शुक्र', 'शनि']
    : ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'];

  // Fetch monthly panchang data
  useEffect(() => {
    const fetchMonthly = async () => {
      setLoading(true);
      // Festivals from dedicated endpoint
      let monthlyFestivalMap: Record<string, FestivalDetail[]> = {};
      try {
        const monthlyRes: any = await api.get(`/api/festivals?year=${year}&month=${month + 1}`);
        const rows: any[] = monthlyRes?.festivals || monthlyRes?.data?.festivals || [];
        monthlyFestivalMap = rows.reduce((acc: Record<string, FestivalDetail[]>, row: any) => {
          const dateStr = String(row?.date || '').slice(0, 10);
          const detail = normalizeFestivalDetail(row);
          if (!dateStr || !detail) return acc;
          acc[dateStr] = [...(acc[dateStr] || []), detail];
          return acc;
        }, {});
      } catch (_) { /* ignore */ }

      try {
        const res = await api.get(`/api/panchang/month?month=${month + 1}&year=${year}&latitude=${latitude}&longitude=${longitude}`);
        const rawDays = (res as any)?.days || res || [];

        const data: DayPanchang[] = rawDays.map((p: any) => {
          const baseRaw = Array.isArray(p.festivals) ? p.festivals : (p.festivals ? [p.festivals] : []);
          const baseDetails = baseRaw.map((f: any) => normalizeFestivalDetail(f)).filter(Boolean) as FestivalDetail[];
          const day = enrichDayFestivals({
            date: p.date || '',
            tithi: p.tithi || '',
            tithi_hindi: p.tithi_hindi,
            nakshatra: p.nakshatra || '',
            nakshatra_hindi: p.nakshatra_hindi,
            paksha: p.paksha || '',
            paksha_hindi: p.paksha_hindi,
            moon_sign: p.moon_sign || p.chandra_rashi || '',
            moon_sign_hindi: p.moon_sign_hindi || p.chandra_rashi_hindi || '',
            sunrise: p.sunrise || '',
            sunset: p.sunset || '',
            moonrise: p.moonrise || '',
            moonset: p.moonset || '',
            festivals: baseDetails.map((f) => f.name),
            festival_details: baseDetails,
          });
          const extra = monthlyFestivalMap[String(p.date || '').slice(0, 10)] || [];
          if (extra.length) {
            const seen = new Set(day.festival_details.map((d) => d.name.toLowerCase()));
            const newDetails = extra.filter((d) => !seen.has(d.name.toLowerCase()));
            return { ...day, festivals: uniqStrings([...day.festivals, ...newDetails.map((d) => d.name)]), festival_details: [...day.festival_details, ...newDetails] };
          }
          return day;
        });

        setMonthlyData(data);
        const today = getLocalDateString();
        setSelectedDay(data.find((d) => d.date === today) || data[0] || null);
      } catch (_) {
        setMonthlyData([]);
      }
      setLoading(false);
    };
    fetchMonthly();
  }, [year, month, latitude, longitude]);

  // Fetch full panchang for selected day (for left panel details)
  useEffect(() => {
    if (!selectedDay) { setSelectedDayFull({ panchang: null, loading: false }); return; }
    let cancelled = false;
    const fetchFull = async () => {
      setSelectedDayFull((prev) => ({ ...prev, loading: true }));
      try {
        const data = await api.get(`/api/panchang?date=${selectedDay.date}&latitude=${latitude}&longitude=${longitude}`);
        if (!cancelled) setSelectedDayFull({ panchang: data as any, loading: false });
      } catch (_) {
        if (!cancelled) setSelectedDayFull({ panchang: null, loading: false });
      }
    };
    fetchFull();
    return () => { cancelled = true; };
  }, [selectedDay?.date, latitude, longitude]);

  const firstDayOfMonth = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const today = getLocalDateString();

  const prevMonth = () => setCurrentDate(new Date(year, month - 1, 1));
  const nextMonth = () => setCurrentDate(new Date(year, month + 1, 1));

  const getDayData = (day: number) => {
    const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    return monthlyData.find((d) => d.date === dateStr);
  };

  // Collect month festivals for the sidebar
  const monthFestivals = useMemo(() => {
    const result: { date: string; name: string; type: string }[] = [];
    monthlyData.forEach((day) => {
      day.festivals.forEach((f) => {
        if (isMajorFestival(f) || isVrat(f)) {
          result.push({ date: day.date, name: f, type: isMajorFestival(f) ? 'major' : 'vrat' });
        }
      });
    });
    return result;
  }, [monthlyData]);

  const p = selectedDayFull.panchang as any;

  return (
    <div className="space-y-2">
      {/* Main Layout: Left Panel + Calendar Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-[280px_1fr] gap-2">

        {/* ===== LEFT PANEL: Selected Day Details + Festivals ===== */}
        <div className="space-y-2">

          {/* Selected Day — Full Dainik Panchang (Drik Panchang style) */}
          <FullPanchangPanel
            selectedDay={selectedDay}
            fullData={selectedDayFull}
            language={language}
            t={t}
            locationName={locationName}
          />

          {/* Festivals moved to below the calendar grid */}
        </div>

        {/* ===== RIGHT PANEL: Calendar Grid ===== */}
        <Card className="border border-sacred-gold/20 bg-[#FFF9F5] shadow-sm">
          <CardContent className="p-2 sm:p-3">
            {/* Month heading — integrated into grid */}
            <div className="flex items-center justify-between mb-2">
              <Button variant="outline" size="icon" onClick={prevMonth} className="border-sacred-gold/30 h-8 w-8">
                <ChevronLeft className="h-4 w-4" />
              </Button>
              <div className="text-center">
                {locationName && (
                  <p className="text-[10px] text-muted-foreground flex items-center justify-center gap-1">
                    📍 {locationName}
                  </p>
                )}
                <h3 className="text-xl font-bold text-[#C45A00]">{monthNames[month]} {year}</h3>
                {p?.hindu_calendar?.maas && (
                  <p className="text-xs text-sacred-gold">
                    {p.hindu_calendar.maas} · {language === 'hi' ? 'विक्रम संवत्' : 'Vikram Samvat'} {p.hindu_calendar.vikram_samvat}
                  </p>
                )}
              </div>
              <Button variant="outline" size="icon" onClick={nextMonth} className="border-sacred-gold/30 h-8 w-8">
                <ChevronRight className="h-4 w-4" />
              </Button>
            </div>

            {loading ? (
              <div className="flex items-center justify-center h-64">
                <div className="animate-spin h-8 w-8 border-2 border-sacred-gold border-t-transparent rounded-full" />
              </div>
            ) : (
              <>
                {/* Weekday Headers */}
                <div className="grid grid-cols-7 gap-px rounded-t-lg overflow-hidden bg-[#E8D5B7]">
                  {weekdaysFull.map((day, i) => (
                    <div key={day} className={`text-center text-[10px] sm:text-xs font-bold py-1.5 ${i === 0 ? 'text-red-600 bg-red-50' : 'text-stone-700 bg-[#F5E6D0]'}`}>
                      {day}
                    </div>
                  ))}
                </div>

                {/* Calendar Grid — Drik Panchang style */}
                <div className="grid grid-cols-7 gap-px bg-[#E8D5B7]">
                  {/* Leading empty cells */}
                  {Array.from({ length: firstDayOfMonth }).map((_, i) => (
                    <div key={`e-${i}`} className="min-h-[130px] sm:min-h-[150px] bg-[#FFF9F5]" />
                  ))}

                  {/* Day cells — dense layout matching Drik Panchang */}
                  {Array.from({ length: daysInMonth }, (_, i) => i + 1).map((day) => {
                    const dayData = getDayData(day);
                    const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
                    const isToday = dateStr === today;
                    const isSelected = selectedDay?.date === dateStr;
                    const isSunday = new Date(year, month, day).getDay() === 0;
                    const majorFests = dayData?.festivals.filter(isMajorFestival) || [];
                    const vrats = dayData?.festivals.filter((f) => isVrat(f) && !isMajorFestival(f)) || [];
                    const moonIcon = dayData ? getMoonIcon(dayData.paksha, dayData.tithi) : '';
                    const tithiDisplay = dayData
                      ? (language === 'hi' ? dayData.tithi_hindi || translateBackend(dayData.tithi, language) : dayData.tithi)
                      : '';
                    const pakshaDisplay = dayData
                      ? (language === 'hi' ? dayData.paksha_hindi || translateBackend(dayData.paksha, language) : dayData.paksha)
                      : '';
                    const nakDisplay = dayData?.nakshatra
                      ? (language === 'hi' ? dayData.nakshatra_hindi || translateBackend(dayData.nakshatra, language) : dayData.nakshatra)
                      : '';
                    const moonSignDisplay = dayData?.moon_sign
                      ? (language === 'hi' ? dayData.moon_sign_hindi || translateBackend(dayData.moon_sign, language) : dayData.moon_sign)
                      : '';

                    const tithiNum = dayData ? getTithiNumber(dayData.tithi) : null;

                    return (
                      <button
                        key={day}
                        onClick={() => dayData && openLightbox(dayData)}
                        className={`
                          min-h-[130px] sm:min-h-[150px] p-0 text-left relative overflow-hidden flex flex-col
                          transition-all hover:brightness-[0.97] cursor-pointer
                          ${isToday ? 'bg-[#F5DEB3] ring-2 ring-inset ring-[#C45A00]' : isSelected ? 'bg-[#FFF0D4]' : isSunday ? 'bg-[#FFF5F5]' : 'bg-[#FFF9F5]'}
                        `}
                      >
                        {/* Tithi + Paksha header + moon phase top-right */}
                        <div className="w-full flex items-center justify-between px-1.5 py-0.5">
                          <span className={`text-[8px] sm:text-[10px] font-medium truncate leading-tight ${isSunday ? 'text-red-600' : 'text-stone-500'}`}>
                            {tithiDisplay} {pakshaDisplay}
                          </span>
                          {moonIcon && (
                            <span className="text-sm sm:text-base leading-none">{moonIcon}</span>
                          )}
                        </div>

                        {/* Main content area */}
                        <div className="flex-1 flex flex-col items-center justify-center px-1.5 py-1">

                          {/* DATE number + tithi badge */}
                          <div className="flex items-start justify-center gap-0.5 mb-1">
                            <span className={`text-3xl sm:text-4xl font-bold leading-none ${isSunday ? 'text-red-600' : isToday ? 'text-[#C45A00]' : 'text-stone-800'}`}>
                              {day}
                            </span>
                            {tithiNum && (
                              <span className="text-[8px] sm:text-[9px] font-bold border border-stone-400 text-stone-600 rounded px-0.5 leading-tight mt-0.5">
                                {tithiNum}
                              </span>
                            )}
                          </div>

                          {/* Sunrise/Sunset + Moonrise/Moonset */}
                          {dayData && (
                            <>
                              <div className="flex items-center justify-between w-full text-[8px] sm:text-[10px] text-stone-400">
                                <span><span className="text-[#C45A00]">☀↑</span> {dayData.sunrise?.slice(0, 5)}</span>
                                <span><span className="text-[#C45A00]">☀↓</span> {dayData.sunset?.slice(0, 5)}</span>
                              </div>
                              <div className="flex items-center justify-between w-full text-[8px] sm:text-[10px] text-stone-400">
                                {dayData.moonrise && dayData.moonrise !== '--:--'
                                  ? <span><span className="text-blue-400">☽↑</span> {dayData.moonrise?.slice(0, 5)}</span>
                                  : <span />}
                                {dayData.moonset && dayData.moonset !== '--:--'
                                  ? <span><span className="text-blue-400">☽↓</span> {dayData.moonset?.slice(0, 5)}</span>
                                  : <span />}
                              </div>
                            </>
                          )}
                        </div>

                        {/* Festival name */}
                        {majorFests.length > 0 && (
                          <div className="px-1 text-center">
                            {majorFests.slice(0, 1).map((f, i) => (
                              <p key={i} className="text-[8px] sm:text-[10px] font-bold text-red-600 leading-tight break-words">
                                {language === 'hi' ? translateBackend(f, language) : f}
                              </p>
                            ))}
                          </div>
                        )}
                        {vrats.length > 0 && majorFests.length === 0 && (
                          <div className="px-1 text-center">
                            {vrats.slice(0, 1).map((f, i) => (
                              <p key={i} className="text-[8px] sm:text-[10px] font-semibold text-purple-700 leading-tight break-words">
                                {language === 'hi' ? translateBackend(f, language) : f}
                              </p>
                            ))}
                          </div>
                        )}

                        {/* Moon sign + Nakshatra at bottom */}
                        <div className="w-full px-1 pb-1 mt-auto text-center">
                          {moonSignDisplay && (
                            <p className="text-[8px] sm:text-[9px] text-stone-400 leading-tight">
                              ☽ {moonSignDisplay}
                            </p>
                          )}
                          {nakDisplay && (
                            <p className="text-[8px] sm:text-[9px] text-stone-400 leading-tight">
                              ☆ {nakDisplay}
                            </p>
                          )}
                        </div>
                      </button>
                    );
                  })}

                  {/* Trailing empty cells — only complete the last row, no extra rows */}
                  {Array.from({ length: (7 - ((firstDayOfMonth + daysInMonth) % 7)) % 7 }).map((_, i) => (
                    <div key={`te-${i}`} className="min-h-[130px] sm:min-h-[150px] bg-[#FFF9F5]" />
                  ))}
                </div>

                {/* Legend */}
                <div className="flex flex-wrap items-center justify-center gap-x-1.5 gap-y-0.5 mt-2 text-[10px] text-stone-400">
                  <span><span className="inline-block border border-stone-400 text-stone-600 rounded text-[8px] font-bold px-0.5 mr-0.5">x</span> {language === 'hi' ? 'तिथि' : 'Tithi'}</span>
                  <span>🌕🌑 {language === 'hi' ? 'चन्द्र कला' : 'Moon Phase'}</span>
                  <span><span className="text-[#C45A00]">☀↑</span> {language === 'hi' ? 'सूर्योदय' : 'Sunrise'}</span>
                  <span><span className="text-[#C45A00]">☀↓</span> {language === 'hi' ? 'सूर्यास्त' : 'Sunset'}</span>
                  <span><span className="text-blue-400">☽↑</span> {language === 'hi' ? 'चन्द्रोदय' : 'Moonrise'}</span>
                  <span><span className="text-blue-400">☽↓</span> {language === 'hi' ? 'चन्द्रास्त' : 'Moonset'}</span>
                  <span>☆ {language === 'hi' ? 'नक्षत्र' : 'Nakshatra'}</span>
                  <span className="text-red-600">{language === 'hi' ? 'पर्व' : 'Festival'}</span>
                  <span className="text-purple-700">{language === 'hi' ? 'व्रत' : 'Vrat'}</span>
                </div>
              </>
            )}
          </CardContent>
        </Card>
      </div>

      {/* ===== FESTIVALS GRID (horizontal, below calendar) ===== */}
      {monthFestivals.length > 0 && (
        <Card className="border border-sacred-gold/20 bg-[#FFF9F5] shadow-sm overflow-hidden">
          <div className="bg-[#C45A00] px-3 py-1.5">
            <h4 className="text-white font-bold text-sm text-center">
              {monthNames[month]} {year} {language === 'hi' ? 'व्रत एवं पर्व' : 'Festivals'}
            </h4>
            {p?.hindu_calendar?.maas && (
              <p className="text-white/80 text-[10px] text-center">
                {p.hindu_calendar.maas} - {language === 'hi' ? 'विक्रम संवत्' : 'Vikram Samvat'} {p.hindu_calendar.vikram_samvat}
              </p>
            )}
          </div>
          <CardContent className="p-3">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-x-4 gap-y-1">
              {monthFestivals.map((f, i) => {
                const d = new Date(f.date + 'T12:00:00');
                const dayNum = d.getDate();
                const dayName = d.toLocaleDateString(language === 'hi' ? 'hi-IN' : 'en-US', { weekday: 'long' });
                return (
                  <div key={i} className="flex items-baseline gap-2 py-1 border-b border-stone-100 last:border-0">
                    <span className="text-lg font-bold text-[#C45A00] w-8 text-right shrink-0">{String(dayNum).padStart(2, '0')}</span>
                    <div className="min-w-0">
                      <p className="text-[11px] font-bold text-stone-700 leading-tight">
                        {language === 'hi' ? translateBackend(f.name, language) : f.name}
                      </p>
                      <p className="text-[9px] text-stone-400">{dayName}</p>
                    </div>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>
      )}

      {/* ===== LIGHTBOX MODAL ===== */}
      {lightboxOpen && selectedDay && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
          onClick={closeLightbox}
        >
          <div
            className="relative w-full max-w-md max-h-[85vh] overflow-y-auto rounded-2xl bg-card border border-border shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Close button */}
            <button
              onClick={closeLightbox}
              className="absolute top-3 right-3 z-10 p-1 rounded-full bg-card/80 hover:bg-card border border-border/50 transition-colors"
            >
              <X className="w-4 h-4 text-muted-foreground" />
            </button>

            {/* Lightbox header */}
            <div className="px-4 pt-4 pb-2 border-b border-border/40">
              <div className="flex items-center gap-3">
                <div className="text-3xl">
                  {getMoonIcon(selectedDay.paksha, selectedDay.tithi)}
                </div>
                <div>
                  <h3 className="font-bold text-foreground text-base">
                    {new Date(selectedDay.date + 'T12:00:00').toLocaleDateString(language === 'hi' ? 'hi-IN' : 'en-US', {
                      weekday: 'long', day: 'numeric', month: 'long', year: 'numeric'
                    })}
                  </h3>
                  <p className="text-xs text-sacred-gold">
                    {language === 'hi'
                      ? (selectedDay.tithi_hindi || translateBackend(selectedDay.tithi, language))
                      : selectedDay.tithi}
                    {' · '}
                    {language === 'hi'
                      ? (selectedDay.paksha_hindi || translateBackend(selectedDay.paksha, language))
                      : selectedDay.paksha}
                  </p>
                </div>
              </div>
            </div>

            {/* Lightbox body — full panchang */}
            <div className="px-4 py-3 space-y-0.5 text-[12px]">
              {selectedDayFull.loading ? (
                <div className="flex items-center justify-center py-12">
                  <div className="animate-spin h-6 w-6 border-2 border-sacred-gold border-t-transparent rounded-full" />
                </div>
              ) : (() => {
                const fp = selectedDayFull.panchang as any;
                if (!fp) return <p className="text-center text-muted-foreground py-8">Loading...</p>;
                return (
                  <>
                    {/* Sun & Moon */}
                    <LightboxSection title={language === 'hi' ? 'सूर्य एवं चन्द्र' : 'Sun & Moon'}>
                      <LBRow label="Sunrise" labelHi="सूर्योदय" lang={language} value={fp.sunrise} />
                      <LBRow label="Sunset" labelHi="सूर्यास्त" lang={language} value={fp.sunset} />
                      <LBRow label="Moonrise" labelHi="चन्द्रोदय" lang={language} value={fp.moonrise} />
                      <LBRow label="Moonset" labelHi="चन्द्रास्त" lang={language} value={fp.moonset} />
                    </LightboxSection>

                    {/* Hindu Calendar */}
                    {fp.hindu_calendar && (
                      <LightboxSection title={language === 'hi' ? 'हिन्दू पंचांग' : 'Hindu Calendar'}>
                        <LBRow label="Shaka Samvat" labelHi="शक संवत्" lang={language} value={String(fp.hindu_calendar.shaka_samvat || '')} />
                        <LBRow label="Vikram Samvat" labelHi="विक्रम संवत्" lang={language} value={String(fp.hindu_calendar.vikram_samvat || '')} />
                        <LBRow label="Month" labelHi="मास" lang={language} value={fp.hindu_calendar.maas} />
                        <LBRow label="Paksha" labelHi="पक्ष" lang={language} value={language === 'hi' ? translateBackend(fp.hindu_calendar.paksha || '', language) : fp.hindu_calendar.paksha} />
                        <LBRow label="Weekday" labelHi="वार" lang={language} value={language === 'hi' ? (fp.vaar?.name || '') : (fp.vaar?.english || '')} />
                        <LBRow label="Ritu" labelHi="ऋतु" lang={language} value={fp.hindu_calendar.ritu} />
                        <LBRow label="Ayana" labelHi="अयन" lang={language} value={fp.hindu_calendar.ayana} />
                      </LightboxSection>
                    )}

                    {/* Panchang Elements */}
                    <LightboxSection title={language === 'hi' ? 'पंचांग तत्व' : 'Panchang Elements'}>
                      <LBRow label="Tithi" labelHi="तिथि" lang={language}
                        value={`${language === 'hi' ? translateBackend(fp.tithi?.name || '', language) : fp.tithi?.name || ''}${fp.tithi?.end_time ? ` upto ${fp.tithi.end_time}` : ''}`}
                        highlight
                      />
                      <LBRow label="Nakshatra" labelHi="नक्षत्र" lang={language}
                        value={`${language === 'hi' ? translateBackend(fp.nakshatra?.name || '', language) : fp.nakshatra?.name || ''}${fp.nakshatra?.end_time ? ` upto ${fp.nakshatra.end_time}` : ''}`}
                        highlight
                      />
                      <LBRow label="Yoga" labelHi="योग" lang={language}
                        value={`${language === 'hi' ? translateBackend(fp.yoga?.name || '', language) : fp.yoga?.name || ''}${fp.yoga?.end_time ? ` upto ${fp.yoga.end_time}` : ''}`}
                      />
                      <LBRow label="Karana" labelHi="करण" lang={language}
                        value={language === 'hi' ? translateBackend(fp.karana?.name || '', language) : fp.karana?.name}
                      />
                    </LightboxSection>

                    {/* Signs */}
                    {(fp.sun_sign || fp.moon_sign) && (
                      <LightboxSection title={language === 'hi' ? 'राशि' : 'Signs'}>
                        {fp.sun_sign && <LBRow label="Sun Sign" labelHi="सूर्य राशि" lang={language} value={fp.sun_sign} />}
                        {fp.moon_sign && <LBRow label="Moon Sign" labelHi="चन्द्र राशि" lang={language} value={fp.moon_sign} />}
                      </LightboxSection>
                    )}

                    {/* Inauspicious */}
                    <LightboxSection title={language === 'hi' ? 'अशुभ काल' : 'Inauspicious Periods'}>
                      <LBRow label="Rahu Kalam" labelHi="राहुकाल" lang={language}
                        value={fp.rahu_kaal ? `${fp.rahu_kaal.start} to ${fp.rahu_kaal.end}` : ''} warn
                      />
                      <LBRow label="Gulika Kalam" labelHi="गुलिक काल" lang={language}
                        value={fp.gulika_kaal ? `${fp.gulika_kaal.start} to ${fp.gulika_kaal.end}` : ''} warn
                      />
                      <LBRow label="Yamaganda" labelHi="यमगण्ड" lang={language}
                        value={fp.yamaganda ? `${fp.yamaganda.start} to ${fp.yamaganda.end}` : ''} warn
                      />
                      {fp.dur_muhurtam && (
                        <LBRow label="Dur Muhurtam" labelHi="दुर्मुहूर्त" lang={language}
                          value={`${fp.dur_muhurtam.start} to ${fp.dur_muhurtam.end}`} warn
                        />
                      )}
                      {fp.varjyam && (
                        <LBRow label="Varjyam" labelHi="वर्ज्यम्" lang={language}
                          value={`${fp.varjyam.start} to ${fp.varjyam.end}`} warn
                        />
                      )}
                    </LightboxSection>

                    {/* Auspicious */}
                    <LightboxSection title={language === 'hi' ? 'शुभ मुहूर्त' : 'Auspicious Muhurat'}>
                      <LBRow label="Abhijit" labelHi="अभिजीत" lang={language}
                        value={fp.abhijit_muhurat ? `${fp.abhijit_muhurat.start} to ${fp.abhijit_muhurat.end}` : 'None'} good
                      />
                      {fp.brahma_muhurat && (
                        <LBRow label="Brahma Muhurat" labelHi="ब्रह्म मुहूर्त" lang={language}
                          value={`${fp.brahma_muhurat.start} to ${fp.brahma_muhurat.end}`} good
                        />
                      )}
                    </LightboxSection>

                    {/* Festivals */}
                    {selectedDay.festivals.length > 0 && (
                      <LightboxSection title={language === 'hi' ? 'व्रत एवं पर्व' : 'Festivals & Vrat'}>
                        <div className="space-y-1">
                          {selectedDay.festivals.map((f, i) => (
                            <div key={i} className="flex items-center gap-1.5">
                              <span className="text-sm">{isMajorFestival(f) ? '🪔' : isVrat(f) ? '🙏' : '✦'}</span>
                              <span className="text-foreground font-medium">
                                {language === 'hi' ? translateBackend(f, language) : f}
                              </span>
                            </div>
                          ))}
                        </div>
                      </LightboxSection>
                    )}
                  </>
                );
              })()}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// ---- Full Panchang Left Panel (Drik Panchang style) ----

function FullPanchangPanel({ selectedDay, fullData, language, t, locationName }: {
  selectedDay: DayPanchang | null;
  fullData: SelectedDayFull;
  language: string;
  t: (key: string) => string;
  locationName?: string;
}) {
  const [timeFormat, setTimeFormat] = useState<'12' | '24' | '24+'>('24');

  const fmt = (time: string | undefined) => {
    if (!time || time === '--' || time === '--:--') return '--';
    if (timeFormat === '24') return time;
    // Parse HH:MM
    const match = time.match(/^(\d{1,2}):(\d{2})/);
    if (!match) return time;
    let h = parseInt(match[1], 10);
    const m = match[2];
    const rest = time.slice(match[0].length); // e.g. "+" suffix
    if (timeFormat === '24+') {
      return h >= 24 ? `${h}:${m}${rest}` : `${h}:${m}${rest}`;
    }
    // 12-hour
    const ampm = h >= 12 && h < 24 ? 'PM' : 'AM';
    if (h === 0) h = 12;
    else if (h > 12 && h < 24) h -= 12;
    else if (h >= 24) return `${time}`; // keep as-is for 24+
    return `${String(h).padStart(2, '0')}:${m} ${ampm}${rest}`;
  };

  const fmtP = (period: any): string => {
    const s = fmtPeriod(period);
    if (!s) return '';
    // format both times in the period string "HH:MM to HH:MM"
    return s.replace(/\d{1,2}:\d{2}/g, (match: string) => fmt(match));
  };

  const p = fullData.panchang as any;

  return (
    <Card className="border border-sacred-gold/20 bg-[#FFF9F5] shadow-sm overflow-hidden">
      {/* Header bar */}
      <div className="bg-[#C45A00] px-3 py-2 rounded-t-lg">
        <h4 className="text-white font-bold text-sm">
          {language === 'hi' ? 'आज का पंचांग' : 'Panchang for Today'}
        </h4>
      </div>

      {/* Time format tabs */}
      <div className="flex items-center justify-center gap-1 px-3 pt-1.5">
        {(['12', '24', '24+'] as const).map((f) => (
          <button
            key={f}
            onClick={() => setTimeFormat(f)}
            className={`px-3 py-1 text-xs rounded-full border transition-colors ${
              timeFormat === f
                ? 'bg-[#C45A00] text-white border-[#C45A00]'
                : 'border-stone-300 text-stone-600 hover:border-[#C45A00]'
            }`}
          >
            {f === '12' ? '12 Hour' : f === '24' ? '24 Hour' : '24 Plus'}
          </button>
        ))}
      </div>

      <CardContent className="p-3">
        {fullData.loading ? (
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin h-6 w-6 border-2 border-sacred-gold border-t-transparent rounded-full" />
          </div>
        ) : selectedDay && p ? (
          <div className="space-y-0.5 text-[12px]">
            {/* Location + Date */}
            <p className="font-bold text-stone-800 text-base flex items-center gap-1">
              {locationName || (language === 'hi' ? 'नई दिल्ली, भारत' : 'New Delhi, India')} <span className="text-[#C45A00]">📍</span>
            </p>
            <p className="text-[#2E7D32] font-semibold text-sm mb-2">
              {new Date(selectedDay.date + 'T12:00:00').toLocaleDateString(language === 'hi' ? 'hi-IN' : 'en-US', {
                weekday: 'long', day: 'numeric', month: 'long', year: 'numeric'
              })}
            </p>

            <div className="border-t border-stone-200 my-1.5" />

            {/* Sun & Moon */}
            <PanchangRow label="Sunrise" labelHi="सूर्योदय" lang={language} value={fmt(p.sunrise)} color="text-[#8B4513]" bold />
            <PanchangRow label="Sunset" labelHi="सूर्यास्त" lang={language} value={fmt(p.sunset)} color="text-[#8B4513]" bold />
            <PanchangRow label="Moonrise" labelHi="चन्द्रोदय" lang={language} value={fmt(p.moonrise)} color="text-[#8B4513]" bold />
            <PanchangRow label="Moonset" labelHi="चन्द्रास्त" lang={language} value={fmt(p.moonset)} color="text-[#8B4513]" bold />

            <div className="border-t border-stone-200 my-1.5" />

            {/* Panchang Elements */}
            <PanchangRow label="Tithi" labelHi="तिथि" lang={language}
              value={`${language === 'hi' ? translateBackend(p.tithi?.name || '', language) : p.tithi?.name || ''}${p.tithi?.end_time ? ` upto ${fmt(p.tithi.end_time)}` : ''}`}
              color="text-[#2E7D32]" bold
            />
            <PanchangRow label="Nakshatra" labelHi="नक्षत्र" lang={language}
              value={`${language === 'hi' ? translateBackend(p.nakshatra?.name || '', language) : p.nakshatra?.name || ''}${p.nakshatra?.end_time ? ` upto ${fmt(p.nakshatra.end_time)}` : ''}`}
              color="text-[#2E7D32]" bold
            />
            <PanchangRow label="Yoga" labelHi="योग" lang={language}
              value={`${language === 'hi' ? translateBackend(p.yoga?.name || '', language) : p.yoga?.name || ''}${p.yoga?.end_time ? ` upto ${fmt(p.yoga.end_time)}` : ''}`}
              color="text-[#2E7D32]" bold
            />
            <PanchangRow label="Karana" labelHi="करण" lang={language}
              value={`${language === 'hi' ? translateBackend(p.karana?.name || '', language) : p.karana?.name || ''}${p.karana?.end_time ? ` upto ${fmt(p.karana.end_time)}` : ''}`}
              color="text-[#2E7D32]" bold
            />

            <div className="border-t border-stone-200 my-1.5" />

            {/* Paksha & Weekday */}
            <PanchangRow label="Paksha" labelHi="पक्ष" lang={language}
              value={p.hindu_calendar?.paksha ? (language === 'hi' ? translateBackend(p.hindu_calendar.paksha, language) : p.hindu_calendar.paksha + ' Paksha') : (p.tithi?.paksha ? p.tithi.paksha + ' Paksha' : '')}
              color="text-[#8B4513]" bold
            />
            <PanchangRow label="Weekday" labelHi="वार" lang={language}
              value={language === 'hi' ? (p.vaar?.name || '') : (p.vaar?.english || new Date(selectedDay.date + 'T12:00:00').toLocaleDateString('en-US', { weekday: 'long' }))}
              color="text-[#8B4513]" bold
            />

            <div className="border-t border-stone-200 my-1.5" />

            {/* Hindu Calendar */}
            <PanchangRow label="Month" labelHi="मास" lang={language} value={p.hindu_calendar?.maas || ''} color="text-[#8B4513]" bold />
            <PanchangRow label="Shaka Samvat" labelHi="शक संवत्" lang={language} value={p.hindu_calendar?.shaka_samvat != null ? String(p.hindu_calendar.shaka_samvat) : ''} color="text-[#8B4513]" />
            <PanchangRow label="Vikram Samvat" labelHi="विक्रम संवत्" lang={language} value={p.hindu_calendar?.vikram_samvat != null ? String(p.hindu_calendar.vikram_samvat) : ''} color="text-[#8B4513]" />
            <PanchangRow label="Ritu" labelHi="ऋतु" lang={language} value={p.hindu_calendar?.ritu || p.hindu_calendar?.ritu_english || ''} />
            <PanchangRow label="Ayana" labelHi="अयन" lang={language} value={p.hindu_calendar?.ayana || ''} />

            <div className="border-t border-stone-200 my-1.5" />

            {/* Day/Night lengths */}
            <PanchangRow label="Day Length" labelHi="दिनमान" lang={language} value={p.dinamana || ''} />
            <PanchangRow label="Night Length" labelHi="रात्रिमान" lang={language} value={p.ratrimana || ''} />
            <PanchangRow label="Mid Day" labelHi="मध्याह्न" lang={language} value={fmt(p.madhyahna) || ''} />

            <div className="border-t border-stone-200 my-1.5" />

            {/* Signs */}
            <PanchangRow label="Sun Sign" labelHi="सूर्य राशि" lang={language} value={p.sun_sign || ''} color="text-[#8B4513]" bold />
            <PanchangRow label="Moon Sign" labelHi="चन्द्र राशि" lang={language} value={p.moon_sign || ''} color="text-[#8B4513]" bold />

            <div className="border-t border-stone-200 my-1.5" />

            {/* Inauspicious times (red) */}
            <PanchangRow label="Rahu Kalam" labelHi="राहुकाल" lang={language} value={fmtP(p.rahu_kaal)} warn />
            <PanchangRow label="Gulika Kalam" labelHi="गुलिक काल" lang={language} value={fmtP(p.gulika_kaal)} warn />
            <PanchangRow label="Yamaganda" labelHi="यमगण्ड" lang={language} value={fmtP(p.yamaganda)} warn />
            <PanchangRow label="Dur Muhurtam" labelHi="दुर्मुहूर्त" lang={language} value={fmtP(p.dur_muhurtam)} warn />
            <PanchangRow label="Varjyam" labelHi="वर्ज्यम्" lang={language} value={fmtP(p.varjyam)} warn />

            {/* Auspicious times (green) */}
            <PanchangRow label="Abhijit" labelHi="अभिजीत" lang={language} value={fmtP(p.abhijit_muhurat) || 'None'} good />
            <PanchangRow label="Brahma Muhurat" labelHi="ब्रह्म मुहूर्त" lang={language} value={fmtP(p.brahma_muhurat)} good />
            <PanchangRow label="Amrit Kalam" labelHi="अमृत काल" lang={language} value={fmtP(p.amrit_kalam)} good />

            {/* Festivals */}
            {selectedDay.festivals.length > 0 && (
              <>
                <div className="border-t border-stone-200 my-1.5" />
                <p className="text-[10px] font-bold text-[#8B4513] uppercase tracking-wider mb-1">
                  {language === 'hi' ? 'व्रत एवं पर्व' : 'Festivals & Vrat'}
                </p>
                {selectedDay.festivals.slice(0, 5).map((f, i) => (
                  <p key={i} className="text-[11px] text-stone-700 flex items-center gap-1">
                    <span>{isMajorFestival(f) ? '🪔' : isVrat(f) ? '🙏' : '✦'}</span>
                    <span className="font-medium">{language === 'hi' ? translateBackend(f, language) : f}</span>
                  </p>
                ))}
              </>
            )}

            <div className="text-center mt-2 pt-1.5 border-t border-stone-200">
              <p className="text-[10px] text-stone-400 italic">
                {language === 'hi' ? 'विस्तृत दैनिक पंचांग' : 'detailed Dainik Panchang'}
              </p>
            </div>
          </div>
        ) : (
          <p className="text-center text-muted-foreground py-8 text-sm">
            {language === 'hi' ? 'दिन चुनें' : 'Select a day'}
          </p>
        )}
      </CardContent>
    </Card>
  );
}

// ---- Small helper components ----

function LightboxSection({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="py-1.5 border-b border-border/20 last:border-b-0">
      <p className="text-[10px] font-bold text-sacred-gold uppercase tracking-wider mb-1">{title}</p>
      <div className="space-y-0.5">{children}</div>
    </div>
  );
}

function LBRow({ label, labelHi, lang, value, warn, good, highlight }: {
  label: string; labelHi?: string; lang?: string; value?: string;
  warn?: boolean; good?: boolean; highlight?: boolean;
}) {
  if (!value) return null;
  const displayLabel = lang === 'hi' && labelHi ? labelHi : label;
  return (
    <div className="flex items-start justify-between gap-2 leading-tight py-[1px]">
      <span className={`whitespace-nowrap ${highlight ? 'font-semibold text-sacred-gold' : 'text-muted-foreground'}`}>
        {displayLabel}:
      </span>
      <span className={`text-right font-medium ${warn ? 'text-red-400' : good ? 'text-green-400' : 'text-foreground'}`}>
        {value}
      </span>
    </div>
  );
}

function PanchangRow({ label, labelHi, lang, value, warn, good, color, bold }: {
  label: string; labelHi?: string; lang?: string; value?: string;
  warn?: boolean; good?: boolean; color?: string; bold?: boolean;
}) {
  if (!value) return null;
  const displayLabel = lang === 'hi' && labelHi ? labelHi : label;
  const labelColor = color || 'text-stone-500';
  return (
    <div className="flex items-start justify-between gap-2 leading-tight py-[2px]">
      <span className={`whitespace-nowrap font-semibold ${labelColor}`}>
        {displayLabel}:
      </span>
      <span className={`text-right min-w-0 ${bold ? 'font-bold' : 'font-medium'} ${warn ? 'text-red-500' : good ? 'text-green-600' : 'text-stone-800'}`}>
        {value}
      </span>
    </div>
  );
}
