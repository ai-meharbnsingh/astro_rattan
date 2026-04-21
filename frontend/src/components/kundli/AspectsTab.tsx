import { useState } from 'react';
import { Loader2, Eye, BookOpen, ChevronDown, ChevronRight } from 'lucide-react';
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
  const l = (en: string, hiStr: string) => (hi ? hiStr : en);
  const [eduOpen, setEduOpen] = useState(true);

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

      {/* Educational Summary (Aspects) */}
      <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
        <button
          type="button"
          onClick={() => setEduOpen((v) => !v)}
          className="w-full flex items-center justify-between px-4 py-3 bg-sacred-gold-dark text-white text-sm font-semibold"
        >
          <span className="flex items-center gap-2">
            <BookOpen className="w-4 h-4 opacity-90" />
            {l('Educational Summary — Aspects (Drishti)', 'शिक्षात्मक सार — दृष्टि')}
          </span>
          {eduOpen ? (
            <ChevronDown className="w-4 h-4 opacity-90" />
          ) : (
            <ChevronRight className="w-4 h-4 opacity-90" />
          )}
        </button>
        {eduOpen && (
          <div className="px-4 py-3 text-sm text-foreground/80 space-y-4">
            <div className="space-y-1">
              <p className="font-semibold text-foreground">{l('What an “aspect” means', '“दृष्टि” का अर्थ')}</p>
              <p>
                {l(
                  'An aspect (Drishti) is a planet’s influence cast onto another planet or a house. It describes where a planet’s energy “reaches” and modifies results.',
                  'दृष्टि (Drishti) का अर्थ है किसी ग्रह का प्रभाव दूसरे ग्रह या भाव पर पड़ना। इससे पता चलता है कि ग्रह की ऊर्जा “कहाँ तक” पहुँच रही है और परिणाम कैसे बदलते हैं।'
                )}
              </p>
            </div>

            <div className="space-y-1">
              <p className="font-semibold text-foreground">{l('How to read the two tables', 'दोनों तालिकाएँ कैसे पढ़ें')}</p>
              <ul className="list-disc pl-5 space-y-1">
                <li>{l('“Aspects on Planets” shows: for each planet, who is aspecting it and which houses it aspects.', '“ग्रहों पर दृष्टि” में: प्रत्येक ग्रह पर कौन दृष्टि डाल रहा है और वह किन भावों को देख रहा है।')}</li>
                <li>{l('“Aspects on Bhavas” shows: for each house, benefic vs malefic planets casting aspects there.', '“भावों पर दृष्टि” में: प्रत्येक भाव पर शुभ/पाप ग्रहों की दृष्टि।')}</li>
              </ul>
            </div>

            <div className="space-y-1">
              <p className="font-semibold text-foreground">{l('Benefic vs Malefic (quick rule)', 'शुभ बनाम पाप (सरल नियम)')}</p>
              <p>
                {l(
                  'This app treats Jupiter, Venus, Moon, and Mercury as benefics for the table split. Benefic aspects generally support growth; malefic aspects create pressure, effort, or obstacles (context matters).',
                  'इस ऐप में बृहस्पति, शुक्र, चंद्र, बुध को “शुभ” मानकर तालिका में अलग किया गया है। शुभ दृष्टि सामान्यतः सहायता करती है; पाप दृष्टि दबाव/परिश्रम/बाधा दिखा सकती है (परिस्थिति पर निर्भर)।'
                )}
              </p>
            </div>

            <div className="space-y-1">
              <p className="font-semibold text-foreground">{l('Strength, offsets, and “Spl”', 'Strength, offsets और “Spl”')}</p>
              <ul className="list-disc pl-5 space-y-1">
                <li>{l('`1.0x`, `0.75x` etc. is aspect strength (higher = stronger influence).', '`1.0x`, `0.75x` आदि दृष्टि-बल है (ज्यादा = अधिक प्रभाव)।')}</li>
                <li>{l('`+4h`, `+8h` indicates the special aspect distance in houses.', '`+4h`, `+8h` भावों के अंतर के रूप में विशेष दृष्टि दूरी दिखाता है।')}</li>
                <li>{l(`“${spl}” marks a special aspect (beyond the standard 7th).`, `“${spl}” का अर्थ है विशेष दृष्टि (सामान्य 7वीं से अतिरिक्त)।`)}</li>
              </ul>
            </div>

            <div className="space-y-1">
              <p className="font-semibold text-foreground">{l('Common Vedic aspect pattern (reference)', 'वैदिक दृष्टि पैटर्न (संदर्भ)')}</p>
              <ul className="list-disc pl-5 space-y-1">
                <li>{l('All planets aspect the 7th house from themselves (opposition).', 'सभी ग्रह अपने से 7वें भाव पर दृष्टि डालते हैं।')}</li>
                <li>{l('Mars: special aspects on 4th and 8th.', 'मंगल: 4वीं और 8वीं विशेष दृष्टि।')}</li>
                <li>{l('Jupiter: special aspects on 5th and 9th.', 'बृहस्पति: 5वीं और 9वीं विशेष दृष्टि।')}</li>
                <li>{l('Saturn: special aspects on 3rd and 10th.', 'शनि: 3वीं और 10वीं विशेष दृष्टि।')}</li>
                <li>{l('Rahu/Ketu are often treated with 5th/7th/9th aspects in many traditions (implementation varies).', 'राहु/केतु को कई परंपराओं में 5/7/9 दृष्टि माना जाता है (परंपरा/इम्प्लीमेंटेशन बदल सकता है)।')}</li>
              </ul>
            </div>

            <div className="rounded-lg bg-muted/30 border border-border/40 p-3">
              <p className="font-semibold text-foreground mb-1">{l('Practical tip', 'व्यावहारिक टिप')}</p>
              <p>
                {l(
                  'Combine aspects with house topics: aspects onto 1/7/10/11 often show visible life events, while aspects onto 4/5/9/12 may show inner shifts, learning, or faith patterns. Timing still comes from Dasha/Transits.',
                  'दृष्टि को भाव-फल के साथ मिलाकर देखें: 1/7/10/11 पर दृष्टि अक्सर बाहरी घटनाएँ दिखाती है, जबकि 4/5/9/12 पर दृष्टि भीतर के बदलाव/सीख/धर्म-प्रवृत्ति दिखा सकती है। समय निर्धारण फिर भी दशा/गोचर से आता है।'
                )}
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
