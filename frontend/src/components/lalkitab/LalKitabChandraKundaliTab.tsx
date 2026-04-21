// LalKitabChandraKundaliTab — P1.12
//
// Renders the Chandra Kundali as an INDEPENDENT LK predictive framework
// (per LK 1952 canon). Moon becomes H1; planets are re-anchored; readings
// come from the LK Chandra-specific table (NOT the Lagna table).
//
// Backend: GET /api/lalkitab/chandra-kundali/{kundli_id}
import { useEffect, useMemo, useState } from 'react';
import { Loader2, Moon, Info, AlertTriangle, CheckCircle2, BookOpen } from 'lucide-react';
import { api } from '@/lib/api';
import { useLalKitab } from './LalKitabContext';
import { toLkPlanetList } from './lalkitab-core';
import InteractiveKundli, { type PlanetData, type ChartData } from '@/components/InteractiveKundli';
import { pickLang } from './safe-render';

interface Props {
  language: string;
  kundliId?: string;
}

interface ChandraPosition {
  planet: string;
  planet_hi: string;
  natal_house: number;
  chandra_house: number;
}

interface ChandraReading {
  planet: string;
  planet_hi: string;
  chandra_house: number;
  natal_house: number;
  en: string;
  hi: string;
  is_favourable: boolean;
}

interface ChandraConflict {
  planet: string;
  planet_hi: string;
  lagna_house: number;
  chandra_house: number;
  lagna_nature: string;
  lagna_is_favourable: boolean;
  chandra_is_favourable: boolean;
  note_en: string;
  note_hi: string;
}

interface ChandraKundaliData {
  moon_lagna_house: number;
  chandra_positions: ChandraPosition[];
  readings: ChandraReading[];
  conflicts_with_lagna: ChandraConflict[];
  framework_note_en: string;
  framework_note_hi: string;
  source: string;
}

const ZODIAC_SIGNS = [
  'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
  'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces',
];

