import { useMemo, useState, useCallback, useEffect } from 'react';
import { Loader2 } from 'lucide-react';
import InteractiveKundli, { type PlanetData, type ChartData } from '@/components/InteractiveKundli';
import { SIGN_LORD, SIGN_ELEMENT, SIGN_TYPE } from '@/components/kundli/kundli-utils';
import { calculateJaiminiKarakas, getPlanetColor } from '@/components/kundli/jhora-utils';
import { api, formatDate } from '@/lib/api';
import { useTranslation } from '@/lib/i18n';
import { translatePlanet, translateSign, translateNakshatra, translateBackend, translateSignAbbr, translatePlanetAbbr } from '@/lib/backend-translations';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell, TableCaption, TableFooter } from '@/components/ui/table';

// Available divisional charts
const DIVISIONAL_OPTIONS_EN = [
  { value: 'D1', label: 'D1 Rashi' },
  { value: 'Moon', label: 'Moon Chart' },
  { value: 'D2', label: 'D2 Hora' },
  { value: 'D3', label: 'D3 Drekkana' },
  { value: 'D4', label: 'D4 Chaturthamsha' },
  { value: 'D7', label: 'D7 Saptamsha' },
  { value: 'D9', label: 'D9 Navamsha' },
  { value: 'D10', label: 'D10 Dashamsha' },
  { value: 'D12', label: 'D12 Dwadashamsha' },
  { value: 'D16', label: 'D16 Shodashamsha' },
  { value: 'D20', label: 'D20 Vimshamsha' },
  { value: 'D24', label: 'D24 Chaturvimshamsha' },
  { value: 'D27', label: 'D27 Bhamsha' },
  { value: 'D30', label: 'D30 Trimshamsha' },
  { value: 'D40', label: 'D40 Khavedamsha' },
  { value: 'D45', label: 'D45 Akshavedamsha' },
  { value: 'D60', label: 'D60 Shashtiamsha' },
];

const DIVISIONAL_OPTIONS_HI = [
  { value: 'D1', label: 'D1 राशि' },
  { value: 'Moon', label: 'चंद्र चार्ट' },
  { value: 'D2', label: 'D2 होरा' },
  { value: 'D3', label: 'D3 द्रेक्काण' },
  { value: 'D4', label: 'D4 चतुर्थांश' },
  { value: 'D7', label: 'D7 सप्तांश' },
  { value: 'D9', label: 'D9 नवांश' },
  { value: 'D10', label: 'D10 दशांश' },
  { value: 'D12', label: 'D12 द्वादशांश' },
  { value: 'D16', label: 'D16 षोडशांश' },
  { value: 'D20', label: 'D20 विंशांश' },
  { value: 'D24', label: 'D24 चतुर्विंशांश' },
  { value: 'D27', label: 'D27 भांश' },
  { value: 'D30', label: 'D30 त्रिंशांश' },
  { value: 'D40', label: 'D40 खवेदांश' },
  { value: 'D45', label: 'D45 अक्षवेदांश' },
  { value: 'D60', label: 'D60 षष्ट्यंश' },
];

interface JHoraKundliViewProps {
  result: any;
  planets: PlanetData[];
  dashaData: any;
  extendedDashaData: any;
  avakhadaData: any;
  yogaDoshaData?: any;
  ashtakvargaData?: any;
  shadbalaData: any;
  divisionalData: any;
  d10Data: any;
  transitData: any;
  loadingDasha: boolean;
  loadingExtendedDasha?: boolean;
  loadingAvakhada: boolean;
  loadingYogaDosha?: boolean;
  loadingAshtakvarga?: boolean;
  loadingShadbala: boolean;
  loadingDivisional: boolean;
  loadingD10: boolean;
  loadingTransit: boolean;
  onBack: () => void;
  onDownloadPDF: () => void;
}

// ─── Design Tokens (single source of truth — change here only) ──────
const BG = '#FDF8F0';
const SERIF = "'Georgia', 'Times New Roman', serif";
const FONT_SIZE = '14px';          // base font size for all tables/text (minimum 12px for readability)
const TEXT_COLOR = '#3E2723';      // dark brown — readable on cream bg
const BORDER_COLOR = '#D4C5A9';
const BORDER = `1px solid ${BORDER_COLOR}`;
const HEADER_BG = '#EDE8DB';
const HEADER_COLOR = 'var(--aged-gold)';
const ALT_ROW = '#FAF6EE';
const MUTED = '#5D4037';           // secondary text — labels, dates

// Planet color map per spec
const PLANET_COLOR_MAP: Record<string, string> = {
  Sun: '#B22222',
  Moon: '#1E3A8A',
  Mars: '#DC2626',
  Mercury: '#15803D',
  Jupiter: '#D97706',
  Venus: '#DB2777',
  Saturn: '#1E40AF',
  Rahu: '#4A4A5A',
  Ketu: '#78350F',
  Ascendant: 'var(--aged-gold)',
  Lagna: 'var(--aged-gold)',
};

function planetColor(planet: string): string {
  return PLANET_COLOR_MAP[planet] || getPlanetColor(planet) || '#666';
}

