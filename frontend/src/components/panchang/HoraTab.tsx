import { useMemo } from 'react';
import { Card, CardContent } from '@/components/ui/card';
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
    <div className="space-y-6">
      {/* Current Hora */}
      {currentHora && (
        <Card className="card-sacred border-sacred-gold/30">
          <CardContent className="p-6">
            <div className="flex flex-col sm:flex-row items-center gap-4">
              <div className="p-4 rounded-2xl bg-sacred-gold/20">
                <Clock className="h-12 w-12 text-sacred-gold" />
              </div>
              <div className="text-center sm:text-left">
                <p className="text-sm text-cosmic-text-secondary">
                  {language === 'hi' ? 'वर्तमान होरा' : 'Current Hora'}
                </p>
                <h3 className="text-3xl font-bold text-cosmic-text-primary">
                  {language === 'hi' ? currentHora.hora_hindi || currentHora.hora : currentHora.hora}
                </h3>
                <p className="text-lg text-sacred-gold">
                  {currentHora.start} - {currentHora.end}
                </p>
                <div className="flex items-center justify-center sm:justify-start gap-2 mt-2">
                  <span className="text-sm text-cosmic-text-secondary">
                    {language === 'hi' ? 'स्वामी' : 'Lord'}:
                  </span>
                  <span className="font-medium text-cosmic-text-primary">
                    {language === 'hi' ? currentHora.lord_hindi || currentHora.lord : currentHora.lord}
                  </span>
                </div>
              </div>
              <div className={`ml-auto px-4 py-2 rounded-full ${getQualityColor(currentHora.type)}`}>
                <span className="font-semibold">
                  {language === 'hi' ? currentHora.type_hindi || currentHora.type : currentHora.type}
                </span>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Hora Table */}
      <Card className="card-sacred">
        <CardContent className="p-4">
          <h3 className="text-lg font-bold text-cosmic-text-primary mb-4 flex items-center gap-2">
            <Clock className="h-5 w-5 text-sacred-gold" />
            {language === 'hi' ? 'दिन की होरा' : 'Day Hora Table'}
          </h3>
          
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-sacred-gold/20">
                  <th className="text-left py-3 px-4 text-sacred-gold-dark font-semibold rounded-tl-lg">
                    {language === 'hi' ? 'होरा' : 'Hora'}
                  </th>
                  <th className="text-left py-3 px-4 text-sacred-gold-dark font-semibold">
                    {language === 'hi' ? 'स्वामी' : 'Lord'}
                  </th>
                  <th className="text-left py-3 px-4 text-sacred-gold-dark font-semibold">
                    {language === 'hi' ? 'समय' : 'Time'}
                  </th>
                  <th className="text-center py-3 px-4 text-sacred-gold-dark font-semibold rounded-tr-lg">
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
                        border-b border-cosmic-border last:border-0
                        ${isCurrent ? 'bg-sacred-gold/10' : index % 2 === 0 ? 'bg-cosmic-card/30' : ''}
                      `}
                    >
                      <td className="py-3 px-4">
                        <div className="flex items-center gap-2">
                          <LordIcon className={`h-4 w-4 ${hora.type.toLowerCase().includes('good') ? 'text-yellow-500' : 'text-slate-400'}`} />
                          <span className={`font-medium ${isCurrent ? 'text-sacred-gold' : 'text-cosmic-text-primary'}`}>
                            {language === 'hi' ? hora.hora_hindi || hora.hora : hora.hora}
                          </span>
                          {isCurrent && (
                            <span className="px-2 py-0.5 text-xs bg-sacred-gold text-cosmic-bg rounded-full">
                              {language === 'hi' ? 'अभी' : 'Now'}
                            </span>
                          )}
                        </div>
                      </td>
                      <td className="py-3 px-4 text-cosmic-text-secondary">
                        {language === 'hi' ? hora.lord_hindi || hora.lord : hora.lord}
                      </td>
                      <td className="py-3 px-4 text-cosmic-text-secondary">
                        {hora.start} - {hora.end}
                      </td>
                      <td className="py-3 px-4">
                        <span className={`inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-medium ${getQualityColor(hora.type)}`}>
                          {language === 'hi' ? hora.type_hindi || hora.type : hora.type}
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>

      {/* Hora Info */}
      <Card className="card-sacred">
        <CardContent className="p-4">
          <div className="flex items-start gap-3">
            <AlertCircle className="h-5 w-5 text-sacred-gold mt-0.5" />
            <div>
              <h4 className="font-semibold text-cosmic-text-primary mb-2">
                {language === 'hi' ? 'होरा के बारे में' : 'About Hora'}
              </h4>
              <p className="text-sm text-cosmic-text-secondary leading-relaxed">
                {language === 'hi' 
                  ? 'होरा दिन का 1/24वां भाग होता है (लगभग 1 घंटा)। प्रत्येक होरा एक ग्रह द्वारा शासित होती है। शुभ होरा में शुभ कार्य करने से सफलता मिलती है।'
                  : 'Hora is 1/24th part of a day (approximately 1 hour). Each Hora is ruled by a planet. Auspicious works done during good Hora yield success.'}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
