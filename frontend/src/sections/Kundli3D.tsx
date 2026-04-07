import { useState, useRef, useEffect, Suspense, lazy } from 'react';
import { User, Calendar, Clock, MapPin, Sparkles, ChevronRight, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { api } from '@/lib/api';

const ZodiacScene = lazy(() => import('@/components/three/ZodiacScene'));

// ── Geocode types & hook ────────────────────────────────────
interface GeocodeResult {
  name: string;
  lat: number;
  lon: number;
}

function useGeocodeAutocomplete() {
  const [suggestions, setSuggestions] = useState<GeocodeResult[]>([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const [loading, setLoading] = useState(false);
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const search = (query: string) => {
    if (timerRef.current) clearTimeout(timerRef.current);
    if (query.length < 3) {
      setSuggestions([]);
      setShowDropdown(false);
      return;
    }
    timerRef.current = setTimeout(async () => {
      setLoading(true);
      try {
        const results = await api.get(`/api/kundli/geocode?query=${encodeURIComponent(query)}`);
        setSuggestions(Array.isArray(results) ? results : []);
        setShowDropdown(true);
      } catch {
        setSuggestions([]);
      }
      setLoading(false);
    }, 300);
  };

  const close = () => {
    setShowDropdown(false);
  };

  return { suggestions, showDropdown, loading, search, close };
}

// 3D Tilt Card Component
function TiltCard({ children, className = '' }: { children: React.ReactNode; className?: string }) {
  const cardRef = useRef<HTMLDivElement>(null);

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!cardRef.current) return;
    const card = cardRef.current;
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;
    const rotateX = (y - centerY) / 20;
    const rotateY = (centerX - x) / 20;
    
    card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
  };

  const handleMouseLeave = () => {
    if (!cardRef.current) return;
    cardRef.current.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale3d(1, 1, 1)';
  };

  return (
    <div
      ref={cardRef}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      className={`transition-transform duration-200 ease-out ${className}`}
      style={{ transformStyle: 'preserve-3d' }}
    >
      {children}
    </div>
  );
}

export default function Kundli3D() {
  const [formData, setFormData] = useState({
    name: '',
    date: '',
    time: '',
    place: '',
    latitude: 28.6139,
    longitude: 77.2090,
    gender: 'male'
  });
  const [loading, setLoading] = useState(false);
  const geocode = useGeocodeAutocomplete();
  const placeWrapperRef = useRef<HTMLDivElement>(null);

  // Close geocode dropdown on outside click
  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (placeWrapperRef.current && !placeWrapperRef.current.contains(e.target as Node)) {
        geocode.close();
      }
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, [geocode]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setTimeout(() => setLoading(false), 2000);
  };

  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* 3D Background */}
      <Suspense fallback={null}>
        <ZodiacScene />
      </Suspense>

      {/* Content Overlay */}
      <div className="relative z-10 min-h-screen flex items-center justify-center px-4 py-24">
        <div className="w-full max-w-6xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            
            {/* Left Side - 3D Text */}
            <div 
              className="text-center lg:text-left animate-fade-in"
              style={{ animation: 'fadeIn 0.8s ease-out' }}
            >
              <div 
                className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-sacred-gold-dark/10 border border-sacred-gold/30 mb-6"
                style={{ animation: 'slideUp 0.6s ease-out 0.2s both' }}
              >
                <Sparkles className="w-4 h-4 text-sacred-gold-dark" />
                <span className="text-sacred-gold-dark text-sm font-medium">3D Experience</span>
              </div>

              <h1 className="text-5xl lg:text-7xl font-bold mb-6" style={{ 
                fontFamily: 'Cinzel, serif',
                animation: 'slideUp 0.8s ease-out 0.3s both'
              }}>
                <span className="text-cosmic-text">Your</span>
                <br />
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-sacred-gold-dark to-sacred-gold-dark">
                  Cosmic Blueprint
                </span>
              </h1>

              <p className="text-xl text-cosmic-text/70 mb-8 max-w-lg" style={{ animation: 'slideUp 0.8s ease-out 0.4s both' }}>
                Discover your destiny through our immersive 3D Vedic birth chart. 
                The stars align in three dimensions to reveal your true path.
              </p>

              {/* Features */}
              <div className="flex flex-wrap gap-4 justify-center lg:justify-start">
                {['Natal Chart', 'Dasha Analysis', 'Planetary Positions', 'Life Predictions'].map((feature, i) => (
                  <span
                    key={feature}
                    className="px-4 py-2 rounded-full bg-white/5 border border-cosmic-text-secondary/10 text-cosmic-text/80 text-sm"
                    style={{ animation: `scaleIn 0.4s ease-out ${0.5 + i * 0.1}s both` }}
                  >
                    {feature}
                  </span>
                ))}
              </div>
            </div>

            {/* Right Side - 3D Form Card */}
            <div style={{ animation: 'slideInRight 0.8s ease-out 0.3s both' }}>
              <TiltCard>
                <div className="bg-cosmic-bg/40 backdrop-blur-xl border border-sacred-gold/30 rounded-3xl p-8 shadow-2xl shadow-sacred-gold-dark/10">
                  <h2 className="text-2xl font-bold text-cosmic-text mb-6 text-center" style={{ fontFamily: 'Cinzel, serif' }}>
                    Generate Your Kundli
                  </h2>

                  <form onSubmit={handleSubmit} className="space-y-5">
                    {/* Name */}
                    <div className="relative">
                      <User className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-sacred-gold-dark" />
                      <Input
                        type="text"
                        placeholder="Full Name"
                        value={formData.name}
                        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                        className="pl-12 h-14 bg-white/5 border-cosmic-text-secondary/10 text-cosmic-text placeholder:text-cosmic-text/40 focus:border-sacred-gold text-lg"
                      />
                    </div>

                    {/* Gender Selection */}
                    <div className="grid grid-cols-2 gap-3">
                      <button
                        type="button"
                        onClick={() => setFormData({ ...formData, gender: 'male' })}
                        className={`h-14 rounded-xl border transition-all text-lg ${
                          formData.gender === 'male'
                            ? 'bg-sacred-gold-dark text-cosmic-bg border-sacred-gold'
                            : 'bg-white/5 text-cosmic-text border-cosmic-text-secondary/10 hover:border-sacred-gold/50'
                        }`}
                      >
                        Male
                      </button>
                      <button
                        type="button"
                        onClick={() => setFormData({ ...formData, gender: 'female' })}
                        className={`h-14 rounded-xl border transition-all text-lg ${
                          formData.gender === 'female'
                            ? 'bg-sacred-gold-dark text-cosmic-bg border-sacred-gold'
                            : 'bg-white/5 text-cosmic-text border-cosmic-text-secondary/10 hover:border-sacred-gold/50'
                        }`}
                      >
                        Female
                      </button>
                    </div>

                    {/* Date & Time */}
                    <div className="grid grid-cols-2 gap-3">
                      <div className="relative">
                        <Calendar className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-sacred-gold-dark" />
                        <Input
                          type="date"
                          value={formData.date}
                          onChange={(e) => setFormData({ ...formData, date: e.target.value })}
                          className="pl-12 h-14 bg-white/5 border-cosmic-text-secondary/10 text-cosmic-text focus:border-sacred-gold text-lg"
                        />
                      </div>
                      <div className="relative">
                        <Clock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-sacred-gold-dark" />
                        <Input
                          type="time"
                          value={formData.time}
                          onChange={(e) => setFormData({ ...formData, time: e.target.value })}
                          className="pl-12 h-14 bg-white/5 border-cosmic-text-secondary/10 text-cosmic-text focus:border-sacred-gold text-lg"
                        />
                      </div>
                    </div>

                    {/* Birth Place with Geocode Autocomplete */}
                    <div className="relative" ref={placeWrapperRef}>
                      <MapPin className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-sacred-gold-dark z-10" />
                      <Input
                        type="text"
                        placeholder="Birth Place (type to search)"
                        value={formData.place}
                        onChange={(e) => {
                          setFormData({ ...formData, place: e.target.value });
                          geocode.search(e.target.value);
                        }}
                        className="pl-12 h-14 bg-white/5 border-cosmic-text-secondary/10 text-cosmic-text placeholder:text-cosmic-text/40 focus:border-sacred-gold text-lg"
                        autoComplete="off"
                      />
                      {geocode.loading && (
                        <Loader2 className="absolute right-4 top-1/2 -translate-y-1/2 w-5 h-5 animate-spin text-sacred-gold-dark" />
                      )}
                      {geocode.showDropdown && geocode.suggestions.length > 0 && (
                        <div className="absolute z-50 left-0 right-0 top-full mt-1 bg-cosmic-bg border border-sacred-gold-dark/30 rounded-2xl shadow-lg max-h-60 overflow-y-auto">
                          {geocode.suggestions.map((s, i) => (
                            <button
                              key={i}
                              type="button"
                              onClick={() => {
                                setFormData({ ...formData, place: s.name.split(',')[0], latitude: s.lat, longitude: s.lon });
                                geocode.close();
                              }}
                              className="w-full text-left px-4 py-3 hover:bg-sacred-purple transition-colors border-b border-sacred-gold-dark/10 last:border-b-0"
                            >
                              <p className="text-sm font-medium text-cosmic-text truncate">{s.name}</p>
                              <p className="text-xs text-cosmic-text/50">{s.lat.toFixed(4)}, {s.lon.toFixed(4)}</p>
                            </button>
                          ))}
                        </div>
                      )}
                    </div>

                    {/* Coordinates display */}
                    <div className="flex items-center gap-2 text-xs text-cosmic-text/50 px-1 -mt-2">
                      <MapPin className="w-3 h-3 text-sacred-gold-dark" />
                      <span>Lat: {formData.latitude.toFixed(4)}, Lon: {formData.longitude.toFixed(4)}</span>
                    </div>

                    {/* Submit Button */}
                    <Button
                      type="submit"
                      disabled={loading}
                      className="w-full h-14 bg-gradient-to-r from-sacred-gold-dark to-sacred-gold-dark text-cosmic-text font-bold text-lg hover:shadow-lg hover:shadow-sacred-gold-dark/30 transition-all"
                    >
                      {loading ? (
                        <span className="flex items-center gap-2">
                          <div className="w-5 h-5 border-2 border-black/30 border-t-black rounded-full animate-spin" />
                          Calculating...
                        </span>
                      ) : (
                        <span className="flex items-center gap-2">
                          Generate 3D Kundli
                          <ChevronRight className="w-5 h-5" />
                        </span>
                      )}
                    </Button>
                  </form>

                  {/* Trust badges */}
                  <div className="mt-6 pt-6 border-t border-cosmic-text-secondary/10 flex items-center justify-center gap-6 text-sm text-cosmic-text/50">
                    <span>🔒 Secure</span>
                    <span>⚡ Instant</span>
                    <span>🎯 Accurate</span>
                  </div>
                </div>
              </TiltCard>
            </div>
          </div>
        </div>
      </div>

      {/* Animations */}
      <style>{`
        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        @keyframes slideUp {
          from { opacity: 0; transform: translateY(30px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes slideInRight {
          from { opacity: 0; transform: translateX(50px); }
          to { opacity: 1; transform: translateX(0); }
        }
        @keyframes scaleIn {
          from { opacity: 0; transform: scale(0.8); }
          to { opacity: 1; transform: scale(1); }
        }
      `}</style>

      {/* Bottom gradient fade */}
      <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-cosmic-bg to-transparent pointer-events-none" />
    </div>
  );
}
