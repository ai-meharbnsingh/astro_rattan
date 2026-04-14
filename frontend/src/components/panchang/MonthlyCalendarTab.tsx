import { useState, useEffect, useMemo } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ChevronLeft, ChevronRight, Calendar, Moon, Sun, Star, Flame, Flag } from 'lucide-react';
import { api } from '@/lib/api';
import { translateBackend } from '@/lib/backend-translations';

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
  festival_hindi?: string;
}

interface FestivalDetail {
  name: string;
  type?: string;
  description?: string;
  rituals?: string;
}

const FIXED_FESTIVALS_BY_MMDD: Record<string, string[]> = {
  '01-01': ['New Year Day', 'Paush Putrada Ekadashi (Approx)'],
  '01-12': ['National Youth Day'],
  '01-13': ['Lohri'],
  '01-14': ['Makar Sankranti', 'Pongal', 'Uttarayana Punya Kala'],
  '01-15': ['Army Day'],
  '01-23': ['Netaji Jayanti'],
  '01-26': ['Republic Day', 'Vasant Panchami (Approx)'],
  '02-04': ['World Cancer Day'],
  '02-14': ['Valentine Day', 'Vijaya Ekadashi (Approx)'],
  '02-19': ['Shivaji Jayanti'],
  '02-26': ['Maha Shivaratri (Approx)'],
  '02-28': ['National Science Day'],
  '03-08': ['International Women Day'],
  '03-14': ['Holika Dahan (Approx)'],
  '03-15': ['Holi (Approx)'],
  '03-22': ['Chaitra Navratri Begins (Approx)'],
  '03-30': ['Ram Navami (Approx)'],
  '04-06': ['Hanuman Jayanti (Approx)'],
  '04-10': ['Mahavir Jayanti (Approx)'],
  '04-13': ['Baisakhi'],
  '04-14': ['Ambedkar Jayanti', 'Mesha Sankranti'],
  '04-18': ['Good Friday (Observed)'],
  '04-22': ['Earth Day'],
  '04-30': ['Akshaya Tritiya (Approx)'],
  '05-01': ['Labour Day', 'Maharashtra Day', 'Gujarat Day'],
  '05-11': ['National Technology Day'],
  '05-12': ['Buddha Purnima (Approx)'],
  '06-05': ['World Environment Day'],
  '06-21': ['International Yoga Day'],
  '06-27': ['Jagannath Rath Yatra (Approx)'],
  '07-10': ['Guru Purnima (Approx)'],
  '07-28': ['Hariyali Teej (Approx)'],
  '08-09': ['Raksha Bandhan (Approx)'],
  '08-15': ['Independence Day'],
  '08-16': ['Krishna Janmashtami (Approx)'],
  '08-27': ['Ganesh Chaturthi (Approx)'],
  '09-05': ['Teachers Day'],
  '09-22': ['Sharad Navratri Begins (Approx)'],
  '10-01': ['Maha Ashtami (Approx)'],
  '10-02': ['Gandhi Jayanti', 'Dussehra (Approx)'],
  '10-10': ['Karva Chauth (Approx)'],
  '10-20': ['Dhanteras (Approx)'],
  '10-21': ['Naraka Chaturdashi (Approx)'],
  '10-22': ['Diwali', 'Lakshmi Puja'],
  '10-23': ['Govardhan Puja'],
  '10-24': ['Bhai Dooj'],
  '10-31': ['National Unity Day'],
  '11-01': ['Kannada Rajyotsava'],
  '11-05': ['Dev Uthani Ekadashi (Approx)'],
  '11-15': ['Kartik Purnima (Approx)', 'Guru Nanak Jayanti (Approx)'],
  '12-04': ['Gita Jayanti (Approx)'],
  '12-25': ['Christmas'],
};

const uniqFestivals = (festivals: string[]) => {
  const seen = new Set<string>();
  return festivals.filter((name) => {
    const key = String(name || '').trim().toLowerCase();
    if (!key || seen.has(key)) return false;
    seen.add(key);
    return true;
  });
};

