import { useMemo, type ReactNode } from 'react';
import { X, ChevronRight, MapPin, Calendar, Clock, User } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useTranslation } from '@/lib/i18n';
import { translateBackend, translatePlanet, translateSign, translateLabel } from '@/lib/backend-translations';

interface KundliData {
  name: string;
  date: string;
  time: string;
  place: string;
  latitude: string;
  longitude: string;
  timezone: string;
}

interface KundliSummaryModalProps {
  isOpen: boolean;
  onClose: () => void;
  data: KundliData;
  onViewFullReport: () => void;
  result?: {
    person_name?: string;
    birth_date?: string;
    birth_time?: string;
    birth_place?: string;
    chart_data?: { planets?: Record<string, PlanetRow | undefined> | PlanetRow[] };
  };
  dashaData?: { periods?: DashaRow[]; mahadasha?: DashaRow[] };
  yogaDoshaData?: { yogas?: YogaRow[]; doshas?: DoshaRow[] };
  doshaData?: {
    mangal_dosha?: { has_dosha?: boolean; severity?: string };
    kaal_sarp_dosha?: { has_dosha?: boolean; severity?: string };
    sade_sati?: { has_sade_sati?: boolean; severity?: string };
  };
  avakhadaData?: { gana?: string; yoni?: string; nadi?: string; varna?: string };
}

interface PlanetRow {
  planet: string;
  sign: string;
  house?: number;
}

interface DashaRow {
  planet?: string;
  name?: string;
  mahadasha?: string;
  start_date?: string;
  startDate?: string;
  end_date?: string;
  endDate?: string;
  years?: number;
  duration_years?: number;
}

interface YogaRow {
  present?: boolean;
  name?: string;
  yoga?: string;
  strength?: string;
  description?: string;
  effect?: string;
}

interface DoshaRow {
  present?: boolean;
  name?: string;
  dosha?: string;
  severity?: string;
  description?: string;
  effect?: string;
}

