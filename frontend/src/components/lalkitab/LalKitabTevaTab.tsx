import { useMemo } from 'react';
import { useTranslation } from '@/lib/i18n';
import type { LalKitabChartData } from './lalkitab-data';
import { EyeOff, Star, Baby, Info } from 'lucide-react';
import InteractiveKundli, { type PlanetData, type ChartData } from '@/components/InteractiveKundli';

interface Props {
  chartData: LalKitabChartData;
  apiResult?: any;
}

type TevaType = 'ratandh' | 'dharmi' | 'nabalik' | 'normal';

const PLANET_HI: Record<string, string> = {
  Sun: 'सूर्य', Moon: 'चंद्र', Mars: 'मंगल', Mercury: 'बुध',
  Jupiter: 'गुरु', Venus: 'शुक्र', Saturn: 'शनि', Rahu: 'राहु', Ketu: 'केतु',
};

const ZODIAC_SIGNS = [
  'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
  'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces',
];

const TEVA_CONFIG: Record<TevaType, { color: string; bgColor: string; borderColor: string }> = {
  ratandh: { color: 'text-red-700',         bgColor: 'bg-red-500/8',         borderColor: 'border-red-300/40' },
  dharmi:  { color: 'text-green-700',        bgColor: 'bg-green-500/8',        borderColor: 'border-green-300/40' },
  nabalik: { color: 'text-orange-700',       bgColor: 'bg-orange-500/8',       borderColor: 'border-orange-300/40' },
  normal:  { color: 'text-sacred-gold-dark', bgColor: 'bg-sacred-gold/8',      borderColor: 'border-sacred-gold/30' },
};

/** Compute Lal Kitab Teva type from chart planet positions. */
function computeTevaType(positions: Record<string, number>): TevaType {
  const saturn = positions['Saturn'] ?? 0;
  const rahu   = positions['Rahu']   ?? 0;
  const jupiter = positions['Jupiter'] ?? 0;
  const moon   = positions['Moon']   ?? 0;
  const mercury = positions['Mercury'] ?? 0;

  // Ratandh: Saturn or Rahu in H1, OR 3+ planets in H6/8/12
  const afflictionCount = Object.values(positions).filter((h) => h === 6 || h === 8 || h === 12).length;
  if (saturn === 1 || rahu === 1 || afflictionCount >= 3) return 'ratandh';

  // Dharmi: Jupiter in H1/4/5/9/12 (own signs: H9 Sagittarius, H12 Pisces; exalted: H4 Cancer)
  if (jupiter === 1 || jupiter === 4 || jupiter === 5 || jupiter === 9 || jupiter === 12) return 'dharmi';

  // Nabalik: Moon in H8/12 or Mercury in H12
  if (moon === 8 || moon === 12 || mercury === 12) return 'nabalik';

  return 'normal';
}

/** Blind planets: Rahu, Ketu always + any planet in H6/8/12 */
function getBlindPlanets(positions: Record<string, number>): string[] {
  const blind = new Set<string>(['Rahu', 'Ketu']);
  for (const [planet, house] of Object.entries(positions)) {
    if (house === 6 || house === 8 || house === 12) blind.add(planet);
  }
  return [...blind].filter((p) => positions[p] !== undefined || p === 'Rahu' || p === 'Ketu');
}

/** Righteous planets: Jupiter always + Moon in H4 + Venus in H2/H7 */
function getRighteousPlanets(positions: Record<string, number>): string[] {
  const righteous: string[] = ['Jupiter'];
  if (positions['Moon'] === 4) righteous.push('Moon');
  if (positions['Venus'] === 2 || positions['Venus'] === 7) righteous.push('Venus');
  return righteous;
}

/** Underage planets: Moon in H8/H12 + Mercury in H12 */
function getUnderagePlanets(positions: Record<string, number>): string[] {
  const underage: string[] = [];
  if (positions['Moon'] === 8 || positions['Moon'] === 12) underage.push('Moon');
  if (positions['Mercury'] === 12) underage.push('Mercury');
  return underage;
}

interface PlanetChipProps {
  planet: string;
  house: number;
  isHi: boolean;
  colorClass: string;
}

function PlanetChip({ planet, house, isHi, colorClass }: PlanetChipProps) {
  const name = isHi ? (PLANET_HI[planet] ?? planet) : planet;
  return (
    <span className={`inline-flex items-center gap-1 px-3 py-1 rounded-full text-sm font-medium border ${colorClass}`}>
      {name}
      {house > 0 && (
        <span className="text-xs opacity-70">H{house}</span>
      )}
    </span>
  );
}

