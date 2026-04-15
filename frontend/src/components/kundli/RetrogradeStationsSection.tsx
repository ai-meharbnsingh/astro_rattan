import { useState } from 'react';
import { Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useTranslation } from '@/lib/i18n';
import { translatePlanet, translateSign } from '@/lib/backend-translations';
import { api } from '@/lib/api';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell, TableCaption, TableFooter } from '@/components/ui/table';
import { Heading } from '@/components/ui/heading';

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

  // Auto-fetch on mount
  if (!data && !loading) {
    fetchStations(year);
  }

  const planets = ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn'];

  return (
    <div className="bg-muted rounded-xl border border-border p-4 mt-4">
      <div className="flex items-center justify-between mb-3">
        <Heading as={4} variant={4}>
          {t('auto.planetRetrogressionD')}
        </Heading>
        <div className="flex items-center gap-2">
          <Button
            size="sm"
            variant="outline"
            onClick={() => handleYearChange(year - 1)}
            className="h-7 px-2 text-sm"
          >
            ←
          </Button>
          <span className="text-sm font-mono font-semibold" className="text-foreground">{year}</span>
          <Button
            size="sm"
            variant="outline"
            onClick={() => handleYearChange(year + 1)}
            className="h-7 px-2 text-sm"
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
          <Table className="w-full text-sm border-collapse">
            <TableHeader>
              <TableRow className="bg-slate-100">
                <TableHead className="text-left p-2 font-medium text-muted-foreground">{t('auto.planet')}</TableHead>
                <TableHead className="text-left p-2 font-medium text-muted-foreground">{t('auto.station')}</TableHead>
                <TableHead className="text-left p-2 font-medium text-muted-foreground">{t('auto.date')}</TableHead>
                <TableHead className="text-left p-2 font-medium text-muted-foreground">{t('auto.time')}</TableHead>
                <TableHead className="text-left p-2 font-medium text-muted-foreground">{t('auto.sign')}</TableHead>
                <TableHead className="text-center p-2 font-medium text-muted-foreground">{t('auto.degree')}</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {planets.map(planet => {
                const stations = data.stations[planet] || [];
                if (stations.length === 0) {
                  return (
                    <TableRow key={planet} className="border-b border-slate-100">
                      <TableCell className="p-2 font-semibold">{translatePlanet(planet, language)}</TableCell>
                      <TableCell colSpan={5} className="p-2 text-muted-foreground text-center">
                        {t('auto.noRetrogressionThisY')}
                      </TableCell>
                    </TableRow>
                  );
                }
                return stations.map((s: any, i: number) => (
                  <TableRow key={`${planet}-${i}`} className="border-b border-slate-100">
                    {i === 0 && (
                      <TableCell className="p-2 font-semibold" rowSpan={stations.length}>
                        {translatePlanet(planet, language)}
                      </TableCell>
                    )}
                    <TableCell className="p-2">
                      <span
                        className="text-sm px-2 py-0.5 rounded-full font-medium"
                        style={{
                          backgroundColor: s.station === 'retrograde' ? '#fee2e2' : '#d1fae5',
                          color: s.station === 'retrograde' ? '#991b1b' : '#065f46',
                        }}
                      >
                        {s.station === 'retrograde'
                          ? (t('auto.retrograde'))
                          : (t('auto.direct'))}
                      </span>
                    </TableCell>
                    <TableCell className="p-2 font-mono text-sm">{s.date}</TableCell>
                    <TableCell className="p-2 font-mono text-sm">{s.datetime ? s.datetime.split(' ')[1] : '—'}</TableCell>
                    <TableCell className="p-2">{translateSign(s.sign, language)}</TableCell>
                    <TableCell className="p-2 text-center font-mono">{s.sign_degree}°</TableCell>
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
