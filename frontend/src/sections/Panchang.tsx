import { useState, useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Card, CardContent } from '@/components/ui/card';
import { Calendar, Clock, Sunrise, Sunset, Star, Loader2 } from 'lucide-react';
import { api } from '@/lib/api';

gsap.registerPlugin(ScrollTrigger);

interface PanchangInfo { tithi: string; nakshatra: string; yoga: string; karana: string; sunrise: string; sunset: string; }
interface ChoghadiyaPeriod { name: string; quality: string; start: string; end: string; }

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
    <section ref={sectionRef} id="panchang" className="relative py-24 bg-cosmic-bg bg-mandala">
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
      </div>
    </section>
  );
}