export default function LalKitabChandraKundaliTab({ language, kundliId: kundliIdProp }: Props) {
  const ctx = useLalKitab();
  const kundliId = kundliIdProp || ctx.kundliId || '';
  const apiResult = ctx.apiResult;
  const hi = language === 'hi';

  const [data, setData] = useState<ChandraKundaliData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!kundliId) { setData(null); return; }
    let cancelled = false;
    setLoading(true);
    setError(null);
    api.get(`/api/lalkitab/chandra-kundali/${kundliId}`)
      .then((res: any) => { if (!cancelled) setData(res as ChandraKundaliData); })
      .catch((err: any) => {
        if (cancelled) return;
        const msg = err instanceof Error ? err.message : (typeof err === 'string' ? err : 'Unknown error');
        setError(msg);
      })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [kundliId]);

  // Build re-anchored InteractiveKundli chart data.
  // We take the natal planets but OVERRIDE each planet's `house` to its
  // chandra_house so the chart visually shows the Moon-anchored positions.
  const chandraChartData: ChartData | null = useMemo(() => {
    const planetsRaw = apiResult?.chart_data?.planets;
    if (!planetsRaw || !data) return null;

    const basePlanets: PlanetData[] = toLkPlanetList(planetsRaw);
    const chandraHouseByPlanet = new Map<string, number>(
      data.chandra_positions.map((p) => [p.planet, p.chandra_house]),
    );

    const rePlanets: PlanetData[] = basePlanets.map((p) => {
      const ch = chandraHouseByPlanet.get(p.planet);
      if (!ch) return p;
      return { ...p, house: ch };
    });

    // For the Chandra chart, H1 is anchored on Moon's natal sign.
    // We still show zodiac signs in the usual sequence so the chart reads
    // as a proper 12-house kundli — but H1 label is the Moon's natal sign.
    const moonPlanet = basePlanets.find((p) => p.planet === 'Moon');
    const anchorSign = moonPlanet?.sign || 'Aries';
    const ascIdx = ZODIAC_SIGNS.indexOf(anchorSign);
    const houses = Array.from({ length: 12 }, (_, i) => ({
      number: i + 1,
      sign: ZODIAC_SIGNS[((ascIdx >= 0 ? ascIdx : 0) + i) % 12],
    }));

    return {
      planets: rePlanets,
      houses,
      ascendant: { longitude: 0, sign: anchorSign },
    };
  }, [apiResult, data]);

  // ── Render guards ──────────────────────────────────────────
  if (!kundliId) {
    return (
      <div className="text-center py-10 text-muted-foreground text-sm">
        {hi
          ? 'चंद्र कुंडली देखने के लिए कुंडली सहेजें।'
          : 'Save a Kundli to see the Chandra Kundali.'}
      </div>
    );
  }

  if (loading) {
    return (
      <div className="flex justify-center py-16">
        <Loader2 className="w-8 h-8 animate-spin text-sacred-gold" />
      </div>
    );
  }

  if (error && !data) {
    return (
      <div className="p-3 mb-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-800">
        {hi ? 'चंद्र कुंडली लोड करने में त्रुटि' : 'Failed to load Chandra Kundali'}: {error}
      </div>
    );
  }

  if (!data) return null;

  const conflicts = data.conflicts_with_lagna || [];
  const readings = data.readings || [];

  return (
    <div className="space-y-6">
      {/* ── Header ───────────────────────────────────────────── */}
      <div className="flex items-center gap-2">
        <Moon className="w-5 h-5 text-sacred-gold" />
        <h3 className="font-sans text-lg font-semibold text-sacred-gold">
          {hi ? 'चंद्र कुंडली — स्वतंत्र लाल किताब ढांचा' : 'Chandra Kundali — Independent LK Framework'}
        </h3>
      </div>

      {/* ── Framework note ───────────────────────────────────── */}
      <div className="rounded-xl border border-blue-200 bg-blue-50/60 p-4 flex items-start gap-3">
        <Info className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
        <div className="text-sm text-blue-900 leading-relaxed">
          <div className="font-semibold mb-1">
            {hi ? 'एक स्वतंत्र कुंडली — वैदिक शॉर्टकट नहीं' : 'An independent chart — not a Vedic shortcut'}
          </div>
          <p>{hi ? data.framework_note_hi : data.framework_note_en}</p>
          <div className="text-xs text-blue-700 mt-2">
            {hi
              ? `चंद्रमा का जन्म-भाव: H${data.moon_lagna_house} → चंद्र कुंडली का H1`
              : `Moon's natal house: H${data.moon_lagna_house} → becomes H1 of Chandra Kundali`}
          </div>
        </div>
      </div>

      {/* ── Re-anchored chart ────────────────────────────────── */}
      <div className="rounded-xl border border-sacred-gold/20 bg-card p-4">
        <div className="text-xs text-muted-foreground mb-3 flex items-center gap-1.5">
          <Moon className="w-3.5 h-3.5" />
          {hi
            ? 'चंद्र-आधारित पुनः-स्थापित चार्ट (चंद्रमा H1 है)'
            : 'Moon-anchored re-mapped chart (Moon is H1)'}
        </div>
        {chandraChartData ? (
          <div className="max-w-[520px] mx-auto">
            <InteractiveKundli chartData={chandraChartData} compact hideCombust />
          </div>
        ) : (
          <div className="text-center text-sm text-muted-foreground py-10">
            {hi ? 'चार्ट डेटा उपलब्ध नहीं' : 'Chart data not available'}
          </div>
        )}
      </div>

      {/* ── Per-planet Chandra readings ──────────────────────── */}
      <div className="rounded-xl border border-sacred-gold/20 bg-card p-4">
        <div className="flex items-center gap-2 mb-3">
          <BookOpen className="w-4 h-4 text-sacred-gold" />
          <h4 className="font-semibold text-sacred-gold">
            {hi ? 'प्रति-ग्रह चंद्र-कुंडली पठन' : 'Per-Planet Chandra Readings'}
          </h4>
          <span className="text-xs text-muted-foreground ml-auto">
            {readings.length} {hi ? 'ग्रह' : 'planets'}
          </span>
        </div>

        {readings.length === 0 ? (
          <div className="text-sm text-muted-foreground py-4 text-center">
            {hi ? 'कोई चंद्र-पठन उपलब्ध नहीं' : 'No Chandra readings available'}
          </div>
        ) : (
          <div className="grid gap-3 sm:grid-cols-2">
            {readings.map((r) => (
              <div
                key={r.planet}
                className={`rounded-xl border p-3 ${
                  r.is_favourable
                    ? 'border-green-200 bg-green-50/40'
                    : 'border-amber-200 bg-amber-50/40'
                }`}
              >
                <div className="flex items-center justify-between mb-1.5">
                  <div className="font-semibold text-sm text-foreground">
                    {hi ? r.planet_hi : r.planet}
                    <span className="text-xs text-muted-foreground ml-2">
                      {hi ? `भाव ${r.natal_house} → भाव ${r.chandra_house}` : `H${r.natal_house} → H${r.chandra_house}`}
                    </span>
                  </div>
                  <span
                    className={`text-[10px] px-2 py-0.5 rounded-full font-medium ${
                      r.is_favourable
                        ? 'bg-green-100 text-green-700'
                        : 'bg-amber-100 text-amber-700'
                    }`}
                  >
                    {r.is_favourable
                      ? (hi ? 'शुभ' : 'favourable')
                      : (hi ? 'पीड़ित' : 'strained')}
                  </span>
                </div>
                <p className="text-xs leading-relaxed text-foreground/80">
                  {pickLang({ en: r.en, hi: r.hi }, hi)}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* ── Conflicts with Lagna ─────────────────────────────── */}
      <div className="rounded-xl border border-sacred-gold/20 bg-card p-4">
        <div className="flex items-center gap-2 mb-3">
          {conflicts.length > 0 ? (
            <AlertTriangle className="w-4 h-4 text-orange-500" />
          ) : (
            <CheckCircle2 className="w-4 h-4 text-green-600" />
          )}
          <h4 className="font-semibold text-sacred-gold">
            {hi ? 'लग्न बनाम चंद्र — असहमतियाँ' : 'Lagna vs Chandra — Conflicts'}
          </h4>
          <span className="text-xs text-muted-foreground ml-auto">
            {conflicts.length} {hi ? 'असहमति' : 'conflicts'}
          </span>
        </div>

        {conflicts.length === 0 ? (
          <div className="text-sm text-green-700 bg-green-50 border border-green-200 rounded-lg p-3">
            {hi
              ? 'लग्न व चंद्र कुंडली के पठन इस जन्म के लिए एक-दूसरे से मेल खाते हैं। बाहरी और भीतरी जीवन संरेखित हैं।'
              : 'Lagna and Chandra readings agree for this chart. Outer and inner life are aligned.'}
          </div>
        ) : (
          <div className="space-y-3">
            <p className="text-xs text-muted-foreground">
              {hi
                ? 'लाल किताब कहती है कि दोनों आवाज़ें ज़रूरी हैं — किसी एक को चुप न करें।'
                : 'Lal Kitab holds both voices matter — do not silence either.'}
            </p>
            {conflicts.map((c) => (
              <div
                key={c.planet}
                className="rounded-xl border border-orange-200 bg-orange-50/40 p-3"
              >
                <div className="flex flex-wrap items-center gap-2 mb-2">
                  <span className="font-semibold text-sm">
                    {hi ? c.planet_hi : c.planet}
                  </span>
                  <span className="text-[10px] px-2 py-0.5 rounded-full bg-blue-100 text-blue-700">
                    {hi ? 'लग्न' : 'Lagna'} {hi ? `भाव ${c.lagna_house}` : `H${c.lagna_house}`}{' '}
                    {c.lagna_is_favourable
                      ? (hi ? '• शुभ' : '• favourable')
                      : (hi ? '• प्रतिकूल' : '• unfavourable')}
                  </span>
                  <span className="text-[10px] px-2 py-0.5 rounded-full bg-indigo-100 text-indigo-700">
                    {hi ? 'चंद्र' : 'Chandra'} {hi ? `भाव ${c.chandra_house}` : `H${c.chandra_house}`}{' '}
                    {c.chandra_is_favourable
                      ? (hi ? '• शुभ' : '• favourable')
                      : (hi ? '• पीड़ित' : '• strained')}
                  </span>
                </div>
                <p className="text-xs leading-relaxed text-foreground/80">
                  {pickLang({ en: c.note_en, hi: c.note_hi }, hi)}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
