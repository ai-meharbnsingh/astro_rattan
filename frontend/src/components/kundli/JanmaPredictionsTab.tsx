import { useState, useEffect } from 'react';
import {
  Loader2, User, Moon, Compass, Sparkles, BookOpen,
  CheckCircle2, AlertTriangle, Briefcase, Flame,
} from 'lucide-react';
import { api } from '@/lib/api';
import { Heading } from '@/components/ui/heading';

interface LagnaProfile {
  lagna_sign: string;
  lagna_sign_hi: string;
  body_type_en: string;
  body_type_hi: string;
  temperament_en: string;
  temperament_hi: string;
  fortune_en: string;
  fortune_hi: string;
  lucky_directions_en: string[];
  lucky_directions_hi: string[];
  sloka_ref: string;
}

interface MoonNakshatra {
  nakshatra: string;
  pada: number;
  deity_en: string;
  deity_hi: string;
  symbol_en: string;
  symbol_hi: string;
  character_en: string;
  character_hi: string;
  strengths_en: string[];
  strengths_hi: string[];
  vulnerabilities_en: string[];
  vulnerabilities_hi: string[];
  career_affinity_en: string[];
  career_affinity_hi: string[];
  sloka_ref: string;
}

interface JanmaData {
  kundli_id?: string;
  person_name?: string;
  lagna_profile: LagnaProfile;
  moon_nakshatra: MoonNakshatra;
  combined_narrative_en: string;
  combined_narrative_hi: string;
  sloka_ref: string;
}

interface Props {
  kundliId: string;
  language: string;
  t: (key: string) => string;
}

const ohContainer = 'rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden';
const ohHeader    = 'bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center gap-2';

function PillGroup({ items, cls }: { items: string[]; cls: string }) {
  if (!items?.length) return null;
  return (
    <div className="flex flex-wrap gap-1.5">
      {items.map((item, i) => (
        <span key={i} className={`px-2.5 py-0.5 rounded-full text-xs font-medium ${cls}`}>{item}</span>
      ))}
    </div>
  );
}

