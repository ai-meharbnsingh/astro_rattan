import { useState, useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Card, CardContent } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Sun, Loader2 } from 'lucide-react';
import { api } from '@/lib/api';

gsap.registerPlugin(ScrollTrigger);

const zodiacSigns = [
  { name: 'Aries', symbol: '\u2648', date: 'Mar 21 - Apr 19', element: 'Fire' },
  { name: 'Taurus', symbol: '\u2649', date: 'Apr 20 - May 20', element: 'Earth' },
  { name: 'Gemini', symbol: '\u264A', date: 'May 21 - Jun 20', element: 'Air' },
  { name: 'Cancer', symbol: '\u264B', date: 'Jun 21 - Jul 22', element: 'Water' },
  { name: 'Leo', symbol: '\u264C', date: 'Jul 23 - Aug 22', element: 'Fire' },
  { name: 'Virgo', symbol: '\u264D', date: 'Aug 23 - Sep 22', element: 'Earth' },
  { name: 'Libra', symbol: '\u264E', date: 'Sep 23 - Oct 22', element: 'Air' },
  { name: 'Scorpio', symbol: '\u264F', date: 'Oct 23 - Nov 21', element: 'Water' },
  { name: 'Sagittarius', symbol: '\u2650', date: 'Nov 22 - Dec 21', element: 'Fire' },
  { name: 'Capricorn', symbol: '\u2651', date: 'Dec 22 - Jan 19', element: 'Earth' },
  { name: 'Aquarius', symbol: '\u2652', date: 'Jan 20 - Feb 18', element: 'Air' },
  { name: 'Pisces', symbol: '\u2653', date: 'Feb 19 - Mar 20', element: 'Water' },
];

const fallbackData: Record<string, string> = {
  general: 'Today brings positive energy. The planets align in your favor, creating opportunities for growth.',
  love: 'Romantic energies are high. If single, you might meet someone special.',
  career: 'Professional opportunities on the horizon. Your hard work is being noticed.',
  finance: 'Financial stability indicated. Good day for long-term investments.',
  health: 'Energy levels rising. Focus on balanced diet and regular exercise.',
};

export default function DailyHoroscope() {
  const sectionRef = useRef<HTMLDivElement>(null);
  const [selectedSign, setSelectedSign] = useState(zodiacSigns[0]);
  const [horoscopeData, setHoroscopeData] = useState<Record<string, string>>(fallbackData);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.fromTo('.horoscope-title', { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 0.8, ease: 'power3.out', scrollTrigger: { trigger: sectionRef.current, start: 'top 80%' } });
    }, sectionRef);
    return () => ctx.revert();
  }, []);

  useEffect(() => {
    let cancelled = false;
    const fetchHoroscope = async () => {
      setLoading(true);
      try {
        const data = await api.get(`/api/horoscope/${selectedSign.name.toLowerCase()}?period=daily`);
        if (!cancelled) {
          setHoroscopeData({
            general: data.content || data.general || fallbackData.general,
            love: data.love || fallbackData.love,
            career: data.career || fallbackData.career,
            finance: data.finance || fallbackData.finance,
            health: data.health || fallbackData.health,
          });
        }
      } catch {
        if (!cancelled) setHoroscopeData(fallbackData);
      } finally {
        if (!cancelled) setLoading(false);
      }
    };
    fetchHoroscope();
    return () => { cancelled = true; };
  }, [selectedSign]);

  return (
    <section ref={sectionRef} id="horoscope" className="relative py-24 bg-cosmic-bg bg-mandala bg-cosmic-stars">
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="horoscope-title text-center mb-12">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-sacred-saffron/10 text-sacred-saffron text-sm font-medium mb-6 border border-sacred-saffron/30">
            <Sun className="w-4 h-4" />Daily Guidance
          </div>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-sacred font-bold text-cosmic-text mb-4">
            Your Daily<span className="text-gradient-saffron"> Horoscope</span>
          </h2>
        </div>
        <div className="grid grid-cols-4 sm:grid-cols-6 lg:grid-cols-12 gap-3 mb-12">
          {zodiacSigns.map((sign, index) => (
            <button key={index} onClick={() => setSelectedSign(sign)} className={`relative p-3 rounded-xl transition-all duration-300 overflow-hidden ${selectedSign.name === sign.name ? 'ring-2 ring-sacred-gold shadow-glow-gold' : 'border border-sacred-gold/20 hover:border-sacred-gold/40'}`}>
              <div className="absolute inset-0 z-0">
                <img
                  src={`/images/zodiac-${sign.name.toLowerCase()}.jpg`}
                  alt={sign.name}
                  className="w-full h-full object-cover opacity-40"
                />
                <div className={`absolute inset-0 ${selectedSign.name === sign.name ? 'bg-sacred-gold/40' : 'bg-[#0a0a0a]/60'}`} />
              </div>
              <span className="relative z-10 text-2xl block mb-1">{sign.symbol}</span>
              <span className="relative z-10 text-xs text-cosmic-text">{sign.name}</span>
            </button>
          ))}
        </div>
        <div className="grid lg:grid-cols-3 gap-8">
          <Card className="lg:col-span-1 card-sacred border-sacred-gold/20">
            <CardContent className="p-6 text-center">
              <div className="relative w-24 h-24 rounded-full overflow-hidden mx-auto mb-4 shadow-glow-gold border-2 border-sacred-gold/40">
                <img
                  src={`/images/zodiac-${selectedSign.name.toLowerCase()}.jpg`}
                  alt={selectedSign.name}
                  className="w-full h-full object-cover"
                  onError={(e) => {
                    (e.currentTarget as HTMLImageElement).style.display = 'none';
                    (e.currentTarget.nextElementSibling as HTMLElement | null)?.classList.remove('hidden');
                  }}
                />
                <div className="hidden absolute inset-0 bg-gradient-to-br from-sacred-gold to-sacred-saffron flex items-center justify-center">
                  <span className="text-5xl text-cosmic-bg">{selectedSign.symbol}</span>
                </div>
              </div>
              <h3 className="text-2xl font-sacred font-bold text-cosmic-text mb-1">{selectedSign.name}</h3>
              <p className="text-sm text-cosmic-text-secondary mb-4">{selectedSign.date}</p>
              <span className="px-3 py-1 rounded-full bg-sacred-saffron/10 text-sacred-saffron text-sm border border-sacred-saffron/30">{selectedSign.element}</span>
            </CardContent>
          </Card>
          <Card className="lg:col-span-2 card-sacred border-sacred-gold/20">
            <CardContent className="p-6">
              {loading ? (
                <div className="flex items-center justify-center py-12">
                  <Loader2 className="w-8 h-8 text-sacred-gold animate-spin" />
                </div>
              ) : (
                <Tabs defaultValue="general">
                  <TabsList className="grid grid-cols-5 bg-cosmic-card mb-6 border border-sacred-gold/10">
                    {['general', 'love', 'career', 'finance', 'health'].map((tab) => (
                      <TabsTrigger key={tab} value={tab} className="data-[state=active]:bg-sacred-gold data-[state=active]:text-cosmic-bg capitalize text-cosmic-text-secondary">{tab}</TabsTrigger>
                    ))}
                  </TabsList>
                  {Object.entries(horoscopeData).map(([key, content]) => (
                    <TabsContent key={key} value={key} className="mt-0">
                      <p className="text-cosmic-text-secondary leading-relaxed">{content}</p>
                    </TabsContent>
                  ))}
                </Tabs>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  );
}
