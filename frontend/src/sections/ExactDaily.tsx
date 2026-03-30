import { useNavigate } from 'react-router-dom';
import { Moon, Sun, Clock, MapPin, Calculator, Sparkles, ChevronRight, MessageCircle } from 'lucide-react';

function CalendarIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <rect x="3" y="4" width="18" height="18" rx="2" ry="2" strokeWidth="2"/>
      <line x1="16" y1="2" x2="16" y2="6" strokeWidth="2"/>
      <line x1="8" y1="2" x2="8" y2="6" strokeWidth="2"/>
      <line x1="3" y1="10" x2="21" y2="10" strokeWidth="2"/>
    </svg>
  );
}

const timingCards = [
  { icon: Moon, title: 'Rahu Kaala', value: '3:14 PM - 4:52 PM', subtext: 'Avoid auspicious work' },
  { icon: Sun, title: 'Sun Transit', value: '8.99\u00B0', subtext: '11am', hasButton: true, btnLabel: 'Learn' },
  { icon: Clock, title: 'Hora Timings', value: '1:16 - 4:42', subtext: 'Current Hora: Jupiter' },
  { icon: MapPin, title: 'Place Timings', value: '4:3:00', subtext: 'Astrology Details' },
  { icon: CalendarIcon, title: 'Tilkut Chaturthi', value: '', subtext: 'auspicious day', hasButton: true, btnLabel: 'See Panchang' },
  { icon: Calculator, title: 'Rashi Calculator', value: '', subtext: 'Find your moon sign', hasButton: true, btnLabel: 'Calculate Rashi' },
];