export default function LalKitabTevaTab({ chartData, apiResult }: Props) {
  const { t, language } = useTranslation();
  const isHi = language === 'hi';
  const positions = chartData.planetPositions;

  const tevaType = computeTevaType(positions);
  const blindPlanets = getBlindPlanets(positions);
  const righteousPlanets = getRighteousPlanets(positions);
  const underagePlanets = getUnderagePlanets(positions);

  const cfg = TEVA_CONFIG[tevaType];

  const tevaLabel = t(`lk.teva.${tevaType}`);

  const interactiveChartData: ChartData | null = useMemo(() => {
    const planetsRaw = apiResult?.chart_data?.planets;
    if (!planetsRaw) return null;

    const planets: PlanetData[] = Array.isArray(planetsRaw)
      ? planetsRaw.map((p: any) => ({
          planet: p.planet,
          sign: p.sign || 'Unknown',
          house: p.house || 0,
          nakshatra: p.nakshatra || '',
          sign_degree: p.sign_degree || 0,
          status: p.status || '',
          is_retrograde: p.is_retrograde || false,
          is_combust: p.is_combust || false,
          is_vargottama: p.is_vargottama || false,
        }))
      : Object.entries(planetsRaw).map(([name, data]: [string, any]) => ({
          planet: name,
          sign: data?.sign || 'Unknown',
          house: data?.house || 0,
          nakshatra: data?.nakshatra || '',
          sign_degree: data?.sign_degree || 0,
          status: data?.status || '',
          is_retrograde: data?.is_retrograde || false,
          is_combust: data?.is_combust || false,
          is_vargottama: data?.is_vargottama || false,
        }));

    const asc = apiResult.chart_data?.ascendant;
    const ascSign = asc?.sign || 'Aries';
    const ascIdx = ZODIAC_SIGNS.indexOf(ascSign);
    const houses = Array.from({ length: 12 }, (_, i) => ({
      number: i + 1,
      sign: ZODIAC_SIGNS[(ascIdx + i) % 12],
    }));

    return {
      planets,
      houses,
      ascendant: asc ? { longitude: asc.longitude || 0, sign: ascSign, sign_degree: asc.sign_degree } : undefined,
    };
  }, [apiResult]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-xl font-sans font-semibold text-sacred-gold flex items-center gap-2 mb-1">
          <Info className="w-5 h-5" />
          {t('lk.teva.title')}
        </h2>
        <p className="text-sm text-gray-500">{t('lk.teva.desc')}</p>
      </div>

      {/* Teva type card */}
      <div className={`rounded-xl border p-6 ${cfg.bgColor} ${cfg.borderColor}`}>
        <p className="text-xs font-semibold uppercase tracking-wider text-gray-500 mb-2">
          {t('lk.teva.type')}
        </p>
        <h3 className={`text-2xl font-sans font-bold mb-3 ${cfg.color}`}>{tevaLabel}</h3>

        <p className="text-sm text-cosmic-text/80 leading-relaxed">
          {tevaType === 'ratandh' && (
            isHi
              ? 'शनि या राहु लग्न में हैं या ३+ ग्रह ६/८/१२ भाव में हैं। यह कुंडली रतांध (अंध) तेवा की है।'
              : 'Saturn or Rahu is in H1, or 3+ planets are in H6/8/12. This chart has a Ratandh (blind) teva.'
          )}
          {tevaType === 'dharmi' && (
            isHi
              ? 'गुरु अपने उच्च/स्वगृह/शुभ भाव में है। यह कुंडली धर्मी तेवा की है — शुभ फल देने वाली।'
              : 'Jupiter is in its own sign, exalted, or a favourable house. This chart has a Dharmi (righteous) teva — giving good results.'
          )}
          {tevaType === 'nabalik' && (
            isHi
              ? 'चंद्र ८/१२ भाव में है या बुध १२वें भाव में है। यह कुंडली नाबालिग तेवा की है।'
              : 'Moon is in H8/12 or Mercury is in H12. This chart has a Nabalik (underage) teva.'
          )}
          {tevaType === 'normal' && (
            isHi
              ? 'ग्रहों की सामान्य स्थिति — कोई विशेष रतांध, धर्मी या नाबालिग तेवा नहीं।'
              : 'Planets are in normal positions — no special Ratandh, Dharmi, or Nabalik teva.'
          )}
        </p>
      </div>

      {/* Three planet classification cards */}
      <div className="grid gap-4 md:grid-cols-3">
        {/* Blind planets */}
        <div className="card-sacred rounded-xl border border-red-300/30 p-5 bg-red-500/5">
          <div className="flex items-center gap-2 mb-3">
            <EyeOff className="w-4 h-4 text-red-600" />
            <h3 className="font-sans font-semibold text-red-700 text-sm">
              {t('lk.teva.blind')}
            </h3>
          </div>
          <p className="text-xs text-gray-500 mb-3">{t('lk.teva.blindDesc')}</p>
          <div className="flex flex-wrap gap-2">
            {blindPlanets.map((p) => (
              <PlanetChip
                key={p}
                planet={p}
                house={positions[p] ?? 0}
                isHi={isHi}
                colorClass="bg-red-500/10 text-red-700 border-red-300/40"
              />
            ))}
            {blindPlanets.length === 0 && (
              <span className="text-xs text-gray-400">{isHi ? 'कोई नहीं' : 'None'}</span>
            )}
          </div>
        </div>

        {/* Righteous planets */}
        <div className="card-sacred rounded-xl border border-green-300/30 p-5 bg-green-500/5">
          <div className="flex items-center gap-2 mb-3">
            <Star className="w-4 h-4 text-green-600" />
            <h3 className="font-sans font-semibold text-green-700 text-sm">
              {t('lk.teva.righteous')}
            </h3>
          </div>
          <p className="text-xs text-gray-500 mb-3">{t('lk.teva.righteousDesc')}</p>
          <div className="flex flex-wrap gap-2">
            {righteousPlanets.map((p) => (
              <PlanetChip
                key={p}
                planet={p}
                house={positions[p] ?? 0}
                isHi={isHi}
                colorClass="bg-green-500/10 text-green-700 border-green-300/40"
              />
            ))}
          </div>
        </div>

        {/* Underage planets */}
        <div className="card-sacred rounded-xl border border-orange-300/30 p-5 bg-orange-500/5">
          <div className="flex items-center gap-2 mb-3">
            <Baby className="w-4 h-4 text-orange-600" />
            <h3 className="font-sans font-semibold text-orange-700 text-sm">
              {t('lk.teva.underage')}
            </h3>
          </div>
          <p className="text-xs text-gray-500 mb-3">{t('lk.teva.underageDesc')}</p>
          <div className="flex flex-wrap gap-2">
            {underagePlanets.map((p) => (
              <PlanetChip
                key={p}
                planet={p}
                house={positions[p] ?? 0}
                isHi={isHi}
                colorClass="bg-orange-500/10 text-orange-700 border-orange-300/40"
              />
            ))}
            {underagePlanets.length === 0 && (
              <span className="text-xs text-gray-400">{isHi ? 'कोई नहीं' : 'None'}</span>
            )}
          </div>
        </div>
      </div>

      {/* Kundli chart */}
      {interactiveChartData ? (
        <div className="card-sacred rounded-xl border border-sacred-gold/20 p-5">
          <h3 className="font-sans font-semibold text-sacred-gold mb-3 text-sm">
            {isHi ? 'लाल किताब कुंडली (तेवा चार्ट)' : 'Lal Kitab Kundli (Teva Chart)'}
          </h3>
          <div className="flex justify-center">
            <div className="w-64 h-64">
              <InteractiveKundli chartData={interactiveChartData} compact />
            </div>
          </div>
        </div>
      ) : (
        <div className="card-sacred rounded-xl border border-sacred-gold/20 p-5">
          <h3 className="font-sans font-semibold text-sacred-gold mb-4 text-sm">
            {isHi ? 'ग्रह स्थान (लाल किताब भाव)' : 'Planet Positions (Lal Kitab Houses)'}
          </h3>
          <div className="grid grid-cols-3 sm:grid-cols-5 gap-2">
            {Object.entries(positions).map(([planet, house]) => (
              <div key={planet} className="flex flex-col items-center p-2 rounded-lg bg-sacred-gold/5 border border-sacred-gold/10">
                <span className="text-xs font-semibold text-sacred-gold-dark">
                  {isHi ? (PLANET_HI[planet] ?? planet) : planet}
                </span>
                <span className="text-lg font-bold text-cosmic-text">{house}</span>
                <span className="text-xs text-gray-400">{isHi ? 'भाव' : 'H'}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
