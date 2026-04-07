import { useRef, useState } from 'react';
import { X, Download, Printer, ChevronRight, MapPin, Calendar, Clock, User } from 'lucide-react';
import { Button } from '@/components/ui/button';

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
    <div className="fixed inset-0 z-50 flex items-center justify-center p-2 sm:p-4 bg-black/90 backdrop-blur-sm">
      <div 
        ref={modalRef}
        className="relative w-full max-w-6xl bg-[#0a0a0a] rounded-2xl border border-[#d4af37]/30 shadow-2xl overflow-hidden"
        style={{ maxHeight: '95vh' }}
      >
        {/* Header */}
        <div className="sticky top-0 z-10 bg-gradient-to-r from-[#0a0a0a] via-[#111] to-[#0a0a0a] border-b border-[#d4af37]/20 p-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-full bg-[#d4af37]/10 border border-[#d4af37]/30 flex items-center justify-center">
              <span className="text-2xl">☉</span>
            </div>
            <div>
              <h2 className="text-xl font-bold text-white" style={{ fontFamily: 'var(--font-sacred, Cormorant Garamond, serif)' }}>
                Vedic Birth Chart
              </h2>
              <p className="text-sm text-[#d4af37]">Complete Analysis Summary</p>
            </div>
          </div>
          
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              className="hidden sm:flex items-center gap-2 border-[#d4af37]/30 text-[#d4af37] hover:bg-[#d4af37]/10"
            >
              <Download className="w-4 h-4" />
              PDF
            </Button>
            <Button
              variant="outline"
              size="sm"
              className="hidden sm:flex items-center gap-2 border-[#d4af37]/30 text-[#d4af37] hover:bg-[#d4af37]/10"
            >
              <Printer className="w-4 h-4" />
              Print
            </Button>
            <Button
              onClick={onViewFullReport}
              className="flex items-center gap-2 bg-[#d4af37] text-black hover:bg-[#ffd700]"
            >
              Full Report
              <ChevronRight className="w-4 h-4" />
            </Button>
            <button
              onClick={onClose}
              className="ml-2 w-10 h-10 rounded-full bg-white/5 hover:bg-white/10 flex items-center justify-center text-white/60 hover:text-white transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Main Content - Landscape Layout */}
        <div className="p-4 overflow-y-auto" style={{ maxHeight: 'calc(95vh - 80px)' }}>
          
          {/* User Info Bar */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-4 p-3 bg-[#111] rounded-xl border border-[#d4af37]/10">
            <div className="flex items-center gap-2">
              <User className="w-4 h-4 text-[#d4af37]" />
              <div>
                <p className="text-xs text-white/50">Name</p>
                <p className="text-sm font-medium text-white">{data.name}</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Calendar className="w-4 h-4 text-[#d4af37]" />
              <div>
                <p className="text-xs text-white/50">Birth Date</p>
                <p className="text-sm font-medium text-white">{data.date}</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Clock className="w-4 h-4 text-[#d4af37]" />
              <div>
                <p className="text-xs text-white/50">Time</p>
                <p className="text-sm font-medium text-white">{data.time}</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <MapPin className="w-4 h-4 text-[#d4af37]" />
              <div>
                <p className="text-xs text-white/50">Place</p>
                <p className="text-sm font-medium text-white">{data.place}</p>
              </div>
            </div>
          </div>

          {/* Main Grid - Chart + Details */}
          <div className="grid lg:grid-cols-3 gap-4">
            
            {/* Left - Main Birth Chart */}
            <div className="lg:col-span-2 space-y-4">
              {/* Chart Container */}
              <div className="bg-[#111] rounded-xl border border-[#d4af37]/20 p-4">
                <h3 className="text-lg font-semibold text-[#d4af37] mb-3 text-center" style={{ fontFamily: 'var(--font-sacred, Cormorant Garamond, serif)' }}>
                  Rashi Chart (D1)
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
                      opacity="0.5"
                    />
                    {/* Cross lines */}
                    <line x1="150" y1="10" x2="150" y2="290" stroke="#d4af37" strokeWidth="1" opacity="0.3"/>
                    <line x1="10" y1="150" x2="290" y2="150" stroke="#d4af37" strokeWidth="1" opacity="0.3"/>
                    
                    {/* House numbers and planets */}
                    {/* House 1 (Ascendant) - Top */}
                    <text x="150" y="30" textAnchor="middle" fill="#d4af37" fontSize="12" fontWeight="bold">1</text>
                    <text x="150" y="55" textAnchor="middle" fill="#FFD700" fontSize="14">Su</text>
                    <text x="150" y="72" textAnchor="middle" fill="#FF69B4" fontSize="11">Ve</text>
                    
                    {/* House 2 - Top Right */}
                    <text x="200" y="60" textAnchor="middle" fill="#d4af37" fontSize="12" fontWeight="bold">2</text>
                    <text x="200" y="80" textAnchor="middle" fill="#00CED1" fontSize="12">Me</text>
                    
                    {/* House 3 - Right */}
                    <text x="240" y="110" textAnchor="middle" fill="#d4af37" fontSize="12" fontWeight="bold">3</text>
                    <text x="240" y="130" textAnchor="middle" fill="#FF69B4" fontSize="12">Ve</text>
                    
                    {/* House 4 - Bottom Right */}
                    <text x="200" y="180" textAnchor="middle" fill="#d4af37" fontSize="12" fontWeight="bold">4</text>
                    <text x="200" y="200" textAnchor="middle" fill="#4169E1" fontSize="12">Ra</text>
                    
                    {/* House 5 - Bottom */}
                    <text x="150" y="230" textAnchor="middle" fill="#d4af37" fontSize="12" fontWeight="bold">5</text>
                    <text x="150" y="250" textAnchor="middle" fill="#FF4500" fontSize="12" opacity="0.7">Ma</text>
                    
                    {/* House 6 - Bottom Left */}
                    <text x="100" y="180" textAnchor="middle" fill="#d4af37" fontSize="12" fontWeight="bold">6</text>
                    
                    {/* House 7 - Left Bottom */}
                    <text x="60" y="150" textAnchor="middle" fill="#d4af37" fontSize="12" fontWeight="bold">7</text>
                    <text x="60" y="170" textAnchor="middle" fill="#808080" fontSize="12">Sa</text>
                    
                    {/* House 8 - Left */}
                    <text x="60" y="110" textAnchor="middle" fill="#d4af37" fontSize="12" fontWeight="bold">8</text>
                    <text x="60" y="90" textAnchor="middle" fill="#FFA500" fontSize="12">Ju</text>
                    
                    {/* House 9 - Top Left */}
                    <text x="100" y="60" textAnchor="middle" fill="#d4af37" fontSize="12" fontWeight="bold">9</text>
                    <text x="100" y="80" textAnchor="middle" fill="#FF4500" fontSize="12">Ma</text>
                    
                    {/* House 10 - Top Left Upper */}
                    <text x="110" y="35" textAnchor="middle" fill="#d4af37" fontSize="12" fontWeight="bold">10</text>
                    <text x="110" y="50" textAnchor="middle" fill="#C0C0C0" fontSize="14">Mo</text>
                    <text x="135" y="50" textAnchor="middle" fill="#8B4513" fontSize="11">Ke</text>
                    
                    {/* House 11 - Top Right Upper */}
                    <text x="190" y="35" textAnchor="middle" fill="#d4af37" fontSize="12" fontWeight="bold">11</text>
                    
                    {/* House 12 - Right Upper */}
                    <text x="240" y="70" textAnchor="middle" fill="#d4af37" fontSize="12" fontWeight="bold">12</text>
                  </svg>
                </div>

                {/* Lagna Info */}
                <div className="mt-4 p-3 bg-[#d4af37]/5 rounded-lg border border-[#d4af37]/10">
                  <div className="flex flex-wrap gap-4 justify-center text-center">
                    <div>
                      <p className="text-xs text-white/50">Ascendant</p>
                      <p className="text-lg font-bold text-[#d4af37]">Leo</p>
                    </div>
                    <div className="w-px bg-[#d4af37]/20" />
                    <div>
                      <p className="text-xs text-white/50">Moon Sign</p>
                      <p className="text-lg font-bold text-[#C0C0C0]">Taurus</p>
                    </div>
                    <div className="w-px bg-[#d4af37]/20" />
                    <div>
                      <p className="text-xs text-white/50">Sun Sign</p>
                      <p className="text-lg font-bold text-[#FFD700]">Leo</p>
                    </div>
                    <div className="w-px bg-[#d4af37]/20" />
                    <div>
                      <p className="text-xs text-white/50">Nakshatra</p>
                      <p className="text-lg font-bold text-white">Rohini</p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Divisional Charts */}
              <div className="grid grid-cols-3 gap-3">
                <div className="bg-[#111] rounded-lg border border-[#d4af37]/10 p-3 text-center">
                  <p className="text-xs text-white/50 mb-1">Navamsha (D9)</p>
                  <p className="text-lg font-semibold text-[#d4af37]">Scorpio</p>
                </div>
                <div className="bg-[#111] rounded-lg border border-[#d4af37]/10 p-3 text-center">
                  <p className="text-xs text-white/50 mb-1">Dashamsha (D10)</p>
                  <p className="text-lg font-semibold text-[#d4af37]">Capricorn</p>
                </div>
                <div className="bg-[#111] rounded-lg border border-[#d4af37]/10 p-3 text-center">
                  <p className="text-xs text-white/50 mb-1">Saptamsha (D7)</p>
                  <p className="text-lg font-semibold text-[#d4af37]">Libra</p>
                </div>
              </div>
            </div>

            {/* Right - Planet Positions & Dasha */}
            <div className="space-y-4">
              {/* Planet Positions */}
              <div className="bg-[#111] rounded-xl border border-[#d4af37]/20 p-3">
                <h3 className="text-sm font-semibold text-[#d4af37] mb-2" style={{ fontFamily: 'var(--font-sacred, Cormorant Garamond, serif)' }}>
                  Planetary Positions
                </h3>
                <div className="space-y-1 max-h-48 overflow-y-auto">
                  {samplePlanets.map((planet, idx) => (
                    <div 
                      key={idx}
                      className="flex items-center justify-between p-2 rounded bg-black/30 text-xs"
                    >
                      <div className="flex items-center gap-2">
                        <span 
                          className="w-2 h-2 rounded-full"
                          style={{ backgroundColor: planetColors[planet.planet] || '#fff' }}
                        />
                        <span className="text-white font-medium">{planet.planet}</span>
                      </div>
                      <div className="text-right">
                        <span className="text-[#d4af37]">{planet.sign}</span>
                        <span className="text-white/50 ml-1">H{planet.house}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Current Dasha */}
              <div className="bg-[#111] rounded-xl border border-[#d4af37]/20 p-3">
                <h3 className="text-sm font-semibold text-[#d4af37] mb-2" style={{ fontFamily: 'var(--font-sacred, Cormorant Garamond, serif)' }}>
                  Vimshottari Dasha
                </h3>
                <div className="space-y-2">
                  {sampleDasha.map((period, idx) => (
                    <div 
                      key={idx}
                      className={`p-2 rounded text-xs ${idx === 0 ? 'bg-[#d4af37]/20 border border-[#d4af37]/30' : 'bg-black/30'}`}
                    >
                      <div className="flex items-center justify-between mb-1">
                        <span className="font-semibold text-white">{period.planet} Mahadasha</span>
                        <span className="text-[#d4af37]">{period.years} Years</span>
                      </div>
                      <p className="text-white/50">{period.startDate} - {period.endDate}</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Quick Stats */}
              <div className="grid grid-cols-2 gap-2 mb-4">
                <div className="bg-[#111] rounded-lg border border-[#d4af37]/10 p-2 text-center">
                  <p className="text-xs text-white/50">Gana</p>
                  <p className="text-sm font-semibold text-white">Manushya</p>
                </div>
                <div className="bg-[#111] rounded-lg border border-[#d4af37]/10 p-2 text-center">
                  <p className="text-xs text-white/50">Yoni</p>
                  <p className="text-sm font-semibold text-white">Serpent</p>
                </div>
                <div className="bg-[#111] rounded-lg border border-[#d4af37]/10 p-2 text-center">
                  <p className="text-xs text-white/50">Nadi</p>
                  <p className="text-sm font-semibold text-white">Kapha</p>
                </div>
                <div className="bg-[#111] rounded-lg border border-[#d4af37]/10 p-2 text-center">
                  <p className="text-xs text-white/50">Varna</p>
                  <p className="text-sm font-semibold text-white">Kshatriya</p>
                </div>
              </div>

              {/* PRESENT Yogas Only - Not showing absent ones */}
              {presentYogas.length > 0 && (
                <div className="bg-[#111] rounded-xl border border-green-500/20 p-3 mb-4">
                  <h3 className="text-sm font-semibold text-green-400 mb-2 flex items-center gap-2" style={{ fontFamily: 'var(--font-sacred, Cormorant Garamond, serif)' }}>
                    <span>✦</span> Present Yogas ({presentYogas.length})
                  </h3>
                  <div className="space-y-2">
                    {presentYogas.map((yoga, idx) => (
                      <div key={idx} className="p-2 rounded bg-green-500/5 border border-green-500/10 text-xs">
                        <div className="flex items-center justify-between mb-1">
                          <span className="font-semibold text-white">{yoga.name}</span>
                          <span className={`px-2 py-0.5 rounded-full text-label ${
                            yoga.strength === 'Strong' ? 'bg-green-500/20 text-green-400' : 'bg-yellow-500/20 text-yellow-400'
                          }`}>
                            {yoga.strength}
                          </span>
                        </div>
                        <p className="text-green-400/70">{yoga.planets} • {yoga.effect}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* PRESENT Doshas Only - Not showing absent ones */}
              {presentDoshas.length > 0 && (
                <div className="bg-[#111] rounded-xl border border-red-500/20 p-3">
                  <h3 className="text-sm font-semibold text-red-400 mb-2 flex items-center gap-2" style={{ fontFamily: 'var(--font-sacred, Cormorant Garamond, serif)' }}>
                    <span>⚠</span> Present Doshas ({presentDoshas.length})
                  </h3>
                  <div className="space-y-2">
                    {presentDoshas.map((dosha, idx) => (
                      <div key={idx} className="p-2 rounded bg-red-500/5 border border-red-500/10 text-xs">
                        <div className="flex items-center justify-between mb-1">
                          <span className="font-semibold text-white">{dosha.name}</span>
                          <span className={`px-2 py-0.5 rounded-full text-label ${
                            dosha.severity === 'High' ? 'bg-red-500/20 text-red-400' : 'bg-yellow-500/20 text-yellow-400'
                          }`}>
                            {dosha.severity}
                          </span>
                        </div>
                        <p className="text-red-400/70 mb-1">{dosha.planet} • {dosha.effect}</p>
                        <p className="text-label text-white/50">💡 Remedy: {dosha.remedy}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* No Yogas/Doshas Message */}
              {presentYogas.length === 0 && presentDoshas.length === 0 && (
                <div className="bg-[#111] rounded-xl border border-[#d4af37]/10 p-3 text-center">
                  <p className="text-xs text-white/50">No significant Yogas or Doshas detected</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
