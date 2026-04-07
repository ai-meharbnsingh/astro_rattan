/**
 * Frontend-side translations for backend-returned English text.
 * Maps known English strings (dosha names, yoga names, remedies, planet/sign names)
 * to Hindi equivalents. Used when language is set to Hindi.
 */

import type { Language } from './i18n';

const PLANET_NAMES: Record<string, string> = {
  'Sun': 'सूर्य', 'Moon': 'चंद्र', 'Mars': 'मंगल', 'Mercury': 'बुध',
  'Jupiter': 'बृहस्पति', 'Venus': 'शुक्र', 'Saturn': 'शनि',
  'Rahu': 'राहु', 'Ketu': 'केतु', 'Lagna': 'लग्न',
};

const SIGN_NAMES: Record<string, string> = {
  'Aries': 'मेष', 'Taurus': 'वृषभ', 'Gemini': 'मिथुन', 'Cancer': 'कर्क',
  'Leo': 'सिंह', 'Virgo': 'कन्या', 'Libra': 'तुला', 'Scorpio': 'वृश्चिक',
  'Sagittarius': 'धनु', 'Capricorn': 'मकर', 'Aquarius': 'कुंभ', 'Pisces': 'मीन',
};

const DOSHA_NAMES: Record<string, string> = {
  'Mangal Dosha': 'मंगल दोष', 'Kaal Sarp Dosha': 'काल सर्प दोष',
  'Sade Sati': 'साढ़े साती', 'Pitra Dosha': 'पितृ दोष',
  'Kemdrum Dosha': 'केमद्रुम दोष', 'Angarak Dosha': 'अंगारक दोष',
  'Guru Chandal Dosha': 'गुरु चांडाल दोष', 'Vish Dosha': 'विष दोष',
  'Shrapit Dosha': 'शापित दोष', 'Grahan Dosha': 'ग्रहण दोष',
  'Daridra Dosha': 'दरिद्र दोष', 'Ghatak Dosha': 'घातक दोष',
};

const YOGA_NAMES: Record<string, string> = {
  'Gajakesari Yoga': 'गजकेसरी योग', 'Budhaditya Yoga': 'बुधादित्य योग',
  'Chandra-Mangal Yoga': 'चंद्र-मंगल योग', 'Ruchaka Yoga': 'रुचक योग',
  'Bhadra Yoga': 'भद्र योग', 'Hamsa Yoga': 'हंस योग',
  'Malavya Yoga': 'मालव्य योग', 'Shasha Yoga': 'शश योग',
  'Sunapha Yoga': 'सुनफा योग', 'Anapha Yoga': 'अनफा योग',
  'Durudhara Yoga': 'दुरुधरा योग', 'Shakata Yoga': 'शकट योग',
  'Adhi Yoga': 'अधि योग', 'Amala Yoga': 'अमल योग',
  'Raja Yoga': 'राज योग', 'Lakshmi Yoga': 'लक्ष्मी योग',
  'Dhana Yoga': 'धन योग', 'Saraswati Yoga': 'सरस्वती योग',
  'Neecha Bhanga Raja Yoga': 'नीचभंग राजयोग',
  'Panch Mahapurusha Yoga': 'पंच महापुरुष योग',
  'Viparit Raja Yoga': 'विपरीत राजयोग',
  'Danda Yoga': 'दंड योग', 'Kemadruma Yoga': 'केमद्रुम योग',
};

const SEVERITY: Record<string, string> = {
  'none': 'कोई नहीं', 'mild': 'हल्का', 'medium': 'मध्यम',
  'high': 'तीव्र', 'severe': 'गंभीर',
};

const DIGNITY: Record<string, string> = {
  'exalted': 'उच्च', 'debilitated': 'नीच', 'own': 'स्वराशि',
  'moolatrikona': 'मूलत्रिकोण', 'friend': 'मित्र', 'enemy': 'शत्रु',
  'neutral': 'सम', 'retrograde': 'वक्री',
};

const PHASE_TYPES: Record<string, string> = {
  'Sade Sati': 'साढ़े साती', 'Dhaiya': 'ढैया', 'Panauti': 'पनौती',
  'Rising (12th from Moon)': 'उदय (चंद्र से 12वां)',
  'Peak (1st from Moon)': 'शिखर (चंद्र से 1ला)',
  'Setting (2nd from Moon)': 'अस्त (चंद्र से 2रा)',
  'Kantak Shani': 'कंटक शनि', 'Ashtam Shani': 'अष्टम शनि',
};

