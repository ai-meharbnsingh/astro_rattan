import { useState, useEffect } from 'react';
import { Sparkles, X } from 'lucide-react';
import { api } from '@/lib/api';
import InteractiveKundli, { type PlanetData, type ChartData } from '@/components/InteractiveKundli';
import { PLANET_ASPECTS, toDMS } from '@/components/kundli/kundli-utils';
import { translatePlanet, translateSign, translateLabel, translateNakshatra } from '@/lib/backend-translations';
import type { SidePanelState } from '@/hooks/useKundliData';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell, TableCaption, TableFooter } from '@/components/ui/table';
import { Heading } from '@/components/ui/heading';

function PlanetPropertiesSection({ kundliId, language }: { kundliId: string; language: string }) {
  const [data, setData] = useState<any>(null);
  const hi = language === 'hi';

  useEffect(() => {
    if (!kundliId) return;
    let cancelled = false;
    api.get<any>(`/api/kundli/${kundliId}/planet-properties`)
      .then(res => { if (!cancelled) setData(res); })
      .catch(() => {});
    return () => { cancelled = true; };
  }, [kundliId]);

  if (!data?.planets || typeof data.planets !== 'object') return null;

  const planetEntries = Object.entries(data.planets as Record<string, any>);
  if (planetEntries.length === 0) return null;

  const dni = data.day_night_indicator;
  const mgs = data.mercury_gender_state;

  return (
    <div className="mt-6 space-y-4">
      {/* ── Parent Indicators (Adhyaya 2 Day/Night Rule) ── */}
      {dni && (
        <div className="rounded-xl border border-border overflow-hidden">
          <div className="px-4 py-2 bg-muted border-b border-border flex items-center gap-2">
            <span className="text-xs font-semibold text-primary uppercase tracking-wide">
              {hi ? 'पितृ-मातृ कारक (दिन/रात्रि नियम)' : 'Parent Indicators (Day/Night Rule)'}
            </span>
            <span className={`text-[10px] px-1.5 py-0.5 rounded font-semibold ${
              dni.day_night_chart === 'day'
                ? 'bg-amber-100 text-amber-800'
                : 'bg-indigo-100 text-indigo-800'
            }`}>
              {hi ? dni.day_night_chart_hi : (dni.day_night_chart === 'day' ? 'Day Chart' : 'Night Chart')}
            </span>
          </div>
          <div className="p-3 grid grid-cols-2 gap-3 text-xs">
            <div className="bg-card rounded-lg p-2.5 border border-border">
              <p className="text-foreground/60 mb-1">{hi ? 'पिता-कारक' : 'Father Indicator'}</p>
              <p className="font-semibold text-foreground text-sm">{translatePlanet(dni.father_indicator?.planet, language)}</p>
              <p className="text-foreground/70 mt-1 leading-snug">
                {hi ? dni.father_indicator?.reason_hi : dni.father_indicator?.reason_en}
              </p>
            </div>
            <div className="bg-card rounded-lg p-2.5 border border-border">
              <p className="text-foreground/60 mb-1">{hi ? 'माता-कारक' : 'Mother Indicator'}</p>
              <p className="font-semibold text-foreground text-sm">{translatePlanet(dni.mother_indicator?.planet, language)}</p>
              <p className="text-foreground/70 mt-1 leading-snug">
                {hi ? dni.mother_indicator?.reason_hi : dni.mother_indicator?.reason_en}
              </p>
            </div>
          </div>
          <p className="px-3 pb-2 text-[10px] text-foreground/40 italic">{dni.sloka_ref}</p>
        </div>
      )}

      {/* ── Mercury Gender State (Adhyaya 2 Hermaphrodite Rule) ── */}
      {mgs && (
        <div className="rounded-xl border border-border overflow-hidden">
          <div className="px-4 py-2 bg-muted border-b border-border flex items-center gap-2">
            <span className="text-xs font-semibold text-primary uppercase tracking-wide">
              {hi ? 'बुध लिंग-अवस्था' : 'Mercury Gender State'}
            </span>
            <span className={`text-[10px] px-1.5 py-0.5 rounded font-semibold ${
              mgs.effective_gender === 'male'
                ? 'bg-blue-100 text-blue-800'
                : mgs.effective_gender === 'female'
                  ? 'bg-pink-100 text-pink-800'
                  : 'bg-slate-100 text-slate-700'
            }`}>
              {hi ? mgs.effective_gender_hi : mgs.effective_gender}
            </span>
          </div>
          <div className="p-3 text-xs text-foreground/80">
            <p>{hi ? mgs.reason_hi : mgs.reason_en}</p>
            {mgs.conjunct_planets?.length > 0 && (
              <div className="mt-2 flex flex-wrap gap-1">
                {mgs.conjunct_planets.map((p: string) => (
                  <span key={p} className="px-1.5 py-0.5 bg-muted rounded text-[10px] font-medium text-foreground">
                    {translatePlanet(p, language)}
                  </span>
                ))}
              </div>
            )}
          </div>
          <p className="px-3 pb-2 text-[10px] text-foreground/40 italic">{mgs.sloka_ref}</p>
        </div>
      )}

      {/* ── Mercury Hermaphrodite Extended Note ── */}
      {data.planets?.Mercury?.hermaphrodite_note && (
        <div className="rounded-xl border border-border overflow-hidden">
          <div className="px-4 py-2 bg-muted border-b border-border">
            <span className="text-xs font-semibold text-primary uppercase tracking-wide">
              {hi ? 'बुध नपुंसक प्रकृति (विस्तृत)' : 'Mercury Hermaphrodite Nature (Extended)'}
            </span>
          </div>
          <div className="p-3 text-xs text-foreground/80 space-y-1">
            {(() => {
              const note = data.planets.Mercury.hermaphrodite_note;
              return (
                <>
                  <p>{hi ? note.reason_hi : note.reason_en}</p>
                  {note.conjunct_planets?.length > 0 && (
                    <div className="flex flex-wrap gap-1 mt-1">
                      {note.conjunct_planets.map((p: string) => (
                        <span key={p} className="px-1.5 py-0.5 bg-muted rounded text-[10px] font-medium">
                          {translatePlanet(p, language)}
                        </span>
                      ))}
                    </div>
                  )}
                  <p className="text-[10px] text-foreground/40 italic mt-1">{note.sloka_ref}</p>
                </>
              );
            })()}
          </div>
        </div>
      )}

      {/* ── Sign Triads — Deva / Manava / Rakshasa (Phaladeepika Adh. 1) ── */}
      {data.lagna_triad?.triad && (
        <div className="rounded-xl border border-border overflow-hidden">
          <div className="px-4 py-2 bg-muted border-b border-border flex items-center gap-2">
            <span className="text-xs font-semibold text-primary uppercase tracking-wide">
              {hi ? 'राशि त्रिगुण वर्गीकरण' : 'Sign Triads — Deva / Manava / Rakshasa'}
            </span>
          </div>
          <div className="p-3 space-y-2">
            {/* Lagna triad badge */}
            <div className="flex items-start gap-2 text-xs">
              <span className="text-foreground/60 shrink-0">{hi ? 'लग्न राशि:' : 'Lagna sign:'}</span>
              <span className={`font-bold px-2 py-0.5 rounded ${
                data.lagna_triad.triad === 'Deva' ? 'bg-amber-100 text-amber-800'
                : data.lagna_triad.triad === 'Manava' ? 'bg-blue-100 text-blue-800'
                : 'bg-red-100 text-red-800'
              }`}>
                {hi ? data.lagna_triad.triad_hi : data.lagna_triad.triad}
              </span>
              <span className="text-foreground/70 leading-snug">
                {hi ? data.lagna_triad.triad_nature_hi : data.lagna_triad.triad_nature_en}
              </span>
            </div>
            {/* Per-planet triads (compact inline) */}
            <div className="flex flex-wrap gap-1.5">
              {Object.entries(data.planets as Record<string, any>).map(([pname, p]: [string, any]) =>
                p.sign_triad?.triad ? (
                  <span key={pname} className={`text-[10px] px-1.5 py-0.5 rounded font-medium ${
                    p.sign_triad.triad === 'Deva' ? 'bg-amber-50 text-amber-700 border border-amber-200'
                    : p.sign_triad.triad === 'Manava' ? 'bg-blue-50 text-blue-700 border border-blue-200'
                    : 'bg-red-50 text-red-700 border border-red-200'
                  }`} title={hi ? p.sign_triad.triad_nature_hi : p.sign_triad.triad_nature_en}>
                    {translatePlanet(pname, language)} — {hi ? p.sign_triad.triad_hi : p.sign_triad.triad}
                  </span>
                ) : null
              )}
            </div>
            {/* Legend */}
            {data.sign_triads_legend && (
              <div className="grid grid-cols-3 gap-2 mt-1">
                {Object.entries(data.sign_triads_legend as Record<string, { en: string; hi: string }>).map(([key, val]) => (
                  <div key={key} className={`rounded p-1.5 text-[10px] ${
                    key === 'Deva' ? 'bg-amber-50 border border-amber-200 text-amber-800'
                    : key === 'Manava' ? 'bg-blue-50 border border-blue-200 text-blue-800'
                    : 'bg-red-50 border border-red-200 text-red-800'
                  }`}>
                    <span className="font-bold block">{key}</span>
                    <span className="leading-snug">{hi ? val.hi : val.en}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
          <p className="px-3 pb-2 text-[10px] text-foreground/40 italic">Phaladeepika Adh. 1</p>
        </div>
      )}

      {/* ── Planet Properties Table (Stage / Guna / Baladi / Metal / Grain / Tree) ── */}
      <div className="rounded-xl border border-sacred-gold/20 overflow-x-auto bg-transparent">
        <div className="px-4 py-2 bg-muted border-b border-border">
          <span className="text-xs font-semibold text-primary uppercase tracking-wide">
            {hi ? 'ग्रह गुण — धातु, अन्न, वृक्ष' : 'Planet Properties — Metal, Grain, Tree'}
          </span>
        </div>
        <table className="table-sacred w-full text-xs">
          <thead className="bg-muted/50">
            <tr>
              <th className="text-left p-1.5 text-primary font-medium">{hi ? 'ग्रह' : 'Planet'}</th>
              <th className="text-left p-1.5 text-primary font-medium">{hi ? 'अवस्था' : 'Stage'}</th>
              <th className="text-left p-1.5 text-primary font-medium">{hi ? 'गुण' : 'Guna'}</th>
              <th className="text-left p-1.5 text-primary font-medium">{hi ? 'बलादि' : 'Baladi'}</th>
              <th className="text-left p-1.5 text-primary font-medium">{hi ? 'धातु' : 'Metal'}</th>
              <th className="text-left p-1.5 text-primary font-medium">{hi ? 'अन्न' : 'Grain'}</th>
              <th className="text-left p-1.5 text-primary font-medium">{hi ? 'वृक्ष' : 'Tree'}</th>
            </tr>
          </thead>
          <tbody>
            {planetEntries.map(([planetName, p]: [string, any]) => (
              <tr key={planetName} className="border-t border-border">
                <td className="p-1.5 font-medium text-foreground">{translatePlanet(planetName, language)}</td>
                <td className="p-1.5 text-foreground/80">
                  {hi ? (p.stage_of_life?.stage_hi || p.stage_of_life?.stage) : p.stage_of_life?.stage}
                </td>
                <td className="p-1.5 text-foreground/80">
                  {hi ? (p.guna?.guna_hi || p.guna?.guna) : p.guna?.guna}
                </td>
                <td className="p-1.5 text-foreground/80">
                  {hi ? (p.baladi_avastha?.name_hi || p.baladi_avastha?.stage) : p.baladi_avastha?.stage}
                </td>
                <td className="p-1.5 text-foreground/70">
                  {hi ? (p.metal_hi || p.metal_en || '—') : (p.metal_en || '—')}
                </td>
                <td className="p-1.5 text-foreground/70">
                  {hi ? (p.grain_hi || p.grain_en || '—') : (p.grain_en || '—')}
                </td>
                <td className="p-1.5 text-foreground/70">
                  {hi ? (p.tree_hi || p.tree_en || '—') : (p.tree_en || '—')}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function PanchadhaMaitriSection({ kundliId, language }: { kundliId: string; language: string }) {
  const [data, setData] = useState<any>(null);
  const hi = language === 'hi';

  useEffect(() => {
    if (!kundliId) return;
    let cancelled = false;
    api.get<any>(`/api/kundli/${kundliId}/panchadha-maitri`)
      .then(res => { if (!cancelled) setData(res); })
      .catch(() => {});
    return () => { cancelled = true; };
  }, [kundliId]);

  if (!data?.relations || (data.relations as any[]).length === 0) return null;

  const relationColor = (rel: string) => {
    if (!rel) return 'bg-slate-100 text-slate-600';
    const r = rel.toLowerCase();
    if (r.includes('great friend')) return 'bg-emerald-100 text-emerald-800';
    if (r.includes('friend')) return 'bg-green-100 text-green-800';
    if (r.includes('great enemy')) return 'bg-red-100 text-red-800';
    if (r.includes('enemy')) return 'bg-orange-100 text-orange-800';
    return 'bg-slate-100 text-slate-700';
  };

  return (
    <div className="mt-6 overflow-x-auto rounded-xl border border-sacred-gold/20 bg-transparent">
      <div className="px-4 py-2 bg-muted border-b border-border">
        <span className="text-xs font-semibold text-primary uppercase tracking-wide">
          {hi ? 'पंचधा मैत्री' : 'Panchadha Maitri (Compound Relations)'}
        </span>
      </div>
      <table className="table-sacred w-full text-xs">
        <thead className="bg-muted/50">
          <tr>
            <th className="text-left p-1.5 text-primary font-medium">{hi ? 'ग्रह' : 'Planet'}</th>
            <th className="text-left p-1.5 text-primary font-medium">{hi ? 'अन्य' : 'With'}</th>
            <th className="text-left p-1.5 text-primary font-medium">{hi ? 'संबंध' : 'Relation'}</th>
          </tr>
        </thead>
        <tbody>
          {(data.relations as any[]).map((r: any, i: number) => (
            <tr key={i} className="border-t border-border">
              <td className="p-1.5 font-medium text-foreground">{translatePlanet(r.planet1, language)}</td>
              <td className="p-1.5 text-foreground/80">{translatePlanet(r.planet2, language)}</td>
              <td className="p-1.5">
                <span className={`px-1.5 py-0.5 rounded text-[10px] font-semibold ${relationColor(r.combined_relation)}`}>
                  {hi ? (r.combined_relation_hi || r.combined_relation) : r.combined_relation}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

const PARAMOCHHA: Record<string, { sign: string; deg: number }> = {
  Sun:     { sign: 'Aries',      deg: 10 },
  Moon:    { sign: 'Taurus',     deg: 3  },
  Mars:    { sign: 'Capricorn',  deg: 28 },
  Mercury: { sign: 'Virgo',      deg: 15 },
  Jupiter: { sign: 'Cancer',     deg: 5  },
  Venus:   { sign: 'Pisces',     deg: 27 },
  Saturn:  { sign: 'Libra',      deg: 20 },
};

const NATURAL_BENEFICS_SET = new Set(['Jupiter', 'Venus', 'Moon', 'Mercury']);

interface PlanetsTabProps {
  planets: any[];
  result: any;
  kundliId: string;
  sidePanel: SidePanelState;
  setSidePanel: (v: SidePanelState) => void;
  handlePlanetClick: (planet: PlanetData) => void;
  handleHouseClick: (house: number, sign: string, planets: PlanetData[]) => void;
  language: string;
  t: (key: string) => string;
  HOUSE_SIGNIFICANCE: Record<number, string>;
}

export default function PlanetsTab({
  planets, result, kundliId, sidePanel, setSidePanel,
  handlePlanetClick, handleHouseClick,
  language, t, HOUSE_SIGNIFICANCE,
}: PlanetsTabProps) {
  return (
    <div className="flex flex-col xl:flex-row gap-8">
      {/* Interactive Chart */}
      <div className="w-full xl:w-[600px] xl:flex-shrink-0 flex justify-center">
        <InteractiveKundli
          chartData={{ planets, houses: result.chart_data?.houses, ascendant: result.chart_data?.ascendant } as ChartData}
          onPlanetClick={handlePlanetClick}
          onHouseClick={handleHouseClick}
        />
      </div>

      {/* Side Panel */}
      <div className="flex-1 min-w-0">
        {sidePanel ? (
          <div className="bg-muted rounded-xl border border-border p-5 animate-in fade-in slide-in-from-right-4 duration-300">
            <div className="flex items-center justify-between mb-4">
              <Heading as={4} variant={4}>
                {sidePanel.type === 'planet'
                  ? `${translatePlanet(sidePanel.planet?.planet || '', language)}${(sidePanel.planet?.status || '').toLowerCase().includes('retrograde') ? ' (R)' : ''} — ${t('kundli.details')}`
                  : t('kundli.houseDetails')}
              </Heading>
              <button
                onClick={() => setSidePanel(null)}
                className="text-foreground hover:text-foreground transition-colors"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {sidePanel.type === 'planet' && sidePanel.planet && (() => {
              const p = sidePanel.planet;
              const status = p.status?.toLowerCase() || '';
              const pmo = PARAMOCHHA[p.planet];
              const isParamochha = !!pmo && p.sign === pmo.sign && p.sign_degree != null && Math.abs(p.sign_degree - pmo.deg) <= 1;
              const strengthLabel = isParamochha
                ? 'Paramochha ★'
                : status.includes('exalted') ? 'Exalted' : status.includes('debilitated') ? 'Debilitated' : status.includes('own') ? 'Own Sign' : p.status || t('kundli.transit');
              const strengthColor = isParamochha
                ? 'text-yellow-600 font-bold'
                : status.includes('exalted') ? 'text-green-500' : status.includes('debilitated') ? 'text-red-500' : status.includes('own') ? 'text-blue-500' : 'text-foreground';
              const moonAspectors = p.planet === 'Moon'
                ? planets.filter(op =>
                    op.planet !== 'Moon' &&
                    (PLANET_ASPECTS[op.planet] || [7]).some(offset =>
                      ((op.house - 1 + offset) % 12) + 1 === p.house
                    )
                  )
                : [];
              const aspects = (PLANET_ASPECTS[p.planet] || [7]).map((offset) => {
                const targetHouse = ((p.house - 1 + offset) % 12) + 1;
                return `${t('table.house')} ${targetHouse}`;
              });

              return (
                <div className="space-y-3">
                  <div className="grid grid-cols-2 gap-3">
                    <div className="bg-card rounded-lg p-3">
                      <p className="text-sm text-foreground">{t('kundli.sign')}</p>
                      <p className="font-semibold text-foreground">{translateSign(p.sign, language)}</p>
                    </div>
                    <div className="bg-card rounded-lg p-3">
                      <p className="text-sm text-foreground">{t('kundli.degree')}</p>
                      <p className="font-semibold text-foreground">{p.sign_degree != null ? toDMS(p.sign_degree) : '\u2014'}</p>
                    </div>
                    <div className="bg-card rounded-lg p-3">
                      <p className="text-sm text-foreground">{t('kundli.house')}</p>
                      <p className="font-semibold text-foreground">{p.house}</p>
                    </div>
                    <div className="bg-card rounded-lg p-3">
                      <p className="text-sm text-foreground">{t('kundli.nakshatra')}</p>
                      <p className="font-semibold text-foreground">
                        {translateNakshatra(p.nakshatra, language) || t('common.noData')}
                        {p.nakshatra_pada ? ` (${t('auto.pada')} ${p.nakshatra_pada})` : ''}
                      </p>
                    </div>
                  </div>
                  <div className="bg-card rounded-lg p-3">
                    <p className="text-sm text-foreground">{t('kundli.strength')}</p>
                    <p className={`font-semibold ${strengthColor}`}>{translateLabel(strengthLabel, language)}</p>
                    {isParamochha && (
                      <p className="text-[10px] text-yellow-600 italic mt-0.5">
                        {language === 'hi' ? 'परमोच्च — अधिकतम उच्च बल' : 'Paramochha — maximum exaltation degree (Phaladeepika Adh. 1)'}
                      </p>
                    )}
                  </div>
                  <div className="bg-card rounded-lg p-3">
                    <p className="text-sm text-foreground">{t('kundli.aspects')}</p>
                    <p className="font-semibold text-foreground text-sm">{aspects.join(', ')}</p>
                  </div>
                  {moonAspectors.length > 0 && (
                    <div className="bg-card rounded-lg p-3 col-span-2">
                      <p className="text-sm text-foreground mb-2">
                        {language === 'hi' ? 'चन्द्र पर ग्रह-दृष्टि (फलदीपिका अ. 18)' : 'Planets aspecting Moon (Phaladeepika Adh. 18)'}
                      </p>
                      <div className="flex flex-wrap gap-1.5">
                        {moonAspectors.map(op => {
                          const isBen = NATURAL_BENEFICS_SET.has(op.planet);
                          return (
                            <span key={op.planet} className={`text-[10px] font-semibold px-2 py-0.5 rounded ${isBen ? 'bg-emerald-100 text-emerald-800' : 'bg-red-100 text-red-800'}`}>
                              {translatePlanet(op.planet, language)} {isBen ? '✦' : '✗'}
                            </span>
                          );
                        })}
                      </div>
                    </div>
                  )}
                  <div className="bg-card rounded-lg p-3">
                    <p className="text-sm text-foreground">{t('kundli.housePlacement')}</p>
                    <p className="text-sm text-foreground">
                      {translatePlanet(p.planet, language)} — {t('kundli.house')} {p.house} ({HOUSE_SIGNIFICANCE[p.house] || t('common.noData')})
                    </p>
                  </div>
                </div>
              );
            })()}

            {sidePanel.type === 'house' && (
              <div className="space-y-3">
                <div className="grid grid-cols-2 gap-3">
                  <div className="bg-card rounded-lg p-3">
                    <p className="text-sm text-foreground">{t('kundli.houseNumber')}</p>
                    <p className="font-semibold text-foreground">{sidePanel.house}</p>
                  </div>
                  <div className="bg-card rounded-lg p-3">
                    <p className="text-sm text-foreground">{t('kundli.sign')}</p>
                    <p className="font-semibold text-foreground">{translateSign(sidePanel.sign || '', language)}</p>
                  </div>
                </div>
                <div className="bg-card rounded-lg p-3">
                  <p className="text-sm text-foreground">{t('kundli.significance')}</p>
                  <p className="font-semibold text-foreground">
                    {HOUSE_SIGNIFICANCE[sidePanel.house || 0] || t('common.noData')}
                  </p>
                </div>
                <div className="bg-card rounded-lg p-3">
                  <p className="text-sm text-foreground mb-2">{t('kundli.planetsInHouse')}</p>
                  {(sidePanel.planets || []).length > 0 ? (
                    <div className="space-y-1">
                      {(sidePanel.planets || []).map((p) => (
                        <button
                          key={p.planet}
                          className="w-full text-left text-sm text-foreground hover:text-primary transition-colors flex items-center gap-2"
                          onClick={() => setSidePanel({ type: 'planet', planet: p })}
                        >
                          <span className="w-2 h-2 rounded-full bg-muted" />
                          {translatePlanet(p.planet, language)}{(p.status || '').toLowerCase().includes('retrograde') ? '*' : ''} ({translateSign(p.sign, language)} {p.sign_degree != null ? toDMS(p.sign_degree) : '\u2014'})
                        </button>
                      ))}
                    </div>
                  ) : (
                    <p className="text-sm text-foreground">{t('kundli.noPlanets')}</p>
                  )}
                </div>
              </div>
            )}
          </div>
        ) : (
          <div className="bg-muted rounded-xl border border-dashed border-border p-8 flex flex-col items-center justify-center h-full min-h-[200px]">
            <Sparkles className="w-8 h-8 text-primary mb-3" />
            <p className="text-foreground text-sm text-center">
              {t('kundli.clickInfo')}
            </p>
          </div>
        )}

        {/* Planet table */}
        <div className="mt-6 overflow-x-auto rounded-xl border border-sacred-gold/20 bg-transparent">
          <Table className="w-full text-xs">
            <TableHeader className="bg-muted">
              <TableRow>
                <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.planet')}</TableHead>
                <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.sign')}</TableHead>
                <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.house')}</TableHead>
                <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.nakshatra')}</TableHead>
                <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.status')}</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {planets.map((planet: any, index: number) => (
                <TableRow
                  key={index}
                  className={`border-t border-border cursor-pointer transition-colors ${
                    sidePanel?.type === 'planet' && sidePanel.planet?.planet === planet.planet
                      ? 'bg-muted'
                      : 'hover:bg-muted/5'
                  }`}
                  onClick={() => handlePlanetClick(planet)}
                >
                  <TableCell className="p-1.5 text-foreground font-medium">
                    {translatePlanet(planet.planet, language)}
                    {(planet.status || '').toLowerCase().includes('retrograde') && <span className="text-red-500 ml-0.5" title={t('kundli.retrograde')}>*</span>}
                  </TableCell>
                  <TableCell className="p-1.5 text-foreground">{translateSign(planet.sign, language)}</TableCell>
                  <TableCell className="p-1.5 text-foreground">{planet.house}</TableCell>
                  <TableCell className="p-1.5 text-foreground">
                    {translateNakshatra(planet.nakshatra, language) || '\u2014'}
                    {planet.nakshatra_pada ? ` (${t('auto.p')}${planet.nakshatra_pada})` : ''}
                  </TableCell>
                  <TableCell className="p-1.5">
                    <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${planet.status === 'Exalted' || planet.status === 'Own Sign' ? 'bg-green-100 text-green-800' : 'bg-card text-foreground'}`}>
                      {translateLabel(planet.status, language)}
                    </span>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>

        {/* Planet Properties & Panchadha Maitri */}
        {kundliId && <PlanetPropertiesSection kundliId={kundliId} language={language} />}
        {kundliId && <PanchadhaMaitriSection kundliId={kundliId} language={language} />}
      </div>
    </div>
  );
}
