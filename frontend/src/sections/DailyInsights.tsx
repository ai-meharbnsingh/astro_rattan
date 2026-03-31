import { dailyInsights, aiAstrologer } from '../config';
import { Moon, Sun, Clock, MapPin, Calendar, Calculator, MessageCircle, Star } from 'lucide-react';

const iconMap: Record<string, React.ReactNode> = {
  '🌙': <Moon className="w-5 h-5 text-amber-600" />,
  '☀️': <Sun className="w-5 h-5 text-amber-600" />,
  '⏰': <Clock className="w-5 h-5 text-amber-600" />,
  '📍': <MapPin className="w-5 h-5 text-amber-600" />,
  '🪔': <Calendar className="w-5 h-5 text-amber-600" />,
  '♈': <Calculator className="w-5 h-5 text-amber-600" />,
};

export default function DailyInsights() {
  return (
    <section className="py-6 px-4">
      <div className="max-w-6xl mx-auto">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Daily Insights Panel */}
          <div className="lg:col-span-2 vedic-card p-5">
            {/* Header */}
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <h2 className="section-title text-lg m-0">{dailyInsights.title}</h2>
                <span className="star-decoration">✦</span>
              </div>
              <div className="flex items-center gap-2 text-sm text-amber-700">
                <span>{dailyInsights.subtitle}</span>
                <span className="text-amber-500">{dailyInsights.note}</span>
              </div>
            </div>
            
            {/* Insights Grid */}
            <div className="grid grid-cols-2 gap-3">
              {dailyInsights.items.map((item) => (
                <div
                  key={item.id}
                  className="bg-gradient-to-br from-amber-50 to-orange-50 rounded-xl p-3 border border-amber-200/50 hover:shadow-md transition-shadow"
                >
                  <div className="flex items-start gap-3">
                    {/* Icon */}
                    <div className="w-10 h-10 rounded-full bg-gradient-to-br from-amber-100 to-orange-100 flex items-center justify-center border border-amber-300 flex-shrink-0">
                      {iconMap[item.icon]}
                    </div>
                    
                    {/* Content */}
                    <div className="flex-1 min-w-0">
                      <h4 className="font-medium text-sm text-amber-900">{item.title}</h4>
                      {item.subtitle && (
                        <p className="text-xs text-amber-600/70">{item.subtitle}</p>
                      )}
                      {item.time && (
                        <p className="text-xs text-amber-700 mt-1">{item.time}</p>
                      )}
                      {item.action && (
                        <div className="flex items-center gap-1 mt-1">
                          <span className="text-xs font-medium text-amber-700">{item.action}</span>
                          <Star className="w-3 h-3 text-amber-500 fill-amber-500" />
                        </div>
                      )}
                      {item.buttonText && (
                        <button className="btn-vedic-outline text-xs mt-2 py-1 px-3">
                          {item.buttonText}
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
          
          {/* AI Astrologer Panel */}
          <div className="vedic-card p-0 overflow-hidden">
            {/* Background Image with Sage */}
            <div className="relative h-48">
              <img
                src={aiAstrologer.backgroundImage}
                alt="AI Astrologer"
                className="w-full h-full object-cover object-top"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-amber-900/60 to-transparent" />
              
              {/* Astrologer Info Overlay */}
              <div className="absolute bottom-3 left-3 right-3">
                <div className="flex items-center gap-2 mb-1">
                  <MessageCircle className="w-4 h-4 text-amber-300" />
                  <span className="text-white text-sm font-medium">{aiAstrologer.title}</span>
                </div>
                <p className="text-amber-200 text-xs">{aiAstrologer.subtitle}</p>
              </div>
            </div>
            
            {/* Chat Preview */}
            <div className="p-4 bg-gradient-to-br from-amber-50 to-orange-50">
              {/* Astrologer Profile */}
              <div className="flex items-center gap-3 mb-3">
                <img
                  src={aiAstrologer.image}
                  alt={aiAstrologer.astrologerName}
                  className="w-10 h-10 rounded-full border-2 border-amber-400 object-cover"
                />
                <div>
                  <p className="font-medium text-sm text-amber-900">{aiAstrologer.astrologerName}</p>
                  <p className="text-xs text-amber-600/70">{aiAstrologer.status}</p>
                </div>
              </div>
              
              {/* Status Detail */}
              <div className="bg-white/70 rounded-lg p-2 mb-3">
                <p className="text-xs text-amber-700">{aiAstrologer.statusDetail}</p>
              </div>
              
              {/* Generate Button */}
              <button className="btn-vedic w-full text-sm py-2">
                {aiAstrologer.buttonText}
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
