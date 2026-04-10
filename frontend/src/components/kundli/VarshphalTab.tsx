import { Loader2 } from 'lucide-react';
import InteractiveKundli, { type ChartData } from '@/components/InteractiveKundli';
import { translatePlanet, translateSign } from '@/lib/backend-translations';
import GeneralRemedies from './GeneralRemedies';

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
        <label className="text-sm font-medium text-sacred-brown">{t('varshphal.selectYear')}:</label>
        <select
          value={varshphalYear}
          onChange={(e) => changeVarshphalYear(Number(e.target.value))}
          className="bg-sacred-cream border border-sacred-gold rounded-lg px-3 py-2 text-sacred-brown text-sm focus:border-sacred-gold focus:outline-none"
        >
          {Array.from({ length: 20 }, (_, i) => new Date().getFullYear() - 10 + i).map((yr) => (
            <option key={yr} value={yr}>{yr}</option>
          ))}
        </select>
      </div>

      {loadingVarshphal ? (
        <div className="flex items-center justify-center py-12"><Loader2 className="w-6 h-6 animate-spin text-sacred-gold" /><span className="ml-2 text-cosmic-text">{t('varshphal.calculating')}</span></div>
      ) : varshphalData ? (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Solar Return Info */}
          <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-4">
            <h4 className="font-display font-semibold text-sacred-brown mb-3">{t('section.solarReturn')}</h4>
            <div className="grid grid-cols-2 gap-3 text-sm">
              <div className="bg-white rounded-lg p-3">
                <p className="text-sm text-cosmic-text">{t('varshphal.solarReturnDate')}</p>
                <p className="font-semibold text-sacred-brown">{varshphalData.solar_return?.date}</p>
              </div>
              <div className="bg-white rounded-lg p-3">
                <p className="text-sm text-cosmic-text">{t('varshphal.solarReturnTime')}</p>
                <p className="font-semibold text-sacred-brown">{varshphalData.solar_return?.time}</p>
              </div>
              <div className="bg-white rounded-lg p-3">
                <p className="text-sm text-cosmic-text">{t('section.yearLord')}</p>
                <p className="font-semibold" style={{ color: 'var(--aged-gold-dim)' }}>{translatePlanet(varshphalData.year_lord, language)}</p>
              </div>
              <div className="bg-white rounded-lg p-3">
                <p className="text-sm text-cosmic-text">{t('varshphal.completedYears')}</p>
                <p className="font-semibold text-sacred-brown">{varshphalData.completed_years}</p>
              </div>
            </div>
          </div>

          {/* Muntha */}
          <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-4">
            <h4 className="font-display font-semibold text-sacred-brown mb-3">{t('section.muntha')}</h4>
            <div className="grid grid-cols-2 gap-3 text-sm">
              <div className="bg-white rounded-lg p-3">
                <p className="text-sm text-cosmic-text">{t('section.munthaSign')}</p>
                <p className="font-semibold text-sacred-brown">{translateSign(varshphalData.muntha?.sign || '', language)}</p>
              </div>
              <div className="bg-white rounded-lg p-3">
                <p className="text-sm text-cosmic-text">{t('varshphal.munthaHouse')}</p>
                <p className="font-semibold text-sacred-brown">{language === 'hi' ? 'भाव' : 'House'} {varshphalData.muntha?.house}</p>
              </div>
              <div className="bg-white rounded-lg p-3">
                <p className="text-sm text-cosmic-text">{t('section.munthaLord')}</p>
                <p className="font-semibold" style={{ color: 'var(--aged-gold-dim)' }}>{translatePlanet(varshphalData.muntha?.lord || '', language)}</p>
              </div>
              <div className="bg-white rounded-lg p-3">
                <p className="text-sm text-cosmic-text">{t('table.status')}</p>
                <p className={`font-semibold ${varshphalData.muntha?.favorable ? 'text-green-400' : 'text-red-500'}`}>
                  {varshphalData.muntha?.favorable ? t('common.favorable') : t('common.challenging')}
                </p>
              </div>
            </div>
          </div>

          {/* Varshphal Chart */}
          <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-4">
            <h4 className="font-display font-semibold text-sacred-brown mb-3">{t('section.varshphalChart')} ({varshphalYear})</h4>
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
            ) : <p className="text-center text-cosmic-text py-4 text-sm">{t('common.noData')}</p>}
          </div>

          {/* Mudda Dasha */}
          <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-4">
            <h4 className="font-display font-semibold text-sacred-brown mb-3">
              {t('section.muddaDasha')}
              {(varshphalData.current_mudda || varshphalData.current_mudda_dasha) && (
                <span className="ml-2 text-sm px-2 py-1 rounded-full bg-sacred-gold-dark text-white-dark">
                  {t('common.current')}: {translatePlanet(varshphalData.current_mudda || varshphalData.current_mudda_dasha, language)}
                </span>
              )}
            </h4>
            <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead><tr className="bg-sacred-gold">
                <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.planet')}</th>
                <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.start')}</th>
                <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.end')}</th>
                <th className="text-center p-2 text-sacred-gold-dark font-medium">{t('table.days')}</th>
              </tr></thead>
              <tbody>
                {(varshphalData.mudda_dasha || []).map((md: any) => (
                  <tr key={md.planet} className={`border-t border-sacred-gold ${md.planet === (varshphalData.current_mudda || varshphalData.current_mudda_dasha) ? 'bg-sacred-gold font-semibold' : ''}`}>
                    <td className="p-2 text-sacred-brown">{translatePlanet(md.planet, language)}{md.planet === (varshphalData.current_mudda || varshphalData.current_mudda_dasha) ? ' \u2190' : ''}</td>
                    <td className="p-2 text-cosmic-text">{md.start_date}</td>
                    <td className="p-2 text-cosmic-text">{md.end_date}</td>
                    <td className="p-2 text-center text-cosmic-text">{md.days}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            </div>
          </div>
        </div>
      ) : (
        <p className="text-center text-cosmic-text py-8">{t('varshphal.clickTab')}</p>
      )}
      <GeneralRemedies language={language} />
    </div>
  );
}
