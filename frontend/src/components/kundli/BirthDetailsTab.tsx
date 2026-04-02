import { useMemo } from 'react';
import { useTranslation } from '@/lib/i18n';
import { getDignity, SIGN_TYPE, SIGN_ELEMENT, PLANET_NATURE } from './kundli-utils';
import { calculateJaiminiKarakas } from './jhora-utils';

interface BirthDetailsTabProps {
  planets: any[];
}

export default function BirthDetailsTab({ planets }: BirthDetailsTabProps) {
  const { t } = useTranslation();
  const karakas = useMemo(() => calculateJaiminiKarakas(planets), [planets]);

  // Reverse map: planet -> karaka abbreviation
  const planetKaraka: Record<string, string> = {};
  for (const [planet, karaka] of Object.entries(karakas)) {
    planetKaraka[planet] = karaka;
  }

  return (
    <div className="overflow-x-auto">
        <table className="w-full text-xs">
          <thead className="bg-sacred-gold/10">
            <tr>
              <th className="text-left p-2 font-medium text-sacred-gold-dark">Planet</th>
              <th className="text-left p-2 font-medium text-sacred-gold-dark">{t('kundli.sign')}</th>
              <th className="text-left p-2 font-medium text-sacred-gold-dark">{t('kundli.degree')}</th>
              <th className="text-left p-2 font-medium text-sacred-gold-dark">{t('kundli.nakshatra')}</th>
              <th className="text-left p-2 font-medium text-sacred-gold-dark">{t('kundli.house')}</th>
              <th className="text-left p-2 font-medium text-sacred-gold-dark">{t('kundli.dignity')}</th>
              <th className="text-left p-2 font-medium text-sacred-gold-dark">{t('kundli.signType')}</th>
              <th className="text-left p-2 font-medium text-sacred-gold-dark">{t('kundli.element')}</th>
              <th className="text-left p-2 font-medium text-sacred-gold-dark">{t('kundli.nature')}</th>
              <th className="text-left p-2 font-medium text-sacred-gold-dark">{t('kundli.retrograde')}</th>
              <th className="text-left p-2 font-medium text-sacred-gold-dark">Jaimini</th>
            </tr>
          </thead>
          <tbody>
            {planets.map((p: any, idx: number) => {
              const dignity = getDignity(p.planet, p.sign, t);
              const signType = SIGN_TYPE[p.sign] || '\u2014';
              const element = SIGN_ELEMENT[p.sign] || '\u2014';
              const nature = PLANET_NATURE[p.planet] || '\u2014';
              const isRetro = (p.status || '').toLowerCase().includes('retrograde') || (p.status || '').toLowerCase().includes(' r');
              const dignityColor = dignity === t('kundli.exalted') ? '#16a34a' : dignity === t('kundli.debilitated') ? '#dc2626' : dignity === t('kundli.ownSign') ? '#2563eb' : '#8B7355';
              const nakshatraParts = (p.nakshatra || '').split(' Pada ');
              const nakshatraName = nakshatraParts[0] || p.nakshatra || '\u2014';
              const pada = nakshatraParts[1] || '\u2014';
              const karaka = planetKaraka[p.planet] || '\u2014';

              return (
                <tr key={idx} className={`border-t border-sacred-gold/10 text-xs ${idx % 2 === 0 ? '' : 'bg-sacred-gold/[0.02]'}`}>
                  <td className="p-2 font-medium text-sacred-brown font-display">{t(`planet.${p.planet}`) !== `planet.${p.planet}` ? t(`planet.${p.planet}`) : p.planet}</td>
                  <td className="p-2 text-sacred-brown">{p.sign}</td>
                  <td className="p-2 text-sacred-brown">{p.sign_degree != null ? `${Number(p.sign_degree).toFixed(2)}\u00b0` : '\u2014'}</td>
                  <td className="p-2 text-sacred-brown">{nakshatraName}{pada !== '\u2014' ? ` (${t('kundli.pada')} ${pada})` : ''}</td>
                  <td className="p-2 text-sacred-brown">{p.house}</td>
                  <td className="p-2 font-medium" style={{ color: dignityColor }}>{dignity}</td>
                  <td className="p-2 text-sacred-text-secondary">{signType}</td>
                  <td className="p-2 text-sacred-text-secondary">{element}</td>
                  <td className="p-2">
                    <span className={`text-xs px-2 py-0.5 rounded-full ${nature === 'Benefic' || nature === t('kundli.benefic') ? 'bg-green-500/15 text-green-600' : 'bg-red-500/15 text-red-600'}`}>
                      {nature}
                    </span>
                  </td>
                  <td className="p-2" style={{ color: isRetro ? '#dc2626' : '#8B7355' }}>
                    {isRetro ? `${t('common.yes')} \u211e` : t('common.no')}
                  </td>
                  <td className="p-2 font-semibold" style={{ color: karaka !== '\u2014' ? '#B8860B' : '#8B7355' }}>
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
