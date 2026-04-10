import { Sparkles, X } from 'lucide-react';
import InteractiveKundli, { type PlanetData, type ChartData } from '@/components/InteractiveKundli';
import { PLANET_ASPECTS, toDMS } from '@/components/kundli/kundli-utils';
import { translatePlanet, translateSign, translateLabel } from '@/lib/backend-translations';
import type { SidePanelState } from '@/hooks/useKundliData';

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
          <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-5 animate-in fade-in slide-in-from-right-4 duration-300">
            <div className="flex items-center justify-between mb-4">
              <h4 className="font-display font-bold text-sacred-brown text-lg">
                {sidePanel.type === 'planet'
                  ? `${translatePlanet(sidePanel.planet?.planet || '', language)}${(sidePanel.planet?.status || '').toLowerCase().includes('retrograde') ? ' (R)' : ''} — ${t('kundli.details')}`
                  : t('kundli.houseDetails')}
              </h4>
              <button
                onClick={() => setSidePanel(null)}
                className="text-cosmic-text hover:text-sacred-brown transition-colors"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {sidePanel.type === 'planet' && sidePanel.planet && (() => {
              const p = sidePanel.planet;
              const status = p.status?.toLowerCase() || '';
              const strengthLabel = status.includes('exalted') ? 'Exalted' : status.includes('debilitated') ? 'Debilitated' : status.includes('own') ? 'Own Sign' : p.status || 'Transiting';
              const strengthColor = status.includes('exalted') ? 'text-green-500' : status.includes('debilitated') ? 'text-red-500' : status.includes('own') ? 'text-blue-500' : 'text-cosmic-text';
              const aspects = (PLANET_ASPECTS[p.planet] || [7]).map((offset) => {
                const targetHouse = ((p.house - 1 + offset) % 12) + 1;
                return `${language === 'hi' ? 'भाव' : 'House'} ${targetHouse}`;
              });

              return (
                <div className="space-y-3">
                  <div className="grid grid-cols-2 gap-3">
                    <div className="bg-cosmic-card rounded-lg p-3">
                      <p className="text-sm text-cosmic-text">{t('kundli.sign')}</p>
                      <p className="font-semibold text-sacred-brown">{translateSign(p.sign, language)}</p>
                    </div>
                    <div className="bg-cosmic-card rounded-lg p-3">
                      <p className="text-sm text-cosmic-text">{t('kundli.degree')}</p>
                      <p className="font-semibold text-sacred-brown">{p.sign_degree != null ? toDMS(p.sign_degree) : '\u2014'}</p>
                    </div>
                    <div className="bg-cosmic-card rounded-lg p-3">
                      <p className="text-sm text-cosmic-text">{t('kundli.house')}</p>
                      <p className="font-semibold text-sacred-brown">{p.house}</p>
                    </div>
                    <div className="bg-cosmic-card rounded-lg p-3">
                      <p className="text-sm text-cosmic-text">{t('kundli.nakshatra')}</p>
                      <p className="font-semibold text-sacred-brown">
                        {p.nakshatra || 'N/A'}
                        {p.nakshatra_pada ? ` (${language === 'hi' ? 'पाद' : 'Pada'} ${p.nakshatra_pada})` : ''}
                      </p>
                    </div>
                  </div>
                  <div className="bg-cosmic-card rounded-lg p-3">
                    <p className="text-sm text-cosmic-text">{t('kundli.strength')}</p>
                    <p className={`font-semibold ${strengthColor}`}>{translateLabel(strengthLabel, language)}</p>
                  </div>
                  <div className="bg-cosmic-card rounded-lg p-3">
                    <p className="text-sm text-cosmic-text">{t('kundli.aspects')}</p>
                    <p className="font-semibold text-sacred-brown text-sm">{aspects.join(', ')}</p>
                  </div>
                  <div className="bg-cosmic-card rounded-lg p-3">
                    <p className="text-sm text-cosmic-text">{t('kundli.housePlacement')}</p>
                    <p className="text-sm text-sacred-brown">
                      {translatePlanet(p.planet, language)} — {t('kundli.house')} {p.house} ({HOUSE_SIGNIFICANCE[p.house] || (language === 'hi' ? 'अज्ञात' : 'Unknown')})
                    </p>
                  </div>
                </div>
              );
            })()}

            {sidePanel.type === 'house' && (
              <div className="space-y-3">
                <div className="grid grid-cols-2 gap-3">
                  <div className="bg-cosmic-card rounded-lg p-3">
                    <p className="text-sm text-cosmic-text">{t('kundli.houseNumber')}</p>
                    <p className="font-semibold text-sacred-brown">{sidePanel.house}</p>
                  </div>
                  <div className="bg-cosmic-card rounded-lg p-3">
                    <p className="text-sm text-cosmic-text">{t('kundli.sign')}</p>
                    <p className="font-semibold text-sacred-brown">{translateSign(sidePanel.sign || '', language)}</p>
                  </div>
                </div>
                <div className="bg-cosmic-card rounded-lg p-3">
                  <p className="text-sm text-cosmic-text">{t('kundli.significance')}</p>
                  <p className="font-semibold text-sacred-brown">
                    {HOUSE_SIGNIFICANCE[sidePanel.house || 0] || (language === 'hi' ? 'अज्ञात' : 'Unknown')}
                  </p>
                </div>
                <div className="bg-cosmic-card rounded-lg p-3">
                  <p className="text-sm text-cosmic-text mb-2">{t('kundli.planetsInHouse')}</p>
                  {(sidePanel.planets || []).length > 0 ? (
                    <div className="space-y-1">
                      {(sidePanel.planets || []).map((p) => (
                        <button
                          key={p.planet}
                          className="w-full text-left text-sm text-sacred-brown hover:text-sacred-gold transition-colors flex items-center gap-2"
                          onClick={() => setSidePanel({ type: 'planet', planet: p })}
                        >
                          <span className="w-2 h-2 rounded-full bg-sacred-gold" />
                          {translatePlanet(p.planet, language)}{(p.status || '').toLowerCase().includes('retrograde') ? '*' : ''} ({translateSign(p.sign, language)} {p.sign_degree != null ? toDMS(p.sign_degree) : '\u2014'})
                        </button>
                      ))}
                    </div>
                  ) : (
                    <p className="text-sm text-cosmic-text">{t('kundli.noPlanets')}</p>
                  )}
                </div>
              </div>
            )}
          </div>
        ) : (
          <div className="bg-sacred-cream rounded-xl border border-dashed border-sacred-gold p-8 flex flex-col items-center justify-center h-full min-h-[200px]">
            <Sparkles className="w-8 h-8 text-sacred-gold mb-3" />
            <p className="text-cosmic-text text-sm text-center">
              {t('kundli.clickInfo')}
            </p>
          </div>
        )}

        {/* Planet table */}
        <div className="mt-6 overflow-x-auto rounded-xl border border-sacred-gold">
          <table className="w-full">
            <thead className="bg-sacred-cream">
              <tr>
                <th className="text-left p-3 text-sacred-gold-dark font-medium text-sm">{t('table.planet')}</th>
                <th className="text-left p-3 text-sacred-gold-dark font-medium text-sm">{t('table.sign')}</th>
                <th className="text-left p-3 text-sacred-gold-dark font-medium text-sm">{t('table.house')}</th>
                <th className="text-left p-3 text-sacred-gold-dark font-medium text-sm">{t('table.nakshatra')}</th>
                <th className="text-left p-3 text-sacred-gold-dark font-medium text-sm">{t('table.status')}</th>
              </tr>
            </thead>
            <tbody>
              {planets.map((planet: any, index: number) => (
                <tr
                  key={index}
                  className={`border-t border-sacred-gold cursor-pointer transition-colors ${
                    sidePanel?.type === 'planet' && sidePanel.planet?.planet === planet.planet
                      ? 'bg-sacred-gold'
                      : 'hover:bg-sacred-gold'
                  }`}
                  onClick={() => handlePlanetClick(planet)}
                >
                  <td className="p-3 text-sacred-brown font-medium text-sm">
                    {translatePlanet(planet.planet, language)}
                    {(planet.status || '').toLowerCase().includes('retrograde') && <span className="text-red-500 ml-0.5" title="Retrograde">*</span>}
                  </td>
                  <td className="p-3 text-cosmic-text text-sm">{translateSign(planet.sign, language)}</td>
                  <td className="p-3 text-cosmic-text text-sm">{planet.house}</td>
                  <td className="p-3 text-cosmic-text text-sm">
                    {planet.nakshatra || '\u2014'}
                    {planet.nakshatra_pada ? ` (${language === 'hi' ? 'पाद' : 'P'}${planet.nakshatra_pada})` : ''}
                  </td>
                  <td className="p-3">
                    <span className={`text-sm px-2 py-1 rounded-full ${planet.status === 'Exalted' || planet.status === 'Own Sign' ? 'bg-green-100 text-green-800' : 'bg-cosmic-surface text-cosmic-text'}`}>
                      {translateLabel(planet.status, language)}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
