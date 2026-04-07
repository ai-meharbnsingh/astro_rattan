import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Hash, Sparkles, Hand, Loader2, Eye } from 'lucide-react';
import { api } from '@/lib/api';
import { useTranslation } from '@/lib/i18n';

interface NumerologyResult {
  life_path: number;
  expression: number;
  soul_urge: number;
  personality: number;
  predictions?: string[];
  summary?: string;
}

interface TarotCard {
  name: string;
  position?: string;
  meaning: string;
  is_reversed?: boolean;
  image_url?: string;
}

interface TarotResult {
  cards: TarotCard[];
  interpretation?: string;
  summary?: string;
  spread_type: string;
}

interface PalmistryLine {
  name: string;
  description: string;
}

interface PalmistryGuide {
  lines: PalmistryLine[];
  mounts: PalmistryLine[];
  hand_shapes: PalmistryLine[];
  introduction?: string;
}

const normalizePalmistryGuide = (data: any): PalmistryGuide => ({
  introduction: Object.values(data?.meanings || {}).join(' '),
  lines: Array.isArray(data?.lines)
    ? data.lines.map((line: any) => ({
        name: line.name,
        description: [line.location, line.meaning || Object.values(line.meanings || {}).join(' ')].filter(Boolean).join(' — '),
      }))
    : [],
  mounts: Array.isArray(data?.mounts)
    ? data.mounts.map((mount: any) => ({
        name: mount.name,
        description: [mount.location, mount.meaning].filter(Boolean).join(' — '),
      }))
    : [],
  hand_shapes: Array.isArray(data?.shapes || data?.hand_shapes)
    ? (data.shapes || data.hand_shapes).map((shape: any) => ({
        name: shape.name,
        description: [shape.features, shape.meaning].filter(Boolean).join(' — '),
      }))
    : [],
});

