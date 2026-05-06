import { useTranslation } from '@/lib/i18n';
import { translatePlanet, translateSign } from '@/lib/backend-translations';
import { SIGN_LORD } from './kundli-utils';
import { Heading } from '@/components/ui/heading';
import { Crown } from 'lucide-react';

interface LordshipsTabProps {
  planets: any[];
  houses: any;
}

const HOUSE_SIGNIFICANCE_HI: Record<number, string> = {
  1: 'स्वयं, व्यक्तित्व, रूप',
  2: 'धन, परिवार, वाणी',
  3: 'साहस, भाई-बहन, संचार',
  4: 'घर, माता, सुख',
  5: 'संतान, शिक्षा, रचनात्मकता',
  6: 'स्वास्थ्य, शत्रु, सेवा',
  7: 'विवाह, साझेदारी, व्यापार',
  8: 'आयु, रूपांतरण, गुप्त विद्या',
  9: 'भाग्य, धर्म, उच्च शिक्षा',
  10: 'कर्म, प्रतिष्ठा, अधिकार',
  11: 'लाभ, आकांक्षाएं, मित्र',
  12: 'हानि, मोक्ष, विदेश',
};

const HOUSE_SIGNIFICANCE_EN: Record<number, string> = {
  1: 'Self, Personality, Appearance',
  2: 'Wealth, Family, Speech',
  3: 'Courage, Siblings, Communication',
  4: 'Home, Mother, Comfort',
  5: 'Children, Education, Creativity',
  6: 'Health, Enemies, Service',
  7: 'Marriage, Partnership, Business',
  8: 'Longevity, Transformation, Occult',
  9: 'Fortune, Dharma, Higher Learning',
  10: 'Career, Status, Authority',
  11: 'Gains, Aspirations, Friends',
  12: 'Losses, Moksha, Foreign Lands',
};

const ohContainer = 'rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden';
const ohHeader    = 'bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2';
const thCls       = 'p-1.5 text-left text-[10px] font-semibold uppercase tracking-wide text-primary border-b border-border';
const tdCls       = 'p-1.5 text-xs text-foreground border-t border-border align-top break-words overflow-hidden';

export default function LordshipsTab({ planets, houses }: LordshipsTabProps) {
  const { language, t } = useTranslation();
  const isHi = language === 'hi';
  const HOUSE_SIGNIFICANCE = isHi ? HOUSE_SIGNIFICANCE_HI : HOUSE_SIGNIFICANCE_EN;

  return (
    <div className="space-y-4">
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
          <Crown className="w-6 h-6" />
          {isHi ? 'भाव स्वामित्व' : 'House Lordships'}
        </Heading>
        <p className="text-sm text-muted-foreground">
          {isHi ? 'प्रत्येक भाव का राशि, स्वामी एवं स्थान' : 'Sign, lord and placement for each house'}
        </p>
      </div>
      <div className={ohContainer}>
      <div className={ohHeader}>
        <span>{isHi ? 'भाव स्वामित्व' : 'House Lordships'}</span>
      </div>
      <div className="overflow-x-auto">
      <table style={{ tableLayout: 'fixed', minWidth: '480px', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
        <colgroup>
          <col style={{ width: '8%' }} />
          <col style={{ width: '16%' }} />
          <col style={{ width: '16%' }} />
          <col style={{ width: '16%' }} />
          <col style={{ width: '44%' }} />
        </colgroup>
        <thead>
          <tr>
            <th className={thCls}>{t('auto.house')}</th>
            <th className={thCls}>{t('auto.sign')}</th>
            <th className={thCls}>{t('auto.lord')}</th>
            <th className={thCls}>{t('auto.placedIn')}</th>
            <th className={thCls}>{t('auto.significance')}</th>
          </tr>
        </thead>
        <tbody>
          {Array.from({ length: 12 }, (_, i) => {
            const houseNum = i + 1;
            const houseData = Array.isArray(houses) ? houses[i] : houses[houseNum] || houses[String(houseNum)];
            const houseSign = houseData?.sign || (Array.isArray(houses) ? houseData : '\u2014');
            const signName = typeof houseSign === 'string' ? houseSign : '\u2014';
            const lord = SIGN_LORD[signName] || '\u2014';

            const lordPlanet = planets.find((p: any) => p.planet === lord);
            const lordPlacedIn = lordPlanet ? `${t('auto.house')} ${lordPlanet.house}` : '\u2014';

            return (
              <tr key={houseNum}>
                <td className={`${tdCls} font-medium text-center`}>{houseNum}</td>
                <td className={tdCls}>{translateSign(signName, language)}</td>
                <td className={`${tdCls} font-medium`}>{translatePlanet(lord, language)}</td>
                <td className={tdCls}>{lordPlacedIn}</td>
                <td className={tdCls}>{HOUSE_SIGNIFICANCE[houseNum] || '\u2014'}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
      </div>
      </div>
    </div>
  );
}
