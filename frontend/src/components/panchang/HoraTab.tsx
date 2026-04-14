import { useMemo } from 'react';
import { Clock, Sun, Moon, AlertCircle } from 'lucide-react';
import type { FullPanchangData } from '@/sections/Panchang';

interface Props {
  panchang: FullPanchangData;
  language: string;
  t: (key: string) => string;
  timezoneOffset: number;
}

export default function HoraTab({ panchang, language, t, timezoneOffset }: Props) {
  const horaTable = panchang.hora_table || [];

  // Memoize current Hora calculation to avoid running on every render
  const currentHora = useMemo(() => {
    // Calculate current time at the panchang location (not browser local time)
    const currentTimeAtLocation = new Date(Date.now() + (timezoneOffset * 60 * 1000));
    const currentHour = currentTimeAtLocation.getHours();

    return horaTable.find(h => {
      const startHour = parseInt(h.start.split(':')[0]);
      const endHour = parseInt(h.end.split(':')[0]);
      return currentHour >= startHour && currentHour < endHour;
    });
  }, [horaTable, timezoneOffset]);

  // Get quality color
  const getQualityColor = (type: string) => {
    if (type.toLowerCase().includes('good') || type === 'शुभ') return 'text-green-500 bg-green-500/10';
    if (type.toLowerCase().includes('bad') || type === 'अशुभ') return 'text-red-500 bg-red-500/10';
    return 'text-yellow-500 bg-yellow-500/10';
  };

  // Get lord icon
  const getLordIcon = (lord: string) => {
    const sunPlanets = ['Sun', 'सूर्य', 'Mars', 'मंगल', 'Jupiter', 'गुरु', 'Saturn', 'शनि'];
    return sunPlanets.includes(lord) ? Sun : Moon;
  };

  return (
    <div className="space-y-3">
      {/* Current Hora */}
      {currentHora && (
        <div className="flex items-center gap-3 p-2 rounded-lg border border-sacred-gold/30 bg-sacred-gold/10">
          <Clock className="h-8 w-8 text-sacred-gold flex-shrink-0" />
          <div className="flex-1 min-w-0">
            <p className="text-xs text-cosmic-text-secondary">
              {language === 'hi' ? 'वर्तमान होरा' : 'Current Hora'}
            </p>
            <span className="font-bold text-cosmic-text-primary">
              {language === 'hi' ? currentHora.hora_hindi || currentHora.hora : currentHora.hora}
            </span>
            <span className="mx-2 text-sacred-gold">{currentHora.start} - {currentHora.end}</span>
            <span className="text-sm text-cosmic-text-secondary">
              {language === 'hi' ? 'स्वामी' : 'Lord'}: {language === 'hi' ? currentHora.lord_hindi || currentHora.lord : currentHora.lord}
            </span>
          </div>
          <span className={`px-2 py-1 rounded-full text-xs font-semibold ${getQualityColor(currentHora.type)}`}>
            {language === 'hi' ? currentHora.type_hindi || currentHora.type : currentHora.type}
          </span>
        </div>
      )}

      {/* Hora Table */}
      <div className="rounded-lg border border-cosmic-border overflow-hidden">
        <h3 className="font-bold text-cosmic-text-primary p-2 flex items-center gap-1 bg-cosmic-card/30">
          <Clock className="h-4 w-4 text-sacred-gold" />
          {language === 'hi' ? 'होरा तालिका' : 'Hora Table'}
        </h3>

        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-sacred-gold/15">
                <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold">
                  {language === 'hi' ? 'होरा' : 'Hora'}
                </th>
                <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold">
                  {language === 'hi' ? 'स्वामी' : 'Lord'}
                </th>
                <th className="text-left px-2 py-1 text-sacred-gold-dark font-semibold">
                  {language === 'hi' ? 'समय' : 'Time'}
                </th>
                <th className="text-center px-2 py-1 text-sacred-gold-dark font-semibold">
                  {language === 'hi' ? 'फल' : 'Result'}
                </th>
              </tr>
            </thead>
            <tbody>
              {horaTable.map((hora, index) => {
                const isCurrent = currentHora?.hora === hora.hora;
                const LordIcon = getLordIcon(hora.lord);

                return (
                  <tr
                    key={index}
                    className={`
                      border-b border-cosmic-border/50 last:border-0
                      ${isCurrent ? 'bg-sacred-gold/10' : index % 2 === 0 ? 'bg-cosmic-card/30' : ''}
                    `}
                  >
                    <td className="px-2 py-1">
                      <div className="flex items-center gap-1">
                        <LordIcon className={`h-3 w-3 ${hora.type.toLowerCase().includes('good') ? 'text-yellow-500' : 'text-slate-400'}`} />
                        <span className={`font-medium ${isCurrent ? 'text-sacred-gold' : 'text-cosmic-text-primary'}`}>
                          {language === 'hi' ? hora.hora_hindi || hora.hora : hora.hora}
                        </span>
                        {isCurrent && (
                          <span className="px-1.5 py-0.5 text-xs bg-sacred-gold text-cosmic-bg rounded-full">
                            {language === 'hi' ? 'अभी' : 'Now'}
                          </span>
                        )}
                      </div>
                    </td>
                    <td className="px-2 py-1 text-cosmic-text-secondary">
                      {language === 'hi' ? hora.lord_hindi || hora.lord : hora.lord}
                    </td>
                    <td className="px-2 py-1 text-cosmic-text-secondary">
                      {hora.start} - {hora.end}
                    </td>
                    <td className="px-2 py-1 text-center">
                      <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${getQualityColor(hora.type)}`}>
                        {language === 'hi' ? hora.type_hindi || hora.type : hora.type}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Hora Info */}
      <div className="rounded-lg border border-cosmic-border p-2">
        <div className="flex items-start gap-2">
          <AlertCircle className="h-4 w-4 text-sacred-gold mt-0.5 flex-shrink-0" />
          <div>
            <h4 className="font-semibold text-cosmic-text-primary mb-1">
              {language === 'hi' ? 'होरा के बारे में' : 'About Hora'}
            </h4>
            <p className="text-sm text-cosmic-text-secondary leading-relaxed">
              {language === 'hi'
                ? 'होरा दिन का 1/24वां भाग होता है (लगभग 1 घंटा)। प्रत्येक होरा एक ग्रह द्वारा शासित होती है। शुभ होरा में शुभ कार्य करने से सफलता मिलती है।'
                : 'Hora is 1/24th part of a day (approximately 1 hour). Each Hora is ruled by a planet. Auspicious works done during good Hora yield success.'}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
