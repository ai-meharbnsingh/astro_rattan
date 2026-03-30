import { useMemo } from 'react';
import { ArrowLeft, Download, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import InteractiveKundli, { type PlanetData, type ChartData } from '@/components/InteractiveKundli';
import { SIGN_LORD } from '@/components/kundli/kundli-utils';
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
      sign: ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'][i],
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
    <div className="flex items-center justify-center py-4">
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

  // Dasha source: prefer extendedDashaData, fall back to dashaData
  const dasha = extendedDashaData || dashaData;

  return (
    <div className="h-[calc(100vh-80px)] overflow-hidden flex flex-col" style={{ background: '#fff' }}>
      {/* Top bar — person name + actions */}
      <div className="flex items-center justify-between px-3 py-1.5 border-b" style={{ borderColor: '#ccc', background: '#f0f0f0' }}>
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="sm" onClick={onBack} className="h-6 w-6 p-0">
            <ArrowLeft className="w-3.5 h-3.5" />
          </Button>
          <span className="text-[11px] font-bold" style={{ color: '#333' }}>
            {result?.person_name}
          </span>
          <span className="text-[9px]" style={{ color: '#666' }}>
            {result?.birth_date} | {result?.birth_time} | {result?.birth_place}
          </span>
        </div>
        <Button variant="ghost" size="sm" onClick={onDownloadPDF} className="h-6 px-2 text-[9px]">
          <Download className="w-3 h-3 mr-1" />PDF
        </Button>
      </div>

      {/* Main grid — 3 rows */}
      <div className="flex-1 overflow-hidden grid" style={{
        gridTemplateRows: '1fr 1fr 1fr',
        gridTemplateColumns: '1fr',
        gap: 0,
      }}>

        {/* === ROW 1: D1 Chart | Planet Table | Lordships === */}
        <div className="grid overflow-hidden" style={{
          gridTemplateColumns: '30% 40% 30%',
          borderBottom: '1px solid #ccc',
        }}>
          {/* D1 Chart */}
          <div className="overflow-hidden border-r" style={{ borderColor: '#ccc' }}>
            <div className="text-[9px] font-bold text-center py-0.5" style={{ background: '#e8f5e9', color: '#2e7d32', borderBottom: '1px solid #ccc' }}>
              Rashi (D1)
            </div>
            <div className="flex items-center justify-center p-1 h-[calc(100%-20px)]">
              <div style={{ maxWidth: '220px', width: '100%' }}>
                <InteractiveKundli
                  chartData={{ planets, houses: result?.chart_data?.houses } as ChartData}
                  compact
                />
              </div>
            </div>
          </div>

          {/* Planet Table */}
          <div className="overflow-auto border-r" style={{ borderColor: '#ccc' }}>
            <div className="text-[9px] font-bold text-center py-0.5 sticky top-0 z-10" style={{ background: '#e8f5e9', color: '#2e7d32', borderBottom: '1px solid #ccc' }}>
              Planet Positions
            </div>
            <table className="w-full text-[9px]" style={{ borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ background: '#f5f5f5' }}>
                  <th className="text-left px-1 py-0.5 font-semibold" style={{ borderBottom: '1px solid #ddd' }}>Planet</th>
                  <th className="text-left px-1 py-0.5 font-semibold" style={{ borderBottom: '1px solid #ddd' }}>Sign</th>
                  <th className="text-center px-1 py-0.5 font-semibold" style={{ borderBottom: '1px solid #ddd' }}>H</th>
                  <th className="text-center px-1 py-0.5 font-semibold" style={{ borderBottom: '1px solid #ddd' }}>Deg</th>
                  <th className="text-left px-1 py-0.5 font-semibold" style={{ borderBottom: '1px solid #ddd' }}>Nak</th>
                  <th className="text-center px-1 py-0.5 font-semibold" style={{ borderBottom: '1px solid #ddd' }}>Status</th>
                </tr>
              </thead>
              <tbody>
                {planets.map((p, i) => (
                  <tr key={i} style={{ borderBottom: '1px solid #eee' }}>
                    <td className="px-1 py-0.5 font-medium" style={{ color: getPlanetColor(p.planet) }}>{p.planet}</td>
                    <td className="px-1 py-0.5" style={{ color: '#333' }}>{p.sign}</td>
                    <td className="px-1 py-0.5 text-center" style={{ color: '#333' }}>{p.house}</td>
                    <td className="px-1 py-0.5 text-center" style={{ color: '#555' }}>{p.sign_degree?.toFixed(1)}&deg;</td>
                    <td className="px-1 py-0.5" style={{ color: '#555' }}>{p.nakshatra || '\u2014'}</td>
                    <td className="px-1 py-0.5 text-center">
                      {(p.status === 'Exalted' || p.status === 'Own Sign') ? (
                        <span className="text-[8px] px-0.5 rounded" style={{ background: '#c8e6c9', color: '#2e7d32' }}>{p.status}</span>
                      ) : p.status === 'Debilitated' ? (
                        <span className="text-[8px] px-0.5 rounded" style={{ background: '#ffcdd2', color: '#c62828' }}>{p.status}</span>
                      ) : (
                        <span className="text-[8px]" style={{ color: '#999' }}>{p.status || '\u2014'}</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Lordships */}
          <div className="overflow-auto">
            <div className="text-[9px] font-bold text-center py-0.5 sticky top-0 z-10" style={{ background: '#e8f5e9', color: '#2e7d32', borderBottom: '1px solid #ccc' }}>
              House Lordships
            </div>
            <table className="w-full text-[9px]" style={{ borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ background: '#f5f5f5' }}>
                  <th className="text-center px-1 py-0.5 font-semibold" style={{ borderBottom: '1px solid #ddd' }}>H</th>
                  <th className="text-left px-1 py-0.5 font-semibold" style={{ borderBottom: '1px solid #ddd' }}>Sign</th>
                  <th className="text-left px-1 py-0.5 font-semibold" style={{ borderBottom: '1px solid #ddd' }}>Lord</th>
                  <th className="text-center px-1 py-0.5 font-semibold" style={{ borderBottom: '1px solid #ddd' }}>In H</th>
                </tr>
              </thead>
              <tbody>
                {Array.from({ length: 12 }, (_, i) => {
                  const houseNum = i + 1;
                  const houses = result?.chart_data?.houses;
                  const houseData = Array.isArray(houses) ? houses[i] : houses?.[houseNum] || houses?.[String(houseNum)];
                  const signName = typeof houseData === 'string' ? houseData : houseData?.sign || '\u2014';
                  const lord = SIGN_LORD[signName] || '\u2014';
                  const lordPlanet = planets.find((p) => p.planet === lord);
                  return (
                    <tr key={houseNum} style={{ borderBottom: '1px solid #eee', background: houseNum % 2 === 0 ? '#fafafa' : '#fff' }}>
                      <td className="px-1 py-0.5 text-center font-medium" style={{ color: '#333' }}>{houseNum}</td>
                      <td className="px-1 py-0.5" style={{ color: '#555' }}>{signName}</td>
                      <td className="px-1 py-0.5 font-medium" style={{ color: getPlanetColor(lord) }}>{lord}</td>
                      <td className="px-1 py-0.5 text-center" style={{ color: '#555' }}>{lordPlanet ? lordPlanet.house : '\u2014'}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>

        {/* === ROW 2: D10 | D9 | Vimshottari Dasha === */}
        <div className="grid overflow-hidden" style={{
          gridTemplateColumns: '25% 25% 50%',
          borderBottom: '1px solid #ccc',
        }}>
          {/* D10 Chart */}
          <div className="overflow-hidden border-r" style={{ borderColor: '#ccc' }}>
            <div className="text-[9px] font-bold text-center py-0.5" style={{ background: '#e8f5e9', color: '#2e7d32', borderBottom: '1px solid #ccc' }}>
              Dashamsha (D10)
            </div>
            <div className="flex items-center justify-center p-1 h-[calc(100%-20px)]">
              {loadingD10 ? <MiniLoader /> : d10ChartData ? (
                <div style={{ maxWidth: '180px', width: '100%' }}>
                  <InteractiveKundli chartData={d10ChartData} compact />
                </div>
              ) : (
                <span className="text-[8px]" style={{ color: '#999' }}>Loading...</span>
              )}
            </div>
          </div>

          {/* D9 Chart */}
          <div className="overflow-hidden border-r" style={{ borderColor: '#ccc' }}>
            <div className="text-[9px] font-bold text-center py-0.5" style={{ background: '#e8f5e9', color: '#2e7d32', borderBottom: '1px solid #ccc' }}>
              Navamsha (D9)
            </div>
            <div className="flex items-center justify-center p-1 h-[calc(100%-20px)]">
              {loadingDivisional ? <MiniLoader /> : d9ChartData ? (
                <div style={{ maxWidth: '180px', width: '100%' }}>
                  <InteractiveKundli chartData={d9ChartData} compact />
                </div>
              ) : (
                <span className="text-[8px]" style={{ color: '#999' }}>Loading...</span>
              )}
            </div>
          </div>

          {/* Vimshottari Dasha */}
          <div className="overflow-auto">
            <div className="text-[9px] font-bold text-center py-0.5 sticky top-0 z-10" style={{ background: '#e8f5e9', color: '#2e7d32', borderBottom: '1px solid #ccc' }}>
              Vimshottari Dasha
            </div>
            {loadingDasha ? <MiniLoader /> : dasha ? (
              <div>
                {/* Current period highlight */}
                <div className="px-2 py-1" style={{ background: '#fffde7', borderBottom: '1px solid #ddd' }}>
                  <span className="text-[9px] font-bold" style={{ color: '#e65100' }}>
                    Current: {dasha.current_dasha}
                  </span>
                  {dasha.current_antardasha && (
                    <span className="text-[8px] ml-1" style={{ color: '#666' }}>
                      / AD: {dasha.current_antardasha}
                    </span>
                  )}
                </div>
                <table className="w-full text-[9px]" style={{ borderCollapse: 'collapse' }}>
                  <thead>
                    <tr style={{ background: '#f5f5f5' }}>
                      <th className="text-left px-1 py-0.5 font-semibold" style={{ borderBottom: '1px solid #ddd' }}>Planet</th>
                      <th className="text-left px-1 py-0.5 font-semibold" style={{ borderBottom: '1px solid #ddd' }}>Start</th>
                      <th className="text-left px-1 py-0.5 font-semibold" style={{ borderBottom: '1px solid #ddd' }}>End</th>
                      <th className="text-center px-1 py-0.5 font-semibold" style={{ borderBottom: '1px solid #ddd' }}>Yrs</th>
                    </tr>
                  </thead>
                  <tbody>
                    {(dasha.mahadasha_periods || dasha.mahadasha || []).map((p: any) => {
                      const planetName = p.planet;
                      const isCurrent = planetName === dasha.current_dasha;
                      return (
                        <tr key={planetName} style={{
                          borderBottom: '1px solid #eee',
                          background: isCurrent ? '#fff9c4' : undefined,
                        }}>
                          <td className="px-1 py-0.5 font-medium" style={{ color: getPlanetColor(planetName) }}>
                            {planetName}{isCurrent ? ' \u2190' : ''}
                          </td>
                          <td className="px-1 py-0.5" style={{ color: '#555' }}>{p.start_date || p.start}</td>
                          <td className="px-1 py-0.5" style={{ color: '#555' }}>{p.end_date || p.end}</td>
                          <td className="px-1 py-0.5 text-center" style={{ color: '#555' }}>{p.years}</td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            ) : (
              <span className="text-[8px] block text-center py-4" style={{ color: '#999' }}>Loading...</span>
            )}
          </div>
        </div>

        {/* === ROW 3: Transit | Avakhada | Jaimini Karakas | Shadbala === */}
        <div className="grid overflow-hidden" style={{
          gridTemplateColumns: '25% 25% 25% 25%',
        }}>
          {/* Transit Chart */}
          <div className="overflow-hidden border-r" style={{ borderColor: '#ccc' }}>
            <div className="text-[9px] font-bold text-center py-0.5" style={{ background: '#e8f5e9', color: '#2e7d32', borderBottom: '1px solid #ccc' }}>
              Gochar (Transit)
            </div>
            <div className="flex items-center justify-center p-1 h-[calc(100%-20px)]">
              {loadingTransit ? <MiniLoader /> : transitChartData ? (
                <div style={{ maxWidth: '160px', width: '100%' }}>
                  <InteractiveKundli chartData={transitChartData} compact />
                </div>
              ) : (
                <span className="text-[8px]" style={{ color: '#999' }}>Loading...</span>
              )}
            </div>
          </div>

          {/* Avakhada Chakra */}
          <div className="overflow-auto border-r" style={{ borderColor: '#ccc' }}>
            <div className="text-[9px] font-bold text-center py-0.5 sticky top-0 z-10" style={{ background: '#e8f5e9', color: '#2e7d32', borderBottom: '1px solid #ccc' }}>
              Avakhada Chakra
            </div>
            {loadingAvakhada ? <MiniLoader /> : avakhadaData ? (
              <div className="px-1 py-0.5">
                {[
                  { k: 'Asc', v: avakhadaData.ascendant },
                  { k: 'Asc Lord', v: avakhadaData.ascendant_lord },
                  { k: 'Rashi', v: avakhadaData.rashi },
                  { k: 'Rashi Lord', v: avakhadaData.rashi_lord },
                  { k: 'Nakshatra', v: avakhadaData.nakshatra ? `${avakhadaData.nakshatra} P${avakhadaData.nakshatra_pada}` : '\u2014' },
                  { k: 'Yoga', v: avakhadaData.yoga },
                  { k: 'Karana', v: avakhadaData.karana },
                  { k: 'Yoni', v: avakhadaData.yoni },
                  { k: 'Gana', v: avakhadaData.gana },
                  { k: 'Nadi', v: avakhadaData.nadi },
                  { k: 'Varna', v: avakhadaData.varna },
                  { k: 'Naamakshar', v: avakhadaData.naamakshar },
                ].map((item) => (
                  <div key={item.k} className="flex justify-between py-px" style={{ borderBottom: '1px solid #f0f0f0' }}>
                    <span className="text-[8px]" style={{ color: '#888' }}>{item.k}</span>
                    <span className="text-[8px] font-medium" style={{ color: '#333' }}>{item.v || '\u2014'}</span>
                  </div>
                ))}
              </div>
            ) : (
              <span className="text-[8px] block text-center py-4" style={{ color: '#999' }}>Loading...</span>
            )}
          </div>

          {/* Jaimini Karakas */}
          <div className="overflow-auto border-r" style={{ borderColor: '#ccc' }}>
            <div className="text-[9px] font-bold text-center py-0.5 sticky top-0 z-10" style={{ background: '#e8f5e9', color: '#2e7d32', borderBottom: '1px solid #ccc' }}>
              Jaimini Karakas
            </div>
            <table className="w-full text-[8px]" style={{ borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ background: '#f5f5f5' }}>
                  <th className="text-left px-1 py-0.5 font-semibold" style={{ borderBottom: '1px solid #ddd' }}>Karaka</th>
                  <th className="text-left px-1 py-0.5 font-semibold" style={{ borderBottom: '1px solid #ddd' }}>Planet</th>
                  <th className="text-center px-1 py-0.5 font-semibold" style={{ borderBottom: '1px solid #ddd' }}>Deg</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(jaiminiKarakas).map(([planet, karaka]) => {
                  const pData = planets.find((p) => p.planet === planet);
                  return (
                    <tr key={planet} style={{ borderBottom: '1px solid #eee' }}>
                      <td className="px-1 py-0.5 font-bold" style={{ color: '#555' }}>{karaka}</td>
                      <td className="px-1 py-0.5 font-medium" style={{ color: getPlanetColor(planet) }}>{planet}</td>
                      <td className="px-1 py-0.5 text-center" style={{ color: '#777' }}>{pData?.sign_degree?.toFixed(1)}&deg;</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
            {/* Karaka legend */}
            <div className="px-1 pt-1" style={{ borderTop: '1px solid #eee' }}>
              {[
                ['AK', 'Atmakaraka (Soul)'],
                ['AmK', 'Amatyakaraka (Mind)'],
                ['BK', 'Bhratrukaraka (Sibling)'],
                ['MK', 'Matrukaraka (Mother)'],
                ['PiK', 'Pitrukaraka (Father)'],
                ['GnK', 'Gnatikaraka (Rival)'],
                ['DK', 'Darakaraka (Spouse)'],
              ].map(([abbr, full]) => (
                <div key={abbr} className="text-[7px]" style={{ color: '#aaa' }}>
                  <strong>{abbr}</strong> = {full}
                </div>
              ))}
            </div>
          </div>

          {/* Shadbala */}
          <div className="overflow-auto">
            <div className="text-[9px] font-bold text-center py-0.5 sticky top-0 z-10" style={{ background: '#e8f5e9', color: '#2e7d32', borderBottom: '1px solid #ccc' }}>
              Shadbala
            </div>
            {loadingShadbala ? <MiniLoader /> : shadbalaData?.planets ? (
              <div className="px-1 py-0.5">
                {['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'].map((planet) => {
                  const data = shadbalaData.planets[planet];
                  if (!data) return null;
                  const pct = Math.min((data.total / data.required) * 100, 100);
                  const isStrong = data.is_strong;
                  return (
                    <div key={planet} className="flex items-center gap-1 py-px">
                      <span className="text-[8px] font-medium w-8 flex-shrink-0" style={{ color: getPlanetColor(planet) }}>
                        {planet.slice(0, 3)}
                      </span>
                      <div className="flex-1 h-2 rounded-sm overflow-hidden" style={{ background: '#eee' }}>
                        <div
                          className="h-full rounded-sm"
                          style={{
                            width: `${pct}%`,
                            background: isStrong ? '#4caf50' : '#e53935',
                          }}
                        />
                      </div>
                      <span className="text-[7px] w-10 text-right flex-shrink-0" style={{ color: isStrong ? '#4caf50' : '#e53935' }}>
                        {data.total}/{data.required}
                      </span>
                    </div>
                  );
                })}
              </div>
            ) : (
              <span className="text-[8px] block text-center py-4" style={{ color: '#999' }}>Loading...</span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
