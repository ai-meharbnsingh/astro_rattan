import { useMemo } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Moon, Sun, CheckCircle2, XCircle } from 'lucide-react';
import type { FullPanchangData } from '@/sections/Panchang';

interface Props {
  panchang: FullPanchangData;
  language: string;
  t: (key: string) => string;
  timezoneOffset: number;
}

export default function GowriTab({ panchang, language, t, timezoneOffset }: Props) {
  const gowriPanchang = panchang.gowri_panchang || [];
  
  // Memoize day/night separation and current gowri calculation
  const { dayGowri, nightGowri, currentGowri } = useMemo(() => {
    // Separate day and night gowri
    const day = gowriPanchang.filter(g => g.type === 'Day' || g.type === 'दिन');
    const night = gowriPanchang.filter(g => g.type === 'Night' || g.type === 'रात्रि');

    // Find current gowri period (based on panchang location time, not browser local time)
    const currentTimeAtLocation = new Date(Date.now() + (timezoneOffset * 60 * 1000));
    const currentTime = `${currentTimeAtLocation.getHours().toString().padStart(2, '0')}:${currentTimeAtLocation.getMinutes().toString().padStart(2, '0')}`;
    
    const current = gowriPanchang.find(g => {
      return currentTime >= g.start && currentTime < g.end;
    });
    
    return { dayGowri: day, nightGowri: night, currentGowri: current };
  }, [gowriPanchang, timezoneOffset]);

  const getQualityStyle = (quality: string) => {
    if (quality.toLowerCase().includes('good') || quality === 'शुभ') {
      return { color: 'text-green-500', bg: 'bg-green-500/10', icon: CheckCircle2 };
    }
    return { color: 'text-red-500', bg: 'bg-red-500/10', icon: XCircle };
  };

  const renderGowriGrid = (periods: typeof gowriPanchang) => (
    <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
      {periods.map((period, index) => {
        const style = getQualityStyle(period.quality);
        const Icon = style.icon;
        const isCurrent = currentGowri?.name === period.name && currentGowri?.type === period.type;
        
        return (
          <div 
            key={index}
            className={`
              p-3 rounded-xl border transition-all
              ${isCurrent ? 'border-sacred-gold bg-sacred-gold/10' : 'border-transparent bg-cosmic-card/50'}
            `}
          >
            <div className="flex items-center justify-between mb-2">
              <span className={`font-semibold ${isCurrent ? 'text-sacred-gold' : 'text-cosmic-text-primary'}`}>
                {language === 'hi' ? period.name_hindi || period.name : period.name}
              </span>
              <Icon className={`h-4 w-4 ${style.color}`} />
            </div>
            <p className="text-sm text-cosmic-text-secondary">
              {period.start} - {period.end}
            </p>
            <span className={`inline-block mt-2 text-xs px-2 py-0.5 rounded-full ${style.bg} ${style.color}`}>
              {language === 'hi' ? period.quality_hindi || period.quality : period.quality}
            </span>
            {isCurrent && (
              <span className="block mt-2 text-xs text-sacred-gold font-medium">
                {language === 'hi' ? 'अभी' : 'Now'}
              </span>
            )}
          </div>
        );
      })}
    </div>
  );

  return (
    <div className="space-y-6">
      {/* Current Gowri */}
      {currentGowri && (
        <Card className="card-sacred border-sacred-gold/30">
          <CardContent className="p-6">
            <div className="flex flex-col sm:flex-row items-center gap-4">
              <div className="p-4 rounded-2xl bg-sacred-gold/20">
                <Moon className="h-12 w-12 text-sacred-gold" />
              </div>
              <div className="text-center sm:text-left">
                <p className="text-sm text-cosmic-text-secondary">
                  {language === 'hi' ? 'वर्तमान गौरी पंचांग' : 'Current Gowri Panchang'}
                </p>
                <h3 className="text-3xl font-bold text-cosmic-text-primary">
                  {language === 'hi' ? currentGowri.name_hindi || currentGowri.name : currentGowri.name}
                </h3>
                <p className="text-lg text-sacred-gold">
                  {currentGowri.start} - {currentGowri.end}
                </p>
                <p className="text-sm text-cosmic-text-secondary mt-1">
                  {language === 'hi' ? currentGowri.type_hindi || currentGowri.type : currentGowri.type}
                </p>
              </div>
              <div className={`ml-auto px-4 py-2 rounded-full ${getQualityStyle(currentGowri.quality).bg}`}>
                <span className={`font-semibold ${getQualityStyle(currentGowri.quality).color}`}>
                  {language === 'hi' ? currentGowri.quality_hindi || currentGowri.quality : currentGowri.quality}
                </span>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Day Gowri */}
      {dayGowri.length > 0 && (
        <Card className="card-sacred">
          <CardContent className="p-4">
            <h3 className="text-lg font-bold text-cosmic-text-primary mb-4 flex items-center gap-2">
              <Sun className="h-5 w-5 text-orange-500" />
              {language === 'hi' ? 'दिन का गौरी पंचांग' : 'Day Gowri Panchang'}
            </h3>
            {renderGowriGrid(dayGowri)}
          </CardContent>
        </Card>
      )}

      {/* Night Gowri */}
      {nightGowri.length > 0 && (
        <Card className="card-sacred">
          <CardContent className="p-4">
            <h3 className="text-lg font-bold text-cosmic-text-primary mb-4 flex items-center gap-2">
              <Moon className="h-5 w-5 text-indigo-400" />
              {language === 'hi' ? 'रात्रि का गौरी पंचांग' : 'Night Gowri Panchang'}
            </h3>
            {renderGowriGrid(nightGowri)}
          </CardContent>
        </Card>
      )}

      {/* Info */}
      <Card className="card-sacred">
        <CardContent className="p-4">
          <h4 className="font-semibold text-cosmic-text-primary mb-2">
            {language === 'hi' ? 'गौरी पंचांग के बारे में' : 'About Gowri Panchang'}
          </h4>
          <p className="text-sm text-cosmic-text-secondary leading-relaxed">
            {language === 'hi' 
              ? 'गौरी पंचांग दिन और रात को 8-8 भागों में बांटता है। प्रत्येक अवधि एक देवता द्वारा शासित होती है। शुभ अवधि में कार्य करने से सफलता मिलती है।'
              : 'Gowri Panchang divides day and night into 8 periods each. Each period is ruled by a deity. Work done during auspicious periods yields success.'}
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
