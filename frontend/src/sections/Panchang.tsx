import { useState, useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Calendar, Clock, Loader2, MapPin, Navigation } from 'lucide-react';
import { api } from '@/lib/api';

import {
  PanchangCore,
  SunMoonTimes,
  InauspiciousPeriods,
  AuspiciousTimings,
  PlanetaryPositions,
  FestivalVrat,
  HinduCalendar,
  MuhuratFinder,
} from '@/components/panchang';

gsap.registerPlugin(ScrollTrigger);

// ============================================================
// Types matching the enhanced API response
// ============================================================
interface TimePeriod { start: string; end: string; }
interface ChoghadiyaPeriod { name: string; quality: string; start: string; end: string; }
interface Planet { name: string; longitude: number; degree: number; rashi: string; rashi_index: number; }
interface Festival { name: string; name_hindi?: string; type: string; description: string; rituals?: string; }
interface HinduCalendarData {
  vikram_samvat: number; shaka_samvat: number; maas: string;
  paksha: string; ritu: string; ritu_english: string; ayana: string;
}
interface VaarData { name: string; english: string; number: number; }

interface FullPanchangData {
  date: string;
  tithi: { name: string; number: number; paksha: string; end_time?: string };
  nakshatra: { name: string; pada: number; lord: string; end_time?: string };
  yoga: { name: string; number: number; end_time?: string };
  karana: { name: string; number: number; end_time?: string };
  sunrise: string;
  sunset: string;
  moonrise: string;
  moonset: string;
  vaar: VaarData;
  rahu_kaal: TimePeriod;
  gulika_kaal: TimePeriod;
  yamaganda: TimePeriod;
  abhijit_muhurat: TimePeriod;
  brahma_muhurat: TimePeriod;
  choghadiya: ChoghadiyaPeriod[];
  planetary_positions: Planet[];
  hindu_calendar: HinduCalendarData;
  festivals: Festival[];
  // Extended fields (may be absent on older cached responses)
  sun_sign?: string;
  moon_sign?: string;
  dinamana?: string;
  ratrimana?: string;
  madhyahna?: string;
  ravi_yoga?: TimePeriod | null;
  vijaya_muhurta?: TimePeriod | null;
  godhuli_muhurta?: TimePeriod | null;
  sayahna_sandhya?: TimePeriod | null;
  nishita_muhurta?: TimePeriod | null;
  pratah_sandhya?: TimePeriod | null;
  dur_muhurtam?: TimePeriod | null;
  varjyam?: TimePeriod | null;
  hora_table?: any[] | null;
  lagna_table?: any[] | null;
  chandrabalam?: any[] | null;
  tarabalam?: any[] | null;
  gowri_panchang?: any[] | null;
  do_ghati_muhurta?: any[] | null;
  panchaka?: { active: boolean; rahita: boolean } | null;
}

const DEFAULT_LAT = '28.6139';
const DEFAULT_LON = '77.2090';

