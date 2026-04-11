import { useRef, useState } from 'react';
import { X, Download, Printer, ChevronRight, MapPin, Calendar, Clock, User } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useTranslation } from '@/lib/i18n';
import { translateBackend, translatePlanet, translateSign, translateNakshatra, translateLabel } from '@/lib/backend-translations';

interface KundliData {
  name: string;
  date: string;
  time: string;
  place: string;
  latitude: string;
  longitude: string;
  timezone: string;
}

interface PlanetPosition {
  planet: string;
  sign: string;
  house: number;
  degree: string;
  nakshatra: string;
  pad: number;
}

interface DashaPeriod {
  planet: string;
  startDate: string;
  endDate: string;
  years: number;
}

const samplePlanets: PlanetPosition[] = [
  { planet: 'Sun', sign: 'Leo', house: 1, degree: '15°32\'', nakshatra: 'Magha', pad: 2 },
  { planet: 'Moon', sign: 'Taurus', house: 10, degree: '22°15\'', nakshatra: 'Rohini', pad: 4 },
  { planet: 'Mars', sign: 'Aries', house: 9, degree: '8°45\'', nakshatra: 'Ashwini', pad: 1 },
  { planet: 'Mercury', sign: 'Virgo', house: 2, degree: '5°20\'', nakshatra: 'Uttara Phalguni', pad: 3 },
  { planet: 'Jupiter', sign: 'Pisces', house: 8, degree: '12°10\'', nakshatra: 'Revati', pad: 2 },
  { planet: 'Venus', sign: 'Libra', house: 3, degree: '28°45\'', nakshatra: 'Vishakha', pad: 4 },
  { planet: 'Saturn', sign: 'Aquarius', house: 7, degree: '18°30\'', nakshatra: 'Shatabhisha', pad: 1 },
  { planet: 'Rahu', sign: 'Scorpio', house: 4, degree: '3°15\'', nakshatra: 'Anuradha', pad: 3 },
  { planet: 'Ketu', sign: 'Taurus', house: 10, degree: '3°15\'', nakshatra: 'Krittika', pad: 1 },
];

const sampleDasha: DashaPeriod[] = [
  { planet: 'Moon', startDate: '04-01-2026', endDate: '04-01-2036', years: 10 },
  { planet: 'Mars', startDate: '04-01-2036', endDate: '04-04-2043', years: 7 },
  { planet: 'Rahu', startDate: '04-04-2043', endDate: '04-04-2061', years: 18 },
];

// Only PRESENT Yogas (not showing absent ones)
const presentYogas = [
  { name: 'Gajakesari Yoga', planets: 'Moon-Jupiter', effect: 'Wealth & Wisdom', strength: 'Strong' },
  { name: 'Budha-Aditya Yoga', planets: 'Sun-Mercury', effect: 'Intelligence', strength: 'Medium' },
  { name: 'Viparita Raja Yoga', planets: '6th-8th-12th lords', effect: 'Success through obstacles', strength: 'Strong' },
];

// Only PRESENT Doshas (not showing absent ones)
const presentDoshas = [
  { name: 'Manglik Dosha', planet: 'Mars', effect: 'Delay in marriage', remedy: 'Hanuman puja', severity: 'Medium' },
];

// Empty arrays would mean no yogas/doshas present
// const presentYogas: any[] = []; // Example: No yogas
// const presentDoshas: any[] = []; // Example: No doshas

interface KundliSummaryModalProps {
  isOpen: boolean;
  onClose: () => void;
  data: KundliData;
  onViewFullReport: () => void;
}

