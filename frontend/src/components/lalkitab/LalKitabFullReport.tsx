/**
 * P2.6 — Comprehensive LK PDF Report (MVP, 10–15 pages).
 *
 * Renders the aggregated payload from GET /api/lalkitab/pdf-report/{id}
 * into a single, long printable document. Print-to-PDF is handled by
 * the browser (window.print()) — no server-side PDF engine required.
 *
 * Sections (each with a <section> tag for print page-breaks):
 *   1. Cover page
 *   2. Table of Contents
 *   3. Tewa chart + identification
 *   4. Per-planet analysis (9 planets × key fields)
 *   5. Detected Doshas
 *   6. Karmic Debts (Rins) — ranked
 *   7. Prediction Studio areas
 *   8. Remedies (full list with savdhaniyan + classification)
 *   9. Varshphal (current year)
 *  10. Sources & references
 *
 * Print CSS:
 *   - A4 page size, 2cm margins
 *   - Each <section> starts a new page via `break-before: page`
 *   - Navigation / interactive chrome is hidden via `.no-print`
 *   - Body is typeset in a serif font for readability
 */
import { useEffect, useMemo, useState } from 'react';
import { useTranslation } from '@/lib/i18n';
import { Printer, X, Loader2 } from 'lucide-react';
import { api } from '@/lib/api';
import InteractiveKundli, { type ChartData, type PlanetData } from '@/components/InteractiveKundli';
import { toLkPlanetList } from './lalkitab-core';

interface Props {
  kundliId: string;
  onClose?: () => void;
}

const ZODIAC_SIGNS = [
  'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
  'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces',
];

const PLANET_HI: Record<string, string> = {
  Sun: 'सूर्य', Moon: 'चंद्र', Mars: 'मंगल', Mercury: 'बुध',
  Jupiter: 'गुरु', Venus: 'शुक्र', Saturn: 'शनि', Rahu: 'राहु', Ketu: 'केतु',
};

function buildChartFromTewa(tewa: any): ChartData | null {
  const chart = tewa?.chart_data;
  if (!chart) return null;
  const planets: PlanetData[] = toLkPlanetList(chart.planets);
  const asc = chart.ascendant;
  const ascSign = asc?.sign || 'Aries';
  const ascIdx = Math.max(0, ZODIAC_SIGNS.indexOf(ascSign));
  const houses = Array.from({ length: 12 }, (_, i) => ({
    number: i + 1,
    // Teva (Lal Kitab Kundli) is ALWAYS Mesha Lagna (Aries in H1).
    // Sign labels (1..12) match house numbers (1..12).
    sign: ZODIAC_SIGNS[i],
  }));
  return {
    planets,
    houses,
    ascendant: asc ? { longitude: asc.longitude || 0, sign: ascSign, sign_degree: asc.sign_degree } : undefined,
  };
}

