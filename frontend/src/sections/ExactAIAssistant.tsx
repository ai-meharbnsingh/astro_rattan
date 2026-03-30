import { useNavigate } from 'react-router-dom';
import { Sparkles, Hash, CreditCard, Search, BookOpen, ChevronRight, MessageCircle, Bot } from 'lucide-react';

const features = [
  { icon: Hash, label: 'Numerology' },
  { icon: CreditCard, label: 'Tarot Reading' },
  { icon: Search, label: 'KP Astrology' },
  { icon: BookOpen, label: 'Lal Kitab' },
];

const recommendedArticles = [
  {
    title: 'Are intense retrogrades\naffecting your 1st house?',
    subtitle: "Here's what to do.",
  },
  {
    title: 'Rahu Green Jade',
    subtitle: '\u20B93,500+',
    hasButton: true,
    btnLabel: 'Book a Call',
  },
];

export default function ExactAIAssistant() {
  const navigate = useNavigate();

  return (
    <section className="relative py-12 px-4 sm:px-6 lg:px-8 overflow-hidden">
      <div className="relative max-w-7xl mx-auto">
        {/* Section Title */}
        <div className="text-center mb-10">
          {/* Decorative banner */}
          <div className="inline-block relative mb-4">
            <div className="flex items-center gap-3">
              <div className="h-px w-12" style={{ background: 'linear-gradient(to right, transparent, #D4A052)' }} />
              <h2 className="font-serif text-3xl md:text-4xl font-bold" style={{ color: '#3D2B1F' }}>
                AI Astrology Assistant
              </h2>
              <div className="h-px w-12" style={{ background: 'linear-gradient(to left, transparent, #D4A052)' }} />
            </div>
            {/* Underline ornament */}
            <div className="mt-2 mx-auto w-24 h-0.5" style={{ background: 'linear-gradient(to right, #D4A052, #B8860B, #D4A052)' }} />
          </div>
          <p className="text-base max-w-2xl mx-auto" style={{ color: '#7A6548' }}>
            Smart Chatbot, Instant Astrology, Guide your users with personalized AI Insights.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
          {/* Left side — Category icons + Recommended */}
          <div className="space-y-6">
            {/* Category icons row */}
            <div className="grid grid-cols-4 gap-3">
              {features.map((feature) => (
                <div key={feature.label}
                     onClick={() => navigate('/ai-chat')}
                     className="rounded-xl p-4 border text-center cursor-pointer
                                transition-all duration-300 hover:-translate-y-1"
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
                  <div className="w-12 h-12 mx-auto mb-2 rounded-full flex items-center justify-center"
                       style={{ background: 'linear-gradient(135deg, #F5E6C8, #EDE0C8)', border: '1.5px solid #D4A052' }}>
                    <feature.icon className="w-5 h-5" style={{ color: '#8B6914' }} />
                  </div>
                  <h3 className="font-serif font-semibold text-xs" style={{ color: '#3D2B1F' }}>{feature.label}</h3>
                </div>
              ))}
            </div>

            {/* Recommended For You */}
            <div>
              <div className="flex items-center justify-between mb-3">
                <h3 className="font-serif text-xl font-bold flex items-center gap-2" style={{ color: '#3D2B1F' }}>
                  Recommended For You
                  <ChevronRight className="w-5 h-5" style={{ color: '#8B6914' }} />
                </h3>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {recommendedArticles.map((item) => (
                  <div key={item.title}
                       className="rounded-xl p-4 border cursor-pointer transition-all duration-300 hover:-translate-y-0.5"
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
                    <h4 className="font-serif font-bold text-sm whitespace-pre-line leading-tight mb-1"
                        style={{ color: '#3D2B1F' }}>
                      {item.title}
                    </h4>
                    <p className="text-sm" style={{ color: '#7A6548' }}>{item.subtitle}</p>
                    {item.hasButton && (
                      <button className="mt-3 px-4 py-1.5 rounded-full text-white text-xs font-medium transition-all hover:shadow-md"
                              style={{ background: 'linear-gradient(to right, #D4A052, #B8860B)' }}>
                        {item.btnLabel}
                      </button>
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* Second category icons row */}
            <div className="grid grid-cols-4 gap-3">
              {features.map((feature) => (
                <button key={`bottom-${feature.label}`}
                        onClick={() => navigate('/ai-chat')}
                        className="flex flex-col items-center gap-1.5 p-3 rounded-xl border text-center
                                   transition-all duration-200 hover:-translate-y-0.5"
                        style={{
                          background: '#FFF8EE',
                          borderColor: '#D4A052',
                        }}>
                  <div className="w-10 h-10 rounded-full flex items-center justify-center"
                       style={{ background: 'linear-gradient(135deg, #F5E6C8, #EDE0C8)', border: '1.5px solid #D4A052' }}>
                    <feature.icon className="w-4 h-4" style={{ color: '#8B6914' }} />
                  </div>
                  <span className="text-xs font-medium" style={{ color: '#3D2B1F' }}>{feature.label}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Right - Phone Mockup */}
          <div className="relative flex justify-center">
            <div className="relative w-[280px] rounded-[36px] p-3 shadow-2xl"
                 style={{ background: '#3D2B1F', border: '3px solid #D4A052' }}>
              {/* Notch */}
              <div className="absolute top-0 left-1/2 -translate-x-1/2 w-28 h-6 rounded-b-2xl z-10"
                   style={{ background: '#3D2B1F' }} />

              {/* Screen */}
              <div className="w-full rounded-[28px] overflow-hidden flex flex-col"
                   style={{ background: 'linear-gradient(135deg, #F5E6C8, #EDE0C8)' }}>
                {/* Status Bar */}
                <div className="h-8 flex items-center justify-between px-5 pt-2"
                     style={{ background: '#FFF8EE' }}>
                  <span className="text-xs font-semibold" style={{ color: '#3D2B1F' }}>19:00</span>
                  <div className="flex gap-1">
                    <div className="w-4 h-2.5 rounded-sm" style={{ background: '#3D2B1F' }} />
                  </div>
                </div>

                {/* Chat Header */}
                <div className="px-4 py-2.5 flex items-center gap-3"
                     style={{ background: '#FFF8EE', borderBottom: '1px solid #D4A052' }}>
                  <div className="w-9 h-9 rounded-full flex items-center justify-center"
                       style={{ background: 'linear-gradient(135deg, #D4A052, #B8860B)' }}>
                    <Bot className="w-4 h-4 text-white" />
                  </div>
                  <div>
                    <h4 className="font-serif font-bold text-xs" style={{ color: '#3D2B1F' }}>AI Astrologer</h4>
                    <p className="text-[10px] flex items-center gap-1" style={{ color: '#2E7D32' }}>
                      <span className="w-1.5 h-1.5 bg-green-600 rounded-full" />
                      Online
                    </p>
                  </div>
                </div>

                {/* Chat Messages */}
                <div className="p-3 space-y-2 overflow-hidden" style={{ minHeight: '340px' }}>
                  {/* Bot message */}
                  <div className="rounded-lg p-2.5 rounded-tl-none"
                       style={{ background: '#FFF8EE', border: '1px solid #D4A052' }}>
                    <p className="text-[11px]" style={{ color: '#3D2B1F' }}>
                      <span className="font-bold">Namaste Aman Sharma,</span>
                    </p>
                    <p className="text-[11px] mt-0.5" style={{ color: '#7A6548' }}>
                      I am your AI Astrologer. Ask me any question about your Kundli.
                    </p>
                  </div>

                  {/* User message */}
                  <div className="rounded-lg p-2.5 rounded-tr-none ml-6"
                       style={{ background: 'linear-gradient(135deg, #D4A052, #B8860B)', color: 'white' }}>
                    <p className="text-[11px] font-medium">Steady job milega kya in 2026?</p>
                  </div>

                  {/* Bot reply */}
                  <div className="rounded-lg p-2.5 rounded-tl-none"
                       style={{ background: '#FFF8EE', border: '1px solid #D4A052' }}>
                    <p className="text-[10px] mb-1 font-medium" style={{ color: '#8B6914' }}>Reading your Kundli...</p>
                    <p className="text-[11px]" style={{ color: '#3D2B1F' }}>
                      Based on your planetary positions, I will share personalized insights.
                    </p>
                    <div className="mt-1.5 p-2 rounded-md text-[10px]"
                         style={{ background: 'linear-gradient(135deg, #F5E6C8, #EDE0C8)', color: '#7A6548' }}>
                      In 2026, the major period will be of Ketu while the sub-period will of Jupiter.
                    </div>
                    <div className="mt-1.5 space-y-0.5">
                      <p className="text-[10px]" style={{ color: '#3D2B1F' }}>
                        {'\u25B8'} Ketu with Jupiter in the 9th house indicates opportunities, but you must stay disciplined.
                      </p>
                      <p className="text-[10px]" style={{ color: '#8B6914' }}>
                        {'\u25B8'} <strong>Remedies:</strong> include yellow sapphire ring, daily Vishnu pooja
                      </p>
                    </div>
                  </div>
                </div>

                {/* Input */}
                <div className="p-2.5" style={{ background: '#FFF8EE', borderTop: '1px solid #D4A052' }}>
                  <div className="flex items-center gap-2 rounded-full px-3 py-1.5"
                       style={{ background: 'linear-gradient(135deg, #F5E6C8, #EDE0C8)', border: '1px solid #D4A052' }}>
                    <MessageCircle className="w-3.5 h-3.5" style={{ color: '#8B6914' }} />
                    <span className="text-[11px] flex-1" style={{ color: '#7A6548' }}>Ask anything...</span>
                    <div className="w-7 h-7 rounded-full flex items-center justify-center"
                         style={{ background: 'linear-gradient(135deg, #D4A052, #B8860B)' }}>
                      <ChevronRight className="w-3.5 h-3.5 text-white" />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* CTA */}
        <div className="text-center mt-10">
          <button onClick={() => navigate('/ai-chat')}
                  className="inline-flex items-center gap-3 text-white px-8 py-3.5 rounded-full
                           font-serif font-bold text-lg transition-all duration-200 hover:shadow-lg hover:-translate-y-0.5"
                  style={{ background: 'linear-gradient(to right, #D4A052, #B8860B)', boxShadow: '0 4px 14px rgba(139, 105, 20, 0.25)' }}>
            <Sparkles className="w-5 h-5" />
            Start Chat with AI Astrologer
            <ChevronRight className="w-5 h-5" />
          </button>
        </div>
      </div>
    </section>
  );
}