export default function Panchang() {
  const sectionRef = useRef<HTMLDivElement>(null);
  const [loading, setLoading] = useState(true);
  const [panchang, setPanchang] = useState<FullPanchangData | null>(null);
  const [selectedDate, setSelectedDate] = useState(() => new Date().toISOString().split('T')[0]);
  const [latitude, setLatitude] = useState(DEFAULT_LAT);
  const [longitude, setLongitude] = useState(DEFAULT_LON);
  const [detectingLocation, setDetectingLocation] = useState(false);
  const [currentTime, setCurrentTime] = useState(new Date());

  // Live clock
  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  // GSAP animation with proper ScrollTrigger cleanup
  useEffect(() => {
    if (gsap.globalTimeline.timeScale() === 0) return; // reduced motion
    const ctx = gsap.context(() => {
      gsap.fromTo('.panchang-title', { y: 50, opacity: 0 }, {
        y: 0, opacity: 1, duration: 0.8, ease: 'power3.out',
        scrollTrigger: { trigger: sectionRef.current, start: 'top 80%' },
      });
    }, sectionRef);
    return () => {
      ctx.revert();
      ScrollTrigger.getAll().forEach(t => t.kill());
    };
  }, []);

  // Fetch panchang data
  useEffect(() => {
    let cancelled = false;
    const fetchPanchang = async () => {
      setLoading(true);
      try {
        const data = await api.get(
          `/api/panchang?date=${selectedDate}&latitude=${latitude}&longitude=${longitude}`
        );
        if (!cancelled && data) {
          setPanchang(normalizePanchang(data));
        }
      } catch {
        // Keep previous data on error
      } finally {
        if (!cancelled) setLoading(false);
      }
    };
    fetchPanchang();
    return () => { cancelled = true; };
  }, [selectedDate, latitude, longitude]);

  // Auto-detect location
  const detectLocation = () => {
    if (!navigator.geolocation) return;
    setDetectingLocation(true);
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setLatitude(pos.coords.latitude.toFixed(4));
        setLongitude(pos.coords.longitude.toFixed(4));
        setDetectingLocation(false);
      },
      () => setDetectingLocation(false),
      { timeout: 10000 },
    );
  };

  const dateDisplay = new Date(selectedDate + 'T12:00:00').toLocaleDateString('en-IN', {
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric',
  });

  return (
    <section ref={sectionRef} id="panchang" className="relative py-24 bg-transparent">
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

        {/* Title */}
        <div className="panchang-title text-center mb-12">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-sacred-saffron text-sacred-saffron text-sm font-medium mb-6 border border-sacred-saffron">
            <Calendar className="w-4 h-4" />Daily Panchang
          </div>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-sans font-bold text-cosmic-text mb-4">
            Cosmic Timekeeping with<span className="text-gradient-saffron"> Panchang</span>
          </h2>
        </div>

        {/* Date/Time Bar + Location Controls */}
        <div className="card-gold-border rounded-xl p-4 mb-8">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-xl bg-sacred-gold flex items-center justify-center border border-sacred-gold">
                <Calendar className="w-6 h-6 text-sacred-gold" />
              </div>
              <div>
                <p className="text-sm text-cosmic-text-secondary">Date</p>
                <p className="text-lg font-sans font-semibold text-cosmic-text">{dateDisplay}</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-xl bg-sacred-saffron flex items-center justify-center border border-sacred-saffron">
                <Clock className="w-6 h-6 text-sacred-saffron" />
              </div>
              <div>
                <p className="text-sm text-cosmic-text-secondary">Current Time</p>
                <p className="text-lg font-sans font-semibold text-cosmic-text">{currentTime.toLocaleTimeString('en-IN')}</p>
              </div>
            </div>
          </div>

          {/* Location & Date grouped inputs */}
          <div className="mt-4 rounded-xl border border-cosmic-border bg-cosmic-card p-4">
            <div className="flex items-center justify-between mb-3">
              <h4 className="text-sm font-semibold text-cosmic-text flex items-center gap-1.5">
                <MapPin className="w-4 h-4 text-sacred-gold" />Location &amp; Date
              </h4>
              <Button
                onClick={detectLocation}
                disabled={detectingLocation}
                className="btn-sacred bg-sacred-gold text-sacred-gold hover:bg-sacred-gold hover:text-cosmic-bg border border-sacred-gold transition-all text-sm px-4 py-2"
              >
                {detectingLocation ? <Loader2 className="w-4 h-4 animate-spin mr-1" /> : <Navigation className="w-4 h-4 mr-1" />}
                Detect Location
              </Button>
            </div>
            <div className="space-y-3">
              {/* Date — full width */}
              <div>
                <label className="block text-sm font-medium text-cosmic-text-secondary mb-1">Date</label>
                <input
                  type="date"
                  value={selectedDate}
                  onChange={(e) => setSelectedDate(e.target.value)}
                  className="w-full px-3 py-2 rounded-xl bg-white border border-cosmic-border text-cosmic-text text-sm focus:border-sacred-gold focus:outline-none transition-colors"
                />
              </div>
              {/* Lat / Lon — side by side */}
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-sm font-medium text-cosmic-text-secondary mb-1 flex items-center gap-1">
                    <MapPin className="w-3 h-3" />Latitude
                  </label>
                  <input
                    type="number" step="0.0001" value={latitude}
                    onChange={(e) => setLatitude(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl bg-white border border-cosmic-border text-cosmic-text text-sm focus:border-sacred-gold focus:outline-none transition-colors"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-cosmic-text-secondary mb-1 flex items-center gap-1">
                    <MapPin className="w-3 h-3" />Longitude
                  </label>
                  <input
                    type="number" step="0.0001" value={longitude}
                    onChange={(e) => setLongitude(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl bg-white border border-cosmic-border text-cosmic-text text-sm focus:border-sacred-gold focus:outline-none transition-colors"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Loading skeleton */}
        {loading && !panchang && (
          <div className="min-h-[400px] space-y-6">
            <div className="grid lg:grid-cols-3 gap-6">
              <div className="h-48 animate-pulse bg-gray-200 rounded-xl" />
              <div className="lg:col-span-2 h-48 animate-pulse bg-gray-200 rounded-xl" />
            </div>
            <div className="grid lg:grid-cols-3 gap-6">
              <div className="h-36 animate-pulse bg-gray-200 rounded-xl" />
              <div className="h-36 animate-pulse bg-gray-200 rounded-xl" />
              <div className="h-36 animate-pulse bg-gray-200 rounded-xl" />
            </div>
          </div>
        )}

        {/* Main Panchang Dashboard */}
        {panchang && (
          <div className="space-y-8 min-h-[400px]">

            {/* ROW 1: Hindu Calendar + Core Panchang */}
            <div className="grid lg:grid-cols-3 gap-6">
              <div className="lg:col-span-1 space-y-6">
                <HinduCalendar
                  hindu_calendar={panchang.hindu_calendar}
                  vaar={panchang.vaar}
                />
                <FestivalVrat festivals={panchang.festivals} />
              </div>
              <div className="lg:col-span-2">
                <Card className="card-sacred border-sacred-gold h-full">
                  <CardContent className="p-6">
                    <h3 className="text-xl font-sans font-semibold text-cosmic-text mb-6 flex items-center gap-2">
                      <Calendar className="w-5 h-5 text-sacred-gold" />Today&apos;s Panchang
                    </h3>
                    <PanchangCore
                      tithi={panchang.tithi}
                      nakshatra={panchang.nakshatra}
                      yoga={panchang.yoga}
                      karana={panchang.karana}
                    />
                  </CardContent>
                </Card>
              </div>
            </div>

            {/* ROW 2: Sun/Moon + Inauspicious + Auspicious */}
            <div className="grid lg:grid-cols-3 gap-6">
              <div className="space-y-4">
                <SunMoonTimes
                  sunrise={panchang.sunrise}
                  sunset={panchang.sunset}
                  moonrise={panchang.moonrise}
                  moonset={panchang.moonset}
                />
                {/* Sun/Moon Sign + Day/Night Duration */}
                <Card className="card-sacred border-sacred-gold">
                  <CardContent className="p-4 space-y-2 text-sm">
                    {panchang.sun_sign && <div className="flex justify-between"><span className="text-cosmic-text">Sun Sign</span><span className="font-medium text-cosmic-text">{panchang.sun_sign}</span></div>}
                    {panchang.moon_sign && <div className="flex justify-between"><span className="text-cosmic-text">Moon Sign</span><span className="font-medium text-cosmic-text">{panchang.moon_sign}</span></div>}
                    {panchang.dinamana && <div className="flex justify-between"><span className="text-cosmic-text">Dinamana</span><span className="font-medium text-cosmic-text">{panchang.dinamana}</span></div>}
                    {panchang.ratrimana && <div className="flex justify-between"><span className="text-cosmic-text">Ratrimana</span><span className="font-medium text-cosmic-text">{panchang.ratrimana}</span></div>}
                    {panchang.madhyahna && <div className="flex justify-between"><span className="text-cosmic-text">Madhyahna</span><span className="font-medium text-cosmic-text">{panchang.madhyahna}</span></div>}
                  </CardContent>
                </Card>
              </div>
              <InauspiciousPeriods
                rahu_kaal={panchang.rahu_kaal}
                gulika_kaal={panchang.gulika_kaal}
                yamaganda={panchang.yamaganda}
                dur_muhurtam={panchang.dur_muhurtam}
                varjyam={panchang.varjyam}
              />
              <AuspiciousTimings
                abhijit_muhurat={panchang.abhijit_muhurat}
                brahma_muhurat={panchang.brahma_muhurat}
                choghadiya={panchang.choghadiya}
                ravi_yoga={panchang.ravi_yoga}
                vijaya_muhurta={panchang.vijaya_muhurta}
                godhuli_muhurta={panchang.godhuli_muhurta}
                sayahna_sandhya={panchang.sayahna_sandhya}
                nishita_muhurta={panchang.nishita_muhurta}
                pratah_sandhya={panchang.pratah_sandhya}
              />
            </div>

            {/* ROW 3: Planetary Positions */}
            <PlanetaryPositions planets={panchang.planetary_positions} />

            {/* ROW 4: Advanced Panchang — Expandable Sections */}
            <div className="space-y-4">
              {/* Hora Table */}
              {panchang.hora_table && <ExpandableSection title="Hora Muhurta" desc="24 planetary hours">
                <div className="overflow-x-auto"><table className="w-full text-sm"><thead><tr className="bg-sacred-gold"><th className="p-2 text-left text-sacred-gold-dark">Hora</th><th className="p-2 text-left">Lord</th><th className="p-2">Start</th><th className="p-2">End</th><th className="p-2">Type</th></tr></thead><tbody>
                {(panchang.hora_table as any[]).map((h: any, i: number) => (
                  <tr key={i} className="border-t border-sacred-gold"><td className="p-2 text-cosmic-text">{h.hora}</td><td className="p-2 text-cosmic-text font-medium">{h.lord}</td><td className="p-2 text-cosmic-text">{h.start}</td><td className="p-2 text-cosmic-text">{h.end}</td><td className="p-2"><span className={`text-sm px-2 py-0.5 rounded ${h.type === 'day' ? 'bg-amber-100 text-amber-700' : 'bg-blue-100 text-blue-700'}`}>{h.type}</span></td></tr>
                ))}</tbody></table></div>
              </ExpandableSection>}

              {/* Lagna Table */}
              {panchang.lagna_table && <ExpandableSection title="Lagna Muhurta" desc="Rising sign through the day">
                <div className="overflow-x-auto"><table className="w-full text-sm"><thead><tr className="bg-sacred-gold"><th className="p-2 text-left text-sacred-gold-dark">Lagna</th><th className="p-2">Start</th><th className="p-2">End</th></tr></thead><tbody>
                {(panchang.lagna_table as any[]).map((l: any, i: number) => (
                  <tr key={i} className="border-t border-sacred-gold"><td className="p-2 text-cosmic-text font-medium">{l.lagna}</td><td className="p-2 text-cosmic-text">{l.start}</td><td className="p-2 text-cosmic-text">{l.end}</td></tr>
                ))}</tbody></table></div>
              </ExpandableSection>}

              {/* Gowri Panchangam */}
              {panchang.gowri_panchang && <ExpandableSection title="Gowri Panchangam" desc="Day and night quality periods">
                <div className="overflow-x-auto"><table className="w-full text-sm"><thead><tr className="bg-sacred-gold"><th className="p-2 text-left text-sacred-gold-dark">Period</th><th className="p-2">Start</th><th className="p-2">End</th><th className="p-2">Type</th><th className="p-2">Quality</th></tr></thead><tbody>
                {(panchang.gowri_panchang as any[]).map((g: any, i: number) => (
                  <tr key={i} className={`border-t border-sacred-gold ${g.quality === 'good' ? 'bg-green-50' : ''}`}><td className="p-2 text-cosmic-text font-medium">{g.name}</td><td className="p-2 text-cosmic-text">{g.start}</td><td className="p-2 text-cosmic-text">{g.end}</td><td className="p-2"><span className={`text-sm px-2 py-0.5 rounded ${g.type === 'day' ? 'bg-amber-100 text-amber-700' : 'bg-blue-100 text-blue-700'}`}>{g.type}</span></td><td className="p-2"><span className={`text-sm px-2 py-0.5 rounded ${g.quality === 'good' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>{g.quality === 'good' ? 'Shubh' : 'Ashubh'}</span></td></tr>
                ))}</tbody></table></div>
              </ExpandableSection>}

              {/* Chandrabalam */}
              {panchang.chandrabalam && <ExpandableSection title="Chandrabalam" desc="Moon strength for all 12 Rashi">
                <div className="grid grid-cols-3 sm:grid-cols-4 gap-2">
                {(panchang.chandrabalam as any[]).map((c: any, i: number) => (
                  <div key={i} className={`p-3 text-center border rounded ${c.good ? 'border-green-300 bg-green-50' : 'border-red-200 bg-red-50'}`}>
                    <p className="text-sm font-medium text-cosmic-text">{c.rashi}</p>
                    <p className={`text-sm font-semibold ${c.good ? 'text-green-600' : 'text-red-500'}`}>{c.balam}</p>
                    <p className="text-sm text-cosmic-text">House {c.house_from_moon}</p>
                  </div>
                ))}
                </div>
              </ExpandableSection>}

              {/* Tarabalam */}
              {panchang.tarabalam && <ExpandableSection title="Tarabalam" desc="Star strength for all 27 Nakshatra">
                <div className="grid grid-cols-3 sm:grid-cols-4 lg:grid-cols-5 gap-2">
                {(panchang.tarabalam as any[]).map((t: any, i: number) => (
                  <div key={i} className={`p-2 text-center border rounded ${t.good ? 'border-green-300 bg-green-50' : 'border-red-200 bg-red-50'}`}>
                    <p className="text-sm font-medium text-cosmic-text">{t.nakshatra}</p>
                    <p className={`text-sm font-semibold ${t.good ? 'text-green-600' : 'text-red-500'}`}>{t.tara}</p>
                  </div>
                ))}
                </div>
              </ExpandableSection>}

              {/* Do Ghati Muhurta */}
              {panchang.do_ghati_muhurta && <ExpandableSection title="Do Ghati Muhurta" desc="30 Muhurta division of the day">
                <div className="overflow-x-auto"><table className="w-full text-sm"><thead><tr className="bg-sacred-gold"><th className="p-2 text-left text-sacred-gold-dark">#</th><th className="p-2 text-left">Name</th><th className="p-2">Start</th><th className="p-2">End</th><th className="p-2">Quality</th></tr></thead><tbody>
                {(panchang.do_ghati_muhurta as any[]).map((m: any, i: number) => (
                  <tr key={i} className={`border-t border-sacred-gold ${m.quality === 'good' ? 'bg-green-50' : ''}`}><td className="p-2 text-cosmic-text">{m.muhurta}</td><td className="p-2 text-cosmic-text font-medium">{m.name}</td><td className="p-2 text-cosmic-text">{m.start}</td><td className="p-2 text-cosmic-text">{m.end}</td><td className="p-2"><span className={`text-sm px-2 py-0.5 rounded ${m.quality === 'good' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'}`}>{m.quality}</span></td></tr>
                ))}</tbody></table></div>
              </ExpandableSection>}

              {/* Panchaka */}
              {panchang.panchaka && <div className={`p-4 rounded-xl border ${panchang.panchaka.active ? 'border-red-300 bg-red-50' : 'border-green-300 bg-green-50'}`}>
                <p className="text-sm font-medium text-cosmic-text">Panchaka Rahita: <span className={`font-semibold ${panchang.panchaka.rahita ? 'text-green-600' : 'text-red-500'}`}>{panchang.panchaka.rahita ? 'Safe — No Panchaka today' : 'Panchaka Active — Caution advised'}</span></p>
              </div>}
            </div>

            {/* ROW 5: Muhurat Finder */}
            <MuhuratFinder
              latitude={latitude}
              longitude={longitude}
              onLatChange={setLatitude}
              onLonChange={setLongitude}
            />
          </div>
        )}
      </div>
    </section>
  );
}

// ============================================================
// Normalize API response to match FullPanchangData
// ============================================================
function ExpandableSection({ title, desc, children }: { title: string; desc: string; children: React.ReactNode }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="border border-sacred-gold rounded-xl overflow-hidden bg-sacred-cream">
      <button onClick={() => setOpen(!open)} className="w-full flex items-center justify-between p-4 hover:bg-sacred-gold transition-colors">
        <div className="text-left">
          <h4 className="font-display font-semibold text-sacred-brown text-sm">{title}</h4>
          <p className="text-sm text-cosmic-text">{desc}</p>
        </div>
        <span className={`text-sacred-gold-dark transition-transform ${open ? 'rotate-180' : ''}`}>▼</span>
      </button>
      {open && <div className="p-4 pt-0 border-t border-sacred-gold">{children}</div>}
    </div>
  );
}

function normalizePanchang(data: Record<string, unknown>): FullPanchangData {
  const d = data as Record<string, any>;
  return {
    date: d.date || '',
    tithi: d.tithi || { name: 'Pratipada', number: 1, paksha: 'Shukla' },
    nakshatra: d.nakshatra || { name: 'Ashwini', pada: 1, lord: 'Ketu' },
    yoga: d.yoga || { name: 'Vishkambha', number: 1 },
    karana: d.karana || { name: 'Bava', number: 1 },
    sunrise: d.sunrise || '06:00',
    sunset: d.sunset || '18:00',
    moonrise: d.moonrise || '--:--',
    moonset: d.moonset || '--:--',
    vaar: d.vaar || { name: 'Somvar', english: 'Monday', number: 0 },
    rahu_kaal: d.rahu_kaal || { start: '--:--', end: '--:--' },
    gulika_kaal: d.gulika_kaal || { start: '--:--', end: '--:--' },
    yamaganda: d.yamaganda || { start: '--:--', end: '--:--' },
    abhijit_muhurat: d.abhijit_muhurat || { start: '--:--', end: '--:--' },
    brahma_muhurat: d.brahma_muhurat || { start: '--:--', end: '--:--' },
    choghadiya: Array.isArray(d.choghadiya) ? d.choghadiya : [],
    planetary_positions: Array.isArray(d.planetary_positions) ? d.planetary_positions : [],
    hindu_calendar: d.hindu_calendar || {
      vikram_samvat: 0, shaka_samvat: 0, maas: '', paksha: '',
      ritu: '', ritu_english: '', ayana: '',
    },
    festivals: Array.isArray(d.festivals) ? d.festivals : [],
    // New fields
    sun_sign: d.sun_sign || '',
    moon_sign: d.moon_sign || '',
    dinamana: d.dinamana || '',
    ratrimana: d.ratrimana || '',
    madhyahna: d.madhyahna || '',
    ravi_yoga: d.ravi_yoga || null,
    vijaya_muhurta: d.vijaya_muhurta || null,
    godhuli_muhurta: d.godhuli_muhurta || null,
    sayahna_sandhya: d.sayahna_sandhya || null,
    nishita_muhurta: d.nishita_muhurta || null,
    pratah_sandhya: d.pratah_sandhya || null,
    dur_muhurtam: d.dur_muhurtam || null,
    varjyam: d.varjyam || null,
    hora_table: d.hora_table || null,
    lagna_table: d.lagna_table || null,
    chandrabalam: d.chandrabalam || null,
    tarabalam: d.tarabalam || null,
    gowri_panchang: d.gowri_panchang || null,
    do_ghati_muhurta: d.do_ghati_muhurta || null,
    panchaka: d.panchaka || null,
  };
}
