/**
 * P2.5 — Comparative Dual-View Tab.
 *
 * Professional LK astrologers read Natal Tewa (fixed-house) AND current-year
 * Varshphal (annual solar-return) side-by-side to see transits + strength
 * shifts. This tab renders both charts synchronised, colour-codes planet
 * states using the P1.1 classifier on BOTH charts, and below the charts
 * shows a Strength-Shift delta table that maps each planet's natal house
 * to its Varshphal house with a colour-coded arrow.
 *
 * Data sources:
 *   - Natal Tewa        → /api/lalkitab/advanced/{id}   (+ apiResult.chart_data)
 *   - Varshphal {year}  → /api/kundli/{id}/varshphal    (POST body: {year})
 *
 * Hover sync:
 *   The two InteractiveKundli charts do not currently expose a controlled
 *   hover prop (their internal hoveredPlanet state is private). Instead we
 *   maintain a shared hoveredPlanet in the delta table; hovering a row
 *   highlights both the natal and varshphal cells on that row so the
 *   astrologer gets visual "same-planet" feedback across the two charts.
 *   This is the MVP path — a future sweep can lift InteractiveKundli's
 *   hover state into a controlled prop for true chart-to-chart cross-hover.
 */
import { useEffect, useMemo, useState } from 'react';
import { useTranslation } from '@/lib/i18n';
import { GitCompareArrows } from 'lucide-react';
import InteractiveKundli, { type ChartData, type PlanetData } from '@/components/InteractiveKundli';
import { api } from '@/lib/api';
import { useLalKitab } from './LalKitabContext';
import { toLkPlanetList } from './lalkitab-core';
import { classifyPlanetStates, legendEntries, LK_PLANETS, type PlanetStateTag } from './planet-state';

interface Props {
  apiResult?: any;
}

const PLANET_HI: Record<string, string> = {
  Sun: 'सूर्य', Moon: 'चंद्र', Mars: 'मंगल', Mercury: 'बुध',
  Jupiter: 'गुरु', Venus: 'शुक्र', Saturn: 'शनि', Rahu: 'राहु', Ketu: 'केतु',
};

const ZODIAC_SIGNS = [
  'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
  'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces',
];

/** Build a ChartData from raw apiResult-like payload ({ chart_data: { planets, ascendant } }). */
function buildChartData(source: any): ChartData | null {
  const planetsRaw = source?.chart_data?.planets;
  if (!planetsRaw) return null;
  const planets: PlanetData[] = toLkPlanetList(planetsRaw);
  const asc = source?.chart_data?.ascendant;
  const ascSign = asc?.sign || 'Aries';
  const ascIdx = Math.max(0, ZODIAC_SIGNS.indexOf(ascSign));
  const houses = Array.from({ length: 12 }, (_, i) => ({
    number: i + 1,
    sign: ZODIAC_SIGNS[(ascIdx + i) % 12],
  }));
  return {
    planets,
    houses,
    ascendant: asc ? { longitude: asc.longitude || 0, sign: ascSign, sign_degree: asc.sign_degree } : undefined,
  };
}

/** Extract a planet→house map from a ChartData (or null). */
function houseMap(chart: ChartData | null): Record<string, number> {
  const out: Record<string, number> = {};
  if (!chart) return out;
  for (const p of chart.planets) {
    if (p?.planet && typeof p.house === 'number' && p.house > 0) {
      out[p.planet] = p.house;
    }
  }
  return out;
}

/** Circular LK-house delta on a 12-house cycle. Returns signed integer in [-6, 6].
 *  Positive = forward (counter-clockwise, same direction as planet progression).
 *  Negative = backward. Zero = same house.
 */
function circularDelta(from: number, to: number): number {
  if (!from || !to) return 0;
  let d = (to - from) % 12;
  if (d > 6) d -= 12;
  if (d < -6) d += 12;
  return d;
}

