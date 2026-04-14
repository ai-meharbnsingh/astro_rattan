import { Sunrise, Sunset, Moon } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { useTranslation } from '@/lib/i18n';

interface SunMoonTimesProps {
  sunrise: string;
  sunset: string;
  moonrise: string;
  moonset: string;
}

const timeItems = [
  {
    key: "sunrise",
    label: "Sunrise",
    icon: Sunrise,
    iconWrapperClass: "bg-sacred-gold/10",
    iconClass: "text-sacred-gold",
  },
  {
    key: "sunset",
    label: "Sunset",
    icon: Sunset,
    iconWrapperClass: "bg-sacred-saffron/10",
    iconClass: "text-sacred-saffron",
  },
  {
    key: "moonrise",
    label: "Moonrise",
    icon: Moon,
    iconWrapperClass: "bg-indigo-500/10",
    iconClass: "text-indigo-400",
  },
  {
    key: "moonset",
    label: "Moonset",
    icon: Moon,
    iconWrapperClass: "bg-indigo-500/10",
    iconClass: "text-indigo-400",
  },
] as const;

export default function SunMoonTimes({
  sunrise,
  sunset,
  moonrise,
  moonset,
}: SunMoonTimesProps) {
  const { language } = useTranslation();
  const values: Record<string, string> = {
    sunrise,
    sunset,
    moonrise,
    moonset,
  };

  return (
    <Card className="bg-cosmic-card border-sacred-gold/10">
      <CardContent>
        <div className="flex items-center gap-2 mb-4">
          <Sunrise className="h-5 w-5 text-sacred-gold" />
          <h3 className="text-lg font-semibold text-cosmic-text">
            {t('auto.sunMoon')}
          </h3>
        </div>

        <div className="grid grid-cols-2 gap-4">
          {timeItems.map((item) => {
            const Icon = item.icon;
            return (
              <div
                key={item.key}
                className="flex flex-row gap-4 p-4 rounded-xl bg-cosmic-card border border-sacred-gold/10"
              >
                <div
                  className={`w-10 h-10 rounded-xl flex items-center justify-center ${item.iconWrapperClass}`}
                >
                  <Icon className={`h-5 w-5 ${item.iconClass}`} />
                </div>
                <div className="flex flex-col justify-center">
                  <span className="text-sm text-cosmic-text-secondary">
                    {language === 'hi'
                      ? item.key === 'sunrise'
                        ? 'सूर्योदय'
                        : item.key === 'sunset'
                          ? 'सूर्यास्त'
                          : item.key === 'moonrise'
                            ? 'चंद्रोदय'
                            : 'चंद्रास्त'
                      : item.label}
                  </span>
                  <span className="text-cosmic-text font-medium">
                    {values[item.key]}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}
