import { Loader2 } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';
import { translatePlanet, translateBackend } from '@/lib/backend-translations';

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
const ASPECT_ABBR_HI: Record<string, string> = {
  conj: 'यु',
  sext: 'षड',
  squr: 'चतु',
  trin: 'त्रि',
  oppo: 'सप्त',
  ssqr: 'अर्ध',
  sesq: 'पौने',
  ququ: 'पंच',
};

const PLANET_ABBR_EN: Record<string, string> = {
  Sun: 'Ravi', Moon: 'Chan', Mars: 'Mang', Mercury: 'Budh',
  Jupiter: 'Guru', Venus: 'Sukr', Saturn: 'Sani',
  Rahu: 'Rahu', Ketu: 'Ketu',
};

const PLANET_ABBR_HI: Record<string, string> = {
  Sun: 'सूर्य', Moon: 'चंद्र', Mars: 'मंगल', Mercury: 'बुध',
  Jupiter: 'गुरु', Venus: 'शुक्र', Saturn: 'शनि',
  Rahu: 'राहु', Ketu: 'केतु',
};

export default function AspectsMatrixTab({ data, loading }: AspectsMatrixTabProps) {
  const { t, language } = useTranslation();
  const PLANET_ABBR = language === 'hi' ? PLANET_ABBR_HI : PLANET_ABBR_EN;

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-6 h-6 animate-spin text-sacred-gold" />
        <span className="ml-2 text-cosmic-text">{t('common.loading')}</span>
      </div>
    );
  }

  if (!data?.matrix) {
    return <p className="text-center text-cosmic-text py-8">{t('common.noData')}</p>;
  }

  const planets = data.planet_order || Object.keys(data.matrix);

  return (
    <div className="space-y-6">
      {/* Matrix Grid */}
      <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-4">
        <h4 className="font-display font-semibold text-sacred-brown mb-3">
          {t('auto.aspectsOnPlanets')}
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
                    {PLANET_ABBR[p] || (translatePlanet(p, language) || p || '').slice(0, 4)}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {planets.map((p1: string, rowIdx: number) => (
                <tr key={p1}>
                  <td className="p-1.5 font-semibold border border-slate-200 bg-slate-50 sticky left-0 z-10">
                    {PLANET_ABBR[p1] || (translatePlanet(p1, language) || p1 || '').slice(0, 4)}
                  </td>
                  {planets.map((p2: string, colIdx: number) => {
                    // Triangle format: only show upper-right half (colIdx > rowIdx)
                    if (colIdx <= rowIdx) {
                      return (
                        <td key={p2} className="p-1 border border-slate-200 bg-slate-50" />
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
                        title={cell.aspect_name ? `${translateBackend(cell.aspect_name, language)} (orb: ${cell.orb}°)` : `${cell.degree}°`}
                      >
                        <div className="font-mono font-semibold">{cell.degree}</div>
                        {cell.aspect && (
                          <div className="text-micro font-medium">{language === 'hi' ? (ASPECT_ABBR_HI[cell.aspect] || cell.aspect) : cell.aspect}</div>
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
        <div className="flex flex-wrap gap-4 mt-4 text-sm text-cosmic-text">
          {[
            { abbr: 'conj', label: t('auto.conjunction0') },
            { abbr: 'sext', label: t('auto.sextile60') },
            { abbr: 'squr', label: t('auto.square90') },
            { abbr: 'trin', label: t('auto.trine120') },
            { abbr: 'oppo', label: t('auto.opposition180') },
            { abbr: 'ssqr', label: t('auto.semiSquare45') },
            { abbr: 'sesq', label: t('auto.sesquiquadrate135') },
            { abbr: 'ququ', label: t('auto.quintile72') },
          ].map(({ abbr, label }) => (
            <span key={abbr} className="flex items-center gap-1.5">
              <span
                className="px-1.5 py-0.5 rounded text-sm font-mono font-bold"
                style={{ backgroundColor: ASPECT_COLORS[abbr].bg, color: ASPECT_COLORS[abbr].text }}
              >
                {abbr}
              </span>
              {label}
            </span>
          ))}
        </div>
      </div>

      {/* Aspects on Cusps (Nirayana) */}
      {data.cusp_aspects?.nirayana && (
        <CuspAspectGrid
          title={t('auto.aspectsOnCuspsNiraya')}
          cuspData={data.cusp_aspects.nirayana}
          planetOrder={data.cusp_aspects.planet_order || data.planet_order}
          language={language}
          t={t}
        />
      )}

      {/* Aspects on Cusps (Sayana) */}
      {data.cusp_aspects?.sayana && (
        <CuspAspectGrid
          title={t('auto.aspectsOnCuspsSayana')}
          cuspData={data.cusp_aspects.sayana}
          planetOrder={data.cusp_aspects.planet_order || data.planet_order}
          language={language}
          t={t}
        />
      )}

      {/* Active Aspects List */}
      {data.aspects_list && data.aspects_list.length > 0 && (
        <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-4">
          <h4 className="font-display font-semibold text-sacred-brown mb-3">
            {t('auto.activeAspects')}
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
                  <span className="text-sm font-mono">
                    {translateBackend(asp.aspect_name, language)} ({asp.degree}° {t('auto.orb')}:{asp.orb}°)
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


/* ── Reusable sub-component for cusp aspect grids ────────── */

interface CuspAspectGridProps {
  title: string;
  cuspData: Record<string, Array<{ cusp: number; degree: number; aspect: string | null; aspect_name: string | null; orb: number }>>;
  planetOrder: string[];
  language: string;
  t: (key: string) => string;
}

function CuspAspectGrid({ title, cuspData, planetOrder, language, t }: CuspAspectGridProps) {
  const cusps = Array.from({ length: 12 }, (_, i) => i + 1);
  const abbr = language === 'hi' ? PLANET_ABBR_HI : PLANET_ABBR_EN;

  return (
    <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-4">
      <h4 className="font-display font-semibold text-sacred-brown mb-3">{title}</h4>
      <div className="overflow-x-auto">
        <table className="w-full text-data border-collapse" style={{ minWidth: '700px' }}>
          <thead>
            <tr>
              <th className="p-1.5 text-left font-semibold border border-slate-200 bg-slate-100 sticky left-0 z-10" style={{ minWidth: '60px' }}>
                -
              </th>
              {cusps.map((c) => (
                <th key={c} className="p-1.5 text-center font-semibold border border-slate-200 bg-slate-100" style={{ minWidth: '50px' }}>
                  {t('auto.cC')}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {planetOrder.map((planet: string) => {
              const row = cuspData[planet];
              if (!row) return null;
              return (
                <tr key={planet}>
                  <td className="p-1.5 font-semibold border border-slate-200 bg-slate-50 sticky left-0 z-10">
                    {abbr[planet] || (translatePlanet(planet, language) || planet || '').slice(0, 4)}
                  </td>
                  {row.map((cell) => {
                    const colors = cell.aspect ? ASPECT_COLORS[cell.aspect] : null;
                    return (
                      <td
                        key={cell.cusp}
                        className="p-1 text-center border border-slate-200"
                        style={colors ? { backgroundColor: colors.bg, color: colors.text } : undefined}
                        title={cell.aspect_name ? `${translateBackend(cell.aspect_name, language)} (orb: ${cell.orb}°)` : `${cell.degree}°`}
                      >
                        <div className="font-mono font-semibold">{cell.degree}</div>
                        {cell.aspect && (
                          <div className="text-micro font-medium">{language === 'hi' ? (ASPECT_ABBR_HI[cell.aspect] || cell.aspect) : cell.aspect}</div>
                        )}
                      </td>
                    );
                  })}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