function deltaLabel(d: number, isHi: boolean): string {
  if (d === 0) return isHi ? 'स्थिर' : 'Same';
  const sign = d > 0 ? '+' : '';
  return `${sign}${d} ${isHi ? 'भाव' : 'h'}`;
}

function deltaColourClass(d: number): string {
  if (d === 0) return 'text-slate-500 bg-slate-100 border-slate-200';
  if (d > 3 || d < -3) return 'text-red-700 bg-red-50 border-red-200';
  if (d > 0) return 'text-emerald-700 bg-emerald-50 border-emerald-200';
  return 'text-amber-700 bg-amber-50 border-amber-200';
}

function deltaArrow(d: number): string {
  if (d === 0) return '=';
  return d > 0 ? '→' : '←';
}

export default function LalKitabDualViewTab({ apiResult }: Props) {
  const { t: _t, language } = useTranslation();
  const isHi = language === 'hi';
  const { kundliId, apiResult: ctxApiResult, fullData } = useLalKitab();

  const natalSource = apiResult || ctxApiResult;
  const currentYear = new Date().getFullYear();

  // ─── Natal advanced (for planet-state classification on the left chart) ───
  const [advanced, setAdvanced] = useState<any | null>(fullData?.advanced ?? null);
  const [advancedLoading, setAdvancedLoading] = useState(false);
  const [advancedError, setAdvancedError] = useState<string>('');

  useEffect(() => {
    if (fullData?.advanced) { setAdvanced(fullData.advanced); return; }
    if (!kundliId) return;
    let cancelled = false;
    setAdvancedLoading(true);
    setAdvancedError('');
    api.get(`/api/lalkitab/advanced/${kundliId}`)
      .then((res) => { if (!cancelled) setAdvanced(res); })
      .catch(() => { if (!cancelled) setAdvancedError(isHi ? 'तेवा डेटा लोड नहीं हो पाया।' : 'Failed to load Tewa data.'); })
      .finally(() => { if (!cancelled) setAdvancedLoading(false); });
    return () => { cancelled = true; };
  }, [kundliId, fullData?.advanced, isHi]);

  // ─── Varshphal (current year) ───
  const [varshphal, setVarshphal] = useState<any | null>(null);
  const [varshphalLoading, setVarshphalLoading] = useState(false);
  const [varshphalError, setVarshphalError] = useState<string>('');

  useEffect(() => {
    if (!kundliId) { setVarshphal(null); return; }
    let cancelled = false;
    setVarshphalLoading(true);
    setVarshphalError('');
    api.post(`/api/kundli/${kundliId}/varshphal`, { year: currentYear })
      .then((res) => { if (!cancelled) setVarshphal(res); })
      .catch(() => { if (!cancelled) setVarshphalError(isHi ? 'वर्षफल लोड नहीं हो पाया।' : 'Failed to load Varshphal.'); })
      .finally(() => { if (!cancelled) setVarshphalLoading(false); });
    return () => { cancelled = true; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [kundliId, currentYear]);

  // ─── Build the two ChartData objects ───
  const natalChart = useMemo(() => buildChartData(natalSource), [natalSource]);
  const varshphalChart = useMemo(() => buildChartData(varshphal), [varshphal]);

  // ─── Planet-state classification for colour coding (P1.1) ───
  // Applied to BOTH charts. Natal states come from /advanced. Varshphal does
  // not carry LK state data — we reuse the natal state as the visual baseline
  // so the astrologer sees the same colour on both charts for each planet.
  const planetStateTags = useMemo(() => classifyPlanetStates(advanced), [advanced]);
  const planetStates = useMemo(() => {
    const out: Record<string, PlanetStateTag> = {};
    for (const [name, tag] of Object.entries(planetStateTags)) {
      if (tag.state !== 'normal') out[name] = tag;
    }
    return out;
  }, [planetStateTags]);
  const hasAnyState = Object.keys(planetStates).length > 0;
  const statesInChart = useMemo(() => {
    const counts: Record<string, number> = {};
    for (const tag of Object.values(planetStates)) {
      counts[tag.state] = (counts[tag.state] ?? 0) + 1;
    }
    return counts;
  }, [planetStates]);

  // ─── Strength-Shift delta rows ───
  const natalHouses = useMemo(() => houseMap(natalChart), [natalChart]);
  const varshphalHouses = useMemo(() => houseMap(varshphalChart), [varshphalChart]);

  const deltaRows = useMemo(() => {
    return LK_PLANETS.map((planet) => {
      const nh = natalHouses[planet] ?? 0;
      const vh = varshphalHouses[planet] ?? 0;
      const d = circularDelta(nh, vh);
      const state = planetStateTags[planet]?.state ?? 'normal';
      return { planet, natalHouse: nh, varshphalHouse: vh, delta: d, state };
    });
  }, [natalHouses, varshphalHouses, planetStateTags]);

  // ─── Compare-hover: shared state lets the delta table highlight rows on both charts ───
  const [hoveredPlanet, setHoveredPlanet] = useState<string | null>(null);
  const [compareMode, setCompareMode] = useState(true);

  const loading = advancedLoading || varshphalLoading;

  return (
    <div className="space-y-6">
      {/* ─── Header ─── */}
      <div>
        <h2 className="text-xl font-sans font-semibold text-sacred-gold flex items-center gap-2 mb-1">
          <GitCompareArrows className="w-5 h-5" />
          {isHi ? 'तुलनात्मक दृश्य: तेवा एवं वर्षफल' : 'Comparative View: Tewa & Varshphal'}
        </h2>
        <p className="text-sm text-gray-500">
          {isHi
            ? 'मूल (जन्म) तेवा कुंडली और वर्तमान वर्षफल को साथ-साथ देखें। नीचे दी गई तालिका में प्रत्येक ग्रह का भाव-परिवर्तन (natal → varshphal) दर्शाया गया है।'
            : 'Read your natal Tewa (fixed-house) chart alongside the current-year Varshphal. The table below shows each planet\'s house shift (natal → varshphal).'}
        </p>
      </div>

      {/* ─── Compare mode toggle ─── */}
      <div className="flex items-center gap-3 flex-wrap">
        <label className="inline-flex items-center gap-2 text-sm">
          <input
            type="checkbox"
            checked={compareMode}
            onChange={(e) => setCompareMode(e.target.checked)}
            className="accent-sacred-gold"
          />
          <span className="text-sacred-gold-dark font-semibold">
            {isHi ? 'तुलना-हाइलाइट' : 'Compare highlight'}
          </span>
        </label>
        <span className="text-xs text-muted-foreground">
          {compareMode
            ? (isHi ? 'नीचे तालिका में ग्रह पर होवर करने पर दोनों चार्ट पंक्ति हाइलाइट होंगे।' : 'Hover a planet in the table below — both chart rows highlight together.')
            : (isHi ? 'हाइलाइट निष्क्रिय।' : 'Highlight disabled.')}
        </span>
      </div>

      {/* ─── Errors ─── */}
      {(advancedError || varshphalError) && (
        <div className="p-3 rounded-xl border border-red-200 bg-red-50 text-red-800 text-sm">
          {advancedError}{advancedError && varshphalError ? ' · ' : ''}{varshphalError}
        </div>
      )}

      {!kundliId && (
        <div className="p-6 text-center border border-amber-200 bg-amber-50 rounded-xl text-amber-900">
          {isHi ? 'तुलना के लिए पहले एक कुंडली लोड करें।' : 'Load a Kundli first to use the comparative view.'}
        </div>
      )}

      {/* ─── Charts side-by-side ─── */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Natal */}
        <div className="card-sacred rounded-xl border border-sacred-gold/20 p-4">
          <div className="flex items-center justify-between mb-3">
            <h3 className="font-sans font-semibold text-sacred-gold text-sm">
              {isHi ? 'मूल तेवा कुंडली' : 'Natal Tewa'}
            </h3>
            <span className="text-[10px] px-2 py-0.5 rounded-full border border-sacred-gold/30 bg-white/40 text-sacred-gold-dark font-semibold">
              {isHi ? 'जन्म' : 'Birth'}
            </span>
          </div>
          {natalChart ? (
            <div className="flex justify-center">
              <div className="w-full max-w-[340px] aspect-square">
                <InteractiveKundli
                  chartData={natalChart}
                  compact
                  hideCombust
                  planetStates={planetStates}
                />
              </div>
            </div>
          ) : (
            <div className="p-4 text-sm text-muted-foreground text-center">
              {loading ? (isHi ? 'लोड हो रहा है...' : 'Loading...') : (isHi ? 'कुंडली डेटा उपलब्ध नहीं।' : 'Natal chart data not available.')}
            </div>
          )}
        </div>

        {/* Varshphal */}
        <div className="card-sacred rounded-xl border border-sacred-gold/20 p-4">
          <div className="flex items-center justify-between mb-3">
            <h3 className="font-sans font-semibold text-sacred-gold text-sm">
              {isHi ? `वर्षफल ${currentYear}` : `Varshphal ${currentYear}`}
            </h3>
            <span className="text-[10px] px-2 py-0.5 rounded-full border border-sacred-gold/30 bg-white/40 text-sacred-gold-dark font-semibold">
              {isHi ? 'वार्षिक' : 'Annual'}
            </span>
          </div>
          {varshphalChart ? (
            <div className="flex justify-center">
              <div className="w-full max-w-[340px] aspect-square">
                <InteractiveKundli
                  chartData={varshphalChart}
                  compact
                  hideCombust
                  planetStates={planetStates}
                />
              </div>
            </div>
          ) : (
            <div className="p-4 text-sm text-muted-foreground text-center">
              {varshphalLoading ? (isHi ? 'लोड हो रहा है...' : 'Loading...') : (isHi ? 'वर्षफल डेटा उपलब्ध नहीं।' : 'Varshphal data not available.')}
            </div>
          )}
        </div>
      </div>

      {/* ─── Planet-state legend (shared across both charts) ─── */}
      {hasAnyState && (
        <div className="rounded-xl border border-sacred-gold/15 p-3">
          <p className="text-[10px] font-bold text-sacred-gold uppercase tracking-widest mb-2">
            {isHi ? 'ग्रह अवस्था रंग-संकेत (दोनों चार्ट)' : 'Planet State Legend (both charts)'}
          </p>
          <div className="flex flex-wrap gap-2">
            {legendEntries().map((entry) => {
              const count = statesInChart[entry.state] ?? 0;
              if (count === 0) return null;
              return (
                <span
                  key={entry.state}
                  className={`inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full border text-[10px] font-semibold ${entry.bgClass} ${entry.textClass} ${entry.borderClass}`}
                  title={isHi ? entry.descHi : entry.descEn}
                >
                  <span
                    className="w-2 h-2 rounded-full"
                    style={{ backgroundColor: entry.hexColour }}
                    aria-hidden="true"
                  />
                  {isHi ? entry.labelHi : entry.labelEn}
                  <span className="opacity-60">· {count}</span>
                </span>
              );
            })}
          </div>
        </div>
      )}

      {/* ─── Strength-shift delta table ─── */}
      <div className="rounded-xl border border-sacred-gold/20 bg-white">
        <div className="p-4 border-b border-sacred-gold/10">
          <h3 className="font-sans font-semibold text-sacred-gold text-sm">
            {isHi ? 'भाव-परिवर्तन तालिका (natal → varshphal)' : 'Strength Shift Table (natal → varshphal)'}
          </h3>
          <p className="text-xs text-muted-foreground mt-1">
            {isHi
              ? 'धनात्मक = ग्रह आगे बढ़ा · ऋणात्मक = पीछे लौटा · ±3 से अधिक = बड़ा परिवर्तन।'
              : 'Positive = planet moved forward · Negative = moved back · |Δ| > 3 = major shift.'}
          </p>
        </div>

        <div className="overflow-x-auto">
          <table className="table-sacred w-full text-sm">
            <thead className="bg-sacred-gold/5 text-xs uppercase tracking-wider text-sacred-gold-dark">
              <tr>
                <th className="text-left px-4 py-2 font-semibold">{isHi ? 'ग्रह' : 'Planet'}</th>
                <th className="text-center px-2 py-2 font-semibold">{isHi ? 'मूल भाव' : 'Natal'}</th>
                <th className="text-center px-2 py-2 font-semibold">{isHi ? 'वर्षफल' : 'Varshphal'}</th>
                <th className="text-center px-4 py-2 font-semibold">Δ</th>
                <th className="text-left px-4 py-2 font-semibold">{isHi ? 'अवस्था' : 'State'}</th>
              </tr>
            </thead>
            <tbody>
              {deltaRows.map((row) => {
                const tag = planetStateTags[row.planet];
                const isHovered = compareMode && hoveredPlanet === row.planet;
                const deltaCls = deltaColourClass(row.delta);
                return (
                  <tr
                    key={row.planet}
                    onMouseEnter={() => compareMode && setHoveredPlanet(row.planet)}
                    onMouseLeave={() => compareMode && setHoveredPlanet(null)}
                    className={`border-t border-sacred-gold/10 transition-colors ${
                      isHovered ? 'bg-sacred-gold/10' : 'hover:bg-sacred-gold/5'
                    }`}
                  >
                    <td className="px-4 py-2">
                      <span
                        className={`inline-flex items-center gap-1.5 px-2 py-0.5 rounded-md border text-xs font-semibold ${tag?.bgClass ?? ''} ${tag?.textClass ?? ''} ${tag?.borderClass ?? ''}`}
                        title={tag ? (isHi ? tag.descHi : tag.descEn) : ''}
                      >
                        <span
                          className="w-2 h-2 rounded-full"
                          style={{ backgroundColor: tag?.hexColour ?? '#1F2937' }}
                          aria-hidden="true"
                        />
                        {isHi ? (PLANET_HI[row.planet] ?? row.planet) : row.planet}
                      </span>
                    </td>
                    <td className="px-2 py-2 text-center font-mono text-foreground">
                      {row.natalHouse || '—'}
                    </td>
                    <td className="px-2 py-2 text-center font-mono text-foreground">
                      {row.varshphalHouse || '—'}
                    </td>
                    <td className="px-4 py-2 text-center">
                      <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full border text-[11px] font-semibold ${deltaCls}`}>
                        <span aria-hidden="true">{deltaArrow(row.delta)}</span>
                        {deltaLabel(row.delta, isHi)}
                      </span>
                    </td>
                    <td className="px-4 py-2 text-xs text-muted-foreground">
                      {tag ? (isHi ? tag.labelHi : tag.labelEn) : (isHi ? 'सामान्य' : 'Normal')}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* ─── Footnote ─── */}
      <p className="text-[11px] text-muted-foreground leading-relaxed">
        {isHi
          ? 'नोट: Δ (डेल्टा) की गणना 12-भाव चक्र पर निकटतम दिशा के अनुसार की जाती है (−6 से +6)। वर्षफल में ग्रह-अवस्था रंग मूल तेवा से ली गई हैं — यह MVP है; भविष्य में वर्षफल-विशिष्ट अवस्था-वर्गीकरण जोड़ा जाएगा।'
          : 'Note: Δ is computed as the nearest-direction shift on the 12-house cycle (−6 to +6). Planet-state colours on the Varshphal chart are inherited from the natal Tewa — this is the MVP; a future phase will add Varshphal-specific state classification.'}
      </p>
    </div>
  );
}
