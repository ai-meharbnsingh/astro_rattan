import { Card, CardContent } from '@/components/ui/card';
import { Calendar, Sun, Moon, Clock, Info } from 'lucide-react';
import type { FullPanchangData } from '@/sections/Panchang';

interface Props {
  panchang: FullPanchangData;
  language: string;
  t: (key: string) => string;
}

const RITU_INFO: Record<string, { en: string; hi: string; description: { en: string; hi: string } }> = {
  'Vasanta': {
    en: 'Spring', hi: 'वसंत',
    description: { en: 'Season of new beginnings and growth', hi: 'नई शुरुआत और विकास का मौसम' }
  },
  'Grishma': {
    en: 'Summer', hi: 'ग्रीष्म',
    description: { en: 'Hot season, time of vitality', hi: 'गर्म मौसम, ऊर्जा का समय' }
  },
  'Varsha': {
    en: 'Monsoon', hi: 'वर्षा',
    description: { en: 'Rainy season, time of renewal', hi: 'बारिश का मौसम, नवीनीकरण का समय' }
  },
  'Sharada': {
    en: 'Autumn', hi: 'शरद',
    description: { en: 'Harvest season, time of abundance', hi: 'कटाई का मौसम, समृद्धि का समय' }
  },
  'Hemanta': {
    en: 'Pre-winter', hi: 'हेमंत',
    description: { en: 'Early winter, time of preservation', hi: 'प्रारंभिक शीतकाल, संरक्षण का समय' }
  },
  'Shishira': {
    en: 'Winter', hi: 'शिशिर',
    description: { en: 'Cold season, time of introspection', hi: 'ठंड का मौसम, आत्मनिरीक्षण का समय' }
  },
};

const AYANA_INFO: Record<string, { en: string; hi: string; meaning: { en: string; hi: string } }> = {
  'Uttarayana': {
    en: 'Uttarayana', hi: 'उत्तरायण',
    meaning: { en: 'Northward journey of Sun - Auspicious period', hi: 'सूर्य का उत्तरायण - शुभ काल' }
  },
  'Dakshinayana': {
    en: 'Dakshinayana', hi: 'दक्षिणायन',
    meaning: { en: 'Southward journey of Sun - Growth period', hi: 'सूर्य का दक्षिणायन - विकास काल' }
  },
};

const PAKSHA_INFO: Record<string, { en: string; hi: string }> = {
  'Shukla': { en: 'Waxing Moon', hi: 'शुक्ल पक्ष' },
  'Krishna': { en: 'Waning Moon', hi: 'कृष्ण पक्ष' },
};

const MAAS_INFO: Record<string, { en: string; hi: string; deity: { en: string; hi: string } }> = {
  'Chaitra': { en: 'Chaitra', hi: 'चैत्र', deity: { en: 'Vishnu', hi: 'विष्णु' } },
  'Vaishakha': { en: 'Vaishakha', hi: 'वैशाख', deity: { en: 'Vishnu', hi: 'विष्णु' } },
  'Jyeshtha': { en: 'Jyeshtha', hi: 'ज्येष्ठ', deity: { en: 'Shiva', hi: 'शिव' } },
  'Ashadha': { en: 'Ashadha', hi: 'आषाढ़', deity: { en: 'Shiva', hi: 'शिव' } },
  'Shravana': { en: 'Shravana', hi: 'श्रावण', deity: { en: 'Shiva', hi: 'शिव' } },
  'Bhadrapada': { en: 'Bhadrapada', hi: 'भाद्रपद', deity: { en: 'Shiva', hi: 'शिव' } },
  'Ashwina': { en: 'Ashwina', hi: 'आश्विन', deity: { en: 'Durga', hi: 'दुर्गा' } },
  'Kartika': { en: 'Kartika', hi: 'कार्तिक', deity: { en: 'Durga', hi: 'दुर्गा' } },
  'Margashirsha': { en: 'Margashirsha', hi: 'मार्गशीर्ष', deity: { en: 'Durga', hi: 'दुर्गा' } },
  'Pausha': { en: 'Pausha', hi: 'पौष', deity: { en: 'Durga', hi: 'दुर्गा' } },
  'Magha': { en: 'Magha', hi: 'माघ', deity: { en: 'Vishnu', hi: 'विष्णु' } },
  'Phalguna': { en: 'Phalguna', hi: 'फाल्गुन', deity: { en: 'Vishnu', hi: 'विष्णु' } },
};

