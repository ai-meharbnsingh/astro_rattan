import { Loader2 } from 'lucide-react';
import { getDivisionalChartOptions } from '@/components/kundli/kundli-utils';
import { translatePlanet, translateSign, translateBackend } from '@/lib/backend-translations';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '@/components/ui/table';
import KundliChartSVG, { type PlanetEntry } from '@/components/KundliChartSVG';

// ── Lord Significance sub-components ──────────────────────────

function HoraLordCard({ positions, language }: { positions: any[]; language: string }) {
  const isHi = language === 'hi';
  const lords = positions
    .filter((p: any) => p.hora_lord)
    .map((p: any) => ({ planet: p.planet, ...p.hora_lord }));
  if (!lords.length) return null;
  return (
    <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden mt-4">
      <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
        {isHi ? 'होरा स्वामी का महत्व (D2)' : 'Hora Lord Significance (D2)'}
      </div>
      <div className="p-4 space-y-2">
        {lords.map((l: any, i: number) => (
          <div key={i} className="flex items-start gap-3 text-sm border-b border-border/20 pb-2 last:border-0">
            <span className="font-bold text-primary w-24 shrink-0">{translatePlanet(l.planet, language)}</span>
            <span className={`px-2 py-0.5 rounded text-[10px] font-black uppercase shrink-0 ${l.planet === 'Sun' ? 'bg-amber-100 text-amber-700 border border-amber-300' : 'bg-blue-100 text-blue-700 border border-blue-300'}`}>
              {isHi ? (l.planet === 'Sun' ? 'सूर्य होरा' : 'चंद्र होरा') : `${l.planet} Hora`}
            </span>
            <span className="text-foreground text-xs leading-relaxed whitespace-normal break-words">{isHi ? l.meaning_hi : l.meaning_en}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function DrekkanaLordCard({ positions, language }: { positions: any[]; language: string }) {
  const isHi = language === 'hi';
  const lords = positions.filter((p: any) => p.drekkana_lord);
  if (!lords.length) return null;
  const TYPE_COLORS: Record<string, string> = {
    Ayudha: 'bg-orange-100 text-orange-800 border-orange-300',
    Pasa:   'bg-purple-100 text-purple-800 border-purple-300',
    Nagala: 'bg-gray-100 text-gray-700 border-gray-300',
    Sarpa:  'bg-green-100 text-green-800 border-green-300',
  };
  return (
    <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden mt-4">
      <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
        {isHi ? 'द्रेष्काण स्वामी और प्रकार (D3)' : 'Drekkana Lord & Decanate Type (D3)'}
      </div>
      <div className="p-0">
        <Table className="w-full text-xs table-fixed">
          <TableHeader>
            <TableRow>
              <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[18%]">{isHi ? 'ग्रह' : 'Planet'}</TableHead>
              <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[15%]">{isHi ? 'द्रेष्काण' : 'Decanate'}</TableHead>
              <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[15%]">{isHi ? 'स्वामी' : 'Lord'}</TableHead>
              <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[15%]">{isHi ? 'प्रकार' : 'Type'}</TableHead>
              <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[37%]">{isHi ? 'अर्थ' : 'Meaning'}</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {lords.map((p: any, i: number) => {
              const dl = p.drekkana_lord;
              const colorClass = TYPE_COLORS[dl.type] || 'bg-muted text-foreground';
              return (
                <TableRow key={i} className="border-t border-border/20 hover:bg-muted/5">
                  <TableCell className="p-2 font-bold">{translatePlanet(p.planet, language)}</TableCell>
                  <TableCell className="p-2">{dl.decanate}</TableCell>
                  <TableCell className="p-2 font-semibold text-primary">{translatePlanet(dl.lord, language)}</TableCell>
                  <TableCell className="p-2">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-black uppercase border ${colorClass}`}>
                      {dl.type}
                    </span>
                  </TableCell>
                  <TableCell className="p-2 text-xs text-foreground/80 whitespace-normal break-words max-w-0">{isHi ? dl.meaning_hi : dl.meaning_en}</TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}

function TrimsamshaLordCard({ positions, language }: { positions: any[]; language: string }) {
  const isHi = language === 'hi';
  const lords = positions.filter((p: any) => p.trimsamsha_lord);
  if (!lords.length) return null;
  return (
    <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden mt-4">
      <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
        {isHi ? 'त्रिंशांश स्वामी (D30)' : 'Trimsamsha Lord Significance (D30)'}
      </div>
      <div className="p-4 space-y-2">
        {lords.map((p: any, i: number) => (
          <div key={i} className="flex items-start gap-3 text-sm border-b border-border/20 pb-2 last:border-0">
            <span className="font-bold text-primary w-24 shrink-0">{translatePlanet(p.planet, language)}</span>
            <span className="px-2 py-0.5 rounded text-[10px] font-black uppercase bg-red-100 text-red-700 border border-red-300 shrink-0">
              {translatePlanet(p.trimsamsha_lord.lord, language)}
            </span>
            <span className="text-foreground text-xs leading-relaxed whitespace-normal break-words">{isHi ? p.trimsamsha_lord.meaning_hi : p.trimsamsha_lord.meaning_en}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

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
  handlePlanetClick, language, t,
}: DivisionalTabProps) {
  const ascFromHouses = (houses: any): string => {
    const list = Array.isArray(houses) ? houses : [];
    const h1 = list.find((h: any) => Number(h?.number) === 1);
    return String(h1?.sign || '').trim();
  };
  const toPlanetEntry = (p: any): PlanetEntry => ({
    planet: p.planet,
    sign: p.sign || p.current_sign || '',
    house: p.house,
    sign_degree: Number(p.sign_degree ?? p.degree ?? 0) || 0,
    status: typeof p.status === 'string' ? p.status : '',
    is_retrograde: !!p.is_retrograde,
    is_combust: !!p.is_combust,
    is_vargottama: !!p.is_vargottama,
    is_exalted: !!p.is_exalted,
    is_debilitated: !!p.is_debilitated,
  } as any);

  return (
    <div className="space-y-6">
      {/* Chart selector */}
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

          {/* Chart name / division header */}
          <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
            <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center justify-between">
              <span>{translateBackend(divisionalData.chart_name || divisionalData.chart_type, language)}</span>
              <span className="text-xs font-bold px-2 py-0.5 bg-white/20 rounded">D{divisionalData.division}</span>
            </div>
          </div>

          {/* Kundli Chart and Planet Table side by side */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">
            {/* Left: Kundli Chart */}
            {divisionalData.planet_positions && (
              <div className="flex justify-center">
                <div className="w-full max-w-[420px]">
                  <div className="w-full aspect-square">
                    <KundliChartSVG
                      planets={(divisionalData.planet_positions || []).map(toPlanetEntry)}
                      ascendantSign={
                        ascFromHouses(divisionalData.houses)
                        || divisionalData.chart_data?.ascendant?.sign
                        || divisionalData.ascendant?.sign
                        || (divisionalData.planet_positions || []).find((p: any) => p.planet === 'Lagna' || p.planet === 'Ascendant')?.sign
                        || ''
                      }
                      language={language}
                      className="w-full h-full"
                      showHouseNumbers={false}
                      showRashiNumbers
                      rashiNumberPlacement="corner"
                      showAscendantMarker={false}
                      onPlanetClick={(pl) => handlePlanetClick(pl as any)}
                    />
                  </div>
                </div>
              </div>
            )}

            {/* Right: Planet Table */}
            <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
              <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
                {t('table.planet')} — {t('table.sign')} / {t('table.degree')}
              </div>
              <Table className="w-full text-xs table-fixed">
                <TableHeader>
                  <TableRow>
                    <TableHead className="text-left p-3 text-primary font-semibold uppercase tracking-wide text-xs w-[40%]">{t('table.planet')}</TableHead>
                    <TableHead className="text-left p-3 text-primary font-semibold uppercase tracking-wide text-xs w-[35%]">{t('table.sign')}</TableHead>
                    <TableHead className="text-left p-3 text-primary font-semibold uppercase tracking-wide text-xs w-[25%]">{t('table.degree')}</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {Object.entries(divisionalData.planet_signs || {}).map(([planet, sign]: [string, any]) => {
                    const posData = (divisionalData.planet_positions || []).find((p: any) => p.planet === planet);
                    const isVargottama = posData?.is_vargottama;
                    return (
                      <TableRow key={planet} className={`border-t border-border hover:bg-muted/5 ${isVargottama ? 'bg-yellow-50/40' : ''}`}>
                        <TableCell className="p-3 text-foreground font-medium text-sm">
                          {translatePlanet(planet, language)}
                          {isVargottama && (
                            <span className="ml-1.5 px-1.5 py-0.5 rounded text-[9px] font-black bg-yellow-100 text-yellow-700 border border-yellow-300 uppercase tracking-tight">VGT</span>
                          )}
                        </TableCell>
                        <TableCell className="p-3 text-foreground text-sm">{translateSign(sign as string, language)}</TableCell>
                        <TableCell className="p-3 text-foreground text-sm">{posData?.sign_degree?.toFixed(1) || '--'}&deg;</TableCell>
                      </TableRow>
                    );
                  })}
                </TableBody>
              </Table>
            </div>
          </div>

          {/* D2 Hora Lord Significance */}
          {divisionalData.division === 2 && divisionalData.planet_positions && (
            <HoraLordCard positions={divisionalData.planet_positions} language={language} />
          )}

          {/* D3 Drekkana Lord & Type */}
          {divisionalData.division === 3 && divisionalData.planet_positions && (
            <DrekkanaLordCard positions={divisionalData.planet_positions} language={language} />
          )}

          {/* D30 Trimsamsha Lord */}
          {divisionalData.division === 30 && divisionalData.planet_positions && (
            <TrimsamshaLordCard positions={divisionalData.planet_positions} language={language} />
          )}

          {/* Varga Strength */}
          {divisionalData.varga_strength?.planets && (
            <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
              <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center justify-between">
                <span>{t('auto.vargaStrength')}</span>
                {divisionalData.varga_strength.sloka_ref && (
                  <span className="text-[10px] italic font-normal opacity-80">{divisionalData.varga_strength.sloka_ref}</span>
                )}
              </div>
              <div className="p-3">
                <p className="text-xs text-foreground/70 mb-3">{t('auto.vargaStrengthDesc')}</p>
                <Table className="w-full text-xs table-fixed">
                  <TableHeader>
                    <TableRow>
                      <TableHead className="text-left p-2.5 text-primary font-semibold uppercase tracking-wide w-[25%]">{t('table.planet')}</TableHead>
                      <TableHead className="text-center p-2.5 text-primary font-semibold uppercase tracking-wide w-[15%]">{t('auto.ownVargas')}</TableHead>
                      <TableHead className="text-left p-2.5 text-primary font-semibold uppercase tracking-wide w-[20%]">{t('auto.vargaTier')}</TableHead>
                      <TableHead className="text-left p-2.5 text-primary font-semibold uppercase tracking-wide w-[40%]">{language === 'hi' ? 'विवरण' : 'Description'}</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {Object.entries(divisionalData.varga_strength.planets).map(([planet, info]: [string, any]) => {
                      const tier = info.tier || {};
                      const tierName = language === 'hi' ? tier.name_hi : tier.name;
                      const tierDesc = language === 'hi' ? tier.description_hi : tier.description;
                      return (
                        <TableRow key={planet} className="border-t border-border/20 hover:bg-muted/5 transition-colors">
                          <TableCell className="p-2.5 text-foreground font-bold">{translatePlanet(planet, language)}</TableCell>
                          <TableCell className="p-2.5 text-center text-foreground font-mono">{info.count}/7</TableCell>
                          <TableCell className="p-2.5 text-primary font-bold italic">{tierName}</TableCell>
                          <TableCell className="p-2.5 text-foreground text-xs leading-relaxed whitespace-normal break-words max-w-0">{tierDesc}</TableCell>
                        </TableRow>
                      );
                    })}
                  </TableBody>
                </Table>
              </div>
            </div>
          )}

          {/* D60 Special Analysis */}
          {divisionalData.d60_analysis && (
            <div className="space-y-4">
              {/* D60 main header */}
              <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
                <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-3">
                  <span>{t('auto.d60ShashtiamsaKarmic')}</span>
                  <span className="text-[10px] px-2 py-0.5 bg-white/20 rounded uppercase font-bold tracking-tight">{t('auto.expert')}</span>
                </div>
              </div>

              {/* Birth Time Sensitivity */}
              {divisionalData.d60_analysis.birth_time_assessment && (
                <div className={`rounded-xl border p-4 ${
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
                    }`}>⚠</div>
                    <div className="flex-1">
                      <p className="font-semibold text-sm mb-1">
                        {t('auto.birthTimeAccuracy')}
                        <span className="ml-2 text-xs uppercase tracking-wider opacity-70">
                          ({divisionalData.d60_analysis.birth_time_assessment.confidence_level})
                        </span>
                      </p>
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
                <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
                  <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
                    {t('auto.karmicSummary')}
                  </div>
                  <div className="p-4 space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div className="bg-green-50 p-3 rounded-lg">
                        <div className="text-xs text-green-700 uppercase font-bold">{t('auto.punyaScoreBenefic')}</div>
                        <div className="text-2xl font-bold text-green-800">{divisionalData.d60_analysis.karmic_summary.punya_score}%</div>
                      </div>
                      <div className="bg-red-50 p-3 rounded-lg">
                        <div className="text-xs text-red-700 uppercase font-bold">{t('auto.papaScoreMalefic')}</div>
                        <div className="text-2xl font-bold text-red-800">{divisionalData.d60_analysis.karmic_summary.papa_score}%</div>
                      </div>
                    </div>
                    <p className="text-sm text-foreground leading-relaxed">
                      {language === 'hi'
                        ? divisionalData.d60_analysis.karmic_summary.overall_description?.hi
                        : divisionalData.d60_analysis.karmic_summary.overall_description?.en}
                    </p>
                    {divisionalData.d60_analysis.karmic_summary.life_purpose && (
                      <div className="p-3 bg-muted/10 rounded-lg border border-border/20">
                        <p className="text-sm font-semibold text-primary mb-1">
                          {t('auto.lifePurpose')}: {' '}
                          {language === 'hi'
                            ? divisionalData.d60_analysis.karmic_summary.life_purpose.primary_hi
                            : divisionalData.d60_analysis.karmic_summary.life_purpose.primary}
                        </p>
                        <p className="text-xs text-foreground whitespace-normal break-words">
                          {language === 'hi'
                            ? divisionalData.d60_analysis.karmic_summary.life_purpose.description_hi
                            : divisionalData.d60_analysis.karmic_summary.life_purpose.description}
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Planetary Karmic Analysis Table */}
              <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
                <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
                  {t('auto.planetWiseKarmicAnal')}
                </div>
                <Table className="w-full text-xs table-fixed">
                  <TableHeader>
                    <TableRow>
                      <TableHead className="text-left p-2.5 text-primary font-semibold uppercase tracking-wide w-[18%]">{t('table.planet')}</TableHead>
                      <TableHead className="text-center p-2.5 text-primary font-semibold uppercase tracking-wide w-[12%]">{t('auto.unit')}</TableHead>
                      <TableHead className="text-left p-2.5 text-primary font-semibold uppercase tracking-wide w-[18%]">{t('auto.sanskritName')}</TableHead>
                      <TableHead className="text-center p-2.5 text-primary font-semibold uppercase tracking-wide w-[12%]">{t('auto.nature')}</TableHead>
                      <TableHead className="text-left p-2.5 text-primary font-semibold uppercase tracking-wide w-[40%]">{t('auto.pastLifeTheme')}</TableHead>
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
                          <TableCell className="p-2.5 text-foreground font-bold">{translatePlanet(planet, language)}</TableCell>
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
                          <TableCell className="p-2.5 text-foreground text-xs leading-relaxed overflow-hidden whitespace-normal break-words">
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
                <div className="rounded-xl border border-red-200 bg-red-50 overflow-hidden">
                  <div className="bg-red-700 text-white px-4 py-2 text-[15px] font-semibold">
                    {t('auto.identifiedKarmicDebt')}
                  </div>
                  <div className="p-4 space-y-3">
                    {divisionalData.d60_analysis.karmic_summary.karmic_debts.map((debt: any, idx: number) => (
                      <div key={idx} className="bg-white p-3 rounded border border-red-100">
                        <p className="font-semibold text-sm text-red-700">
                          {language === 'hi' ? debt.debt_type_hi : debt.debt_type}
                        </p>
                        <p className="text-xs text-foreground mt-1">
                          <span className="font-semibold">{t('auto.planets')}</span>
                          {debt.planets_involved?.join(', ')}
                        </p>
                        <p className="text-xs text-foreground mt-1 whitespace-normal break-words">
                          {language === 'hi' ? debt.manifestation_hi : debt.manifestation}
                        </p>
                        <p className="text-xs text-green-700 mt-2 font-medium whitespace-normal break-words">
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
                <div className="rounded-xl border border-blue-200 bg-blue-50 overflow-hidden">
                  <div className="bg-blue-700 text-white px-4 py-2 text-[15px] font-semibold">
                    {t('auto.remedyAccessibility')}: {' '}
                    {language === 'hi'
                      ? divisionalData.d60_analysis.karmic_summary.remedy_accessibility.level_hi
                      : divisionalData.d60_analysis.karmic_summary.remedy_accessibility.level}
                  </div>
                  <div className="p-4">
                    <p className="text-sm text-foreground mb-3 whitespace-normal break-words">
                      {language === 'hi'
                        ? divisionalData.d60_analysis.karmic_summary.remedy_accessibility.description_hi
                        : divisionalData.d60_analysis.karmic_summary.remedy_accessibility.description}
                    </p>
                    {divisionalData.d60_analysis.karmic_summary.remedy_accessibility.recommendations?.length > 0 && (
                      <ul className="text-xs space-y-1">
                        {divisionalData.d60_analysis.karmic_summary.remedy_accessibility.recommendations.map((rec: any, idx: number) => (
                          <li key={idx} className="flex items-start gap-2 text-blue-800">
                            <span>•</span>
                            <span className="whitespace-normal break-words">{language === 'hi' ? rec.hi : rec.en}</span>
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>
                </div>
              )}

              {/* Footer Note */}
              <div className="p-3 bg-muted/10 rounded-lg border border-border/10 text-xs text-foreground italic leading-relaxed">
                {t('auto.AccordingToSageParas')}
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
