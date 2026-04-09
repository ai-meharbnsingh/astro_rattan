import { useMemo } from 'react';
import { getDignity, SIGN_TYPE, SIGN_ELEMENT, PLANET_NATURE } from './kundli-utils';
import { calculateJaiminiKarakas } from './jhora-utils';
import { useTranslation } from '@/lib/i18n';
import { translatePlanet, translateSign, translateNakshatra, translateLabel } from '@/lib/backend-translations';

interface BirthDetailsTabProps {
  planets: any[];
}

export default function BirthDetailsTab({ planets }: BirthDetailsTabProps) {
  const { language } = useTranslation();
  const karakas = useMemo(() => calculateJaiminiKarakas(planets), [planets]);

  // Reverse map: planet -> karaka abbreviation
  const planetKaraka: Record<string, string> = {};
  for (const [planet, karaka] of Object.entries(karakas)) {
    planetKaraka[planet] = karaka;
  }

  return (
    <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="bg-sacred-gold">
            <tr>
              <th className="text-left p-2 font-medium text-sacred-gold-dark">{language === 'hi' ? 'ग्रह' : 'Planet'}</th>
              <th className="text-left p-2 font-medium text-sacred-gold-dark">{language === 'hi' ? 'राशि' : 'Sign'}</th>
              <th className="text-left p-2 font-medium text-sacred-gold-dark">{language === 'hi' ? 'अंश' : 'Degree'}</th>
              <th className="text-left p-2 font-medium text-sacred-gold-dark">{language === 'hi' ? 'नक्षत्र' : 'Nakshatra'}</th>
              <th className="text-left p-2 font-medium text-sacred-gold-dark">{language === 'hi' ? 'भाव' : 'House'}</th>
              <th className="text-left p-2 font-medium text-sacred-gold-dark">{language === 'hi' ? 'गौरव' : 'Dignity'}</th>
              <th className="text-left p-2 font-medium text-sacred-gold-dark">{language === 'hi' ? 'राशि प्रकार' : 'Sign Type'}</th>
              <th className="text-left p-2 font-medium text-sacred-gold-dark">{language === 'hi' ? 'तत्व' : 'Element'}</th>
              <th className="text-left p-2 font-medium text-sacred-gold-dark">{language === 'hi' ? 'स्वभाव' : 'Nature'}</th>
              <th className="text-left p-2 font-medium text-sacred-gold-dark">{language === 'hi' ? 'वक्री' : 'Retrograde'}</th>
              <th className="text-left p-2 font-medium text-sacred-gold-dark">{language === 'hi' ? 'जैमिनी' : 'Jaimini'}</th>
            </tr>
          </thead>
          <tbody>
            {planets.map((p: any, idx: number) => {
              const dignity = getDignity(p.planet, p.sign);
              const signType = SIGN_TYPE[p.sign] || '\u2014';
              const element = SIGN_ELEMENT[p.sign] || '\u2014';
              const nature = PLANET_NATURE[p.planet] || '\u2014';
              const isRetro = (p.status || '').toLowerCase().includes('retrograde') || (p.status || '').toLowerCase().includes(' r');
              const dignityColor = dignity === 'Exalted' ? '#16a34a' : dignity === 'Debilitated' ? '#dc2626' : dignity === 'Own Sign' ? '#2563eb' : 'var(--ink-light)';
              const nakshatraName = translateNakshatra(p.nakshatra || '', language) || '\u2014';
              const pada = p.nakshatra_pada || (p.nakshatra || '').split(' Pada ')[1] || '\u2014';
              const signDeg = p.sign_degree != null ? Number(p.sign_degree) : null;
              const isSandhi = signDeg !== null && (signDeg < 1 || signDeg > 29);
              const karaka = planetKaraka[p.planet] || '\u2014';

              return (
                <tr key={idx} className={`border-t border-sacred-gold text-sm ${idx % 2 === 0 ? '' : 'bg-sacred-gold/[0.02]'}`}>
                  <td className="p-2 font-medium text-sacred-brown font-display">{translatePlanet(p.planet, language)}</td>
                  <td className="p-2 text-sacred-brown">{translateSign(p.sign, language)}</td>
                  <td className="p-2 text-sacred-brown">
                    {signDeg !== null ? `${signDeg.toFixed(2)}\u00b0` : '\u2014'}
                    {isSandhi && <span className="ml-1 text-sm px-1 py-0.5 rounded bg-amber-500 text-amber-600 font-medium">{language === 'hi' ? 'संधि' : 'Sandhi'}</span>}
                  </td>
                  <td className="p-2 text-sacred-brown">{nakshatraName} ({language === 'hi' ? 'पाद' : 'Pada'} {pada})</td>
                  <td className="p-2 text-sacred-brown">{p.house}</td>
                  <td className="p-2 font-medium" style={{ color: dignityColor }}>{translateLabel(dignity, language)}</td>
                  <td className="p-2 text-cosmic-text">{translateLabel(signType, language)}</td>
                  <td className="p-2 text-cosmic-text">{translateLabel(element, language)}</td>
                  <td className="p-2">
                    <span className={`text-sm px-2 py-0.5 rounded-full ${nature === 'Benefic' ? 'bg-green-500 text-green-400' : 'bg-red-500 text-red-400'}`}>
                      {language === 'hi' ? (nature === 'Benefic' ? 'शुभ' : 'पापी') : nature}
                    </span>
                  </td>
                  <td className="p-2" style={{ color: isRetro ? '#dc2626' : 'var(--ink-light)' }}>
                    {isRetro ? (language === 'hi' ? 'हाँ \u211e' : 'Yes \u211e') : (language === 'hi' ? 'नहीं' : 'No')}
                  </td>
                  <td className="p-2 font-semibold" style={{ color: karaka !== '\u2014' ? 'var(--aged-gold-dim)' : 'var(--ink-light)' }}>
                    {karaka}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
  );
}
