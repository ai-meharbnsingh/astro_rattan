import { useState, useEffect, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Menu, X, Sparkles, LogOut, Shield, User, ChevronDown, Briefcase } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import { useTranslation } from '@/lib/i18n';
import LanguageSwitcher from '@/components/LanguageSwitcher';

// Vastu is WIP — only visible on staging (non-production hosts)
const isProduction = typeof window !== 'undefined' && window.location.hostname === 'astrorattan.com';

const serviceLinks: { key: string; href: string; highlight?: boolean; megaMenuKey?: string }[] = [
  { key: 'nav.kundli', href: '/kundli', megaMenuKey: 'kundli' },
  { key: 'nav.horoscope', href: '/horoscope', megaMenuKey: 'horoscope' },
  { key: 'nav.panchang', href: '/panchang', megaMenuKey: 'panchang' },
  { key: 'nav.lalKitab', href: '/lal-kitab', megaMenuKey: 'lalKitab' },
  { key: 'nav.numerology', href: '/numerology', megaMenuKey: 'numerology' },
  ...(!isProduction ? [{ key: 'nav.vastu', href: '/vastu', highlight: true, megaMenuKey: 'vastu' }] : []),
  { key: 'nav.blog', href: '/blog' },
];

// Routes that require authentication — unauthenticated users go to /login
const authRequiredRoutes = new Set(['/kundli']);

// ── Mega Menu Data ───────────────────────────────────────────
interface MegaMenuTab { en: string; hi: string; value: string; }
interface MegaMenuCat { key: string; label: { en: string; hi: string }; tabs: MegaMenuTab[]; }

