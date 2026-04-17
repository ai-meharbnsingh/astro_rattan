import { Loader2 } from 'lucide-react';
import InteractiveKundli, { type ChartData } from '@/components/InteractiveKundli';
import { getDivisionalChartOptions } from '@/components/kundli/kundli-utils';
import { translatePlanet, translateSign, translateBackend } from '@/lib/backend-translations';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell, TableCaption, TableFooter } from '@/components/ui/table';
import { Heading } from '@/components/ui/heading';

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
        <label className="text-sm font-medium text-foreground">{t('kundli.selectChart')}:</label>
        <select
          value={selectedDivision}
          onChange={(e) => changeDivision(e.target.value)}
          className="bg-muted border border-border rounded-lg px-3 py-2 text-foreground text-sm focus:border-border focus:outline-none"
        >
          {getDivisionalChartOptions(language).map((c) => (
            <option key={c.code} value={c.code}>{c.name}</option>
          ))}
        </select>
      </div>

      {loadingDivisional ? (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="w-6 h-6 animate-spin text-primary" />
          <span className="ml-2 text-foreground">{t('kundli.loadingDivisional')}</span>
        </div>
      ) : divisionalData ? (
        <div className="space-y-6">
          <div className="bg-gradient-to-r from-muted to-muted rounded-xl p-4 border border-border">
            <Heading as={4} variant={4}>{translateBackend(divisionalData.chart_name || divisionalData.chart_type, language)}</Heading>
            <p className="text-sm text-foreground">{t('kundli.division')}: {divisionalData.division}</p>
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
            <div className="rounded-xl border border-border h-fit">
              <Table className="w-full">
                <TableHeader className="bg-muted">
                  <TableRow>
                    <TableHead className="text-left p-3 text-primary font-medium text-sm">{t('table.planet')}</TableHead>
                    <TableHead className="text-left p-3 text-primary font-medium text-sm">{t('table.sign')}</TableHead>
                    <TableHead className="text-left p-3 text-primary font-medium text-sm">{t('table.degree')}</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {Object.entries(divisionalData.planet_signs || {}).map(([planet, sign]: [string, any]) => {
                    const posData = (divisionalData.planet_positions || []).find((p: any) => p.planet === planet);
                    return (
                      <TableRow key={planet} className="border-t border-border hover:bg-muted/5">
                        <TableCell className="p-3 text-foreground font-medium text-sm">{translatePlanet(planet, language)}</TableCell>
                        <TableCell className="p-3 text-foreground text-sm">{translateSign(sign as string, language)}</TableCell>
                        <TableCell className="p-3 text-foreground text-sm">{posData?.sign_degree?.toFixed(1) || '--'}&deg;</TableCell>
                      </TableRow>
                    );
                  })}
                </TableBody>
              </Table>
            </div>
          </div>

          {/* D60 Special Analysis */}
          {divisionalData.d60_analysis && (
            <div className="bg-muted rounded-xl p-5 border border-border shadow-sm animate-in fade-in slide-in-from-bottom-4 space-y-6">
              <div className="flex items-center gap-2 mb-4 border-b border-border/30 pb-3">
                <Heading as={4} variant={4} className="text-primary">{t('auto.d60ShashtiamsaKarmic')}</Heading>
                <span className="text-xs px-2 py-0.5 rounded-full bg-muted/10 text-primary border border-border/20 font-bold uppercase tracking-tighter">{t('auto.expert')}</span>
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
                      <Heading as={5} variant={5} className="mb-1">
                        {t('auto.birthTimeAccuracy')}
                        <span className="ml-2 text-xs uppercase tracking-wider opacity-70">
                          ({divisionalData.d60_analysis.birth_time_assessment.confidence_level})
                        </span>
                      </Heading>
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
                <div className="bg-white rounded-lg p-4 border border-border/20">
                  <Heading as={5} variant={5} className="mb-3">
                    {t('auto.karmicSummary')}
                  </Heading>
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
                  <p className="text-sm text-foreground mb-3">
                    {language === 'hi'
                      ? divisionalData.d60_analysis.karmic_summary.overall_description?.hi
                      : divisionalData.d60_analysis.karmic_summary.overall_description?.en}
                  </p>
                  
                  {/* Life Purpose */}
                  {divisionalData.d60_analysis.karmic_summary.life_purpose && (
                    <div className="mt-4 p-3 bg-muted/10 rounded-lg">
                      <Heading as={6} variant={6} className="text-primary mb-1">
                        {t('auto.lifePurpose')}: {' '}
                        {language === 'hi'
                          ? divisionalData.d60_analysis.karmic_summary.life_purpose.primary_hi
                          : divisionalData.d60_analysis.karmic_summary.life_purpose.primary}
                      </Heading>
                      <p className="text-xs text-foreground">
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
                <Heading as={5} variant={5} className="mb-3">
                  {t('auto.planetWiseKarmicAnal')}
                </Heading>
                <Table className="w-full text-sm border-collapse">
                  <TableHeader>
                    <TableRow className="bg-muted/10">
                      <TableHead className="text-left p-2.5 text-primary font-bold border-b border-border">{t('table.planet')}</TableHead>
                      <TableHead className="text-center p-2.5 text-primary font-bold border-b border-border">{t('auto.unit')}</TableHead>
                      <TableHead className="text-left p-2.5 text-primary font-bold border-b border-border">{t('auto.sanskritName')}</TableHead>
                      <TableHead className="text-center p-2.5 text-primary font-bold border-b border-border">{t('auto.nature')}</TableHead>
                      <TableHead className="text-left p-2.5 text-primary font-bold border-b border-border">{t('auto.pastLifeTheme')}</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {Object.entries(divisionalData.d60_analysis.planetary_analysis || {}).map(([planet, info]: [string, any]) => {
                      const isMalefic = info.nature === 'Malefic';
                      const isBenefic = info.nature === 'Benefic';
                      const natureLabel = language === 'hi' 
                        ? (isBenefic ? 'शुभ' : isMalefic ? 'पाप' : 'मिश्रित') 
                        : info.nature;
                      const theme = language === 'hi' ? info.past_life_theme?.theme_hi : info.past_life_theme?.theme;

                      return (
                        <TableRow key={planet} className="border-t border-border/20 hover:bg-muted/5 transition-colors">
                          <TableCell className="p-2.5 text-foreground font-bold whitespace-nowrap">{translatePlanet(planet, language)}</TableCell>
                          <TableCell className="p-2.5 text-center text-foreground font-mono">{info.unit}</TableCell>
                          <TableCell className="p-2.5 text-primary font-bold italic">{language === 'hi' ? info.name_hi : info.name}</TableCell>
                          <TableCell className="p-2.5 text-center">
                            <span className={`px-2 py-0.5 rounded-full text-[10px] font-black uppercase ${
                              isBenefic ? 'bg-green-100 text-green-700 border border-green-200' :
                              isMalefic ? 'bg-red-100 text-red-700 border border-red-200' :
                              'bg-blue-50 text-blue-700 border border-blue-100'
                            }`}>
                              {natureLabel}
                            </span>
                          </TableCell>
                          <TableCell className="p-2.5 text-foreground text-xs leading-relaxed">
                            {theme || info.description}
                          </TableCell>
                        </TableRow>
                      );
                    })}
                  </TableBody>
                </Table>
              </div>

              {/* Karmic Debts */}
              {divisionalData.d60_analysis.karmic_summary?.karmic_debts?.length > 0 && (
                <div className="bg-red-50 rounded-lg p-4 border border-red-100">
                  <Heading as={5} variant={5} className="text-red-800 mb-3">
                    {t('auto.identifiedKarmicDebt')}
                  </Heading>
                  <div className="space-y-3">
                    {divisionalData.d60_analysis.karmic_summary.karmic_debts.map((debt: any, idx: number) => (
                      <div key={idx} className="bg-white p-3 rounded border border-red-100">
                        <Heading as={6} variant={6} className="text-red-700">
                          {language === 'hi' ? debt.debt_type_hi : debt.debt_type}
                        </Heading>
                        <p className="text-xs text-foreground mt-1">
                          <span className="font-semibold">{t('auto.planets')}</span>
                          {debt.planets_involved?.join(', ')}
                        </p>
                        <p className="text-xs text-foreground mt-1">
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
                  <Heading as={5} variant={5} className="text-blue-800 mb-2">
                    {t('auto.remedyAccessibility')}: {' '}
                    {language === 'hi' 
                      ? divisionalData.d60_analysis.karmic_summary.remedy_accessibility.level_hi
                      : divisionalData.d60_analysis.karmic_summary.remedy_accessibility.level}
                  </Heading>
                  <p className="text-sm text-foreground mb-3">
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
              <div className="mt-4 p-3 bg-white/50 rounded-lg border border-border/10 text-xs text-foreground italic leading-relaxed">
                {t('auto.AccordingToSageParas')
                }
              </div>
            </div>
          )}
        </div>
      ) : (
        <p className="text-center text-foreground py-8">{t('kundli.selectChartToLoad')}</p>
      )}
    </div>
  );
}
