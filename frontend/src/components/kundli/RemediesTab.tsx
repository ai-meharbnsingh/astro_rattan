import { useEffect, useMemo, useState } from 'react';
import { Loader2, Sparkles } from 'lucide-react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Heading } from '@/components/ui/heading';
import { api } from '@/lib/api';
import { translatePlanet, translateRemedy } from '@/lib/backend-translations';
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

  const [varshphal, setVarshphal] = useState<any>(null);
  const [loadingVarshphal, setLoadingVarshphal] = useState(false);

  const [enriched, setEnriched] = useState<any[] | null>(null);
  const [loadingEnriched, setLoadingEnriched] = useState(false);

  useEffect(() => {
    if (!kundliId) return;
    let cancelled = false;
    setLoadingEnriched(true);
    api.get<any>(`/api/lalkitab/remedies/enriched/${kundliId}`)
      .then((res) => { if (!cancelled) setEnriched(Array.isArray(res) ? res : res?.enriched || res?.remedies || res?.data || null); })
      .catch(() => { if (!cancelled) setEnriched(null); })
      .finally(() => { if (!cancelled) setLoadingEnriched(false); });
    return () => { cancelled = true; };
  }, [kundliId]);

  useEffect(() => {
    if (!kundliId) return;
    if (active !== 'yearly') return;
    let cancelled = false;
    setLoadingVarshphal(true);
    api.post<any>(`/api/kundli/${kundliId}/varshphal`, { year })
      .then((res) => { if (!cancelled) setVarshphal(res); })
      .catch(() => { if (!cancelled) setVarshphal(null); })
      .finally(() => { if (!cancelled) setLoadingVarshphal(false); });
    return () => { cancelled = true; };
  }, [kundliId, active, year]);

  const yearLord = String(varshphal?.year_lord || '').trim();

  const yearLordRemedy = useMemo(() => {
    if (!yearLord) return null;
    const list = Array.isArray(enriched) ? enriched : [];
    return list.find((r: any) => String(r?.planet || '').trim() === yearLord) || null;
  }, [enriched, yearLord]);

  return (
    <div className="space-y-6">
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
          <Sparkles className="w-6 h-6" />
          {isHi ? 'उपाय' : 'Remedies'}
        </Heading>
        <p className="text-sm text-muted-foreground">
          {isHi ? 'कुंडली के आधार पर सामान्य और वार्षिक उपाय' : 'General and yearly remedies based on the chart'}
        </p>
      </div>

      <Tabs value={active} onValueChange={(v) => setActive(v as any)} className="w-full">
        <TabsList className="grid grid-cols-2 w-full max-w-[520px]">
          <TabsTrigger value="general">{isHi ? 'सामान्य उपाय' : 'General Remedies'}</TabsTrigger>
          <TabsTrigger value="yearly">{isHi ? 'वार्षिक उपाय' : 'Yearly Remedies'}</TabsTrigger>
        </TabsList>

        <TabsContent value="general" className="space-y-4">
          <GeneralRemedies language={language} t={t} kundliId={kundliId} />
        </TabsContent>

        <TabsContent value="yearly" className="space-y-4">
          <div className="flex items-center gap-4">
            <label className="text-sm font-medium text-foreground">{isHi ? 'वर्ष:' : 'Year:'}</label>
            <select
              value={year}
              onChange={(e) => setYear(Number(e.target.value))}
              className="bg-muted border border-border rounded-lg px-3 py-2 text-foreground text-sm focus:border-border focus:outline-none"
            >
              {Array.from({ length: 20 }, (_, i) => new Date().getFullYear() - 10 + i).map((yr) => (
                <option key={yr} value={yr}>{yr}</option>
              ))}
            </select>
          </div>

          {(loadingVarshphal || loadingEnriched) && (
            <div className="flex items-center justify-center py-10 text-sm text-muted-foreground">
              <Loader2 className="w-5 h-5 animate-spin mr-2 text-primary" />
              {isHi ? 'लोड हो रहा है...' : 'Loading...'}
            </div>
          )}

          {!loadingVarshphal && varshphal && (
            <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
              <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
                {isHi ? 'वर्ष-उपाय' : 'Yearly Remedy'}
              </div>
              <div className="p-4 space-y-3 text-sm">
                <div className="grid grid-cols-2 gap-3">
                  <div className="rounded-lg border border-border p-3">
                    <p className="text-xs text-muted-foreground">{isHi ? 'वर्षेश्वर' : 'Year Lord'}</p>
                    <p className="font-semibold text-primary mt-0.5">{translatePlanet(yearLord, language) || '—'}</p>
                  </div>
                  <div className="rounded-lg border border-border p-3">
                    <p className="text-xs text-muted-foreground">{isHi ? 'सोलर रिटर्न' : 'Solar Return'}</p>
                    <p className="font-semibold text-foreground mt-0.5">
                      {varshphal?.solar_return?.date ? `${varshphal.solar_return.date} ${varshphal.solar_return.time || ''}` : '—'}
                    </p>
                  </div>
                </div>

                {yearLordRemedy?.remedy_en ? (
                  <div className="rounded-lg border border-border bg-card p-3">
                    <p className="text-xs text-muted-foreground mb-1">{isHi ? 'अनुशंसित उपाय' : 'Recommended Remedy'}</p>
                    <p className="font-semibold text-foreground">{translateRemedy(yearLordRemedy.remedy_en, language)}</p>
                    {(yearLordRemedy.day || yearLordRemedy.material) && (
                      <p className="text-xs text-muted-foreground mt-1">
                        {yearLordRemedy.day ? `${isHi ? 'दिन' : 'Day'}: ${yearLordRemedy.day}` : ''}
                        {yearLordRemedy.day && yearLordRemedy.material ? ' • ' : ''}
                        {yearLordRemedy.material ? `${isHi ? 'सामग्री' : 'Material'}: ${yearLordRemedy.material}` : ''}
                      </p>
                    )}
                  </div>
                ) : (
                  <div className="rounded-lg border border-amber-200 bg-amber-50 p-3 text-amber-800 text-sm">
                    {isHi ? 'इस वर्ष के लिए कोई विशेष उपाय उपलब्ध नहीं।' : 'No specific yearly remedy available.'}
                  </div>
                )}
              </div>
            </div>
          )}

          {!loadingVarshphal && active === 'yearly' && kundliId && !varshphal && (
            <div className="rounded-xl border border-amber-200 bg-amber-50 p-4 text-amber-800 text-sm">
              {isHi ? 'वर्षफल लोड नहीं हो पाया।' : 'Failed to load Varshphal.'}
            </div>
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
}

