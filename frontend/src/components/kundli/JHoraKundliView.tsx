import { useMemo } from 'react';
import { Loader2 } from 'lucide-react';
import InteractiveKundli, { type PlanetData, type ChartData } from '@/components/InteractiveKundli';
import { SIGN_LORD, SIGN_ELEMENT, SIGN_TYPE, PLANET_NATURE } from '@/components/kundli/kundli-utils';
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
  divisionalData: any; // D9
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

const MONO = "'Courier New', monospace";
const F9 = { fontFamily: MONO, fontSize: '9px', lineHeight: '12px' };
const BORDER = '1px solid #999';
const THIN_BORDER = '1px solid #ccc';

const ZODIAC_SIGNS = [
  'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
  'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces',
];

// Odd signs = Male, Even = Female
function getGender(sign: string): string {
  const idx = ZODIAC_SIGNS.indexOf(sign);
  if (idx < 0) return '-';
  return (idx + 1) % 2 === 1 ? 'M' : 'F';
}

// Modality by sign number: 1,4,7,10=Mov; 2,5,8,11=Fix; 3,6,9,12=Dual
function getModality(sign: string): string {
  return SIGN_TYPE[sign] || '-';
}

// Element
function getElement(sign: string): string {
  return SIGN_ELEMENT[sign] || '-';
}

// Functional nature
function getFunctionalNature(planet: string): string {
  return PLANET_NATURE[planet] || '-';
}

// Dignity color
function getDignityColor(status: string): string {
  if (!status) return '#999';
  const s = status.toLowerCase();
  if (s.includes('exalted')) return '#2e7d32';
  if (s.includes('own')) return '#1565C0';
  if (s.includes('friend')) return '#4caf50';
  if (s.includes('debilitated')) return '#c62828';
  if (s.includes('enemy')) return '#e53935';
  return '#999';
}

// Placement assessment
function getPlacement(status: string): { label: string; color: string } {
  if (!status) return { label: '-', color: '#999' };
  const s = status.toLowerCase();
  if (s.includes('exalted') || s.includes('own') || s.includes('friend'))
    return { label: 'Good', color: '#2e7d32' };
  if (s.includes('debilitated') || s.includes('enemy'))
    return { label: 'Bad', color: '#c62828' };
  return { label: '-', color: '#999' };
}

// Planet abbreviations for compact display
const PLANET_ABBR: Record<string, string> = {
  Sun: 'Su', Moon: 'Mo', Mars: 'Ma', Mercury: 'Me', Jupiter: 'Ju',
  Venus: 'Ve', Saturn: 'Sa', Rahu: 'Ra', Ketu: 'Ke',
  Ascendant: 'As', Lagna: 'As',
};

// Build chart data from divisional response
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

// Build transit chart data
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