const REMEDY_MAP: Record<string, string> = {
  'Wear a coral (Moonga) gemstone after consulting an astrologer': 'ज्योतिषी से परामर्श के बाद मूंगा रत्न धारण करें',
  'Recite Hanuman Chalisa daily': 'प्रतिदिन हनुमान चालीसा का पाठ करें',
  'Donate red items on Tuesday': 'मंगलवार को लाल वस्तुएं दान करें',
  'Worship Lord Shani on Saturdays': 'शनिवार को शनिदेव की पूजा करें',
  'Recite Shani Mantra or Shani Stotra': 'शनि मंत्र या शनि स्तोत्र का पाठ करें',
  'Donate black sesame, mustard oil on Saturdays': 'शनिवार को काले तिल, सरसों का तेल दान करें',
  'Wear Blue Sapphire (Neelam) or Amethyst after astrological advice': 'ज्योतिषीय सलाह के बाद नीलम या जामुनिया धारण करें',
  'Visit Shani temple and light mustard oil lamp': 'शनि मंदिर जाएं और सरसों के तेल का दीपक जलाएं',
  'Feed crows and black dogs on Saturdays': 'शनिवार को कौओं और काले कुत्तों को भोजन दें',
  'Chant Om Sham Shanaishcharaye Namah 108 times': 'ॐ शं शनैश्चराय नमः 108 बार जपें',
  'Perform Shani Shanti Puja': 'शनि शांति पूजा करवाएं',
};

const YOGINI_NAMES: Record<string, string> = {
  'Mangala': 'मंगला', 'Pingala': 'पिंगला', 'Dhanya': 'धन्या',
  'Bhramari': 'भ्रामरी', 'Bhadrika': 'भद्रिका', 'Ulka': 'उल्का',
  'Siddha': 'सिद्धा', 'Sankata': 'संकटा',
};

const STRENGTH: Record<string, string> = {
  'Strong': 'बलवान', 'Medium': 'मध्यम', 'Weak': 'दुर्बल',
};

// All lookup tables merged for generic matching
const ALL_LOOKUPS: Record<string, string> = {
  ...PLANET_NAMES, ...SIGN_NAMES, ...DOSHA_NAMES, ...YOGA_NAMES,
  ...SEVERITY, ...DIGNITY, ...PHASE_TYPES, ...REMEDY_MAP,
  ...YOGINI_NAMES, ...STRENGTH,
};

/**
 * Translate a backend-returned string to Hindi.
 * Returns original text if no translation found (graceful degradation).
 */
export function translateBackend(text: string | null | undefined, lang: Language): string {
  if (!text) return '';
  if (lang === 'en') return text;

  // Exact match first
  if (ALL_LOOKUPS[text]) return ALL_LOOKUPS[text];

  // Try matching planet/sign names within the text (for composite strings)
  let result = text;
  for (const [en, hi] of Object.entries(PLANET_NAMES)) {
    result = result.replace(new RegExp(`\\b${en}\\b`, 'g'), hi);
  }
  for (const [en, hi] of Object.entries(SIGN_NAMES)) {
    result = result.replace(new RegExp(`\\b${en}\\b`, 'g'), hi);
  }

  return result;
}

/** Translate a planet name */
export function translatePlanet(name: string, lang: Language): string {
  if (lang === 'en') return name;
  return PLANET_NAMES[name] || name;
}

/** Translate a zodiac sign name */
export function translateSign(name: string, lang: Language): string {
  if (lang === 'en') return name;
  return SIGN_NAMES[name] || name;
}

/** Translate a dosha or yoga name */
export function translateName(name: string, lang: Language): string {
  if (lang === 'en') return name;
  return DOSHA_NAMES[name] || YOGA_NAMES[name] || YOGINI_NAMES[name] || name;
}

/** Translate a remedy string */
export function translateRemedy(text: string, lang: Language): string {
  if (lang === 'en') return text;
  return REMEDY_MAP[text] || text;
}

/** Translate severity/dignity/strength */
export function translateLabel(text: string, lang: Language): string {
  if (lang === 'en') return text;
  return SEVERITY[text] || DIGNITY[text] || STRENGTH[text] || PHASE_TYPES[text] || text;
}
