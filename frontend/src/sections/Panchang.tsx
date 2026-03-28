import { useState, useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Calendar, Clock, Sunrise, Sunset, Star, Loader2, Search, MapPin, CalendarDays } from 'lucide-react';
import { api } from '@/lib/api';

gsap.registerPlugin(ScrollTrigger);

interface PanchangInfo { tithi: string; nakshatra: string; yoga: string; karana: string; sunrise: string; sunset: string; }
interface ChoghadiyaPeriod { name: string; quality: string; start: string; end: string; }

interface MuhuratType { id: string; name: string; description?: string; }
interface MuhuratWindow { start_time: string; end_time: string; quality: string; factors?: string[]; }
interface MonthlyMuhuratDay { date: string; has_muhurat: boolean; quality?: string; windows_count?: number; }

const fallbackPanchang: PanchangInfo = { tithi: 'Shukla Paksha - Pratipada', nakshatra: 'Ashwini', yoga: 'Vriddhi', karana: 'Bava', sunrise: '06:45 AM', sunset: '05:52 PM' };
const fallbackChoghadiya: ChoghadiyaPeriod[] = [
  { name: 'Amrit', start: '06:00', end: '07:30', quality: 'good' },
  { name: 'Kaal', start: '07:30', end: '09:00', quality: 'bad' },
  { name: 'Shubh', start: '09:00', end: '10:30', quality: 'good' },
  { name: 'Rog', start: '10:30', end: '12:00', quality: 'bad' },
];

