import { Sparkles, Loader2, Info, CheckCircle, AlertCircle, AlertTriangle } from 'lucide-react';
import { useState, useEffect } from 'react';
import { apiFetch } from '@/lib/api';
import { useTranslation } from '@/lib/i18n';
import { Heading } from '@/components/ui/heading';

interface RemedyItem {
  type: string;
  title: string;
  what_to_do: string;
  how_to_do: string;
  when_to_do?: string;
  frequency?: string;
  expected_benefit?: string;
  caution?: string;
  source_type: string;
  source_label: string;
  scriptural_reference?: string;
}

interface RemedyCategory {
  category: string;
  problem_detected: string;
  why_it_matters: string;
  remedies: RemedyItem[];
}

interface GeneralRemediesProps {
  language: string;
  t?: (key: string) => string;
  title?: string;
  kundliId?: string;
}

export default function GeneralRemedies({ language, t: tProp, title, kundliId }: GeneralRemediesProps) {
  const { t: tContext } = useTranslation();
  const t = tProp ?? tContext;
  const isHi = language === 'hi';
  const [categories, setCategories] = useState<RemedyCategory[] | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (kundliId) {
      setLoading(true);
      apiFetch('/api/kundli/remedies', {
        method: 'POST',
        body: JSON.stringify({ kundli_id: kundliId }),
      })
        .then((data) => {
          if (data?.general_remedies) setCategories(data.general_remedies);
        })
        .catch((err) => {
          console.error('Error fetching remedies:', err);
        })
        .finally(() => setLoading(false));
    }
  }, [kundliId]);

  const defaultTitle = isHi ? 'ज्योतिषीय उपाय' : 'Astrological Remedies';

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'mantra': return <Sparkles className="w-4 h-4 text-purple-500" />;
      case 'daan': return <CheckCircle className="w-4 h-4 text-emerald-500" />;
      case 'behavioral': return <Info className="w-4 h-4 text-blue-500" />;
      case 'puja': return <AlertCircle className="w-4 h-4 text-orange-500" />;
      default: return <Sparkles className="w-4 h-4 text-primary" />;
    }
  };

  return (
    <div className="space-y-6 mt-6">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <Sparkles className="w-6 h-6 text-primary" />
          <Heading as={3} variant={3}>{title || defaultTitle}</Heading>
        </div>
        {loading && <Loader2 className="w-5 h-5 animate-spin text-primary" />}
      </div>

      <p className="text-sm text-muted-foreground italic -mt-4">
        {isHi 
          ? 'नारद पुराण और पारंपरिक वैदिक सिद्धांतों पर आधारित व्यक्तिगत उपाय' 
          : 'Personalized remedies based on Narad Puran and traditional Vedic principles.'}
      </p>
      
      {loading && !categories && (
        <div className="flex flex-col items-center justify-center py-20 bg-muted/30 rounded-2xl border border-dashed border-border">
          <Loader2 className="w-10 h-10 animate-spin text-primary/40 mb-4" />
          <p className="text-muted-foreground animate-pulse">
            {isHi ? 'आपके लिए उत्तम उपायों की गणना की जा रही है...' : 'Calculating best remedies for you...'}
          </p>
        </div>
      )}

      {/* Dynamic Results if available */}
      {categories && categories.length > 0 && categories.map((cat, cidx) => (
        <div key={cidx} className="bg-card rounded-2xl border-2 border-sacred-gold/30 overflow-hidden shadow-md hover:shadow-lg transition-all duration-300">
          <div className="bg-sacred-gold/20 px-6 py-5 border-b border-sacred-gold/30">
            <div className="flex items-center gap-3">
              <span className="bg-sacred-gold-dark text-white text-[10px] font-black px-2.5 py-1 rounded-md uppercase tracking-widest shadow-sm">
                {cat.category}
              </span>
            </div>
            <div className="mt-4 space-y-2">
              <p className="text-sm font-bold text-foreground flex items-baseline gap-2">
                <span className="text-red-600 shrink-0 text-xs font-black uppercase tracking-tighter">{isHi ? 'समस्या:' : 'PROBLEM:'}</span> 
                <span className="leading-tight">{cat.problem_detected}</span>
              </p>
              <div className="bg-white/40 p-3 rounded-lg border border-sacred-gold/10">
                <p className="text-xs text-foreground/80 leading-relaxed italic">
                  "{cat.why_it_matters}"
                </p>
              </div>
            </div>
          </div>
          
          <div className="p-6 grid grid-cols-1 lg:grid-cols-2 gap-5 bg-gradient-to-br from-white to-sacred-gold/5">
            {cat.remedies && cat.remedies.map((rem, ridx) => (
              <div key={ridx} className="relative bg-white rounded-xl p-5 border border-sacred-gold/20 shadow-sm hover:border-sacred-gold/50 transition-colors flex flex-col h-full">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-2">
                    <div className="p-1.5 rounded-lg bg-sacred-gold/10 text-sacred-gold-dark">
                      {getTypeIcon(rem.type)}
                    </div>
                    <span className="text-sm font-black uppercase tracking-wider text-sacred-gold-dark">{rem.title}</span>
                  </div>
                  {rem.source_type === 'narad_puran' && (
                    <span className="text-[9px] font-bold bg-purple-100 text-purple-700 px-2 py-0.5 rounded-full border border-purple-200 uppercase">Narad Puran</span>
                  )}
                </div>
                
                <div className="space-y-4 flex-grow">
                  <div className="space-y-1">
                    <p className="text-[10px] uppercase font-black text-sacred-gold-dark/60 tracking-widest">{isHi ? 'क्या करें' : 'THE RITUAL'}</p>
                    <p className="text-[13px] text-foreground font-semibold leading-snug">{rem.what_to_do}</p>
                  </div>
                  
                  <div className="space-y-1">
                    <p className="text-[10px] uppercase font-black text-sacred-gold-dark/60 tracking-widest">{isHi ? 'विधि' : 'HOW TO PERFORM'}</p>
                    <p className="text-[13px] text-foreground/70 leading-relaxed">{rem.how_to_do}</p>
                  </div>

                  <div className="flex flex-wrap gap-4 pt-2">
                    {rem.when_to_do && (
                      <div className="bg-muted/50 px-2 py-1 rounded border border-border/50">
                        <p className="text-[9px] uppercase font-bold text-muted-foreground tracking-tighter">{isHi ? 'समय' : 'WHEN'}</p>
                        <p className="text-[11px] font-bold text-foreground">{rem.when_to_do}</p>
                      </div>
                    )}
                    {rem.frequency && (
                      <div className="bg-muted/50 px-2 py-1 rounded border border-border/50">
                        <p className="text-[9px] uppercase font-bold text-muted-foreground tracking-tighter">{isHi ? 'आवृत्ति' : 'FREQUENCY'}</p>
                        <p className="text-[11px] font-bold text-foreground">{rem.frequency}</p>
                      </div>
                    )}
                  </div>

                  {rem.expected_benefit && (
                    <div className="pt-3 border-t border-sacred-gold/10">
                      <p className="text-[10px] uppercase font-black text-emerald-700 tracking-widest flex items-center gap-1 mb-1">
                         <CheckCircle className="w-3 h-3" /> {isHi ? 'अपेक्षित लाभ' : 'KEY BENEFIT'}
                      </p>
                      <p className="text-[12px] text-emerald-800/80 font-medium italic leading-snug">{rem.expected_benefit}</p>
                    </div>
                  )}
                </div>

                <div className="mt-5 pt-3 border-t border-dashed border-sacred-gold/20 flex items-center justify-between">
                  <div className="flex items-center gap-1.5 opacity-50 grayscale hover:opacity-100 transition-all cursor-help" title={rem.source_label}>
                    <BookOpenIcon className="w-3.5 h-3.5 text-sacred-gold-dark" />
                    <span className="text-[10px] font-bold text-sacred-gold-dark">{rem.source_label}</span>
                  </div>
                  {rem.type === 'gemstone' && (
                    <div className="flex items-center gap-1 text-red-600 bg-red-50 px-2 py-0.5 rounded border border-red-100 animate-pulse">
                      <AlertTriangle className="w-3 h-3" />
                      <span className="text-[9px] font-black uppercase tracking-tighter">{isHi ? 'सावधानी' : 'CAUTION'}</span>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}

      {/* No chart-based remedies fallback */}
      {(!categories || categories.length === 0) && !loading && (
        <div className="flex flex-col items-center justify-center py-12 bg-muted/20 rounded-2xl border border-border">
          <p className="text-sm text-muted-foreground text-center">
            {t('auto.noChartSpecificRemedies')}
          </p>
        </div>
      )}
    </div>
  );
}

function BookOpenIcon({ className }: { className?: string }) {
  return (
    <svg 
      xmlns="http://www.w3.org/2000/svg" 
      width="24" 
      height="24" 
      viewBox="0 0 24 24" 
      fill="none" 
      stroke="currentColor" 
      strokeWidth="2" 
      strokeLinecap="round" 
      strokeLinejoin="round" 
      className={className}
    >
      <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z" />
      <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z" />
    </svg>
  );
}