const pageMegaMenus: Record<string, MegaMenuCat[]> = {
  kundli: [
    {
      key: 'primary',
      label: { en: 'Primary', hi: 'मुख्य' },
      tabs: [
        { en: 'Report', hi: 'रिपोर्ट', value: 'report' },
        { en: 'Remedies', hi: 'उपाय', value: 'remedies' },
        { en: 'Planets', hi: 'ग्रह', value: 'planets' },
        { en: 'Dasha', hi: 'दशा', value: 'dasha' },
        { en: 'Yogas / Dosha', hi: 'योग / दोष', value: 'yoga-dosha' },
        { en: 'Divisional', hi: 'विभाजन चार्ट', value: 'divisional' },
        { en: 'Aspects', hi: 'दृष्टि', value: 'aspects' },
      ],
    },
    {
      key: 'charts',
      label: { en: 'Charts', hi: 'चार्ट' },
      tabs: [
        { en: 'Ashtakvarga', hi: 'अष्टकवर्ग', value: 'ashtakvarga' },
        { en: 'Ashtakvarga Effects', hi: 'अष्टकवर्ग फल', value: 'ashtakvarga-phala' },
        { en: 'Sodashvarga', hi: 'षोडशवर्ग', value: 'sodashvarga' },
        { en: 'D108 Chart', hi: 'D108 अष्टोत्तरांश', value: 'd108' },
        { en: 'Chart Animation', hi: 'चार्ट एनिमेशन', value: 'animation' },
        { en: 'Sarvatobhadra', hi: 'सर्वतोभद्र चक्र', value: 'sarvatobhadra' },
      ],
    },
    {
      key: 'timing',
      label: { en: 'Timing', hi: 'समय' },
      tabs: [
        { en: 'Yogini Dasha', hi: 'योगिनी दशा', value: 'yogini' },
        { en: 'Dasha Effects', hi: 'दशा फल', value: 'dasha-phala' },
        { en: 'Varshphal', hi: 'वर्षफल', value: 'varshphal' },
        { en: 'Transits', hi: 'गोचर', value: 'transits' },
        { en: 'Sade Sati', hi: 'साढ़े साती', value: 'sadesati' },
        { en: 'Kalachakra Dasha', hi: 'कालचक्र दशा', value: 'kalachakra' },
        { en: 'Gochara Vedha', hi: 'गोचर वेध', value: 'gochara-vedha' },
        { en: 'Transit Interpretations', hi: 'गोचर व्याख्या', value: 'transit-interp' },
        { en: 'Lucky Indicators', hi: 'शुभ संकेतक', value: 'transit-lucky' },
      ],
    },
    {
      key: 'analysis',
      label: { en: 'Analysis', hi: 'विश्लेषण' },
      tabs: [
        { en: 'Shadbala', hi: 'षड्बल', value: 'shadbala' },
        { en: 'KP System', hi: 'केपी सिस्टम', value: 'kp' },
        { en: 'KP Horary', hi: 'केपी प्रश्न', value: 'kp-horary' },
        { en: 'Jaimini', hi: 'जैमिनी', value: 'jaimini' },
        { en: 'Pravrajya Yogas', hi: 'प्रव्रज्या योग', value: 'pravrajya' },
        { en: 'Progeny (Apatya)', hi: 'संतान', value: 'apatya' },
        { en: 'Stri Jataka', hi: 'स्त्री जातक', value: 'stri-jataka' },
        { en: 'Conjunctions', hi: 'ग्रह युतियाँ', value: 'conjunctions' },
        { en: 'Disease Analysis', hi: 'रोग विश्लेषण', value: 'roga' },
        { en: 'Bhava Phala', hi: 'भाव फल', value: 'bhava-phala' },
        { en: 'Career (Vritti)', hi: 'आजीविका', value: 'vritti' },
        { en: 'Janma Predictions', hi: 'जन्म फल', value: 'janma-predictions' },
        { en: 'Interpretations', hi: 'कुंडली व्याख्या', value: 'kundli-interpretations' },
        { en: 'Iogita', hi: 'आयोगिता', value: 'iogita' },
        { en: 'Aspects Matrix', hi: 'दृष्टि मैट्रिक्स', value: 'aspects-matrix' },
        { en: 'Navamsha Career', hi: 'नवांश करियर', value: 'navamsha-career' },
        { en: 'Graha Sambandha', hi: 'ग्रह सम्बन्ध', value: 'graha-sambandha' },
        { en: 'Panchadha Maitri', hi: 'पंचधा मैत्री', value: 'panchadha-maitri' },
        { en: 'Nadi Analysis', hi: 'नाड़ी विश्लेषण', value: 'nadi-analysis' },
      ],
    },
    {
      key: 'advanced',
      label: { en: 'Advanced', hi: 'उन्नत' },
      tabs: [
        { en: 'Bhava Analysis', hi: 'भाव विचार', value: 'bhava-vichara' },
        { en: 'Longevity Indicators', hi: 'आयु संकेतक', value: 'longevity' },
        { en: 'Mundane', hi: 'मुंडन ज्योतिष', value: 'mundane' },
        { en: 'Birth Rectification', hi: 'जन्म समय शोधन', value: 'rectification' },
        { en: 'Upagrahas', hi: 'उपग्रह', value: 'upagrahas' },
        { en: 'Lordships', hi: 'लॉर्डशिप', value: 'lordships' },
        { en: 'Birth Details', hi: 'विवरण', value: 'details' },
        { en: 'Avakhada', hi: 'अवखड़ा', value: 'avakhada' },
        { en: 'Kundli Milan', hi: 'कुंडली मिलान', value: 'milan' },
        { en: 'Family Longevity', hi: 'परिवार आयु विचार', value: 'family-demise' },
        { en: 'Astro Map', hi: 'ज्योतिष मानचित्र', value: 'astro-map' },
      ],
    },
  ],
  horoscope: [
    {
      key: 'periods',
      label: { en: 'Time Periods', hi: 'समय अवधि' },
      tabs: [
        { en: 'Daily', hi: 'दैनिक', value: 'daily' },
        { en: 'Tomorrow', hi: 'कल', value: 'tomorrow' },
        { en: 'Weekly', hi: 'साप्ताहिक', value: 'weekly' },
        { en: 'Monthly', hi: 'मासिक', value: 'monthly' },
        { en: 'Yearly', hi: 'वार्षिक', value: 'yearly' },
      ],
    },
    {
      key: 'special',
      label: { en: 'Special', hi: 'विशेष' },
      tabs: [
        { en: 'All Signs', hi: 'सभी राशियाँ', value: 'all' },
        { en: 'Transit Insights', hi: 'गोचर अंतर्दृष्टि', value: 'transits' },
      ],
    },
  ],
  panchang: [
    {
      key: 'calendar',
      label: { en: 'Calendar', hi: 'कैलेंडर' },
      tabs: [
        { en: 'Hindu Calendar', hi: 'हिंदू कैलेंडर', value: 'calendar' },
        { en: 'Festivals', hi: 'त्योहार', value: 'festivals' },
        { en: 'Sankranti', hi: 'संक्रांति', value: 'sankranti' },
      ],
    },
    {
      key: 'muhurat',
      label: { en: 'Muhurat', hi: 'मुहूर्त' },
      tabs: [
        { en: 'Muhurat Finder', hi: 'मुहूर्त खोजक', value: 'muhurat-finder' },
        { en: 'Muhurat', hi: 'मुहूर्त', value: 'muhurat' },
        { en: 'Advanced', hi: 'विशेष', value: 'advanced' },
      ],
    },
    {
      key: 'details',
      label: { en: 'Panchang Details', hi: 'पंचांग विवरण' },
      tabs: [
        { en: 'Planets', hi: 'ग्रह', value: 'planets' },
        { en: 'Hora', hi: 'होरा', value: 'hora' },
        { en: 'Lagna', hi: 'लग्न', value: 'lagna' },
        { en: 'Choghadiya', hi: 'चौघड़िया', value: 'choghadiya' },
        { en: 'Gowri', hi: 'गौरी', value: 'gowri' },
        { en: 'Tara / Chandra', hi: 'तारा / चन्द्र', value: 'tarabalam' },
      ],
    },
  ],
  lalKitab: [
    {
      key: 'core',
      label: { en: 'Core', hi: 'मुख्य' },
      tabs: [
        { en: 'Dashboard', hi: 'डैशबोर्ड', value: 'dashboard' },
        { en: 'Chart', hi: 'चार्ट', value: 'chart' },
        { en: 'Analysis', hi: 'विश्लेषण', value: 'analysis' },
        { en: 'Predictions', hi: 'भविष्यवाणी', value: 'predictions' },
      ],
    },
    {
      key: 'timing',
      label: { en: 'Timing & Remedies', hi: 'समय और उपाय' },
      tabs: [
        { en: 'Timing', hi: 'समय', value: 'timing' },
        { en: 'Upay', hi: 'उपाय', value: 'upay' },
        { en: 'Tracker', hi: 'ट्रैकर', value: 'tracker' },
      ],
    },
    {
      key: 'special',
      label: { en: 'Special', hi: 'विशेष' },
      tabs: [
        { en: 'Nishaniyan', hi: 'निशानियां', value: 'nishaniyan' },
        { en: 'Advanced', hi: 'उन्नत', value: 'advanced' },
        { en: 'Vastu', hi: 'वास्तु', value: 'vastu' },
        { en: 'Farmaan', hi: 'फ़रमान', value: 'farmaan' },
      ],
    },
  ],
  numerology: [
    {
      key: 'calculators',
      label: { en: 'Calculators', hi: 'कैलकुलेटर' },
      tabs: [
        { en: 'Life Path', hi: 'जीवन पथ', value: 'life_path' },
        { en: 'Mobile', hi: 'मोबाइल', value: 'mobile' },
        { en: 'Name', hi: 'नाम', value: 'name' },
      ],
    },
    {
      key: 'more',
      label: { en: 'More', hi: 'अधिक' },
      tabs: [
        { en: 'Vehicle', hi: 'वाहन', value: 'vehicle' },
        { en: 'House', hi: 'घर', value: 'house' },
        { en: 'Mook Prashna', hi: 'मूक प्रश्न', value: 'mook_prashna' },
        { en: 'Khoyi Vastu', hi: 'खोई वस्तु', value: 'khoyi_vastu' },
      ],
    },
  ],
  vastu: [
    {
      key: 'modes',
      label: { en: 'Modes', hi: 'मोड' },
      tabs: [
        { en: 'Vastu Analysis', hi: 'वास्तु विश्लेषण', value: 'analysis' },
        { en: 'My Home Grid', hi: 'माय होम ग्रिड', value: 'home-grid' },
        { en: 'Floor Plan Upload', hi: 'फ्लोर प्लान अपलोड', value: 'floorplan' },
      ],
    },
    {
      key: 'result',
      label: { en: 'Analysis Tabs', hi: 'विश्लेषण टैब' },
      tabs: [
        { en: 'Home', hi: 'होम', value: 'home' },
        { en: 'Mandala', hi: 'मंडल', value: 'mandala' },
        { en: 'Entrance', hi: 'प्रवेश', value: 'entrance' },
        { en: 'Remedies', hi: 'उपाय', value: 'remedies' },
        { en: 'Rooms', hi: 'कमरे', value: 'rooms' },
      ],
    },
  ],
};

