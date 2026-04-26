import { useState } from 'react';
import { Loader2, Grid3X3, BookOpen, ChevronDown, ChevronRight } from 'lucide-react';
import { getDivisionalChartOptions } from '@/components/kundli/kundli-utils';
import { translatePlanet, translateSign, translateBackend } from '@/lib/backend-translations';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '@/components/ui/table';
import KundliChartSVG, { type PlanetEntry } from '@/components/KundliChartSVG';
import { Heading } from '@/components/ui/heading';

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
        <div className="overflow-x-auto">
          <Table className="w-full text-xs table-fixed min-w-[500px]">
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
  const hi = language === 'hi';
  const l = (en: string, hiStr: string) => (hi ? hiStr : en);
  const [eduOpen, setEduOpen] = useState(true);

  const CHART_INFO: Record<string, { en: string; hi: string }> = {
    D1: {
      en: 'Foundation chart for the whole life: body, identity, overall karma and events. Use it to see baseline strengths (signs, houses, aspects) and then refine with other vargas.',
      hi: 'मुख्य आधार चार्ट: शरीर, व्यक्तित्व, समग्र जीवन-घटनाएँ। पहले D1 से बेसलाइन ताकत/कमज़ोरी समझें, फिर अन्य वर्ग चार्ट से परिष्कृत करें।',
    },
    Moon: {
      en: 'Moon chart is the Rashi chart read from the Moon as the 1st house. It highlights mind, emotions, how experiences feel internally, and day-to-day psychological patterns.',
      hi: 'चंद्र चार्ट में चंद्रमा को लग्न मानकर भाव चलते हैं। यह मन, भावनाएँ और घटनाओं का आंतरिक अनुभव दिखाता है।',
    },
    D2: {
      en: 'Wealth & resources (income, savings habits, asset-building). Helpful for “money style” and financial stability. In this app you’ll also see Hora-lord meanings.',
      hi: 'धन/संसाधन: आय, बचत प्रवृत्ति, संपत्ति निर्माण। आर्थिक स्थिरता और “मनी स्टाइल” समझने में उपयोगी। यहाँ होरा-स्वामी के अर्थ भी दिखते हैं।',
    },
    D3: {
      en: 'Courage, siblings, initiative, communication, short efforts. Often used for younger siblings/co-born and “self-effort” outcomes. This app also shows Drekkana lord/type.',
      hi: 'साहस, भाई-बहन, पहल, संवाद, छोटे प्रयास। सहोदर/पराक्रम के संकेत। यहाँ द्रेक्काण स्वामी/प्रकार भी दिखता है।',
    },
    D4: {
      en: 'Home, property, fixed assets, roots, inner security. Useful for house/land, settlement, and long-term comfort themes.',
      hi: 'घर, संपत्ति, स्थायी संपदा, जड़ें/सुरक्षा। मकान/भूमि और दीर्घकालीन सुख-सुविधा के लिए।',
    },
    D7: {
      en: 'Children, creativity, nurturing responsibilities and legacy. Often used for progeny indicators and the “next generation” themes.',
      hi: 'संतान, रचनात्मकता, पालन-पोषण और वंश परंपरा। संतान-संबंधी संकेतों के लिए।',
    },
    D9: {
      en: 'Marriage/partnership quality, dharma, maturity of planets. Also used to judge the deeper strength of planets and long-term life direction.',
      hi: 'विवाह/साझेदारी की गुणवत्ता, धर्म और ग्रहों की परिपक्व शक्ति। दीर्घकालीन दिशा और ग्रह-बल जाँचने में बहुत उपयोगी।',
    },
    D10: {
      en: 'Career, public role, authority, achievements and professional reputation. Best for job trajectory, responsibility levels, and vocation themes.',
      hi: 'करियर, प्रतिष्ठा, अधिकार और उपलब्धियाँ। नौकरी/भूमिका परिवर्तन और प्रोफेशनल दिशा के लिए।',
    },
    D12: {
      en: 'Parents, lineage, inherited patterns, family conditioning. Helpful for understanding parental influence and ancestral themes.',
      hi: 'माता-पिता, वंश/परिवार की धारणाएँ, विरासत में मिले पैटर्न। अभिभावक-प्रभाव और पूर्वज-थीम के लिए।',
    },
    D16: {
      en: 'Comforts, vehicles, luxuries and “quality of life” enjoyments. Often read for conveyances and lifestyle upgrades/downgrades.',
      hi: 'सुख-सुविधा, वाहन, विलासिता और लाइफ़स्टाइल। वाहन/कम्फर्ट के संकेतों के लिए।',
    },
    D20: {
      en: 'Spiritual practice, devotion, inner growth and “how one connects to the divine”. Useful for sadhana and spiritual temperament.',
      hi: 'आध्यात्मिक साधना, भक्ति और आंतरिक विकास। साधना-प्रवृत्ति और आध्यात्मिक झुकाव के लिए।',
    },
    D24: {
      en: 'Education, learning capacity, skills, and knowledge transmission. Useful for studies, certifications, and academic growth.',
      hi: 'शिक्षा, सीखने की क्षमता, कौशल और विद्या। पढ़ाई/डिग्री/स्किल-ग्रोथ के लिए।',
    },
    D27: {
      en: 'Strengths/weaknesses, resilience, “where you win vs struggle”. Often used for finer assessment of stamina and competence.',
      hi: 'बल/कमज़ोरी, धैर्य, कहाँ जीत और कहाँ संघर्ष। स्टैमिना/कम्पिटेंस की सूक्ष्म जाँच के लिए।',
    },
    D30: {
      en: 'Challenges, mishaps, vulnerabilities and “what trips you up”. Useful for identifying problem patterns; this app also shows Trimsamsha-lord meanings.',
      hi: 'कष्ट/विघ्न, कमजोरियाँ और “कहाँ बाधा आती है”। समस्या-पैटर्न समझने के लिए; यहाँ त्रिंशांश स्वामी के अर्थ भी दिखते हैं।',
    },
    D40: {
      en: 'Maternal lineage themes (tradition-dependent) and subtle inherited traits. Use as a supporting chart for family-pattern reading.',
      hi: 'मातृ-पक्ष/वंश से जुड़े सूक्ष्म संकेत (परंपरा अनुसार)। फैमिली-पैटर्न के सपोर्टिंग चार्ट की तरह देखें।',
    },
    D45: {
      en: 'Character refinement, inner nature and subtle personality traits (tradition-dependent). Use as a supporting “fine-tuning” chart.',
      hi: 'चरित्र, स्वभाव और सूक्ष्म व्यक्तित्व (परंपरा अनुसार)। फाइन-ट्यूनिंग सपोर्टिंग चार्ट।',
    },
    D60: {
      en: 'Karmic roots and deep patterns (very birth-time sensitive). Use only if birth time is accurate; even 1–2 minutes can change D60.',
      hi: 'कर्म के गहरे संकेत (जन्म-समय के प्रति अत्यंत संवेदनशील)। केवल सटीक जन्म-समय होने पर ही देखें; 1–2 मिनट से भी बदल सकता है।',
    },
    D108: {
      en: 'Ultra-fine varga analysis (extremely birth-time sensitive). Best treated as “expert mode” and only with verified birth time.',
      hi: 'अत्यंत सूक्ष्म वर्ग (जन्म-समय अत्यधिक संवेदनशील)। इसे “एक्सपर्ट मोड” की तरह, सत्यापित जन्म-समय पर ही देखें।',
    },
  };

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
      {/* Page heading */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
          <Grid3X3 className="w-6 h-6" />
          {hi ? 'विभाजन चार्ट' : 'Divisional Charts'}
        </Heading>
        <p className="text-sm text-muted-foreground">
          {hi
            ? 'D1, D9, D10 जैसे वर्ग चार्ट चुनें और जीवन-क्षेत्र आधारित विश्लेषण करें।'
            : 'Switch D-charts (D1, D9, D10, etc.) for life-area specific analysis.'}
        </p>
      </div>

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
              <div className="overflow-x-auto">
                <Table className="w-full text-xs table-fixed min-w-[500px]">
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
                <div className="overflow-x-auto">
                  <Table className="w-full text-xs table-fixed min-w-[600px]">
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
                <div className="overflow-x-auto">
                  <Table className="w-full text-xs table-fixed min-w-[700px]">
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

      {/* Educational Summary (Divisional Charts) */}
      <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
        <button
          type="button"
          onClick={() => setEduOpen((v) => !v)}
          className="w-full flex items-center justify-between px-4 py-3 bg-sacred-gold-dark text-white text-sm font-semibold"
        >
          <span className="flex items-center gap-2">
            <BookOpen className="w-4 h-4 opacity-90" />
            {l('Educational Summary — Divisional Charts', 'शिक्षात्मक सार — विभाजन चार्ट')}
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
              <p className="font-semibold text-foreground">{l('How to use this tab', 'इस टैब का उपयोग कैसे करें')}</p>
              <ul className="list-disc pl-5 space-y-1">
                <li>{l('Select a D-chart (D1/D9/D10 etc.) from the dropdown.', 'ड्रॉपडाउन से D-चार्ट (D1/D9/D10 आदि) चुनें।')}</li>
                <li>{l('Use D1 as baseline, then use specific vargas for the life area you care about.', 'पहले D1 को आधार मानें, फिर संबंधित जीवन-क्षेत्र के वर्ग चार्ट देखें।')}</li>
                <li>{l('For D60/D108, accuracy of birth time is critical.', 'D60/D108 के लिए जन्म-समय की सटीकता बहुत महत्वपूर्ण है।')}</li>
              </ul>
            </div>

            <div className="space-y-1">
              <p className="font-semibold text-foreground">{l('What a “Divisional (Varga) chart” means', '“वर्ग चार्ट” का अर्थ')}</p>
              <p>
                {l(
                  'A divisional chart is a refinement of the same birth chart for a specific domain (marriage, career, children, etc.). Think of D1 as the full map, and other D-charts as “zoom lenses” for particular topics.',
                  'वर्ग चार्ट जन्म-कुंडली का किसी विशेष क्षेत्र (विवाह, करियर, संतान आदि) के लिए परिष्कृत रूप है। D1 को “पूरा नक्शा” और अन्य D-चार्ट को “ज़ूम लेंस” समझें।'
                )}
              </p>
            </div>

            <div className="space-y-2">
              <p className="font-semibold text-foreground">{l('Charts available here (and why they matter)', 'यहाँ उपलब्ध चार्ट (और उनका महत्व)')}</p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {getDivisionalChartOptions(language).map((opt) => {
                  const info = CHART_INFO[opt.code] || {
                    en: 'Supporting divisional view for additional context.',
                    hi: 'अतिरिक्त संदर्भ के लिए सहायक वर्ग दृश्य।',
                  };
                  return (
                    <div key={opt.code} className="rounded-lg border border-border/40 bg-muted/20 p-3">
                      <div className="text-xs font-bold text-primary mb-1">{opt.name}</div>
                      <div className="text-xs text-foreground/80 leading-relaxed">
                        {hi ? info.hi : info.en}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            <div className="rounded-lg bg-muted/30 border border-border/40 p-3">
              <p className="font-semibold text-foreground mb-1">{l('Practical tip', 'व्यावहारिक टिप')}</p>
              <p>
                {l(
                  'Use divisional charts together with timing (Dasha/Transits). A strong D-chart promise tends to manifest more clearly during supportive dashas and transits.',
                  'वर्ग चार्ट को समय (दशा/गोचर) के साथ मिलाकर देखें। अनुकूल दशा/गोचर में मजबूत संकेत अधिक स्पष्ट रूप से फलित होते हैं।'
                )}
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
