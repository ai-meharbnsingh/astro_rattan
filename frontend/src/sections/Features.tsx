import { useEffect, useRef, useState } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Card, CardContent } from '@/components/ui/card';
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { api } from '@/lib/api';
import { useTranslation } from '@/lib/i18n';
import { AlertTriangle, Calendar, CheckCircle, ChevronDown, ChevronUp, Clock, HelpCircle, Info, Loader2, MapPin, MessageCircle, Moon, Sparkles, Star, Sun, X, XCircle } from 'lucide-react';
import { Heading } from '@/components/ui/heading';
import KundliChartSVG from '@/components/KundliChartSVG';

gsap.registerPlugin(ScrollTrigger);

// Live ticking clock for Present Kundli section
function LiveClock({ language }: { language: string }) {
  const [now, setNow] = useState(new Date());
  useEffect(() => {
    const id = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(id);
  }, []);
  const hi = language === 'hi';
  const date = now.toLocaleDateString(hi ? 'hi-IN' : 'en-IN', { day: '2-digit', month: 'short', year: 'numeric' });
  const time = now.toLocaleTimeString(hi ? 'hi-IN' : 'en-IN', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true });
  return (
    <p className="text-center text-lg text-gray-600 mb-6">
      <strong className="text-sacred-gold-dark">{hi ? 'अभी ग्रहों की लाइव स्थिति' : 'Live planetary positions right now'}</strong>
      {' — '}
      <span className="font-mono text-sacred-gold-dark">{date} {time} IST</span>
    </p>
  );
}

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

const PLANET_COLORS: Record<string, string> = {
  Sun: '#F97316',
  Moon: '#94A3B8',
  Mars: '#DC2626',
  Mercury: '#10B981',
  Jupiter: '#D97706',
  Venus: '#EC4899',
  Saturn: '#1E40AF',
  Rahu: '#6366F1',
  Ketu: '#9F1239',
};

const SIGN_THEMES: Record<string, { en: string; hi: string }> = {
  Aries:       { en: 'impulsive decisions, action-oriented day',     hi: 'आवेगपूर्ण निर्णय, क्रियाशील दिन' },
  Taurus:      { en: 'stability focus, material concerns',           hi: 'स्थिरता, भौतिक विषयों पर ध्यान' },
  Gemini:      { en: 'communication active, mental energy high',     hi: 'संचार सक्रिय, मानसिक ऊर्जा उच्च' },
  Cancer:      { en: 'emotional sensitivity, home focus',            hi: 'भावनात्मक संवेदनशीलता, घर पर ध्यान' },
  Leo:         { en: 'confidence boost, creative expression',        hi: 'आत्मविश्वास, रचनात्मक अभिव्यक्ति' },
  Virgo:       { en: 'analytical thinking, detail-oriented',         hi: 'विश्लेषणात्मक सोच, विवरण पर ध्यान' },
  Libra:       { en: 'relationship focus, balance-seeking',          hi: 'संबंधों पर ध्यान, संतुलन की खोज' },
  Scorpio:     { en: 'intense focus, transformation energy',         hi: 'गहन ध्यान, परिवर्तनकारी ऊर्जा' },
  Sagittarius: { en: 'optimism, expansion, higher learning',         hi: 'आशावाद, विस्तार, उच्च शिक्षा' },
  Capricorn:   { en: 'discipline, career focus, ambition',           hi: 'अनुशासन, करियर पर ध्यान' },
  Aquarius:    { en: 'innovation, community, unconventional ideas',  hi: 'नवाचार, समुदाय, अपरंपरागत विचार' },
  Pisces:      { en: 'emotional thinking, avoid confusion',          hi: 'भावनात्मक सोच, भ्रम से बचें' },
};

const SIGN_HI_NAMES: Record<string, string> = {
  Aries: 'मेष', Taurus: 'वृषभ', Gemini: 'मिथुन', Cancer: 'कर्क', Leo: 'सिंह',
  Virgo: 'कन्या', Libra: 'तुला', Scorpio: 'वृश्चिक', Sagittarius: 'धनु',
  Capricorn: 'मकर', Aquarius: 'कुंभ', Pisces: 'मीन',
};

const PLANET_HI_NAMES: Record<string, string> = {
  Sun: 'सूर्य', Moon: 'चंद्र', Mars: 'मंगल', Mercury: 'बुध',
  Jupiter: 'गुरु', Venus: 'शुक्र', Saturn: 'शनि', Rahu: 'राहु', Ketu: 'केतु',
};

function computeDailyInsights(planets: any[], language: string): string[] {
  if (!planets || planets.length === 0) return [];
  const hi = language === 'hi';
  const insights: string[] = [];

  const signCount: Record<string, string[]> = {};
  for (const p of planets) {
    if (!p.sign || p.planet === 'Rahu' || p.planet === 'Ketu') continue;
    if (!signCount[p.sign]) signCount[p.sign] = [];
    signCount[p.sign].push(p.planet);
  }

  for (const [sign, ps] of Object.entries(signCount)) {
    if (ps.length >= 2) {
      const theme = SIGN_THEMES[sign];
      const signLabel = hi ? (SIGN_HI_NAMES[sign] || sign) : sign;
      const pLabels = ps.map(n => hi ? (PLANET_HI_NAMES[n] || n) : n).join(', ');
      if (theme) insights.push(`${hi ? 'मजबूत' : 'Strong'} ${signLabel} ${hi ? 'प्रभाव' : 'influence'} (${pLabels}) → ${hi ? theme.hi : theme.en}`);
    }
  }

  const rahu = planets.find(p => p.planet === 'Rahu');
  if (rahu?.sign) {
    const signLabel = hi ? (SIGN_HI_NAMES[rahu.sign] || rahu.sign) : rahu.sign;
    insights.push(hi
      ? `राहु ${signLabel} में → नए जोखिम भरे कार्यों से बचें, सतर्क रहें`
      : `Rahu in ${signLabel} → avoid risky new beginnings, stay mindful`);
  }

  const retros = planets.filter(p => p.is_retrograde && p.planet !== 'Rahu' && p.planet !== 'Ketu');
  if (retros.length > 0) {
    const names = retros.map(p => hi ? (PLANET_HI_NAMES[p.planet] || p.planet) : p.planet).join(', ');
    insights.push(hi
      ? `${names} वक्री → लंबित मामलों की समीक्षा करें, नए अनुबंधों में देरी करें`
      : `${names} retrograde → review pending matters, delay new contracts`);
  }

  return insights.slice(0, 5);
}

