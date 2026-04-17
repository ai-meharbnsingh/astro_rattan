import { useState, useCallback } from 'react';
import { Loader2, HelpCircle, CheckCircle, XCircle, AlertTriangle } from 'lucide-react';
import { api } from '@/lib/api';
import { translatePlanet, translateSign, translateNakshatra } from '@/lib/backend-translations';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '@/components/ui/table';
import { Heading } from '@/components/ui/heading';
import { Button } from '@/components/ui/button';

/* ------------------------------------------------------------------ */
/*  Types                                                              */
/* ------------------------------------------------------------------ */

interface HoraryChartResult {
  horary_number: number;
  sign?: string;
  star_lord?: string;
  sub_lord?: string;
  degree_range?: string;
  cusps?: Array<{
    house: number;
    sign: string;
    degree?: number;
    degree_dms?: string;
    nakshatra?: string;
    sign_lord?: string;
    star_lord?: string;
    sub_lord?: string;
  }>;
  planets?: Array<{
    planet: string;
    sign: string;
    degree?: number;
    degree_dms?: string;
    nakshatra?: string;
    sign_lord?: string;
    star_lord?: string;
    sub_lord?: string;
    retrograde?: boolean;
  }>;
  house_significations?: Record<string, any>;
  significators?: Record<string, any>;
}

interface HoraryPrediction {
  verdict?: 'favorable' | 'unfavorable' | 'mixed';
  summary?: string;
  summary_hi?: string;
  analysis?: string;
  analysis_hi?: string;
  relevant_houses?: number[];
  significator_analysis?: Array<{
    planet: string;
    houses_signified: number[];
    strength: string;
    role: string;
  }>;
  timing?: string;
  timing_hi?: string;
}

interface KPHoraryProps {
  language: string;
  t: (key: string) => string;
}

/* ------------------------------------------------------------------ */
/*  Constants                                                          */
/* ------------------------------------------------------------------ */

interface QuestionType {
  key: string;
  labelEn: string;
  labelHi: string;
}

const QUESTION_TYPES: QuestionType[] = [
  { key: 'marriage', labelEn: 'Marriage', labelHi: 'विवाह' },
  { key: 'job', labelEn: 'Job / Career', labelHi: 'नौकरी / करियर' },
  { key: 'travel', labelEn: 'Travel', labelHi: 'यात्रा' },
  { key: 'health', labelEn: 'Health', labelHi: 'स्वास्थ्य' },
  { key: 'finance', labelEn: 'Finance', labelHi: 'वित्त' },
  { key: 'legal', labelEn: 'Legal', labelHi: 'कानूनी' },
  { key: 'education', labelEn: 'Education', labelHi: 'शिक्षा' },
  { key: 'property', labelEn: 'Property', labelHi: 'संपत्ति' },
];

/* ------------------------------------------------------------------ */
/*  Component                                                          */
/* ------------------------------------------------------------------ */