// Compact loading spinner
function MiniLoader() {
  return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '8px 0' }}>
      <Loader2 className="w-3 h-3 animate-spin" style={{ color: '#4a7c59' }} />
    </div>
  );
}

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

  const d9ChartData = useMemo(() => buildDivisionalChartData(divisionalData), [divisionalData]);
  const d10ChartData = useMemo(() => buildDivisionalChartData(d10Data), [d10Data]);
  const transitChartData = useMemo(() => buildTransitChartData(transitData), [transitData]);
  const jaiminiKarakas = useMemo(() => calculateJaiminiKarakas(planets), [planets]);
  const dasha = extendedDashaData || dashaData;

  // Compute Jaimini karaka reverse map: planet -> karaka name
  const karakaByPlanet = useMemo(() => {
    const m: Record<string, string> = {};
    Object.entries(jaiminiKarakas).forEach(([planet, karaka]) => {
      m[planet] = karaka;
    });
    return m;
  }, [jaiminiKarakas]);

  // Format degree as DD:MM
  const fmtDeg = (deg: number | undefined): string => {
    if (deg === undefined || deg === null) return '-';
    const d = Math.floor(deg);
    const m = Math.round((deg - d) * 60);
    return `${String(d).padStart(2, '0')}:${String(m).padStart(2, '0')}`;
  };

  // Retrograde check (simple heuristic from status)
  const isRetrograde = (p: PlanetData): string => {
    if (p.status?.toLowerCase().includes('retro')) return 'R';
    return '';
  };

  // Get short sign abbreviation
  const signAbbr = (sign: string): string => {
    const map: Record<string, string> = {
      Aries: 'Ari', Taurus: 'Tau', Gemini: 'Gem', Cancer: 'Can',
      Leo: 'Leo', Virgo: 'Vir', Libra: 'Lib', Scorpio: 'Sco',
      Sagittarius: 'Sag', Capricorn: 'Cap', Aquarius: 'Aqu', Pisces: 'Pis',
    };
    return map[sign] || sign.slice(0, 3);
  };

  // Build dasha periods for MD-AD-PD display
  const dashaPeriods = useMemo(() => {
    if (!dasha) return [];
    const periods: { label: string; date: string; isCurrent: boolean }[] = [];
    const mahadashas = dasha.mahadasha_periods || dasha.mahadasha || [];
    const currentMD = dasha.current_dasha;
    const currentAD = dasha.current_antardasha;

    for (const md of mahadashas) {
      const mdName = PLANET_ABBR[md.planet] || md.planet?.slice(0, 2) || '??';
      const isMDCurrent = md.planet === currentMD;

      // If there are antardasha sub-periods
      if (md.antardashas && Array.isArray(md.antardashas)) {
        for (const ad of md.antardashas) {
          const adName = PLANET_ABBR[ad.planet] || ad.planet?.slice(0, 2) || '??';
          const isADCurrent = isMDCurrent && ad.planet === currentAD;

          if (ad.pratyantardashas && Array.isArray(ad.pratyantardashas)) {
            for (const pd of ad.pratyantardashas) {
              const pdName = PLANET_ABBR[pd.planet] || pd.planet?.slice(0, 2) || '??';
              periods.push({
                label: `${mdName}-${adName}-${pdName}`,
                date: pd.start_date || pd.start || '',
                isCurrent: isADCurrent,
              });
            }
          } else {
            periods.push({
              label: `${mdName}-${adName}`,
              date: ad.start_date || ad.start || '',
              isCurrent: isADCurrent,
            });
          }
        }
      } else {
        periods.push({
          label: mdName,
          date: md.start_date || md.start || '',
          isCurrent: isMDCurrent,
        });
      }
    }
    return periods;
  }, [dasha]);

  // Lordship data
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

  // Cell style helper
  const cellS = (extra?: React.CSSProperties): React.CSSProperties => ({
    ...F9,
    padding: '1px 3px',
    whiteSpace: 'nowrap' as const,
    borderBottom: '1px solid #ddd',
    ...extra,
  });

  const thS = (extra?: React.CSSProperties): React.CSSProperties => ({
    ...cellS(extra),
    fontWeight: 'bold',
    background: '#f5f5f5',
    borderBottom: '1px solid #bbb',
  });

  return (
    <div style={{
      width: '100%',
      height: '100%',
      overflow: 'hidden',
      background: '#fff',
      fontFamily: MONO,
      fontSize: '9px',
      display: 'grid',
      gridTemplateRows: '48% 30% 22%',
      gridTemplateColumns: '1fr',
      boxSizing: 'border-box',
    }}>

      {/* === ROW 1 (50%): D1 Chart (35%) | Planet Table (65%) === */}
      <div style={{ display: 'grid', gridTemplateColumns: '35% 65%', overflow: 'hidden', borderBottom: BORDER }}>

        {/* D1 Birth Chart */}
        <div style={{ borderRight: BORDER, display: 'flex', alignItems: 'center', justifyContent: 'center', overflow: 'hidden' }}>
          <div style={{ width: '100%', maxWidth: '300px', padding: '4px' }}>
            <InteractiveKundli
              chartData={{ planets, houses: result?.chart_data?.houses } as ChartData}
              compact
            />
          </div>
        </div>

        {/* Planet Table with ALL columns */}
        <div style={{ overflow: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr>
                {['Planet', 'Degree', 'RC', 'Rashi', 'M/F', 'Mod', 'Elem', 'Nakshatra', 'Dignity', 'Hemmed', 'Karaka', 'Func', 'In', 'Placement'].map((h) => (
                  <th key={h} style={thS({ textAlign: h === 'Planet' || h === 'Rashi' || h === 'Nakshatra' ? 'left' : 'center' })}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {planets.map((p, i) => {
                const placement = getPlacement(p.status);
                const dignityStatus = p.status || '-';
                return (
                  <tr key={i} style={{ background: i % 2 === 0 ? '#fff' : '#fafafa' }}>
                    <td style={cellS({ color: getPlanetColor(p.planet), fontWeight: 'bold', textAlign: 'left' })}>
                      {PLANET_ABBR[p.planet] || p.planet.slice(0, 2)}
                    </td>
                    <td style={cellS({ textAlign: 'center' })}>{fmtDeg(p.sign_degree)}</td>
                    <td style={cellS({ textAlign: 'center', color: '#c62828' })}>{isRetrograde(p)}</td>
                    <td style={cellS({ textAlign: 'left' })}>{signAbbr(p.sign)}</td>
                    <td style={cellS({ textAlign: 'center' })}>{getGender(p.sign)}</td>
                    <td style={cellS({ textAlign: 'center' })}>{getModality(p.sign)?.slice(0, 3)}</td>
                    <td style={cellS({ textAlign: 'center' })}>{getElement(p.sign)?.slice(0, 4)}</td>
                    <td style={cellS({ textAlign: 'left' })}>{p.nakshatra || '-'}</td>
                    <td style={cellS({ textAlign: 'center', color: getDignityColor(dignityStatus), fontWeight: 'bold' })}>
                      {dignityStatus !== '-' && dignityStatus ? dignityStatus : '-'}
                    </td>
                    <td style={cellS({ textAlign: 'center', color: '#999' })}>-</td>
                    <td style={cellS({ textAlign: 'center', color: '#555' })}>{karakaByPlanet[p.planet] || '-'}</td>
                    <td style={cellS({ textAlign: 'center' })}>{getFunctionalNature(p.planet)?.slice(0, 3)}</td>
                    <td style={cellS({ textAlign: 'center' })}>{p.house || '-'}</td>
                    <td style={cellS({ textAlign: 'center', color: placement.color, fontWeight: 'bold' })}>{placement.label}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* === ROW 2 (30%): 3 small charts (35%) | Vimshottari (30%) | Lordships (35%) === */}
      <div style={{ display: 'grid', gridTemplateColumns: '35% 30% 35%', overflow: 'hidden', borderBottom: BORDER }}>

        {/* Three small charts side by side */}
        <div style={{ borderRight: BORDER, display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', overflow: 'hidden' }}>
          {/* Transit */}
          <div style={{ borderRight: THIN_BORDER, display: 'flex', flexDirection: 'column', alignItems: 'center', overflow: 'hidden' }}>
            <div style={{ ...F9, fontWeight: 'bold', textAlign: 'center', padding: '1px 0', borderBottom: THIN_BORDER, width: '100%' }}>Today</div>
            <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '2px' }}>
              {loadingTransit ? <MiniLoader /> : transitChartData ? (
                <div style={{ width: '100%', maxWidth: '130px' }}>
                  <InteractiveKundli chartData={transitChartData} compact />
                </div>
              ) : <span style={{ ...F9, color: '#999' }}>--</span>}
            </div>
          </div>
          {/* D9 */}
          <div style={{ borderRight: THIN_BORDER, display: 'flex', flexDirection: 'column', alignItems: 'center', overflow: 'hidden' }}>
            <div style={{ ...F9, fontWeight: 'bold', textAlign: 'center', padding: '1px 0', borderBottom: THIN_BORDER, width: '100%' }}>D9</div>
            <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '2px' }}>
              {loadingDivisional ? <MiniLoader /> : d9ChartData ? (
                <div style={{ width: '100%', maxWidth: '130px' }}>
                  <InteractiveKundli chartData={d9ChartData} compact />
                </div>
              ) : <span style={{ ...F9, color: '#999' }}>--</span>}
            </div>
          </div>
          {/* D10 */}
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', overflow: 'hidden' }}>
            <div style={{ ...F9, fontWeight: 'bold', textAlign: 'center', padding: '1px 0', borderBottom: THIN_BORDER, width: '100%' }}>D10</div>
            <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '2px' }}>
              {loadingD10 ? <MiniLoader /> : d10ChartData ? (
                <div style={{ width: '100%', maxWidth: '130px' }}>
                  <InteractiveKundli chartData={d10ChartData} compact />
                </div>
              ) : <span style={{ ...F9, color: '#999' }}>--</span>}
            </div>
          </div>
        </div>

        {/* Vimshottari Dasha (MD-AD-PD with dates) */}
        <div style={{ borderRight: BORDER, overflow: 'auto' }}>
          <div style={{ ...F9, fontWeight: 'bold', textAlign: 'center', padding: '1px 0', borderBottom: THIN_BORDER }}>Vimshottari Dasha</div>
          {loadingDasha ? <MiniLoader /> : dasha ? (
            <div style={{ padding: 0 }}>
              {dashaPeriods.length > 0 ? (
                <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                  <tbody>
                    {dashaPeriods.slice(0, 30).map((dp, i) => (
                      <tr key={i} style={{ background: dp.isCurrent ? '#fff0f0' : (i % 2 === 0 ? '#fff' : '#fafafa') }}>
                        <td style={cellS({
                          color: dp.isCurrent ? '#c62828' : '#333',
                          fontWeight: dp.isCurrent ? 'bold' : 'normal',
                        })}>{dp.label}</td>
                        <td style={cellS({
                          color: dp.isCurrent ? '#c62828' : '#555',
                          textAlign: 'right',
                        })}>{dp.date}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              ) : (
                /* Fallback: show mahadasha list */
                <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                  <tbody>
                    {(dasha.mahadasha_periods || dasha.mahadasha || []).map((p: any, i: number) => {
                      const isCurrent = p.planet === dasha.current_dasha;
                      return (
                        <tr key={i} style={{ background: isCurrent ? '#fff0f0' : (i % 2 === 0 ? '#fff' : '#fafafa') }}>
                          <td style={cellS({ color: isCurrent ? '#c62828' : getPlanetColor(p.planet), fontWeight: 'bold' })}>
                            {PLANET_ABBR[p.planet] || p.planet?.slice(0, 2)}{isCurrent ? ' *' : ''}
                          </td>
                          <td style={cellS({ color: '#555' })}>{p.start_date || p.start}</td>
                          <td style={cellS({ color: '#555' })}>{p.end_date || p.end}</td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              )}
            </div>
          ) : <span style={{ ...F9, color: '#999', display: 'block', textAlign: 'center', padding: '8px' }}>--</span>}
        </div>

        {/* Lordships */}
        <div style={{ overflow: 'auto' }}>
          <div style={{ ...F9, fontWeight: 'bold', textAlign: 'center', padding: '1px 0', borderBottom: THIN_BORDER }}>Lordships</div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', padding: 0 }}>
            {/* Left column: houses 1-6 */}
            <div style={{ borderRight: THIN_BORDER }}>
              {lordships.slice(0, 6).map((l) => (
                <div key={l.houseNum} style={{ ...F9, padding: '1px 3px', borderBottom: '1px solid #eee', display: 'flex', justifyContent: 'space-between' }}>
                  <span>Lrd.{String(l.houseNum).padStart(2, ' ')} in {l.lordHouse}</span>
                  <span style={{ color: getPlanetColor(l.lord), fontWeight: 'bold' }}>{PLANET_ABBR[l.lord] || l.lord.slice(0, 2)}</span>
                </div>
              ))}
            </div>
            {/* Right column: houses 7-12 */}
            <div>
              {lordships.slice(6, 12).map((l) => (
                <div key={l.houseNum} style={{ ...F9, padding: '1px 3px', borderBottom: '1px solid #eee', display: 'flex', justifyContent: 'space-between' }}>
                  <span>L{String(l.houseNum).padStart(2, ' ')} in {l.lordHouse}</span>
                  <span style={{ color: getPlanetColor(l.lord), fontWeight: 'bold' }}>{PLANET_ABBR[l.lord] || l.lord.slice(0, 2)}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* === ROW 3 (20%): Avakhada (25%) | Jeeva/Deha + Jaimini (25%) | Shadbala (50%) === */}
      <div style={{ display: 'grid', gridTemplateColumns: '25% 25% 50%', overflow: 'hidden' }}>

        {/* Avakhada Chakra */}
        <div style={{ borderRight: BORDER, overflow: 'auto' }}>
          <div style={{ ...F9, fontWeight: 'bold', textAlign: 'center', padding: '1px 0', borderBottom: THIN_BORDER }}>Avakhada Chakra</div>
          {loadingAvakhada ? <MiniLoader /> : avakhadaData ? (
            <div style={{ padding: 0 }}>
              {[
                { k: 'Asc', v: avakhadaData.ascendant },
                { k: 'Asc Lord', v: avakhadaData.ascendant_lord },
                { k: 'Rashi', v: avakhadaData.rashi },
                { k: 'Rashi Lord', v: avakhadaData.rashi_lord },
                { k: 'Nakshatra', v: avakhadaData.nakshatra ? `${avakhadaData.nakshatra} P${avakhadaData.nakshatra_pada}` : '-' },
                { k: 'Yoga', v: avakhadaData.yoga },
                { k: 'Karana', v: avakhadaData.karana },
                { k: 'Yoni', v: avakhadaData.yoni },
                { k: 'Gana', v: avakhadaData.gana },
                { k: 'Nadi', v: avakhadaData.nadi },
                { k: 'Varna', v: avakhadaData.varna },
                { k: 'Naamakshar', v: avakhadaData.naamakshar },
              ].map((item) => (
                <div key={item.k} style={{ ...F9, display: 'flex', justifyContent: 'space-between', padding: '0px 3px', borderBottom: '1px solid #eee' }}>
                  <span style={{ color: '#888' }}>{item.k}</span>
                  <span style={{ color: '#333', fontWeight: 500 }}>{item.v || '-'}</span>
                </div>
              ))}
            </div>
          ) : <span style={{ ...F9, color: '#999', display: 'block', textAlign: 'center', padding: '8px' }}>--</span>}
        </div>

        {/* Jeeva/Deha + Jaimini Karakas */}
        <div style={{ borderRight: BORDER, overflow: 'auto' }}>
          <div style={{ ...F9, fontWeight: 'bold', textAlign: 'center', padding: '1px 0', borderBottom: THIN_BORDER }}>Jaimini Karakas</div>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr>
                <th style={thS({ textAlign: 'left' })}>Karaka</th>
                <th style={thS({ textAlign: 'left' })}>Planet</th>
                <th style={thS({ textAlign: 'center' })}>Deg</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(jaiminiKarakas).map(([planet, karaka], i) => {
                const pData = planets.find((p) => p.planet === planet);
                return (
                  <tr key={planet} style={{ background: i % 2 === 0 ? '#fff' : '#fafafa' }}>
                    <td style={cellS({ fontWeight: 'bold', color: '#555' })}>{karaka}</td>
                    <td style={cellS({ color: getPlanetColor(planet), fontWeight: 'bold' })}>{PLANET_ABBR[planet] || planet.slice(0, 2)}</td>
                    <td style={cellS({ textAlign: 'center', color: '#777' })}>{fmtDeg(pData?.sign_degree)}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
          {/* Legend */}
          <div style={{ padding: '2px 3px', borderTop: '1px solid #ddd' }}>
            {[
              ['AK', 'Atmakaraka'],
              ['AmK', 'Amatyakaraka'],
              ['BK', 'Bhratrukaraka'],
              ['MK', 'Matrukaraka'],
              ['PiK', 'Pitrukaraka'],
              ['GnK', 'Gnatikaraka'],
              ['DK', 'Darakaraka'],
            ].map(([abbr, full]) => (
              <div key={abbr} style={{ ...F9, fontSize: '7px', color: '#aaa' }}>
                <strong>{abbr}</strong>={full}
              </div>
            ))}
          </div>
        </div>

        {/* Shadbala — horizontal green bar chart */}
        <div style={{ overflow: 'auto' }}>
          <div style={{ ...F9, fontWeight: 'bold', textAlign: 'center', padding: '1px 0', borderBottom: THIN_BORDER }}>Shadbala</div>
          {loadingShadbala ? <MiniLoader /> : shadbalaData?.planets ? (
            <div style={{ padding: '2px 4px' }}>
              {['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'].map((planet) => {
                const data = shadbalaData.planets[planet];
                if (!data) return null;
                const ratio = data.total / data.required;
                const pct = Math.min(ratio * 100, 100);
                return (
                  <div key={planet} style={{ display: 'flex', alignItems: 'center', gap: '4px', padding: '1px 0' }}>
                    <span style={{ ...F9, fontWeight: 'bold', width: '24px', flexShrink: 0, color: getPlanetColor(planet) }}>
                      {PLANET_ABBR[planet] || planet.slice(0, 2)}
                    </span>
                    <div style={{ flex: 1, height: '10px', background: '#eee', position: 'relative' }}>
                      <div style={{
                        height: '100%',
                        width: `${pct}%`,
                        background: '#4caf50',
                      }} />
                    </div>
                    <span style={{ ...F9, width: '36px', textAlign: 'right', flexShrink: 0, color: ratio >= 1 ? '#4caf50' : '#e53935' }}>
                      {ratio.toFixed(2)}
                    </span>
                  </div>
                );
              })}
            </div>
          ) : <span style={{ ...F9, color: '#999', display: 'block', textAlign: 'center', padding: '8px' }}>--</span>}
        </div>
      </div>
    </div>
  );
}
