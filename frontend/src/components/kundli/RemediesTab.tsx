import { useEffect, useMemo, useState } from 'react';
import { Loader2, Sparkles, Calendar, Zap } from 'lucide-react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Heading } from '@/components/ui/heading';
import { apiFetch } from '@/lib/api';
import GeneralRemedies from '@/components/kundli/GeneralRemedies';

interface Props {
  kundliId: string;
  language: string;
  t: (key: string) => string;
}

export default function RemediesTab({ kundliId, language, t }: Props) {
  const isHi = language === 'hi';
  const [active, setActive] = useState<'general' | 'yearly'>('general');
  const [year, setYear] = useState(() => new Date().getFullYear());

  const [yearlyData, setYearlyData] = useState<any>(null);
  const [loadingYearly, setLoadingYearly] = useState(false);

  useEffect(() => {
    if (!kundliId) return;
    if (active !== 'yearly') return;
    
    setLoadingYearly(true);
    apiFetch('/api/kundli/remedies', {
      method: 'POST',
      body: JSON.stringify({ kundli_id: kundliId, year: year }),
    })
      .then((data) => {
        if (data?.yearly_remedies) setYearlyData(data.yearly_remedies);
      })
      .catch(() => setYearlyData(null))
      .finally(() => setLoadingYearly(false));
  }, [kundliId, active, year]);

  return (
    <div className="space-y-6">
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
          <Sparkles className="w-6 h-6" />
          {isHi ? 'ज्योतिषीय उपाय' : 'Astrological Remedies'}
        </Heading>
        <p className="text-sm text-muted-foreground">
          {isHi 
            ? 'आपके जन्म चार्ट और वर्तमान ग्रहों के गोचर पर आधारित व्यक्तिगत मार्गदर्शन' 
            : 'Personalized guidance based on your birth chart and current planetary transits.'}
        </p>
      </div>

      <Tabs value={active} onValueChange={(v) => setActive(v as any)} className="w-full">
        <TabsList className="grid grid-cols-2 w-full max-w-[520px] bg-muted/50 p-1 rounded-xl border border-border/50">
          <TabsTrigger value="general" className="rounded-lg data-[state=active]:bg-background data-[state=active]:shadow-sm">
            <Zap className="w-3.5 h-3.5 mr-2" />
            {isHi ? 'स्थायी उपाय' : 'General Remedies'}
          </TabsTrigger>
          <TabsTrigger value="yearly" className="rounded-lg data-[state=active]:bg-background data-[state=active]:shadow-sm">
            <Calendar className="w-3.5 h-3.5 mr-2" />
            {isHi ? 'वार्षिक उपाय' : 'Yearly Remedies'}
          </TabsTrigger>
        </TabsList>

        <TabsContent value="general" className="space-y-4 animate-in fade-in duration-500">
          <GeneralRemedies language={language} t={t} kundliId={kundliId} />
        </TabsContent>

        <TabsContent value="yearly" className="space-y-6 animate-in fade-in duration-500 mt-6">
          <div className="flex items-center justify-between bg-card p-4 rounded-xl border border-border shadow-sm">
            <div className="flex items-center gap-3">
              <div className="bg-primary/10 p-2 rounded-lg">
                <Calendar className="w-5 h-5 text-primary" />
              </div>
              <div>
                <p className="text-xs text-muted-foreground font-bold uppercase tracking-wider">{isHi ? 'अवधि चयन' : 'Period Selection'}</p>
                <p className="text-sm font-medium">{isHi ? 'वर्ष' : 'Year'} {year} {isHi ? 'के लिए मार्गदर्शन' : 'Guidance'}</p>
              </div>
            </div>
            
            <select
              value={year}
              onChange={(e) => setYear(Number(e.target.value))}
              className="bg-muted hover:bg-muted/80 border border-border rounded-lg px-4 py-2 text-foreground text-sm font-bold focus:ring-2 focus:ring-primary/20 transition-all outline-none"
            >
              {Array.from({ length: 10 }, (_, i) => new Date().getFullYear() - 2 + i).map((yr) => (
                <option key={yr} value={yr}>{yr}</option>
              ))}
            </select>
          </div>

          {loadingYearly && (
            <div className="flex flex-col items-center justify-center py-20">
              <Loader2 className="w-10 h-10 animate-spin text-primary/40 mb-4" />
              <p className="text-sm text-muted-foreground animate-pulse">
                {isHi ? 'वार्षिक चक्रों का विश्लेषण किया जा रहा है...' : 'Analyzing yearly cycles...'}
              </p>
            </div>
          )}

          {!loadingYearly && yearlyData && yearlyData.length > 0 ? (
            <div className="space-y-6">
              {yearlyData.map((section: any, sidx: number) => (
                <div key={sidx} className="bg-card rounded-2xl border border-primary/20 overflow-hidden shadow-sm">
                  <div className="bg-primary/5 px-6 py-4 border-b border-primary/10">
                    <div className="flex items-center justify-between">
                      <h3 className="text-lg font-bold text-primary flex items-center gap-2">
                        {section.category || (isHi ? 'समय का प्रभाव' : 'Timing Influence')}
                      </h3>
                      <span className="text-[10px] font-black uppercase tracking-widest bg-primary/10 text-primary px-2 py-0.5 rounded">
                        {section.based_on}
                      </span>
                    </div>
                    <p className="text-sm text-foreground/80 mt-2 leading-relaxed">
                      {section.summary}
                    </p>
                  </div>
                  
                  <div className="p-6 grid grid-cols-1 md:grid-cols-2 gap-4">
                    {section.remedies.map((rem: any, ridx: number) => (
                      <div key={ridx} className="bg-muted/30 rounded-xl p-5 border border-border/40 flex flex-col">
                        <div className="flex items-center gap-2 mb-3">
                           <Sparkles className="w-4 h-4 text-primary" />
                           <span className="text-sm font-bold uppercase tracking-wide text-primary">{rem.title}</span>
                        </div>
                        
                        <div className="space-y-3 flex-grow">
                          <div>
                            <p className="text-[10px] uppercase font-bold text-muted-foreground tracking-tighter">{isHi ? 'क्या करें' : 'What to do'}</p>
                            <p className="text-sm text-foreground leading-snug">{rem.what_to_do}</p>
                          </div>
                          
                          <div>
                            <p className="text-[10px] uppercase font-bold text-muted-foreground tracking-tighter">{isHi ? 'कैसे करें' : 'How to do'}</p>
                            <p className="text-sm text-foreground/80 leading-snug">{rem.how_to_do}</p>
                          </div>

                          {(rem.when_to_do || rem.frequency) && (
                            <div className="flex gap-4 pt-1">
                              {rem.when_to_do && (
                                <div>
                                  <p className="text-[10px] uppercase font-bold text-muted-foreground tracking-tighter">{isHi ? 'कब' : 'When'}</p>
                                  <p className="text-xs font-medium text-foreground">{rem.when_to_do}</p>
                                </div>
                              )}
                            </div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          ) : !loadingYearly && active === 'yearly' && (
             <div className="flex flex-col items-center justify-center py-16 bg-muted/20 rounded-2xl border border-dashed border-border">
                <p className="text-sm text-muted-foreground">
                  {isHi ? 'इस वर्ष के लिए कोई विशेष उपाय आवश्यक नहीं हैं।' : 'No specific yearly remedies required for this period.'}
                </p>
             </div>
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
}
