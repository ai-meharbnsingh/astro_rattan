import { useMemo } from 'react';
import { Loader2 } from 'lucide-react';
import InteractiveKundli, { type PlanetData, type ChartData } from '@/components/InteractiveKundli';
import { SIGN_LORD, SIGN_ELEMENT, SIGN_TYPE } from '@/components/kundli/kundli-utils';
import { calculateJaiminiKarakas, getPlanetColor } from '@/components/kundli/jhora-utils';

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

// ─── Design Tokens ──────────────────────────────────────────────────
const BG = '#FDF8F0';
const SERIF = "'Georgia', 'Times New Roman', serif";
const BORDER_COLOR = '#D4C5A9';
const BORDER = `1px solid ${BORDER_COLOR}`;
const HEADER_BG = '#EDE8DB';
const HEADER_COLOR = '#5D4037';
const ALT_ROW = '#FAF6EE';
const MUTED = '#78716C';

// Planet color map per spec
const PLANET_COLOR_MAP: Record<string, string> = {
  Sun: '#B22222',
  Moon: '#1E3A8A',
  Mars: '#DC2626',
  Mercury: '#15803D',
  Jupiter: '#D97706',
  Venus: '#DB2777',
  Saturn: '#1E40AF',
  Rahu: '#6B7280',
  Ketu: '#78350F',
  Ascendant: '#5D4037',
  Lagna: '#5D4037',
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
  return {
    planets: transitData.transits.map((tr: any) => ({
      planet: tr.planet,
      sign: tr.current_sign || tr.sign || 'Aries',
      house: tr.house_from_moon || tr.house || 1,
      nakshatra: tr.nakshatra || '',
      sign_degree: tr.degree || 0,
      status: tr.effect || '',
    })),
  };
}

