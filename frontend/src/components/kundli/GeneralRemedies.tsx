import { Sparkles } from 'lucide-react';

interface GeneralRemediesProps {
  language: string;
  t?: (key: string) => string;
  title?: string;
}

// General remedies for all tabs
const REMEDIES = {
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

export default function GeneralRemedies({ language, t, title }: GeneralRemediesProps) {
  void t;
  const remedies = language === 'hi' ? REMEDIES.hi : REMEDIES.en;
  const defaultTitle = language === 'hi' ? 'सामान्य उपाय' : 'General Remedies';

  return (
    <div className="bg-sacred-cream rounded-xl p-5 border border-sacred-gold mt-6">
      <div className="flex items-center gap-2 mb-4">
        <Sparkles className="w-5 h-5 text-sacred-gold-dark" />
        <h4 className="text-lg font-semibold text-gray-800">{title || defaultTitle}</h4>
      </div>
      
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {remedies.map((category, idx) => (
          <div key={idx} className="bg-white rounded-lg p-3 border border-sacred-gold/30">
            <h5 className="font-semibold text-sacred-brown mb-2 text-sm">{category.category}</h5>
            <ul className="space-y-1">
              {category.items.map((item, itemIdx) => (
                <li key={itemIdx} className="text-sm text-cosmic-text flex items-start gap-2">
                  <span className="w-1 h-1 rounded-full bg-sacred-gold-dark mt-2 flex-shrink-0" />
                  {item}
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
      
      <p className="text-xs text-cosmic-text mt-4 italic">
        {language === 'hi' 
          ? 'नोट: ये सामान्य उपाय हैं। व्यक्तिगत परामर्श के लिए किसी अनुभवी ज्योतिषी से मिलें।'
          : 'Note: These are general remedies. Consult an experienced astrologer for personalized guidance.'}
      </p>
    </div>
  );
}
