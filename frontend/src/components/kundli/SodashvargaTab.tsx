import { Layers, Loader2 } from 'lucide-react';
import { translatePlanet, translateSign } from '@/lib/backend-translations';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '@/components/ui/table';
import { Heading } from '@/components/ui/heading';

interface SodashvargaTabProps {
  sodashvargaData: any;
  loadingSodashvarga: boolean;
  language: string;
  t: (key: string) => string;
}

const TIER_COLORS: Record<string, string> = {
  Bhedaka:      'bg-red-100 text-red-800',
  Parijatamsa:  'bg-orange-100 text-orange-800',
  Uttamamsa:    'bg-amber-100 text-amber-800',
  Gopuramsa:    'bg-blue-100 text-blue-800',
  Simhasanamsa: 'bg-emerald-100 text-emerald-800',
  Parvatamsa:   'bg-green-100 text-green-800',
};

const METER_COLORS: Record<string, string> = {
  Strong: 'bg-green-500',
  Medium: 'bg-amber-400',
  Weak:   'bg-red-500',
};

export default function SodashvargaTab({ sodashvargaData, loadingSodashvarga, language, t }: SodashvargaTabProps) {
  const signShort = (sign: string) => {
    const translated = translateSign(sign || '', language) || sign || '';
    return language === 'hi' ? translated.slice(0, 2) : translated.slice(0, 3);
  };

  if (loadingSodashvarga) {
    return (
      <div className="flex items-center justify-center py-12"><Loader2 className="w-6 h-6 animate-spin text-primary" /><span className="ml-2 text-foreground">{t('kundli.loadingSodashvarga')}</span></div>
    );
  }

  if (!sodashvargaData) {
    return <p className="text-center text-foreground py-8">{t('common.noData')}</p>;
  }

  const strengthColors: Record<string, string> = {
    Strong: 'text-green-800 bg-green-100',
    Medium: 'text-yellow-800 bg-yellow-100',
    Weak: 'text-red-800 bg-red-100',
  };

  const dignityLabels: Record<string, { label: string; hiLabel: string; color: string }> = {
    exalted:      { label: 'Ex',  hiLabel: 'उच्च', color: 'text-green-800 bg-green-100' },
    own:          { label: 'Own', hiLabel: 'स्व',  color: 'text-blue-800 bg-blue-100' },
    moolatrikona: { label: 'Moo', hiLabel: 'मू',   color: 'text-blue-800 bg-blue-100' },
    friend:       { label: 'Fr',  hiLabel: 'मि',   color: 'text-amber-800 bg-amber-100' },
    neutral:      { label: 'Neu', hiLabel: 'सम',   color: 'text-slate-700 bg-slate-200' },
    enemy:        { label: 'En',  hiLabel: 'श',    color: 'text-orange-800 bg-orange-100' },
    debilitated:  { label: 'Deb', hiLabel: 'नी',   color: 'text-red-800 bg-red-100' },
  };
  const strengthHi: Record<string, string> = { Strong: 'प्रबल', Medium: 'मध्यम', Weak: 'दुर्बल' };
  const strLabel = (s: string) => language === 'hi' ? (strengthHi[s] || s) : s;
  const toFiniteNumber = (value: unknown): number | null => {
    if (typeof value === 'number') return Number.isFinite(value) ? value : null;
    if (typeof value === 'string') {
      const cleaned = value.replace('%', '').trim();
      if (!cleaned) return null;
      const parsed = Number.parseFloat(cleaned);
      return Number.isFinite(parsed) ? parsed : null;
    }
    return null;
  };
  const normalizePercent = (value: number): number => {
    if (!Number.isFinite(value)) return 0;
    const scaled = value > 0 && value <= 1 ? value * 100 : value;
    return Math.max(0, Math.min(100, scaled));
  };

  return (
    <div className="space-y-6">
      {/* Page heading */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
          <Layers className="w-6 h-6" />
          {language === 'hi' ? 'षोडशवर्ग' : 'Sodashvarga'}
        </Heading>
        <p className="text-sm text-muted-foreground">
          {language === 'hi' ? 'जीवन-क्षेत्र विशिष्ट विश्लेषण के लिए 16 विभागीय चार्ट' : '16 divisional charts for life-area specific analysis'}
        </p>
      </div>
      {/* Varga Table */}
      <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
        <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
          {t('section.sodashvargaTitle')}
        </div>
        <div className="p-4">
        {(() => {
          const rows = sodashvargaData.varga_table || (Array.isArray(sodashvargaData.by_sign) ? sodashvargaData.by_sign : []);
          if (rows.length > 0) {
            return (
              <div className="overflow-x-auto">
              <Table className="w-full text-xs min-w-[700px]">
                <TableHeader><TableRow>
                  <TableHead className="text-left p-2 text-primary font-semibold uppercase tracking-wide">{t('table.varga')}</TableHead>
                  {['Su', 'Mo', 'Ma', 'Me', 'Ju', 'Ve', 'Sa', 'Ra', 'Ke'].map(p => (
                    <TableHead key={p} className="text-center p-1.5 text-primary font-semibold">{p}</TableHead>
                  ))}
                </TableRow></TableHeader>
                <TableBody>
                  {rows.map((row: any) => {
                    const planets = row.placements || row.planets;
                    const planetEntries = Array.isArray(planets)
                      ? planets
                      : typeof planets === 'object'
                        ? ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu'].map(p => planets[p] || '')
                        : [];
                    return (
                      <TableRow key={row.varga || row.division || row.name} className="border-t border-border">
                        <TableCell className="p-2 font-semibold text-foreground whitespace-nowrap">{row.varga || row.name || `D${row.division}`}</TableCell>
                        {planetEntries.map((pl: any, i: number) => {
                          const signRaw = typeof pl === 'string' ? pl : (pl?.sign || '');
                          const sign = signRaw ? signShort(signRaw) : (pl?.sign_abbr || '');
                          const dignity = typeof pl === 'object' ? pl?.dignity?.toLowerCase() : '';
                          const dignityColors: Record<string, string> = {
                            exalted: 'bg-green-100 text-green-800', own: 'bg-blue-100 text-blue-800',
                            moolatrikona: 'bg-blue-100 text-blue-800', friend: 'bg-amber-100 text-amber-800',
                            enemy: 'bg-orange-100 text-orange-800', debilitated: 'bg-red-100 text-red-800',
                          };
                          return <TableCell key={i} className={`p-1.5 text-center text-sm rounded ${dignityColors[dignity] || ''}`}>{sign}</TableCell>;
                        })}
                      </TableRow>
                    );
                  })}
                </TableBody>
              </Table>
              </div>
            );
          }
          if (sodashvargaData.by_sign && typeof sodashvargaData.by_sign === 'object') {
            return (
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 text-xs">
                {Object.entries(sodashvargaData.by_sign).map(([planet, data]: [string, any]) => (
                  <div key={planet} className="bg-white rounded-lg p-3">
                    <p className="font-semibold text-foreground mb-1">{translatePlanet(planet, language)}</p>
                    {typeof data === 'object' && Object.entries(data as Record<string, any>).map(([varga, sign]) => (
                      <p key={varga} className="text-foreground">{varga}: {translateSign(String(sign), language)}</p>
                    ))}
                  </div>
                ))}
              </div>
            );
          }
          return <p className="text-center text-foreground">{t('common.noData')}</p>;
        })()}
        <div className="flex flex-wrap gap-2 mt-3 text-xs">
          <span className="px-2 py-1 rounded bg-green-100 text-green-800">{t('dignity.exalted')}</span>
          <span className="px-2 py-1 rounded bg-blue-100 text-blue-800">{t('dignity.ownMoolatrikona')}</span>
          <span className="px-2 py-1 rounded bg-amber-100 text-amber-800">{t('dignity.friend')}</span>
          <span className="px-2 py-1 rounded bg-orange-100 text-orange-800">{t('dignity.enemy')}</span>
          <span className="px-2 py-1 rounded bg-red-100 text-red-800">{t('dignity.debilitated')}</span>
        </div>
        </div>
      </div>

      {/* Vimshopak Bala */}
      {(sodashvargaData.by_planet || sodashvargaData.vimshopak) && (
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
            {t('section.vimshopakBala')}
          </div>
          <div className="p-4">
          <div className="overflow-x-auto">
          <div className="space-y-3 min-w-[420px]">
            {(() => {
              const items = Array.isArray(sodashvargaData.vimshopak) ? sodashvargaData.vimshopak
                : Object.entries(sodashvargaData.by_planet || {}).map(([planet, data]: [string, any]) => ({
                    planet,
                    score: typeof data === 'number' ? data : data?.vimshopak_bala ?? data?.vimshopak ?? data?.score ?? 0,
                    percentage: data?.percentage,
                    strength: data?.strength,
                    dignities: data?.dignities,
                  }));
              return items.map((v: any) => (
                (() => {
                  const score = toFiniteNumber(v?.score);
                  const scoreBasedPercent = score != null ? (score / 20) * 100 : 0;
                  const inputPercent = toFiniteNumber(v?.percentage);
                  const resolvedPercent = normalizePercent(inputPercent != null ? inputPercent : scoreBasedPercent);
                  const showPercent = v?.percentage !== null && v?.percentage !== undefined && v?.percentage !== '';
                  const displayPercent = Number.isInteger(resolvedPercent) ? String(resolvedPercent) : resolvedPercent.toFixed(1);

                  // Saptavarga classical tier from varga_strength (if available)
                  const vs = sodashvargaData.varga_strength?.planets?.[v.planet];
                  const tierName: string | undefined = vs?.tier?.name;
                  const tierNameHi: string | undefined = vs?.tier?.name_hi;
                  const tierDesc: string | undefined = vs?.tier?.description;
                  const tierDescHi: string | undefined = vs?.tier?.description_hi;
                  const tierLabel = language === 'hi' ? (tierNameHi || tierName) : tierName;
                  const tierTooltip = language === 'hi' ? (tierDescHi || tierDesc) : tierDesc;

                  const meterColor = METER_COLORS[v.strength] || 'bg-primary';
                  const tierColor = tierName ? (TIER_COLORS[tierName] || 'bg-slate-100 text-slate-700') : '';

                  return (
                    <div key={v.planet} className="space-y-1">
                      <div className="flex items-center gap-3 text-sm">
                        <span className="w-12 text-foreground font-medium">{(translatePlanet(v.planet || '', language) || v.planet || '').slice(0, language === 'hi' ? 3 : 4)}</span>
                        <div className="flex-1 bg-muted/30 rounded-full h-4 overflow-hidden">
                          <div className={`${meterColor} rounded-full h-4 transition-all`} style={{ width: `${resolvedPercent}%` }} />
                        </div>
                        <span className="w-16 text-right text-foreground text-sm">{score != null ? score.toFixed(1) : '?'} / 20</span>
                        {showPercent && (
                          <span className="w-12 text-right text-foreground font-semibold text-sm">{displayPercent}%</span>
                        )}
                        {v.strength && (
                          <span className={`px-1.5 py-0.5 rounded text-xs font-semibold ${strengthColors[v.strength] || 'text-muted-foreground bg-gray-500'}`}>{strLabel(v.strength)}</span>
                        )}
                        {tierLabel && (
                          <span className={`px-1.5 py-0.5 rounded text-xs font-semibold ${tierColor}`} title={tierTooltip}>
                            {tierLabel}
                          </span>
                        )}
                      </div>
                      {v.dignities && typeof v.dignities === 'object' && (
                        <div className="flex items-center gap-1 ml-[60px] flex-wrap">
                          {Object.entries(v.dignities as Record<string, number>)
                            .filter(([, count]) => (count as number) > 0)
                            .map(([dignity, count]) => {
                              const info = dignityLabels[dignity] || { label: dignity.slice(0, 3), hiLabel: dignity.slice(0, 3), color: 'text-muted-foreground bg-gray-500' };
                              return (
                                <span key={dignity} className={`px-1.5 py-0.5 rounded text-xs font-medium ${info.color}`}>
                                  {language === 'hi' ? info.hiLabel : info.label}:{count as number}
                                </span>
                              );
                            })}
                        </div>
                      )}
                    </div>
                  );
                })()
              ));
            })()}
          </div>

          {/* Saptavarga tier legend */}
          {sodashvargaData.varga_strength && (
            <div className="mt-4 pt-3 border-t border-border/40">
              <p className="text-xs text-muted-foreground font-semibold uppercase tracking-wide mb-2">
                {language === 'hi' ? 'सप्तवर्ग बल — शास्त्रीय श्रेणी' : 'Saptavarga Tier (Phaladeepika Adh. 3)'}
              </p>
              <div className="flex flex-wrap gap-1.5 text-xs">
                {[
                  ['Bhedaka', language === 'hi' ? 'भेदक' : 'Bhedaka', '0-1'],
                  ['Parijatamsa', language === 'hi' ? 'पारिजातांश' : 'Parijatamsa', '2'],
                  ['Uttamamsa', language === 'hi' ? 'उत्तमांश' : 'Uttamamsa', '3'],
                  ['Gopuramsa', language === 'hi' ? 'गोपुरांश' : 'Gopuramsa', '4-5'],
                  ['Simhasanamsa', language === 'hi' ? 'सिंहासनांश' : 'Simhasanamsa', '6'],
                  ['Parvatamsa', language === 'hi' ? 'पर्वतांश' : 'Parvatamsa', '7'],
                ].map(([key, label, holds]) => (
                  <span key={key} className={`px-2 py-0.5 rounded font-medium ${TIER_COLORS[key] || 'bg-slate-100 text-slate-700'}`}>
                    {label} <span className="opacity-60">({holds})</span>
                  </span>
                ))}
              </div>
            </div>
          )}
          </div>
          </div>
        </div>
      )}
    </div>
  );
}
