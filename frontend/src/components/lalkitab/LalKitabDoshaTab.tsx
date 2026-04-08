import { useTranslation } from '@/lib/i18n';
import { LalKitabChartData } from './lalkitab-data';
import { AlertTriangle, CheckCircle, Shield } from 'lucide-react';

interface DoshaResult {
  key: string;
  nameEn: string;
  nameHi: string;
  detected: boolean;
  severity: 'high' | 'medium' | 'low';
  descEn: string;
  descHi: string;
  remedyEn: string;
  remedyHi: string;
}

interface Props {
  chartData: LalKitabChartData;
}

const severityStyles: Record<DoshaResult['severity'], string> = {
  high: 'bg-red-500/20 text-red-600',
  medium: 'bg-orange-500/20 text-orange-600',
  low: 'bg-yellow-500/20 text-yellow-700',
};

export default function LalKitabDoshaTab({ chartData }: Props) {
  const { t, language } = useTranslation();
  const isHi = language === 'hi';

  const doshas: DoshaResult[] = chartData.doshas ?? [];
  const detectedDoshas = doshas.filter((d) => d.detected);
  const cleanDoshas = doshas.filter((d) => !d.detected);
  const sortedDoshas = [...detectedDoshas, ...cleanDoshas];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="font-sacred text-2xl text-sacred-gold flex items-center gap-2">
          <Shield className="w-6 h-6" />
          {t('lk.dosha.title')}
        </h2>
        <p className="text-gray-400 mt-1">{t('lk.dosha.desc')}</p>
      </div>

      {/* Summary bar */}
      <div className="rounded-2xl p-5 border border-sacred-gold/20 bg-sacred-gold/5 flex items-center justify-between">
        <span className="font-sacred text-lg text-sacred-gold">
          {t('lk.dosha.detected')}: {detectedDoshas.length} / {doshas.length}
        </span>
        <div className="flex items-center gap-2">
          {detectedDoshas.length > 0 ? (
            <AlertTriangle className="w-5 h-5 text-red-500" />
          ) : (
            <CheckCircle className="w-5 h-5 text-green-500" />
          )}
        </div>
      </div>

      {/* Dosha cards */}
      <div className="space-y-4">
        {sortedDoshas.map((dosha) => {
          const name = isHi ? dosha.nameHi : dosha.nameEn;
          const desc = isHi ? dosha.descHi : dosha.descEn;
          const remedy = isHi ? dosha.remedyHi : dosha.remedyEn;

          return (
            <div
              key={dosha.key}
              className={`rounded-2xl p-5 border transition-all ${
                dosha.detected
                  ? 'border-red-500/30 bg-red-500/5'
                  : 'border-green-500/30 bg-green-500/5'
              }`}
            >
              {/* Card header */}
              <div className="flex items-center justify-between">
                <h3 className="font-sacred text-lg text-white">{name}</h3>
                {dosha.detected ? (
                  <span className="flex items-center gap-1.5 text-red-500 text-sm font-medium">
                    <AlertTriangle className="w-4 h-4" />
                    {t('lk.dosha.detected')}
                  </span>
                ) : (
                  <span className="flex items-center gap-1.5 text-green-500 text-sm font-medium">
                    <CheckCircle className="w-4 h-4" />
                    {t('lk.dosha.notDetected')}
                  </span>
                )}
              </div>

              {/* Detected details */}
              {dosha.detected && (
                <div className="mt-3 space-y-3">
                  {/* Severity badge */}
                  <div className="flex items-center gap-2">
                    <span className="text-sm text-gray-400">
                      {t('lk.dosha.severity')}:
                    </span>
                    <span
                      className={`text-xs font-semibold px-2.5 py-0.5 rounded-full ${severityStyles[dosha.severity]}`}
                    >
                      {dosha.severity === 'high'
                        ? t('lk.dosha.high')
                        : dosha.severity === 'medium'
                          ? t('lk.dosha.medium')
                          : t('lk.dosha.low')}
                    </span>
                  </div>

                  {/* Description */}
                  <p className="text-sm text-gray-300">{desc}</p>

                  {/* Remedy box */}
                  <div className="bg-sacred-gold/5 border border-sacred-gold/20 rounded-xl p-4 mt-3">
                    <p className="text-sm text-sacred-gold font-medium">{remedy}</p>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
