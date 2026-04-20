import { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import {
  Loader2, ChevronDown, ChevronUp, User, Moon, Briefcase,
  Heart, Star, BookOpen, Gem, Sparkles,
} from 'lucide-react';
import { Heading } from '@/components/ui/heading';

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

const thCls     = 'p-1.5 text-left text-[10px] font-semibold uppercase tracking-wide text-primary border-b border-border';
const tdCls     = 'p-1.5 text-xs text-foreground border-t border-border align-top';
const tdMuted   = 'p-1.5 text-xs text-muted-foreground border-t border-border align-top';
const tdWrapCls = 'p-1.5 text-xs text-foreground border-t border-border align-top break-words overflow-hidden';

function OhSection({
  title, icon: Icon, count, children, defaultOpen = true,
}: {
  title: string; icon: typeof User; count?: number; children: React.ReactNode; defaultOpen?: boolean;
}) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
      <button
        className="w-full bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2 hover:bg-sacred-gold-dark/90 transition-colors"
        onClick={() => setOpen(o => !o)}
      >
        <Icon className="w-4 h-4 shrink-0" />
        <span className="flex-1 text-left">{title}</span>
        {count !== undefined && (
          <span className="text-[12px] font-normal opacity-80 mr-1">{count}</span>
        )}
        {open ? <ChevronUp className="w-4 h-4 opacity-70" /> : <ChevronDown className="w-4 h-4 opacity-70" />}
      </button>
      {open && <div>{children}</div>}
    </div>
  );
}

