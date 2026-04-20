import { useState, useCallback } from 'react';
import { Loader2, HelpCircle, CheckCircle, XCircle, AlertTriangle } from 'lucide-react';
import { api } from '@/lib/api';
import { translatePlanet, translateSign, translateNakshatra } from '@/lib/backend-translations';
import { Button } from '@/components/ui/button';
import { Heading } from '@/components/ui/heading';

interface HoraryChartResult {
  horary_number: number;
  sign?: string;
  star_lord?: string;
  sub_lord?: string;
  degree_range?: string;
  cusps?: Array<{
    house: number; sign: string; degree?: number; degree_dms?: string;
    nakshatra?: string; sign_lord?: string; star_lord?: string; sub_lord?: string;
  }>;
  planets?: Array<{
    planet: string; sign: string; degree?: number; degree_dms?: string;
    nakshatra?: string; sign_lord?: string; star_lord?: string; sub_lord?: string; retrograde?: boolean;
  }>;
  house_significations?: Record<string, any>;
  significators?: Record<string, any>;
}

interface HoraryPrediction {
  verdict?: 'favorable' | 'unfavorable' | 'mixed';
  summary?: string; summary_hi?: string;
  analysis?: string; analysis_hi?: string;
  relevant_houses?: number[];
  significator_analysis?: Array<{
    planet: string; houses_signified: number[]; strength: string; role: string;
  }>;
  timing?: string; timing_hi?: string;
}

interface KPHoraryProps {
  language: string;
  t: (key: string) => string;
}

const QUESTION_TYPES = [
  { key: 'marriage',  labelEn: 'Marriage',     labelHi: 'विवाह' },
  { key: 'job',       labelEn: 'Job / Career',  labelHi: 'नौकरी / करियर' },
  { key: 'travel',    labelEn: 'Travel',        labelHi: 'यात्रा' },
  { key: 'health',    labelEn: 'Health',        labelHi: 'स्वास्थ्य' },
  { key: 'finance',   labelEn: 'Finance',       labelHi: 'वित्त' },
  { key: 'legal',     labelEn: 'Legal',         labelHi: 'कानूनी' },
  { key: 'education', labelEn: 'Education',     labelHi: 'शिक्षा' },
  { key: 'property',  labelEn: 'Property',      labelHi: 'संपत्ति' },
];

const thL = 'p-1.5 text-left   text-[10px] font-semibold uppercase tracking-wide text-primary border-b border-border';
const thC = 'p-1.5 text-center text-[10px] font-semibold uppercase tracking-wide text-primary border-b border-border';
const tdL = 'p-1.5 text-xs text-foreground border-t border-border';
const tdC = 'p-1.5 text-xs text-foreground border-t border-border text-center';
const tdP = 'p-1.5 text-xs text-primary font-medium border-t border-border text-center';

const safeStr = (v: unknown): string => {
  if (v == null) return '-';
  if (typeof v === 'string') return v;
  if (typeof v === 'number') return v.toFixed(2);
  if (typeof v === 'object') {
    const o = v as Record<string, unknown>;
    if ('start_dms' in o && 'end_dms' in o) return `${o.start_dms} - ${o.end_dms}`;
    if ('start' in o && 'end' in o) return `${o.start} - ${o.end}`;
    return JSON.stringify(v);
  }
  return String(v);
};

