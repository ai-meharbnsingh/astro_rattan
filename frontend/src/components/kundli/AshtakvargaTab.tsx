import { useState, useEffect } from 'react';
import { Loader2 } from 'lucide-react';
import { api } from '@/lib/api';
import { translatePlanet, translateSign, translateSignAbbr } from '@/lib/backend-translations';
import GeneralRemedies from './GeneralRemedies';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell, TableCaption, TableFooter } from '@/components/ui/table';
import { Heading } from '@/components/ui/heading';

const ALL_SIGNS  = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces'];
const ALL_ABBR   = ['Ari','Tau','Gem','Can','Leo','Vir','Lib','Sco','Sag','Cap','Aqu','Pis'];
const ALL_HI     = ['मे','वृ','मि','कर','सिं','कन','तु','वृ','धन','मक','कु','मी'];

// Rotate array so lagnaSign is first (H1 = Lagna in North Indian chart)
function rotateByLagna<T>(arr: T[], lagnaSign: string): T[] {
  const idx = ALL_SIGNS.indexOf(lagnaSign);
  if (idx <= 0) return arr;
  return [...arr.slice(idx), ...arr.slice(0, idx)];
}

// SAV Kundli Chart — North Indian diamond SVG with Lagna at H1
function SAVKundliChart({ savData, language, lagnaSign, t }: { savData: Record<string, number>; language: string; lagnaSign: string; t: (key: string) => string }) {
  const signs    = rotateByLagna(ALL_SIGNS, lagnaSign);
  const signAbbr = rotateByLagna(ALL_ABBR,  lagnaSign);
  const hiAbbr   = rotateByLagna(ALL_HI,    lagnaSign);
  // Fixed 12-house outer-ring mapping (Aries..Pisces, 1..12):
  // 1 top-center, 2 top-left, 3 left-top, 4 left-center, 5 left-bottom, 6 bottom-left,
  // 7 bottom-center, 8 bottom-right, 9 right-bottom, 10 right-center, 11 right-top, 12 top-right.
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
        {/* outer square */}
        <rect x="2" y="2" width="276" height="276" fill="white" stroke="#c8a96e" strokeWidth="1.5"/>
        {/* diagonal lines */}
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

  const assessment = language === 'hi'
    ? (data.overall_assessment_hi || data.overall_assessment_en)
    : data.overall_assessment_en;
  const triggeredRules = (data.special_rules || []).filter((r: any) => r.triggered);
  const planetReadings = data.planet_bav_readings || [];

  return (
    <div className="bg-muted rounded-xl p-5 border border-border">
      <Heading as={4} variant={4} className="mb-3">
        {language === 'hi' ? 'होरासार फल' : 'Horasara Phala'}
      </Heading>
      {assessment && (
        <p className="text-sm text-foreground/90 leading-relaxed mb-4">{assessment}</p>
      )}
      {triggeredRules.length > 0 && (
        <div className="mb-4">
          <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-2">
            {language === 'hi' ? 'विशेष योग' : 'Special Rules Triggered'}
          </p>
          <div className="space-y-1">
            {triggeredRules.map((rule: any, i: number) => (
              <div key={i} className="flex items-start gap-2 text-sm">
                <span className="text-green-600 mt-0.5">✓</span>
                <span className="text-foreground/90">
                  {language === 'hi' ? (rule.description_hi || rule.description_en) : rule.description_en}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
      {planetReadings.length > 0 && (
        <div className="overflow-x-auto">
          <Table className="w-full text-sm">
            <TableHeader>
              <TableRow className="border-b border-border">
                <TableHead className="text-left p-2 text-primary font-medium">{t('table.planet')}</TableHead>
                <TableHead className="text-center p-2 text-primary font-medium">House</TableHead>
                <TableHead className="text-center p-2 text-primary font-medium">Bindus</TableHead>
                <TableHead className="text-left p-2 text-primary font-medium">Reading</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {planetReadings.map((row: any, i: number) => (
                <TableRow key={i} className="border-t border-border hover:bg-muted/5">
                  <TableCell className="p-2 font-medium text-foreground">{translatePlanet(row.planet, language)}</TableCell>
                  <TableCell className="p-2 text-center text-foreground">{row.house}</TableCell>
                  <TableCell className="p-2 text-center">
                    <span className={`inline-block px-2 py-0.5 rounded text-xs font-bold ${row.bindus >= 28 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                      {row.bindus}
                      <span className="ml-1 font-normal opacity-70">{row.bindus >= 28 ? '▲' : '▼'}</span>
                    </span>
                  </TableCell>
                  <TableCell className="p-2 text-muted-foreground text-xs">
                    {language === 'hi' ? (row.reading_hi || row.reading_en) : row.reading_en}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      )}
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

  // Derive Lagna-rotated sign arrays once — used by every chart/table in this tab
  // ascendant is an object {sign, longitude} — extract .sign
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
          {/* SAV Chart — Custom North Indian style with large bindu numbers */}
          <div className="bg-muted rounded-xl p-5 border border-border">
            <Heading as={4} variant={4} className="mb-4">{t('section.sarvashtakvarga')} {t('kundli.chart')}</Heading>
            <SAVKundliChart savData={ashtakvargaData.sarvashtakvarga || {}} language={language} lagnaSign={result?.chart_data?.ascendant?.sign || 'Aries'} t={t} />
            <p className="text-sm text-center text-foreground mt-2">{t('ashtakvarga.savDescription')}</p>
          </div>

          {/* SAV Bar Chart */}
          <div className="bg-muted rounded-xl p-5 border border-border">
            <Heading as={4} variant={4} className="mb-4">{t('section.sarvashtakvarga')}</Heading>
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
                    <span className="text-sm text-foreground truncate w-full text-center" title={translateSign(sign, language)}>
                      {translateSignAbbr(sign, language)}
                    </span>
                  </div>
                );
              })}
            </div>
            </div>
            <div className="flex items-center gap-4 mt-3 text-sm text-foreground">
              <div className="flex items-center gap-1">
                <div className="w-3 h-3 rounded" style={{ backgroundColor: 'var(--aged-gold-dim)' }} />
                <span>{t('kundli.strong')} (&ge;28)</span>
              </div>
              <div className="flex items-center gap-1">
                <div className="w-3 h-3 rounded" style={{ backgroundColor: 'var(--ink-light)' }} />
                <span>{t('kundli.weak')} (&lt;28)</span>
              </div>
            </div>
          </div>

          {/* Bhinna Ashtakvarga Charts — Parashara's Light format: table + diamond chart per planet */}
          <div className="bg-muted rounded-xl p-5 border border-border">
            <Heading as={4} variant={4} className="mb-2">{t('auto.bhinnaAshtakvargaCha')}</Heading>
            <p className="text-sm text-muted-foreground mb-4">{t('auto.individualPlanetBind')} (Parashara Light format)</p>
            <div className="grid grid-cols-1 gap-5">
              {['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Lagna'].map((planet) => {
                const bindus = ashtakvargaData.planet_bindus?.[planet] || {};
                const vals = signs.map((s) => bindus[s] || 0);
                const total = vals.reduce((sum, v) => sum + v, 0);

                const binduColor = (v: number) =>
                  v >= 5 ? '#166534' : v >= 3 ? '#B8860B' : '#991b1b';
                const binduBg = (v: number) =>
                  v >= 5 ? '#dcfce7' : v >= 3 ? '#fef3c7' : '#fee2e2';

                // Fixed 12-house outer-ring mapping (Aries..Pisces, 1..12):
                // 1 top-center, 2 top-left, 3 left-top, 4 left-center, 5 left-bottom, 6 bottom-left,
                // 7 bottom-center, 8 bottom-right, 9 right-bottom, 10 right-center, 11 right-top, 12 top-right.
                const housePos: { x: number; y: number }[] = [
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

                return (
                  <div key={planet} className="bg-white rounded-lg border border-border overflow-hidden">
                    {/* Planet header */}
                    <div className="bg-muted px-4 py-2 border-b border-border flex items-center justify-between">
                      <Heading as={5} variant={5}>
                        {translatePlanet(planet, language)}
                      </Heading>
                      <span className="text-sm font-semibold text-primary">{t('auto.total')}: {total}</span>
                    </div>
                    <div className="flex flex-col lg:flex-row">
                      {/* LEFT: Full contributor matrix table */}
                      <div className="flex-1 overflow-x-auto p-3">
                        {(() => {
                          const contributors = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Lagna'];
                          const contribData = ashtakvargaData.planet_details?.[planet]?.contributors;
                          return (
                            <Table className="w-full text-sm border-collapse">
                              <TableHeader>
                                <TableRow>
                                  <TableHead className="text-left p-1 text-primary font-medium border-b border-border whitespace-nowrap">{t('auto.contributor')}</TableHead>
                                  {signs.map((s, i) => (
                                    <TableHead key={i} className="text-center p-1 text-primary font-medium border-b border-border min-w-[26px] text-xs">
                                      {language === 'hi' ? hindiSignAbbr[i] : signAbbr[i]}
                                    </TableHead>
                                  ))}
                                  <TableHead className="text-center p-1 text-primary font-bold border-b border-border">&Sigma;</TableHead>
                                </TableRow>
                              </TableHeader>
                              <TableBody>
                                {contributors.map((contrib) => {
                                  const row = contribData?.[contrib] || {};
                                  const rowVals = signs.map((s) => row[s] || 0);
                                  const rowTotal = rowVals.reduce((a, b) => a + b, 0);
                                  return (
                                    <TableRow key={contrib} className="border-t border-border hover:bg-muted/5">
                                      <TableCell className="p-1 text-foreground font-medium whitespace-nowrap">{translatePlanet(contrib, language)}</TableCell>
                                      {rowVals.map((v, i) => (
                                        <TableCell key={i} className="text-center p-1">
                                          <span className={`inline-block w-5 h-5 leading-5 rounded-sm text-sm font-semibold ${v === 1 ? 'bg-green-100 text-green-800' : 'text-foreground'}`}>
                                            {v}
                                          </span>
                                        </TableCell>
                                      ))}
                                      <TableCell className="text-center p-1 font-semibold text-foreground">{rowTotal}</TableCell>
                                    </TableRow>
                                  );
                                })}
                                {/* Bindu total row */}
                                <TableRow className="border-t-2 border-border bg-muted">
                                  <TableCell className="p-1 text-primary font-bold whitespace-nowrap">{t('auto.bindu')}</TableCell>
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
                          {/* Bindu values in each house position — white bg rect prevents overlap with lines */}
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
            <div className="flex items-center gap-4 mt-4 text-sm text-foreground">
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

          <div className="bg-muted rounded-xl p-5 border border-border">
            <Heading as={4} variant={4} className="mb-4">{t('section.bhinnashtakvarga')}</Heading>
            <div className="overflow-x-auto">
              <Table className="w-full text-sm">
                <TableHeader>
                  <TableRow className="border-b border-border">
                    <TableHead className="text-left p-2 text-primary font-medium">{t('table.planet')}</TableHead>
                    {signs.map((s) => (
                      <TableHead key={s} className="text-center p-2 text-primary font-medium text-xs">{translateSignAbbr(s, language)}</TableHead>
                    ))}
                    <TableHead className="text-center p-2 text-primary font-medium">{t('table.total')}</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'].map((planet) => {
                    const bindus = ashtakvargaData.planet_bindus?.[planet] || {};
                    const total = signs.reduce((sum, s) => sum + (bindus[s] || 0), 0);
                    return (
                      <TableRow key={planet} className="border-t border-border hover:bg-muted/5">
                        <TableCell className="p-2 text-foreground font-medium">{translatePlanet(planet, language)}</TableCell>
                        {signs.map((s) => {
                          const val = bindus[s] || 0;
                          return (
                            <TableCell key={s} className="text-center p-2">
                              <span className={`inline-block w-6 h-6 rounded text-sm leading-6 ${val >= 5 ? 'bg-primary text-white font-bold' : val <= 2 ? 'bg-red-10 text-wax-red-deep' : 'text-foreground'}`}>
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

          <div className="bg-muted rounded-xl p-5 border border-border">
            <Heading as={4} variant={4} className="mb-2">{t('ashtakvarga.purifiedPoints')}</Heading>
            <p className="text-sm text-muted-foreground mb-4">{t('ashtakvarga.purificationDesc')}</p>

            <div className="space-y-8">
              {['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'].map((planet) => {
                const purified = ashtakvargaData.purified?.[planet];
                if (!purified) return null;

                return (
                  <div key={planet} className="bg-white rounded-lg border border-border overflow-hidden">
                    <div className="bg-muted px-4 py-2 flex items-center justify-between">
                      <Heading as={5} variant={5}>
                        {translatePlanet(planet, language)} - {t('ashtakvarga.purifiedPoints')}
                      </Heading>
                      <div className="text-sm font-bold text-primary">
                        {t('ashtakvarga.shodhyaPinda')}: <span className="text-foreground text-lg">{purified.shodhya_pinda}</span>
                      </div>
                    </div>

                    <div className="overflow-x-auto p-3">
                      <Table className="w-full text-sm border-collapse">
                        <TableHeader>
                          <TableRow>
                            <TableHead className="text-left p-1 text-primary font-medium border-b border-border">{t('auto.process')}</TableHead>
                            {signs.map((s, i) => (
                              <TableHead key={i} className="text-center p-1 text-primary font-medium border-b border-border min-w-[26px] text-xs">
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
                                <span className={`inline-block w-6 h-6 leading-6 rounded text-sm font-bold bg-muted/20 text-primary`}>
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

          {/* Horasara Phala */}
          {ashtakvargaData.kundli_id && (
            <HorasaraPhalaSection kundliId={ashtakvargaData.kundli_id} language={language} t={t} />
          )}

          {/* General Remedies */}
          <GeneralRemedies language={language} t={t} kundliId={ashtakvargaData.kundli_id} />
        </div>
      ) : (
        <p className="text-center text-foreground py-8">{t('kundli.clickAshtakvargaTab')}</p>
      )}
    </>
  );
}
