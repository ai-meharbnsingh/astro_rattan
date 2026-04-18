import { useState, useEffect, useRef, useMemo } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Heading } from '@/components/ui/heading';
import { Calendar, Clock, Download, Loader2, MapPin, Search, Share2, Sun, Moon, Star, Sparkles, Timer, Microscope } from 'lucide-react';
import { api } from '@/lib/api';
import { useTranslation } from '@/lib/i18n';
import { translateBackend } from '@/lib/backend-translations';
import MuhuratFinderTab from '@/components/panchang/MuhuratFinderTab';
import MuhuratTab from '@/components/panchang/MuhuratTab';
import SankrantiTab from '@/components/panchang/SankrantiTab';
import PlanetaryPositionsTab from '@/components/panchang/PlanetaryPositionsTab';
import HoraTab from '@/components/panchang/HoraTab';
import LagnaTab from '@/components/panchang/LagnaTab';
import ChoghadiyaTab from '@/components/panchang/ChoghadiyaTab';
import GowriTab from '@/components/panchang/GowriTab';
import TarabalamTab from '@/components/panchang/TarabalamTab';
import HinduCalendarTab from '@/components/panchang/HinduCalendarTab';
import FestivalsTab from '@/components/panchang/FestivalsTab';
import AdvancedTab from '@/components/panchang/AdvancedTab';
import TodaysKeyInsights from '@/components/sections/TodaysKeyInsights';

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
  special_yogas?: {
    sarvartha_siddhi?: { active: boolean; type?: string; name: string; name_hindi: string };
    amrit_siddhi?: { active: boolean; name: string; name_hindi: string };
    dwipushkar?: { active: boolean; name: string; name_hindi: string };
    tripushkar?: { active: boolean; name: string; name_hindi: string };
    ganda_moola?: { active: boolean; nakshatra?: string; name: string; name_hindi: string };
  };
  directions?: {
    disha_shool?: { direction: string; direction_hindi: string; name: string; name_hindi: string };
    baana?: { element: string; element_hindi: string; direction: string; direction_hindi: string };
    anandadi_yoga?: { name: string; name_hindi: string; auspicious: boolean; index: number };
    lucky?: { color: string; color_hindi: string; number: number; direction: string; direction_hindi: string };
  };
  ekadashi_parana?: { name: string; name_hindi: string; start: string; end: string; note: string; note_hindi: string } | null;
  misc?: {
    mantri_mandala?: Array<{ role: string; role_hindi: string; planet: string; planet_hindi: string }>;
    astronomical?: { kaliyuga_year: number; ayanamsha: number; julian_day: number; kali_ahargana: number; rata_die: number; modified_julian_day: number; ayanamsha_label: string };
    panchaka_rahita?: any | null;
  };
  ayanamsa?: number;
}

