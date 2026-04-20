import React, { useState } from 'react';
import { Loader2, ChevronDown, ChevronRight } from 'lucide-react';
import { translatePlanet } from '@/lib/backend-translations';
import { Heading } from '@/components/ui/heading';

const STHANA_DETAIL_KEYS: Record<string, { en: string; hi: string }> = {
  uchcha:       { en: 'Exaltation', hi: 'उच्च' },
  saptavargaja: { en: 'Saptavarga', hi: 'सप्तवर्ग' },
  ojayugma:     { en: 'Odd/Even',   hi: 'ओजयुग्म' },
  kendra:       { en: 'Kendra',     hi: 'केन्द्र' },
  drekkana:     { en: 'Drekkana',   hi: 'द्रेक्काण' },
};

const KALA_DETAIL_KEYS: Record<string, { en: string; hi: string }> = {
  nathonnatha: { en: 'Day/Night', hi: 'दिन/रात्रि' },
  paksha:      { en: 'Paksha',    hi: 'पक्ष' },
  tribhaga:    { en: 'Tribhaga',  hi: 'त्रिभाग' },
  abda:        { en: 'Year',      hi: 'वर्ष' },
  masa:        { en: 'Month',     hi: 'मास' },
  vara:        { en: 'Day',       hi: 'वार' },
  hora:        { en: 'Hora',      hi: 'होरा' },
  ayana:       { en: 'Ayana',     hi: 'अयन' },
};

const PLANETS = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'];

const thCls = 'p-2 text-left text-[10px] font-semibold uppercase tracking-wide text-primary border-b border-border';
const thCenterCls = 'p-2 text-center text-[10px] font-semibold uppercase tracking-wide text-primary border-b border-border';

interface ShadbalaTabProps {
  shadbalaData: any;
  loadingShadbala: boolean;
  language: string;
  t: (key: string) => string;
}

