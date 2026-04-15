import { useState, useEffect, useMemo } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ChevronLeft, ChevronRight, Sun, Moon, Star, Flame, Calendar } from 'lucide-react';
import { api } from '@/lib/api';
import { translateBackend } from '@/lib/backend-translations';
import type { FullPanchangData } from '@/sections/Panchang';

interface Props {
  language: string;
  t: (key: string) => string;
  latitude: string;
  longitude: string;
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

export default function HinduCalendarTab({ language, t, latitude, longitude }: Props) {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [monthlyData, setMonthlyData] = useState<DayPanchang[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedDay, setSelectedDay] = useState<DayPanchang | null>(null);
  const [selectedDayFull, setSelectedDayFull] = useState<SelectedDayFull>({ panchang: null, loading: false });

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
    <div className="space-y-3">
      {/* Month Navigation Header */}
      <Card className="card-sacred !py-0 !gap-0">
        <CardContent className="p-2">
          <div className="flex items-center justify-between">
            <Button variant="outline" size="icon" onClick={prevMonth} className="border-sacred-gold/30 h-8 w-8">
              <ChevronLeft className="h-4 w-4" />
            </Button>
            <div className="text-center">
              <h3 className="text-lg font-bold text-foreground">{monthNames[month]} {year}</h3>
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
        </CardContent>
      </Card>

      {/* Main Layout: Left Panel + Calendar Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-[280px_1fr] gap-3">

        {/* ===== LEFT PANEL: Selected Day Details + Festivals ===== */}
        <div className="space-y-3">

          {/* Selected Day Panchang Details */}
          <Card className="card-sacred">
            <CardContent className="p-3">
              {selectedDayFull.loading ? (
                <div className="flex items-center justify-center py-8">
                  <div className="animate-spin h-6 w-6 border-2 border-sacred-gold border-t-transparent rounded-full" />
                </div>
              ) : selectedDay && p ? (
                <div className="space-y-1.5">
                  {/* Date header */}
                  <div className="text-center pb-2 border-b border-border/50">
                    <p className="font-bold text-foreground text-sm">
                      {new Date(selectedDay.date + 'T12:00:00').toLocaleDateString(language === 'hi' ? 'hi-IN' : 'en-US', {
                        weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
                      })}
                    </p>
                    {p.hindu_calendar && (
                      <p className="text-[11px] text-sacred-gold mt-0.5">
                        {p.hindu_calendar.maas} {p.hindu_calendar.paksha}
                      </p>
                    )}
                  </div>

                  {/* Nakshatra badge */}
                  {p.nakshatra && (
                    <div className="flex items-center justify-center gap-2 py-1.5 bg-sacred-gold/10 rounded-lg">
                      <span className="text-lg">{getMoonIcon(selectedDay.paksha, selectedDay.tithi)}</span>
                      <div className="text-center">
                        <p className="text-xs text-muted-foreground">{language === 'hi' ? 'नक्षत्र' : 'Nakshatra'}</p>
                        <p className="font-bold text-foreground text-sm">
                          {language === 'hi' ? translateBackend(p.nakshatra?.name || '', language) : p.nakshatra?.name}
                        </p>
                      </div>
                    </div>
                  )}

                  {/* Panchang details rows */}
                  <PanchangRow label={language === 'hi' ? 'सूर्योदय' : 'Sunrise'} value={p.sunrise} icon="🌅" />
                  <PanchangRow label={language === 'hi' ? 'सूर्यास्त' : 'Sunset'} value={p.sunset} icon="🌇" />
                  <PanchangRow label={language === 'hi' ? 'चन्द्रोदय' : 'Moonrise'} value={p.moonrise} icon="🌙" />
                  <PanchangRow label={language === 'hi' ? 'चन्द्रास्त' : 'Moonset'} value={p.moonset} icon="🌘" />
                  <div className="border-t border-border/30 my-1" />
                  <PanchangRow
                    label={language === 'hi' ? 'तिथि' : 'Tithi'}
                    value={`${language === 'hi' ? translateBackend(p.tithi?.name || '', language) : p.tithi?.name || ''}${p.tithi?.end_time ? ` ${language === 'hi' ? 'तक' : 'upto'} ${p.tithi.end_time}` : ''}`}
                  />
                  <PanchangRow label={language === 'hi' ? 'पक्ष' : 'Paksha'} value={language === 'hi' ? translateBackend(p.tithi?.paksha || '', language) : p.tithi?.paksha} />
                  <PanchangRow
                    label={language === 'hi' ? 'नक्षत्र' : 'Nakshatra'}
                    value={`${language === 'hi' ? translateBackend(p.nakshatra?.name || '', language) : p.nakshatra?.name || ''}${p.nakshatra?.end_time ? ` ${language === 'hi' ? 'तक' : 'upto'} ${p.nakshatra.end_time}` : ''}`}
                  />
                  <PanchangRow
                    label={language === 'hi' ? 'योग' : 'Yoga'}
                    value={`${language === 'hi' ? translateBackend(p.yoga?.name || '', language) : p.yoga?.name || ''}${p.yoga?.end_time ? ` ${language === 'hi' ? 'तक' : 'upto'} ${p.yoga.end_time}` : ''}`}
                  />
                  <PanchangRow
                    label={language === 'hi' ? 'करण' : 'Karana'}
                    value={language === 'hi' ? translateBackend(p.karana?.name || '', language) : p.karana?.name}
                  />
                  <div className="border-t border-border/30 my-1" />
                  <PanchangRow
                    label={language === 'hi' ? 'राहुकाल' : 'Rahu Kaal'}
                    value={p.rahu_kaal ? `${p.rahu_kaal.start} - ${p.rahu_kaal.end}` : ''}
                    warn
                  />
                  <PanchangRow
                    label={language === 'hi' ? 'गुलिक काल' : 'Gulika Kaal'}
                    value={p.gulika_kaal ? `${p.gulika_kaal.start} - ${p.gulika_kaal.end}` : ''}
                    warn
                  />
                  <PanchangRow
                    label={language === 'hi' ? 'यमगण्ड' : 'Yamaganda'}
                    value={p.yamaganda ? `${p.yamaganda.start} - ${p.yamaganda.end}` : ''}
                    warn
                  />
                  <div className="border-t border-border/30 my-1" />
                  <PanchangRow
                    label={language === 'hi' ? 'अभिजीत मुहूर्त' : 'Abhijit Muhurat'}
                    value={p.abhijit_muhurat ? `${p.abhijit_muhurat.start} - ${p.abhijit_muhurat.end}` : ''}
                    good
                  />
                  {p.sun_sign && <PanchangRow label={language === 'hi' ? 'सूर्य राशि' : 'Sun Sign'} value={p.sun_sign} />}
                  {p.moon_sign && <PanchangRow label={language === 'hi' ? 'चंद्र राशि' : 'Moon Sign'} value={p.moon_sign} />}
                </div>
              ) : (
                <p className="text-center text-muted-foreground py-8 text-sm">
                  {language === 'hi' ? 'दिन चुनें' : 'Select a day'}
                </p>
              )}
            </CardContent>
          </Card>

          {/* Festivals & Vrat this month */}
          {monthFestivals.length > 0 && (
            <Card className="card-sacred">
              <CardContent className="p-3">
                <h4 className="font-semibold text-foreground text-sm mb-2 flex items-center gap-1.5">
                  <Star className="h-4 w-4 text-sacred-gold" />
                  {language === 'hi' ? 'व्रत एवं पर्व' : 'Festivals & Vrat'}
                </h4>
                <div className="space-y-1.5 max-h-48 overflow-y-auto">
                  {monthFestivals.slice(0, 15).map((f, i) => (
                    <div key={i} className="flex items-start gap-2 text-xs">
                      <span className="text-base leading-none mt-0.5">
                        {f.type === 'major' ? '🪔' : '🙏'}
                      </span>
                      <div className="min-w-0">
                        <p className="font-medium text-foreground leading-tight">
                          {language === 'hi' ? translateBackend(f.name, language) : f.name}
                        </p>
                        <p className="text-[10px] text-muted-foreground">
                          {new Date(f.date + 'T12:00:00').toLocaleDateString(language === 'hi' ? 'hi-IN' : 'en-US', { month: 'short', day: 'numeric' })}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </div>

        {/* ===== RIGHT PANEL: Calendar Grid ===== */}
        <Card className="card-sacred">
          <CardContent className="p-2 sm:p-3">
            {loading ? (
              <div className="flex items-center justify-center h-64">
                <div className="animate-spin h-8 w-8 border-2 border-sacred-gold border-t-transparent rounded-full" />
              </div>
            ) : (
              <>
                {/* Weekday Headers */}
                <div className="grid grid-cols-7 gap-px bg-border/30 rounded-t-lg overflow-hidden">
                  {weekdaysFull.map((day, i) => (
                    <div key={day} className={`text-center text-[10px] sm:text-xs font-bold py-1.5 ${i === 0 ? 'text-red-400 bg-red-500/5' : 'text-foreground/70 bg-card/30'}`}>
                      {day}
                    </div>
                  ))}
                </div>

                {/* Calendar Grid */}
                <div className="grid grid-cols-7 gap-px bg-border/20">
                  {/* Leading empty cells */}
                  {Array.from({ length: firstDayOfMonth }).map((_, i) => (
                    <div key={`e-${i}`} className="min-h-[80px] sm:min-h-[100px] bg-card/5" />
                  ))}

                  {/* Day cells */}
                  {Array.from({ length: daysInMonth }, (_, i) => i + 1).map((day) => {
                    const dayData = getDayData(day);
                    const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
                    const isToday = dateStr === today;
                    const isSelected = selectedDay?.date === dateStr;
                    const isSunday = new Date(year, month, day).getDay() === 0;
                    const majorFests = dayData?.festivals.filter(isMajorFestival) || [];
                    const vrats = dayData?.festivals.filter((f) => isVrat(f) && !isMajorFestival(f)) || [];
                    const moonIcon = dayData ? getMoonIcon(dayData.paksha, dayData.tithi) : '';

                    return (
                      <button
                        key={day}
                        onClick={() => dayData && setSelectedDay(dayData)}
                        className={`
                          min-h-[80px] sm:min-h-[100px] p-1 text-left relative overflow-hidden
                          transition-all hover:bg-sacred-gold/5
                          ${isToday ? 'bg-sacred-gold/15 ring-1 ring-sacred-gold' : isSelected ? 'bg-sacred-gold/10' : 'bg-card/10 hover:bg-card/20'}
                          ${isSunday ? 'border-l border-l-red-500/20' : ''}
                        `}
                      >
                        {/* Day number + moon icon row */}
                        <div className="flex items-start justify-between">
                          <span className={`text-sm sm:text-lg font-bold leading-none ${isSunday ? 'text-red-400' : isToday ? 'text-sacred-gold' : 'text-foreground'}`}>
                            {day}
                          </span>
                          {moonIcon && <span className="text-[10px] sm:text-xs leading-none">{moonIcon}</span>}
                        </div>

                        {/* Tithi */}
                        {dayData && (
                          <p className="text-[8px] sm:text-[10px] text-muted-foreground leading-tight mt-0.5 truncate">
                            {language === 'hi'
                              ? dayData.tithi_hindi || translateBackend(dayData.tithi, language)
                              : dayData.tithi}
                          </p>
                        )}

                        {/* Nakshatra */}
                        {dayData?.nakshatra && (
                          <p className="text-[7px] sm:text-[9px] text-blue-400/70 leading-tight truncate">
                            {language === 'hi'
                              ? dayData.nakshatra_hindi || translateBackend(dayData.nakshatra, language)
                              : dayData.nakshatra}
                          </p>
                        )}

                        {/* Festival names in cell */}
                        {majorFests.length > 0 && (
                          <div className="mt-0.5">
                            {majorFests.slice(0, 2).map((f, i) => (
                              <p key={i} className="text-[7px] sm:text-[9px] font-semibold text-amber-400 leading-tight truncate">
                                {language === 'hi' ? translateBackend(f, language) : f}
                              </p>
                            ))}
                          </div>
                        )}
                        {vrats.length > 0 && majorFests.length === 0 && (
                          <div className="mt-0.5">
                            {vrats.slice(0, 1).map((f, i) => (
                              <p key={i} className="text-[7px] sm:text-[9px] text-purple-400/80 leading-tight truncate">
                                {language === 'hi' ? translateBackend(f, language) : f}
                              </p>
                            ))}
                          </div>
                        )}

                        {/* Today marker dot */}
                        {isToday && (
                          <div className="absolute bottom-0.5 left-1/2 -translate-x-1/2 w-1 h-1 rounded-full bg-sacred-gold" />
                        )}
                      </button>
                    );
                  })}

                  {/* Trailing empty cells */}
                  {Array.from({ length: Math.max(0, 42 - (firstDayOfMonth + daysInMonth)) }).map((_, i) => (
                    <div key={`te-${i}`} className="min-h-[80px] sm:min-h-[100px] bg-card/5" />
                  ))}
                </div>

                {/* Legend */}
                <div className="flex flex-wrap items-center justify-center gap-3 mt-2 text-[10px] text-muted-foreground">
                  <span>🌕 {language === 'hi' ? 'पूर्णिमा' : 'Purnima'}</span>
                  <span>🌑 {language === 'hi' ? 'अमावस्या' : 'Amavasya'}</span>
                  <span className="text-amber-400 font-semibold">{language === 'hi' ? 'पर्व' : 'Festival'}</span>
                  <span className="text-purple-400">{language === 'hi' ? 'व्रत' : 'Vrat'}</span>
                  <span className="text-red-400">{language === 'hi' ? 'रवि' : 'Sunday'}</span>
                </div>
              </>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

// ---- Small helper components ----

function PanchangRow({ label, value, icon, warn, good }: { label: string; value?: string; icon?: string; warn?: boolean; good?: boolean }) {
  if (!value) return null;
  return (
    <div className="flex items-start justify-between gap-1.5 text-[11px] leading-tight">
      <span className="text-muted-foreground whitespace-nowrap flex items-center gap-1">
        {icon && <span className="text-xs">{icon}</span>}
        {label}
      </span>
      <span className={`text-right font-medium ${warn ? 'text-red-400' : good ? 'text-green-400' : 'text-foreground'}`}>
        {value}
      </span>
    </div>
  );
}
