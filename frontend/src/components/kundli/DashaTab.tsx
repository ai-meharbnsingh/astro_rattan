import React, { useState, useEffect } from 'react';
import { Loader2, ChevronDown } from 'lucide-react';
import { api } from '@/lib/api';
import { translatePlanet } from '@/lib/backend-translations';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell, TableCaption, TableFooter } from '@/components/ui/table';
import { Heading } from '@/components/ui/heading';

function SookshmaSection({ kundliId, language, t }: { kundliId: string; language: string; t: (k: string) => string }) {
  const [data, setData] = useState<any>(null);
  const hi = language === 'hi';

  useEffect(() => {
    if (!kundliId) return;
    let cancelled = false;
    api.get<any>(`/api/kundli/${kundliId}/sookshma-prana`)
      .then(res => { if (!cancelled) setData(res); })
      .catch(() => {});
    return () => { cancelled = true; };
  }, [kundliId]);

  if (!data) return null;

  const currentSookshma = (data.sookshma || []).find((s: any) => s.is_current);
  const currentPrana = (data.prana || []).find((p: any) => p.is_current);
  if (!currentSookshma && !currentPrana) return null;

  return (
    <div className="bg-muted rounded-xl border border-border p-4">
      <Heading as={4} variant={4} className="mb-3">{hi ? 'सूक्ष्म-प्राण दशा' : 'Sookshma-Prana Dasha'}</Heading>
      <div className="overflow-x-auto">
        <Table className="w-full text-xs">
          <TableHeader className="bg-muted">
            <TableRow>
              <TableHead className="p-1.5 text-primary font-medium">{hi ? 'स्तर' : 'Level'}</TableHead>
              <TableHead className="p-1.5 text-primary font-medium">{hi ? 'स्वामी' : 'Lord'}</TableHead>
              <TableHead className="p-1.5 text-primary font-medium">{hi ? 'आरम्भ' : 'Start'}</TableHead>
              <TableHead className="p-1.5 text-primary font-medium">{hi ? 'समाप्त' : 'End'}</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {currentSookshma && (
              <TableRow className="bg-violet-50/30 border-t border-border">
                <TableCell className="p-1.5 font-semibold text-violet-700">{hi ? 'सूक्ष्म' : 'Sookshma'}</TableCell>
                <TableCell className="p-1.5 text-foreground">{translatePlanet(currentSookshma.planet, language)}</TableCell>
                <TableCell className="p-1.5 text-foreground/70">{currentSookshma.start}</TableCell>
                <TableCell className="p-1.5 text-foreground/70">{currentSookshma.end}</TableCell>
              </TableRow>
            )}
            {currentPrana && (
              <TableRow className="bg-rose-50/30 border-t border-border">
                <TableCell className="p-1.5 pl-6 font-semibold text-rose-700">{hi ? 'प्राण' : 'Prana'}</TableCell>
                <TableCell className="p-1.5 text-foreground">{translatePlanet(currentPrana.planet, language)}</TableCell>
                <TableCell className="p-1.5 text-foreground/70">{currentPrana.start}</TableCell>
                <TableCell className="p-1.5 text-foreground/70">{currentPrana.end}</TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}

interface DashaTabProps {
  dashaData: any;
  extendedDashaData: any;
  loadingDasha: boolean;
  loadingExtendedDasha: boolean;
  expandedMahadasha: string | null;
  setExpandedMahadasha: (v: string | null) => void;
  expandedAntardasha: string | null;
  setExpandedAntardasha: (v: string | null) => void;
  language: string;
  t: (key: string) => string;
}

export default function DashaTab({
  dashaData, extendedDashaData, loadingDasha, loadingExtendedDasha,
  expandedMahadasha, setExpandedMahadasha, expandedAntardasha, setExpandedAntardasha,
  language, t,
}: DashaTabProps) {
  const l = (en: string, hi: string) => (language === 'hi' ? hi : en);
  const hi = language === 'hi';

  if (loadingDasha || loadingExtendedDasha) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-6 h-6 animate-spin text-primary" />
        <span className="ml-2 text-foreground">{t('kundli.calculatingDasha')}</span>
      </div>
    );
  }

  if (extendedDashaData) {
    const currentMD = extendedDashaData.mahadasha?.find((md: any) => md.is_current);
    const currentAD = currentMD?.antardasha?.find((ad: any) => ad.is_current);
    const currentPT = currentAD?.pratyantar?.find((pt: any) => pt.is_current);

    return (
      <div className="space-y-6">
        {/* Current Dasha Summary Table */}
        <div className="bg-muted rounded-xl border border-border p-4">
          <div className="flex items-center justify-between mb-3">
            <Heading as={4} variant={4} className="uppercase tracking-wide">{t('section.currentDashaStatus')}</Heading>
            <span className="px-2 py-0.5 bg-muted text-white text-[10px] font-bold rounded animate-pulse">● {l('LIVE', 'लाइव')}</span>
          </div>
          <div className="overflow-x-auto">
            <Table className="w-full text-xs">
              <TableHeader className="bg-muted">
                <TableRow>
                  <TableHead className="text-left p-1.5 text-primary font-medium uppercase">{t('kundli.mahadasha')}</TableHead>
                  <TableHead className="text-left p-1.5 text-primary font-medium uppercase">{t('kundli.antardasha')}</TableHead>
                  <TableHead className="text-left p-1.5 text-primary font-medium uppercase">{t('kundli.pratyantar')}</TableHead>
                  <TableHead className="text-center p-1.5 text-primary font-medium uppercase">{hi ? 'अवधि' : 'Period'}</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                <TableRow className="border-t border-border bg-muted/5 font-semibold">
                  <TableCell className="p-2 text-foreground text-sm">{translatePlanet(extendedDashaData.current_dasha, language)}</TableCell>
                  <TableCell className="p-2 text-foreground text-sm">{translatePlanet(extendedDashaData.current_antardasha, language)}</TableCell>
                  <TableCell className="p-2 text-foreground text-sm">{translatePlanet(extendedDashaData.current_pratyantar, language)}</TableCell>
                  <TableCell className="p-2 text-center text-foreground whitespace-nowrap">
                    {currentPT ? `${currentPT.start} — ${currentPT.end}` : currentAD ? `${currentAD.start} — ${currentAD.end}` : ''}
                  </TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </div>
        </div>

        {/* Full Dasha Timeline Table */}
        <div className="bg-muted rounded-xl border border-border p-4">
          <Heading as={4} variant={4} className="mb-3">{hi ? 'विस्तृत दशा तालिका' : 'Detailed Dasha Timeline'}</Heading>
          <div className="overflow-x-auto">
            <Table className="w-full text-xs">
              <TableHeader className="bg-muted">
                <TableRow>
                  <TableHead className="w-8"></TableHead>
                  <TableHead className="text-left p-1.5 text-primary font-medium">{hi ? 'दशा स्वामी' : 'Dasha Lord'}</TableHead>
                  <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.start')}</TableHead>
                  <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.end')}</TableHead>
                  <TableHead className="text-center p-1.5 text-primary font-medium">{t('table.years')}</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody className="divide-y divide-border/30">
                {(extendedDashaData.mahadasha || []).map((md: any) => {
                  const isMdExpanded = expandedMahadasha === md.planet;
                  return (
                    <React.Fragment key={md.planet}>
                      {/* Mahadasha Row */}
                      <TableRow
                        className={`cursor-pointer transition-colors ${md.is_current ? 'bg-primary/10' : 'hover:bg-muted/5'}`}
                        onClick={() => setExpandedMahadasha(isMdExpanded ? null : md.planet)}
                      >
                        <TableCell className="p-1.5 text-center">
                          <ChevronDown className={`w-3.5 h-3.5 text-primary transition-transform ${isMdExpanded ? 'rotate-180' : ''}`} />
                        </TableCell>
                        <TableCell className="p-1.5">
                          <span className={`font-bold ${md.is_current ? 'text-primary' : 'text-foreground'}`}>
                            {translatePlanet(md.planet, language)} {t('kundli.mahadasha')}
                          </span>
                          {md.is_current && <span className="ml-2 text-[9px] px-1 rounded bg-primary text-white font-bold uppercase">{t('common.current')}</span>}
                        </TableCell>
                        <TableCell className="p-1.5 text-foreground font-medium">{md.start}</TableCell>
                        <TableCell className="p-1.5 text-foreground font-medium">{md.end}</TableCell>
                        <TableCell className="p-1.5 text-center text-primary font-bold">{md.years}</TableCell>
                      </TableRow>

                      {/* Antardasha Rows */}
                      {isMdExpanded && (md.antardasha || []).map((ad: any) => {
                        const adKey = `${md.planet}-${ad.planet}`;
                        const isAdExpanded = expandedAntardasha === adKey;
                        return (
                          <React.Fragment key={adKey}>
                            <TableRow
                              className={`cursor-pointer transition-colors bg-white/30 ${ad.is_current ? 'bg-primary/5 border-l-2 border-l-primary' : 'hover:bg-muted/10'}`}
                              onClick={(e) => { e.stopPropagation(); setExpandedAntardasha(isAdExpanded ? null : adKey); }}
                            >
                              <TableCell className="p-1.5 text-center pl-4">
                                <ChevronDown className={`w-3 h-3 text-primary transition-transform ${isAdExpanded ? 'rotate-180' : ''}`} />
                              </TableCell>
                              <TableCell className="p-1.5 pl-4">
                                <span className={`font-semibold ${ad.is_current ? 'text-primary' : 'text-foreground/80'}`}>
                                  {translatePlanet(ad.planet, language)} {t('kundli.antardasha')}
                                </span>
                                {ad.is_current && <span className="ml-2 text-[8px] px-1 rounded border border-border-dark text-primary font-bold uppercase">{t('common.current')}</span>}
                              </TableCell>
                              <TableCell className="p-1.5 text-foreground italic opacity-80">{ad.start}</TableCell>
                              <TableCell className="p-1.5 text-foreground italic opacity-80">{ad.end}</TableCell>
                              <TableCell className="p-1.5 text-center text-foreground opacity-60">{(ad.years || (parseFloat(ad.duration_years) || 0).toFixed(2))}</TableCell>
                            </TableRow>

                            {/* Antardasha Synthesis */}
                            {isAdExpanded && (ad.analysis?.combined_synthesis_en || ad.analysis?.combined_synthesis_hi) && (
                              <TableRow className="bg-indigo-50/30">
                                <TableCell colSpan={5} className="p-3 pl-8">
                                  <p className="text-[11px] text-indigo-900 leading-relaxed">
                                    <span className="font-semibold text-indigo-700">{hi ? 'दशा विश्लेषण: ' : 'Dasha Analysis: '}</span>
                                    {hi ? (ad.analysis?.combined_synthesis_hi || ad.analysis?.combined_synthesis_en) : (ad.analysis?.combined_synthesis_en || ad.analysis?.combined_synthesis_hi)}
                                  </p>
                                </TableCell>
                              </TableRow>
                            )}

                            {/* Pratyantar Rows */}
                            {isAdExpanded && (ad.pratyantar || []).map((pt: any, idx: number) => (
                              <TableRow
                                key={idx}
                                className={`bg-white/60 transition-colors ${pt.is_current ? 'bg-primary/5' : 'hover:bg-muted/5'}`}
                              >
                                <TableCell className="p-1"></TableCell>
                                <TableCell className="p-1.5 pl-12 text-[11px]">
                                  <span className={`${pt.is_current ? 'text-primary font-bold' : 'text-foreground opacity-70'}`}>
                                    {translatePlanet(pt.planet, language)} {t('kundli.pratyantar')}
                                  </span>
                                  {pt.is_current && <span className="ml-1 text-primary font-bold">●</span>}
                                </TableCell>
                                <TableCell className="p-1.5 text-[11px] text-foreground opacity-60">{pt.start}</TableCell>
                                <TableCell className="p-1.5 text-[11px] text-foreground opacity-60">{pt.end}</TableCell>
                                <TableCell className="p-1"></TableCell>
                              </TableRow>
                            ))}
                          </React.Fragment>
                        );
                      })}
                    </React.Fragment>
                  );
                })}
              </TableBody>
            </Table>
          </div>
        </div>

        {/* Sookshma-Prana Dasha */}
        {extendedDashaData.kundli_id && (
          <SookshmaSection kundliId={extendedDashaData.kundli_id} language={language} t={t} />
        )}

      </div>
    );
  }

  if (dashaData) {
    return (
      <div className="space-y-4">
        <div className="bg-muted rounded-xl border border-border p-4">
          <div className="flex items-center justify-between mb-2">
            <p className="text-xs text-foreground uppercase font-bold tracking-wider">{t('section.currentMahadasha')}</p>
          </div>
          <p className="text-lg font-bold text-foreground">
            {translatePlanet(dashaData.current_dasha, language)} {t('kundli.mahadasha')}
          </p>
          {dashaData.current_antardasha && (
            <p className="text-sm text-primary font-medium mt-1">
              {t('kundli.antardasha')}: {translatePlanet(dashaData.current_antardasha, language)}
            </p>
          )}
        </div>

        <div className="bg-muted rounded-xl border border-border p-4">
          <div className="overflow-x-auto">
            <Table className="w-full text-xs">
              <TableHeader className="bg-muted">
                <TableRow>
                  <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.planet')}</TableHead>
                  <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.start')}</TableHead>
                  <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.end')}</TableHead>
                  <TableHead className="text-center p-1.5 text-primary font-medium">{t('table.years')}</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {(dashaData.mahadasha_periods || []).map((p: any) => (
                  <TableRow key={p.planet} className={`border-t border-border transition-colors ${p.planet === dashaData.current_dasha ? 'bg-primary/10 font-bold' : 'hover:bg-muted/5'}`}>
                    <TableCell className="p-1.5 text-foreground font-medium">
                      {translatePlanet(p.planet, language)}
                      {p.planet === dashaData.current_dasha && <span className="ml-2 text-[9px] px-1 rounded bg-primary text-white uppercase">{t('common.current')}</span>}
                    </TableCell>
                    <TableCell className="p-1.5 text-foreground">{p.start_date}</TableCell>
                    <TableCell className="p-1.5 text-foreground">{p.end_date}</TableCell>
                    <TableCell className="p-1.5 text-center text-foreground font-bold">{p.years}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </div>

      </div>
    );
  }

  return (
    <div className="flex flex-col items-center justify-center py-12">
      <p className="text-foreground mb-3 text-sm">{t('kundli.clickDashaTab')}</p>
      <span className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-muted/10 border border-border text-primary text-sm font-medium cursor-default">
        <ChevronDown className="w-4 h-4" />
        {t('kundli.clickDashaTab')}
      </span>
    </div>
  );
}
