import { useEffect, useState } from 'react';
import { Clock, ChevronLeft, ChevronRight, Loader2, Star } from 'lucide-react';
import { api } from '@/lib/api';
import { Heading } from '@/components/ui/heading';
import { pickLang } from './safe-render';

interface SaalaPeriod {
  age: number;
  planet: string;
  planet_hi: string;
  en_desc: string;
  hi_desc: string;
}

interface DashaData {
  current_age: number;
  current_saala_grah: {
    planet: string;
    planet_hi: string;
    sequence_position: number;
    cycle_year: number;
    en_desc: string;
    hi_desc: string;
  };
  next_saala_grah: {
    planet: string;
    planet_hi: string;
    en_desc: string;
    hi_desc: string;
  };
  life_phase: {
    phase: number;
    label: string;
    years_in_phase: number;
    phase_end_age: number;
  };
  years_into_phase: number;
  years_remaining_in_phase: number;
  upcoming_periods: SaalaPeriod[];
  past_periods: SaalaPeriod[];
}

const PLANET_COLORS: Record<string, string> = {
  Sun: 'text-amber-500 bg-amber-50 border-amber-200',
  Moon: 'text-blue-400 bg-blue-50 border-blue-200',
  Mars: 'text-red-500 bg-red-50 border-red-200',
  Mercury: 'text-green-500 bg-green-50 border-green-200',
  Jupiter: 'text-yellow-600 bg-yellow-50 border-yellow-200',
  Venus: 'text-pink-500 bg-pink-50 border-pink-200',
  Saturn: 'text-gray-600 bg-gray-100 border-gray-300',
  Rahu: 'text-purple-600 bg-purple-50 border-purple-200',
  Ketu: 'text-orange-600 bg-orange-50 border-orange-200',
};

function getPlanetColor(planet: string) {
  return PLANET_COLORS[planet] || 'text-sacred-gold bg-sacred-gold/10 border-sacred-gold/30';
}

interface Props {
  kundliId: string;
  language: string;
}