const uniqFestivalDetails = (items: FestivalDetail[]) => {
  const seen = new Set<string>();
  return items.filter((item) => {
    const key = String(item?.name || '').trim().toLowerCase();
    if (!key || seen.has(key)) return false;
    seen.add(key);
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
  const tithi = String(day.tithi || '').toLowerCase();
  const nakshatra = String(day.nakshatra || '').toLowerCase();
  const paksha = String(day.paksha || '').toLowerCase();
  const dateObj = new Date(`${day.date}T00:00:00`);
  const weekday = dateObj.getDay();
  const list: string[] = [];

  if (tithi.includes('ekadashi')) list.push('Ekadashi Vrat');
  if (tithi.includes('pradosh') || tithi.includes('trayodashi')) list.push('Pradosh Vrat');
  if (tithi.includes('amavasya')) list.push('Amavasya');
  if (tithi.includes('purnima')) list.push('Purnima');
  if (tithi.includes('chaturthi')) {
    list.push(paksha.includes('krishna') ? 'Sankashti Chaturthi' : 'Vinayaka Chaturthi (Monthly)');
  }
  if (tithi.includes('ashtami') && paksha.includes('krishna')) list.push('Kalashtami');
  if (tithi.includes('navami')) list.push('Navami Vrat');
  if (tithi.includes('saptami')) list.push('Saptami Vrat');
  if (tithi.includes('panchami')) list.push('Panchami Vrat');
  if (tithi.includes('dwadashi') || tithi.includes('dwadsi')) list.push('Dwadashi Parana');

  if (nakshatra.includes('shravana')) list.push('Shravana Nakshatra Vrat');
  if (nakshatra.includes('rohini')) list.push('Rohini Nakshatra Puja');
  if (nakshatra.includes('pushya')) list.push('Pushya Yoga Observance');
  if (nakshatra.includes('moola') || nakshatra.includes('mula')) list.push('Moola Nakshatra Shanti');

  if (weekday === 1) list.push('Somvar Vrat');
  if (weekday === 2) list.push('Mangalvar Vrat');
  if (weekday === 4) list.push('Guruvar Vrat');
  if (weekday === 5) list.push('Shukravar Vrat');
  if (weekday === 6) list.push('Shani Vrat');

  const mmdd = day.date.slice(5, 10);
  const fixed = FIXED_FESTIVALS_BY_MMDD[mmdd] || [];
  return uniqFestivals([...list, ...fixed]);
};

const enrichDayFestivals = (day: DayPanchang): DayPanchang => {
  const generated = generateObservances(day);
  const generatedDetails: FestivalDetail[] = generated.map((name) => ({ name, type: 'observance' }));
  const mergedDetails = uniqFestivalDetails([...(day.festival_details || []), ...generatedDetails]);
  return {
    ...day,
    festivals: uniqFestivals([...(day.festivals || []), ...generated, ...mergedDetails.map((f) => f.name)]),
    festival_details: mergedDetails,
  };
};

const mergeMonthlyFestivalDetails = (day: DayPanchang, extra: FestivalDetail[]) => {
  const mergedDetails = uniqFestivalDetails([...(day.festival_details || []), ...(extra || [])]);
  return {
    ...day,
    festivals: uniqFestivals([...(day.festivals || []), ...mergedDetails.map((f) => f.name)]),
    festival_details: mergedDetails,
  };
};

// Helper: Get local date as YYYY-MM-DD (fixes UTC timezone issue)
const getLocalDateString = () => {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
};

// Festival type icon helper
const festivalIcon = (name: string) => {
  const lower = name.toLowerCase();
  if (lower.includes('purnima') || lower.includes('amavasya'))
    return <Moon className="h-3 w-3 text-indigo-400 inline-block flex-shrink-0" />;
  if (lower.includes('sankranti'))
    return <Sun className="h-3 w-3 text-yellow-400 inline-block flex-shrink-0" />;
  if (lower.includes('ekadashi') || lower.includes('vrat') || lower.includes('pradosh') || lower.includes('chaturthi'))
    return <Star className="h-3 w-3 text-cyan-400 inline-block flex-shrink-0" />;
  if (lower.includes('republic') || lower.includes('independence') || lower.includes('gandhi') || lower.includes('ambedkar'))
    return <Flag className="h-3 w-3 text-green-400 inline-block flex-shrink-0" />;
  if (lower.includes('diwali') || lower.includes('deepawali') || lower.includes('holika') || lower.includes('dahan'))
    return <Flame className="h-3 w-3 text-orange-400 inline-block flex-shrink-0" />;
  return <Star className="h-3 w-3 text-purple-400 inline-block flex-shrink-0" />;
};

interface DayMarker {
  key: string;
  short: string;
  titleEn: string;
  titleHi: string;
  className: string;
}

const hasKeyword = (text: string, words: string[]) => words.some((w) => text.includes(w));
const markerDotClass = (key: string) => {
  switch (key) {
    case 'major': return 'bg-amber-500';
    case 'vrat': return 'bg-purple-500';
    case 'ekadashi': return 'bg-cyan-500';
    case 'purnima': return 'bg-indigo-500';
    case 'amavasya': return 'bg-slate-500';
    case 'sankranti': return 'bg-yellow-500';
    case 'moon-sign': return 'bg-blue-500';
    default: return 'bg-gray-400';
  }
};

const getFestivalTone = (name: string, type?: string) => {
  const text = `${name} ${type || ''}`.toLowerCase();
  if (hasKeyword(text, ['diwali', 'holi', 'dussehra', 'navratri', 'janmashtami', 'shivaratri', 'baisakhi', 'jayanti'])) {
    return 'bg-amber-500/10 border-amber-500/30';
  }
  if (hasKeyword(text, ['ekadashi', 'vrat', 'pradosh', 'chaturthi', 'somvar', 'mangalvar', 'guruvar', 'shani'])) {
    return 'bg-purple-500/10 border-purple-500/30';
  }
  if (hasKeyword(text, ['purnima', 'amavasya'])) {
    return 'bg-indigo-500/10 border-indigo-500/30';
  }
  if (hasKeyword(text, ['sankranti'])) {
    return 'bg-yellow-500/10 border-yellow-500/30';
  }
  return 'bg-cosmic-card/40 border-cosmic-border';
};

const getDayMarkers = (day: DayPanchang): DayMarker[] => {
  const allFest = day.festivals.join(' ').toLowerCase();
  const tithi = String(day.tithi || '').toLowerCase();
  const markers: DayMarker[] = [];

  const major = hasKeyword(allFest, [
    'diwali', 'deepawali', 'holi', 'dussehra', 'navratri', 'janmashtami', 'shivaratri',
    'ganesh', 'ram navami', 'hanuman jayanti', 'raksha bandhan', 'republic', 'independence',
    'christmas', 'guru nanak', 'mahavir', 'buddha purnima', 'pongal', 'lohri'
  ]);
  const vrat = hasKeyword(allFest, ['vrat', 'pradosh', 'somvar', 'mangalvar', 'guruvar', 'shukravar', 'shani']);
  const ekadashi = hasKeyword(allFest, ['ekadashi']) || tithi.includes('ekadashi');
  const purnima = hasKeyword(allFest, ['purnima']) || tithi.includes('purnima');
  const amavasya = hasKeyword(allFest, ['amavasya']) || tithi.includes('amavasya');
  const sankranti = hasKeyword(allFest, ['sankranti']);

  if (major) markers.push({ key: 'major', short: 'M', titleEn: 'Major Festival', titleHi: 'प्रमुख पर्व', className: 'bg-amber-500/20 text-amber-300 border border-amber-500/40' });
  if (vrat) markers.push({ key: 'vrat', short: 'V', titleEn: 'Vrat / Fast', titleHi: 'व्रत', className: 'bg-purple-500/15 text-purple-300 border border-purple-500/40' });
  if (ekadashi) markers.push({ key: 'ekadashi', short: 'E', titleEn: 'Ekadashi', titleHi: 'एकादशी', className: 'bg-cyan-500/15 text-cyan-300 border border-cyan-500/40' });
  if (purnima) markers.push({ key: 'purnima', short: 'P', titleEn: 'Purnima', titleHi: 'पूर्णिमा', className: 'bg-indigo-500/15 text-indigo-300 border border-indigo-500/40' });
  if (amavasya) markers.push({ key: 'amavasya', short: 'A', titleEn: 'Amavasya', titleHi: 'अमावस्या', className: 'bg-slate-500/25 text-slate-200 border border-slate-500/40' });
  if (sankranti) markers.push({ key: 'sankranti', short: 'S', titleEn: 'Sankranti', titleHi: 'संक्रांति', className: 'bg-yellow-500/20 text-yellow-300 border border-yellow-500/40' });
  if (day.moon_sign) markers.push({ key: 'moon-sign', short: 'R', titleEn: `Moon Sign: ${day.moon_sign}`, titleHi: `चंद्र राशि: ${day.moon_sign_hindi || day.moon_sign}`, className: 'bg-blue-500/15 text-blue-300 border border-blue-500/40' });

  return markers;
};

export default function MonthlyCalendarTab({ language, t, latitude, longitude }: Props) {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [monthlyData, setMonthlyData] = useState<DayPanchang[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedDay, setSelectedDay] = useState<DayPanchang | null>(null);

  const year = currentDate.getFullYear();
  const month = currentDate.getMonth();

  // Month names
  const monthNames = useMemo(() => ({
    en: ['January', 'February', 'March', 'April', 'May', 'June',
         'July', 'August', 'September', 'October', 'November', 'December'],
    hi: ['जनवरी', 'फरवरी', 'मार्च', 'अप्रैल', 'मई', 'जून',
         'जुलाई', 'अगस्त', 'सितंबर', 'अक्टूबर', 'नवंबर', 'दिसंबर']
  }), []);

  // Weekday names
  const weekdays = useMemo(() => ({
    en: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
    hi: ['रवि', 'सोम', 'मंगल', 'बुध', 'गुरु', 'शुक्र', 'शनि']
  }), []);

  // Fetch monthly data using batch endpoint
  useEffect(() => {
    const fetchMonthly = async () => {
      setLoading(true);
      let monthlyFestivalMap: Record<string, FestivalDetail[]> = {};
      try {
        const monthlyRes: any = await api.get(`/api/festivals?year=${year}&month=${month + 1}`);
        const monthlyRows: any[] = monthlyRes?.festivals || monthlyRes?.data?.festivals || [];
        monthlyFestivalMap = monthlyRows.reduce((acc: Record<string, FestivalDetail[]>, row: any) => {
          const dateStr = String(row?.date || '').slice(0, 10);
          const detail = normalizeFestivalDetail(row);
          if (!dateStr || !detail) return acc;
          acc[dateStr] = [...(acc[dateStr] || []), detail];
          return acc;
        }, {});
      } catch (_) {
        monthlyFestivalMap = {};
      }
      try {
        const res = await api.get(`/api/panchang/month?month=${month + 1}&year=${year}&latitude=${latitude}&longitude=${longitude}`);
        const rawDays = (res as any)?.days || res || [];

        const data: DayPanchang[] = rawDays.map((p: any) => {
          const baseDetailsRaw = Array.isArray(p.festivals) ? p.festivals : (p.festivals ? [p.festivals] : []);
          const baseDetails = uniqFestivalDetails(baseDetailsRaw.map((f: any) => normalizeFestivalDetail(f)).filter(Boolean) as FestivalDetail[]);
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
          return mergeMonthlyFestivalDetails(day, monthlyFestivalMap[String(p.date || '').slice(0, 10)] || []);
        });

        setMonthlyData(data);

        // Select today if current month
        const today = getLocalDateString();
        const todayData = data.find((d: DayPanchang) => d.date === today);
        setSelectedDay(todayData || data[0] || null);
      } catch (e) {
        // Fallback: fetch individual days if batch endpoint fails
        try {
          const daysInMonth = new Date(year, month + 1, 0).getDate();
          const data: DayPanchang[] = [];

          for (let day = 1; day <= daysInMonth; day++) {
            const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
            try {
              const dayRes = await api.get(`/api/panchang?date=${dateStr}&latitude=${latitude}&longitude=${longitude}`);
              const p = dayRes as any;
              const festsRaw = Array.isArray(p.festivals) ? p.festivals : (p.festivals ? [p.festivals] : []);
              const festDetails = uniqFestivalDetails(festsRaw.map((f: any) => normalizeFestivalDetail(f)).filter(Boolean) as FestivalDetail[]);
              const dayData = enrichDayFestivals({
                date: dateStr,
                tithi: p.tithi?.name || '',
                tithi_hindi: p.tithi?.name_hindi,
                nakshatra: p.nakshatra?.name || '',
                nakshatra_hindi: p.nakshatra?.name_hindi,
                paksha: p.tithi?.paksha || '',
                paksha_hindi: p.tithi?.paksha_hindi,
                moon_sign: p.moon_sign || p.chandra_rashi || '',
                moon_sign_hindi: p.moon_sign_hindi || p.chandra_rashi_hindi || '',
                sunrise: p.sunrise || '',
                sunset: p.sunset || '',
                festivals: festDetails.map((f) => f.name),
                festival_details: festDetails,
              });
              data.push(mergeMonthlyFestivalDetails(dayData, monthlyFestivalMap[dateStr] || []));
            } catch (_) {
              // Skip failed days
            }
          }
          setMonthlyData(data);

          const today = getLocalDateString();
          const todayData = data.find(d => d.date === today);
          setSelectedDay(todayData || data[0] || null);
        } catch (_) {
          setMonthlyData([]);
        }
      }
      setLoading(false);
    };

    fetchMonthly();
  }, [year, month, latitude, longitude]);

  // Calendar grid
  const firstDayOfMonth = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const trailingEmptyCells = Math.max(0, 42 - (firstDayOfMonth + daysInMonth));
  const today = getLocalDateString();

  const prevMonth = () => setCurrentDate(new Date(year, month - 1, 1));
  const nextMonth = () => setCurrentDate(new Date(year, month + 1, 1));

  const getDayData = (day: number) => {
    const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    return monthlyData.find(d => d.date === dateStr);
  };

  // Count total festivals in the month
  const festivalCount = monthlyData.reduce((sum, d) => sum + d.festivals.length, 0);

  return (
    <div className="space-y-3">
      {/* Month Navigation */}
      <Card className="card-sacred !py-0 !gap-0">
        <CardContent className="p-1.5 sm:p-2">
          <div className="flex items-center justify-between">
            <Button variant="outline" size="icon" onClick={prevMonth} className="border-sacred-gold/30 h-7 w-7 sm:h-8 sm:w-8">
              <ChevronLeft className="h-3.5 w-3.5" />
            </Button>
            <div className="text-center">
              <h3 className="text-base sm:text-lg font-bold text-cosmic-text-primary leading-tight">
                {language === 'hi' ? monthNames.hi[month] : monthNames.en[month]} {year}
              </h3>
              {festivalCount > 0 && (
                <p className="text-[10px] text-purple-400 mt-0">
                  {festivalCount} {language === 'hi' ? 'त्योहार / व्रत' : 'festivals / observances'}
                </p>
              )}
            </div>
            <Button variant="outline" size="icon" onClick={nextMonth} className="border-sacred-gold/30 h-7 w-7 sm:h-8 sm:w-8">
              <ChevronRight className="h-3.5 w-3.5" />
            </Button>
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-3">
        {/* Calendar Grid */}
        <Card className="card-sacred lg:col-span-2">
          <CardContent className="p-2 sm:p-3 h-full flex flex-col">
            {loading ? (
              <div className="flex items-center justify-center h-64">
                <div className="animate-spin h-8 w-8 border-2 border-sacred-gold border-t-transparent rounded-full" />
              </div>
            ) : (
              <>
                {/* Weekday Headers */}
                <div className="grid grid-cols-7 gap-1 mb-1">
                  {weekdays[language === 'hi' ? 'hi' : 'en'].map((day) => (
                    <div key={day} className="text-center text-xs font-semibold text-sacred-gold py-1">
                      {day}
                    </div>
                  ))}
                </div>

                {/* Calendar Days - Clean Design */}
                <div className="grid grid-cols-7 grid-rows-6 gap-1.5 flex-1 min-h-0">
                  {/* Empty cells for padding */}
                  {Array.from({ length: firstDayOfMonth }).map((_, i) => (
                    <div key={`empty-start-${i}`} className="h-full min-h-[56px] sm:min-h-[64px]" />
                  ))}

                  {/* Day cells - Minimal Clean Design */}
                  {Array.from({ length: daysInMonth }, (_, i) => i + 1).map((day) => {
                    const dayData = getDayData(day);
                    const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
                    const isToday = dateStr === today;
                    const isSelected = selectedDay?.date === dateStr;
                    const hasFestivals = dayData && dayData.festivals.length > 0;
                    const dayMarkers = dayData ? getDayMarkers(dayData) : [];
                    const hasMajorFestival = dayMarkers.some((m) => m.key === 'major');

                    return (
                      <button
                        key={day}
                        onClick={() => dayData && setSelectedDay(dayData)}
                        className={`
                          h-full min-h-[56px] sm:min-h-[64px] p-1 rounded-lg relative overflow-hidden
                          transition-all hover:scale-[1.02]
                          ${isToday ? 'ring-2 ring-sacred-gold bg-sacred-gold/10' : ''}
                          ${isSelected ? 'bg-sacred-gold/20 border border-sacred-gold' : 'bg-cosmic-card/20 hover:bg-cosmic-card/40'}
                          ${hasMajorFestival ? 'border-l-2 border-l-amber-500' : hasFestivals ? 'border-l-2 border-l-purple-400/50' : ''}
                        `}
                      >
                        {/* Day Number */}
                        <div className={`text-center text-sm sm:text-base font-bold mb-0.5 ${isToday ? 'text-sacred-gold' : 'text-cosmic-text-primary'}`}>
                          {day}
                        </div>
                        
                        {/* Marker Badges - Compact */}
                        {dayMarkers.length > 0 && (
                          <div className="flex flex-wrap justify-center gap-0.5 px-0.5">
                            {dayMarkers.slice(0, 3).map((marker) => (
                              <span
                                key={marker.key}
                                title={language === 'hi' ? marker.titleHi : marker.titleEn}
                                className={`text-[9px] leading-3 px-1 rounded font-semibold ${marker.className}`}
                              >
                                {marker.short}
                              </span>
                            ))}
                          </div>
                        )}
                        
                        {/* Festival indicator for non-marker festivals */}
                        {hasFestivals && dayMarkers.length === 0 && (
                          <div className="flex justify-center">
                            <span className="w-1.5 h-1.5 rounded-full bg-purple-400" />
                          </div>
                        )}
                      </button>
                    );
                  })}

                  {/* Trailing empty cells */}
                  {Array.from({ length: trailingEmptyCells }).map((_, i) => (
                    <div key={`empty-end-${i}`} className="h-full min-h-[56px] sm:min-h-[64px]" />
                  ))}
                </div>

                {/* Legend with Badges */}
                <div className="flex flex-wrap items-center justify-center gap-2 mt-3 text-[10px] sm:text-xs">
                  <div className="flex items-center gap-1">
                    <span className="px-1 rounded text-[9px] font-semibold bg-amber-500/20 text-amber-300 border border-amber-500/40">M</span>
                    <span className="text-cosmic-text-secondary">{language === 'hi' ? 'प्रमुख पर्व' : 'Major'}</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <span className="px-1 rounded text-[9px] font-semibold bg-purple-500/15 text-purple-300 border border-purple-500/40">V</span>
                    <span className="text-cosmic-text-secondary">{language === 'hi' ? 'व्रत' : 'Vrat'}</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <span className="px-1 rounded text-[9px] font-semibold bg-cyan-500/15 text-cyan-300 border border-cyan-500/40">E</span>
                    <span className="text-cosmic-text-secondary">{language === 'hi' ? 'एकादशी' : 'Ekadashi'}</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <span className="px-1 rounded text-[9px] font-semibold bg-indigo-500/15 text-indigo-300 border border-indigo-500/40">P</span>
                    <span className="text-cosmic-text-secondary">{language === 'hi' ? 'पूर्णिमा' : 'Purnima'}</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <span className="px-1 rounded text-[9px] font-semibold bg-slate-500/25 text-slate-200 border border-slate-500/40">A</span>
                    <span className="text-cosmic-text-secondary">{language === 'hi' ? 'अमावस्या' : 'Amavasya'}</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <span className="px-1 rounded text-[9px] font-semibold bg-yellow-500/20 text-yellow-300 border border-yellow-500/40">S</span>
                    <span className="text-cosmic-text-secondary">{language === 'hi' ? 'संक्रांति' : 'Sankranti'}</span>
                  </div>
                </div>
              </>
            )}
          </CardContent>
        </Card>

        {/* Selected Day Details */}
        <Card className="card-sacred">
          <CardContent className="p-2 sm:p-3 h-full">
            <h4 className="font-semibold text-cosmic-text-primary mb-2 flex items-center gap-2">
              <Calendar className="h-4 w-4 text-sacred-gold" />
              {language === 'hi' ? 'विवरण' : 'Details'}
            </h4>

            {selectedDay ? (
              <div className="space-y-2">
                <div className="text-center pb-2 border-b border-cosmic-border">
                  <p className="text-xs sm:text-sm text-cosmic-text-secondary">
                    {new Date(selectedDay.date + 'T00:00:00').toLocaleDateString(language === 'hi' ? 'hi-IN' : 'en-US', {
                      weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
                    })}
                  </p>
                </div>

                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-xs sm:text-sm text-cosmic-text-secondary">{language === 'hi' ? 'तिथि' : 'Tithi'}</span>
                    <span className="text-xs sm:text-sm font-medium text-cosmic-text-primary">
                      {language === 'hi'
                        ? selectedDay.tithi_hindi || translateBackend(selectedDay.tithi, language)
                        : selectedDay.tithi}
                    </span>
                  </div>

                  <div className="flex justify-between">
                    <span className="text-xs sm:text-sm text-cosmic-text-secondary">{language === 'hi' ? 'नक्षत्र' : 'Nakshatra'}</span>
                    <span className="text-xs sm:text-sm font-medium text-cosmic-text-primary">
                      {language === 'hi'
                        ? selectedDay.nakshatra_hindi || translateBackend(selectedDay.nakshatra, language)
                        : selectedDay.nakshatra}
                    </span>
                  </div>

                  <div className="flex justify-between">
                    <span className="text-xs sm:text-sm text-cosmic-text-secondary">{language === 'hi' ? 'पक्ष' : 'Paksha'}</span>
                    <span className="text-xs sm:text-sm font-medium text-cosmic-text-primary">
                      {language === 'hi'
                        ? selectedDay.paksha_hindi || translateBackend(selectedDay.paksha, language)
                        : selectedDay.paksha}
                    </span>
                  </div>
                  {selectedDay.moon_sign && (
                    <div className="flex justify-between">
                      <span className="text-xs sm:text-sm text-cosmic-text-secondary">{language === 'hi' ? 'चंद्र राशि' : 'Moon Sign'}</span>
                      <span className="text-xs sm:text-sm font-medium text-cosmic-text-primary">
                        {language === 'hi'
                          ? selectedDay.moon_sign_hindi || translateBackend(selectedDay.moon_sign, language)
                          : selectedDay.moon_sign}
                      </span>
                    </div>
                  )}

                  <div className="flex justify-between">
                    <span className="text-xs sm:text-sm text-cosmic-text-secondary">{language === 'hi' ? 'सूर्योदय' : 'Sunrise'}</span>
                    <span className="text-xs sm:text-sm font-medium text-cosmic-text-primary">{selectedDay.sunrise}</span>
                  </div>

                  <div className="flex justify-between">
                    <span className="text-xs sm:text-sm text-cosmic-text-secondary">{language === 'hi' ? 'सूर्यास्त' : 'Sunset'}</span>
                    <span className="text-xs sm:text-sm font-medium text-cosmic-text-primary">{selectedDay.sunset}</span>
                  </div>

                  {/* Festival list -- show ALL festivals for the day */}
                  {selectedDay.festivals.length > 0 && (
                    <div className="mt-2 space-y-1.5">
                      <div className="flex flex-wrap gap-1">
                        {getDayMarkers(selectedDay).map((marker) => (
                          <span key={marker.key} className={`px-1.5 py-0.5 rounded text-[10px] font-semibold ${marker.className}`}>
                            {language === 'hi' ? marker.titleHi : marker.titleEn}
                          </span>
                        ))}
                      </div>
                      <span className="text-xs font-semibold text-purple-400 uppercase tracking-wide">
                        {language === 'hi' ? 'त्योहार / व्रत' : 'Festivals & Observances'}
                      </span>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                      {selectedDay.festivals.map((fest, idx) => (
                        (() => {
                          const detail = selectedDay.festival_details.find((d) => d.name === fest);
                          return (
                            <div
                              key={idx}
                              className={`p-2 rounded-lg border flex items-start gap-2 ${getFestivalTone(fest, detail?.type)}`}
                            >
                              {festivalIcon(fest)}
                              <div className="min-w-0">
                                <p className="text-xs sm:text-sm font-medium text-cosmic-text-primary leading-tight">
                                  {language === 'hi' ? translateBackend(fest, language) : fest}
                                </p>
                                {detail?.type && (
                                  <p className="text-[10px] text-cosmic-text-secondary mt-0.5">
                                    {language === 'hi' ? 'प्रकार' : 'Type'}: {detail.type}
                                  </p>
                                )}
                                {detail?.description && (
                                  <p className="text-[10px] text-cosmic-text-secondary mt-0.5 leading-snug">
                                    {detail.description}
                                  </p>
                                )}
                                {detail?.rituals && (
                                  <p className="text-[10px] text-cosmic-text-secondary mt-0.5 leading-snug">
                                    {language === 'hi' ? 'विधि' : 'Rituals'}: {detail.rituals}
                                  </p>
                                )}
                              </div>
                            </div>
                          );
                        })()
                      ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ) : (
              <p className="text-center text-cosmic-text-secondary py-8">
                {language === 'hi' ? 'दिन चुनें' : 'Select a day'}
              </p>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
