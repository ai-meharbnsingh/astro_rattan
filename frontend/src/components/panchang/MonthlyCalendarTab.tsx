import { useState, useEffect, useMemo } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ChevronLeft, ChevronRight, Calendar, Moon, Sun, Star, Flame, Flag } from 'lucide-react';
import { api } from '@/lib/api';

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
  sunrise: string;
  sunset: string;
  festivals: string[];
  festival_hindi?: string;
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
  return {
    ...day,
    festivals: uniqFestivals([...(day.festivals || []), ...generated]),
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
  if (lower.includes('republic') || lower.includes('independence') || lower.includes('gandhi') || lower.includes('ambedkar'))
    return <Flag className="h-3 w-3 text-green-400 inline-block flex-shrink-0" />;
  if (lower.includes('diwali') || lower.includes('deepawali') || lower.includes('holika') || lower.includes('dahan'))
    return <Flame className="h-3 w-3 text-orange-400 inline-block flex-shrink-0" />;
  return <Star className="h-3 w-3 text-purple-400 inline-block flex-shrink-0" />;
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
      try {
        const res = await api.get(`/api/panchang/month?month=${month + 1}&year=${year}&latitude=${latitude}&longitude=${longitude}`);
        const rawDays = (res as any)?.days || res || [];

        const data: DayPanchang[] = rawDays.map((p: any) => enrichDayFestivals({
          date: p.date || '',
          tithi: p.tithi || '',
          tithi_hindi: p.tithi_hindi,
          nakshatra: p.nakshatra || '',
          nakshatra_hindi: p.nakshatra_hindi,
          paksha: p.paksha || '',
          paksha_hindi: p.paksha_hindi,
          sunrise: p.sunrise || '',
          sunset: p.sunset || '',
          festivals: Array.isArray(p.festivals)
            ? p.festivals.map((f: any) => typeof f === 'string' ? f : f.name || '')
            : (p.festivals ? [typeof p.festivals === 'string' ? p.festivals : (p.festivals as any).name || ''] : []),
        }));

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
              const fests = p.festivals || [];
              data.push(enrichDayFestivals({
                date: dateStr,
                tithi: p.tithi?.name || '',
                tithi_hindi: p.tithi?.name_hindi,
                nakshatra: p.nakshatra?.name || '',
                nakshatra_hindi: p.nakshatra?.name_hindi,
                paksha: p.tithi?.paksha || '',
                paksha_hindi: p.tithi?.paksha_hindi,
                sunrise: p.sunrise || '',
                sunset: p.sunset || '',
                festivals: fests.map((f: any) => typeof f === 'string' ? f : f.name || ''),
              }));
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
          <CardContent className="p-2 sm:p-3">
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

                {/* Calendar Days */}
                <div className="grid grid-cols-7 gap-1">
                  {/* Empty cells for padding */}
                  {Array.from({ length: firstDayOfMonth }).map((_, i) => (
                    <div key={`empty-${i}`} className="aspect-square" />
                  ))}

                  {/* Day cells */}
                  {Array.from({ length: daysInMonth }, (_, i) => i + 1).map((day) => {
                    const dayData = getDayData(day);
                    const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
                    const isToday = dateStr === today;
                    const isSelected = selectedDay?.date === dateStr;
                    const isShukla = dayData?.paksha === 'Shukla';
                    const hasFestivals = dayData && dayData.festivals.length > 0;
                    const hasMajorFestival = hasFestivals && dayData.festivals.some(
                      f => !['Ekadashi Vrat', 'Purnima', 'Amavasya', 'Pradosh Vrat', 'Sankashti Chaturthi',
                             'Masik Shivaratri', 'Kalashtami', 'Vivah Panchami / Surya Saptami'].includes(f)
                    );

                    return (
                      <button
                        key={day}
                        onClick={() => dayData && setSelectedDay(dayData)}
                        className={`
                          h-14 sm:h-16 lg:h-14 xl:h-16 p-1 rounded-lg text-left text-[11px] sm:text-xs relative
                          transition-all hover:scale-105
                          ${isToday ? 'ring-2 ring-sacred-gold' : ''}
                          ${isSelected ? 'bg-sacred-gold/20 border border-sacred-gold' : 'bg-cosmic-card/30 hover:bg-cosmic-card/50'}
                          ${hasMajorFestival ? 'border-l-2 border-l-amber-500' : hasFestivals ? 'border-l-2 border-l-purple-500/60' : ''}
                        `}
                      >
                        <span className={`font-semibold text-xs sm:text-sm ${isToday ? 'text-sacred-gold' : 'text-cosmic-text-primary'}`}>
                          {day}
                        </span>
                        {dayData && (
                          <>
                            <div className="text-[9px] sm:text-[10px] text-cosmic-text-secondary truncate mt-0.5 leading-tight">
                              {language === 'hi' ? dayData.tithi_hindi || dayData.tithi : dayData.tithi}
                            </div>
                            {hasFestivals && (
                              <div className="text-[9px] text-purple-400 leading-tight mt-0.5 flex items-center gap-0.5">
                                {festivalIcon(dayData.festivals[0])}
                              </div>
                            )}
                            {/* Badge for multiple festivals */}
                            {dayData.festivals.length > 1 && (
                              <span className="absolute top-0.5 right-0.5 bg-purple-500 text-white text-[8px] rounded-full w-3 h-3 flex items-center justify-center font-bold">
                                {dayData.festivals.length}
                              </span>
                            )}
                            <div className="absolute bottom-0.5 right-0.5">
                              {isShukla ? (
                                <Sun className="h-2.5 w-2.5 text-orange-400" />
                              ) : (
                                <Moon className="h-2.5 w-2.5 text-indigo-400" />
                              )}
                            </div>
                          </>
                        )}
                      </button>
                    );
                  })}
                </div>

                {/* Legend */}
                <div className="flex flex-wrap items-center gap-2 mt-2 text-[10px] sm:text-xs">
                  <div className="flex items-center gap-1">
                    <Sun className="h-3 w-3 text-orange-400" />
                    <span className="text-cosmic-text-secondary">{language === 'hi' ? 'शुक्ल' : 'Shukla'}</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <Moon className="h-3 w-3 text-indigo-400" />
                    <span className="text-cosmic-text-secondary">{language === 'hi' ? 'कृष्ण' : 'Krishna'}</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <div className="w-1 h-3 rounded-sm bg-amber-500" />
                    <span className="text-cosmic-text-secondary">{language === 'hi' ? 'प्रमुख त्योहार' : 'Major Festival'}</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <div className="w-1 h-3 rounded-sm bg-purple-500/60" />
                    <span className="text-cosmic-text-secondary">{language === 'hi' ? 'व्रत / पर्व' : 'Vrat / Observance'}</span>
                  </div>
                </div>
              </>
            )}
          </CardContent>
        </Card>

        {/* Selected Day Details */}
        <Card className="card-sacred">
          <CardContent className="p-2 sm:p-3">
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
                      {language === 'hi' ? selectedDay.tithi_hindi || selectedDay.tithi : selectedDay.tithi}
                    </span>
                  </div>

                  <div className="flex justify-between">
                    <span className="text-xs sm:text-sm text-cosmic-text-secondary">{language === 'hi' ? 'नक्षत्र' : 'Nakshatra'}</span>
                    <span className="text-xs sm:text-sm font-medium text-cosmic-text-primary">
                      {language === 'hi' ? selectedDay.nakshatra_hindi || selectedDay.nakshatra : selectedDay.nakshatra}
                    </span>
                  </div>

                  <div className="flex justify-between">
                    <span className="text-xs sm:text-sm text-cosmic-text-secondary">{language === 'hi' ? 'पक्ष' : 'Paksha'}</span>
                    <span className="text-xs sm:text-sm font-medium text-cosmic-text-primary">
                      {language === 'hi' ? selectedDay.paksha_hindi || selectedDay.paksha : selectedDay.paksha}
                    </span>
                  </div>

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
                      <span className="text-xs font-semibold text-purple-400 uppercase tracking-wide">
                        {language === 'hi' ? 'त्योहार / व्रत' : 'Festivals & Observances'}
                      </span>
                      {selectedDay.festivals.map((fest, idx) => (
                        <div
                          key={idx}
                          className="p-2 rounded-lg bg-purple-500/10 border border-purple-500/30 flex items-start gap-2"
                        >
                          {festivalIcon(fest)}
                          <p className="text-xs sm:text-sm font-medium text-cosmic-text-primary leading-tight">
                            {fest}
                          </p>
                        </div>
                      ))}
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
