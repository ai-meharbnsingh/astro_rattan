import { useState, useEffect, useRef, useMemo } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Calendar, Clock, Download, Loader2, MapPin, Navigation, Share2, Sun, Moon, Star, Sparkles, Timer, AlignLeft, CalendarDays, ChevronRight } from 'lucide-react';
import { api } from '@/lib/api';
import { useTranslation } from '@/lib/i18n';
import { translateBackend } from '@/lib/backend-translations';
import PanchangCoreTab from '@/components/panchang/PanchangCoreTab';
import MuhuratTab from '@/components/panchang/MuhuratTab';
import PlanetaryPositionsTab from '@/components/panchang/PlanetaryPositionsTab';
import HoraTab from '@/components/panchang/HoraTab';
import LagnaTab from '@/components/panchang/LagnaTab';
import ChoghadiyaTab from '@/components/panchang/ChoghadiyaTab';
import GowriTab from '@/components/panchang/GowriTab';
import MonthlyCalendarTab from '@/components/panchang/MonthlyCalendarTab';

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

export interface FullPanchangData {
  date: string;
  tithi: { name: string; number: number; paksha: string; end_time?: string; [key: string]: any };
  nakshatra: { name: string; pada: number; lord: string; end_time?: string; [key: string]: any };
  yoga: { name: string; number: number; end_time?: string; [key: string]: any };
  karana: { name: string; number: number; end_time?: string; [key: string]: any };
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
  night_choghadiya?: ChoghadiyaPeriod[];
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
  hora_table?: HoraRow[] | null;
  lagna_table?: LagnaRow[] | null;
  chandrabalam?: ChandrabalamRow[] | null;
  tarabalam?: TarabalamRow[] | null;
  gowri_panchang?: GowriRow[] | null;
  do_ghati_muhurta?: DoGhatiRow[] | null;
  panchaka?: { active: boolean; rahita: boolean } | null;
}

interface HoraRow { hora: string; lord: string; start: string; end: string; type: string }
interface LagnaRow { lagna: string; start: string; end: string }
interface GowriRow { name: string; start: string; end: string; type: string; quality: string }
interface ChandrabalamRow { rashi: string; balam: string; good: boolean; house_from_moon: number }
interface TarabalamRow { nakshatra: string; tara: string; good: boolean }
interface DoGhatiRow { muhurta: string; name: string; start: string; end: string; quality: string }

const DEFAULT_LAT = '28.6139';
const DEFAULT_LON = '77.2090';

// Helper: Get local date as YYYY-MM-DD (fixes UTC timezone issue)
const getLocalDateString = () => {
  const now = new Date();
  return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;
};

