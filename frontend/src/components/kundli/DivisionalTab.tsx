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
            <div className="bg-sacred-cream rounded-xl p-5 border border-sacred-gold shadow-sm animate-in fade-in slide-in-from-bottom-4 space-y-6">
              <div className="flex items-center gap-2 mb-4 border-b border-sacred-gold/30 pb-3">
                <h4 className="text-lg font-bold text-sacred-gold-dark">{t('auto.d60ShashtiamsaKarmic')}</h4>
                <span className="text-xs px-2 py-0.5 rounded-full bg-sacred-gold/10 text-sacred-gold-dark border border-sacred-gold/20 font-bold uppercase tracking-tighter">EXPERT</span>
              </div>

              {/* Birth Time Sensitivity Warning */}
              {divisionalData.d60_analysis.birth_time_assessment && (
                <div className={`p-4 rounded-lg border ${
                  divisionalData.d60_analysis.birth_time_assessment.confidence_level === 'high' 
                    ? 'bg-green-50 border-green-200' :
                  divisionalData.d60_analysis.birth_time_assessment.confidence_level === 'moderate'
                    ? 'bg-yellow-50 border-yellow-200' :
                  divisionalData.d60_analysis.birth_time_assessment.confidence_level === 'low'
                    ? 'bg-orange-50 border-orange-200' :
                  'bg-red-50 border-red-200'
                }`}>
                  <div className="flex items-start gap-3">
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                      divisionalData.d60_analysis.birth_time_assessment.confidence_level === 'high' 
                        ? 'bg-green-100 text-green-700' :
                      divisionalData.d60_analysis.birth_time_assessment.confidence_level === 'moderate'
                        ? 'bg-yellow-100 text-yellow-700' :
                      divisionalData.d60_analysis.birth_time_assessment.confidence_level === 'low'
                        ? 'bg-orange-100 text-orange-700' :
                        'bg-red-100 text-red-700'
                    }`}>
                      ⚠
                    </div>
                    <div className="flex-1">
                      <h5 className="font-bold text-sm mb-1">
                        {t('auto.birthTimeAccuracy')}
                        <span className="ml-2 text-xs uppercase tracking-wider opacity-70">
                          ({divisionalData.d60_analysis.birth_time_assessment.confidence_level})
                        </span>
                      </h5>
                      <p className="text-sm mb-2">
                        {language === 'hi' 
                          ? divisionalData.d60_analysis.birth_time_assessment.assessment?.hi 
                          : divisionalData.d60_analysis.birth_time_assessment.assessment?.en}
                      </p>
                      <p className="text-xs opacity-80 mb-2">
                        {language === 'hi'
                          ? divisionalData.d60_analysis.birth_time_assessment.time_sensitivity?.hi
                          : divisionalData.d60_analysis.birth_time_assessment.time_sensitivity?.en}
                      </p>
                      {divisionalData.d60_analysis.birth_time_assessment.recommendations?.length > 0 && (
                        <ul className="text-xs space-y-1 mt-2">
                          {divisionalData.d60_analysis.birth_time_assessment.recommendations.map((rec: any, idx: number) => (
                            <li key={idx} className="flex items-start gap-1">
                              <span>•</span>
                              <span>{language === 'hi' ? rec.hi : rec.en}</span>
                            </li>
                          ))}
                        </ul>
                      )}
                    </div>
                  </div>
                </div>
              )}

              {/* Karmic Summary */}
              {divisionalData.d60_analysis.karmic_summary && (
                <div className="bg-white rounded-lg p-4 border border-sacred-gold/20">
                  <h5 className="font-bold text-sacred-brown mb-3">
                    {t('auto.karmicSummary')}
                  </h5>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                    <div className="bg-green-50 p-3 rounded-lg">
                      <div className="text-xs text-green-700 uppercase font-bold">
                        {t('auto.punyaScoreBenefic')}
                      </div>
                      <div className="text-2xl font-bold text-green-800">
                        {divisionalData.d60_analysis.karmic_summary.punya_score}%
                      </div>
                    </div>
                    <div className="bg-red-50 p-3 rounded-lg">
                      <div className="text-xs text-red-700 uppercase font-bold">
                        {t('auto.papaScoreMalefic')}
                      </div>
                      <div className="text-2xl font-bold text-red-800">
                        {divisionalData.d60_analysis.karmic_summary.papa_score}%
                      </div>
                    </div>
                  </div>
                  <p className="text-sm text-cosmic-text mb-3">
                    {language === 'hi'
                      ? divisionalData.d60_analysis.karmic_summary.overall_description?.hi
                      : divisionalData.d60_analysis.karmic_summary.overall_description?.en}
                  </p>
                  
                  {/* Life Purpose */}
                  {divisionalData.d60_analysis.karmic_summary.life_purpose && (
                    <div className="mt-4 p-3 bg-sacred-gold/10 rounded-lg">
                      <h6 className="font-bold text-sacred-gold-dark text-sm mb-1">
                        {t('auto.lifePurpose')}: {' '}
                        {language === 'hi'
                          ? divisionalData.d60_analysis.karmic_summary.life_purpose.primary_hi
                          : divisionalData.d60_analysis.karmic_summary.life_purpose.primary}
                      </h6>
                      <p className="text-xs text-cosmic-text">
                        {language === 'hi'
                          ? divisionalData.d60_analysis.karmic_summary.life_purpose.description_hi
                          : divisionalData.d60_analysis.karmic_summary.life_purpose.description}
                      </p>
                    </div>
                  )}
                </div>
              )}

              {/* Planetary Analysis Table */}
              <div className="overflow-x-auto">
                <h5 className="font-bold text-sacred-brown mb-3 text-sm">
                  {t('auto.planetWiseKarmicAnal')}
                </h5>
                <table className="w-full text-sm border-collapse">
                  <thead>
                    <tr className="bg-sacred-gold/10">
                      <th className="text-left p-2.5 text-sacred-gold-dark font-bold border-b border-sacred-gold">{t('table.planet')}</th>
                      <th className="text-center p-2.5 text-sacred-gold-dark font-bold border-b border-sacred-gold">{t('auto.unit')}</th>
                      <th className="text-left p-2.5 text-sacred-gold-dark font-bold border-b border-sacred-gold">{t('auto.sanskritName')}</th>
                      <th className="text-center p-2.5 text-sacred-gold-dark font-bold border-b border-sacred-gold">{t('auto.nature')}</th>
                      <th className="text-left p-2.5 text-sacred-gold-dark font-bold border-b border-sacred-gold">{t('auto.pastLifeTheme')}</th>
                    </tr>
                  </thead>
                  <tbody>
                    {Object.entries(divisionalData.d60_analysis.planetary_analysis || {}).map(([planet, info]: [string, any]) => {
                      const isMalefic = info.nature === 'Malefic';
                      const isBenefic = info.nature === 'Benefic';
                      const natureLabel = language === 'hi' 
                        ? (isBenefic ? 'शुभ' : isMalefic ? 'पाप' : 'मिश्रित') 
                        : info.nature;
                      const theme = language === 'hi' ? info.past_life_theme?.theme_hi : info.past_life_theme?.theme;

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
                            {theme || info.description}
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>

              {/* Karmic Debts */}
              {divisionalData.d60_analysis.karmic_summary?.karmic_debts?.length > 0 && (
                <div className="bg-red-50 rounded-lg p-4 border border-red-100">
                  <h5 className="font-bold text-red-800 mb-3">
                    {t('auto.identifiedKarmicDebt')}
                  </h5>
                  <div className="space-y-3">
                    {divisionalData.d60_analysis.karmic_summary.karmic_debts.map((debt: any, idx: number) => (
                      <div key={idx} className="bg-white p-3 rounded border border-red-100">
                        <h6 className="font-bold text-red-700 text-sm">
                          {language === 'hi' ? debt.debt_type_hi : debt.debt_type}
                        </h6>
                        <p className="text-xs text-cosmic-text mt-1">
                          <span className="font-semibold">{t('auto.planets')}</span>
                          {debt.planets_involved?.join(', ')}
                        </p>
                        <p className="text-xs text-cosmic-text mt-1">
                          {language === 'hi' ? debt.manifestation_hi : debt.manifestation}
                        </p>
                        <p className="text-xs text-green-700 mt-2 font-medium">
                          <span className="font-semibold">{t('auto.resolution')}</span>
                          {language === 'hi' ? debt.resolution_hi : debt.resolution}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Remedy Accessibility */}
              {divisionalData.d60_analysis.karmic_summary?.remedy_accessibility && (
                <div className="bg-blue-50 rounded-lg p-4 border border-blue-100">
                  <h5 className="font-bold text-blue-800 mb-2">
                    {t('auto.remedyAccessibility')}: {' '}
                    {language === 'hi' 
                      ? divisionalData.d60_analysis.karmic_summary.remedy_accessibility.level_hi
                      : divisionalData.d60_analysis.karmic_summary.remedy_accessibility.level}
                  </h5>
                  <p className="text-sm text-cosmic-text mb-3">
                    {language === 'hi'
                      ? divisionalData.d60_analysis.karmic_summary.remedy_accessibility.description_hi
                      : divisionalData.d60_analysis.karmic_summary.remedy_accessibility.description}
                  </p>
                  {divisionalData.d60_analysis.karmic_summary.remedy_accessibility.recommendations?.length > 0 && (
                    <ul className="text-xs space-y-1">
                      {divisionalData.d60_analysis.karmic_summary.remedy_accessibility.recommendations.map((rec: any, idx: number) => (
                        <li key={idx} className="flex items-start gap-2 text-blue-800">
                          <span>•</span>
                          <span>{language === 'hi' ? rec.hi : rec.en}</span>
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
              )}

              {/* Footer Note */}
              <div className="mt-4 p-3 bg-white/50 rounded-lg border border-sacred-gold/10 text-xs text-cosmic-text italic leading-relaxed">
                {t('auto.AccordingToSageParas')
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
