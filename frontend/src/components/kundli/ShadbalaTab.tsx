import React, { useState } from 'react';
import { Loader2, ChevronDown, ChevronRight } from 'lucide-react';
import { translatePlanet } from '@/lib/backend-translations';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell, TableCaption, TableFooter } from '@/components/ui/table';
import { Heading } from '@/components/ui/heading';

// Shadbala detail key translations
const STHANA_DETAIL_KEYS: Record<string, { en: string; hi: string }> = {
  uchcha: { en: 'Exaltation', hi: 'उच्च' },
  saptavargaja: { en: 'Saptavarga', hi: 'सप्तवर्ग' },
  ojayugma: { en: 'Odd/Even', hi: 'ओजयुग्म' },
  kendra: { en: 'Kendra', hi: 'केन्द्र' },
  drekkana: { en: 'Drekkana', hi: 'द्रेक्काण' },
};

const KALA_DETAIL_KEYS: Record<string, { en: string; hi: string }> = {
  nathonnatha: { en: 'Day/Night', hi: 'दिन/रात्रि' },
  paksha: { en: 'Paksha', hi: 'पक्ष' },
  tribhaga: { en: 'Tribhaga', hi: 'त्रिभाग' },
  abda: { en: 'Year', hi: 'वर्ष' },
  masa: { en: 'Month', hi: 'मास' },
  vara: { en: 'Day', hi: 'वार' },
  hora: { en: 'Hora', hi: 'होरा' },
  ayana: { en: 'Ayana', hi: 'अयन' },
};

interface ShadbalaTabProps {
  shadbalaData: any;
  loadingShadbala: boolean;
  language: string;
  t: (key: string) => string;
}

