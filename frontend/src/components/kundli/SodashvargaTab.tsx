import { Loader2 } from 'lucide-react';
import { translatePlanet } from '@/lib/backend-translations';

interface SodashvargaTabProps {
  sodashvargaData: any;
  loadingSodashvarga: boolean;
  language: string;
  t: (key: string) => string;
}

export default function SodashvargaTab({ sodashvargaData, loadingSodashvarga, language, t }: SodashvargaTabProps) {
  if (loadingSodashvarga) {
    return (
      <div className="flex items-center justify-center py-12"><Loader2 className="w-6 h-6 animate-spin text-sacred-gold" /><span className="ml-2 text-cosmic-text">{t('kundli.loadingSodashvarga')}</span></div>
    );
  }

  if (!sodashvargaData) {
    return <p className="text-center text-cosmic-text py-8">{t('common.noData')}</p>;
  }

  const strengthColors: Record<string, string> = {
    Strong: 'text-green-600 bg-green-500',
    Medium: 'text-yellow-600 bg-yellow-500',
    Weak: 'text-red-500 bg-red-500',
  };

  const dignityLabels: Record<string, { label: string; color: string }> = {
    exalted: { label: 'Ex', color: 'text-green-700 bg-green-500' },
    own: { label: 'Own', color: 'text-blue-700 bg-blue-500' },
    moolatrikona: { label: 'Moo', color: 'text-blue-700 bg-blue-500' },
    friend: { label: 'Fr', color: 'text-yellow-700 bg-yellow-500' },
    neutral: { label: 'Neu', color: 'text-gray-600 bg-gray-500' },
    enemy: { label: 'En', color: 'text-orange-700 bg-orange-500' },
    debilitated: { label: 'Deb', color: 'text-red-700 bg-red-500' },
  };

  return (
    <div className="space-y-6">
      {/* Varga Table */}
      <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-4 overflow-x-auto">
        <h4 className="font-display font-semibold text-sacred-brown mb-3">{t('section.sodashvargaTitle')}</h4>
        {(() => {
          const rows = sodashvargaData.varga_table || (Array.isArray(sodashvargaData.by_sign) ? sodashvargaData.by_sign : []);
          if (rows.length > 0) {
            return (
              <table className="w-full text-sm min-w-[700px]">
                <thead><tr className="bg-sacred-gold">
                  <th className="text-left p-2 text-sacred-gold-dark font-medium">{t('table.varga')}</th>
                  {['Su', 'Mo', 'Ma', 'Me', 'Ju', 'Ve', 'Sa', 'Ra', 'Ke'].map(p => (
                    <th key={p} className="text-center p-1.5 text-sacred-gold-dark font-medium">{p}</th>
                  ))}
                </tr></thead>
                <tbody>
                  {rows.map((row: any) => {
                    const planets = row.placements || row.planets;
                    const planetEntries = Array.isArray(planets)
                      ? planets
                      : typeof planets === 'object'
                        ? ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu'].map(p => planets[p] || '')
                        : [];
                    return (
                      <tr key={row.varga || row.division || row.name} className="border-t border-sacred-gold">
                        <td className="p-2 font-semibold text-sacred-brown whitespace-nowrap">{row.varga || row.name || `D${row.division}`}</td>
                        {planetEntries.map((pl: any, i: number) => {
                          const sign = typeof pl === 'string' ? pl?.slice(0, 3) : (pl?.sign_abbr || pl?.sign?.slice(0, 3) || '');
                          const dignity = typeof pl === 'object' ? pl?.dignity?.toLowerCase() : '';
                          const dignityColors: Record<string, string> = {
                            exalted: 'bg-green-500 text-green-700', own: 'bg-blue-500 text-blue-700',
                            moolatrikona: 'bg-blue-500 text-blue-700', friend: 'bg-yellow-500 text-yellow-700',
                            enemy: 'bg-orange-500 text-orange-700', debilitated: 'bg-red-500 text-red-700',
                          };
                          return <td key={i} className={`p-1.5 text-center text-sm rounded ${dignityColors[dignity] || ''}`}>{sign}</td>;
                        })}
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            );
          }
          // Fallback: by_sign is a dict
          if (sodashvargaData.by_sign && typeof sodashvargaData.by_sign === 'object') {
            return (
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 text-sm">
                {Object.entries(sodashvargaData.by_sign).map(([planet, data]: [string, any]) => (
                  <div key={planet} className="bg-white rounded-lg p-3">
                    <p className="font-semibold text-sacred-brown mb-1">{planet}</p>
                    {typeof data === 'object' && Object.entries(data as Record<string, any>).map(([varga, sign]) => (
                      <p key={varga} className="text-cosmic-text">{varga}: {String(sign)}</p>
                    ))}
                  </div>
                ))}
              </div>
            );
          }
          return <p className="text-center text-cosmic-text">{t('common.noData')}</p>;
        })()}
        <div className="flex flex-wrap gap-2 mt-3 text-sm">
          <span className="px-2 py-1 rounded bg-green-500 text-green-700">{t('dignity.exalted')}</span>
          <span className="px-2 py-1 rounded bg-blue-500 text-blue-700">{t('dignity.ownMoolatrikona')}</span>
          <span className="px-2 py-1 rounded bg-yellow-500 text-yellow-700">{t('dignity.friend')}</span>
          <span className="px-2 py-1 rounded bg-orange-500 text-orange-700">{t('dignity.enemy')}</span>
          <span className="px-2 py-1 rounded bg-red-500 text-red-700">{t('dignity.debilitated')}</span>
        </div>
      </div>

      {/* Vimshopak Bala */}
      {(sodashvargaData.by_planet || sodashvargaData.vimshopak) && (
        <div className="bg-sacred-cream rounded-xl border border-sacred-gold p-4">
          <h4 className="font-display font-semibold text-sacred-brown mb-3">{t('section.vimshopakBala')}</h4>
          <div className="space-y-3">
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
                <div key={v.planet} className="space-y-1">
                  <div className="flex items-center gap-3 text-sm">
                    <span className="w-12 text-sacred-brown font-medium">{translatePlanet(v.planet || '', language).slice(0, 4)}</span>
                    <div className="flex-1 bg-sacred-gold rounded-full h-4">
                      <div className="bg-sacred-gold rounded-full h-4 transition-all" style={{ width: `${Math.min(100, ((typeof v.score === 'number' ? v.score : 0) / 20) * 100)}%` }} />
                    </div>
                    <span className="w-16 text-right text-cosmic-text text-sm">{typeof v.score === 'number' ? v.score.toFixed(1) : '?'} / 20</span>
                    {v.percentage != null && (
                      <span className="w-12 text-right text-sacred-brown font-semibold text-sm">{v.percentage}%</span>
                    )}
                    {v.strength && (
                      <span className={`px-1.5 py-0.5 rounded text-label font-semibold ${strengthColors[v.strength] || 'text-gray-500 bg-gray-500'}`}>{v.strength}</span>
                    )}
                  </div>
                  {v.dignities && typeof v.dignities === 'object' && (
                    <div className="flex items-center gap-1 ml-[60px] flex-wrap">
                      {Object.entries(v.dignities as Record<string, number>)
                        .filter(([, count]) => (count as number) > 0)
                        .map(([dignity, count]) => {
                          const info = dignityLabels[dignity] || { label: dignity.slice(0, 3), color: 'text-gray-500 bg-gray-500' };
                          return (
                            <span key={dignity} className={`px-1.5 py-0.5 rounded text-label font-medium ${info.color}`}>
                              {info.label}:{count as number}
                            </span>
                          );
                        })}
                    </div>
                  )}
                </div>
              ));
            })()}
          </div>
        </div>
      )}
    </div>
  );
}