// ─── Section header ─────────────────────────────────────────────────
function SectionHeader({ children }: { children: React.ReactNode }) {
  return (
    <div style={{
      fontFamily: SERIF,
      fontSize: '10px',
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
function abbrDignity(status: string): string {
  if (!status) return '-';
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
  loadingAvakhada,
  loadingShadbala,
  loadingDivisional,
  loadingD10,
  loadingTransit,
  onBack,
  onDownloadPDF,
}: JHoraKundliViewProps) {

  const dasha = extendedDashaData || dashaData;

  // Build divisional chart data from props
  const d9ChartData = useMemo(() => buildDivisionalChartData(divisionalData), [divisionalData]);
  const d10ChartData = useMemo(() => buildDivisionalChartData(d10Data), [d10Data]);
  const transitChartData = useMemo(() => buildTransitChartData(transitData), [transitData]);

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

  // Sign abbreviation
  const signAbbr = (sign: string): string => {
    const map: Record<string, string> = {
      Aries: 'Ari', Taurus: 'Tau', Gemini: 'Gem', Cancer: 'Can',
      Leo: 'Leo', Virgo: 'Vir', Libra: 'Lib', Scorpio: 'Sco',
      Sagittarius: 'Sag', Capricorn: 'Cap', Aquarius: 'Aqu', Pisces: 'Pis',
    };
    return map[sign] || sign?.slice(0, 3) || '-';
  };

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

  // Table cell base style — tight padding for compact JHora layout
  const cellBase: React.CSSProperties = {
    fontFamily: SERIF,
    fontSize: '10px',
    padding: '2px 3px',
    borderBottom: `1px solid ${BORDER_COLOR}`,
    whiteSpace: 'nowrap',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
  };

  const cellCompact: React.CSSProperties = {
    ...cellBase,
    fontSize: '9px',
    padding: '1px 3px',
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
    fontSize: '9px',
    padding: '1px 3px',
  };

  // Chart cell label style
  const chartLabel: React.CSSProperties = {
    fontFamily: SERIF,
    fontSize: '9px',
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
      width: '100vw',
      height: '100vh',
      overflow: 'hidden',
      background: BG,
      fontFamily: SERIF,
      fontSize: '11px',
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

        {/* ── Transit (top-right) ── */}
        <div style={chartCell}>
          <div style={chartLabel}>Transit</div>
          <div style={chartInner}>
            {loadingTransit ? <MiniLoader /> : transitChartData ? (
              <InteractiveKundli chartData={transitChartData} compact />
            ) : (
              <span style={{ color: MUTED, fontSize: '10px' }}>Loading...</span>
            )}
          </div>
        </div>

        {/* ── D9 Navamsha (bottom-left) ── */}
        <div style={{ ...chartCell, borderRight: BORDER, borderBottom: 'none' }}>
          <div style={chartLabel}>D9</div>
          <div style={chartInner}>
            {loadingDivisional ? <MiniLoader /> : d9ChartData ? (
              <InteractiveKundli chartData={d9ChartData} compact />
            ) : (
              <span style={{ color: MUTED, fontSize: '10px' }}>--</span>
            )}
          </div>
        </div>

        {/* ── D10 Dashamsha (bottom-right) ── */}
        <div style={{ ...chartCell, borderBottom: 'none' }}>
          <div style={chartLabel}>D10</div>
          <div style={chartInner}>
            {loadingD10 ? <MiniLoader /> : d10ChartData ? (
              <InteractiveKundli chartData={d10ChartData} compact />
            ) : (
              <span style={{ color: MUTED, fontSize: '10px' }}>--</span>
            )}
          </div>
        </div>
      </div>

      {/* ═══════════ RIGHT: Planet Table | Dasha+Lordships | Avakhada+Karakas+Shadbala ═══════════ */}
      <div style={{
        display: 'grid',
        gridTemplateRows: '1fr 1fr 1fr',
        overflow: 'hidden',
      }}>

        {/* ── Row 1: Planet Positions Table ── */}
        <div style={{ overflow: 'hidden', borderBottom: BORDER, display: 'flex', flexDirection: 'column', minHeight: 0 }}>
          <SectionHeader>Birth Chart</SectionHeader>
          <div style={{ flex: 1, overflow: 'auto', minHeight: 0 }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr>
                  {['Planet', 'Degree', 'R/C', 'Sign', 'Mod', 'Elem', 'Nakshatra', 'Dignity', 'Karaka'].map((h) => (
                    <th key={h} style={{
                      ...thCompact,
                      textAlign: h === 'Degree' ? 'right' : h === 'R/C' || h === 'Mod' || h === 'Elem' ? 'center' : 'left',
                    }}>
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {planets.filter(p => p.planet !== 'Lagna').map((p, i) => {
                  const rc = [
                    p.is_retrograde ? 'R' : '',
                    p.is_combust ? 'C' : '',
                    p.is_vargottama ? 'V' : '',
                  ].filter(Boolean).join(',') || '-';
                  const mod = SIGN_TYPE[p.sign] || '-';
                  const modAbbr = mod === 'Moveable' ? 'Mov' : mod === 'Fixed' ? 'Fix' : mod === 'Dual' ? 'Dual' : '-';
                  const elem = SIGN_ELEMENT[p.sign] || '-';
                  const karaka = karakas[p.planet] || '-';
                  return (
                    <tr key={i} style={{ background: i % 2 === 0 ? 'transparent' : ALT_ROW }}>
                      <td style={{ ...cellCompact, color: planetColor(p.planet), fontWeight: 600 }}>
                        {p.planet}
                      </td>
                      <td style={{ ...cellCompact, textAlign: 'right' }}>
                        {fmtDegree(p.sign_degree)}
                      </td>
                      <td style={{ ...cellCompact, textAlign: 'center', color: rc.includes('R') ? '#DC2626' : rc.includes('C') ? '#D97706' : MUTED, fontWeight: rc !== '-' ? 600 : 400 }}>
                        {rc}
                      </td>
                      <td style={{ ...cellCompact }}>{signAbbr(p.sign)}</td>
                      <td style={{ ...cellCompact, textAlign: 'center' }}>{modAbbr}</td>
                      <td style={{ ...cellCompact, textAlign: 'center' }}>{elem}</td>
                      <td style={{ ...cellCompact }}>{p.nakshatra || '-'}</td>
                      <td style={{ ...cellCompact, color: statusColor(p.status), fontWeight: p.status ? 600 : 400 }}>
                        {abbrDignity(p.status)}
                      </td>
                      <td style={{ ...cellCompact, fontWeight: 600, color: karaka !== '-' ? '#5D4037' : MUTED }}>
                        {karaka}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>

        {/* ── Row 2: Vimshottari Dasha | Lordships ── */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: '50% 50%',
          overflow: 'hidden',
          borderBottom: BORDER,
        }}>
          {/* Vimshottari Dasha */}
          <div style={{ borderRight: BORDER, overflow: 'hidden', display: 'flex', flexDirection: 'column', minHeight: 0 }}>
            <SectionHeader>Vimshottari Dasha</SectionHeader>
            {loadingDasha ? <MiniLoader /> : dasha ? (
              <div style={{ flex: 1, overflow: 'auto', minHeight: 0 }}>
                <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                  <thead>
                    <tr>
                      {['Planet', 'Start', 'End', 'Yrs'].map((h) => (
                        <th key={h} style={thCompact}>{h}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {mahadashaPeriods.map((md: any, i: number) => (
                      <tr key={i} style={{
                        background: md.isCurrent ? '#FEF3C7' : (i % 2 === 0 ? 'transparent' : ALT_ROW),
                      }}>
                        <td style={{ ...cellCompact, color: planetColor(md.planet), fontWeight: 600 }}>
                          {md.planet}
                        </td>
                        <td style={cellCompact}>{md.start ? md.start.slice(0, 10) : '-'}</td>
                        <td style={cellCompact}>{md.end ? md.end.slice(0, 10) : '-'}</td>
                        <td style={{ ...cellCompact, textAlign: 'center' }}>{md.years || '-'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <div style={{ padding: '8px', color: MUTED, textAlign: 'center', fontSize: '10px' }}>--</div>
            )}
          </div>

          {/* Lordships */}
          <div style={{ overflow: 'hidden', display: 'flex', flexDirection: 'column', minHeight: 0 }}>
            <SectionHeader>Lordships</SectionHeader>
            <div style={{ flex: 1, overflow: 'auto', minHeight: 0 }}>
              <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead>
                  <tr>
                    {['H', 'Sign', 'Lord', 'In H'].map((h) => (
                      <th key={h} style={thCompact}>{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {lordships.map((l, i) => (
                    <tr key={l.houseNum} style={{ background: i % 2 === 0 ? 'transparent' : ALT_ROW }}>
                      <td style={{ ...cellCompact, textAlign: 'center', fontWeight: 600 }}>{l.houseNum}</td>
                      <td style={cellCompact}>{signAbbr(l.signName)}</td>
                      <td style={{ ...cellCompact, color: planetColor(l.lord), fontWeight: 600 }}>{l.lord}</td>
                      <td style={{ ...cellCompact, textAlign: 'center' }}>{l.lordHouse}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
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
            <SectionHeader>Avakhada Chakra</SectionHeader>
            {loadingAvakhada ? <MiniLoader /> : avakhadaData ? (
              <div style={{ flex: 1, overflow: 'auto', minHeight: 0, padding: '1px 0' }}>
                {[
                  { k: 'Ascendant/Lord', v: `${avakhadaData.ascendant || '-'}/${avakhadaData.ascendant_lord || '-'}` },
                  { k: 'Sign/Lord', v: `${avakhadaData.rashi || '-'}/${avakhadaData.rashi_lord || '-'}` },
                  { k: 'Nakshatra/Pada', v: avakhadaData.nakshatra ? `${avakhadaData.nakshatra}/${avakhadaData.nakshatra_pada}` : '-' },
                  { k: 'Yoga/Karana', v: `${avakhadaData.yoga || '-'}/${avakhadaData.karana || '-'}` },
                  { k: 'Yoni/Gana', v: `${avakhadaData.yoni || '-'}/${avakhadaData.gana || '-'}` },
                  { k: 'Nadi/Varna', v: avakhadaData.nadi || '-' },
                ].map((item) => (
                  <div key={item.k} style={{
                    display: 'flex', justifyContent: 'space-between',
                    padding: '2px 6px', borderBottom: `1px solid ${BORDER_COLOR}`,
                    fontFamily: SERIF, fontSize: '9px',
                  }}>
                    <span style={{ color: MUTED }}>{item.k}</span>
                    <span style={{ color: HEADER_COLOR, fontWeight: 600 }}>{item.v}</span>
                  </div>
                ))}
              </div>
            ) : (
              <div style={{ padding: '8px', color: MUTED, textAlign: 'center', fontSize: '10px' }}>--</div>
            )}
          </div>

          {/* Jaimini Karakas */}
          <div style={{ borderRight: BORDER, overflow: 'hidden', display: 'flex', flexDirection: 'column', minHeight: 0 }}>
            <SectionHeader>Jaimini Karakas</SectionHeader>
            <div style={{ flex: 1, overflow: 'auto', minHeight: 0 }}>
              <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead>
                  <tr>
                    <th style={thCompact}>Karaka</th>
                    <th style={thCompact}>Planet</th>
                  </tr>
                </thead>
                <tbody>
                  {['AK', 'AmK', 'BK', 'MK', 'PiK', 'GnK', 'DK'].map((k, i) => {
                    const planet = Object.entries(karakas).find(([, v]) => v === k)?.[0] || '-';
                    const karakaNames: Record<string, string> = {
                      AK: 'Atma', AmK: 'Amatya', BK: 'Bhratri', MK: 'Matri',
                      PiK: 'Pitri', GnK: 'Gnati', DK: 'Dara',
                    };
                    return (
                      <tr key={k} style={{ background: i % 2 === 0 ? 'transparent' : ALT_ROW }}>
                        <td style={{ ...cellCompact, fontWeight: 600 }}>{k} ({karakaNames[k]})</td>
                        <td style={{ ...cellCompact, color: planetColor(planet), fontWeight: 600 }}>{planet}</td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>

          {/* Shadbala */}
          <div style={{ overflow: 'hidden', display: 'flex', flexDirection: 'column', minHeight: 0 }}>
            <SectionHeader>Shadbala</SectionHeader>
            {loadingShadbala ? <MiniLoader /> : shadbalaData?.planets ? (
              <div style={{ flex: 1, overflow: 'auto', minHeight: 0, padding: '2px 6px' }}>
                {['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'].map((planet) => {
                  const data = shadbalaData.planets[planet];
                  if (!data) return null;
                  const ratio = data.total / data.required;
                  const pct = Math.min(ratio * 100, 100);
                  return (
                    <div key={planet} style={{
                      display: 'flex', alignItems: 'center', gap: '4px',
                      padding: '2px 0', fontFamily: SERIF, fontSize: '10px',
                    }}>
                      <span style={{ width: '42px', flexShrink: 0, color: planetColor(planet), fontWeight: 600 }}>
                        {planet}
                      </span>
                      <div style={{ flex: 1, height: '10px', background: '#E8E0D0', borderRadius: '2px', overflow: 'hidden' }}>
                        <div style={{ height: '100%', width: `${pct}%`, background: '#4CAF50', borderRadius: '2px' }} />
                      </div>
                      <span style={{ width: '30px', flexShrink: 0, textAlign: 'right', color: ratio >= 1 ? '#4CAF50' : '#DC2626', fontWeight: 600 }}>
                        {ratio.toFixed(2)}
                      </span>
                    </div>
                  );
                })}
              </div>
            ) : (
              <div style={{ padding: '8px', color: MUTED, textAlign: 'center', fontSize: '10px' }}>--</div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
