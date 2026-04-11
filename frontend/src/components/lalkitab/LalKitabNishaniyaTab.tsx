import { useState, useEffect } from 'react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';
import { BookOpen, Loader2, AlertTriangle, Flame, Minus } from 'lucide-react';

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

type CategoryFilter = 'all' | 'general' | 'health' | 'wealth' | 'marriage' | 'career' | 'family';
type SeverityFilter = 'all' | 'mild' | 'moderate' | 'strong';

const PLANET_HI: Record<string, string> = {
  sun: 'सूर्य', moon: 'चंद्र', mars: 'मंगल', mercury: 'बुध',
  jupiter: 'गुरु', venus: 'शुक्र', saturn: 'शनि', rahu: 'राहु', ketu: 'केतु',
};

const severityConfig: Record<string, { label: string; labelHi: string; cls: string; icon: React.ElementType }> = {
  mild:     { label: 'Mild',     labelHi: 'सौम्य',    cls: 'bg-green-500/10 text-green-700 border-green-300/40',   icon: Minus },
  moderate: { label: 'Moderate', labelHi: 'मध्यम',   cls: 'bg-sacred-gold/10 text-sacred-gold-dark border-sacred-gold/30', icon: AlertTriangle },
  strong:   { label: 'Strong',   labelHi: 'प्रबल',   cls: 'bg-red-500/10 text-red-700 border-red-300/40',          icon: Flame },
};

const categoryLabels: Record<string, { en: string; hi: string }> = {
  all:      { en: 'All',      hi: 'सभी' },
  general:  { en: 'General',  hi: 'सामान्य' },
  health:   { en: 'Health',   hi: 'स्वास्थ्य' },
  wealth:   { en: 'Wealth',   hi: 'धन' },
  marriage: { en: 'Marriage', hi: 'विवाह' },
  career:   { en: 'Career',   hi: 'करियर' },
  family:   { en: 'Family',   hi: 'परिवार' },
};

const CATEGORIES: CategoryFilter[] = ['all', 'general', 'health', 'wealth', 'marriage', 'career', 'family'];
const SEVERITIES: SeverityFilter[] = ['all', 'mild', 'moderate', 'strong'];

