import { aiAssistant, aiAstrologer } from '../config';
import { Sparkles } from 'lucide-react';

export default function AiAstrologyAssistant() {
  return (
    <section className="py-8 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Section Title */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-2 mb-2">
            <span className="text-2xl font-serif font-bold text-amber-800">
              {aiAssistant.sectionNumber}
            </span>
            <h2 className="text-2xl md:text-3xl font-serif font-bold text-amber-900 tracking-wide">
              {aiAssistant.title}
            </h2>
          </div>
          <p className="text-amber-700/80 max-w-xl mx-auto text-sm md:text-base">
            {aiAssistant.subtitle}
          </p>
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
          {/* Left Side - Categories */}
          <div>
            {/* Category Icons */}
            <div className="grid grid-cols-4 gap-4 mb-8">
              {aiAssistant.categories.map((cat) => (
                <div key={cat.id} className="flex flex-col items-center">
                  <div className="w-16 h-16 rounded-xl overflow-hidden border-2 border-amber-300 shadow-lg mb-2 hover:scale-110 transition-transform cursor-pointer">
                    <img
                      src={cat.icon}
                      alt={cat.label}
                      className="w-full h-full object-cover"
                    />
                  </div>
                  <span className="text-xs text-amber-800 text-center font-medium">
                    {cat.label}
                  </span>
                </div>
              ))}
            </div>
            
            {/* Recommended Cards */}
            <div className="vedic-card p-4">
              <div className="flex items-center gap-2 mb-4">
                <h3 className="font-serif font-semibold text-amber-900">
                  Recommended For You
                </h3>
                <span className="text-amber-600">→</span>
              </div>
              
              <div className="grid grid-cols-2 gap-3">
                {/* Retrograde Card */}
                <div className="bg-gradient-to-br from-amber-50 to-orange-50 rounded-xl p-3 border border-amber-200">
                  <p className="text-sm text-amber-900 font-medium leading-tight">
                    Are intense retrogrades affecting your 1st house?
                  </p>
                  <p className="text-xs text-amber-600/70 mt-1">
                    Here's what to do.
                  </p>
                </div>
                
                {/* Jade Card */}
                <div className="bg-gradient-to-br from-amber-50 to-orange-50 rounded-xl p-3 border border-amber-200 relative overflow-hidden">
                  <div className="relative z-10">
                    <p className="text-sm text-amber-900 font-medium">Rahu Green Jade</p>
                    <p className="text-lg font-bold text-amber-700">₹3,500+</p>
                    <button className="btn-vedic text-xs py-1 px-3 mt-2">
                      Book a Call
                    </button>
                  </div>
                  <img
                    src="/images/recommended/jade.png"
                    alt="Green Jade"
                    className="absolute -right-4 -bottom-4 w-20 h-20 object-contain opacity-80"
                  />
                </div>
              </div>
            </div>
          </div>
          
          {/* Right Side - Phone Mockup */}
          <div className="flex justify-center">
            <div className="phone-mockup w-72">
              <div className="phone-screen p-4">
                {/* Phone Header */}
                <div className="flex items-center justify-between mb-4">
                  <span className="text-xs text-amber-700">{aiAssistant.phoneMockup.time}</span>
                  <div className="flex items-center gap-1">
                    <span className="text-xs text-amber-700">📶</span>
                    <span className="text-xs text-amber-700">🔋</span>
                  </div>
                </div>
                
                {/* App Header */}
                <div className="flex items-center gap-2 mb-4">
                  <Sparkles className="w-5 h-5 text-amber-600" />
                  <span className="font-serif font-semibold text-amber-900">
                    {aiAssistant.phoneMockup.appName}
                  </span>
                </div>
                
                {/* Chat Messages */}
                <div className="space-y-3">
                  {/* Bot Message 1 */}
                  <div className="chat-bubble chat-bubble-bot">
                    <p className="text-xs">{aiAstrologer.chatPreview.greeting}</p>
                    <p className="text-xs mt-1">{aiAstrologer.chatPreview.intro}</p>
                  </div>
                  
                  {/* User Message */}
                  <div className="chat-bubble chat-bubble-user">
                    <p className="text-xs">{aiAstrologer.chatPreview.sampleQuestion}</p>
                  </div>
                  
                  {/* Bot Message 2 */}
                  <div className="chat-bubble chat-bubble-bot">
                    <p className="text-xs">{aiAstrologer.chatPreview.response}</p>
                    <p className="text-xs mt-1">{aiAstrologer.chatPreview.insight}</p>
                  </div>
                  
                  {/* Bot Message 3 - Detailed */}
                  <div className="chat-bubble chat-bubble-bot">
                    <p className="text-xs whitespace-pre-line">{aiAstrologer.chatPreview.detailedResponse}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
