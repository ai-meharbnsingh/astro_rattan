import { useTranslation } from '@/lib/i18n';
import { translatePlanet, translateSign } from '@/lib/backend-translations';
import { SIGN_LORD } from './kundli-utils';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell, TableCaption, TableFooter } from '@/components/ui/table';

interface LordshipsTabProps {
  planets: any[];
  houses: any;
}

// House significance with direct Hindi translations
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

export default function LordshipsTab({ planets, houses }: LordshipsTabProps) {
  const { language, t } = useTranslation();
  const HOUSE_SIGNIFICANCE = language === 'hi' ? HOUSE_SIGNIFICANCE_HI : HOUSE_SIGNIFICANCE_EN;

  return (
    <div className="overflow-x-auto rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
        <Table className="w-full text-xs">
          <TableHeader>
            <TableRow>
              <TableHead className="text-left">{t('auto.house')}</TableHead>
              <TableHead className="text-left">{t('auto.sign')}</TableHead>
              <TableHead className="text-left">{t('auto.lord')}</TableHead>
              <TableHead className="text-left">{t('auto.placedIn')}</TableHead>
              <TableHead className="text-left">{t('auto.significance')}</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {Array.from({ length: 12 }, (_, i) => {
              const houseNum = i + 1;
              // Houses can be an array or object
              const houseData = Array.isArray(houses) ? houses[i] : houses[houseNum] || houses[String(houseNum)];
              const houseSign = houseData?.sign || (Array.isArray(houses) ? houseData : '\u2014');
              const signName = typeof houseSign === 'string' ? houseSign : '\u2014';
              const lord = SIGN_LORD[signName] || '\u2014';

              // Find which house the lord sits in
              const lordPlanet = planets.find((p: any) => p.planet === lord);
              const lordPlacedIn = lordPlanet ? `${t('auto.house')} ${lordPlanet.house}` : '\u2014';

              return (
                <TableRow key={houseNum}>
                  <TableCell className="font-medium text-foreground">{houseNum}</TableCell>
                  <TableCell className="text-foreground">{translateSign(signName, language)}</TableCell>
                  <TableCell className="font-medium text-foreground">{translatePlanet(lord, language)}</TableCell>
                  <TableCell className="text-foreground">{lordPlacedIn}</TableCell>
                  <TableCell className="text-foreground">{HOUSE_SIGNIFICANCE[houseNum] || '\u2014'}</TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
    </div>
  );
}