export default function CalendarTab({ panchang, language, t }: Props) {
  const calendar = panchang.hindu_calendar;
  if (!calendar) return null;

  const rituInfo = RITU_INFO[calendar.ritu_english] || { en: calendar.ritu, hi: calendar.ritu, description: { en: '', hi: '' } };
  const ayanaInfo = AYANA_INFO[calendar.ayana] || { en: calendar.ayana, hi: calendar.ayana, meaning: { en: '', hi: '' } };
  const maasInfo = MAAS_INFO[calendar.maas] || { en: calendar.maas, hi: calendar.maas, deity: { en: '', hi: '' } };

  return (
    <div className="space-y-6">
      {/* Hindu Calendar Overview */}
      <Card className="card-sacred border-sacred-gold/30">
        <CardContent className="p-6">
          <h3 className="text-xl font-bold text-cosmic-text-primary mb-6 flex items-center gap-2">
            <Calendar className="h-6 w-6 text-sacred-gold" />
            {language === 'hi' ? 'हिंदू कैलेंडर' : 'Hindu Calendar'}
          </h3>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {/* Vikram Samvat */}
            <div className="p-4 rounded-xl bg-cosmic-card/50">
              <p className="text-sm text-cosmic-text-secondary mb-1">
                {language === 'hi' ? 'विक्रम संवत्' : 'Vikram Samvat'}
              </p>
              <p className="text-2xl font-bold text-sacred-gold">
                {calendar.vikram_samvat}
              </p>
              <p className="text-xs text-cosmic-text-secondary mt-1">
                {language === 'hi' ? 'हिंदू नव वर्ष' : 'Hindu New Year Era'}
              </p>
            </div>

            {/* Shaka Samvat */}
            <div className="p-4 rounded-xl bg-cosmic-card/50">
              <p className="text-sm text-cosmic-text-secondary mb-1">
                {language === 'hi' ? 'शक संवत्' : 'Shaka Samvat'}
              </p>
              <p className="text-2xl font-bold text-cosmic-text-primary">
                {calendar.shaka_samvat}
              </p>
              <p className="text-xs text-cosmic-text-secondary mt-1">
                {language === 'hi' ? 'राष्ट्रीय कैलेंडर' : 'National Calendar Era'}
              </p>
            </div>

            {/* Month */}
            <div className="p-4 rounded-xl bg-cosmic-card/50">
              <p className="text-sm text-cosmic-text-secondary mb-1">
                {language === 'hi' ? 'मास' : 'Month (Maas)'}
              </p>
              <p className="text-2xl font-bold text-cosmic-text-primary">
                {language === 'hi' ? calendar.maas_hindi || maasInfo.hi : maasInfo.en}
              </p>
              <p className="text-xs text-cosmic-text-secondary mt-1">
                {language === 'hi' 
                  ? `देवता: ${maasInfo.deity.hi}` 
                  : `Deity: ${maasInfo.deity.en}`}
              </p>
            </div>

            {/* Paksha */}
            <div className="p-4 rounded-xl bg-cosmic-card/50">
              <p className="text-sm text-cosmic-text-secondary mb-1">
                {language === 'hi' ? 'पक्ष' : 'Paksha (Lunar Fortnight)'}
              </p>
              <p className="text-2xl font-bold text-cosmic-text-primary">
                {language === 'hi' 
                  ? calendar.paksha_hindi || PAKSHA_INFO[calendar.paksha]?.hi || calendar.paksha
                  : PAKSHA_INFO[calendar.paksha]?.en || calendar.paksha}
              </p>
              <p className="text-xs text-cosmic-text-secondary mt-1">
                {language === 'hi' 
                  ? calendar.paksha === 'Shukla' ? 'बढ़ता चांद' : 'घटता चांद'
                  : calendar.paksha === 'Shukla' ? 'Waxing Moon' : 'Waning Moon'}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Season & Ayana */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <Card className="card-sacred">
          <CardContent className="p-4">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 rounded-lg bg-green-500/10">
                <Sun className="h-5 w-5 text-green-500" />
              </div>
              <div>
                <p className="text-sm text-cosmic-text-secondary">
                  {language === 'hi' ? 'ऋतु' : 'Season (Ritu)'}
                </p>
                <h4 className="text-xl font-bold text-cosmic-text-primary">
                  {language === 'hi' ? rituInfo.hi : rituInfo.en}
                </h4>
              </div>
            </div>
            <p className="text-sm text-cosmic-text-secondary">
              {language === 'hi' ? rituInfo.description.hi : rituInfo.description.en}
            </p>
          </CardContent>
        </Card>

        <Card className="card-sacred">
          <CardContent className="p-4">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 rounded-lg bg-orange-500/10">
                <Clock className="h-5 w-5 text-orange-500" />
              </div>
              <div>
                <p className="text-sm text-cosmic-text-secondary">
                  {language === 'hi' ? 'अयन' : 'Ayana (Sun\'s Journey)'}
                </p>
                <h4 className="text-xl font-bold text-cosmic-text-primary">
                  {language === 'hi' ? ayanaInfo.hi : ayanaInfo.en}
                </h4>
              </div>
            </div>
            <p className="text-sm text-cosmic-text-secondary">
              {language === 'hi' ? ayanaInfo.meaning.hi : ayanaInfo.meaning.en}
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Calendar Info */}
      <Card className="card-sacred">
        <CardContent className="p-4">
          <div className="flex items-start gap-3">
            <Info className="h-5 w-5 text-sacred-gold mt-0.5" />
            <div>
              <h4 className="font-semibold text-cosmic-text-primary mb-2">
                {language === 'hi' ? 'हिंदू कैलेंडर के बारे में' : 'About Hindu Calendar'}
              </h4>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm text-cosmic-text-secondary">
                <div>
                  <strong className="text-cosmic-text-primary">
                    {language === 'hi' ? 'विक्रम संवत्:' : 'Vikram Samvat:'}
                  </strong>
                  <p className="mt-1">
                    {language === 'hi' 
                      ? 'राजा विक्रमादित्य द्वारा प्रारंभ किया गया। यह भारत का प्रमुख हिंदू कैलेंडर है।'
                      : 'Started by King Vikramaditya. This is the main Hindu calendar of India.'}
                  </p>
                </div>
                <div>
                  <strong className="text-cosmic-text-primary">
                    {language === 'hi' ? 'शक संवत्:' : 'Shaka Samvat:'}
                  </strong>
                  <p className="mt-1">
                    {language === 'hi' 
                      ? 'भारत का राष्ट्रीय कैलेंडर। 1957 में अपनाया गया।'
                      : 'India\'s national calendar. Adopted in 1957.'}
                  </p>
                </div>
                <div>
                  <strong className="text-cosmic-text-primary">
                    {language === 'hi' ? 'अयन:' : 'Ayana:'}
                  </strong>
                  <p className="mt-1">
                    {language === 'hi' 
                      ? 'सूर्य का उत्तरायण 6 महीने और दक्षिणायन 6 महीने रहता है।'
                      : 'Sun remains in Uttarayana for 6 months and Dakshinayana for 6 months.'}
                  </p>
                </div>
                <div>
                  <strong className="text-cosmic-text-primary">
                    {language === 'hi' ? 'ऋतु:' : 'Ritu:'}
                  </strong>
                  <p className="mt-1">
                    {language === 'hi' 
                      ? 'भारतीय कैलेंडर में 6 ऋतुएं होती हैं - वसंत, ग्रीष्म, वर्षा, शरद, हेमंत, शिशिर।'
                      : 'Indian calendar has 6 seasons - Spring, Summer, Monsoon, Autumn, Pre-winter, Winter.'}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
