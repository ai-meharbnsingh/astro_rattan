import { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import { pickLang } from '@/components/lalkitab/safe-render';
import { Loader2, AlertTriangle, ShieldAlert, Ban } from 'lucide-react';

interface ForbiddenRule {
  planet: string; house: number; severity: 'critical' | 'high' | 'moderate';
  category: string;
  action: { en: string; hi: string };
  reason: { en: string; hi: string };
  consequence: { en: string; hi: string };
}
interface ForbiddenData { kundli_id: string; forbidden_count: number; rules: ForbiddenRule[]; }

interface Props { kundliId?: string; language: string; }

const PLANET_DOT: Record<string, string> = {
  Sun:'bg-orange-500', Moon:'bg-blue-300', Mars:'bg-red-500', Mercury:'bg-green-500',
  Jupiter:'bg-yellow-500', Venus:'bg-pink-400', Saturn:'bg-gray-500', Rahu:'bg-purple-600', Ketu:'bg-amber-700',
};
const SEVERITY_STYLE: Record<string, string> = {
  critical: 'border-red-400 bg-red-50',
  high: 'border-orange-300 bg-orange-50',
  moderate: 'border-yellow-300 bg-yellow-50',
};
const SEVERITY_BADGE: Record<string, string> = {
  critical: 'bg-red-100 text-red-700',
  high: 'bg-orange-100 text-orange-700',
  moderate: 'bg-yellow-100 text-yellow-700',
};
const CATEGORY_ICON: Record<string, string> = {
  construction: '🏗️', charity: '🤲', household: '🏠', spiritual: '🕯️',
  property: '🏘️', remedies: '💊', behavior: '🧠', timing: '⏰', gifts: '🎁',
};

export default function LalKitabForbiddenTab({ kundliId, language }: Props) {
  const [data, setData] = useState<ForbiddenData | null>(null);
  const [loading, setLoading] = useState(false);
  const [loadError, setLoadError] = useState<string | null>(null);
  const hi = language === 'hi';

  useEffect(() => {
    if (!kundliId) return;
    setLoading(true);
    setLoadError(null);
    api.get(`/api/lalkitab/forbidden/${kundliId}`)
      .then(setData)
      .catch((err) => {
        console.error('Failed to load forbidden data:', err);
        const msg = err instanceof Error ? err.message : (typeof err === 'string' ? err : 'Unknown error');
        setLoadError(msg);
      })
      .finally(() => setLoading(false));
  }, [kundliId]);

  if (!kundliId) return (
    <div className="text-center py-10 text-muted-foreground text-sm">
      {hi ? 'विश्लेषण के लिए कुंडली सहेजें।' : 'Save a Kundli to see forbidden actions.'}
    </div>
  );
  if (loading) return <div className="flex justify-center py-16"><Loader2 className="w-8 h-8 animate-spin text-sacred-gold" /></div>;
  if (loadError && !data) return (
    <div className="p-3 mb-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-800">
      {hi ? 'डेटा लोड करने में त्रुटि' : 'Failed to load data'}: {loadError}
    </div>
  );
  if (!data) return null;

  const criticalRules = data.rules.filter(r => r.severity === 'critical');
  const highRules = data.rules.filter(r => r.severity === 'high');
  const moderateRules = data.rules.filter(r => r.severity === 'moderate');

  return (
    <div className="space-y-4">
      {loadError && (
        <div className="p-3 mb-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-800">
          {hi ? 'डेटा लोड करने में त्रुटि' : 'Failed to load data'}: {loadError}
        </div>
      )}
      {/* Header */}
      <div className="text-center">
        <div className="text-3xl mb-1">🚫</div>
        <h3 className="font-bold text-foreground">
          {hi ? 'वर्जित कर्म — इन्हें कभी मत करो' : 'Varjit Karm — Forbidden Actions'}
        </h3>
        <p className="text-sm text-muted-foreground mt-1">
          {hi
            ? 'आपकी कुंडली के अनुसार ये कार्य आपके लिए हानिकारक हैं'
            : 'Based on your chart, these specific actions are contraindicated for you'}
        </p>
      </div>

      {/* Summary bar */}
      <div className={`rounded-xl p-4 text-center ${data.forbidden_count > 0 ? 'bg-red-50 border border-red-200' : 'bg-green-50 border border-green-200'}`}>
        {data.forbidden_count > 0 ? (
          <div className="flex items-center justify-center gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-red-700">{criticalRules.length}</div>
              <div className="text-xs text-red-500">Critical</div>
            </div>
            <div className="w-px h-8 bg-red-200" />
            <div className="text-center">
              <div className="text-2xl font-bold text-orange-600">{highRules.length}</div>
              <div className="text-xs text-orange-500">High</div>
            </div>
            <div className="w-px h-8 bg-red-200" />
            <div className="text-center">
              <div className="text-2xl font-bold text-yellow-600">{moderateRules.length}</div>
              <div className="text-xs text-yellow-500">Moderate</div>
            </div>
          </div>
        ) : (
          <>
            <div className="text-2xl">✅</div>
            <div className="text-sm text-green-700">
              {hi ? 'कोई विशेष वर्जना नहीं मिली।' : 'No specific forbidden actions for your chart.'}
            </div>
          </>
        )}
      </div>

      {/* Critical notice */}
      {criticalRules.length > 0 && (
        <div className="flex items-start gap-2 bg-red-100 border border-red-300 rounded-xl p-3">
          <ShieldAlert className="w-4 h-4 text-red-600 mt-0.5 shrink-0" />
          <p className="text-xs text-red-700 leading-relaxed">
            {hi
              ? `आपकी कुंडली में ${criticalRules.length} अत्यंत गंभीर वर्जनाएं हैं। इन्हें तुरंत जानना जरूरी है।`
              : `Your chart has ${criticalRules.length} critical prohibition(s). These require immediate awareness.`}
          </p>
        </div>
      )}

      {/* Rules list */}
      {data.rules.map((rule, i) => (
        <div key={i} className={`border rounded-xl p-4 ${SEVERITY_STYLE[rule.severity] || 'border-border bg-card'}`}>
          {/* Rule header */}
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <span className={`w-3 h-3 rounded-full ${PLANET_DOT[typeof rule.planet === 'string' ? rule.planet : pickLang(rule.planet, false)] || 'bg-gray-400'}`} />
              <span className="font-bold text-foreground text-sm">{typeof rule.planet === 'string' ? rule.planet : pickLang(rule.planet, false)}</span>
              <span className="text-xs text-muted-foreground px-1.5 py-0.5 bg-white/60 rounded">
                H{rule.house}
              </span>
              <span className="text-sm">{CATEGORY_ICON[rule.category] || '⚠️'}</span>
              <span className="text-xs text-muted-foreground capitalize">{rule.category}</span>
            </div>
            <span className={`text-xs px-2 py-0.5 rounded-full font-semibold ${SEVERITY_BADGE[rule.severity]}`}>
              {rule.severity.toUpperCase()}
            </span>
          </div>

          {/* Forbidden action */}
          <div className="flex items-start gap-2 mb-2">
            <Ban className="w-4 h-4 text-red-500 mt-0.5 shrink-0" />
            <p className="text-sm font-semibold text-foreground">
              {hi ? rule.action.hi : rule.action.en}
            </p>
          </div>

          {/* Reason */}
          <div className="bg-white/60 rounded-lg p-2.5 mb-2">
            <div className="text-xs font-semibold text-muted-foreground mb-0.5">
              {hi ? 'कारण' : 'Why'}
            </div>
            <p className="text-xs text-foreground leading-relaxed">
              {hi ? rule.reason.hi : rule.reason.en}
            </p>
          </div>

          {/* Consequence */}
          <div className="flex items-start gap-1.5 bg-red-100/60 rounded-lg p-2.5">
            <AlertTriangle className="w-3.5 h-3.5 text-red-500 mt-0.5 shrink-0" />
            <div>
              <div className="text-xs font-semibold text-red-600 mb-0.5">
                {hi ? 'अनदेखा करने पर' : 'If ignored'}
              </div>
              <p className="text-xs text-red-700 leading-relaxed">
                {hi ? rule.consequence.hi : rule.consequence.en}
              </p>
            </div>
          </div>
        </div>
      ))}

      {data.forbidden_count === 0 && (
        <p className="text-center text-xs text-muted-foreground pb-4">
          {hi ? 'सामान्य लाल किताब नियम लागू होते हैं।' : 'Standard Lal Kitab general rules apply.'}
        </p>
      )}
    </div>
  );
}