export default function KundliInterpretationsTab({ kundliId, language }: Props) {
  const isHi = language === 'hi';
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const header = (
    <div>
      <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
        <BookOpen className="w-6 h-6" />
        {isHi ? 'कुंडली व्याख्या' : 'Interpretations'}
      </Heading>
      <p className="text-sm text-muted-foreground">
        {isHi ? 'सभी जीवन क्षेत्रों के लिए व्यापक कुंडली व्याख्याएं' : 'Comprehensive chart interpretations for all life areas'}
      </p>
    </div>
  );

  useEffect(() => {
    if (!kundliId) return;
    setLoading(true);
    api.get(`/api/interpretations/kundli/${kundliId}/full`)
      .then((res: any) => setData(res))
      .catch(() => setError(isHi ? 'व्याख्या लोड नहीं हो सकी' : 'Could not load interpretations'))
      .finally(() => setLoading(false));
  }, [kundliId]);

  if (loading) return (
    <div className="space-y-4">
      {header}
      <div className="flex items-center justify-center py-16">
        <Loader2 className="w-6 h-6 animate-spin text-primary mr-2" />
        <span className="text-sm text-muted-foreground">{isHi ? 'व्याख्या लोड हो रही है...' : 'Loading interpretations...'}</span>
      </div>
    </div>
  );
  if (error) return (
    <div className="space-y-4">
      {header}
      <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-red-700 text-sm">{error}</div>
    </div>
  );
  if (!data) return (
    <div className="space-y-4">
      {header}
      <div className="rounded-xl border border-border p-6 text-center text-muted-foreground text-sm">
        {isHi ? 'डेटा उपलब्ध नहीं है' : 'No data available'}
      </div>
    </div>
  );

  const asc         = data.ascendant || {};
  const lagnaNature = asc.lagna_nature || {};
  const nak         = data.nakshatra || {};
  const life        = data.life_predictions || {};
  const pih         = data.planet_in_house || {};
  const dasha       = data.dasha_interpretations || {};
  const gems        = data.gemstones || {};

  const lifeRows    = LIFE_AREAS.filter(({ key }) => life[key]);
  const pihPlanets  = PLANET_ORDER.filter(p => pih[p]);
  const dashaPlanets= PLANET_ORDER.filter(p => dasha[p]);
  const gemEntries  = Object.entries(gems).filter(([, info]: [string, any]) => {
    const gem = typeof info === 'string' ? info : (info?.stone || info?.primary || info?.name_en || '');
    return !!gem;
  });

  return (
    <div className="space-y-4">

      {header}

      {/* 1 — Ascendant Personality */}
      {(lagnaNature.nature || lagnaNature.biggest_talent) && (
        <OhSection
          title={isHi ? `लग्न — ${asc.sign} व्यक्तित्व` : `Ascendant — ${asc.sign} Personality`}
          icon={User}
        >
          <div className="px-4 py-3 space-y-3">
            {lagnaNature.nature && (
              <ul className="space-y-1">
                {(lagnaNature.nature as string[]).map((n: string, i: number) => (
                  <li key={i} className="text-sm text-foreground flex gap-2">
                    <span className="text-sacred-gold-dark mt-0.5 shrink-0">•</span>{n}
                  </li>
                ))}
              </ul>
            )}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
              {lagnaNature.biggest_talent && (
                <div className="rounded-lg border border-emerald-200 bg-emerald-50 p-2.5">
                  <p className="text-[10px] font-semibold text-emerald-700 uppercase tracking-wide mb-0.5">
                    {isHi ? 'सबसे बड़ी प्रतिभा' : 'Biggest Talent'}
                  </p>
                  <p className="text-xs text-emerald-900">{lagnaNature.biggest_talent}</p>
                </div>
              )}
              {lagnaNature.biggest_weakness && (
                <div className="rounded-lg border border-red-200 bg-red-50 p-2.5">
                  <p className="text-[10px] font-semibold text-red-700 uppercase tracking-wide mb-0.5">
                    {isHi ? 'सबसे बड़ी कमज़ोरी' : 'Biggest Weakness'}
                  </p>
                  <p className="text-xs text-red-900">{lagnaNature.biggest_weakness}</p>
                </div>
              )}
              {lagnaNature.lucky_stone && (
                <div className="rounded-lg border border-amber-200 bg-amber-50 p-2.5">
                  <p className="text-[10px] font-semibold text-amber-700 uppercase tracking-wide mb-0.5">
                    {isHi ? 'भाग्यशाली रत्न' : 'Lucky Stone'}
                  </p>
                  <p className="text-xs text-amber-900">{lagnaNature.lucky_stone}</p>
                </div>
              )}
            </div>
          </div>
        </OhSection>
      )}

      {/* 2 — Nakshatra */}
      {(nak.interpretation || nak.pada_prediction) && (
        <OhSection
          title={isHi ? `नक्षत्र — ${nak.name} (पाद ${nak.pada})` : `Nakshatra — ${nak.name} (Pada ${nak.pada})`}
          icon={Moon}
        >
          <div className="px-4 py-3 space-y-2">
            {nak.pada_prediction && (
              <p className="text-sm text-foreground leading-relaxed">{nak.pada_prediction}</p>
            )}
            {nak.interpretation?.character && (
              <p className="text-sm text-foreground/80 leading-relaxed italic">{nak.interpretation.character}</p>
            )}
          </div>
        </OhSection>
      )}

      {/* 3 — Life Predictions */}
      {lifeRows.length > 0 && (
        <OhSection
          title={isHi ? 'जीवन क्षेत्र फल' : 'Life Area Predictions'}
          icon={Sparkles}
          count={lifeRows.length}
        >
          <table style={{ tableLayout: 'fixed', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
            <colgroup>
              <col style={{ width: '15%' }} />
              <col style={{ width: '85%' }} />
            </colgroup>
            <thead>
              <tr>
                <th className={thCls}>{isHi ? 'क्षेत्र' : 'Area'}</th>
                <th className={thCls}>{isHi ? 'फलादेश' : 'Prediction'}</th>
              </tr>
            </thead>
            <tbody>
              {lifeRows.map(({ key, labelEn, labelHi, icon: AreaIcon }) => (
                <tr key={key}>
                  <td className={tdMuted}>
                    <div className="flex items-center gap-1.5">
                      <AreaIcon className="w-3 h-3 shrink-0" />
                      <span className="font-medium">{isHi ? labelHi : labelEn}</span>
                    </div>
                  </td>
                  <td className={tdWrapCls}>{life[key]}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </OhSection>
      )}

      {/* 4 — Planet in House */}
      {pihPlanets.length > 0 && (
        <OhSection
          title={isHi ? 'ग्रह-भाव फल' : 'Planet in House Effects'}
          icon={Star}
          count={pihPlanets.length}
        >
          <table style={{ tableLayout: 'fixed', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
            <colgroup>
              <col style={{ width: '13%' }} />
              <col style={{ width: '44%' }} />
              <col style={{ width: '43%' }} />
            </colgroup>
            <thead>
              <tr>
                <th className={thCls}>{isHi ? 'ग्रह' : 'Planet'}</th>
                <th className={thCls}>{isHi ? 'शुभ फल' : 'Auspicious'}</th>
                <th className={thCls}>{isHi ? 'अशुभ फल' : 'Inauspicious'}</th>
              </tr>
            </thead>
            <tbody>
              {pihPlanets.map(planet => {
                const h = pih[planet] || {};
                return (
                  <tr key={planet}>
                    <td className={`${tdCls} font-semibold`}>{planet}</td>
                    <td className={tdWrapCls}>
                      {h.auspicious
                        ? <span className="text-emerald-700">{h.auspicious}</span>
                        : <span className="text-muted-foreground">—</span>}
                    </td>
                    <td className={tdWrapCls}>
                      {h.inauspicious
                        ? <span className="text-red-700">{h.inauspicious}</span>
                        : <span className="text-muted-foreground">—</span>}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </OhSection>
      )}

      {/* 5 — Dasha Interpretations */}
      {dashaPlanets.length > 0 && (
        <OhSection
          title={isHi ? 'महादशा व्याख्या' : 'Mahadasha Interpretations'}
          icon={BookOpen}
          count={dashaPlanets.length}
        >
          <table style={{ tableLayout: 'fixed', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
            <colgroup>
              <col style={{ width: '13%' }} />
              <col style={{ width: '39%' }} />
              <col style={{ width: '24%' }} />
              <col style={{ width: '24%' }} />
            </colgroup>
            <thead>
              <tr>
                <th className={thCls}>{isHi ? 'दशा' : 'Dasha'}</th>
                <th className={thCls}>{isHi ? 'सामान्य फल' : 'General'}</th>
                <th className={thCls}>{isHi ? 'शुभ प्रभाव' : 'Beneficial'}</th>
                <th className={thCls}>{isHi ? 'अशुभ प्रभाव' : 'Challenging'}</th>
              </tr>
            </thead>
            <tbody>
              {dashaPlanets.map(planet => {
                const d = dasha[planet] || {};
                const generalArr = Array.isArray(d.general) ? d.general : (d.general ? [d.general] : []);
                const goodArr    = Array.isArray(d.specific_good) ? d.specific_good : [];
                const badArr     = Array.isArray(d.specific_bad)  ? d.specific_bad  : [];
                return (
                  <tr key={planet}>
                    <td className={`${tdCls} font-semibold`}>{planet}</td>
                    <td className={tdWrapCls}>
                      {generalArr.length > 0
                        ? <ul className="space-y-0.5">{generalArr.map((g: string, i: number) => <li key={i} className="flex gap-1"><span className="text-sacred-gold-dark shrink-0">•</span>{g}</li>)}</ul>
                        : <span className="text-muted-foreground">—</span>}
                    </td>
                    <td className={tdWrapCls}>
                      {goodArr.length > 0
                        ? <ul className="space-y-0.5">{goodArr.map((g: string, i: number) => <li key={i} className="flex gap-1 text-emerald-700"><span className="shrink-0">•</span>{g}</li>)}</ul>
                        : <span className="text-muted-foreground">—</span>}
                    </td>
                    <td className={tdWrapCls}>
                      {badArr.length > 0
                        ? <ul className="space-y-0.5">{badArr.map((b: string, i: number) => <li key={i} className="flex gap-1 text-red-700"><span className="shrink-0">•</span>{b}</li>)}</ul>
                        : <span className="text-muted-foreground">—</span>}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </OhSection>
      )}

      {/* 6 — Gemstones */}
      {gemEntries.length > 0 && (
        <OhSection
          title={isHi ? 'रत्न सुझाव' : 'Gemstone Recommendations'}
          icon={Gem}
          count={gemEntries.length}
        >
          <table style={{ tableLayout: 'fixed', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
            <colgroup>
              <col style={{ width: '11%' }} />
              <col style={{ width: '17%' }} />
              <col style={{ width: '15%' }} />
              <col style={{ width: '22%' }} />
              <col style={{ width: '35%' }} />
            </colgroup>
            <thead>
              <tr>
                <th className={thCls}>{isHi ? 'ग्रह' : 'Planet'}</th>
                <th className={thCls}>{isHi ? 'रत्न' : 'Stone'}</th>
                <th className={thCls}>{isHi ? 'उपरत्न' : 'Alt Stone'}</th>
                <th className={thCls}>{isHi ? 'धारण विधि' : 'Wear (Metal · Finger · Day)'}</th>
                <th className={thCls}>{isHi ? 'विवरण' : 'Description'}</th>
              </tr>
            </thead>
            <tbody>
              {gemEntries.map(([planet, info]: [string, any]) => {
                const gem        = typeof info === 'string' ? info : (info?.stone || '');
                const upratna    = info?.upratna || '—';
                const wearParts  = [info?.metal, info?.finger, info?.day].filter(Boolean);
                const wearText   = wearParts.join(' · ') || '—';
                const description= info?.description || '—';
                return (
                  <tr key={planet}>
                    <td className={`${tdCls} font-semibold`}>{planet}</td>
                    <td className={`${tdCls} text-amber-700 font-medium`}>{gem || '—'}</td>
                    <td className={`${tdCls} text-amber-600`}>{upratna}</td>
                    <td className={tdWrapCls}>{wearText}</td>
                    <td className={tdWrapCls}>{description}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </OhSection>
      )}
    </div>
  );
}
