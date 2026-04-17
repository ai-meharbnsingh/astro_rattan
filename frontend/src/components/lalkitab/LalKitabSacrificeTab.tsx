import { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import { Loader2, ArrowRight, AlertTriangle, Sparkles } from 'lucide-react';

interface SacrificeResult {
  rule_id: string; sacrificer: string; victim: string;
  severity: 'high' | 'medium' | 'low';
  condition: string;
  message: { en: string; hi: string };
  growth_area: { planet: string; areas: { en: string; hi: string } };
  cost_area: { planet: string; areas: { en: string; hi: string } };
  remedy: { en: string; hi: string };
}
interface SacrificeData { kundli_id: string; sacrifice_count: number; has_sacrifices: boolean; results: SacrificeResult[]; }

interface Props { kundliId?: string; language: string; }

const PLANET_DOT: Record<string, string> = {
  Sun:'bg-orange-500', Moon:'bg-blue-300', Mars:'bg-red-500', Mercury:'bg-green-500',
  Jupiter:'bg-yellow-500', Venus:'bg-pink-400', Saturn:'bg-gray-500', Rahu:'bg-purple-600', Ketu:'bg-amber-700',
};
const SEVERITY_STYLE: Record<string, string> = {
  high: 'bg-red-100 text-red-700 border-red-200',
  medium: 'bg-orange-100 text-orange-700 border-orange-200',
  low: 'bg-yellow-100 text-yellow-700 border-yellow-200',
};

export default function LalKitabSacrificeTab({ kundliId, language }: Props) {
  const [data, setData] = useState<SacrificeData | null>(null);
  const [loading, setLoading] = useState(false);
  const hi = language === 'hi';

  useEffect(() => {
    if (!kundliId) return;
    setLoading(true);
    api.get(`/api/lalkitab/sacrifice/${kundliId}`)
      .then(setData).catch(() => {}).finally(() => setLoading(false));
  }, [kundliId]);

  if (!kundliId) return (
    <div className="text-center py-10 text-muted-foreground text-sm">
      {hi ? 'विश्लेषण के लिए कुंडली सहेजें।' : 'Save a Kundli to see sacrifice analysis.'}
    </div>
  );
  if (loading) return <div className="flex justify-center py-16"><Loader2 className="w-8 h-8 animate-spin text-sacred-gold" /></div>;
  if (!data) return null;

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="text-center">
        <div className="text-3xl mb-1">🐐</div>
        <h3 className="font-bold text-foreground">
          {hi ? 'बलि का बकरा — बलिदान विश्लेषण' : 'Bali Ka Bakra — Sacrifice Analysis'}
        </h3>
        <p className="text-sm text-muted-foreground mt-1">
          {hi
            ? 'जब एक ग्रह स्वयं नहीं बल्कि दूसरे ग्रह की कारकता की बलि देता है'
            : 'When one planet sacrifices the significations of another without suffering itself'}
        </p>
      </div>

      {/* Summary */}
      <div className={`rounded-xl p-4 text-center ${data.has_sacrifices ? 'bg-red-50 border border-red-200' : 'bg-green-50 border border-green-200'}`}>
        {data.has_sacrifices ? (
          <>
            <div className="text-2xl font-bold text-red-700">{data.sacrifice_count}</div>
            <div className="text-sm text-red-600">
              {hi ? `${data.sacrifice_count} बलिदान पैटर्न मिले` : `${data.sacrifice_count} sacrifice pattern(s) detected`}
            </div>
          </>
        ) : (
          <>
            <div className="text-2xl">✅</div>
            <div className="text-sm text-green-700">
              {hi ? 'कोई बलिदान पैटर्न नहीं मिला।' : 'No sacrifice patterns detected. All planets operate independently.'}
            </div>
          </>
        )}
      </div>

      {/* Sacrifice Chain Visual + Cards */}
      {data.results.map((result, i) => (
        <div key={result.rule_id} className={`border rounded-xl p-4 ${SEVERITY_STYLE[result.severity] || 'border-border bg-card'}`}>
          {/* Chain visual */}
          <div className="flex items-center gap-3 mb-3">
            <div className="flex items-center gap-2">
              <span className={`w-3 h-3 rounded-full ${PLANET_DOT[result.sacrificer] || 'bg-gray-400'}`} />
              <span className="font-bold text-foreground">{result.sacrificer}</span>
            </div>
            <ArrowRight className="w-4 h-4 text-red-500" />
            <div className="px-2 py-0.5 rounded bg-red-100 text-red-700 text-xs font-bold">
              {hi ? 'बलि देता है' : 'SACRIFICES'}
            </div>
            <ArrowRight className="w-4 h-4 text-red-500" />
            <div className="flex items-center gap-2">
              <span className={`w-3 h-3 rounded-full ${PLANET_DOT[result.victim] || 'bg-gray-400'}`} />
              <span className="font-bold text-foreground">{result.victim === 'siblings' ? (hi?'भाई-बहन':'Siblings') : result.victim}</span>
            </div>
            <span className={`ml-auto text-xs px-2 py-0.5 rounded-full font-semibold ${SEVERITY_STYLE[result.severity]}`}>
              {result.severity.toUpperCase()}
            </span>
          </div>

          {/* Growth vs Cost */}
          <div className="grid grid-cols-2 gap-2 mb-3">
            <div className="bg-white/60 rounded-lg p-2">
              <div className="text-xs font-semibold text-green-700 mb-1">📈 {hi ? 'जो बढ़ता है' : 'What GROWS'}</div>
              <div className="text-xs text-foreground">{hi ? result.growth_area.areas.hi : result.growth_area.areas.en}</div>
            </div>
            <div className="bg-white/60 rounded-lg p-2">
              <div className="text-xs font-semibold text-red-700 mb-1">📉 {hi ? 'जो पीड़ित होता है' : 'What SUFFERS'}</div>
              <div className="text-xs text-foreground">{hi ? result.cost_area.areas.hi : result.cost_area.areas.en}</div>
            </div>
          </div>

          {/* Message */}
          <p className="text-sm text-foreground leading-relaxed mb-3 italic">
            "{hi ? result.message.hi : result.message.en}"
          </p>

          {/* Remedy */}
          <div className="flex items-start gap-2 bg-white/70 rounded-lg p-2.5">
            <Sparkles className="w-3.5 h-3.5 text-sacred-gold mt-0.5 shrink-0" />
            <div>
              <div className="text-xs font-semibold text-sacred-gold mb-0.5">{hi ? 'उपाय' : 'Remedy'}</div>
              <div className="text-xs text-foreground">{hi ? result.remedy.hi : result.remedy.en}</div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