export default function Panchang() {
  const { t, language } = useTranslation();
  const sectionRef = useRef<HTMLDivElement>(null);
  const [loading, setLoading] = useState(true);
  const [panchang, setPanchang] = useState<FullPanchangData | null>(null);
  const [selectedDate, setSelectedDate] = useState(() => getLocalDateString());
  const [latitude, setLatitude] = useState(DEFAULT_LAT);
  const [longitude, setLongitude] = useState(DEFAULT_LON);
  const [detectingLocation, setDetectingLocation] = useState(false);
  const [currentTime, setCurrentTime] = useState(new Date());
  const [activeTab, setActiveTab] = useState('core');

  // Calculate timezone offset from longitude (IST for India, otherwise approximate)
  const tzOffset = useMemo(() => {
    const lon = parseFloat(longitude) || 77.2090;
    if (lon >= 68 && lon <= 97.5) return 5.5 * 60; // IST in minutes
    return Math.round(lon / 15) * 60; // approximate
  }, [longitude]);

  // Format date in Hindi for WhatsApp sharing
  const formatDateHindi = (dateStr: string) => {
    return new Date(dateStr + 'T12:00:00').toLocaleDateString('hi-IN', {
      weekday: 'long', year: 'numeric', month: 'long', day: 'numeric',
    });
  };

  // Download Panchang as PDF
  const handleDownloadPDF = () => {
    const params = new URLSearchParams({
      date: selectedDate,
      latitude: String(latitude),
      longitude: String(longitude),
    });
    const a = document.createElement('a');
    a.href = `/api/panchang/pdf?${params}`;
    a.download = `Panchang_${selectedDate}.pdf`;
    a.style.display = 'none';
    document.body.appendChild(a);
    a.click();
    // Remove after a delay so browser can initiate download
    setTimeout(() => document.body.removeChild(a), 1000);
  };

  // Share Panchang via WhatsApp
  const handleShareWhatsApp = () => {
    if (!panchang) return;
    const p = panchang;
    const hc = p.hindu_calendar || {} as HinduCalendarData;
    const tithiLine = `${p.tithi?.name || ''} ${p.tithi?.end_time || ''} तक${(p.tithi as any)?.next ? ' तत्पश्चात् ' + (p.tithi as any).next : ''}`;
    const nakLine = `${p.nakshatra?.name || ''} ${p.nakshatra?.end_time || ''} तक${(p.nakshatra as any)?.next ? ' तत्पश्चात् ' + (p.nakshatra as any).next : ''}`;
    const yogaLine = `${p.yoga?.name || ''} ${p.yoga?.end_time || ''} तक${(p.yoga as any)?.next ? ' तत्पश्चात् ' + (p.yoga as any).next : ''}`;
    const karanaLine = `${p.karana?.name || ''}${(p.karana as any)?.second_karana ? ' तत्पश्चात् ' + (p.karana as any).second_karana : ''}`;

    const text = `*卐~ हिन्दू पंचांग ~卐*

*🌞 दिनांक - ${formatDateHindi(selectedDate)}*
*⛅दिन - ${p.vaar?.name || ''}*
*⛅विक्रम संवत् - ${hc.vikram_samvat || ''}*
*⛅अयन - ${hc.ayana || ''}*
*⛅ऋतु - ${hc.ritu || ''}*
*⛅मास - ${hc.maas || ''}*
*⛅पक्ष - ${hc.paksha || ''}*
*⛅तिथि - ${tithiLine}*
*⛅नक्षत्र - ${nakLine}*
*⛅योग - ${yogaLine}*
*⛅करण - ${karanaLine}*
*⛅राहुकाल - ${p.rahu_kaal?.start || ''} से ${p.rahu_kaal?.end || ''} तक*
*⛅सूर्योदय - ${p.sunrise || ''}*
*⛅सूर्यास्त - ${p.sunset || ''}*
*⛅ब्रह्ममुहूर्त - ${p.brahma_muhurat?.start || ''} से ${p.brahma_muhurat?.end || ''} तक*
*⛅अभिजीत मुहूर्त - ${p.abhijit_muhurat?.start || ''} से ${p.abhijit_muhurat?.end || ''} तक*
*⛅निशिता मुहूर्त - ${(p as any).nishita_muhurta?.start || (p as any).nishita_muhurat?.start || ''} से ${(p as any).nishita_muhurta?.end || (p as any).nishita_muhurat?.end || ''} तक*
*⛅सूर्य राशि - ${p.sun_sign || ''}*
*⛅चन्द्र राशि - ${p.moon_sign || ''}*
${p.festivals?.length ? '*🌥️व्रत पर्व - ' + p.festivals.map((f: any) => f.name_hindi || f.name).join(', ') + '*' : ''}

_Generated by AstroRattan.com_`;

    const encoded = encodeURIComponent(text);
    window.open(`https://wa.me/?text=${encoded}`, '_blank');
  };

  // Live clock - update every minute instead of every second to reduce re-renders
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
    <section ref={sectionRef} id="panchang" className="relative pt-24 pb-8 bg-transparent">
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

        {/* Compact Date/Time + Location — all in one row */}
        <div className="rounded-xl border border-cosmic-border bg-cosmic-card p-3 mb-4">
          <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
            <span className="font-semibold text-cosmic-text">{dateDisplay}</span>
            <span className="text-sm text-cosmic-text-secondary">{currentTime.toLocaleTimeString('en-IN')}</span>
          </div>
          <div className="flex flex-wrap items-end gap-2">
            <input type="date" value={selectedDate} onChange={(e) => setSelectedDate(e.target.value)}
              className="px-2 py-1.5 rounded-lg bg-white border border-cosmic-border text-cosmic-text text-sm focus:border-sacred-gold focus:outline-none" />
            <input type="number" step="0.0001" value={latitude} onChange={(e) => setLatitude(e.target.value)} placeholder="Lat"
              className="w-24 px-2 py-1.5 rounded-lg bg-white border border-cosmic-border text-cosmic-text text-sm focus:border-sacred-gold focus:outline-none" />
            <input type="number" step="0.0001" value={longitude} onChange={(e) => setLongitude(e.target.value)} placeholder="Lon"
              className="w-24 px-2 py-1.5 rounded-lg bg-white border border-cosmic-border text-cosmic-text text-sm focus:border-sacred-gold focus:outline-none" />
            <div className="flex items-center gap-2">
              <h4 className="sr-only">{t('panchang.locationAndDate')}</h4>
              <Button onClick={detectLocation} disabled={detectingLocation} size="sm"
                className="btn-sacred text-sm px-3 py-1.5">
                {detectingLocation ? <Loader2 className="w-3 h-3 animate-spin mr-1" /> : <MapPin className="w-3 h-3 mr-1" />}
                {language === 'hi' ? 'स्थान' : 'Detect'}
              </Button>
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
          <div className="space-y-4 min-h-[400px]">

            {/* Download & Share Buttons */}
            <div className="flex flex-wrap items-center gap-2">
              <button
                onClick={handleDownloadPDF}
                disabled={!panchang}
                className="flex items-center gap-2 px-4 py-2 bg-sacred-gold text-white rounded-lg hover:bg-sacred-gold/90 disabled:opacity-50 font-medium text-sm transition-colors"
              >
                <Download className="w-4 h-4" />
                Download PDF
              </button>
              <button
                onClick={handleShareWhatsApp}
                disabled={!panchang}
                className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 font-medium text-sm transition-colors"
              >
                <Share2 className="w-4 h-4" />
                Share WhatsApp
              </button>
            </div>

            {/* Tab Navigation */}
            <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
              <TabsList className="grid grid-cols-5 sm:grid-cols-10 gap-1 h-auto p-1 bg-cosmic-card rounded-xl">
                {[
                  { id: 'core', label: language === 'hi' ? 'पंचांग' : 'Core', icon: AlignLeft },
                  { id: 'muhurat', label: language === 'hi' ? 'मुहूर्त' : 'Muhurat', icon: Timer },
                  { id: 'planets', label: language === 'hi' ? 'ग्रह' : 'Planets', icon: Star },
                  { id: 'hora', label: language === 'hi' ? 'होरा' : 'Hora', icon: Clock },
                  { id: 'lagna', label: language === 'hi' ? 'लग्न' : 'Lagna', icon: Sun },
                  { id: 'choghadiya', label: language === 'hi' ? 'चौघड़िया' : 'Choghadiya', icon: Sparkles },
                  { id: 'gowri', label: language === 'hi' ? 'गौरी' : 'Gowri', icon: Moon },
                  { id: 'monthly', label: language === 'hi' ? 'त्योहार' : 'Festivals', icon: CalendarDays },
                ].map(tab => (
                  <TabsTrigger key={tab.id} value={tab.id} className="flex flex-col items-center gap-0.5 py-2 px-1 text-xs data-[state=active]:bg-sacred-gold data-[state=active]:text-white rounded-lg">
                    <tab.icon className="w-4 h-4" />
                    <span className="hidden sm:block">{tab.label}</span>
                  </TabsTrigger>
                ))}
              </TabsList>

              <div className="mt-4">
                <TabsContent value="core">
                  <PanchangCoreTab panchang={panchang} language={language} t={t} />
                </TabsContent>
                <TabsContent value="muhurat">
                  <MuhuratTab panchang={panchang} language={language} t={t} />
                </TabsContent>
                <TabsContent value="planets">
                  <PlanetaryPositionsTab panchang={panchang} language={language} t={t} />
                </TabsContent>
                <TabsContent value="hora">
                  <HoraTab panchang={panchang} language={language} t={t} timezoneOffset={tzOffset} />
                </TabsContent>
                <TabsContent value="lagna">
                  <LagnaTab panchang={panchang} language={language} t={t} timezoneOffset={tzOffset} />
                </TabsContent>
                <TabsContent value="choghadiya">
                  <ChoghadiyaTab panchang={panchang} language={language} t={t} timezoneOffset={tzOffset} />
                </TabsContent>
                <TabsContent value="gowri">
                  <GowriTab panchang={panchang} language={language} t={t} timezoneOffset={tzOffset} />
                </TabsContent>
                <TabsContent value="monthly">
                  <MonthlyCalendarTab language={language} t={t} latitude={latitude} longitude={longitude} />
                </TabsContent>
              </div>
            </Tabs>
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
  const d = data as Partial<FullPanchangData>;
  return {
    date: d.date || '',
    tithi: d.tithi || { name: '', number: 0, paksha: '' },
    nakshatra: d.nakshatra || { name: '', pada: 0, lord: '' },
    yoga: d.yoga || { name: '', number: 0 },
    karana: d.karana || { name: '', number: 0 },
    sunrise: d.sunrise || '--:--',
    sunset: d.sunset || '--:--',
    moonrise: d.moonrise || '--:--',
    moonset: d.moonset || '--:--',
    vaar: d.vaar || { name: 'Somvar', english: 'Monday', number: 0 },
    rahu_kaal: d.rahu_kaal || { start: '--:--', end: '--:--' },
    gulika_kaal: d.gulika_kaal || { start: '--:--', end: '--:--' },
    yamaganda: d.yamaganda || { start: '--:--', end: '--:--' },
    abhijit_muhurat: d.abhijit_muhurat || { start: '--:--', end: '--:--' },
    brahma_muhurat: d.brahma_muhurat || { start: '--:--', end: '--:--' },
    choghadiya: Array.isArray(d.choghadiya) ? d.choghadiya : [],
    night_choghadiya: Array.isArray(d.night_choghadiya) ? d.night_choghadiya : [],
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
