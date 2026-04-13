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
        const res = await api.get(`/api/panchang/month?month=${month + 1}&year=${year}&lat=${latitude}&lon=${longitude}`);
        const rawDays = res.data?.days || [];

        const data: DayPanchang[] = rawDays.map((p: any) => ({
          date: p.date || '',
          tithi: p.tithi || '',
          tithi_hindi: p.tithi_hindi,
          nakshatra: p.nakshatra || '',
          nakshatra_hindi: p.nakshatra_hindi,
          paksha: p.paksha || '',
          paksha_hindi: p.paksha_hindi,
          sunrise: p.sunrise || '',
          sunset: p.sunset || '',
          festivals: Array.isArray(p.festivals) ? p.festivals : (p.festivals ? [p.festivals] : []),
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
              const dayRes = await api.get(`/api/panchang?date=${dateStr}&lat=${latitude}&lon=${longitude}`);
              const p = dayRes.data;
              const fests = p.festivals || [];
              data.push({
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
              });
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
    <div className="space-y-6">
      {/* Month Navigation */}
      <Card className="card-sacred">
        <CardContent className="p-4">
          <div className="flex items-center justify-between">
            <Button variant="outline" size="icon" onClick={prevMonth} className="border-sacred-gold/30">
              <ChevronLeft className="h-5 w-5" />
            </Button>
            <div className="text-center">
              <h3 className="text-xl font-bold text-cosmic-text-primary">
                {language === 'hi' ? monthNames.hi[month] : monthNames.en[month]} {year}
              </h3>
              {festivalCount > 0 && (
                <p className="text-xs text-purple-400 mt-1">
                  {festivalCount} {language === 'hi' ? 'त्योहार / व्रत' : 'festivals / observances'}
                </p>
              )}
            </div>
            <Button variant="outline" size="icon" onClick={nextMonth} className="border-sacred-gold/30">
              <ChevronRight className="h-5 w-5" />
            </Button>
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Calendar Grid */}
        <Card className="card-sacred lg:col-span-2">
          <CardContent className="p-4">
            {loading ? (
              <div className="flex items-center justify-center h-64">
                <div className="animate-spin h-8 w-8 border-2 border-sacred-gold border-t-transparent rounded-full" />
              </div>
            ) : (
              <>
                {/* Weekday Headers */}
                <div className="grid grid-cols-7 gap-1 mb-2">
                  {weekdays[language === 'hi' ? 'hi' : 'en'].map((day) => (
                    <div key={day} className="text-center text-sm font-semibold text-sacred-gold py-2">
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
                          aspect-square p-1 rounded-lg text-left text-xs sm:text-sm relative
                          transition-all hover:scale-105
                          ${isToday ? 'ring-2 ring-sacred-gold' : ''}
                          ${isSelected ? 'bg-sacred-gold/20 border border-sacred-gold' : 'bg-cosmic-card/30 hover:bg-cosmic-card/50'}
                          ${hasMajorFestival ? 'border-l-2 border-l-amber-500' : hasFestivals ? 'border-l-2 border-l-purple-500/60' : ''}
                        `}
                      >
                        <span className={`font-semibold ${isToday ? 'text-sacred-gold' : 'text-cosmic-text-primary'}`}>
                          {day}
                        </span>
                        {dayData && (
                          <>
                            <div className="text-[10px] text-cosmic-text-secondary truncate mt-0.5 leading-tight">
                              {language === 'hi' ? dayData.tithi_hindi || dayData.tithi : dayData.tithi}
                            </div>
                            {/* Show first festival name if any */}
                            {hasFestivals && (
                              <div className="text-[9px] text-purple-400 truncate leading-tight mt-0.5 flex items-center gap-0.5">
                                {festivalIcon(dayData.festivals[0])}
                                <span className="truncate">{dayData.festivals[0]}</span>
                              </div>
                            )}
                            {/* Badge for multiple festivals */}
                            {dayData.festivals.length > 1 && (
                              <span className="absolute top-0.5 right-0.5 bg-purple-500 text-white text-[8px] rounded-full w-3.5 h-3.5 flex items-center justify-center font-bold">
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
                <div className="flex flex-wrap items-center gap-4 mt-4 text-xs">
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
          <CardContent className="p-4">
            <h4 className="font-semibold text-cosmic-text-primary mb-4 flex items-center gap-2">
              <Calendar className="h-4 w-4 text-sacred-gold" />
              {language === 'hi' ? 'विवरण' : 'Details'}
            </h4>

            {selectedDay ? (
              <div className="space-y-4">
                <div className="text-center pb-4 border-b border-cosmic-border">
                  <p className="text-sm text-cosmic-text-secondary">
                    {new Date(selectedDay.date + 'T00:00:00').toLocaleDateString(language === 'hi' ? 'hi-IN' : 'en-US', {
                      weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
                    })}
                  </p>
                </div>

                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-sm text-cosmic-text-secondary">{language === 'hi' ? 'तिथि' : 'Tithi'}</span>
                    <span className="text-sm font-medium text-cosmic-text-primary">
                      {language === 'hi' ? selectedDay.tithi_hindi || selectedDay.tithi : selectedDay.tithi}
                    </span>
                  </div>

                  <div className="flex justify-between">
                    <span className="text-sm text-cosmic-text-secondary">{language === 'hi' ? 'नक्षत्र' : 'Nakshatra'}</span>
                    <span className="text-sm font-medium text-cosmic-text-primary">
                      {language === 'hi' ? selectedDay.nakshatra_hindi || selectedDay.nakshatra : selectedDay.nakshatra}
                    </span>
                  </div>

                  <div className="flex justify-between">
                    <span className="text-sm text-cosmic-text-secondary">{language === 'hi' ? 'पक्ष' : 'Paksha'}</span>
                    <span className="text-sm font-medium text-cosmic-text-primary">
                      {language === 'hi' ? selectedDay.paksha_hindi || selectedDay.paksha : selectedDay.paksha}
                    </span>
                  </div>

                  <div className="flex justify-between">
                    <span className="text-sm text-cosmic-text-secondary">{language === 'hi' ? 'सूर्योदय' : 'Sunrise'}</span>
                    <span className="text-sm font-medium text-cosmic-text-primary">{selectedDay.sunrise}</span>
                  </div>

                  <div className="flex justify-between">
                    <span className="text-sm text-cosmic-text-secondary">{language === 'hi' ? 'सूर्यास्त' : 'Sunset'}</span>
                    <span className="text-sm font-medium text-cosmic-text-primary">{selectedDay.sunset}</span>
                  </div>

                  {/* Festival list -- show ALL festivals for the day */}
                  {selectedDay.festivals.length > 0 && (
                    <div className="mt-4 space-y-2">
                      <span className="text-xs font-semibold text-purple-400 uppercase tracking-wide">
                        {language === 'hi' ? 'त्योहार / व्रत' : 'Festivals & Observances'}
                      </span>
                      {selectedDay.festivals.map((fest, idx) => (
                        <div
                          key={idx}
                          className="p-2.5 rounded-lg bg-purple-500/10 border border-purple-500/30 flex items-start gap-2"
                        >
                          {festivalIcon(fest)}
                          <p className="text-sm font-medium text-cosmic-text-primary leading-tight">
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
