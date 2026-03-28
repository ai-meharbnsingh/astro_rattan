import { useTranslation } from '@/lib/i18n';
import { SIGN_LORD, getHouseSignificance } from './kundli-utils';

interface LordshipsTabProps {
  planets: any[];
  houses: any;
}

export default function LordshipsTab({ planets, houses }: LordshipsTabProps) {
  const { t } = useTranslation();
  const HOUSE_SIGNIFICANCE = getHouseSignificance(t);

  return (
    <div className="space-y-4">
      <h4 className="font-sacred text-lg font-bold text-[#1a1a2e]">{t('kundli.houseLordships')}</h4>
      <div className="overflow-x-auto rounded-xl border" style={{ borderColor: 'rgba(139,115,85,0.2)' }}>
        <table className="w-full text-sm">
          <thead style={{ backgroundColor: '#E8E0D4' }}>
            <tr>
              <th className="text-left p-3 font-medium" style={{ color: '#B8860B' }}>{t('kundli.house')}</th>
              <th className="text-left p-3 font-medium" style={{ color: '#B8860B' }}>{t('kundli.sign')}</th>
              <th className="text-left p-3 font-medium" style={{ color: '#B8860B' }}>{t('kundli.lord')}</th>
              <th className="text-left p-3 font-medium" style={{ color: '#B8860B' }}>{t('kundli.placedIn')}</th>
              <th className="text-left p-3 font-medium" style={{ color: '#B8860B' }}>{t('kundli.significance')}</th>
            </tr>
          </thead>
          <tbody>
            {Array.from({ length: 12 }, (_, i) => {
              const houseNum = i + 1;
              // Houses can be an array or object
              const houseData = Array.isArray(houses) ? houses[i] : houses[houseNum] || houses[String(houseNum)];
              const houseSign = houseData?.sign || (Array.isArray(houses) ? houseData : '\u2014');
              const signName = typeof houseSign === 'string' ? houseSign : '\u2014';
              const lord = SIGN_LORD[signName] || '\u2014';

              // Find which house the lord sits in
              const lordPlanet = planets.find((p: any) => p.planet === lord);
              const lordPlacedIn = lordPlanet ? `House ${lordPlanet.house}` : '\u2014';

              return (
                <tr key={houseNum} className="border-t" style={{ borderColor: 'rgba(139,115,85,0.2)', backgroundColor: houseNum % 2 === 1 ? '#F5F0E8' : '#FDFBF7' }}>
                  <td className="p-3 font-medium" style={{ color: '#1a1a2e', fontFamily: 'serif' }}>{houseNum}</td>
                  <td className="p-3" style={{ color: '#1a1a2e' }}>{signName}</td>
                  <td className="p-3 font-medium" style={{ color: '#B8860B' }}>{lord}</td>
                  <td className="p-3" style={{ color: '#1a1a2e' }}>{lordPlacedIn}</td>
                  <td className="p-3" style={{ color: '#8B7355' }}>{HOUSE_SIGNIFICANCE[houseNum] || '\u2014'}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