const ZODIAC_SIGNS = [
  'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
  'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces',
];

// ─── Helper: build ChartData from divisional API response ───────────
function buildDivisionalChartData(data: any): ChartData | null {
  if (!data?.planet_positions) return null;
  return {
    planets: data.planet_positions.map((p: any) => ({
      planet: p.planet,
      sign: p.sign,
      house: p.house,
      nakshatra: p.nakshatra || '',
      sign_degree: p.sign_degree || 0,
      status: '',
    })),
    houses: Array.from({ length: 12 }, (_, i) => ({
      number: i + 1,
      sign: ZODIAC_SIGNS[i],
    })),
  };
}

// ─── Helper: build ChartData from transit API response ──────────────
function buildTransitChartData(transitData: any): ChartData | null {
  if (!transitData?.transits) return null;
  const asc = transitData.chart_data?.ascendant;
  let houses = transitData.chart_data?.houses;
  // Generate houses from ascendant if API didn't return them
  if (!houses && asc?.sign) {
    const ascIdx = ZODIAC_SIGNS.indexOf(asc.sign);
    if (ascIdx >= 0) {
      houses = Array.from({ length: 12 }, (_, i) => ({
        number: i + 1,
        sign: ZODIAC_SIGNS[(ascIdx + i) % 12],
      }));
    }
  }
  return {
    planets: transitData.transits.map((tr: any) => ({
      planet: tr.planet,
      sign: tr.current_sign || tr.sign || 'Aries',
      house: tr.house || 1,
      nakshatra: tr.nakshatra || '',
      sign_degree: tr.sign_degree || tr.degree || 0,
      status: tr.is_retrograde ? 'Retrograde' : (tr.effect || ''),
    })),
    houses,
    ascendant: asc,
  };
}

// ─── Section header ─────────────────────────────────────────────────
function SectionHeader({ children }: { children: React.ReactNode }) {
  return (
    <div style={{
      fontFamily: SERIF,
      fontSize: FONT_SIZE,
      fontWeight: 600,
      color: HEADER_COLOR,
      padding: '2px 6px',
      borderBottom: BORDER,
      background: HEADER_BG,
      whiteSpace: 'nowrap',
      overflow: 'hidden',
      textOverflow: 'ellipsis',
      flexShrink: 0,
    }}>
      {children}
    </div>
  );
}

// ─── Loading spinner ────────────────────────────────────────────────
function MiniLoader() {
  return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '16px 0' }}>
      <Loader2 className="w-4 h-4 animate-spin" style={{ color: HEADER_COLOR }} />
    </div>
  );
}

// ─── Status color helper ────────────────────────────────────────────
function statusColor(status: string): string {
  if (!status) return MUTED;
  const s = status.toLowerCase();
  if (s.includes('exalted') || s.includes('own')) return '#15803D';
  if (s.includes('debilitated')) return '#DC2626';
  return MUTED;
}

// ─── Degree formatter ───────────────────────────────────────────────
function fmtDegree(deg: number | undefined): string {
  if (deg === undefined || deg === null) return '-';
  return `${deg.toFixed(1)}\u00B0`;
}

// ─── Abbreviate dignity status ──────────────────────────────────────
function abbrDignity(status: string, lang?: string): string {
  if (!status) return '-';
  if (lang === 'hi') {
    return status
      .replace('Debilitated', 'नीच')
      .replace('Exalted', 'उच्च')
      .replace('Own Sign', 'स्व')
      .replace('Retrograde', 'व')
      .replace('Combust', 'अस्त')
      .replace('Vargottama', 'वर्गो')
      .replace('Neutral', '-');
  }
  return status
    .replace('Debilitated', 'Deb')
    .replace('Exalted', 'Exl')
    .replace('Own Sign', 'Own')
    .replace('Retrograde', 'R')
    .replace('Combust', 'C')
    .replace('Vargottama', 'Varg')
    .replace('Neutral', '-');
}

