import React, { useState, useEffect } from 'react';
import { Loader2, ChevronDown, Sparkles, Clock, Calendar } from 'lucide-react';
import { api } from '@/lib/api';
import { translatePlanet } from '@/lib/backend-translations';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '@/components/ui/table';
import { Heading } from '@/components/ui/heading';

function DashaTheorySection({ language }: { language: string }) {
  const hi = language === 'hi';
  const l = (en: string, hiStr: string) => (hi ? hiStr : en);

  const levels = [
    {
      name: l('Mahadasha (Major Period)', 'महादशा (मुख्य अवधि)'),
      duration: l('Years', 'वर्षों तक'),
      desc: l('The "Season" of your life. It sets the primary theme and background for a long period.', 'आपके जीवन का "सीजन"। यह एक लंबी अवधि के लिए प्राथमिक विषय और पृष्ठभूमि निर्धारित करता है।'),
    },
    {
      name: l('Antardasha (Sub-Period)', 'अंतर्दशा (उप-अवधि)'),
      duration: l('Months', 'महीनों तक'),
      desc: l('The "Weather" within the season. It fine-tunes the results and shows specific events.', 'सीजन के भीतर का "मौसम"। यह परिणामों को और अधिक सटीक बनाता है और विशिष्ट घटनाओं को दर्शाता है।'),
    },
    {
      name: l('Pratyantar (Sub-sub-period)', 'प्रत्यंतर दशा (सूक्ष्म अवधि)'),
      duration: l('Days', 'दिनों तक'),
      desc: l('The "Daily Forecast". It highlights the immediate focus and mood of shorter intervals.', ' "दैनिक पूर्वानुमान"। यह छोटे अंतराल के तत्काल फोकस और मूड को उजागर करता है।'),
    },
  ];

  return (
    <div className="mt-8 space-y-6 pb-6">
      <div className="rounded-xl border border-sacred-gold/30 bg-sacred-gold/5 p-6 overflow-hidden">
        <Heading as={3} variant={3} className="text-sacred-gold-dark mb-4 flex items-center gap-2">
          <Clock className="w-5 h-5" />
          {l('Understanding Life Timing (The Seasons Metaphor)', 'जीवन के समय को समझना (सीजन का रूपक)')}
        </Heading>
        
        <p className="text-sm text-foreground/80 mb-6 leading-relaxed">
          {l(
            'While your birth chart shows "what" is in your destiny, the Dasha system reveals "when" it will happen. In Vedic Astrology, life is divided into cycles ruled by different planets. This is called the Vimshottari Dasha — a 120-year cycle that governs the unfolding of your karma.',
            'जबकि आपकी जन्म कुंडली बताती है कि आपके भाग्य में "क्या" है, दशा प्रणाली यह प्रकट करती है कि वह "कब" होगा। वैदिक ज्योतिष में, जीवन को विभिन्न ग्रहों द्वारा शासित चक्रों में विभाजित किया गया है। इसे विंशोत्तरी दशा कहा जाता है — एक 120 साल का चक्र जो आपके कर्मों के प्रकट होने को नियंत्रित करता है।'
          )}
        </p>

        {/* Metaphor Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          {levels.map((level, idx) => (
            <div key={idx} className="bg-white/40 p-4 rounded-lg border border-sacred-gold/10">
              <h5 className="font-bold text-sacred-gold-dark text-xs uppercase mb-1">{level.name}</h5>
              <p className="text-[10px] font-bold text-primary mb-2 italic">[{level.duration}]</p>
              <p className="text-xs text-foreground/70 leading-relaxed">
                {level.desc}
              </p>
            </div>
          ))}
        </div>

        <div className="space-y-8">
          <div className="space-y-4">
            <h4 className="text-sm font-bold text-primary flex items-center gap-2 border-b border-sacred-gold/20 pb-1.5 uppercase tracking-wide">
              {l('Detailed Planetary Dasha Significance', 'ग्रहों की दशाओं का विस्तृत महत्व')}
            </h4>
            
            <div className="space-y-6">
              {/* Sun */}
              <div className="space-y-1">
                <p className="text-xs font-bold text-sacred-gold-dark">{l('Sun (Surya) Dasha — 6 Years', 'सूर्य दशा — 6 वर्ष')}</p>
                <p className="text-xs text-foreground/70 leading-relaxed">
                  {l(
                    'The Sun represents your soul and authority. During its 6-year dasha, the focus shifts to your career, public image, and relationship with your father or government figures. It is a period for finding your true identity and taking charge of your life. If well-placed, it brings fame and promotion; if weak, it may cause health issues or ego clashes.',
                    'सूर्य आपकी आत्मा और अधिकार का प्रतिनिधित्व करता है। इसकी 6 साल की दशा के दौरान, ध्यान आपके करियर, सार्वजनिक छवि और आपके पिता या सरकारी हस्तियों के साथ संबंधों पर केंद्रित होता है। यह अपनी वास्तविक पहचान खोजने और अपने जीवन की जिम्मेदारी लेने की अवधि है। यदि शुभ हो, तो यह प्रसिद्धि और पदोन्नति लाता है; यदि कमजोर हो, तो स्वास्थ्य समस्याएं या अहंकार का टकराव हो सकता है।'
                  )}
                </p>
              </div>

              {/* Moon */}
              <div className="space-y-1">
                <p className="text-xs font-bold text-sacred-gold-dark">{l('Moon (Chandra) Dasha — 10 Years', 'चंद्र दशा — 10 वर्ष')}</p>
                <p className="text-xs text-foreground/70 leading-relaxed">
                  {l(
                    'The Moon rules your emotions and mental peace. This 10-year cycle emphasizes your domestic life, relationship with your mother, and emotional maturity. It is often a period of significant changes in your living situation and mental outlook. You may become more sensitive and intuitive during this time, focusing on comfort and inner happiness.',
                    'चंद्रमा आपकी भावनाओं और मानसिक शांति पर शासन करता है। यह 10 वर्षीय चक्र आपके घरेलू जीवन, माता के साथ संबंधों और भावनात्मक परिपक्वता पर जोर देता है। यह अक्सर आपकी रहने की स्थिति और मानसिक दृष्टिकोण में महत्वपूर्ण बदलावों की अवधि होती है। इस समय के दौरान आप अधिक संवेदनशील और सहज बन सकते हैं, सुख-सुविधा और आंतरिक खुशी पर ध्यान केंद्रित कर सकते हैं।'
                  )}
                </p>
              </div>

              {/* Mars */}
              <div className="space-y-1">
                <p className="text-xs font-bold text-sacred-gold-dark">{l('Mars (Mangal) Dasha — 7 Years', 'मंगल दशा — 7 वर्ष')}</p>
                <p className="text-xs text-foreground/70 leading-relaxed">
                  {l(
                    'Mars is the planet of energy and courage. In its 7-year dasha, you feel a surge of drive and ambition. It is a highly active phase often involving property matters, siblings, and competitive ventures. While it provides the strength to overcome obstacles, an afflicted Mars can lead to impulsive decisions, anger issues, or minor injuries.',
                    'मंगल ऊर्जा और साहस का ग्रह है। इसकी 7 साल की दशा में, आप प्रेरणा और महत्वाकांक्षा का संचार महसूस करते हैं। यह एक अत्यधिक सक्रिय चरण है जिसमें अक्सर संपत्ति के मामले, भाई-बहन और प्रतिस्पर्धी उद्यम शामिल होते हैं। जबकि यह बाधाओं को दूर करने की शक्ति प्रदान करता है, एक पीड़ित मंगल जल्दबाजी में लिए गए निर्णयों, गुस्से की समस्याओं या छोटी चोटों का कारण बन सकता है।'
                  )}
                </p>
              </div>

              {/* Rahu */}
              <div className="space-y-1">
                <p className="text-xs font-bold text-sacred-gold-dark">{l('Rahu Dasha — 18 Years', 'राहु दशा — 18 वर्ष')}</p>
                <p className="text-xs text-foreground/70 leading-relaxed">
                  {l(
                    'Rahu is the planet of desire and worldly expansion. Spanning 18 years, this is often the most transformative and unpredictable period of life. It can bring sudden rises in status, foreign travels, or innovative breakthroughs. However, it can also create illusions and obsession. The focus is on breaking boundaries and achieving material goals that previously felt out of reach.',
                    'राहु इच्छा और सांसारिक विस्तार का ग्रह है। 18 वर्षों तक चलने वाली यह अवधि अक्सर जीवन की सबसे परिवर्तनकारी और अप्रत्याशित अवधि होती है। यह स्थिति में अचानक वृद्धि, विदेश यात्रा या अभिनव प्रगति ला सकता है। हालाँकि, यह भ्रम और जुनून भी पैदा कर सकता है। ध्यान सीमाओं को तोड़ने और उन भौतिक लक्ष्यों को प्राप्त करने पर होता है जो पहले पहुंच से बाहर महसूस होते थे।'
                  )}
                </p>
              </div>

              {/* Jupiter */}
              <div className="space-y-1">
                <p className="text-xs font-bold text-sacred-gold-dark">{l('Jupiter (Guru) Dasha — 16 Years', 'गुरु दशा — 16 वर्ष')}</p>
                <p className="text-xs text-foreground/70 leading-relaxed">
                  {l(
                    'Jupiter is the "Great Benefic" representing wisdom and wealth. This 16-year dasha is generally a period of spiritual growth, education, and prosperity. It is an excellent time for marriage, the birth of children, and gaining respect in society. You naturally find yourself seeking higher knowledge and acting with more optimism and generosity during this phase.',
                    'गुरु ज्ञान और धन का प्रतिनिधित्व करने वाला "महान शुभ" ग्रह है। यह 16 वर्षीय दशा आम तौर पर आध्यात्मिक विकास, शिक्षा और समृद्धि की अवधि होती है। यह विवाह, संतान के जन्म और समाज में सम्मान प्राप्त करने के लिए एक उत्कृष्ट समय है। आप स्वाभाविक रूप से खुद को उच्च ज्ञान की तलाश में और इस चरण के दौरान अधिक आशावाद और उदारता के साथ कार्य करते हुए पाते हैं।'
                  )}
                </p>
              </div>

              {/* Saturn */}
              <div className="space-y-1">
                <p className="text-xs font-bold text-sacred-gold-dark">{l('Saturn (Shani) Dasha — 19 Years', 'शनि दशा — 19 वर्ष')}</p>
                <p className="text-xs text-foreground/70 leading-relaxed">
                  {l(
                    'Saturn is the planet of Karma and discipline. Over 19 years, it teaches patience and perseverance. This period demands hard work and often brings delays or responsibilities that feel heavy. However, it is the most rewarding dasha in the long run, as it builds a solid foundation for your life and rewards honest effort with permanent status and stability.',
                    'शनि कर्म और अनुशासन का ग्रह है। 19 वर्षों के दौरान, यह धैर्य और दृढ़ता सिखाता है। यह अवधि कड़ी मेहनत की मांग करती है और अक्सर देरी या जिम्मेदारियां लाती है जो भारी महसूस होती हैं। हालाँकि, लंबे समय में यह सबसे फलदायी दशा है, क्योंकि यह आपके जीवन के लिए एक ठोस आधार बनाती है और स्थायी स्थिति और स्थिरता के साथ ईमानदार प्रयास का इनाम देती है।'
                  )}
                </p>
              </div>

              {/* Mercury */}
              <div className="space-y-1">
                <p className="text-xs font-bold text-sacred-gold-dark">{l('Mercury (Budh) Dasha — 17 Years', 'बुध दशा — 17 वर्ष')}</p>
                <p className="text-xs text-foreground/70 leading-relaxed">
                  {l(
                    'Mercury rules the intellect and communication. In this 17-year cycle, the focus is on learning, business ventures, and social networking. It is a busy period for your mind, often involving writing, speaking, and analytical tasks. You may feel more youthful and adaptable, making it a great time for skill development and financial planning.',
                    'बुध बुद्धि और संचार पर शासन करता है। इस 17 वर्षीय चक्र में, ध्यान सीखने, व्यावसायिक उद्यमों और सामाजिक नेटवर्किंग पर होता है। यह आपके दिमाग के लिए एक व्यस्त अवधि है, जिसमें अक्सर लिखना, बोलना और विश्लेषणात्मक कार्य शामिल होते हैं। आप अधिक युवा और अनुकूलनीय महसूस कर सकते हैं, जिससे यह कौशल विकास और वित्तीय योजना के लिए एक महान समय बन जाता है।'
                  )}
                </p>
              </div>

              {/* Ketu */}
              <div className="space-y-1">
                <p className="text-xs font-bold text-sacred-gold-dark">{l('Ketu Dasha — 7 Years', 'केतु दशा — 7 वर्ष')}</p>
                <p className="text-xs text-foreground/70 leading-relaxed">
                  {l(
                    'Ketu is the planet of detachment and liberation. Its 7-year dasha is a time for inner reflection and letting go of material obsessions. While it can cause feelings of isolation or confusion in worldly matters, it is the most powerful period for spiritual breakthroughs and resolving deep-seated karmic patterns. It often brings sudden, unexpected insights.',
                    'केतु वैराग्य और मुक्ति का ग्रह है। इसकी 7 साल की दशा आंतरिक प्रतिबिंब और भौतिक जुनून को छोड़ने का समय है। जबकि यह सांसारिक मामलों में अलगाव या भ्रम की भावना पैदा कर सकता है, यह आध्यात्मिक प्रगति और गहरे कर्म पैटर्न को सुलझाने के लिए सबसे शक्तिशाली अवधि है। यह अक्सर अचानक, अप्रत्याशित अंतर्दृष्टि लाता है।'
                  )}
                </p>
              </div>

              {/* Venus */}
              <div className="space-y-1">
                <p className="text-xs font-bold text-sacred-gold-dark">{l('Venus (Shukra) Dasha — 20 Years', 'शुक्र दशा — 20 वर्ष')}</p>
                <p className="text-xs text-foreground/70 leading-relaxed">
                  {l(
                    'Venus is the planet of love, luxury, and art. The longest dasha (20 years), it brings a focus on relationships, artistic pursuits, and enjoying the comforts of life. If well-placed, this is a period of great happiness, material gains, and pleasant social gatherings. It encourages you to find beauty in the world and cultivate harmonious connections with others.',
                    'शुक्र प्रेम, विलासिता और कला का ग्रह है। सबसे लंबी दशा (20 वर्ष), यह रिश्तों, कलात्मक गतिविधियों और जीवन की सुख-सुविधाओं का आनंद लेने पर ध्यान लाती है। यदि शुभ हो, तो यह महान खुशी, भौतिक लाभ और सुखद सामाजिक मेलजोल की अवधि है। यह आपको दुनिया में सुंदरता खोजने और दूसरों के साथ सामंजस्यपूर्ण संबंध विकसित करने के लिए प्रोत्साहित करता है।'
                  )}
                </p>
              </div>
            </div>
          </div>

          <div className="p-4 bg-sacred-gold-dark/[0.03] rounded-lg border border-sacred-gold/20">
            <h4 className="text-xs font-bold text-sacred-gold-dark uppercase mb-2 flex items-center gap-2">
              <Calendar className="w-3.5 h-3.5" />
              {l('Practical Interpretation Tip', 'व्यावहारिक व्याख्या टिप')}
            </h4>
            <p className="text-xs text-foreground/80 leading-relaxed">
              {l(
                'The Dasha Lord is the "temporary boss" of your life. If the boss is well-placed in your birth chart (e.g., in their own sign or an exalted sign), the period brings growth. If the boss is weak, it brings learning through challenges.',
                'दशा स्वामी आपके जीवन का "अस्थायी बॉस" है। यदि बॉस आपकी जन्म कुंडली में अच्छी तरह से स्थित है (जैसे, अपनी राशि में या उच्च राशि में), तो अवधि विकास लाती है। यदि बॉस कमजोर है, तो यह चुनौतियों के माध्यम से सीख लाता है।'
              )}
            </p>
          </div>
        </div>

        <div className="mt-8 pt-4 border-t border-sacred-gold/20">
          <p className="text-[11px] text-foreground/50 italic text-center">
            {l(
              'Note: The final results are a blend of the Mahadasha lord and the Antardasha lord. Always look at both to understand the current phase.',
              'नोट: अंतिम परिणाम महादशा स्वामी और अंतर्दशा स्वामी का मिश्रण होते हैं। वर्तमान चरण को समझने के लिए हमेशा दोनों को देखें।'
            )}
          </p>
        </div>
      </div>
    </div>
  );
}

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
    <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
      <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">{hi ? 'सूक्ष्म-प्राण दशा' : 'Sookshma-Prana Dasha'}</div>
      <div className="overflow-x-auto">
        <Table className="w-full text-xs table-fixed">
          <TableHeader>
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

  let content;

  if (extendedDashaData) {
    const currentMD = extendedDashaData.mahadasha?.find((md: any) => md.is_current);
    const currentAD = currentMD?.antardasha?.find((ad: any) => ad.is_current);
    const currentPT = currentAD?.pratyantar?.find((pt: any) => pt.is_current);

    content = (
      <div className="space-y-6">
        {/* Current Dasha Summary Table */}
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center justify-between">
            <span>{t('section.currentDashaStatus')}</span>
            <span className="px-2 py-0.5 bg-white/20 text-white text-[10px] font-bold rounded animate-pulse">● {l('LIVE', 'लाइव')}</span>
          </div>
          <div>
            <Table className="w-full text-xs table-fixed">
              <TableHeader>
                <TableRow>
                  <TableHead className="text-left p-1.5 text-primary font-semibold uppercase tracking-wide w-[25%]">{t('kundli.mahadasha')}</TableHead>
                  <TableHead className="text-left p-1.5 text-primary font-semibold uppercase tracking-wide w-[25%]">{t('kundli.antardasha')}</TableHead>
                  <TableHead className="text-left p-1.5 text-primary font-semibold uppercase tracking-wide w-[25%]">{t('kundli.pratyantar')}</TableHead>
                  <TableHead className="text-center p-1.5 text-primary font-semibold uppercase tracking-wide w-[25%]">{hi ? 'अवधि' : 'Period'}</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                <TableRow className="border-t border-border hover:bg-muted/5 font-semibold">
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
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">{hi ? 'विस्तृत दशा तालिका' : 'Detailed Dasha Timeline'}</div>
          <div>
            <Table className="w-full text-xs table-fixed">
              <TableHeader>
                <TableRow>
                  <TableHead className="w-8 p-1.5"></TableHead>
                  <TableHead className="text-left p-1.5 text-primary font-semibold uppercase tracking-wide w-[28%]">{hi ? 'दशा स्वामी' : 'Dasha Lord'}</TableHead>
                  <TableHead className="text-left p-1.5 text-primary font-semibold uppercase tracking-wide w-[22%]">{t('table.start')}</TableHead>
                  <TableHead className="text-left p-1.5 text-primary font-semibold uppercase tracking-wide w-[22%]">{t('table.end')}</TableHead>
                  <TableHead className="text-center p-1.5 text-primary font-semibold uppercase tracking-wide w-[15%]">{t('table.years')}</TableHead>
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
                              className={`cursor-pointer transition-colors ${ad.is_current ? 'bg-primary/5 border-l-2 border-l-primary' : 'hover:bg-muted/5'}`}
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

                            {/* Antardasha Synthesis + Effect + Severity */}
                            {isAdExpanded && ad.analysis && (
                              <TableRow className="bg-indigo-50/30">
                                <TableCell colSpan={5} className="p-3 pl-8 space-y-2">
                                  {/* Severity badge */}
                                  {ad.analysis.severity && (
                                    <div className="flex flex-wrap items-center gap-2">
                                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${
                                        ad.analysis.severity === 'favorable'
                                          ? 'bg-emerald-100 text-emerald-800 border-emerald-300'
                                          : ad.analysis.severity === 'challenging'
                                            ? 'bg-rose-100 text-rose-800 border-rose-300'
                                            : 'bg-amber-100 text-amber-800 border-amber-300'
                                      }`}>
                                        {ad.analysis.severity.charAt(0).toUpperCase() + ad.analysis.severity.slice(1)}
                                      </span>
                                      {(ad.analysis.severity_factors || []).map((f: string) => (
                                        <span key={f} className="text-[9px] px-1 py-0.5 rounded bg-background border border-border text-foreground/60 uppercase">{f.replace(/_/g, ' ')}</span>
                                      ))}
                                    </div>
                                  )}
                                  {/* Phala effect */}
                                  {(ad.analysis.effect_en || ad.analysis.effect_hi) && (
                                    <p className="text-[11px] text-indigo-900 leading-relaxed">
                                      <span className="font-semibold text-indigo-700">{hi ? 'फल: ' : 'Effect: '}</span>
                                      {hi ? (ad.analysis.effect_hi || ad.analysis.effect_en) : (ad.analysis.effect_en || ad.analysis.effect_hi)}
                                    </p>
                                  )}
                                  {/* Combined synthesis */}
                                  {(ad.analysis.combined_synthesis_en || ad.analysis.combined_synthesis_hi) && (
                                    <p className="text-[11px] text-indigo-900/80 leading-relaxed italic">
                                      <span className="font-semibold not-italic text-indigo-700">{hi ? 'विश्लेषण: ' : 'Analysis: '}</span>
                                      {hi ? (ad.analysis.combined_synthesis_hi || ad.analysis.combined_synthesis_en) : (ad.analysis.combined_synthesis_en || ad.analysis.combined_synthesis_hi)}
                                    </p>
                                  )}
                                  {/* Sloka reference */}
                                  {ad.analysis.sloka_ref && (
                                    <p className="text-[9px] italic text-foreground/40">{ad.analysis.sloka_ref}</p>
                                  )}
                                </TableCell>
                              </TableRow>
                            )}

                            {/* Pratyantar Rows */}
                            {isAdExpanded && (ad.pratyantar || []).map((pt: any, idx: number) => (
                              <TableRow
                                key={idx}
                                className={`transition-colors ${pt.is_current ? 'bg-primary/5' : 'hover:bg-muted/5'}`}
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
  } else if (dashaData) {
    content = (
      <div className="space-y-4">
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent p-4">
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

        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">{hi ? 'दशा तालिका' : 'Dasha Timeline'}</div>
          <div className="overflow-x-auto">
            <Table className="w-full text-xs table-fixed">
              <TableHeader>
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
  } else {
    content = (
      <div className="flex flex-col items-center justify-center py-12">
        <p className="text-foreground mb-3 text-sm">{t('kundli.clickDashaTab')}</p>
        <span className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-muted/10 border border-border text-primary text-sm font-medium cursor-default">
          <ChevronDown className="w-4 h-4" />
          {t('kundli.clickDashaTab')}
        </span>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {content}
      {/* Dasha Theory Section — ALWAYS visible educational summary */}
      <DashaTheorySection language={language} />
    </div>
  );
}
