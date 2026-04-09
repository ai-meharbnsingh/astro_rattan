import { useTranslation } from '@/lib/i18n';
import { translatePlanet, translateSign } from '@/lib/backend-translations';
import { SIGN_LORD, getHouseSignificance } from './kundli-utils';

interface LordshipsTabProps {
  planets: any[];
  houses: any;
}

export default function LordshipsTab({ planets, houses }: LordshipsTabProps) {
  const { t, language } = useTranslation();
  const HOUSE_SIGNIFICANCE = getHouseSignificance(t);

  return (
    <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="bg-sacred-gold">
            <tr>
              <th className="text-left p-2 font-medium text-sacred-gold-dark">{language === 'hi' ? 'भाव' : 'House'}</th>
              <th className="text-left p-2 font-medium text-sacred-gold-dark">{language === 'hi' ? 'राशि' : 'Sign'}</th>
              <th className="text-left p-2 font-medium text-sacred-gold-dark">{language === 'hi' ? 'स्वामी' : 'Lord'}</th>
              <th className="text-left p-2 font-medium text-sacred-gold-dark">{language === 'hi' ? 'स्थित' : 'Placed In'}</th>
              <th className="text-left p-2 font-medium text-sacred-gold-dark">{language === 'hi' ? 'महत्व' : 'Significance'}</th>
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
              const lordPlacedIn = lordPlanet ? `${language === 'hi' ? 'भाव' : 'House'} ${lordPlanet.house}` : '\u2014';

              return (
                <tr key={houseNum} className={`border-t border-sacred-gold text-sm ${houseNum % 2 === 0 ? 'bg-sacred-gold/[0.02]' : ''}`}>
                  <td className="p-2 font-medium text-sacred-brown font-display">{houseNum}</td>
                  <td className="p-2 text-sacred-brown">{translateSign(signName, language)}</td>
                  <td className="p-2 font-medium text-sacred-gold-dark">{translatePlanet(lord, language)}</td>
                  <td className="p-2 text-cosmic-text">{lordPlacedIn}</td>
                  <td className="p-2 text-cosmic-text">{HOUSE_SIGNIFICANCE[houseNum] || '\u2014'}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
    </div>
  );
}