// ─── Main Component ─────────────────────────────────────────────────
export default function JHoraKundliView({
  result,
  planets,
  dashaData,
  extendedDashaData,
  avakhadaData,
  shadbalaData,
  divisionalData,
  d10Data,
  transitData,
  loadingDasha,
  loadingExtendedDasha,
  loadingAvakhada,
  loadingShadbala,
  loadingDivisional,
  loadingD10,
  loadingTransit,
  onBack,
  onDownloadPDF,
}: JHoraKundliViewProps) {
  void onBack;
  void onDownloadPDF;

  const { t, language } = useTranslation();
  const DIVISIONAL_OPTIONS = language === 'hi' ? DIVISIONAL_OPTIONS_HI : DIVISIONAL_OPTIONS_EN;
  const dasha = extendedDashaData || dashaData;
  const [expandedMD, setExpandedMD] = useState<string | null>(null);
  const [expandedAD, setExpandedAD] = useState<string | null>(null);

  // Transit chart data
  const transitChartData = useMemo(() => buildTransitChartData(transitData), [transitData]);
  const [gocharShift, setGocharShift] = useState(0);

  // Divisional chart dropdown state + cache
  const [leftChart, setLeftChart] = useState('D9');
  const [rightChart, setRightChart] = useState('D10');
  const [divCache, setDivCache] = useState<Record<string, any>>({});
  const [divLoading, setDivLoading] = useState<Record<string, boolean>>({});

  // Seed cache from props
  useEffect(() => {
    if (divisionalData) setDivCache(prev => ({ ...prev, D9: divisionalData }));
  }, [divisionalData]);
  useEffect(() => {
    if (d10Data) setDivCache(prev => ({ ...prev, D10: d10Data }));
  }, [d10Data]);

  // Build Moon Chart client-side by shifting houses so Moon's house = 1
  const moonChartData = useMemo((): ChartData | null => {
    const moonPlanet = planets.find((p) => p.planet === 'Moon');
    if (!moonPlanet) return null;
    const shift = (moonPlanet.house || 1) - 1;
    return {
      planets: planets.map((p) => ({
        ...p,
        house: ((p.house - 1 - shift + 12) % 12) + 1,
      })),
      houses: result?.chart_data?.houses
        ? result.chart_data.houses.map((h: { number: number; sign: string }) => ({
            number: ((h.number - 1 - shift + 12) % 12) + 1,
            sign: h.sign,
          }))
        : undefined,
    };
  }, [planets, result]);

  const fetchDiv = useCallback(async (chartType: string) => {
    if (chartType === 'Moon' || divCache[chartType] || divLoading[chartType] || !result?.id) return;
    setDivLoading(prev => ({ ...prev, [chartType]: true }));
    try {
      const data = await api.post(`/api/kundli/${result.id}/divisional`, { chart_type: chartType });
      setDivCache(prev => ({ ...prev, [chartType]: data }));
    } catch { /* ignored */ }
    setDivLoading(prev => ({ ...prev, [chartType]: false }));
  }, [divCache, divLoading, result?.id]);

  // Fetch when dropdown changes
  useEffect(() => { if (leftChart !== 'D9' && leftChart !== 'Moon') fetchDiv(leftChart); }, [leftChart, fetchDiv]);
  useEffect(() => { if (rightChart !== 'D10' && rightChart !== 'Moon') fetchDiv(rightChart); }, [rightChart, fetchDiv]);

  const leftChartData = useMemo(() => leftChart === 'Moon' ? moonChartData : buildDivisionalChartData(divCache[leftChart]), [divCache, leftChart, moonChartData]);
  const rightChartData = useMemo(() => rightChart === 'Moon' ? moonChartData : buildDivisionalChartData(divCache[rightChart]), [divCache, rightChart, moonChartData]);
  const leftLoading = leftChart === 'Moon' ? false : leftChart === 'D9' ? loadingDivisional : !!divLoading[leftChart];
  const rightLoading = rightChart === 'Moon' ? false : rightChart === 'D10' ? loadingD10 : !!divLoading[rightChart];

  // Lordship rows
  const lordships = useMemo(() => {
    const rows: { houseNum: number; signName: string; lord: string; lordHouse: number | string }[] = [];
    for (let i = 0; i < 12; i++) {
      const houseNum = i + 1;
      const houses = result?.chart_data?.houses;
      const houseData = Array.isArray(houses) ? houses[i] : houses?.[houseNum] || houses?.[String(houseNum)];
      const signName = typeof houseData === 'string' ? houseData : houseData?.sign || '-';
      const lord = SIGN_LORD[signName] || '-';
      const lordPlanet = planets.find((p) => p.planet === lord);
      rows.push({ houseNum, signName, lord, lordHouse: lordPlanet ? lordPlanet.house : '-' });
    }
    return rows;
  }, [result, planets]);

  // Jaimini Karakas (AK, AmK, BK, etc.)
  const karakas = useMemo(() => calculateJaiminiKarakas(planets), [planets]);

  // Mahadasha periods
  const mahadashaPeriods = useMemo(() => {
    if (!dasha) return [];
    const periods = dasha.mahadasha_periods || dasha.mahadasha || [];
    const currentMD = dasha.current_dasha;
    return periods.map((md: any) => ({
      planet: md.planet || '?',
      start: md.start_date || md.start || '',
      end: md.end_date || md.end || '',
      years: md.years || md.duration || '',
      isCurrent: md.planet === currentMD,
    }));
  }, [dasha]);

  // Table cell base style — uses design tokens for consistency
  const cellBase: React.CSSProperties = {
    fontFamily: SERIF,
    fontSize: FONT_SIZE,
    color: TEXT_COLOR,
    padding: '2px 4px',
    borderBottom: `1px solid ${BORDER_COLOR}`,
    whiteSpace: 'nowrap',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
  };

  const cellCompact: React.CSSProperties = {
    ...cellBase,
    padding: '2px 3px',
  };

  const thBase: React.CSSProperties = {
    ...cellBase,
    fontWeight: 600,
    background: HEADER_BG,
    color: HEADER_COLOR,
    borderBottom: BORDER,
  };

  const thCompact: React.CSSProperties = {
    ...thBase,
    padding: '2px 3px',
  };

  // Chart cell label style
  const chartLabel: React.CSSProperties = {
    fontFamily: SERIF,
    fontSize: FONT_SIZE,
    color: HEADER_COLOR,
    fontWeight: 600,
    textAlign: 'center' as const,
    padding: '1px 0 0 0',
    flexShrink: 0,
    lineHeight: 1,
  };

  // Chart cell wrapper style — constrains chart to fit within grid cell
  const chartCell: React.CSSProperties = {
    overflow: 'hidden',
    borderBottom: BORDER,
    padding: '2px',
    boxSizing: 'border-box',
    display: 'flex',
    flexDirection: 'column',
    minHeight: 0,
  };

  // Inner wrapper — takes remaining space after label, centers the SVG
  const chartInner: React.CSSProperties = {
    flex: 1,
    minHeight: 0,
    overflow: 'hidden',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  };

  return (
    <div style={{
      width: '100%',
      height: '100%',
      overflow: 'hidden',
      background: BG,
      fontFamily: SERIF,
      fontSize: FONT_SIZE,
      display: 'grid',
      gridTemplateColumns: '42% 58%',
      boxSizing: 'border-box',
      padding: '4px',
    }}>

      {/* ═══════════ LEFT: 2×2 chart grid (D1 | Transit / D9 | D10) ═══════════ */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: '1fr 1fr',
        gridTemplateRows: '1fr 1fr',
        overflow: 'hidden',
        borderRight: BORDER,
      }}>

        {/* ── D1 Birth Chart (top-left) ── */}
        <div style={{ ...chartCell, borderRight: BORDER }}>
          <div style={chartLabel}>D1</div>
          <div style={chartInner}>
            <InteractiveKundli
              chartData={{ planets, houses: result?.chart_data?.houses, ascendant: result?.chart_data?.ascendant } as ChartData}
              compact
            />
          </div>
        </div>

        {/* ── Transit (top-right) — clickable ── */}
        <div style={chartCell}>
          <div style={chartLabel}>{t('kundli.transit')} <span style={{ fontSize: FONT_SIZE, opacity: 0.6, fontWeight: 'normal' }}>({t('kundli.clickHouseLagan')})</span></div>
          <div style={chartInner}>
            {loadingTransit ? <MiniLoader /> : transitChartData ? (() => {
              const shift = gocharShift;
              const shiftedPlanets = transitChartData.planets.map((p: PlanetData) => ({
                ...p,
                house: shift ? ((((p.house || 1) - 1 - shift + 12) % 12) + 1) : (p.house || 1),
              }));
              const baseHouses = transitChartData.houses || transitData?.chart_data?.houses || result?.chart_data?.houses;
              const shiftedHouses = shift && baseHouses
                ? baseHouses.map((h: any) => ({ number: ((h.number - 1 - shift + 12) % 12) + 1, sign: h.sign }))
                : baseHouses;
              return (
                <InteractiveKundli
                  chartData={{ planets: shiftedPlanets, houses: shiftedHouses, ascendant: transitChartData.ascendant }}
                  compact
                  onHouseClick={(house) => {
                    const orig = shift ? ((house - 1 + shift) % 12) + 1 : house;
                    setGocharShift(orig - 1 === 0 ? 0 : orig - 1);
                  }}
                />
              );
            })() : (
              <span style={{ color: MUTED, fontSize: FONT_SIZE }}>{t('common.loading')}</span>
            )}
          </div>
          {gocharShift > 0 && (
            <button onClick={() => setGocharShift(0)} style={{ display: 'block', margin: '2px auto', fontSize: FONT_SIZE, color: HEADER_COLOR, textDecoration: 'underline', background: 'none', border: 'none', cursor: 'pointer' }}>{t('common.resetView')}</button>
          )}
        </div>

        {/* ── Bottom-left: selectable divisional chart ── */}
        <div style={{ ...chartCell, borderRight: BORDER, borderBottom: 'none' }}>
          <select
            value={leftChart}
            onChange={(e) => setLeftChart(e.target.value)}
            style={{
              ...chartLabel, background: HEADER_BG, border: 'none', cursor: 'pointer',
              borderBottom: BORDER, width: '100%', outline: 'none',
            }}
          >
            {DIVISIONAL_OPTIONS.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
          </select>
          <div style={chartInner}>
            {leftLoading ? <MiniLoader /> : leftChartData ? (
              <InteractiveKundli chartData={leftChartData} compact />
            ) : (
              <span style={{ color: MUTED, fontSize: FONT_SIZE }}>--</span>
            )}
          </div>
        </div>

        {/* ── Bottom-right: selectable divisional chart ── */}
        <div style={{ ...chartCell, borderBottom: 'none' }}>
          <select
            value={rightChart}
            onChange={(e) => setRightChart(e.target.value)}
            style={{
              ...chartLabel, background: HEADER_BG, border: 'none', cursor: 'pointer',
              borderBottom: BORDER, width: '100%', outline: 'none',
            }}
          >
            {DIVISIONAL_OPTIONS.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
          </select>
          <div style={chartInner}>
            {rightLoading ? <MiniLoader /> : rightChartData ? (
              <InteractiveKundli chartData={rightChartData} compact />
            ) : (
              <span style={{ color: MUTED, fontSize: FONT_SIZE }}>--</span>
            )}
          </div>
        </div>
      </div>

      {/* ═══════════ RIGHT: Planet Table | Dasha+Lordships | Avakhada+Karakas+Shadbala ═══════════ */}
      <div style={{
        display: 'grid',
        gridTemplateRows: '30% 38% 32%',
        overflow: 'hidden',
      }}>

        {/* ── Row 1: Planet Positions Table ── */}
        <div style={{ overflow: 'hidden', borderBottom: BORDER, display: 'flex', flexDirection: 'column', minHeight: 0 }}>
          <SectionHeader>{t('section.rashiD1')}</SectionHeader>
          <div style={{ flex: 1, overflow: 'auto', minHeight: 0 }}>
            <Table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <TableHeader>
                <TableRow>
                  {[
                    { key: 'Planet', label: t('table.planet') },
                    { key: 'Degree', label: t('table.degree') },
                    { key: 'R/C', label: t('auto.rC') },
                    { key: 'Sign', label: t('table.sign') },
                    { key: 'Mod', label: t('auto.mod') },
                    { key: 'Elem', label: t('auto.elem') },
                    { key: 'Nakshatra', label: t('table.nakshatra') },
                    { key: 'Dignity', label: t('table.dignity') },
                    { key: 'Karaka', label: t('table.karaka') },
                  ].map((h) => (
                    <TableHead key={h.key} style={{
                      ...thCompact,
                      textAlign: h.key === 'Degree' ? 'right' : h.key === 'R/C' || h.key === 'Mod' || h.key === 'Elem' ? 'center' : 'left',
                    }}>
                      {h.label}
                    </TableHead>
                  ))}
                </TableRow>
              </TableHeader>
              <TableBody>
                {planets.filter(p => p.planet !== 'Lagna').map((p, i) => {
                  const hasRetro = !!p.is_retrograde;
                  const hasCombust = !!p.is_combust;
                  const hasVarg = !!p.is_vargottama;
                  const rc = language === 'hi'
                    ? ([hasRetro ? 'व' : '', hasCombust ? 'अ' : '', hasVarg ? 'वर्' : ''].filter(Boolean).join(',') || '-')
                    : ([hasRetro ? 'R' : '', hasCombust ? 'C' : '', hasVarg ? 'V' : ''].filter(Boolean).join(',') || '-');
                  const mod = SIGN_TYPE[p.sign] || '-';
                  const modAbbr = language === 'hi'
                    ? (mod === 'Moveable' ? 'चर' : mod === 'Fixed' ? 'स्थि' : mod === 'Dual' ? 'द्वि' : '-')
                    : (mod === 'Moveable' ? 'Mov' : mod === 'Fixed' ? 'Fix' : mod === 'Dual' ? 'Dual' : '-');
                  const elemRaw = SIGN_ELEMENT[p.sign] || '-';
                  const elem = language === 'hi'
                    ? (elemRaw === 'Fire' ? 'अग्नि' : elemRaw === 'Earth' ? 'पृथ्वी' : elemRaw === 'Air' ? 'वायु' : elemRaw === 'Water' ? 'जल' : '-')
                    : elemRaw;
                  const karaka = karakas[p.planet] || '-';
                  return (
                    <TableRow key={i} style={{ background: i % 2 === 0 ? 'transparent' : ALT_ROW }}>
                      <TableCell style={{ ...cellCompact, color: planetColor(p.planet), fontWeight: 600 }}>
                        {translatePlanet(p.planet, language)}
                      </TableCell>
                      <TableCell style={{ ...cellCompact, textAlign: 'right' }}>
                        {fmtDegree(p.sign_degree)}
                      </TableCell>
                      <TableCell style={{ ...cellCompact, textAlign: 'center', color: hasRetro ? '#DC2626' : hasCombust ? '#D97706' : MUTED, fontWeight: rc !== '-' ? 600 : 400 }}>
                        {rc}
                      </TableCell>
                      <TableCell style={{ ...cellCompact }}>{translateSignAbbr(p.sign, language)}</TableCell>
                      <TableCell style={{ ...cellCompact, textAlign: 'center' }}>{modAbbr}</TableCell>
                      <TableCell style={{ ...cellCompact, textAlign: 'center' }}>{elem}</TableCell>
                      <TableCell style={{ ...cellCompact }}>{translateNakshatra(p.nakshatra, language) || '-'}</TableCell>
                      <TableCell style={{ ...cellCompact, color: statusColor(p.status), fontWeight: p.status ? 600 : 400 }}>
                        {abbrDignity(p.status, language)}
                      </TableCell>
                      <TableCell style={{ ...cellCompact, fontWeight: 600, color: karaka !== '-' ? 'var(--aged-gold)' : MUTED }}>
                        {karaka}
                      </TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          </div>
        </div>

        {/* ── Row 2: Vimshottari Dasha | Lordships ── */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: '50% 50%',
          overflow: 'hidden',
          borderBottom: BORDER,
        }}>
          {/* Vimshottari Dasha — Mahadasha > Antardasha > Pratyantara */}
          <div style={{ borderRight: BORDER, overflow: 'hidden', display: 'flex', flexDirection: 'column', minHeight: 0 }}>
            <SectionHeader>{t('section.vimshottariDasha')}</SectionHeader>
            {(loadingDasha || loadingExtendedDasha) ? <MiniLoader /> : dasha ? (
              <div style={{ flex: 1, overflow: 'auto', minHeight: 0 }}>
                {/* Current Dasha Info */}
                <div style={{ padding: '3px 6px', background: '#FEF3C7', borderBottom: `1px solid ${BORDER_COLOR}`, fontSize: FONT_SIZE, fontFamily: SERIF }}>
                  <span style={{ color: HEADER_COLOR, fontWeight: 600 }}>{t('section.currentDasha')}{' '}</span>
                  <span style={{ color: 'var(--aged-gold-dim)', fontWeight: 700 }}>{translatePlanet(dasha.current_dasha, language)}</span>
                  {dasha.current_antardasha && dasha.current_antardasha !== 'Unknown' && (
                    <span style={{ color: MUTED }}> / {translatePlanet(dasha.current_antardasha, language)}</span>
                  )}
                  {dasha.current_pratyantar && dasha.current_pratyantar !== 'Unknown' && (
                    <span style={{ color: MUTED }}> / {translatePlanet(dasha.current_pratyantar, language)}</span>
                  )}
                </div>

                {/* Mahadasha list with expandable Antardasha/Pratyantar */}
                {(extendedDashaData?.mahadasha || []).length > 0 ? (
                  <div>
                    {extendedDashaData.mahadasha.map((md: any, i: number) => (
                      <div key={i}>
                        {/* Mahadasha row — clickable */}
                        <div
                          onClick={() => setExpandedMD(expandedMD === md.planet ? null : md.planet)}
                          style={{
                            display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                            padding: '2px 4px', cursor: 'pointer',
                            background: md.is_current ? '#FEF3C7' : (i % 2 === 0 ? 'transparent' : ALT_ROW),
                            borderBottom: `1px solid ${BORDER_COLOR}`,
                            fontFamily: SERIF, fontSize: FONT_SIZE,
                          }}
                        >
                          <span style={{ display: 'flex', alignItems: 'center', gap: '3px' }}>
                            <span style={{ fontSize: FONT_SIZE, color: MUTED }}>{expandedMD === md.planet ? '\u25BC' : '\u25B6'}</span>
                            <span style={{ color: planetColor(md.planet), fontWeight: 600 }}>{translatePlanet(md.planet, language)}</span>
                            {md.is_current && <span style={{ color: 'var(--aged-gold-dim)', fontSize: FONT_SIZE }}>\u2190</span>}
                          </span>
                          <span style={{ color: MUTED, fontSize: FONT_SIZE }}>
                            {formatDate(md.start)} — {formatDate(md.end)} ({md.years}{t('report.yearLabel')})
                          </span>
                        </div>

                        {/* Antardasha list (expanded) */}
                        {expandedMD === md.planet && (md.antardasha || []).map((ad: any, j: number) => (
                          <div key={j}>
                            <div
                              onClick={(e) => { e.stopPropagation(); setExpandedAD(expandedAD === `${md.planet}-${ad.planet}` ? null : `${md.planet}-${ad.planet}`); }}
                              style={{
                                display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                                padding: '1px 4px 1px 16px', cursor: ad.pratyantar?.length ? 'pointer' : 'default',
                                background: ad.is_current ? 'rgba(184,134,11,0.08)' : 'transparent',
                                borderBottom: `1px solid rgba(212,197,169,0.5)`,
                                fontFamily: SERIF, fontSize: FONT_SIZE,
                              }}
                            >
                              <span style={{ display: 'flex', alignItems: 'center', gap: '2px' }}>
                                {ad.pratyantar?.length > 0 && <span style={{ fontSize: FONT_SIZE, color: MUTED }}>{expandedAD === `${md.planet}-${ad.planet}` ? '\u25BC' : '\u25B6'}</span>}
                                <span style={{ color: planetColor(ad.planet), fontWeight: 600 }}>{translatePlanet(ad.planet, language)}</span>
                                <span style={{ color: MUTED }}> {t('auto.aD')}</span>
                                {ad.is_current && <span style={{ color: 'var(--aged-gold-dim)', fontSize: FONT_SIZE }}>*</span>}
                              </span>
                              <span style={{ color: MUTED, fontSize: FONT_SIZE }}>{formatDate(ad.start)} — {formatDate(ad.end)}</span>
                            </div>

                            {/* Pratyantara list (expanded) */}
                            {expandedAD === `${md.planet}-${ad.planet}` && (ad.pratyantar || []).map((pt: any, k: number) => (
                              <div
                                key={k}
                                style={{
                                  display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                                  padding: '1px 4px 1px 28px',
                                  background: pt.is_current ? 'rgba(184,134,11,0.05)' : 'transparent',
                                  borderBottom: `1px solid rgba(212,197,169,0.3)`,
                                  fontFamily: SERIF, fontSize: FONT_SIZE,
                                }}
                              >
                                <span>
                                  <span style={{ color: planetColor(pt.planet), fontWeight: 600 }}>{translatePlanet(pt.planet, language)}</span>
                                  <span style={{ color: MUTED }}> {t('auto.pD')}</span>
                                  {pt.is_current && <span className="text-primary">*</span>}
                                </span>
                                <span style={{ color: MUTED }}>{formatDate(pt.start)} — {formatDate(pt.end)}</span>
                              </div>
                            ))}
                          </div>
                        ))}
                      </div>
                    ))}
                  </div>
                ) : (
                  /* Fallback: simple Mahadasha table when extendedDashaData is not available */
                  <Table style={{ width: '100%', borderCollapse: 'collapse' }}>
                    <TableHeader>
                      <TableRow>
                        {[
                          { key: 'Planet', label: t('table.planet') },
                          { key: 'Start', label: t('table.start') },
                          { key: 'End', label: t('table.end') },
                          { key: 'Yrs', label: t('table.years') },
                        ].map((h) => (
                          <TableHead key={h.key} style={thCompact}>{h.label}</TableHead>
                        ))}
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {mahadashaPeriods.map((md: any, i: number) => (
                        <TableRow key={i} style={{
                          background: md.isCurrent ? '#FEF3C7' : (i % 2 === 0 ? 'transparent' : ALT_ROW),
                        }}>
                          <TableCell style={{ ...cellCompact, color: planetColor(md.planet), fontWeight: 600 }}>
                            {translatePlanet(md.planet, language)}
                          </TableCell>
                          <TableCell style={cellCompact}>{md.start ? formatDate(md.start) : '-'}</TableCell>
                          <TableCell style={cellCompact}>{md.end ? formatDate(md.end) : '-'}</TableCell>
                          <TableCell style={{ ...cellCompact, textAlign: 'center' }}>{md.years || '-'}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                )}
              </div>
            ) : (
              <div style={{ padding: '8px', color: MUTED, textAlign: 'center', fontSize: FONT_SIZE }}>--</div>
            )}
          </div>

          {/* Lordships */}
          <div style={{ overflow: 'hidden', display: 'flex', flexDirection: 'column', minHeight: 0 }}>
            <SectionHeader>{t('tab.lordships')}</SectionHeader>
            <div style={{ flex: 1, overflow: 'auto', minHeight: 0 }}>
              <Table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <TableHeader>
                  <TableRow>
                    {[
                      { key: 'H', label: t('auto.h') },
                      { key: 'Sign', label: t('table.sign') },
                      { key: 'Lord', label: t('table.lord') },
                      { key: 'In H', label: t('table.inHouse') },
                    ].map((h) => (
                      <TableHead key={h.key} style={thCompact}>{h.label}</TableHead>
                    ))}
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {lordships.map((l, i) => (
                    <TableRow key={l.houseNum} style={{ background: i % 2 === 0 ? 'transparent' : ALT_ROW }}>
                      <TableCell style={{ ...cellCompact, textAlign: 'center', fontWeight: 600 }}>{l.houseNum}</TableCell>
                      <TableCell style={cellCompact}>{translateSignAbbr(l.signName, language)}</TableCell>
                      <TableCell style={{ ...cellCompact, color: planetColor(l.lord), fontWeight: 600 }}>{translatePlanet(l.lord, language)}</TableCell>
                      <TableCell style={{ ...cellCompact, textAlign: 'center' }}>{l.lordHouse}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </div>
        </div>

        {/* ── Row 3: Avakhada Chakra | Jaimini Karakas | Shadbala ── */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: '35% 30% 35%',
          overflow: 'hidden',
        }}>
          {/* Avakhada Chakra */}
          <div style={{ borderRight: BORDER, overflow: 'hidden', display: 'flex', flexDirection: 'column', minHeight: 0 }}>
            <SectionHeader>{t('avakhada.title')}</SectionHeader>
            {loadingAvakhada ? <MiniLoader /> : avakhadaData ? (
              <div style={{ flex: 1, overflow: 'auto', minHeight: 0, padding: '1px 0' }}>
                {[
                  { k: t('avakhada.ascendantSlashLord'), v: `${translateSign(avakhadaData.ascendant || '-', language)}/${translatePlanet(avakhadaData.ascendant_lord || '-', language)}` },
                  { k: t('avakhada.signLord'), v: `${translateSign(avakhadaData.rashi || '-', language)}/${translatePlanet(avakhadaData.rashi_lord || '-', language)}` },
                  { k: t('avakhada.nakshatraPada'), v: avakhadaData.nakshatra ? `${translateNakshatra(avakhadaData.nakshatra, language)}/${avakhadaData.nakshatra_pada}` : '-' },
                  { k: t('avakhada.yogaKarana'), v: `${translateBackend(avakhadaData.yoga, language) || '-'}/${translateBackend(avakhadaData.karana, language) || '-'}` },
                  { k: t('avakhada.yoniGana'), v: `${translateBackend(avakhadaData.yoni, language) || '-'}/${translateBackend(avakhadaData.gana, language) || '-'}` },
                  { k: t('avakhada.nadiVarna'), v: `${translateBackend(avakhadaData.nadi, language) || '-'} / ${translateBackend(avakhadaData.varna, language) || '-'}` },
                ].map((item) => (
                  <div key={item.k} style={{
                    display: 'flex', justifyContent: 'space-between',
                    padding: '2px 6px', borderBottom: `1px solid ${BORDER_COLOR}`,
                    fontFamily: SERIF, fontSize: FONT_SIZE,
                  }}>
                    <span style={{ color: MUTED }}>{item.k}</span>
                    <span style={{ color: HEADER_COLOR, fontWeight: 600 }}>{item.v}</span>
                  </div>
                ))}
              </div>
            ) : (
              <div style={{ padding: '8px', color: MUTED, textAlign: 'center', fontSize: FONT_SIZE }}>--</div>
            )}
          </div>

          {/* Jaimini Karakas */}
          <div style={{ borderRight: BORDER, overflow: 'hidden', display: 'flex', flexDirection: 'column', minHeight: 0 }}>
            <SectionHeader>{t('section.jaiminiKarakas')}</SectionHeader>
            <div style={{ flex: 1, overflow: 'auto', minHeight: 0 }}>
              <Table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <TableHeader>
                  <TableRow>
                    <TableHead style={thCompact}>{t('table.karaka')}</TableHead>
                    <TableHead style={thCompact}>{t('table.planet')}</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {['AK', 'AmK', 'BK', 'MK', 'PiK', 'GnK', 'DK'].map((k, i) => {
                    const planet = Object.entries(karakas).find(([, v]) => v === k)?.[0] || '-';
                    const karakaNames: Record<string, string> = language === 'hi' ? {
                      AK: 'आत्मा', AmK: 'अमात्य', BK: 'भ्रातृ', MK: 'मातृ',
                      PiK: 'पितृ', GnK: 'ज्ञाति', DK: 'दारा',
                    } : {
                      AK: 'Atma', AmK: 'Amatya', BK: 'Bhratri', MK: 'Matri',
                      PiK: 'Pitri', GnK: 'Gnati', DK: 'Dara',
                    };
                    return (
                      <TableRow key={k} style={{ background: i % 2 === 0 ? 'transparent' : ALT_ROW }}>
                        <TableCell style={{ ...cellCompact, fontWeight: 600 }}>{k} ({karakaNames[k]})</TableCell>
                        <TableCell style={{ ...cellCompact, color: planetColor(planet), fontWeight: 600 }}>{translatePlanet(planet, language)}</TableCell>
                      </TableRow>
                    );
                  })}
                </TableBody>
              </Table>
            </div>
          </div>

          {/* Shadbala — Horizontal bar chart for readability */}
          <div style={{ overflow: 'auto', display: 'flex', flexDirection: 'column', minHeight: 0 }}>
            <SectionHeader>{t('tab.shadbala')}</SectionHeader>
            {loadingShadbala ? <MiniLoader /> : shadbalaData?.planets ? (
              <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '3px', padding: '4px 6px 2px', minHeight: 0 }}>
                {['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'].map((planet) => {
                  const data = shadbalaData.planets[planet];
                  if (!data) return null;
                  const ratio = data.total / data.required;
                  const pct = Math.min(ratio * 100, 100);
                  const isStrong = ratio >= 1;
                  return (
                    <div key={planet} style={{
                      display: 'flex', alignItems: 'center', gap: '4px',
                      fontFamily: SERIF, fontSize: FONT_SIZE,
                    }}>
                      <span style={{ color: planetColor(planet), fontWeight: 700, width: '24px', textAlign: 'right', flexShrink: 0 }}>
                        {translatePlanetAbbr(planet, language)}
                      </span>
                      <div style={{
                        flex: 1, height: '14px', background: '#E8E0D0', borderRadius: '2px', overflow: 'hidden',
                        position: 'relative',
                      }}>
                        <div style={{
                          width: `${pct}%`, height: '100%',
                          background: isStrong ? '#4CAF50' : '#DC2626',
                          borderRadius: '2px', minWidth: '2px',
                        }} />
                        {/* Required threshold line at 1.0x */}
                        <div style={{
                          position: 'absolute', left: `${Math.min((1 / Math.max(ratio, 1)) * 100, 100)}%`,
                          top: 0, bottom: 0, borderLeft: '1.5px dashed rgba(93,64,55,0.5)',
                        }} />
                      </div>
                      <span style={{ color: isStrong ? '#4CAF50' : '#DC2626', fontWeight: 600, fontSize: FONT_SIZE, width: '32px', textAlign: 'left', flexShrink: 0 }}>
                        {ratio.toFixed(1)}
                      </span>
                    </div>
                  );
                })}
              </div>
            ) : (
              <div style={{ padding: '8px', color: MUTED, textAlign: 'center', fontSize: FONT_SIZE }}>--</div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
