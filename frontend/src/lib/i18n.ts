import { createContext, useContext, useState, useCallback, ReactNode, createElement } from 'react';

export type Language = 'en' | 'hi';

type TranslationMap = Record<string, string>;

const translations: Record<Language, TranslationMap> = {
  en: {
    // Navigation
    'nav.home': 'Home',
    'nav.kundli': 'Kundli',
    'nav.horoscope': 'Horoscope',
    'nav.panchang': 'Panchang',
    'nav.prashnavali': 'Prashnavali',
    'nav.numerology': 'Numerology',
    'nav.palmistry': 'Palmistry',
    'nav.library': 'Library',
    'nav.blog': 'Blog',
    'nav.shop': 'Shop',
    'nav.consultation': 'Consultation',
    'nav.reports': 'Reports',
    'nav.aiChat': 'AI Chat',
    'nav.askAI': 'Ask AI',
    'nav.askAIAstrologer': 'Ask AI Astrologer',
    'nav.admin': 'Admin',
    'nav.dashboard': 'Dashboard',
    'nav.astrologerDashboard': 'Astrologer Dashboard',
    'nav.cart': 'Cart',
    'nav.profile': 'Profile',

    // Auth
    'auth.signIn': 'Sign In',
    'auth.signUp': 'Sign Up',
    'auth.signOut': 'Sign Out',
    'auth.forgotPassword': 'Forgot Password?',
    'auth.email': 'Email',
    'auth.password': 'Password',
    'auth.confirmPassword': 'Confirm Password',
    'auth.fullName': 'Full Name',
    'auth.orContinueWith': 'Or continue with',

    // Common UI
    'common.loading': 'Loading...',
    'common.submit': 'Submit',
    'common.cancel': 'Cancel',
    'common.save': 'Save',
    'common.delete': 'Delete',
    'common.edit': 'Edit',
    'common.close': 'Close',
    'common.back': 'Back',
    'common.next': 'Next',
    'common.previous': 'Previous',
    'common.search': 'Search',
    'common.filter': 'Filter',
    'common.sortBy': 'Sort By',
    'common.viewAll': 'View All',
    'common.readMore': 'Read More',
    'common.learnMore': 'Learn More',
    'common.explore': 'Explore',
    'common.generate': 'Generate',
    'common.download': 'Download',
    'common.share': 'Share',
    'common.price': 'Price',
    'common.addToCart': 'Add to Cart',
    'common.buyNow': 'Buy Now',
    'common.free': 'Free',
    'common.new': 'New',
    'common.popular': 'Popular',
    'common.featured': 'Featured',
    'common.all': 'All',
    'common.noResults': 'No results found',
    'common.error': 'Something went wrong',
    'common.retry': 'Retry',
    'common.yes': 'Yes',
    'common.no': 'No',

    // Hero Section
    'hero.badge': 'Sidereal Astrology',
    'hero.knowYour': 'Know Your',
    'hero.destiny': 'Destiny',
    'hero.getFreeKundli': 'Get Free Kundli',
    'hero.quickKundli': 'Quick Kundli',
    'hero.birthPlace': 'Birth Place',
    'hero.generateKundli': 'Generate Kundli',

    // Features Section
    'features.heading': 'Unlock the Secrets of',
    'features.headingHighlight': ' Vedic Astrology',
    'features.kundli.title': 'Kundli',
    'features.kundli.description': 'Detailed Birth Charts',
    'features.kundli.action': 'Generate Kundli',
    'features.panchang.title': 'Panchang',
    'features.panchang.description': 'Daily Auspicious Times',
    'features.panchang.action': 'View Panchang',
    'features.aiAstrologer.title': 'AI Astrologer',
    'features.aiAstrologer.description': 'Instant Cosmic Guidance',
    'features.aiAstrologer.action': 'Ask AI',
    'features.shop.title': 'Shop',
    'features.shop.description': 'Astrological Products',
    'features.shop.action': 'Explore',
    'features.dosha.title': 'Dosha Analysis',
    'features.dosha.description': 'Personalized Remedies',
    'features.dosha.action': 'Check Dosha',
    'features.muhurat.title': 'Muhurat Finder',
    'features.muhurat.description': 'Perfect Timing for Events',
    'features.muhurat.action': 'Find Muhurat',
    'features.chatWithAI': 'Chat with AI Astrologer',

    // Daily Horoscope
    'horoscope.title': 'Daily Horoscope',
    'horoscope.subtitle': 'What the stars have in store for you today',
    'horoscope.selectSign': 'Select Your Sign',
    'horoscope.todayForecast': "Today's Forecast",
    'horoscope.love': 'Love',
    'horoscope.career': 'Career',
    'horoscope.health': 'Health',
    'horoscope.finance': 'Finance',
    'horoscope.luckyNumber': 'Lucky Number',
    'horoscope.luckyColor': 'Lucky Color',

    // Panchang
    'panchang.title': 'Panchang',
    'panchang.todayPanchang': "Today's Panchang",
    'panchang.tithi': 'Tithi',
    'panchang.nakshatra': 'Nakshatra',
    'panchang.yoga': 'Yoga',
    'panchang.karana': 'Karana',
    'panchang.sunrise': 'Sunrise',
    'panchang.sunset': 'Sunset',
    'panchang.rahuKaal': 'Rahu Kaal',
    'panchang.auspiciousTime': 'Auspicious Time',

    // Shop
    'shop.title': 'Sacred Products',
    'shop.subtitle': 'Authentic spiritual products for your journey',
    'shop.categories': 'Categories',
    'shop.gemstones': 'Gemstones',
    'shop.rudraksha': 'Rudraksha',
    'shop.yantras': 'Yantras',
    'shop.malas': 'Malas',
    'shop.books': 'Books',

    // About / CTA
    'about.title': 'Ancient Wisdom, Modern Technology',
    'about.subtitle': 'Bridging the gap between traditional Vedic astrology and cutting-edge AI',
    'cta.title': 'Begin Your Cosmic Journey',
    'cta.subtitle': 'Discover the wisdom of the stars and unlock your true potential',
    'cta.button': 'Get Started Free',

    // Testimonials
    'testimonials.title': 'What Our Users Say',
    'testimonials.subtitle': 'Trusted by thousands of astrology enthusiasts',

    // Footer
    'footer.tagline': 'Bridging ancient Vedic wisdom with modern technology',
    'footer.quickLinks': 'Quick Links',
    'footer.services': 'Services',
    'footer.resources': 'Resources',
    'footer.contact': 'Contact Us',
    'footer.privacy': 'Privacy Policy',
    'footer.terms': 'Terms of Service',
    'footer.copyright': 'All rights reserved',
    'footer.madeWith': 'Made with',
    'footer.forSeekers': 'for spiritual seekers',

    // Consultation
    'consultation.title': 'Consult an Astrologer',
    'consultation.bookNow': 'Book Now',
    'consultation.available': 'Available',
    'consultation.busy': 'Busy',
    'consultation.experience': 'Experience',
    'consultation.languages': 'Languages',
    'consultation.rating': 'Rating',
    'consultation.perMinute': 'per minute',

    // Kundli
    'kundli.title': 'Kundli Generator',
    'kundli.subtitle': 'Generate your Vedic birth chart',
    'kundli.birthDetails': 'Birth Details',
    'kundli.birthDate': 'Birth Date',
    'kundli.birthTime': 'Birth Time',
    'kundli.birthPlace': 'Birth Place',
    'kundli.generateChart': 'Generate Chart',
    'kundli.planets': 'Planets',
    'kundli.houses': 'Houses',
    'kundli.dashas': 'Dashas',

    // Miscellaneous
    'misc.language': 'Language',
    'misc.english': 'English',
    'misc.hindi': 'Hindi',
    'misc.darkMode': 'Dark Mode',
    'misc.lightMode': 'Light Mode',
    'misc.notifications': 'Notifications',
    'misc.settings': 'Settings',
  },

  hi: {
    // Navigation
    'nav.home': 'होम',
    'nav.kundli': 'कुंडली',
    'nav.horoscope': 'राशिफल',
    'nav.panchang': 'पंचांग',
    'nav.prashnavali': 'प्रश्नावली',
    'nav.numerology': 'अंक ज्योतिष',
    'nav.palmistry': 'हस्तरेखा',
    'nav.library': 'पुस्तकालय',
    'nav.blog': 'ब्लॉग',
    'nav.shop': 'दुकान',
    'nav.consultation': 'परामर्श',
    'nav.reports': 'रिपोर्ट',
    'nav.aiChat': 'AI चैट',
    'nav.askAI': 'AI से पूछें',
    'nav.askAIAstrologer': 'AI ज्योतिषी से पूछें',
    'nav.admin': 'एडमिन',
    'nav.dashboard': 'डैशबोर्ड',
    'nav.astrologerDashboard': 'ज्योतिषी डैशबोर्ड',
    'nav.cart': 'कार्ट',
    'nav.profile': 'प्रोफ़ाइल',

    // Auth
    'auth.signIn': 'साइन इन',
    'auth.signUp': 'साइन अप',
    'auth.signOut': 'साइन आउट',
    'auth.forgotPassword': 'पासवर्ड भूल गए?',
    'auth.email': 'ईमेल',
    'auth.password': 'पासवर्ड',
    'auth.confirmPassword': 'पासवर्ड पुष्टि',
    'auth.fullName': 'पूरा नाम',
    'auth.orContinueWith': 'या इसके साथ जारी रखें',

    // Common UI
    'common.loading': 'लोड हो रहा है...',
    'common.submit': 'जमा करें',
    'common.cancel': 'रद्द करें',
    'common.save': 'सहेजें',
    'common.delete': 'हटाएं',
    'common.edit': 'संपादित करें',
    'common.close': 'बंद करें',
    'common.back': 'वापस',
    'common.next': 'अगला',
    'common.previous': 'पिछला',
    'common.search': 'खोजें',
    'common.filter': 'फ़िल्टर',
    'common.sortBy': 'क्रमबद्ध करें',
    'common.viewAll': 'सभी देखें',
    'common.readMore': 'और पढ़ें',
    'common.learnMore': 'और जानें',
    'common.explore': 'देखें',
    'common.generate': 'बनाएं',
    'common.download': 'डाउनलोड',
    'common.share': 'साझा करें',
    'common.price': 'मूल्य',
    'common.addToCart': 'कार्ट में जोड़ें',
    'common.buyNow': 'अभी खरीदें',
    'common.free': 'मुफ़्त',
    'common.new': 'नया',
    'common.popular': 'लोकप्रिय',
    'common.featured': 'विशेष',
    'common.all': 'सभी',
    'common.noResults': 'कोई परिणाम नहीं मिला',
    'common.error': 'कुछ गलत हो गया',
    'common.retry': 'पुनः प्रयास',
    'common.yes': 'हाँ',
    'common.no': 'नहीं',

    // Hero Section
    'hero.badge': 'सायन ज्योतिष',
    'hero.knowYour': 'जानें अपना',
    'hero.destiny': 'भाग्य',
    'hero.getFreeKundli': 'मुफ़्त कुंडली पाएं',
    'hero.quickKundli': 'त्वरित कुंडली',
    'hero.birthPlace': 'जन्म स्थान',
    'hero.generateKundli': 'कुंडली बनाएं',

    // Features Section
    'features.heading': 'खोलें रहस्य',
    'features.headingHighlight': ' वैदिक ज्योतिष के',
    'features.kundli.title': 'कुंडली',
    'features.kundli.description': 'विस्तृत जन्म कुंडली',
    'features.kundli.action': 'कुंडली बनाएं',
    'features.panchang.title': 'पंचांग',
    'features.panchang.description': 'दैनिक शुभ समय',
    'features.panchang.action': 'पंचांग देखें',
    'features.aiAstrologer.title': 'AI ज्योतिषी',
    'features.aiAstrologer.description': 'तुरंत ब्रह्मांडीय मार्गदर्शन',
    'features.aiAstrologer.action': 'AI से पूछें',
    'features.shop.title': 'दुकान',
    'features.shop.description': 'ज्योतिषीय उत्पाद',
    'features.shop.action': 'देखें',
    'features.dosha.title': 'दोष विश्लेषण',
    'features.dosha.description': 'व्यक्तिगत उपाय',
    'features.dosha.action': 'दोष जांचें',
    'features.muhurat.title': 'मुहूर्त खोजक',
    'features.muhurat.description': 'कार्यों के लिए सही समय',
    'features.muhurat.action': 'मुहूर्त खोजें',
    'features.chatWithAI': 'AI ज्योतिषी से बात करें',

    // Daily Horoscope
    'horoscope.title': 'दैनिक राशिफल',
    'horoscope.subtitle': 'आज सितारे आपके लिए क्या लेकर आए हैं',
    'horoscope.selectSign': 'अपनी राशि चुनें',
    'horoscope.todayForecast': 'आज का पूर्वानुमान',
    'horoscope.love': 'प्रेम',
    'horoscope.career': 'करियर',
    'horoscope.health': 'स्वास्थ्य',
    'horoscope.finance': 'वित्त',
    'horoscope.luckyNumber': 'भाग्यशाली अंक',
    'horoscope.luckyColor': 'भाग्यशाली रंग',

    // Panchang
    'panchang.title': 'पंचांग',
    'panchang.todayPanchang': 'आज का पंचांग',
    'panchang.tithi': 'तिथि',
    'panchang.nakshatra': 'नक्षत्र',
    'panchang.yoga': 'योग',
    'panchang.karana': 'करण',
    'panchang.sunrise': 'सूर्योदय',
    'panchang.sunset': 'सूर्यास्त',
    'panchang.rahuKaal': 'राहु काल',
    'panchang.auspiciousTime': 'शुभ समय',

    // Shop
    'shop.title': 'पवित्र उत्पाद',
    'shop.subtitle': 'आपकी आध्यात्मिक यात्रा के लिए प्रामाणिक उत्पाद',
    'shop.categories': 'श्रेणियां',
    'shop.gemstones': 'रत्न',
    'shop.rudraksha': 'रुद्राक्ष',
    'shop.yantras': 'यंत्र',
    'shop.malas': 'मालाएं',
    'shop.books': 'पुस्तकें',

    // About / CTA
    'about.title': 'प्राचीन ज्ञान, आधुनिक तकनीक',
    'about.subtitle': 'पारंपरिक वैदिक ज्योतिष और अत्याधुनिक AI के बीच सेतु',
    'cta.title': 'अपनी ब्रह्मांडीय यात्रा शुरू करें',
    'cta.subtitle': 'सितारों का ज्ञान खोजें और अपनी सच्ची क्षमता को जागृत करें',
    'cta.button': 'मुफ़्त शुरू करें',

    // Testimonials
    'testimonials.title': 'हमारे उपयोगकर्ता क्या कहते हैं',
    'testimonials.subtitle': 'हजारों ज्योतिष प्रेमियों द्वारा विश्वसनीय',

    // Footer
    'footer.tagline': 'प्राचीन वैदिक ज्ञान को आधुनिक तकनीक से जोड़ना',
    'footer.quickLinks': 'त्वरित लिंक',
    'footer.services': 'सेवाएं',
    'footer.resources': 'संसाधन',
    'footer.contact': 'संपर्क करें',
    'footer.privacy': 'गोपनीयता नीति',
    'footer.terms': 'सेवा की शर्तें',
    'footer.copyright': 'सर्वाधिकार सुरक्षित',
    'footer.madeWith': 'बनाया गया',
    'footer.forSeekers': 'आध्यात्मिक साधकों के लिए',

    // Consultation
    'consultation.title': 'ज्योतिषी से परामर्श करें',
    'consultation.bookNow': 'अभी बुक करें',
    'consultation.available': 'उपलब्ध',
    'consultation.busy': 'व्यस्त',
    'consultation.experience': 'अनुभव',
    'consultation.languages': 'भाषाएं',
    'consultation.rating': 'रेटिंग',
    'consultation.perMinute': 'प्रति मिनट',

    // Kundli
    'kundli.title': 'कुंडली जनरेटर',
    'kundli.subtitle': 'अपनी वैदिक जन्म कुंडली बनाएं',
    'kundli.birthDetails': 'जन्म विवरण',
    'kundli.birthDate': 'जन्म तिथि',
    'kundli.birthTime': 'जन्म समय',
    'kundli.birthPlace': 'जन्म स्थान',
    'kundli.generateChart': 'कुंडली बनाएं',
    'kundli.planets': 'ग्रह',
    'kundli.houses': 'भाव',
    'kundli.dashas': 'दशाएं',

    // Miscellaneous
    'misc.language': 'भाषा',
    'misc.english': 'English',
    'misc.hindi': 'हिन्दी',
    'misc.darkMode': 'डार्क मोड',
    'misc.lightMode': 'लाइट मोड',
    'misc.notifications': 'सूचनाएं',
    'misc.settings': 'सेटिंग्स',
  },
};

function getStoredLanguage(): Language {
  if (typeof window === 'undefined') return 'en';
  const stored = localStorage.getItem('astrovedic-language');
  if (stored === 'en' || stored === 'hi') return stored;
  return 'en';
}

function storeLanguage(lang: Language) {
  if (typeof window !== 'undefined') {
    localStorage.setItem('astrovedic-language', lang);
  }
}

interface I18nContextValue {
  language: Language;
  setLanguage: (lang: Language) => void;
  t: (key: string) => string;
}

export const I18nContext = createContext<I18nContextValue>({
  language: 'en',
  setLanguage: () => {},
  t: (key: string) => key,
});

export function useTranslation() {
  return useContext(I18nContext);
}

export function I18nProvider({ children }: { children: ReactNode }) {
  const [language, setLanguageState] = useState<Language>(getStoredLanguage);

  const setLanguage = useCallback((lang: Language) => {
    setLanguageState(lang);
    storeLanguage(lang);
  }, []);

  const t = useCallback(
    (key: string): string => {
      return translations[language][key] ?? translations['en'][key] ?? key;
    },
    [language]
  );

  return createElement(
    I18nContext.Provider,
    { value: { language, setLanguage, t } },
    children
  );
}
