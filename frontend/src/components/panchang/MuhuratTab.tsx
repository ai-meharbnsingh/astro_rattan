import { AlertTriangle, CheckCircle2, Sparkles, Sunrise } from 'lucide-react';
import type { FullPanchangData } from '@/sections/Panchang';

interface Props {
  panchang: FullPanchangData;
  language: string;
  t: (key: string) => string;
}

export default function MuhuratTab({ panchang, language, t }: Props) {
  // Inauspicious periods
  const inauspiciousPeriods = [
    {
      key: 'rahu_kaal',
      name: language === 'hi' ? 'राहु काल' : 'Rahu Kaal',
      period: panchang.rahu_kaal,
      desc: language === 'hi' ? 'अशुभ समय - कोई भी शुभ कार्य न करें' : 'Inauspicious - avoid new beginnings'
    },
    {
      key: 'gulika_kaal',
      name: language === 'hi' ? 'गुलिक काल' : 'Gulika Kaal',
      period: panchang.gulika_kaal,
      desc: language === 'hi' ? 'मिश्रित फल' : 'Mixed results'
    },
    {
      key: 'yamaganda',
      name: language === 'hi' ? 'यमगंड' : 'Yamaganda',
      period: panchang.yamaganda,
      desc: language === 'hi' ? 'यम का समय - यात्रा से बचें' : 'Yama time - avoid travel'
    },
    {
      key: 'dur_muhurtam',
      name: language === 'hi' ? 'दुर्मुहूर्त' : 'Dur Muhurtam',
      period: panchang.dur_muhurtam,
      desc: language === 'hi' ? 'अत्यंत अशुभ' : 'Highly inauspicious'
    },
    {
      key: 'varjyam',
      name: language === 'hi' ? 'वर्ज्य' : 'Varjyam',
      period: panchang.varjyam,
      desc: language === 'hi' ? 'वर्जित समय' : 'Prohibited time'
    },
  ].filter(p => p.period && (p.period.start !== '--:--' || p.period.end !== '--:--'));

  // Auspicious periods
  const auspiciousPeriods = [
    {
      key: 'brahma_muhurat',
      name: language === 'hi' ? 'ब्रह्म मुहूर्त' : 'Brahma Muhurat',
      period: panchang.brahma_muhurat,
      desc: language === 'hi' ? 'सबसे शुभ - ध्यान और पूजा के लिए' : 'Most auspicious - meditation & puja'
    },
    {
      key: 'abhijit_muhurat',
      name: language === 'hi' ? 'अभिजित मुहूर्त' : 'Abhijit Muhurat',
      period: panchang.abhijit_muhurat,
      desc: language === 'hi' ? 'विजय का समय - कोई भी कार्य सफल' : 'Victory time - any work succeeds'
    },
    {
      key: 'vijaya_muhurta',
      name: language === 'hi' ? 'विजया मुहूर्त' : 'Vijaya Muhurta',
      period: panchang.vijaya_muhurta,
      desc: language === 'hi' ? 'विजय प्राप्ति का समय' : 'Time for victory'
    },
    {
      key: 'godhuli_muhurta',
      name: language === 'hi' ? 'गोधूलि मुहूर्त' : 'Godhuli Muhurta',
      period: panchang.godhuli_muhurta,
      desc: language === 'hi' ? 'गायों के घर लौटने का समय - शुभ' : 'When cows return - auspicious'
    },
    {
      key: 'nishita_muhurta',
      name: language === 'hi' ? 'निशीथ मुहूर्त' : 'Nishita Muhurta',
      period: panchang.nishita_muhurta,
      desc: language === 'hi' ? 'रात्रि का शुभ समय' : 'Auspicious night time'
    },
  ].filter(p => p.period && (p.period.start !== '--:--' || p.period.end !== '--:--'));

  // Special Yogas
  const specialYogas = [
    { key: 'ravi_yoga', name: language === 'hi' ? 'रवि योग' : 'Ravi Yoga', data: panchang.ravi_yoga },
    { key: 'amrit_siddhi', name: language === 'hi' ? 'अमृत सिद्धि' : 'Amrit Siddhi', data: panchang.amrit_siddhi },
    { key: 'sarvartha_siddhi', name: language === 'hi' ? 'सर्वार्थ सिद्धि' : 'Sarvartha Siddhi', data: panchang.sarvartha_siddhi },
    { key: 'tripushkar', name: language === 'hi' ? 'त्रिपुष्कर' : 'Tripushkar', data: panchang.tripushkar },
    { key: 'dwipushkar', name: language === 'hi' ? 'द्विपुष्कर' : 'Dwipushkar', data: panchang.dwipushkar },
  ].filter(y => y.data && (y.data.active || (y.data.start && y.data.end)));

  const sandhyaRows = [
    {
      key: 'pratah_sandhya',
      name: language === 'hi' ? 'प्रातः संध्या' : 'Pratah Sandhya',
      period: panchang.pratah_sandhya,
      desc: language === 'hi' ? 'गायत्री जप का समय' : 'Time for Gayatri Japa',
    },
    {
      key: 'sayahna_sandhya',
      name: language === 'hi' ? 'सायंह्न संध्या' : 'Sayahna Sandhya',
      period: panchang.sayahna_sandhya,
      desc: language === 'hi' ? 'सन्ध्या जप का समय' : 'Time for Sandhya Japa',
    },
  ].filter(s => s.period && (s.period.start !== '--:--' || s.period.end !== '--:--'));

  return (
    <div className="space-y-3">
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-3">
        <div className="rounded-lg border border-green-500/30 p-2">
          <h3 className="font-bold text-cosmic-text-primary mb-1 flex items-center gap-1">
            <CheckCircle2 className="h-4 w-4" />
            {language === 'hi' ? 'शुभ मुहूर्त (उपयुक्त समय)' : 'Auspicious Muhurats (Good Times)'}
          </h3>
          <table className="w-full table-fixed text-xs sm:text-sm">
            <thead>
              <tr className="bg-green-500/15">
                <th className="text-left px-2 py-1 text-green-700 font-semibold w-[28%]">{language === 'hi' ? 'मुहूर्त' : 'Muhurta'}</th>
                <th className="text-left px-2 py-1 text-green-700 font-semibold w-[18%]">{language === 'hi' ? 'आरंभ' : 'Start'}</th>
                <th className="text-left px-2 py-1 text-green-700 font-semibold w-[18%]">{language === 'hi' ? 'समाप्ति' : 'End'}</th>
                <th className="text-left px-2 py-1 text-green-700 font-semibold w-[36%]">{language === 'hi' ? 'टिप्पणी' : 'Notes'}</th>
              </tr>
            </thead>
            <tbody>
              {auspiciousPeriods.map((period) => (
                <tr key={period.key} className="border-b border-cosmic-border/50 last:border-0 align-top">
                  <td className="px-2 py-1 font-medium text-cosmic-text-primary whitespace-normal break-words">{period.name}</td>
                  <td className="px-2 py-1 text-cosmic-text-primary">{period.period?.start || '--'}</td>
                  <td className="px-2 py-1 text-cosmic-text-primary">{period.period?.end || '--'}</td>
                  <td className="px-2 py-1 text-cosmic-text-secondary whitespace-normal break-words">{period.desc}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="rounded-lg border border-red-500/30 p-2">
          <h3 className="font-bold text-cosmic-text-primary mb-1 flex items-center gap-1">
            <AlertTriangle className="h-4 w-4" />
            {language === 'hi' ? 'अशुभ समय (वर्जित)' : 'Inauspicious Times (Avoid)'}
          </h3>
          <table className="w-full table-fixed text-xs sm:text-sm">
            <thead>
              <tr className="bg-red-500/15">
                <th className="text-left px-2 py-1 text-red-700 font-semibold w-[28%]">{language === 'hi' ? 'काल' : 'Period'}</th>
                <th className="text-left px-2 py-1 text-red-700 font-semibold w-[18%]">{language === 'hi' ? 'आरंभ' : 'Start'}</th>
                <th className="text-left px-2 py-1 text-red-700 font-semibold w-[18%]">{language === 'hi' ? 'समाप्ति' : 'End'}</th>
                <th className="text-left px-2 py-1 text-red-700 font-semibold w-[36%]">{language === 'hi' ? 'टिप्पणी' : 'Notes'}</th>
              </tr>
            </thead>
            <tbody>
              {inauspiciousPeriods.map((period) => (
                <tr key={period.key} className="border-b border-cosmic-border/50 last:border-0 align-top">
                  <td className="px-2 py-1 font-medium text-cosmic-text-primary whitespace-normal break-words">{period.name}</td>
                  <td className="px-2 py-1 text-cosmic-text-primary">{period.period?.start || '--'}</td>
                  <td className="px-2 py-1 text-cosmic-text-primary">{period.period?.end || '--'}</td>
                  <td className="px-2 py-1 text-cosmic-text-secondary whitespace-normal break-words">{period.desc}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-3">
        {specialYogas.length > 0 && (
          <div className="rounded-lg border border-sacred-gold/30 p-2">
            <h3 className="font-bold text-cosmic-text-primary mb-1 flex items-center gap-1">
              <Sparkles className="h-4 w-4" />
              {language === 'hi' ? 'विशेष योग' : 'Special Yogas'}
            </h3>
            <table className="w-full table-fixed text-xs sm:text-sm">
              <thead>
                <tr className="bg-sacred-gold/15">
                  <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[30%]">{language === 'hi' ? 'योग' : 'Yoga'}</th>
                  <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[20%]">{language === 'hi' ? 'आरंभ' : 'Start'}</th>
                  <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[20%]">{language === 'hi' ? 'समाप्ति' : 'End'}</th>
                  <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[30%]">{language === 'hi' ? 'स्थिति' : 'Status'}</th>
                </tr>
              </thead>
              <tbody>
                {specialYogas.map((yoga) => (
                  <tr key={yoga.key} className="border-b border-cosmic-border/50 last:border-0 align-top">
                    <td className="px-2 py-1 font-medium text-cosmic-text-primary whitespace-normal break-words">{yoga.name}</td>
                    <td className="px-2 py-1 text-cosmic-text-primary">{yoga.data?.start || '--'}</td>
                    <td className="px-2 py-1 text-cosmic-text-primary">{yoga.data?.end || '--'}</td>
                    <td className="px-2 py-1 text-green-600 whitespace-normal break-words">
                      {language === 'hi' ? 'आज सक्रिय' : 'Active today'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {sandhyaRows.length > 0 && (
          <div className="rounded-lg border border-cosmic-border p-2">
            <h3 className="font-bold text-cosmic-text-primary mb-1 flex items-center gap-1">
              <Sunrise className="h-4 w-4 text-orange-500" />
              {language === 'hi' ? 'संध्या समय' : 'Sandhya Times'}
            </h3>
            <table className="w-full table-fixed text-xs sm:text-sm">
              <thead>
                <tr className="bg-sacred-gold/15">
                  <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[28%]">{language === 'hi' ? 'काल' : 'Period'}</th>
                  <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[18%]">{language === 'hi' ? 'आरंभ' : 'Start'}</th>
                  <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[18%]">{language === 'hi' ? 'समाप्ति' : 'End'}</th>
                  <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold w-[36%]">{language === 'hi' ? 'टिप्पणी' : 'Notes'}</th>
                </tr>
              </thead>
              <tbody>
                {sandhyaRows.map((row) => (
                  <tr key={row.key} className="border-b border-cosmic-border/50 last:border-0 align-top">
                    <td className="px-2 py-1 font-medium text-cosmic-text-primary whitespace-normal break-words">{row.name}</td>
                    <td className="px-2 py-1 text-cosmic-text-primary">{row.period?.start || '--'}</td>
                    <td className="px-2 py-1 text-cosmic-text-primary">{row.period?.end || '--'}</td>
                    <td className="px-2 py-1 text-cosmic-text-secondary whitespace-normal break-words">{row.desc}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
