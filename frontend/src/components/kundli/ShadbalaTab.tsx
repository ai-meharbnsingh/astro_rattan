import React, { useState } from 'react';
import { Loader2, ChevronDown, ChevronRight } from 'lucide-react';
import { translatePlanet } from '@/lib/backend-translations';

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
        <Loader2 className="w-6 h-6 animate-spin text-sacred-gold" />
        <span className="ml-2 text-cosmic-text">{t('kundli.calculatingShadbala')}</span>
      </div>
    );
  }

  if (!shadbalaData?.planets) {
    return <p className="text-center text-cosmic-text py-8">{t('kundli.clickShadbalaTab')}</p>;
  }

  return (
    <div className="space-y-6">
      <div className="bg-sacred-cream rounded-xl p-5 border border-sacred-gold">
        <h4 className="text-lg font-semibold text-gray-800 mb-4">{t('section.shadbalaStrength')}</h4>
        <div className="flex items-end justify-around gap-2" style={{ height: '280px' }}>
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
                <span className={`text-sm font-bold ${isStrong ? 'text-sacred-brown' : 'text-cosmic-text'}`}>
                  {total.toFixed(1)}
                </span>
                <div className="relative w-full flex justify-center bg-sacred-gold/20 rounded-t-lg" style={{ height: '200px' }}>
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
                        <span className="text-xs text-sacred-gold-dark">★</span>
                      </div>
                    )}
                  </div>
                </div>
                <span className="text-xs font-medium text-sacred-brown text-center leading-tight mt-1">
                  {translatePlanet(planet, language)}
                </span>
                <span className={`text-xs ${isStrong ? 'text-green-600 font-semibold' : 'text-red-500'}`}>
                  {isStrong ? '✓' : '✗'}
                </span>
              </div>
            );
          })}
        </div>
        <div className="flex items-center justify-center gap-6 mt-4 text-sm text-cosmic-text">
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded" style={{ backgroundColor: '#16a34a' }} />
            <span>{t('kundli.strong')}</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded" style={{ backgroundColor: '#dc2626' }} />
            <span>{t('kundli.weak')}</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-6 border-t-2 border-dashed border-sacred-brown" />
            <span>{language === 'hi' ? 'आवश्यक' : 'Required'}</span>
          </div>
        </div>
      </div>

      <div className="bg-sacred-cream rounded-xl p-5 border border-sacred-gold">
        <h4 className="text-lg font-semibold text-gray-800 mb-4">{t('section.detailedBreakdown')}</h4>
        <div className="overflow-x-auto">
          <table className="w-full text-sm border-collapse">
            <thead>
              <tr className="bg-sacred-gold">
                <th className="text-left p-2 text-sacred-gold-dark font-medium text-xs">{t('table.planet')}</th>
                <th className="text-center p-2 text-sacred-gold-dark font-medium text-xs">{language === 'hi' ? 'स्थान' : 'Sthana'}</th>
                <th className="text-center p-2 text-sacred-gold-dark font-medium text-xs">{language === 'hi' ? 'दिग्' : 'Dig'}</th>
                <th className="text-center p-2 text-sacred-gold-dark font-medium text-xs">{language === 'hi' ? 'काल' : 'Kala'}</th>
                <th className="text-center p-2 text-sacred-gold-dark font-medium text-xs">{language === 'hi' ? 'चेष्टा' : 'Cheshta'}</th>
                <th className="text-center p-2 text-sacred-gold-dark font-medium text-xs">{language === 'hi' ? 'नैसर्गिक' : 'Naisargika'}</th>
                <th className="text-center p-2 text-sacred-gold-dark font-medium text-xs">{language === 'hi' ? 'दृक्' : 'Drik'}</th>
                <th className="text-center p-2 text-sacred-gold-dark font-medium text-xs">{t('table.total')}</th>
                <th className="text-center p-2 text-sacred-gold-dark font-medium text-xs">{language === 'hi' ? 'अनुपात' : 'Ratio'}</th>
              </tr>
            </thead>
            <tbody>
              {['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'].map((planet) => {
                const d = shadbalaData.planets[planet];
                if (!d) return null;
                const hasDetail = d.sthana_detail || d.kala_detail;
                const isExpanded = expandedPlanets.has(planet);
                return (
                  <React.Fragment key={planet}>
                    <tr
                      className={`border-t border-sacred-gold/50 ${d.is_strong ? 'bg-white' : 'bg-red-50/30'} ${hasDetail ? 'cursor-pointer hover:bg-sacred-gold/10' : ''} transition-colors`}
                      onClick={hasDetail ? () => toggleExpand(planet) : undefined}
                    >
                      <td className="p-2 text-sacred-brown font-medium">
                        <div className="flex items-center gap-1">
                          {hasDetail && (isExpanded ? <ChevronDown className="w-3 h-3 text-sacred-gold-dark" /> : <ChevronRight className="w-3 h-3 text-sacred-gold-dark" />)}
                          {translatePlanet(planet, language)}
                        </div>
                      </td>
                      <td className="text-center p-2 text-cosmic-text text-xs">{d.sthana?.toFixed ? d.sthana.toFixed(2) : d.sthana}</td>
                      <td className="text-center p-2 text-cosmic-text text-xs">{d.dig?.toFixed ? d.dig.toFixed(2) : d.dig}</td>
                      <td className="text-center p-2 text-cosmic-text text-xs">{d.kala?.toFixed ? d.kala.toFixed(2) : d.kala}</td>
                      <td className="text-center p-2 text-cosmic-text text-xs">{d.cheshta?.toFixed ? d.cheshta.toFixed(2) : d.cheshta}</td>
                      <td className="text-center p-2 text-cosmic-text text-xs">{d.naisargika?.toFixed ? d.naisargika.toFixed(2) : d.naisargika}</td>
                      <td className="text-center p-2 text-cosmic-text text-xs">{d.drik?.toFixed ? d.drik.toFixed(2) : d.drik}</td>
                      <td className={`text-center p-2 font-semibold text-xs ${d.is_strong ? 'text-green-600' : 'text-red-600'}`}>{d.total?.toFixed ? d.total.toFixed(2) : d.total}</td>
                      <td className={`text-center p-2 font-medium text-xs ${d.ratio >= 1 ? 'text-green-600' : 'text-red-600'}`}>{d.ratio?.toFixed ? d.ratio.toFixed(2) : d.ratio}x</td>
                    </tr>
                    {isExpanded && d.sthana_detail && (
                      <tr className="bg-sacred-cream">
                        <td className="p-2 pl-6 text-sm text-cosmic-text italic" colSpan={2}>
                          {language === 'hi' ? 'स्थान विवरण' : 'Sthana Detail'}
                        </td>
                        <td colSpan={7} className="p-2 text-sm text-cosmic-text">
                          {(['uchcha', 'saptavargaja', 'ojhayugma', 'kendra', 'drekkana'] as const)
                            .filter((k) => d.sthana_detail[k] != null)
                            .map((k) => {
                              const label = STHANA_DETAIL_KEYS[k]?.[language as 'en' | 'hi'] || k;
                              return `${label}: ${d.sthana_detail[k]}`;
                            })
                            .join(' | ')}
                        </td>
                      </tr>
                    )}
                    {isExpanded && d.kala_detail && (
                      <tr className="bg-sacred-cream">
                        <td className="p-2 pl-6 text-sm text-cosmic-text italic" colSpan={2}>
                          {language === 'hi' ? 'काल विवरण' : 'Kala Detail'}
                        </td>
                        <td colSpan={7} className="p-2 text-sm text-cosmic-text">
                          {(['nathonnatha', 'paksha', 'tribhaga', 'abda', 'masa', 'vara', 'hora', 'ayana'] as const)
                            .filter((k) => d.kala_detail[k] != null)
                            .map((k) => {
                              const label = KALA_DETAIL_KEYS[k]?.[language as 'en' | 'hi'] || k;
                              return `${label}: ${d.kala_detail[k]}`;
                            })
                            .join(' | ')}
                        </td>
                      </tr>
                    )}
                  </React.Fragment>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