export default function KPHorary({ language, t }: KPHoraryProps) {
  const hi = language === 'hi';
  const l  = (en: string, hn: string) => (hi ? hn : en);

  const header = (
    <div>
      <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
        <HelpCircle className="w-6 h-6" />
        {hi ? 'केपी प्रश्न' : 'KP Horary'}
      </Heading>
      <p className="text-sm text-muted-foreground">
        {hi
          ? '1–249 संख्या के आधार पर प्रश्न का उत्तर (KP होररी पद्धति)'
          : 'Answer a specific question using the KP horary (1–249) method.'}
      </p>
    </div>
  );

  const [horaryNumber, setHoraryNumber] = useState('');
  const [questionType, setQuestionType] = useState('marriage');
  const [questionText, setQuestionText] = useState('');
  const [loading, setLoading]           = useState(false);
  const [error, setError]               = useState<string | null>(null);
  const [chartResult, setChartResult]   = useState<HoraryChartResult | null>(null);
  const [prediction, setPrediction]     = useState<HoraryPrediction | null>(null);

  const num     = parseInt(horaryNumber, 10);
  const isValid = !isNaN(num) && num >= 1 && num <= 249;

  const handleAsk = useCallback(async () => {
    if (!isValid) return;
    setLoading(true); setError(null); setChartResult(null); setPrediction(null);
    try {
      const now = new Date();
      const queryDatetime = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')} ${String(now.getHours()).padStart(2,'0')}:${String(now.getMinutes()).padStart(2,'0')}:${String(now.getSeconds()).padStart(2,'0')}`;
      const [chart, pred] = await Promise.all([
        api.post('/api/kp/horary', { number: num, query_datetime: queryDatetime }),
        api.post('/api/kp/horary/predict', { number: num, question_type: questionType, query_datetime: queryDatetime }),
      ]);
      setChartResult(chart); setPrediction(pred);
    } catch (err: any) {
      setError(typeof err?.message === 'string' ? err.message : typeof err?.detail === 'string' ? err.detail : 'Failed to get horary analysis');
    } finally {
      setLoading(false);
    }
  }, [num, questionType, isValid]);

  const planetShort = (name: string) => (translatePlanet(name || '', language) || name || '-').slice(0, 2);

  const verdictConfig = {
    favorable:   { icon: <CheckCircle  className="w-5 h-5 text-emerald-600" />, badgeCls: 'bg-emerald-100 text-emerald-800', label: l('Favorable',   'अनुकूल') },
    unfavorable: { icon: <XCircle      className="w-5 h-5 text-red-600"     />, badgeCls: 'bg-red-100 text-red-800',         label: l('Unfavorable', 'प्रतिकूल') },
    mixed:       { icon: <AlertTriangle className="w-5 h-5 text-amber-600"  />, badgeCls: 'bg-amber-100 text-amber-800',     label: l('Mixed',       'मिश्रित') },
  };

  return (
    <div className="space-y-6">
      {header}

      {/* Input */}
      <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
        <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold text-center">
          {l('KP Horary Astrology', 'KP प्रश्न ज्योतिष')}
        </div>
        <div className="p-6">
          <p className="text-sm text-muted-foreground text-center mb-6">
            {l('Think of your question and pick a number between 1 and 249', 'अपने प्रश्न के बारे में सोचें और 1 से 249 के बीच एक संख्या चुनें')}
          </p>
          <div className="flex flex-col items-center mb-6">
            <div className="relative">
              <input
                type="number" min={1} max={249} value={horaryNumber}
                onChange={(e) => { const v = e.target.value; if (v === '' || (parseInt(v) >= 0 && parseInt(v) <= 249)) setHoraryNumber(v); }}
                onKeyDown={(e) => { if (e.key === 'Enter' && isValid) handleAsk(); }}
                placeholder="1-249"
                className="w-40 h-20 text-center text-4xl font-bold rounded-xl border-2 border-border bg-background text-primary focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all placeholder:text-muted-foreground"
              />
              {horaryNumber && !isValid && (
                <p className="absolute -bottom-5 left-0 right-0 text-center text-xs text-red-500">{l('Enter 1-249', '1-249 दर्ज करें')}</p>
              )}
            </div>
          </div>
          <div className="max-w-md mx-auto space-y-4">
            <div>
              <label className="text-sm font-medium text-foreground block mb-1">{l('Question Category', 'प्रश्न श्रेणी')}</label>
              <select value={questionType} onChange={(e) => setQuestionType(e.target.value)} className="input-sacred">
                {QUESTION_TYPES.map((qt) => <option key={qt.key} value={qt.key}>{hi ? qt.labelHi : qt.labelEn}</option>)}
              </select>
            </div>
            <div>
              <label className="text-sm font-medium text-foreground block mb-1">{l('Your Question (optional)', 'आपका प्रश्न (वैकल्पिक)')}</label>
              <input
                type="text" value={questionText} onChange={(e) => setQuestionText(e.target.value)}
                placeholder={l('e.g., Will I get the job at XYZ?', 'जैसे, क्या मुझे XYZ में नौकरी मिलेगी?')}
                className="w-full bg-background border border-border rounded-lg px-3 py-2 text-foreground text-sm focus:border-primary focus:outline-none placeholder:text-muted-foreground"
              />
            </div>
            <Button onClick={handleAsk} disabled={!isValid || loading} className="w-full" size="lg">
              {loading ? <><Loader2 className="w-4 h-4 animate-spin mr-2" />{l('Analyzing...', 'विश्लेषण हो रहा है...')}</> : <><HelpCircle className="w-4 h-4 mr-2" />{l('Ask', 'पूछें')}</>}
            </Button>
          </div>
        </div>
      </div>

      {/* Error */}
      {error && <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">{error}</div>}

      {/* Verdict */}
      {prediction?.verdict && (() => {
        const vc = verdictConfig[prediction.verdict] ?? verdictConfig.mixed;
        return (
          <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
            <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2">
              {vc.icon}
              <span>{l('Prediction', 'भविष्यवाणी')}</span>
              <span className={`ml-2 text-sm px-2 py-0.5 rounded-full font-semibold ${vc.badgeCls}`}>{vc.label}</span>
            </div>
            <div className="p-4 space-y-2 text-sm text-foreground leading-relaxed">
              <p>{String(hi ? prediction.summary_hi || prediction.summary || '' : prediction.summary || '')}</p>
              {prediction.timing && (
                <p className="text-xs text-muted-foreground"><strong>{l('Timing', 'समय')}:</strong> {hi ? prediction.timing_hi : prediction.timing}</p>
              )}
            </div>
          </div>
        );
      })()}

      {/* Chart Details */}
      {chartResult && (
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2">
            <span>{l('Horary Chart Details', 'प्रश्न कुंडली विवरण')}</span>
            <span className="text-sm font-normal opacity-80">#{chartResult.horary_number}</span>
          </div>
          <div className="p-4 space-y-4">
            {/* Quick info cards */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {chartResult.sign && (
                <div className="rounded-lg border border-border p-3 text-center">
                  <p className="text-[10px] uppercase text-muted-foreground font-semibold">{l('Sign', 'राशि')}</p>
                  <p className="text-sm font-bold text-primary mt-0.5">{translateSign(chartResult.sign, language)}</p>
                </div>
              )}
              {chartResult.star_lord && (
                <div className="rounded-lg border border-border p-3 text-center">
                  <p className="text-[10px] uppercase text-muted-foreground font-semibold">{l('Star Lord', 'नक्षत्र स्वामी')}</p>
                  <p className="text-sm font-bold text-primary mt-0.5">{translatePlanet(chartResult.star_lord, language)}</p>
                </div>
              )}
              {chartResult.sub_lord && (
                <div className="rounded-lg border border-border p-3 text-center">
                  <p className="text-[10px] uppercase text-muted-foreground font-semibold">{l('Sub Lord', 'उप स्वामी')}</p>
                  <p className="text-sm font-bold text-primary mt-0.5">{translatePlanet(chartResult.sub_lord, language)}</p>
                </div>
              )}
              {chartResult.degree_range && (
                <div className="rounded-lg border border-border p-3 text-center">
                  <p className="text-[10px] uppercase text-muted-foreground font-semibold">{l('Degree Range', 'अंश सीमा')}</p>
                  <p className="text-sm font-bold text-foreground mt-0.5">{safeStr(chartResult.degree_range)}</p>
                </div>
              )}
            </div>

            {/* Planet Positions */}
            {chartResult.planets && chartResult.planets.length > 0 && (
              <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
                <div className="bg-sacred-gold-dark text-white px-3 py-1.5 text-[13px] font-semibold">
                  {l('Planet Positions', 'ग्रह स्थिति')}
                </div>
                <table style={{ tableLayout: 'fixed', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
                  <colgroup>
                    <col style={{ width: '16%' }} /><col style={{ width: '14%' }} />
                    <col style={{ width: '16%' }} /><col style={{ width: '22%' }} />
                    <col style={{ width: '11%' }} /><col style={{ width: '11%' }} />
                    <col style={{ width: '10%' }} />
                  </colgroup>
                  <thead><tr>
                    <th className={thL}>{t('table.planet')}</th>
                    <th className={thL}>{t('table.sign')}</th>
                    <th className={thL}>{t('table.degree')}</th>
                    <th className={thL}>{t('table.nakshatra')}</th>
                    <th className={thC} title={t('auto.signLord')}>RL</th>
                    <th className={thC} title={t('auto.starLord')}>NL</th>
                    <th className={thC} title={t('auto.subLord')}>SL</th>
                  </tr></thead>
                  <tbody>
                    {chartResult.planets.map((p) => (
                      <tr key={p.planet}>
                        <td className={`${tdL} font-semibold`}>
                          {translatePlanet(p.planet, language)}
                          {p.retrograde && <span className="ml-1 text-red-500 text-[10px] font-bold">(R)</span>}
                        </td>
                        <td className={tdL}>{translateSign(p.sign, language)}</td>
                        <td className={`${tdL} font-mono`}>{safeStr(p.degree_dms || p.degree)}</td>
                        <td className={tdL}>{p.nakshatra ? translateNakshatra(p.nakshatra, language) : '-'}</td>
                        <td className={tdP}>{p.sign_lord  ? planetShort(p.sign_lord)  : '-'}</td>
                        <td className={tdP}>{p.star_lord  ? planetShort(p.star_lord)  : '-'}</td>
                        <td className={tdP}>{p.sub_lord   ? planetShort(p.sub_lord)   : '-'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}

            {/* House Cusps */}
            {chartResult.cusps && chartResult.cusps.length > 0 && (
              <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
                <div className="bg-sacred-gold-dark text-white px-3 py-1.5 text-[13px] font-semibold">
                  {l('House Cusps', 'भाव शीर्ष')}
                </div>
                <table style={{ tableLayout: 'fixed', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
                  <colgroup>
                    <col style={{ width: '8%' }} /><col style={{ width: '14%' }} />
                    <col style={{ width: '16%' }} /><col style={{ width: '22%' }} />
                    <col style={{ width: '13%' }} /><col style={{ width: '13%' }} />
                    <col style={{ width: '14%' }} />
                  </colgroup>
                  <thead><tr>
                    <th className={thC}>{t('table.house')}</th>
                    <th className={thL}>{t('table.sign')}</th>
                    <th className={thL}>{t('table.degree')}</th>
                    <th className={thL}>{t('table.nakshatra')}</th>
                    <th className={thC}>RL</th>
                    <th className={thC}>NL</th>
                    <th className={thC}>SL</th>
                  </tr></thead>
                  <tbody>
                    {chartResult.cusps.map((c, i) => (
                      <tr key={i}>
                        <td className={`${tdC} font-semibold`}>{c.house}</td>
                        <td className={tdL}>{translateSign(c.sign, language)}</td>
                        <td className={`${tdL} font-mono`}>{safeStr(c.degree_dms || c.degree)}</td>
                        <td className={tdL}>{c.nakshatra ? translateNakshatra(c.nakshatra, language) : '-'}</td>
                        <td className={tdP}>{c.sign_lord  ? planetShort(c.sign_lord)  : '-'}</td>
                        <td className={tdP}>{c.star_lord  ? planetShort(c.star_lord)  : '-'}</td>
                        <td className={tdP}>{c.sub_lord   ? planetShort(c.sub_lord)   : '-'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Significator Analysis */}
      {prediction?.significator_analysis && prediction.significator_analysis.length > 0 && (
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
            {l('Significator Analysis', 'कारक विश्लेषण')}
          </div>
          <table style={{ tableLayout: 'fixed', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
            <colgroup>
              <col style={{ width: '15%' }} /><col style={{ width: '35%' }} />
              <col style={{ width: '15%' }} /><col style={{ width: '35%' }} />
            </colgroup>
            <thead><tr>
              <th className={thL}>{t('table.planet')}</th>
              <th className={thL}>{l('Houses Signified', 'भाव कारकत्व')}</th>
              <th className={thC}>{l('Strength', 'बल')}</th>
              <th className={thL}>{l('Role', 'भूमिका')}</th>
            </tr></thead>
            <tbody>
              {prediction.significator_analysis.map((sig) => (
                <tr key={sig.planet}>
                  <td className={`${tdL} font-semibold`}>{translatePlanet(sig.planet, language)}</td>
                  <td className={tdL}>{sig.houses_signified?.join(', ') || '-'}</td>
                  <td className={tdC}>
                    <span className={`px-1.5 py-0.5 rounded text-[10px] font-semibold ${
                      sig.strength === 'strong' ? 'bg-emerald-100 text-emerald-800' :
                      sig.strength === 'weak'   ? 'bg-red-100 text-red-800' :
                                                  'bg-amber-100 text-amber-800'
                    }`}>{sig.strength}</span>
                  </td>
                  <td className={`${tdL} break-words overflow-hidden`}>{sig.role}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Detailed Analysis */}
      {prediction?.analysis && (
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
            {l('Detailed Analysis', 'विस्तृत विश्लेषण')}
          </div>
          <div className="p-4 text-sm text-foreground leading-relaxed whitespace-pre-line">
            {String(hi ? prediction.analysis_hi || prediction.analysis || '' : prediction.analysis || '')}
          </div>
        </div>
      )}

    </div>
  );
}
