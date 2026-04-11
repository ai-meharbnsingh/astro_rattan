import { useState, useEffect, useMemo } from 'react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';
import { 
  BookOpen, 
  Loader2, 
  AlertTriangle, 
  Flame, 
  Minus, 
  CheckCircle2, 
  Circle,
  TrendingUp,
  Target
} from 'lucide-react';

interface Props {
  kundliId: string;
}

interface Nishani {
  id: string;
  planet: string;
  house: number;
  nishani_text: string;
  category: string;
  severity: string;
}

const STORAGE_KEY_PREFIX = 'lk_nishani_verify_';

export default function LalKitabNishaniyaTab({ kundliId }: Props) {
  const { t, language } = useTranslation();
  const isHi = language === 'hi';

  const [nishaniyan, setNishaniyan] = useState<Nishani[]>([]);
  const [confirmedIds, setConfirmedIds] = useState<Set<string>>(new Set());
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [activeCategory, setActiveCategory] = useState<string>('all');
  const [activeSeverity, setActiveSeverity] = useState<string>('all');

  // Load confirmed IDs from localStorage
  useEffect(() => {
    if (!kundliId) return;
    const stored = localStorage.getItem(`${STORAGE_KEY_PREFIX}${kundliId}`);
    if (stored) {
      try {
        setConfirmedIds(new Set(JSON.parse(stored)));
      } catch (e) {
        console.error('Failed to parse stored nishani verification', e);
      }
    }
  }, [kundliId]);

  // Save confirmed IDs to localStorage
  useEffect(() => {
    if (!kundliId) return;
    localStorage.setItem(`${STORAGE_KEY_PREFIX}${kundliId}`, JSON.stringify(Array.from(confirmedIds)));
  }, [confirmedIds, kundliId]);

  useEffect(() => {
    if (!kundliId) {
      setNishaniyan([]);
      setError('');
      return;
    }
    setLoading(true);
    setError('');
    api.get(`/api/lalkitab/nishaniyan/${kundliId}`)
      .then((res: any) => setNishaniyan(Array.isArray(res?.nishaniyan) ? res.nishaniyan : []))
      .catch(() => setError(isHi ? 'निशानियां लोड नहीं हो सकीं' : 'Failed to load nishaniyan'))
      .finally(() => setLoading(false));
  }, [kundliId]);

  const toggleConfirm = (id: string) => {
    const next = new Set(confirmedIds);
    if (next.has(id)) {
      next.delete(id);
    } else {
      next.add(id);
    }
    setConfirmedIds(next);
  };

  const filtered = nishaniyan.filter((n) => {
    if (activeCategory !== 'all' && n.category !== activeCategory) return false;
    if (activeSeverity !== 'all' && n.severity !== activeSeverity) return false;
    return true;
  });

  const accuracyScore = useMemo(() => {
    if (nishaniyan.length === 0) return 0;
    return Math.round((confirmedIds.size / nishaniyan.length) * 100);
  }, [confirmedIds, nishaniyan]);

  const strongCount = nishaniyan.filter((n) => n.severity === 'strong').length;
  const moderateCount = nishaniyan.filter((n) => n.severity === 'moderate').length;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-xl font-sans font-semibold text-sacred-gold flex items-center gap-2 mb-1">
          <BookOpen className="w-5 h-5" />
          {isHi ? 'लाल किताब निशानियां' : 'Lal Kitab Nishaniyan'}
        </h2>
        <p className="text-sm text-gray-500">
          {isHi
            ? 'आपकी कुंडली के ग्रहों के अनुसार जीवन के संकेत व निशानियां'
            : 'Life signs & omens based on your birth chart planet positions'}
        </p>
      </div>

      {/* Accuracy Meter */}
      {!loading && nishaniyan.length > 0 && (
        <div className="card-sacred p-5 rounded-2xl border border-sacred-gold/30 bg-gradient-to-br from-white to-sacred-gold/5">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-full bg-sacred-gold/10 flex items-center justify-center shrink-0">
                <Target className="w-6 h-6 text-sacred-gold" />
              </div>
              <div>
                <h3 className="font-sans font-bold text-cosmic-text">{t('lk.nishani.accuracyMeter')}</h3>
                <p className="text-xs text-cosmic-text/60">{t('lk.nishani.accuracyDesc')}</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="text-right">
                <p className="text-2xl font-sans font-black text-sacred-gold leading-none">{accuracyScore}%</p>
                <p className="text-[10px] text-gray-400 uppercase font-bold tracking-wider mt-1">VERIFIED</p>
              </div>
              <div className="w-32 h-2 bg-gray-200 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-sacred-gold transition-all duration-1000"
                  style={{ width: `${accuracyScore}%` }}
                />
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Summary badges */}
      {!loading && nishaniyan.length > 0 && (
        <div className="flex flex-wrap gap-3">
          <div className="flex items-center gap-2 px-4 py-2 rounded-xl bg-sacred-gold/10 border border-sacred-gold/20 text-sacred-gold text-sm font-semibold">
            <BookOpen className="w-4 h-4" />
            {nishaniyan.length} {isHi ? 'निशानियां' : 'Nishaniyan'}
          </div>
          <div className="flex items-center gap-2 px-4 py-2 rounded-xl bg-green-500/10 border border-green-300/20 text-green-700 text-sm font-semibold">
            <CheckCircle2 className="w-4 h-4" />
            {confirmedIds.size} {t('lk.nishani.confirmed')}
          </div>
        </div>
      )}

      {/* Checklist instructions */}
      <div className="p-4 rounded-xl bg-sacred-gold/5 border border-dashed border-sacred-gold/30">
        <p className="text-xs text-sacred-gold-dark font-medium leading-relaxed">
          <strong>{t('lk.nishani.verifyTitle')}:</strong> {t('lk.nishani.verifyDesc')}
        </p>
      </div>

      {/* Category filter */}
      <div className="flex flex-wrap gap-2">
        {['all', 'general', 'health', 'wealth', 'marriage', 'career', 'family'].map((cat) => (
          <button
            key={cat}
            onClick={() => setActiveCategory(cat)}
            className={`px-3 py-1.5 rounded-full text-xs font-medium transition-all ${
              activeCategory === cat
                ? 'bg-sacred-gold text-white shadow-sm'
                : 'bg-sacred-gold/10 text-sacred-gold hover:bg-sacred-gold/20'
            }`}
          >
            {isHi ? (cat === 'all' ? 'सभी' : cat) : cat.charAt(0).toUpperCase() + cat.slice(1)}
          </button>
        ))}
      </div>

      {/* Loading */}
      {loading && (
        <div className="flex items-center justify-center py-16">
          <Loader2 className="w-8 h-8 animate-spin text-sacred-gold" />
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="p-4 rounded-xl bg-red-50 border border-red-200 text-red-700 text-sm">
          {error}
        </div>
      )}

      {/* Grid */}
      {!loading && filtered.length > 0 && (
        <div className="grid gap-4 md:grid-cols-2">
          {filtered.map((n) => {
            const isConfirmed = confirmedIds.has(n.id);
            const planetLabel = isHi 
              ? ({sun:'सूर्य', moon:'चंद्र', mars:'मंगल', mercury:'बुध', jupiter:'गुरु', venus:'शुक्र', saturn:'शनि', rahu:'राहु', ketu:'केतु'}[n.planet] || n.planet)
              : n.planet.charAt(0).toUpperCase() + n.planet.slice(1);

            return (
              <div
                key={n.id}
                onClick={() => toggleConfirm(n.id)}
                className={`card-sacred rounded-xl border p-4 transition-all cursor-pointer group hover:scale-[1.01] ${
                  isConfirmed 
                    ? 'border-green-500 bg-green-50/30' 
                    : 'border-sacred-gold/20 bg-white/30'
                }`}
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <span className="px-2 py-0.5 rounded-full bg-sacred-gold/10 text-sacred-gold-dark text-[10px] font-bold uppercase tracking-tight">
                      {planetLabel} · H{n.house}
                    </span>
                    <span className="text-[10px] text-gray-400 font-medium uppercase">{n.category}</span>
                  </div>
                  <div className={`shrink-0 ${isConfirmed ? 'text-green-600' : 'text-gray-300 group-hover:text-sacred-gold/50'}`}>
                    {isConfirmed ? <CheckCircle2 className="w-5 h-5 fill-green-50" /> : <Circle className="w-5 h-5" />}
                  </div>
                </div>

                <p className="text-sm text-cosmic-text leading-relaxed font-medium">
                  {n.nishani_text}
                </p>

                <div className="mt-4 flex items-center justify-between">
                  <span className={`text-[10px] font-bold uppercase tracking-widest ${isConfirmed ? 'text-green-600' : 'text-gray-400'}`}>
                    {isConfirmed ? t('lk.nishani.confirmed') : t('lk.nishani.notConfirmed')}
                  </span>
                  <span className="text-[10px] text-sacred-gold font-bold opacity-0 group-hover:opacity-100 transition-opacity">
                    {isConfirmed ? t('lk.nishani.unconfirmBtn') : t('lk.nishani.confirmBtn')} →
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Empty */}
      {!loading && !error && nishaniyan.length === 0 && (
        <div className="text-center py-12 text-gray-400 text-sm">
          {isHi ? 'कोई निशानियां नहीं मिलीं' : 'No nishaniyan found for this chart'}
        </div>
      )}
    </div>
  );
}