function computeDayEnergy(insights: string[]): { en: string; hi: string } {
  const text = insights.join(' ').toLowerCase();
  const avoidCount = (text.match(/avoid/g) || []).length + (text.match(/बचें/g) || []).length;
  const hasRetro = text.includes('retrograde') || text.includes('वक्री');
  const hasAction = text.includes('action-oriented') || text.includes('सक्रिय');
  const hasEmotional = text.includes('emotional') || text.includes('भावनात्मक');
  if (hasRetro && avoidCount >= 2) return { en: '🔄 Reflective', hi: '🔄 चिंतनशील' };
  if (avoidCount >= 2) return { en: '⚠ Cautious', hi: '⚠ सावधानी' };
  if (hasAction && !hasEmotional) return { en: '⚡ Action Day', hi: '⚡ सक्रिय दिन' };
  if (hasEmotional && avoidCount >= 1) return { en: '🌊 Mixed Energy', hi: '🌊 मिश्रित ऊर्जा' };
  if (hasEmotional) return { en: '🌊 Emotional', hi: '🌊 भावनात्मक' };
  if (hasRetro) return { en: '🔄 Reflective', hi: '🔄 चिंतनशील' };
  return { en: '🌟 Steady', hi: '🌟 सामान्य' };
}

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
  scores?: { overall: number; love: number; career: number; finance: number; health: number };
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
  hora_table?: Array<{ hora: number; lord: string; start: string; end: string; type: string }>;
  choghadiya?: Array<{ name: string; quality: string; start: string; end: string }>;
  night_choghadiya?: Array<{ name: string; quality: string; start: string; end: string }>;
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
const PLANET_HI: Record<string, string> = {
  Sun: 'सूर्य', Moon: 'चंद्र', Mars: 'मंगल', Mercury: 'बुध',
  Jupiter: 'गुरु', Venus: 'शुक्र', Saturn: 'शनि',
  Rahu: 'राहु', Ketu: 'केतु', Uranus: 'यूरेनस', Neptune: 'नेपच्यून', Pluto: 'प्लूटो',
};
const CHOGHADIYA_HI: Record<string, string> = {
  Amrit: 'अमृत', Shubh: 'शुभ', Labh: 'लाभ', Char: 'चर',
  Rog: 'रोग', Kaal: 'काल', Udveg: 'उद्वेग',
};
const FESTIVAL_HI: Record<string, string> = {
  'Pradosh Vrat': 'प्रदोष व्रत', 'Guruvar Vrat': 'गुरुवार व्रत', 'Masik Shivaratri': 'मासिक शिवरात्रि',
  'Amavasya': 'अमावस्या', 'Shukravar Vrat': 'शुक्रवार व्रत', 'Shani Vrat': 'शनि व्रत',
  'Akshaya Tritiya': 'अक्षय तृतीया', 'Parashurama Jayanti': 'परशुराम जयंती',
  'Rohini Nakshatra Puja': 'रोहिणी नक्षत्र पूजा', 'Somvar Vrat': 'सोमवार व्रत',
  'Mangalvar Vrat': 'मंगलवार व्रत', 'Panchami Vrat': 'पंचमी व्रत',
  'Saptami Vrat': 'सप्तमी व्रत', 'Navami Vrat': 'नवमी व्रत',
  'Vivah Panchami': 'विवाह पंचमी', 'Surya Saptami': 'सूर्य सप्तमी',
  'Pushya Yoga Observance': 'पुष्य योग अनुष्ठान',
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

// Safely extract a string from either a plain string or a bilingual {en, hi} object
const extractStr = (value: any, lang = 'en'): string => {
  if (!value) return '';
  if (typeof value === 'string') return value;
  if (typeof value === 'object') return String(value[lang] || value['en'] || '');
  return String(value);
};

const compactLine = (value?: any, fallback = 'Guidance will update shortly.', lang = 'en') => {
  const text = extractStr(value, lang).replace(/\s+/g, ' ').trim();
  if (!text) return fallback;
  const sentence = text.split(/(?<=[.!?])\s+/)[0] || text;
  return sentence.length > 95 ? `${sentence.slice(0, 92).trim()}...` : sentence;
};

const hasMeaningfulSections = (sections?: HoroscopeSections) => {
  if (!sections) return false;
  return ['general', 'love', 'career', 'finance', 'health'].some((k) => {
    const raw = sections[k as keyof HoroscopeSections];
    const value = extractStr(raw).trim();
    return value.length >= 15;
  });
};

const PRASHNA_QUESTIONS = [
  { key: 'marriage', emoji: '💑', en: 'Marriage', hi: 'विवाह' },
  { key: 'job', emoji: '💼', en: 'Career', hi: 'करियर' },
  { key: 'finance', emoji: '💰', en: 'Finance', hi: 'वित्त' },
  { key: 'health', emoji: '🏥', en: 'Health', hi: 'स्वास्थ्य' },
  { key: 'travel', emoji: '✈️', en: 'Travel', hi: 'यात्रा' },
];

function PrashnaResultCard({ result, l }: { result: any; l: (en: string, hi: string) => string }) {
  const v: string = result.verdict || 'neutral';
  const palette: Record<string, { bg: string; border: string; text: string; icon: string }> = {
    favorable:   { bg: 'bg-emerald-50', border: 'border-emerald-300', text: 'text-emerald-800', icon: 'text-emerald-500' },
    unfavorable: { bg: 'bg-red-50',     border: 'border-red-300',     text: 'text-red-800',     icon: 'text-red-500'     },
    mixed:       { bg: 'bg-amber-50',   border: 'border-amber-300',   text: 'text-amber-800',   icon: 'text-amber-500'   },
    neutral:     { bg: 'bg-gray-50',    border: 'border-gray-300',    text: 'text-gray-700',    icon: 'text-gray-400'    },
  };
  const c = palette[v] || palette.neutral;
  const Icon = v === 'favorable' ? CheckCircle : v === 'unfavorable' ? XCircle : Info;
  const label: Record<string, string> = {
    favorable:   l('Favorable ✓', 'अनुकूल ✓'),
    unfavorable: l('Unfavorable ✗', 'प्रतिकूल ✗'),
    mixed:       l('Mixed', 'मिश्रित'),
    neutral:     l('Neutral', 'तटस्थ'),
  };
  return (
    <div className={`mt-4 p-4 rounded-xl border ${c.bg} ${c.border}`}>
      <div className="flex items-center gap-2 mb-2">
        <Icon className={`w-5 h-5 shrink-0 ${c.icon}`} />
        <span className={`font-bold text-base ${c.text}`}>{label[v] || v}</span>
      </div>
      <p className={`text-sm ${c.text} leading-relaxed mb-2`}>{result.verdict_detail}</p>
      {result.timing && (
        <p className="text-xs text-muted-foreground italic leading-relaxed">{result.timing}</p>
      )}
      <p className="text-[10px] text-muted-foreground mt-2 pt-2 border-t border-current/10">
        {l('KP Horary', 'KP होरेरी')} #{result.number} · {result.queried_at}
      </p>
    </div>
  );
}

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
  const [currentSky, setCurrentSky] = useState<any>(null);
  const [numeroDob, setNumeroDob] = useState<string>('');
  const [numeroResult, setNumeroResult] = useState<{ lifePath: number; personalDay: number } | null>(null);
  const locSearchRef = useRef<HTMLDivElement>(null);
  const locSearchTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Prashna Kundli state
  const [prashnaQ, setPrashnaQ] = useState<string>('marriage');
  const [prashnaCity, setPrashnaCity] = useState<string>('New Delhi');
  const [prashnaLat, setPrashnaLat] = useState<number | null>(null);
  const [prashnaLon, setPrashnaLon] = useState<number | null>(null);
  const [prashnaSuggs, setPrashnaSuggs] = useState<Array<{ name: string; lat: number; lon: number }>>([]);
  const [prashnaLoading, setPrashnaLoading] = useState<boolean>(false);
  const [prashnaResult, setPrashnaResult] = useState<any>(null);
  const prashnaCityTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

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

  const searchPrashnaCity = (q: string) => {
    setPrashnaCity(q);
    setPrashnaLat(null); setPrashnaLon(null);
    if (prashnaCityTimer.current) clearTimeout(prashnaCityTimer.current);
    if (q.trim().length < 2) { setPrashnaSuggs([]); return; }
    prashnaCityTimer.current = setTimeout(async () => {
      try {
        const r = await api.get(`/api/kundli/geocode?query=${encodeURIComponent(q.trim())}`);
        setPrashnaSuggs(Array.isArray(r) ? r.slice(0, 5) : []);
      } catch { setPrashnaSuggs([]); }
    }, 300);
  };

  const askPrashna = async () => {
    setPrashnaLoading(true);
    setPrashnaResult(null);
    try {
      const r = await api.post('/api/prashna/quick', {
        question_type: prashnaQ,
        city: prashnaCity,
        latitude: prashnaLat,
        longitude: prashnaLon,
      });
      setPrashnaResult(r);
    } catch { /* silent — user sees no change */ }
    setPrashnaLoading(false);
  };

  // Close search dropdown on outside click
  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (locSearchRef.current && !locSearchRef.current.contains(e.target as Node)) setLocSearchOpen(false);
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  // Fetch current sky for Present Kundli section (auto-refresh every 60s)
  useEffect(() => {
    let cancelled = false;
    const load = () => {
      api.get('/api/kundli/current-sky').then(data => {
        if (!cancelled && data) setCurrentSky(data);
      }).catch(() => {});
    };
    load();
    const interval = setInterval(load, 60000);
    return () => { cancelled = true; clearInterval(interval); };
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
      image: '/images/features/feature-kundli.jpg',
      imagePosition: 'center top',
      imageFilter: 'sepia(0.15) brightness(0.95) contrast(1.05)',
      title: l('Kundli — 29 Analysis Modules', 'कुंडली — 29 विश्लेषण मॉड्यूल'),
      subtitle: l('29 Tabs, 3 Systems', '29 टैब, 3 सिस्टम'),
      desc: l(
        'Parashari, Jaimini & KP System in one place. 6 Dasha systems (Vimshottari, Ashtottari, Yogini, Moola, Tara, Kalachakra), 17 Divisional Charts (D1 to D108), KP Horary 1-249, Sarvatobhadra Chakra, Birth Time Rectification, Chart Animation, Ashtakvarga, Shadbala, Sodashvarga, 27 Yogas, 11 Doshas, Kundli Milan — the deepest Vedic analysis available online.',
        'पाराशरी, जैमिनी और केपी एक जगह। 6 दशा पद्धतियाँ (विंशोत्तरी, अष्टोत्तरी, योगिनी, मूल, तारा, कालचक्र), 17 वर्ग कुंडलियाँ (D1 से D108), केपी प्रश्न 1-249, सर्वतोभद्र चक्र, जन्म समय शोधन, चार्ट एनिमेशन, अष्टकवर्ग, षड्बल, 27 योग, 11 दोष — ऑनलाइन सबसे गहन वैदिक विश्लेषण।'
      ),
      badge: l('29 MODULES', '29 मॉड्यूल'),
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
      image: '/images/features/feature-lalkitab.png',
      title: l('Lal Kitab — 20 Tabs + Bunyaad', 'लाल किताब — 20 टैब + बुनियाद'),
      subtitle: l('ONLY HERE', 'केवल यहाँ'),
      desc: l(
        '20-tab Lal Kitab system: Nishaniyan Matcher, Chandra Chalana 43-day protocol, Remedy Tracker, Teva, Masnui Grah, Karmic Rin, Sleeping/Kayam planets, Gochar. NEW: Bunyaad (foundation) analysis, Takkar (1-8 collision) detection, Enemy Siege mapping, 108 per-house interpretations, 5 validated remedies (Mitti ka Kuja, Kanya Pujan, Hanuman Halwa) — the most comprehensive Lal Kitab system available anywhere.',
        '20-टैब लाल किताब: निशानियां, चंद्र चालना, रेमेडी ट्रैकर, तेवा, मसनूई ग्रह, कर्मिक ऋण, गोचर। नया: बुनियाद विश्लेषण, टक्कर (1-8) पहचान, दुश्मन घेराबंदी, 108 भाव-अनुसार फलादेश, 5 प्रमाणित उपाय (मिट्टी का कूजा, कन्या पूजन, हनुमान हलवा) — कहीं भी उपलब्ध सबसे व्यापक लाल किताब प्रणाली।'
      ),
      badge: l('20 TABS', '20 टैब'),
    },
    {
      image: '/images/features/feature-numerology.jpg',
      imagePosition: 'center center',
      imageFilter: 'sepia(0.15) brightness(0.95) contrast(1.05)',
      title: l('Numerology — 7 Analysis Types', 'अंकशास्त्र — 7 विश्लेषण प्रकार'),
      subtitle: l('Complete System', 'पूर्ण प्रणाली'),
      desc: l(
        'Life Path, Expression, Soul Urge, Personality, Birthday, Maturity & Karmic Debt numbers. Pinnacles, Challenges, Personal Year/Month/Day forecast. Lo Shu Grid with Arrows & Planes analysis. Mobile, Vehicle, House & Name numerology — plus daily universal and personal day forecasts.',
        'जीवन पथ, भाग्यांक, आत्मांक, व्यक्तित्व, जन्मदिन, परिपक्वता और कर्मिक ऋण अंक। शिखर, चुनौतियां, व्यक्तिगत वर्ष/माह/दिन पूर्वानुमान। लो शू ग्रिड एरो और प्लेन विश्लेषण। मोबाइल, वाहन, घर और नाम अंकशास्त्र — साथ ही दैनिक सार्वभौमिक और व्यक्तिगत दिन पूर्वानुमान।'
      ),
      badge: l('7 TYPES', '7 प्रकार'),
    },
    {
      image: '/images/features/feature-vastu.jpg',
      imagePosition: 'center center',
      imageFilter: 'sepia(0.15) brightness(0.95) contrast(1.05)',
      title: l('Vastu Shastra Analyzer', 'वास्तु शास्त्र विश्लेषक'),
      subtitle: l('Mandala + Remedies', 'मंडल + उपाय'),
      desc: l(
        '45-Devta Vastu Purusha Mandala scoring with zone-wise energy mapping. 32-entrance Pada analysis, direction optimization for every room, metal remedies (copper, iron, silver, gold), color therapy — for homes and offices.',
        '45-देवता वास्तु पुरुष मंडल स्कोरिंग। 32-प्रवेश पद विश्लेषण, हर कमरे के लिए दिशा अनुकूलन, धातु उपाय (तांबा, लोहा, चांदी, सोना), रंग चिकित्सा — घरों और कार्यालयों के लिए।'
      ),
      badge: l('AI + MANDALA', 'एआई + मंडल'),
    },
  ];


  // ── Numerology helpers ──────────────────────────────────────
  const reduceToSingle = (n: number): number => {
    while (n > 9 && n !== 11 && n !== 22 && n !== 33) {
      n = [...`${n}`].reduce((a, c) => a + parseInt(c), 0);
    }
    return n;
  };

  const digitSum = (n: number): number => {
    return [...`${Math.abs(n)}`].reduce((a, c) => a + parseInt(c), 0);
  };

  const universalDayNumber = (() => {
    const today = new Date();
    const y = today.getFullYear();
    const m = today.getMonth() + 1;
    const d = today.getDate();
    // Match backend logic:
    // UY = reduce(digitSum(year))
    // UM = reduce(UY + digitSum(month))
    // UD = reduce(UM + digitSum(day))
    const uy = reduceToSingle(digitSum(y));
    const um = reduceToSingle(uy + digitSum(m));
    return reduceToSingle(um + digitSum(d));
  })();

  const calcLifePath = (dob: string): number => {
    const [y, m, d] = dob.split('-').map(Number);
    if (!y || !m || !d) return 0;
    return reduceToSingle(reduceToSingle(m) + reduceToSingle(d) + reduceToSingle(y));
  };

  const calcPersonalDay = (dob: string): number => {
    const [, m, d] = dob.split('-').map(Number);
    if (!m || !d) return 0;
    const today = new Date();
    const cm = today.getMonth() + 1;
    const cd = today.getDate();
    const cy = today.getFullYear();
    const personalYear = reduceToSingle(reduceToSingle(m) + reduceToSingle(d) + reduceToSingle(cy));
    return reduceToSingle(reduceToSingle(cm) + reduceToSingle(cd) + reduceToSingle(personalYear));
  };

  const NUMERO_MEANINGS: Record<number, { en: string; hi: string; title_en: string; title_hi: string }> = {
    1: { title_en: 'The Leader', title_hi: 'नेता', en: 'Independent, ambitious, pioneering spirit.', hi: 'स्वतंत्र, महत्वाकांक्षी, अग्रणी भावना।' },
    2: { title_en: 'The Diplomat', title_hi: 'कूटनीतिज्ञ', en: 'Cooperative, sensitive, peacemaking nature.', hi: 'सहयोगी, संवेदनशील, शांतिप्रिय स्वभाव।' },
    3: { title_en: 'The Communicator', title_hi: 'संवादक', en: 'Creative, expressive, joyful energy.', hi: 'रचनात्मक, अभिव्यक्त, आनंदमय ऊर्जा।' },
    4: { title_en: 'The Builder', title_hi: 'निर्माता', en: 'Practical, disciplined, strong foundation.', hi: 'व्यावहारिक, अनुशासित, मज़बूत नींव।' },
    5: { title_en: 'The Adventurer', title_hi: 'साहसी', en: 'Freedom-loving, versatile, dynamic change.', hi: 'स्वतंत्रता-प्रेमी, बहुमुखी, गतिशील परिवर्तन।' },
    6: { title_en: 'The Nurturer', title_hi: 'पालनकर्ता', en: 'Responsible, loving, domestic harmony.', hi: 'जिम्मेदार, स्नेही, पारिवारिक सामंजस्य।' },
    7: { title_en: 'The Seeker', title_hi: 'खोजी', en: 'Spiritual, analytical, introspective depth.', hi: 'आध्यात्मिक, विश्लेषणात्मक, आत्मनिरीक्षण।' },
    8: { title_en: 'The Powerhouse', title_hi: 'शक्तिशाली', en: 'Power, achievement, material success.', hi: 'शक्ति, उपलब्धि, भौतिक सफलता।' },
    9: { title_en: 'The Humanitarian', title_hi: 'मानवतावादी', en: 'Compassionate, wise, universal service.', hi: 'करुणामय, बुद्धिमान, सार्वभौमिक सेवा।' },
    11: { title_en: 'The Intuitive', title_hi: 'अंतर्ज्ञानी', en: 'Master number — visionary, inspiring, spiritually gifted.', hi: 'मास्टर अंक — दूरदर्शी, प्रेरणादायक, आध्यात्मिक।' },
    22: { title_en: 'The Master Builder', title_hi: 'मास्टर निर्माता', en: 'Master number — turns dreams into reality on a grand scale.', hi: 'मास्टर अंक — बड़े पैमाने पर सपनों को साकार करता है।' },
    33: { title_en: 'The Master Teacher', title_hi: 'मास्टर गुरु', en: 'Master number — selfless service, spiritual upliftment.', hi: 'मास्टर अंक — निःस्वार्थ सेवा, आध्यात्मिक उत्थान।' },
  };

  const PERSONAL_DAY_MEANINGS: Record<number, { en: string; hi: string }> = {
    1: { en: 'New beginnings and bold action.', hi: 'नई शुरुआत और साहसिक कदम।' },
    2: { en: 'Partnership, patience, and diplomacy.', hi: 'साझेदारी, धैर्य और कूटनीति।' },
    3: { en: 'Self-expression and social connections.', hi: 'आत्म-अभिव्यक्ति और सामाजिक संबंध।' },
    4: { en: 'Hard work, planning, and building.', hi: 'कड़ी मेहनत, योजना और निर्माण।' },
    5: { en: 'Expect changes and adventure!', hi: 'बदलाव और रोमांच की उम्मीद करें!' },
    6: { en: 'Family, responsibility, and love.', hi: 'परिवार, जिम्मेदारी और प्रेम।' },
    7: { en: 'Reflection, study, and inner wisdom.', hi: 'चिंतन, अध्ययन और आंतरिक ज्ञान।' },
    8: { en: 'Money matters and power moves.', hi: 'धन के मामले और शक्ति कदम।' },
    9: { en: 'Completion, compassion, and letting go.', hi: 'पूर्णता, करुणा और समर्पण।' },
    11: { en: 'Heightened intuition and inspiration.', hi: 'उन्नत अंतर्ज्ञान और प्रेरणा।' },
    22: { en: 'Manifest big visions into reality.', hi: 'बड़े सपनों को वास्तविकता में बदलें।' },
    33: { en: 'Selfless service and spiritual healing.', hi: 'निःस्वार्थ सेवा और आध्यात्मिक उपचार।' },
  };

  const handleNumeroSubmit = () => {
    if (!numeroDob) return;
    const lp = calcLifePath(numeroDob);
    const pd = calcPersonalDay(numeroDob);
    if (lp > 0) setNumeroResult({ lifePath: lp, personalDay: pd });
  };

  const universalMeaning = NUMERO_MEANINGS[universalDayNumber] || NUMERO_MEANINGS[1];

  useEffect(() => {
    if (gsap.globalTimeline.timeScale() === 0) return;
    const ctx = gsap.context(() => {
      gsap.fromTo('.features-title', { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 0.8, ease: 'power3.out', scrollTrigger: { trigger: sectionRef.current, start: 'top 80%' } });
      gsap.fromTo('.feature-card', { y: 80, opacity: 0 }, { y: 0, opacity: 1, duration: 0.8, stagger: 0.1, ease: 'power3.out', scrollTrigger: { trigger: sectionRef.current, start: 'top 70%' } });
      gsap.fromTo('.numero-section', { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.8, ease: 'power3.out', scrollTrigger: { trigger: '.numero-section', start: 'top 80%' } });
    }, sectionRef);
    return () => ctx.revert();
  }, []);

  return (
    <>
    <section ref={sectionRef} id="features" className="relative pt-4 pb-24 bg-background">

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Live Planetary Positions (Gochar) */}
        {currentSky && (
          <div id="present-kundli-section" className="features-title mb-12">
            <Heading as={2} variant={2} className="text-sacred-gold-dark mb-6 leading-[1.1] text-center">
              {l('Live Planetary Positions (Gochar)', 'लाइव ग्रह स्थिति (गोचर)')}
            </Heading>
            <LiveClock language={language} />

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">
              {/* LEFT: Chart */}
              <div className="flex flex-col items-center -mt-[5px]">
                <div className="w-full max-w-[480px] aspect-square">
                  <KundliChartSVG
                    planets={(currentSky.planets || []).map((p: any) => {
                      const SIGNS_ORDER = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces'];
                      const lagnaIdx = SIGNS_ORDER.indexOf(currentSky.lagna_sign || '');
                      const planetIdx = SIGNS_ORDER.indexOf(p.sign || '');
                      const house = lagnaIdx >= 0 && planetIdx >= 0 ? ((planetIdx - lagnaIdx + 12) % 12) + 1 : (p.house || 0);

                      // Compute statuses from sign (API doesn't send these)
                      const EXALTED: Record<string,string> = {Sun:'Aries',Moon:'Taurus',Mars:'Capricorn',Mercury:'Virgo',Jupiter:'Cancer',Venus:'Pisces',Saturn:'Libra'};
                      const DEBILITATED: Record<string,string> = {Sun:'Libra',Moon:'Scorpio',Mars:'Cancer',Mercury:'Pisces',Jupiter:'Capricorn',Venus:'Virgo',Saturn:'Aries'};
                      const sign = p.sign || '';
                      const name = p.planet || '';

                      // Combust: planet within ~10° of Sun (except Rahu/Ketu)
                      const sunData = (currentSky.planets || []).find((s: any) => s.planet === 'Sun');
                      const sunLong = sunData?.longitude ?? -999;
                      const pLong = p.longitude ?? -999;
                      const diff = Math.abs(pLong - sunLong);
                      const angDiff = diff > 180 ? 360 - diff : diff;
                      const isCombust = name !== 'Sun' && name !== 'Rahu' && name !== 'Ketu' && angDiff < 10;

                      // Use API values first, fallback to frontend computation
                      const status = (p.status || '').toLowerCase();
                      return {
                        planet: name,
                        sign,
                        house,
                        sign_degree: p.sign_degree || 0,
                        is_retrograde: !!p.is_retrograde || status.includes('retrograde'),
                        is_combust: !!p.is_combust || isCombust || status.includes('combust'),
                        is_vargottama: !!p.is_vargottama || status.includes('vargottama'),
                        is_exalted: EXALTED[name] === sign || status.includes('exalted'),
                        is_debilitated: DEBILITATED[name] === sign || status.includes('debilitated'),
                      };
                    })}
                    ascendantSign={currentSky.lagna_sign || ''}
                    ascendantDegree={currentSky.lagna_longitude || currentSky.chart_data?.ascendant?.longitude}
                    language={language}
                  />
                </div>
              </div>

              {/* RIGHT: Planet Details */}
              <div>
                <div className="rounded-xl border border-sacred-gold/20 bg-transparent backdrop-blur-[1px] overflow-hidden">
                  <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center justify-between">
                    <span>{l('Planetary Positions', 'ग्रह स्थिति')}</span>
                    <span className="text-xs font-normal opacity-80">{l('Lagna', 'लग्न')}: {hi ? (SIGN_HI[currentSky.lagna_sign] || currentSky.lagna_sign) : currentSky.lagna_sign}</span>
                  </div>
                  <table className="table-sacred w-full text-sm">
                    <thead>
                      <tr className="bg-sacred-gold/10 text-sacred-gold-dark text-xs uppercase tracking-wider">
                        <th className="text-left px-3 py-2">{l('Planet', 'ग्रह')}</th>
                        <th className="text-left px-3 py-2">{l('Sign', 'राशि')}</th>
                        <th className="text-right px-3 py-2">{l('Degree', 'अंश')}</th>
                        <th className="text-right px-3 py-2">{l('Longitude', 'रेखांश')}</th>
                        <th className="text-center px-3 py-2">{l('R', 'वक्री')}</th>
                      </tr>
                    </thead>
                    <tbody>
                      {/* Ascendant row */}
                      <tr className="border-b border-sacred-gold/20 bg-sacred-gold/[0.06]">
                        <td className="px-3 py-2 font-bold text-sacred-gold-dark">{l('Ascendant', 'लग्न')}</td>
                        <td className="px-3 py-2 font-semibold text-sacred-gold-dark">{hi ? (SIGN_HI[currentSky.lagna_sign] || currentSky.lagna_sign || '--') : (currentSky.lagna_sign || '--')}</td>
                        <td className="px-3 py-2 text-right text-muted-foreground">
                          {currentSky.chart_data?.ascendant?.sign_degree != null ? `${currentSky.chart_data.ascendant.sign_degree}°` : '--'}
                        </td>
                        <td className="px-3 py-2 text-right text-muted-foreground">
                          {currentSky.chart_data?.ascendant?.longitude != null ? `${Number(currentSky.chart_data.ascendant.longitude).toFixed(2)}°` : '--'}
                        </td>
                        <td className="px-3 py-2 text-center">--</td>
                      </tr>
                      {(currentSky.planets || []).map((p: any, i: number) => {
                        const planetColor = PLANET_COLORS[p.planet] || '#888';
                        const planetLabel = hi ? (PLANET_HI[p.planet] || p.planet) : p.planet;
                        const signLabel = hi ? (SIGN_HI[p.sign] || p.sign) : p.sign;
                        const tooltipText = `${planetLabel} ${l('in', 'में')} ${signLabel} (${l('Transit', 'गोचर')})`;
                        return (
                        <tr key={p.planet} title={tooltipText} className={`border-b border-sacred-gold/10 cursor-default ${i % 2 === 0 ? 'bg-sacred-gold/[0.03]' : ''} hover:bg-sacred-gold/10 transition-colors`}>
                          <td className="px-3 py-2 font-semibold text-foreground">
                            <span className="inline-flex items-center gap-1.5">
                              <span className="w-2.5 h-2.5 rounded-full shrink-0" style={{ backgroundColor: planetColor }} />
                              {planetLabel}
                            </span>
                          </td>
                          <td className="px-3 py-2 text-foreground">{signLabel}</td>
                          <td className="px-3 py-2 text-right text-muted-foreground">{p.sign_degree != null ? `${p.sign_degree}°` : '--'}</td>
                          <td className="px-3 py-2 text-right text-muted-foreground">{p.longitude != null ? `${Number(p.longitude).toFixed(2)}°` : '--'}</td>
                          <td className="px-3 py-2 text-center text-xs font-bold">
                            {(() => {
                              const st = (p.status || '').toLowerCase();
                              const parts: string[] = [];
                              if (p.is_retrograde || st.includes('retrograde')) parts.push('*');
                              if (p.is_combust || st.includes('combust')) parts.push('^');
                              if (st.includes('vargottama')) parts.push('v');
                              if (st.includes('exalted')) parts.push('+');
                              if (st.includes('debilitated')) parts.push('-');
                              return parts.length ? <span className="text-sacred-gold-dark">{parts.join('')}</span> : <span className="text-muted-foreground">--</span>;
                            })()}
                          </td>
                        </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>

            {/* Legend — below chart, full width, same as transit wheel */}
            <div className="rounded-lg bg-sacred-gold/5 px-3 py-1.5 mt-3 text-sm text-center" style={{ fontFamily: 'Inter,sans-serif', color: '#C4611F' }}>
              <span className="flex items-center justify-center gap-4 flex-wrap">
                <span className="flex items-center gap-1"><span className="font-bold" style={{ color: '#C4611F' }}>*</span>{l('Retro', 'वक्री')}</span>
                <span className="flex items-center gap-1"><span className="font-bold" style={{ color: '#C4611F' }}>^</span>{l('Combust', 'अस्त')}</span>
                <span className="flex items-center gap-1"><span className="font-bold" style={{ color: '#C4611F' }}>v</span>{l('Vargottama', 'वर्गोत्तम')}</span>
                <span className="flex items-center gap-1"><span className="font-bold" style={{ color: '#059669' }}>+</span>{l('Exalted', 'उच्च')}</span>
                <span className="flex items-center gap-1"><span className="font-bold" style={{ color: '#DC2626' }}>-</span>{l('Debilitated', 'नीच')}</span>
              </span>
              <span className="flex items-center justify-center gap-4 flex-wrap mt-0.5">
                <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full inline-block" style={{ background: '#C4611F' }} />{l('Benefic', 'शुभ')}</span>
                <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full inline-block" style={{ background: '#1a1a2e' }} />{l('Malefic', 'पापी')}</span>
                <span className="flex items-center gap-1"><span style={{ color: '#C4611F' }}>▲</span>{l('ASC', 'लग्न')}</span>
              </span>
            </div>

            {/* Today's Planetary Influence */}
            {(() => {
              const insights = computeDailyInsights(currentSky.planets || [], language);
              if (insights.length === 0) return null;
              return (
                <div className="mt-5 rounded-xl border border-sacred-gold/30 bg-sacred-gold/5 p-4">
                  <div className="flex items-center gap-2 mb-3">
                    <Sparkles className="w-4 h-4 text-sacred-gold-dark shrink-0" />
                    <h3 className="text-sm font-semibold text-sacred-gold-dark uppercase tracking-wide">
                      {l("Today's Planetary Influence", 'आज का ग्रह प्रभाव')}
                    </h3>
                  </div>
                  <ul className="space-y-2">
                    {insights.map((insight, idx) => (
                      <li key={idx} className="flex items-start gap-2 text-sm text-foreground">
                        <span className="text-sacred-gold-dark mt-0.5 shrink-0">•</span>
                        <span>{insight}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              );
            })()}
          </div>
        )}

        {/* ── Prashna Kundli ── */}
        <div id="prashna-section" className="features-title mb-16">
          <div className="text-center mb-8">
            <Heading as={2} variant={2} className="text-sacred-gold-dark mb-2 leading-[1.1]">
              {l('Prashna Kundli', 'प्रश्न कुंडली')}
            </Heading>
            <p className="text-gray-600 max-w-xl mx-auto text-sm leading-relaxed">
              {l('No birth details needed. Ask any life question — get an instant KP Horary answer, free.',
                 'जन्म विवरण की जरूरत नहीं। कोई भी जीवन प्रश्न पूछें — तुरंत KP होरेरी उत्तर, मुफ्त।')}
            </p>
          </div>

          <div className="max-w-xl mx-auto">
            <div className="rounded-2xl border border-sacred-gold/30 bg-gradient-to-br from-[#FFF9F5] to-white shadow-sm p-6">
              {/* Question selector */}
              <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-2">
                {l('What is your question about?', 'आपका सवाल किस बारे में है?')}
              </p>
              <div className="grid grid-cols-5 gap-2 mb-5">
                {PRASHNA_QUESTIONS.map(q => (
                  <button key={q.key} onClick={() => setPrashnaQ(q.key)}
                    className={`py-2 px-1 rounded-xl text-center transition-all text-xs font-semibold ${
                      prashnaQ === q.key
                        ? 'bg-sacred-gold-dark text-white shadow-sm'
                        : 'border border-sacred-gold/35 text-foreground hover:bg-sacred-gold/10'
                    }`}>
                    <span className="block text-base mb-0.5">{q.emoji}</span>
                    {l(q.en, q.hi)}
                  </button>
                ))}
              </div>

              {/* City input */}
              <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-2">
                {l('Your city', 'आपका शहर')}
              </p>
              <div className="relative mb-4">
                <MapPin className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-sacred-gold-dark/50 pointer-events-none" />
                <input type="text" value={prashnaCity}
                  onChange={e => searchPrashnaCity(e.target.value)}
                  placeholder={l('Search city…', 'शहर खोजें…')}
                  className="input-sacred pl-9 pr-3 placeholder:text-muted-foreground/50" />
                {prashnaSuggs.length > 0 && (
                  <div className="absolute left-0 right-0 top-full z-20 bg-white border border-sacred-gold/20 rounded-lg shadow-lg max-h-40 overflow-y-auto mt-1">
                    {prashnaSuggs.map((s, i) => (
                      <button key={i} onClick={() => { setPrashnaCity(s.name.split(',')[0]); setPrashnaLat(s.lat); setPrashnaLon(s.lon); setPrashnaSuggs([]); }}
                        className="w-full text-left px-3 py-2 text-xs hover:bg-sacred-gold/10 transition-colors">
                        {s.name}
                      </button>
                    ))}
                  </div>
                )}
              </div>

              {/* Ask button */}
              <button onClick={askPrashna} disabled={prashnaLoading || !prashnaCity.trim()}
                className="w-full py-2.5 rounded-xl font-semibold bg-sacred-gold hover:bg-sacred-gold-dark text-white flex items-center justify-center gap-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed">
                {prashnaLoading
                  ? <><Loader2 className="w-4 h-4 animate-spin" />{l('Calculating…', 'गणना हो रही है…')}</>
                  : <><Sparkles className="w-4 h-4" />{l('Ask the Stars', 'तारों से पूछें')}</>
                }
              </button>

              {prashnaResult && <PrashnaResultCard result={prashnaResult} l={l} />}
            </div>
            <p className="text-center text-[11px] text-muted-foreground mt-3">
              {l('Powered by KP Horary — Krishnamurti Paddhati classical system',
                 'KP होरेरी द्वारा संचालित — कृष्णमूर्ति पद्धति शास्त्रीय प्रणाली')}
            </p>
          </div>
        </div>

        {/* ── Don't Know Birth Time? ── */}
        <div id="unknown-birth-time-section" className="features-title mb-16">
          <div className="rounded-2xl overflow-hidden border border-sacred-gold/25 shadow-sm bg-gradient-to-br from-amber-50/60 to-white">
            {/* Header */}
            <div className="p-6 text-center border-b border-sacred-gold/15 bg-gradient-to-r from-amber-50 to-orange-50/40">
              <div className="inline-flex items-center gap-2 bg-amber-100 text-amber-800 text-xs font-semibold px-3 py-1.5 rounded-full mb-3">
                <HelpCircle className="w-3.5 h-3.5" />
                {l("Don't know your birth time?", "जन्म समय नहीं पता?")}
              </div>
              <Heading as={2} variant={2} className="text-sacred-gold-dark mb-2 leading-[1.1]">
                {l('Still Get Accurate Insights', 'फिर भी सटीक ज्योतिष पाएं')}
              </Heading>
              <p className="text-gray-600 text-sm max-w-lg mx-auto leading-relaxed">
                {l("30–40% of people don't know their exact birth time. These three paths give you powerful Vedic astrology without it.",
                   "30–40% लोगों को अपना जन्म समय नहीं पता। इन तीन रास्तों से बिना जन्म समय के भी ज्योतिष का पूरा लाभ उठाएं।")}
              </p>
            </div>

            {/* Three cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 divide-y md:divide-y-0 md:divide-x divide-sacred-gold/15">
              {/* Moon Kundli */}
              <a href="/kundli?mode=moon" className="p-6 hover:bg-amber-50/60 transition-colors group block">
                <div className="w-10 h-10 rounded-xl bg-blue-100 text-blue-600 flex items-center justify-center mb-3">
                  <Moon className="w-5 h-5" />
                </div>
                <span className="inline-block bg-emerald-100 text-emerald-700 text-[10px] font-semibold px-2 py-0.5 rounded mb-2">
                  {l('Free', 'मुफ्त')}
                </span>
                <h3 className="font-bold text-foreground mb-1.5 text-base">{l('Moon Kundli', 'चंद्र कुंडली')}</h3>
                <p className="text-xs text-muted-foreground leading-relaxed mb-3">
                  {l("Have your DOB but not the time? Moon chart gives emotional patterns, Dasha timeline, and life predictions — no birth time needed.",
                     "DOB है पर समय नहीं? चंद्र कुंडली से भावनात्मक पैटर्न, दशा और जीवन भविष्यवाणी मिलेगी।")}
                </p>
                <span className="text-sacred-gold-dark text-xs font-semibold flex items-center gap-1 group-hover:gap-2 transition-all">
                  {l('Get Moon Kundli', 'चंद्र कुंडली पाएं')} →
                </span>
              </a>

              {/* Ask a Question */}
              <a href="/kundli?mode=horary"
                className="p-6 hover:bg-amber-50/60 transition-colors group block">
                <div className="w-10 h-10 rounded-xl bg-purple-100 text-purple-600 flex items-center justify-center mb-3">
                  <MessageCircle className="w-5 h-5" />
                </div>
                <span className="inline-block bg-emerald-100 text-emerald-700 text-[10px] font-semibold px-2 py-0.5 rounded mb-2">
                  {l('Free', 'मुफ्त')}
                </span>
                <h3 className="font-bold text-foreground mb-1.5 text-base">{l('Ask a Question', 'सवाल पूछें')}</h3>
                <p className="text-xs text-muted-foreground leading-relaxed mb-3">
                  {l("No DOB needed at all. Ask about marriage, career, finance, or health using Prashna Kundli — instant KP Horary answer.",
                     "DOB की भी जरूरत नहीं। विवाह, करियर, वित्त या स्वास्थ्य के बारे में प्रश्न कुंडली से तुरंत उत्तर पाएं।")}
                </p>
                <span className="text-sacred-gold-dark text-xs font-semibold flex items-center gap-1 group-hover:gap-2 transition-all">
                  {l('Ask Now', 'अभी पूछें')} →
                </span>
              </a>

              {/* Birth Rectification */}
              <a href="/kundli?mode=rectification" className="p-6 hover:bg-amber-50/60 transition-colors group block">
                <div className="w-10 h-10 rounded-xl bg-orange-100 text-orange-600 flex items-center justify-center mb-3">
                  <Clock className="w-5 h-5" />
                </div>
                <span className="inline-block bg-amber-100 text-amber-700 text-[10px] font-semibold px-2 py-0.5 rounded mb-2">
                  {l('Premium', 'प्रीमियम')}
                </span>
                <h3 className="font-bold text-foreground mb-1.5 text-base">{l('Birth Rectification', 'जन्म समय शुद्धि')}</h3>
                <p className="text-xs text-muted-foreground leading-relaxed mb-3">
                  {l("Know an approximate time + key life events? Our engine pinpoints your exact birth time using advanced rectification techniques.",
                     "अनुमानित समय और जीवन की प्रमुख घटनाएं पता हैं? हमारा इंजन उन्नत तकनीक से सटीक जन्म समय निकाल सकता है।")}
                </p>
                <span className="text-sacred-gold-dark text-xs font-semibold flex items-center gap-1 group-hover:gap-2 transition-all">
                  {l('Explore', 'जानें')} →
                </span>
              </a>
            </div>
          </div>
        </div>

        {/* Horoscope (Compact) */}
        <div id="horoscope-section" className="features-title mb-12">
          <Heading as={2} variant={2} className="text-sacred-gold-dark mb-6 leading-[1.1] text-center">
            {l('Horoscope', 'राशिफल')}
          </Heading>
          <div className="max-w-full mx-auto text-lg text-gray-600 leading-relaxed mb-6 text-center">

            <p><strong className="text-sacred-gold-dark">{l('Astro Rattan aligns sign forecasts with real planetary context and period logic', 'Astro Rattan वास्तविक ग्रह स्थिति और पीरियड लॉजिक के साथ राशिफल को संरेखित करता है')}</strong>{l(' — giving clearer daily, weekly, monthly, and yearly guidance.', ' — जिससे दैनिक, साप्ताहिक, मासिक और वार्षिक मार्गदर्शन अधिक स्पष्ट मिलता है।')}</p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-5 gap-4">
            {/* LEFT: 4x3 Sign Grid (40%) */}
            <div className="lg:col-span-2 rounded-xl border border-sacred-gold/20 bg-transparent backdrop-blur-[1px] p-3">
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
                      alt={language === 'hi' ? s.hi : s.en}
                      className="w-10 h-10 object-contain"
                      loading="lazy"
                    />
                    <span className="font-medium">{language === 'hi' ? s.hi : s.en}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* RIGHT: Tabs + Prediction (60%) */}
            <div className="lg:col-span-3 flex flex-col gap-3">
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
                      <div className="flex items-center gap-2">
                        <p className="text-base font-semibold text-foreground">
                          {language === 'hi' ? (horoscopeData?.sign_hindi || '') : (horoscopeData?.sign || horoscopeSign).toString().replace(/^./, c => c.toUpperCase())}
                        </p>
                        {horoscopeData?.scores?.overall != null && (
                          <span className="inline-flex items-center gap-0.5 rounded-full bg-amber-100 text-amber-800 px-1.5 py-0.5 text-xs font-semibold">
                            <Star className="w-3 h-3" />
                            {horoscopeData.scores.overall}/10
                          </span>
                        )}
                      </div>
                      <p className="text-xs text-muted-foreground">{horoscopeData?.dates || ''}</p>
                    </div>
                    <div className="space-y-1.5 text-sm text-foreground">
                      <p><span className="font-semibold text-sacred-gold-dark">{l('General', 'सामान्य')}:</span> {compactLine(horoscopeData?.sections?.general, l('Guidance will update shortly.', 'मार्गदर्शन शीघ्र अपडेट होगा।'), language)}</p>
                      <p><span className="font-semibold text-sacred-gold-dark">{l('Love', 'प्रेम')}:</span> {compactLine(horoscopeData?.sections?.love, l('Guidance will update shortly.', 'मार्गदर्शन शीघ्र अपडेट होगा।'), language)}</p>
                      <p><span className="font-semibold text-sacred-gold-dark">{l('Career', 'करियर')}:</span> {compactLine(horoscopeData?.sections?.career, l('Guidance will update shortly.', 'मार्गदर्शन शीघ्र अपडेट होगा।'), language)}</p>
                      <p><span className="font-semibold text-sacred-gold-dark">{l('Health', 'स्वास्थ्य')}:</span> {compactLine(horoscopeData?.sections?.health, l('Guidance will update shortly.', 'मार्गदर्शन शीघ्र अपडेट होगा।'), language)}</p>
                      <p><span className="font-semibold text-sacred-gold-dark">{l('Finance', 'वित्त')}:</span> {compactLine(horoscopeData?.sections?.finance, l('Guidance will update shortly.', 'मार्गदर्शन शीघ्र अपडेट होगा।'), language)}</p>
                    </div>
                  </>
                )}
              </div>
            </div>
          </div>
          <div className="flex justify-end mt-3">
            <a href="/horoscope" className="text-sm text-sacred-gold-dark hover:underline font-medium flex items-center gap-1">
              {l('Click here to view more in detail', 'विस्तार से देखने के लिए यहां क्लिक करें')} →
            </a>
          </div>
        </div>

        {/* Panchang Section */}
        <div id="panchang-section" className="features-title mb-12">
          <Heading as={2} variant={2} className="text-sacred-gold-dark mb-6 leading-[1.1] text-center">
            {l('Panchang', 'पंचांग')}
          </Heading>
          <div className="max-w-full mx-auto text-lg text-gray-600 leading-relaxed mb-6 text-center">

            <p><strong className="text-sacred-gold-dark">{l('Astro Rattan computes Tithi, Nakshatra, Yoga, Karana end times using Swiss Ephemeris for YOUR exact coordinates', 'Astro Rattan आपके सटीक निर्देशांकों के लिए स्विस एफेमेरिस का उपयोग करके तिथि, नक्षत्र, योग, करण के अंत समय की गणना करता है')}</strong>{l(' — with 12+ Muhurat windows, Hora table, Choghadiya, and Hindu calendar.', ' — 12+ मुहूर्त, होरा तालिका, चौघड़िया और हिंदू कैलेंडर के साथ।')}</p>
          </div>

          {/* Compact Daily Snapshot — best time, avoid time, tip + planetary influence */}
          {(panchangData || currentSky) && (() => {
            const bestTime = panchangData?.abhijit_muhurat || panchangData?.brahma_muhurat;
            const rahuKaal = panchangData?.rahu_kaal;
            const tithi = (panchangData?.tithi?.name || '').toLowerCase();
            const tip = tithi.includes('ekadashi')
              ? l('Fasting Day', 'व्रत का दिन')
              : tithi.includes('chaturthi')
              ? l('Ganesha Worship', 'गणेश पूजा')
              : tithi.includes('purnima') || tithi.includes('amavasya')
              ? l('Ancestor Worship', 'पितृ पूजन')
              : tithi.includes('pradosh')
              ? l('Shiva Worship', 'शिव पूजा')
              : l('Good for Regular Work', 'सामान्य कार्यों के लिए अच्छा');
            const insights = computeDailyInsights(currentSky?.planets || [], language);
            if (!bestTime && !rahuKaal && insights.length === 0) return null;
            const energy = computeDayEnergy(insights);
            const todayLabel = new Date().toLocaleDateString(language === 'hi' ? 'hi-IN' : 'en-IN', { weekday: 'short', day: 'numeric', month: 'short' });
            const tithiLabel = panchangData?.tithi?.name;
            const nakshatraLabel = panchangData?.nakshatra?.name;
            return (
              <div className="mb-6 rounded-xl border border-sacred-gold/20 bg-sacred-gold/[0.02] p-4">
                {/* Context header */}
                <div className="flex items-center justify-between mb-3 pb-2.5 border-b border-sacred-gold/15">
                  <div className="flex flex-wrap items-center gap-1.5 text-sm text-muted-foreground">
                    <Calendar className="w-4 h-4 text-sacred-gold-dark shrink-0" />
                    <span className="font-medium text-foreground">{hi ? 'आज का सारांश' : "Today's Snapshot"}</span>
                    <span>·</span>
                    <span>{todayLabel}</span>
                    {tithiLabel && <><span>·</span><span>{tithiLabel}</span></>}
                    {nakshatraLabel && <><span>·</span><span>{nakshatraLabel}</span></>}
                  </div>
                  <span className="shrink-0 text-sm font-medium px-2 py-0.5 rounded-full bg-sacred-gold/10 text-sacred-gold-dark">
                    {hi ? energy.hi : energy.en}
                  </span>
                </div>
                <div className="flex flex-wrap gap-2 mb-3">
                  {bestTime && (bestTime.start !== '--:--') && (
                    <div className="flex items-center gap-1.5 bg-green-50 border border-green-200 rounded-lg px-3 py-1.5 text-sm">
                      <span className="text-green-600 font-bold text-base leading-none">✓</span>
                      <span className="text-green-800 font-medium">{l('Best Time', 'सर्वश्रेष्ठ')}: {bestTime.start}–{bestTime.end}</span>
                    </div>
                  )}
                  {rahuKaal && (rahuKaal.start !== '--:--') && (
                    <div className="flex items-center gap-1.5 bg-orange-50 border border-orange-200 rounded-lg px-3 py-1.5 text-sm">
                      <span className="text-orange-500 font-bold text-base leading-none">⚠</span>
                      <span className="text-orange-800 font-medium">{l('Avoid', 'बचें')} (Rahu Kaal): {rahuKaal.start}–{rahuKaal.end}</span>
                    </div>
                  )}
                  <div className="flex items-center gap-1.5 bg-blue-50 border border-blue-200 rounded-lg px-3 py-1.5 text-sm">
                    <span className="text-blue-600 font-bold text-base leading-none">→</span>
                    <span className="text-blue-800 font-medium">{tip}</span>
                  </div>
                </div>
                {insights.length > 0 && (
                  <>
                    <div className="flex items-center gap-1.5 mb-2">
                      <Sparkles className="w-3.5 h-3.5 text-sacred-gold-dark shrink-0" />
                      <span className="text-xs font-semibold text-sacred-gold-dark uppercase tracking-wide">
                        {l("Today's Planetary Influence", 'आज का ग्रह प्रभाव')}
                      </span>
                    </div>
                    <ul className="flex flex-wrap gap-x-5 gap-y-1">
                      {insights.map((insight, idx) => (
                        <li key={idx} className="flex items-start gap-1.5 text-xs text-foreground">
                          <span className="text-sacred-gold-dark shrink-0 mt-0.5">•</span>
                          <span>{insight}</span>
                        </li>
                      ))}
                    </ul>
                  </>
                )}
              </div>
            );
          })()}

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 lg:h-[620px]">
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
        <div id="hora-section" />
        {panchangData && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-12">
            {/* Hora Table */}
            {panchangData.hora_table && panchangData.hora_table.length > 0 && (
              <div className="rounded-xl border border-sacred-gold/20 bg-transparent backdrop-blur-[1px] shadow-sm overflow-hidden">
                <div className="bg-sacred-gold-dark text-white px-3 py-2 text-[15px] font-semibold">
                  {l('Hora Table', 'होरा तालिका')}
                </div>
                <div className="p-2.5 max-h-[400px] overflow-y-auto">
                  <table className="table-sacred w-full text-sm">
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
                          <td className="px-2 py-1.5 text-foreground">{hi ? (PLANET_HI[h.lord] || h.lord) : h.lord}</td>
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
                  <table className="table-sacred w-full text-sm">
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
                            <td className="px-2 py-1.5 font-medium text-foreground">{hi ? (CHOGHADIYA_HI[c.name] || c.name) : c.name}</td>
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
                            <td className="px-2 py-1.5 font-medium text-foreground">{hi ? (CHOGHADIYA_HI[c.name] || c.name) : c.name} <span className="text-[10px] text-indigo-500">{l('(Night)', '(रात)')}</span></td>
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
        <div className="flex justify-end mt-3 mb-8">
          <a href="/panchang" className="text-sm text-sacred-gold-dark hover:underline font-medium flex items-center gap-1">
            {l('Click here to view more in detail', 'विस्तार से देखने के लिए यहां क्लिक करें')} →
          </a>
        </div>

        {/* ── Today's Numerology — Quick Widget ──────────────────── */}
        <div id="numerology-widget" className="numero-section features-title mb-12">
          <Heading as={2} variant={2} className="text-sacred-gold-dark mb-6 leading-[1.1] text-center">
            {l("Today's Numerology", 'आज का अंकशास्त्र')}
          </Heading>
          <div className="max-w-full mx-auto text-lg text-gray-600 leading-relaxed mb-6 text-center">
            <p>
              <strong className="text-sacred-gold-dark">
                {l('Discover how numbers shape your day', 'जानें कैसे अंक आपका दिन बनाते हैं')}
              </strong>
              {l(' — enter your date of birth and get instant insights. No login required.', ' — अपनी जन्मतिथि दर्ज करें और तुरंत जानकारी पाएं। लॉगिन की जरूरत नहीं।')}
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-5 gap-6 items-start">
            {/* LEFT: Universal Day + Quick Calculator (3 cols) */}
            <div className="lg:col-span-3 space-y-4">
              {/* Universal Day Number */}
              <div className="rounded-xl border border-sacred-gold/20 bg-transparent backdrop-blur-[1px] shadow-sm overflow-hidden">
                <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
                  {l('Universal Day Number', 'सार्वभौमिक दिन अंक')}
                </div>
                <div className="p-4 flex items-center gap-4">
                  <div className="w-16 h-16 rounded-full bg-gradient-to-br from-sacred-gold to-sacred-gold-dark flex items-center justify-center shrink-0 shadow-lg shadow-sacred-gold/30">
                    <span className="text-3xl font-bold text-white">{universalDayNumber}</span>
                  </div>
                  <div>
                    <p className="text-base font-semibold text-foreground">
                      {l(`Today is a Universal Day ${universalDayNumber}`, `आज सार्वभौमिक दिन ${universalDayNumber} है`)}
                      {' — '}
                      <span className="text-sacred-gold-dark">{l(universalMeaning.title_en, universalMeaning.title_hi)}</span>
                    </p>
                    <p className="text-sm text-muted-foreground mt-0.5">
                      {l(universalMeaning.en, universalMeaning.hi)}
                    </p>
                  </div>
                </div>
              </div>

              {/* Quick Calculator */}
              <div className="rounded-xl border border-sacred-gold/20 bg-transparent backdrop-blur-[1px] shadow-sm overflow-hidden">
                <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
                  {l("What's Your Number?", 'आपका अंक क्या है?')}
                </div>
                <div className="p-4">
                  <div className="flex flex-col sm:flex-row gap-3 items-start sm:items-end">
                    <div className="flex-1 w-full">
                      <label className="text-sm font-medium text-foreground mb-1 block">
                        {l('Date of Birth', 'जन्म तिथि')}
                      </label>
                      <input
                        type="date"
                        value={numeroDob}
                        onChange={(e) => {
                          setNumeroDob(e.target.value);
                          setNumeroResult(null);
                        }}
                        max={new Date().toISOString().split('T')[0]}
                        className="w-full px-3 py-2.5 text-sm border border-sacred-gold/30 rounded-lg focus:outline-none focus:border-sacred-gold focus:ring-1 focus:ring-sacred-gold/30 text-[#333] bg-white"
                      />
                    </div>
                    <button
                      type="button"
                      onClick={handleNumeroSubmit}
                      disabled={!numeroDob}
                      className="px-6 py-2.5 bg-sacred-gold-dark text-white rounded-lg font-semibold text-sm hover:bg-sacred-gold transition-all disabled:opacity-40 disabled:cursor-not-allowed shadow-md shadow-sacred-gold/20 whitespace-nowrap"
                    >
                      {l('Calculate', 'गणना करें')}
                    </button>
                  </div>

                  {/* Results */}
                  {numeroResult && (
                    <div className="mt-4 space-y-3">
                      {/* Life Path */}
                      <div className="rounded-lg border border-sacred-gold/15 bg-sacred-gold/[0.04] p-3">
                        <div className="flex items-center gap-3">
                          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-sacred-gold to-sacred-gold-dark flex items-center justify-center shrink-0">
                            <span className="text-lg font-bold text-white">{numeroResult.lifePath}</span>
                          </div>
                          <div>
                            <p className="text-sm font-semibold text-foreground">
                              {l(`Your Life Path is ${numeroResult.lifePath}`, `आपका मूलांक ${numeroResult.lifePath} है`)}
                              {' — '}
                              <span className="text-sacred-gold-dark">
                                {l(
                                  (NUMERO_MEANINGS[numeroResult.lifePath] || NUMERO_MEANINGS[1]).title_en,
                                  (NUMERO_MEANINGS[numeroResult.lifePath] || NUMERO_MEANINGS[1]).title_hi
                                )}
                              </span>
                            </p>
                            <p className="text-xs text-muted-foreground">
                              {l(
                                (NUMERO_MEANINGS[numeroResult.lifePath] || NUMERO_MEANINGS[1]).en,
                                (NUMERO_MEANINGS[numeroResult.lifePath] || NUMERO_MEANINGS[1]).hi
                              )}
                            </p>
                          </div>
                        </div>
                      </div>

                      {/* Personal Day */}
                      <div className="rounded-lg border border-sacred-gold/15 bg-sacred-gold/[0.04] p-3">
                        <div className="flex items-center gap-3">
                          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-amber-500 to-amber-700 flex items-center justify-center shrink-0">
                            <span className="text-lg font-bold text-white">{numeroResult.personalDay}</span>
                          </div>
                          <div>
                            <p className="text-sm font-semibold text-foreground">
                              {l(`Your Personal Day is ${numeroResult.personalDay}`, `आपका व्यक्तिगत दिन अंक ${numeroResult.personalDay} है`)}
                            </p>
                            <p className="text-xs text-muted-foreground">
                              {l(
                                (PERSONAL_DAY_MEANINGS[numeroResult.personalDay] || PERSONAL_DAY_MEANINGS[1]).en,
                                (PERSONAL_DAY_MEANINGS[numeroResult.personalDay] || PERSONAL_DAY_MEANINGS[1]).hi
                              )}
                            </p>
                          </div>
                        </div>
                      </div>

                      {/* CTA */}
                      <a
                        href="/numerology"
                        className="inline-flex items-center gap-2 px-5 py-2.5 bg-sacred-gold-dark text-white rounded-lg font-semibold text-sm hover:bg-sacred-gold transition-all shadow-md shadow-sacred-gold/20 mt-1"
                      >
                        {l('See Full Analysis', 'पूर्ण विश्लेषण देखें')} →
                      </a>
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* RIGHT: Visual Number Circle (2 cols) */}
            <div className="lg:col-span-2 flex items-center justify-center">
              <div className="relative w-full max-w-[320px] aspect-square">
                {/* Outer ring */}
                <div className="absolute inset-0 rounded-full border-4 border-sacred-gold/20" />
                <div className="absolute inset-3 rounded-full border-2 border-sacred-gold/15" />
                {/* Number positions around the circle */}
                {[1, 2, 3, 4, 5, 6, 7, 8, 9].map((n) => {
                  const angle = ((n - 1) * 40 - 90) * (Math.PI / 180);
                  const radius = 42;
                  const left = 50 + radius * Math.cos(angle);
                  const top = 50 + radius * Math.sin(angle);
                  const isUniversal = n === universalDayNumber;
                  const isLifePath = numeroResult && n === numeroResult.lifePath;
                  return (
                    <div
                      key={n}
                      className={`absolute w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold transition-all duration-300 ${
                        isUniversal
                          ? 'bg-sacred-gold-dark text-white shadow-lg shadow-sacred-gold/40 scale-110'
                          : isLifePath
                            ? 'bg-gradient-to-br from-amber-500 to-amber-700 text-white shadow-md shadow-amber-500/30 scale-105'
                            : 'bg-sacred-gold/10 text-sacred-gold-dark border border-sacred-gold/20'
                      }`}
                      style={{
                        left: `calc(${left}% - 20px)`,
                        top: `calc(${top}% - 20px)`,
                      }}
                    >
                      {n}
                    </div>
                  );
                })}
                {/* Center content */}
                <div className="absolute inset-0 flex flex-col items-center justify-center">
                  <div className="w-24 h-24 rounded-full bg-gradient-to-br from-sacred-gold to-sacred-gold-dark flex items-center justify-center shadow-xl shadow-sacred-gold/30">
                    <span className="text-4xl font-bold text-white">{universalDayNumber}</span>
                  </div>
                  <p className="text-xs font-semibold text-sacred-gold-dark mt-2 text-center">
                    {l('Universal Day', 'सार्वभौमिक दिन')}
                  </p>
                </div>
                {/* Legend */}
                <div className="absolute -bottom-8 left-0 right-0 flex items-center justify-center gap-4 text-[11px]">
                  <span className="flex items-center gap-1">
                    <span className="w-3 h-3 rounded-full bg-sacred-gold-dark inline-block" />
                    {l('Universal', 'सार्वभौमिक')}
                  </span>
                  {numeroResult && (
                    <span className="flex items-center gap-1">
                      <span className="w-3 h-3 rounded-full bg-gradient-to-br from-amber-500 to-amber-700 inline-block" />
                      {l('Life Path', 'मूलांक')}
                    </span>
                  )}
                </div>
              </div>
            </div>
          </div>

          <div className="flex justify-end mt-16">
            <a href="/numerology" className="text-sm text-sacred-gold-dark hover:underline font-medium flex items-center gap-1">
              {l('Explore full numerology analysis', 'पूर्ण अंकशास्त्र विश्लेषण देखें')} →
            </a>
          </div>
        </div>

        <div className="features-title text-center mb-16">
          <Heading as={2} variant={2} className="text-sacred-gold-dark mb-6 leading-[1.1]">
            {l('Complete astrological operating system', 'पूर्ण ज्योतिषीय ऑपरेटिंग सिस्टम')}
          </Heading>
          <div className="max-w-full mx-auto text-lg text-gray-600 leading-relaxed">

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
        <div id="faq-section" className="mt-24">
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
              aria-label={l('Close', 'बंद करें')}
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
