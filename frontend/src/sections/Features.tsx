import { useEffect, useRef, useState } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Card, CardContent } from '@/components/ui/card';
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { api } from '@/lib/api';
import { useTranslation } from '@/lib/i18n';
import { Calendar, ChevronDown, ChevronUp, Loader2, MapPin, Sparkles, Sun, X } from 'lucide-react';
import { Heading } from '@/components/ui/heading';

gsap.registerPlugin(ScrollTrigger);

const SIGNS = [
  { id: 'aries', en: 'Aries', hi: 'मेष' },
  { id: 'taurus', en: 'Taurus', hi: 'वृषभ' },
  { id: 'gemini', en: 'Gemini', hi: 'मिथुन' },
  { id: 'cancer', en: 'Cancer', hi: 'कर्क' },
  { id: 'leo', en: 'Leo', hi: 'सिंह' },
  { id: 'virgo', en: 'Virgo', hi: 'कन्या' },
  { id: 'libra', en: 'Libra', hi: 'तुला' },
  { id: 'scorpio', en: 'Scorpio', hi: 'वृश्चिक' },
  { id: 'sagittarius', en: 'Sagittarius', hi: 'धनु' },
  { id: 'capricorn', en: 'Capricorn', hi: 'मकर' },
  { id: 'aquarius', en: 'Aquarius', hi: 'कुंभ' },
  { id: 'pisces', en: 'Pisces', hi: 'मीन' },
] as const;

type HoroscopeSections = {
  general?: string;
  love?: string;
  career?: string;
  finance?: string;
  health?: string;
};

type HoroscopeData = {
  sign?: string;
  sign_hindi?: string;
  dates?: string;
  sections?: HoroscopeSections;
};

type PanchangData = {
  sunrise?: string;
  sunset?: string;
  moonrise?: string;
  moonset?: string;
  dinamana?: string;
  ratrimana?: string;
  madhyahna?: string;
  sun_sign?: string;
  moon_sign?: string;
  sun_longitude?: number;
  tithi?: { name?: string; end_time?: string; paksha?: string };
  nakshatra?: { name?: string; end_time?: string };
  yoga?: { name?: string; end_time?: string };
  karana?: { name?: string; end_time?: string; second_karana?: string; second_karana_end_time?: string };
  vaar?: { name?: string; english?: string };
  rahu_kaal?: { start?: string; end?: string };
  gulika_kaal?: { start?: string; end?: string };
  yamaganda?: { start?: string; end?: string };
  abhijit_muhurat?: { start?: string; end?: string };
  brahma_muhurat?: { start?: string; end?: string };
  dur_muhurtam?: { start?: string; end?: string };
  varjyam?: { start?: string; end?: string };
  amrit_siddhi?: { active?: boolean; start?: string; end?: string };
  moon_sign_transition?: { time?: string; to_sign?: string };
  hindu_calendar?: { maas?: string; shaka_samvat?: number; vikram_samvat?: number };
};

type FestivalRow = {
  name?: string;
  date?: string;
  description?: string;
  rituals?: string;
};

const uniqNames = (items: string[]) => {
  const seen = new Set<string>();
  return items.filter((item) => {
    const key = String(item || '').trim().toLowerCase();
    if (!key || seen.has(key)) return false;
    seen.add(key);
    return true;
  });
};

const generateObservancesFromDay = (day: { date?: string; tithi?: string; nakshatra?: string; paksha?: string }) => {
  const tithi = String(day?.tithi || '').toLowerCase();
  const nakshatra = String(day?.nakshatra || '').toLowerCase();
  const paksha = String(day?.paksha || '').toLowerCase();
  const dateObj = day?.date ? new Date(`${day.date}T00:00:00`) : null;
  const weekday = dateObj ? dateObj.getDay() : -1;
  const list: string[] = [];

  if (tithi.includes('ekadashi')) list.push('Ekadashi Vrat');
  if (tithi.includes('trayodashi') || tithi.includes('pradosh')) list.push('Pradosh Vrat');
  if (tithi.includes('amavasya')) list.push('Amavasya');
  if (tithi.includes('purnima')) list.push('Purnima');
  if (tithi.includes('chaturthi')) list.push(paksha.includes('krishna') ? 'Sankashti Chaturthi' : 'Vinayaka Chaturthi');
  if (tithi.includes('ashtami') && paksha.includes('krishna')) list.push('Kalashtami');
  if (tithi.includes('navami')) list.push('Navami Vrat');
  if (tithi.includes('saptami')) list.push('Saptami Vrat');
  if (tithi.includes('panchami')) list.push('Panchami Vrat');
  if (tithi.includes('dwadashi') || tithi.includes('dwadsi')) list.push('Dwadashi Parana');

  if (nakshatra.includes('shravana')) list.push('Shravana Nakshatra Vrat');
  if (nakshatra.includes('rohini')) list.push('Rohini Nakshatra Puja');
  if (nakshatra.includes('pushya')) list.push('Pushya Yoga Observance');
  if (nakshatra.includes('moola') || nakshatra.includes('mula')) list.push('Moola Nakshatra Shanti');

  if (weekday === 1) list.push('Somvar Vrat');
  if (weekday === 2) list.push('Mangalvar Vrat');
  if (weekday === 4) list.push('Guruvar Vrat');
  if (weekday === 5) list.push('Shukravar Vrat');
  if (weekday === 6) list.push('Shani Vrat');

  return uniqNames(list);
};

const getLocalDateString = () => {
  const now = new Date();
  return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;
};

const DEFAULT_LAT = 28.6139;
const DEFAULT_LON = 77.2090;

const formatTime12 = (value?: string) => {
  const raw = (value || '').trim();
  if (!raw || !raw.includes(':')) return '--:--';
  const [hStr, mStr] = raw.split(':');
  const h = Number(hStr);
  const m = Number(mStr);
  if (Number.isNaN(h) || Number.isNaN(m)) return raw;
  const suffix = h >= 12 ? 'PM' : 'AM';
  const hour12 = ((h + 11) % 12) + 1;
  return `${String(hour12).padStart(2, '0')}:${String(m).padStart(2, '0')} ${suffix}`;
};

