import { Card, CardContent } from '@/components/ui/card';
import { Heading } from '@/components/ui/heading';
import { AlertCircle, CheckCircle, Clock, Lightbulb, Zap } from 'lucide-react';
import type { FullPanchangData } from '@/sections/Panchang';

interface Props {
  panchang: FullPanchangData;
  language: string;
  t: (key: string) => string;
  currentTime: Date;
}

export default function MuhuratSummary({ panchang, language, t, currentTime }: Props) {
  const isHi = language === 'hi';
  const l = (en: string, hi: string) => isHi ? hi : en;

  // Get best muhurat for today
  const bestMuhurat = panchang.abhijit_muhurat || panchang.brahma_muhurat || panchang.vijaya_muhurta;

  // Get main things to avoid
  const thingsToAvoid = [];
  if (panchang.rahu_kaal) {
    thingsToAvoid.push({
      name: t('auto.rahuKaal'),
      time: `${panchang.rahu_kaal.start} – ${panchang.rahu_kaal.end}`,
      icon: '⚠️'
    });
  }

  // Generate do's based on panchang
  const dos: string[] = [];
  const tithi = panchang.tithi?.name?.toLowerCase() || '';

  if (tithi.includes('ekadashi')) {
    dos.push(l('Fast (Vrat)', 'व्रत रखें'));
    dos.push(l('Worship Vishnu', 'विष्णु पूजा'));
  }
  if (tithi.includes('pradosh')) {
    dos.push(l('Shiva worship', 'शिव पूजा'));
    dos.push(l('Evening rituals', 'संध्या पूजन'));
  }
  if (tithi.includes('chaturthi')) {
    dos.push(l('Ganesha worship', 'गणेश पूजा'));
  }
  if (tithi.includes('purnima') || tithi.includes('amavasya')) {
    dos.push(l('Ancestor worship', 'पितृ अर्चना'));
  }

  // Current time comparison with Rahu Kaal
  const currentMins = currentTime.getHours() * 60 + currentTime.getMinutes();
  const formatTime = (timeStr: string | undefined) => {
    if (!timeStr) return null;
    const [hours, mins] = timeStr.split(':').map(Number);
    return hours * 60 + mins;
  };

  const rahuStartMins = formatTime(panchang.rahu_kaal?.start);
  const rahuEndMins = formatTime(panchang.rahu_kaal?.end);
  const isRahuActive = rahuStartMins !== null && rahuEndMins !== null && currentMins >= rahuStartMins && currentMins < rahuEndMins;

  return (
    <div className="space-y-4 pb-4 border-b border-border/30">
      {/* Quick Status Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        {/* Best Muhurat */}
        {bestMuhurat && (
          <Card className="bg-gradient-to-br from-green-50 to-green-50/50 border-green-200/50">
            <CardContent className="p-3">
              <div className="flex items-start gap-2">
                <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                <div className="min-w-0 flex-1">
                  <p className="text-[10px] font-bold text-green-600 uppercase tracking-wide">
                    {l('Best Time Today', 'आज का सर्वश्रेष्ठ समय')}
                  </p>
                  <p className="text-sm font-bold text-foreground mt-1 truncate">
                    {bestMuhurat.start} – {bestMuhurat.end}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Main Thing to Avoid */}
        {thingsToAvoid.length > 0 && (
          <Card className={`bg-gradient-to-br ${isRahuActive ? 'from-red-50 to-red-50/50 border-red-200/50' : 'from-orange-50 to-orange-50/50 border-orange-200/50'}`}>
            <CardContent className="p-3">
              <div className="flex items-start gap-2">
                <AlertCircle className={`w-5 h-5 ${isRahuActive ? 'text-red-600' : 'text-orange-600'} flex-shrink-0 mt-0.5`} />
                <div className="min-w-0 flex-1">
                  <p className={`text-[10px] font-bold ${isRahuActive ? 'text-red-600' : 'text-orange-600'} uppercase tracking-wide`}>
                    {l('Time to Avoid', 'बचने का समय')}
                  </p>
                  <p className="text-sm font-bold text-foreground mt-1 truncate">
                    {thingsToAvoid[0].time}
                  </p>
                  {isRahuActive && (
                    <p className="text-[10px] text-red-600 font-semibold mt-1">
                      {l('🔴 ACTIVE NOW', '🔴 अभी सक्रिय')}
                    </p>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Special Yoga Highlight */}
        {(panchang.special_yogas?.sarvartha_siddhi?.active || panchang.special_yogas?.amrit_siddhi?.active) && (
          <Card className="bg-gradient-to-br from-purple-50 to-purple-50/50 border-purple-200/50">
            <CardContent className="p-3">
              <div className="flex items-start gap-2">
                <Zap className="w-5 h-5 text-purple-600 flex-shrink-0 mt-0.5" />
                <div className="min-w-0 flex-1">
                  <p className="text-[10px] font-bold text-purple-600 uppercase tracking-wide">
                    {l('Rare Yoga', 'विशेष योग')}
                  </p>
                  <p className="text-sm font-bold text-foreground mt-1 truncate">
                    {panchang.special_yogas?.sarvartha_siddhi?.active
                      ? (isHi && panchang.special_yogas.sarvartha_siddhi.name_hindi
                          ? panchang.special_yogas.sarvartha_siddhi.name_hindi
                          : 'Sarvartha Siddhi')
                      : (isHi && panchang.special_yogas?.amrit_siddhi?.name_hindi
                          ? panchang.special_yogas.amrit_siddhi.name_hindi
                          : 'Amrit Siddhi')}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}
      </div>

      {/* Quick Tips */}
      {dos.length > 0 && (
        <Card className="bg-card/50 border-border/30">
          <CardContent className="p-3">
            <div className="flex items-start gap-2">
              <Lightbulb className="w-4 h-4 text-sacred-gold flex-shrink-0 mt-0.5" />
              <div className="min-w-0 flex-1">
                <p className="text-xs font-bold text-muted-foreground uppercase tracking-wide mb-2">
                  {l('Good to Do Today', 'आज करने के लिए अच्छे काम')}
                </p>
                <div className="flex flex-wrap gap-2">
                  {dos.map((item, idx) => (
                    <span key={idx} className="text-xs font-medium bg-sacred-gold/10 text-sacred-gold px-2.5 py-1 rounded-full">
                      ✓ {item}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Warning for Ganda Moola */}
      {panchang.special_yogas?.ganda_moola?.active && (
        <Card className="bg-red-50/50 border-red-200/50">
          <CardContent className="p-3">
            <div className="flex items-start gap-2">
              <AlertCircle className="w-4 h-4 text-red-600 flex-shrink-0 mt-0.5" />
              <div className="min-w-0 flex-1">
                <p className="text-xs font-bold text-red-700">
                  {l('⚡ Ganda Moola Active', '⚡ गंड मूल सावधानी')}
                </p>
                <p className="text-xs text-red-600 mt-1">
                  {l('Postpone major events to another date', 'बड़े कार्यों के लिए दूसरी तारीख चुनें')}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
