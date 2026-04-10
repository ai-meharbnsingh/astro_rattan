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
        <h4 className="font-display font-semibold text-sacred-brown mb-4">{t('section.shadbalaStrength')}</h4>
        <div className="flex items-end justify-around gap-3" style={{ height: '220px' }}>
          {['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'].map((planet) => {
            const data = shadbalaData.planets[planet];
            if (!data) return null;
            const pct = Math.min((data.total / data.required) * 100, 150);
            const barHeight = Math.min(pct, 100);
            const barColor = data.is_strong ? '#3B2712' : '#F5F0E8';
            const barBorder = data.is_strong ? 'none' : '1px solid #C4A96A';
            const requiredPct = Math.min((1 / 1.5) * 100, 100);
            return (
              <div key={planet} className="flex flex-col items-center gap-1" style={{ flex: '1 1 0' }}>
                <span className={`text-xs font-medium ${data.is_strong ? 'text-sacred-brown' : 'text-cosmic-text'}`}>
                  {data.total}
                </span>
                <div className="relative w-full flex justify-center" style={{ height: '160px' }}>
                  <div
                    className="w-8 rounded-t-md transition-all relative"
                    style={{
                      height: `${barHeight}%`,
                      backgroundColor: barColor,
                      border: barBorder,
                      alignSelf: 'flex-end',
                    }}
                  />
                  <div
                    className="absolute w-full border-t-2 border-dashed border-sacred-brown"
                    style={{ bottom: `${requiredPct}%` }}
                    title={`Required: ${data.required}`}
                  />
                </div>
                <span className="text-xs font-medium text-sacred-brown text-center leading-tight">
                  {translatePlanet(planet, language)}
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
        <h4 className="font-display font-semibold text-sacred-brown mb-4">{t('section.detailedBreakdown')}</h4>
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
                      className={`border-t border-sacred-gold ${d.is_strong ? '' : 'bg-red-5'} ${hasDetail ? 'cursor-pointer hover:bg-sacred-gold' : ''}`}
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
                        <td className="p-2 pl-6 text-xs text-cosmic-text italic" colSpan={2}>
                          {language === 'hi' ? 'स्थान विवरण' : 'Sthana Detail'}
                        </td>
                        <td colSpan={7} className="p-2 text-xs text-cosmic-text">
                          {['uchcha', 'saptavargaja', 'ojhayugma', 'kendra', 'drekkana']
                            .filter((k) => d.sthana_detail[k] != null)
                            .map((k) => `${k}: ${d.sthana_detail[k]}`)
                            .join(' | ')}
                        </td>
                      </tr>
                    )}
                    {isExpanded && d.kala_detail && (
                      <tr className="bg-sacred-cream">
                        <td className="p-2 pl-6 text-xs text-cosmic-text italic" colSpan={2}>
                          {language === 'hi' ? 'काल विवरण' : 'Kala Detail'}
                        </td>
                        <td colSpan={7} className="p-2 text-xs text-cosmic-text">
                          {['nathonnatha', 'paksha', 'tribhaga', 'abda', 'masa', 'vara']
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