export default function KundliSummaryModal({
  isOpen,
  onClose,
  data,
  onViewFullReport,
  result,
  dashaData,
  yogaDoshaData,
  doshaData,
  avakhadaData,
}: KundliSummaryModalProps) {
  const { t, language } = useTranslation();

  const planets = useMemo(() => {
    const raw = result?.chart_data?.planets || {};
    const arr: PlanetRow[] = Array.isArray(raw)
      ? raw
      : Object.entries(raw).map(([planet, p]) => ({ planet, ...(p || {}) as Partial<PlanetRow> }));
    return arr
      .filter((p) => Boolean(p?.planet && p?.sign))
      .slice(0, 12);
  }, [result]);

  const dashaPeriods = useMemo(() => {
    if (Array.isArray(dashaData?.periods)) return dashaData.periods.slice(0, 3);
    if (Array.isArray(dashaData?.mahadasha)) return dashaData.mahadasha.slice(0, 3);
    return [];
  }, [dashaData]);

  const presentYogas = useMemo(
    () => (Array.isArray(yogaDoshaData?.yogas) ? yogaDoshaData.yogas.filter((y) => y?.present).slice(0, 4) : []),
    [yogaDoshaData],
  );

  const presentDoshas = useMemo(() => {
    if (Array.isArray(yogaDoshaData?.doshas)) {
      return yogaDoshaData.doshas.filter((d) => d?.present).slice(0, 4);
    }
    const fallback: DoshaRow[] = [];
    if (doshaData?.mangal_dosha?.has_dosha) fallback.push({ name: 'Mangal Dosha', severity: doshaData.mangal_dosha.severity });
    if (doshaData?.kaal_sarp_dosha?.has_dosha) fallback.push({ name: 'Kaal Sarp Dosha', severity: doshaData.kaal_sarp_dosha.severity });
    if (doshaData?.sade_sati?.has_sade_sati) fallback.push({ name: 'Sade Sati', severity: doshaData.sade_sati.severity });
    return fallback;
  }, [doshaData, yogaDoshaData]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-2 sm:p-4 bg-black/70">
      <div className="relative w-full max-w-5xl bg-[var(--dark-bg)] rounded-xl border border-[var(--sacred-gold-hex)] shadow-2xl overflow-hidden">
        <div className="sticky top-0 z-10 bg-gradient-to-r from-[var(--dark-bg)] via-[#111] to-[var(--dark-bg)] border-b border-[var(--sacred-gold-hex)] p-4 flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold text-white">{t('section.vedicBirthChart')}</h2>
            <p className="text-sm text-[#d4af37]">{t('kundli.summary.title')}</p>
          </div>
          <div className="flex items-center gap-2">
            <Button onClick={onViewFullReport} className="flex items-center gap-2 bg-[var(--sacred-gold-hex)] text-black hover:bg-[var(--sacred-gold)]">
              {t('kundli.fullReport')}
              <ChevronRight className="w-4 h-4" />
            </Button>
            <button onClick={onClose} className="ml-1 w-9 h-9 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center text-white">
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        <div className="p-4 max-h-[80vh] overflow-y-auto space-y-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 p-3 bg-[#111] rounded-xl border border-[var(--sacred-gold-hex)]">
            <InfoCell icon={<User className="w-4 h-4 text-[#d4af37]" />} label={t('auth.fullName')} value={result?.person_name || data.name} />
            <InfoCell icon={<Calendar className="w-4 h-4 text-[#d4af37]" />} label={t('kundli.birthDate')} value={result?.birth_date || data.date} />
            <InfoCell icon={<Clock className="w-4 h-4 text-[#d4af37]" />} label={t('kundli.birthTime')} value={result?.birth_time || data.time} />
            <InfoCell icon={<MapPin className="w-4 h-4 text-[#d4af37]" />} label={t('kundli.birthPlace')} value={result?.birth_place || data.place} />
          </div>

          <div className="grid lg:grid-cols-2 gap-4">
            <div className="bg-[#111] rounded-xl border border-[var(--sacred-gold-hex)] p-3">
              <h3 className="text-sm font-semibold text-[#d4af37] mb-2">{t('section.detailedPlanetPositions')}</h3>
              {planets.length === 0 ? (
                <p className="text-sm text-white/70">{language === 'hi' ? 'ग्रह स्थिति उपलब्ध नहीं' : 'Planet positions unavailable'}</p>
              ) : (
                <div className="space-y-1 max-h-64 overflow-y-auto">
                  {planets.map((planet, idx) => (
                    <div key={`${planet.planet}-${idx}`} className="flex items-center justify-between p-2 rounded bg-black text-sm">
                      <span className="text-white font-medium">{translatePlanet(planet.planet, language)}</span>
                      <span className="text-[#d4af37]">
                        {translateSign(planet.sign, language)} {planet.house ? `• H${planet.house}` : ''}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div className="bg-[#111] rounded-xl border border-[var(--sacred-gold-hex)] p-3">
              <h3 className="text-sm font-semibold text-[#d4af37] mb-2">{t('section.vimshottariDasha')}</h3>
              {dashaPeriods.length === 0 ? (
                <p className="text-sm text-white/70">{language === 'hi' ? 'दशा डेटा उपलब्ध नहीं' : 'Dasha data unavailable'}</p>
              ) : (
                <div className="space-y-2">
                  {dashaPeriods.map((period, idx) => {
                    const planet = period.planet || period.name || period.mahadasha || '';
                    const start = period.start_date || period.startDate || '';
                    const end = period.end_date || period.endDate || '';
                    const years = period.years ?? period.duration_years ?? '';
                    return (
                      <div key={`${planet}-${idx}`} className={`p-2 rounded text-sm ${idx === 0 ? 'bg-[var(--sacred-gold-hex)]/20 border border-[var(--sacred-gold-hex)]' : 'bg-black'}`}>
                        <div className="flex items-center justify-between mb-1">
                          <span className="font-semibold text-white">{translatePlanet(planet, language)} {t('kundli.mahadasha')}</span>
                          <span className="text-[#d4af37]">{years ? `${years} ${t('table.years')}` : ''}</span>
                        </div>
                        <p className="text-white/85">{start} {start && end ? ' - ' : ''}{end}</p>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
            <QuickStat label={t('avakhada.gana')} value={translateBackend(avakhadaData?.gana || '-', language)} />
            <QuickStat label={t('avakhada.yoni')} value={translateBackend(avakhadaData?.yoni || '-', language)} />
            <QuickStat label={t('avakhada.nadi')} value={translateBackend(avakhadaData?.nadi || '-', language)} />
            <QuickStat label={t('avakhada.varna')} value={translateBackend(avakhadaData?.varna || '-', language)} />
          </div>

          {presentYogas.length > 0 && (
            <div className="bg-[#111] rounded-xl border border-green-300 p-3">
              <h3 className="text-sm font-semibold text-green-400 mb-2">{t('kundli.summary.presentYogas')} ({presentYogas.length})</h3>
              <div className="space-y-2">
                {presentYogas.map((yoga, idx) => (
                  <div key={`${yoga.name || yoga.yoga || 'y'}-${idx}`} className="p-2 rounded bg-green-500/10 border border-green-300/30 text-sm">
                    <div className="flex items-center justify-between mb-1">
                      <span className="font-semibold text-white">{translateBackend(yoga.name || yoga.yoga || '', language)}</span>
                      <span className="text-xs px-2 py-0.5 rounded-full bg-green-100 text-green-800">{translateLabel(yoga.strength || 'Strong', language)}</span>
                    </div>
                    <p className="text-green-300">{translateBackend(yoga.description || yoga.effect || '', language)}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {presentDoshas.length > 0 && (
            <div className="bg-[#111] rounded-xl border border-red-300 p-3">
              <h3 className="text-sm font-semibold text-red-400 mb-2">{t('kundli.summary.presentDoshas')} ({presentDoshas.length})</h3>
              <div className="space-y-2">
                {presentDoshas.map((dosha, idx) => (
                  <div key={`${dosha.name || dosha.dosha || 'd'}-${idx}`} className="p-2 rounded bg-red-500/10 border border-red-300/30 text-sm">
                    <div className="flex items-center justify-between mb-1">
                      <span className="font-semibold text-white">{translateBackend(dosha.name || dosha.dosha || '', language)}</span>
                      <span className="text-xs px-2 py-0.5 rounded-full bg-red-100 text-red-800">{translateLabel(dosha.severity || 'high', language)}</span>
                    </div>
                    <p className="text-red-300">{translateBackend(dosha.description || dosha.effect || '', language)}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function InfoCell({ icon, label, value }: { icon: ReactNode; label: string; value: string }) {
  return (
    <div className="flex items-center gap-2">
      {icon}
      <div>
        <p className="text-xs text-white/70">{label}</p>
        <p className="text-sm font-medium text-white">{value || '-'}</p>
      </div>
    </div>
  );
}

function QuickStat({ label, value }: { label: string; value: string }) {
  return (
    <div className="bg-[#111] rounded-lg border border-[var(--sacred-gold-hex)] p-2 text-center">
      <p className="text-xs text-white/70">{label}</p>
      <p className="text-sm font-semibold text-white">{value}</p>
    </div>
  );
}