export default function Navigation() {
  const { user, isAuthenticated, logout } = useAuth();
  const { t, language } = useTranslation();
  const navigate = useNavigate();
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isProfileMenuOpen, setIsProfileMenuOpen] = useState(false);
  const [openMegaMenu, setOpenMegaMenu] = useState<string | null>(null);
  const [mobileMegaMenu, setMobileMegaMenu] = useState<string | null>(null);
  const profileMenuRef = useRef<HTMLDivElement>(null);
  const megaMenuRef = useRef<HTMLDivElement>(null);
  const megaMenuTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    const handleScroll = () => setIsScrolled(window.scrollY > 50);
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    const handleOutsideClick = (event: MouseEvent) => {
      if (profileMenuRef.current && !profileMenuRef.current.contains(event.target as Node)) {
        setIsProfileMenuOpen(false);
      }
      if (megaMenuRef.current && !megaMenuRef.current.contains(event.target as Node)) {
        setOpenMegaMenu(null);
      }
    };
    document.addEventListener('mousedown', handleOutsideClick);
    return () => document.removeEventListener('mousedown', handleOutsideClick);
  }, []);

  return (
    <>
      <nav className={`fixed top-0 left-0 right-0 z-50 border-b border-sacred-gold/45 shadow-[0_8px_18px_-14px_rgba(196,97,31,0.55)] transition-all duration-500 ${
        isScrolled
          ? 'bg-background/96 backdrop-blur-lg py-2'
          : 'bg-background/92 py-3'
      }`}>
        <div className="max-w-screen-2xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            {/* Logo */}
            <Link to="/about" className="flex items-center gap-2 shrink-0">
              <img src="/logo.png" alt="Astro Rattan" className="h-14 sm:h-16 w-auto" />
            </Link>

            {/* Desktop Navigation */}
            <div className="hidden lg:flex items-center gap-6 notranslate" translate="no">
              {serviceLinks.map((link) => {
                if (link.megaMenuKey && pageMegaMenus[link.megaMenuKey]) {
                  const menu = pageMegaMenus[link.megaMenuKey];
                  const isOpen = openMegaMenu === link.megaMenuKey;
                  const cols = menu.length;
                  const widthClass = cols <= 2 ? 'w-[400px]' : cols === 3 ? 'w-[560px]' : cols === 4 ? 'w-[680px]' : 'w-[800px]';
                  const gridClass =
                    cols === 1 ? 'grid-cols-1' :
                    cols === 2 ? 'grid-cols-2' :
                    cols === 3 ? 'grid-cols-3' :
                    cols === 4 ? 'grid-cols-4' :
                    cols === 5 ? 'grid-cols-5' :
                    'grid-cols-6';
                  return (
                    <div
                      key={link.key}
                      ref={isOpen ? megaMenuRef : undefined}
                      className="relative"
                      onMouseEnter={() => {
                        if (megaMenuTimer.current) clearTimeout(megaMenuTimer.current);
                        setOpenMegaMenu(link.megaMenuKey!);
                      }}
                      onMouseLeave={() => {
                        megaMenuTimer.current = setTimeout(() => setOpenMegaMenu(null), 150);
                      }}
                    >
                      <Link
                        to={link.href}
                        onClick={(e) => {
                          if (authRequiredRoutes.has(link.href) && !isAuthenticated) {
                            e.preventDefault();
                            navigate('/login');
                          }
                          setOpenMegaMenu(null);
                        }}
                        className="text-base text-foreground hover:text-sacred-gold-dark transition-colors tracking-wide inline-flex items-center gap-1"
                      >
                        {t(link.key)}
                        <ChevronDown className={`w-3.5 h-3.5 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
                      </Link>

                      {/* Mega Dropdown */}
                      {isOpen && (
                        <div className={`absolute top-full left-1/2 -translate-x-1/2 mt-2 ${widthClass} bg-background border border-sacred-gold/40 rounded-xl shadow-2xl shadow-sacred-gold/10 py-4 px-5 z-50`}
                          onMouseEnter={() => {
                            if (megaMenuTimer.current) clearTimeout(megaMenuTimer.current);
                          }}
                          onMouseLeave={() => {
                            megaMenuTimer.current = setTimeout(() => setOpenMegaMenu(null), 150);
                          }}
                        >
                          <div className={`grid ${gridClass} gap-4`}>
                            {menu.map((cat) => (
                              <div key={cat.key}>
                                <p className="text-[11px] font-bold uppercase tracking-wider text-sacred-gold-dark mb-2 border-b border-sacred-gold/20 pb-1">
                                  {language === 'hi' ? cat.label.hi : cat.label.en}
                                </p>
                                <ul className="space-y-0.5">
                                  {cat.tabs.map((tab) => (
                                    <li key={tab.value}>
                                      <Link
                                        to={`${link.href}?tab=${tab.value}`}
                                        onClick={(e) => {
                                          if (authRequiredRoutes.has(link.href) && !isAuthenticated) {
                                            e.preventDefault();
                                            navigate('/login');
                                          }
                                          setOpenMegaMenu(null);
                                        }}
                                        className="block text-xs text-foreground hover:text-sacred-gold-dark hover:bg-sacred-gold/5 rounded px-1.5 py-1 transition-colors leading-tight"
                                      >
                                        {language === 'hi' ? tab.hi : tab.en}
                                      </Link>
                                    </li>
                                  ))}
                                </ul>
                              </div>
                            ))}
                          </div>
                          <div className="mt-3 pt-2 border-t border-sacred-gold/20 text-center">
                            <Link
                              to={link.href}
                              onClick={(e) => {
                                if (authRequiredRoutes.has(link.href) && !isAuthenticated) {
                                  e.preventDefault();
                                  navigate('/login');
                                }
                                setOpenMegaMenu(null);
                              }}
                              className="text-xs font-semibold text-sacred-gold-dark hover:text-sacred-gold transition-colors"
                            >
                              {language === 'hi' ? 'सभी देखें →' : 'View all →'}
                            </Link>
                          </div>
                        </div>
                      )}
                    </div>
                  );
                }
                return (
                  <Link
                    key={link.key}
                    to={link.href}
                    onClick={(e) => {
                      if (authRequiredRoutes.has(link.href) && !isAuthenticated) {
                        e.preventDefault();
                        navigate('/login');
                      }
                    }}
                    className={
                      link.highlight
                        ? 'text-base font-semibold text-sacred-gold-dark border border-sacred-gold px-3 py-1 rounded-lg hover:bg-sacred-gold hover:text-white transition-all font-sans tracking-wide'
                        : 'text-base text-foreground hover:text-sacred-gold-dark transition-colors tracking-wide'
                    }
                  >
                    {t(link.key)}
                  </Link>
                );
              })}
            </div>

            {/* Action buttons */}
            <div className="flex items-center gap-1">
              <div className="hidden sm:block">
                <LanguageSwitcher />
              </div>

              {/* Persistent Dashboard link for astrologers/admins — always
                  visible so they can return to /astrologer from anywhere
                  without hunting in the profile dropdown. */}
              {isAuthenticated && (user?.role === 'astrologer' || user?.role === 'admin') && (
                <Link
                  to="/astrologer"
                  className="hidden sm:inline-flex items-center gap-1.5 ml-2 px-3 py-2 rounded-lg bg-sacred-gold-dark text-white hover:bg-sacred-gold transition-colors text-sm font-semibold"
                  title={language === 'hi' ? 'पेशेवर डैशबोर्ड' : 'Professional Dashboard'}
                >
                  <Briefcase className="w-4 h-4" />
                  <span className="hidden md:inline">
                    {language === 'hi' ? 'डैशबोर्ड' : 'Dashboard'}
                  </span>
                </Link>
              )}

              {isAuthenticated ? (
                <div ref={profileMenuRef} className="relative hidden sm:block">
                  <button
                    onClick={() => setIsProfileMenuOpen((prev) => !prev)}
                    className="ml-2 inline-flex items-center gap-1.5 px-3 py-2 border border-sacred-gold rounded-lg text-foreground hover:text-sacred-gold-dark hover:bg-gray-50 transition-colors"
                    title={t('nav.profile')}
                  >
                    <User className="w-4 h-4" />
                    <span className="text-sm font-medium">{t('nav.profile')}</span>
                    <ChevronDown className={`w-3.5 h-3.5 transition-transform ${isProfileMenuOpen ? 'rotate-180' : ''}`} />
                  </button>
                  {isProfileMenuOpen && (
                    <div className="absolute right-0 mt-2 w-44 bg-background border border-sacred-gold rounded-lg shadow-lg py-1 z-50">
                      <Link
                        to="/dashboard"
                        onClick={() => setIsProfileMenuOpen(false)}
                        className="flex items-center gap-2 px-3 py-2 text-sm text-foreground hover:bg-gray-50 hover:text-sacred-gold-dark transition-colors"
                      >
                        <User className="w-4 h-4" />
                        {t('nav.profile')}
                      </Link>
                      {/* P3.5 — Professional dashboard (astrologers + admins) */}
                      {(user?.role === 'astrologer' || user?.role === 'admin') && (
                        <Link
                          to="/astrologer"
                          onClick={() => setIsProfileMenuOpen(false)}
                          className="flex items-center gap-2 px-3 py-2 text-sm text-foreground hover:bg-gray-50 hover:text-sacred-gold-dark transition-colors"
                        >
                          <Briefcase className="w-4 h-4" />
                          {language === 'hi' ? 'पेशेवर डैशबोर्ड' : 'Professional'}
                        </Link>
                      )}
                      {user?.role === 'admin' && (
                        <Link
                          to="/admin"
                          onClick={() => setIsProfileMenuOpen(false)}
                          className="flex items-center gap-2 px-3 py-2 text-sm text-foreground hover:bg-gray-50 hover:text-sacred-gold-dark transition-colors"
                        >
                          <Shield className="w-4 h-4" />
                          {t('nav.admin')}
                        </Link>
                      )}
                      <button
                        onClick={() => {
                          logout();
                          setIsProfileMenuOpen(false);
                        }}
                        className="w-full flex items-center gap-2 px-3 py-2 text-sm text-foreground hover:bg-gray-50 hover:text-sacred-gold-dark transition-colors"
                      >
                        <LogOut className="w-4 h-4" />
                        {t('auth.signOut')}
                      </button>
                    </div>
                  )}
                </div>
              ) : (
                <Link to="/login" className="ml-2 px-4 py-2 bg-transparent border border-sacred-gold text-sacred-gold-dark text-base font-medium hover:bg-gray-50 hover:text-background transition-all hidden sm:flex items-center gap-1.5">
                  <Sparkles className="w-4 h-4" />
                  {t('auth.signIn')}
                </Link>
              )}

              {/* Mobile shortcut: Professional Dashboard for astrologers/admins */}
              {isAuthenticated && (user?.role === 'astrologer' || user?.role === 'admin') && (
                <Link
                  to="/astrologer"
                  className="p-2.5 text-sacred-gold-dark hover:text-sacred-gold transition-colors sm:hidden"
                  title={language === 'hi' ? 'पेशेवर डैशबोर्ड' : 'Professional Dashboard'}
                >
                  <Briefcase className="w-5 h-5" />
                </Link>
              )}

              {isAuthenticated && user?.role === 'admin' && (
                <Link to="/admin" className="p-2.5 text-foreground hover:text-sacred-gold-dark transition-colors sm:hidden" title={t('nav.admin')}>
                  <Shield className="w-5 h-5" />
                </Link>
              )}

              {/* Mobile toggle */}
              <button
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                className="lg:hidden p-2 text-foreground ml-1"
                aria-expanded={isMobileMenuOpen}
                aria-controls="mobile-menu"
                aria-label={isMobileMenuOpen ? t('common.closeMenu') : t('common.openMenu')}
              >
                {isMobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Mobile Menu */}
      <div id="mobile-menu" className={`fixed inset-0 z-40 lg:hidden transition-all duration-500 ${isMobileMenuOpen ? 'opacity-100 visible' : 'opacity-0 invisible pointer-events-none'}`}>
        <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={() => setIsMobileMenuOpen(false)} />
        <div className={`absolute top-20 left-4 right-4 bg-background backdrop-blur-lg border border-sacred-gold rounded-lg p-6 transition-all duration-500 ${isMobileMenuOpen ? 'translate-y-0 opacity-100' : '-translate-y-10 opacity-0'}`}>
          <div className="space-y-1">
            {serviceLinks.map((link) => {
              if (link.megaMenuKey && pageMegaMenus[link.megaMenuKey]) {
                const menu = pageMegaMenus[link.megaMenuKey];
                const isOpen = mobileMegaMenu === link.megaMenuKey;
                return (
                  <div key={link.key}>
                    <button
                      onClick={() => {
                        if (authRequiredRoutes.has(link.href) && !isAuthenticated) {
                          navigate('/login');
                          setIsMobileMenuOpen(false);
                          return;
                        }
                        setMobileMegaMenu((p) => (p === link.megaMenuKey ? null : link.megaMenuKey));
                      }}
                      className="w-full flex items-center justify-between py-3 px-3 text-foreground hover:text-sacred-gold-dark hover:bg-gray-50 transition-colors rounded-lg"
                    >
                      <span>{t(link.key)}</span>
                      <ChevronDown className={`w-4 h-4 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
                    </button>
                    {isOpen && (
                      <div className="pl-3 pr-1 pb-2 space-y-3">
                        {menu.map((cat) => (
                          <div key={cat.key}>
                            <p className="text-[10px] font-bold uppercase tracking-wider text-sacred-gold-dark mb-1 px-2">
                              {language === 'hi' ? cat.label.hi : cat.label.en}
                            </p>
                            <div className="grid grid-cols-2 gap-1">
                              {cat.tabs.map((tab) => (
                                <Link
                                  key={tab.value}
                                  to={`${link.href}?tab=${tab.value}`}
                                  onClick={() => setIsMobileMenuOpen(false)}
                                  className="block text-xs text-foreground hover:text-sacred-gold-dark hover:bg-sacred-gold/5 rounded px-2 py-1.5 transition-colors"
                                >
                                  {language === 'hi' ? tab.hi : tab.en}
                                </Link>
                              ))}
                            </div>
                          </div>
                        ))}
                        <Link
                          to={link.href}
                          onClick={() => setIsMobileMenuOpen(false)}
                          className="block text-xs font-semibold text-sacred-gold-dark hover:text-sacred-gold transition-colors px-2 py-1"
                        >
                          {language === 'hi' ? 'सभी देखें →' : 'View all →'}
                        </Link>
                      </div>
                    )}
                  </div>
                );
              }
              return (
                <Link
                  key={link.key}
                  to={link.href}
                  onClick={(e) => {
                    if (authRequiredRoutes.has(link.href) && !isAuthenticated) {
                      e.preventDefault();
                      navigate('/login');
                    }
                    setIsMobileMenuOpen(false);
                  }}
                  className={
                    link.highlight
                      ? 'block py-3 px-3 font-semibold text-sacred-gold-dark border border-sacred-gold rounded-lg hover:bg-sacred-gold hover:text-white transition-all font-sans'
                      : 'block py-3 px-3 text-foreground hover:text-sacred-gold-dark hover:bg-gray-50 transition-colors'
                  }
                >
                  {t(link.key)}
                </Link>
              );
	            })}
	            <div className="pt-4 mt-4 border-t border-sacred-gold space-y-3">
	              <LanguageSwitcher />
	              {isAuthenticated ? (
                <div className="space-y-2">
                  {(user?.role === 'astrologer' || user?.role === 'admin') && (
                    <Link
                      to="/astrologer"
                      onClick={() => setIsMobileMenuOpen(false)}
                      className="flex items-center gap-2 w-full px-4 py-3 bg-sacred-gold-dark text-white font-semibold justify-center hover:bg-sacred-gold transition-colors rounded-lg"
                    >
                      <Briefcase className="w-4 h-4" />
                      {language === 'hi' ? 'पेशेवर डैशबोर्ड' : 'Professional Dashboard'}
                    </Link>
                  )}
                  <Link
                    to="/dashboard"
                    onClick={() => setIsMobileMenuOpen(false)}
                    className="flex items-center gap-2 w-full px-4 py-3 border border-sacred-gold text-sacred-gold-dark font-medium justify-center hover:bg-gray-50 transition-colors"
                  >
                    <User className="w-4 h-4" />
                    {t('nav.profile')}
                  </Link>
                  <button
                    onClick={() => { logout(); setIsMobileMenuOpen(false); }}
                    className="flex items-center gap-2 w-full px-4 py-3 border border-sacred-gold text-sacred-gold-dark font-medium text-center justify-center hover:bg-gray-50 transition-colors"
                  >
                    <LogOut className="w-4 h-4" />
                    {t('auth.signOut')}
                  </button>
                </div>
              ) : (
                <Link
                  to="/login"
                  onClick={() => setIsMobileMenuOpen(false)}
                  className="flex items-center gap-2 w-full px-4 py-3 border border-sacred-gold text-sacred-gold-dark font-medium text-center justify-center hover:bg-gray-50 transition-colors"
                >
                  <Sparkles className="w-4 h-4" />
                  {t('auth.signIn')}
                </Link>
              )}
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
