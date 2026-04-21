import { useState, useEffect } from 'react';
import { Loader2, BookOpen, ChevronDown, ChevronUp, Heart, Briefcase, Coins, Activity } from 'lucide-react';
import { api } from '@/lib/api';
import { Heading } from '@/components/ui/heading';
import TimingTheorySection from '@/components/kundli/TimingTheorySection';

interface InterpretationCategory {
  en: string;
  hi: string;
}

interface PlanetInterpretation {
  planet: string;
  house: number;
  interpretation: {
    general: InterpretationCategory;
    love: InterpretationCategory;
    career: InterpretationCategory;
    finance: InterpretationCategory;
    health: InterpretationCategory;
  };
}

interface TransitInterpretationsData {
  kundli_id?: string;
  person_name?: string;
  interpretations: PlanetInterpretation[];
}

interface Props {
  kundliId: string;
  language?: string;
}

const PLANET_ICONS: Record<string, string> = {
  Sun: '☉', Moon: '☽', Mars: '♂', Mercury: '☿',
  Jupiter: '♃', Venus: '♀', Saturn: '♄', Rahu: '☊', Ketu: '☋',
};

const CATEGORIES = [
  { key: 'love',    icon: Heart,     en: 'Love & Relationships', hi: 'प्रेम व संबंध',      cls: 'text-pink-600' },
  { key: 'career',  icon: Briefcase, en: 'Career & Work',        hi: 'करियर व कार्य',      cls: 'text-blue-600' },
  { key: 'finance', icon: Coins,     en: 'Finance & Wealth',     hi: 'धन व वित्त',         cls: 'text-amber-600' },
  { key: 'health',  icon: Activity,  en: 'Health & Vitality',    hi: 'स्वास्थ्य व जीवनशक्ति', cls: 'text-emerald-600' },
] as const;

const ohContainer = 'rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden';
const thCls       = 'p-1.5 text-left text-[10px] font-semibold uppercase tracking-wide text-primary border-b border-border';
const tdCls       = 'p-1.5 text-xs text-muted-foreground border-t border-border align-top w-[28%]';
const tdValCls    = 'p-1.5 text-xs text-foreground border-t border-border align-top break-words overflow-hidden';

function PlanetSection({ item, isHi, defaultOpen }: { item: PlanetInterpretation; isHi: boolean; defaultOpen: boolean }) {
  const [open, setOpen] = useState(defaultOpen);
  const interp = item.interpretation ?? {};
  const general = interp.general;

  return (
    <div className={ohContainer}>
      <button
        className="w-full bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2 hover:bg-sacred-gold-dark/90 transition-colors"
        onClick={() => setOpen(o => !o)}
      >
        <span className="text-base w-5 text-center">{PLANET_ICONS[item.planet] ?? item.planet?.charAt(0)}</span>
        <span className="flex-1 text-left">{item.planet}</span>
        {item.house > 0 && (
          <span className="text-[11px] font-normal bg-white/20 px-2 py-0.5 rounded mr-1">
            {isHi ? `भाव ${item.house}` : `House ${item.house}`}
          </span>
        )}
        {open ? <ChevronUp className="w-4 h-4 opacity-70" /> : <ChevronDown className="w-4 h-4 opacity-70" />}
      </button>

      {open && (
        <div>
          {/* General — always shown when open */}
          {general && (
            <div className="px-4 py-3 border-b border-border">
              <p className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wide mb-1">
                {isHi ? 'सामान्य फल' : 'General'}
              </p>
              <p className="text-sm text-foreground leading-relaxed">
                {isHi ? (general.hi || general.en) : general.en}
              </p>
            </div>
          )}

          {/* 4 categories as table */}
          <table style={{ tableLayout: 'fixed', width: '100%', borderCollapse: 'collapse' }} className="text-xs">
            <colgroup>
              <col style={{ width: '28%' }} />
              <col style={{ width: '72%' }} />
            </colgroup>
            <thead>
              <tr>
                <th className={thCls}>{isHi ? 'क्षेत्र' : 'Area'}</th>
                <th className={thCls}>{isHi ? 'फल' : 'Interpretation'}</th>
              </tr>
            </thead>
            <tbody>
              {CATEGORIES.map(({ key, icon: Icon, en, hi, cls }) => {
                const catData = interp[key];
                if (!catData?.en && !catData?.hi) return null;
                return (
                  <tr key={key}>
                    <td className={tdCls}>
                      <div className={`flex items-center gap-1.5 font-semibold ${cls}`}>
                        <Icon className="w-3 h-3 shrink-0" />
                        {isHi ? hi : en}
                      </div>
                    </td>
                    <td className={tdValCls}>
                      {isHi ? (catData.hi || catData.en) : catData.en}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default function TransitInterpretationsTab({ kundliId, language }: Props) {
  const [data, setData] = useState<TransitInterpretationsData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const isHi = language === 'hi';
  const header = (
    <div>
      <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
        <BookOpen className="w-6 h-6" />
        {isHi ? 'गोचर व्याख्या' : 'Transit Interpretations'}
      </Heading>
      <p className="text-sm text-muted-foreground">
        {isHi
          ? 'प्रत्येक गोचर ग्रह के सामान्य फल और क्षेत्र-वार (प्रेम/करियर/धन/स्वास्थ्य) संकेत।'
          : 'General and area-wise (love/career/finance/health) results for each transiting planet.'}
      </p>
    </div>
  );

  useEffect(() => {
    if (!kundliId) return;
    let cancelled = false;
    setLoading(true);
    setError(null);
    api.get<TransitInterpretationsData>(`/api/kundli/${kundliId}/transit-interpretations`)
      .then(res => { if (!cancelled) setData(res as TransitInterpretationsData); })
      .catch((err: any) => { if (!cancelled) setError(err?.message || 'Failed to load Transit Interpretations'); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [kundliId]);

  if (loading) {
    return (
      <div className="space-y-4">
        {header}
        <div className="flex items-center justify-center py-12">
          <Loader2 className="w-6 h-6 animate-spin text-primary" />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-4">
        {header}
        <div className="p-4 rounded-lg bg-red-50 border border-red-200 text-red-700 text-sm">{error}</div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="space-y-4">
        {header}
        <div className="p-8 rounded-xl border border-sacred-gold/20 text-center text-sm text-muted-foreground">
          {isHi ? 'कोई गोचर व्याख्या उपलब्ध नहीं' : 'No transit interpretations available'}
        </div>
      </div>
    );
  }

  const interpretations = data.interpretations ?? [];

  return (
    <div className="space-y-4">
      {header}

      {interpretations.length === 0 ? (
        <div className="p-8 rounded-xl border border-sacred-gold/20 text-center text-sm text-muted-foreground">
          {isHi ? 'कोई गोचर व्याख्या उपलब्ध नहीं' : 'No transit interpretations available'}
        </div>
      ) : (
        <>
          <div className="space-y-3">
            {interpretations.map((item, i) => (
              <PlanetSection key={i} item={item} isHi={isHi} defaultOpen={i === 0} />
            ))}
          </div>
          {interpretations.length > 0 && <TimingTheorySection language={language || 'en'} tab="transit-interp" />}
        </>
      )}
    </div>
  );
}
