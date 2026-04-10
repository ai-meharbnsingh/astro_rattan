import { ShieldAlert, AlertTriangle } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";

interface TimePeriod {
  start: string;
  end: string;
}

interface InauspiciousPeriodsProps {
  rahu_kaal: TimePeriod;
  gulika_kaal: TimePeriod;
  yamaganda: TimePeriod;
  dur_muhurtam?: TimePeriod | null;
  varjyam?: TimePeriod | null;
}

const periods = [
  { key: "rahu_kaal" as const, label: "Rahu Kalam", icon: ShieldAlert },
  { key: "gulika_kaal" as const, label: "Gulikai Kalam", icon: AlertTriangle },
  { key: "yamaganda" as const, label: "Yamaganda", icon: AlertTriangle },
  { key: "dur_muhurtam" as const, label: "Dur Muhurtam", icon: AlertTriangle },
  { key: "varjyam" as const, label: "Varjyam", icon: AlertTriangle },
];

export default function InauspiciousPeriods({
  rahu_kaal, gulika_kaal, yamaganda, dur_muhurtam, varjyam,
}: InauspiciousPeriodsProps) {
  const values: Record<string, TimePeriod | null | undefined> = {
    rahu_kaal, gulika_kaal, yamaganda, dur_muhurtam, varjyam,
  };

  return (
    <Card className="card-sacred border-sacred-gold/20">
      <CardContent>
        <div className="flex items-center gap-2 mb-4">
          <ShieldAlert className="h-5 w-5 text-red-400" />
          <h3 className="text-lg font-semibold text-cosmic-text">
            Inauspicious Periods
          </h3>
        </div>

        <div className="flex flex-col gap-3">
          {periods.map((period) => {
            const Icon = period.icon;
            const time = values[period.key];
            if (!time) return null;
            return (
              <div
                key={period.key}
                className="flex items-center justify-between p-3 rounded-xl bg-red-900/10 border border-red-300/20"
              >
                <div className="flex items-center gap-3">
                  <Icon className="h-4 w-4 text-red-400 shrink-0" />
                  <div>
                    <span className="text-red-400 font-medium text-sm">
                      {period.label}
                    </span>
                  </div>
                </div>
                <span className="text-cosmic-text-secondary text-sm whitespace-nowrap">
                  {time.start} – {time.end}
                </span>
              </div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}
