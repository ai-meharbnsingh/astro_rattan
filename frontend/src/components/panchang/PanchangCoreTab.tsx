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
    <div className="space-y-3">
      <div className="rounded-lg border border-cosmic-border overflow-x-auto">
        <table className="w-full min-w-[640px]">
          <thead className="bg-cosmic-card">
            <tr>
              <th className="text-left px-3 py-2 text-xs font-semibold text-cosmic-text-secondary">{language === 'hi' ? 'अंग' : 'Metric'}</th>
              <th className="text-left px-3 py-2 text-xs font-semibold text-cosmic-text-secondary">{language === 'hi' ? 'मान' : 'Value'}</th>
              <th className="text-left px-3 py-2 text-xs font-semibold text-cosmic-text-secondary">{language === 'hi' ? 'विवरण' : 'Details'}</th>
              <th className="text-left px-3 py-2 text-xs font-semibold text-cosmic-text-secondary">{language === 'hi' ? 'समाप्ति' : 'Ends'}</th>
            </tr>
          </thead>
          <tbody>
            {coreRows.map((row) => (
              <tr key={row.metric} className="border-t border-cosmic-border/80">
                <td className="px-3 py-2 text-sm font-medium text-cosmic-text-primary">{row.metric}</td>
                <td className="px-3 py-2 text-sm text-cosmic-text-primary">{row.value}</td>
                <td className="px-3 py-2 text-sm text-cosmic-text-secondary">{row.details}</td>
                <td className="px-3 py-2 text-sm text-sacred-gold">{row.endTime}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="rounded-lg border border-cosmic-border overflow-x-auto">
        <table className="w-full min-w-[640px]">
          <thead className="bg-cosmic-card">
            <tr>
              <th className="text-left px-3 py-2 text-xs font-semibold text-cosmic-text-secondary">{language === 'hi' ? 'समय' : 'Metric'}</th>
              <th className="text-left px-3 py-2 text-xs font-semibold text-cosmic-text-secondary">{language === 'hi' ? 'मान' : 'Value'}</th>
              <th className="text-left px-3 py-2 text-xs font-semibold text-cosmic-text-secondary">{language === 'hi' ? 'विवरण' : 'Details'}</th>
            </tr>
          </thead>
          <tbody>
            {sunMoonRows.map((row) => (
              <tr key={row.metric} className="border-t border-cosmic-border/80">
                <td className="px-3 py-2 text-sm font-medium text-cosmic-text-primary">{row.metric}</td>
                <td className="px-3 py-2 text-sm text-cosmic-text-primary">{row.value}</td>
                <td className="px-3 py-2 text-sm text-cosmic-text-secondary">{row.details}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="rounded-lg border border-sacred-gold/30 overflow-x-auto">
        <table className="w-full min-w-[640px]">
          <thead className="bg-sacred-gold/5">
            <tr>
              <th className="text-left px-3 py-2 text-xs font-semibold text-cosmic-text-secondary">{language === 'hi' ? 'दिन की अवधि' : 'Day Duration Metric'}</th>
              <th className="text-left px-3 py-2 text-xs font-semibold text-cosmic-text-secondary">{language === 'hi' ? 'मान' : 'Value'}</th>
              <th className="text-left px-3 py-2 text-xs font-semibold text-cosmic-text-secondary">{language === 'hi' ? 'विवरण' : 'Details'}</th>
            </tr>
          </thead>
          <tbody>
            {dayRows.map((row) => (
              <tr key={row.metric} className="border-t border-sacred-gold/20">
                <td className="px-3 py-2 text-sm font-medium text-cosmic-text-primary">{row.metric}</td>
                <td className="px-3 py-2 text-sm text-cosmic-text-primary">{row.value}</td>
                <td className="px-3 py-2 text-sm text-cosmic-text-secondary">{row.details}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
