import { useMemo } from 'react';
import { getDignity, SIGN_TYPE, SIGN_ELEMENT, PLANET_NATURE, toDMS } from './kundli-utils';
import { calculateJaiminiKarakas } from './jhora-utils';
import { useTranslation } from '@/lib/i18n';
import { translatePlanet, translateSign, translateNakshatra, translateLabel } from '@/lib/backend-translations';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell, TableCaption, TableFooter } from '@/components/ui/table';

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
    <div className="overflow-x-auto rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
        <Table className="w-full text-sm">
          <TableHeader className="bg-muted">
            <TableRow>
              <TableHead className="text-left p-2 font-medium text-primary">{t('auto.planet')}</TableHead>
              <TableHead className="text-left p-2 font-medium text-primary">{t('auto.sign')}</TableHead>
              <TableHead className="text-left p-2 font-medium text-primary">{t('auto.degree')}</TableHead>
              <TableHead className="text-left p-2 font-medium text-primary">{t('auto.nakshatra')}</TableHead>
              <TableHead className="text-left p-2 font-medium text-primary">{t('auto.house')}</TableHead>
              <TableHead className="text-left p-2 font-medium text-primary">{t('auto.dignity')}</TableHead>
              <TableHead className="text-left p-2 font-medium text-primary">{t('auto.signType')}</TableHead>
              <TableHead className="text-left p-2 font-medium text-primary">{t('auto.element')}</TableHead>
              <TableHead className="text-left p-2 font-medium text-primary">{t('auto.nature')}</TableHead>
              <TableHead className="text-left p-2 font-medium text-primary">{t('auto.retrograde')}</TableHead>
              <TableHead className="text-left p-2 font-medium text-primary">{t('auto.jaimini')}</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
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
                <TableRow key={idx} className={`border-t border-border text-sm ${idx % 2 === 0 ? '' : 'bg-muted/5'}`}>
                  <TableCell className="p-2 font-medium text-foreground">
                    {translatePlanet(p.planet, language)}
                    {isRetro && <span className="text-red-500 ml-0.5" title={t('kundli.retrograde')}>*</span>}
                  </TableCell>
                  <TableCell className="p-2 text-foreground">{translateSign(p.sign, language)}</TableCell>
                  <TableCell className="p-2 text-foreground">
                    {signDeg !== null ? toDMS(signDeg) : '\u2014'}
                    {isSandhi && <span className="ml-1 text-sm px-1 py-0.5 rounded bg-amber-500 text-amber-600 font-medium">{t('auto.sandhi')}</span>}
                  </TableCell>
                  <TableCell className="p-2 text-foreground">{nakshatraName} ({t('auto.pada')} {pada})</TableCell>
                  <TableCell className="p-2 text-foreground">{p.house}</TableCell>
                  <TableCell className="p-2 font-medium" style={{ color: dignityColor }}>{translateLabel(dignity, language)}</TableCell>
                  <TableCell className="p-2 text-foreground">{translateLabel(signType, language)}</TableCell>
                  <TableCell className="p-2 text-foreground">{translateLabel(element, language)}</TableCell>
                  <TableCell className="p-2">
                    <span className={`text-sm px-2 py-0.5 rounded-full ${nature === 'Benefic' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                      {language === 'hi' ? (nature === 'Benefic' ? 'शुभ' : 'पापी') : nature}
                    </span>
                  </TableCell>
                  <TableCell className="p-2" style={{ color: isRetro ? '#dc2626' : 'var(--ink-light)' }}>
                    {isRetro ? `${t('common.yes')} ℞` : t('common.no')}
                  </TableCell>
                  <TableCell className="p-2 font-semibold" style={{ color: karaka !== '\u2014' ? 'var(--aged-gold-dim)' : 'var(--ink-light)' }}>
                    {karaka}
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </div>
  );
}
