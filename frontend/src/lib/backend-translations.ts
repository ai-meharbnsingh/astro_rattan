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

const NAKSHATRA_NAMES: Record<string, string> = {
  'Ashwini': 'अश्विनी', 'Bharani': 'भरणी', 'Krittika': 'कृत्तिका',
  'Rohini': 'रोहिणी', 'Mrigashira': 'मृगशिरा', 'Ardra': 'आर्द्रा',
  'Punarvasu': 'पुनर्वसु', 'Pushya': 'पुष्य', 'Ashlesha': 'अश्लेषा',
  'Magha': 'मघा', 'Purva Phalguni': 'पूर्व फाल्गुनी', 'Uttara Phalguni': 'उत्तर फाल्गुनी',
  'Hasta': 'हस्त', 'Chitra': 'चित्रा', 'Swati': 'स्वाति',
  'Vishakha': 'विशाखा', 'Anuradha': 'अनुराधा', 'Jyeshtha': 'ज्येष्ठा',
  'Mula': 'मूल', 'Purva Ashadha': 'पूर्व आषाढ़ा', 'Uttara Ashadha': 'उत्तर आषाढ़ा',
  'Shravana': 'श्रवण', 'Dhanishta': 'धनिष्ठा', 'Shatabhisha': 'शतभिषा',
  'Purva Bhadrapada': 'पूर्व भाद्रपद', 'Uttara Bhadrapada': 'उत्तर भाद्रपद', 'Revati': 'रेवती',
};

const SEVERITY: Record<string, string> = {
  'none': 'कोई नहीं', 'mild': 'हल्का', 'medium': 'मध्यम',
  'high': 'तीव्र', 'severe': 'गंभीर',
};

const DIGNITY: Record<string, string> = {
  'exalted': 'उच्च', 'Exalted': 'उच्च',
  'debilitated': 'नीच', 'Debilitated': 'नीच',
  'own': 'स्वराशि', 'Own Sign': 'स्वराशि',
  'moolatrikona': 'मूलत्रिकोण', 'Moolatrikona': 'मूलत्रिकोण',
  'friend': 'मित्र', 'Friend': 'मित्र',
  'enemy': 'शत्रु', 'Enemy': 'शत्रु',
  'neutral': 'सम', 'Neutral': 'सम',
  'retrograde': 'वक्री', 'Retrograde': 'वक्री',
  'combust': 'अस्त', 'Combust': 'अस्त',
  'vargottama': 'वर्गोत्तम', 'Vargottama': 'वर्गोत्तम',
  'transiting': 'गोचर', 'Transiting': 'गोचर',
  'benefic': 'शुभ', 'Benefic': 'शुभ',
  'malefic': 'पापी', 'Malefic': 'पापी',
};

const SIGN_TYPE_LABELS: Record<string, string> = {
  'Moveable': 'चर', 'Fixed': 'स्थिर', 'Dual': 'द्विस्वभाव',
};

const ELEMENT_LABELS: Record<string, string> = {
  'Fire': 'अग्नि', 'Earth': 'पृथ्वी', 'Air': 'वायु', 'Water': 'जल',
};

const PHASE_TYPES: Record<string, string> = {
  'Sade Sati': 'साढ़े साती', 'Dhaiya': 'ढैया', 'Panauti': 'पनौती',
  'Rising (12th from Moon)': 'उदय (चंद्र से 12वां)',
  'Peak (1st from Moon)': 'शिखर (चंद्र से 1ला)',
  'Setting (2nd from Moon)': 'अस्त (चंद्र से 2रा)',
  'Kantak Shani': 'कंटक शनि', 'Ashtam Shani': 'अष्टम शनि',
  'Kantaka': 'कंटक', 'Kantaka Saturn': 'कंटक शनि',
};

// Sade Sati Cycle Titles
const SADE_SATI_CYCLES: Record<string, string> = {
  'First Cycle of Sadhesati': 'साढ़ेसाती का प्रथम चक्र',
  'Second Cycle of Sadhesati': 'साढ़ेसाती का द्वितीय चक्र',
  'Third Cycle of Sadhesati': 'साढ़ेसाती का तृतीय चक्र',
  'Fourth Cycle of Sadhesati': 'साढ़ेसाती का चतुर्थ चक्र',
  'Fifth Cycle of Sadhesati': 'साढ़ेसाती का पंचम चक्र',
  'Sixth Cycle of Sadhesati': 'साढ़ेसाती का षष्ठम चक्र',
  '7th Cycle of Sadhesati': 'साढ़ेसाती का सप्तम चक्र',
  '8th Cycle of Sadhesati': 'साढ़ेसाती का अष्टम चक्र',
};

