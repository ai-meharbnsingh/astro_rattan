import { Sparkles, X } from 'lucide-react';
import InteractiveKundli, { type PlanetData, type ChartData } from '@/components/InteractiveKundli';
import { PLANET_ASPECTS, toDMS } from '@/components/kundli/kundli-utils';
import { translatePlanet, translateSign, translateLabel, translateNakshatra } from '@/lib/backend-translations';
import type { SidePanelState } from '@/hooks/useKundliData';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell, TableCaption, TableFooter } from '@/components/ui/table';
import { Heading } from '@/components/ui/heading';

interface PlanetsTabProps {
  planets: any[];
  result: any;
  sidePanel: SidePanelState;
  setSidePanel: (v: SidePanelState) => void;
  handlePlanetClick: (planet: PlanetData) => void;
  handleHouseClick: (house: number, sign: string, planets: PlanetData[]) => void;
  language: string;
  t: (key: string) => string;
  HOUSE_SIGNIFICANCE: Record<number, string>;
}

export default function PlanetsTab({
  planets, result, sidePanel, setSidePanel,
  handlePlanetClick, handleHouseClick,
  language, t, HOUSE_SIGNIFICANCE,
}: PlanetsTabProps) {
  return (
    <div className="flex flex-col xl:flex-row gap-8">
      {/* Interactive Chart */}
      <div className="w-full xl:w-[600px] xl:flex-shrink-0 flex justify-center">
        <InteractiveKundli
          chartData={{ planets, houses: result.chart_data?.houses, ascendant: result.chart_data?.ascendant } as ChartData}
          onPlanetClick={handlePlanetClick}
          onHouseClick={handleHouseClick}
        />
      </div>

      {/* Side Panel */}
      <div className="flex-1 min-w-0">
        {sidePanel ? (
          <div className="bg-muted rounded-xl border border-border p-5 animate-in fade-in slide-in-from-right-4 duration-300">
            <div className="flex items-center justify-between mb-4">
              <Heading as={4} variant={4}>
                {sidePanel.type === 'planet'
                  ? `${translatePlanet(sidePanel.planet?.planet || '', language)}${(sidePanel.planet?.status || '').toLowerCase().includes('retrograde') ? ' (R)' : ''} — ${t('kundli.details')}`
                  : t('kundli.houseDetails')}
              </Heading>
              <button
                onClick={() => setSidePanel(null)}
                className="text-foreground hover:text-foreground transition-colors"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {sidePanel.type === 'planet' && sidePanel.planet && (() => {
              const p = sidePanel.planet;
              const status = p.status?.toLowerCase() || '';
              const strengthLabel = status.includes('exalted') ? 'Exalted' : status.includes('debilitated') ? 'Debilitated' : status.includes('own') ? 'Own Sign' : p.status || t('kundli.transit');
              const strengthColor = status.includes('exalted') ? 'text-green-500' : status.includes('debilitated') ? 'text-red-500' : status.includes('own') ? 'text-blue-500' : 'text-foreground';
              const aspects = (PLANET_ASPECTS[p.planet] || [7]).map((offset) => {
                const targetHouse = ((p.house - 1 + offset) % 12) + 1;
                return `${t('table.house')} ${targetHouse}`;
              });

              return (
                <div className="space-y-3">
                  <div className="grid grid-cols-2 gap-3">
                    <div className="bg-card rounded-lg p-3">
                      <p className="text-sm text-foreground">{t('kundli.sign')}</p>
                      <p className="font-semibold text-foreground">{translateSign(p.sign, language)}</p>
                    </div>
                    <div className="bg-card rounded-lg p-3">
                      <p className="text-sm text-foreground">{t('kundli.degree')}</p>
                      <p className="font-semibold text-foreground">{p.sign_degree != null ? toDMS(p.sign_degree) : '\u2014'}</p>
                    </div>
                    <div className="bg-card rounded-lg p-3">
                      <p className="text-sm text-foreground">{t('kundli.house')}</p>
                      <p className="font-semibold text-foreground">{p.house}</p>
                    </div>
                    <div className="bg-card rounded-lg p-3">
                      <p className="text-sm text-foreground">{t('kundli.nakshatra')}</p>
                      <p className="font-semibold text-foreground">
                        {translateNakshatra(p.nakshatra, language) || t('common.noData')}
                        {p.nakshatra_pada ? ` (${t('auto.pada')} ${p.nakshatra_pada})` : ''}
                      </p>
                    </div>
                  </div>
                  <div className="bg-card rounded-lg p-3">
                    <p className="text-sm text-foreground">{t('kundli.strength')}</p>
                    <p className={`font-semibold ${strengthColor}`}>{translateLabel(strengthLabel, language)}</p>
                  </div>
                  <div className="bg-card rounded-lg p-3">
                    <p className="text-sm text-foreground">{t('kundli.aspects')}</p>
                    <p className="font-semibold text-foreground text-sm">{aspects.join(', ')}</p>
                  </div>
                  <div className="bg-card rounded-lg p-3">
                    <p className="text-sm text-foreground">{t('kundli.housePlacement')}</p>
                    <p className="text-sm text-foreground">
                      {translatePlanet(p.planet, language)} — {t('kundli.house')} {p.house} ({HOUSE_SIGNIFICANCE[p.house] || t('common.noData')})
                    </p>
                  </div>
                </div>
              );
            })()}

            {sidePanel.type === 'house' && (
              <div className="space-y-3">
                <div className="grid grid-cols-2 gap-3">
                  <div className="bg-card rounded-lg p-3">
                    <p className="text-sm text-foreground">{t('kundli.houseNumber')}</p>
                    <p className="font-semibold text-foreground">{sidePanel.house}</p>
                  </div>
                  <div className="bg-card rounded-lg p-3">
                    <p className="text-sm text-foreground">{t('kundli.sign')}</p>
                    <p className="font-semibold text-foreground">{translateSign(sidePanel.sign || '', language)}</p>
                  </div>
                </div>
                <div className="bg-card rounded-lg p-3">
                  <p className="text-sm text-foreground">{t('kundli.significance')}</p>
                  <p className="font-semibold text-foreground">
                    {HOUSE_SIGNIFICANCE[sidePanel.house || 0] || t('common.noData')}
                  </p>
                </div>
                <div className="bg-card rounded-lg p-3">
                  <p className="text-sm text-foreground mb-2">{t('kundli.planetsInHouse')}</p>
                  {(sidePanel.planets || []).length > 0 ? (
                    <div className="space-y-1">
                      {(sidePanel.planets || []).map((p) => (
                        <button
                          key={p.planet}
                          className="w-full text-left text-sm text-foreground hover:text-primary transition-colors flex items-center gap-2"
                          onClick={() => setSidePanel({ type: 'planet', planet: p })}
                        >
                          <span className="w-2 h-2 rounded-full bg-muted" />
                          {translatePlanet(p.planet, language)}{(p.status || '').toLowerCase().includes('retrograde') ? '*' : ''} ({translateSign(p.sign, language)} {p.sign_degree != null ? toDMS(p.sign_degree) : '\u2014'})
                        </button>
                      ))}
                    </div>
                  ) : (
                    <p className="text-sm text-foreground">{t('kundli.noPlanets')}</p>
                  )}
                </div>
              </div>
            )}
          </div>
        ) : (
          <div className="bg-muted rounded-xl border border-dashed border-border p-8 flex flex-col items-center justify-center h-full min-h-[200px]">
            <Sparkles className="w-8 h-8 text-primary mb-3" />
            <p className="text-foreground text-sm text-center">
              {t('kundli.clickInfo')}
            </p>
          </div>
        )}

        {/* Planet table */}
        <div className="mt-6 overflow-x-auto rounded-xl border border-border">
          <Table className="w-full text-xs">
            <TableHeader className="bg-muted">
              <TableRow>
                <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.planet')}</TableHead>
                <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.sign')}</TableHead>
                <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.house')}</TableHead>
                <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.nakshatra')}</TableHead>
                <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.status')}</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {planets.map((planet: any, index: number) => (
                <TableRow
                  key={index}
                  className={`border-t border-border cursor-pointer transition-colors ${
                    sidePanel?.type === 'planet' && sidePanel.planet?.planet === planet.planet
                      ? 'bg-muted'
                      : 'hover:bg-muted/5'
                  }`}
                  onClick={() => handlePlanetClick(planet)}
                >
                  <TableCell className="p-1.5 text-foreground font-medium">
                    {translatePlanet(planet.planet, language)}
                    {(planet.status || '').toLowerCase().includes('retrograde') && <span className="text-red-500 ml-0.5" title={t('kundli.retrograde')}>*</span>}
                  </TableCell>
                  <TableCell className="p-1.5 text-foreground">{translateSign(planet.sign, language)}</TableCell>
                  <TableCell className="p-1.5 text-foreground">{planet.house}</TableCell>
                  <TableCell className="p-1.5 text-foreground">
                    {translateNakshatra(planet.nakshatra, language) || '\u2014'}
                    {planet.nakshatra_pada ? ` (${t('auto.p')}${planet.nakshatra_pada})` : ''}
                  </TableCell>
                  <TableCell className="p-1.5">
                    <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${planet.status === 'Exalted' || planet.status === 'Own Sign' ? 'bg-green-100 text-green-800' : 'bg-card text-foreground'}`}>
                      {translateLabel(planet.status, language)}
                    </span>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </div>
    </div>
  );
}