export default function KundliSummaryModal({ isOpen, onClose, data, onViewFullReport }: KundliSummaryModalProps) {
  const modalRef = useRef<HTMLDivElement>(null);
  const [showChart, setShowChart] = useState(true);
  const { t, language } = useTranslation();

  if (!isOpen) return null;

  const planetColors: Record<string, string> = {
    Sun: '#FFD700',
    Moon: '#C0C0C0',
    Mars: '#FF4500',
    Mercury: '#00CED1',
    Jupiter: '#FFA500',
    Venus: '#FF69B4',
    Saturn: '#808080',
    Rahu: '#4169E1',
    Ketu: '#8B4513',
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-2 sm:p-4 bg-black backdrop-blur-sm">
      <div 
        ref={modalRef}
        className="relative w-full max-w-6xl bg-[var(--dark-bg)] rounded-xl border border-[var(--sacred-gold-hex)] shadow-2xl overflow-hidden"
        style={{ maxHeight: '95vh' }}
      >
        {/* Header */}
        <div className="sticky top-0 z-10 bg-gradient-to-r from-[var(--dark-bg)] via-[#111] to-[var(--dark-bg)] border-b border-[var(--sacred-gold-hex)] p-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-full bg-[var(--sacred-gold-hex)] border border-[var(--sacred-gold-hex)] flex items-center justify-center">
              <span className="text-2xl">☉</span>
            </div>
            <div>
              <h2 className="text-xl font-bold text-white" style={{ fontFamily: 'var(--font-sacred, Inter, sans-serif)' }}>
                {t('section.vedicBirthChart')}
              </h2>
              <p className="text-sm text-[#d4af37]">{language === 'hi' ? 'पूर्ण विश्लेषण सारांश' : 'Complete Analysis Summary'}</p>
            </div>
          </div>
          
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              className="hidden sm:flex items-center gap-2 border-[var(--sacred-gold-hex)] text-[var(--sacred-gold-hex)] hover:bg-[var(--sacred-gold-hex)]"
            >
              <Download className="w-4 h-4" />
              {language === 'hi' ? 'पीडीएफ' : 'PDF'}
            </Button>
            <Button
              variant="outline"
              size="sm"
              className="hidden sm:flex items-center gap-2 border-[var(--sacred-gold-hex)] text-[var(--sacred-gold-hex)] hover:bg-[var(--sacred-gold-hex)]"
            >
              <Printer className="w-4 h-4" />
              {language === 'hi' ? 'प्रिंट' : 'Print'}
            </Button>
            <Button
              onClick={onViewFullReport}
              className="flex items-center gap-2 bg-[var(--sacred-gold-hex)] text-black hover:bg-[var(--sacred-gold)]"
            >
              {t('kundli.fullReport')}
              <ChevronRight className="w-4 h-4" />
            </Button>
            <button
              onClick={onClose}
              className="ml-2 w-10 h-10 rounded-full bg-white hover:bg-white flex items-center justify-center text-white hover:text-white transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Main Content - Landscape Layout */}
        <div className="p-4 overflow-y-auto" style={{ maxHeight: 'calc(95vh - 80px)' }}>
          
          {/* User Info Bar */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-4 p-3 bg-[#111] rounded-xl border border-[var(--sacred-gold-hex)]">
            <div className="flex items-center gap-2">
              <User className="w-4 h-4 text-[#d4af37]" />
              <div>
                <p className="text-sm text-white">{language === 'hi' ? 'नाम' : 'Name'}</p>
                <p className="text-sm font-medium text-white">{data.name}</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Calendar className="w-4 h-4 text-[#d4af37]" />
              <div>
                <p className="text-sm text-white">{language === 'hi' ? 'जन्म तिथि' : 'Birth Date'}</p>
                <p className="text-sm font-medium text-white">{data.date}</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Clock className="w-4 h-4 text-[#d4af37]" />
              <div>
                <p className="text-sm text-white">{language === 'hi' ? 'समय' : 'Time'}</p>
                <p className="text-sm font-medium text-white">{data.time}</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <MapPin className="w-4 h-4 text-[#d4af37]" />
              <div>
                <p className="text-sm text-white">{language === 'hi' ? 'स्थान' : 'Place'}</p>
                <p className="text-sm font-medium text-white">{data.place}</p>
              </div>
            </div>
          </div>

          {/* Main Grid - Chart + Details */}
          <div className="grid lg:grid-cols-3 gap-4">
            
            {/* Left - Main Birth Chart */}
            <div className="lg:col-span-2 space-y-4">
              {/* Chart Container */}
              <div className="bg-[#111] rounded-xl border border-[var(--sacred-gold-hex)] p-4">
                <h3 className="text-lg font-semibold text-[#d4af37] mb-3 text-center" style={{ fontFamily: 'var(--font-sacred, Inter, sans-serif)' }}>
                  {t('section.rashiD1')}
                </h3>
                
                {/* North Indian Style Chart */}
                <div className="relative w-full aspect-square max-w-md mx-auto">
                  <svg viewBox="0 0 300 300" className="w-full h-full">
                    {/* Outer diamond */}
                    <polygon 
                      points="150,10 290,150 150,290 10,150" 
                      fill="none" 
                      stroke="#d4af37" 
                      strokeWidth="2"
                    />
                    {/* Inner diamond */}
                    <polygon 
                      points="150,40 260,150 150,260 40,150" 
                      fill="none" 
                      stroke="#d4af37" 
                      strokeWidth="1"
                      
                    />
                    {/* Cross lines */}
                    <line x1="150" y1="10" x2="150" y2="290" stroke="#d4af37" strokeWidth="1" />
                    <line x1="10" y1="150" x2="290" y2="150" stroke="#d4af37" strokeWidth="1" opacity="0.3"/>
                    
                    {/* House numbers and planets */}
                    {/* House 1 (Ascendant) - Top */}
                    <text x="150" y="30" textAnchor="middle" fill="#d4af37" fontSize="14" fontWeight="bold">1</text>
                    <text x="150" y="55" textAnchor="middle" fill="#FFD700" fontSize="14">Su</text>
                    <text x="150" y="72" textAnchor="middle" fill="#FF69B4" fontSize="14">Ve</text>
                    
                    {/* House 2 - Top Right */}
                    <text x="200" y="60" textAnchor="middle" fill="#d4af37" fontSize="14" fontWeight="bold">2</text>
                    <text x="200" y="80" textAnchor="middle" fill="#00CED1" fontSize="14">Me</text>
                    
                    {/* House 3 - Right */}
                    <text x="240" y="110" textAnchor="middle" fill="#d4af37" fontSize="14" fontWeight="bold">3</text>
                    <text x="240" y="130" textAnchor="middle" fill="#FF69B4" fontSize="14">Ve</text>
                    
                    {/* House 4 - Bottom Right */}
                    <text x="200" y="180" textAnchor="middle" fill="#d4af37" fontSize="14" fontWeight="bold">4</text>
                    <text x="200" y="200" textAnchor="middle" fill="#4169E1" fontSize="14">Ra</text>
                    
                    {/* House 5 - Bottom */}
                    <text x="150" y="230" textAnchor="middle" fill="#d4af37" fontSize="14" fontWeight="bold">5</text>
                    <text x="150" y="250" textAnchor="middle" fill="#FF4500" fontSize="14" >Ma</text>
                    
                    {/* House 6 - Bottom Left */}
                    <text x="100" y="180" textAnchor="middle" fill="#d4af37" fontSize="14" fontWeight="bold">6</text>
                    
                    {/* House 7 - Left Bottom */}
                    <text x="60" y="150" textAnchor="middle" fill="#d4af37" fontSize="14" fontWeight="bold">7</text>
                    <text x="60" y="170" textAnchor="middle" fill="#808080" fontSize="14">Sa</text>
                    
                    {/* House 8 - Left */}
                    <text x="60" y="110" textAnchor="middle" fill="#d4af37" fontSize="14" fontWeight="bold">8</text>
                    <text x="60" y="90" textAnchor="middle" fill="#FFA500" fontSize="14">Ju</text>
                    
                    {/* House 9 - Top Left */}
                    <text x="100" y="60" textAnchor="middle" fill="#d4af37" fontSize="14" fontWeight="bold">9</text>
                    <text x="100" y="80" textAnchor="middle" fill="#FF4500" fontSize="14">Ma</text>
                    
                    {/* House 10 - Top Left Upper */}
                    <text x="110" y="35" textAnchor="middle" fill="#d4af37" fontSize="14" fontWeight="bold">10</text>
                    <text x="110" y="50" textAnchor="middle" fill="#C0C0C0" fontSize="14">Mo</text>
                    <text x="135" y="50" textAnchor="middle" fill="#8B4513" fontSize="14">Ke</text>
                    
                    {/* House 11 - Top Right Upper */}
                    <text x="190" y="35" textAnchor="middle" fill="#d4af37" fontSize="14" fontWeight="bold">11</text>
                    
                    {/* House 12 - Right Upper */}
                    <text x="240" y="70" textAnchor="middle" fill="#d4af37" fontSize="14" fontWeight="bold">12</text>
                  </svg>
                </div>

                {/* Lagna Info */}
                <div className="mt-4 p-3 bg-[var(--sacred-gold-hex)] rounded-lg border border-[var(--sacred-gold-hex)]">
                  <div className="flex flex-wrap gap-4 justify-center text-center">
                    <div>
                      <p className="text-sm text-white">{language === 'hi' ? 'लग्न' : 'Ascendant'}</p>
                      <p className="text-lg font-bold text-[#d4af37]">{translateSign('Leo', language)}</p>
                    </div>
                    <div className="w-px bg-[var(--sacred-gold-hex)]" />
                    <div>
                      <p className="text-sm text-white">{language === 'hi' ? 'चंद्र राशि' : 'Moon Sign'}</p>
                      <p className="text-lg font-bold text-[#C0C0C0]">{translateSign('Taurus', language)}</p>
                    </div>
                    <div className="w-px bg-[var(--sacred-gold-hex)]" />
                    <div>
                      <p className="text-sm text-white">{language === 'hi' ? 'सूर्य राशि' : 'Sun Sign'}</p>
                      <p className="text-lg font-bold text-[#FFD700]">{translateSign('Leo', language)}</p>
                    </div>
                    <div className="w-px bg-[var(--sacred-gold-hex)]" />
                    <div>
                      <p className="text-sm text-white">{language === 'hi' ? 'नक्षत्र' : 'Nakshatra'}</p>
                      <p className="text-lg font-bold text-white">{translateNakshatra('Rohini', language)}</p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Divisional Charts */}
              <div className="grid grid-cols-3 gap-3">
                <div className="bg-[#111] rounded-lg border border-[var(--sacred-gold-hex)] p-3 text-center">
                  <p className="text-sm text-white mb-1">{t('section.navamshaD9')}</p>
                  <p className="text-lg font-semibold text-[#d4af37]">{translateSign('Scorpio', language)}</p>
                </div>
                <div className="bg-[#111] rounded-lg border border-[var(--sacred-gold-hex)] p-3 text-center">
                  <p className="text-sm text-white mb-1">{language === 'hi' ? 'दशमांश (D10)' : 'Dashamsha (D10)'}</p>
                  <p className="text-lg font-semibold text-[#d4af37]">{translateSign('Capricorn', language)}</p>
                </div>
                <div className="bg-[#111] rounded-lg border border-[var(--sacred-gold-hex)] p-3 text-center">
                  <p className="text-sm text-white mb-1">{language === 'hi' ? 'सप्तमांश (D7)' : 'Saptamsha (D7)'}</p>
                  <p className="text-lg font-semibold text-[#d4af37]">{translateSign('Libra', language)}</p>
                </div>
              </div>
            </div>

            {/* Right - Planet Positions & Dasha */}
            <div className="space-y-4">
              {/* Planet Positions */}
              <div className="bg-[#111] rounded-xl border border-[var(--sacred-gold-hex)] p-3">
                <h3 className="text-sm font-semibold text-[#d4af37] mb-2" style={{ fontFamily: 'var(--font-sacred, Inter, sans-serif)' }}>
                  {language === 'hi' ? 'ग्रह स्थिति' : 'Planetary Positions'}
                </h3>
                <div className="space-y-1 max-h-48 overflow-y-auto">
                  {samplePlanets.map((planet, idx) => (
                    <div 
                      key={idx}
                      className="flex items-center justify-between p-2 rounded bg-black text-sm"
                    >
                      <div className="flex items-center gap-2">
                        <span 
                          className="w-2 h-2 rounded-full"
                          style={{ backgroundColor: planetColors[planet.planet] || '#fff' }}
                        />
                        <span className="text-white font-medium">{translatePlanet(planet.planet, language)}</span>
                      </div>
                      <div className="text-right">
                        <span className="text-[#d4af37]">{translateSign(planet.sign, language)}</span>
                        <span className="text-white ml-1">H{planet.house}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Current Dasha */}
              <div className="bg-[#111] rounded-xl border border-[var(--sacred-gold-hex)] p-3">
                <h3 className="text-sm font-semibold text-[#d4af37] mb-2" style={{ fontFamily: 'var(--font-sacred, Inter, sans-serif)' }}>
                  {t('section.vimshottariDasha')}
                </h3>
                <div className="space-y-2">
                  {sampleDasha.map((period, idx) => (
                    <div 
                      key={idx}
                      className={`p-2 rounded text-sm ${idx === 0 ? 'bg-[var(--sacred-gold-hex)] border border-[var(--sacred-gold-hex)]' : 'bg-black'}`}
                    >
                      <div className="flex items-center justify-between mb-1">
                        <span className="font-semibold text-white">{translatePlanet(period.planet, language)} {t('kundli.mahadasha')}</span>
                        <span className="text-[#d4af37]">{period.years} {language === 'hi' ? 'वर्ष' : 'Years'}</span>
                      </div>
                      <p className="text-white">{period.startDate} - {period.endDate}</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Quick Stats */}
              <div className="grid grid-cols-2 gap-2 mb-4">
                <div className="bg-[#111] rounded-lg border border-[var(--sacred-gold-hex)] p-2 text-center">
                  <p className="text-sm text-white">{language === 'hi' ? 'गण' : 'Gana'}</p>
                  <p className="text-sm font-semibold text-white">{translateBackend('Manushya', language)}</p>
                </div>
                <div className="bg-[#111] rounded-lg border border-[var(--sacred-gold-hex)] p-2 text-center">
                  <p className="text-sm text-white">{language === 'hi' ? 'योनि' : 'Yoni'}</p>
                  <p className="text-sm font-semibold text-white">{translateBackend('Serpent', language)}</p>
                </div>
                <div className="bg-[#111] rounded-lg border border-[var(--sacred-gold-hex)] p-2 text-center">
                  <p className="text-sm text-white">{language === 'hi' ? 'नाड़ी' : 'Nadi'}</p>
                  <p className="text-sm font-semibold text-white">{translateBackend('Kapha', language)}</p>
                </div>
                <div className="bg-[#111] rounded-lg border border-[var(--sacred-gold-hex)] p-2 text-center">
                  <p className="text-sm text-white">{language === 'hi' ? 'वर्ण' : 'Varna'}</p>
                  <p className="text-sm font-semibold text-white">{translateBackend('Kshatriya', language)}</p>
                </div>
              </div>

              {/* PRESENT Yogas Only - Not showing absent ones */}
              {presentYogas.length > 0 && (
                <div className="bg-[#111] rounded-xl border border-green-300 p-3 mb-4">
                  <h3 className="text-sm font-semibold text-green-400 mb-2 flex items-center gap-2" style={{ fontFamily: 'var(--font-sacred, Inter, sans-serif)' }}>
                    <span>✦</span> {language === 'hi' ? 'उपस्थित योग' : 'Present Yogas'} ({presentYogas.length})
                  </h3>
                  <div className="space-y-2">
                    {presentYogas.map((yoga, idx) => (
                      <div key={idx} className="p-2 rounded bg-green-500 border border-green-300 text-sm">
                        <div className="flex items-center justify-between mb-1">
                          <span className="font-semibold text-white">{translateBackend(yoga.name, language)}</span>
                          <span className={`px-2 py-0.5 rounded-full text-label ${
                            yoga.strength === 'Strong' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                          }`}>
                            {translateLabel(yoga.strength, language)}
                          </span>
                        </div>
                        <p className="text-green-400">{translateBackend(yoga.planets, language)} • {translateBackend(yoga.effect, language)}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* PRESENT Doshas Only - Not showing absent ones */}
              {presentDoshas.length > 0 && (
                <div className="bg-[#111] rounded-xl border border-red-300 p-3">
                  <h3 className="text-sm font-semibold text-red-400 mb-2 flex items-center gap-2" style={{ fontFamily: 'var(--font-sacred, Inter, sans-serif)' }}>
                    <span>⚠</span> {language === 'hi' ? 'उपस्थित दोष' : 'Present Doshas'} ({presentDoshas.length})
                  </h3>
                  <div className="space-y-2">
                    {presentDoshas.map((dosha, idx) => (
                      <div key={idx} className="p-2 rounded bg-red-500 border border-red-300 text-sm">
                        <div className="flex items-center justify-between mb-1">
                          <span className="font-semibold text-white">{translateBackend(dosha.name, language)}</span>
                          <span className={`px-2 py-0.5 rounded-full text-label ${
                            dosha.severity === 'High' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'
                          }`}>
                            {translateLabel(dosha.severity, language)}
                          </span>
                        </div>
                        <p className="text-red-400 mb-1">{translatePlanet(dosha.planet, language)} • {translateBackend(dosha.effect, language)}</p>
                        <p className="text-label text-white">💡 {language === 'hi' ? 'उपाय' : 'Remedy'}: {translateBackend(dosha.remedy, language)}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* No Yogas/Doshas Message */}
              {presentYogas.length === 0 && presentDoshas.length === 0 && (
                <div className="bg-[#111] rounded-xl border border-[var(--sacred-gold-hex)] p-3 text-center">
                  <p className="text-sm text-white">{language === 'hi' ? 'कोई महत्वपूर्ण योग या दोष नहीं मिला' : 'No significant Yogas or Doshas detected'}</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
