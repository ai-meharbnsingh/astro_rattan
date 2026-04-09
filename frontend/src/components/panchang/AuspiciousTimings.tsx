import { Sparkles } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";

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
    case "Good":
      return {
        badge: "bg-green-500/20 text-green-400 border border-green-500/30",
        row: "bg-green-900/10",
      };
    case "Neutral":
      return {
        badge: "bg-amber-500/20 text-amber-400 border border-amber-500/30",
        row: "bg-amber-900/10",
      };
    case "Inauspicious":
      return {
        badge: "bg-red-500/20 text-red-400 border border-red-500/30",
        row: "bg-red-900/10",
      };
    default:
      return {
        badge: "bg-cosmic-card text-cosmic-text-secondary border border-sacred-gold/10",
        row: "bg-cosmic-card",
      };
  }
}

function MuhuratCard({
  title,
  period,
}: {
  title: string;
  period: TimePeriod;
}) {
  return (
    <div className="flex flex-row gap-4 p-4 rounded-xl bg-green-900/10 border border-green-500/20">
      <div className="w-10 h-10 rounded-xl flex items-center justify-center bg-green-500/10">
        <Sparkles className="h-5 w-5 text-green-400" />
      </div>
      <div className="flex flex-col justify-center">
        <span className="text-sm text-green-400 font-medium">{title}</span>
        <span className="text-cosmic-text font-semibold">
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
  return (
    <Card className="bg-cosmic-card border-sacred-gold/10">
      <CardContent>
        <div className="flex items-center gap-2 mb-4">
          <Sparkles className="h-5 w-5 text-green-400" />
          <h3 className="text-lg font-semibold text-cosmic-text">
            Auspicious Timings
          </h3>
        </div>

        {/* Muhurat highlight cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-6">
          <MuhuratCard title="Abhijit Muhurat" period={abhijit_muhurat} />
          <MuhuratCard title="Brahma Muhurat" period={brahma_muhurat} />
          {ravi_yoga && <MuhuratCard title="Ravi Yoga" period={ravi_yoga} />}
          {vijaya_muhurta && <MuhuratCard title="Vijaya Muhurta" period={vijaya_muhurta} />}
          {godhuli_muhurta && <MuhuratCard title="Godhuli Muhurta" period={godhuli_muhurta} />}
          {sayahna_sandhya && <MuhuratCard title="Sayahna Sandhya" period={sayahna_sandhya} />}
          {nishita_muhurta && <MuhuratCard title="Nishita Muhurta" period={nishita_muhurta} />}
          {pratah_sandhya && <MuhuratCard title="Pratah Sandhya" period={pratah_sandhya} />}
        </div>

        {/* Choghadiya periods */}
        <div className="flex flex-col gap-2">
          <span className="text-sm text-cosmic-text-secondary mb-1">
            Choghadiya
          </span>
          {choghadiya.map((period, index) => {
            const classes = qualityClasses(period.quality);
            return (
              <div
                key={`${period.name}-${index}`}
                className={`flex items-center justify-between p-3 rounded-xl ${classes.row}`}
              >
                <div className="flex flex-col">
                  <span className="text-cosmic-text font-medium">
                    {period.name}
                  </span>
                  <span className="text-xs text-cosmic-text-secondary">
                    {period.start} &ndash; {period.end}
                  </span>
                </div>
                <span
                  className={`text-xs px-2 py-0.5 rounded-full ${classes.badge}`}
                >
                  {period.quality}
                </span>
              </div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}
