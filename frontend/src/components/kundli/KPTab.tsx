import { Loader2 } from 'lucide-react';
import InteractiveKundli, { type PlanetData, type ChartData } from '@/components/InteractiveKundli';
import { translatePlanet, translateSign } from '@/lib/backend-translations';
import GeneralRemedies from './GeneralRemedies';

interface KPTabProps {
  kpData: any;
  loadingKp: boolean;
  result: any;
  language: string;
  t: (key: string) => string;
}

export default function KPTab(props: KPTabProps) {
  const { kpData, loadingKp, result, language, t } = props;

  return (
    <div className="space-y-6">
      {loadingKp ? (
        <div className="flex items-center justify-center py-12"><Loader2 className="w-6 h-6 animate-spin text-sacred-gold" /><span className="ml-2 text-cosmic-text">{t('kundli.loadingKP')}</span></div>
      ) : kpData ? (
        <div className="space-y-6">
          {/* 1. KP Planet Table — full reference chart style */}
          <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-4">
            <h4 className="font-display font-semibold text-sacred-brown mb-3">{language === 'hi' ? 'कृष्णमूर्ति पद्धति — ग्रह चार्ट' : 'Krishnamurti Paddhati — Planet Chart'}</h4>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead><tr className="bg-sacred-gold">
                  <th className="text-left p-1.5 text-sacred-gold-dark font-medium">{t('table.planet')}</th>
                  <th className="text-center p-1.5 text-sacred-gold-dark font-medium">R/C</th>
                  <th className="text-left p-1.5 text-sacred-gold-dark font-medium">{t('table.sign')}</th>
                  <th className="text-left p-1.5 text-sacred-gold-dark font-medium">{t('table.degree')}</th>
                  <th className="text-left p-1.5 text-sacred-gold-dark font-medium">{t('table.nakshatra')}</th>
                  <th className="text-center p-1.5 text-sacred-gold-dark font-medium">{t('kundli.pada')}</th>
                  <th className="text-center p-1.5 text-sacred-gold-dark font-medium">RL</th>
                  <th className="text-center p-1.5 text-sacred-gold-dark font-medium">NL</th>
                  <th className="text-center p-1.5 text-sacred-gold-dark font-medium">SL</th>
                  <th className="text-center p-1.5 text-sacred-gold-dark font-medium">SS</th>
                </tr></thead>
                <tbody>
                  {(kpData.planets || []).map((p: any) => (
                    <tr key={p.planet} className="border-t border-sacred-gold">
                      <td className="p-1.5 font-semibold text-sacred-brown">{translatePlanet(p.planet, language)}</td>
                      <td className="p-1.5 text-center">{p.retrograde ? <span className="text-red-400 font-bold">R</span> : ''}</td>
                      <td className="p-1.5 text-cosmic-text">{translateSign(p.sign, language)}</td>
                      <td className="p-1.5 text-cosmic-text font-mono">{p.degree_dms || (typeof p.degree === 'number' ? p.degree.toFixed(2) : p.degree)}</td>
                      <td className="p-1.5 text-cosmic-text">{p.nakshatra || '-'}</td>
                      <td className="p-1.5 text-center text-cosmic-text">{p.pada || '-'}</td>
                      <td className="p-1.5 text-center text-sacred-gold-dark font-medium">{p.sign_lord ? p.sign_lord.slice(0, 2) : '-'}</td>
                      <td className="p-1.5 text-center text-sacred-gold-dark font-medium">{(p.star_lord || p.nakshatra_lord || '-').slice(0, 2)}</td>
                      <td className="p-1.5 text-center text-sacred-gold-dark font-medium">{p.sub_lord ? p.sub_lord.slice(0, 2) : '-'}</td>
                      <td className="p-1.5 text-center text-sacred-gold-dark font-medium">{p.sub_sub_lord ? p.sub_sub_lord.slice(0, 2) : '-'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Birth Chart + Cuspal Chart — North Indian Diamond */}
          {(() => {
            // Build chart data from KP planets for Birth Chart (Rashi-based houses)
            const SIGNS = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces'];
            const kpPlanets = kpData.planets || [];
            // Birth chart: house derived from sign relative to ascendant sign
            const ascSign = result?.chart_data?.ascendant?.sign || (kpData.cusps?.[0]?.sign) || 'Aries';
            const ascIdx = SIGNS.indexOf(ascSign);
            const birthPlanets: PlanetData[] = kpPlanets.map((p: any) => {
              const signIdx = SIGNS.indexOf(p.sign);
              const house = signIdx >= 0 && ascIdx >= 0 ? ((signIdx - ascIdx + 12) % 12) + 1 : 1;
              return { planet: p.planet, sign: p.sign, house, nakshatra: p.nakshatra || '', sign_degree: typeof p.degree === 'number' ? p.degree % 30 : 0, status: '', is_retrograde: p.retrograde };
            });
            const birthHouses = SIGNS.map((_, i) => ({ number: i + 1, sign: SIGNS[(ascIdx + i) % 12] }));

            // Cuspal chart: house based on which cusp range the planet falls in
            const cusps = kpData.cusps || [];
            const cuspDegrees = cusps.map((c: any) => typeof c.degree === 'number' ? c.degree : 0);
            const cuspalPlanets: PlanetData[] = kpPlanets.map((p: any) => {
              const lon = typeof p.degree === 'number' ? p.degree : 0;
              let house = 1;
              for (let h = 0; h < 12; h++) {
                const start = cuspDegrees[h] || 0;
                const end = cuspDegrees[(h + 1) % 12] || 0;
                if (end > start ? (lon >= start && lon < end) : (lon >= start || lon < end)) { house = h + 1; break; }
              }
              return { planet: p.planet, sign: p.sign, house, nakshatra: p.nakshatra || '', sign_degree: typeof p.degree === 'number' ? p.degree % 30 : 0, status: '', is_retrograde: p.retrograde };
            });
            const cuspalHouses = cusps.map((c: any, i: number) => ({ number: i + 1, sign: c.sign || SIGNS[(ascIdx + i) % 12] }));

            return (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-4">
                  <h4 className="font-display font-semibold text-sacred-brown mb-2 text-center">{t('section.vedicBirthChart')}</h4>
                  <InteractiveKundli chartData={{ planets: birthPlanets, houses: birthHouses, ascendant: result?.chart_data?.ascendant } as ChartData} compact />
                </div>
                <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-4">
                  <h4 className="font-display font-semibold text-sacred-brown mb-2 text-center">{language === 'hi' ? 'कस्पल चार्ट' : 'Cuspal Chart'}</h4>
                  <InteractiveKundli chartData={{ planets: cuspalPlanets, houses: cuspalHouses, ascendant: result?.chart_data?.ascendant } as ChartData} compact />
                </div>
              </div>
            );
          })()}

          {/* 2. Bhava Details (Placidus) — House Cusps */}
          <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-4">
            <h4 className="font-display font-semibold text-sacred-brown mb-3">{language === 'hi' ? 'भाव विवरण (प्लेसिडस पद्धति)' : 'Bhava Details (Placidus System)'}</h4>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead><tr className="bg-sacred-gold">
                  <th className="text-left p-1.5 text-sacred-gold-dark font-medium">{t('table.house')}</th>
                  <th className="text-left p-1.5 text-sacred-gold-dark font-medium">{t('table.sign')}</th>
                  <th className="text-left p-1.5 text-sacred-gold-dark font-medium">{t('table.degree')}</th>
                  <th className="text-left p-1.5 text-sacred-gold-dark font-medium">{t('table.nakshatra')}</th>
                  <th className="text-center p-1.5 text-sacred-gold-dark font-medium">{t('kundli.pada')}</th>
                  <th className="text-center p-1.5 text-sacred-gold-dark font-medium">RL</th>
                  <th className="text-center p-1.5 text-sacred-gold-dark font-medium">NL</th>
                  <th className="text-center p-1.5 text-sacred-gold-dark font-medium">SL</th>
                  <th className="text-center p-1.5 text-sacred-gold-dark font-medium">SS</th>
                </tr></thead>
                <tbody>
                  {(() => {
                    const houseNames = language === 'hi'
                      ? ['प्रथम','द्वितीय','तृतीय','चतुर्थ','पंचम','षष्ठ','सप्तम','अष्टम','नवम','दशम','एकादश','द्वादश']
                      : ['First','Second','Third','Fourth','Fifth','Sixth','Seventh','Eighth','Ninth','Tenth','Eleventh','Twelfth'];
                    return (kpData.cusps || []).map((c: any, i: number) => {
                    return (
                      <tr key={i} className="border-t border-sacred-gold">
                        <td className="p-1.5 font-semibold text-sacred-brown">{(c.house || i + 1)}.{houseNames[i] || ''}</td>
                        <td className="p-1.5 text-cosmic-text">{translateSign(c.sign || '', language)}</td>
                        <td className="p-1.5 text-cosmic-text font-mono">{c.degree_dms || (typeof c.degree === 'number' ? c.degree.toFixed(2) : c.degree || '-')}</td>
                        <td className="p-1.5 text-cosmic-text">{c.nakshatra || '-'}</td>
                        <td className="p-1.5 text-center text-cosmic-text">{c.pada || '-'}</td>
                        <td className="p-1.5 text-center text-sacred-gold-dark font-medium">{c.sign_lord ? c.sign_lord.slice(0, 2) : '-'}</td>
                        <td className="p-1.5 text-center text-sacred-gold-dark font-medium">{(c.star_lord || '-').slice(0, 2)}</td>
                        <td className="p-1.5 text-center text-sacred-gold-dark font-medium">{(c.sub_lord || '-').slice(0, 2)}</td>
                        <td className="p-1.5 text-center text-sacred-gold-dark font-medium">{(c.sub_sub_lord || '-').slice(0, 2)}</td>
                      </tr>
                    );
                  });
                  })()}
                </tbody>
              </table>
            </div>
          </div>

          {/* 3. Significations of Houses */}
          {kpData.house_significations && Object.keys(kpData.house_significations).length > 0 && (
            <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-4">
              <h4 className="font-display font-semibold text-sacred-brown mb-3">{language === 'hi' ? 'भावों के कारकत्व' : 'Significations of Houses'}</h4>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead><tr className="bg-sacred-gold">
                    <th className="text-left p-1.5 text-sacred-gold-dark font-medium">{t('table.house')}</th>
                    <th className="text-left p-1.5 text-sacred-gold-dark font-medium">{language === 'hi' ? 'अधिपतियों की नक्ष. के ग्रह' : 'Planets in Nak. of Occupants'}</th>
                    <th className="text-left p-1.5 text-sacred-gold-dark font-medium">{language === 'hi' ? 'अधिपति' : 'Occupants'}</th>
                    <th className="text-left p-1.5 text-sacred-gold-dark font-medium">{language === 'hi' ? 'कस्प स्वामी की नक्ष. के ग्रह' : 'Planets in Nak. of Cusp Lord'}</th>
                    <th className="text-left p-1.5 text-sacred-gold-dark font-medium">{language === 'hi' ? 'कस्प राशि स्वामी' : 'Cusp Sign Lord'}</th>
                  </tr></thead>
                  <tbody>
                    {[1,2,3,4,5,6,7,8,9,10,11,12].map(h => {
                      const sig = kpData.house_significations[h] || kpData.house_significations[String(h)] || {};
                      return (
                        <tr key={h} className="border-t border-sacred-gold">
                          <td className="p-1.5 font-semibold text-sacred-brown">{h}</td>
                          <td className="p-1.5 text-cosmic-text">{(sig.planets_in_nak_of_occupants || []).join(', ') || '-'}</td>
                          <td className="p-1.5 text-cosmic-text font-medium">{(sig.occupants || []).join(', ') || '-'}</td>
                          <td className="p-1.5 text-cosmic-text">{(sig.planets_in_nak_of_cusp_sign_lord || []).join(', ') || '-'}</td>
                          <td className="p-1.5 text-sacred-gold-dark font-medium">{sig.cusp_sign_lord || '-'}</td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* 4. Houses Signified by Planets */}
          {kpData.planet_significator_strengths && Object.keys(kpData.planet_significator_strengths).length > 0 && (
            <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-4">
              <h4 className="font-display font-semibold text-sacred-brown mb-3">{language === 'hi' ? 'ग्रहों द्वारा भावों का कारकत्व' : 'Houses Signified by Planets'}</h4>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead><tr className="bg-sacred-gold">
                    <th className="text-left p-1.5 text-sacred-gold-dark font-medium">{t('table.planet')}</th>
                    <th className="text-left p-1.5 text-sacred-gold-dark font-medium">{language === 'hi' ? 'अति बलवान' : 'Very Strong'}</th>
                    <th className="text-left p-1.5 text-sacred-gold-dark font-medium">{language === 'hi' ? 'बलवान' : 'Strong'}</th>
                    <th className="text-left p-1.5 text-sacred-gold-dark font-medium">{language === 'hi' ? 'सामान्य' : 'Normal'}</th>
                    <th className="text-left p-1.5 text-sacred-gold-dark font-medium">{language === 'hi' ? 'दुर्बल' : 'Weak'}</th>
                  </tr></thead>
                  <tbody>
                    {Object.entries(kpData.planet_significator_strengths).map(([planet, levels]: [string, any]) => (
                      <tr key={planet} className="border-t border-sacred-gold">
                        <td className="p-1.5 font-semibold text-sacred-brown">{translatePlanet(planet, language)}</td>
                        <td className="p-1.5 text-green-500 font-medium">{(levels.very_strong || []).join(' ')}</td>
                        <td className="p-1.5 text-blue-400 font-medium">{(levels.strong || []).join(' ')}</td>
                        <td className="p-1.5 text-cosmic-text">{(levels.normal || []).join(' ')}</td>
                        <td className="p-1.5 text-orange-400">{(levels.weak || []).join(' ')}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* 5. Ruling Planets */}
          {kpData.ruling_planets && Object.keys(kpData.ruling_planets).length > 0 && (
            <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-4">
              <h4 className="font-display font-semibold text-sacred-brown mb-3">{language === 'hi' ? 'शासक ग्रह' : 'Ruling Planets'}</h4>
              <div className="grid grid-cols-2 gap-3 text-sm">
                {[
                  ['day_lord', language === 'hi' ? 'दिन स्वामी' : 'Day Lord'],
                  ['lagna_lord', language === 'hi' ? 'लग्न स्वामी' : 'Lagna Lord'],
                  ['lagna_nak_lord', language === 'hi' ? 'लग्न नक्ष. स्वामी' : 'Lagna Nak Lord'],
                  ['lagna_sub_lord', language === 'hi' ? 'लग्न उप स्वामी' : 'Lagna Sub Lord'],
                  ['moon_rashi_lord', language === 'hi' ? 'चंद्र राशि स्वामी' : 'Moon Rashi Lord'],
                  ['moon_nak_lord', language === 'hi' ? 'चंद्र नक्ष. स्वामी' : 'Moon Nak Lord'],
                  ['moon_sub_lord', language === 'hi' ? 'चंद्र उप स्वामी' : 'Moon Sub Lord'],
                ].map(([key, label]) => (
                  <div key={key} className="flex items-center justify-between bg-white rounded-lg p-2">
                    <span className="text-cosmic-text">{label}</span>
                    <span className="font-semibold text-sacred-gold-dark">{translatePlanet(kpData.ruling_planets[key] || '-', language)}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      ) : (
        <p className="text-center text-cosmic-text py-8">{t('kundli.clickKPTab')}</p>
      )}
      <GeneralRemedies language={language} />
    </div>
  );
}