export default function NumerologyTarot() {
  const { t } = useTranslation();
  // Numerology
  const [numName, setNumName] = useState('');
  const [numDob, setNumDob] = useState('');
  const [numResult, setNumResult] = useState<NumerologyResult | null>(null);
  const [numLoading, setNumLoading] = useState(false);

  // Tarot
  const [tarotSpread, setTarotSpread] = useState('single');
  const [tarotQuestion, setTarotQuestion] = useState('');
  const [tarotResult, setTarotResult] = useState<TarotResult | null>(null);
  const [tarotLoading, setTarotLoading] = useState(false);

  // Palmistry
  const [palmGuide, setPalmGuide] = useState<PalmistryGuide | null>(null);
  const [palmLoading, setPalmLoading] = useState(false);

  // Error state for user feedback
  const [error, setError] = useState('');

  const calculateNumerology = async () => {
    if (!numName.trim() || !numDob) return;
    setNumLoading(true);
    setNumResult(null);
    setError('');
    try {
      const data = await api.post('/api/numerology/calculate', { name: numName.trim(), birth_date: numDob });
      // Normalize predictions: API may return string (old) or array (new)
      if (data.predictions && !Array.isArray(data.predictions)) {
        data.predictions = [data.predictions];
      }
      setNumResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Numerology calculation failed. Please try again.');
    }
    setNumLoading(false);
  };

  const drawTarot = async () => {
    setTarotLoading(true);
    setTarotResult(null);
    setError('');
    try {
      const data = await api.post('/api/tarot/draw', { spread: tarotSpread, question: tarotQuestion.trim() || undefined });
      setTarotResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Tarot draw failed. Please try again.');
    }
    setTarotLoading(false);
  };

  const loadPalmistry = async () => {
    if (palmGuide) return;
    setPalmLoading(true);
    setError('');
    try {
      const data = await api.get('/api/palmistry/guide');
      setPalmGuide(normalizePalmistryGuide(data));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load palmistry guide. Please try again.');
    }
    setPalmLoading(false);
  };

  return (
    <section className="max-w-4xl mx-auto py-24 px-4">
      <div className="text-center mb-10">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-sacred-gold/10 text-sacred-gold text-sm font-medium mb-4">
          <Sparkles className="w-4 h-4" />{t('numerology.badge')}
        </div>
        <h2 className="text-3xl sm:text-4xl font-display font-bold text-cosmic-text mb-2">
          {t('numerology.heading')}<span className="text-gradient-indigo"> {t('numerology.headingHighlight')}</span>
        </h2>
        <p className="text-cosmic-text-secondary">{t('numerology.subtitle')}</p>
      </div>

      {error && (
        <div className="mb-6 p-3 rounded-xl bg-red-900/30 border border-red-500/30 text-red-400 text-sm text-center max-w-xl mx-auto">
          {error}
        </div>
      )}

      <Tabs defaultValue="numerology">
        <TabsList className="grid grid-cols-3 bg-cosmic-surface mb-8 max-w-md mx-auto">
          <TabsTrigger value="numerology" className="data-[state=active]:bg-sacred-gold data-[state=active]:text-[#1a1a2e]">
            <Hash className="w-4 h-4 mr-1" />{t('numerology.tabNumerology')}
          </TabsTrigger>
          <TabsTrigger value="tarot" className="data-[state=active]:bg-sacred-gold data-[state=active]:text-[#1a1a2e]">
            <Eye className="w-4 h-4 mr-1" />{t('numerology.tabTarot')}
          </TabsTrigger>
          <TabsTrigger value="palmistry" onClick={loadPalmistry} className="data-[state=active]:bg-sacred-gold data-[state=active]:text-[#1a1a2e]">
            <Hand className="w-4 h-4 mr-1" />{t('numerology.tabPalmistry')}
          </TabsTrigger>
        </TabsList>

        {/* Numerology Tab */}
        <TabsContent value="numerology">
          <Card className="bg-cosmic-card border-0 shadow-soft max-w-xl mx-auto">
            <CardContent className="p-6">
              <h3 className="font-display font-semibold text-cosmic-text mb-4 text-center">{t('numerology.calculateNumbers')}</h3>
              <div className="space-y-3">
                <Input placeholder={t('numerology.fullName')} value={numName} onChange={(e) => setNumName(e.target.value)} className="bg-cosmic-card border-sacred-gold/15" />
                <Input type="date" value={numDob} onChange={(e) => setNumDob(e.target.value)} className="bg-cosmic-card border-sacred-gold/15" />
                <Button onClick={calculateNumerology} disabled={numLoading || !numName.trim() || !numDob} className="w-full bg-sacred-gold text-[#1a1a2e] hover:bg-sacred-gold-dark">
                  {numLoading ? <><Loader2 className="w-4 h-4 mr-2 animate-spin" />{t('common.calculating')}</> : <><Hash className="w-4 h-4 mr-2" />{t('numerology.calculate')}</>}
                </Button>
              </div>
            </CardContent>
          </Card>
          {numResult && (
            <Card className="mt-6 bg-cosmic-card border-0 shadow-soft-lg max-w-xl mx-auto">
              <CardContent className="p-6">
                <h4 className="font-display font-semibold text-cosmic-text mb-4 text-center">{t('numerology.report')}</h4>
                <div className="grid grid-cols-2 gap-4 mb-4">
                  {[
                    { label: t('numerology.lifePath'), value: numResult.life_path, color: 'bg-purple-100 text-purple-700' },
                    { label: t('numerology.expression'), value: numResult.expression, color: 'bg-blue-100 text-blue-700' },
                    { label: t('numerology.soulUrge'), value: numResult.soul_urge, color: 'bg-green-500/20 text-green-400' },
                    { label: t('numerology.personality'), value: numResult.personality, color: 'bg-yellow-100 text-yellow-700' },
                  ].map((n) => (
                    <div key={n.label} className="text-center p-3 rounded-xl bg-cosmic-card">
                      <p className="text-xs text-cosmic-text-secondary mb-1">{n.label}</p>
                      <Badge className={`text-lg px-3 py-1 ${n.color}`}>{n.value}</Badge>
                    </div>
                  ))}
                </div>
                {numResult.summary && <p className="text-sm text-cosmic-text-secondary text-center">{numResult.summary}</p>}
                {numResult.predictions && numResult.predictions.length > 0 && (
                  <div className="mt-4">
                    <p className="text-sm font-medium text-cosmic-text mb-2">{t('numerology.predictions')}:</p>
                    <ul className="space-y-1">
                      {numResult.predictions.map((p, i) => (
                        <li key={i} className="text-sm text-cosmic-text-secondary flex gap-2">
                          <Sparkles className="w-4 h-4 text-sacred-gold shrink-0 mt-0.5" />{p}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </CardContent>
            </Card>
          )}
        </TabsContent>

        {/* Tarot Tab */}
        <TabsContent value="tarot">
          <Card className="bg-cosmic-card border-0 shadow-soft max-w-xl mx-auto">
            <CardContent className="p-6">
              <h3 className="font-display font-semibold text-cosmic-text mb-4 text-center">{t('numerology.drawTarot')}</h3>
              <div className="space-y-3">
                <Select value={tarotSpread} onValueChange={setTarotSpread}>
                  <SelectTrigger className="w-full bg-cosmic-card border-sacred-gold/15">
                    <SelectValue placeholder="Select spread" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="single">Single Card</SelectItem>
                    <SelectItem value="three">Three Card Spread (Past / Present / Future)</SelectItem>
                    <SelectItem value="celtic_cross">Celtic Cross (10 cards)</SelectItem>
                  </SelectContent>
                </Select>
                <Input placeholder="Your question (optional)" value={tarotQuestion} onChange={(e) => setTarotQuestion(e.target.value)} className="bg-cosmic-card border-sacred-gold/15" />
                <Button onClick={drawTarot} disabled={tarotLoading} className="w-full bg-sacred-gold text-[#1a1a2e] hover:bg-sacred-gold-dark">
                  {tarotLoading ? <><Loader2 className="w-4 h-4 mr-2 animate-spin" />Drawing...</> : <><Eye className="w-4 h-4 mr-2" />Draw Cards</>}
                </Button>
              </div>
            </CardContent>
          </Card>
          {tarotResult && (
            <div className="mt-6 space-y-4">
              <div className={`grid gap-4 max-w-3xl mx-auto ${tarotResult.cards.length === 1 ? 'grid-cols-1 max-w-xs' : tarotResult.cards.length <= 3 ? 'grid-cols-3 max-w-xl' : 'grid-cols-2 sm:grid-cols-3 lg:grid-cols-5'}`}>
                {tarotResult.cards.map((card, i) => (
                  <Card key={i} className="bg-cosmic-card border-0 shadow-soft text-center">
                    <CardContent className="p-4">
                      <div className="w-full aspect-[2/3] bg-gradient-to-b from-sacred-gold/10 to-sacred-gold-dark/10 rounded-lg flex items-center justify-center mb-3">
                        <Eye className="w-8 h-8 text-sacred-gold" />
                      </div>
                      {card.position && <p className="text-xs text-cosmic-text-muted mb-1">{card.position}</p>}
                      <p className="font-display font-semibold text-cosmic-text text-sm">{card.name}</p>
                      {card.is_reversed && <Badge className="mt-1 bg-red-500/20 text-red-400 text-xs">Reversed</Badge>}
                      <p className="text-xs text-cosmic-text-secondary mt-2">{card.meaning}</p>
                    </CardContent>
                  </Card>
                ))}
              </div>
              {(tarotResult.interpretation || tarotResult.summary) && (
                <Card className="bg-cosmic-card border-0 shadow-soft max-w-xl mx-auto">
                  <CardContent className="p-4 text-center">
                    <p className="text-sm text-cosmic-text-secondary">{tarotResult.interpretation || tarotResult.summary}</p>
                  </CardContent>
                </Card>
              )}
            </div>
          )}
        </TabsContent>

        {/* Palmistry Tab */}
        <TabsContent value="palmistry">
          {palmLoading ? (
            <div className="flex items-center justify-center py-12">
              <Loader2 className="w-8 h-8 text-sacred-gold animate-spin" />
            </div>
          ) : palmGuide ? (
            <div className="space-y-6 max-w-2xl mx-auto">
              <Card className="bg-gradient-to-br from-sacred-gold/5 to-sacred-gold-dark/5 border-0 shadow-soft">
                <CardContent className="p-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                  <div>
                    <h3 className="font-display font-semibold text-cosmic-text">Need a deeper palm reading?</h3>
                    <p className="text-sm text-cosmic-text-secondary mt-1">Use the dedicated palmistry page for photo-based analysis and guided line selection.</p>
                  </div>
                  <Button asChild className="bg-sacred-gold text-[#1a1a2e] hover:bg-sacred-gold-dark">
                    <Link to="/palmistry">
                      <Hand className="w-4 h-4 mr-2" />Open Palmistry
                    </Link>
                  </Button>
                </CardContent>
              </Card>
              {palmGuide.introduction && (
                <Card className="bg-cosmic-card border-0 shadow-soft">
                  <CardContent className="p-6 text-center">
                    <Hand className="w-8 h-8 text-sacred-gold mx-auto mb-2" />
                    <p className="text-sm text-cosmic-text-secondary">{palmGuide.introduction}</p>
                  </CardContent>
                </Card>
              )}
              {palmGuide.lines && palmGuide.lines.length > 0 && (
                <div>
                  <h3 className="font-display font-semibold text-cosmic-text mb-3">Palm Lines</h3>
                  <div className="grid sm:grid-cols-2 gap-3">
                    {palmGuide.lines.map((line) => (
                      <Card key={line.name} className="bg-cosmic-card border-0 shadow-soft">
                        <CardContent className="p-4">
                          <Badge className="bg-sacred-gold/10 text-sacred-gold mb-2">{line.name}</Badge>
                          <p className="text-sm text-cosmic-text-secondary">{line.description}</p>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                </div>
              )}
              {palmGuide.mounts && palmGuide.mounts.length > 0 && (
                <div>
                  <h3 className="font-display font-semibold text-cosmic-text mb-3">Mounts</h3>
                  <div className="grid sm:grid-cols-2 gap-3">
                    {palmGuide.mounts.map((mount) => (
                      <Card key={mount.name} className="bg-cosmic-card border-0 shadow-soft">
                        <CardContent className="p-4">
                          <Badge className="bg-purple-100 text-purple-700 mb-2">{mount.name}</Badge>
                          <p className="text-sm text-cosmic-text-secondary">{mount.description}</p>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                </div>
              )}
              {palmGuide.hand_shapes && palmGuide.hand_shapes.length > 0 && (
                <div>
                  <h3 className="font-display font-semibold text-cosmic-text mb-3">Hand Shapes</h3>
                  <div className="grid sm:grid-cols-2 gap-3">
                    {palmGuide.hand_shapes.map((shape) => (
                      <Card key={shape.name} className="bg-cosmic-card border-0 shadow-soft">
                        <CardContent className="p-4">
                          <Badge className="bg-green-500/20 text-green-400 mb-2">{shape.name}</Badge>
                          <p className="text-sm text-cosmic-text-secondary">{shape.description}</p>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="text-center py-12">
              <Hand className="w-12 h-12 text-cosmic-text-muted mx-auto mb-3" />
              <p className="text-cosmic-text-secondary mb-4">Click to load the palmistry guide</p>
              <Button onClick={loadPalmistry} className="bg-sacred-gold text-[#1a1a2e] hover:bg-sacred-gold-dark">
                <Hand className="w-4 h-4 mr-2" />Load Guide
              </Button>
            </div>
          )}
        </TabsContent>
      </Tabs>
    </section>
  );
}
