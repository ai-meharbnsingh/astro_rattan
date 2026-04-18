import { Card } from '@/components/ui/card';
import { AlertCircle, CheckCircle, Zap, Clock } from 'lucide-react';
import type { FullPanchangData } from '@/sections/Panchang';

interface Props {
  panchang: FullPanchangData | null;
  language: string;
  t: (key: string) => string;
  currentTime: Date;
}

export default function TodaysKeyInsights({ panchang, language, t, currentTime }: Props) {
  if (!panchang) return null;

  const isHi = language === 'hi';
  const l = (en: string, hi: string) => isHi ? hi : en;

  // Get best muhurat
  const bestMuhurat = panchang.abhijit_muhurat || panchang.brahma_muhurat || panchang.vijaya_muhurta;

  // Check if Rahu Kaal is active
  const currentMins = currentTime.getHours() * 60 + currentTime.getMinutes();
  const formatTime = (timeStr: string | undefined) => {
    if (!timeStr) return null;
    const [hours, mins] = timeStr.split(':').map(Number);
    return hours * 60 + mins;
  };

  const rahuStartMins = formatTime(panchang.rahu_kaal?.start);
  const rahuEndMins = formatTime(panchang.rahu_kaal?.end);
  const isRahuActive = rahuStartMins !== null && rahuEndMins !== null &&
    currentMins >= rahuStartMins && currentMins < rahuEndMins;

  // Get main festival if any
  const mainFestival = panchang.festivals?.[0];

  // Get special yoga highlight
  const specialYoga = panchang.special_yogas?.sarvartha_siddhi?.active
    ? panchang.special_yogas.sarvartha_siddhi
    : panchang.special_yogas?.amrit_siddhi?.active
    ? panchang.special_yogas.amrit_siddhi
    : null;

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
      {/* Best Muhurat Card */}
      {bestMuhurat && (
        <Card className="rounded-lg overflow-hidden shadow-sm border-0">
          <div className="bg-gradient-to-r from-green-600 to-green-700 px-3 py-2 text-white">
            <h3 className="text-xs font-bold uppercase tracking-wide">
              {l('Best Time Today', 'आज का सर्वश्रेष्ठ')}
            </h3>
          </div>
          <div className="bg-green-50 px-3 py-3 min-h-[80px] flex flex-col justify-center">
            <div className="flex items-center gap-2 mb-2">
              <CheckCircle className="w-4 h-4 text-green-600 flex-shrink-0" />
              <span className="text-xs font-medium text-green-700">{l('Muhurat', 'मुहूर्त')}</span>
            </div>
            <p className="text-lg font-bold text-green-900">
              {bestMuhurat.start}
            </p>
            <p className="text-xs text-green-700 mt-1">
              {l('to', 'से')} {bestMuhurat.end}
            </p>
          </div>
        </Card>
      )}

      {/* Rahu Kaal / Time to Avoid */}
      {panchang.rahu_kaal && (
        <Card className={`rounded-lg overflow-hidden shadow-sm border-0 ${isRahuActive ? 'ring-2 ring-red-500' : ''}`}>
          <div className={`px-3 py-2 text-white ${isRahuActive ? 'bg-gradient-to-r from-red-600 to-red-700' : 'bg-gradient-to-r from-orange-600 to-orange-700'}`}>
            <h3 className="text-xs font-bold uppercase tracking-wide">
              {l('Avoid Time', 'बचने का समय')}
            </h3>
          </div>
          <div className={`px-3 py-3 min-h-[80px] flex flex-col justify-center ${isRahuActive ? 'bg-red-50' : 'bg-orange-50'}`}>
            <div className="flex items-center gap-2 mb-2">
              <AlertCircle className={`w-4 h-4 flex-shrink-0 ${isRahuActive ? 'text-red-600' : 'text-orange-600'}`} />
              <span className={`text-xs font-medium ${isRahuActive ? 'text-red-700' : 'text-orange-700'}`}>
                {t('auto.rahuKaal')}
              </span>
            </div>
            <p className={`text-lg font-bold ${isRahuActive ? 'text-red-900' : 'text-orange-900'}`}>
              {panchang.rahu_kaal.start}
            </p>
            <p className={`text-xs mt-1 ${isRahuActive ? 'text-red-700' : 'text-orange-700'}`}>
              {l('to', 'से')} {panchang.rahu_kaal.end}
            </p>
            {isRahuActive && (
              <p className="text-xs font-bold text-red-600 mt-2 flex items-center gap-1">
                <span className="relative flex h-1.5 w-1.5">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-500 opacity-75" />
                  <span className="relative inline-flex h-1.5 w-1.5 rounded-full bg-red-600" />
                </span>
                {l('ACTIVE NOW', 'अभी सक्रिय')}
              </p>
            )}
          </div>
        </Card>
      )}

      {/* Festival / Special Yoga */}
      {(mainFestival || specialYoga) && (
        <Card className="rounded-lg overflow-hidden shadow-sm border-0">
          <div className={`px-3 py-2 text-white bg-gradient-to-r ${
            mainFestival ? 'from-red-600 to-red-700' : 'from-purple-600 to-purple-700'
          }`}>
            <h3 className="text-xs font-bold uppercase tracking-wide">
              {mainFestival ? l('Festival Today', 'आज पर्व है') : l('Special Yoga', 'विशेष योग')}
            </h3>
          </div>
          <div className={`px-3 py-3 min-h-[80px] flex flex-col justify-center ${
            mainFestival ? 'bg-red-50' : 'bg-purple-50'
          }`}>
            {mainFestival && (
              <>
                <p className="text-sm font-bold text-red-900 leading-tight">
                  {isHi && mainFestival.name_hindi ? mainFestival.name_hindi : mainFestival.name}
                </p>
                {mainFestival.description && (
                  <p className="text-xs text-red-700 mt-2 line-clamp-2">
                    {mainFestival.description}
                  </p>
                )}
              </>
            )}
            {specialYoga && (
              <>
                <div className="flex items-start gap-2 mb-2">
                  <Zap className="w-4 h-4 text-purple-600 flex-shrink-0 mt-0.5" />
                </div>
                <p className="text-sm font-bold text-purple-900 leading-tight">
                  {isHi && specialYoga.name_hindi ? specialYoga.name_hindi : specialYoga.name}
                </p>
                <p className="text-xs text-purple-700 mt-2">
                  {l('Do not miss this opportunity!', 'इस मौके को न छोड़ें!')}
                </p>
              </>
            )}
          </div>
        </Card>
      )}

      {/* Quick Tip / Do's */}
      {(() => {
        const tithi = panchang.tithi?.name?.toLowerCase() || '';
        const tips: string[] = [];

        if (tithi.includes('ekadashi')) {
          tips.push(l('Fasting Day', 'व्रत का दिन'));
        } else if (tithi.includes('pradosh')) {
          tips.push(l('Shiva Worship', 'शिव पूजा'));
        } else if (tithi.includes('chaturthi')) {
          tips.push(l('Ganesha Worship', 'गणेश पूजा'));
        } else if (tithi.includes('purnima') || tithi.includes('amavasya')) {
          tips.push(l('Ancestor Worship', 'पितृ पूजन'));
        }

        if (panchang.special_yogas?.ganda_moola?.active) {
          tips.push(l('Avoid Major Events', 'बड़े काम न करें'));
        }

        if (tips.length === 0) {
          tips.push(l('Good for Regular Work', 'सामान्य कार्यों के लिए अच्छा'));
        }

        return (
          <Card className="rounded-lg overflow-hidden shadow-sm border-0">
            <div className="bg-gradient-to-r from-blue-600 to-blue-700 px-3 py-2 text-white">
              <h3 className="text-xs font-bold uppercase tracking-wide">
                {l("Today's Tip", 'आज की सलाह')}
              </h3>
            </div>
            <div className="bg-blue-50 px-3 py-3 min-h-[80px] flex flex-col justify-center">
              <div className="space-y-1">
                {tips.map((tip, idx) => (
                  <div key={idx} className="flex items-start gap-2">
                    <span className="text-xs text-blue-600 font-bold mt-0.5">✓</span>
                    <p className="text-xs font-medium text-blue-900">{tip}</p>
                  </div>
                ))}
              </div>
            </div>
          </Card>
        );
      })()}
    </div>
  );
}
