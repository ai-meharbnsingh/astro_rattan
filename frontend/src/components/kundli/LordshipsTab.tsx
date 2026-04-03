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
    <div className="overflow-x-auto">
        <table className="w-full text-xs">
          <thead className="bg-sacred-gold/10">
            <tr>
              <th className="text-left p-2 font-medium text-sacred-gold-dark">House</th>
              <th className="text-left p-2 font-medium text-sacred-gold-dark">Sign</th>
              <th className="text-left p-2 font-medium text-sacred-gold-dark">Lord</th>
              <th className="text-left p-2 font-medium text-sacred-gold-dark">Placed In</th>
              <th className="text-left p-2 font-medium text-sacred-gold-dark">Significance</th>
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
                <tr key={houseNum} className={`border-t border-sacred-gold/10 text-xs ${houseNum % 2 === 0 ? 'bg-sacred-gold/[0.02]' : ''}`}>
                  <td className="p-2 font-medium text-sacred-brown font-display">{houseNum}</td>
                  <td className="p-2 text-sacred-brown">{signName}</td>
                  <td className="p-2 font-medium text-sacred-gold-dark">{lord}</td>
                  <td className="p-2 text-sacred-text-secondary">{lordPlacedIn}</td>
                  <td className="p-2 text-sacred-text-secondary">{HOUSE_SIGNIFICANCE[houseNum] || '\u2014'}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
    </div>
  );
}
