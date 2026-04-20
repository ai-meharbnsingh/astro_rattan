import { Loader2 } from 'lucide-react';
import KundliChartSVG, { type PlanetEntry } from '@/components/KundliChartSVG';
import { translatePlanet, translateSign } from '@/lib/backend-translations';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '@/components/ui/table';
import { Heading } from '@/components/ui/heading';

interface VarshphalTabProps {
  varshphalData: any;
  loadingVarshphal: boolean;
  varshphalYear: number;
  changeVarshphalYear: (yr: number) => void;
  handlePlanetClick: (planet: any) => void;
  handleHouseClick: (house: number, sign: string, planets: any[]) => void;
  language: string;
  t: (key: string) => string;
}

export default function VarshphalTab({
  varshphalData, loadingVarshphal, varshphalYear, changeVarshphalYear,
  handlePlanetClick: _handlePlanetClick, handleHouseClick: _handleHouseClick, language, t,
}: VarshphalTabProps) {
  return (
    <div className="space-y-6">
      {/* Page heading */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1">
          {language === 'hi' ? 'वर्षफल' : 'Varshphal'}
        </Heading>
        <p className="text-sm text-muted-foreground">
          {language === 'hi' ? 'चालू वर्ष के लिए वार्षिक सौर वापसी चार्ट विश्लेषण' : 'Annual solar return chart analysis for the current year'}
        </p>
      </div>
      {/* Year selector */}
      <div className="flex items-center gap-4">
        <label className="text-sm font-medium text-foreground">{t('varshphal.selectYear')}:</label>
        <select
          value={varshphalYear}
          onChange={(e) => changeVarshphalYear(Number(e.target.value))}
          className="bg-muted border border-border rounded-lg px-3 py-2 text-foreground text-sm focus:border-border focus:outline-none"
        >
          {Array.from({ length: 20 }, (_, i) => new Date().getFullYear() - 10 + i).map((yr) => (
            <option key={yr} value={yr}>{yr}</option>
          ))}
        </select>
      </div>

      {loadingVarshphal ? (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="w-6 h-6 animate-spin text-primary" />
          <span className="ml-2 text-foreground">{t('varshphal.calculating')}</span>
        </div>
      ) : varshphalData ? (
        <div className="space-y-6">
          {/* Top row: Solar Return + Muntha */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Solar Return Info */}
            <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
              <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
                {t('section.solarReturn')}
              </div>
              <div className="p-4 grid grid-cols-2 gap-3 text-sm">
                <div className="rounded-lg border border-border p-3">
                  <p className="text-xs text-muted-foreground">{t('varshphal.solarReturnDate')}</p>
                  <p className="font-semibold text-foreground mt-0.5">{varshphalData.solar_return?.date || '—'}</p>
                </div>
                <div className="rounded-lg border border-border p-3">
                  <p className="text-xs text-muted-foreground">{t('varshphal.solarReturnTime')}</p>
                  <p className="font-semibold text-foreground mt-0.5">{varshphalData.solar_return?.time || '—'}</p>
                </div>
                <div className="rounded-lg border border-border p-3">
                  <p className="text-xs text-muted-foreground">{t('section.yearLord')}</p>
                  <p className="font-semibold text-primary mt-0.5">{translatePlanet(varshphalData.year_lord, language) || '—'}</p>
                </div>
                <div className="rounded-lg border border-border p-3">
                  <p className="text-xs text-muted-foreground">{t('varshphal.completedYears')}</p>
                  <p className="font-semibold text-foreground mt-0.5">{varshphalData.completed_years ?? '—'}</p>
                </div>
              </div>
            </div>

            {/* Muntha */}
            <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
              <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
                {t('section.muntha')}
              </div>
              <div className="p-4 grid grid-cols-2 gap-3 text-sm">
                <div className="rounded-lg border border-border p-3">
                  <p className="text-xs text-muted-foreground">{t('section.munthaSign')}</p>
                  <p className="font-semibold text-foreground mt-0.5">{translateSign(varshphalData.muntha?.sign || '', language) || '—'}</p>
                </div>
                <div className="rounded-lg border border-border p-3">
                  <p className="text-xs text-muted-foreground">{t('varshphal.munthaHouse')}</p>
                  <p className="font-semibold text-foreground mt-0.5">{varshphalData.muntha?.house ? `${t('auto.house')} ${varshphalData.muntha.house}` : '—'}</p>
                </div>
                <div className="rounded-lg border border-border p-3">
                  <p className="text-xs text-muted-foreground">{t('section.munthaLord')}</p>
                  <p className="font-semibold text-primary mt-0.5">{translatePlanet(varshphalData.muntha?.lord || '', language) || '—'}</p>
                </div>
                <div className="rounded-lg border border-border p-3">
                  <p className="text-xs text-muted-foreground">{t('table.status')}</p>
                  <p className={`font-semibold mt-0.5 ${varshphalData.muntha?.favorable ? 'text-emerald-600' : 'text-red-500'}`}>
                    {varshphalData.muntha?.favorable ? t('common.favorable') : t('common.challenging')}
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Bottom row: Chart + Mudda Dasha */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Varshphal Chart */}
            <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
              <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
                {t('section.varshphalChart')} ({varshphalYear})
              </div>
              {varshphalData.chart_data?.planets ? (
                <div className="flex justify-center p-4">
                  <div className="w-full max-w-[480px] aspect-square">
                    <KundliChartSVG
                      planets={Object.entries(varshphalData.chart_data.planets).map(([name, data]: [string, any]) => ({
                        planet: name,
                        sign: data?.sign || '',
                        house: data?.house || 1,
                        sign_degree: data?.sign_degree || 0,
                        is_retrograde: data?.retrograde || false,
                      } as PlanetEntry))}
                      ascendantSign={
                        typeof varshphalData.chart_data.ascendant === 'string'
                          ? varshphalData.chart_data.ascendant
                          : varshphalData.chart_data.ascendant?.sign || ''
                      }
                      language={language}
                      showHouseNumbers={false}
                      showRashiNumbers
                      rashiNumberPlacement="corner"
                      showAscendantMarker={false}
                    />
                  </div>
                </div>
              ) : (
                <p className="text-center text-foreground py-8 text-sm">{t('common.noData')}</p>
              )}
            </div>

            {/* Mudda Dasha */}
            <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
              <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-3">
                <span>{t('section.muddaDasha')}</span>
                {(varshphalData.current_mudda || varshphalData.current_mudda_dasha) && (
                  <span className="text-sm px-2 py-0.5 rounded-full bg-white/20 border border-white/30">
                    {t('common.current')}: {translatePlanet(varshphalData.current_mudda || varshphalData.current_mudda_dasha, language)}
                  </span>
                )}
              </div>
              <div className="overflow-x-auto">
                <Table className="w-full text-xs table-fixed">
                  <TableHeader>
                    <TableRow>
                      <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[28%]">{t('table.planet')}</TableHead>
                      <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[28%]">{t('table.start')}</TableHead>
                      <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[28%]">{t('table.end')}</TableHead>
                      <TableHead className="text-center p-2 text-primary font-semibold uppercase tracking-wide w-[16%]">{t('table.days')}</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {(varshphalData.mudda_dasha || []).map((md: any) => {
                      const currentMudda = varshphalData.current_mudda || varshphalData.current_mudda_dasha;
                      const isCurrent = md.planet === currentMudda;
                      return (
                        <TableRow key={md.planet} className={`border-t border-border ${isCurrent ? 'font-semibold' : ''}`}>
                          <TableCell className="p-2 text-foreground">
                            {translatePlanet(md.planet, language)}{isCurrent ? ' ←' : ''}
                          </TableCell>
                          <TableCell className="p-2 text-foreground">{md.start_date}</TableCell>
                          <TableCell className="p-2 text-foreground">{md.end_date}</TableCell>
                          <TableCell className="p-2 text-center text-foreground">{md.days}</TableCell>
                        </TableRow>
                      );
                    })}
                  </TableBody>
                </Table>
              </div>
            </div>
          </div>
        </div>
      ) : (
        <p className="text-center text-foreground py-8">{t('varshphal.clickTab')}</p>
      )}
    </div>
  );
}
