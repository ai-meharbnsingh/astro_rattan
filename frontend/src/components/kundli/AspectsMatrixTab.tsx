import { Loader2 } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';
import { translatePlanet } from '@/lib/backend-translations';

interface AspectsMatrixTabProps {
  data: any;
  loading: boolean;
}

// Color mapping by aspect type
const ASPECT_COLORS: Record<string, { bg: string; text: string }> = {
  conj: { bg: '#dbeafe', text: '#1e40af' },   // blue
  sext: { bg: '#d1fae5', text: '#065f46' },   // green
  squr: { bg: '#fee2e2', text: '#991b1b' },   // red
  trin: { bg: '#d1fae5', text: '#065f46' },   // green
  oppo: { bg: '#fee2e2', text: '#991b1b' },   // red
  ssqr: { bg: '#ffedd5', text: '#9a3412' },   // orange
  sesq: { bg: '#ffedd5', text: '#9a3412' },   // orange
  ququ: { bg: '#ede9fe', text: '#5b21b6' },   // purple
};

const PLANET_ABBR: Record<string, string> = {
  Sun: 'Ravi', Moon: 'Chan', Mars: 'Mang', Mercury: 'Budh',
  Jupiter: 'Guru', Venus: 'Sukr', Saturn: 'Sani',
  Rahu: 'Rahu', Ketu: 'Ketu',
};

export default function AspectsMatrixTab({ data, loading }: AspectsMatrixTabProps) {
  const { t, language } = useTranslation();

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-6 h-6 animate-spin text-sacred-gold" />
        <span className="ml-2 text-sacred-text-secondary">{t('common.loading')}</span>
      </div>
    );
  }

  if (!data?.matrix) {
    return <p className="text-center text-sacred-text-secondary py-8">{t('common.noData')}</p>;
  }

  const planets = data.planet_order || Object.keys(data.matrix);

  return (
    <div className="space-y-6">
      {/* Matrix Grid */}
      <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
        <h4 className="font-display font-semibold text-sacred-brown mb-3">
          {language === 'hi' ? 'ग्रहों के पारस्परिक दृष्टि' : 'Aspects on Planets'}
        </h4>
        <div className="overflow-x-auto">
          <table className="w-full text-data border-collapse" style={{ minWidth: '600px' }}>
            <thead>
              <tr>
                <th className="p-1.5 text-left font-semibold border border-slate-200 bg-slate-100 sticky left-0 z-10" style={{ minWidth: '60px' }}>
                  -
                </th>
                {planets.map((p: string) => (
                  <th key={p} className="p-1.5 text-center font-semibold border border-slate-200 bg-slate-100" style={{ minWidth: '55px' }}>
                    {PLANET_ABBR[p] || translatePlanet(p, language).slice(0, 4)}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {planets.map((p1: string, rowIdx: number) => (
                <tr key={p1}>
                  <td className="p-1.5 font-semibold border border-slate-200 bg-slate-50 sticky left-0 z-10">
                    {PLANET_ABBR[p1] || translatePlanet(p1, language).slice(0, 4)}
                  </td>
                  {planets.map((p2: string, colIdx: number) => {
                    if (p1 === p2) {
                      return (
                        <td key={p2} className="p-1 text-center border border-slate-200 bg-slate-100 text-slate-400">
                          —
                        </td>
                      );
                    }
                    const cell = data.matrix[p1]?.[p2];
                    if (!cell) return <td key={p2} className="p-1 border border-slate-200" />;

                    const colors = cell.aspect ? ASPECT_COLORS[cell.aspect] : null;

                    return (
                      <td
                        key={p2}
                        className="p-1 text-center border border-slate-200"
                        style={colors ? { backgroundColor: colors.bg, color: colors.text } : undefined}
                        title={cell.aspect_name ? `${cell.aspect_name} (orb: ${cell.orb}°)` : `${cell.degree}°`}
                      >
                        <div className="font-mono font-semibold">{cell.degree}</div>
                        {cell.aspect && (
                          <div className="text-micro font-medium">{cell.aspect}</div>
                        )}
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Legend */}
        <div className="flex flex-wrap gap-3 mt-3 text-xs text-cosmic-text-secondary">
          {[
            { abbr: 'conj', label: 'Conjunction (0°)' },
            { abbr: 'sext', label: 'Sextile (60°)' },
            { abbr: 'squr', label: 'Square (90°)' },
            { abbr: 'trin', label: 'Trine (120°)' },
            { abbr: 'oppo', label: 'Opposition (180°)' },
            { abbr: 'ssqr', label: 'Semi-Square (45°)' },
            { abbr: 'sesq', label: 'Sesquiquadrate (135°)' },
            { abbr: 'ququ', label: 'Quintile (72°)' },
          ].map(({ abbr, label }) => (
            <span key={abbr} className="flex items-center gap-1">
              <span
                className="w-4 h-3 rounded text-micro font-mono font-bold flex items-center justify-center"
                style={{ backgroundColor: ASPECT_COLORS[abbr].bg, color: ASPECT_COLORS[abbr].text }}
              >
                {abbr}
              </span>
              {label}
            </span>
          ))}
        </div>
      </div>

      {/* Active Aspects List */}
      {data.aspects_list && data.aspects_list.length > 0 && (
        <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4">
          <h4 className="font-display font-semibold text-sacred-brown mb-3">
            {language === 'hi' ? 'सक्रिय दृष्टियां' : 'Active Aspects'}
          </h4>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
            {data.aspects_list.map((asp: any, i: number) => {
              const colors = ASPECT_COLORS[asp.aspect] || { bg: '#f1f5f9', text: '#334155' };
              return (
                <div
                  key={i}
                  className="flex items-center justify-between rounded-lg px-3 py-2 border"
                  style={{ backgroundColor: colors.bg, borderColor: colors.text + '30', color: colors.text }}
                >
                  <span className="font-semibold text-sm">
                    {translatePlanet(asp.planet1, language)} — {translatePlanet(asp.planet2, language)}
                  </span>
                  <span className="text-xs font-mono">
                    {asp.aspect_name} ({asp.degree}° orb:{asp.orb}°)
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
