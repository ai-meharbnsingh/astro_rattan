import { useState, useEffect } from 'react';
import { Loader2, Target } from 'lucide-react';
import { api } from '@/lib/api';
import { translatePlanet, translateSign, translateSignAbbr } from '@/lib/backend-translations';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '@/components/ui/table';
import { Heading } from '@/components/ui/heading';

const ALL_SIGNS  = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces'];
const ALL_ABBR   = ['Ari','Tau','Gem','Can','Leo','Vir','Lib','Sco','Sag','Cap','Aqu','Pis'];
const ALL_HI     = ['मे','वृ','मि','कर','सिं','कन','तु','वृ','धन','मक','कु','मी'];

function rotateByLagna<T>(arr: T[], lagnaSign: string): T[] {
  const idx = ALL_SIGNS.indexOf(lagnaSign);
  if (idx <= 0) return arr;
  return [...arr.slice(idx), ...arr.slice(0, idx)];
}

function SAVKundliChart({ savData, language, lagnaSign, t }: { savData: Record<string, number>; language: string; lagnaSign: string; t: (key: string) => string }) {
  const signs    = rotateByLagna(ALL_SIGNS, lagnaSign);
  const signAbbr = rotateByLagna(ALL_ABBR,  lagnaSign);
  const hiAbbr   = rotateByLagna(ALL_HI,    lagnaSign);
  const housePos = [
    { x: 140, y: 66 },   // 1
    { x: 80,  y: 35 },   // 2
    { x: 32,  y: 78 },   // 3
    { x: 32,  y: 140 },  // 4
    { x: 32,  y: 202 },  // 5
    { x: 80,  y: 245 },  // 6
    { x: 140, y: 215 },  // 7
    { x: 200, y: 245 },  // 8
    { x: 248, y: 202 },  // 9
    { x: 248, y: 140 },  // 10
    { x: 248, y: 78 },   // 11
    { x: 200, y: 35 },   // 12
  ];
  const binduColor = (v: number) => v >= 28 ? '#166534' : '#991b1b';

  return (
    <div className="w-full max-w-[280px] mx-auto">
      <svg viewBox="0 0 280 280" className="w-full h-auto block">
        <rect x="2" y="2" width="276" height="276" fill="white" stroke="#c8a96e" strokeWidth="1.5"/>
        <line x1="2"   y1="2"   x2="278" y2="278" stroke="#c8a96e" strokeWidth="0.75"/>
        <line x1="278" y1="2"   x2="2"   y2="278" stroke="#c8a96e" strokeWidth="0.75"/>
        <line x1="140" y1="2"   x2="278" y2="140" stroke="#c8a96e" strokeWidth="0.75"/>
        <line x1="278" y1="140" x2="140" y2="278" stroke="#c8a96e" strokeWidth="0.75"/>
        <line x1="140" y1="278" x2="2"   y2="140" stroke="#c8a96e" strokeWidth="0.75"/>
        <line x1="2"   y1="140" x2="140" y2="2"   stroke="#c8a96e" strokeWidth="0.75"/>
        {housePos.map((pos, i) => {
          const val = savData[signs[i]] || 0;
          return (
            <g key={i}>
              <rect x={pos.x - 17} y={pos.y - 16} width="34" height="30" fill="white" rx="2" opacity="0.9"/>
              <text x={pos.x} y={pos.y - 4} textAnchor="middle" fontSize="9" fill="#8B7355" fontFamily="sans-serif">
                {language === 'hi' ? hiAbbr[i] : signAbbr[i]}
              </text>
              <text x={pos.x} y={pos.y + 10} textAnchor="middle" fontSize="15" fontWeight="bold" fill={binduColor(val)} fontFamily="sans-serif">
                {val}
              </text>
            </g>
          );
        })}
      </svg>
      <div className="flex justify-center gap-4 mt-2 text-xs">
        <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full bg-green-700"/>&ge;28 {t('auto.strong')}</span>
        <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full bg-red-700"/>&lt;28 {t('auto.weak')}</span>
      </div>
    </div>
  );
}

