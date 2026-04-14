import type { FullPanchangData } from '@/sections/Panchang';

interface Props {
  panchang: FullPanchangData;
  language: string;
  t: (key: string) => string;
}

export default function PanchangCoreTab({ panchang, language, t }: Props) {
  const coreRows = [
    {
      metric: language === 'hi' ? 'तिथि' : t('panchang.tithi'),
      value: language === 'hi' ? panchang.tithi.name_hindi || panchang.tithi.name : panchang.tithi.name,
      details: `${language === 'hi' ? 'संख्या' : 'No.'} ${panchang.tithi.number} • ${language === 'hi' ? panchang.tithi.paksha_hindi || panchang.tithi.paksha : panchang.tithi.paksha}`,
      endTime: panchang.tithi.end_time || '--',
    },
    {
      metric: language === 'hi' ? 'नक्षत्र' : t('panchang.nakshatra'),
      value: language === 'hi' ? panchang.nakshatra.name_hindi || panchang.nakshatra.name : panchang.nakshatra.name,
      details: `${language === 'hi' ? 'पाद' : 'Pada'} ${panchang.nakshatra.pada} • ${language === 'hi' ? 'स्वामी' : 'Lord'} ${language === 'hi' ? panchang.nakshatra.lord_hindi || panchang.nakshatra.lord : panchang.nakshatra.lord}`,
      endTime: panchang.nakshatra.end_time || '--',
    },
    {
      metric: language === 'hi' ? 'योग' : t('panchang.yoga'),
      value: language === 'hi' ? panchang.yoga.name_hindi || panchang.yoga.name : panchang.yoga.name,
      details: `${language === 'hi' ? 'संख्या' : 'No.'} ${panchang.yoga.number}`,
      endTime: panchang.yoga.end_time || '--',
    },
    {
      metric: language === 'hi' ? 'करण' : t('panchang.karana'),
      value: language === 'hi' ? panchang.karana.name_hindi || panchang.karana.name : panchang.karana.name,
      details: `${language === 'hi' ? 'संख्या' : 'No.'} ${panchang.karana.number}`,
      endTime: panchang.karana.end_time || '--',
    },
  ];

  const sunMoonRows = [
    {
      metric: language === 'hi' ? 'सूर्योदय' : t('panchang.sunrise'),
      value: panchang.sunrise || '--',
      details: language === 'hi' ? 'दिन आरंभ' : 'Day start',
    },
    {
      metric: language === 'hi' ? 'सूर्यास्त' : t('panchang.sunset'),
      value: panchang.sunset || '--',
      details: language === 'hi' ? 'दिन समाप्ति' : 'Day end',
    },
    {
      metric: language === 'hi' ? 'चंद्रोदय' : t('panchang.moonrise'),
      value: panchang.moonrise || '--',
      details: language === 'hi' ? 'चंद्र उदय' : 'Moon rise',
    },
    {
      metric: language === 'hi' ? 'चंद्रास्त' : t('panchang.moonset'),
      value: panchang.moonset || '--',
      details: language === 'hi' ? 'चंद्र अस्त' : 'Moon set',
    },
  ];

  const dayRows = [
    {
      metric: language === 'hi' ? 'दिनमान' : 'Day Length',
      value: panchang.dinamana || '--',
      details: language === 'hi' ? 'कुल दिन अवधि' : 'Total daylight',
    },
    {
      metric: language === 'hi' ? 'रात्रिमान' : 'Night Length',
      value: panchang.ratrimana || '--',
      details: language === 'hi' ? 'कुल रात्रि अवधि' : 'Total nighttime',
    },
    {
      metric: language === 'hi' ? 'मध्याह्न' : 'Mid-day',
      value: panchang.madhyahna || '--',
      details: language === 'hi' ? 'मध्य समय' : 'Middle of day',
    },
    {
      metric: language === 'hi' ? 'वार' : 'Weekday',
      value: language === 'hi' ? panchang.vaar?.name_hindi || panchang.vaar?.name || '--' : panchang.vaar?.name || '--',
      details: language === 'hi' ? 'दिन का नाम' : 'Day name',
    },
  ];

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-3">
      <div className="rounded-lg border border-cosmic-border p-2">
        <h3 className="font-bold text-cosmic-text-primary mb-1">
          {language === 'hi' ? 'तिथि / नक्षत्र / योग / करण' : 'Tithi / Nakshatra / Yoga / Karana'}
        </h3>
        <table className="w-full table-fixed text-xs sm:text-sm">
          <thead>
            <tr className="bg-sacred-gold/15">
              <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[22%]">{language === 'hi' ? 'अंग' : 'Metric'}</th>
              <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[24%]">{language === 'hi' ? 'मान' : 'Value'}</th>
              <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[34%]">{language === 'hi' ? 'विवरण' : 'Details'}</th>
              <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[20%]">{language === 'hi' ? 'समाप्ति' : 'Ends'}</th>
            </tr>
          </thead>
          <tbody>
            {coreRows.map((row) => (
              <tr key={row.metric} className="border-b border-cosmic-border/50 last:border-0 align-top">
                <td className="px-2 py-1 font-medium text-cosmic-text-primary whitespace-normal break-words">{row.metric}</td>
                <td className="px-2 py-1 text-cosmic-text-primary whitespace-normal break-words">{row.value}</td>
                <td className="px-2 py-1 text-cosmic-text-secondary whitespace-normal break-words">{row.details}</td>
                <td className="px-2 py-1 text-sacred-gold whitespace-normal break-words">{row.endTime}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="rounded-lg border border-cosmic-border p-2">
        <h3 className="font-bold text-cosmic-text-primary mb-1">
          {language === 'hi' ? 'सूर्य और चंद्र समय' : 'Sun and Moon Times'}
        </h3>
        <table className="w-full table-fixed text-xs sm:text-sm">
          <thead>
            <tr className="bg-sacred-gold/15">
              <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[34%]">{language === 'hi' ? 'समय' : 'Metric'}</th>
              <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[28%]">{language === 'hi' ? 'मान' : 'Value'}</th>
              <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[38%]">{language === 'hi' ? 'विवरण' : 'Details'}</th>
            </tr>
          </thead>
          <tbody>
            {sunMoonRows.map((row) => (
              <tr key={row.metric} className="border-b border-cosmic-border/50 last:border-0 align-top">
                <td className="px-2 py-1 font-medium text-cosmic-text-primary whitespace-normal break-words">{row.metric}</td>
                <td className="px-2 py-1 text-cosmic-text-primary whitespace-normal break-words">{row.value}</td>
                <td className="px-2 py-1 text-cosmic-text-secondary whitespace-normal break-words">{row.details}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="rounded-lg border border-cosmic-border p-2">
        <h3 className="font-bold text-cosmic-text-primary mb-1">
          {language === 'hi' ? 'दिन की अवधि' : 'Day Duration'}
        </h3>
        <table className="w-full table-fixed text-xs sm:text-sm">
          <thead>
            <tr className="bg-sacred-gold/15">
              <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[34%]">{language === 'hi' ? 'काल' : 'Metric'}</th>
              <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[28%]">{language === 'hi' ? 'मान' : 'Value'}</th>
              <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[38%]">{language === 'hi' ? 'विवरण' : 'Details'}</th>
            </tr>
          </thead>
          <tbody>
            {dayRows.map((row) => (
              <tr key={row.metric} className="border-b border-cosmic-border/50 last:border-0 align-top">
                <td className="px-2 py-1 font-medium text-cosmic-text-primary whitespace-normal break-words">{row.metric}</td>
                <td className="px-2 py-1 text-cosmic-text-primary whitespace-normal break-words">{row.value}</td>
                <td className="px-2 py-1 text-cosmic-text-secondary whitespace-normal break-words">{row.details}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
