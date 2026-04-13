import { useMemo } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Clock, Sun, Moon, CheckCircle2, XCircle, AlertCircle } from 'lucide-react';
import type { FullPanchangData } from '@/sections/Panchang';

interface Props {
  panchang: FullPanchangData;
  language: string;
  t: (key: string) => string;
  timezoneOffset: number;
}

const CHOGHADIYA_QUALITY: Record<string, { color: string; bg: string; icon: typeof CheckCircle2 }> = {
  'Amrit': { color: 'text-green-500', bg: 'bg-green-500/10', icon: CheckCircle2 },
  'Shubh': { color: 'text-green-600', bg: 'bg-green-600/10', icon: CheckCircle2 },
  'Labh': { color: 'text-emerald-500', bg: 'bg-emerald-500/10', icon: CheckCircle2 },
  'Char': { color: 'text-blue-500', bg: 'bg-blue-500/10', icon: AlertCircle },
  'Udveg': { color: 'text-red-500', bg: 'bg-red-500/10', icon: XCircle },
  'Kaal': { color: 'text-red-600', bg: 'bg-red-600/10', icon: XCircle },
  'Rog': { color: 'text-orange-500', bg: 'bg-orange-500/10', icon: XCircle },
};

const CHOGHADIYA_HINDI: Record<string, string> = {
  'Amrit': 'अमृत', 'Shubh': 'शुभ', 'Labh': 'लाभ', 'Char': 'चर',
  'Udveg': 'उद्वेग', 'Kaal': 'काल', 'Rog': 'रोग',
};

