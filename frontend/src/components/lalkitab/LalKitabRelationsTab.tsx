import { useEffect, useMemo, useState } from 'react';
import { useTranslation } from '@/lib/i18n';
import { api } from '@/lib/api';
import { useLalKitab } from './LalKitabContext';
import { Users, Eye, AlertTriangle, CheckCircle } from 'lucide-react';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '@/components/ui/table';

interface RelationsResponse {
  kundli_id: string;
  conjunctions: Array<{
    house: number;
    planets: string[];
    clashes: [string, string][];
    friendships: [string, string][];
  }>;
  aspects: Array<{
    planet: string;
    from_house: number;
    aspect_houses: number[];
  }>;
}

export default function LalKitabRelationsTab() {
  const { t, language } = useTranslation();
  const isHi = language === 'hi';
  const { kundliId } = useLalKitab();
  const [data, setData] = useState<RelationsResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!kundliId) { setData(null); return; }
    setError(null);
    api.get(`/api/lalkitab/relations/${kundliId}`)
      .then((res: any) => setData(res as RelationsResponse))
      .catch((e: any) => setError(e instanceof Error ? e.message : (isHi ? 'लोड नहीं हो सका' : 'Failed to load')));
  }, [kundliId]);

  const conjunctions = data?.conjunctions || [];
  const aspects = data?.aspects || [];

  const hasAny = conjunctions.length > 0 || aspects.length > 0;
  const sortedAspects = useMemo(() => {
    return [...aspects].sort((a, b) => (a.from_house - b.from_house) || a.planet.localeCompare(b.planet));
  }, [data]);

  if (!kundliId) {
    return (
      <div className="text-center py-10 text-muted-foreground text-sm">
        {isHi ? 'कुंडली चुनें या बनाएं।' : 'Select or generate a Kundli.'}
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl text-sacred-gold flex items-center gap-2">
          <Users className="w-6 h-6" />
          {t('lk.relations.title')}
        </h2>
        <p className="text-gray-500 mt-1">{t('lk.relations.desc')}</p>
      </div>

      {error && (
        <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-red-700 text-sm">
          {error}
        </div>
      )}

      {!error && !hasAny && (
        <p className="text-sm text-gray-600 italic">
          {t('auto.noDataAvailable')}
        </p>
      )}

      {/* Conjunctions (Yuti) */}
      <section>
        <h3 className="text-lg text-sacred-gold mb-4">
          {t('lk.relations.conjunction')} ({t('auto.yuti')})
        </h3>

        {conjunctions.length === 0 ? (
          <p className="text-sm text-gray-600 italic">{t('auto.noConjunctionsFound')}</p>
        ) : (
          <div className="space-y-4">
            {conjunctions.map((conj) => {
              const hasClash = (conj.clashes || []).length > 0;
              return (
                <div
                  key={conj.house}
                  className={`rounded-xl p-5 border transition-all ${
                    hasClash ? 'border-red-300/30 bg-red-500/5' : 'border-blue-500/20 bg-blue-500/5'
                  }`}
                >
                  <div className="flex items-center justify-between mb-3">
                    <div>
                      <span className="text-sm text-gray-600">{t('auto.house')} {isNaN(Number(conj.house)) ? 0 : conj.house}</span>
                      <div className="flex items-center gap-2 mt-1 flex-wrap">
                        {conj.planets.map((planet) => (
                          <span
                            key={planet}
                            className="px-2.5 py-1 rounded-full bg-sacred-gold/10 text-sacred-gold text-sm font-medium"
                          >
                            {planet}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>

                  {(conj.clashes || []).map(([p1, p2]) => (
                    <div key={`${p1}-${p2}`} className="flex items-center gap-2 mt-2 text-sm text-red-600">
                      <AlertTriangle className="w-4 h-4 shrink-0" />
                      <span>{t('lk.relations.clash')}: {p1} &amp; {p2}</span>
                    </div>
                  ))}

                  {(conj.friendships || []).map(([p1, p2]) => (
                    <div key={`${p1}-${p2}`} className="flex items-center gap-2 mt-2 text-sm text-green-600">
                      <CheckCircle className="w-4 h-4 shrink-0" />
                      <span>{t('lk.relations.noClash')}: {p1} &amp; {p2}</span>
                    </div>
                  ))}
                </div>
              );
            })}
          </div>
        )}
      </section>

      <div className="border-t border-sacred-gold/10" />

      {/* Aspects (Drishti) */}
      <section>
        <h3 className="text-lg text-sacred-gold mb-4 flex items-center gap-2">
          <Eye className="w-5 h-5" />
          {t('auto.aspectsDrishti')}
        </h3>

        <div className="overflow-x-auto">
          <Table className="w-full text-sm">
            <TableHeader>
              <TableRow className="border-b border-sacred-gold/10">
                <TableHead className="text-left py-2 px-3 text-sacred-gold/70 font-medium">{t('auto.planet')}</TableHead>
                <TableHead className="text-left py-2 px-3 text-sacred-gold/70 font-medium">{t('auto.inHouse')}</TableHead>
                <TableHead className="text-left py-2 px-3 text-sacred-gold/70 font-medium">{t('auto.aspectsHouses')}</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {sortedAspects.map((entry) => (
                <TableRow key={entry.planet} className="border-b border-sacred-gold/10">
                  <TableCell className="py-2 px-3 font-medium text-foreground">{entry.planet}</TableCell>
                  <TableCell className="py-2 px-3 text-muted-foreground">{isNaN(Number(entry.from_house)) ? 0 : entry.from_house}</TableCell>
                  <TableCell className="py-2 px-3 text-muted-foreground">
                    {(entry.aspect_houses || []).map(h => isNaN(Number(h)) ? 0 : h).join(', ')}
                  </TableCell>
                </TableRow>
              ))}
              {sortedAspects.length === 0 && (
                <TableRow>
                  <TableCell colSpan={3} className="py-6 text-center text-xs text-muted-foreground">
                    {isHi ? 'कोई दृष्टि डेटा नहीं।' : 'No aspects data.'}
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </div>
      </section>
    </div>
  );
}

