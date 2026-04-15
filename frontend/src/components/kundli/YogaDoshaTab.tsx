import { Loader2, CheckCircle, Shield, AlertTriangle, Gem } from 'lucide-react';
import { translateName, translateLabel, translateRemedy, translateBackend, translatePlanet } from '@/lib/backend-translations';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell, TableCaption, TableFooter } from '@/components/ui/table';
import { Heading } from '@/components/ui/heading';

interface YogaDoshaTabProps {
  yogaDoshaData: any;
  loadingYogaDosha: boolean;
  doshaDisplay?: { mangal: any; kaalsarp: any; sadesati: any } | null;
  doshaData?: any;
  loadingDosha?: boolean;
  language: string;
  t: (key: string) => string;
}

export default function YogaDoshaTab({ yogaDoshaData, loadingYogaDosha, doshaDisplay, doshaData, loadingDosha, language, t }: YogaDoshaTabProps) {
  if (loadingYogaDosha) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-6 h-6 animate-spin text-primary" />
        <span className="ml-2 text-foreground">{t('kundli.analyzingYogasAndDoshas')}</span>
      </div>
    );
  }

  if (!yogaDoshaData) {
    return (
      <div className="flex flex-col items-center justify-center py-12">
        <p className="text-foreground mb-3 text-sm">{t('kundli.clickYogasTab')}</p>
        <span className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-muted/10 border border-border text-primary text-sm font-medium cursor-default">
          <CheckCircle className="w-4 h-4" />
          {t('kundli.clickYogasTab')}
        </span>
      </div>
    );
  }

  const hi = language === 'hi';

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* 1. Yogas Table */}
        <div className="bg-muted rounded-xl border border-border p-4 flex flex-col">
          <div className="flex items-center gap-2 mb-3">
            <CheckCircle className="w-4 h-4 text-green-600" />
            <Heading as={4} variant={4}>{t('section.yogas')}</Heading>
          </div>
          <div className="overflow-x-auto flex-1">
            <Table className="w-full text-xs">
              <TableHeader className="bg-muted">
                <TableRow>
                  <TableHead className="text-left p-1.5 text-primary font-medium">{hi ? 'योग का नाम' : 'Yoga Name'}</TableHead>
                  <TableHead className="text-left p-1.5 text-primary font-medium">{hi ? 'विवरण' : 'Description'}</TableHead>
                  <TableHead className="text-center p-1.5 text-primary font-medium">{hi ? 'ग्रह' : 'Planets'}</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {(() => {
                  const presentYogas = (yogaDoshaData.yogas || []).filter((y: any) => y.present);
                  if (presentYogas.length === 0) {
                    return <TableRow><TableCell colSpan={3} className="p-4 text-center text-foreground">{t('yoga.noneDetected')}</TableCell></TableRow>;
                  }
                  return presentYogas.map((yoga: any, idx: number) => (
                    <TableRow key={idx} className="border-t border-border hover:bg-muted/5 transition-colors">
                      <TableCell className="p-1.5 font-semibold text-foreground whitespace-nowrap">{translateName(yoga.name, language)}</TableCell>
                      <TableCell className="p-1.5 text-foreground leading-relaxed">{translateBackend(yoga.description, language)}</TableCell>
                      <TableCell className="p-1.5 text-center">
                        <div className="flex flex-wrap justify-center gap-1">
                          {(yoga.planets_involved || []).map((p: string) => (
                            <span key={p} className="px-1.5 py-0.5 rounded bg-green-100 text-green-800 font-medium">
                              {translatePlanet(p, language)}
                            </span>
                          ))}
                        </div>
                      </TableCell>
                    </TableRow>
                  ));
                })()}
              </TableBody>
            </Table>
          </div>
        </div>

        {/* 2. Doshas Table */}
        <div className="bg-muted rounded-xl border border-border p-4 flex flex-col">
          <div className="flex items-center gap-2 mb-3">
            <Shield className="w-4 h-4 text-red-700" />
            <Heading as={4} variant={4}>{t('section.doshas')}</Heading>
          </div>
          <div className="overflow-x-auto flex-1">
            <Table className="w-full text-xs">
              <TableHeader className="bg-muted">
                <TableRow>
                  <TableHead className="text-left p-1.5 text-primary font-medium">{hi ? 'दोष का नाम' : 'Dosha Name'}</TableHead>
                  <TableHead className="text-center p-1.5 text-primary font-medium">{hi ? 'तीव्रता' : 'Severity'}</TableHead>
                  <TableHead className="text-left p-1.5 text-primary font-medium">{hi ? 'विवरण और उपाय' : 'Description & Remedies'}</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {(() => {
                  const presentDoshas = (yogaDoshaData.doshas || []).filter((d: any) => d.present);
                  if (presentDoshas.length === 0) {
                    return <TableRow><TableCell colSpan={3} className="p-4 text-center text-green-600 font-medium">{t('kundli.noDoshasInChart')}</TableCell></TableRow>;
                  }
                  return presentDoshas.map((dosha: any, idx: number) => (
                    <TableRow key={idx} className="border-t border-border hover:bg-muted/5 transition-colors">
                      <TableCell className="p-1.5 font-semibold text-foreground whitespace-nowrap">{translateName(dosha.name, language)}</TableCell>
                      <TableCell className="p-1.5 text-center">
                        <span className={`px-2 py-0.5 rounded-full font-medium ${
                          dosha.severity === 'high' ? 'bg-red-100 text-red-800' : 
                          dosha.severity === 'medium' ? 'bg-amber-100 text-amber-800' : 'bg-yellow-100 text-yellow-800'
                        }`}>
                          {translateLabel(dosha.severity, language)}
                        </span>
                      </TableCell>
                      <TableCell className="p-1.5">
                        <p className="text-foreground mb-1.5">{translateBackend(dosha.description, language)}</p>
                        {dosha.remedies && dosha.remedies.length > 0 && (
                          <div className="bg-white/40 p-1.5 rounded border border-border/20">
                            <p className="text-[10px] font-bold text-primary uppercase mb-1">{t('section.remedies')}:</p>
                            <ul className="space-y-0.5">
                              {dosha.remedies.map((r: string, ri: number) => (
                                <li key={ri} className="flex items-start gap-1 text-[11px] text-foreground">
                                  <span className="mt-1 w-1 h-1 rounded-full bg-muted shrink-0" />
                                  {translateRemedy(r, language)}
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </TableCell>
                    </TableRow>
                  ));
                })()}
              </TableBody>
            </Table>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* 3. Specific Dosha Analysis Table */}
        <div className="bg-muted rounded-xl border border-border p-4 flex flex-col">
          <div className="flex items-center gap-2 mb-3">
            <AlertTriangle className="w-4 h-4 text-orange-600" />
            <Heading as={4} variant={4}>{t('section.doshaAnalysis')}</Heading>
          </div>
          {loadingDosha ? (
            <div className="flex items-center justify-center py-8 flex-1"><Loader2 className="w-5 h-5 animate-spin text-primary" /></div>
          ) : (
            <div className="overflow-x-auto flex-1">
              <Table className="w-full text-xs">
                <TableHeader className="bg-muted">
                  <TableRow>
                    <TableHead className="text-left p-1.5 text-primary font-medium">{hi ? 'दोष' : 'Analysis'}</TableHead>
                    <TableHead className="text-center p-1.5 text-primary font-medium">{hi ? 'स्थिति' : 'Status'}</TableHead>
                    <TableHead className="text-left p-1.5 text-primary font-medium">{hi ? 'विवरण' : 'Details'}</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {doshaDisplay ? (
                    <>
                      {/* Mangal Dosha */}
                      <TableRow className="border-t border-border hover:bg-muted/5 transition-colors">
                        <TableCell className="p-1.5 font-semibold text-foreground whitespace-nowrap">{translateName('Mangal Dosha', language)}</TableCell>
                        <TableCell className="p-1.5 text-center">
                          <span className={`px-2 py-0.5 rounded-full font-medium ${doshaDisplay.mangal.has_dosha ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'}`}>
                            {doshaDisplay.mangal.has_dosha ? (hi ? 'उपस्थित' : 'Present') : (hi ? 'नहीं है' : 'Absent')}
                          </span>
                        </TableCell>
                        <TableCell className="p-1.5 text-foreground">{translateBackend(doshaDisplay.mangal.description, language)}</TableCell>
                      </TableRow>
                      {/* Kaal Sarp */}
                      <TableRow className="border-t border-border hover:bg-muted/5 transition-colors">
                        <TableCell className="p-1.5 font-semibold text-foreground whitespace-nowrap">{translateName('Kaal Sarp Dosha', language)}</TableCell>
                        <TableCell className="p-1.5 text-center">
                          <span className={`px-2 py-0.5 rounded-full font-medium ${doshaDisplay.kaalsarp.has_dosha ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'}`}>
                            {doshaDisplay.kaalsarp.has_dosha ? (hi ? 'उपस्थित' : 'Present') : (hi ? 'नहीं है' : 'Absent')}
                          </span>
                        </TableCell>
                        <TableCell className="p-1.5 text-foreground">{translateBackend(doshaDisplay.kaalsarp.description, language)}</TableCell>
                      </TableRow>
                      {/* Sade Sati */}
                      <TableRow className="border-t border-border hover:bg-muted/5 transition-colors">
                        <TableCell className="p-1.5 font-semibold text-foreground whitespace-nowrap">{translateName('Sade Sati', language)}</TableCell>
                        <TableCell className="p-1.5 text-center">
                          <span className={`px-2 py-0.5 rounded-full font-medium ${doshaDisplay.sadesati.has_sade_sati ? 'bg-orange-100 text-orange-700' : 'bg-green-100 text-green-800'}`}>
                            {doshaDisplay.sadesati.has_sade_sati ? (hi ? 'सक्रिय' : 'Active') : (hi ? 'नहीं है' : 'Inactive')}
                          </span>
                        </TableCell>
                        <TableCell className="p-1.5 text-foreground">
                          {doshaDisplay.sadesati.has_sade_sati && <span className="font-bold text-orange-700">[{translateLabel(doshaDisplay.sadesati.phase, language)}] </span>}
                          {translateBackend(doshaDisplay.sadesati.description, language)}
                        </TableCell>
                      </TableRow>
                    </>
                  ) : (
                    <TableRow><TableCell colSpan={3} className="p-4 text-center text-foreground">{t('common.noData')}</TableCell></TableRow>
                  )}
                </TableBody>
              </Table>
            </div>
          )}
        </div>

        {/* 4. Gemstones Table */}
        <div className="bg-muted rounded-xl border border-border p-4 flex flex-col">
          <div className="flex items-center gap-2 mb-3">
            <Gem className="w-4 h-4 text-primary" />
            <Heading as={4} variant={4}>{t('section.remediesGemstone')}</Heading>
          </div>
          <div className="overflow-x-auto flex-1">
            <Table className="w-full text-xs">
              <TableHeader className="bg-muted">
                <TableRow>
                  <TableHead className="text-left p-1.5 text-primary font-medium">{hi ? 'रत्न' : 'Gemstone'}</TableHead>
                  <TableHead className="text-center p-1.5 text-primary font-medium">{hi ? 'ग्रह' : 'Planet'}</TableHead>
                  <TableHead className="text-left p-1.5 text-primary font-medium">{hi ? 'विवरण और धारण विधि' : 'Reason & wearing'}</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {(() => {
                  const gems = doshaData?.gemstone_recommendations || [];
                  if (gems.length === 0) {
                    return <TableRow><TableCell colSpan={3} className="p-4 text-center text-foreground">{t('common.noData')}</TableCell></TableRow>;
                  }
                  return gems.map((gem: any, idx: number) => (
                    <TableRow key={idx} className="border-t border-border hover:bg-muted/5 transition-colors">
                      <TableCell className="p-1.5">
                        <p className="font-semibold text-foreground whitespace-nowrap">{hi && gem.gemstone_hi ? gem.gemstone_hi : gem.gemstone}</p>
                        <span className={`text-[10px] px-1.5 py-0.5 rounded uppercase font-bold ${gem.priority === 'primary' ? 'bg-primary text-white' : 'bg-muted/20 text-primary'}`}>
                          {gem.priority === 'primary' ? (hi ? 'प्राथमिक' : 'Primary') : (hi ? 'द्वितीयक' : 'Secondary')}
                        </span>
                      </TableCell>
                      <TableCell className="p-1.5 text-center font-medium">{translatePlanet(gem.planet, language)}</TableCell>
                      <TableCell className="p-1.5">
                        <p className="text-foreground mb-1.5 leading-relaxed">{translateBackend(gem.reason, language)}</p>
                        <div className="flex flex-wrap gap-2 text-[10px] text-primary font-bold">
                          {gem.metal && <span className="bg-white/50 px-1.5 py-0.5 rounded border border-border/10 whitespace-nowrap">{hi ? 'धातु' : 'Metal'}: {translateBackend(gem.metal, language)}</span>}
                          {gem.finger && <span className="bg-white/50 px-1.5 py-0.5 rounded border border-border/10 whitespace-nowrap">{hi ? 'उंगली' : 'Finger'}: {translateBackend(gem.finger, language)}</span>}
                          {gem.day && <span className="bg-white/50 px-1.5 py-0.5 rounded border border-border/10 whitespace-nowrap">{hi ? 'दिन' : 'Day'}: {translateBackend(gem.day, language)}</span>}
                        </div>
                      </TableCell>
                    </TableRow>
                  ));
                })()}
              </TableBody>
            </Table>
          </div>
        </div>
      </div>
    </div>
  );
}
