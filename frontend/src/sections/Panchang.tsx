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

  // GSAP animation
  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.fromTo('.panchang-title', { y: 50, opacity: 0 }, {
        y: 0, opacity: 1, duration: 0.8, ease: 'power3.out',
        scrollTrigger: { trigger: sectionRef.current, start: 'top 80%' },
      });
    }, sectionRef);
    return () => ctx.revert();
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
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-sacred-saffron/10 text-sacred-saffron text-sm font-medium mb-6 border border-sacred-saffron/30">
            <Calendar className="w-4 h-4" />Daily Panchang
          </div>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-sacred font-bold text-cosmic-text mb-4">
            Cosmic Timekeeping with<span className="text-gradient-saffron"> Panchang</span>
          </h2>
        </div>

        {/* Date/Time Bar + Location Controls */}
        <div className="card-gold-border rounded-2xl p-4 mb-8">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-xl bg-sacred-gold/10 flex items-center justify-center border border-sacred-gold/20">
                <Calendar className="w-6 h-6 text-sacred-gold" />
              </div>
              <div>
                <p className="text-sm text-cosmic-text-secondary">Date</p>
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

          {/* Date picker + Location row */}
          <div className="mt-4 flex flex-wrap items-end gap-3">
            <div>
              <label className="block text-xs text-cosmic-text-secondary mb-1">Date</label>
              <input
                type="date"
                value={selectedDate}
                onChange={(e) => setSelectedDate(e.target.value)}
                className="px-3 py-2 rounded-xl bg-cosmic-card border border-sacred-gold/20 text-cosmic-text text-sm focus:border-sacred-gold/50 focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-xs text-cosmic-text-secondary mb-1 flex items-center gap-1">
                <MapPin className="w-3 h-3" />Latitude
              </label>
              <input
                type="number" step="0.0001" value={latitude}
                onChange={(e) => setLatitude(e.target.value)}
                className="w-28 px-3 py-2 rounded-xl bg-cosmic-card border border-sacred-gold/20 text-cosmic-text text-sm focus:border-sacred-gold/50 focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-xs text-cosmic-text-secondary mb-1 flex items-center gap-1">
                <MapPin className="w-3 h-3" />Longitude
              </label>
              <input
                type="number" step="0.0001" value={longitude}
                onChange={(e) => setLongitude(e.target.value)}
                className="w-28 px-3 py-2 rounded-xl bg-cosmic-card border border-sacred-gold/20 text-cosmic-text text-sm focus:border-sacred-gold/50 focus:outline-none"
              />
            </div>
            <Button
              onClick={detectLocation}
              disabled={detectingLocation}
              className="btn-sacred bg-sacred-gold/10 text-sacred-gold hover:bg-sacred-gold hover:text-cosmic-bg border border-sacred-gold/30 transition-all text-sm px-4 py-2"
            >
              {detectingLocation ? <Loader2 className="w-4 h-4 animate-spin mr-1" /> : <Navigation className="w-4 h-4 mr-1" />}
              Detect Location
            </Button>
          </div>
        </div>

        {/* Loading */}
        {loading && !panchang && (
          <div className="flex items-center justify-center py-20">
            <Loader2 className="w-10 h-10 text-sacred-gold animate-spin" />
          </div>
        )}

        {/* Main Panchang Dashboard */}
        {panchang && (
          <div className="space-y-8">

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
                <Card className="card-sacred border-sacred-gold/20 h-full">
                  <CardContent className="p-6">
                    <h3 className="text-xl font-sacred font-semibold text-cosmic-text mb-6 flex items-center gap-2">
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
              <SunMoonTimes
                sunrise={panchang.sunrise}
                sunset={panchang.sunset}
                moonrise={panchang.moonrise}
                moonset={panchang.moonset}
              />
              <InauspiciousPeriods
                rahu_kaal={panchang.rahu_kaal}
                gulika_kaal={panchang.gulika_kaal}
                yamaganda={panchang.yamaganda}
              />
              <AuspiciousTimings
                abhijit_muhurat={panchang.abhijit_muhurat}
                brahma_muhurat={panchang.brahma_muhurat}
                choghadiya={panchang.choghadiya}
              />
            </div>

            {/* ROW 3: Planetary Positions */}
            <PlanetaryPositions planets={panchang.planetary_positions} />

            {/* ROW 4: Muhurat Finder */}
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
  };
}