export default function ShadbalaTab({ shadbalaData, loadingShadbala, language, t }: ShadbalaTabProps) {
  const [expandedPlanets, setExpandedPlanets] = useState<Set<string>>(new Set());

  const toggleExpand = (planet: string) => {
    setExpandedPlanets((prev) => {
      const next = new Set(prev);
      if (next.has(planet)) next.delete(planet);
      else next.add(planet);
      return next;
    });
  };

  if (loadingShadbala) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-6 h-6 animate-spin text-primary" />
        <span className="ml-2 text-foreground">{t('kundli.calculatingShadbala')}</span>
      </div>
    );
  }

  if (!shadbalaData?.planets) {
    return <p className="text-center text-foreground py-8">{t('kundli.clickShadbalaTab')}</p>;
  }

  return (
    <div className="space-y-6">
      <div className="bg-muted rounded-xl p-5 border border-border">
        <Heading as={4} variant={4} className="mb-4">{t('section.shadbalaStrength')}</Heading>
        <div className="flex items-end justify-around gap-2 h-[280px]">
          {['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'].map((planet) => {
            const data = shadbalaData.planets[planet];
            if (!data) return null;
            const required = data.required || 1.0;
            const total = data.total || 0;
            const ratio = total / required;
            const barHeight = Math.min((ratio / 1.5) * 100, 100);
            const isStrong = ratio >= 1.0;
            const barColor = isStrong ? '#16a34a' : '#dc2626';
            const requiredPct = (1 / 1.5) * 100;
            return (
              <div key={planet} className="flex flex-col items-center gap-1 flex-1 min-w-[60px]">
                <span className={`text-sm font-bold ${isStrong ? 'text-foreground' : 'text-foreground'}`}>
                  {total.toFixed(1)}
                </span>
                <div className="relative w-full flex justify-center bg-muted/20 rounded-t-lg h-[200px]">
                  {/* Required line */}
                  <div
                    className="absolute w-full border-t-2 border-dashed border-red-500 z-10"
                    style={{ bottom: `${requiredPct}%` }}
                    title={`Required: ${required}`}
                  />
                  {/* Bar */}
                  <div
                    className="w-10 rounded-t-lg transition-all duration-500 relative"
                    style={{
                      height: `${barHeight}%`,
                      backgroundColor: barColor,
                      alignSelf: 'flex-end',
                    }}
                  >
                    {ratio > 1.2 && (
                      <div className="absolute -top-6 left-1/2 transform -translate-x-1/2">
                        <span className="text-xs text-primary">★</span>
                      </div>
                    )}
                  </div>
                </div>
                <span className="text-xs font-medium text-foreground text-center leading-tight mt-1">
                  {translatePlanet(planet, language)}
                </span>
                <span className={`text-xs ${isStrong ? 'text-green-600 font-semibold' : 'text-red-500'}`}>
                  {isStrong ? '✓' : '✗'}
                </span>
              </div>
            );
          })}
        </div>
        <div className="flex items-center justify-center gap-6 mt-4 text-sm text-foreground">
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded" style={{ backgroundColor: '#16a34a' }} />
            <span>{t('kundli.strong')}</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded" style={{ backgroundColor: '#dc2626' }} />
            <span>{t('kundli.weak')}</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-6 border-t-2 border-dashed border-border" />
            <span>{t('auto.required')}</span>
          </div>
        </div>
      </div>

      {/* Bhav Bala */}
      {shadbalaData.bhav_bala && (
        <div className="bg-muted rounded-xl p-5 border border-border">
          <Heading as={4} variant={4} className="mb-4">{t('auto.bhavBalaHouseStrengt')}</Heading>
          <div className="overflow-x-auto -mx-1 px-1">
            <div className="flex items-end gap-1" style={{ height: '220px', minWidth: '420px' }}>
              {Array.from({ length: 12 }, (_, i) => i + 1).map((house) => {
                const data = shadbalaData.bhav_bala[house];
                if (!data) return null;
                const maxVal = Math.max(...Object.values(shadbalaData.bhav_bala as Record<string, {total: number}>).map((d) => d.total), 1);
                const barHeight = Math.min((data.total / maxVal) * 100, 100);
                const barColor = data.total >= maxVal * 0.5 ? '#16a34a' : '#dc2626';
                return (
                  <div key={house} className="flex flex-col items-center gap-1 flex-1">
                    <span className="text-xs font-bold" style={{ color: barColor }}>{data.total.toFixed(1)}</span>
                    <div className="relative w-full flex justify-center bg-muted/20 rounded-t-lg h-[160px]">
                      <div
                        className="w-6 rounded-t-lg transition-all duration-500"
                        style={{ height: `${barHeight}%`, backgroundColor: barColor, alignSelf: 'flex-end' }}
                      />
                    </div>
                    <span className="text-xs font-medium text-foreground text-center mt-1">{house}</span>
                    <span className="text-center leading-tight text-foreground" style={{ fontSize: '9px' }}>
                      {data.sign?.substring(0, 3)}
                    </span>
                  </div>
                );
              })}
            </div>
          </div>
          <div className="flex items-center justify-center gap-6 mt-3 text-sm text-foreground">
            <span className="flex items-center gap-1"><span className="w-2 h-2 rounded" style={{ backgroundColor: '#16a34a' }} />{t('auto.strong')}</span>
            <span className="flex items-center gap-1"><span className="w-2 h-2 rounded" style={{ backgroundColor: '#dc2626' }} />{t('auto.weak')}</span>
            <span className="text-xs text-foreground">{t('auto.valuesInRupas')}</span>
          </div>
        </div>
      )}

      <div className="bg-muted rounded-xl p-5 border border-border">
        <Heading as={4} variant={4} className="mb-4">{t('section.detailedBreakdown')}</Heading>
        <div className="overflow-x-auto">
          <Table className="w-full text-sm border-collapse">
            <TableHeader>
              <TableRow className="bg-muted">
                <TableHead className="text-left p-2 text-primary font-medium text-xs">{t('table.planet')}</TableHead>
                <TableHead className="text-center p-2 text-primary font-medium text-xs">{t('auto.sthana')}</TableHead>
                <TableHead className="text-center p-2 text-primary font-medium text-xs">{t('auto.dig')}</TableHead>
                <TableHead className="text-center p-2 text-primary font-medium text-xs">{t('auto.kala')}</TableHead>
                <TableHead className="text-center p-2 text-primary font-medium text-xs">{t('auto.cheshta')}</TableHead>
                <TableHead className="text-center p-2 text-primary font-medium text-xs">{t('auto.naisargika')}</TableHead>
                <TableHead className="text-center p-2 text-primary font-medium text-xs">{t('auto.drik')}</TableHead>
                <TableHead className="text-center p-2 text-primary font-medium text-xs">{t('table.total')}</TableHead>
                <TableHead className="text-center p-2 text-primary font-medium text-xs">{t('auto.ratio')}</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'].map((planet) => {
                const d = shadbalaData.planets[planet];
                if (!d) return null;
                const hasDetail = d.sthana_detail || d.kala_detail;
                const isExpanded = expandedPlanets.has(planet);
                return (
                  <React.Fragment key={planet}>
                    <TableRow
                      className={`border-t border-border/50 ${d.is_strong ? 'bg-white' : 'bg-red-50/30'} ${hasDetail ? 'cursor-pointer hover:bg-muted/10' : ''} transition-colors`}
                      onClick={hasDetail ? () => toggleExpand(planet) : undefined}
                    >
                      <TableCell className="p-2 text-foreground font-medium">
                        <div className="flex items-center gap-1">
                          {hasDetail && (isExpanded ? <ChevronDown className="w-3 h-3 text-primary" /> : <ChevronRight className="w-3 h-3 text-primary" />)}
                          {translatePlanet(planet, language)}
                        </div>
                      </TableCell>
                      <TableCell className="text-center p-2 text-foreground text-xs">{d.sthana?.toFixed ? d.sthana.toFixed(2) : d.sthana}</TableCell>
                      <TableCell className="text-center p-2 text-foreground text-xs">{d.dig?.toFixed ? d.dig.toFixed(2) : d.dig}</TableCell>
                      <TableCell className="text-center p-2 text-foreground text-xs">{d.kala?.toFixed ? d.kala.toFixed(2) : d.kala}</TableCell>
                      <TableCell className="text-center p-2 text-foreground text-xs">{d.cheshta?.toFixed ? d.cheshta.toFixed(2) : d.cheshta}</TableCell>
                      <TableCell className="text-center p-2 text-foreground text-xs">{d.naisargika?.toFixed ? d.naisargika.toFixed(2) : d.naisargika}</TableCell>
                      <TableCell className="text-center p-2 text-foreground text-xs">{d.drik?.toFixed ? d.drik.toFixed(2) : d.drik}</TableCell>
                      <TableCell className={`text-center p-2 font-semibold text-xs ${d.is_strong ? 'text-green-600' : 'text-red-600'}`}>{d.total?.toFixed ? d.total.toFixed(2) : d.total}</TableCell>
                      <TableCell className={`text-center p-2 font-medium text-xs ${d.ratio >= 1 ? 'text-green-600' : 'text-red-600'}`}>{d.ratio?.toFixed ? d.ratio.toFixed(2) : d.ratio}x</TableCell>
                    </TableRow>
                    {isExpanded && d.sthana_detail && (
                      <TableRow className="bg-muted">
                        <TableCell className="p-2 pl-6 text-sm text-foreground italic" colSpan={2}>
                          {t('auto.sthanaDetail')}
                        </TableCell>
                        <TableCell colSpan={7} className="p-2 text-sm text-foreground">
                          {(['uchcha', 'saptavargaja', 'ojhayugma', 'kendra', 'drekkana'] as const)
                            .filter((k) => d.sthana_detail[k] != null)
                            .map((k) => {
                              const label = STHANA_DETAIL_KEYS[k]?.[language as 'en' | 'hi'] || k;
                              return `${label}: ${d.sthana_detail[k]}`;
                            })
                            .join(' | ')}
                        </TableCell>
                      </TableRow>
                    )}
                    {isExpanded && d.kala_detail && (
                      <TableRow className="bg-muted">
                        <TableCell className="p-2 pl-6 text-sm text-foreground italic" colSpan={2}>
                          {t('auto.kalaDetail')}
                        </TableCell>
                        <TableCell colSpan={7} className="p-2 text-sm text-foreground">
                          {(['nathonnatha', 'paksha', 'tribhaga', 'abda', 'masa', 'vara', 'hora', 'ayana'] as const)
                            .filter((k) => d.kala_detail[k] != null)
                            .map((k) => {
                              const label = KALA_DETAIL_KEYS[k]?.[language as 'en' | 'hi'] || k;
                              return `${label}: ${d.kala_detail[k]}`;
                            })
                            .join(' | ')}
                        </TableCell>
                      </TableRow>
                    )}
                  </React.Fragment>
                );
              })}
            </TableBody>
          </Table>
        </div>
      </div>
    </div>
  );
}
