import { Loader2 } from 'lucide-react';
import KundliChartSVG, { type PlanetEntry } from '@/components/KundliChartSVG';
import { translatePlanet, translateSign, translateNakshatra, translateBackend } from '@/lib/backend-translations';

interface KPTabProps {
  kpData: any;
  loadingKp: boolean;
  result: any;
  language: string;
  t: (key: string) => string;
}

const SIGNS = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces'];

const thL  = 'p-1.5 text-left   text-[10px] font-semibold uppercase tracking-wide text-primary border-b border-border';
const thC  = 'p-1.5 text-center text-[10px] font-semibold uppercase tracking-wide text-primary border-b border-border';
const tdL  = 'p-1.5 text-xs text-foreground border-t border-border';
const tdC  = 'p-1.5 text-xs text-foreground border-t border-border text-center';
const tdPL = 'p-1.5 text-xs text-primary font-medium border-t border-border text-center';

function FT({ style }: { style: React.CSSProperties }) {
  return <table style={{ tableLayout: 'fixed', width: '100%', borderCollapse: 'collapse', ...style }} className="text-xs" />;
}

export default function KPTab({ kpData, loadingKp, result, language, t }: KPTabProps) {
  const hi = language === 'hi';
  const planetShort = (name: string) => (translatePlanet(name || '', language) || name || '-').slice(0, 2);
  const planetList  = (items: any[]) => (items || []).map((x) => translatePlanet(String(x || ''), language)).join(', ') || '-';

  if (loadingKp) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-6 h-6 animate-spin text-primary" />
        <span className="ml-2 text-foreground">{t('kundli.loadingKP')}</span>
      </div>
    );
  }

  if (!kpData) {
    return <p className="text-center text-foreground py-8">{t('kundli.clickKPTab')}</p>;
  }

  // ── Build chart data ──────────────────────────────────────────────────────
  const kpPlanets = kpData.planets || [];
  const ascSign   = result?.chart_data?.ascendant?.sign || kpData.cusps?.[0]?.sign || 'Aries';
  const ascIdx    = SIGNS.indexOf(ascSign);

  const birthPlanets: PlanetEntry[] = kpPlanets.map((p: any) => {
    const signIdx = SIGNS.indexOf(p.sign);
    const house   = signIdx >= 0 && ascIdx >= 0 ? ((signIdx - ascIdx + 12) % 12) + 1 : 1;
    return { planet: p.planet, sign: p.sign, house, sign_degree: typeof p.degree === 'number' ? p.degree % 30 : 0, is_retrograde: p.retrograde };
  });

  const cusps        = kpData.cusps || [];
  const cuspDegrees  = cusps.map((c: any) => typeof c.degree === 'number' ? c.degree : 0);
  const cuspalPlanets: PlanetEntry[] = kpPlanets.map((p: any) => {
    const lon = typeof p.degree === 'number' ? p.degree : 0;
    let house = 1;
    for (let h = 0; h < 12; h++) {
      const start = cuspDegrees[h] || 0;
      const end   = cuspDegrees[(h + 1) % 12] || 0;
      if (end > start ? (lon >= start && lon < end) : (lon >= start || lon < end)) { house = h + 1; break; }
    }
    return { planet: p.planet, sign: p.sign, house, sign_degree: typeof p.degree === 'number' ? p.degree % 30 : 0, is_retrograde: p.retrograde };
  });
  const cuspalAscSign = cusps[0]?.sign || ascSign;

  const houseNames = hi
    ? ['प्रथम','द्वितीय','तृतीय','चतुर्थ','पंचम','षष्ठ','सप्तम','अष्टम','नवम','दशम','एकादश','द्वादश']
    : ['First','Second','Third','Fourth','Fifth','Sixth','Seventh','Eighth','Ninth','Tenth','Eleventh','Twelfth'];

  return (
    <div className="space-y-6">

      {/* 1. KP Planet Table */}
      <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
        <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
          {t('auto.krishnamurtiPaddhati')}
        </div>
        <table style={{ tableLayout: 'fixed', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
          <colgroup>
            <col style={{ width: '10%' }} /><col style={{ width: '5%' }} />
            <col style={{ width: '10%' }} /><col style={{ width: '10%' }} />
            <col style={{ width: '16%' }} /><col style={{ width: '5%' }} />
            <col style={{ width: '8%' }} /><col style={{ width: '8%' }} />
            <col style={{ width: '8%' }} /><col style={{ width: '8%' }} />
            <col style={{ width: '12%' }} />
          </colgroup>
          <thead><tr>
            <th className={thL}>{t('table.planet')}</th>
            <th className={thC}>R/C</th>
            <th className={thL}>{t('table.sign')}</th>
            <th className={thL}>{t('table.degree')}</th>
            <th className={thL}>{t('table.nakshatra')}</th>
            <th className={thC}>{t('kundli.pada')}</th>
            <th className={thC} title={t('auto.rashiLord')}>RL</th>
            <th className={thC} title={t('auto.nakshatraLord')}>NL</th>
            <th className={thC} title={t('auto.subLord')}>SL</th>
            <th className={thC} title={t('auto.subSubLord')}>SS</th>
            <th className={thC} title={t('auto.starLordOfSubLord')}>SSSL</th>
          </tr></thead>
          <tbody>
            {kpPlanets.map((p: any) => (
              <tr key={p.planet}>
                <td className={`${tdL} font-semibold`}>{translatePlanet(p.planet, language)}</td>
                <td className={tdC}>{p.retrograde ? <span className="text-red-500 font-bold">{hi ? 'व' : 'R'}</span> : ''}</td>
                <td className={tdL}>{translateSign(p.sign, language)}</td>
                <td className={`${tdL} font-mono`}>{p.degree_dms || (typeof p.degree === 'number' ? p.degree.toFixed(2) : p.degree)}</td>
                <td className={tdL}>{translateNakshatra(p.nakshatra, language) || '-'}</td>
                <td className={tdC}>{p.pada || '-'}</td>
                <td className={tdPL}>{p.sign_lord ? planetShort(p.sign_lord) : '-'}</td>
                <td className={tdPL}>{p.star_lord || p.nakshatra_lord ? planetShort(p.star_lord || p.nakshatra_lord) : '-'}</td>
                <td className={tdPL}>{p.sub_lord ? planetShort(p.sub_lord) : '-'}</td>
                <td className={tdPL}>{p.sub_sub_lord ? planetShort(p.sub_sub_lord) : '-'}</td>
                <td className={tdPL}>{p.star_lord_of_sub_lord ? planetShort(p.star_lord_of_sub_lord) : '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* 2. Charts: Birth + Cuspal */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold text-center">
            {t('section.vedicBirthChart')}
          </div>
          <div className="flex justify-center p-4">
            <div className="w-full max-w-[380px] aspect-square">
              <KundliChartSVG
                planets={birthPlanets}
                ascendantSign={ascSign}
                language={language}
                showHouseNumbers={false}
                showRashiNumbers
                rashiNumberPlacement="corner"
                showAscendantMarker={false}
              />
            </div>
          </div>
        </div>
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold text-center">
            {t('auto.cuspalChart')}
          </div>
          <div className="flex justify-center p-4">
            <div className="w-full max-w-[380px] aspect-square">
              <KundliChartSVG
                planets={cuspalPlanets}
                ascendantSign={cuspalAscSign}
                language={language}
                showHouseNumbers={false}
                showRashiNumbers
                rashiNumberPlacement="corner"
                showAscendantMarker={false}
              />
            </div>
          </div>
        </div>
      </div>

      {/* 3. Bhava Details (Cusps) */}
      <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
        <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
          {t('auto.bhavaDetailsPlacidus')}
        </div>
        <table style={{ tableLayout: 'fixed', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
          <colgroup>
            <col style={{ width: '16%' }} /><col style={{ width: '12%' }} />
            <col style={{ width: '12%' }} /><col style={{ width: '16%' }} />
            <col style={{ width: '6%' }} /><col style={{ width: '8%' }} />
            <col style={{ width: '8%' }} /><col style={{ width: '8%' }} />
            <col style={{ width: '7%' }} /><col style={{ width: '7%' }} />
          </colgroup>
          <thead><tr>
            <th className={thL}>{t('table.house')}</th>
            <th className={thL}>{t('table.sign')}</th>
            <th className={thL}>{t('table.degree')}</th>
            <th className={thL}>{t('table.nakshatra')}</th>
            <th className={thC}>{t('kundli.pada')}</th>
            <th className={thC} title={t('auto.rashiLord')}>RL</th>
            <th className={thC} title={t('auto.nakshatraLord')}>NL</th>
            <th className={thC} title={t('auto.subLord')}>SL</th>
            <th className={thC} title={t('auto.subSubLord')}>SS</th>
            <th className={thC} title={t('auto.starLordOfSubLord')}>SSSL</th>
          </tr></thead>
          <tbody>
            {cusps.map((c: any, i: number) => (
              <tr key={i}>
                <td className={`${tdL} font-semibold`}>{(c.house || i + 1)}. {houseNames[i] || ''}</td>
                <td className={tdL}>{translateSign(c.sign || '', language)}</td>
                <td className={`${tdL} font-mono`}>{c.degree_dms || (typeof c.degree === 'number' ? c.degree.toFixed(2) : c.degree || '-')}</td>
                <td className={tdL}>{translateNakshatra(c.nakshatra, language) || '-'}</td>
                <td className={tdC}>{c.pada || '-'}</td>
                <td className={tdPL}>{c.sign_lord ? c.sign_lord.slice(0, 2) : '-'}</td>
                <td className={tdPL}>{(c.star_lord || '-').slice(0, 2)}</td>
                <td className={tdPL}>{(c.sub_lord || '-').slice(0, 2)}</td>
                <td className={tdPL}>{(c.sub_sub_lord || '-').slice(0, 2)}</td>
                <td className={tdPL}>{(c.star_lord_of_sub_lord || '-').slice(0, 2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* 4. Significations of Houses */}
      {kpData.house_significations && Object.keys(kpData.house_significations).length > 0 && (
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
            {t('auto.significationsOfHous')}
          </div>
          <table style={{ tableLayout: 'fixed', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
            <colgroup>
              <col style={{ width: '6%' }} /><col style={{ width: '26%' }} />
              <col style={{ width: '20%' }} /><col style={{ width: '26%' }} />
              <col style={{ width: '22%' }} />
            </colgroup>
            <thead><tr>
              <th className={thC}>{t('table.house')}</th>
              <th className={thL}>{t('auto.planetsInNakOfOccupa')}</th>
              <th className={thL}>{t('auto.occupants')}</th>
              <th className={thL}>{t('auto.planetsInNakOfCuspLo')}</th>
              <th className={thL}>{t('auto.cuspSignLord')}</th>
            </tr></thead>
            <tbody>
              {[1,2,3,4,5,6,7,8,9,10,11,12].map(h => {
                const sig = kpData.house_significations[h] || kpData.house_significations[String(h)] || {};
                return (
                  <tr key={h}>
                    <td className={`${tdC} font-semibold`}>{h}</td>
                    <td className={`${tdL} break-words overflow-hidden`}>{planetList(sig.planets_in_nak_of_occupants || [])}</td>
                    <td className={`${tdL} font-medium break-words overflow-hidden`}>{planetList(sig.occupants || [])}</td>
                    <td className={`${tdL} break-words overflow-hidden`}>{planetList(sig.planets_in_nak_of_cusp_sign_lord || [])}</td>
                    <td className={`${tdPL} text-left`}>{sig.cusp_sign_lord ? translatePlanet(sig.cusp_sign_lord, language) : '-'}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

      {/* 5. Houses Signified by Planets */}
      {kpData.planet_significator_strengths && Object.keys(kpData.planet_significator_strengths).length > 0 && (
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
            {t('auto.housesSignifiedByPla')}
          </div>
          <table style={{ tableLayout: 'fixed', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
            <colgroup>
              <col style={{ width: '15%' }} /><col style={{ width: '25%' }} />
              <col style={{ width: '20%' }} /><col style={{ width: '20%' }} />
              <col style={{ width: '20%' }} />
            </colgroup>
            <thead><tr>
              <th className={thL}>{t('table.planet')}</th>
              <th className={thL}>{t('auto.veryStrong')}</th>
              <th className={thL}>{t('auto.strong')}</th>
              <th className={thL}>{t('auto.normal')}</th>
              <th className={thL}>{t('auto.weak')}</th>
            </tr></thead>
            <tbody>
              {Object.entries(kpData.planet_significator_strengths).map(([planet, levels]: [string, any]) => (
                <tr key={planet}>
                  <td className={`${tdL} font-semibold`}>{translatePlanet(planet, language)}</td>
                  <td className={`${tdL} text-green-600 font-medium`}>{planetList(levels.very_strong || [])}</td>
                  <td className={`${tdL} text-blue-500 font-medium`}>{planetList(levels.strong || [])}</td>
                  <td className={tdL}>{planetList(levels.normal || [])}</td>
                  <td className={`${tdL} text-orange-500`}>{planetList(levels.weak || [])}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* 6. Ruling Planets */}
      {kpData.ruling_planets && Object.keys(kpData.ruling_planets).length > 0 && (
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
            {t('auto.rulingPlanets')}
          </div>
          <div className="p-4 grid grid-cols-2 sm:grid-cols-4 gap-3 text-sm">
            {[
              ['day_lord',          t('auto.dayLord')],
              ['lagna_lord',        t('auto.lagnaLord')],
              ['lagna_nak_lord',    t('auto.lagnaNakLord')],
              ['lagna_sub_lord',    t('auto.lagnaSubLord')],
              ['moon_rashi_lord',   t('auto.moonRashiLord')],
              ['moon_nak_lord',     t('auto.moonNakLord')],
              ['moon_sub_lord',     t('auto.moonSubLord')],
            ].map(([key, label]) => (
              <div key={key} className="rounded-lg border border-border p-3">
                <p className="text-xs text-muted-foreground">{translateBackend(label, language)}</p>
                <p className="font-semibold text-primary mt-0.5">
                  {kpData.ruling_planets[key] ? translatePlanet(kpData.ruling_planets[key], language) : '—'}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

    </div>
  );
}
