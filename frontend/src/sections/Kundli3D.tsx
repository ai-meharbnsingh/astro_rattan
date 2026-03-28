import { useState, useRef, Suspense, lazy } from 'react';
import { User, Calendar, Clock, MapPin, Sparkles, ChevronRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

const ZodiacScene = lazy(() => import('@/components/three/ZodiacScene'));

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
    gender: 'male'
  });
  const [loading, setLoading] = useState(false);

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
                className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-[#9A7B0A]/10 border border-[#9A7B0A]/30 mb-6"
                style={{ animation: 'slideUp 0.6s ease-out 0.2s both' }}
              >
                <Sparkles className="w-4 h-4 text-[#9A7B0A]" />
                <span className="text-[#9A7B0A] text-sm font-medium">3D Experience</span>
              </div>

              <h1 className="text-5xl lg:text-7xl font-bold mb-6" style={{ 
                fontFamily: 'Cinzel, serif',
                animation: 'slideUp 0.8s ease-out 0.3s both'
              }}>
                <span className="text-[#1a1a2e]">Your</span>
                <br />
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#B8860B] to-[#9A7B0A]">
                  Cosmic Blueprint
                </span>
              </h1>

              <p className="text-xl text-[#1a1a2e]/70 mb-8 max-w-lg" style={{ animation: 'slideUp 0.8s ease-out 0.4s both' }}>
                Discover your destiny through our immersive 3D Vedic birth chart. 
                The stars align in three dimensions to reveal your true path.
              </p>

              {/* Features */}
              <div className="flex flex-wrap gap-4 justify-center lg:justify-start">
                {['Natal Chart', 'Dasha Analysis', 'Planetary Positions', 'Life Predictions'].map((feature, i) => (
                  <span
                    key={feature}
                    className="px-4 py-2 rounded-full bg-white/5 border border-[#8B7355]/10 text-[#1a1a2e]/80 text-sm"
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
                <div className="bg-[#F5F0E8]/40 backdrop-blur-xl border border-[#9A7B0A]/30 rounded-3xl p-8 shadow-2xl shadow-[#9A7B0A]/10">
                  <h2 className="text-2xl font-bold text-[#1a1a2e] mb-6 text-center" style={{ fontFamily: 'Cinzel, serif' }}>
                    Generate Your Kundli
                  </h2>

                  <form onSubmit={handleSubmit} className="space-y-5">
                    {/* Name */}
                    <div className="relative">
                      <User className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-[#9A7B0A]" />
                      <Input
                        type="text"
                        placeholder="Full Name"
                        value={formData.name}
                        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                        className="pl-12 h-14 bg-white/5 border-[#8B7355]/10 text-[#1a1a2e] placeholder:text-[#1a1a2e]/40 focus:border-[#9A7B0A] text-lg"
                      />
                    </div>

                    {/* Gender Selection */}
                    <div className="grid grid-cols-2 gap-3">
                      <button
                        type="button"
                        onClick={() => setFormData({ ...formData, gender: 'male' })}
                        className={`h-14 rounded-xl border transition-all text-lg ${
                          formData.gender === 'male'
                            ? 'bg-[#9A7B0A] text-[#1a1a2e] border-[#9A7B0A]'
                            : 'bg-white/5 text-[#1a1a2e] border-[#8B7355]/10 hover:border-[#9A7B0A]/50'
                        }`}
                      >
                        Male
                      </button>
                      <button
                        type="button"
                        onClick={() => setFormData({ ...formData, gender: 'female' })}
                        className={`h-14 rounded-xl border transition-all text-lg ${
                          formData.gender === 'female'
                            ? 'bg-[#9A7B0A] text-[#1a1a2e] border-[#9A7B0A]'
                            : 'bg-white/5 text-[#1a1a2e] border-[#8B7355]/10 hover:border-[#9A7B0A]/50'
                        }`}
                      >
                        Female
                      </button>
                    </div>

                    {/* Date & Time */}
                    <div className="grid grid-cols-2 gap-3">
                      <div className="relative">
                        <Calendar className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-[#9A7B0A]" />
                        <Input
                          type="date"
                          value={formData.date}
                          onChange={(e) => setFormData({ ...formData, date: e.target.value })}
                          className="pl-12 h-14 bg-white/5 border-[#8B7355]/10 text-[#1a1a2e] focus:border-[#9A7B0A] text-lg"
                        />
                      </div>
                      <div className="relative">
                        <Clock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-[#9A7B0A]" />
                        <Input
                          type="time"
                          value={formData.time}
                          onChange={(e) => setFormData({ ...formData, time: e.target.value })}
                          className="pl-12 h-14 bg-white/5 border-[#8B7355]/10 text-[#1a1a2e] focus:border-[#9A7B0A] text-lg"
                        />
                      </div>
                    </div>

                    {/* Birth Place */}
                    <div className="relative">
                      <MapPin className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-[#9A7B0A]" />
                      <Input
                        type="text"
                        placeholder="Birth Place (City)"
                        value={formData.place}
                        onChange={(e) => setFormData({ ...formData, place: e.target.value })}
                        className="pl-12 h-14 bg-white/5 border-[#8B7355]/10 text-[#1a1a2e] placeholder:text-[#1a1a2e]/40 focus:border-[#9A7B0A] text-lg"
                      />
                    </div>

                    {/* Submit Button */}
                    <Button
                      type="submit"
                      disabled={loading}
                      className="w-full h-14 bg-gradient-to-r from-[#9A7B0A] to-[#B8860B] text-[#1a1a2e] font-bold text-lg hover:shadow-lg hover:shadow-[#9A7B0A]/30 transition-all"
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
                  <div className="mt-6 pt-6 border-t border-[#8B7355]/10 flex items-center justify-center gap-6 text-sm text-[#1a1a2e]/50">
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
      <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-[#F5F0E8] to-transparent pointer-events-none" />
    </div>
  );
}