export default function Panchang() {
  const sectionRef = useRef<HTMLDivElement>(null);
  const [currentTime] = useState(new Date());
  const [panchang, setPanchang] = useState<PanchangInfo>(fallbackPanchang);
  const [choghadiya, setChoghadiya] = useState<ChoghadiyaPeriod[]>(fallbackChoghadiya);
  const [loading, setLoading] = useState(true);
  const todayStr = new Date().toISOString().split('T')[0];
  const dateDisplay = new Date().toLocaleDateString('en-IN', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });

  // Muhurat Finder state
  const [muhuratTypes, setMuhuratTypes] = useState<MuhuratType[]>([]);
  const [selectedEventType, setSelectedEventType] = useState('');
  const [muhuratDate, setMuhuratDate] = useState(todayStr);
  const [latitude, setLatitude] = useState('28.6139');
  const [longitude, setLongitude] = useState('77.2090');
  const [muhuratWindows, setMuhuratWindows] = useState<MuhuratWindow[]>([]);
  const [muhuratLoading, setMuhuratLoading] = useState(false);
  const [monthlyView, setMonthlyView] = useState<MonthlyMuhuratDay[]>([]);
  const [monthlyLoading, setMonthlyLoading] = useState(false);
  const [showMonthly, setShowMonthly] = useState(false);

  // Fetch muhurat types on mount
  useEffect(() => {
    let cancelled = false;
    api.get('/api/muhurat/types').then((data) => {
      if (cancelled) return;
      const types = Array.isArray(data) ? data : data.types || data.items || [];
      setMuhuratTypes(types);
      if (types.length > 0 && !selectedEventType) setSelectedEventType(types[0].id);
    }).catch(() => {});
    return () => { cancelled = true; };
  }, []);

  const findMuhurat = async () => {
    if (!selectedEventType) return;
    setMuhuratLoading(true);
    setShowMonthly(false);
    try {
      const data = await api.get(`/api/muhurat/find?event_type=${selectedEventType}&date=${muhuratDate}&latitude=${latitude}&longitude=${longitude}`);
      const windows = Array.isArray(data) ? data : data.windows || data.muhurats || [];
      setMuhuratWindows(windows);
    } catch {
      setMuhuratWindows([]);
    } finally {
      setMuhuratLoading(false);
    }
  };

  const fetchMonthlyView = async () => {
    if (!selectedEventType) return;
    setMonthlyLoading(true);
    setShowMonthly(true);
    try {
      const [year, month] = muhuratDate.split('-');
      const data = await api.get(`/api/muhurat/monthly?event_type=${selectedEventType}&year=${year}&month=${month}&latitude=${latitude}&longitude=${longitude}`);
      const days = Array.isArray(data) ? data : data.days || data.dates || [];
      setMonthlyView(days);
    } catch {
      setMonthlyView([]);
    } finally {
      setMonthlyLoading(false);
    }
  };

  const qualityIcon = (quality: string) => {
    switch (quality?.toLowerCase()) {
      case 'excellent': return <Star className="w-5 h-5 text-yellow-400 fill-yellow-400" />;
      case 'good': return <Star className="w-5 h-5 text-[#8B7355] fill-gray-300" />;
      case 'average': return <Star className="w-5 h-5 text-amber-700 fill-amber-700" />;
      default: return <Star className="w-5 h-5 text-cosmic-text-secondary" />;
    }
  };

  const qualityLabel = (quality: string) => {
    switch (quality?.toLowerCase()) {
      case 'excellent': return 'text-yellow-400';
      case 'good': return 'text-[#8B7355]';
      case 'average': return 'text-amber-700';
      default: return 'text-cosmic-text-secondary';
    }
  };

  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.fromTo('.panchang-title', { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 0.8, ease: 'power3.out', scrollTrigger: { trigger: sectionRef.current, start: 'top 80%' } });
    }, sectionRef);
    return () => ctx.revert();
  }, []);

  useEffect(() => {
    let cancelled = false;
    const fetchPanchang = async () => {
      setLoading(true);
      try {
        const [panchangRes, choghadiyaRes] = await Promise.all([
          api.get(`/api/panchang?date=${todayStr}&latitude=28.6139&longitude=77.2090`).catch(() => null),
          api.get(`/api/panchang/choghadiya?date=${todayStr}&latitude=28.6139&longitude=77.2090`).catch(() => null),
        ]);
        if (!cancelled && panchangRes) {
          setPanchang({
            tithi: panchangRes.tithi?.name || panchangRes.tithi || fallbackPanchang.tithi,
            nakshatra: panchangRes.nakshatra?.name || panchangRes.nakshatra || fallbackPanchang.nakshatra,
            yoga: panchangRes.yoga?.name || panchangRes.yoga || fallbackPanchang.yoga,
            karana: panchangRes.karana?.name || panchangRes.karana || fallbackPanchang.karana,
            sunrise: panchangRes.sunrise || fallbackPanchang.sunrise,
            sunset: panchangRes.sunset || fallbackPanchang.sunset,
          });
        }
        if (!cancelled && choghadiyaRes) {
          setChoghadiya(Array.isArray(choghadiyaRes.periods) && choghadiyaRes.periods.length > 0 ? choghadiyaRes.periods : fallbackChoghadiya);
        }
      } catch { /* fallback already set */ } finally { if (!cancelled) setLoading(false); }
    };
    fetchPanchang();
    return () => { cancelled = true; };
  }, [todayStr]);

  return (
    <section ref={sectionRef} id="panchang" className="relative py-24 bg-transparent">
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="panchang-title text-center mb-12">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-sacred-saffron/10 text-sacred-saffron text-sm font-medium mb-6 border border-sacred-saffron/30">
            <Calendar className="w-4 h-4" />Daily Panchang
          </div>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-sacred font-bold text-cosmic-text mb-4">
            Cosmic Timekeeping with<span className="text-gradient-saffron"> Panchang</span>
          </h2>
        </div>
        <div className="card-gold-border rounded-2xl p-4 mb-8 flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-xl bg-sacred-gold/10 flex items-center justify-center border border-sacred-gold/20">
              <Calendar className="w-6 h-6 text-sacred-gold" />
            </div>
            <div>
              <p className="text-sm text-cosmic-text-secondary">Today</p>
              <p className="text-lg font-sacred font-semibold text-cosmic-text">{dateDisplay}</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-xl bg-sacred-saffron/10 flex items-center justify-center border border-sacred-saffron/20">
              <Clock className="w-6 h-6 text-sacred-saffron" />
            </div>
            <div>
              <p className="text-sm text-cosmic-text-secondary">Current Time</p>
              <p className="text-lg font-sacred font-semibold text-cosmic-text">{currentTime.toLocaleTimeString('en-IN')}</p>
            </div>
          </div>
        </div>
        {loading ? (
          <div className="flex items-center justify-center py-20"><Loader2 className="w-10 h-10 text-sacred-gold animate-spin" /></div>
        ) : (
          <div className="grid lg:grid-cols-3 gap-6">
            <Card className="card-sacred border-sacred-gold/20">
              <CardContent className="p-6">
                <h3 className="text-xl font-sacred font-semibold text-cosmic-text mb-6 flex items-center gap-2">
                  <Star className="w-5 h-5 text-sacred-gold" />Today&apos;s Panchang
                </h3>
                <div className="space-y-4">
                  {(['tithi', 'nakshatra', 'yoga', 'karana'] as const).map((key) => (
                    <div key={key} className="p-4 rounded-xl bg-cosmic-card border border-sacred-gold/10">
                      <p className="text-sm text-cosmic-text-secondary capitalize">{key}</p>
                      <p className="text-cosmic-text font-medium">{panchang[key]}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
            <Card className="card-sacred border-sacred-gold/20">
              <CardContent className="p-6">
                <h3 className="text-xl font-sacred font-semibold text-cosmic-text mb-6">Choghadiya</h3>
                <div className="space-y-2">
                  {choghadiya.map((item, index) => (
                    <div key={index} className={`flex items-center justify-between p-3 rounded-xl border ${item.quality === 'good' ? 'bg-green-900/20 border-green-500/30' : 'bg-red-900/20 border-red-500/30'}`}>
                      <div>
                        <p className={`text-sm font-medium ${item.quality === 'good' ? 'text-green-400' : 'text-red-400'}`}>{item.name}</p>
                        <p className="text-xs text-cosmic-text-secondary">{item.start} - {item.end}</p>
                      </div>
                      <span className={`text-xs px-2 py-1 rounded-full ${item.quality === 'good' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'}`}>{item.quality === 'good' ? 'Good' : 'Avoid'}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
            <Card className="card-sacred border-sacred-gold/20">
              <CardContent className="p-6">
                <h3 className="text-xl font-sacred font-semibold text-cosmic-text mb-6">Sun Times</h3>
                <div className="space-y-4">
                  <div className="flex items-center gap-4 p-4 rounded-xl bg-cosmic-card border border-sacred-gold/10">
                    <div className="w-10 h-10 rounded-xl bg-sacred-gold/10 flex items-center justify-center">
                      <Sunrise className="w-5 h-5 text-sacred-gold" />
                    </div>
                    <div>
                      <p className="text-sm text-cosmic-text-secondary">Sunrise</p>
                      <p className="text-cosmic-text font-medium">{panchang.sunrise}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-4 p-4 rounded-xl bg-cosmic-card border border-sacred-saffron/10">
                    <div className="w-10 h-10 rounded-xl bg-sacred-saffron/10 flex items-center justify-center">
                      <Sunset className="w-5 h-5 text-sacred-saffron" />
                    </div>
                    <div>
                      <p className="text-sm text-cosmic-text-secondary">Sunset</p>
                      <p className="text-cosmic-text font-medium">{panchang.sunset}</p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Muhurat Finder Section */}
        <div className="mt-16">
          <div className="text-center mb-10">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-sacred-gold/10 text-sacred-gold text-sm font-medium mb-6 border border-sacred-gold/30">
              <Search className="w-4 h-4" />Muhurat Finder
            </div>
            <h3 className="text-2xl sm:text-3xl font-sacred font-bold text-cosmic-text">
              Find <span className="text-gradient-gold">Auspicious Times</span>
            </h3>
          </div>

          <Card className="card-sacred bg-cosmic-card border-sacred-gold/20 mb-8">
            <CardContent className="p-6">
              <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
                {/* Event Type Dropdown */}
                <div>
                  <label className="block text-sm text-cosmic-text-secondary mb-2">Event Type</label>
                  <select
                    value={selectedEventType}
                    onChange={(e) => setSelectedEventType(e.target.value)}
                    className="w-full px-4 py-2.5 rounded-xl bg-cosmic-card border border-sacred-gold/20 text-cosmic-text focus:border-sacred-gold/50 focus:outline-none appearance-none cursor-pointer"
                  >
                    {muhuratTypes.length === 0 && <option value="">Loading...</option>}
                    {muhuratTypes.map((type) => (
                      <option key={type.id} value={type.id}>{type.name}</option>
                    ))}
                  </select>
                </div>

                {/* Date Picker */}
                <div>
                  <label className="block text-sm text-cosmic-text-secondary mb-2">Date</label>
                  <input
                    type="date"
                    value={muhuratDate}
                    onChange={(e) => setMuhuratDate(e.target.value)}
                    className="w-full px-4 py-2.5 rounded-xl bg-cosmic-card border border-sacred-gold/20 text-cosmic-text focus:border-sacred-gold/50 focus:outline-none"
                  />
                </div>

                {/* Latitude */}
                <div>
                  <label className="block text-sm text-cosmic-text-secondary mb-2 flex items-center gap-1">
                    <MapPin className="w-3 h-3" />Latitude
                  </label>
                  <input
                    type="number"
                    step="0.0001"
                    value={latitude}
                    onChange={(e) => setLatitude(e.target.value)}
                    placeholder="28.6139"
                    className="w-full px-4 py-2.5 rounded-xl bg-cosmic-card border border-sacred-gold/20 text-cosmic-text focus:border-sacred-gold/50 focus:outline-none"
                  />
                </div>

                {/* Longitude */}
                <div>
                  <label className="block text-sm text-cosmic-text-secondary mb-2 flex items-center gap-1">
                    <MapPin className="w-3 h-3" />Longitude
                  </label>
                  <input
                    type="number"
                    step="0.0001"
                    value={longitude}
                    onChange={(e) => setLongitude(e.target.value)}
                    placeholder="77.2090"
                    className="w-full px-4 py-2.5 rounded-xl bg-cosmic-card border border-sacred-gold/20 text-cosmic-text focus:border-sacred-gold/50 focus:outline-none"
                  />
                </div>
              </div>

              <div className="flex flex-wrap gap-3">
                <Button
                  onClick={findMuhurat}
                  disabled={muhuratLoading || !selectedEventType}
                  className="btn-sacred bg-sacred-gold/10 text-sacred-gold hover:bg-sacred-gold hover:text-cosmic-bg border border-sacred-gold/30 transition-all font-medium px-6"
                >
                  {muhuratLoading ? <Loader2 className="w-4 h-4 animate-spin mr-2" /> : <Search className="w-4 h-4 mr-2" />}
                  Find Muhurat
                </Button>
                <Button
                  onClick={fetchMonthlyView}
                  disabled={monthlyLoading || !selectedEventType}
                  className="btn-sacred bg-cosmic-card text-cosmic-text-secondary hover:bg-sacred-gold/10 hover:text-sacred-gold border border-sacred-gold/20 transition-all font-medium px-6"
                >
                  {monthlyLoading ? <Loader2 className="w-4 h-4 animate-spin mr-2" /> : <CalendarDays className="w-4 h-4 mr-2" />}
                  Monthly View
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Muhurat Results */}
          {!showMonthly && muhuratWindows.length > 0 && (
            <div className="space-y-4">
              <h4 className="text-lg font-sacred font-semibold text-cosmic-text mb-4">Auspicious Windows</h4>
              {muhuratWindows.map((window, idx) => (
                <Card key={idx} className="card-sacred bg-cosmic-card border-sacred-gold/20 hover:border-sacred-gold/40 transition-all">
                  <CardContent className="p-5">
                    <div className="flex items-start gap-4">
                      <div className="flex-shrink-0 mt-1">
                        {qualityIcon(window.quality)}
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <span className="text-cosmic-text font-medium">
                            {window.start_time} - {window.end_time}
                          </span>
                          <span className={`text-xs font-bold uppercase tracking-wide px-2 py-0.5 rounded-full border ${
                            window.quality?.toLowerCase() === 'excellent' ? 'bg-yellow-400/10 text-yellow-400 border-yellow-400/30' :
                            window.quality?.toLowerCase() === 'good' ? 'bg-gray-300/10 text-[#8B7355] border-gray-300/30' :
                            'bg-amber-700/10 text-amber-700 border-amber-700/30'
                          }`}>
                            {window.quality}
                          </span>
                        </div>
                        {window.factors && window.factors.length > 0 && (
                          <div className="flex flex-wrap gap-2 mt-2">
                            {window.factors.map((factor, fIdx) => (
                              <span key={fIdx} className="text-xs px-2 py-1 rounded-full bg-sacred-gold/10 text-sacred-gold border border-sacred-gold/20">
                                {factor}
                              </span>
                            ))}
                          </div>
                        )}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}

          {!showMonthly && !muhuratLoading && muhuratWindows.length === 0 && selectedEventType && (
            <div className="text-center py-10">
              <Search className="w-12 h-12 text-sacred-gold/30 mx-auto mb-3" />
              <p className="text-cosmic-text-secondary">Select an event type and click &quot;Find Muhurat&quot; to discover auspicious times.</p>
            </div>
          )}

          {/* Monthly Calendar View */}
          {showMonthly && (
            <div>
              <h4 className="text-lg font-sacred font-semibold text-cosmic-text mb-4">Monthly Muhurat Calendar</h4>
              {monthlyLoading ? (
                <div className="flex items-center justify-center py-12"><Loader2 className="w-8 h-8 text-sacred-gold animate-spin" /></div>
              ) : monthlyView.length === 0 ? (
                <div className="text-center py-10">
                  <CalendarDays className="w-12 h-12 text-sacred-gold/30 mx-auto mb-3" />
                  <p className="text-cosmic-text-secondary">No muhurat data available for this month.</p>
                </div>
              ) : (
                <div className="grid grid-cols-7 gap-2">
                  {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map((day) => (
                    <div key={day} className="text-center text-xs text-cosmic-text-secondary font-medium py-2">{day}</div>
                  ))}
                  {/* Offset for first day of month */}
                  {monthlyView.length > 0 && Array.from({ length: new Date(monthlyView[0].date).getDay() }).map((_, i) => (
                    <div key={`empty-${i}`} />
                  ))}
                  {monthlyView.map((day) => {
                    const dayNum = new Date(day.date).getDate();
                    const bgColor = !day.has_muhurat ? 'bg-cosmic-card border-sacred-gold/10' :
                      day.quality?.toLowerCase() === 'excellent' ? 'bg-yellow-400/15 border-yellow-400/40' :
                      day.quality?.toLowerCase() === 'good' ? 'bg-gray-300/10 border-gray-300/30' :
                      'bg-amber-700/10 border-amber-700/30';
                    const textColor = !day.has_muhurat ? 'text-cosmic-text-secondary' :
                      day.quality?.toLowerCase() === 'excellent' ? 'text-yellow-400' :
                      day.quality?.toLowerCase() === 'good' ? 'text-[#8B7355]' :
                      'text-amber-700';
                    return (
                      <div key={day.date} className={`p-2 rounded-xl border text-center ${bgColor} transition-all hover:scale-105`}>
                        <p className={`text-sm font-medium ${textColor}`}>{dayNum}</p>
                        {day.has_muhurat && day.windows_count && (
                          <p className="text-[10px] text-cosmic-text-secondary mt-0.5">{day.windows_count} slot{day.windows_count > 1 ? 's' : ''}</p>
                        )}
                        {day.has_muhurat && (
                          <div className="flex justify-center mt-1">
                            {qualityIcon(day.quality || '')}
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
