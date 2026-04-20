import { useState } from 'react';
import { Heart, AlertTriangle, CheckCircle, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { api } from '@/lib/api';
import { useTranslation } from '@/lib/i18n';
import { Heading } from '@/components/ui/heading';

interface KundliOption {
  id: string;
  person_name: string;
  birth_date: string;
}

interface KootScore {
  koot: string;
  max: number;
  score: number;
  description: string;
}

interface MatchResult {
  total_score: number;
  compatibility_percentage: number;
  recommendation: string;
  koot_scores: Record<string, KootScore>;
  doshas: Array<{ name: string; present: boolean; severity: string; description: string }>;
  person1_name: string;
  person2_name: string;
  person1_details: Record<string, string>;
  person2_details: Record<string, string>;
}

interface Props {
  savedKundlis: KundliOption[];
  currentKundliId?: string;
}

const ohContainer = 'rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden';
const ohHeader    = 'bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2';
const thCls       = 'p-1.5 text-left text-[10px] font-semibold uppercase tracking-wide text-primary border-b border-border';
const tdCls       = 'p-1.5 text-xs text-foreground border-t border-border align-top break-words overflow-hidden';

export default function KundliMilanTab({ savedKundlis, currentKundliId }: Props) {
  const { language, t } = useTranslation();
  const isHi = language === 'hi';
  const [kundliId1, setKundliId1] = useState(currentKundliId || '');
  const [kundliId2, setKundliId2] = useState('');
  const [result, setResult] = useState<MatchResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleMatch = async () => {
    if (!kundliId1 || !kundliId2) { setError(t('milan.selectBoth')); return; }
    if (kundliId1 === kundliId2) { setError(t('milan.selectDifferent')); return; }
    setLoading(true); setError(''); setResult(null);
    try {
      const data = await api.post('/api/kundli/match', { kundli_id_1: kundliId1, kundli_id_2: kundliId2 });
      if (!data || typeof data.total_score !== 'number') throw new Error(t('common.error'));
      setResult(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : t('common.error'));
    }
    setLoading(false);
  };

  const scoreBadge = (score: number, max: number) =>
    score >= max ? 'bg-green-500 text-white' : score >= max * 0.5 ? 'bg-yellow-500 text-white' : 'bg-red-500 text-white';

  const totalBadge = (total: number) =>
    total >= 24 ? 'bg-green-600 text-white' : total >= 18 ? 'bg-yellow-500 text-white' : 'bg-red-500 text-white';

  const getMilanRemedies = (isPerson1: boolean) => {
    if (!result) return [];
    const doshas = result.doshas || [];
    const hasNadi = doshas.some((d) => d.name === 'Nadi Dosha' && d.present && !(d as any).cancelled);
    const hasBhakoot = doshas.some((d) => d.name === 'Bhakoot Dosha' && d.present && !(d as any).cancelled);
    const hasGana = doshas.some((d) => d.name === 'Gana Dosha' && d.present);
    const remedies: string[] = [];
    if (hasNadi) remedies.push(t('auto.performMahamrityunja'));
    if (hasBhakoot) remedies.push(t('auto.worshipShivaParvatiT'));
    if (hasGana) remedies.push(t('auto.reciteNarayanaKavach'));
    if (remedies.length === 0) {
      remedies.push(isPerson1 ? t('auto.offerWhiteSweetsOnFr') : t('auto.reciteHanumanChalisa'));
    }
    return remedies;
  };

  return (
    <div className="space-y-4">
      {/* Page heading */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
          <Heart className="w-6 h-6" />
          {t('milan.title')}
        </Heading>
        <p className="text-sm text-muted-foreground">{t('milan.subtitle')}</p>
      </div>

      {savedKundlis.length < 2 ? (
        <div className="text-center py-8 text-foreground">
          <p>{t('milan.minRequired')}</p>
          <p className="text-sm mt-2">{t('milan.generatePrompt')}</p>
        </div>
      ) : (
        <>
          {/* Person selectors */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-1 block">{t('milan.person1')}</label>
              <select value={kundliId1} onChange={e => setKundliId1(e.target.value)}
                className="w-full bg-muted border border-border text-foreground p-2 text-sm rounded">
                <option value="">{t('milan.selectKundli')}</option>
                {savedKundlis.map(k => (
                  <option key={k.id} value={k.id}>{k.person_name} ({k.birth_date})</option>
                ))}
              </select>
            </div>
            <div>
              <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-1 block">{t('milan.person2')}</label>
              <select value={kundliId2} onChange={e => setKundliId2(e.target.value)}
                className="w-full bg-muted border border-border text-foreground p-2 text-sm rounded">
                <option value="">{t('milan.selectKundli')}</option>
                {savedKundlis.filter(k => k.id !== kundliId1).map(k => (
                  <option key={k.id} value={k.id}>{k.person_name} ({k.birth_date})</option>
                ))}
              </select>
            </div>
          </div>

          {error && <p className="text-red-500 text-sm text-center">{error}</p>}

          <div className="text-center">
            <Button onClick={handleMatch} disabled={loading || !kundliId1 || !kundliId2}
              className="bg-primary text-background hover:bg-gray-50 px-8 py-3 font-sans uppercase tracking-wider disabled:opacity-50">
              {loading ? <><Loader2 className="w-4 h-4 animate-spin mr-2" />{t('milan.calculating')}</> : t('milan.matchButton')}
            </Button>
          </div>

          {result && (
            <div className="space-y-4">
              {/* Score banner */}
              <div className={`${ohContainer}`}>
                <div className={ohHeader}>
                  <Heart className="w-4 h-4" />
                  <span>{result.person1_name} & {result.person2_name}</span>
                  <span className={`ml-auto text-sm font-bold px-3 py-0.5 rounded ${totalBadge(result.total_score)}`}>
                    {result.total_score}/36
                  </span>
                </div>
                <div className="px-4 py-3 text-center">
                  <p className="text-4xl font-bold text-sacred-gold-dark">{result.total_score}<span className="text-base text-muted-foreground">/36</span></p>
                  <p className="text-sm mt-1 text-muted-foreground">{result.compatibility_percentage}% {t('milan.compatibility')}</p>
                  <p className="text-base font-semibold mt-1 text-foreground">{result.recommendation}</p>
                </div>
              </div>

              {/* Koot Scores Table */}
              <div className={ohContainer}>
                <div className={ohHeader}>
                  <span>{t('milan.koot')} {t('milan.score')}</span>
                </div>
                <table style={{ tableLayout: 'fixed', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
                  <colgroup>
                    <col style={{ width: '28%' }} />
                    <col style={{ width: '14%' }} />
                    <col style={{ width: '14%' }} />
                    <col style={{ width: '44%' }} />
                  </colgroup>
                  <thead>
                    <tr>
                      <th className={thCls}>{t('milan.koot')}</th>
                      <th className={`${thCls} text-center`}>{t('milan.score')}</th>
                      <th className={`${thCls} text-center`}>{t('milan.max')}</th>
                      <th className={thCls}>{t('numerology.description')}</th>
                    </tr>
                  </thead>
                  <tbody>
                    {Object.entries(result.koot_scores || {}).map(([name, koot]) => (
                      <tr key={name}>
                        <td className={`${tdCls} font-medium`}>{name}</td>
                        <td className={`${tdCls} text-center`}>
                          <span className={`inline-flex items-center justify-center w-7 h-7 rounded-full text-xs font-bold ${scoreBadge(koot.score, koot.max)}`}>
                            {koot.score}
                          </span>
                        </td>
                        <td className={`${tdCls} text-center`}>{koot.max}</td>
                        <td className={tdCls}>{koot.description}</td>
                      </tr>
                    ))}
                    {/* Total row */}
                    <tr className="bg-muted/30">
                      <td className="p-1.5 text-xs font-bold text-foreground border-t-2 border-border">{t('table.total')}</td>
                      <td className="p-1.5 text-xs border-t-2 border-border text-center">
                        <span className={`inline-flex items-center justify-center px-2 py-0.5 rounded-full text-xs font-bold ${totalBadge(result.total_score)}`}>
                          {result.total_score}
                        </span>
                      </td>
                      <td className="p-1.5 text-xs font-bold text-foreground border-t-2 border-border text-center">36</td>
                      <td className="p-1.5 text-xs font-medium text-foreground border-t-2 border-border">
                        {result.compatibility_percentage}% — {result.recommendation}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              {/* Person details */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {[
                  { label: result.person1_name, details: result.person1_details },
                  { label: result.person2_name, details: result.person2_details },
                ].map(({ label, details }) => (
                  <div key={label} className={ohContainer}>
                    <div className={ohHeader}>
                      <span>{label}</span>
                    </div>
                    <div className="p-3 space-y-1">
                      {Object.entries(details).map(([k, v]) => (
                        <div key={k} className="flex justify-between text-xs">
                          <span className="text-muted-foreground capitalize">{k}</span>
                          <span className="text-foreground font-medium">{v}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>

              {/* Dosha Analysis */}
              {result.doshas.length > 0 && (
                <div className={ohContainer}>
                  <div className={ohHeader}>
                    <AlertTriangle className="w-4 h-4" />
                    <span>{t('milan.doshaAnalysis')}</span>
                  </div>
                  <div className="p-3 space-y-3">
                    {result.doshas.map((dosha, i) => (
                      <div key={i} className="flex items-start gap-3">
                        {dosha.present ? (
                          <AlertTriangle className={`w-4 h-4 mt-0.5 shrink-0 ${dosha.severity === 'High' ? 'text-red-500' : 'text-yellow-500'}`} />
                        ) : (
                          <CheckCircle className="w-4 h-4 mt-0.5 text-green-500 shrink-0" />
                        )}
                        <div>
                          <p className="text-sm font-medium text-foreground">{dosha.name}</p>
                          <p className="text-xs text-muted-foreground">{dosha.description}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Remedies */}
              <div className={ohContainer}>
                <div className={ohHeader}>
                  <span>{t('auto.remediesForBoyGirl')}</span>
                </div>
                <div className="p-3 grid grid-cols-1 sm:grid-cols-2 gap-4">
                  {[
                    { name: result.person1_name, remedies: getMilanRemedies(true), key: 'p1' },
                    { name: result.person2_name, remedies: getMilanRemedies(false), key: 'p2' },
                  ].map(({ name, remedies, key }) => (
                    <div key={key} className="bg-muted/30 border border-border/40 rounded-lg p-3">
                      <p className="text-xs font-semibold text-foreground mb-2">{isHi ? `${name} के लिए` : `For ${name}`}</p>
                      <ul className="space-y-1.5 text-xs text-foreground">
                        {remedies.slice(0, 2).map((item, idx) => (
                          <li key={`${key}-${idx}`}>{idx + 1}. {item}</li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}
