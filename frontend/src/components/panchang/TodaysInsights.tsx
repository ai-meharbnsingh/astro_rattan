import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Heading } from '@/components/ui/heading';
import { AlertCircle, Lightbulb, CheckCircle, Clock, Zap, BookOpen } from 'lucide-react';
import type { FullPanchangData } from '@/sections/Panchang';

interface Props {
  panchang: FullPanchangData;
  language: string;
  t: (key: string) => string;
  currentTime: Date;
}

export default function TodaysInsights({ panchang, language, t, currentTime }: Props) {
  const isHi = language === 'hi';
  const l = (en: string, hi: string) => isHi ? hi : en;

  // Generate insights based on panchang data
  const insights = [];

  // 1. Festival insight
  if (panchang.festivals && panchang.festivals.length > 0) {
    const majorFestival = panchang.festivals.find(f => f.type === 'major');
    const festival = majorFestival || panchang.festivals[0];
    insights.push({
      type: 'festival',
      icon: '🎊',
      title: l('Festival Today', 'आज पर्व है'),
      content: isHi && festival.name_hindi ? festival.name_hindi : festival.name,
      description: festival.description || '',
      color: 'bg-red-50 border-red-200',
      textColor: 'text-red-700',
    });
  }

  // 2. Auspicious muhurat insight
  if (panchang.abhijit_muhurat) {
    insights.push({
      type: 'muhurat',
      icon: '✨',
      title: l('Auspicious Time', 'शुभ मुहूर्त'),
      content: `${panchang.abhijit_muhurat.start} – ${panchang.abhijit_muhurat.end}`,
      description: l('Best time for important work', 'महत्वपूर्ण कार्यों के लिए शुभ समय'),
      color: 'bg-green-50 border-green-200',
      textColor: 'text-green-700',
    });
  }

  // 3. Avoid time insight (Rahu Kaal)
  if (panchang.rahu_kaal) {
    insights.push({
      type: 'caution',
      icon: '⚠️',
      title: l('Time to Avoid', 'बचने का समय'),
      content: `${panchang.rahu_kaal.start} – ${panchang.rahu_kaal.end}`,
      description: l('Avoid starting new ventures', 'नए काम शुरू न करें'),
      color: 'bg-orange-50 border-orange-200',
      textColor: 'text-orange-700',
    });
  }

  // 4. Special yoga insight
  const specialYoga = panchang.special_yogas?.sarvartha_siddhi || panchang.special_yogas?.amrit_siddhi;
  if (specialYoga && specialYoga.active) {
    insights.push({
      type: 'yoga',
      icon: '🔥',
      title: l('Rare Yoga Active', 'विशेष योग सक्रिय है'),
      content: isHi && specialYoga.name_hindi ? specialYoga.name_hindi : specialYoga.name,
      description: l('Extra favorable for auspicious activities', 'शुभ कार्यों के लिए अतिरिक्त अनुकूल'),
      color: 'bg-purple-50 border-purple-200',
      textColor: 'text-purple-700',
    });
  }

  // 5. Avoid if Ganda Moola
  if (panchang.special_yogas?.ganda_moola?.active) {
    insights.push({
      type: 'caution',
      icon: '⚡',
      title: l('Ganda Moola Alert', 'गंड मूल सावधानी'),
      content: panchang.special_yogas.ganda_moola.nakshatra || 'Active',
      description: l('Postpone major events to another date', 'बड़े कार्यों के लिए दूसरी तारीख चुनें'),
      color: 'bg-red-50 border-red-200',
      textColor: 'text-red-700',
    });
  }

  // Format current time for comparison with tithi end time
  const formatTime = (timeStr: string | undefined) => {
    if (!timeStr) return null;
    const [hours, mins] = timeStr.split(':').map(Number);
    return hours * 60 + mins;
  };

  // Get next transition info
  const currentMins = currentTime.getHours() * 60 + currentTime.getMinutes();
  const tithiEndMins = formatTime(panchang.tithi?.end_time);
  const nakEndMins = formatTime(panchang.nakshatra?.end_time);
  const yogaEndMins = formatTime(panchang.yoga?.end_time);

  const getMinutesUntil = (endMins: number | null) => {
    if (!endMins) return null;
    const diff = endMins - currentMins;
    return diff > 0 ? diff : null;
  };

  const tithiMinsLeft = getMinutesUntil(tithiEndMins);
  const nakMinsLeft = getMinutesUntil(nakEndMins);
  const yogaMinsLeft = getMinutesUntil(yogaEndMins);

  const formatMinsToTime = (mins: number) => {
    const h = Math.floor(mins / 60);
    const m = mins % 60;
    return `${h}h ${m}m`;
  };

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center gap-2">
        <Lightbulb className="w-5 h-5 text-sacred-gold" />
        <Heading as={3} variant={3} className="text-foreground">
          {l("Today's Key Insights", 'आज के मुख्य सूचक')}
        </Heading>
      </div>

      {/* Insights Grid */}
      {insights.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {insights.map((insight, idx) => (
            <Card key={idx} className={`border-l-4 ${insight.color}`}>
              <CardContent className="p-3">
                <div className="flex items-start gap-2">
                  <span className="text-2xl flex-shrink-0">{insight.icon}</span>
                  <div className="min-w-0 flex-1">
                    <p className={`text-sm font-bold ${insight.textColor} leading-tight`}>
                      {insight.title}
                    </p>
                    <p className="text-sm font-semibold text-foreground mt-0.5 line-clamp-2">
                      {insight.content}
                    </p>
                    {insight.description && (
                      <p className="text-xs text-muted-foreground mt-1">
                        {insight.description}
                      </p>
                    )}
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <Card className="bg-card/50">
          <CardContent className="p-4 text-center text-muted-foreground">
            {l('No special insights for today', 'आज के लिए कोई विशेष सूचक नहीं')}
          </CardContent>
        </Card>
      )}

      {/* Transitions Timeline */}
      <Card className="card-sacred border-sacred-gold/30 bg-gradient-to-r from-sacred-gold/5 to-transparent">
        <CardContent className="p-4">
          <div className="flex items-center gap-2 mb-3">
            <Clock className="w-4 h-4 text-sacred-gold" />
            <Heading as={4} variant={4} className="text-foreground">
              {l('Next Transitions', 'अगला परिवर्तन')}
            </Heading>
          </div>

          <div className="space-y-2 text-sm">
            {tithiMinsLeft !== null && (
              <div className="flex items-center justify-between p-2 rounded-lg bg-background/50">
                <span className="text-muted-foreground">
                  {panchang.tithi?.name} {l('ends', 'समाप्त होता है')}
                </span>
                <span className="font-semibold text-foreground">
                  {formatMinsToTime(tithiMinsLeft)}
                </span>
              </div>
            )}
            {nakMinsLeft !== null && (
              <div className="flex items-center justify-between p-2 rounded-lg bg-background/50">
                <span className="text-muted-foreground">
                  {panchang.nakshatra?.name} {l('ends', 'समाप्त होता है')}
                </span>
                <span className="font-semibold text-foreground">
                  {formatMinsToTime(nakMinsLeft)}
                </span>
              </div>
            )}
            {yogaMinsLeft !== null && (
              <div className="flex items-center justify-between p-2 rounded-lg bg-background/50">
                <span className="text-muted-foreground">
                  {panchang.yoga?.name} {l('ends', 'समाप्त होता है')}
                </span>
                <span className="font-semibold text-foreground">
                  {formatMinsToTime(yogaMinsLeft)}
                </span>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* CTA for Personalization */}
      <Card className="bg-gradient-to-r from-sacred-gold/10 to-orange-500/10 border-sacred-gold/30">
        <CardContent className="p-4">
          <div className="flex items-start gap-3">
            <BookOpen className="w-5 h-5 text-sacred-gold flex-shrink-0 mt-0.5" />
            <div className="flex-1">
              <p className="text-sm font-semibold text-foreground mb-2">
                {l('Get Personal Insights', 'अपनी कुंडली के अनुसार सूचक पाएं')}
              </p>
              <p className="text-xs text-muted-foreground mb-3">
                {l('Check how today\'s panchang affects YOUR chart', 'आज का पंचांग आपकी कुंडली को कैसे प्रभावित करता है')}
              </p>
              <Button className="btn-sacred text-xs h-8">
                {l('View Prediction', 'व्यक्तिगत भविष्यवाणी देखें')}
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
