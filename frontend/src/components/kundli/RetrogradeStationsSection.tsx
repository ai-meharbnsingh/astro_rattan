import { useState } from 'react';
import { Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useTranslation } from '@/lib/i18n';
import { translatePlanet, translateSign } from '@/lib/backend-translations';
import { api } from '@/lib/api';

interface RetrogradeStationsSectionProps {
  kundliId: string;
}

export default function RetrogradeStationsSection({ kundliId }: RetrogradeStationsSectionProps) {
  const { t, language } = useTranslation();
  const currentYear = new Date().getFullYear();
  const [year, setYear] = useState(currentYear);
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const fetchStations = async (yr: number) => {
    setLoading(true);
    try {
      const result = await api.get(`/api/kundli/${kundliId}/retrograde-stations?year=${yr}`);
      setData(result);
    } catch (e) { console.error(e); }
    setLoading(false);
  };

  const handleYearChange = (yr: number) => {
    setYear(yr);
    fetchStations(yr);
  };

  // Auto-fetch on mount
  if (!data && !loading) {
    fetchStations(year);
  }

  const planets = ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn'];

  return (
    <div className="bg-sacred-cream rounded-xl border border-sacred-gold/20 p-4 mt-4">
      <div className="flex items-center justify-between mb-3">
        <h4 className="font-display font-semibold text-sacred-brown">
          {language === 'hi' ? 'ग्रह वक्री तिथियाँ' : 'Planet Retrogression Dates'}
        </h4>
        <div className="flex items-center gap-2">
          <Button
            size="sm"
            variant="outline"
            onClick={() => handleYearChange(year - 1)}
            className="h-7 px-2 text-xs"
          >
            ←
          </Button>
          <span className="text-sm font-mono font-semibold" style={{ color: 'var(--ink)' }}>{year}</span>
          <Button
            size="sm"
            variant="outline"
            onClick={() => handleYearChange(year + 1)}
            className="h-7 px-2 text-xs"
          >
            →
          </Button>
        </div>
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-8">
          <Loader2 className="w-5 h-5 animate-spin text-sacred-gold" />
          <span className="ml-2 text-sm text-sacred-text-secondary">{t('common.loading')}</span>
        </div>
      ) : data?.stations ? (
        <div className="overflow-x-auto">
          <table className="w-full text-sm border-collapse">
            <thead>
              <tr className="bg-slate-100">
                <th className="text-left p-2 font-medium text-slate-600">{language === 'hi' ? 'ग्रह' : 'Planet'}</th>
                <th className="text-left p-2 font-medium text-slate-600">{language === 'hi' ? 'प्रकार' : 'Station'}</th>
                <th className="text-left p-2 font-medium text-slate-600">{language === 'hi' ? 'तिथि' : 'Date'}</th>
                <th className="text-left p-2 font-medium text-slate-600">{language === 'hi' ? 'समय' : 'Time'}</th>
                <th className="text-left p-2 font-medium text-slate-600">{language === 'hi' ? 'राशि' : 'Sign'}</th>
                <th className="text-center p-2 font-medium text-slate-600">{language === 'hi' ? 'अंश' : 'Degree'}</th>
              </tr>
            </thead>
            <tbody>
              {planets.map(planet => {
                const stations = data.stations[planet] || [];
                if (stations.length === 0) {
                  return (
                    <tr key={planet} className="border-b border-slate-100">
                      <td className="p-2 font-semibold">{translatePlanet(planet, language)}</td>
                      <td colSpan={5} className="p-2 text-slate-400 text-center">
                        {language === 'hi' ? 'इस वर्ष वक्री नहीं' : 'No retrogression this year'}
                      </td>
                    </tr>
                  );
                }
                return stations.map((s: any, i: number) => (
                  <tr key={`${planet}-${i}`} className="border-b border-slate-100">
                    {i === 0 && (
                      <td className="p-2 font-semibold" rowSpan={stations.length}>
                        {translatePlanet(planet, language)}
                      </td>
                    )}
                    <td className="p-2">
                      <span
                        className="text-xs px-2 py-0.5 rounded-full font-medium"
                        style={{
                          backgroundColor: s.station === 'retrograde' ? '#fee2e2' : '#d1fae5',
                          color: s.station === 'retrograde' ? '#991b1b' : '#065f46',
                        }}
                      >
                        {s.station === 'retrograde'
                          ? (language === 'hi' ? 'वक्री' : 'Retrograde')
                          : (language === 'hi' ? 'मार्गी' : 'Direct')}
                      </span>
                    </td>
                    <td className="p-2 font-mono text-sm">{s.date}</td>
                    <td className="p-2 font-mono text-sm">{s.datetime ? s.datetime.split(' ')[1] : '—'}</td>
                    <td className="p-2">{translateSign(s.sign, language)}</td>
                    <td className="p-2 text-center font-mono">{s.sign_degree}°</td>
                  </tr>
                ));
              })}
            </tbody>
          </table>
        </div>
      ) : null}
    </div>
  );
}
