import { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import { Loader2, Hand, Sparkles, X, RotateCcw } from 'lucide-react';
import PalmSVG from './PalmSVG';

interface PalmZone {
  zone_id: string; name: string; planet: string;
  svg_cx: number; svg_cy: number; svg_r: number; zone_type: string;
}
interface PalmMark { zone_id: string; mark_type: string; }
interface Correlation {
  zone_id: string; zone_name: string; planet: string;
  mark_type: string; nature: 'benefic' | 'malefic' | 'mixed';
  interpretation: { en: string; hi: string };
}
interface CorrelationResult {
  kundli_id: string; correlations: Correlation[];
  overall_samudrik_score: number; benefic_count: number; malefic_count: number;
  summary: { en: string; hi: string };
}

interface Props { kundliId?: string; language: string; }

const MARK_TYPES = ['cross','star','island','chain','dot','triangle','square','trident','circle'];
const MARK_SYMBOL: Record<string, string> = {
  cross:'✕', star:'★', island:'◈', chain:'⊕', dot:'•',
  triangle:'△', square:'□', trident:'ψ', circle:'○',
};
const NATURE_STYLE: Record<string, string> = {
  benefic: 'bg-green-100 text-green-700 border-green-200',
  malefic: 'bg-red-100 text-red-700 border-red-200',
  mixed: 'bg-yellow-100 text-yellow-700 border-yellow-200',
};

export default function LalKitabPalmistryTab({ kundliId, language }: Props) {
  const [zones, setZones] = useState<PalmZone[]>([]);
  const [marks, setMarks] = useState<PalmMark[]>([]);
  const [selectedZone, setSelectedZone] = useState<string | null>(null);
  const [result, setResult] = useState<CorrelationResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const hi = language === 'hi';

  useEffect(() => {
    setLoading(true);
    api.get('/api/lalkitab/palm/zones')
      .then(r => setZones(r.zones ?? r)).catch(() => {}).finally(() => setLoading(false));
  }, []);

  const handleZoneClick = (zoneId: string) => {
    setSelectedZone(zoneId === selectedZone ? null : zoneId);
    setResult(null);
  };

  const addMark = (markType: string) => {
    if (!selectedZone) return;
    setMarks(prev => {
      const existing = prev.findIndex(m => m.zone_id === selectedZone);
      if (existing >= 0) {
        const updated = [...prev];
        updated[existing] = { zone_id: selectedZone, mark_type: markType };
        return updated;
      }
      return [...prev, { zone_id: selectedZone, mark_type: markType }];
    });
    setSelectedZone(null);
    setResult(null);
  };

  const removeMark = (zoneId: string) => {
    setMarks(prev => prev.filter(m => m.zone_id !== zoneId));
    setResult(null);
  };

  const analyze = async () => {
    if (!kundliId || marks.length === 0) return;
    setAnalyzing(true);
    try {
      const res = await api.post('/api/lalkitab/palm/correlate', { kundli_id: kundliId, palm_marks: marks });
      setResult(res);
    } catch (e) {
      // silent
    } finally {
      setAnalyzing(false);
    }
  };

  const reset = () => { setMarks([]); setResult(null); setSelectedZone(null); };

  if (!kundliId) return (
    <div className="text-center py-10 text-muted-foreground text-sm">
      {hi ? 'विश्लेषण के लिए कुंडली सहेजें।' : 'Save a Kundli to use Palmistry Analysis.'}
    </div>
  );

  if (loading) return <div className="flex justify-center py-16"><Loader2 className="w-8 h-8 animate-spin text-sacred-gold" /></div>;

  const selectedZoneData = zones.find(z => z.zone_id === selectedZone);

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="text-center">
        <div className="text-3xl mb-1">🖐️</div>
        <h3 className="font-bold text-foreground">
          {hi ? 'समुद्रिक शास्त्र — हस्तरेखा' : 'Samudrik Shastra — Palmistry'}
        </h3>
        <p className="text-sm text-muted-foreground mt-1">
          {hi ? 'हस्तरेखा पर निशान चुनकर ग्रह प्रभाव जानें' : 'Select marks on your palm to correlate with planetary energies'}
        </p>
      </div>

      {/* Palm diagram */}
      <div className="bg-amber-50/40 border border-amber-100 rounded-2xl p-3">
        <PalmSVG
          zones={zones}
          marks={marks}
          onZoneClick={handleZoneClick}
          selectedZone={selectedZone}
          language={language}
        />
      </div>

      {/* Mark selector (shown when zone selected) */}
      {selectedZone && (
        <div className="border border-sacred-gold/30 bg-sacred-gold/5 rounded-xl p-3">
          <div className="text-xs font-semibold text-sacred-gold mb-2">
            {hi
              ? `${selectedZoneData?.name || selectedZone} पर निशान चुनें`
              : `Select mark for ${selectedZoneData?.name || selectedZone}`}
          </div>
          <div className="grid grid-cols-5 gap-1.5">
            {MARK_TYPES.map(mt => (
              <button
                key={mt}
                onClick={() => addMark(mt)}
                className="flex flex-col items-center gap-0.5 p-2 rounded-lg bg-white border border-border hover:border-sacred-gold/50 transition-all"
              >
                <span className="text-lg leading-none">{MARK_SYMBOL[mt]}</span>
                <span className="text-[9px] text-muted-foreground capitalize">{mt}</span>
              </button>
            ))}
          </div>
          <button onClick={() => setSelectedZone(null)} className="mt-2 text-xs text-muted-foreground flex items-center gap-1">
            <X className="w-3 h-3" /> {hi ? 'रद्द करें' : 'Cancel'}
          </button>
        </div>
      )}

      {/* Applied marks */}
      {marks.length > 0 && (
        <div>
          <div className="flex items-center justify-between mb-2">
            <div className="text-xs font-semibold text-foreground">
              {hi ? `${marks.length} निशान लगाए` : `${marks.length} mark(s) placed`}
            </div>
            <button onClick={reset} className="text-xs text-muted-foreground flex items-center gap-1">
              <RotateCcw className="w-3 h-3" /> {hi ? 'साफ करें' : 'Reset'}
            </button>
          </div>
          <div className="flex flex-wrap gap-1.5">
            {marks.map(m => {
              const z = zones.find(z => z.zone_id === m.zone_id);
              return (
                <div key={m.zone_id} className="flex items-center gap-1 text-xs bg-white border border-border rounded-full px-2 py-1">
                  <span>{MARK_SYMBOL[m.mark_type]}</span>
                  <span className="text-muted-foreground">{z?.name || m.zone_id}</span>
                  <button onClick={() => removeMark(m.zone_id)} className="text-muted-foreground hover:text-destructive">
                    <X className="w-3 h-3" />
                  </button>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Analyze button */}
      {marks.length > 0 && !result && (
        <button
          onClick={analyze}
          disabled={analyzing}
          className="w-full py-3 rounded-xl bg-sacred-gold text-white font-semibold text-sm flex items-center justify-center gap-2 hover:opacity-90 disabled:opacity-50 transition-all"
        >
          {analyzing ? <Loader2 className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4" />}
          {hi ? 'ग्रह प्रभाव जानें' : 'Analyze Planetary Correlations'}
        </button>
      )}

      {/* Results */}
      {result && (
        <div className="space-y-3">
          {/* Score */}
          <div className="rounded-xl p-4 bg-gradient-to-r from-amber-50 to-sacred-gold/5 border border-sacred-gold/20 text-center">
            <div className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-1">
              {hi ? 'समुद्रिक स्कोर' : 'Samudrik Score'}
            </div>
            <div className="text-5xl font-bold text-sacred-gold mb-1">{result.overall_samudrik_score}</div>
            <div className="text-xs text-muted-foreground">
              {hi
                ? `${result.benefic_count} शुभ • ${result.malefic_count} अशुभ निशान`
                : `${result.benefic_count} benefic • ${result.malefic_count} malefic marks`}
            </div>
            <p className="text-sm text-foreground mt-2 italic">
              "{hi ? result.summary.hi : result.summary.en}"
            </p>
          </div>

          {/* Correlations */}
          {result.correlations.map((c, i) => (
            <div key={i} className={`border rounded-xl p-3 ${NATURE_STYLE[c.nature] || 'border-border bg-card'}`}>
              <div className="flex items-center gap-2 mb-1.5">
                <span className="text-base">{MARK_SYMBOL[c.mark_type] || '•'}</span>
                <span className="text-sm font-semibold text-foreground">{c.zone_name}</span>
                <span className="text-xs text-muted-foreground">({c.planet})</span>
                <span className={`ml-auto text-xs px-1.5 py-0.5 rounded-full ${NATURE_STYLE[c.nature]}`}>
                  {c.nature}
                </span>
              </div>
              <p className="text-xs text-foreground leading-relaxed">
                {hi ? c.interpretation.hi : c.interpretation.en}
              </p>
            </div>
          ))}

          <button onClick={reset} className="w-full py-2 text-xs text-muted-foreground border border-border rounded-xl hover:bg-muted/30 transition-all">
            {hi ? 'नए निशान के साथ दोबारा करें' : 'Start over with new marks'}
          </button>
        </div>
      )}
    </div>
  );
}