export default function LalKitabFullReport({ kundliId, onClose }: Props) {
  const { language } = useTranslation();
  const isHi = language === 'hi';

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');
  const [report, setReport] = useState<any | null>(null);

  useEffect(() => {
    if (!kundliId) return;
    let cancelled = false;
    setLoading(true);
    setError('');
    api.get(`/api/lalkitab/pdf-report/${kundliId}`)
      .then((res) => { if (!cancelled) setReport(res); })
      .catch(() => {
        if (!cancelled) {
          setError(isHi ? 'पूर्ण रिपोर्ट लोड नहीं हो पाई।' : 'Failed to load the full report.');
        }
      })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [kundliId, isHi]);

  const tewaChart = useMemo(() => buildChartFromTewa(report?.tewa), [report]);

  const handlePrint = () => {
    window.print();
  };

  if (!kundliId) {
    return null;
  }

  return (
    <div className="fixed inset-0 z-50 bg-white overflow-y-auto">
      {/* Print-mode CSS. Scoped to this component via a <style> tag so the
          rules only apply while the report is mounted. */}
      <style>{`
        @media print {
          @page {
            size: A4;
            margin: 2cm;
          }
          .no-print { display: none !important; }
          body { background: white !important; }
          .lk-report {
            color: #000 !important;
            font-family: Georgia, 'Times New Roman', serif !important;
            font-size: 11pt;
            line-height: 1.55;
          }
          .lk-report section {
            break-before: page;
            page-break-before: always;
          }
          .lk-report section:first-of-type {
            break-before: auto;
            page-break-before: auto;
          }
          .lk-report h1, .lk-report h2, .lk-report h3 {
            break-after: avoid;
            page-break-after: avoid;
          }
          .lk-report table { break-inside: avoid; page-break-inside: avoid; }
          .lk-report .avoid-break { break-inside: avoid; page-break-inside: avoid; }
        }
        .lk-report {
          font-family: Georgia, 'Times New Roman', serif;
        }
      `}</style>

      {/* Toolbar — hidden when printing */}
      <div className="no-print sticky top-0 z-10 bg-sacred-gold text-white px-6 py-3 flex items-center justify-between shadow-md">
        <div className="flex items-center gap-3">
          <h2 className="font-sans font-bold">
            {isHi ? 'लाल किताब — पूर्ण रिपोर्ट' : 'Lal Kitab — Full Report'}
          </h2>
          {loading && <Loader2 className="w-4 h-4 animate-spin" />}
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={handlePrint}
            disabled={!report || loading}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-md bg-white text-sacred-gold-dark font-semibold text-sm disabled:opacity-60 hover:bg-white/90"
          >
            <Printer className="w-4 h-4" />
            {isHi ? 'PDF के रूप में डाउनलोड करें' : 'Download as PDF'}
          </button>
          {onClose && (
            <button
              onClick={onClose}
              className="p-2 rounded-md hover:bg-white/20"
              aria-label={isHi ? 'बंद करें' : 'Close'}
            >
              <X className="w-5 h-5" />
            </button>
          )}
        </div>
      </div>

      <div className="lk-report max-w-4xl mx-auto px-6 py-8 text-foreground">
        {error && (
          <div className="no-print p-4 rounded-xl border border-red-200 bg-red-50 text-red-800 text-sm mb-4">
            {error}
          </div>
        )}

        {loading && !report && (
          <div className="text-center py-24 text-muted-foreground">
            <Loader2 className="w-8 h-8 animate-spin mx-auto mb-3 text-sacred-gold" />
            {isHi ? 'रिपोर्ट तैयार हो रही है...' : 'Preparing report...'}
          </div>
        )}

        {report && (
          <>
            {/* ═══ Section 1: Cover Page ═══ */}
            <section className="min-h-[80vh] flex flex-col items-center justify-center text-center avoid-break">
              <div className="w-20 h-20 rounded-full bg-gradient-to-br from-red-600 to-sacred-gold flex items-center justify-center mx-auto mb-6">
                <span className="text-white text-3xl font-bold">ॐ</span>
              </div>
              <h1 className="text-4xl font-bold text-sacred-gold mb-2">
                {isHi ? 'लाल किताब — पूर्ण रिपोर्ट' : 'Lal Kitab — Full Report'}
              </h1>
              <p className="text-sm text-muted-foreground italic mb-10">
                {isHi ? '(MVP संस्करण — 10–15 पृष्ठ)' : '(MVP edition — 10–15 pages)'}
              </p>
              <div className="space-y-2 mb-10">
                <p className="text-2xl font-semibold text-foreground">
                  {report.person?.person_name || (isHi ? 'नाम उपलब्ध नहीं' : 'Name not available')}
                </p>
                <p className="text-sm text-muted-foreground">
                  {isHi ? 'जन्म तिथि' : 'Date of Birth'}: {report.person?.birth_date || '—'}
                </p>
                <p className="text-sm text-muted-foreground">
                  {isHi ? 'जन्म समय' : 'Time of Birth'}: {report.person?.birth_time || '—'}
                </p>
                <p className="text-sm text-muted-foreground">
                  {isHi ? 'जन्म स्थान' : 'Place of Birth'}: {report.person?.birth_place || '—'}
                </p>
              </div>
              <p className="text-xs text-muted-foreground">
                {isHi ? 'रिपोर्ट निर्मित' : 'Report generated'}: {report.generated_at}
              </p>
              <p className="text-xs text-muted-foreground italic mt-6">
                {isHi ? 'AstroRattan — शास्त्र-आधारित लाल किताब विश्लेषण' : 'AstroRattan — Shastra-based Lal Kitab Analysis'}
              </p>
            </section>

            {/* ═══ Section 2: Table of Contents ═══ */}
            <section className="avoid-break">
              <h2 className="text-2xl font-bold text-sacred-gold mb-6 border-b-2 border-sacred-gold/30 pb-2">
                {isHi ? 'विषय-सूची' : 'Table of Contents'}
              </h2>
              <ol className="space-y-2 text-base list-decimal pl-6">
                <li>{isHi ? 'तेवा कुंडली एवं पहचान' : 'Tewa Chart & Identification'}</li>
                <li>{isHi ? 'ग्रह-वार विश्लेषण (9 ग्रह)' : 'Per-Planet Analysis (9 planets)'}</li>
                <li>{isHi ? 'लाल किताब दोष' : 'Lal Kitab Doshas'}</li>
                <li>{isHi ? 'कर्म-ऋण (Rins)' : 'Karmic Debts (Rins)'}</li>
                <li>{isHi ? 'भविष्यवाणी स्टूडियो' : 'Prediction Studio'}</li>
                <li>{isHi ? 'उपाय' : 'Remedies'}</li>
                <li>{isHi ? `वर्षफल ${report.varshphal?.year ?? ''}` : `Varshphal ${report.varshphal?.year ?? ''}`}</li>
                <li>{isHi ? 'स्रोत एवं संदर्भ' : 'Sources & References'}</li>
              </ol>
            </section>

            {/* ═══ Section 3: Tewa Chart + Identification ═══ */}
            <section>
              <h2 className="text-2xl font-bold text-sacred-gold mb-4 border-b-2 border-sacred-gold/30 pb-2">
                1. {isHi ? 'तेवा कुंडली' : 'Tewa Chart'}
              </h2>
              {tewaChart ? (
                <div className="flex justify-center mb-6 avoid-break">
                  <div className="w-full max-w-[380px] aspect-square">
                    <InteractiveKundli chartData={tewaChart} compact hideCombust />
                  </div>
                </div>
              ) : (
                <p className="text-muted-foreground italic">
                  {isHi ? 'कुंडली डेटा उपलब्ध नहीं।' : 'Chart data not available.'}
                </p>
              )}
              {report.tewa?.teva_type && (
                <div className="avoid-break">
                  <h3 className="text-lg font-semibold text-sacred-gold-dark mt-4 mb-2">
                    {isHi ? 'तेवा प्रकार' : 'Tewa Classification'}
                  </h3>
                  <p className="text-sm">
                    {isHi ? 'सक्रिय प्रकार' : 'Active types'}:{' '}
                    <span className="font-semibold">
                      {(report.tewa.teva_type?.active_types ?? []).join(', ') || (isHi ? 'कोई नहीं' : 'None')}
                    </span>
                  </p>
                </div>
              )}
            </section>

            {/* ═══ Section 4: Per-Planet Analysis ═══ */}
            <section>
              <h2 className="text-2xl font-bold text-sacred-gold mb-4 border-b-2 border-sacred-gold/30 pb-2">
                2. {isHi ? 'ग्रह-वार विश्लेषण' : 'Per-Planet Analysis'}
              </h2>
              <table className="table-sacred w-full text-sm border-collapse">
                <thead>
                  <tr className="bg-sacred-gold/10 text-sacred-gold-dark">
                    <th className="text-left px-3 py-2 border border-sacred-gold/20">{isHi ? 'ग्रह' : 'Planet'}</th>
                    <th className="text-left px-3 py-2 border border-sacred-gold/20">{isHi ? 'राशि' : 'Sign'}</th>
                    <th className="text-center px-3 py-2 border border-sacred-gold/20">{isHi ? 'भाव (LK)' : 'LK House'}</th>
                    <th className="text-left px-3 py-2 border border-sacred-gold/20">{isHi ? 'नक्षत्र' : 'Nakshatra'}</th>
                    <th className="text-center px-3 py-2 border border-sacred-gold/20">{isHi ? 'वक्री' : 'Retro'}</th>
                    <th className="text-left px-3 py-2 border border-sacred-gold/20">{isHi ? 'स्थिति' : 'Status'}</th>
                  </tr>
                </thead>
                <tbody>
                  {(report.planets || []).map((p: any) => (
                    <tr key={p.planet} className="avoid-break">
                      <td className="px-3 py-2 border border-sacred-gold/20 font-semibold">
                        {isHi ? (PLANET_HI[p.planet] ?? p.planet_hi ?? p.planet) : p.planet}
                      </td>
                      <td className="px-3 py-2 border border-sacred-gold/20">{p.sign || '—'}</td>
                      <td className="px-3 py-2 border border-sacred-gold/20 text-center">{p.lk_house || '—'}</td>
                      <td className="px-3 py-2 border border-sacred-gold/20">{p.nakshatra || '—'}</td>
                      <td className="px-3 py-2 border border-sacred-gold/20 text-center">{p.is_retrograde ? '✓' : '—'}</td>
                      <td className="px-3 py-2 border border-sacred-gold/20 text-xs">{p.status || '—'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </section>

            {/* ═══ Section 5: Doshas ═══ */}
            <section>
              <h2 className="text-2xl font-bold text-sacred-gold mb-4 border-b-2 border-sacred-gold/30 pb-2">
                3. {isHi ? 'लाल किताब दोष' : 'Lal Kitab Doshas'}
              </h2>
              {Array.isArray(report.doshas) && report.doshas.length > 0 ? (
                <div className="space-y-3">
                  {report.doshas.map((d: any, i: number) => (
                    <div key={`dosha-${i}`} className="border border-sacred-gold/20 rounded-md p-3 avoid-break">
                      <h3 className="font-semibold text-sacred-gold-dark">
                        {isHi ? (d.name_hi || d.name) : (d.name_en || d.name)}
                      </h3>
                      <p className="text-xs text-muted-foreground mt-1">
                        {isHi ? (d.description_hi || d.description) : (d.description_en || d.description) || '—'}
                      </p>
                      {d.severity && (
                        <p className="text-[11px] mt-1">
                          <span className="font-semibold">{isHi ? 'गंभीरता' : 'Severity'}:</span>{' '}
                          {isHi
                            ? ({critical:'अत्यंत गंभीर', high:'उच्च', moderate:'मध्यम', low:'निम्न', severe:'गंभीर'}[d.severity] || d.severity)
                            : d.severity.charAt(0).toUpperCase() + d.severity.slice(1)}
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-muted-foreground italic">
                  {isHi ? 'कोई सक्रिय दोष नहीं मिला।' : 'No active doshas detected.'}
                </p>
              )}
            </section>

            {/* ═══ Section 6: Karmic Debts ═══ */}
            <section>
              <h2 className="text-2xl font-bold text-sacred-gold mb-4 border-b-2 border-sacred-gold/30 pb-2">
                4. {isHi ? 'कर्म-ऋण' : 'Karmic Debts (Rins)'}
              </h2>
              {report.karmic_debts?.debts && report.karmic_debts.debts.length > 0 ? (
                <div className="space-y-3">
                  {report.karmic_debts.debts.map((d: any, i: number) => (
                    <div key={`rin-${i}`} className="border border-sacred-gold/20 rounded-md p-3 avoid-break">
                      <h3 className="font-semibold text-sacred-gold-dark">
                        {isHi ? (d.name_hi || d.rin_name_hi || d.name) : (d.name_en || d.rin_name_en || d.name)}
                      </h3>
                      {(d.reason_en || d.reason_hi || d.reason) && (
                        <p className="text-xs mt-1">
                          <span className="font-semibold">{isHi ? 'कारण' : 'Reason'}:</span>{' '}
                          {isHi ? (d.reason_hi || d.reason) : (d.reason_en || d.reason)}
                        </p>
                      )}
                      {typeof d.active === 'boolean' && (
                        <p className="text-[11px] mt-1">
                          <span className="font-semibold">{isHi ? 'स्थिति' : 'Status'}:</span>{' '}
                          {d.active ? (isHi ? 'सक्रिय' : 'Active') : (isHi ? 'निष्क्रिय' : 'Passive')}
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-muted-foreground italic">
                  {isHi ? 'कोई कर्म-ऋण नहीं मिला।' : 'No karmic debts detected.'}
                </p>
              )}
            </section>

            {/* ═══ Section 7: Prediction Studio ═══ */}
            <section>
              <h2 className="text-2xl font-bold text-sacred-gold mb-4 border-b-2 border-sacred-gold/30 pb-2">
                5. {isHi ? 'भविष्यवाणी स्टूडियो' : 'Prediction Studio'}
              </h2>
              {report.prediction_studio?.areas ? (
                <table className="table-sacred w-full text-sm border-collapse">
                  <thead>
                    <tr className="bg-sacred-gold/10 text-sacred-gold-dark">
                      <th className="text-left px-3 py-2 border border-sacred-gold/20">{isHi ? 'क्षेत्र' : 'Area'}</th>
                      <th className="text-center px-3 py-2 border border-sacred-gold/20">{isHi ? 'स्कोर' : 'Score'}</th>
                      <th className="text-left px-3 py-2 border border-sacred-gold/20">{isHi ? 'टिप्पणी' : 'Note'}</th>
                    </tr>
                  </thead>
                  <tbody>
                    {Object.entries(report.prediction_studio.areas).map(([area, info]: [string, any]) => (
                      <tr key={area} className="avoid-break">
                        <td className="px-3 py-2 border border-sacred-gold/20 font-semibold">
                          {isHi
                            ? ({career:'करियर', health:'स्वास्थ्य', wealth:'धन', marriage:'विवाह', family:'परिवार', general:'सामान्य', education:'शिक्षा', spiritual:'आध्यात्मिक'}[area] || area)
                            : area.charAt(0).toUpperCase() + area.slice(1)}
                        </td>
                        <td className="px-3 py-2 border border-sacred-gold/20 text-center font-mono">
                          {typeof info?.score === 'number' ? info.score.toFixed(2) : '—'}
                        </td>
                        <td className="px-3 py-2 border border-sacred-gold/20 text-xs">
                          {isHi ? (info?.note_hi || info?.summary_hi || info?.note || '') : (info?.note_en || info?.summary_en || info?.note || '')}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              ) : (
                <p className="text-sm text-muted-foreground italic">
                  {isHi ? 'भविष्यवाणी डेटा उपलब्ध नहीं।' : 'Prediction Studio data not available.'}
                </p>
              )}
            </section>

            {/* ═══ Section 8: Remedies ═══ */}
            <section>
              <h2 className="text-2xl font-bold text-sacred-gold mb-4 border-b-2 border-sacred-gold/30 pb-2">
                6. {isHi ? 'उपाय' : 'Remedies'}
              </h2>
              {report.remedies?.remedies && report.remedies.remedies.length > 0 ? (
                <div className="space-y-4">
                  {report.remedies.remedies.map((r: any, i: number) => (
                    <div key={`rem-${i}`} className="border border-sacred-gold/20 rounded-md p-4 avoid-break">
                      <div className="flex items-baseline justify-between mb-2">
                        <h3 className="font-semibold text-sacred-gold-dark">
                          {isHi ? (PLANET_HI[r.planet] ?? r.planet_hi ?? r.planet) : r.planet}
                          <span className="ml-2 text-xs text-muted-foreground">
                            ({isHi ? 'भाव' : 'House'} {r.lk_house} · {r.sign})
                          </span>
                        </h3>
                        {r.urgency && (
                          <span className={`text-[10px] px-2 py-0.5 rounded-full font-semibold ${
                            r.urgency === 'high' ? 'bg-red-100 text-red-700 border border-red-200' :
                            r.urgency === 'medium' ? 'bg-amber-100 text-amber-700 border border-amber-200' :
                            'bg-slate-100 text-slate-700 border border-slate-200'
                          }`}>
                            {isHi
                              ? ({high:'उच्च', medium:'मध्यम', low:'निम्न'}[r.urgency] || r.urgency)
                              : r.urgency.charAt(0).toUpperCase() + r.urgency.slice(1)}
                          </span>
                        )}
                      </div>
                      {r.classification && (
                        <p className="text-[11px] mb-1">
                          <span className="font-semibold">{isHi ? 'वर्गीकरण' : 'Classification'}:</span> {r.classification}
                        </p>
                      )}
                      {(r.problem_en || r.problem_hi) && (
                        <p className="text-xs mb-1">
                          <span className="font-semibold">{isHi ? 'समस्या' : 'Problem'}:</span>{' '}
                          {isHi ? (r.problem_hi || r.problem_en) : (r.problem_en || r.problem_hi)}
                        </p>
                      )}
                      {(r.remedy_en || r.remedy_hi) && (
                        <p className="text-sm mb-1">
                          <span className="font-semibold">{isHi ? 'उपाय' : 'Remedy'}:</span>{' '}
                          {isHi ? (r.remedy_hi || r.remedy_en) : (r.remedy_en || r.remedy_hi)}
                        </p>
                      )}
                      {(r.how_en || r.how_hi) && (
                        <p className="text-xs mb-1">
                          <span className="font-semibold">{isHi ? 'विधि' : 'Method'}:</span>{' '}
                          {isHi ? (r.how_hi || r.how_en) : (r.how_en || r.how_hi)}
                        </p>
                      )}
                      {(r.savdhaniyan_en || r.savdhaniyan_hi) && (
                        <p className="text-xs mt-2 p-2 rounded bg-amber-50 border border-amber-200 text-amber-900">
                          <span className="font-semibold">{isHi ? 'सावधानियाँ' : 'Cautions (Savdhaniyan)'}:</span>{' '}
                          {isHi ? (r.savdhaniyan_hi || r.savdhaniyan_en) : (r.savdhaniyan_en || r.savdhaniyan_hi)}
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-muted-foreground italic">
                  {isHi ? 'कोई उपाय उपलब्ध नहीं।' : 'No remedies available.'}
                </p>
              )}
            </section>

            {/* ═══ Section 9: Varshphal ═══ */}
            <section>
              <h2 className="text-2xl font-bold text-sacred-gold mb-4 border-b-2 border-sacred-gold/30 pb-2">
                7. {isHi ? `वर्षफल ${report.varshphal?.year ?? ''}` : `Varshphal ${report.varshphal?.year ?? ''}`}
              </h2>
              {report.varshphal ? (
                <div className="space-y-3 avoid-break">
                  <p className="text-sm">
                    <span className="font-semibold">{isHi ? 'सोलर रिटर्न' : 'Solar Return'}:</span>{' '}
                    {report.varshphal.solar_return?.date || '—'} {report.varshphal.solar_return?.time || ''}
                  </p>
                  <p className="text-sm">
                    <span className="font-semibold">{isHi ? 'मुनथा' : 'Muntha'}:</span>{' '}
                    {isHi ? 'भाव' : 'House'} {report.varshphal.muntha?.house ?? '—'}
                    {report.varshphal.muntha?.favorable ? (isHi ? ' (अनुकूल)' : ' (favorable)') : (isHi ? ' (सावधानी)' : ' (caution)')}
                  </p>
                  <p className="text-sm">
                    <span className="font-semibold">{isHi ? 'वर्षेश' : 'Year Lord'}:</span>{' '}
                    {report.varshphal.year_lord || '—'}
                  </p>
                  {Array.isArray(report.varshphal.mudda_dasha) && report.varshphal.mudda_dasha.length > 0 && (
                    <div>
                      <h3 className="text-lg font-semibold text-sacred-gold-dark mt-4 mb-2">
                        {isHi ? 'मुद्दा दशा' : 'Mudda Dasha'}
                      </h3>
                      <table className="table-sacred w-full text-sm border-collapse">
                        <thead>
                          <tr className="bg-sacred-gold/10 text-sacred-gold-dark">
                            <th className="text-left px-3 py-2 border border-sacred-gold/20">{isHi ? 'ग्रह' : 'Planet'}</th>
                            <th className="text-left px-3 py-2 border border-sacred-gold/20">{isHi ? 'प्रारम्भ' : 'Start'}</th>
                            <th className="text-left px-3 py-2 border border-sacred-gold/20">{isHi ? 'अंत' : 'End'}</th>
                            <th className="text-center px-3 py-2 border border-sacred-gold/20">{isHi ? 'दिन' : 'Days'}</th>
                          </tr>
                        </thead>
                        <tbody>
                          {report.varshphal.mudda_dasha.map((md: any, i: number) => (
                            <tr key={`md-${i}`} className="avoid-break">
                              <td className="px-3 py-2 border border-sacred-gold/20 font-semibold">{md.planet}</td>
                              <td className="px-3 py-2 border border-sacred-gold/20 text-xs">{md.start_date}</td>
                              <td className="px-3 py-2 border border-sacred-gold/20 text-xs">{md.end_date}</td>
                              <td className="px-3 py-2 border border-sacred-gold/20 text-center">{md.days}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  )}
                </div>
              ) : (
                <p className="text-sm text-muted-foreground italic">
                  {isHi ? 'वर्षफल डेटा उपलब्ध नहीं।' : 'Varshphal data not available.'}
                </p>
              )}
            </section>

            {/* ═══ Section 10: Sources ═══ */}
            <section>
              <h2 className="text-2xl font-bold text-sacred-gold mb-4 border-b-2 border-sacred-gold/30 pb-2">
                8. {isHi ? 'स्रोत एवं संदर्भ' : 'Sources & References'}
              </h2>
              <div className="space-y-3">
                {(report.sources || []).map((s: any, i: number) => (
                  <div key={`src-${i}`} className="border border-sacred-gold/20 rounded-md p-3 avoid-break">
                    <h3 className="font-semibold text-sacred-gold-dark">
                      <span className="text-xs font-mono text-muted-foreground mr-2">[{s.tag}]</span>
                      {isHi ? s.title_hi : s.title_en}
                    </h3>
                    <p className="text-xs text-muted-foreground mt-1">
                      {isHi ? s.summary_hi : s.summary_en}
                    </p>
                  </div>
                ))}
              </div>
            </section>

            {/* End marker */}
            <section className="avoid-break text-center py-12 text-xs text-muted-foreground italic">
              {isHi
                ? '—— रिपोर्ट समाप्त · शास्त्र के साथ-साथ अनुभवी ज्योतिषी से परामर्श अवश्य लें ——'
                : '—— End of report · Please consult a qualified astrologer alongside the shastra ——'}
            </section>
          </>
        )}
      </div>
    </div>
  );
}