export default function LalKitabDashaTab({ kundliId, language }: Props) {
  const [data, setData] = useState<DashaData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const isHi = language === 'hi';

  useEffect(() => {
    if (!kundliId) {
      setData(null);
      setError('');
      setLoading(false);
      return;
    }

    setLoading(true);
    setError('');

    api.get(`/api/lalkitab/dasha/${kundliId}`)
      .then(setData)
      .catch(() => setError(isHi ? 'दशा डेटा लोड नहीं हो सका' : 'Could not load dasha data'))
      .finally(() => setLoading(false));
  }, [kundliId, isHi]);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-6 h-6 animate-spin text-sacred-gold mr-2" />
        <span className="text-muted-foreground text-sm">
          {isHi ? 'साला ग्रह दशा लोड हो रही है...' : 'Loading Saala Grah Dasha...'}
        </span>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-red-700 text-sm">
        {error || (isHi ? 'डेटा उपलब्ध नहीं है' : 'No data')}
      </div>
    );
  }

  const {
    current_saala_grah: current,
    next_saala_grah: next,
    life_phase,
    years_into_phase,
    years_remaining_in_phase,
    current_age,
    upcoming_periods,
    past_periods,
  } = data;

  const denom = (years_into_phase || 0) + (years_remaining_in_phase || 0);
  const phaseProgress = denom > 0 ? Math.round(((years_into_phase || 0) / denom) * 100) : 0;
  const currentColor = getPlanetColor(current.planet);

  return (
    <div className="space-y-6">
      <div className="rounded-xl border border-sacred-gold/20 bg-card p-5">
        <div className="flex items-center gap-2 mb-1">
          <Clock className="w-4 h-4 text-sacred-gold" />
          <h3 className="font-semibold text-sacred-gold text-sm">{isHi ? 'साला ग्रह दशा' : 'Saala Grah Dasha'}</h3>
        </div>
        <p className="text-xs text-muted-foreground">
          {isHi
            ? 'लाल किताब की सालाना ग्रह दशा — जन्म से प्रत्येक वर्ष एक ग्रह का प्रभाव'
            : 'Lal Kitab annual planet cycle — one ruling planet per year of life'}
        </p>
      </div>

      <div className={`rounded-xl border-2 p-5 ${currentColor}`}>
        <div className="flex items-start justify-between gap-3">
          <div>
            <div className="text-xs font-medium uppercase tracking-wide opacity-60 mb-1">
              {isHi ? `आयु ${current_age} — वर्तमान साला ग्रह` : `Age ${current_age} — Current Saala Grah`}
            </div>
            <div className="text-2xl font-bold mb-0.5">{isHi ? current.planet_hi : current.planet}</div>
            <div className="text-xs opacity-70 mb-3">
              {isHi ? current.planet_hi : current.planet} &bull; {isHi ? 'क्रम स्थान' : 'Sequence'}{' '}
              {current.sequence_position}/9 &bull; {isHi ? 'चक्र वर्ष' : 'Cycle year'} {current.cycle_year}
            </div>
            <p className="text-sm leading-relaxed">{pickLang({ en: current.en_desc, hi: current.hi_desc }, isHi)}</p>
          </div>
          <Star className="w-8 h-8 opacity-40 flex-shrink-0 mt-1" />
        </div>

        <div className="mt-4 pt-4 border-t border-current/20">
          <div className="flex justify-between text-xs mb-1.5 opacity-70">
            <span>{isHi ? `जीवन चरण: ${life_phase?.label || '-'}` : `Life Phase: ${life_phase?.label || '-'}`}</span>
            <span>
              {(Number.isFinite(Number(years_into_phase)) ? years_into_phase : 0)}y in /{' '}
              {(Number.isFinite(Number(years_remaining_in_phase)) ? years_remaining_in_phase : 0)}y left
            </span>
          </div>
          <div className="h-1.5 rounded-full bg-current/20 overflow-hidden">
            <div className="h-full rounded-full bg-current/60 transition-all" style={{ width: `${phaseProgress}%` }} />
          </div>
        </div>
      </div>

      <div className={`rounded-xl border p-4 opacity-80 ${getPlanetColor(next.planet)}`}>
        <div className="flex items-center gap-2 text-xs font-medium opacity-60 mb-1">
          <ChevronRight className="w-3 h-3" />
          {isHi ? 'अगला साला ग्रह' : 'Next Saala Grah'}
        </div>
        <div className="font-semibold">{isHi ? next.planet_hi : next.planet}</div>
        <p className="text-xs mt-1 opacity-70 leading-relaxed">{pickLang({ en: next.en_desc, hi: next.hi_desc }, isHi)}</p>
      </div>

      {past_periods && past_periods.length > 0 && (
        <div className="rounded-xl border border-border bg-card p-4">
          <div className="flex items-center gap-1.5 text-xs font-medium text-muted-foreground mb-3">
            <ChevronLeft className="w-3 h-3" />
            {isHi ? 'पिछले साला ग्रह' : 'Past Saala Graha'}
          </div>
          <div className="space-y-2">
            {past_periods.map((p) => {
              const c = getPlanetColor(p.planet);
              return (
                <div key={p.age} className={`flex items-center gap-3 rounded-lg border px-3 py-2 text-xs ${c} opacity-60`}>
                  <span className="font-semibold w-16 shrink-0">
                    {isHi ? `आयु ${Number.isFinite(Number(p.age)) ? p.age : 0}` : `Age ${Number.isFinite(Number(p.age)) ? p.age : 0}`}
                  </span>
                  <span className="font-medium">{isHi ? p.planet_hi : p.planet}</span>
                  <span className="opacity-70 line-clamp-1">{pickLang({ en: p.en_desc, hi: p.hi_desc }, isHi)}</span>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {upcoming_periods && upcoming_periods.length > 0 && (
        <div className="rounded-xl border border-border bg-card p-4">
          <div className="text-xs font-medium text-muted-foreground mb-3">
            {isHi ? 'आने वाले साला ग्रह (अगले 5 वर्ष)' : 'Upcoming Saala Graha (next 5 years)'}
          </div>
          <div className="space-y-2">
            {upcoming_periods.map((p, i) => {
              const c = getPlanetColor(p.planet);
              return (
                <div
                  key={p.age}
                  className={`flex items-center gap-3 rounded-lg border px-3 py-2.5 text-xs ${c}`}
                  style={{ opacity: Math.max(0.35, 1 - i * 0.12) }}
                >
                  <span className="font-semibold w-16 shrink-0">
                    {isHi ? `आयु ${Number.isFinite(Number(p.age)) ? p.age : 0}` : `Age ${Number.isFinite(Number(p.age)) ? p.age : 0}`}
                  </span>
                  <span className="font-medium">{isHi ? p.planet_hi : p.planet}</span>
                  <span className="opacity-70 leading-relaxed">{pickLang({ en: p.en_desc, hi: p.hi_desc }, isHi)}</span>
                </div>
              );
            })}
          </div>
        </div>
      )}

      <AstrologyTheorySection language={language} />
    </div>
  );
}

function AstrologyTheorySection({ language }: { language: string }) {
  const hi = language === 'hi';
  const l = (en: string, hiStr: string) => (hi ? hiStr : en);

  return (
    <div className="mt-12 space-y-6 pb-10">
      <div className="rounded-xl border border-sacred-gold/30 bg-sacred-gold/5 p-6 overflow-hidden">
        <Heading as={3} variant={3} className="text-sacred-gold-dark mb-4 flex items-center gap-2">
          <Clock className="w-5 h-5" />
          {l('Understanding Lal Kitab Dasha', 'लाल किताब दशा को समझना')}
        </Heading>

        <p className="text-sm text-foreground/80 mb-6 leading-relaxed">
          {l(
            'Unlike standard Vedic astrology, Lal Kitab uses a unique "Saala Grah" (Annual Planet) system. Your life is divided into specific cycles, and every single year a specific planet takes the lead as your "Yearly Ruler".',
            'सामान्य वैदिक ज्योतिष के विपरीत, लाल किताब एक अद्वितीय "साला ग्रह" (वार्षिक ग्रह) प्रणाली का उपयोग करती है। आपका जीवन विशिष्ट चक्रों में विभाजित है, और हर साल एक विशिष्ट ग्रह आपके "वार्षिक शासक" के रूप में नेतृत्व करता है।'
          )}
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="space-y-3">
            <h4 className="text-sm font-bold text-primary border-b border-sacred-gold/20 pb-1.5 uppercase tracking-wide">
              {l('The 35-Year Cycle', '35 वर्षीय चक्र')}
            </h4>
            <p className="text-xs text-foreground/70 leading-relaxed">
              {l(
                'Lal Kitab dasha follows a fixed sequence of planets. These cycles repeat and influence different phases of your maturity and destiny.',
                'लाल किताब दशा ग्रहों के एक निश्चित क्रम का पालन करती है। ये चक्र दोहराते हैं और आपकी परिपक्वता और भाग्य के विभिन्न चरणों को प्रभावित करते हैं।'
              )}
            </p>
          </div>
          <div className="space-y-3">
            <h4 className="text-sm font-bold text-primary border-b border-sacred-gold/20 pb-1.5 uppercase tracking-wide">
              {l('The Yearly Ruler (Saala Grah)', 'साला ग्रह (वार्षिक शासक)')}
            </h4>
            <p className="text-xs text-foreground/70 leading-relaxed">
              {l(
                'The planet ruling your current age acts as your guide for that year. Its position in your birth chart (Teva) determines the flavor of your experiences.',
                'आपकी वर्तमान आयु पर शासन करने वाला ग्रह उस वर्ष के लिए आपके मार्गदर्शक के रूप में कार्य करता है। आपकी जन्म कुंडली (तेवा) में इसकी स्थिति आपके अनुभवों के स्वभाव को निर्धारित करती है।'
              )}
            </p>
          </div>
        </div>

        <div className="mt-8 p-4 bg-sacred-gold-dark/[0.03] rounded-lg border border-sacred-gold/20 text-center">
          <p className="text-xs text-foreground/80 leading-relaxed italic">
            {l(
              'Interpretation Tip: In Lal Kitab, the dasha results are combined with the "Varshphal" (Yearly Chart) to give precise yearly predictions.',
              'व्याख्या टिप: लाल किताब में, सटीक वार्षिक भविष्यवाणियां देने के लिए दशा परिणामों को "वर्षफल" (वार्षिक चार्ट) के साथ जोड़ा जाता है।'
            )}
          </p>
        </div>
      </div>
    </div>
  );
}
