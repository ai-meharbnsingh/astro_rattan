import { Loader2 } from 'lucide-react';
import InteractiveKundli, { type ChartData } from '@/components/InteractiveKundli';
import { translatePlanet, translateSign } from '@/lib/backend-translations';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell, TableCaption, TableFooter } from '@/components/ui/table';
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
  handlePlanetClick, handleHouseClick, language, t,
}: VarshphalTabProps) {
  return (
    <div className="space-y-6">
      {/* Year selector */}
      <div className="flex items-center gap-4 mb-4">
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
        <div className="flex items-center justify-center py-12"><Loader2 className="w-6 h-6 animate-spin text-primary" /><span className="ml-2 text-foreground">{t('varshphal.calculating')}</span></div>
      ) : varshphalData ? (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Solar Return Info */}
          <div className="bg-muted rounded-xl border border-border p-4">
            <Heading as={4} variant={4} className="mb-3">{t('section.solarReturn')}</Heading>
            <div className="grid grid-cols-2 gap-3 text-sm">
              <div className="bg-white rounded-lg p-3">
                <p className="text-sm text-foreground">{t('varshphal.solarReturnDate')}</p>
                <p className="font-semibold text-foreground">{varshphalData.solar_return?.date}</p>
              </div>
              <div className="bg-white rounded-lg p-3">
                <p className="text-sm text-foreground">{t('varshphal.solarReturnTime')}</p>
                <p className="font-semibold text-foreground">{varshphalData.solar_return?.time}</p>
              </div>
              <div className="bg-white rounded-lg p-3">
                <p className="text-sm text-foreground">{t('section.yearLord')}</p>
                <p className="font-semibold text-primary">{translatePlanet(varshphalData.year_lord, language)}</p>
              </div>
              <div className="bg-white rounded-lg p-3">
                <p className="text-sm text-foreground">{t('varshphal.completedYears')}</p>
                <p className="font-semibold text-foreground">{varshphalData.completed_years}</p>
              </div>
            </div>
          </div>

          {/* Muntha */}
          <div className="bg-muted rounded-xl border border-border p-4">
            <Heading as={4} variant={4} className="mb-3">{t('section.muntha')}</Heading>
            <div className="grid grid-cols-2 gap-3 text-sm">
              <div className="bg-white rounded-lg p-3">
                <p className="text-sm text-foreground">{t('section.munthaSign')}</p>
                <p className="font-semibold text-foreground">{translateSign(varshphalData.muntha?.sign || '', language)}</p>
              </div>
              <div className="bg-white rounded-lg p-3">
                <p className="text-sm text-foreground">{t('varshphal.munthaHouse')}</p>
                <p className="font-semibold text-foreground">{t('auto.house')} {varshphalData.muntha?.house}</p>
              </div>
              <div className="bg-white rounded-lg p-3">
                <p className="text-sm text-foreground">{t('section.munthaLord')}</p>
                <p className="font-semibold text-primary">{translatePlanet(varshphalData.muntha?.lord || '', language)}</p>
              </div>
              <div className="bg-white rounded-lg p-3">
                <p className="text-sm text-foreground">{t('table.status')}</p>
                <p className={`font-semibold ${varshphalData.muntha?.favorable ? 'text-green-400' : 'text-red-500'}`}>
                  {varshphalData.muntha?.favorable ? t('common.favorable') : t('common.challenging')}
                </p>
              </div>
            </div>
          </div>

          {/* Varshphal Chart */}
          <div className="bg-muted rounded-xl border border-border p-4">
            <Heading as={4} variant={4} className="mb-3">{t('section.varshphalChart')} ({varshphalYear})</Heading>
            {varshphalData.chart_data?.planets ? (
              <div className="flex justify-center">
                <InteractiveKundli
                  chartData={{
                    planets: Object.entries(varshphalData.chart_data.planets).map(([name, data]: [string, any]) => ({
                      planet: name, sign: data?.sign || '', house: data?.house || 1,
                      nakshatra: data?.nakshatra || '', sign_degree: data?.sign_degree || 0,
                      status: data?.status || '', is_retrograde: data?.retrograde || false,
                    })),
                    houses: varshphalData.chart_data.houses,
                    ascendant: varshphalData.chart_data.ascendant,
                  } as ChartData}
                  onPlanetClick={handlePlanetClick}
                  onHouseClick={handleHouseClick}
                />
              </div>
            ) : <p className="text-center text-foreground py-4 text-sm">{t('common.noData')}</p>}
          </div>

          {/* Mudda Dasha */}
          <div className="bg-muted rounded-xl border border-border p-4">
            <Heading as={4} variant={4} className="mb-3">
              {t('section.muddaDasha')}
              {(varshphalData.current_mudda || varshphalData.current_mudda_dasha) && (
                <span className="ml-2 text-sm px-2 py-1 rounded-full bg-primary text-white-dark">
                  {t('common.current')}: {translatePlanet(varshphalData.current_mudda || varshphalData.current_mudda_dasha, language)}
                </span>
              )}
            </Heading>
            <div className="overflow-x-auto">
            <Table className="w-full text-sm">
              <TableHeader><TableRow className="bg-muted">
                <TableHead className="text-left p-2 text-primary font-medium">{t('table.planet')}</TableHead>
                <TableHead className="text-left p-2 text-primary font-medium">{t('table.start')}</TableHead>
                <TableHead className="text-left p-2 text-primary font-medium">{t('table.end')}</TableHead>
                <TableHead className="text-center p-2 text-primary font-medium">{t('table.days')}</TableHead>
              </TableRow></TableHeader>
              <TableBody>
                {(varshphalData.mudda_dasha || []).map((md: any) => (
                  <TableRow key={md.planet} className={`border-t border-border ${md.planet === (varshphalData.current_mudda || varshphalData.current_mudda_dasha) ? 'bg-muted font-semibold' : ''}`}>
                    <TableCell className="p-2 text-foreground">{translatePlanet(md.planet, language)}{md.planet === (varshphalData.current_mudda || varshphalData.current_mudda_dasha) ? ' \u2190' : ''}</TableCell>
                    <TableCell className="p-2 text-foreground">{md.start_date}</TableCell>
                    <TableCell className="p-2 text-foreground">{md.end_date}</TableCell>
                    <TableCell className="p-2 text-center text-foreground">{md.days}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
            </div>
          </div>
        </div>
      ) : (
        <p className="text-center text-foreground py-8">{t('varshphal.clickTab')}</p>
      )}
    </div>
  );
}
