import { useState, useEffect, useCallback } from 'react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';
import { BookOpen, Search, Info, ShieldCheck, HelpCircle, AlertCircle } from 'lucide-react';
import SourceBadge from './SourceBadge';

/**
 * LalKitabFarmaanTab — P2.1 + P2.7 + P2.8 MVP.
 *
 * The Farmaan corpus ships EMPTY at first release. Content is populated
 * by the admin import pipeline (future sprint) from the 5 editions of
 * Lal Kitab (1939 / 1940 / 1941 / 1942 / 1952) — scan → OCR → translit
 * → translate → commentary.
 *
 * In the meantime this tab:
 *   - Shows a clear "corpus is being populated" hero message so users
 *     aren't confused by an empty list
 *   - Provides the search UI so users can see the interaction surface
 *   - Shows the rights-provenance badge catalog (P2.8) as a reference
 *     panel — educates users about how different content types are
 *     handled legally and why
 *   - Renders any rows that DO get ingested (list view with rights
 *     badge + confidence pill + planet/house/debt tag chips)
 */

interface FarmaanRow {
  id: string;
  farmaan_number: number | null;
  urdu_script: string;
  urdu_latin: string | null;
  hindi: string | null;
  english: string | null;
  confidence_level: string;
  planet_tags: string[] | null;
  house_tags: number[] | null;
  debt_tags: string[] | null;
  rights_status: string;
}

interface RightsEntry {
  label_en: string;
  label_hi: string;
  desc_en: string;
  desc_hi: string;
  colour: string;
  allows_reuse: boolean;
}

const CONFIDENCE_STYLE: Record<string, { cls: string; label_en: string; label_hi: string }> = {
  undeciphered: { cls: 'bg-gray-200 text-gray-700 border-gray-300', label_en: 'Undeciphered', label_hi: 'अडिकोडेड' },
  low:          { cls: 'bg-orange-100 text-orange-800 border-orange-300', label_en: 'Low', label_hi: 'कम' },
  moderate:     { cls: 'bg-amber-100 text-amber-800 border-amber-300', label_en: 'Moderate', label_hi: 'मध्यम' },
  high:         { cls: 'bg-emerald-100 text-emerald-800 border-emerald-300', label_en: 'High', label_hi: 'उच्च' },
  canonical:    { cls: 'bg-sacred-gold/20 text-sacred-gold-dark border-sacred-gold/50', label_en: 'Canonical', label_hi: 'प्रमाणिक' },
};

