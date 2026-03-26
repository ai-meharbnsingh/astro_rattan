import { useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { BookOpen, Loader2, Sparkles, Grid3X3 } from 'lucide-react';
import { api } from '@/lib/api';

interface OracleResult {
  answer: string;
  answer_devanagari?: string;
  meaning?: string;
  source?: string;
  verse?: string;
  chapter?: number;
}

export default function PrashnavaliPage() {
  const [result, setResult] = useState<OracleResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [question, setQuestion] = useState('');
  const [activeTab, setActiveTab] = useState('ram-shalaka');

  const clearResult = () => {
    setResult(null);
    setQuestion('');
  };

  const handleRamShalaka = async (row: number, col: number) => {
    setLoading(true);
    setResult(null);
    try {
      const data = await api.post('/api/prashnavali/ram-shalaka', { row, col });
      setResult(data);
    } catch {
      setResult({ answer: 'Unable to consult the oracle at this time. Please try again.', meaning: '' });
    }
    setLoading(false);
  };

  const handleOracle = async (endpoint: string) => {
    if (!question.trim()) return;
    setLoading(true);
    setResult(null);
    try {
      const data = await api.post(endpoint, { question: question.trim() });
      setResult(data);
    } catch {
      setResult({ answer: 'Unable to consult the oracle at this time. Please try again.', meaning: '' });
    }
    setLoading(false);
  };

  return (
    <section className="max-w-4xl mx-auto py-24 px-4">
      <div className="text-center mb-10">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-minimal-indigo/10 text-minimal-indigo text-sm font-medium mb-4">
          <BookOpen className="w-4 h-4" />Sacred Oracles
        </div>
        <h2 className="text-3xl sm:text-4xl font-display font-bold text-minimal-gray-900 mb-2">
          <span className="text-gradient-indigo">Prashnavali</span>
        </h2>
        <p className="text-minimal-gray-500">Seek divine guidance from ancient scriptures</p>
      </div>

      <Tabs value={activeTab} onValueChange={(v) => { setActiveTab(v); clearResult(); }}>
        <TabsList className="grid grid-cols-4 bg-minimal-gray-100 mb-8 max-w-lg mx-auto">
          <TabsTrigger value="ram-shalaka" className="data-[state=active]:bg-minimal-indigo data-[state=active]:text-white text-xs sm:text-sm">Ram Shalaka</TabsTrigger>
          <TabsTrigger value="hanuman" className="data-[state=active]:bg-minimal-indigo data-[state=active]:text-white text-xs sm:text-sm">Hanuman</TabsTrigger>
          <TabsTrigger value="gita" className="data-[state=active]:bg-minimal-indigo data-[state=active]:text-white text-xs sm:text-sm">Gita</TabsTrigger>
          <TabsTrigger value="ramcharitmanas" className="data-[state=active]:bg-minimal-indigo data-[state=active]:text-white text-xs sm:text-sm">Ramcharitmanas</TabsTrigger>
        </TabsList>

        {/* Ram Shalaka - clickable grid */}
        <TabsContent value="ram-shalaka">
          <Card className="bg-white border-0 shadow-soft">
            <CardContent className="p-6">
              <div className="text-center mb-4">
                <h3 className="font-display font-semibold text-minimal-gray-900 flex items-center justify-center gap-2">
                  <Grid3X3 className="w-5 h-5 text-minimal-indigo" />Ram Shalaka Prashnavali
                </h3>
                <p className="text-sm text-minimal-gray-500 mt-1">Close your eyes, think of your question, and click any cell in the grid</p>
              </div>
              <div className="grid grid-cols-15 gap-px bg-minimal-gray-200 rounded-lg overflow-hidden max-w-md mx-auto" style={{ gridTemplateColumns: 'repeat(15, 1fr)' }}>
                {Array.from({ length: 15 }, (_, r) =>
                  Array.from({ length: 15 }, (_, c) => (
                    <button
                      key={`${r}-${c}`}
                      onClick={() => handleRamShalaka(r + 1, c + 1)}
                      disabled={loading}
                      className="aspect-square bg-white hover:bg-minimal-indigo/10 transition-colors flex items-center justify-center text-xs font-devanagari text-minimal-gray-400 hover:text-minimal-indigo disabled:opacity-50"
                      aria-label={`Grid cell row ${r + 1}, column ${c + 1}`}
                    >
                      <span className="text-[8px] sm:text-[10px]">{String.fromCharCode(0x0905 + ((r * 15 + c) % 52))}</span>
                    </button>
                  ))
                )}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Hanuman Prashna */}
        <TabsContent value="hanuman">
          <Card className="bg-white border-0 shadow-soft max-w-xl mx-auto">
            <CardContent className="p-6">
              <h3 className="font-display font-semibold text-minimal-gray-900 mb-1 text-center">Hanuman Prashnavali</h3>
              <p className="text-sm text-minimal-gray-500 text-center mb-4">Ask Lord Hanuman for guidance</p>
              <div className="flex gap-2">
                <Input
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleOracle('/api/prashnavali/hanuman')}
                  placeholder="Type your question..."
                  className="flex-1 bg-minimal-gray-50 border-minimal-gray-200"
                />
                <Button onClick={() => handleOracle('/api/prashnavali/hanuman')} disabled={loading || !question.trim()} className="bg-minimal-indigo text-white hover:bg-minimal-violet">
                  {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4" />}
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Gita Prashnavali */}
        <TabsContent value="gita">
          <Card className="bg-white border-0 shadow-soft max-w-xl mx-auto">
            <CardContent className="p-6">
              <h3 className="font-display font-semibold text-minimal-gray-900 mb-1 text-center">Gita Prashnavali</h3>
              <p className="text-sm text-minimal-gray-500 text-center mb-4">Receive wisdom from the Bhagavad Gita</p>
              <div className="flex gap-2">
                <Input
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleOracle('/api/prashnavali/gita')}
                  placeholder="Type your question..."
                  className="flex-1 bg-minimal-gray-50 border-minimal-gray-200"
                />
                <Button onClick={() => handleOracle('/api/prashnavali/gita')} disabled={loading || !question.trim()} className="bg-minimal-indigo text-white hover:bg-minimal-violet">
                  {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4" />}
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Ramcharitmanas */}
        <TabsContent value="ramcharitmanas">
          <Card className="bg-white border-0 shadow-soft max-w-xl mx-auto">
            <CardContent className="p-6">
              <h3 className="font-display font-semibold text-minimal-gray-900 mb-1 text-center">Ramcharitmanas Prashnavali</h3>
              <p className="text-sm text-minimal-gray-500 text-center mb-4">Seek answers from Tulsidas&apos;s Ramcharitmanas</p>
              <div className="flex gap-2">
                <Input
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleOracle('/api/prashnavali/ramcharitmanas')}
                  placeholder="Type your question..."
                  className="flex-1 bg-minimal-gray-50 border-minimal-gray-200"
                />
                <Button onClick={() => handleOracle('/api/prashnavali/ramcharitmanas')} disabled={loading || !question.trim()} className="bg-minimal-indigo text-white hover:bg-minimal-violet">
                  {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4" />}
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Result display */}
      {loading && (
        <div className="flex items-center justify-center py-10">
          <Loader2 className="w-8 h-8 text-minimal-indigo animate-spin" />
        </div>
      )}

      {result && !loading && (
        <Card className="mt-8 bg-white border-0 shadow-soft-lg max-w-xl mx-auto">
          <CardContent className="p-6 text-center">
            <Sparkles className="w-8 h-8 text-minimal-indigo mx-auto mb-3" />
            {result.answer_devanagari && (
              <p className="text-2xl font-devanagari text-minimal-gray-900 mb-3 leading-relaxed">{result.answer_devanagari}</p>
            )}
            <p className="text-lg text-minimal-gray-800 font-medium mb-2">{result.answer}</p>
            {result.meaning && (
              <p className="text-sm text-minimal-gray-500 mt-2">{result.meaning}</p>
            )}
            {(result.source || result.verse) && (
              <div className="mt-4 flex justify-center gap-2">
                {result.source && <Badge variant="outline">{result.source}</Badge>}
                {result.verse && <Badge variant="outline">Verse {result.verse}</Badge>}
                {result.chapter && <Badge variant="outline">Ch. {result.chapter}</Badge>}
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </section>
  );
}
