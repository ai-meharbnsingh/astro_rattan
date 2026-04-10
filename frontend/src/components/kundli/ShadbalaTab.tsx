import React, { useState } from 'react';
import { Loader2, ChevronDown, ChevronRight } from 'lucide-react';
import { translatePlanet } from '@/lib/backend-translations';

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
            const pct = Math.min(ratio * 100, 150);
            const barHeight = Math.min(pct, 100);
            const isStrong = ratio >= 1.0;
            const barColor = isStrong ? 'var(--sacred-brown)' : 'var(--sacred-gold)';
            const barBg = isStrong ? 'var(--sacred-brown)' : 'var(--sacred-cream)';
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
            <div className="w-3 h-3 rounded" style={{ backgroundColor: '#3B2712' }} />
            <span>{t('kundli.strong')}</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded" style={{ backgroundColor: '#F5F0E8', border: '1px solid #C4A96A' }} />
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
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-sacred-gold">
                <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.planet')}</th>
                <th className="text-center p-2 text-sacred-gold-dark font-medium">{language === 'hi' ? 'स्थान' : 'Sthana'}</th>
                <th className="text-center p-2 text-sacred-gold-dark font-medium">{language === 'hi' ? 'दिग्' : 'Dig'}</th>
                <th className="text-center p-2 text-sacred-gold-dark font-medium">{language === 'hi' ? 'काल' : 'Kala'}</th>
                <th className="text-center p-2 text-sacred-gold-dark font-medium">{language === 'hi' ? 'चेष्टा' : 'Cheshta'}</th>
                <th className="text-center p-2 text-sacred-gold-dark font-medium">{language === 'hi' ? 'नैसर्गिक' : 'Naisargika'}</th>
                <th className="text-center p-2 text-sacred-gold-dark font-medium">{language === 'hi' ? 'दृक्' : 'Drik'}</th>
                <th className="text-center p-2 text-sacred-gold-dark font-medium">{t('table.total')}</th>
                <th className="text-center p-2 text-sacred-gold-dark font-medium">{language === 'hi' ? 'अनुपात' : 'Ratio'}</th>
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
                      className={`border-t border-sacred-gold ${d.is_strong ? '' : 'bg-red-5'} ${hasDetail ? 'cursor-pointer hover:bg-sacred-gold/5' : ''}`}
                      onClick={hasDetail ? () => toggleExpand(planet) : undefined}
                    >
                      <td className="p-2 text-sacred-brown font-medium flex items-center gap-1">
                        {hasDetail && (isExpanded ? <ChevronDown className="w-3 h-3" /> : <ChevronRight className="w-3 h-3" />)}
                        {translatePlanet(planet, language)}
                      </td>
                      <td className="text-center p-2 text-cosmic-text">{d.sthana}</td>
                      <td className="text-center p-2 text-cosmic-text">{d.dig}</td>
                      <td className="text-center p-2 text-cosmic-text">{d.kala}</td>
                      <td className="text-center p-2 text-cosmic-text">{d.cheshta}</td>
                      <td className="text-center p-2 text-cosmic-text">{d.naisargika}</td>
                      <td className="text-center p-2 text-cosmic-text">{d.drik}</td>
                      <td className={`text-center p-2 font-semibold ${d.is_strong ? 'text-sacred-gold-dark' : 'text-wax-red-deep'}`}>{d.total}</td>
                      <td className={`text-center p-2 font-medium ${d.ratio >= 1 ? 'text-sacred-gold-dark' : 'text-wax-red-deep'}`}>{d.ratio}x</td>
                    </tr>
                    {isExpanded && d.sthana_detail && (
                      <tr className="bg-sacred-cream">
                        <td className="p-2 pl-6 text-sm text-cosmic-text italic" colSpan={2}>
                          {language === 'hi' ? 'स्थान विवरण' : 'Sthana Detail'}
                        </td>
                        <td colSpan={7} className="p-2 text-sm text-cosmic-text">
                          {['uchcha', 'saptavargaja', 'ojhayugma', 'kendra', 'drekkana']
                            .filter((k) => d.sthana_detail[k] != null)
                            .map((k) => `${k}: ${d.sthana_detail[k]}`)
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
                          {['nathonnatha', 'paksha', 'tribhaga', 'abda', 'masa', 'vara', 'hora', 'ayana']
                            .filter((k) => d.kala_detail[k] != null)
                            .map((k) => `${k}: ${d.kala_detail[k]}`)
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