// Sade Sati Descriptions
const SADE_SATI_DESCRIPTIONS: Record<string, string> = {
  'The first cycle of Sadhesati of Saturn is extremely intense. During this period you may experience physical pain. There would be obstacles and hardships of various kinds. During this period of Sadhesati, there may also be some troubles to your parents.':
    'शनि की साढ़ेसाती का प्रथम चक्र अत्यंत तीव्र होता है। इस अवधि में आपको शारीरिक पीड़ा का अनुभव हो सकता है। विभिन्न प्रकार की बाधाएं और कठिनाइयां रहेंगी। इस साढ़ेसाती की अवधि में आपके माता-पिता को भी कुछ परेशानियां हो सकती हैं।',
  
  'In the second cycle of Sadhesati, Saturn exerts mediocre influence compared to first cycle. During this period you succeed through physical struggle and labour. Despite mental unrest, your worldly progress continues. You may suffer separation or loss of parents or other elders in the family.':
    'साढ़ेसाती के द्वितीय चक्र में, शनि प्रथम चक्र की तुलना में मध्यम प्रभाव डालता है। इस अवधि में आप शारीरिक संघर्ष और परिश्रम के माध्यम से सफल होते हैं। मानसिक अशांति के बावजूद, आपकी सांसारिक प्रगति जारी रहती है। आपको माता-पिता या परिवार के अन्य बुजुर्गों से अलगाव या हानि हो सकती है।',
  
  'In the third cycle of Sadhesati, Saturn inflicts extremely harsh results. During this period you may face tremendous physical hardships. There will be illness and even fear of death. During this period only fortunate persons survive.':
    'साढ़ेसाती के तृतीय चक्र में, शनि अत्यंत कठोर परिणाम देता है। इस अवधि में आपको अत्यधिक शारीरिक कठिनाइयों का सामना करना पड़ सकता है। बीमारी और मृत्यु का भय भी रहेगा। इस अवधि में केवल भाग्यशाली व्यक्ति ही जीवित रहते हैं।',
};

// Transit Details Translation
const TRANSIT_DETAILS: Record<string, string> = {
  'Kantak Shani (4th from Moon)': 'कंटक शनि (चंद्र से 4वां)',
  'Kantaka Saturn (7th from Moon)': 'कंटक शनि (चंद्र से 7वां)',
  'Kantaka Saturn (10th from Moon)': 'कंटक शनि (चंद्र से 10वां)',
  'Ashtam Shani (8th from Moon)': 'अष्टम शनि (चंद्र से 8वां)',
};

// Remedy Categories
const REMEDY_CATEGORIES: Record<string, string> = {
  'Mantra Remedies': 'मंत्र उपाय',
  'Stotra (Hymns)': 'स्तोत्र',
  'Vrata (Fasting)': 'व्रत (उपवास)',
  'Donation (Daan)': 'दान',
  'Gems and Metals': 'रत्न और धातु',
  'Other Remedies': 'अन्य उपाय',
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
  ...SEVERITY, ...DIGNITY, ...SIGN_TYPE_LABELS, ...ELEMENT_LABELS,
  ...PHASE_TYPES, ...REMEDY_MAP, ...YOGINI_NAMES, ...STRENGTH,
  ...NAKSHATRA_NAMES, ...SADE_SATI_CYCLES, ...SADE_SATI_DESCRIPTIONS,
  ...TRANSIT_DETAILS, ...REMEDY_CATEGORIES,
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
  const n = typeof name === 'string' ? name : '';
  if (lang === 'en') return n;
  return PLANET_NAMES[n] || n;
}

/** Translate a zodiac sign name */
export function translateSign(name: string, lang: Language): string {
  const n = typeof name === 'string' ? name : '';
  if (lang === 'en') return n;
  return SIGN_NAMES[n] || n;
}

/** Translate a nakshatra name */
export function translateNakshatra(name: string | null | undefined, lang: Language): string {
  if (!name) return '';
  if (lang === 'en') return name;
  return NAKSHATRA_NAMES[name] || name;
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

/** Translate severity/dignity/strength/sign-type/element */
export function translateLabel(text: string, lang: Language): string {
  if (lang === 'en') return text;
  return SEVERITY[text] || DIGNITY[text] || STRENGTH[text] || SIGN_TYPE_LABELS[text] || ELEMENT_LABELS[text] || PHASE_TYPES[text] || text;
}
