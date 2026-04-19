import { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import {
  Loader2, ChevronDown, ChevronUp, User, Moon, Briefcase,
  Heart, Star, BookOpen, Gem, Sparkles,
} from 'lucide-react';

interface Props {
  kundliId: string;
  language: string;
}

const LIFE_AREAS: Array<{ key: string; labelEn: string; labelHi: string; icon: typeof Briefcase }> = [
  { key: 'career',    labelEn: 'Career',    labelHi: 'करियर',     icon: Briefcase },
  { key: 'marriage',  labelEn: 'Marriage',  labelHi: 'विवाह',     icon: Heart },
  { key: 'health',    labelEn: 'Health',    labelHi: 'स्वास्थ्य', icon: Star },
  { key: 'finance',   labelEn: 'Finance',   labelHi: 'वित्त',     icon: Gem },
  { key: 'education', labelEn: 'Education', labelHi: 'शिक्षा',    icon: BookOpen },
  { key: 'family',    labelEn: 'Family',    labelHi: 'परिवार',    icon: User },
];

const PLANET_ORDER = ['Sun','Moon','Mars','Mercury','Jupiter','Venus','Saturn','Rahu','Ketu'];

function Section({ title, icon: Icon, children }: { title: string; icon: typeof User; children: React.ReactNode }) {
  const [open, setOpen] = useState(true);
  return (
    <div className="rounded-xl border border-border/50 overflow-hidden">
      <button
        className="w-full flex items-center gap-2 px-4 py-3 bg-muted/30 text-left hover:bg-muted/50 transition-colors"
        onClick={() => setOpen(o => !o)}
      >
        <Icon className="w-4 h-4 text-primary shrink-0" />
        <span className="font-semibold text-sm text-foreground flex-1">{title}</span>
        {open ? <ChevronUp className="w-4 h-4 text-muted-foreground" /> : <ChevronDown className="w-4 h-4 text-muted-foreground" />}
      </button>
      {open && <div className="p-4">{children}</div>}
    </div>
  );
}

export default function KundliInterpretationsTab({ kundliId, language }: Props) {
  const isHi = language === 'hi';
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!kundliId) return;
    setLoading(true);
    api.get(`/api/interpretations/kundli/${kundliId}/full`)
      .then((res: any) => setData(res))
      .catch(() => setError(isHi ? 'व्याख्या लोड नहीं हो सकी' : 'Could not load interpretations'))
      .finally(() => setLoading(false));
  }, [kundliId]);

  if (loading) return (
    <div className="flex items-center justify-center py-16">
      <Loader2 className="w-6 h-6 animate-spin text-primary mr-2" />
      <span className="text-sm text-muted-foreground">{isHi ? 'व्याख्या लोड हो रही है...' : 'Loading interpretations...'}</span>
    </div>
  );
  if (error) return <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-red-700 text-sm">{error}</div>;
  if (!data) return null;

  const asc = data.ascendant || {};
  const lagnaNature = asc.lagna_nature || {};
  const personality = asc.personality || {};
  const nak = data.nakshatra || {};
  const life = data.life_predictions || {};
  const pih = data.planet_in_house || {};
  const dasha = data.dasha_interpretations || {};
  const gems = data.gemstones || {};

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="rounded-xl border border-primary/20 bg-card p-4">
        <div className="flex items-center gap-2 mb-1">
          <Sparkles className="w-4 h-4 text-primary" />
          <h3 className="font-semibold text-primary text-sm">
            {isHi ? 'कुंडली व्याख्या — व्यक्तित्व · जीवन क्षेत्र · ग्रह फल · दशा' : 'Kundli Interpretations — Personality · Life Areas · Planet Effects · Dasha'}
          </h3>
        </div>
        <p className="text-xs text-muted-foreground">
          {isHi ? 'जन्म कुंडली के अनुसार व्यक्तित्व, जीवन क्षेत्र, ग्रह फल और दशा व्याख्या' : 'Personality, life area predictions, planet-in-house effects, and dasha readings for this chart'}
        </p>
        {data.person_name && (
          <p className="text-xs text-foreground/70 mt-1 font-medium">{data.person_name} · {asc.sign}</p>
        )}
      </div>

      {/* 1 — Ascendant Personality */}
      {(lagnaNature.nature || personality.strengths) && (
        <Section title={isHi ? `लग्न — ${asc.sign} व्यक्तित्व` : `Ascendant — ${asc.sign} Personality`} icon={User}>
          {lagnaNature.nature && (
            <ul className="space-y-1 mb-3">
              {(lagnaNature.nature as string[]).map((n, i) => (
                <li key={i} className="text-sm text-foreground flex gap-2">
                  <span className="text-primary mt-0.5">•</span>{n}
                </li>
              ))}
            </ul>
          )}
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 text-xs">
            {lagnaNature.biggest_talent && (
              <div className="rounded-lg bg-green-50 border border-green-200 p-2">
                <p className="font-semibold text-green-700 mb-0.5">{isHi ? 'सबसे बड़ी प्रतिभा' : 'Biggest Talent'}</p>
                <p className="text-green-900">{lagnaNature.biggest_talent}</p>
              </div>
            )}
            {lagnaNature.biggest_weakness && (
              <div className="rounded-lg bg-red-50 border border-red-200 p-2">
                <p className="font-semibold text-red-700 mb-0.5">{isHi ? 'सबसे बड़ी कमज़ोरी' : 'Biggest Weakness'}</p>
                <p className="text-red-900">{lagnaNature.biggest_weakness}</p>
              </div>
            )}
            {lagnaNature.lucky_stone && (
              <div className="rounded-lg bg-amber-50 border border-amber-200 p-2">
                <p className="font-semibold text-amber-700 mb-0.5">{isHi ? 'भाग्यशाली रत्न' : 'Lucky Stone'}</p>
                <p className="text-amber-900">{lagnaNature.lucky_stone}</p>
              </div>
            )}
          </div>
        </Section>
      )}

      {/* 2 — Nakshatra */}
      {(nak.interpretation || nak.pada_prediction) && (
        <Section title={isHi ? `नक्षत्र — ${nak.name} (पाद ${nak.pada})` : `Nakshatra — ${nak.name} (Pada ${nak.pada})`} icon={Moon}>
          {nak.pada_prediction && (
            <p className="text-sm text-foreground leading-relaxed mb-3">{nak.pada_prediction}</p>
          )}
          {nak.interpretation?.character && (
            <p className="text-sm text-foreground/80 leading-relaxed italic">{nak.interpretation.character}</p>
          )}
        </Section>
      )}

      {/* 3 — Life Predictions */}
      {Object.keys(life).some(k => life[k]) && (
        <Section title={isHi ? 'जीवन क्षेत्र फल' : 'Life Area Predictions'} icon={Sparkles}>
          <div className="space-y-3">
            {LIFE_AREAS.map(({ key, labelEn, labelHi, icon: AreaIcon }) => {
              const text = life[key];
              if (!text) return null;
              return (
                <div key={key} className="flex gap-2.5">
                  <AreaIcon className="w-4 h-4 text-primary shrink-0 mt-0.5" />
                  <div>
                    <p className="text-xs font-semibold text-primary uppercase tracking-wide mb-0.5">
                      {isHi ? labelHi : labelEn}
                    </p>
                    <p className="text-sm text-foreground leading-relaxed">{text}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </Section>
      )}

      {/* 4 — Planet in House */}
      {Object.keys(pih).length > 0 && (
        <Section title={isHi ? 'ग्रह-भाव फल' : 'Planet in House Effects'} icon={Star}>
          <div className="space-y-3">
            {PLANET_ORDER.filter(p => pih[p]).map(planet => {
              const h = pih[planet] || {};
              return (
                <div key={planet} className="rounded-lg bg-muted/30 border border-border/40 p-3">
                  <p className="text-xs font-bold text-foreground mb-1">{planet}</p>
                  {h.general && <p className="text-sm text-foreground/80 leading-relaxed">{h.general}</p>}
                  {typeof h === 'string' && <p className="text-sm text-foreground/80 leading-relaxed">{h}</p>}
                  {h.auspicious && (
                    <p className="text-xs text-green-700 mt-1"><span className="font-semibold">✓ </span>{h.auspicious}</p>
                  )}
                  {h.inauspicious && (
                    <p className="text-xs text-red-700 mt-1"><span className="font-semibold">⚠ </span>{h.inauspicious}</p>
                  )}
                </div>
              );
            })}
          </div>
        </Section>
      )}

      {/* 5 — Dasha Interpretations */}
      {Object.keys(dasha).some(k => dasha[k]) && (
        <Section title={isHi ? 'महादशा व्याख्या' : 'Mahadasha Interpretations'} icon={BookOpen}>
          <div className="space-y-3">
            {PLANET_ORDER.filter(p => dasha[p]).map(planet => {
              const d = dasha[planet] || {};
              return (
                <div key={planet} className="rounded-lg bg-muted/30 border border-border/40 p-3">
                  <p className="text-xs font-bold text-foreground mb-1">{planet} {isHi ? 'महादशा' : 'Mahadasha'}</p>
                  {typeof d === 'string' && <p className="text-sm text-foreground/80 leading-relaxed">{d}</p>}
                  {d.general && <p className="text-sm text-foreground/80 leading-relaxed">{d.general}</p>}
                  {d.career && <p className="text-xs text-foreground/70 mt-1"><span className="font-semibold">{isHi ? 'करियर: ' : 'Career: '}</span>{d.career}</p>}
                  {d.health && <p className="text-xs text-foreground/70 mt-0.5"><span className="font-semibold">{isHi ? 'स्वास्थ्य: ' : 'Health: '}</span>{d.health}</p>}
                </div>
              );
            })}
          </div>
        </Section>
      )}

      {/* 6 — Gemstones */}
      {Object.keys(gems).length > 0 && (
        <Section title={isHi ? 'रत्न सुझाव' : 'Gemstone Recommendations'} icon={Gem}>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {Object.entries(gems).map(([planet, info]: [string, any]) => {
              if (!info) return null;
              const gem = typeof info === 'string' ? info : (info.stone || info.primary || info.name_en || '');
              if (!gem) return null;
              return (
                <div key={planet} className="rounded-lg bg-amber-50/60 border border-amber-200/60 p-2.5">
                  <p className="text-xs font-bold text-amber-800">{planet}</p>
                  <p className="text-sm text-amber-900">{gem}</p>
                  {info.benefits && <p className="text-xs text-amber-700/80 mt-0.5">{typeof info.benefits === 'string' ? info.benefits : info.benefits?.join(', ')}</p>}
                </div>
              );
            })}
          </div>
        </Section>
      )}
    </div>
  );
}