const formatTime24 = (value?: string) => {
  const raw = (value || '').trim();
  if (!raw || !raw.includes(':')) return '--:--';
  const [hStr, mStr] = raw.split(':');
  const h = Number(hStr);
  const m = Number(mStr);
  if (Number.isNaN(h) || Number.isNaN(m)) return raw;
  return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}`;
};

const MONTHS = ['Chaitra', 'Vaishakha', 'Jyeshtha', 'Ashadha', 'Shravana', 'Bhadrapada', 'Ashwin', 'Kartik', 'Margashirsha', 'Pausha', 'Magha', 'Phalguna'];
const MONTHS_HI: Record<string, string> = {
  Chaitra: 'चैत्र', Vaishakha: 'वैशाख', Jyeshtha: 'ज्येष्ठ', Ashadha: 'आषाढ़',
  Shravana: 'श्रावण', Bhadrapada: 'भाद्रपद', Ashwin: 'आश्विन', Kartik: 'कार्तिक',
  Margashirsha: 'मार्गशीर्ष', Pausha: 'पौष', Magha: 'माघ', Phalguna: 'फाल्गुन',
};
const SIGN_HI: Record<string, string> = {
  Aries: 'मेष', Taurus: 'वृषभ', Gemini: 'मिथुन', Cancer: 'कर्क', Leo: 'सिंह', Virgo: 'कन्या',
  Libra: 'तुला', Scorpio: 'वृश्चिक', Sagittarius: 'धनु', Capricorn: 'मकर', Aquarius: 'कुंभ', Pisces: 'मीन',
};
const VAAR_HI: Record<string, string> = {
  Ravivara: 'रविवार', Somavara: 'सोमवार', Mangalavara: 'मंगलवार', Budhawara: 'बुधवार',
  Guruvara: 'गुरुवार', Shukravara: 'शुक्रवार', Shanivara: 'शनिवार',
  Ravivar: 'रविवार', Somvar: 'सोमवार', Mangalvar: 'मंगलवार', Budhvar: 'बुधवार',
  Guruvar: 'गुरुवार', Shukravar: 'शुक्रवार', Shanivar: 'शनिवार',
  Sunday: 'रविवार', Monday: 'सोमवार', Tuesday: 'मंगलवार', Wednesday: 'बुधवार',
  Thursday: 'गुरुवार', Friday: 'शुक्रवार', Saturday: 'शनिवार',
};
const TITHI_HI: Record<string, string> = {
  Pratipada: 'प्रतिपदा', Dwitiya: 'द्वितीया', Tritiya: 'तृतीया', Chaturthi: 'चतुर्थी',
  Panchami: 'पंचमी', Shashthi: 'षष्ठी', Saptami: 'सप्तमी', Ashtami: 'अष्टमी',
  Navami: 'नवमी', Dashami: 'दशमी', Ekadashi: 'एकादशी', Dwadashi: 'द्वादशी',
  Trayodashi: 'त्रयोदशी', Chaturdashi: 'चतुर्दशी', Purnima: 'पूर्णिमा', Amavasya: 'अमावस्या',
};
const NAKSHATRA_HI: Record<string, string> = {
  Ashwini: 'अश्विनी', Bharani: 'भरणी', Krittika: 'कृत्तिका', Rohini: 'रोहिणी',
  Mrigashira: 'मृगशिरा', Ardra: 'आर्द्रा', Punarvasu: 'पुनर्वसु', Pushya: 'पुष्य',
  Ashlesha: 'आश्लेषा', Magha: 'मघा', 'Purva Phalguni': 'पूर्वा फाल्गुनी', 'Uttara Phalguni': 'उत्तरा फाल्गुनी',
  Hasta: 'हस्त', Chitra: 'चित्रा', Swati: 'स्वाति', Vishakha: 'विशाखा',
  Anuradha: 'अनुराधा', Jyeshtha: 'ज्येष्ठा', Moola: 'मूल', 'Purva Ashadha': 'पूर्वाषाढ़ा',
  'Uttara Ashadha': 'उत्तराषाढ़ा', Shravana: 'श्रवण', Dhanishta: 'धनिष्ठा', Shatabhisha: 'शतभिषा',
  'Purva Bhadrapada': 'पूर्वा भाद्रपदा', 'Uttara Bhadrapada': 'उत्तरा भाद्रपदा', Revati: 'रेवती',
};
const YOGA_HI: Record<string, string> = {
  Vishkambha: 'विष्कम्भ', Priti: 'प्रीति', Ayushman: 'आयुष्मान', Saubhagya: 'सौभाग्य',
  Shobhana: 'शोभन', Atiganda: 'अतिगण्ड', Sukarma: 'सुकर्मा', Dhriti: 'धृति',
  Shoola: 'शूल', Ganda: 'गण्ड', Vriddhi: 'वृद्धि', Dhruva: 'ध्रुव',
  Vyaghata: 'व्याघात', Harshana: 'हर्षण', Vajra: 'वज्र', Siddhi: 'सिद्धि',
  Vyatipata: 'व्यतीपात', Variyan: 'वरीयान', Parigha: 'परिघ', Shiva: 'शिव',
  Siddha: 'सिद्ध', Sadhya: 'साध्य', Shubha: 'शुभ', Shukla: 'शुक्ल',
  Brahma: 'ब्रह्म', Indra: 'इन्द्र', Vaidhriti: 'वैधृति',
};
const KARANA_HI: Record<string, string> = {
  Bava: 'बव', Balava: 'बालव', Kaulava: 'कौलव', Taitila: 'तैतिल',
  Garaja: 'गरज', Vanija: 'वणिज', Vishti: 'विष्टि', Shakuni: 'शकुनि',
  Chatushpada: 'चतुष्पद', Naga: 'नाग', Kimstughna: 'किंस्तुघ्न',
};
const PAKSHA_HI: Record<string, string> = {
  Shukla: 'शुक्ल', Krishna: 'कृष्ण',
};
const FESTIVAL_HI: Record<string, string> = {
  'Pradosh Vrat': 'प्रदोष व्रत', 'Guruvar Vrat': 'गुरुवार व्रत', 'Masik Shivaratri': 'मासिक शिवरात्रि',
  'Amavasya': 'अमावस्या', 'Shukravar Vrat': 'शुक्रवार व्रत', 'Shani Vrat': 'शनि व्रत',
  'Akshaya Tritiya': 'अक्षय तृतीया', 'Parashurama Jayanti': 'परशुराम जयंती',
  'Rohini Nakshatra Puja': 'रोहिणी नक्षत्र पूजा', 'Somvar Vrat': 'सोमवार व्रत',
  'Mangalvar Vrat': 'मंगलवार व्रत', 'Panchami Vrat': 'पंचमी व्रत', 'Guruvar Vrat': 'गुरुवार व्रत',
  'Saptami Vrat': 'सप्तमी व्रत', 'Navami Vrat': 'नवमी व्रत',
  'Vivah Panchami': 'विवाह पंचमी', 'Surya Saptami': 'सूर्य सप्तमी',
  'Pushya Yoga Observance': 'पुष्य योग अनुष्ठान', 'Shukravar Vrat': 'शुक्रवार व्रत',
  'Ekadashi Vrat': 'एकादशी व्रत', 'Purnima': 'पूर्णिमा',
  'Sankashti Chaturthi': 'संकष्टी चतुर्थी', 'Vinayaka Chaturthi': 'विनायक चतुर्थी',
  'Kalashtami': 'कालाष्टमी', 'Dwadashi Parana': 'द्वादशी पारण',
  'Shravana Nakshatra Vrat': 'श्रवण नक्षत्र व्रत', 'Moola Nakshatra Shanti': 'मूल नक्षत्र शांति',
  'Hanuman Jayanti': 'हनुमान जयंती', 'Chaitra Purnima': 'चैत्र पूर्णिमा',
};
const SAMVATSARA_60 = ['Prabhava', 'Vibhava', 'Shukla', 'Pramoda', 'Prajapati', 'Angirasa', 'Shrimukha', 'Bhava', 'Yuva', 'Dhata', 'Ishvara', 'Bahudhanya', 'Pramathi', 'Vikrama', 'Vrisha', 'Chitrabhanu', 'Svabhanu', 'Tarana', 'Parthiva', 'Vyaya', 'Sarvajit', 'Sarvadhari', 'Virodhi', 'Vikruti', 'Khara', 'Nandana', 'Vijaya', 'Jaya', 'Manmatha', 'Durmukha', 'Hevilambi', 'Vilambi', 'Vikari', 'Sharvari', 'Plava', 'Shubhakrith', 'Shobhakrith', 'Krodhi', 'Vishvavasu', 'Parabhava', 'Plavanga', 'Kilaka', 'Saumya', 'Sadharana', 'Virodhikrith', 'Paridhavi', 'Pramadicha', 'Ananda', 'Rakshasa', 'Nala', 'Pingala', 'Kalayukti', 'Siddharthi', 'Raudra', 'Durmati', 'Dundubhi', 'Rudhirodgari', 'Raktakshi', 'Krodhana', 'Akshaya'];
const SAMVATSARA_60_HI = ['प्रभव', 'विभव', 'शुक्ल', 'प्रमोद', 'प्रजापति', 'अंगिरा', 'श्रीमुख', 'भव', 'युवा', 'धाता', 'ईश्वर', 'बहुधान्य', 'प्रमाथी', 'विक्रम', 'वृष', 'चित्रभानु', 'स्वभानु', 'तारण', 'पार्थिव', 'व्यय', 'सर्वजित', 'सर्वधारी', 'विरोधी', 'विकृति', 'खर', 'नन्दन', 'विजय', 'जय', 'मन्मथ', 'दुर्मुख', 'हेविलम्बी', 'विलम्बी', 'विकारी', 'शार्वरी', 'प्लव', 'शुभकृत', 'शोभकृत', 'क्रोधी', 'विश्वावसु', 'पराभव', 'प्लवंग', 'कीलक', 'सौम्य', 'साधारण', 'विरोधिकृत', 'परिधावी', 'प्रमादीच', 'आनन्द', 'राक्षस', 'नल', 'पिंगल', 'कालयुक्ति', 'सिद्धार्थी', 'रौद्र', 'दुर्मति', 'दुन्दुभि', 'रुधिरोद्गारी', 'रक्ताक्षी', 'क्रोधन', 'अक्षय'];
const samvatsaraName = (year?: number, offset = 12, lang = 'en') => {
  if (!year) return '';
  const idx = ((year + offset) % 60 + 60) % 60;
  return lang === 'hi' ? SAMVATSARA_60_HI[idx] : SAMVATSARA_60[idx];
};

const compactLine = (value?: string) => {
  const text = (value || '').replace(/\s+/g, ' ').trim();
  if (!text) return 'Guidance will update shortly.';
  const sentence = text.split(/(?<=[.!?])\s+/)[0] || text;
  return sentence.length > 95 ? `${sentence.slice(0, 92).trim()}...` : sentence;
};

const hasMeaningfulSections = (sections?: HoroscopeSections) => {
  if (!sections) return false;
  return ['general', 'love', 'career', 'finance', 'health'].some((k) => {
    const value = (sections[k as keyof HoroscopeSections] || '').trim();
    return value.length >= 15;
  });
};

export default function Features() {
  const sectionRef = useRef<HTMLDivElement>(null);
  const { language } = useTranslation();
  const l = (en: string, hi: string) => (language === 'hi' ? hi : en);

  const [lightbox, setLightbox] = useState<{ file: string; label: string } | null>(null);
  const [horoscopeTab, setHoroscopeTab] = useState<'daily' | 'weekly' | 'monthly' | 'yearly'>('daily');
  const [horoscopeSign, setHoroscopeSign] = useState<string>('aries');
  const [horoscopeLoading, setHoroscopeLoading] = useState<boolean>(false);
  const [horoscopeData, setHoroscopeData] = useState<HoroscopeData | null>(null);
  const [panchangTab, setPanchangTab] = useState<'12' | '24' | '24+'>('12');
  const [panchangLoading, setPanchangLoading] = useState<boolean>(false);
  const [panchangData, setPanchangData] = useState<PanchangData | null>(null);
  const [vedicClockMode, setVedicClockMode] = useState<'30' | '60'>('30');
  const [now, setNow] = useState<Date>(new Date());
  const [upcomingFestivals, setUpcomingFestivals] = useState<FestivalRow[]>([]);
  const [festivalsLoading, setFestivalsLoading] = useState<boolean>(false);
  const [latitude, setLatitude] = useState<number>(DEFAULT_LAT);
  const [longitude, setLongitude] = useState<number>(DEFAULT_LON);
  const [locationLabel, setLocationLabel] = useState<string>('New Delhi, India');
  const [locSearchOpen, setLocSearchOpen] = useState(false);
  const [locSearchQuery, setLocSearchQuery] = useState('');
  const [locSearchResults, setLocSearchResults] = useState<Array<{ name: string; lat: number; lon: number }>>([]);
  const [locSearchLoading, setLocSearchLoading] = useState(false);
  const [openFaq, setOpenFaq] = useState<number | null>(null);
  const locSearchRef = useRef<HTMLDivElement>(null);
  const locSearchTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Location search: debounced geocode
  const handleLocSearch = (query: string) => {
    setLocSearchQuery(query);
    if (locSearchTimer.current) clearTimeout(locSearchTimer.current);
    if (query.trim().length < 2) { setLocSearchResults([]); return; }
    locSearchTimer.current = setTimeout(async () => {
      setLocSearchLoading(true);
      try {
        const results = await api.get(`/api/kundli/geocode?query=${encodeURIComponent(query.trim())}`);
        setLocSearchResults(Array.isArray(results) ? results.slice(0, 5) : []);
      } catch { setLocSearchResults([]); }
      setLocSearchLoading(false);
    }, 300);
  };

  const selectLocation = (result: { name: string; lat: number; lon: number }) => {
    const shortName = result.name.split(',').slice(0, 2).join(',').trim();
    setLocationLabel(shortName);
    setLatitude(result.lat);
    setLongitude(result.lon);
    setLocSearchOpen(false);
    setLocSearchQuery('');
    setLocSearchResults([]);
  };

  // Close search dropdown on outside click
  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (locSearchRef.current && !locSearchRef.current.contains(e.target as Node)) setLocSearchOpen(false);
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  useEffect(() => {
    if (!lightbox) return;
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') setLightbox(null); };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [lightbox]);

  useEffect(() => {
    let cancelled = false;
    const loadHoroscope = async () => {
      setHoroscopeLoading(true);
      try {
        const qs = horoscopeTab === 'daily' ? `?sign=${horoscopeSign}&date=${getLocalDateString()}` : `?sign=${horoscopeSign}`;
        const data = await api.get(`/api/horoscope/${horoscopeTab}${qs}`);
        if (!cancelled && data && hasMeaningfulSections(data.sections)) {
          setHoroscopeData(data);
          return;
        }
        // Fallback for empty/monthly-yearly missing content (or older backend without endpoints)
        const fallback = await api.get(`/api/horoscope/weekly?sign=${horoscopeSign}`);
        if (!cancelled && fallback) setHoroscopeData(fallback);
      } catch {
        try {
          const fallback = await api.get(`/api/horoscope/weekly?sign=${horoscopeSign}`);
          if (!cancelled && fallback) setHoroscopeData(fallback);
        } catch {
          if (!cancelled) setHoroscopeData(null);
        }
      } finally {
        if (!cancelled) setHoroscopeLoading(false);
      }
    };
    loadHoroscope();
    return () => { cancelled = true; };
  }, [horoscopeSign, horoscopeTab]);

  useEffect(() => {
    const timer = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    if (!navigator.geolocation) return;
    navigator.geolocation.getCurrentPosition(
      async (pos) => {
        const lat = Number(pos.coords.latitude.toFixed(4));
        const lon = Number(pos.coords.longitude.toFixed(4));
        setLatitude(lat);
        setLongitude(lon);
        try {
          const r = await fetch(`https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${lat}&lon=${lon}`, {
            headers: { Accept: 'application/json' },
          });
          if (!r.ok) return;
          const j: any = await r.json();
          const a = j?.address || {};
          const city = a.city || a.town || a.village || a.county || a.state_district || '';
          const state = a.state || '';
          const country = a.country || '';
          const parts = [city, state, country].filter(Boolean);
          if (parts.length > 0) setLocationLabel(parts.join(', '));
        } catch {
          setLocationLabel(`${lat.toFixed(2)}, ${lon.toFixed(2)}`);
        }
      },
      () => {},
      { timeout: 10000, maximumAge: 300000, enableHighAccuracy: false },
    );
  }, []);

  const localDateKey = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;

  useEffect(() => {
    let cancelled = false;
    const loadFestivals = async () => {
      setFestivalsLoading(true);
      try {
        const year = now.getFullYear();
        const month = now.getMonth() + 1;
        const curRes = await api.get(`/api/panchang/month?month=${month}&year=${year}&latitude=${latitude}&longitude=${longitude}`);
        const dayRows = [...(curRes?.days || [])];
        const today = localDateKey;
        const todayDt = new Date(`${today}T12:00:00`);
        const monthEndDt = new Date(year, month, 0, 12, 0, 0);
        const seen = new Set<string>();
        let parsed: FestivalRow[] = [];

        for (const d of dayRows) {
          const dStr = String(d?.date || '');
          if (!dStr) continue;
          const dObj = new Date(`${dStr}T12:00:00`);
          if (dObj < todayDt || dObj > monthEndDt) continue;
          const items = [
            ...(Array.isArray(d?.festivals) ? d.festivals : []),
            ...generateObservancesFromDay({ date: dStr, tithi: d?.tithi, nakshatra: d?.nakshatra, paksha: d?.paksha }),
          ];
          for (const rawName of items) {
            const name = String(rawName || '').trim();
            if (!name) continue;
            const key = `${dStr}::${name.toLowerCase()}`;
            if (seen.has(key)) continue;
            seen.add(key);
            parsed.push({ name, date: dStr });
          }
        }

        parsed.sort((a, b) => {
          const dc = String(a.date).localeCompare(String(b.date));
          if (dc !== 0) return dc;
          return String(a.name).localeCompare(String(b.name));
        });

        // Merge source: yearly festival table (filtered to current month only)
        try {
          const fallback = await api.get(`/api/festivals?year=${year}`);
          const fallbackRows: FestivalRow[] = Array.isArray(fallback)
            ? fallback
            : Array.isArray((fallback as any)?.festivals)
              ? (fallback as any).festivals
              : Array.isArray((fallback as any)?.data?.festivals)
                ? (fallback as any).data.festivals
                : [];
          const seen = new Set(parsed.map((f) => `${String(f.date)}::${String(f.name).toLowerCase()}`));
          for (const f of fallbackRows) {
            const dStr = String(f?.date || '').slice(0, 10);
            const name = String(f?.name || '').trim();
            if (!dStr || !name) continue;
            const dObj = new Date(`${dStr}T12:00:00`);
            if (Number.isNaN(dObj.getTime()) || dObj < todayDt || dObj > monthEndDt) continue;
            if ((dObj.getMonth() + 1) !== month) continue;
            const key = `${dStr}::${name.toLowerCase()}`;
            if (seen.has(key)) continue;
            seen.add(key);
            parsed.push({ name, date: dStr, description: f.description, rituals: f.rituals });
          }
        } catch {
          // Keep whatever monthly-derived list we already have.
        }

        parsed = parsed.sort((a, b) => {
          const dc = String(a.date).localeCompare(String(b.date));
          if (dc !== 0) return dc;
          return String(a.name).localeCompare(String(b.name));
        });

        if (!cancelled) setUpcomingFestivals(parsed);
      } catch {
        if (!cancelled) setUpcomingFestivals([]);
      } finally {
        if (!cancelled) setFestivalsLoading(false);
      }
    };
    loadFestivals();
    return () => { cancelled = true; };
  }, [localDateKey, latitude, longitude]);

  useEffect(() => {
    let cancelled = false;
    const loadPanchang = async () => {
      setPanchangLoading(true);
      try {
        const date = getLocalDateString();
        const data = await api.get(`/api/panchang?date=${date}&latitude=${latitude}&longitude=${longitude}`);
        if (!cancelled && data) setPanchangData(data);
      } catch {
        if (!cancelled) setPanchangData(null);
      } finally {
        if (!cancelled) setPanchangLoading(false);
      }
    };
    loadPanchang();
    return () => { cancelled = true; };
  }, [latitude, longitude]);

  const purnimantaMonth = panchangData?.hindu_calendar?.maas || '--';
  const monthIdx = MONTHS.indexOf(purnimantaMonth);
  const amantaMonth = monthIdx >= 0 ? MONTHS[(monthIdx + 11) % 12] : '--';
  const gate = typeof panchangData?.sun_longitude === 'number' ? Math.floor((panchangData.sun_longitude % 30 + 30) % 30) + 1 : '--';
  const shaka = panchangData?.hindu_calendar?.shaka_samvat;
  const vikram = panchangData?.hindu_calendar?.vikram_samvat;
  const gujarati = typeof vikram === 'number' ? vikram - 1 : undefined;
  const weekday = panchangData?.vaar?.name || panchangData?.vaar?.english || '--';
  const weekdayDisplay = language === 'hi' ? (VAAR_HI[weekday] || weekday) : weekday;
  const sunSignDisplay = language === 'hi' ? (SIGN_HI[panchangData?.sun_sign || ''] || (panchangData?.sun_sign || '--')) : (panchangData?.sun_sign || '--');
  const moonSignDisplay = language === 'hi' ? (SIGN_HI[panchangData?.moon_sign || ''] || (panchangData?.moon_sign || '--')) : (panchangData?.moon_sign || '--');
  const amantaDisplay = language === 'hi' ? (MONTHS_HI[amantaMonth] || amantaMonth) : amantaMonth;
  const purnimantaDisplay = language === 'hi' ? (MONTHS_HI[purnimantaMonth] || purnimantaMonth) : purnimantaMonth;

  const tf = (value?: string) => (panchangTab === '12' ? formatTime12(value) : formatTime24(value));
  const hi = language === 'hi';
  const thi = (name: string, map: Record<string, string>) => hi ? (map[name] || name) : name;

  // Format kaal/muhurat period as "start to end"
  const tfPeriod = (period?: { start?: string; end?: string }) => {
    if (!period?.start || !period?.end) return l('None', 'कोई नहीं');
    return `${tf(period.start)} ${l('to', 'से')} ${tf(period.end)}`;
  };

  // Moon sign with transition time
  const moonSignFull = (() => {
    const base = moonSignDisplay || '--';
    const trans = panchangData?.moon_sign_transition;
    if (trans?.time) return `${base} ${l('upto', 'तक')} ${tf(trans.time)}`;
    return base;
  })();

  // Extra lines for 24+ mode
  const panchangExtraLines: Array<{ label: string; value: string }> = [
    { label: l('Rahu Kalam', 'राहु काल'), value: tfPeriod(panchangData?.rahu_kaal) },
    { label: l('Gulikai Kalam', 'गुलिक काल'), value: tfPeriod(panchangData?.gulika_kaal) },
    { label: l('Yamaganda', 'यमगण्ड'), value: tfPeriod(panchangData?.yamaganda) },
    { label: l('Abhijit', 'अभिजित'), value: tfPeriod(panchangData?.abhijit_muhurat) },
    { label: l('Dur Muhurtam', 'दुर्मुहूर्त'), value: tfPeriod(panchangData?.dur_muhurtam) },
    { label: l('Amrit Kalam', 'अमृत काल'), value: panchangData?.amrit_siddhi?.active ? tfPeriod(panchangData.amrit_siddhi) : l('None', 'कोई नहीं') },
    { label: l('Varjyam', 'वर्ज्यम'), value: tfPeriod(panchangData?.varjyam) },
  ];

  const panchangBaseLines: Array<{ label: string; value: string }> = [
    { label: l('Sunrise', 'सूर्योदय'), value: tf(panchangData?.sunrise) },
    { label: l('Sunset', 'सूर्यास्त'), value: tf(panchangData?.sunset) },
    { label: l('Moonrise', 'चंद्रोदय'), value: tf(panchangData?.moonrise) || '--' },
    { label: l('Moonset', 'चंद्रास्त'), value: tf(panchangData?.moonset) || '--' },
    { label: l('Tithi', 'तिथि'), value: `${thi(panchangData?.tithi?.name || '--', TITHI_HI)}${panchangData?.tithi?.end_time ? ` ${l('upto', 'तक')} ${tf(panchangData?.tithi?.end_time)}` : ''}` },
    { label: l('Nakshatra', 'नक्षत्र'), value: `${thi(panchangData?.nakshatra?.name || '--', NAKSHATRA_HI)}${panchangData?.nakshatra?.end_time ? ` ${l('upto', 'तक')} ${tf(panchangData?.nakshatra?.end_time)}` : ''}` },
    { label: l('Yoga', 'योग'), value: `${thi(panchangData?.yoga?.name || '--', YOGA_HI)}${panchangData?.yoga?.end_time ? ` ${l('upto', 'तक')} ${tf(panchangData?.yoga?.end_time)}` : ''}` },
    { label: l('Karana', 'करण'), value: `${thi(panchangData?.karana?.name || '--', KARANA_HI)}${panchangData?.karana?.end_time ? ` ${l('upto', 'तक')} ${tf(panchangData?.karana?.end_time)}` : ''}` },
    { label: l('Karana', 'करण'), value: `${thi(panchangData?.karana?.second_karana || '--', KARANA_HI)}${panchangData?.karana?.second_karana_end_time ? ` ${l('upto', 'तक')} ${tf(panchangData?.karana?.second_karana_end_time)}` : ''}` },
    { label: l('Paksha', 'पक्ष'), value: `${thi(panchangData?.tithi?.paksha || '--', PAKSHA_HI)} ${l('Paksha', 'पक्ष')}` },
    { label: l('Weekday', 'वार'), value: weekdayDisplay },
    { label: l('Amanta Month', 'अमांत महीना'), value: amantaDisplay },
    { label: l('Purnimanta Month', 'पूर्णिमांत महीना'), value: purnimantaDisplay },
    { label: l('Moonsign', 'चंद्र राशि'), value: moonSignFull },
    { label: l('Sunsign', 'सूर्य राशि'), value: sunSignDisplay },
    { label: l('Pravishte/Gate', 'प्रविष्टे/गेट'), value: String(gate) },
    { label: l('Shaka Samvat', 'शक संवत'), value: `${shaka || '--'}${shaka ? ` ${samvatsaraName(shaka, 11, language)}` : ''}` },
    { label: l('Vikram Samvat', 'विक्रम संवत'), value: `${vikram || '--'}${vikram ? ` ${samvatsaraName(vikram, 9, language)}` : ''}` },
    { label: l('Gujarati Samvat', 'गुजराती संवत'), value: `${gujarati || '--'}${gujarati ? ` ${samvatsaraName(gujarati, 8, language)}` : ''}` },
  ];

  const visiblePanchangLines = panchangTab === '24+' ? [...panchangBaseLines, ...panchangExtraLines] : panchangBaseLines;

  const parseHmToSec = (v?: string) => {
    const raw = (v || '').trim();
    if (!raw.includes(':')) return null;
    const [h, m] = raw.split(':').map(Number);
    if (Number.isNaN(h) || Number.isNaN(m)) return null;
    return (h * 3600) + (m * 60);
  };
  const sunriseSec = parseHmToSec(panchangData?.sunrise);
  const sunsetSec = parseHmToSec(panchangData?.sunset);
  const nowSec = now.getHours() * 3600 + now.getMinutes() * 60 + now.getSeconds();

  let dayDuration = 43200;
  if (sunriseSec !== null && sunsetSec !== null) {
    dayDuration = sunsetSec >= sunriseSec ? (sunsetSec - sunriseSec) : (86400 - sunriseSec + sunsetSec);
  }
  const nightDuration = Math.max(1, 86400 - dayDuration);
  let elapsedFromSunrise = 0;
  if (sunriseSec !== null) {
    elapsedFromSunrise = nowSec >= sunriseSec ? (nowSec - sunriseSec) : (86400 - sunriseSec + nowSec);
  }
  const isDaytime = elapsedFromSunrise <= dayDuration;

  const vedicGhatiFloat = (() => {
    if (vedicClockMode === '30') {
      if (isDaytime) return (elapsedFromSunrise / Math.max(1, dayDuration)) * 30;
      return 30 + ((elapsedFromSunrise - dayDuration) / nightDuration) * 30;
    }
    const ghatiSec = 86400 / 60;
    return elapsedFromSunrise / ghatiSec;
  })();
  const vedicGhati = Math.floor(Math.max(0, vedicGhatiFloat));
  const vedicPalFloat = (Math.max(0, vedicGhatiFloat) - vedicGhati) * 60;
  const vedicPal = Math.floor(vedicPalFloat);
  const vedicVipal = Math.floor((vedicPalFloat - vedicPal) * 60);
  const vedicTimeStr = `${String(vedicGhati).padStart(2, '0')}:${String(vedicPal).padStart(2, '0')}:${String(vedicVipal).padStart(2, '0')}`;

  const features = [
    {
      image: '/images/features/feature-lalkitab.png',
      title: l('Lal Kitab — Complete System', 'लाल किताब — पूर्ण सिस्टम'),
      subtitle: l('ONLY HERE', 'केवल यहाँ'),
      desc: l('Complete Lal Kitab toolkit with Nishaniyan Matcher, Chandra Chalana 43-day protocol, Remedy Tracker with streaks, Teva classification, Masnui Grah (artificial planets), Karmic Debt (Rin) analysis, Sleeping & Kayam planets, Annual Gochar — the most comprehensive Lal Kitab system available online.', 'निशानियां मैचर, चंद्र चालना 43-दिन प्रोटोकॉल, रेमेडी ट्रैकर, तेवा वर्गीकरण, मसनूई ग्रह, कर्मिक ऋण विश्लेषण, सोया और कायम ग्रह, वार्षिक गोचर — ऑनलाइन सबसे व्यापक लाल किताब प्रणाली।'),
      badge: l('EXCLUSIVE', 'विशेष'),
    },
    {
      image: '/images/features/feature-kundli.jpg',
      imagePosition: 'center top',
      imageFilter: 'sepia(0.15) brightness(0.95) contrast(1.05)',
      title: l('Kundli — 3 Vedic Systems', 'कुंडली — 3 वैदिक सिस्टम'),
      subtitle: l('Unmatched Depth', 'बेजोड़ गहराई'),
      desc: l('Parashari, Jaimini & KP System in one place. Ashtakvarga, Shadbala, Dasha timeline, Varshphal, Kundli Milan, 10+ Divisional Charts (D9 Navamsha to D60), Dosha analysis, General Remedies — 12+ deep-analysis modules, not just a birth chart.', 'पाराशरी, जैमिनी और केपी प्रणाली एक जगह। अष्टकवर्ग, षड्बल, दशा समयरेखा, वर्षफल, कुंडली मिलान, 10+ वर्ग चार्ट, दोष विश्लेषण — 12+ गहन विश्लेषण मॉड्यूल।'),
      badge: l('UNMATCHED DEPTH', 'बेजोड़ गहराई'),
    },
    {
      image: '/images/features/feature-horoscope.jpg',
      imagePosition: 'center center',
      imageFilter: 'sepia(0.15) brightness(0.95) contrast(1.05)',
      title: l('Horoscope — Daily + Predictive', 'राशिफल — दैनिक + प्रेडिक्टिव'),
      subtitle: l('AI Powered', 'एआई समर्थित'),
      desc: l(
        'Daily, weekly, monthly & yearly horoscope for all 12 signs. Sign-based forecasts enriched with real planetary transit context, ruling planet dignity, and seasonal timing — helping you plan each day with cosmic awareness.',
        'सभी 12 राशियों के लिए दैनिक, साप्ताहिक, मासिक और वार्षिक राशिफल। वास्तविक ग्रह गोचर संदर्भ, शासक ग्रह गरिमा और मौसमी समय से समृद्ध — ब्रह्मांडीय जागरूकता के साथ हर दिन की योजना बनाएं।'
      ),
      badge: l('SIGN-BASED', 'राशि-आधारित'),
    },
    {
      image: '/images/features/feature-panchang.jpg',
      title: l('Live Panchang', 'लाइव पंचांग'),
      subtitle: l('Location-Aware', 'लोकेशन-आधारित'),
      desc: l('Real-time Tithi, Nakshatra, Yoga, Karana with exact end times. 12+ Muhurat windows (Abhijit, Brahma, Vijaya, Dur Muhurtam, Varjyam), Rahu Kaal, Choghadiya, Hora table, Lagna transitions, Hindu calendar with Samvat — all for YOUR exact location.', 'सटीक अंत समय के साथ तिथि, नक्षत्र, योग, करण। 12+ मुहूर्त (अभिजित, ब्रह्म, विजय), राहु काल, चौघड़िया, होरा, लग्न, संवत सहित हिंदू कैलेंडर — आपके सटीक स्थान के लिए।'),
      badge: l('LOCATION-AWARE', 'लोकेशन-आधारित'),
    },
    {
      image: '/images/features/feature-numerology.jpg',
      imagePosition: 'center center',
      imageFilter: 'sepia(0.15) brightness(0.95) contrast(1.05)',
      title: l('Numerology — Name + Mobile', 'अंकशास्त्र — नाम + मोबाइल'),
      subtitle: l('Dual Engine', 'डुअल इंजन'),
      desc: l(
        'Pythagorean + Chaldean name numerology, mobile number vibration analysis, Lo Shu & Vedic grids, vehicle number & property address numerology. Life Path, Expression, Soul Urge numbers with lucky colors, career guidance, and compatibility insights.',
        'पाइथागोरियन + कैल्डियन नाम अंक शास्त्र, मोबाइल नंबर कंपन विश्लेषण, लो शू और वैदिक ग्रिड, वाहन नंबर और संपत्ति पता अंक शास्त्र। जीवन पथ, भाग्यांक, आत्मांक संख्याएं।'
      ),
      badge: l('DUAL ENGINE', 'डुअल इंजन'),
    },
    {
      image: '/images/features/feature-vastu.jpg',
      imagePosition: 'center center',
      imageFilter: 'sepia(0.15) brightness(0.95) contrast(1.05)',
      title: l('Vastu Shastra Analyzer', 'वास्तु शास्त्र विश्लेषक'),
      subtitle: l('Pro', 'प्रो'),
      desc: l(
        '45-Devta Vastu Purusha Mandala scoring with zone-wise energy mapping. 32-entrance Pada analysis, direction optimization for every room, metal remedies (copper, iron, silver, gold), color therapy — for homes and offices.',
        '45-देवता वास्तु पुरुष मंडल स्कोरिंग। 32-प्रवेश पद विश्लेषण, हर कमरे के लिए दिशा अनुकूलन, धातु उपाय (तांबा, लोहा, चांदी, सोना), रंग चिकित्सा — घरों और कार्यालयों के लिए।'
      ),
      badge: l('MANDALA-BASED', 'मंडल-आधारित'),
    },
  ];


  useEffect(() => {
    if (gsap.globalTimeline.timeScale() === 0) return;
    const ctx = gsap.context(() => {
      gsap.fromTo('.features-title', { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 0.8, ease: 'power3.out', scrollTrigger: { trigger: sectionRef.current, start: 'top 80%' } });
      gsap.fromTo('.feature-card', { y: 80, opacity: 0 }, { y: 0, opacity: 1, duration: 0.8, stagger: 0.1, ease: 'power3.out', scrollTrigger: { trigger: sectionRef.current, start: 'top 70%' } });
    }, sectionRef);
    return () => ctx.revert();
  }, []);

  return (
    <>
    <section ref={sectionRef} id="features" className="relative pt-4 pb-24 bg-background">

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Horoscope (Compact) */}
        <div className="features-title mb-12">
          <Heading as={2} variant={2} className="text-sacred-gold-dark mb-6 leading-[1.1] text-center">
            {l('Horoscope', 'राशिफल')}
          </Heading>
          <div className="max-w-full mx-auto text-lg text-gray-600 leading-relaxed mb-6 text-center">
            <p>{l('Most horoscope apps use generic sun-sign text and repeated templates.', 'अधिकांश राशिफल ऐप सामान्य सन-साइन टेक्स्ट और दोहराए गए टेम्पलेट का उपयोग करते हैं।')}</p>
            <p><strong className="text-sacred-gold-dark">{l('Astro Rattan aligns sign forecasts with real planetary context and period logic', 'Astro Rattan वास्तविक ग्रह स्थिति और पीरियड लॉजिक के साथ राशिफल को संरेखित करता है')}</strong>{l(' — giving clearer daily, weekly, monthly, and yearly guidance.', ' — जिससे दैनिक, साप्ताहिक, मासिक और वार्षिक मार्गदर्शन अधिक स्पष्ट मिलता है।')}</p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {/* LEFT: 4x3 Sign Grid */}
            <div className="rounded-xl border border-sacred-gold/20 bg-transparent backdrop-blur-[1px] p-3">
              <div className="grid grid-cols-4 gap-2">
                {SIGNS.map((s) => (
                  <button
                    key={s.id}
                    onClick={() => setHoroscopeSign(s.id)}
                    className={`flex flex-col items-center gap-1.5 px-2 py-3 rounded-lg text-xs w-full border transition-all ${
                      horoscopeSign === s.id
                        ? 'bg-sacred-gold/[0.12] text-sacred-gold-dark border-sacred-gold/50 shadow-sm'
                        : 'text-muted-foreground border-transparent hover:bg-sacred-gold/10'
                    }`}
                  >
                    <img
                      src={`/images/zodiac-orange/zodiac-${s.id}-orange.png`}
                      alt={s.en}
                      className="w-10 h-10 object-contain"
                      loading="lazy"
                    />
                    <span className="font-medium">{language === 'hi' ? s.hi : s.en}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* RIGHT: Tabs + Prediction */}
            <div className="flex flex-col gap-3">
              <Tabs value={horoscopeTab} onValueChange={(v) => setHoroscopeTab(v as 'daily' | 'weekly' | 'monthly' | 'yearly')} className="w-full">
                <TabsList className="grid w-full grid-cols-4 h-auto p-1 bg-transparent border border-sacred-gold/20 rounded-xl">
                  {[
                    { id: 'daily', label: l('Daily', 'दैनिक'), icon: Sun },
                    { id: 'weekly', label: l('Weekly', 'साप्ताहिक'), icon: Calendar },
                    { id: 'monthly', label: l('Monthly', 'मासिक'), icon: Calendar },
                    { id: 'yearly', label: l('Yearly', 'वार्षिक'), icon: Calendar },
                  ].map(tab => (
                    <TabsTrigger key={tab.id} value={tab.id} className="flex-1 flex items-center justify-center gap-1.5 py-2 text-xs data-[state=active]:bg-sacred-gold data-[state=active]:text-white rounded-lg">
                      <tab.icon className="w-3.5 h-3.5" />
                      <span>{tab.label}</span>
                    </TabsTrigger>
                  ))}
                </TabsList>
              </Tabs>

              <div className="rounded-xl border border-sacred-gold/20 bg-sacred-gold/[0.02] p-4 flex-1">
                {horoscopeLoading ? (
                  <div className="h-full min-h-[160px] flex items-center justify-center text-muted-foreground">
                    <Loader2 className="w-5 h-5 animate-spin mr-2" />
                    <span>{l('Loading horoscope...', 'राशिफल लोड हो रहा है...')}</span>
                  </div>
                ) : (
                  <>
                    <div className="mb-3">
                      <p className="text-base font-semibold text-foreground">
                        {language === 'hi' ? (horoscopeData?.sign_hindi || '') : (horoscopeData?.sign || horoscopeSign).toString().replace(/^./, c => c.toUpperCase())}
                      </p>
                      <p className="text-xs text-muted-foreground">{horoscopeData?.dates || ''}</p>
                    </div>
                    <div className="space-y-1.5 text-sm text-foreground">
                      <p><span className="font-semibold text-sacred-gold-dark">{l('General', 'सामान्य')}:</span> {compactLine(horoscopeData?.sections?.general)}</p>
                      <p><span className="font-semibold text-sacred-gold-dark">{l('Love', 'प्रेम')}:</span> {compactLine(horoscopeData?.sections?.love)}</p>
                      <p><span className="font-semibold text-sacred-gold-dark">{l('Career', 'करियर')}:</span> {compactLine(horoscopeData?.sections?.career)}</p>
                      <p><span className="font-semibold text-sacred-gold-dark">{l('Health', 'स्वास्थ्य')}:</span> {compactLine(horoscopeData?.sections?.health)}</p>
                      <p><span className="font-semibold text-sacred-gold-dark">{l('Finance', 'वित्त')}:</span> {compactLine(horoscopeData?.sections?.finance)}</p>
                    </div>
                  </>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Section Header */}
        <div className="features-title mb-12">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-2" style={{ height: '620px' }}>
            <div className="w-full max-w-none h-full rounded-xl border border-sacred-gold/20 bg-transparent backdrop-blur-[1px] shadow-sm overflow-hidden flex flex-col">
              <div className="bg-sacred-gold-dark text-white px-3 py-2 text-[15px] font-semibold leading-tight">
                {l('Panchang for Today', 'आज का पंचांग')}
              </div>
              <div className="p-2.5 flex-1 overflow-hidden flex flex-col min-h-0">
                <div className="grid grid-cols-3 rounded-md bg-sacred-gold/8 p-1 mb-2.5 gap-1 shrink-0">
                  {(['12', '24', '24+'] as const).map((tab) => (
                    <button
                      key={tab}
                      type="button"
                      onClick={() => setPanchangTab(tab)}
                      className={`w-full px-2 py-1.5 text-[13px] rounded-sm transition-colors ${
                        panchangTab === tab ? 'bg-sacred-gold/25 text-sacred-gold-dark font-semibold' : 'text-muted-foreground'
                      }`}
                    >
                      {tab === '12' ? l('12 Hour', '12 घंटे') : tab === '24' ? l('24 Hour', '24 घंटे') : l('24 Plus', '24 प्लस')}
                    </button>
                  ))}
                </div>
                <div className="relative shrink-0" ref={locSearchRef}>
                  <div className="flex items-center gap-2">
                    <p className="text-[24px] font-semibold text-[#333]">{hi ? locationLabel.replace(', India', ', भारत').replace('New Delhi', 'नई दिल्ली').replace('Delhi', 'दिल्ली') : locationLabel}</p>
                    <button
                      type="button"
                      onClick={() => setLocSearchOpen(!locSearchOpen)}
                      className="text-sacred-gold-dark hover:text-sacred-gold transition-colors shrink-0"
                      title={l('Change location', 'स्थान बदलें')}
                    >
                      <MapPin className="w-5 h-5" />
                    </button>
                  </div>
                  {locSearchOpen && (
                    <div className="absolute left-0 right-0 top-full mt-1 z-30 bg-white border border-sacred-gold/30 rounded-lg shadow-lg p-1.5">
                      <input
                        type="text"
                        value={locSearchQuery}
                        onChange={(e) => handleLocSearch(e.target.value)}
                        placeholder={l('Search city or pincode...', 'शहर या पिनकोड खोजें...')}
                        className="w-full px-2.5 py-1.5 text-sm border border-sacred-gold/20 rounded-md focus:outline-none focus:border-sacred-gold text-[#333]"
                        autoFocus
                      />
                      {locSearchLoading && <p className="text-xs text-muted-foreground px-2 py-1">{l('Searching...', 'खोज रहे हैं...')}</p>}
                      {locSearchResults.length > 0 && (
                        <div className="mt-1 max-h-[160px] overflow-y-auto">
                          {locSearchResults.map((r, i) => (
                            <button
                              key={`${r.name}-${i}`}
                              type="button"
                              onClick={() => selectLocation(r)}
                              className="w-full text-left px-2.5 py-1.5 text-xs text-[#333] hover:bg-sacred-gold/10 rounded transition-colors truncate"
                            >
                              {r.name}
                            </button>
                          ))}
                        </div>
                      )}
                    </div>
                  )}
                </div>
                <p className="text-[15px] font-semibold text-green-700 mb-2.5 shrink-0">
                  {new Date(`${getLocalDateString()}T12:00:00`).toLocaleDateString(hi ? 'hi-IN' : 'en-IN', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' })}
                </p>
                {panchangLoading ? (
                  <div className="flex items-center gap-2 text-sm text-muted-foreground py-8">
                    <Loader2 className="w-5 h-5 animate-spin" />
                    <span>{l('Loading Panchang...', 'पंचांग लोड हो रहा है...')}</span>
                  </div>
                ) : (
                  <div className="space-y-0.5 text-[15px] leading-6 text-[#2a2a2a] flex-1 overflow-y-auto pr-1 min-h-0">
                    {visiblePanchangLines.map((line, idx) => (
                      <p key={`${line.label}-${idx}`}>
                        <span className="font-semibold text-sacred-gold-dark">{line.label}:</span>{' '}
                        <span className="text-[#2a2a2a]">{line.value}</span>
                      </p>
                    ))}
                  </div>
                )}
              </div>
            </div>
            <div className="w-full max-w-none h-full rounded-xl border border-sacred-gold/20 bg-transparent backdrop-blur-[1px] shadow-sm overflow-hidden flex flex-col">
              <div className="bg-sacred-gold-dark text-white px-3 py-1.5 text-[15px] font-semibold shrink-0">
                {hi ? `${locationLabel.replace(', India', ', भारत').replace('New Delhi', 'नई दिल्ली').replace('Delhi', 'दिल्ली')} वैदिक समय` : `Vedic Time for ${locationLabel}`}
              </div>
              <div className="p-2.5 flex-1 flex flex-col">
                <div className="grid grid-cols-2 rounded-md bg-sacred-gold/8 p-1 mb-2 gap-1">
                  <button
                    type="button"
                    onClick={() => setVedicClockMode('30')}
                    className={`w-full px-2 py-1.5 text-[13px] rounded-sm transition-colors ${vedicClockMode === '30' ? 'bg-sacred-gold/25 text-sacred-gold-dark font-semibold' : 'text-muted-foreground'}`}
                  >
                    {l('30 Ghati Clock', '30 घटी घड़ी')}
                  </button>
                  <button
                    type="button"
                    onClick={() => setVedicClockMode('60')}
                    className={`w-full px-2 py-1.5 text-[13px] rounded-sm transition-colors ${vedicClockMode === '60' ? 'bg-sacred-gold/25 text-sacred-gold-dark font-semibold' : 'text-muted-foreground'}`}
                  >
                    {l('60 Ghati Clock', '60 घटी घड़ी')}
                  </button>
                </div>
                <div className="rounded-lg bg-transparent border border-sacred-gold/10 p-2.5 text-center flex-1">
                  <p className="text-[42px] leading-none font-bold text-[#9b1c1c] tracking-wide">{vedicTimeStr}</p>
                  <p className="text-[16px] mt-1.5 font-semibold text-[#4b4b4b]">{l('Ghati : Pal : Vipal', 'घटी : पल : विपल')}</p>
                  <div className="h-px bg-[#b9aa95] my-2" />
                  <div className="flex items-center justify-between text-[14px]">
                    <span className="text-[#666]">{l('Sunrise', 'सूर्योदय')} <span className="text-[#b21f1f]">☀ {formatTime12(panchangData?.sunrise)}</span></span>
                    <span className="text-[#666]">{l('Sunset', 'सूर्यास्त')} <span className="text-[#b21f1f]">☀ {formatTime12(panchangData?.sunset)}</span></span>
                  </div>
                  <div className="h-px bg-[#d4c8b8] my-2" />
                  <p className="text-[13px] text-[#4a4a4a]">
                    <span className="underline decoration-sacred-gold/60">{purnimantaDisplay}</span>,{' '}
                    <span className="underline decoration-sacred-gold/60">{thi(panchangData?.tithi?.paksha || '--', PAKSHA_HI)} {thi(panchangData?.tithi?.name || '', TITHI_HI)}</span>,{' '}
                    {vikram || '--'} {l('Vikrama Samvata', 'विक्रम संवत')}
                  </p>
                  <p className="text-[13px] text-[#4a4a4a]">{weekdayDisplay}</p>
                </div>
                <div className="h-px bg-[#b9aa95] my-2" />
                <div className="rounded-lg bg-transparent border border-sacred-gold/10 p-2.5 text-center">
                  <p className="text-[30px] font-bold text-[#9b1c1c] tracking-wide">
                    {l('Gregorian Time', 'ग्रेगोरियन समय')}
                  </p>
                  <p className="text-[42px] leading-none font-bold text-[#9b1c1c] tracking-wide mt-1">
                    {now.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false })}
                  </p>
                  <p className="text-[18px] mt-1.5 font-semibold text-[#4b4b4b]">{l('Hours : Minutes : Seconds', 'घंटे : मिनट : सेकंड')}</p>
                  <div className="h-px bg-[#b9aa95] my-2" />
                  <div className="flex items-center justify-between text-[14px]">
                    <span className="text-[#666]">{l('Sunrise', 'सूर्योदय')} <span className="text-[#b21f1f]">☀ {formatTime12(panchangData?.sunrise)}</span></span>
                    <span className="text-[#666]">{l('Sunset', 'सूर्यास्त')} <span className="text-[#b21f1f]">☀ {formatTime12(panchangData?.sunset)}</span></span>
                  </div>
                  <div className="h-px bg-[#d4c8b8] my-2" />
                  <p className="text-[13px] text-[#4a4a4a]">
                    {now.toLocaleDateString(hi ? 'hi-IN' : 'en-IN', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })}
                  </p>
                </div>
              </div>
            </div>
            <div className="w-full max-w-none h-full rounded-xl border border-sacred-gold/20 bg-transparent backdrop-blur-[1px] shadow-sm overflow-hidden flex flex-col">
              <div className="bg-sacred-gold-dark text-white px-3 py-1.5 text-[15px] font-semibold shrink-0">
                {l('Upcoming Fasts and Festivals', 'आगामी व्रत और त्योहार')}
              </div>
              <div className="p-2.5 flex-1 overflow-hidden min-h-0">
                <div className="rounded-lg bg-transparent border border-sacred-gold/10 h-full overflow-y-auto">
                  {festivalsLoading ? (
                    <div className="h-full flex items-center justify-center text-sm text-muted-foreground py-8">
                      <Loader2 className="w-4 h-4 animate-spin mr-2" />
                      <span>{l('Loading festivals...', 'त्योहार लोड हो रहे हैं...')}</span>
                    </div>
                  ) : upcomingFestivals.length === 0 ? (
                    <div className="h-full flex items-center justify-center text-sm text-muted-foreground py-8">
                      {l('No upcoming festivals found', 'कोई आगामी त्योहार नहीं मिला')}
                    </div>
                  ) : (
                    <div className="divide-y divide-sacred-gold/15">
                      {upcomingFestivals.map((f, idx) => {
                        const dateObj = f.date ? new Date(`${f.date}T12:00:00`) : null;
                        const todayObj = new Date(`${getLocalDateString()}T12:00:00`);
                        const days = dateObj ? Math.max(0, Math.round((dateObj.getTime() - todayObj.getTime()) / 86400000)) : null;
                        const dateLabel = dateObj
                          ? dateObj.toLocaleDateString(hi ? 'hi-IN' : 'en-IN', { month: 'short', day: 'numeric' })
                          : '--';
                        return (
                          <div key={`${f.name || 'fest'}-${idx}`} className="px-2 py-1.5">
                            <p className="text-[14px] leading-5 truncate">
                              <span className="font-semibold text-sacred-gold-dark">{hi ? ((f.name || '--').split(' / ').map(p => FESTIVAL_HI[p.trim()] || p.trim()).join(' / ')) : (f.name || '--')}</span>
                              <span className="text-[#2a2a2a]">: {dateLabel} {days !== null ? `(${days} ${l('Days', 'दिन')})` : ''}</span>
                            </p>
                          </div>
                        );
                      })}
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Hora & Choghadiya Tables */}
        {panchangData && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-12">
            {/* Hora Table */}
            {panchangData.hora_table && panchangData.hora_table.length > 0 && (
              <div className="rounded-xl border border-sacred-gold/20 bg-transparent backdrop-blur-[1px] shadow-sm overflow-hidden">
                <div className="bg-sacred-gold-dark text-white px-3 py-2 text-[15px] font-semibold">
                  {l('Hora Table', 'होरा तालिका')}
                </div>
                <div className="p-2.5 max-h-[400px] overflow-y-auto">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="bg-sacred-gold/10 text-sacred-gold-dark text-xs uppercase tracking-wider">
                        <th className="text-left px-2 py-1.5">{l('Hora', 'होरा')}</th>
                        <th className="text-left px-2 py-1.5">{l('Lord', 'स्वामी')}</th>
                        <th className="text-left px-2 py-1.5">{l('Time', 'समय')}</th>
                        <th className="text-center px-2 py-1.5">{l('Type', 'प्रकार')}</th>
                      </tr>
                    </thead>
                    <tbody>
                      {panchangData.hora_table.map((h: any, i: number) => (
                        <tr key={i} className="border-b border-sacred-gold/10 last:border-0">
                          <td className="px-2 py-1.5 font-medium text-foreground">{h.hora}</td>
                          <td className="px-2 py-1.5 text-foreground">{h.lord}</td>
                          <td className="px-2 py-1.5 text-muted-foreground">{h.start} - {h.end}</td>
                          <td className="px-2 py-1.5 text-center">
                            <span className={`text-xs px-1.5 py-0.5 rounded-full ${h.type === 'day' ? 'bg-amber-50 text-amber-700' : 'bg-indigo-50 text-indigo-700'}`}>
                              {h.type === 'day' ? l('Day', 'दिन') : l('Night', 'रात')}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* Choghadiya Table */}
            {panchangData.choghadiya && panchangData.choghadiya.length > 0 && (
              <div className="rounded-xl border border-sacred-gold/20 bg-transparent backdrop-blur-[1px] shadow-sm overflow-hidden">
                <div className="bg-sacred-gold-dark text-white px-3 py-2 text-[15px] font-semibold">
                  {l('Choghadiya', 'चौघड़िया')}
                </div>
                <div className="p-2.5 max-h-[400px] overflow-y-auto">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="bg-sacred-gold/10 text-sacred-gold-dark text-xs uppercase tracking-wider">
                        <th className="text-left px-2 py-1.5">{l('Name', 'नाम')}</th>
                        <th className="text-left px-2 py-1.5">{l('Time', 'समय')}</th>
                        <th className="text-center px-2 py-1.5">{l('Quality', 'गुणवत्ता')}</th>
                      </tr>
                    </thead>
                    <tbody>
                      {panchangData.choghadiya.map((c: any, i: number) => {
                        const qualityColor = c.quality === 'Best' ? 'bg-green-50 text-green-700' :
                          c.quality === 'Good' ? 'bg-blue-50 text-blue-700' :
                          c.quality === 'Neutral' ? 'bg-gray-50 text-gray-600' :
                          'bg-red-50 text-red-600';
                        return (
                          <tr key={i} className="border-b border-sacred-gold/10 last:border-0">
                            <td className="px-2 py-1.5 font-medium text-foreground">{c.name}</td>
                            <td className="px-2 py-1.5 text-muted-foreground">{c.start} - {c.end}</td>
                            <td className="px-2 py-1.5 text-center">
                              <span className={`text-xs px-1.5 py-0.5 rounded-full ${qualityColor}`}>
                                {c.quality === 'Best' ? l('Best', 'सर्वोत्तम') :
                                 c.quality === 'Good' ? l('Good', 'शुभ') :
                                 c.quality === 'Neutral' ? l('Neutral', 'सामान्य') :
                                 l('Inauspicious', 'अशुभ')}
                              </span>
                            </td>
                          </tr>
                        );
                      })}
                      {/* Night Choghadiya */}
                      {panchangData.night_choghadiya && panchangData.night_choghadiya.map((c: any, i: number) => {
                        const qualityColor = c.quality === 'Best' ? 'bg-green-50 text-green-700' :
                          c.quality === 'Good' ? 'bg-blue-50 text-blue-700' :
                          c.quality === 'Neutral' ? 'bg-gray-50 text-gray-600' :
                          'bg-red-50 text-red-600';
                        return (
                          <tr key={`night-${i}`} className="border-b border-sacred-gold/10 last:border-0 bg-indigo-50/30">
                            <td className="px-2 py-1.5 font-medium text-foreground">{c.name} <span className="text-[10px] text-indigo-500">{l('(Night)', '(रात)')}</span></td>
                            <td className="px-2 py-1.5 text-muted-foreground">{c.start} - {c.end}</td>
                            <td className="px-2 py-1.5 text-center">
                              <span className={`text-xs px-1.5 py-0.5 rounded-full ${qualityColor}`}>
                                {c.quality === 'Best' ? l('Best', 'सर्वोत्तम') :
                                 c.quality === 'Good' ? l('Good', 'शुभ') :
                                 c.quality === 'Neutral' ? l('Neutral', 'सामान्य') :
                                 l('Inauspicious', 'अशुभ')}
                              </span>
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        )}

        <div className="features-title text-center mb-16">
          <Heading as={2} variant={2} className="text-sacred-gold-dark mb-6 leading-[1.1]">
            {l('Complete astrological operating system', 'पूर्ण ज्योतिषीय ऑपरेटिंग सिस्टम')}
          </Heading>
          <div className="max-w-full mx-auto text-lg text-gray-600 leading-relaxed">
            <p>{l('Most astrology apps use lookup tables and generic predictions.', 'अधिकांश ज्योतिष ऐप लुकअप टेबल और सामान्य भविष्यवाणी का उपयोग करते हैं।')}</p>
            <p><strong className="text-sacred-gold-dark">{l('Astro Rattan computes every position from Swiss Ephemeris', 'Astro Rattan Swiss Ephemeris से हर स्थिति की गणना करता है')}</strong>{l(' — the same library used by research astronomers — accurate to arc-seconds.', ' — यही लाइब्रेरी शोध खगोलविद भी उपयोग करते हैं — आर्क-सेकंड तक सटीक।')}</p>
          </div>
        </div>

        {/* Feature Cards Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <Card
              key={index}
              className="feature-card group relative bg-white border border-[#e0d5c5] overflow-hidden transition-all duration-300 hover:shadow-lg hover:shadow-sacred-gold/10"
            >
              <div className="relative px-3 pt-3">
                <img
                  src={feature.image}
                  alt={feature.title}
                  className="w-full h-[180px] object-cover object-center"
                  style={{
                    objectPosition: feature.imagePosition || 'center center',
                    filter: feature.imageFilter || 'sepia(0.2) brightness(0.95) contrast(1.05)',
                  }}
                  loading="lazy"
                />
                {feature.badge && (
                  <span className="absolute top-3 right-3 z-10 bg-[#8B4513] text-white text-[10px] font-semibold px-[10px] py-1 rounded">
                    {feature.badge}
                  </span>
                )}
              </div>
              <CardContent className="p-5">
                <Heading as={3} variant={3} className="mb-1 uppercase tracking-wide">
                  {feature.title}
                </Heading>
                <p className="text-xs font-semibold text-sacred-gold-dark uppercase tracking-wider mb-3">
                  {feature.subtitle}
                </p>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  {feature.desc}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>


        {/* CTA */}
        <div className="text-center mt-16">
          <p className="text-xl text-foreground mb-6">
            {l('Ready to experience the difference?', 'अंतर अनुभव करने के लिए तैयार हैं?')}
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a
              href="/login"
              className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-sacred-gold-dark text-white rounded-lg font-semibold hover:bg-sacred-gold transition-all shadow-lg shadow-sacred-gold/20"
            >
              {l('Create Your Account', 'अपना अकाउंट बनाएं')}
              <Sparkles className="w-4 h-4" />
            </a>
            <button
              onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
              className="inline-flex items-center justify-center gap-2 px-8 py-4 border-2 border-sacred-gold/50 text-sacred-gold-dark rounded-lg font-semibold hover:bg-sacred-gold/10 transition-all"
            >
              {l('Try Free Kundli', 'मुफ्त कुंडली देखें')}
            </button>
          </div>
        </div>

        {/* ── FAQ Section ──────────────────────────────────────────── */}
        <div className="mt-24">
          <div className="text-center mb-12">
            <h2 className="text-3xl sm:text-4xl font-sans text-foreground mb-2">
              {l('Frequently Asked Questions', 'अक्सर पूछे जाने वाले प्रश्न')}
            </h2>
            <div className="w-20 h-1 bg-sacred-gold mx-auto rounded-full" />
          </div>

          <div className="max-w-7xl mx-auto space-y-8">
            {[
              {
                category: l('BASICS', 'बुनियादी बातें'),
                faqs: [
                  {
                    q: l('What is a Kundli?', 'कुंडली क्या है?'),
                    a: l(
                      'Your Kundli is a birth chart based on your date, time, and place of birth. It shows planetary positions at the exact moment you were born and reveals life patterns across career, marriage, health, and more.',
                      'कुंडली आपकी जन्म तिथि, समय और जन्म स्थान पर आधारित जन्म चार्ट है। यह आपके जन्म के सटीक क्षण में ग्रहों की स्थिति दिखाती है और करियर, विवाह, स्वास्थ्य आदि में जीवन पैटर्न प्रकट करती है।'
                    ),
                  },
                  {
                    q: l('Is this Kundli really accurate?', 'क्या यह कुंडली वास्तव में सटीक है?'),
                    a: l(
                      'Yes. We use Swiss Ephemeris — the same astronomical engine used by research institutions worldwide — accurate to arc-seconds. Combined with your exact birth time and coordinates, the calculations match professional Vedic astrology software like Jagannatha Hora.',
                      'हां। हम स्विस एफेमेरिस का उपयोग करते हैं — वही खगोलीय इंजन जो दुनिया भर के अनुसंधान संस्थानों द्वारा उपयोग किया जाता है — आर्क-सेकंड तक सटीक। आपके सटीक जन्म समय और निर्देशांकों के साथ, गणनाएं जगन्नाथ होरा जैसे पेशेवर वैदिक ज्योतिष सॉफ्टवेयर से मेल खाती हैं।'
                    ),
                  },
                  {
                    q: l('What details are required to generate Kundli?', 'कुंडली बनाने के लिए क्या विवरण आवश्यक हैं?'),
                    a: l(
                      'You need: Date of birth, Time of birth, and Place of birth. More accurate birth time = better predictions. Even a 4-minute difference can change your Ascendant (Lagna).',
                      'आपको चाहिए: जन्म तिथि, जन्म समय, और जन्म स्थान। अधिक सटीक जन्म समय = बेहतर भविष्यवाणी। 4 मिनट का अंतर भी आपका लग्न बदल सकता है।'
                    ),
                  },
                  {
                    q: l('Can I generate Kundli for free?', 'क्या मैं मुफ्त में कुंडली बना सकता हूं?'),
                    a: l(
                      'Yes! You can generate your basic Kundli for free and view key insights instantly — including birth chart, planet positions, current Dasha, and basic life predictions.',
                      'हां! आप अपनी मुफ्त कुंडली बना सकते हैं और तुरंत मुख्य अंतर्दृष्टि देख सकते हैं — जन्म चार्ट, ग्रह स्थिति, वर्तमान दशा, और बुनियादी जीवन भविष्यवाणी सहित।'
                    ),
                  },
                ],
              },
              {
                category: l('FEATURES', 'विशेषताएं'),
                faqs: [
                  {
                    q: l('What will I get in the free Kundli?', 'मुफ्त कुंडली में मुझे क्या मिलेगा?'),
                    a: l(
                      'You will see: Birth chart (Lagna, Chandra & Lal Kitab charts), Planet positions with dignity status, Basic life insights (career, marriage, health), Current Dasha period, Key planetary effects and doshas, One Lal Kitab remedy, and Today\'s Panchang snapshot.',
                      'आपको मिलेगा: जन्म चार्ट (लग्न, चंद्र और लाल किताब कुंडली), ग्रह स्थिति और गरिमा स्थिति, बुनियादी जीवन अंतर्दृष्टि (करियर, विवाह, स्वास्थ्य), वर्तमान दशा, प्रमुख ग्रह प्रभाव और दोष, एक लाल किताब उपाय, और आज का पंचांग।'
                    ),
                  },
                  {
                    q: l('What is included in the full Kundli analysis?', 'पूर्ण कुंडली विश्लेषण में क्या शामिल है?'),
                    a: l(
                      'Full analysis includes: Detailed life predictions across all 12 houses, Complete Lal Kitab remedies for every planet, Dasha timeline with Antardasha and Pratyantar periods, Advanced systems (KP, Jaimini, Ashtakvarga, Shadbala), Divisional charts (D9 Navamsha, D10 Dasamsha, and more), Kundli matching for marriage compatibility, and Downloadable PDF report.',
                      'पूर्ण विश्लेषण में शामिल है: सभी 12 भावों में विस्तृत जीवन भविष्यवाणी, हर ग्रह के लिए पूर्ण लाल किताब उपाय, अंतर्दशा और प्रत्यंतर के साथ दशा समयरेखा, उन्नत प्रणालियां (केपी, जैमिनी, अष्टकवर्ग, षड्बल), वर्ग चार्ट, विवाह के लिए कुंडली मिलान, और डाउनलोड करने योग्य PDF रिपोर्ट।'
                    ),
                  },
                ],
              },
              {
                category: l('PREDICTIONS', 'भविष्यवाणी'),
                faqs: [
                  {
                    q: l('Can Kundli predict my future?', 'क्या कुंडली मेरे भविष्य की भविष्यवाणी कर सकती है?'),
                    a: l(
                      'Kundli shows tendencies, timing, and possibilities — not fixed outcomes. It reveals which life areas will be active during specific Dasha periods, helping you prepare for opportunities and challenges.',
                      'कुंडली प्रवृत्तियां, समय और संभावनाएं दिखाती है — निश्चित परिणाम नहीं। यह बताती है कि विशिष्ट दशा अवधि के दौरान कौन से जीवन क्षेत्र सक्रिय होंगे।'
                    ),
                  },
                  {
                    q: l('When will I get married?', 'मेरी शादी कब होगी?'),
                    a: l(
                      'Marriage timing depends on your 7th house, Venus placement, and Dasha periods. The free preview shows basic indicators — unlock the full report for detailed marriage timing with specific year predictions.',
                      'विवाह का समय आपके 7वें भाव, शुक्र की स्थिति और दशा काल पर निर्भर करता है। मुफ्त प्रीव्यू बुनियादी संकेतक दिखाता है — विस्तृत विवाह समय के लिए पूर्ण रिपोर्ट अनलॉक करें।'
                    ),
                  },
                  {
                    q: l('When will I get a job or career growth?', 'मुझे नौकरी या करियर में वृद्धि कब मिलेगी?'),
                    a: l(
                      'Career timing depends on your 10th house, Saturn and Mercury placements, and current Dasha. Strong 10th house lords in favorable Dasha periods indicate career breakthroughs.',
                      'करियर का समय आपके 10वें भाव, शनि और बुध की स्थिति, और वर्तमान दशा पर निर्भर करता है।'
                    ),
                  },
                  {
                    q: l('Can Kundli help in relationships?', 'क्या कुंडली रिश्तों में मदद कर सकती है?'),
                    a: l(
                      'Yes. Your Kundli reveals compatibility patterns, emotional tendencies, and relationship challenges through 7th house analysis, Venus-Mars dynamics, and Nakshatra compatibility.',
                      'हां। आपकी कुंडली 7वें भाव विश्लेषण, शुक्र-मंगल गतिशीलता, और नक्षत्र अनुकूलता के माध्यम से अनुकूलता पैटर्न, भावनात्मक प्रवृत्तियां और रिश्ते की चुनौतियां प्रकट करती है।'
                    ),
                  },
                  {
                    q: l('Can I ask questions from my Kundli?', 'क्या मैं अपनी कुंडली से सवाल पूछ सकता हूं?'),
                    a: l(
                      'Yes! Common questions include: When will I get married? Job or business? Financial growth timeline? Health concerns? Best time for major decisions? Your Kundli has answers for all life areas.',
                      'हां! आम सवालों में शामिल हैं: शादी कब होगी? नौकरी या व्यापार? वित्तीय वृद्धि? स्वास्थ्य चिंताएं? महत्वपूर्ण निर्णयों के लिए सर्वोत्तम समय? आपकी कुंडली में सभी जीवन क्षेत्रों के उत्तर हैं।'
                    ),
                  },
                ],
              },
              {
                category: l('DOSHAS & REMEDIES', 'दोष और उपाय'),
                faqs: [
                  {
                    q: l('Do I have Manglik Dosha?', 'क्या मुझे मांगलिक दोष है?'),
                    a: l(
                      'Manglik Dosha depends on Mars placement in houses 1, 4, 7, 8, or 12. Our free preview checks this automatically. If present, Lal Kitab remedies can help reduce its effects.',
                      'मांगलिक दोष भाव 1, 4, 7, 8 या 12 में मंगल की स्थिति पर निर्भर करता है। हमारा मुफ्त प्रीव्यू इसे स्वचालित रूप से जांचता है। यदि मौजूद है, तो लाल किताब उपाय इसके प्रभावों को कम करने में मदद कर सकते हैं।'
                    ),
                  },
                  {
                    q: l('What is Kaal Sarp Dosha?', 'काल सर्प दोष क्या है?'),
                    a: l(
                      'Kaal Sarp Dosha occurs when all planets are placed between Rahu and Ketu in your birth chart. It can cause delays and obstacles. We detect this automatically and suggest specific remedies.',
                      'काल सर्प दोष तब होता है जब सभी ग्रह आपकी कुंडली में राहु और केतु के बीच स्थित होते हैं। यह देरी और बाधाएं पैदा कर सकता है। हम इसे स्वचालित रूप से पहचानते हैं और विशिष्ट उपाय सुझाते हैं।'
                    ),
                  },
                  {
                    q: l('Can astrology problems be fixed?', 'क्या ज्योतिष समस्याओं को ठीक किया जा सकता है?'),
                    a: l(
                      'Yes. Remedies like Lal Kitab upay, specific mantras, gemstone recommendations, and lifestyle adjustments can help balance planetary effects. Our system suggests personalized remedies based on your exact chart.',
                      'हां। लाल किताब उपाय, विशिष्ट मंत्र, रत्न सिफारिशें, और जीवनशैली समायोजन ग्रह प्रभावों को संतुलित करने में मदद कर सकते हैं। हमारी प्रणाली आपकी सटीक कुंडली के आधार पर व्यक्तिगत उपाय सुझाती है।'
                    ),
                  },
                  {
                    q: l('What remedies does Lal Kitab suggest?', 'लाल किताब क्या उपाय सुझाती है?'),
                    a: l(
                      'Lal Kitab offers practical, everyday remedies based on planetary house placement — like feeding dogs on Saturdays for Ketu, donating mustard oil for Saturn, keeping a silver square for Moon problems, or watering a Peepal tree for Jupiter. Each remedy is specific to your chart.',
                      'लाल किताब ग्रहों के भाव स्थान के आधार पर व्यावहारिक, रोजमर्रा के उपाय प्रदान करती है — जैसे केतु के लिए शनिवार को कुत्तों को खिलाना, शनि के लिए सरसों का तेल दान करना, चंद्रमा की समस्याओं के लिए चांदी का चौकोर टुकड़ा रखना।'
                    ),
                  },
                  {
                    q: l('What is Lal Kitab and how is it different?', 'लाल किताब क्या है और यह कैसे अलग है?'),
                    a: l(
                      'Lal Kitab is a unique astrology system from ancient Persian-Urdu texts. Unlike Vedic astrology\'s complex rituals, Lal Kitab uses simple house-based analysis with practical remedies anyone can follow — like feeding animals, donating items, or wearing specific colors.',
                      'लाल किताब प्राचीन फ़ारसी-उर्दू ग्रंथों से एक अनूठी ज्योतिष प्रणाली है। वैदिक ज्योतिष के जटिल अनुष्ठानों के विपरीत, लाल किताब सरल भाव-आधारित विश्लेषण का उपयोग करती है जिसमें व्यावहारिक उपाय होते हैं।'
                    ),
                  },
                ],
              },
              {
                category: l('UPGRADE & TRUST', 'अपग्रेड और विश्वास'),
                faqs: [
                  {
                    q: l('Why should I upgrade to full Kundli?', 'मुझे पूर्ण कुंडली में अपग्रेड क्यों करना चाहिए?'),
                    a: l(
                      'Free Kundli shows basics. Full Kundli gives: deeper insights into all 12 life areas, exact timing predictions through Dasha analysis, complete Lal Kitab remedies for every weak planet, advanced systems (KP, Jaimini, Ashtakvarga), and a downloadable professional PDF report.',
                      'मुफ्त कुंडली बुनियादी बातें दिखाती है। पूर्ण कुंडली देती है: सभी 12 जीवन क्षेत्रों में गहरी अंतर्दृष्टि, दशा विश्लेषण के माध्यम से सटीक समय भविष्यवाणी, हर कमजोर ग्रह के लिए पूर्ण लाल किताब उपाय, उन्नत प्रणालियां, और डाउनलोड करने योग्य PDF रिपोर्ट।'
                    ),
                  },
                  {
                    q: l('Is my data safe?', 'क्या मेरा डेटा सुरक्षित है?'),
                    a: l(
                      'Yes. Your birth details are encrypted and stored securely. We use them only for generating your Kundli. We never share personal data with third parties.',
                      'हां। आपके जन्म विवरण एन्क्रिप्टेड और सुरक्षित रूप से संग्रहीत हैं। हम उनका उपयोग केवल आपकी कुंडली बनाने के लिए करते हैं। हम कभी भी व्यक्तिगत डेटा तीसरे पक्ष के साथ साझा नहीं करते।'
                    ),
                  },
                  {
                    q: l('What is the most important part of Kundli?', 'कुंडली का सबसे महत्वपूर्ण हिस्सा क्या है?'),
                    a: l(
                      'Lagna (Ascendant), Moon sign, Nakshatra, and current Dasha are the four most important elements. Together they define your personality, emotional nature, karmic path, and life timing.',
                      'लग्न, चंद्र राशि, नक्षत्र, और वर्तमान दशा चार सबसे महत्वपूर्ण तत्व हैं। साथ मिलकर वे आपके व्यक्तित्व, भावनात्मक स्वभाव, कर्म पथ और जीवन समय को परिभाषित करते हैं।'
                    ),
                  },
                  {
                    q: l('How accurate is the Panchang on Astro Rattan?', 'Astro Rattan पर पंचांग कितना सटीक है?'),
                    a: l(
                      'Our Panchang uses Swiss Ephemeris — accurate to within 1 minute for Tithi, Nakshatra, and Yoga end times. Sunrise/sunset calculated for your exact GPS coordinates with atmospheric refraction. Matches Drik Panchang exactly.',
                      'हमारा पंचांग स्विस एफेमेरिस का उपयोग करता है — तिथि, नक्षत्र और योग के अंत समय के लिए 1 मिनट के भीतर सटीक। सूर्योदय/सूर्यास्त आपके सटीक GPS निर्देशांकों के लिए गणना किया जाता है।'
                    ),
                  },
                  {
                    q: l('How does Numerology work with Astrology?', 'ज्योतिष के साथ अंक शास्त्र कैसे काम करता है?'),
                    a: l(
                      'Numerology analyzes vibrations from your birth date and name. Your Life Path Number reveals core personality, while Expression Number shows talents. Combined with your Vedic chart, it gives a complete picture of strengths, challenges, and ideal timing.',
                      'अंक शास्त्र आपकी जन्म तिथि और नाम से कंपन का विश्लेषण करता है। आपका जीवन पथ अंक मूल व्यक्तित्व प्रकट करता है। वैदिक चार्ट के साथ मिलकर, यह शक्तियों, चुनौतियों और आदर्श समय की पूरी तस्वीर देता है।'
                    ),
                  },
                  {
                    q: l('Can I use Astro Rattan for Kundli matching?', 'क्या मैं कुंडली मिलान के लिए Astro Rattan का उपयोग कर सकता हूं?'),
                    a: l(
                      'Yes! We provide comprehensive Kundli matching with Ashtakoot (8-fold) compatibility scoring — Varna, Vashya, Tara, Yoni, Graha Maitri, Gana, Bhakoot, and Nadi — with detailed score out of 36 points plus Mangal Dosha check.',
                      'हां! हम अष्टकूट अनुकूलता स्कोरिंग के साथ व्यापक कुंडली मिलान प्रदान करते हैं — 36 अंकों में से विस्तृत स्कोर और मंगल दोष जांच के साथ।'
                    ),
                  },
                  {
                    q: l('How accurate are the answers?', 'उत्तर कितने सटीक हैं?'),
                    a: l(
                      'Accuracy depends on correct birth details and depth of analysis. With exact birth time, our Swiss Ephemeris calculations match professional astrology software. The more precise your birth time, the more accurate the predictions.',
                      'सटीकता सही जन्म विवरण और विश्लेषण की गहराई पर निर्भर करती है। सटीक जन्म समय के साथ, हमारी स्विस एफेमेरिस गणनाएं पेशेवर ज्योतिष सॉफ्टवेयर से मेल खाती हैं।'
                    ),
                  },
                ],
              },
            ].map((section, sIdx) => {
              const baseIdx = [0, 4, 6, 11, 16][sIdx] ?? sIdx * 5;
              return (
                <div key={sIdx}>
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-1 h-6 bg-sacred-gold-dark rounded-full" />
                    <span className="text-xs font-bold uppercase tracking-widest text-sacred-gold-dark">
                      {section.category}
                    </span>
                  </div>
                  <div className="space-y-3">
                    {section.faqs.map((faq, fIdx) => {
                      const globalIdx = baseIdx + fIdx;
                      return (
                        <div
                          key={fIdx}
                          className="border border-sacred-gold/30 rounded-lg overflow-hidden transition-all"
                        >
                          <button
                            onClick={() => setOpenFaq(openFaq === globalIdx ? null : globalIdx)}
                            className="w-full flex items-center justify-between px-5 py-4 text-left hover:bg-sacred-gold/5 transition-colors"
                          >
                            <span className="text-base font-medium text-foreground pr-4">{faq.q}</span>
                            {openFaq === globalIdx ? (
                              <ChevronUp className="w-5 h-5 text-sacred-gold-dark shrink-0" />
                            ) : (
                              <ChevronDown className="w-5 h-5 text-sacred-gold-dark shrink-0" />
                            )}
                          </button>
                          <div
                            className={`overflow-hidden transition-all duration-300 ${
                              openFaq === globalIdx ? 'max-h-96 opacity-100' : 'max-h-0 opacity-0'
                            }`}
                          >
                            <p className="px-5 pb-4 text-sm leading-relaxed text-foreground/80">
                              {faq.a}
                            </p>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

      </div>
    </section>

    {/* ── Lightbox ─────────────────────────────────────────────── */}
    {lightbox && (
      <div
        className="fixed inset-0 z-[9999] flex items-center justify-center p-4 sm:p-8 bg-black/85"
        onClick={() => setLightbox(null)}
      >
        {/* Card — stops propagation so clicking the image doesn't close */}
        <div
          className="relative max-w-5xl w-full rounded-2xl overflow-hidden shadow-2xl"
          onClick={e => e.stopPropagation()}
        >
          <img
            src={`/images/showcase/${lightbox.file}`}
            alt={lightbox.label}
            className="w-full h-auto block"
          />
          {/* Label bar */}
          <div className="px-6 py-4 flex items-center justify-between bg-[#1a1625]">
            <p className="text-sm font-bold uppercase tracking-widest text-[#C4611F]">
              {lightbox.label}
            </p>
            <button
              type="button"
              onClick={() => setLightbox(null)}
              className="text-gray-500 hover:text-gray-800 transition-colors"
              aria-label="Close"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* ESC hint */}
        <p className="absolute bottom-4 left-0 right-0 text-center text-white/50 text-xs pointer-events-none">
          {l('Press ESC or click outside to close', 'बंद करने के लिए ESC दबाएं या बाहर क्लिक करें')}
        </p>
      </div>
    )}
  </>
  );
}
