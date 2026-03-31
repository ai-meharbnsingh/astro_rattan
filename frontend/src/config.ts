/**
 * VEDIC ASTROLOGY WEBSITE CONFIGURATION
 * 
 * Modify this file to customize all content, images, and assets.
 * All paths are relative to the public folder.
 */

// ==================== SERVICE CARDS ====================
export const serviceCards = [
  {
    id: 'kundli',
    title: 'Kundli Generation',
    subtitle: 'Generate your Vedic Birth Chart',
    buttonText: 'Start Kundli',
    icon: '🔮',
    image: '/images/services/kundli.png',
    gradient: 'from-orange-400 to-amber-600'
  },
  {
    id: 'horoscope',
    title: 'Horoscope',
    subtitle: 'Daily Monthly Yearly',
    rating: '4.7/5',
    buttonText: 'Read Now',
    icon: '☀️',
    image: '/images/services/horoscope.png',
    gradient: 'from-amber-500 to-yellow-600'
  },
  {
    id: 'matching',
    title: 'Kundli Matching',
    subtitle: 'Marriage Compatibility Check',
    buttonText: 'Check Match',
    icon: '💑',
    image: '/images/services/matching.png',
    gradient: 'from-orange-500 to-red-500'
  },
  {
    id: 'muhurat',
    title: 'Muhurat Finder',
    subtitle: 'Find Auspicious Dates & Timings',
    buttonText: 'Search',
    icon: '📅',
    image: '/images/services/muhurat.png',
    gradient: 'from-yellow-500 to-amber-600'
  },
  {
    id: 'library',
    title: 'Spiritual Library',
    subtitle: 'Bhagavad Gita, Mantras, Aarti, Chalisa...',
    buttonText: 'Explore',
    icon: '📚',
    image: '/images/services/library.png',
    gradient: 'from-amber-600 to-orange-700'
  }
];

// ==================== STATS BAR ====================
export const statsData = [
  {
    id: 'kundli-count',
    value: '500,000+',
    label: 'Kundli Generated',
    icon: '📊'
  },
  {
    id: 'astrologers',
    value: '120+',
    label: 'Expert Astrologers',
    icon: '👨‍🦳'
  },
  {
    id: 'rating',
    value: '4.9/5',
    label: 'Trusted Since 1998',
    icon: '⭐'
  },
  {
    id: 'certified',
    value: '100%',
    label: 'Certified & Brangcers',
    icon: '✓'
  },
  {
    id: 'energized',
    value: '100% Certified',
    label: '4. Energiced',
    icon: '⚡'
  }
];

// ==================== DAILY INSIGHTS ====================
export const dailyInsights = {
  title: 'Daily Insights',
  subtitle: 'mewmirtng Reports',
  note: 'Nove...',
  items: [
    {
      id: 'rahu-kaala',
      title: 'Rahu Kaala',
      time: '3:114 PM - 4:52 PM',
      icon: '🌙'
    },
    {
      id: 'sun',
      title: 'Sun',
      subtitle: 'Anrehin - Dintcted',
      time: '8:99',
      action: 'Harn',
      icon: '☀️'
    },
    {
      id: 'hora-timings',
      title: 'Hora Timings',
      time: '1.16 - 4.42%',
      icon: '⏰'
    },
    {
      id: 'place-timings',
      title: 'Place Timings',
      subtitle: '4.3.00 Aemlogy Deloes',
      icon: '📍'
    },
    {
      id: 'tilkut-chaturthi',
      title: 'Tilkut Chaturthi',
      buttonText: 'See Panchang',
      icon: '🪔'
    },
    {
      id: 'rashi-calculator',
      title: 'Rashi Calculator',
      buttonText: 'Calculate Rashi',
      icon: '♈'
    }
  ]
};

// ==================== AI ASTROLOGER ====================
export const aiAstrologer = {
  title: 'Ai Atrologer',
  subtitle: 'Tap Roniat Reninders',
  astrologerName: 'Aman Sharma',
  status: 'TS Raepey Tour Hane CONTE PM',
  statusDetail: 'Tous Genee: Pucer 10ate.',
  buttonText: 'Generate Kundli',
  chatPreview: {
    greeting: 'Namaste: Aman Sharma,',
    intro: 'I am veu: &, Matrologert, Ask-me ary question about your Kundli.',
    sampleQuestion: 'Steady job milega kya in 2026?',
    response: 'Reading your Kundli ....',
    insight: 'Based on your planetary positions. I will share personalized insights.',
    detailedResponse: `In 2026, the major period will be of hotel while the sub-period will of of Jupiter.

Ketu with Jupiter in the 9th house inclustes opportunities, hit you muat teap disciplined. Seturn in your Pith house vaew of delays.

Remedies, include syollow sapphire-ring. daily Varna(posjs`
  },
  image: '/images/ai-astrologer.png',
  backgroundImage: '/images/sage-meditation.png'
};

// ==================== CATEGORY TABS ====================
export const categoryTabs = [
  { id: 'numerology', label: 'Numerology', icon: '🔢' },
  { id: 'tarot', label: 'Tarot', icon: '🃏' },
  { id: 'kp', label: 'KP', sublabel: 'Aantrology', icon: '📐' },
  { id: 'lal-rets', label: 'LAL Rets', icon: '📜' },
  { id: 'lal-kitab', label: 'Lal Kitab', icon: '📖' },
  { id: 'remedies', label: 'Remedies', icon: '🪔' }
];

