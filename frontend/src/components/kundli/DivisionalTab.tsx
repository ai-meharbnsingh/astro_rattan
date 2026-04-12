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

          {/* D60 Special Analysis */}
          {divisionalData.d60_analysis && (
            <div className="bg-sacred-cream rounded-xl p-5 border border-sacred-gold shadow-sm animate-in fade-in slide-in-from-bottom-4">
              <div className="flex items-center gap-2 mb-4 border-b border-sacred-gold/30 pb-3">
                <h4 className="text-lg font-bold text-sacred-gold-dark">{language === 'hi' ? 'षष्टयंश (D60) कर्मिक विश्लेषण' : 'D60 Karmic Analysis'}</h4>
                <span className="text-xs px-2 py-0.5 rounded-full bg-sacred-gold/10 text-sacred-gold-dark border border-sacred-gold/20 font-bold uppercase tracking-tighter">EXPERT</span>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-sm border-collapse">
                  <thead>
                    <tr className="bg-sacred-gold/10">
                      <th className="text-left p-2.5 text-sacred-gold-dark font-bold border-b border-sacred-gold">{t('table.planet')}</th>
                      <th className="text-center p-2.5 text-sacred-gold-dark font-bold border-b border-sacred-gold">{language === 'hi' ? 'इकाई' : 'Unit'}</th>
                      <th className="text-left p-2.5 text-sacred-gold-dark font-bold border-b border-sacred-gold">{language === 'hi' ? 'संस्कृत नाम' : 'Sanskrit Name'}</th>
                      <th className="text-center p-2.5 text-sacred-gold-dark font-bold border-b border-sacred-gold">{language === 'hi' ? 'प्रकृति' : 'Nature'}</th>
                      <th className="text-left p-2.5 text-sacred-gold-dark font-bold border-b border-sacred-gold">{language === 'hi' ? 'व्याख्या' : 'Meaning'}</th>
                    </tr>
                  </thead>
                  <tbody>
                    {Object.entries(divisionalData.d60_analysis).map(([planet, info]: [string, any]) => {
                      const isMalefic = info.nature === 'Malefic';
                      const isBenefic = info.nature === 'Benefic';
                      const natureLabel = language === 'hi' 
                        ? (isBenefic ? 'शुभ' : isMalefic ? 'पाप' : 'मिश्रित') 
                        : info.nature;

                      return (
                        <tr key={planet} className="border-t border-sacred-gold/20 hover:bg-sacred-gold/5 transition-colors">
                          <td className="p-2.5 text-sacred-brown font-bold whitespace-nowrap">{translatePlanet(planet, language)}</td>
                          <td className="p-2.5 text-center text-cosmic-text font-mono">{info.unit}</td>
                          <td className="p-2.5 text-sacred-gold-dark font-bold italic">{language === 'hi' ? info.name_hi : info.name}</td>
                          <td className="p-2.5 text-center">
                            <span className={`px-2 py-0.5 rounded-full text-[10px] font-black uppercase ${
                              isBenefic ? 'bg-green-100 text-green-700 border border-green-200' :
                              isMalefic ? 'bg-red-100 text-red-700 border border-red-200' :
                              'bg-blue-50 text-blue-700 border border-blue-100'
                            }`}>
                              {natureLabel}
                            </span>
                          </td>
                          <td className="p-2.5 text-cosmic-text text-xs leading-relaxed">
                            {info.description}
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
              <div className="mt-4 p-3 bg-white/50 rounded-lg border border-sacred-gold/10 text-xs text-cosmic-text italic leading-relaxed">
                {language === 'hi' 
                  ? "* पराशर ऋषि के अनुसार, षष्टयंश (D60) विश्लेषण के बिना किसी भी जन्म कुंडली पर अंतिम निर्णय नहीं सुनाया जाना चाहिए। यह चार्ट पूर्व जन्म के संचित कर्मों को प्रकट करता है।"
                  : "* According to Sage Parashara, no final judgment should be pronounced on any horoscope without Shashtiamsa (D60) analysis. This chart reveals the accumulated Sanchita Karma from past incarnations."
                }
              </div>
            </div>
          )}
        </div>
      ) : (
        <p className="text-center text-cosmic-text py-8">{t('kundli.selectChartToLoad')}</p>
      )}
    </div>
  );
}
