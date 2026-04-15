import { Sparkles, Loader2 } from 'lucide-react';
import { useState, useEffect } from 'react';
import { apiFetch } from '@/lib/api';
import { translatePlanet, translateRemedy } from '@/lib/backend-translations';
import { useTranslation } from '@/lib/i18n';
import { Heading } from '@/components/ui/heading';

interface GeneralRemediesProps {
  language: string;
  t?: (key: string) => string;
  title?: string;
  kundliId?: string;
}

// General remedies as fallback
const STATIC_REMEDIES = {
  hi: [
    {
      category: 'मंत्र जाप',
      items: [
        'प्रतिदिन सूर्य देवता को जल अर्पित करें',
        'शनिवार को शनिदेव के मंत्र "ॐ शं शनैश्चराय नमः" का जप करें',
        'मंगलवार को हनुमान चालीसा का पाठ करें',
      ]
    },
    {
      category: 'दान',
      items: [
        'गुरुवार को पीले वस्त्र या केले का दान करें',
        'शनिवार को काले तिल, सरसों का तेल या कंबल दान करें',
        'रविवार को गेहूं और गुड़ का दान करें',
      ]
    },
    {
      category: 'उपाय',
      items: [
        'प्रतिदिन सुबह स्नान के बाद धूप-दीप जलाएं',
        'मंदिर में नियमित दर्शन करें',
        'गाय को रोटी और गुड़ खिलाएं',
        'पीपल के वृक्ष की परिक्रमा करें',
      ]
    },
    {
      category: 'रत्न धारण',
      items: [
        'ज्योतिषी की सलाह से ही रत्न धारण करें',
        'रत्न शुद्ध करके ही पहनें',
        'शुक्ल पक्ष के गुरुवार को रत्न धारण करें',
      ]
    },
  ],
  en: [
    {
      category: 'Mantra Recitation',
      items: [
        'Offer water to Sun God daily',
        'Chant Shani mantra "Om Sham Shanishcharaya Namah" on Saturdays',
        'Read Hanuman Chalisa on Tuesdays',
      ]
    },
    {
      category: 'Donations',
      items: [
        'Donate yellow clothes or bananas on Thursdays',
        'Donate black sesame, mustard oil or blankets on Saturdays',
        'Donate wheat and jaggery on Sundays',
      ]
    },
    {
      category: 'Remedies',
      items: [
        'Light incense and lamp after bath daily',
        'Visit temples regularly',
        'Feed roti and jaggery to cows',
        'Circumambulate Peepal tree',
      ]
    },
    {
      category: 'Gemstones',
      items: [
        'Wear gemstones only after astrologer\'s advice',
        'Purify gemstones before wearing',
        'Wear gemstones on Thursday of Shukla Paksha',
      ]
    },
  ],
};

export default function GeneralRemedies({ language, t: tProp, title, kundliId }: GeneralRemediesProps) {
  const { t: tContext } = useTranslation();
  const t = tProp ?? tContext;
  const lang = language as any;
  const isHi = language === 'hi';
  const [dynamicRemedies, setDynamicRemedies] = useState<any[] | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (kundliId) {
      setLoading(true);
      apiFetch('/api/lalkitab/remedies', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ kundli_id: kundliId }),
      })
        .then(async (res) => {
          if (!res.ok) return null;
          return res.json();
        })
        .then((data) => {
          if (data?.remedies) setDynamicRemedies(data.remedies);
        })
        .catch(() => {})
        .finally(() => setLoading(false));
    }
  }, [kundliId]);

  const staticRemedies = isHi ? STATIC_REMEDIES.hi : STATIC_REMEDIES.en;
  const defaultTitle = t('auto.astrologicalRemedies');

  return (
    <div className="bg-muted rounded-xl p-5 border border-border mt-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Sparkles className="w-5 h-5 text-primary" />
          <Heading as={4} variant={4}>{title || defaultTitle}</Heading>
        </div>
        {loading && <Loader2 className="w-4 h-4 animate-spin text-primary" />}
      </div>
      
      {/* Dynamic Results if available */}
      {dynamicRemedies && dynamicRemedies.length > 0 && (
        <div className="mb-6 space-y-3">
          <Heading as={5} variant={5} className="text-primary border-b border-border/30 pb-1">
            {t('auto.basedOnYourChart')}
          </Heading>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {dynamicRemedies.map((rem, idx) => (
              <div key={idx} className="bg-muted/5 rounded-lg p-3 border border-border/20">
                <p className="text-sm font-semibold text-foreground">
                  {translatePlanet(rem.planet_en, lang)}
                </p>
                <p className="text-xs text-foreground mt-1">
                  {translateRemedy(rem.remedy_en, lang)}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Baseline / General */}
      <Heading as={5} variant={5} className="text-muted-foreground mb-3 uppercase tracking-wider">
        {t('auto.generalGuidance')}
      </Heading>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {staticRemedies.map((category, idx) => (
          <div key={idx} className="bg-white rounded-lg p-3 border border-border/30">
            <Heading as={5} variant={5} className="mb-2">{category.category}</Heading>
            <ul className="space-y-1">
              {category.items.map((item, itemIdx) => (
                <li key={itemIdx} className="text-sm text-foreground flex items-start gap-2">
                  <span className="w-1 h-1 rounded-full bg-primary mt-2 flex-shrink-0" />
                  {item}
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
      
      <p className="text-xs text-foreground mt-4 italic">
        {t('auto.noteTheseRemediesAre')}
      </p>
    </div>
  );
}
