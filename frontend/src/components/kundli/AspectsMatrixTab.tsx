import { Grid3X3, Loader2 } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';
import { translatePlanet, translateBackend } from '@/lib/backend-translations';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '@/components/ui/table';
import { Heading } from '@/components/ui/heading';

interface AspectsMatrixTabProps {
  data: any;
  loading: boolean;
}

const ASPECT_COLORS: Record<string, { bg: string; text: string }> = {
  conj: { bg: '#dbeafe', text: '#1e40af' },
  sext: { bg: '#d1fae5', text: '#065f46' },
  squr: { bg: '#fee2e2', text: '#991b1b' },
  trin: { bg: '#d1fae5', text: '#065f46' },
  oppo: { bg: '#fee2e2', text: '#991b1b' },
  ssqr: { bg: '#ffedd5', text: '#9a3412' },
  sesq: { bg: '#ffedd5', text: '#9a3412' },
  ququ: { bg: '#ede9fe', text: '#5b21b6' },
};
const ASPECT_ABBR_HI: Record<string, string> = {
  conj: 'यु', sext: 'षड', squr: 'चतु', trin: 'त्रि',
  oppo: 'सप्त', ssqr: 'अर्ध', sesq: 'पौने', ququ: 'पंच',
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

  const header = (
    <div>
      <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
        <Grid3X3 className="w-6 h-6" />
        {language === 'hi' ? 'दृष्टि मैट्रिक्स' : 'Aspects Matrix'}
      </Heading>
      <p className="text-sm text-muted-foreground">
        {language === 'hi' ? 'सभी ग्रहीय दृष्टियों का पूर्ण ग्रिड — वैदिक और पाश्चात्य दोनों' : 'Full grid of all planetary aspects — both Vedic & Western'}
      </p>
    </div>
  );

  if (loading) {
    return (
      <div className="space-y-4">
        {header}
        <div className="flex items-center justify-center py-12">
          <Loader2 className="w-6 h-6 animate-spin text-primary" />
          <span className="ml-2 text-foreground">{t('common.loading')}</span>
        </div>
      </div>
    );
  }

  if (!data?.matrix) {
    return (
      <div className="space-y-4">
        {header}
        <p className="text-center text-foreground py-8">{t('common.noData')}</p>
      </div>
    );
  }

  const planets = data.planet_order || Object.keys(data.matrix);

  return (
    <div className="space-y-6">
      {header}

      {/* Planet × Planet Matrix */}
      <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
        <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
          {t('auto.aspectsOnPlanets')}
        </div>
        <div className="p-4">
          <div className="w-full overflow-x-auto">
            <Table className="text-xs border-collapse" style={{ minWidth: '560px' }}>
              <TableHeader>
                <TableRow>
                  <TableHead className="p-1.5 text-left font-semibold border border-slate-200 bg-muted sticky left-0 z-10 min-w-[60px]">—</TableHead>
                  {planets.map((p: string) => (
                    <TableHead key={p} className="p-1.5 text-center font-semibold border border-slate-200 bg-muted min-w-[52px] text-primary">
                      {PLANET_ABBR[p] || (translatePlanet(p, language) || p || '').slice(0, 4)}
                    </TableHead>
                  ))}
                </TableRow>
              </TableHeader>
              <TableBody>
                {planets.map((p1: string, rowIdx: number) => (
                  <TableRow key={p1}>
                    <TableCell className="p-1.5 font-semibold border border-slate-200 bg-muted/50 sticky left-0 z-10 text-primary">
                      {PLANET_ABBR[p1] || (translatePlanet(p1, language) || p1 || '').slice(0, 4)}
                    </TableCell>
                    {planets.map((p2: string, colIdx: number) => {
                      if (colIdx <= rowIdx) {
                        return <TableCell key={p2} className="p-1 border border-slate-200 bg-muted/20" />;
                      }
                      const cell = data.matrix[p1]?.[p2];
                      if (!cell) return <TableCell key={p2} className="p-1 border border-slate-200" />;
                      const colors = cell.aspect ? ASPECT_COLORS[cell.aspect] : null;
                      return (
                        <TableCell
                          key={p2}
                          className="p-1 text-center border border-slate-200"
                          style={colors ? { backgroundColor: colors.bg, color: colors.text } : undefined}
                          title={cell.aspect_name ? `${translateBackend(cell.aspect_name, language)} (orb: ${cell.orb}°)` : `${cell.degree}°`}
                        >
                          <div className="font-mono font-semibold">{cell.degree}</div>
                          {cell.aspect && (
                            <div className="text-[10px] font-medium">{language === 'hi' ? (ASPECT_ABBR_HI[cell.aspect] || cell.aspect) : cell.aspect}</div>
                          )}
                        </TableCell>
                      );
                    })}
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>

          {/* Legend */}
          <div className="flex flex-wrap gap-3 mt-4 text-xs text-foreground">
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
              <span key={abbr} className="flex items-center gap-1">
                <span
                  className="px-1.5 py-0.5 rounded text-xs font-mono font-bold"
                  style={{ backgroundColor: ASPECT_COLORS[abbr].bg, color: ASPECT_COLORS[abbr].text }}
                >
                  {abbr}
                </span>
                <span>{label}</span>
              </span>
            ))}
          </div>
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
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
            {t('auto.activeAspects')}
          </div>
          <div className="p-4 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
            {data.aspects_list.map((asp: any, i: number) => {
              const colors = ASPECT_COLORS[asp.aspect] || { bg: '#f1f5f9', text: '#334155' };
              return (
                <div
                  key={i}
                  className="flex items-center justify-between rounded-lg px-3 py-2 border text-xs"
                  style={{ backgroundColor: colors.bg, borderColor: colors.text + '30', color: colors.text }}
                >
                  <span className="font-semibold">
                    {translatePlanet(asp.planet1, language)} — {translatePlanet(asp.planet2, language)}
                  </span>
                  <span className="font-mono">
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
    <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
      <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
        {title}
      </div>
      <div className="p-4">
        <div className="w-full overflow-x-auto">
          <Table className="text-xs border-collapse" style={{ minWidth: '700px' }}>
            <TableHeader>
              <TableRow>
                <TableHead className="p-1.5 text-left font-semibold border border-slate-200 bg-muted sticky left-0 z-10 min-w-[60px]">—</TableHead>
                {cusps.map((c) => (
                  <TableHead key={c} className="p-1.5 text-center font-semibold border border-slate-200 bg-muted min-w-[48px] text-primary">
                    C{c}
                  </TableHead>
                ))}
              </TableRow>
            </TableHeader>
            <TableBody>
              {planetOrder.map((planet: string) => {
                const row = cuspData[planet];
                if (!row) return null;
                return (
                  <TableRow key={planet}>
                    <TableCell className="p-1.5 font-semibold border border-slate-200 bg-muted/50 sticky left-0 z-10 text-primary">
                      {abbr[planet] || (translatePlanet(planet, language) || planet || '').slice(0, 4)}
                    </TableCell>
                    {row.map((cell) => {
                      const colors = cell.aspect ? ASPECT_COLORS[cell.aspect] : null;
                      return (
                        <TableCell
                          key={cell.cusp}
                          className="p-1 text-center border border-slate-200"
                          style={colors ? { backgroundColor: colors.bg, color: colors.text } : undefined}
                          title={cell.aspect_name ? `${translateBackend(cell.aspect_name, language)} (orb: ${cell.orb}°)` : `${cell.degree}°`}
                        >
                          <div className="font-mono font-semibold">{cell.degree}</div>
                          {cell.aspect && (
                            <div className="text-[10px] font-medium">{language === 'hi' ? (ASPECT_ABBR_HI[cell.aspect] || cell.aspect) : cell.aspect}</div>
                          )}
                        </TableCell>
                      );
                    })}
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </div>
      </div>
    </div>
  );
}
