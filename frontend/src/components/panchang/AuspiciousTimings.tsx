import { Sparkles } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { useTranslation } from '@/lib/i18n';
import { translateBackend } from '@/lib/backend-translations';

interface TimePeriod {
  start: string;
  end: string;
}

interface ChoghadiyaPeriod {
  name: string;
  quality: string;
  start: string;
  end: string;
}

interface AuspiciousTimingsProps {
  abhijit_muhurat: TimePeriod;
  brahma_muhurat: TimePeriod;
  choghadiya: ChoghadiyaPeriod[];
  ravi_yoga?: TimePeriod | null;
  vijaya_muhurta?: TimePeriod | null;
  godhuli_muhurta?: TimePeriod | null;
  sayahna_sandhya?: TimePeriod | null;
  nishita_muhurta?: TimePeriod | null;
  pratah_sandhya?: TimePeriod | null;
}

function qualityClasses(quality: string) {
  switch (quality) {
    case "Best":
      return {
        badge: "bg-green-100 text-green-800 border border-green-300",
        row: "bg-green-50",
      };
    case "Good":
      return {
        badge: "bg-green-100 text-green-700 border border-green-200",
        row: "bg-green-50/50",
      };
    case "Neutral":
      return {
        badge: "bg-amber-100 text-amber-800 border border-amber-300",
        row: "bg-amber-50",
      };
    case "Inauspicious":
      return {
        badge: "bg-red-100 text-red-700 border border-red-300",
        row: "bg-red-50",
      };
    default:
      return {
        badge: "bg-gray-100 text-gray-600 border border-gray-200",
        row: "bg-gray-50",
      };
  }
}

function qualityLabel(quality: string, language: string): string {
  if (language !== 'hi') return quality;
  if (quality === 'Best') return 'श्रेष्ठ';
  if (quality === 'Good') return 'अच्छा';
  if (quality === 'Neutral') return 'सामान्य';
  if (quality === 'Inauspicious') return 'अशुभ';
  return quality;
}

function MuhuratCard({
  title,
  period,
}: {
  title: string;
  period: TimePeriod;
}) {
  return (
    <div className="flex flex-row gap-4 p-4 rounded-xl bg-green-50 border border-green-200">
      <div className="w-10 h-10 rounded-xl flex items-center justify-center bg-green-100">
        <Sparkles className="h-5 w-5 text-green-700" />
      </div>
      <div className="flex flex-col justify-center">
        <span className="text-sm text-green-700 font-medium">{title}</span>
        <span className="text-gray-800 font-semibold">
          {period.start} &ndash; {period.end}
        </span>
      </div>
    </div>
  );
}

export default function AuspiciousTimings({
  abhijit_muhurat, brahma_muhurat, choghadiya,
  ravi_yoga, vijaya_muhurta, godhuli_muhurta,
  sayahna_sandhya, nishita_muhurta, pratah_sandhya,
}: AuspiciousTimingsProps) {
  const { language } = useTranslation();
  return (
    <Card className="bg-white border-sacred-gold/20">
      <CardContent>
        <div className="flex items-center gap-2 mb-4">
          <Sparkles className="h-5 w-5 text-green-700" />
          <h3 className="text-lg font-semibold text-gray-800">
            {language === 'hi' ? 'शुभ समय' : 'Auspicious Timings'}
          </h3>
        </div>

        {/* Muhurat highlight cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-6">
          <MuhuratCard title={language === 'hi' ? 'अभिजीत मुहूर्त' : 'Abhijit Muhurat'} period={abhijit_muhurat} />
          <MuhuratCard title={language === 'hi' ? 'ब्रह्म मुहूर्त' : 'Brahma Muhurat'} period={brahma_muhurat} />
          {ravi_yoga && <MuhuratCard title={language === 'hi' ? 'रवि योग' : 'Ravi Yoga'} period={ravi_yoga} />}
          {vijaya_muhurta && <MuhuratCard title={language === 'hi' ? 'विजय मुहूर्त' : 'Vijaya Muhurta'} period={vijaya_muhurta} />}
          {godhuli_muhurta && <MuhuratCard title={language === 'hi' ? 'गोधूलि मुहूर्त' : 'Godhuli Muhurta'} period={godhuli_muhurta} />}
          {sayahna_sandhya && <MuhuratCard title={language === 'hi' ? 'सायाह्न संध्या' : 'Sayahna Sandhya'} period={sayahna_sandhya} />}
          {nishita_muhurta && <MuhuratCard title={language === 'hi' ? 'निशीथ मुहूर्त' : 'Nishita Muhurta'} period={nishita_muhurta} />}
          {pratah_sandhya && <MuhuratCard title={language === 'hi' ? 'प्रातः संध्या' : 'Pratah Sandhya'} period={pratah_sandhya} />}
        </div>

        {/* Choghadiya periods */}
        <div className="flex flex-col gap-2">
          <span className="text-sm text-cosmic-text-secondary mb-1">
            {language === 'hi' ? 'चौघड़िया' : 'Choghadiya'}
          </span>
          {choghadiya.map((period, index) => {
            const classes = qualityClasses(period.quality);
            return (
              <div
                key={`${period.name}-${index}`}
                className={`flex items-center justify-between p-3 rounded-xl ${classes.row}`}
              >
                <div className="flex flex-col">
                  <span className="text-gray-800 font-medium">
                    {translateBackend(period.name, language)}
                  </span>
                  <span className="text-sm text-gray-600">
                    {period.start} &ndash; {period.end}
                  </span>
                </div>
                <span
                  className={`text-sm px-2 py-0.5 rounded-full ${classes.badge}`}
                >
                  {qualityLabel(period.quality, language)}
                </span>
              </div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}