export default function LalKitabFarmaanTab() {
  const { t, language } = useTranslation();
  const isHi = language === 'hi';

  const [results, setResults] = useState<FarmaanRow[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');
  const [query, setQuery] = useState('');
  const [planetFilter, setPlanetFilter] = useState<string>('');
  const [debtFilter, setDebtFilter] = useState<string>('');
  const [rightsCatalog, setRightsCatalog] = useState<Record<string, RightsEntry>>({});

  // Load rights catalog once (cheap + static).
  useEffect(() => {
    api.get('/api/lalkitab/rights-catalog')
      .then((res: any) => setRightsCatalog(res?.rights ?? {}))
      .catch(() => { /* non-fatal */ });
  }, []);

  const runSearch = useCallback(() => {
    setLoading(true);
    setError('');
    const params = new URLSearchParams();
    if (query) params.set('q', query);
    if (planetFilter) params.set('planet', planetFilter);
    if (debtFilter) params.set('debt', debtFilter);
    api.get(`/api/lalkitab/farmaan/search?${params.toString()}`)
      .then((res: any) => setResults(Array.isArray(res?.results) ? res.results : []))
      .catch(() => setError(isHi ? 'खोज विफल।' : 'Search failed.'))
      .finally(() => setLoading(false));
  }, [query, planetFilter, debtFilter, isHi]);

  useEffect(() => { runSearch(); }, [runSearch]);

  const isEmpty = !loading && results.length === 0 && !error;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-xl font-sans font-semibold text-sacred-gold flex items-center gap-2 mb-1 flex-wrap">
          <BookOpen className="w-5 h-5" />
          {isHi ? 'फ़रमान (उर्दू दोहे)' : 'Farmaan (Urdu Couplets)'}
          <SourceBadge source="LK_CANONICAL" size="xs" />
        </h2>
        <p className="text-sm text-gray-500">
          {isHi
            ? 'लाल किताब 1939–1952 के उर्दू दोहे — शाब्दिक, पारंपरिक और आधुनिक व्याख्याओं के साथ।'
            : 'Urdu couplets from Lal Kitab 1939–1952 with literal, traditional, and modern commentary.'}
        </p>
      </div>

      {/* MVP NOTICE — corpus is being populated */}
      {isEmpty && (
        <div className="rounded-xl border border-sacred-gold/30 bg-sacred-gold/5 p-5 flex items-start gap-3">
          <Info className="w-5 h-5 text-sacred-gold shrink-0 mt-0.5" />
          <div>
            <p className="font-semibold text-sacred-gold-dark mb-1">
              {isHi ? 'फ़रमान संग्रह तैयार हो रहा है' : 'Farmaan corpus is being populated'}
            </p>
            <p className="text-sm text-foreground/75 leading-relaxed">
              {isHi
                ? 'हम 5 संस्करणों (1939 / 1940 / 1941 / 1942 / 1952) से स्कैन → लिप्यंतरण → अनुवाद → व्याख्या की प्रक्रिया से फ़रमान जोड़ रहे हैं। जैसे-जैसे सामग्री तैयार होती है, वे यहाँ दिखाई देंगे।'
                : 'We are adding Farmaan from 5 editions (1939 / 1940 / 1941 / 1942 / 1952) via a scan → transliterate → translate → commentate pipeline. Entries will appear here as they are verified.'}
            </p>
            <p className="text-xs text-foreground/60 mt-2">
              {isHi
                ? 'डेटाबेस व खोज API पहले से ही लाइव हैं — केवल सामग्री अपलोड होना बाकी है।'
                : 'The database and search API are already live — only content ingestion is pending.'}
            </p>
          </div>
        </div>
      )}

      {/* Search bar */}
      <div className="rounded-xl border border-border bg-white/60 p-4 space-y-3">
        <div className="flex items-center gap-2">
          <Search className="w-4 h-4 text-sacred-gold shrink-0" />
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => { if (e.key === 'Enter') runSearch(); }}
            placeholder={isHi ? 'जैसे: विवाह, स्वास्थ्य, धन, शत्रु, संतान…' : 'e.g. marriage, health, wealth, enemy, property…'}
            className="flex-1 px-3 py-2 rounded-lg border border-border text-sm bg-white focus:border-sacred-gold focus:outline-none"
          />
          <button
            onClick={runSearch}
            className="px-3 py-2 rounded-lg bg-sacred-gold text-white text-sm font-semibold hover:bg-sacred-gold-dark transition-colors"
          >
            {isHi ? 'खोजें' : 'Search'}
          </button>
        </div>
        <div className="flex flex-wrap gap-2">
          <select
            value={planetFilter}
            onChange={(e) => setPlanetFilter(e.target.value)}
            className="px-2 py-1 rounded border text-xs bg-white"
          >
            <option value="">{isHi ? 'सभी ग्रह' : 'All planets'}</option>
            {['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu'].map((p) => (
              <option key={p} value={p}>{p}</option>
            ))}
          </select>
          <select
            value={debtFilter}
            onChange={(e) => setDebtFilter(e.target.value)}
            className="px-2 py-1 rounded border text-xs bg-white"
          >
            <option value="">{isHi ? 'सभी ऋण' : 'All debts'}</option>
            {['Pitru Rin', 'Matru Rin', 'Deva Rin', 'Rishi Rin', 'Nri Rin', 'Bhoot Rin'].map((d) => (
              <option key={d} value={d}>{d}</option>
            ))}
          </select>
        </div>
      </div>

      {error && (
        <div className="rounded-xl border border-red-200 bg-red-50 p-3 text-sm text-red-700 flex items-center gap-2">
          <AlertCircle className="w-4 h-4" />
          {error}
        </div>
      )}

      {/* Results list */}
      {!loading && results.length > 0 && (
        <div className="space-y-3">
          {results.map((f) => {
            const rights = rightsCatalog[f.rights_status];
            const conf = CONFIDENCE_STYLE[f.confidence_level] ?? CONFIDENCE_STYLE.undeciphered;
            return (
              <div key={f.id} className="rounded-xl border border-border bg-white/70 p-4">
                <div className="flex items-start justify-between gap-3 mb-2 flex-wrap">
                  <div className="flex items-center gap-2">
                    {f.farmaan_number != null && (
                      <span className="text-xs text-gray-400 font-mono">#{f.farmaan_number}</span>
                    )}
                    <span className={`text-[10px] px-2 py-0.5 rounded-full border font-semibold uppercase ${conf.cls}`}>
                      {isHi ? conf.label_hi : conf.label_en}
                    </span>
                  </div>
                  {rights && (
                    <span
                      className="text-[10px] px-2 py-0.5 rounded-full border font-semibold flex items-center gap-1"
                      style={{ backgroundColor: `${rights.colour}15`, color: rights.colour, borderColor: `${rights.colour}60` }}
                      title={isHi ? rights.desc_hi : rights.desc_en}
                    >
                      <ShieldCheck className="w-3 h-3" />
                      {isHi ? rights.label_hi : rights.label_en}
                    </span>
                  )}
                </div>

                {/* Bilingual body */}
                {f.urdu_script && (
                  <p dir="rtl" className="text-lg text-sacred-brown font-serif mb-1.5" lang="ur">{f.urdu_script}</p>
                )}
                {f.urdu_latin && <p className="text-sm text-foreground/70 italic mb-1">{f.urdu_latin}</p>}
                {(isHi ? f.hindi : f.english) && (
                  <p className="text-sm text-foreground">{isHi ? f.hindi : f.english}</p>
                )}

                {/* Tags */}
                <div className="flex flex-wrap gap-1.5 mt-3">
                  {(f.planet_tags ?? []).map((p) => (
                    <span key={`p-${p}`} className="text-[10px] px-2 py-0.5 rounded-full bg-sacred-gold/10 text-sacred-gold-dark font-semibold">
                      {p}
                    </span>
                  ))}
                  {(f.house_tags ?? []).map((h) => (
                    <span key={`h-${h}`} className="text-[10px] px-2 py-0.5 rounded-full bg-indigo-100 text-indigo-700 font-semibold">
                      H{h}
                    </span>
                  ))}
                  {(f.debt_tags ?? []).map((d) => (
                    <span key={`d-${d}`} className="text-[10px] px-2 py-0.5 rounded-full bg-violet-100 text-violet-700 font-semibold">
                      {d}
                    </span>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Rights-provenance catalog — always visible so users understand the badges */}
      {Object.keys(rightsCatalog).length > 0 && (
        <div className="rounded-xl border border-border bg-white/50 p-5">
          <h3 className="font-sans font-semibold text-sacred-gold mb-3 flex items-center gap-2">
            <HelpCircle className="w-4 h-4" />
            {isHi ? 'अधिकार सूची (P2.8)' : 'Rights Provenance Catalogue (P2.8)'}
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
            {Object.entries(rightsCatalog).map(([key, r]) => (
              <div key={key} className="flex items-start gap-2 p-2 rounded border border-gray-100">
                <span
                  className="w-3 h-3 rounded-full mt-0.5 shrink-0"
                  style={{ backgroundColor: r.colour }}
                />
                <div>
                  <p className="text-xs font-semibold text-foreground">
                    {isHi ? r.label_hi : r.label_en}
                    <span className="text-[10px] text-gray-400 font-mono ml-1.5">{key}</span>
                  </p>
                  <p className="text-[11px] text-foreground/60 leading-snug">
                    {isHi ? r.desc_hi : r.desc_en}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