// ==================== AI ASTROLOGY ASSISTANT ====================
export const aiAssistant = {
  sectionNumber: '2.',
  title: 'AI ASTROLOGY ASSISTANT',
  subtitle: 'Smart Chatbot, Instant Astrology, Guide your users with personalized A1 Insights.',
  categories: [
    { id: 'numerology', label: 'Numerology', icon: '/images/categories/numerology.png' },
    { id: 'tarot', label: 'Tarot Reading', icon: '/images/categories/tarot.png' },
    { id: 'kp', label: 'KP Astrology', icon: '/images/categories/kp.png' },
    { id: 'lal-kitab', label: 'Lal Kitab', icon: '/images/categories/lal-kitab.png' }
  ],
  phoneMockup: {
    time: '19:00',
    appName: 'Ai Arologer'
  }
};

// ==================== RECOMMENDED SECTION ====================
export const recommendedSection = {
  title: 'Recommended For You',
  arrow: '→',
  cards: [
    {
      id: 'retrograde',
      title: 'Are intense retrogrades affecting your 1st house?',
      subtitle: "Here's what to do.",
      image: '/images/recommended/retrograde.png'
    },
    {
      id: 'rahu-jade',
      title: 'Rahu Green Jade',
      price: '₹3,500+',
      buttonText: 'Book a Call',
      image: '/images/recommended/jade.png'
    }
  ],
  bottomCategories: [
    { id: 'numerology', label: 'Numerology', icon: '/images/categories/numerology.png' },
    { id: 'tarot', label: 'Tarot Reading', icon: '/images/categories/tarot.png' },
    { id: 'kp', label: 'KP Astrology', icon: '/images/categories/kp.png' },
    { id: 'lal-kitab', label: 'Lal Kitab Remedies', icon: '/images/categories/lal-kitab.png' }
  ]
};

// ==================== SHOP SECTION ====================
export const shopSection = {
  label: 'PRAITS SKONS',
  title: 'Shop Astrovedic',
  products: [
    {
      id: 'gemstone',
      name: 'Gemstone Order',
      rating: 5,
      reviews: 'Franee Bobang',
      image: '/images/shop/gemstone.png'
    }
  ],
  backgroundImage: '/images/temple-bg.png'
};

// ==================== IMAGES CONFIGURATION ====================
// Use these paths to replace images. Place your images in public/images/
export const imagePaths = {
  // Service card images
  services: {
    kundli: '/images/services/kundli.png',
    horoscope: '/images/services/horoscope.png',
    matching: '/images/services/matching.png',
    muhurat: '/images/services/muhurat.png',
    library: '/images/services/library.png'
  },
  
  // AI Astrologer
  aiAstrologer: '/images/ai-astrologer.png',
  sageMeditation: '/images/sage-meditation.png',
  
  // Category icons
  categories: {
    numerology: '/images/categories/numerology.png',
    tarot: '/images/categories/tarot.png',
    kp: '/images/categories/kp.png',
    lalKitab: '/images/categories/lal-kitab.png'
  },
  
  // Recommended section
  recommended: {
    retrograde: '/images/recommended/retrograde.png',
    jade: '/images/recommended/jade.png'
  },
  
  // Shop section
  shop: {
    gemstone: '/images/shop/gemstone.png',
    templeBg: '/images/temple-bg.png'
  }
};

// ==================== COLORS CONFIGURATION ====================
// Modify these to change the color scheme
export const colors = {
  // Primary colors
  primary: '#D2691E',
  primaryDark: '#8B4513',
  primaryLight: '#E67E22',
  
  // Gold/Amber accents
  gold: '#DAA520',
  goldLight: '#FFD700',
  
  // Background colors
  parchment: '#F5E6D3',
  parchmentDark: '#E8D4BC',
  cream: '#FFF8E7',
  
  // Text colors
  brown: '#5D4037',
  brownLight: '#8D6E63',
  
  // Border colors
  border: '#D4A574',
  
  // Saffron
  saffron: '#FF9933',
  saffronDark: '#E65100'
};

// ==================== TYPOGRAPHY CONFIGURATION ====================
export const typography = {
  // Heading font (decorative/traditional)
  heading: "'Cinzel', serif",
  
  // Body font (clean/readable)
  body: "'Noto Sans', sans-serif",
  
  // Alternative serif for subtitles
  serif: "'Cormorant Garamond', serif"
};

// ==================== ANIMATION CONFIGURATION ====================
export const animations = {
  // Enable/disable animations
  enabled: true,
  
  // Animation durations (in seconds)
  duration: {
    fast: 0.2,
    normal: 0.3,
    slow: 0.5
  },
  
  // Floating animation for decorative elements
  floating: true
};

// ==================== EXPORT DEFAULT ====================
export default {
  serviceCards,
  statsData,
  dailyInsights,
  aiAstrologer,
  categoryTabs,
  aiAssistant,
  recommendedSection,
  shopSection,
  imagePaths,
  colors,
  typography,
  animations
};