interface HoraRow { hora: string; lord: string; start: string; end: string; type: string }
interface LagnaRow { lagna: string; start: string; end: string }
interface GowriRow { name: string; start: string; end: string; type: string; quality: string }
interface ChandrabalamRow { rashi: string; balam: string; good: boolean; house_from_moon: number }
interface TarabalamRow { nakshatra: string; tara: string; good: boolean }
interface DoGhatiRow { muhurta: string; name: string; start: string; end: string; quality: string }
interface GeocodeResult { name: string; lat: number; lon: number }

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
  const [cityQuery, setCityQuery] = useState('');
  const [citySuggestions, setCitySuggestions] = useState<GeocodeResult[]>([]);
  const [showCityDropdown, setShowCityDropdown] = useState(false);
  const [searchingCity, setSearchingCity] = useState(false);
  const [currentTime, setCurrentTime] = useState(new Date());
  const [minuteTick, setMinuteTick] = useState(() => Math.floor(Date.now() / 60000));
  const [activeTab, setActiveTab] = useState('calendar');
  const citySearchTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const citySearchRef = useRef<HTMLDivElement>(null);

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
      lang: language,
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

  // Shared minute tick for auto-updating current-period highlights in tabs
  useEffect(() => {
    const updateTick = () => setMinuteTick(Math.floor(Date.now() / 60000));
    updateTick();
    const timer = setInterval(updateTick, 30000);
    const onVisibility = () => {
      if (!document.hidden) updateTick();
    };
    document.addEventListener('visibilitychange', onVisibility);
    return () => {
      clearInterval(timer);
      document.removeEventListener('visibilitychange', onVisibility);
    };
  }, []);

  useEffect(() => {
    const onClickOutside = (event: MouseEvent) => {
      if (citySearchRef.current && !citySearchRef.current.contains(event.target as Node)) {
        setShowCityDropdown(false);
      }
    };
    document.addEventListener('mousedown', onClickOutside);
    return () => document.removeEventListener('mousedown', onClickOutside);
  }, []);

  useEffect(() => {
    return () => {
      if (citySearchTimerRef.current) clearTimeout(citySearchTimerRef.current);
    };
  }, []);



  // Fetch panchang data
  useEffect(() => {
    let cancelled = false;
    const fetchPanchang = async () => {
      setLoading(true);
      try {
        const data = await api.get(
          `/api/panchang?date=${selectedDate}&latitude=${latitude}&longitude=${longitude}&lang=${language}`
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
  }, [selectedDate, latitude, longitude, language]);

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

  const searchCity = (query: string) => {
    setCityQuery(query);
    if (citySearchTimerRef.current) clearTimeout(citySearchTimerRef.current);

    if (query.trim().length < 3) {
      setCitySuggestions([]);
      setShowCityDropdown(false);
      return;
    }

    citySearchTimerRef.current = setTimeout(async () => {
      setSearchingCity(true);
      try {
        const results = await api.get(`/api/kundli/geocode?query=${encodeURIComponent(query.trim())}`);
        const list = Array.isArray(results) ? results as GeocodeResult[] : [];
        setCitySuggestions(list);
        setShowCityDropdown(list.length > 0);
      } catch {
        setCitySuggestions([]);
        setShowCityDropdown(false);
      } finally {
        setSearchingCity(false);
      }
    }, 300);
  };

  const selectCity = (city: GeocodeResult) => {
    setCityQuery(city.name.split(',')[0] || city.name);
    setLatitude(city.lat.toFixed(4));
    setLongitude(city.lon.toFixed(4));
    setShowCityDropdown(false);
  };

  const dateDisplay = new Date(selectedDate + 'T12:00:00').toLocaleDateString(language === 'hi' ? 'hi-IN' : 'en-IN', {
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric',
  });

  return (
    <section ref={sectionRef} id="panchang" className="relative pt-32 pb-8 bg-transparent">
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

        {/* Compact Date/Time + Location — all in one row */}
        <div className="rounded-xl border border-border bg-card p-3 mb-4">
          <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
            <span className="font-semibold text-foreground">{dateDisplay}</span>
            <span className="text-sm text-muted-foreground">{currentTime.toLocaleTimeString(language === 'hi' ? 'hi-IN' : 'en-IN')}</span>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 items-end gap-2">
            <input
              type="date"
              value={selectedDate}
              onChange={(e) => setSelectedDate(e.target.value)}
              className="w-full px-2 py-1.5 rounded-lg bg-white border border-border text-foreground text-sm focus:border-sacred-gold focus:outline-none"
            />
            <div className="relative" ref={citySearchRef}>
              <input
                type="text"
                value={cityQuery}
                onChange={(e) => searchCity(e.target.value)}
                placeholder={t('auto.searchCity')}
                className="w-full px-2 py-1.5 rounded-lg bg-white border border-border text-foreground text-sm focus:border-sacred-gold focus:outline-none"
              />
              {searchingCity && <Loader2 className="w-3.5 h-3.5 animate-spin absolute right-2 top-1/2 -translate-y-1/2 text-muted-foreground" />}
              {showCityDropdown && citySuggestions.length > 0 && (
                <div className="absolute left-0 right-0 top-[calc(100%+4px)] z-30 bg-white border border-border rounded-lg shadow-lg max-h-44 overflow-y-auto">
                  {citySuggestions.map((result, idx) => (
                    <button
                      key={`${result.name}-${idx}`}
                      type="button"
                      onClick={() => selectCity(result)}
                      className="w-full text-left px-2.5 py-2 text-xs text-foreground hover:bg-gray-50 transition-colors"
                    >
                      {result.name}
                    </button>
                  ))}
                </div>
              )}
            </div>
            <input
              type="number"
              step="0.0001"
              value={latitude}
              onChange={(e) => setLatitude(e.target.value)}
              placeholder={t('auto.lat')}
              className="w-full px-2 py-1.5 rounded-lg bg-white border border-border text-foreground text-sm focus:border-sacred-gold focus:outline-none"
            />
            <input
              type="number"
              step="0.0001"
              value={longitude}
              onChange={(e) => setLongitude(e.target.value)}
              placeholder={t('auto.lon')}
              className="w-full px-2 py-1.5 rounded-lg bg-white border border-border text-foreground text-sm focus:border-sacred-gold focus:outline-none"
            />
            <div className="flex items-center">
              <Heading as={4} variant={4} className="sr-only">{t('panchang.locationAndDate')}</Heading>
              <Button onClick={detectLocation} disabled={detectingLocation} size="sm"
                className="btn-sacred text-sm px-3 py-1.5 w-full">
                {detectingLocation ? <Loader2 className="w-3 h-3 animate-spin mr-1" /> : <MapPin className="w-3 h-3 mr-1" />}
                {t('auto.detect')}
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
              <Button
                onClick={handleDownloadPDF}
                disabled={!panchang}
                className="flex items-center gap-2 px-4 py-2 bg-sacred-gold text-white rounded-lg hover:bg-sacred-gold/90 disabled:opacity-50 font-medium text-sm transition-colors"
              >
                <Download className="w-4 h-4" />
                {t('auto.downloadPdf')}
              </Button>
              <Button
                onClick={handleShareWhatsApp}
                disabled={!panchang}
                className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 font-medium text-sm transition-colors"
              >
                <Share2 className="w-4 h-4" />
                {t('auto.shareWhatsApp')}
              </Button>
            </div>

            {/* Today's Key Insights */}
            <TodaysKeyInsights panchang={panchang} language={language} t={t} currentTime={currentTime} />

            {/* Tab Navigation */}
            <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
              <TabsList className="flex w-full flex-wrap gap-1 h-auto p-1 bg-card rounded-xl">
                {[
                  { id: 'calendar', label: language === 'hi' ? 'हिन्दू कैलेंडर' : 'Hindu Calendar', icon: Calendar },
                  { id: 'festivals', label: language === 'hi' ? 'त्योहार/व्रत' : 'Festivals', icon: Sparkles },
                  { id: 'sankranti', label: language === 'hi' ? 'संक्रांति' : 'Sankranti', icon: Calendar },
                  { id: 'muhurat-finder', label: language === 'hi' ? 'मुहूर्त खोजक' : 'Muhurat Finder', icon: Search },
                  { id: 'muhurat', label: t('auto.muhurat'), icon: Timer },
                  { id: 'planets', label: t('auto.planets'), icon: Star },
                  { id: 'hora', label: t('auto.hora'), icon: Clock },
                  { id: 'lagna', label: t('auto.lagna'), icon: Sun },
                  { id: 'choghadiya', label: t('auto.choghadiya'), icon: Sparkles },
                  { id: 'gowri', label: t('auto.gowri'), icon: Moon },
                  { id: 'tarabalam', label: language === 'hi' ? 'तारा/चन्द्र बल' : 'Tara/Chandra', icon: Star },
                  { id: 'advanced', label: language === 'hi' ? 'विशेष' : 'Advanced', icon: Microscope },
                ].map(tab => (
                  <TabsTrigger key={tab.id} value={tab.id} className="flex-1 min-w-0 flex flex-col items-center gap-0.5 py-2 px-1 text-xs data-[state=active]:bg-sacred-gold data-[state=active]:text-white rounded-lg">
                    <tab.icon className="w-4 h-4" />
                    <span className="hidden sm:block">{tab.label}</span>
                  </TabsTrigger>
                ))}
              </TabsList>

              <div className="mt-2">
                <TabsContent value="calendar">
                  {activeTab === 'calendar' && <HinduCalendarTab language={language} t={t} latitude={latitude} longitude={longitude} locationName={cityQuery || undefined} />}
                </TabsContent>
                <TabsContent value="festivals">
                  {activeTab === 'festivals' && <FestivalsTab panchang={panchang} language={language} t={t} selectedDate={selectedDate} />}
                </TabsContent>
                <TabsContent value="sankranti">
                  {activeTab === 'sankranti' && (
                    <SankrantiTab
                      language={language}
                      t={t}
                      latitude={latitude}
                      longitude={longitude}
                      selectedDate={selectedDate}
                    />
                  )}
                </TabsContent>
                <TabsContent value="muhurat-finder">
                  {activeTab === 'muhurat-finder' && <MuhuratFinderTab language={language} t={t} latitude={latitude} longitude={longitude} />}
                </TabsContent>
                <TabsContent value="muhurat">
                  {activeTab === 'muhurat' && <MuhuratTab panchang={panchang} language={language} t={t} currentTime={currentTime} />}
                </TabsContent>
                <TabsContent value="planets">
                  {activeTab === 'planets' && <PlanetaryPositionsTab panchang={panchang} language={language} t={t} />}
                </TabsContent>
                <TabsContent value="hora">
                  {activeTab === 'hora' && <HoraTab panchang={panchang} language={language} t={t} timezoneOffset={tzOffset} minuteTick={minuteTick} />}
                </TabsContent>
                <TabsContent value="lagna">
                  {activeTab === 'lagna' && <LagnaTab panchang={panchang} language={language} t={t} timezoneOffset={tzOffset} minuteTick={minuteTick} />}
                </TabsContent>
                <TabsContent value="choghadiya">
                  {activeTab === 'choghadiya' && <ChoghadiyaTab panchang={panchang} language={language} t={t} timezoneOffset={tzOffset} minuteTick={minuteTick} />}
                </TabsContent>
                <TabsContent value="gowri">
                  {activeTab === 'gowri' && <GowriTab panchang={panchang} language={language} t={t} timezoneOffset={tzOffset} minuteTick={minuteTick} />}
                </TabsContent>
                <TabsContent value="tarabalam">
                  {activeTab === 'tarabalam' && <TarabalamTab panchang={panchang} language={language} t={t} />}
                </TabsContent>
                <TabsContent value="advanced">
                  {activeTab === 'advanced' && <AdvancedTab panchang={panchang} language={language} t={t} />}
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
    misc: d.misc || null,
  };
}