export default function ExactDaily() {
  const navigate = useNavigate();

  return (
    <section className="py-10 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex items-center gap-3 mb-6">
          <div className="flex items-center gap-2 px-4 py-1.5 rounded-md text-sm font-serif font-semibold tracking-wide"
               style={{ background: 'linear-gradient(to right, #D4A052, #B8860B)', color: 'white' }}>
            <Sparkles className="w-4 h-4" />
            Daily Insights
          </div>
          <div className="h-px flex-1" style={{ background: 'linear-gradient(to right, #D4A052, transparent)' }} />
          <span className="text-sm flex items-center gap-2" style={{ color: '#7A6548' }}>
            <span className="w-2 h-2 bg-green-600 rounded-full animate-pulse" />
            monitoring Bharatpur
          </span>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
          {/* Left - 6 Timing Cards */}
          <div className="lg:col-span-5">
            <div className="grid grid-cols-2 gap-3">
              {timingCards.map((card) => (
                <div key={card.title}
                     onClick={() => card.hasButton && navigate('/panchang')}
                     className="rounded-xl p-4 border transition-all duration-300 hover:-translate-y-0.5 cursor-pointer"
                     style={{
                       background: '#FFF8EE',
                       borderColor: '#D4A052',
                       boxShadow: '0 2px 6px rgba(139, 105, 20, 0.06)',
                     }}
                     onMouseEnter={(e) => {
                       e.currentTarget.style.boxShadow = '0 6px 16px rgba(139, 105, 20, 0.14)';
                     }}
                     onMouseLeave={(e) => {
                       e.currentTarget.style.boxShadow = '0 2px 6px rgba(139, 105, 20, 0.06)';
                     }}>
                  <div className="flex items-start gap-3">
                    <div className="w-9 h-9 rounded-full flex items-center justify-center flex-shrink-0"
                         style={{ background: 'linear-gradient(135deg, #F5E6C8, #EDE0C8)', border: '1.5px solid #D4A052' }}>
                      <card.icon className="w-4 h-4" style={{ color: '#8B6914' }} />
                    </div>
                    <div className="flex-1 min-w-0">
                      <h4 className="font-serif font-semibold text-sm" style={{ color: '#3D2B1F' }}>{card.title}</h4>
                      {card.value && (
                        <p className="font-bold text-sm" style={{ color: '#3D2B1F' }}>{card.value}</p>
                      )}
                      <p className="text-xs" style={{ color: '#7A6548' }}>{card.subtext}</p>
                      {card.hasButton && (
                        <button className="mt-1.5 text-xs px-3 py-1 rounded-full transition-colors font-medium"
                                style={{ background: 'linear-gradient(to right, #D4A052, #B8860B)', color: 'white' }}>
                          {card.btnLabel}
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Middle - Sage / Rishi placeholder */}
          <div className="lg:col-span-4">
            <div className="relative h-full min-h-[360px] rounded-xl overflow-hidden border"
                 style={{
                   background: 'linear-gradient(160deg, #F5E6C8 0%, #FFE4C4 40%, #F0DFC0 70%, #E8D5B0 100%)',
                   borderColor: '#D4A052',
                 }}>
              {/* Decorative concentric circles */}
              <div className="absolute top-8 left-8 w-20 h-20 rounded-full opacity-20"
                   style={{ border: '2px solid #B8860B' }} />
              <div className="absolute bottom-20 right-8 w-28 h-28 rounded-full opacity-15"
                   style={{ border: '2px solid #B8860B' }} />
              <div className="absolute top-1/2 left-1/2 w-44 h-44 rounded-full -translate-x-1/2 -translate-y-1/2 opacity-10"
                   style={{ border: '2px solid #B8860B' }} />

              {/* Sage placeholder with Om symbol */}
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="text-center">
                  <div className="w-32 h-32 mx-auto mb-4 rounded-full flex items-center justify-center shadow-lg"
                       style={{ background: 'linear-gradient(135deg, #D4A052, #B8860B)', border: '3px solid #8B6914' }}>
                    <span className="text-5xl text-white font-serif" style={{ textShadow: '0 2px 4px rgba(0,0,0,0.2)' }}>
                      {'\u0950'}
                    </span>
                  </div>
                  <p className="font-serif text-xl font-bold" style={{ color: '#3D2B1F' }}>AI Astrologer</p>
                  <p className="text-sm mt-1" style={{ color: '#7A6548' }}>Aman Sharma</p>
                  <p className="text-xs mt-0.5" style={{ color: '#9A8A70' }}>Ancient Wisdom, Modern AI</p>
                </div>
              </div>

              {/* Bottom reminder */}
              <div className="absolute bottom-4 left-1/2 -translate-x-1/2">
                <span className="text-xs px-3 py-1.5 rounded-full"
                      style={{ background: 'rgba(255,248,238,0.9)', color: '#7A6548', border: '1px solid #D4A052' }}>
                  Tap Romal Reminders
                </span>
              </div>
            </div>
          </div>

          {/* Right - AI Chat Card */}
          <div className="lg:col-span-3">
            <div className="rounded-xl p-5 border h-full flex flex-col"
                 style={{ background: '#FFF8EE', borderColor: '#D4A052', boxShadow: '0 4px 12px rgba(139, 105, 20, 0.1)' }}>
              <div className="flex items-center gap-3 mb-4">
                <div className="w-11 h-11 rounded-full flex items-center justify-center"
                     style={{ background: 'linear-gradient(135deg, #D4A052, #B8860B)' }}>
                  <MessageCircle className="w-5 h-5 text-white" />
                </div>
                <div>
                  <h3 className="font-serif font-bold" style={{ color: '#3D2B1F' }}>AI Astrologer</h3>
                  <p className="text-xs" style={{ color: '#7A6548' }}>24/7 Guidance</p>
                </div>
              </div>

              {/* Chat preview */}
              <div className="flex-1 rounded-lg p-3 mb-4 space-y-2.5"
                   style={{ background: 'linear-gradient(135deg, #F5E6C8, #EDE0C8)' }}>
                <div className="rounded-lg p-2.5 rounded-tl-none"
                     style={{ background: '#FFF8EE', border: '1px solid #D4A052' }}>
                  <p className="text-xs mb-0.5" style={{ color: '#7A6548' }}>
                    Aman Sharma <span style={{ color: '#9A8A70' }}>Today, 10:45 AM</span>
                  </p>
                  <p className="text-sm" style={{ color: '#3D2B1F' }}>Will I get a steady job in 2026?</p>
                </div>
                <div className="rounded-lg p-2.5 rounded-tr-none"
                     style={{ background: '#FFF8EE', border: '1px solid #D4A052' }}>
                  <p className="text-xs mb-0.5 font-medium" style={{ color: '#8B6914' }}>Reading your Kundli...</p>
                  <p className="text-sm" style={{ color: '#3D2B1F' }}>
                    Based on Jupiter's transit in your 10th house,{' '}
                    <span className="font-bold" style={{ color: '#8B6914' }}>mid-2026 looks promising</span> for career growth.
                  </p>
                </div>
              </div>

              <button onClick={() => navigate('/ai-chat')}
                      className="w-full py-3 text-white font-serif font-medium rounded-full
                               flex items-center justify-center gap-2 transition-all duration-200 hover:shadow-lg"
                      style={{ background: 'linear-gradient(to right, #D4A052, #B8860B)' }}>
                <Sparkles className="w-4 h-4" />
                Generate Kundli
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