export default function JanmaPredictionsTab({ kundliId, language, t }: Props) {
  const [data, setData] = useState<JanmaData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const isHi = language === 'hi';

  useEffect(() => {
    if (!kundliId) return;
    let cancelled = false;
    setLoading(true);
    setError('');
    (async () => {
      try {
        const res = await api.get<JanmaData>(`/api/kundli/${kundliId}/janma-predictions`);
        if (!cancelled) setData(res);
      } catch (err: any) {
        if (!cancelled) setError(err?.message || 'Failed to load Janma Predictions');
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => { cancelled = true; };
  }, [kundliId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-6 h-6 animate-spin text-primary" />
        <span className="ml-2 text-sm text-foreground">{isHi ? 'लोड हो रहा है...' : 'Loading...'}</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 rounded-lg bg-red-50 border border-red-200 text-red-700 text-sm">{error}</div>
    );
  }

  if (!data) return null;

  const lp = data.lagna_profile;
  const mn = data.moon_nakshatra;

  const lagnaName  = isHi ? (lp.lagna_sign_hi || lp.lagna_sign) : lp.lagna_sign;
  const bodyType   = isHi ? lp.body_type_hi   : lp.body_type_en;
  const temperament= isHi ? lp.temperament_hi : lp.temperament_en;
  const fortune    = isHi ? lp.fortune_hi     : lp.fortune_en;
  const luckyDirs  = isHi ? lp.lucky_directions_hi : lp.lucky_directions_en;

  const deity    = isHi ? mn.deity_hi    : mn.deity_en;
  const symbol   = isHi ? mn.symbol_hi   : mn.symbol_en;
  const character= isHi ? mn.character_hi: mn.character_en;
  const strengths= isHi ? mn.strengths_hi: mn.strengths_en;
  const vulns    = isHi ? mn.vulnerabilities_hi : mn.vulnerabilities_en;
  const careers  = isHi ? mn.career_affinity_hi : mn.career_affinity_en;

  return (
    <div className="space-y-6">

      {/* Header */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
          <Sparkles className="w-6 h-6" />
          {t('auto.janmaPredictions')}
        </Heading>
        <p className="text-sm text-muted-foreground">{t('auto.janmaPredictionsDesc')}</p>
      </div>

      {/* Lagna Profile */}
      <div className={ohContainer}>
        <div className={ohHeader}>
          <User className="w-4 h-4" />
          <span>{t('auto.lagnaProfile')}</span>
          {lagnaName && (
            <span className="ml-auto text-[12px] font-normal bg-white/20 px-2 py-0.5 rounded">{lagnaName}</span>
          )}
        </div>

        {!lp.lagna_sign ? (
          <div className="px-4 py-3 text-sm text-muted-foreground">{t('auto.lagnaNotAvailable')}</div>
        ) : (
          <div className="divide-y divide-border">
            {/* Body Type */}
            <div className="px-4 py-3 grid grid-cols-[140px_1fr] gap-3 items-start">
              <div className="flex items-center gap-1.5 text-xs font-semibold text-muted-foreground pt-0.5">
                <User className="w-3.5 h-3.5 shrink-0" />
                {t('auto.bodyType')}
              </div>
              <p className="text-sm text-foreground leading-relaxed">{bodyType}</p>
            </div>

            {/* Temperament */}
            <div className="px-4 py-3 grid grid-cols-[140px_1fr] gap-3 items-start">
              <div className="flex items-center gap-1.5 text-xs font-semibold text-muted-foreground pt-0.5">
                <Flame className="w-3.5 h-3.5 shrink-0" />
                {t('auto.temperament')}
              </div>
              <p className="text-sm text-foreground leading-relaxed">{temperament}</p>
            </div>

            {/* Fortune */}
            <div className="px-4 py-3 grid grid-cols-[140px_1fr] gap-3 items-start">
              <div className="flex items-center gap-1.5 text-xs font-semibold text-muted-foreground pt-0.5">
                <Sparkles className="w-3.5 h-3.5 shrink-0" />
                {t('auto.fortuneProfile')}
              </div>
              <p className="text-sm text-foreground leading-relaxed">{fortune}</p>
            </div>

            {/* Lucky Directions */}
            {luckyDirs?.length > 0 && (
              <div className="px-4 py-3 grid grid-cols-[140px_1fr] gap-3 items-start">
                <div className="flex items-center gap-1.5 text-xs font-semibold text-muted-foreground pt-0.5">
                  <Compass className="w-3.5 h-3.5 shrink-0" />
                  {t('auto.luckyDirections')}
                </div>
                <PillGroup items={luckyDirs} cls="bg-emerald-100 text-emerald-800 border border-emerald-200" />
              </div>
            )}
          </div>
        )}

        {lp.sloka_ref && (
          <div className="px-4 py-2 border-t border-border flex items-center gap-1.5 text-[11px] text-muted-foreground italic">
            <BookOpen className="w-3 h-3" />
            <span>{lp.sloka_ref}</span>
          </div>
        )}
      </div>

      {/* Moon Nakshatra */}
      <div className={ohContainer}>
        <div className={ohHeader}>
          <Moon className="w-4 h-4" />
          <span>{t('auto.moonNakshatra')}</span>
          {mn.nakshatra && (
            <span className="ml-auto text-[12px] font-normal bg-white/20 px-2 py-0.5 rounded">
              {mn.nakshatra} · {t('auto.pada')} {mn.pada}
            </span>
          )}
        </div>

        {!mn.nakshatra ? (
          <div className="px-4 py-3 text-sm text-muted-foreground">{t('auto.moonNakshatraNotAvailable')}</div>
        ) : (
          <div className="divide-y divide-border">

            {/* Deity + Symbol inline */}
            <div className="px-4 py-3 grid grid-cols-2 gap-4">
              <div>
                <p className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wide mb-0.5">{t('auto.deity')}</p>
                <p className="text-sm font-semibold text-foreground">{deity}</p>
              </div>
              <div>
                <p className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wide mb-0.5">{t('auto.symbol')}</p>
                <p className="text-sm font-semibold text-foreground">{symbol}</p>
              </div>
            </div>

            {/* Character */}
            <div className="px-4 py-3 grid grid-cols-[140px_1fr] gap-3 items-start">
              <div className="flex items-center gap-1.5 text-xs font-semibold text-muted-foreground pt-0.5">
                <Moon className="w-3.5 h-3.5 shrink-0" />
                {t('auto.characterProfile')}
              </div>
              <p className="text-sm text-foreground leading-relaxed">{character}</p>
            </div>

            {/* Strengths */}
            {strengths?.length > 0 && (
              <div className="px-4 py-3 grid grid-cols-[140px_1fr] gap-3 items-start">
                <div className="flex items-center gap-1.5 text-xs font-semibold text-emerald-700 pt-0.5">
                  <CheckCircle2 className="w-3.5 h-3.5 shrink-0" />
                  {t('auto.strengthsList')}
                </div>
                <PillGroup items={strengths} cls="bg-emerald-100 text-emerald-800 border border-emerald-200" />
              </div>
            )}

            {/* Vulnerabilities */}
            {vulns?.length > 0 && (
              <div className="px-4 py-3 grid grid-cols-[140px_1fr] gap-3 items-start">
                <div className="flex items-center gap-1.5 text-xs font-semibold text-amber-700 pt-0.5">
                  <AlertTriangle className="w-3.5 h-3.5 shrink-0" />
                  {t('auto.vulnerabilitiesList')}
                </div>
                <PillGroup items={vulns} cls="bg-amber-100 text-amber-800 border border-amber-200" />
              </div>
            )}

            {/* Career Affinity */}
            {careers?.length > 0 && (
              <div className="px-4 py-3 grid grid-cols-[140px_1fr] gap-3 items-start">
                <div className="flex items-center gap-1.5 text-xs font-semibold text-blue-700 pt-0.5">
                  <Briefcase className="w-3.5 h-3.5 shrink-0" />
                  {t('auto.careerAffinity')}
                </div>
                <PillGroup items={careers} cls="bg-blue-100 text-blue-800 border border-blue-200" />
              </div>
            )}
          </div>
        )}

        {mn.sloka_ref && (
          <div className="px-4 py-2 border-t border-border flex items-center gap-1.5 text-[11px] text-muted-foreground italic">
            <BookOpen className="w-3 h-3" />
            <span>{mn.sloka_ref}</span>
          </div>
        )}
      </div>

      {/* Combined Narrative */}
      {(data.combined_narrative_en || data.combined_narrative_hi) && (
        <div className={ohContainer}>
          <div className={ohHeader}>
            <Sparkles className="w-4 h-4" />
            <span>{t('auto.combinedJanmaNarrative')}</span>
          </div>
          <div className="px-4 py-3">
            <p className="text-sm text-foreground leading-relaxed">
              {isHi ? data.combined_narrative_hi : data.combined_narrative_en}
            </p>
          </div>
        </div>
      )}

      {/* Footer */}
      <div className="flex items-center gap-1.5 text-[11px] text-muted-foreground italic pt-2 border-t border-border">
        <BookOpen className="w-3 h-3" />
        <span>{data.sloka_ref}</span>
      </div>
    </div>
  );
}