export default function LalKitabNishaniyaTab({ kundliId }: Props) {  // chartData prop removed — tab uses DB API
  const { language } = useTranslation();
  const isHi = language === 'hi';

  const [nishaniyan, setNishaniyan] = useState<Nishani[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [activeCategory, setActiveCategory] = useState<CategoryFilter>('all');
  const [activeSeverity, setActiveSeverity] = useState<SeverityFilter>('all');

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

  const filtered = nishaniyan.filter((n) => {
    if (activeCategory !== 'all' && n.category !== activeCategory) return false;
    if (activeSeverity !== 'all' && n.severity !== activeSeverity) return false;
    return true;
  });

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

      {/* Summary badges */}
      {!loading && nishaniyan.length > 0 && (
        <div className="flex flex-wrap gap-3">
          <div className="flex items-center gap-2 px-4 py-2 rounded-xl bg-sacred-gold/10 border border-sacred-gold/20">
            <BookOpen className="w-4 h-4 text-sacred-gold" />
            <span className="text-sm font-semibold text-sacred-gold">
              {nishaniyan.length} {isHi ? 'निशानियां' : 'Nishaniyan'}
            </span>
          </div>
          {strongCount > 0 && (
            <div className="flex items-center gap-2 px-4 py-2 rounded-xl bg-red-500/10 border border-red-300/20">
              <Flame className="w-4 h-4 text-red-600" />
              <span className="text-sm font-semibold text-red-700">
                {strongCount} {isHi ? 'प्रबल' : 'Strong'}
              </span>
            </div>
          )}
          {moderateCount > 0 && (
            <div className="flex items-center gap-2 px-4 py-2 rounded-xl bg-sacred-gold/10 border border-sacred-gold/20">
              <AlertTriangle className="w-4 h-4 text-sacred-gold" />
              <span className="text-sm font-semibold text-sacred-gold-dark">
                {moderateCount} {isHi ? 'मध्यम' : 'Moderate'}
              </span>
            </div>
          )}
        </div>
      )}

      {/* Category filter */}
      <div className="flex flex-wrap gap-2">
        {CATEGORIES.map((cat) => (
          <button
            key={cat}
            onClick={() => setActiveCategory(cat)}
            className={`px-3 py-1.5 rounded-full text-xs font-medium transition-all ${
              activeCategory === cat
                ? 'bg-sacred-gold text-white shadow-sm'
                : 'bg-sacred-gold/10 text-sacred-gold hover:bg-sacred-gold/20'
            }`}
          >
            {isHi ? categoryLabels[cat].hi : categoryLabels[cat].en}
          </button>
        ))}
      </div>

      {/* Severity filter */}
      <div className="flex flex-wrap gap-2">
        {SEVERITIES.map((sev) => {
          const cfg = sev === 'all' ? null : severityConfig[sev];
          return (
            <button
              key={sev}
              onClick={() => setActiveSeverity(sev)}
              className={`px-3 py-1.5 rounded-full text-xs font-medium transition-all border ${
                activeSeverity === sev
                  ? 'bg-cosmic-text text-white border-cosmic-text'
                  : 'bg-white/40 text-gray-600 border-gray-200/60 hover:bg-gray-100'
              }`}
            >
              {sev === 'all'
                ? (isHi ? 'सभी स्तर' : 'All Severity')
                : (isHi ? cfg?.labelHi : cfg?.label)}
            </button>
          );
        })}
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

      {/* Empty */}
      {!loading && !error && nishaniyan.length === 0 && (
        <div className="text-center py-12 text-gray-400 text-sm">
          {isHi ? 'कोई निशानियां नहीं मिलीं' : 'No nishaniyan found for this chart'}
        </div>
      )}

      {/* Grid */}
      {!loading && filtered.length > 0 && (
        <div className="grid gap-4 md:grid-cols-2">
          {filtered.map((n) => {
            const sev = severityConfig[n.severity] ?? severityConfig.moderate;
            const SevIcon = sev.icon;
            return (
              <div
                key={n.id}
                className="card-sacred rounded-xl border border-sacred-gold/20 p-4 bg-white/30"
              >
                {/* Planet + house row */}
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <span className="px-2.5 py-1 rounded-full bg-sacred-gold/15 text-sacred-gold-dark text-xs font-semibold">
                      {isHi ? (PLANET_HI[n.planet] ?? n.planet) : n.planet.charAt(0).toUpperCase() + n.planet.slice(1)}
                    </span>
                    <span className="px-2.5 py-1 rounded-full bg-cosmic-text/8 text-cosmic-text text-xs font-medium">
                      {isHi ? `भाव ${n.house}` : `House ${n.house}`}
                    </span>
                  </div>
                  <span className={`flex items-center gap-1 px-2 py-0.5 rounded-full border text-xs font-medium ${sev.cls}`}>
                    <SevIcon className="w-3 h-3" />
                    {isHi ? sev.labelHi : sev.label}
                  </span>
                </div>

                {/* Text */}
                <p className="text-sm text-cosmic-text leading-relaxed">{n.nishani_text}</p>

                {/* Category badge */}
                <div className="mt-3">
                  <span className="text-xs px-2 py-0.5 rounded-full bg-gray-100 text-gray-500">
                    {isHi ? categoryLabels[n.category]?.hi ?? n.category : categoryLabels[n.category]?.en ?? n.category}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Filtered empty */}
      {!loading && !error && nishaniyan.length > 0 && filtered.length === 0 && (
        <div className="text-center py-8 text-gray-400 text-sm">
          {isHi ? 'इस फ़िल्टर में कोई निशानियां नहीं हैं' : 'No nishaniyan match the selected filters'}
        </div>
      )}
    </div>
  );
}
