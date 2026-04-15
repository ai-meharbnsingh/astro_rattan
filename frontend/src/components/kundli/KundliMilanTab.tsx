import { useState } from 'react';
import { Heart, AlertTriangle, CheckCircle, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { api } from '@/lib/api';
import { useTranslation } from '@/lib/i18n';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell, TableCaption, TableFooter } from '@/components/ui/table';
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

export default function KundliMilanTab({ savedKundlis, currentKundliId }: Props) {
  const { language, t } = useTranslation();
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
      if (!data || typeof data.total_score !== 'number') {
        throw new Error(t('common.error'));
      }
      setResult(data);
    } catch (e) { 
      const msg = e instanceof Error ? e.message : t('common.error');
      setError(msg);
    }
    setLoading(false);
  };

  const overallColor = (total: number) => {
    if (total >= 24) return 'text-green-400 border-green-300';
    if (total >= 18) return 'text-yellow-400 border-yellow-500';
    return 'text-red-400 border-red-300';
  };

  const getMilanRemedies = (isPerson1: boolean) => {
    const isHi = language === 'hi';
    if (!result) return [];

    const doshas = result.doshas || [];
    const hasNadiDosha = doshas.some((d) => d.name === 'Nadi Dosha' && d.present && !d.cancelled);
    const hasBhakootDosha = doshas.some((d) => d.name === 'Bhakoot Dosha' && d.present && !d.cancelled);
    const hasGanaDosha = doshas.some((d) => d.name === 'Gana Dosha' && d.present);

    const remedies: string[] = [];

    if (hasNadiDosha) {
      remedies.push(t('auto.performMahamrityunja'));
    }
    if (hasBhakootDosha) {
      remedies.push(t('auto.worshipShivaParvatiT'));
    }
    if (hasGanaDosha) {
      remedies.push(t('auto.reciteNarayanaKavach'));
    }

    // Add general fallback if no specific doshas but low score
    if (remedies.length === 0) {
      if (isPerson1) {
        remedies.push(t('auto.offerWhiteSweetsOnFr'));
      } else {
        remedies.push(t('auto.reciteHanumanChalisa'));
      }
    }

    return remedies;
  };

  return (
    <div className="space-y-6">
      <div className="text-center mb-4">
        <Heart className="w-8 h-8 text-primary mx-auto mb-2" />
        <Heading as={3} variant={3} className="font-sans">{t('milan.title')}</Heading>
        <p className="text-sm text-foreground">{t('milan.subtitle')}</p>
      </div>

      {savedKundlis.length < 2 ? (
        <div className="text-center py-8 text-foreground">
          <p>{t('milan.minRequired')}</p>
          <p className="text-sm mt-2">{t('milan.generatePrompt')}</p>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="text-sm text-foreground uppercase tracking-wider mb-1 block">{t('milan.person1')}</label>
              <select value={kundliId1} onChange={e => setKundliId1(e.target.value)}
                className="w-full bg-muted border border-border text-foreground p-2 text-sm">
                <option value="">{t('milan.selectKundli')}</option>
                {savedKundlis.map(k => (
                  <option key={k.id} value={k.id}>{k.person_name} ({k.birth_date})</option>
                ))}
              </select>
            </div>
            <div>
              <label className="text-sm text-foreground uppercase tracking-wider mb-1 block">{t('milan.person2')}</label>
              <select value={kundliId2} onChange={e => setKundliId2(e.target.value)}
                className="w-full bg-muted border border-border text-foreground p-2 text-sm">
                <option value="">{t('milan.selectKundli')}</option>
                {savedKundlis.filter(k => k.id !== kundliId1).map(k => (
                  <option key={k.id} value={k.id}>{k.person_name} ({k.birth_date})</option>
                ))}
              </select>
            </div>
          </div>

          {error && <p className="text-red-400 text-sm text-center">{error}</p>}

          <div className="text-center">
            <Button onClick={handleMatch} disabled={loading || !kundliId1 || !kundliId2}
              className="bg-primary text-background hover:bg-gray-50 px-8 py-3 font-sans uppercase tracking-wider disabled:opacity-50">
              {loading ? <><Loader2 className="w-4 h-4 animate-spin mr-2" />{t('milan.calculating')}</> : t('milan.matchButton')}
            </Button>
          </div>

          {result && (
            <div className="space-y-6 mt-6">
              <div className={`text-center p-6 border ${overallColor(result.total_score)} bg-muted`}>
                <p className="text-5xl font-sans font-bold">{result.total_score}<span className="text-lg text-foreground">/36</span></p>
                <p className="text-sm mt-1">{result.compatibility_percentage}% {t('milan.compatibility')}</p>
                <p className="text-lg font-sans mt-2">{result.recommendation}</p>
                <p className="text-sm text-foreground mt-1">{result.person1_name} & {result.person2_name}</p>
              </div>

              {/* Koot Scores Table */}
              <div className="bg-muted rounded-xl border border-border overflow-hidden">
                <div className="bg-muted px-4 py-2">
                  <Heading as={4} variant={4}>{t('milan.koot')} {t('milan.score')}</Heading>
                </div>
                <div className="overflow-x-auto">
                  <Table className="w-full text-sm">
                    <TableHeader>
                      <TableRow className="bg-muted/50">
                        <TableHead className="text-left p-3 font-medium text-primary">{t('milan.koot')}</TableHead>
                        <TableHead className="text-center p-3 font-medium text-primary">{t('milan.score')}</TableHead>
                        <TableHead className="text-center p-3 font-medium text-primary">{t('milan.max')}</TableHead>
                        <TableHead className="text-left p-3 font-medium text-primary">{t('numerology.description')}</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {Object.entries(result.koot_scores || {}).map(([name, koot]) => (
                        <TableRow key={name} className="border-t border-border/30 hover:bg-muted/10">
                          <TableCell className="p-3 font-medium text-foreground">{name}</TableCell>
                          <TableCell className="p-3 text-center">
                            <span className={`inline-block w-8 h-8 leading-8 rounded-full font-bold ${
                              koot.score >= koot.max ? 'bg-green-500 text-white' : 
                              koot.score >= koot.max * 0.5 ? 'bg-yellow-500 text-white' : 
                              'bg-red-500 text-white'
                            }`}>
                              {koot.score}
                            </span>
                          </TableCell>
                          <TableCell className="p-3 text-center text-foreground">{koot.max}</TableCell>
                          <TableCell className="p-3 text-sm text-foreground">{koot.description}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                    <TableFooter>
                      <TableRow className="bg-muted/30 border-t-2 border-border">
                        <TableCell className="p-3 font-bold text-foreground">{t('table.total')}</TableCell>
                        <TableCell className="p-3 text-center">
                          <span className={`inline-block px-3 py-1 rounded-full font-bold text-lg ${
                            result.total_score >= 24 ? 'bg-green-600 text-white' : 
                            result.total_score >= 18 ? 'bg-yellow-500 text-white' : 
                            'bg-red-500 text-white'
                          }`}>
                            {result.total_score}
                          </span>
                        </TableCell>
                        <TableCell className="p-3 text-center font-bold text-foreground">36</TableCell>
                        <TableCell className="p-3 text-sm font-medium text-foreground">
                          {result.compatibility_percentage}% - {result.recommendation}
                        </TableCell>
                      </TableRow>
                    </TableFooter>
                  </Table>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {[
                  { label: result.person1_name, details: result.person1_details },
                  { label: result.person2_name, details: result.person2_details },
                ].map(({ label, details }) => (
                  <div key={label} className="border border-border p-4">
                    <Heading as={4} variant={4} className="font-sans text-primary mb-3 uppercase">{label}</Heading>
                    <div className="space-y-1">
                      {Object.entries(details).map(([k, v]) => (
                        <div key={k} className="flex justify-between text-sm">
                          <span className="text-foreground capitalize">{k}</span>
                          <span className="text-foreground">{v}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>

              {result.doshas.length > 0 && (
                <div className="border border-border p-4">
                  <Heading as={4} variant={4} className="font-sans text-primary mb-3 uppercase">{t('milan.doshaAnalysis')}</Heading>
                  <div className="space-y-3">
                    {result.doshas.map((dosha, i) => (
                      <div key={i} className="flex items-start gap-3">
                        {dosha.present ? (
                          <AlertTriangle className={`w-4 h-4 mt-0.5 shrink-0 ${dosha.severity === 'High' ? 'text-red-400' : 'text-yellow-400'}`} />
                        ) : (
                          <CheckCircle className="w-4 h-4 mt-0.5 text-green-400 shrink-0" />
                        )}
                        <div>
                          <p className="text-sm text-foreground">{dosha.name}</p>
                          <p className="text-sm text-foreground">{dosha.description}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <div className="border border-border p-4">
                <Heading as={4} variant={4} className="font-sans text-primary mb-3 uppercase">
                  {t('auto.remediesForBoyGirl')}
                </Heading>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div className="bg-muted border border-border/40 rounded-lg p-3">
                    <p className="text-sm font-semibold text-foreground mb-2">
                      {t('auto.forResultPerson1name')}
                    </p>
                    <ul className="space-y-2 text-sm text-foreground">
                      {getMilanRemedies(true).slice(0, 2).map((item, idx) => (
                        <li key={`p1-${idx}`}>{idx + 1}. {item}</li>
                      ))}
                    </ul>
                  </div>

                  <div className="bg-muted border border-border/40 rounded-lg p-3">
                    <p className="text-sm font-semibold text-foreground mb-2">
                      {t('auto.forResultPerson2name')}
                    </p>
                    <ul className="space-y-2 text-sm text-foreground">
                      {getMilanRemedies(false).slice(0, 2).map((item, idx) => (
                        <li key={`p2-${idx}`}>{idx + 1}. {item}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}
