import { Card, CardContent } from '@/components/ui/card';
import { Sun, Moon, Star, Sunrise, Sunset } from 'lucide-react';
import type { FullPanchangData } from '@/sections/Panchang';

interface Props {
  panchang: FullPanchangData;
  language: string;
  t: (key: string) => string;
}

export default function PanchangCoreTab({ panchang, language, t }: Props) {
  const coreElements = [
    { 
      key: 'tithi', 
      icon: Moon, 
      label: language === 'hi' ? 'तिथि' : t('panchang.tithi'),
      value: language === 'hi' ? panchang.tithi.name_hindi || panchang.tithi.name : panchang.tithi.name,
      sub: `${panchang.tithi.number} • ${language === 'hi' ? panchang.tithi.paksha_hindi || panchang.tithi.paksha : panchang.tithi.paksha}`,
      endTime: panchang.tithi.end_time,
      color: 'text-indigo-500',
      bgColor: 'bg-indigo-500/10'
    },
    { 
      key: 'nakshatra', 
      icon: Star, 
      label: language === 'hi' ? 'नक्षत्र' : t('panchang.nakshatra'),
      value: language === 'hi' ? panchang.nakshatra.name_hindi || panchang.nakshatra.name : panchang.nakshatra.name,
      sub: `${language === 'hi' ? 'चरण' : 'Pada'} ${panchang.nakshatra.pada} • ${language === 'hi' ? panchang.nakshatra.lord_hindi || panchang.nakshatra.lord : panchang.nakshatra.lord} ${language === 'hi' ? 'स्वामी' : 'Lord'}`,
      endTime: panchang.nakshatra.end_time,
      color: 'text-yellow-500',
      bgColor: 'bg-yellow-500/10'
    },
    { 
      key: 'yoga', 
      icon: Sun, 
      label: language === 'hi' ? 'योग' : t('panchang.yoga'),
      value: language === 'hi' ? panchang.yoga.name_hindi || panchang.yoga.name : panchang.yoga.name,
      sub: `${language === 'hi' ? 'संख्या' : 'No.'} ${panchang.yoga.number}`,
      endTime: panchang.yoga.end_time,
      color: 'text-orange-500',
      bgColor: 'bg-orange-500/10'
    },
    { 
      key: 'karana', 
      icon: Sunrise, 
      label: language === 'hi' ? 'करण' : t('panchang.karana'),
      value: language === 'hi' ? panchang.karana.name_hindi || panchang.karana.name : panchang.karana.name,
      sub: `${language === 'hi' ? 'संख्या' : 'No.'} ${panchang.karana.number}`,
      endTime: panchang.karana.end_time,
      color: 'text-teal-500',
      bgColor: 'bg-teal-500/10'
    },
  ];

  return (
    <div className="space-y-6">
      {/* Five Elements - Main Display */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {coreElements.map((element) => (
          <Card key={element.key} className="card-sacred overflow-hidden">
            <CardContent className="p-4">
              <div className="flex items-start gap-3">
                <div className={`p-3 rounded-xl ${element.bgColor}`}>
                  <element.icon className={`h-6 w-6 ${element.color}`} />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-cosmic-text-secondary">{element.label}</p>
                  <h3 className="text-lg font-bold text-cosmic-text-primary truncate">{element.value}</h3>
                  <p className="text-xs text-cosmic-text-secondary">{element.sub}</p>
                  {element.endTime && (
                    <p className="text-xs text-sacred-gold mt-1">
                      {language === 'hi' ? 'समाप्ति' : 'Ends'}: {element.endTime}
                    </p>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Sun & Moon Times */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="card-sacred">
          <CardContent className="p-4 text-center">
            <Sun className="h-8 w-8 text-orange-500 mx-auto mb-2" />
            <p className="text-sm text-cosmic-text-secondary">{language === 'hi' ? 'सूर्योदय' : t('panchang.sunrise')}</p>
            <p className="text-xl font-bold text-cosmic-text-primary">{panchang.sunrise}</p>
          </CardContent>
        </Card>
        
        <Card className="card-sacred">
          <CardContent className="p-4 text-center">
            <Sunset className="h-8 w-8 text-orange-600 mx-auto mb-2" />
            <p className="text-sm text-cosmic-text-secondary">{language === 'hi' ? 'सूर्यास्त' : t('panchang.sunset')}</p>
            <p className="text-xl font-bold text-cosmic-text-primary">{panchang.sunset}</p>
          </CardContent>
        </Card>
        
        <Card className="card-sacred">
          <CardContent className="p-4 text-center">
            <Moon className="h-8 w-8 text-indigo-400 mx-auto mb-2" />
            <p className="text-sm text-cosmic-text-secondary">{language === 'hi' ? 'चंद्रोदय' : t('panchang.moonrise')}</p>
            <p className="text-xl font-bold text-cosmic-text-primary">{panchang.moonrise}</p>
          </CardContent>
        </Card>
        
        <Card className="card-sacred">
          <CardContent className="p-4 text-center">
            <Moon className="h-8 w-8 text-indigo-600 mx-auto mb-2" />
            <p className="text-sm text-cosmic-text-secondary">{language === 'hi' ? 'चंद्रास्त' : t('panchang.moonset')}</p>
            <p className="text-xl font-bold text-cosmic-text-primary">{panchang.moonset}</p>
          </CardContent>
        </Card>
      </div>

      {/* Day Duration Info */}
      <Card className="card-sacred border-sacred-gold/30">
        <CardContent className="p-4">
          <h4 className="font-semibold text-cosmic-text-primary mb-3">
            {language === 'hi' ? 'दिन की अवधि' : 'Day Duration'}
          </h4>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            {panchang.dinamana && (
              <div>
                <p className="text-xs text-cosmic-text-secondary">{language === 'hi' ? 'दिनमान' : 'Day Length'}</p>
                <p className="font-medium text-cosmic-text-primary">{panchang.dinamana}</p>
              </div>
            )}
            {panchang.ratrimana && (
              <div>
                <p className="text-xs text-cosmic-text-secondary">{language === 'hi' ? 'रात्रिमान' : 'Night Length'}</p>
                <p className="font-medium text-cosmic-text-primary">{panchang.ratrimana}</p>
              </div>
            )}
            {panchang.madhyahna && (
              <div>
                <p className="text-xs text-cosmic-text-secondary">{language === 'hi' ? 'मध्याह्न' : 'Mid-day'}</p>
                <p className="font-medium text-cosmic-text-primary">{panchang.madhyahna}</p>
              </div>
            )}
            {panchang.vaar && (
              <div>
                <p className="text-xs text-cosmic-text-secondary">{language === 'hi' ? 'वार' : 'Weekday'}</p>
                <p className="font-medium text-cosmic-text-primary">
                  {language === 'hi' ? panchang.vaar.name_hindi || panchang.vaar.name : panchang.vaar.name}
                </p>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
