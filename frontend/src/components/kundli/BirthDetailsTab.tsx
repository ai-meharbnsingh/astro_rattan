import { useTranslation } from '@/lib/i18n';
import { getDignity, SIGN_TYPE, SIGN_ELEMENT, PLANET_NATURE } from './kundli-utils';

interface BirthDetailsTabProps {
  planets: any[];
}

export default function BirthDetailsTab({ planets }: BirthDetailsTabProps) {
  const { t } = useTranslation();

  return (
    <div className="space-y-4">
      <h4 className="font-display text-lg font-semibold text-sacred-brown">{t('kundli.birthDetailsTable')}</h4>
      <div className="overflow-x-auto rounded-xl border border-sacred-gold/20">
        <table className="w-full text-sm">
          <thead className="bg-sacred-gold/10">
            <tr>
              <th className="text-left p-3 font-medium text-sacred-gold-dark">Planet</th>
              <th className="text-left p-3 font-medium text-sacred-gold-dark">{t('kundli.sign')}</th>
              <th className="text-left p-3 font-medium text-sacred-gold-dark">{t('kundli.degree')}</th>
              <th className="text-left p-3 font-medium text-sacred-gold-dark">{t('kundli.nakshatra')}</th>
              <th className="text-left p-3 font-medium text-sacred-gold-dark">{t('kundli.house')}</th>
              <th className="text-left p-3 font-medium text-sacred-gold-dark">{t('kundli.dignity')}</th>
              <th className="text-left p-3 font-medium text-sacred-gold-dark">{t('kundli.signType')}</th>
              <th className="text-left p-3 font-medium text-sacred-gold-dark">{t('kundli.element')}</th>
              <th className="text-left p-3 font-medium text-sacred-gold-dark">{t('kundli.nature')}</th>
              <th className="text-left p-3 font-medium text-sacred-gold-dark">{t('kundli.retrograde')}</th>
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

              return (
                <tr key={idx} className="border-t" style={{ borderColor: 'rgba(139,115,85,0.2)', backgroundColor: idx % 2 === 0 ? '#F5F0E8' : '#FDFBF7' }}>
                  <td className="p-3 font-medium" style={{ color: '#1a1a2e', fontFamily: 'serif' }}>{p.planet}</td>
                  <td className="p-3" style={{ color: '#1a1a2e' }}>{p.sign}</td>
                  <td className="p-3" style={{ color: '#1a1a2e' }}>{p.sign_degree != null ? `${Number(p.sign_degree).toFixed(2)}\u00b0` : '\u2014'}</td>
                  <td className="p-3" style={{ color: '#1a1a2e' }}>{nakshatraName}{pada !== '\u2014' ? ` (${t('kundli.pada')} ${pada})` : ''}</td>
                  <td className="p-3" style={{ color: '#1a1a2e' }}>{p.house}</td>
                  <td className="p-3 font-medium" style={{ color: dignityColor }}>{dignity}</td>
                  <td className="p-3" style={{ color: '#8B7355' }}>{signType}</td>
                  <td className="p-3" style={{ color: '#8B7355' }}>{element}</td>
                  <td className="p-3">
                    <span className={`text-xs px-2 py-0.5 rounded-full ${nature === 'Benefic' || nature === t('kundli.benefic') ? 'bg-green-500/15 text-green-600' : 'bg-red-500/15 text-red-600'}`}>
                      {nature}
                    </span>
                  </td>
                  <td className="p-3" style={{ color: isRetro ? '#dc2626' : '#8B7355' }}>
                    {isRetro ? `${t('common.yes')} \u211e` : t('common.no')}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
