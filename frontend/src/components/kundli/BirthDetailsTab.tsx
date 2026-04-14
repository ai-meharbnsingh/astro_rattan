import { useMemo } from 'react';
import { getDignity, SIGN_TYPE, SIGN_ELEMENT, PLANET_NATURE, toDMS } from './kundli-utils';
import { calculateJaiminiKarakas } from './jhora-utils';
import { useTranslation } from '@/lib/i18n';
import { translatePlanet, translateSign, translateNakshatra, translateLabel } from '@/lib/backend-translations';

interface BirthDetailsTabProps {
  planets: any[];
}

export default function BirthDetailsTab({ planets }: BirthDetailsTabProps) {
  const { language, t } = useTranslation();
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
              <th className="text-left p-2 font-medium text-sacred-gold-dark">{t('auto.planet')}</th>
              <th className="text-left p-2 font-medium text-sacred-gold-dark">{t('auto.sign')}</th>
              <th className="text-left p-2 font-medium text-sacred-gold-dark">{t('auto.degree')}</th>
              <th className="text-left p-2 font-medium text-sacred-gold-dark">{t('auto.nakshatra')}</th>
              <th className="text-left p-2 font-medium text-sacred-gold-dark">{t('auto.house')}</th>
              <th className="text-left p-2 font-medium text-sacred-gold-dark">{t('auto.dignity')}</th>
              <th className="text-left p-2 font-medium text-sacred-gold-dark">{t('auto.signType')}</th>
              <th className="text-left p-2 font-medium text-sacred-gold-dark">{t('auto.element')}</th>
              <th className="text-left p-2 font-medium text-sacred-gold-dark">{t('auto.nature')}</th>
              <th className="text-left p-2 font-medium text-sacred-gold-dark">{t('auto.retrograde')}</th>
              <th className="text-left p-2 font-medium text-sacred-gold-dark">{t('auto.jaimini')}</th>
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
                  <td className="p-2 font-medium text-sacred-brown font-display">
                    {translatePlanet(p.planet, language)}
                    {isRetro && <span className="text-red-500 ml-0.5" title={t('kundli.retrograde')}>*</span>}
                  </td>
                  <td className="p-2 text-sacred-brown">{translateSign(p.sign, language)}</td>
                  <td className="p-2 text-sacred-brown">
                    {signDeg !== null ? toDMS(signDeg) : '\u2014'}
                    {isSandhi && <span className="ml-1 text-sm px-1 py-0.5 rounded bg-amber-500 text-amber-600 font-medium">{t('auto.sandhi')}</span>}
                  </td>
                  <td className="p-2 text-sacred-brown">{nakshatraName} ({t('auto.pada')} {pada})</td>
                  <td className="p-2 text-sacred-brown">{p.house}</td>
                  <td className="p-2 font-medium" style={{ color: dignityColor }}>{translateLabel(dignity, language)}</td>
                  <td className="p-2 text-cosmic-text">{translateLabel(signType, language)}</td>
                  <td className="p-2 text-cosmic-text">{translateLabel(element, language)}</td>
                  <td className="p-2">
                    <span className={`text-sm px-2 py-0.5 rounded-full ${nature === 'Benefic' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                      {language === 'hi' ? (nature === 'Benefic' ? 'शुभ' : 'पापी') : nature}
                    </span>
                  </td>
                  <td className="p-2" style={{ color: isRetro ? '#dc2626' : 'var(--ink-light)' }}>
                    {isRetro ? (language === 'hi' ? 'हाँ \u211e' : `${t('common.yes')} \u211e`) : t('common.no')}
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
