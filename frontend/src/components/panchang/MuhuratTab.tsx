import { Card, CardContent } from '@/components/ui/card';
import { Clock, AlertTriangle, CheckCircle2, Sparkles, Sunrise, Moon } from 'lucide-react';
import type { FullPanchangData } from '@/sections/Panchang';

interface Props {
  panchang: FullPanchangData;
  language: string;
  t: (key: string) => string;
}

export default function MuhuratTab({ panchang, language, t }: Props) {
  // Inauspicious periods
  const inauspiciousPeriods = [
    {
      key: 'rahu_kaal',
      name: language === 'hi' ? 'राहु काल' : 'Rahu Kaal',
      period: panchang.rahu_kaal,
      icon: AlertTriangle,
      color: 'text-red-500',
      bgColor: 'bg-red-500/10',
      desc: language === 'hi' ? 'अशुभ समय - कोई भी शुभ कार्य न करें' : 'Inauspicious - avoid new beginnings'
    },
    {
      key: 'gulika_kaal',
      name: language === 'hi' ? 'गुलिक काल' : 'Gulika Kaal',
      period: panchang.gulika_kaal,
      icon: AlertTriangle,
      color: 'text-orange-600',
      bgColor: 'bg-orange-600/10',
      desc: language === 'hi' ? 'मिश्रित फल' : 'Mixed results'
    },
    {
      key: 'yamaganda',
      name: language === 'hi' ? 'यमगंड' : 'Yamaganda',
      period: panchang.yamaganda,
      icon: AlertTriangle,
      color: 'text-amber-600',
      bgColor: 'bg-amber-600/10',
      desc: language === 'hi' ? 'यम का समय - यात्रा से बचें' : 'Yama time - avoid travel'
    },
    {
      key: 'dur_muhurtam',
      name: language === 'hi' ? 'दुर्मुहूर्त' : 'Dur Muhurtam',
      period: panchang.dur_muhurtam,
      icon: AlertTriangle,
      color: 'text-red-600',
      bgColor: 'bg-red-600/10',
      desc: language === 'hi' ? 'अत्यंत अशुभ' : 'Highly inauspicious'
    },
    {
      key: 'varjyam',
      name: language === 'hi' ? 'वर्ज्य' : 'Varjyam',
      period: panchang.varjyam,
      icon: AlertTriangle,
      color: 'text-rose-500',
      bgColor: 'bg-rose-500/10',
      desc: language === 'hi' ? 'वर्जित समय' : 'Prohibited time'
    },
  ].filter(p => p.period && (p.period.start !== '--:--' || p.period.end !== '--:--'));

  // Auspicious periods
  const auspiciousPeriods = [
    {
      key: 'brahma_muhurat',
      name: language === 'hi' ? 'ब्रह्म मुहूर्त' : 'Brahma Muhurat',
      period: panchang.brahma_muhurat,
      icon: Sunrise,
      color: 'text-purple-500',
      bgColor: 'bg-purple-500/10',
      desc: language === 'hi' ? 'सबसे शुभ - ध्यान और पूजा के लिए' : 'Most auspicious - meditation & puja'
    },
    {
      key: 'abhijit_muhurat',
      name: language === 'hi' ? 'अभिजित मुहूर्त' : 'Abhijit Muhurat',
      period: panchang.abhijit_muhurat,
      icon: Sparkles,
      color: 'text-green-500',
      bgColor: 'bg-green-500/10',
      desc: language === 'hi' ? 'विजय का समय - कोई भी कार्य सफल' : 'Victory time - any work succeeds'
    },
    {
      key: 'vijaya_muhurta',
      name: language === 'hi' ? 'विजया मुहूर्त' : 'Vijaya Muhurta',
      period: panchang.vijaya_muhurta,
      icon: CheckCircle2,
      color: 'text-emerald-500',
      bgColor: 'bg-emerald-500/10',
      desc: language === 'hi' ? 'विजय प्राप्ति का समय' : 'Time for victory'
    },
    {
      key: 'godhuli_muhurta',
      name: language === 'hi' ? 'गोधूलि मुहूर्त' : 'Godhuli Muhurta',
      period: panchang.godhuli_muhurta,
      icon: Sparkles,
      color: 'text-amber-500',
      bgColor: 'bg-amber-500/10',
      desc: language === 'hi' ? 'गायों के घर लौटने का समय - शुभ' : 'When cows return - auspicious'
    },
    {
      key: 'nishita_muhurta',
      name: language === 'hi' ? 'निशीथ मुहूर्त' : 'Nishita Muhurta',
      period: panchang.nishita_muhurta,
      icon: Moon,
      color: 'text-indigo-500',
      bgColor: 'bg-indigo-500/10',
      desc: language === 'hi' ? 'रात्रि का शुभ समय' : 'Auspicious night time'
    },
  ].filter(p => p.period && (p.period.start !== '--:--' || p.period.end !== '--:--'));

  // Special Yogas
  const specialYogas = [
    { key: 'ravi_yoga', name: language === 'hi' ? 'रवि योग' : 'Ravi Yoga', data: panchang.ravi_yoga },
    { key: 'amrit_siddhi', name: language === 'hi' ? 'अमृत सिद्धि' : 'Amrit Siddhi', data: panchang.amrit_siddhi },
    { key: 'sarvartha_siddhi', name: language === 'hi' ? 'सर्वार्थ सिद्धि' : 'Sarvartha Siddhi', data: panchang.sarvartha_siddhi },
    { key: 'tripushkar', name: language === 'hi' ? 'त्रिपुष्कर' : 'Tripushkar', data: panchang.tripushkar },
    { key: 'dwipushkar', name: language === 'hi' ? 'द्विपुष्कर' : 'Dwipushkar', data: panchang.dwipushkar },
  ].filter(y => y.data && (y.data.active || (y.data.start && y.data.end)));

  return (
    <div className="space-y-6">
      {/* Auspicious Periods */}
      <Card className="card-sacred border-green-500/30">
        <CardContent className="p-4">
          <h3 className="text-lg font-bold text-green-600 mb-4 flex items-center gap-2">
            <CheckCircle2 className="h-5 w-5" />
            {language === 'hi' ? 'शुभ मुहूर्त (उपयुक्त समय)' : 'Auspicious Muhurats (Good Times)'}
          </h3>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {auspiciousPeriods.map((period) => (
              <div key={period.key} className={`p-4 rounded-xl ${period.bgColor} border border-transparent`}>
                <div className="flex items-center gap-2 mb-2">
                  <period.icon className={`h-5 w-5 ${period.color}`} />
                  <span className="font-semibold text-cosmic-text-primary">{period.name}</span>
                </div>
                <div className="text-2xl font-bold text-cosmic-text-primary mb-1">
                  {period.period?.start} - {period.period?.end}
                </div>
                <p className="text-xs text-cosmic-text-secondary">{period.desc}</p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Inauspicious Periods */}
      <Card className="card-sacred border-red-500/30">
        <CardContent className="p-4">
          <h3 className="text-lg font-bold text-red-600 mb-4 flex items-center gap-2">
            <AlertTriangle className="h-5 w-5" />
            {language === 'hi' ? 'अशुभ समय (वर्जित)' : 'Inauspicious Times (Avoid)'}
          </h3>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {inauspiciousPeriods.map((period) => (
              <div key={period.key} className={`p-4 rounded-xl ${period.bgColor} border border-transparent`}>
                <div className="flex items-center gap-2 mb-2">
                  <period.icon className={`h-5 w-5 ${period.color}`} />
                  <span className="font-semibold text-cosmic-text-primary">{period.name}</span>
                </div>
                <div className="text-2xl font-bold text-cosmic-text-primary mb-1">
                  {period.period?.start} - {period.period?.end}
                </div>
                <p className="text-xs text-cosmic-text-secondary">{period.desc}</p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Special Yogas */}
      {specialYogas.length > 0 && (
        <Card className="card-sacred border-sacred-gold/30">
          <CardContent className="p-4">
            <h3 className="text-lg font-bold text-sacred-gold mb-4 flex items-center gap-2">
              <Sparkles className="h-5 w-5" />
              {language === 'hi' ? 'विशेष योग' : 'Special Yogas'}
            </h3>
            
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {specialYogas.map((yoga) => (
                <div key={yoga.key} className="p-4 rounded-xl bg-sacred-gold/10 border border-sacred-gold/30">
                  <div className="flex items-center gap-2 mb-2">
                    <Sparkles className="h-5 w-5 text-sacred-gold" />
                    <span className="font-semibold text-cosmic-text-primary">{yoga.name}</span>
                  </div>
                  {yoga.data?.start && yoga.data?.end && (
                    <div className="text-lg font-bold text-cosmic-text-primary">
                      {yoga.data.start} - {yoga.data.end}
                    </div>
                  )}
                  <p className="text-xs text-green-600 mt-1">
                    {language === 'hi' ? 'आज यह योग सक्रिय है' : 'This yoga is active today'}
                  </p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Sandhya Times */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {panchang.pratah_sandhya && (
          <Card className="card-sacred">
            <CardContent className="p-4">
              <div className="flex items-center gap-2 mb-2">
                <Sunrise className="h-5 w-5 text-orange-500" />
                <span className="font-semibold text-cosmic-text-primary">
                  {language === 'hi' ? 'प्रातः संध्या' : 'Pratah Sandhya'}
                </span>
              </div>
              <p className="text-lg font-bold text-cosmic-text-primary">
                {panchang.pratah_sandhya.start} - {panchang.pratah_sandhya.end}
              </p>
              <p className="text-xs text-cosmic-text-secondary">
                {language === 'hi' ? 'गायत्री जप का समय' : 'Time for Gayatri Japa'}
              </p>
            </CardContent>
          </Card>
        )}
        
        {panchang.sayahna_sandhya && (
          <Card className="card-sacred">
            <CardContent className="p-4">
              <div className="flex items-center gap-2 mb-2">
                <Clock className="h-5 w-5 text-indigo-500" />
                <span className="font-semibold text-cosmic-text-primary">
                  {language === 'hi' ? 'सायंह्न संध्या' : 'Sayahna Sandhya'}
                </span>
              </div>
              <p className="text-lg font-bold text-cosmic-text-primary">
                {panchang.sayahna_sandhya.start} - {panchang.sayahna_sandhya.end}
              </p>
              <p className="text-xs text-cosmic-text-secondary">
                {language === 'hi' ? 'सन्ध्या जप का समय' : 'Time for Sandhya Japa'}
              </p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
