import { Loader2, Eye } from 'lucide-react';
import { translatePlanet } from '@/lib/backend-translations';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '@/components/ui/table';
import { Heading } from '@/components/ui/heading';

interface AspectsTabProps {
  aspectsData: any;
  loadingAspects: boolean;
  language: string;
  t: (key: string) => string;
}

export default function AspectsTab({ aspectsData, loadingAspects, language, t }: AspectsTabProps) {
  const BENEFICS = ['Jupiter', 'Venus', 'Moon', 'Mercury'];
  const spl = t('auto.Spl');
  const housePrefix = t('auto.h');
  const hi = language === 'hi';

  const header = (
    <div>
      <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
        <Eye className="w-6 h-6" />
        {hi ? 'दृष्टि' : 'Aspects (Drishti)'}
      </Heading>
      <p className="text-sm text-muted-foreground">
        {hi
          ? 'कौन-सा ग्रह किन ग्रहों/भावों पर दृष्टि डाल रहा है — शुभ/अशुभ प्रभाव सहित — यहाँ दिखता है।'
          : 'See which planets aspect other planets and houses, including benefic/malefic influence.'}
      </p>
    </div>
  );

  if (loadingAspects) {
    return (
      <div className="space-y-4">
        {header}
        <div className="flex items-center justify-center py-12">
          <Loader2 className="w-6 h-6 animate-spin text-primary" />
          <span className="ml-2 text-foreground">{t('kundli.loadingAspects')}</span>
        </div>
      </div>
    );
  }

  if (!aspectsData) {
    return (
      <div className="space-y-4">
        {header}
        <p className="text-center text-foreground py-8">{t('common.noData')}</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {header}
      <div className="space-y-6">

        {/* Aspects on Planets */}
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
            {t('section.aspectsOnPlanets')}
          </div>
          <Table className="w-full text-xs table-fixed">
            <TableHeader>
              <TableRow>
                <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[18%]">{t('table.planet')}</TableHead>
                <TableHead className="text-center p-2 text-primary font-semibold uppercase tracking-wide w-[8%]">{t('table.house')}</TableHead>
                <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[25%]">{t('auto.aspectedByBenefic')}</TableHead>
                <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[25%]">{t('auto.aspectedByMalefic')}</TableHead>
                <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[24%]">{t('auto.aspectsTo')}</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {(() => {
                const summary = aspectsData.planet_aspects_summary;
                if (summary && typeof summary === 'object' && !Array.isArray(summary)) {
                  return Object.entries(summary).map(([planet, data]: [string, any]) => {
                    const aspBy = data.aspected_by || [];
                    const beneficList = aspBy.filter((a: any) => BENEFICS.includes(a.planet || a));
                    const maleficList = aspBy.filter((a: any) => !BENEFICS.includes(a.planet || a));
                    const aspectsTo = data.aspects_to || [];
                    return (
                      <TableRow key={planet} className="border-t border-border hover:bg-muted/5 align-top">
                        <TableCell className="p-2 font-semibold text-foreground">{translatePlanet(planet, language)}</TableCell>
                        <TableCell className="p-2 text-center text-foreground">{data.house}</TableCell>
                        <TableCell className="p-2 whitespace-normal break-words">
                          {beneficList.length > 0 ? beneficList.map((a: any, j: number) => (
                            <span key={j} className="inline-flex items-center gap-1 mr-2">
                              <span className="text-green-600 font-medium">{translatePlanet(a.planet || a, language)}</span>
                              <span className="text-[10px] text-foreground/70">({a.strength || '1.0'}x{a.offset ? ` ${a.offset}${housePrefix}` : ''}{a.type === 'special' ? ` ${spl}` : ''})</span>
                            </span>
                          )) : <span className="text-foreground/50">—</span>}
                        </TableCell>
                        <TableCell className="p-2 whitespace-normal break-words">
                          {maleficList.length > 0 ? maleficList.map((a: any, j: number) => (
                            <span key={j} className="inline-flex items-center gap-1 mr-2">
                              <span className="text-red-500 font-medium">{translatePlanet(a.planet || a, language)}</span>
                              <span className="text-[10px] text-foreground/70">({a.strength || '1.0'}x{a.offset ? ` ${a.offset}${housePrefix}` : ''}{a.type === 'special' ? ` ${spl}` : ''})</span>
                            </span>
                          )) : <span className="text-foreground/50">—</span>}
                        </TableCell>
                        <TableCell className="p-2 whitespace-normal break-words">
                          {aspectsTo.length > 0 ? aspectsTo.map((a: any, j: number) => (
                            <span key={j} className="inline-flex items-center gap-1 mr-2">
                              <span className="font-medium text-foreground">{housePrefix}{a.house}</span>
                              <span className="text-[10px] text-foreground/70">({a.strength}x)</span>
                            </span>
                          )) : <span className="text-foreground/50">—</span>}
                        </TableCell>
                      </TableRow>
                    );
                  });
                }
                return <TableRow><TableCell colSpan={5} className="text-center p-4 text-foreground">{t('common.noData')}</TableCell></TableRow>;
              })()}
            </TableBody>
          </Table>
        </div>

        {/* Aspects on Bhavas */}
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
            {t('section.aspectsOnBhavas')}
          </div>
          <Table className="w-full text-xs table-fixed">
            <TableHeader>
              <TableRow>
                <TableHead className="text-center p-2 text-primary font-semibold uppercase tracking-wide w-[12%]">{t('table.house')}</TableHead>
                <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[44%]">{t('auto.beneficAspectsShubh')}</TableHead>
                <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[44%]">{t('auto.maleficAspectsAshubh')}</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {(() => {
                const bhavas = aspectsData.bhava_summary || aspectsData.bhava_aspects;
                const bhavaAspects = aspectsData.aspects_on_bhavas || {};
                const renderHouse = (houseNum: number, ba: any) => {
                  const entries = bhavaAspects[String(houseNum)] || [];
                  const aspectedBy = Array.isArray(ba?.aspected_by) ? ba.aspected_by : [];
                  const beneficPlanets: string[] = [];
                  const maleficPlanets: string[] = [];
                  if (Array.isArray(entries) && entries.length > 0) {
                    entries.forEach((e: any) => {
                      const pName = e.planet || '';
                      const detail = `${translatePlanet(pName, language)} (${e.strength || 1}x${e.type === 'special' ? ` ${spl}` : ''})`;
                      if (BENEFICS.includes(pName)) beneficPlanets.push(detail);
                      else maleficPlanets.push(detail);
                    });
                  } else {
                    aspectedBy.forEach((p: any) => {
                      const pName = typeof p === 'string' ? p : p.planet || '';
                      if (BENEFICS.includes(pName)) beneficPlanets.push(translatePlanet(pName, language));
                      else maleficPlanets.push(translatePlanet(pName, language));
                    });
                  }
                  return (
                    <TableRow key={houseNum} className="border-t border-border hover:bg-muted/5 align-top">
                      <TableCell className="p-2 text-center font-semibold text-foreground">{houseNum}</TableCell>
                      <TableCell className="p-2 whitespace-normal break-words max-w-0">
                        {beneficPlanets.length > 0
                          ? <span className="text-green-600">{beneficPlanets.join(', ')}</span>
                          : <span className="text-foreground/50">—</span>}
                      </TableCell>
                      <TableCell className="p-2 whitespace-normal break-words max-w-0">
                        {maleficPlanets.length > 0
                          ? <span className="text-red-500">{maleficPlanets.join(', ')}</span>
                          : <span className="text-foreground/50">—</span>}
                      </TableCell>
                    </TableRow>
                  );
                };
                if (Array.isArray(bhavas)) {
                  return bhavas.map((ba: any, i: number) => renderHouse(ba.house || ba.bhava || i + 1, ba));
                }
                return [1,2,3,4,5,6,7,8,9,10,11,12].map(h => renderHouse(h, (bhavas || {})[h] || (bhavas || {})[String(h)]));
              })()}
            </TableBody>
          </Table>
        </div>

      </div>
    </div>
  );
}
