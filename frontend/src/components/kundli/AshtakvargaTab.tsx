import { Loader2 } from 'lucide-react';
import InteractiveKundli from '@/components/InteractiveKundli';
import { translatePlanet } from '@/lib/backend-translations';

interface AshtakvargaTabProps {
  ashtakvargaData: any;
  loadingAshtakvarga: boolean;
  result: any;
  language: string;
  t: (key: string) => string;
}

export default function AshtakvargaTab(props: AshtakvargaTabProps) {
  const { ashtakvargaData, loadingAshtakvarga, result, language, t } = props;

  return (
    <>
      {loadingAshtakvarga ? (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="w-6 h-6 animate-spin text-sacred-gold" />
          <span className="ml-2 text-sacred-text-secondary">{t('kundli.loadingAshtakvarga')}</span>
        </div>
      ) : ashtakvargaData ? (
        <div className="space-y-6">
          {/* SAV Chart — Visual Kundli with points in each house */}
          <div className="bg-sacred-cream rounded-xl p-5 border border-sacred-gold/20">
            <h4 className="font-display font-semibold text-sacred-brown mb-4">{t('section.sarvashtakvarga')} {t('kundli.chart')}</h4>
            <div className="w-full max-w-[600px] mx-auto">
              <InteractiveKundli
                chartData={{
                  planets: (() => {
                    const signNames = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces'];
                    return signNames.map((sign, i) => ({
                      planet: `${ashtakvargaData.sarvashtakvarga?.[sign] || 0}`,
                      sign,
                      house: i + 1,
                      nakshatra: 'SAV',
                      sign_degree: 15,
                      status: (ashtakvargaData.sarvashtakvarga?.[sign] || 0) >= 28 ? 'Strong' : 'Weak',
                    }));
                  })(),
                  houses: result?.chart_data?.houses,
                }}
                onPlanetClick={() => {}}
                onHouseClick={() => {}}
              />
            </div>
            <p className="text-xs text-center text-sacred-text-secondary mt-2">{t('ashtakvarga.savDescription')}</p>
          </div>

          {/* SAV Bar Chart */}
          <div className="bg-sacred-cream rounded-xl p-5 border border-sacred-gold/20">
            <h4 className="font-display font-semibold text-sacred-brown mb-4">{t('section.sarvashtakvarga')}</h4>
            <div className="flex items-end gap-2 h-48">
              {['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'].map((sign) => {
                const points = ashtakvargaData.sarvashtakvarga?.[sign] || 0;
                const maxPoints = 56;
                const heightPct = Math.round((points / maxPoints) * 100);
                const isStrong = points >= 28;
                return (
                  <div key={sign} className="flex-1 flex flex-col items-center gap-1">
                    <span className="text-xs font-medium text-sacred-brown">{points}</span>
                    <div className="w-full bg-sacred-gold/10 rounded-t-md relative" style={{ height: '140px' }}>
                      <div
                        className="absolute bottom-0 w-full rounded-t-md transition-all"
                        style={{
                          height: `${heightPct}%`,
                          backgroundColor: isStrong ? 'var(--aged-gold-dim)' : 'var(--ink-light)',
                        }}
                      />
                    </div>
                    <span className="text-xs text-sacred-text-secondary truncate w-full text-center" title={sign}>
                      {sign.slice(0, 3)}
                    </span>
                  </div>
                );
              })}
            </div>
            <div className="flex items-center gap-4 mt-3 text-xs text-sacred-text-secondary">
              <div className="flex items-center gap-1">
                <div className="w-3 h-3 rounded" style={{ backgroundColor: 'var(--aged-gold-dim)' }} />
                <span>{t('kundli.strong')} (&ge;28)</span>
              </div>
              <div className="flex items-center gap-1">
                <div className="w-3 h-3 rounded" style={{ backgroundColor: 'var(--ink-light)' }} />
                <span>{t('kundli.weak')} (&lt;28)</span>
              </div>
            </div>
          </div>

          {/* Bhinna Ashtakvarga Charts — Parashara's Light format: table + diamond chart per planet */}
          <div className="bg-sacred-cream rounded-xl p-5 border border-sacred-gold/20">
            <h4 className="font-display font-semibold text-sacred-brown mb-2">{language === 'hi' ? 'भिन्न अष्टकवर्ग चार्ट' : 'Bhinna Ashtakvarga Charts'}</h4>
            <p className="text-xs text-sacred-text-secondary mb-4">{language === 'hi' ? '12 राशियों में प्रत्येक ग्रह के बिंदु (पराशर प्रकाश प्रारूप)।' : 'Individual planet bindus across 12 signs (Parashara\'s Light format).'}</p>
            <div className="grid grid-cols-1 gap-5">
              {['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Lagna'].map((planet) => {
                const bindus = ashtakvargaData.planet_bindus?.[planet] || {};
                const signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'];
                const signAbbr = ['Ari', 'Tau', 'Gem', 'Can', 'Leo', 'Vir', 'Lib', 'Sco', 'Sag', 'Cap', 'Aqu', 'Pis'];
                const vals = signs.map((s) => bindus[s] || 0);
                const total = vals.reduce((sum, v) => sum + v, 0);

                const binduColor = (v: number) =>
                  v >= 5 ? '#166534' : v >= 3 ? '#B8860B' : '#991b1b';
                const binduBg = (v: number) =>
                  v >= 5 ? '#dcfce7' : v >= 3 ? '#fef3c7' : '#fee2e2';

                // North Indian diamond chart positions (280x280 SVG)
                const housePos: { x: number; y: number }[] = [
                  { x: 140, y: 45 },   // 1 Ari  — top center
                  { x: 210, y: 45 },   // 2 Tau  — top right
                  { x: 240, y: 95 },   // 3 Gem  — right upper
                  { x: 240, y: 185 },  // 4 Can  — right lower
                  { x: 210, y: 235 },  // 5 Leo  — bottom right
                  { x: 140, y: 235 },  // 6 Vir  — bottom center
                  { x: 70, y: 235 },   // 7 Lib  — bottom left
                  { x: 40, y: 185 },   // 8 Sco  — left lower
                  { x: 40, y: 95 },    // 9 Sag  — left upper
                  { x: 70, y: 45 },    // 10 Cap — top left
                  { x: 140, y: 110 },  // 11 Aqu — inner top
                  { x: 140, y: 170 },  // 12 Pis — inner bottom
                ];

                return (
                  <div key={planet} className="bg-white rounded-lg border border-sacred-gold/20 overflow-hidden">
                    {/* Planet header */}
                    <div className="bg-sacred-gold/10 px-4 py-2 border-b border-sacred-gold/20 flex items-center justify-between">
                      <h5 className="font-display font-semibold text-sacred-brown text-sm">
                        {translatePlanet(planet, language)}
                      </h5>
                      <span className="text-xs font-semibold text-sacred-gold-dark">{language === 'hi' ? 'कुल' : 'Total'}: {total}</span>
                    </div>
                    <div className="flex flex-col lg:flex-row">
                      {/* LEFT: Full contributor matrix table (compact) */}
                      <div className="lg:max-w-[550px] overflow-x-auto p-3">
                        {(() => {
                          const contributors = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Lagna'];
                          const contribData = ashtakvargaData.planet_details?.[planet]?.contributors;
                          return (
                            <table className="w-full text-xs border-collapse">
                              <thead>
                                <tr>
                                  <th className="text-left p-1 text-sacred-gold-dark font-medium border-b border-sacred-gold/20 whitespace-nowrap">Contributor</th>
                                  {signAbbr.map((s, i) => (
                                    <th key={i} className="text-center p-1 text-sacred-gold-dark font-medium border-b border-sacred-gold/20 min-w-[26px]">{s}</th>
                                  ))}
                                  <th className="text-center p-1 text-sacred-gold-dark font-bold border-b border-sacred-gold/20">&Sigma;</th>
                                </tr>
                              </thead>
                              <tbody>
                                {contributors.map((contrib) => {
                                  const row = contribData?.[contrib] || {};
                                  const rowVals = signs.map((s) => row[s] || 0);
                                  const rowTotal = rowVals.reduce((a, b) => a + b, 0);
                                  return (
                                    <tr key={contrib} className="border-t border-sacred-gold/10 hover:bg-sacred-gold/5">
                                      <td className="p-1 text-sacred-brown font-medium whitespace-nowrap">{translatePlanet(contrib, language)}</td>
                                      {rowVals.map((v, i) => (
                                        <td key={i} className="text-center p-1">
                                          <span className={`inline-block w-5 h-5 leading-5 rounded-sm text-xs font-semibold ${v === 1 ? 'bg-green-100 text-green-800' : 'text-sacred-text-secondary/40'}`}>
                                            {v}
                                          </span>
                                        </td>
                                      ))}
                                      <td className="text-center p-1 font-semibold text-sacred-brown">{rowTotal}</td>
                                    </tr>
                                  );
                                })}
                                {/* Bindu total row */}
                                <tr className="border-t-2 border-sacred-gold/30 bg-sacred-gold/5">
                                  <td className="p-1 text-sacred-gold-dark font-bold whitespace-nowrap">{language === 'hi' ? 'बिंदु' : 'Bindu'}</td>
                                  {vals.map((v, i) => (
                                    <td key={i} className="text-center p-1">
                                      <span
                                        className="inline-block w-6 h-6 leading-6 rounded text-xs font-bold"
                                        style={{ backgroundColor: binduBg(v), color: binduColor(v) }}
                                      >
                                        {v}
                                      </span>
                                    </td>
                                  ))}
                                  <td className="text-center p-1 font-bold text-sacred-brown">{total}</td>
                                </tr>
                              </tbody>
                            </table>
                          );
                        })()}
                      </div>
                      {/* RIGHT: North Indian diamond chart SVG */}
                      <div className="flex-shrink-0 flex items-center justify-center p-4 lg:border-l border-t lg:border-t-0 border-sacred-gold/10">
                        <svg viewBox="0 0 280 280" width="280" height="280" className="block">
                          <rect x="2" y="2" width="276" height="276" fill="none" stroke="#c8a96e" strokeWidth="1.5" />
                          <line x1="2" y1="2" x2="278" y2="278" stroke="#c8a96e" strokeWidth="0.75" />
                          <line x1="278" y1="2" x2="2" y2="278" stroke="#c8a96e" strokeWidth="0.75" />
                          <line x1="140" y1="2" x2="278" y2="140" stroke="#c8a96e" strokeWidth="0.75" />
                          <line x1="278" y1="140" x2="140" y2="278" stroke="#c8a96e" strokeWidth="0.75" />
                          <line x1="140" y1="278" x2="2" y2="140" stroke="#c8a96e" strokeWidth="0.75" />
                          <line x1="2" y1="140" x2="140" y2="2" stroke="#c8a96e" strokeWidth="0.75" />
                          {/* Bindu values in each house position */}
                          {housePos.map((pos, i) => (
                            <g key={i}>
                              <text x={pos.x} y={pos.y - 10} textAnchor="middle" fontSize="10" fill="#8B7355" fontFamily="sans-serif">
                                {signAbbr[i]}
                              </text>
                              <text x={pos.x} y={pos.y + 8} textAnchor="middle" fontSize="22" fontWeight="bold" fill={binduColor(vals[i])} fontFamily="sans-serif">
                                {vals[i]}
                              </text>
                            </g>
                          ))}
                        </svg>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
            {/* Color legend */}
            <div className="flex items-center gap-4 mt-4 text-xs text-sacred-text-secondary">
              <div className="flex items-center gap-1">
                <div className="w-3 h-3 rounded border" style={{ backgroundColor: '#dcfce7', borderColor: '#86efac' }} />
                <span>{language === 'hi' ? '5-8 प्रबल' : '5-8 Strong'}</span>
              </div>
              <div className="flex items-center gap-1">
                <div className="w-3 h-3 rounded border" style={{ backgroundColor: '#fef3c7', borderColor: '#fcd34d' }} />
                <span>{language === 'hi' ? '3-4 मध्यम' : '3-4 Medium'}</span>
              </div>
              <div className="flex items-center gap-1">
                <div className="w-3 h-3 rounded border" style={{ backgroundColor: '#fee2e2', borderColor: '#fca5a5' }} />
                <span>{language === 'hi' ? '0-2 दुर्बल' : '0-2 Weak'}</span>
              </div>
            </div>
          </div>

          <div className="bg-sacred-cream rounded-xl p-5 border border-sacred-gold/20">
            <h4 className="font-display font-semibold text-sacred-brown mb-4">{t('section.bhinnashtakvarga')}</h4>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-sacred-gold/20">
                    <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.planet')}</th>
                    {['Ari', 'Tau', 'Gem', 'Can', 'Leo', 'Vir', 'Lib', 'Sco', 'Sag', 'Cap', 'Aqu', 'Pis'].map((s) => (
                      <th key={s} className="text-center p-2 text-sacred-gold-dark font-medium text-xs">{s}</th>
                    ))}
                    <th className="text-center p-2 text-sacred-gold-dark font-medium">{t('table.total')}</th>
                  </tr>
                </thead>
                <tbody>
                  {['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'].map((planet) => {
                    const bindus = ashtakvargaData.planet_bindus?.[planet] || {};
                    const signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'];
                    const total = signs.reduce((sum, s) => sum + (bindus[s] || 0), 0);
                    return (
                      <tr key={planet} className="border-t border-sacred-gold/10 hover:bg-sacred-gold/5">
                        <td className="p-2 text-sacred-brown font-medium">{translatePlanet(planet, language)}</td>
                        {signs.map((s) => {
                          const val = bindus[s] || 0;
                          return (
                            <td key={s} className="text-center p-2">
                              <span className={`inline-block w-6 h-6 rounded text-xs leading-6 ${val >= 5 ? 'bg-sacred-gold-dark/20 text-sacred-gold-dark font-bold' : val <= 2 ? 'bg-red-10 text-wax-red-deep' : 'text-sacred-text-secondary'}`}>
                                {val}
                              </span>
                            </td>
                          );
                        })}
                        <td className="text-center p-2 font-semibold text-sacred-brown">{total}</td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      ) : (
        <p className="text-center text-sacred-text-secondary py-8">{t('kundli.clickAshtakvargaTab')}</p>
      )}
    </>
  );
}
