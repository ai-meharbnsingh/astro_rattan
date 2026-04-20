import { useMemo } from 'react';
import { getDignity, SIGN_TYPE, SIGN_ELEMENT, PLANET_NATURE, toDMS } from './kundli-utils';
import { calculateJaiminiKarakas } from './jhora-utils';
import { useTranslation } from '@/lib/i18n';
import { translatePlanet, translateSign, translateNakshatra, translateLabel } from '@/lib/backend-translations';
import { Heading } from '@/components/ui/heading';

interface BirthDetailsTabProps {
  planets: any[];
}

const ohContainer = 'rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden';
const ohHeader    = 'bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2';
const thCls       = 'p-1.5 text-left text-[10px] font-semibold uppercase tracking-wide text-primary border-b border-border';
const tdCls       = 'p-1.5 text-xs text-foreground border-t border-border align-top break-words overflow-hidden';

export default function BirthDetailsTab({ planets }: BirthDetailsTabProps) {
  const { language, t } = useTranslation();
  const isHi = language === 'hi';
  const karakas = useMemo(() => calculateJaiminiKarakas(planets), [planets]);

  const planetKaraka: Record<string, string> = {};
  for (const [planet, karaka] of Object.entries(karakas)) {
    planetKaraka[planet] = karaka;
  }

  return (
    <div className="space-y-4">
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1">
          {isHi ? 'जन्म विवरण — ग्रह स्थिति' : 'Birth Details — Planetary Positions'}
        </Heading>
        <p className="text-sm text-muted-foreground">
          {isHi ? 'राशि, नक्षत्र, दिशा, तत्व, स्वभाव एवं जैमिनी कारक' : 'Sign, nakshatra, dignity, element, nature and Jaimini karakas'}
        </p>
      </div>
      <div className={ohContainer}>
      <div className={ohHeader}>
        <span>{isHi ? 'ग्रह स्थिति' : 'Planetary Positions'}</span>
      </div>
      <div className="overflow-x-auto">
        <table style={{ tableLayout: 'fixed', width: '100%', minWidth: '720px', borderCollapse: 'collapse' }} className="text-xs">
          <colgroup>
            <col style={{ width: '9%' }} />
            <col style={{ width: '9%' }} />
            <col style={{ width: '8%' }} />
            <col style={{ width: '14%' }} />
            <col style={{ width: '6%' }} />
            <col style={{ width: '8%' }} />
            <col style={{ width: '9%' }} />
            <col style={{ width: '8%' }} />
            <col style={{ width: '8%' }} />
            <col style={{ width: '9%' }} />
            <col style={{ width: '12%' }} />
          </colgroup>
          <thead>
            <tr>
              <th className={thCls}>{t('auto.planet')}</th>
              <th className={thCls}>{t('auto.sign')}</th>
              <th className={thCls}>{t('auto.degree')}</th>
              <th className={thCls}>{t('auto.nakshatra')}</th>
              <th className={thCls}>{t('auto.house')}</th>
              <th className={thCls}>{t('auto.dignity')}</th>
              <th className={thCls}>{t('auto.signType')}</th>
              <th className={thCls}>{t('auto.element')}</th>
              <th className={thCls}>{t('auto.nature')}</th>
              <th className={thCls}>{t('auto.retrograde')}</th>
              <th className={thCls}>{t('auto.jaimini')}</th>
            </tr>
          </thead>
          <tbody>
            {planets.map((p: any, idx: number) => {
              const dignity = getDignity(p.planet, p.sign);
              const signType = SIGN_TYPE[p.sign] || '\u2014';
              const element = SIGN_ELEMENT[p.sign] || '\u2014';
              const nature = PLANET_NATURE[p.planet] || '\u2014';
              const isRetro = (p.status || '').toLowerCase().includes('retrograde') || (p.status || '').toLowerCase().includes(' r');
              const dignityColor = dignity === 'Exalted' ? '#16a34a' : dignity === 'Debilitated' ? '#dc2626' : dignity === 'Own Sign' ? '#2563eb' : undefined;
              const nakshatraName = translateNakshatra(p.nakshatra || '', language) || '\u2014';
              const pada = p.nakshatra_pada || (p.nakshatra || '').split(' Pada ')[1] || '\u2014';
              const signDeg = p.sign_degree != null ? Number(p.sign_degree) : null;
              const isSandhi = signDeg !== null && (signDeg < 1 || signDeg > 29);
              const karaka = planetKaraka[p.planet] || '\u2014';

              return (
                <tr key={idx} className={idx % 2 !== 0 ? 'bg-muted/5' : ''}>
                  <td className={`${tdCls} font-medium`}>
                    {translatePlanet(p.planet, language)}
                    {isRetro && <span className="text-red-500 ml-0.5" title={t('kundli.retrograde')}>*</span>}
                  </td>
                  <td className={tdCls}>{translateSign(p.sign, language)}</td>
                  <td className={tdCls}>
                    {signDeg !== null ? toDMS(signDeg) : '\u2014'}
                    {isSandhi && <span className="ml-1 px-1 py-0.5 rounded bg-amber-100 text-amber-700 font-medium text-[9px]">{t('auto.sandhi')}</span>}
                  </td>
                  <td className={tdCls}>{nakshatraName} ({t('auto.pada')} {pada})</td>
                  <td className={`${tdCls} text-center`}>{p.house}</td>
                  <td className={`${tdCls} font-medium`} style={dignityColor ? { color: dignityColor } : undefined}>
                    {translateLabel(dignity, language)}
                  </td>
                  <td className={tdCls}>{translateLabel(signType, language)}</td>
                  <td className={tdCls}>{translateLabel(element, language)}</td>
                  <td className={tdCls}>
                    <span className={`px-1.5 py-0.5 rounded text-[10px] font-semibold ${nature === 'Benefic' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                      {isHi ? (nature === 'Benefic' ? 'शुभ' : 'पापी') : nature}
                    </span>
                  </td>
                  <td className={tdCls} style={isRetro ? { color: '#dc2626' } : undefined}>
                    {isRetro ? `${t('common.yes')} ℞` : t('common.no')}
                  </td>
                  <td className={`${tdCls} font-semibold`} style={karaka !== '\u2014' ? { color: 'var(--aged-gold-dim)' } : undefined}>
                    {karaka}
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