export default function ShadbalaTab({ shadbalaData, loadingShadbala, language, t }: ShadbalaTabProps) {
  const [expandedPlanets, setExpandedPlanets] = useState<Set<string>>(new Set());
  const hi = language === 'hi';

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
      {/* Page heading */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1">
          {hi ? 'षड्बल' : 'Shadbala'}
        </Heading>
        <p className="text-sm text-muted-foreground">
          {hi ? 'छः गुना बल मापन — प्रत्येक ग्रह की संख्यात्मक शक्ति' : 'Six-fold strength measurement — numerical power of each planet'}
        </p>
      </div>

      {/* Shadbala Bar Chart */}
      <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
        <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
          {t('section.shadbalaStrength')}
        </div>
        <div className="p-5">
          <div className="flex items-end justify-around gap-2 h-[280px]">
            {PLANETS.map((planet) => {
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
                  <span className="text-sm font-bold text-foreground">{total.toFixed(1)}</span>
                  <div className="relative w-full flex justify-center bg-muted/20 rounded-t-lg h-[200px]">
                    <div className="absolute w-full border-t-2 border-dashed border-red-500 z-10" style={{ bottom: `${requiredPct}%` }} title={`Required: ${required}`} />
                    <div className="w-10 rounded-t-lg transition-all duration-500 relative" style={{ height: `${barHeight}%`, backgroundColor: barColor, alignSelf: 'flex-end' }}>
                      {ratio > 1.2 && (
                        <div className="absolute -top-6 left-1/2 transform -translate-x-1/2">
                          <span className="text-xs text-primary">★</span>
                        </div>
                      )}
                    </div>
                  </div>
                  <span className="text-xs font-medium text-foreground text-center leading-tight mt-1">{translatePlanet(planet, language)}</span>
                  <span className={`text-xs ${isStrong ? 'text-green-600 font-semibold' : 'text-red-500'}`}>{isStrong ? '✓' : '✗'}</span>
                  <span className="text-[10px] text-muted-foreground leading-none">Req: {required.toFixed(1)}</span>
                </div>
              );
            })}
          </div>
          <div className="flex items-center justify-center gap-6 mt-4 text-sm text-foreground">
            <div className="flex items-center gap-1"><div className="w-3 h-3 rounded" style={{ backgroundColor: '#16a34a' }} /><span>{t('kundli.strong')}</span></div>
            <div className="flex items-center gap-1"><div className="w-3 h-3 rounded" style={{ backgroundColor: '#dc2626' }} /><span>{t('kundli.weak')}</span></div>
            <div className="flex items-center gap-1"><div className="w-6 border-t-2 border-dashed border-border" /><span>{t('auto.required')}</span></div>
          </div>
        </div>
      </div>

      {/* Bhav Bala Bar Chart */}
      {shadbalaData.bhav_bala && (
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
            {t('auto.bhavBalaHouseStrengt')}
          </div>
          <div className="p-5">
            <div className="overflow-x-auto -mx-1 px-1">
              <div className="flex items-end gap-1" style={{ height: '220px', minWidth: '420px' }}>
                {Array.from({ length: 12 }, (_, i) => i + 1).map((house) => {
                  const data = shadbalaData.bhav_bala[house];
                  if (!data) return null;
                  const maxVal = Math.max(...Object.values(shadbalaData.bhav_bala as Record<string, { total: number }>).map((d) => d.total), 1);
                  const barHeight = Math.min((data.total / maxVal) * 100, 100);
                  const barColor = data.total >= maxVal * 0.5 ? '#16a34a' : '#dc2626';
                  return (
                    <div key={house} className="flex flex-col items-center gap-1 flex-1">
                      <span className="text-xs font-bold" style={{ color: barColor }}>{data.total.toFixed(1)}</span>
                      <div className="relative w-full flex justify-center bg-muted/20 rounded-t-lg h-[160px]">
                        <div className="w-6 rounded-t-lg transition-all duration-500" style={{ height: `${barHeight}%`, backgroundColor: barColor, alignSelf: 'flex-end' }} />
                      </div>
                      <span className="text-xs font-medium text-foreground text-center mt-1">{house}</span>
                      <span className="text-center leading-tight text-foreground" style={{ fontSize: '9px' }}>{data.sign?.substring(0, 3)}</span>
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
        </div>
      )}

      {/* Detailed Breakdown Table */}
      <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
        <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
          {t('section.detailedBreakdown')}
        </div>
        <table style={{ tableLayout: 'fixed', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
          <colgroup>
            <col style={{ width: '11%' }} />
            <col style={{ width: '8%' }} />
            <col style={{ width: '6%' }} />
            <col style={{ width: '8%' }} />
            <col style={{ width: '8%' }} />
            <col style={{ width: '9%' }} />
            <col style={{ width: '6%' }} />
            <col style={{ width: '7%' }} />
            <col style={{ width: '8%' }} />
            <col style={{ width: '11%' }} />
            <col style={{ width: '9%' }} />
            <col style={{ width: '9%' }} />
          </colgroup>
          <thead>
            <tr>
              <th className={thCls}>{t('table.planet')}</th>
              <th className={thCenterCls}>{t('auto.sthana')}</th>
              <th className={thCenterCls}>{t('auto.dig')}</th>
              <th className={thCenterCls}>{t('auto.kala')}</th>
              <th className={thCenterCls}>{t('auto.cheshta')}</th>
              <th className={thCenterCls}>{t('auto.naisargika')}</th>
              <th className={thCenterCls}>{t('auto.drik')}</th>
              <th className={thCenterCls}>{hi ? 'चन्द्र' : 'Chandra'}</th>
              <th className={thCenterCls}>{t('table.total')}</th>
              <th className={thCenterCls}>{t('auto.ratio')}</th>
              <th className={thCenterCls}>{hi ? 'इष्ट' : 'Ishta'}</th>
              <th className={thCenterCls}>{hi ? 'कष्ट' : 'Kashta'}</th>
            </tr>
          </thead>
          <tbody>
            {PLANETS.map((planet) => {
              const d = shadbalaData.planets[planet];
              if (!d) return null;
              const hasDetail = d.sthana_detail || d.kala_detail;
              const isExpanded = expandedPlanets.has(planet);
              const tdBase = `p-2 border-t border-border text-foreground`;
              return (
                <React.Fragment key={planet}>
                  <tr
                    className={`${d.is_strong ? '' : 'bg-red-50/30'} ${hasDetail ? 'cursor-pointer hover:bg-muted/20' : ''}`}
                    onClick={hasDetail ? () => toggleExpand(planet) : undefined}
                  >
                    <td className={`${tdBase} font-medium`}>
                      <div className="flex items-center gap-1">
                        {hasDetail && (isExpanded
                          ? <ChevronDown className="w-3 h-3 text-primary shrink-0" />
                          : <ChevronRight className="w-3 h-3 text-primary shrink-0" />)}
                        {translatePlanet(planet, language)}
                      </div>
                    </td>
                    <td className={`${tdBase} text-center`}>{d.sthana?.toFixed ? d.sthana.toFixed(2) : d.sthana}</td>
                    <td className={`${tdBase} text-center`}>{d.dig?.toFixed ? d.dig.toFixed(2) : d.dig}</td>
                    <td className={`${tdBase} text-center`}>{d.kala?.toFixed ? d.kala.toFixed(2) : d.kala}</td>
                    <td className={`${tdBase} text-center`}>{d.cheshta?.toFixed ? d.cheshta.toFixed(2) : d.cheshta}</td>
                    <td className={`${tdBase} text-center`}>{d.naisargika?.toFixed ? d.naisargika.toFixed(2) : d.naisargika}</td>
                    <td className={`${tdBase} text-center`}>{d.drik?.toFixed ? d.drik.toFixed(2) : d.drik}</td>
                    <td className={`${tdBase} text-center`}>{d.chandra != null ? (d.chandra?.toFixed ? d.chandra.toFixed(1) : d.chandra) : '—'}</td>
                    <td className={`${tdBase} text-center font-semibold ${d.is_strong ? 'text-green-600' : 'text-red-600'}`}>
                      {d.total?.toFixed ? d.total.toFixed(2) : d.total}
                    </td>
                    <td className={`${tdBase} text-center`}>
                      <div className="flex flex-col items-center gap-0.5">
                        <span className={`font-medium ${d.ratio >= 1 ? 'text-green-600' : 'text-red-600'}`}>
                          {d.ratio?.toFixed ? d.ratio.toFixed(2) : d.ratio}x
                        </span>
                        <span className={`text-[9px] font-semibold px-1 rounded ${
                          d.ratio >= 1.5 ? 'bg-emerald-100 text-emerald-800' :
                          d.ratio >= 1.0 ? 'bg-blue-100 text-blue-800' :
                          d.ratio >= 0.7 ? 'bg-amber-100 text-amber-800' :
                                           'bg-red-100 text-red-800'
                        }`}>
                          {d.ratio >= 1.5 ? (hi ? 'बलवान' : 'Strong') :
                           d.ratio >= 1.0 ? (hi ? 'पर्याप्त' : 'Adequate') :
                           d.ratio >= 0.7 ? (hi ? 'दुर्बल' : 'Weak') :
                                            (hi ? 'अतिदुर्बल' : 'V.Weak')}
                        </span>
                      </div>
                    </td>
                    <td className={`${tdBase} text-center text-emerald-700 font-medium`}>
                      {d.ishta_phala != null ? Number(d.ishta_phala).toFixed(1) : '—'}
                    </td>
                    <td className={`${tdBase} text-center text-rose-600 font-medium`}>
                      {d.kashta_phala != null ? Number(d.kashta_phala).toFixed(1) : '—'}
                    </td>
                  </tr>
                  {isExpanded && d.sthana_detail && (
                    <tr className="bg-muted/40">
                      <td className="p-2 pl-6 text-xs text-foreground italic border-t border-border" colSpan={2}>{t('auto.sthanaDetail')}</td>
                      <td className="p-2 text-xs text-foreground border-t border-border" colSpan={10}>
                        {(['uchcha', 'saptavargaja', 'ojhayugma', 'kendra', 'drekkana'] as const)
                          .filter((k) => d.sthana_detail[k] != null)
                          .map((k) => `${STHANA_DETAIL_KEYS[k]?.[language as 'en' | 'hi'] || k}: ${d.sthana_detail[k]}`)
                          .join(' | ')}
                      </td>
                    </tr>
                  )}
                  {isExpanded && d.kala_detail && (
                    <tr className="bg-muted/40">
                      <td className="p-2 pl-6 text-xs text-foreground italic border-t border-border" colSpan={2}>{t('auto.kalaDetail')}</td>
                      <td className="p-2 text-xs text-foreground border-t border-border" colSpan={10}>
                        {(['nathonnatha', 'paksha', 'tribhaga', 'abda', 'masa', 'vara', 'hora', 'ayana'] as const)
                          .filter((k) => d.kala_detail[k] != null)
                          .map((k) => `${KALA_DETAIL_KEYS[k]?.[language as 'en' | 'hi'] || k}: ${d.kala_detail[k]}`)
                          .join(' | ')}
                      </td>
                    </tr>
                  )}
                  {isExpanded && planet === 'Moon' && d.chandravritta_bala && (
                    <tr className="bg-amber-50/40">
                      <td className="p-2 pl-6 text-xs font-medium text-amber-700 border-t border-border" colSpan={2}>
                        {hi ? 'चन्द्रवृत्त-बल (अ. 4)' : 'Chandravritta Bala (Adh. 4)'}
                      </td>
                      <td className="p-2 text-xs text-foreground/80 border-t border-border" colSpan={10}>
                        <span className="font-semibold text-amber-700 mr-2">{hi ? 'कुल:' : 'Total:'} {d.chandravritta_bala.total?.toFixed(1)}</span>
                        {hi
                          ? `पक्ष: ${d.chandravritta_bala.paksha_component?.toFixed(1)} | गरिमा: ${d.chandravritta_bala.dignity_component?.toFixed(1)}`
                          : `Paksha: ${d.chandravritta_bala.paksha_component?.toFixed(1)} | Dignity: ${d.chandravritta_bala.dignity_component?.toFixed(1)}`}
                        {' — '}
                        {hi ? d.chandravritta_bala.description_hi : d.chandravritta_bala.description_en}
                      </td>
                    </tr>
                  )}
                </React.Fragment>
              );
            })}
          </tbody>
        </table>
        <p className="text-[10px] text-muted-foreground text-right px-3 py-2 italic">
          {hi
            ? 'न्यूनतम षड्बल (फलदीपिका अध्याय 4) — सूर्य 390, चन्द्र 360, मंगल 300, बुध 420, बृहस्पति 390, शुक्र 330, शनि 300 (रूप)'
            : 'Minimum Shadbala per Phaladeepika Adh. 4 — Sun 390, Moon 360, Mars 300, Mercury 420, Jupiter 390, Venus 330, Saturn 300 (Rupas)'}
        </p>
      </div>

      {/* Ishta-Kashta Summary */}
      {shadbalaData.ishta_kashta_summary && (
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
            {hi ? 'इष्ट-कष्ट फल (फलदीपिका अध्याय 4, श्लोक 26)' : 'Ishta-Kashta Phala (Phaladeepika Adh. 4 Sloka 26)'}
          </div>
          <div className="p-4">
            <p className="text-xs text-muted-foreground mb-4">
              {hi ? 'इष्ट > कष्ट = शुभकारक ग्रह; कष्ट > इष्ट = पीड़ित ग्रह' : 'Ishta > Kashta = beneficial planet; Kashta > Ishta = afflicted planet'}
            </p>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              {PLANETS.map((planet) => {
                const s = shadbalaData.ishta_kashta_summary[planet];
                if (!s) return null;
                const isBeneficial = s.ishta > s.kashta;
                return (
                  <div key={planet} className={`rounded-xl p-3 border text-center ${isBeneficial ? 'border-emerald-300/50 bg-emerald-50/30' : 'border-rose-300/50 bg-rose-50/30'}`}>
                    <p className="text-xs font-semibold text-foreground mb-1">{translatePlanet(planet, language)}</p>
                    <div className="flex justify-center gap-2 text-xs">
                      <span className="text-emerald-700 font-medium">I: {Number(s.ishta).toFixed(1)}</span>
                      <span className="text-rose-600 font-medium">K: {Number(s.kashta).toFixed(1)}</span>
                    </div>
                    <span className={`mt-1 inline-block text-[10px] font-bold px-1.5 py-0.5 rounded ${isBeneficial ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'}`}>
                      {hi ? s.verdict_hi : s.verdict_en}
                    </span>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
