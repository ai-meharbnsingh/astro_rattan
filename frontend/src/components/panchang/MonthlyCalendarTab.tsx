import { useState, useEffect, useMemo } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ChevronLeft, ChevronRight, Calendar, Moon, Sun } from 'lucide-react';
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
  festival?: string;
  festival_hindi?: string;
}

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

  // Fetch monthly data
  useEffect(() => {
    const fetchMonthly = async () => {
      setLoading(true);
      try {
        // Generate array of dates for the month
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        const data: DayPanchang[] = [];
        
        for (let day = 1; day <= daysInMonth; day++) {
          const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
          try {
            const res = await api.get(`/api/panchang?date=${dateStr}&lat=${latitude}&lon=${longitude}`);
            const p = res.data;
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
              festival: p.festivals?.[0]?.name,
              festival_hindi: p.festivals?.[0]?.name_hindi,
            });
          } catch (e) {
            // Skip failed days
          }
        }
        setMonthlyData(data);
        
        // Select today if current month
        const today = new Date().toISOString().split('T')[0];
        const todayData = data.find(d => d.date === today);
        setSelectedDay(todayData || data[0] || null);
      } catch (e) {
        setMonthlyData([]);
      }
      setLoading(false);
    };
    
    fetchMonthly();
  }, [year, month, latitude, longitude]);

  // Calendar grid
  const firstDayOfMonth = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const today = new Date().toISOString().split('T')[0];

  const prevMonth = () => setCurrentDate(new Date(year, month - 1, 1));
  const nextMonth = () => setCurrentDate(new Date(year, month + 1, 1));

  const getDayData = (day: number) => {
    const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    return monthlyData.find(d => d.date === dateStr);
  };

  return (
    <div className="space-y-6">
      {/* Month Navigation */}
      <Card className="card-sacred">
        <CardContent className="p-4">
          <div className="flex items-center justify-between">
            <Button variant="outline" size="icon" onClick={prevMonth} className="border-sacred-gold/30">
              <ChevronLeft className="h-5 w-5" />
            </Button>
            <h3 className="text-xl font-bold text-cosmic-text-primary">
              {language === 'hi' ? monthNames.hi[month] : monthNames.en[month]} {year}
            </h3>
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

                    return (
                      <button
                        key={day}
                        onClick={() => dayData && setSelectedDay(dayData)}
                        className={`
                          aspect-square p-1 rounded-lg text-left text-sm relative
                          transition-all hover:scale-105
                          ${isToday ? 'ring-2 ring-sacred-gold' : ''}
                          ${isSelected ? 'bg-sacred-gold/20 border border-sacred-gold' : 'bg-cosmic-card/30 hover:bg-cosmic-card/50'}
                          ${dayData?.festival ? 'border-l-2 border-l-purple-500' : ''}
                        `}
                      >
                        <span className={`font-semibold ${isToday ? 'text-sacred-gold' : 'text-cosmic-text-primary'}`}>
                          {day}
                        </span>
                        {dayData && (
                          <>
                            <div className="text-xs text-cosmic-text-secondary truncate mt-1">
                              {language === 'hi' ? dayData.tithi_hindi || dayData.tithi : dayData.tithi}
                            </div>
                            <div className="absolute bottom-1 right-1">
                              {isShukla ? (
                                <Sun className="h-3 w-3 text-orange-400" />
                              ) : (
                                <Moon className="h-3 w-3 text-indigo-400" />
                              )}
                            </div>
                          </>
                        )}
                      </button>
                    );
                  })}
                </div>

                {/* Legend */}
                <div className="flex items-center gap-4 mt-4 text-xs">
                  <div className="flex items-center gap-1">
                    <Sun className="h-3 w-3 text-orange-400" />
                    <span className="text-cosmic-text-secondary">{language === 'hi' ? 'शुक्ल' : 'Shukla'}</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <Moon className="h-3 w-3 text-indigo-400" />
                    <span className="text-cosmic-text-secondary">{language === 'hi' ? 'कृष्ण' : 'Krishna'}</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <div className="w-2 h-2 rounded-full bg-purple-500" />
                    <span className="text-cosmic-text-secondary">{language === 'hi' ? 'त्योहार' : 'Festival'}</span>
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
                    {new Date(selectedDay.date).toLocaleDateString(language === 'hi' ? 'hi-IN' : 'en-US', { 
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

                  {selectedDay.festival && (
                    <div className="p-3 rounded-lg bg-purple-500/10 border border-purple-500/30 mt-4">
                      <span className="text-xs text-purple-400">{language === 'hi' ? 'त्योहार' : 'Festival'}</span>
                      <p className="font-medium text-cosmic-text-primary">
                        {language === 'hi' ? selectedDay.festival_hindi || selectedDay.festival : selectedDay.festival}
                      </p>
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