export default function KPHorary({ language, t }: KPHoraryProps) {
  const l = (en: string, hi: string) => (language === 'hi' ? hi : en);
  const hi = language === 'hi';

  // Form state
  const [horaryNumber, setHoraryNumber] = useState<string>('');
  const [questionType, setQuestionType] = useState<string>('marriage');
  const [questionText, setQuestionText] = useState<string>('');

  // Result state
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [chartResult, setChartResult] = useState<HoraryChartResult | null>(null);
  const [prediction, setPrediction] = useState<HoraryPrediction | null>(null);

  /* Validation */
  const num = parseInt(horaryNumber, 10);
  const isValid = !isNaN(num) && num >= 1 && num <= 249;

  /* Submit */
  const handleAsk = useCallback(async () => {
    if (!isValid) return;
    setLoading(true);
    setError(null);
    setChartResult(null);
    setPrediction(null);

    try {
      const now = new Date();
      const queryDatetime = now.getFullYear() + '-' +
        String(now.getMonth() + 1).padStart(2, '0') + '-' +
        String(now.getDate()).padStart(2, '0') + ' ' +
        String(now.getHours()).padStart(2, '0') + ':' +
        String(now.getMinutes()).padStart(2, '0') + ':' +
        String(now.getSeconds()).padStart(2, '0');

      const chartPayload = {
        number: num,
        query_datetime: queryDatetime,
      };
      const predictPayload = {
        number: num,
        question_type: questionType,
        query_datetime: queryDatetime,
      };

      // Fetch chart and prediction in parallel
      const [chart, pred] = await Promise.all([
        api.post('/api/kp/horary', chartPayload),
        api.post('/api/kp/horary/predict', predictPayload),
      ]);

      setChartResult(chart);
      setPrediction(pred);
    } catch (err: any) {
      const msg = typeof err?.message === 'string' ? err.message
        : typeof err?.detail === 'string' ? err.detail
        : typeof err?.detail === 'object' ? JSON.stringify(err.detail)
        : 'Failed to get horary analysis';
      setError(msg);
    } finally {
      setLoading(false);
    }
  }, [num, questionType, questionText, isValid]);

  /* Verdict styling */
  const verdictConfig = {
    favorable: {
      icon: <CheckCircle className="w-6 h-6 text-green-600" />,
      bg: 'bg-green-50 border-green-200',
      text: 'text-green-800',
      label: l('Favorable', 'अनुकूल'),
    },
    unfavorable: {
      icon: <XCircle className="w-6 h-6 text-red-600" />,
      bg: 'bg-red-50 border-red-200',
      text: 'text-red-800',
      label: l('Unfavorable', 'प्रतिकूल'),
    },
    mixed: {
      icon: <AlertTriangle className="w-6 h-6 text-amber-600" />,
      bg: 'bg-amber-50 border-amber-200',
      text: 'text-amber-800',
      label: l('Mixed', 'मिश्रित'),
    },
  };

  const planetShort = (name: string) =>
    (translatePlanet(name || '', language) || name || '-').slice(0, 2);

  /* ---------------------------------------------------------------- */
  /*  Render                                                           */
  /* ---------------------------------------------------------------- */

  return (
    <div className="space-y-8">
      {/* --- Input Section --- */}
      <div className="bg-muted rounded-xl border border-border p-6 md:p-8">
        <div className="text-center mb-6">
          <Heading as={3} variant={3} className="mb-2">
            {l('KP Horary Astrology', 'KP प्रश्न ज्योतिष')}
          </Heading>
          <p className="text-sm text-foreground/70">
            {l(
              'Think of your question and pick a number between 1 and 249',
              'अपने प्रश्न के बारे में सोचें और 1 से 249 के बीच एक संख्या चुनें'
            )}
          </p>
        </div>

        {/* Large number input */}
        <div className="flex flex-col items-center mb-6">
          <div className="relative">
            <input
              type="number"
              min={1}
              max={249}
              value={horaryNumber}
              onChange={(e) => {
                const val = e.target.value;
                if (val === '' || (parseInt(val) >= 0 && parseInt(val) <= 249)) {
                  setHoraryNumber(val);
                }
              }}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && isValid) handleAsk();
              }}
              placeholder="1-249"
              className="w-40 h-20 text-center text-4xl font-bold rounded-xl border-2 border-border bg-white text-primary focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all placeholder:text-foreground/20"
            />
            {horaryNumber && !isValid && (
              <p className="absolute -bottom-5 left-0 right-0 text-center text-xs text-red-500">
                {l('Enter 1-249', '1-249 दर्ज करें')}
              </p>
            )}
          </div>
        </div>

        {/* Question type + optional text */}
        <div className="max-w-md mx-auto space-y-4">
          <div>
            <label className="text-sm font-medium text-foreground block mb-1">
              {l('Question Category', 'प्रश्न श्रेणी')}
            </label>
            <select
              value={questionType}
              onChange={(e) => setQuestionType(e.target.value)}
              className="w-full bg-white border border-border rounded-lg px-3 py-2 text-foreground text-sm focus:border-primary focus:outline-none"
            >
              {QUESTION_TYPES.map((qt) => (
                <option key={qt.key} value={qt.key}>
                  {hi ? qt.labelHi : qt.labelEn}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="text-sm font-medium text-foreground block mb-1">
              {l('Your Question (optional)', 'आपका प्रश्न (वैकल्पिक)')}
            </label>
            <input
              type="text"
              value={questionText}
              onChange={(e) => setQuestionText(e.target.value)}
              placeholder={l('e.g., Will I get the job at XYZ?', 'जैसे, क्या मुझे XYZ में नौकरी मिलेगी?')}
              className="w-full bg-white border border-border rounded-lg px-3 py-2 text-foreground text-sm focus:border-primary focus:outline-none placeholder:text-foreground/40"
            />
          </div>

          <Button
            onClick={handleAsk}
            disabled={!isValid || loading}
            className="w-full"
            size="lg"
          >
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin mr-2" />
                {l('Analyzing...', 'विश्लेषण हो रहा है...')}
              </>
            ) : (
              <>
                <HelpCircle className="w-4 h-4 mr-2" />
                {l('Ask', 'पूछें')}
              </>
            )}
          </Button>
        </div>
      </div>

      {/* --- Error --- */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-xl p-4 text-sm text-red-700">
          {error}
        </div>
      )}

      {/* --- Prediction Verdict --- */}
      {prediction?.verdict && (
        <div className={`rounded-xl border p-5 ${verdictConfig[prediction.verdict]?.bg || 'bg-muted border-border'}`}>
          <div className="flex items-start gap-4">
            {verdictConfig[prediction.verdict]?.icon}
            <div className="flex-1">
              <Heading as={4} variant={4} className={verdictConfig[prediction.verdict]?.text || ''}>
                {verdictConfig[prediction.verdict]?.label}
              </Heading>
              <p className="text-sm mt-1">
                {String(hi ? prediction.summary_hi || prediction.summary || '' : prediction.summary || '')}
              </p>
              {prediction.timing && (
                <p className="text-xs mt-2 opacity-80">
                  <strong>{l('Timing', 'समय')}:</strong> {hi ? prediction.timing_hi : prediction.timing}
                </p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* --- Chart Details --- */}
      {chartResult && (
        <div className="bg-muted rounded-xl border border-border p-4">
          <Heading as={4} variant={4} className="mb-3">
            {l('Horary Chart Details', 'प्रश्न कुंडली विवरण')}
            <span className="ml-2 text-sm text-primary font-normal">#{chartResult.horary_number}</span>
          </Heading>

          {/* Quick info cards */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-4">
            {chartResult.sign && (
              <div className="bg-white rounded-lg p-3 text-center border border-border/20">
                <p className="text-[10px] uppercase text-foreground/50 font-bold">{l('Sign', 'राशि')}</p>
                <p className="text-sm font-bold text-primary">{translateSign(chartResult.sign, language)}</p>
              </div>
            )}
            {chartResult.star_lord && (
              <div className="bg-white rounded-lg p-3 text-center border border-border/20">
                <p className="text-[10px] uppercase text-foreground/50 font-bold">{l('Star Lord', 'नक्षत्र स्वामी')}</p>
                <p className="text-sm font-bold text-primary">{translatePlanet(chartResult.star_lord, language)}</p>
              </div>
            )}
            {chartResult.sub_lord && (
              <div className="bg-white rounded-lg p-3 text-center border border-border/20">
                <p className="text-[10px] uppercase text-foreground/50 font-bold">{l('Sub Lord', 'उप स्वामी')}</p>
                <p className="text-sm font-bold text-primary">{translatePlanet(chartResult.sub_lord, language)}</p>
              </div>
            )}
            {chartResult.degree_range && (
              <div className="bg-white rounded-lg p-3 text-center border border-border/20">
                <p className="text-[10px] uppercase text-foreground/50 font-bold">{l('Degree Range', 'अंश सीमा')}</p>
                <p className="text-sm font-bold text-foreground">{chartResult.degree_range}</p>
              </div>
            )}
          </div>

          {/* Planet positions table */}
          {chartResult.planets && chartResult.planets.length > 0 && (
            <div className="mb-4">
              <Heading as={5} variant={5} className="mb-2">
                {l('Planet Positions', 'ग्रह स्थिति')}
              </Heading>
              <div className="overflow-x-auto">
                <Table className="w-full text-sm">
                  <TableHeader>
                    <TableRow className="bg-muted">
                      <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.planet')}</TableHead>
                      <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.sign')}</TableHead>
                      <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.degree')}</TableHead>
                      <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.nakshatra')}</TableHead>
                      <TableHead className="text-center p-1.5 text-primary font-medium" title={t('auto.signLord')}>RL</TableHead>
                      <TableHead className="text-center p-1.5 text-primary font-medium" title={t('auto.starLord')}>NL</TableHead>
                      <TableHead className="text-center p-1.5 text-primary font-medium" title={t('auto.subLord')}>SL</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {chartResult.planets.map((p) => (
                      <TableRow key={p.planet} className="border-t border-border">
                        <TableCell className="p-1.5 font-semibold text-foreground">
                          {translatePlanet(p.planet, language)}
                          {p.retrograde && <span className="ml-1 text-red-400 text-[10px] font-bold">(R)</span>}
                        </TableCell>
                        <TableCell className="p-1.5 text-foreground">{translateSign(p.sign, language)}</TableCell>
                        <TableCell className="p-1.5 text-foreground font-mono">{p.degree_dms || (typeof p.degree === 'number' ? p.degree.toFixed(2) : p.degree || '-')}</TableCell>
                        <TableCell className="p-1.5 text-foreground">{p.nakshatra ? translateNakshatra(p.nakshatra, language) : '-'}</TableCell>
                        <TableCell className="p-1.5 text-center text-primary font-medium">{p.sign_lord ? planetShort(p.sign_lord) : '-'}</TableCell>
                        <TableCell className="p-1.5 text-center text-primary font-medium">{p.star_lord ? planetShort(p.star_lord) : '-'}</TableCell>
                        <TableCell className="p-1.5 text-center text-primary font-medium">{p.sub_lord ? planetShort(p.sub_lord) : '-'}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </div>
          )}

          {/* House cusps table */}
          {chartResult.cusps && chartResult.cusps.length > 0 && (
            <div className="mb-4">
              <Heading as={5} variant={5} className="mb-2">
                {l('House Cusps', 'भाव शीर्ष')}
              </Heading>
              <div className="overflow-x-auto">
                <Table className="w-full text-sm">
                  <TableHeader>
                    <TableRow className="bg-muted">
                      <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.house')}</TableHead>
                      <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.sign')}</TableHead>
                      <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.degree')}</TableHead>
                      <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.nakshatra')}</TableHead>
                      <TableHead className="text-center p-1.5 text-primary font-medium">RL</TableHead>
                      <TableHead className="text-center p-1.5 text-primary font-medium">NL</TableHead>
                      <TableHead className="text-center p-1.5 text-primary font-medium">SL</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {chartResult.cusps.map((c, i) => (
                      <TableRow key={i} className="border-t border-border">
                        <TableCell className="p-1.5 font-semibold text-foreground">{c.house}</TableCell>
                        <TableCell className="p-1.5 text-foreground">{translateSign(c.sign, language)}</TableCell>
                        <TableCell className="p-1.5 text-foreground font-mono">{c.degree_dms || (typeof c.degree === 'number' ? c.degree.toFixed(2) : '-')}</TableCell>
                        <TableCell className="p-1.5 text-foreground">{c.nakshatra ? translateNakshatra(c.nakshatra, language) : '-'}</TableCell>
                        <TableCell className="p-1.5 text-center text-primary font-medium">{c.sign_lord ? planetShort(c.sign_lord) : '-'}</TableCell>
                        <TableCell className="p-1.5 text-center text-primary font-medium">{c.star_lord ? planetShort(c.star_lord) : '-'}</TableCell>
                        <TableCell className="p-1.5 text-center text-primary font-medium">{c.sub_lord ? planetShort(c.sub_lord) : '-'}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </div>
          )}
        </div>
      )}

      {/* --- Significator Analysis --- */}
      {prediction?.significator_analysis && prediction.significator_analysis.length > 0 && (
        <div className="bg-muted rounded-xl border border-border p-4">
          <Heading as={4} variant={4} className="mb-3">
            {l('Significator Analysis', 'कारक विश्लेषण')}
          </Heading>
          <div className="overflow-x-auto">
            <Table className="w-full text-sm">
              <TableHeader>
                <TableRow className="bg-muted">
                  <TableHead className="text-left p-2 text-primary font-medium">{t('table.planet')}</TableHead>
                  <TableHead className="text-left p-2 text-primary font-medium">{l('Houses Signified', 'भाव कारकत्व')}</TableHead>
                  <TableHead className="text-center p-2 text-primary font-medium">{l('Strength', 'बल')}</TableHead>
                  <TableHead className="text-left p-2 text-primary font-medium">{l('Role', 'भूमिका')}</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {prediction.significator_analysis.map((sig) => (
                  <TableRow key={sig.planet} className="border-t border-border">
                    <TableCell className="p-2 font-semibold text-foreground">{translatePlanet(sig.planet, language)}</TableCell>
                    <TableCell className="p-2 text-foreground">{sig.houses_signified?.join(', ') || '-'}</TableCell>
                    <TableCell className="p-2 text-center">
                      <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold uppercase ${
                        sig.strength === 'strong' ? 'bg-green-100 text-green-700 border border-green-200' :
                        sig.strength === 'weak' ? 'bg-red-100 text-red-700 border border-red-200' :
                        'bg-amber-100 text-amber-700 border border-amber-200'
                      }`}>
                        {sig.strength}
                      </span>
                    </TableCell>
                    <TableCell className="p-2 text-foreground text-xs">{sig.role}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </div>
      )}

      {/* --- Detailed Analysis Text --- */}
      {prediction?.analysis && (
        <div className="bg-muted rounded-xl border border-border p-4">
          <Heading as={4} variant={4} className="mb-3">
            {l('Detailed Analysis', 'विस्तृत विश्लेषण')}
          </Heading>
          <div className="text-sm text-foreground leading-relaxed whitespace-pre-line">
            {String(hi ? prediction.analysis_hi || prediction.analysis || '' : prediction.analysis || '')}
          </div>
        </div>
      )}
    </div>
  );
}