export default function ChoghadiyaTab({ panchang, language, t, timezoneOffset }: Props) {
  const choghadiya = panchang.choghadiya || [];
  
  // Memoize day/night separation and current choghadiya calculation
  const { dayChoghadiya, nightChoghadiya, currentChoghadiya } = useMemo(() => {
    // Separate day and night choghadiya
    const day = choghadiya.filter(c => {
      const startHour = parseInt(c.start.split(':')[0]);
      return startHour >= 6 && startHour < 18;
    });
    
    const night = choghadiya.filter(c => {
      const startHour = parseInt(c.start.split(':')[0]);
      return startHour < 6 || startHour >= 18;
    });

    // Find current choghadiya (based on panchang location time, not browser local time)
    const currentTimeAtLocation = new Date(Date.now() + (timezoneOffset * 60 * 1000));
    const currentHour = currentTimeAtLocation.getHours();
    const currentMinute = currentTimeAtLocation.getMinutes();
    const currentTime = `${currentHour.toString().padStart(2, '0')}:${currentMinute.toString().padStart(2, '0')}`;
    
    const current = choghadiya.find(c => {
      return currentTime >= c.start && currentTime < c.end;
    });
    
    return { dayChoghadiya: day, nightChoghadiya: night, currentChoghadiya: current };
  }, [choghadiya, timezoneOffset]);

  const renderChoghadiyaCard = (period: typeof choghadiya[0], isCurrent: boolean) => {
    const quality = CHOGHADIYA_QUALITY[period.name] || { color: 'text-gray-500', bg: 'bg-gray-500/10', icon: AlertCircle };
    const Icon = quality.icon;
    
    return (
      <div 
        key={`${period.start}-${period.end}`}
        className={`
          p-3 rounded-xl border transition-all
          ${isCurrent ? 'border-sacred-gold bg-sacred-gold/10' : 'border-transparent hover:border-cosmic-border'}
          ${!isCurrent ? quality.bg : ''}
        `}
      >
        <div className="flex items-center justify-between mb-2">
          <span className={`font-semibold ${isCurrent ? 'text-sacred-gold' : 'text-cosmic-text-primary'}`}>
            {language === 'hi' ? period.name_hindi || CHOGHADIYA_HINDI[period.name] || period.name : period.name}
          </span>
          <Icon className={`h-4 w-4 ${quality.color}`} />
        </div>
        <p className="text-sm text-cosmic-text-secondary">
          {period.start} - {period.end}
        </p>
        <p className={`text-xs mt-1 ${quality.color}`}>
          {language === 'hi' ? period.quality : period.quality}
        </p>
        {isCurrent && (
          <span className="inline-block mt-2 px-2 py-0.5 text-xs bg-sacred-gold text-cosmic-bg rounded-full">
            {language === 'hi' ? 'अभी' : 'Now'}
          </span>
        )}
      </div>
    );
  };

  return (
    <div className="space-y-6">
      {/* Current Choghadiya */}
      {currentChoghadiya && (
        <Card className="card-sacred border-sacred-gold/30">
          <CardContent className="p-6">
            <div className="flex flex-col sm:flex-row items-center gap-4">
              <div className="p-4 rounded-2xl bg-sacred-gold/20">
                <Clock className="h-12 w-12 text-sacred-gold" />
              </div>
              <div className="text-center sm:text-left">
                <p className="text-sm text-cosmic-text-secondary">
                  {language === 'hi' ? 'वर्तमान चौघड़िया' : 'Current Choghadiya'}
                </p>
                <h3 className="text-3xl font-bold text-cosmic-text-primary">
                  {language === 'hi' 
                    ? currentChoghadiya.name_hindi || CHOGHADIYA_HINDI[currentChoghadiya.name] || currentChoghadiya.name
                    : currentChoghadiya.name}
                </h3>
                <p className="text-lg text-sacred-gold">
                  {currentChoghadiya.start} - {currentChoghadiya.end}
                </p>
                <p className={`text-sm mt-1 ${CHOGHADIYA_QUALITY[currentChoghadiya.name]?.color || 'text-gray-500'}`}>
                  {language === 'hi' ? currentChoghadiya.quality : currentChoghadiya.quality}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Day Choghadiya */}
      {dayChoghadiya.length > 0 && (
        <Card className="card-sacred">
          <CardContent className="p-4">
            <h3 className="text-lg font-bold text-cosmic-text-primary mb-4 flex items-center gap-2">
              <Sun className="h-5 w-5 text-orange-500" />
              {language === 'hi' ? 'दिन के चौघड़िया' : 'Day Choghadiya (Sunrise to Sunset)'}
            </h3>
            <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-3">
              {dayChoghadiya.map((period) => renderChoghadiyaCard(
                period, 
                currentChoghadiya?.start === period.start
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Night Choghadiya */}
      {nightChoghadiya.length > 0 && (
        <Card className="card-sacred">
          <CardContent className="p-4">
            <h3 className="text-lg font-bold text-cosmic-text-primary mb-4 flex items-center gap-2">
              <Moon className="h-5 w-5 text-indigo-400" />
              {language === 'hi' ? 'रात्रि के चौघड़िया' : 'Night Choghadiya (Sunset to Sunrise)'}
            </h3>
            <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-3">
              {nightChoghadiya.map((period) => renderChoghadiyaCard(
                period, 
                currentChoghadiya?.start === period.start
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Legend */}
      <Card className="card-sacred">
        <CardContent className="p-4">
          <h4 className="font-semibold text-cosmic-text-primary mb-3">
            {language === 'hi' ? 'चौघड़िया का अर्थ' : 'Choghadiya Meanings'}
          </h4>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-sm">
            <div className="flex items-center gap-2 p-2 rounded-lg bg-green-500/10">
              <CheckCircle2 className="h-4 w-4 text-green-500" />
              <div>
                <p className="font-medium text-cosmic-text-primary">
                  {language === 'hi' ? 'अमृत, शुभ, लाभ' : 'Amrit, Shubh, Labh'}
                </p>
                <p className="text-xs text-cosmic-text-secondary">
                  {language === 'hi' ? 'सर्वश्रेष्ठ - कोई भी कार्य' : 'Best for any work'}
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2 p-2 rounded-lg bg-blue-500/10">
              <AlertCircle className="h-4 w-4 text-blue-500" />
              <div>
                <p className="font-medium text-cosmic-text-primary">
                  {language === 'hi' ? 'चर' : 'Char'}
                </p>
                <p className="text-xs text-cosmic-text-secondary">
                  {language === 'hi' ? 'यात्रा के लिए अच्छा' : 'Good for travel'}
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2 p-2 rounded-lg bg-orange-500/10">
              <XCircle className="h-4 w-4 text-orange-500" />
              <div>
                <p className="font-medium text-cosmic-text-primary">
                  {language === 'hi' ? 'रोग, उद्वेग' : 'Rog, Udveg'}
                </p>
                <p className="text-xs text-cosmic-text-secondary">
                  {language === 'hi' ? 'सामान्य - सावधानी बरतें' : 'Average - be cautious'}
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2 p-2 rounded-lg bg-red-500/10">
              <XCircle className="h-4 w-4 text-red-500" />
              <div>
                <p className="font-medium text-cosmic-text-primary">
                  {language === 'hi' ? 'काल' : 'Kaal'}
                </p>
                <p className="text-xs text-cosmic-text-secondary">
                  {language === 'hi' ? 'अशुभ - टालें' : 'Inauspicious - avoid'}
                </p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
