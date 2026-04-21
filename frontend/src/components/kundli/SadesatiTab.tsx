import { Loader2, Shield } from 'lucide-react';
import { translateSign, translateBackend } from '@/lib/backend-translations';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '@/components/ui/table';
import { Heading } from '@/components/ui/heading';
import TimingTheorySection from '@/components/kundli/TimingTheorySection';


interface SadesatiTabProps {
  sadesatiData: any;
  loadingSadesati: boolean;
  doshaData: any;
  language: string;
  t: (key: string) => string;
}

function translateRemedy(remedy: string, language: string): string {
  return language === 'hi' ? translateBackend(remedy, language) || remedy : remedy;
}

export default function SadesatiTab({ sadesatiData, loadingSadesati, language, t }: SadesatiTabProps) {
  const hi = language === 'hi';

  if (loadingSadesati) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-6 h-6 animate-spin text-primary" />
        <span className="ml-2 text-foreground">{t('kundli.loadingSadeSati')}</span>
      </div>
    );
  }

  if (!sadesatiData) {
    return <p className="text-center text-foreground py-8">{t('kundli.clickSadeSatiTab')}</p>;
  }

  const phaseNames: Record<string, string> = {
    first_dhayya:  t('sadeSati.firstDhayya'),
    second_dhayya: t('sadeSati.secondDhayya'),
    third_dhayya:  t('sadeSati.thirdDhayya'),
  };

  const severityClass = (sev: string) =>
    sev === 'extreme' ? 'bg-red-100 text-red-800' :
    sev === 'high'    ? 'bg-orange-100 text-orange-800' :
                        'bg-amber-100 text-amber-800';

  const severityLabel = (sev: string) =>
    sev === 'extreme' ? t('sadeSati.extremeImpact') :
    sev === 'high'    ? t('sadeSati.intenseImpact') :
                        t('sadeSati.moderateImpact');

  // Flatten cycle phases for table 1
  interface CycleRow { cycle: string; phase: string; sign: string; start: string; end: string; severity?: string; }
  const cycleRows: CycleRow[] = [];
  (sadesatiData.cycles || []).forEach((cycle: any) => {
    const phases = cycle.phases || [];
    if (phases.length === 0) {
      cycleRows.push({ cycle: translateBackend(cycle.title, language) || '', phase: '—', sign: translateSign(cycle.sign_name || '', language), start: cycle.start_date || '—', end: cycle.end_date || '—', severity: cycle.severity });
    } else {
      phases.forEach((phase: any) => {
        cycleRows.push({ cycle: translateBackend(cycle.title, language) || '', phase: phaseNames[phase.phase_key] || translateBackend(phase.sub_phase, language) || phase.sub_phase, sign: translateSign(phase.sign_name, language), start: phase.start_date, end: phase.end_date, severity: cycle.severity });
      });
    }
  });

  // Split other_phases into Dhaiya vs Kantaka/Panauti
  const dhaiyaRows = (sadesatiData.other_phases || []).filter((p: any) => p.phase === 'Dhaiya');
  const kantakaRows = (sadesatiData.other_phases || []).filter((p: any) => p.phase !== 'Dhaiya');

  const phaseEffects = [
    { key: 'first_dhayya',  title: t('sadeSati.firstDhayyaEffectsTitle'),   effects: hi ? ["मानसिक और शारीरिक सुख में गिरावट","आंखों की बीमारी की संभावना","वित्तीय हानि और अनावश्यक व्यय","परिवार से अलगाव","पिता को बीमारी हो सकती है","आध्यात्मिकता में रुचि बढ़ती है","दुर्घटना का भय; व्यर्थ घूमना"] : ["Fall in mental and physical happiness","Possibility of eye ailments","Financial losses and unwanted expenditure","Separation from family","Father may suffer ailments","Interest in spiritualism increases","Fear of accidents; may wander uselessly"] },
    { key: 'second_dhayya', title: t('sadeSati.secondDhayyaEffectsTitle'),  effects: hi ? ["शरीर के मध्य भाग में रोग","शारीरिक ऊर्जा प्रभावित","भाइयों और भागीदारों के साथ विवाद","वित्तीय समस्याएं बनी रहती हैं","गलत निर्णय लिए जा सकते हैं","पारिवारिक और व्यावसायिक जीवन अस्थिर","शत्रु नुकसान पहुंचा सकते हैं; प्रियजनों से अलगाव"] : ["Ailments in middle part of body","Physical energy affected","Disputes with brothers and partners","Financial problems persist","Wrong decisions may be taken","Family and business life unstable","Enemies may inflict harm; separation from near ones"] },
    { key: 'third_dhayya',  title: t('sadeSati.thirdDhayyaEffectsTitle'),   effects: hi ? ["पैरों में रोग हो सकते हैं","शारीरिक कमजोरी और आलस्य","सुख में बाधाएं","व्यय में वृद्धि","रिश्तेदारों के साथ विवाद","घरेलू सुख में बाधाएं","नीच लोग परेशानी देते हैं"] : ["Legs may suffer from ailments","Physical weakness and laziness","Happiness faces hurdles","Expenses increase","Conflicts with relatives","Domestic happiness obstacles","Lowly people give troubles"] },
    { key: 'kantak_4th',    title: t('sadeSati.kantaka4thEffectsTitle'),    effects: hi ? ["स्थान परिवर्तन या तबादला","आवास समस्याएं","हृदय रोग हो सकते हैं","रक्तचाप अस्थिरता","जनता/सरकार का विरोध","कार्य क्षेत्र में बाधाएं","शनि की दृष्टि से मानसिक भय"] : ["Change of place or transfer","Housing problems","Heart problems may occur","Blood pressure instability","Opposition from public/government","Obstacles in work sphere","Mental fear due to Saturn's aspect"] },
    { key: 'kantak_7th',    title: t('sadeSati.kantaka7thEffectsTitle'),    effects: hi ? ["जीवन साथी को बीमारी हो सकती है","मानसिक चिंता बढ़ती है","भाग्य में बाधाएं","पिता को कष्ट हो सकता है","माता के स्वास्थ्य को कष्ट","वाहन संबंधी समस्याएं","यात्रा में कठिनाइयां"] : ["Spouse may suffer ailments","Mental anxiety increases","Obstacles in fortune","Father may suffer","Mother's health may suffer","Vehicle related problems","Hardships in travelling"] },
    { key: 'ashtam_8th',    title: t('sadeSati.ashtam8thEffectsTitle'),     effects: hi ? ["दीर्घकालिक रोग और दुर्घटनाएं","अपमानित होने का भय","कार्य क्षेत्र में परिवर्तन","धन में कमी आ सकती है","बच्चों को कष्ट हो सकता है","सबसे चुनौतीपूर्ण अवधि","बच्चों से अलगाव की संभावना"] : ["Long term ailments and accidents","Fear of being insulted","Change in work-sphere","Wealth may diminish","Children may suffer","Most challenging period","Possibilities of separation from children"] },
  ];

  return (
    <div className="space-y-6">
      {/* Page heading */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
          <Shield className="w-6 h-6" />
          {hi ? 'साढ़े साती' : 'Sade Sati'}
        </Heading>
        <p className="text-sm text-muted-foreground">
          {hi ? 'जन्म चंद्र पर शनि का 7.5 वर्षीय चक्र — चरण और तीव्रता' : "Saturn's 7.5-year cycle over natal Moon — phase & intensity"}
        </p>
      </div>
      {/* Intro */}
      <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
        <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-3">
          <span>♄</span>
          <span>{t('sadeSati.analysisTitle')}</span>
          <span className="text-sm font-normal opacity-80 ml-1">
            — {hi ? 'जन्म चंद्र राशि' : 'Birth Moon'}: <span className="font-semibold">{translateSign(sadesatiData.moon_sign, language)}</span>
          </span>
        </div>
        <div className="p-4 space-y-2 text-sm text-foreground leading-relaxed">
          <p>{translateBackend(sadesatiData.explanation?.sadesati, language) || t('sadeSati.sadesatiExplanation')}</p>
          <p>{translateBackend(sadesatiData.explanation?.dhayya, language) || t('sadeSati.dhayyaExplanation')}</p>
        </div>
      </div>

      {/* Table 1: Sade Sati Cycles (rowspan per cycle) */}
      {(sadesatiData.cycles || []).length > 0 && (
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
            {t('sadeSati.cyclesTitle')}
          </div>
          <div className="overflow-x-auto">
            <Table className="w-full text-xs table-fixed">
              <TableHeader>
                <TableRow>
                  <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[22%]">{hi ? 'चक्र' : 'Cycle'}</TableHead>
                  <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[18%]">{t('table.dhayya')}</TableHead>
                  <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[14%]">{t('table.transitSign')}</TableHead>
                  <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[16%]">{t('table.startDate')}</TableHead>
                  <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[16%]">{t('table.endDate')}</TableHead>
                  <TableHead className="text-center p-2 text-primary font-semibold uppercase tracking-wide w-[14%]">{hi ? 'प्रभाव' : 'Impact'}</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {(sadesatiData.cycles || []).map((cycle: any, cidx: number) => {
                  const phases = cycle.phases?.length ? cycle.phases : [null];
                  return phases.map((phase: any, pidx: number) => (
                    <TableRow key={`${cidx}-${pidx}`} className="border-t border-border">
                      {pidx === 0 && (
                        <TableCell className="p-2 font-semibold text-foreground align-middle" rowSpan={phases.length}>
                          <span className={`px-1.5 py-0.5 rounded text-[10px] font-semibold ${severityClass(cycle.severity)}`}>
                            {translateBackend(cycle.title, language)}
                          </span>
                          <p className="text-[10px] text-muted-foreground mt-1">{cycle.start_date} → {cycle.end_date}</p>
                        </TableCell>
                      )}
                      <TableCell className="p-2 text-foreground">
                        {phase ? (phaseNames[phase.phase_key] || translateBackend(phase.sub_phase, language)) : '—'}
                      </TableCell>
                      <TableCell className="p-2 text-foreground">
                        {phase ? translateSign(phase.sign_name, language) : translateSign(cycle.sign_name || '', language)}
                      </TableCell>
                      <TableCell className="p-2 text-foreground">{phase ? phase.start_date : cycle.start_date}</TableCell>
                      <TableCell className="p-2 text-foreground">{phase ? phase.end_date : cycle.end_date}</TableCell>
                      <TableCell className="p-2 text-center">
                        {cycle.severity && (
                          <span className={`px-1.5 py-0.5 rounded text-[10px] font-semibold ${severityClass(cycle.severity)}`}>
                            {severityLabel(cycle.severity)}
                          </span>
                        )}
                      </TableCell>
                    </TableRow>
                  ));
                })}
              </TableBody>
            </Table>
          </div>
        </div>
      )}

      {/* Table 2: Dhaiya + Kantaka + Panauti combined */}
      {(dhaiyaRows.length > 0 || kantakaRows.length > 0) && (
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
            {hi ? 'ढैया / कंटक शनि / पनौती' : 'Dhaiya / Kantaka Saturn / Panauti'}
          </div>
          <div className="overflow-x-auto">
            <Table className="w-full text-xs table-fixed">
              <TableHeader>
                <TableRow>
                  <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[16%]">{hi ? 'प्रकार' : 'Type'}</TableHead>
                  <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[30%]">{hi ? 'उप-चरण' : 'Sub-Phase'}</TableHead>
                  <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[18%]">{t('table.transitSign')}</TableHead>
                  <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[18%]">{t('table.startDate')}</TableHead>
                  <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[18%]">{t('table.endDate')}</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {[...dhaiyaRows, ...kantakaRows]
                  .sort((a, b) => new Date(a.start_date).getTime() - new Date(b.start_date).getTime())
                  .map((phase: any, idx: number) => {
                  const typeBadgeClass =
                    phase.phase === 'Dhaiya'  ? 'bg-amber-100 text-amber-800' :
                    phase.phase === 'Panauti' ? 'bg-red-100 text-red-800'    :
                                                'bg-blue-100 text-blue-800';
                  return (
                    <TableRow key={idx} className="border-t border-border">
                      <TableCell className="p-2">
                        <span className={`px-1.5 py-0.5 rounded text-[10px] font-semibold ${typeBadgeClass}`}>
                          {translateBackend(phase.phase, language)}
                        </span>
                      </TableCell>
                      <TableCell className="p-2 text-foreground">{translateBackend(phase.sub_phase, language) || phase.sub_phase}</TableCell>
                      <TableCell className="p-2 text-foreground">{translateSign(phase.sign_name, language)}</TableCell>
                      <TableCell className="p-2 text-foreground">{phase.start_date}</TableCell>
                      <TableCell className="p-2 text-foreground">{phase.end_date}</TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          </div>
        </div>
      )}

      {/* Phase Effects */}
      <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
        <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
          {t('sadeSati.detailedEffects')}
        </div>
        <div className="p-4 grid grid-cols-1 md:grid-cols-2 gap-3">
          {phaseEffects.map((phase) => (
            <div key={phase.key} className="rounded-lg border border-border p-3">
              <p className="text-xs font-semibold text-primary uppercase tracking-wide mb-2">{phase.title}</p>
              <ul className="space-y-1">
                {phase.effects.map((effect, idx) => (
                  <li key={idx} className="text-xs text-foreground flex items-start gap-1.5">
                    <span className="mt-1.5 w-1 h-1 rounded-full bg-sacred-gold-dark shrink-0" />
                    {effect}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>

      {/* Detailed Remedies */}
      {sadesatiData.detailed_remedies && (
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
            {t('sadeSati.remediesTitle')}
          </div>
          <div className="p-4 space-y-4">
            {sadesatiData.detailed_remedies.mantra && (
              <div>
                <p className="text-xs font-semibold text-primary uppercase tracking-wide mb-2">
                  {translateBackend(sadesatiData.detailed_remedies.mantra.title, language)}
                </p>
                <div className="space-y-2">
                  {sadesatiData.detailed_remedies.mantra.items.map((item: any, idx: number) => (
                    <div key={idx} className="rounded-lg border border-border p-3 text-xs">
                      <p className="font-semibold text-foreground">{item.name}</p>
                      {item.text && <p className="text-primary my-1">{item.text}</p>}
                      <p className="text-foreground/80">{item.instruction}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
            {['stotra', 'vrat', 'donation', 'gemstones', 'other'].map((category) => {
              const data = sadesatiData.detailed_remedies[category];
              if (!data) return null;
              return (
                <div key={category}>
                  <p className="text-xs font-semibold text-primary uppercase tracking-wide mb-2">
                    {translateBackend(data.title, language)}
                  </p>
                  <ul className="space-y-1">
                    {(data.items || []).map((item: any, idx: number) => (
                      <li key={idx} className="text-xs text-foreground flex items-start gap-1.5">
                        <span className="mt-1.5 w-1 h-1 rounded-full bg-sacred-gold-dark shrink-0" />
                        {typeof item === 'string' ? translateBackend(item, language) : translateBackend(item.name, language) || translateBackend(item.instruction, language)}
                      </li>
                    ))}
                  </ul>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Fallback Remedies */}
      {!sadesatiData.detailed_remedies && sadesatiData.remedies && (
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
            {t('section.remedies')}
          </div>
          <ul className="p-4 space-y-2">
            {sadesatiData.remedies.map((remedy: string, idx: number) => (
              <li key={idx} className="text-sm text-foreground flex items-start gap-2">
                <Shield className="w-4 h-4 text-primary shrink-0 mt-0.5" />
                <span>{translateRemedy(remedy, language)}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
          <TimingTheorySection language={language} tab="sadesati" />
    </div>
  );
}
