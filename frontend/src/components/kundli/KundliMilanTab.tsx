import { useState } from 'react';
import { Heart, AlertTriangle, CheckCircle, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { api } from '@/lib/api';

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
  const [kundliId1, setKundliId1] = useState(currentKundliId || '');
  const [kundliId2, setKundliId2] = useState('');
  const [result, setResult] = useState<MatchResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleMatch = async () => {
    if (!kundliId1 || !kundliId2) { setError('Please select both kundlis'); return; }
    if (kundliId1 === kundliId2) { setError('Please select two different kundlis'); return; }
    setLoading(true); setError(''); setResult(null);
    try {
      const data = await api.post('/api/kundli/match', { kundli_id_1: kundliId1, kundli_id_2: kundliId2 });
      console.log('Match result:', data);
      if (!data || typeof data.total_score !== 'number') {
        throw new Error('Invalid response from server');
      }
      setResult(data);
    } catch (e) { 
      const msg = e instanceof Error ? e.message : 'Match calculation failed';
      setError(msg); 
      console.error('Match error:', e); 
    }
    setLoading(false);
  };

  const scoreColor = (score: number, max: number) => {
    const pct = score / max;
    if (pct >= 0.8) return 'text-green-400';
    if (pct >= 0.5) return 'text-yellow-400';
    return 'text-red-400';
  };

  const overallColor = (total: number) => {
    if (total >= 24) return 'text-green-400 border-green-300';
    if (total >= 18) return 'text-yellow-400 border-yellow-500';
    return 'text-red-400 border-red-300';
  };

  return (
    <div className="space-y-6">
      <div className="text-center mb-4">
        <Heart className="w-8 h-8 text-sacred-gold-dark mx-auto mb-2" />
        <h3 className="text-xl font-sans text-cosmic-text">Kundli Milan</h3>
        <p className="text-sm text-cosmic-text">Ashtakoota Gun Milan — 36-point compatibility</p>
      </div>

      {savedKundlis.length < 2 ? (
        <div className="text-center py-8 text-cosmic-text">
          <p>You need at least 2 saved kundlis to perform matching.</p>
          <p className="text-sm mt-2">Generate kundlis for both persons first.</p>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="text-sm text-cosmic-text uppercase tracking-wider mb-1 block">Person 1</label>
              <select value={kundliId1} onChange={e => setKundliId1(e.target.value)}
                className="w-full bg-cosmic-bg border border-sacred-gold text-cosmic-text p-2 text-sm">
                <option value="">Select kundli...</option>
                {savedKundlis.map(k => (
                  <option key={k.id} value={k.id}>{k.person_name} ({k.birth_date})</option>
                ))}
              </select>
            </div>
            <div>
              <label className="text-sm text-cosmic-text uppercase tracking-wider mb-1 block">Person 2</label>
              <select value={kundliId2} onChange={e => setKundliId2(e.target.value)}
                className="w-full bg-cosmic-bg border border-sacred-gold text-cosmic-text p-2 text-sm">
                <option value="">Select kundli...</option>
                {savedKundlis.filter(k => k.id !== kundliId1).map(k => (
                  <option key={k.id} value={k.id}>{k.person_name} ({k.birth_date})</option>
                ))}
              </select>
            </div>
          </div>

          {error && <p className="text-red-400 text-sm text-center">{error}</p>}

          <div className="text-center">
            <Button onClick={handleMatch} disabled={loading || !kundliId1 || !kundliId2}
              className="bg-sacred-gold-dark text-cosmic-bg hover:bg-gray-50 px-8 py-3 font-sans uppercase tracking-wider disabled:opacity-50">
              {loading ? <><Loader2 className="w-4 h-4 animate-spin mr-2" />Calculating...</> : 'Match Kundlis'}
            </Button>
          </div>

          {result && (
            <div className="space-y-6 mt-6">
              <div className={`text-center p-6 border ${overallColor(result.total_score)} bg-cosmic-bg`}>
                <p className="text-5xl font-sans font-bold">{result.total_score}<span className="text-lg text-cosmic-text">/36</span></p>
                <p className="text-sm mt-1">{result.compatibility_percentage}% Compatibility</p>
                <p className="text-lg font-sans mt-2">{result.recommendation}</p>
                <p className="text-sm text-cosmic-text mt-1">{result.person1_name} & {result.person2_name}</p>
              </div>

              {/* Koot Scores Table */}
              <div className="bg-sacred-cream rounded-xl border border-sacred-gold overflow-hidden">
                <div className="bg-sacred-gold px-4 py-2">
                  <h4 className="font-semibold text-sacred-brown">Ashtakoota Scores (8 Koots)</h4>
                </div>
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="bg-sacred-gold/50">
                        <th className="text-left p-3 font-medium text-sacred-gold-dark">Koot</th>
                        <th className="text-center p-3 font-medium text-sacred-gold-dark">Score</th>
                        <th className="text-center p-3 font-medium text-sacred-gold-dark">Max</th>
                        <th className="text-left p-3 font-medium text-sacred-gold-dark">Description</th>
                      </tr>
                    </thead>
                    <tbody>
                      {Object.entries(result.koot_scores || {}).map(([name, koot]) => (
                        <tr key={name} className="border-t border-sacred-gold/30 hover:bg-sacred-gold/10">
                          <td className="p-3 font-medium text-sacred-brown">{name}</td>
                          <td className="p-3 text-center">
                            <span className={`inline-block w-8 h-8 leading-8 rounded-full font-bold ${
                              koot.score >= koot.max ? 'bg-green-500 text-white' : 
                              koot.score >= koot.max * 0.5 ? 'bg-yellow-500 text-white' : 
                              'bg-red-500 text-white'
                            }`}>
                              {koot.score}
                            </span>
                          </td>
                          <td className="p-3 text-center text-cosmic-text">{koot.max}</td>
                          <td className="p-3 text-sm text-cosmic-text">{koot.description}</td>
                        </tr>
                      ))}
                    </tbody>
                    <tfoot>
                      <tr className="bg-sacred-gold/30 border-t-2 border-sacred-gold">
                        <td className="p-3 font-bold text-sacred-brown">Total</td>
                        <td className="p-3 text-center">
                          <span className={`inline-block px-3 py-1 rounded-full font-bold text-lg ${
                            result.total_score >= 24 ? 'bg-green-600 text-white' : 
                            result.total_score >= 18 ? 'bg-yellow-500 text-white' : 
                            'bg-red-500 text-white'
                          }`}>
                            {result.total_score}
                          </span>
                        </td>
                        <td className="p-3 text-center font-bold text-sacred-brown">36</td>
                        <td className="p-3 text-sm font-medium text-sacred-brown">
                          {result.compatibility_percentage}% - {result.recommendation}
                        </td>
                      </tr>
                    </tfoot>
                  </table>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {[
                  { label: result.person1_name, details: result.person1_details },
                  { label: result.person2_name, details: result.person2_details },
                ].map(({ label, details }) => (
                  <div key={label} className="border border-sacred-gold p-4">
                    <h4 className="text-sm font-sans text-sacred-gold-dark mb-3 uppercase">{label}</h4>
                    <div className="space-y-1">
                      {Object.entries(details).map(([k, v]) => (
                        <div key={k} className="flex justify-between text-sm">
                          <span className="text-cosmic-text capitalize">{k}</span>
                          <span className="text-cosmic-text">{v}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>

              {result.doshas.length > 0 && (
                <div className="border border-sacred-gold p-4">
                  <h4 className="text-sm font-sans text-sacred-gold-dark mb-3 uppercase">Dosha Analysis</h4>
                  <div className="space-y-3">
                    {result.doshas.map((dosha, i) => (
                      <div key={i} className="flex items-start gap-3">
                        {dosha.present ? (
                          <AlertTriangle className={`w-4 h-4 mt-0.5 shrink-0 ${dosha.severity === 'High' ? 'text-red-400' : 'text-yellow-400'}`} />
                        ) : (
                          <CheckCircle className="w-4 h-4 mt-0.5 text-green-400 shrink-0" />
                        )}
                        <div>
                          <p className="text-sm text-cosmic-text">{dosha.name}</p>
                          <p className="text-sm text-cosmic-text">{dosha.description}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </>
      )}
    </div>
  );
}