function HorasaraPhalaSection({ kundliId, language, t }: { kundliId: string; language: string; t: (key: string) => string }) {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    if (!kundliId) return;
    let cancelled = false;
    api.get<any>(`/api/kundli/${kundliId}/horasara-phala`)
      .then(res => { if (!cancelled) setData(res); })
      .catch(() => {});
    return () => { cancelled = true; };
  }, [kundliId]);

  if (!data) return null;

  // API returns: sav_sign_readings, planet_transit_readings, special_rules, sloka_ref
  const sr = data.special_rules || {};
  const assessment = language === 'hi'
    ? (sr.total_sav_assessment_hi || sr.total_sav_assessment_en)
    : sr.total_sav_assessment_en;
  const groupInterp = language === 'hi'
    ? (sr.group_interpretation_hi || sr.group_interpretation_en)
    : sr.group_interpretation_en;
  const planetReadings: any[] = data.planet_transit_readings || [];

  return (
    <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
      <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
        {language === 'hi' ? 'होरासार फल' : 'Horasara Phala'}
      </div>
      <div className="p-5">
        {assessment && (
          <p className="text-xs text-foreground/90 leading-relaxed mb-3">{assessment}</p>
        )}
        {groupInterp && (
          <div className="mb-4 flex items-start gap-2 text-xs">
            <span className="text-green-600 mt-0.5">✓</span>
            <span className="text-foreground/90">{groupInterp}</span>
          </div>
        )}
        {planetReadings.length > 0 && (
          <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
            <Table className="w-full text-xs table-fixed">
              <TableHeader>
                <TableRow>
                  <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[18%]">{t('table.planet')}</TableHead>
                  <TableHead className="text-center p-2 text-primary font-semibold uppercase tracking-wide w-[14%]">{language === 'hi' ? 'राशि' : 'Sign'}</TableHead>
                  <TableHead className="text-center p-2 text-primary font-semibold uppercase tracking-wide w-[12%]">{language === 'hi' ? 'बिंदु' : 'Bindus'}</TableHead>
                  <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[56%]">{language === 'hi' ? 'फल' : 'Reading'}</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {planetReadings.map((row: any, i: number) => (
                  <TableRow key={i} className="border-t border-border hover:bg-muted/5 align-top">
                    <TableCell className="p-2 font-medium text-foreground">{translatePlanet(row.planet, language)}</TableCell>
                    <TableCell className="p-2 text-center text-foreground">{translateSign(row.transit_sign, language)}</TableCell>
                    <TableCell className="p-2 text-center">
                      <span className={`inline-block px-2 py-0.5 rounded text-xs font-bold ${(row.bav_bindus || 0) >= 4 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                        {row.bav_bindus}
                        <span className="ml-1 font-normal opacity-70">{(row.bav_bindus || 0) >= 4 ? '▲' : '▼'}</span>
                      </span>
                    </TableCell>
                    <TableCell className="p-2 text-muted-foreground whitespace-normal break-words max-w-0">
                      {language === 'hi' ? (row.interpretation_hi || row.interpretation_en) : row.interpretation_en}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        )}
      </div>
    </div>
  );
}

interface AshtakvargaTabProps {
  ashtakvargaData: any;
  loadingAshtakvarga: boolean;
  result: any;
  language: string;
  t: (key: string) => string;
}

export default function AshtakvargaTab(props: AshtakvargaTabProps) {
  const { ashtakvargaData, loadingAshtakvarga, result, language, t } = props;

  const lagnaSign      = result?.chart_data?.ascendant?.sign || 'Aries';
  const signs          = rotateByLagna(ALL_SIGNS, lagnaSign);
  const signAbbr       = rotateByLagna(ALL_ABBR,  lagnaSign);
  const hindiSignAbbr  = rotateByLagna(ALL_HI,    lagnaSign);

  return (
    <>
      {loadingAshtakvarga ? (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="w-6 h-6 animate-spin text-primary" />
          <span className="ml-2 text-foreground">{t('kundli.loadingAshtakvarga')}</span>
        </div>
      ) : ashtakvargaData ? (
        <div className="space-y-6">
          {/* Page heading */}
          <div>
            <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
              <Target className="w-6 h-6" />
              {language === 'hi' ? 'अष्टकवर्ग' : 'Ashtakvarga'}
            </Heading>
            <p className="text-sm text-muted-foreground">
              {language === 'hi' ? 'प्रति राशि 8 संवेदनशील बिंदुओं में ग्रहीय शक्ति स्कोर' : 'Planetary strength scores across 8 sensitive points per sign'}
            </p>
          </div>

          {/* SAV Kundli Chart + SAV Bar Chart — side by side */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

            {/* SAV Kundli Chart */}
            <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
              <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
                {t('section.sarvashtakvarga')} {t('kundli.chart')}
              </div>
              <div className="p-5">
                <SAVKundliChart
                  savData={ashtakvargaData.sarvashtakvarga || {}}
                  language={language}
                  lagnaSign={result?.chart_data?.ascendant?.sign || 'Aries'}
                  t={t}
                />
                <p className="text-xs text-center text-foreground mt-2">{t('ashtakvarga.savDescription')}</p>
              </div>
            </div>

            {/* SAV Bar Chart */}
            <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
              <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
                {t('section.sarvashtakvarga')}
              </div>
              <div className="p-5">
                <div className="overflow-x-auto">
                  <div className="flex items-end gap-2 h-48 min-w-[400px]">
                    {signs.map((sign) => {
                      const points = ashtakvargaData.sarvashtakvarga?.[sign] || 0;
                      const maxPoints = 56;
                      const heightPct = Math.round((points / maxPoints) * 100);
                      const isStrong = points >= 28;
                      return (
                        <div key={sign} className="flex-1 flex flex-col items-center gap-1">
                          <span className="text-sm font-medium text-foreground">{points}</span>
                          <div className="w-full bg-muted rounded-t-md relative h-[140px]">
                            <div
                              className="absolute bottom-0 w-full rounded-t-md transition-all"
                              style={{
                                height: `${heightPct}%`,
                                backgroundColor: isStrong ? 'var(--aged-gold-dim)' : 'var(--ink-light)',
                              }}
                            />
                          </div>
                          <span className="text-xs text-foreground truncate w-full text-center" title={translateSign(sign, language)}>
                            {translateSignAbbr(sign, language)}
                          </span>
                        </div>
                      );
                    })}
                  </div>
                </div>
                <div className="flex items-center gap-4 mt-3 text-xs text-foreground">
                  <div className="flex items-center gap-1">
                    <div className="w-3 h-3 rounded" style={{ backgroundColor: 'var(--aged-gold-dim)' }} />
                    <span>{t('kundli.strong')} (&ge;28)</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <div className="w-3 h-3 rounded" style={{ backgroundColor: 'var(--ink-light)' }} />
                    <span>{t('kundli.weak')} (&lt;28)</span>
                  </div>
                </div>

                {/* SAV Grand Total */}
                {(() => {
                  const savTotal = Object.values(ashtakvargaData.sarvashtakvarga as Record<string, number>).reduce((a, b) => a + b, 0);
                  const isAbove = savTotal >= 337;
                  const isAvg   = savTotal >= 300 && savTotal < 337;
                  const totalColor = isAbove ? 'text-green-700' : isAvg ? 'text-amber-600' : 'text-red-700';
                  const totalBg    = isAbove ? 'bg-green-50 border-green-200' : isAvg ? 'bg-amber-50 border-amber-200' : 'bg-red-50 border-red-200';
                  const note = isAbove
                    ? (language === 'hi' ? 'औसत से ऊपर — जीवन-शक्ति सबल है' : 'Above average — strong overall life force')
                    : isAvg
                      ? (language === 'hi' ? 'औसत — संतुलित क्षमता' : 'Average — balanced potential')
                      : (language === 'hi' ? 'औसत से कम — केंद्रित उपाय आवश्यक' : 'Below average — requires focused remedies');
                  return (
                    <div className={`mt-4 flex flex-wrap items-center gap-3 rounded-lg border px-4 py-3 ${totalBg}`}>
                      <span className="text-sm font-semibold text-foreground/80">
                        {language === 'hi' ? 'SAV कुल' : 'SAV Total'}:
                      </span>
                      <span className={`text-xl font-bold ${totalColor}`}>{savTotal}</span>
                      <span className="text-xs text-foreground/60">/ 337 {language === 'hi' ? 'औसत' : 'avg'}</span>
                      <span className={`text-xs font-medium ml-1 ${totalColor}`}>{note}</span>
                    </div>
                  );
                })()}
              </div>
            </div>
          </div>

          {/* Bhinna Ashtakvarga Charts */}
          <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
            <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
              {t('auto.bhinnaAshtakvargaCha')}
            </div>
            <div className="p-5">
              <p className="text-sm text-muted-foreground mb-1">{t('auto.individualPlanetBind')} (Parashara Light format)</p>
              <p className="text-xs text-violet-700 bg-violet-50 border border-violet-200 rounded px-3 py-1.5 mb-4">
                ◈ <strong>{language === 'hi' ? 'काक्षा क्रम' : 'Kaksha Order'}</strong>: {language === 'hi' ? 'प्रत्येक पंक्ति एक काक्षा (3°45\') है — शनि→गुरु→मंगल→सूर्य→शुक्र→बुध→चंद्र→लग्न क्रम में। यदि काक्षाधिपति ने बिंदु दिया तो वह काक्षा गोचर के लिए अनुकूल है।' : 'Each row is one Kaksha (3°45\' sub-zone of the sign) in classical order: Saturn→Jupiter→Mars→Sun→Venus→Mercury→Moon→Lagna. A ✓ means the Kaksha lord granted a bindu — transit through that Kaksha is favorable.'}
              </p>
              <div className="grid grid-cols-1 gap-5">
                {['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Lagna'].map((planet) => {
                  const bindus = ashtakvargaData.planet_bindus?.[planet] || {};
                  const vals = signs.map((s) => bindus[s] || 0);
                  const total = vals.reduce((sum, v) => sum + v, 0);

                  const binduColor = (v: number) =>
                    v >= 5 ? '#166534' : v >= 3 ? '#B8860B' : '#991b1b';
                  const binduBg = (v: number) =>
                    v >= 5 ? '#dcfce7' : v >= 3 ? '#fef3c7' : '#fee2e2';

                  const housePos: { x: number; y: number }[] = [
                    { x: 140, y: 66 },
                    { x: 80,  y: 35 },
                    { x: 32,  y: 78 },
                    { x: 32,  y: 140 },
                    { x: 32,  y: 202 },
                    { x: 80,  y: 245 },
                    { x: 140, y: 215 },
                    { x: 200, y: 245 },
                    { x: 248, y: 202 },
                    { x: 248, y: 140 },
                    { x: 248, y: 78 },
                    { x: 200, y: 35 },
                  ];

                  return (
                    <div key={planet} className="bg-transparent rounded-lg border border-sacred-gold/20 overflow-hidden">
                      {/* Planet header */}
                      <div className="bg-sacred-gold-dark text-white px-4 py-2 flex items-center justify-between">
                        <span className="text-sm font-semibold">{translatePlanet(planet, language)}</span>
                        <span className="text-sm font-semibold">{t('auto.total')}: {total}</span>
                      </div>
                      <div className="flex flex-col lg:flex-row">
                        {/* LEFT: Full contributor matrix table */}
                        <div className="flex-1 overflow-x-auto p-3">
                          {(() => {
                            const kakshaOrder = ['Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury', 'Moon', 'Lagna'];
                            const contribData = ashtakvargaData.planet_details?.[planet]?.contributors;
                            return (
                              <Table className="w-full text-xs border-collapse">
                                <TableHeader>
                                  <TableRow>
                                    <TableHead className="text-center p-1 text-violet-700 font-bold border-b border-border w-8 text-xs">K#</TableHead>
                                    <TableHead className="text-left p-1 text-primary font-semibold border-b border-border whitespace-nowrap">{t('auto.contributor')}</TableHead>
                                    {signs.map((s, i) => (
                                      <TableHead key={i} className="text-center p-1 text-primary font-semibold border-b border-border min-w-[26px] text-xs">
                                        {language === 'hi' ? hindiSignAbbr[i] : signAbbr[i]}
                                      </TableHead>
                                    ))}
                                    <TableHead className="text-center p-1 text-primary font-bold border-b border-border">&Sigma;</TableHead>
                                  </TableRow>
                                </TableHeader>
                                <TableBody>
                                  {kakshaOrder.map((contrib, kIdx) => {
                                    const row = contribData?.[contrib] || {};
                                    const rowVals = signs.map((s) => row[s] || 0);
                                    const rowTotal = rowVals.reduce((a, b) => a + b, 0);
                                    return (
                                      <TableRow key={contrib} className="border-t border-border hover:bg-violet-50/30">
                                        <TableCell className="text-center p-1">
                                          <span className="inline-block w-5 h-5 leading-5 rounded-full bg-violet-100 text-violet-700 text-[10px] font-bold">{kIdx + 1}</span>
                                        </TableCell>
                                        <TableCell className="p-1 text-foreground font-medium whitespace-nowrap">{translatePlanet(contrib, language)}</TableCell>
                                        {rowVals.map((v, i) => (
                                          <TableCell key={i} className="text-center p-1">
                                            <span className={`inline-block w-5 h-5 leading-5 rounded-sm text-xs font-semibold ${v === 1 ? 'bg-green-100 text-green-800' : 'text-muted-foreground'}`}>
                                              {v === 1 ? '✓' : '–'}
                                            </span>
                                          </TableCell>
                                        ))}
                                        <TableCell className="text-center p-1 font-semibold text-foreground">{rowTotal}</TableCell>
                                      </TableRow>
                                    );
                                  })}
                                  {/* Bindu total row */}
                                  <TableRow className="border-t-2 border-border bg-muted">
                                    <TableCell className="p-1 text-primary font-bold whitespace-nowrap" colSpan={2}>{t('auto.bindu')}</TableCell>
                                    {vals.map((v, i) => (
                                      <TableCell key={i} className="text-center p-1">
                                        <span
                                          className="inline-block w-6 h-6 leading-6 rounded text-sm font-bold"
                                          style={{ backgroundColor: binduBg(v), color: binduColor(v) }}
                                        >
                                          {v}
                                        </span>
                                      </TableCell>
                                    ))}
                                    <TableCell className="text-center p-1 font-bold text-foreground">{total}</TableCell>
                                  </TableRow>
                                </TableBody>
                              </Table>
                            );
                          })()}
                        </div>
                        {/* RIGHT: North Indian diamond chart SVG */}
                        <div className="flex-shrink-0 flex items-center justify-center p-4 lg:border-l border-t lg:border-t-0 border-border">
                          <svg viewBox="0 0 280 280" className="w-full max-w-[280px] h-auto block">
                            <rect x="2" y="2" width="276" height="276" fill="none" stroke="#c8a96e" strokeWidth="1.5" />
                            <line x1="2" y1="2" x2="278" y2="278" stroke="#c8a96e" strokeWidth="0.75" />
                            <line x1="278" y1="2" x2="2" y2="278" stroke="#c8a96e" strokeWidth="0.75" />
                            <line x1="140" y1="2" x2="278" y2="140" stroke="#c8a96e" strokeWidth="0.75" />
                            <line x1="278" y1="140" x2="140" y2="278" stroke="#c8a96e" strokeWidth="0.75" />
                            <line x1="140" y1="278" x2="2" y2="140" stroke="#c8a96e" strokeWidth="0.75" />
                            <line x1="2" y1="140" x2="140" y2="2" stroke="#c8a96e" strokeWidth="0.75" />
                            {housePos.map((pos, i) => (
                              <g key={i}>
                                <rect x={pos.x - 17} y={pos.y - 16} width="34" height="30" fill="white" rx="2" opacity="0.9"/>
                                <text x={pos.x} y={pos.y - 4} textAnchor="middle" fontSize="9" fill="#8B7355" fontFamily="sans-serif">
                                  {language === 'hi' ? hindiSignAbbr[i] : signAbbr[i]}
                                </text>
                                <text x={pos.x} y={pos.y + 10} textAnchor="middle" fontSize="14" fontWeight="bold" fill={binduColor(vals[i])} fontFamily="sans-serif">
                                  {vals[i]}
                                </text>
                              </g>
                            ))}
                          </svg>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
              {/* Color legend */}
              <div className="flex items-center gap-4 mt-4 text-xs text-foreground">
                <div className="flex items-center gap-1">
                  <div className="w-3 h-3 rounded border" style={{ backgroundColor: '#dcfce7', borderColor: '#86efac' }} />
                  <span>{t('auto.58Strong')}</span>
                </div>
                <div className="flex items-center gap-1">
                  <div className="w-3 h-3 rounded border" style={{ backgroundColor: '#fef3c7', borderColor: '#fcd34d' }} />
                  <span>{t('auto.34Medium')}</span>
                </div>
                <div className="flex items-center gap-1">
                  <div className="w-3 h-3 rounded border" style={{ backgroundColor: '#fee2e2', borderColor: '#fca5a5' }} />
                  <span>{t('auto.02Weak')}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Bhinnashtakvarga summary table */}
          <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
            <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
              {t('section.bhinnashtakvarga')}
            </div>
            <div className="overflow-x-auto">
              <Table className="w-full text-xs">
                <TableHeader>
                  <TableRow>
                    <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide sticky left-0 bg-background z-10">{t('table.planet')}</TableHead>
                    {signs.map((s) => (
                      <TableHead key={s} className="text-center p-2 text-primary font-semibold text-xs min-w-[32px]">{translateSignAbbr(s, language)}</TableHead>
                    ))}
                    <TableHead className="text-center p-2 text-primary font-semibold uppercase tracking-wide">{t('table.total')}</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'].map((planet) => {
                    const bindus = ashtakvargaData.planet_bindus?.[planet] || {};
                    const total = signs.reduce((sum, s) => sum + (bindus[s] || 0), 0);
                    return (
                      <TableRow key={planet} className="border-t border-border hover:bg-muted/5">
                        <TableCell className="p-2 text-foreground font-medium sticky left-0 bg-background z-10">{translatePlanet(planet, language)}</TableCell>
                        {signs.map((s) => {
                          const val = bindus[s] || 0;
                          return (
                            <TableCell key={s} className="text-center p-2">
                              <span className={`inline-block w-6 h-6 rounded text-xs leading-6 ${val >= 5 ? 'bg-primary text-white font-bold' : val <= 2 ? 'bg-red-10 text-wax-red-deep' : 'text-foreground'}`}>
                                {val}
                              </span>
                            </TableCell>
                          );
                        })}
                        <TableCell className="text-center p-2 font-semibold text-foreground">{total}</TableCell>
                      </TableRow>
                    );
                  })}
                </TableBody>
              </Table>
            </div>
          </div>

          {/* Purified Points */}
          <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
            <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
              {t('ashtakvarga.purifiedPoints')}
            </div>
            <div className="p-5">
              <p className="text-xs text-muted-foreground mb-4">{t('ashtakvarga.purificationDesc')}</p>
              <div className="space-y-8">
                {['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'].map((planet) => {
                  const purified = ashtakvargaData.purified?.[planet];
                  if (!purified) return null;

                  return (
                    <div key={planet} className="bg-transparent rounded-lg border border-sacred-gold/20 overflow-hidden">
                      <div className="bg-sacred-gold-dark text-white px-4 py-2 flex items-center justify-between">
                        <span className="text-sm font-semibold">{translatePlanet(planet, language)} — {t('ashtakvarga.purifiedPoints')}</span>
                        <span className="text-xs font-semibold">
                          {t('ashtakvarga.shodhyaPinda')}: <span className="text-lg font-bold">{purified.shodhya_pinda}</span>
                        </span>
                      </div>
                      <div className="overflow-x-auto p-3">
                        <Table className="w-full text-xs border-collapse">
                          <TableHeader>
                            <TableRow>
                              <TableHead className="text-left p-1 text-primary font-semibold border-b border-border whitespace-nowrap">{t('auto.process')}</TableHead>
                              {signs.map((s, i) => (
                                <TableHead key={i} className="text-center p-1 text-primary font-semibold border-b border-border min-w-[26px] text-xs">
                                  {translateSignAbbr(s, language)}
                                </TableHead>
                              ))}
                            </TableRow>
                          </TableHeader>
                          <TableBody>
                            <TableRow className="border-t border-border hover:bg-muted/5">
                              <TableCell className="p-1 text-foreground font-medium whitespace-nowrap">{t('ashtakvarga.trikonaShodhana')}</TableCell>
                              {signs.map((s, i) => (
                                <TableCell key={i} className="text-center p-1 text-foreground font-semibold">
                                  {purified.trikona[s]}
                                </TableCell>
                              ))}
                            </TableRow>
                            <TableRow className="border-t border-border hover:bg-muted/5 bg-muted/5">
                              <TableCell className="p-1 text-foreground font-bold whitespace-nowrap">{t('ashtakvarga.ekadhipatyaShodhana')}</TableCell>
                              {signs.map((s, i) => (
                                <TableCell key={i} className="text-center p-1">
                                  <span className="inline-block w-6 h-6 leading-6 rounded text-xs font-bold bg-muted/20 text-primary">
                                    {purified.ekadhipatya[s]}
                                  </span>
                                </TableCell>
                              ))}
                            </TableRow>
                          </TableBody>
                        </Table>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>

          {/* Horasara Phala */}
          {(ashtakvargaData.kundli_id || result?.id) && (
            <HorasaraPhalaSection kundliId={ashtakvargaData.kundli_id || result?.id} language={language} t={t} />
          )}

          {/* Ashtakvarga Theory Section — General educational summary */}
          <AshtakvargaTheorySection language={language} />

        </div>
      ) : (
        <p className="text-center text-foreground py-8">{t('kundli.clickAshtakvargaTab')}</p>
      )}
    </>
  );
}

function AshtakvargaTheorySection({ language }: { language: string }) {
  const hi = language === 'hi';
  const l = (en: string, hiStr: string) => (hi ? hiStr : en);

  return (
    <div className="mt-12 space-y-6 pb-10">
      <div className="rounded-xl border border-sacred-gold/30 bg-sacred-gold/5 p-6 overflow-hidden">
        <Heading as={3} variant={3} className="text-sacred-gold-dark mb-4 flex items-center gap-2">
          <Target className="w-5 h-5" />
          {l('Understanding Ashtakvarga (The Points System)', 'अष्टकवर्ग को समझना (अंक प्रणाली)')}
        </Heading>
        
        <p className="text-sm text-foreground/80 mb-6 leading-relaxed">
          {l(
            'Ashtakvarga is a unique numerical system in Vedic Astrology that measures the strength of houses and planets using "Bindus" (points). Think of it as a "Vedic Scorecard" that tells you which areas of your life have the most supporting energy.',
            'अष्टकवर्ग वैदिक ज्योतिष में एक अद्वितीय संख्यात्मक प्रणाली है जो "बिंदु" (अंकों) का उपयोग करके भावों और ग्रहों की शक्ति को मापती है। इसे एक "वैदिक स्कोरकार्ड" के रूप में सोचें जो आपको बताता है कि आपके जीवन के किन क्षेत्रों में सबसे अधिक सहायक ऊर्जा है।'
          )}
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* SAV Section */}
          <div className="space-y-3">
            <h4 className="text-sm font-bold text-primary border-b border-sacred-gold/20 pb-1.5 uppercase tracking-wide">
              {l('Sarvashtakvarga (SAV) — The Total Score', 'सर्वाष्टकवर्ग (SAV) — कुल स्कोर')}
            </h4>
            <div className="space-y-4">
              <p className="text-xs text-foreground/70 leading-relaxed">
                {l('SAV is the total energy of a house from all 7 planets + Lagna. It shows the collective strength of a specific sign in your life.', 'SAV सभी 7 ग्रहों + लग्न से एक भाव की कुल ऊर्जा है। यह आपके जीवन में एक विशिष्ट राशि की सामूहिक शक्ति को दर्शाता है।')}
              </p>
              <div className="text-xs bg-white/40 p-3 rounded border border-sacred-gold/10">
                <span className="font-bold text-sacred-gold-dark">{l('The Magic Number 28:', 'जादुई संख्या 28:')}</span>{' '}
                <span className="text-foreground/70">{l('A house with 28 or more points is considered strong and capable of giving good results. Less than 28 points suggests areas where you may need more effort.', '28 या उससे अधिक अंकों वाले भाव को मजबूत माना जाता है और यह अच्छे परिणाम देने में सक्षम होता है। 28 से कम अंक उन क्षेत्रों का सुझाव देते हैं जहाँ आपको अधिक प्रयास की आवश्यकता हो सकती है।')}</span>
              </div>
            </div>
          </div>

          {/* BAV Section */}
          <div className="space-y-3">
            <h4 className="text-sm font-bold text-primary border-b border-sacred-gold/20 pb-1.5 uppercase tracking-wide">
              {l('Bhinnashtakvarga (BAV) — Individual Score', 'भिन्नाष्टकवर्ग (BAV) — व्यक्तिगत स्कोर')}
            </h4>
            <div className="space-y-4">
              <p className="text-xs text-foreground/70 leading-relaxed">
                {l('BAV shows the strength of an individual planet in each sign. It helps in predicting how a specific planet will behave during its transit.', 'BAV प्रत्येक राशि में एक व्यक्तिगत ग्रह की शक्ति को दर्शाता है। यह भविष्यवाणी करने में मदद करता है कि एक विशिष्ट ग्रह अपने गोचर के दौरान कैसा व्यवहार करेगा।')}
              </p>
              <div className="text-xs bg-white/40 p-3 rounded border border-sacred-gold/10">
                <span className="font-bold text-sacred-gold-dark">{l('The Magic Number 4:', 'जादुई संख्या 4:')}</span>{' '}
                <span className="text-foreground/70">{l('For an individual planet, 4 points is average. 5-8 points make the planet very powerful in that sign, while 0-3 points make it weak.', 'एक व्यक्तिगत ग्रह के लिए, 4 अंक औसत है। 5-8 अंक उस राशि में ग्रह को बहुत शक्तिशाली बनाते हैं, जबकि 0-3 अंक उसे कमजोर बनाते हैं।')}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Practical Use */}
        <div className="mt-8 p-4 bg-sacred-gold-dark/[0.03] rounded-lg border border-sacred-gold/20">
          <h4 className="text-xs font-bold text-sacred-gold-dark uppercase mb-2">{l('How to use this data?', 'इसका उपयोग कैसे करें?')}</h4>
          <p className="text-xs text-foreground/80 leading-relaxed italic">
            {l(
              'Look at your 10th House (Career) and 11th House (Gains). If they have high SAV scores (30+), you will find it easier to succeed in professional life. When a planet like Jupiter transits through a sign where it has 6 BAV points, it will bring exceptionally lucky results.',
              'अपने 10वें भाव (करियर) और 11वें भाव (लाभ) को देखें। यदि उनके पास उच्च SAV स्कोर (30+) हैं, तो आपको पेशेवर जीवन में सफल होना आसान लगेगा। जब बृहस्पति जैसा ग्रह उस राशि से गुजरता है जहाँ उसके 6 BAV अंक होते हैं, तो वह असाधारण रूप से भाग्यशाली परिणाम लाएगा।'
            )}
          </p>
        </div>

        <div className="mt-8 pt-4 border-t border-sacred-gold/20">
          <p className="text-[11px] text-foreground/50 italic text-center">
            {l(
              'Note: High points provide a "safety net," but the actual event still depends on your current Dasha period.',
              'नोट: उच्च अंक एक "सुरक्षा जाल" प्रदान करते हैं, लेकिन वास्तविक घटना अभी भी आपकी वर्तमान दशा अवधि पर निर्भर करती है।'
            )}
          </p>
        </div>
      </div>
    </div>
  );
}
