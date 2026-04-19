import { useState } from 'react';
import { Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useTranslation } from '@/lib/i18n';
import { translatePlanet, translateSign } from '@/lib/backend-translations';
import { api } from '@/lib/api';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '@/components/ui/table';

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
    } catch { /* ignored */ }
    setLoading(false);
  };

  const handleYearChange = (yr: number) => {
    setYear(yr);
    fetchStations(yr);
  };

  if (!data && !loading) {
    fetchStations(year);
  }

  const planets = ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn'];

  return (
    <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
      <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center justify-between">
        <span>{t('auto.planetRetrogressionD')}</span>
        <div className="flex items-center gap-2">
          <Button
            size="sm"
            variant="outline"
            onClick={() => handleYearChange(year - 1)}
            className="h-6 px-2 text-xs bg-white/10 border-white/30 text-white hover:bg-white/20"
          >
            ←
          </Button>
          <span className="text-sm font-mono font-semibold">{year}</span>
          <Button
            size="sm"
            variant="outline"
            onClick={() => handleYearChange(year + 1)}
            className="h-6 px-2 text-xs bg-white/10 border-white/30 text-white hover:bg-white/20"
          >
            →
          </Button>
        </div>
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-8">
          <Loader2 className="w-5 h-5 animate-spin text-primary" />
          <span className="ml-2 text-sm text-foreground">{t('common.loading')}</span>
        </div>
      ) : data?.stations ? (
        <div className="overflow-x-auto">
          <Table className="w-full text-xs table-fixed">
            <TableHeader>
              <TableRow>
                <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[16%]">{t('auto.planet')}</TableHead>
                <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[18%]">{t('auto.station')}</TableHead>
                <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[20%]">{t('auto.date')}</TableHead>
                <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[16%]">{t('auto.time')}</TableHead>
                <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide w-[18%]">{t('auto.sign')}</TableHead>
                <TableHead className="text-center p-2 text-primary font-semibold uppercase tracking-wide w-[12%]">{t('auto.degree')}</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {planets.map(planet => {
                const stations = data.stations[planet] || [];
                if (stations.length === 0) {
                  return (
                    <TableRow key={planet} className="border-t border-border">
                      <TableCell className="p-2 font-semibold text-foreground">{translatePlanet(planet, language)}</TableCell>
                      <TableCell colSpan={5} className="p-2 text-muted-foreground text-center">
                        {t('auto.noRetrogressionThisY')}
                      </TableCell>
                    </TableRow>
                  );
                }
                return stations.map((s: any, i: number) => (
                  <TableRow key={`${planet}-${i}`} className="border-t border-border">
                    {i === 0 && (
                      <TableCell className="p-2 font-semibold text-foreground" rowSpan={stations.length}>
                        {translatePlanet(planet, language)}
                      </TableCell>
                    )}
                    <TableCell className="p-2">
                      <span className={`px-1.5 py-0.5 rounded text-[10px] font-semibold ${
                        s.station === 'retrograde'
                          ? 'bg-red-100 text-red-800'
                          : 'bg-emerald-100 text-emerald-800'
                      }`}>
                        {s.station === 'retrograde' ? t('auto.retrograde') : t('auto.direct')}
                      </span>
                    </TableCell>
                    <TableCell className="p-2 font-mono text-foreground">{s.date}</TableCell>
                    <TableCell className="p-2 font-mono text-foreground">{s.datetime ? s.datetime.split(' ')[1] : '—'}</TableCell>
                    <TableCell className="p-2 text-foreground">{translateSign(s.sign, language)}</TableCell>
                    <TableCell className="p-2 text-center font-mono text-foreground">{s.sign_degree}°</TableCell>
                  </TableRow>
                ));
              })}
            </TableBody>
          </Table>
        </div>
      ) : null}
    </div>
  );
}
