import { Loader2 } from 'lucide-react';
import InteractiveKundli, { type ChartData } from '@/components/InteractiveKundli';
import { getDivisionalChartOptions } from '@/components/kundli/kundli-utils';
import { translatePlanet, translateSign, translateBackend } from '@/lib/backend-translations';

interface DivisionalTabProps {
  divisionalData: any;
  loadingDivisional: boolean;
  selectedDivision: string;
  changeDivision: (code: string) => void;
  handlePlanetClick: (planet: any) => void;
  handleHouseClick: (house: number, sign: string, planets: any[]) => void;
  language: string;
  t: (key: string) => string;
}

export default function DivisionalTab({
  divisionalData, loadingDivisional, selectedDivision, changeDivision,
  handlePlanetClick, handleHouseClick, language, t,
}: DivisionalTabProps) {
  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4 mb-4">
        <label className="text-sm font-medium text-sacred-brown">{t('kundli.selectChart')}:</label>
        <select
          value={selectedDivision}
          onChange={(e) => changeDivision(e.target.value)}
          className="bg-sacred-cream border border-sacred-gold rounded-lg px-3 py-2 text-sacred-brown text-sm focus:border-sacred-gold focus:outline-none"
        >
          {getDivisionalChartOptions(language).map((c) => (
            <option key={c.code} value={c.code}>{c.name}</option>
          ))}
        </select>
      </div>

      {loadingDivisional ? (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="w-6 h-6 animate-spin text-sacred-gold" />
          <span className="ml-2 text-cosmic-text">{t('kundli.loadingDivisional')}</span>
        </div>
      ) : divisionalData ? (
        <div className="space-y-6">
          <div className="bg-gradient-to-r from-sacred-cream to-sacred-gold rounded-xl p-4 border border-sacred-gold">
            <h4 className="font-display font-bold text-sacred-brown text-lg">{translateBackend(divisionalData.chart_name || divisionalData.chart_type, language)}</h4>
            <p className="text-sm text-cosmic-text">{t('kundli.division')}: {divisionalData.division}</p>
          </div>

          {/* Kundli Chart and Table side by side - same height, no scroll */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">
            {/* Left: Kundli Chart - 25% smaller */}
            {divisionalData.planet_positions && (
              <div className="flex justify-center">
                <div className="w-full max-w-[420px]">
                  <InteractiveKundli
                    chartData={{
                      planets: divisionalData.planet_positions.map((p: any) => ({
                        planet: p.planet,
                        sign: p.sign,
                        house: p.house,
                        nakshatra: p.nakshatra || '',
                        sign_degree: p.sign_degree || 0,
                        status: '',
                      })),
                      houses: divisionalData.houses || Array.from({ length: 12 }, (_, i) => ({
                        number: i + 1,
                        sign: ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'][i],
                      })),
                    } as ChartData}
                    onPlanetClick={handlePlanetClick}
                    onHouseClick={handleHouseClick}
                  />
                </div>
              </div>
            )}

            {/* Right: Planet Table - full height, no scroll */}
            <div className="rounded-xl border border-sacred-gold h-fit">
              <table className="w-full">
                <thead className="bg-sacred-cream">
                  <tr>
                    <th className="text-left p-3 text-sacred-gold-dark font-medium text-sm">{t('table.planet')}</th>
                    <th className="text-left p-3 text-sacred-gold-dark font-medium text-sm">{t('table.sign')}</th>
                    <th className="text-left p-3 text-sacred-gold-dark font-medium text-sm">{t('table.degree')}</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.entries(divisionalData.planet_signs || {}).map(([planet, sign]: [string, any]) => {
                    const posData = (divisionalData.planet_positions || []).find((p: any) => p.planet === planet);
                    return (
                      <tr key={planet} className="border-t border-sacred-gold hover:bg-sacred-gold/5">
                        <td className="p-3 text-sacred-brown font-medium text-sm">{translatePlanet(planet, language)}</td>
                        <td className="p-3 text-cosmic-text text-sm">{translateSign(sign as string, language)}</td>
                        <td className="p-3 text-cosmic-text text-sm">{posData?.sign_degree?.toFixed(1) || '--'}&deg;</td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      ) : (
        <p className="text-center text-cosmic-text py-8">{t('kundli.selectChartToLoad')}</p>
      )}
    </div>
  );
}
