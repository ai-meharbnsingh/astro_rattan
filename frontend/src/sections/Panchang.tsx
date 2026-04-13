import { useState, useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Calendar, Clock, Download, Loader2, MapPin, Navigation, Share2 } from 'lucide-react';
import { api } from '@/lib/api';
import { useTranslation } from '@/lib/i18n';
import { translateBackend } from '@/lib/backend-translations';

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

export default function Panchang() {
  const { t, language } = useTranslation();
  const sectionRef = useRef<HTMLDivElement>(null);
  const [loading, setLoading] = useState(true);
  const [panchang, setPanchang] = useState<FullPanchangData | null>(null);
  const [selectedDate, setSelectedDate] = useState(() => new Date().toISOString().split('T')[0]);
  const [latitude, setLatitude] = useState(DEFAULT_LAT);
  const [longitude, setLongitude] = useState(DEFAULT_LON);
  const [detectingLocation, setDetectingLocation] = useState(false);
  const [downloadingPdf, setDownloadingPdf] = useState(false);
  const [currentTime, setCurrentTime] = useState(new Date());

  // Format date in Hindi for WhatsApp sharing
  const formatDateHindi = (dateStr: string) => {
    return new Date(dateStr + 'T12:00:00').toLocaleDateString('hi-IN', {
      weekday: 'long', year: 'numeric', month: 'long', day: 'numeric',
    });
  };

  // Download Panchang as PDF
  const handleDownloadPDF = async () => {
    try {
      setDownloadingPdf(true);
      const params = new URLSearchParams({
        date: selectedDate,
        latitude: String(latitude),
        longitude: String(longitude),
      });
      const response = await fetch(`/api/panchang/pdf?${params}`);
      if (!response.ok) throw new Error('Download failed');
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `panchang_${selectedDate}.pdf`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error('PDF download failed:', err);
    } finally {
      setDownloadingPdf(false);
    }
  };

  // Share Panchang via WhatsApp
  const handleShareWhatsApp = () => {
    if (!panchang) return;
    const p = panchang;
    const hc = p.hindu_calendar || {} as HinduCalendarData;
    const text = `*卐~ हिन्दू पंचांग ~卐*

*🌞 दिनांक - ${formatDateHindi(selectedDate)}*
*⛅दिन - ${p.vaar?.name || ''}*
*⛅विक्रम संवत् - ${hc.vikram_samvat || ''}*
*⛅अयन - ${hc.ayana || ''}*
*⛅ऋतु - ${hc.ritu || ''}*
*⛅मास - ${hc.maas || ''}*
*⛅पक्ष - ${hc.paksha || ''}*
*⛅तिथि - ${p.tithi?.name || ''} ${p.tithi?.end_time || ''} तक*
*⛅नक्षत्र - ${p.nakshatra?.name || ''} ${p.nakshatra?.end_time || ''} तक*
*⛅योग - ${p.yoga?.name || ''} ${p.yoga?.end_time || ''} तक*
*⛅करण - ${p.karana?.name || ''}*
*⛅राहुकाल - ${p.rahu_kaal?.start || ''} से ${p.rahu_kaal?.end || ''} तक*
*⛅सूर्योदय - ${p.sunrise || ''}*
*⛅सूर्यास्त - ${p.sunset || ''}*
*⛅ब्रह्ममुहूर्त - ${p.brahma_muhurat?.start || ''} से ${p.brahma_muhurat?.end || ''} तक*
*⛅अभिजीत मुहूर्त - ${p.abhijit_muhurat?.start || ''} से ${p.abhijit_muhurat?.end || ''} तक*
${p.festivals?.length ? '*🌥️व्रत पर्व - ' + p.festivals.map(f => f.name_hindi || f.name).join(', ') + '*' : ''}

_Generated by AstroRattan.com_`;

    const encoded = encodeURIComponent(text);
    window.open(`https://wa.me/?text=${encoded}`, '_blank');
  };

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
            <Calendar className="w-4 h-4" />{t('panchang.dailyPanchang')}
          </div>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-sans font-bold text-cosmic-text mb-4">
            {t('panchang.cosmicTimekeepingWith')}<span className="text-gradient-saffron"> {t('nav.panchang')}</span>
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
                <p className="text-sm text-cosmic-text-secondary">{t('common.date')}</p>
                <p className="text-lg font-sans font-semibold text-cosmic-text">{dateDisplay}</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-xl bg-sacred-saffron flex items-center justify-center border border-sacred-saffron">
                <Clock className="w-6 h-6 text-sacred-saffron" />
              </div>
              <div>
                <p className="text-sm text-cosmic-text-secondary">{t('panchang.currentTime')}</p>
                <p className="text-lg font-sans font-semibold text-cosmic-text">{currentTime.toLocaleTimeString('en-IN')}</p>
              </div>
            </div>
          </div>

          {/* Location & Date grouped inputs */}
          <div className="mt-4 rounded-xl border border-cosmic-border bg-cosmic-card p-4">
            <div className="flex items-center justify-between mb-3">
              <h4 className="text-sm font-semibold text-cosmic-text flex items-center gap-1.5">
                <MapPin className="w-4 h-4 text-sacred-gold" />{t('panchang.locationAndDate')}
              </h4>
              <Button
                onClick={detectLocation}
                disabled={detectingLocation}
                className="btn-sacred bg-sacred-gold-dark text-white hover:bg-gray-50 hover:text-cosmic-bg border border-sacred-gold transition-all text-sm px-4 py-2"
              >
                {detectingLocation ? <Loader2 className="w-4 h-4 animate-spin mr-1" /> : <Navigation className="w-4 h-4 mr-1" />}
                {t('panchang.detectLocation')}
              </Button>
            </div>
            <div className="space-y-3">
              {/* Date — full width */}
              <div>
                <label className="block text-sm font-medium text-cosmic-text-secondary mb-1">{t('common.date')}</label>
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
                    <MapPin className="w-3 h-3" />{t('panchang.latitude')}
                  </label>
                  <input
                    type="number" step="0.0001" value={latitude}
                    onChange={(e) => setLatitude(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl bg-white border border-cosmic-border text-cosmic-text text-sm focus:border-sacred-gold focus:outline-none transition-colors"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-cosmic-text-secondary mb-1 flex items-center gap-1">
                    <MapPin className="w-3 h-3" />{t('panchang.longitude')}
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

            {/* Download & Share Buttons */}
            <div className="flex flex-wrap items-center gap-3">
              <button
                onClick={handleDownloadPDF}
                disabled={downloadingPdf || !panchang}
                className="flex items-center gap-2 px-4 py-2 bg-sacred-gold text-white rounded-lg hover:bg-sacred-gold/90 disabled:opacity-50 font-medium text-sm transition-colors"
              >
                <Download className="w-4 h-4" />
                {downloadingPdf ? 'Generating...' : 'Download PDF'}
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
                      <Calendar className="w-5 h-5 text-sacred-gold" />{t('panchang.todayPanchang')}
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
                    {panchang.sun_sign && <div className="flex justify-between"><span className="text-cosmic-text">{t('panchang.sunSign')}</span><span className="font-medium text-cosmic-text">{translateBackend(panchang.sun_sign, language)}</span></div>}
                    {panchang.moon_sign && <div className="flex justify-between"><span className="text-cosmic-text">{t('panchang.moonSign')}</span><span className="font-medium text-cosmic-text">{translateBackend(panchang.moon_sign, language)}</span></div>}
                    {panchang.dinamana && <div className="flex justify-between"><span className="text-cosmic-text">{t('panchang.dinamana')}</span><span className="font-medium text-cosmic-text">{panchang.dinamana}</span></div>}
                    {panchang.ratrimana && <div className="flex justify-between"><span className="text-cosmic-text">{t('panchang.ratrimana')}</span><span className="font-medium text-cosmic-text">{panchang.ratrimana}</span></div>}
                    {panchang.madhyahna && <div className="flex justify-between"><span className="text-cosmic-text">{t('panchang.madhyahna')}</span><span className="font-medium text-cosmic-text">{panchang.madhyahna}</span></div>}
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
              {panchang.hora_table && <ExpandableSection title={language === 'hi' ? 'होरा मुहूर्त' : 'Hora Muhurta'} desc={language === 'hi' ? '24 ग्रह घंटे' : '24 planetary hours'}>
                <div className="overflow-x-auto"><table className="w-full text-sm"><thead><tr className="bg-sacred-gold/20"><th className="p-2 text-left text-sacred-gold-dark">{language === 'hi' ? 'होरा' : 'Hora'}</th><th className="p-2 text-left">{t('kundli.lord')}</th><th className="p-2">{t('table.start')}</th><th className="p-2">{t('table.end')}</th><th className="p-2">{t('table.type')}</th></tr></thead><tbody>
                {(panchang.hora_table as HoraRow[]).map((h, i) => (
                  <tr key={i} className="border-t border-sacred-gold"><td className="p-2 text-cosmic-text">{h.hora}</td><td className="p-2 text-cosmic-text font-medium">{translateBackend(h.lord, language)}</td><td className="p-2 text-cosmic-text">{h.start}</td><td className="p-2 text-cosmic-text">{h.end}</td><td className="p-2"><span className={`text-sm px-2 py-0.5 rounded ${h.type === 'day' ? 'bg-amber-100 text-amber-700' : 'bg-blue-100 text-blue-700'}`}>{translateBackend(h.type, language)}</span></td></tr>
                ))}</tbody></table></div>
              </ExpandableSection>}

              {/* Lagna Table */}
              {panchang.lagna_table && <ExpandableSection title={language === 'hi' ? 'लग्न मुहूर्त' : 'Lagna Muhurta'} desc={language === 'hi' ? 'दिन भर की उदय राशि' : 'Rising sign through the day'}>
                <div className="overflow-x-auto"><table className="w-full text-sm"><thead><tr className="bg-sacred-gold/20"><th className="p-2 text-left text-sacred-gold-dark">{t('section.lagna')}</th><th className="p-2">{t('table.start')}</th><th className="p-2">{t('table.end')}</th></tr></thead><tbody>
                {(panchang.lagna_table as LagnaRow[]).map((l, i) => (
                  <tr key={i} className="border-t border-sacred-gold"><td className="p-2 text-cosmic-text font-medium">{translateBackend(l.lagna, language)}</td><td className="p-2 text-cosmic-text">{l.start}</td><td className="p-2 text-cosmic-text">{l.end}</td></tr>
                ))}</tbody></table></div>
              </ExpandableSection>}

              {/* Gowri Panchangam */}
              {panchang.gowri_panchang && <ExpandableSection title={language === 'hi' ? 'गौरी पंचांगम' : 'Gowri Panchangam'} desc={language === 'hi' ? 'दिन और रात के गुणवत्ता काल' : 'Day and night quality periods'}>
                <div className="overflow-x-auto"><table className="w-full text-sm"><thead><tr className="bg-sacred-gold/20"><th className="p-2 text-left text-sacred-gold-dark">{t('table.period')}</th><th className="p-2">{t('table.start')}</th><th className="p-2">{t('table.end')}</th><th className="p-2">{t('table.type')}</th><th className="p-2">{language === 'hi' ? 'गुणवत्ता' : 'Quality'}</th></tr></thead><tbody>
                {(panchang.gowri_panchang as GowriRow[]).map((g, i) => (
                  <tr key={i} className={`border-t border-sacred-gold ${g.quality === 'good' ? 'bg-green-50' : ''}`}><td className="p-2 text-cosmic-text font-medium">{translateBackend(g.name, language)}</td><td className="p-2 text-cosmic-text">{g.start}</td><td className="p-2 text-cosmic-text">{g.end}</td><td className="p-2"><span className={`text-sm px-2 py-0.5 rounded ${g.type === 'day' ? 'bg-amber-100 text-amber-700' : 'bg-blue-100 text-blue-700'}`}>{translateBackend(g.type, language)}</span></td><td className="p-2"><span className={`text-sm px-2 py-0.5 rounded ${g.quality === 'good' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>{g.quality === 'good' ? (language === 'hi' ? 'शुभ' : 'Shubh') : (language === 'hi' ? 'अशुभ' : 'Ashubh')}</span></td></tr>
                ))}</tbody></table></div>
              </ExpandableSection>}

              {/* Chandrabalam */}
              {panchang.chandrabalam && <ExpandableSection title={language === 'hi' ? 'चंद्रबल' : 'Chandrabalam'} desc={language === 'hi' ? 'सभी 12 राशियों के लिए चंद्र बल' : 'Moon strength for all 12 Rashi'}>
                <div className="grid grid-cols-3 sm:grid-cols-4 gap-2">
                {(panchang.chandrabalam as ChandrabalamRow[]).map((c, i) => (
                  <div key={i} className={`p-3 text-center border rounded ${c.good ? 'border-green-300 bg-green-50' : 'border-red-200 bg-red-50'}`}>
                    <p className="text-sm font-medium text-cosmic-text">{translateBackend(c.rashi, language)}</p>
                    <p className={`text-sm font-semibold ${c.good ? 'text-green-600' : 'text-red-500'}`}>{translateBackend(c.balam, language)}</p>
                    <p className="text-sm text-cosmic-text">{t('common.house')} {c.house_from_moon}</p>
                  </div>
                ))}
                </div>
              </ExpandableSection>}

              {/* Tarabalam */}
              {panchang.tarabalam && <ExpandableSection title={language === 'hi' ? 'ताराबल' : 'Tarabalam'} desc={language === 'hi' ? 'सभी 27 नक्षत्रों का बल' : 'Star strength for all 27 Nakshatra'}>
                <div className="grid grid-cols-3 sm:grid-cols-4 lg:grid-cols-5 gap-2">
                {(panchang.tarabalam as TarabalamRow[]).map((t, i) => (
                  <div key={i} className={`p-2 text-center border rounded ${t.good ? 'border-green-300 bg-green-50' : 'border-red-200 bg-red-50'}`}>
                    <p className="text-sm font-medium text-cosmic-text">{translateBackend(t.nakshatra, language)}</p>
                    <p className={`text-sm font-semibold ${t.good ? 'text-green-600' : 'text-red-500'}`}>{translateBackend(t.tara, language)}</p>
                  </div>
                ))}
                </div>
              </ExpandableSection>}

              {/* Do Ghati Muhurta */}
              {panchang.do_ghati_muhurta && <ExpandableSection title={language === 'hi' ? 'दो घटी मुहूर्त' : 'Do Ghati Muhurta'} desc={language === 'hi' ? 'दिन का 30 मुहूर्त विभाजन' : '30 Muhurta division of the day'}>
                <div className="overflow-x-auto"><table className="w-full text-sm"><thead><tr className="bg-sacred-gold/20"><th className="p-2 text-left text-sacred-gold-dark">#</th><th className="p-2 text-left">{t('table.name')}</th><th className="p-2">{t('table.start')}</th><th className="p-2">{t('table.end')}</th><th className="p-2">{language === 'hi' ? 'गुणवत्ता' : 'Quality'}</th></tr></thead><tbody>
                {(panchang.do_ghati_muhurta as DoGhatiRow[]).map((m, i) => (
                  <tr key={i} className={`border-t border-sacred-gold ${m.quality === 'good' ? 'bg-green-50' : ''}`}><td className="p-2 text-cosmic-text">{m.muhurta}</td><td className="p-2 text-cosmic-text font-medium">{translateBackend(m.name, language)}</td><td className="p-2 text-cosmic-text">{m.start}</td><td className="p-2 text-cosmic-text">{m.end}</td><td className="p-2"><span className={`text-sm px-2 py-0.5 rounded ${m.quality === 'good' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'}`}>{translateBackend(m.quality, language)}</span></td></tr>
                ))}</tbody></table></div>
              </ExpandableSection>}

              {/* Panchaka */}
              {panchang.panchaka && <div className={`p-4 rounded-xl border ${panchang.panchaka.active ? 'border-red-300 bg-red-50' : 'border-green-300 bg-green-50'}`}>
                <p className="text-sm font-medium text-cosmic-text">{language === 'hi' ? 'पंचक रहित' : 'Panchaka Rahita'}: <span className={`font-semibold ${panchang.panchaka.rahita ? 'text-green-600' : 'text-red-500'}`}>{panchang.panchaka.rahita ? (language === 'hi' ? 'सुरक्षित — आज पंचक नहीं' : 'Safe — No Panchaka today') : (language === 'hi' ? 'पंचक सक्रिय — सावधानी रखें' : 'Panchaka Active — Caution advised')}</span></p>
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
      <button onClick={() => setOpen(!open)} className="w-full flex items-center justify-between p-4 hover:bg-gray-50 transition-colors">
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
