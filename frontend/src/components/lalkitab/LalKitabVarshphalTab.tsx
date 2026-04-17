import { useState, useMemo } from 'react';
import { useTranslation } from '@/lib/i18n';
import { Calendar } from 'lucide-react';
import type { LalKitabChartData } from './lalkitab-data';

interface Props {
  chartData: LalKitabChartData;
  birthDate: string;
  apiResult?: any;
}

/** Build the current year and +/- 5 years range. */
function getYearRange(): number[] {
  const current = new Date().getFullYear();
  const years: number[] = [];
  for (let y = current - 5; y <= current + 5; y++) {
    years.push(y);
  }
  return years;
}

export default function LalKitabVarshphalTab(_props: Props) {
  const { t, language } = useTranslation();

  const currentYear = new Date().getFullYear();
  const [selectedYear, setSelectedYear] = useState<number>(currentYear);
  const yearRange = useMemo(() => getYearRange(), []);

  // Real Varshapravesh (annual chart) requires ephemeris calculation for the
  // birthday date in the selected year. The previous implementation fabricated
  // results by shifting birth-chart houses by (year-birthYear) % 12 — a made-up
  // algorithm with no astrological basis. That has been removed.
  // TODO: call backend ephemeris for true Varshapravesh chart.
  const isVarshphalStub = true;

  return (
    <div className="space-y-8">
      {/* ─── Header ─── */}
      <div className="text-center space-y-2">
        <h2 className="text-2xl font-sans font-bold text-sacred-gold flex items-center justify-center gap-2">
          <Calendar className="w-6 h-6" />
          {t('lk.varshphal.title')}
        </h2>
        <p className="text-sm text-gray-600">{t('lk.varshphal.desc')}</p>
      </div>

      {/* ─── Year Selector (kept for future use) ─── */}
      <div className="flex items-center justify-center gap-3">
        <label className="text-sm font-medium text-sacred-gold">
          {t('lk.varshphal.selectYear')}
        </label>
        <select
          value={selectedYear}
          onChange={(e) => setSelectedYear(Number(e.target.value))}
          className="rounded-xl bg-card border border-sacred-gold/20 text-foreground px-4 py-3 focus:outline-none focus:border-sacred-gold/50 transition-colors"
          disabled={isVarshphalStub}
        >
          {yearRange.map((y) => (
            <option key={y} value={y}>
              {y}
            </option>
          ))}
        </select>
      </div>

      {isVarshphalStub ? (
        <div className="p-8 text-center border border-amber-200 bg-amber-50 rounded-xl">
          <h3 className="text-lg font-semibold text-amber-900 mb-2">
            {t('lk.varshphal.comingSoon')}
          </h3>
          <p className="text-sm text-amber-700">
            {language === 'hi'
              ? 'वास्तविक वर्षप्रवेश गणना के लिए ग्रह स्थितियों का पुनर्गणन आवश्यक है। यह सुविधा जल्द ही उपलब्ध होगी।'
              : 'Real Varshapravesh requires recomputing planetary positions for the anniversary date. This feature is under development.'}
          </p>
        </div>
      ) : null}
    </div>
  );
}
