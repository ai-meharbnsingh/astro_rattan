import { useTranslation } from '@/lib/i18n';
import React, { useState, useCallback, useEffect } from 'react';
import { Loader2, ChevronDown, ChevronRight, Clock3 } from 'lucide-react';
import { api } from '@/lib/api';
import { translatePlanet, translateName, translateSign } from '@/lib/backend-translations';
import { PLANET_NATURE } from '@/components/kundli/kundli-utils';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { Heading } from '@/components/ui/heading';

/* ------------------------------------------------------------------ */
/*  Types                                                              */
/* ------------------------------------------------------------------ */

interface DashaPeriod {
  planet: string;
  yogini?: string;
  sign?: string;
  tara?: string;
  start: string;
  end: string;
  years?: number;
  duration_years?: number;
  span?: number;
  is_current?: boolean;
  antardasha?: DashaPeriod[];
  pratyantar?: DashaPeriod[];
  sub_periods?: DashaPeriod[];
  lord?: string;
  nakshatras?: string[];
}

interface DashaResponse {
  system: string;
  current_dasha?: string;
  current_antardasha?: string;
  current_pratyantar?: string;
  current_sub_period?: string;
  mahadasha?: DashaPeriod[];
  periods?: DashaPeriod[];
  dashas?: DashaPeriod[];
}

interface DashaSelectorProps {
  kundliId: string;
  language: string;
  t: (key: string) => string;
}

/* ------------------------------------------------------------------ */
/*  Dasha systems config                                               */
/* ------------------------------------------------------------------ */

type DashaSystem = 'vimshottari' | 'yogini' | 'ashtottari' | 'moola' | 'tara';

interface DashaSystemMeta {
  key: DashaSystem;
  labelEn: string;
  labelHi: string;
  endpoint: string;
  method?: 'GET' | 'POST';
}

const DASHA_SYSTEMS: DashaSystemMeta[] = [
  // Use extended endpoint so rows can expand MD → AD → PT in the UI.
  { key: 'vimshottari', labelEn: 'Vimshottari (120yr)', labelHi: 'विंशोत्तरी (120 वर्ष)', endpoint: '/api/kundli/{id}/extended-dasha', method: 'POST' },
  { key: 'yogini', labelEn: 'Yogini (36yr)', labelHi: 'योगिनी (36 वर्ष)', endpoint: '/api/kundli/{id}/yogini-dasha' },
  { key: 'ashtottari', labelEn: 'Ashtottari (108yr)', labelHi: 'अष्टोत्तरी (108 वर्ष)', endpoint: '/api/kundli/{id}/ashtottari-dasha' },
  { key: 'moola', labelEn: 'Moola', labelHi: 'मूल', endpoint: '/api/kundli/{id}/moola-dasha' },
  { key: 'tara', labelEn: 'Tara', labelHi: 'तारा', endpoint: '/api/kundli/{id}/tara-dasha' },
];

/* ------------------------------------------------------------------ */
/*  Helper: nature-based color                                         */
/* ------------------------------------------------------------------ */

function periodColor(planet: string): string {
  const nature = PLANET_NATURE[planet];
  if (!nature) return 'text-foreground';
  if (nature === 'Benefic') return 'text-green-600';
  if (nature === 'Malefic') return 'text-red-600';
  return 'text-amber-600';
}

function periodBg(planet: string, isCurrent: boolean): string {
  if (!isCurrent) return '';
  const nature = PLANET_NATURE[planet];
  if (!nature) return 'bg-muted/10';
  if (nature === 'Benefic') return 'bg-green-50';
  if (nature === 'Malefic') return 'bg-red-50';
  return 'bg-amber-50';
}

function natureBadge(planet: string, hi: boolean): React.ReactNode {
  const nature = PLANET_NATURE[planet];
  if (!nature) return null;
  const label = hi
    ? (nature === 'Benefic' ? 'शुभ' : nature === 'Malefic' ? 'पाप' : 'मिश्रित')
    : nature;
  const cls = nature === 'Benefic'
    ? 'bg-green-100 text-green-700 border-green-200'
    : nature === 'Malefic'
      ? 'bg-red-100 text-red-700 border-red-200'
      : 'bg-amber-100 text-amber-700 border-amber-200';
  return (
    <span className={`ml-2 px-1.5 py-0.5 rounded-full text-[9px] font-bold uppercase border ${cls}`}>
      {label}
    </span>
  );
}

function cloneResponse<T>(value: T): T {
  // Defensive copy: ensures each dasha system keeps an isolated snapshot
  // even if a downstream consumer mutates the response object/arrays.
  if (typeof structuredClone === 'function') return structuredClone(value);
  return JSON.parse(JSON.stringify(value)) as T;
}

const EMPTY_DATA: Record<DashaSystem, DashaResponse | null> = {
  vimshottari: null,
  yogini: null,
  ashtottari: null,
  moola: null,
  tara: null,
};

const SIGN_LORD: Record<string, string> = {
  Aries: 'Mars',
  Taurus: 'Venus',
  Gemini: 'Mercury',
  Cancer: 'Moon',
  Leo: 'Sun',
  Virgo: 'Mercury',
  Libra: 'Venus',
  Scorpio: 'Mars',
  Sagittarius: 'Jupiter',
  Capricorn: 'Saturn',
  Aquarius: 'Saturn',
  Pisces: 'Jupiter',
};

function naturePlanetFor(system: DashaSystem, period?: DashaPeriod | null): string {
  if (!period) return '';
  if (system === 'yogini') return String(period.lord ?? '');
  if (system === 'tara') return String(period.lord ?? '');
  if (system === 'moola') return SIGN_LORD[String(period.sign ?? period.planet ?? '')] || '';
  // vimshottari / ashtottari
  return String(period.planet ?? '');
}

function normalizeResponse(system: DashaSystem, raw: any): DashaResponse {
  const src = (raw && typeof raw === 'object') ? raw : {};

  if (system === 'yogini') {
    const periods = (src.periods || src.dashas || []) as any[];
    const mahadasha = periods.map((p: any) => ({
      // Prefer `yogini` (dasha name). If backend only provides `planet`, treat it as the dasha name.
      planet: String(p?.yogini ?? p?.planet ?? ''),
      // If backend provides both `yogini` and `planet`, treat `planet` as the ruling graha.
      lord: p?.yogini ? String(p?.planet ?? '') : undefined,
      start: String(p?.start ?? ''),
      end: String(p?.end ?? ''),
      years: p?.years,
      duration_years: p?.duration_years,
      span: p?.span,
      is_current: !!p?.is_current,
    })) as DashaPeriod[];
    return {
      system,
      mahadasha,
      current_dasha: src.current_dasha,
      current_antardasha: src.current_antardasha,
      current_pratyantar: src.current_pratyantar,
      current_sub_period: src.current_sub_period,
    };
  }

  if (system === 'moola') {
    const md = (src.mahadasha || []) as any[];
    const mahadasha = md.map((m: any) => ({
      planet: String(m?.sign ?? ''),
      sign: m?.sign,
      start: String(m?.start ?? ''),
      end: String(m?.end ?? ''),
      years: m?.years,
      is_current: !!m?.is_current,
      antardasha: ((m?.sub_periods || []) as any[]).map((sp: any) => ({
        planet: String(sp?.sign ?? ''),
        sign: sp?.sign,
        start: String(sp?.start ?? ''),
        end: String(sp?.end ?? ''),
        years: sp?.years,
        is_current: !!sp?.is_current,
      })),
    })) as DashaPeriod[];
    return {
      system,
      mahadasha,
      current_dasha: src.current_dasha,
      current_antardasha: src.current_sub_period || src.current_antardasha,
      current_pratyantar: src.current_pratyantar,
      current_sub_period: src.current_sub_period,
    };
  }

  if (system === 'tara') {
    const md = (src.mahadasha || []) as any[];
    const mahadasha = md.map((m: any) => ({
      planet: String(m?.tara ?? ''),
      tara: m?.tara,
      lord: m?.lord,
      nakshatras: m?.nakshatras,
      start: String(m?.start ?? ''),
      end: String(m?.end ?? ''),
      years: m?.years,
      is_current: !!m?.is_current,
      antardasha: ((m?.sub_periods || []) as any[]).map((sp: any) => ({
        planet: String(sp?.tara ?? ''),
        tara: sp?.tara,
        lord: sp?.lord,
        start: String(sp?.start ?? ''),
        end: String(sp?.end ?? ''),
        years: sp?.years,
        is_current: !!sp?.is_current,
      })),
    })) as DashaPeriod[];
    return {
      system,
      mahadasha,
      current_dasha: src.current_dasha,
      current_antardasha: src.current_sub_period || src.current_antardasha,
      current_pratyantar: src.current_pratyantar,
      current_sub_period: src.current_sub_period,
    };
  }

  // vimshottari / ashtottari (already structured)
  return {
    ...(src as DashaResponse),
    system,
  };
}

function formatLabel(system: DashaSystem, rawLabel: string, language: string): string {
  if (!rawLabel) return '';
  if (system === 'yogini' || system === 'tara') return translateName(rawLabel, language as any) || rawLabel;
  if (system === 'moola') return translateSign(rawLabel, language as any) || rawLabel;
  return translatePlanet(rawLabel, language as any) || translateName(rawLabel, language as any) || rawLabel;
}

/* ------------------------------------------------------------------ */
/*  Component                                                          */
/* ------------------------------------------------------------------ */

export default function DashaSelector({
  kundliId,
  language,
  t,
}: DashaSelectorProps) {
  const l = (en: string, hi: string) => (language === 'hi' ? hi : en);
  const hi = language === 'hi';

  const [eduOpen, setEduOpen] = useState(true);
  const [selectedSystem, setSelectedSystem] = useState<DashaSystem>('vimshottari');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<Record<DashaSystem, DashaResponse | null>>(EMPTY_DATA);

  // Ensure loading/error are driven by the latest request (avoid race confusion)
  const latestReqRef = React.useRef(0);

  // Accordion state
  const [expandedMD, setExpandedMD] = useState<string | null>(null);
  const [expandedAD, setExpandedAD] = useState<string | null>(null);

  // Reset state when the kundli changes (e.g., regenerate / load saved)
  useEffect(() => {
    setSelectedSystem('vimshottari');
    setExpandedMD(null);
    setExpandedAD(null);
    setError(null);
    setLoading(false);
    setData(EMPTY_DATA);
    latestReqRef.current = 0;
  }, [kundliId]);

  /* Fetch on system change — stable callback (no data dependency) */
  const fetchDasha = useCallback(async (system: DashaSystem) => {
    if (!kundliId) return;
    const reqId = ++latestReqRef.current;
    setError(null);
    setLoading(true);
    try {
      const meta = DASHA_SYSTEMS.find((s) => s.key === system)!;
      const url = meta.endpoint.replace('{id}', kundliId);
      const res = meta.method === 'POST' ? await api.post(url, {}) : await api.get(url);
      const normalized = normalizeResponse(system, res);
      setData((prev) => ({ ...prev, [system]: cloneResponse(normalized) }));
    } catch (err: any) {
      // Only surface the error if this is still the latest request (prevents stale errors)
      if (reqId === latestReqRef.current) {
        setError(err?.message || t('auto.genericError'));
      }
    } finally {
      if (reqId === latestReqRef.current) {
        setLoading(false);
      }
    }
  }, [kundliId]);

  useEffect(() => {
    fetchDasha(selectedSystem);
  }, [selectedSystem, fetchDasha]);

  // Reset accordion when system changes
  useEffect(() => {
    setExpandedMD(null);
    setExpandedAD(null);
  }, [selectedSystem]);

  const currentData = data[selectedSystem];
  const periods: DashaPeriod[] = currentData?.mahadasha || currentData?.periods || currentData?.dashas || [];
  const showBlockingLoader = loading && !currentData;

  /* ---------------------------------------------------------------- */
  /*  Render                                                           */
  /* ---------------------------------------------------------------- */

  return (
    <div className="space-y-6">
      {/* Page heading */}
      <div>
        <Heading as={2} variant={2} className="text-sacred-gold-dark mb-1 flex items-center gap-2">
          <Clock3 className="w-6 h-6" />
          {hi ? 'दशा' : 'Dasha'}
        </Heading>
        <p className="text-sm text-muted-foreground">
          {hi
            ? 'यहाँ विभिन्न दशा-पद्धतियों के महादशा/अन्तरदशा की अवधि और वर्तमान चल रही अवधि दिखती है।'
            : 'View major and sub-periods across dasha systems and see what is currently running.'}
        </p>
      </div>

      {/* System selector */}
      <div className="flex flex-wrap items-center gap-3">
        <label className="text-sm font-medium text-foreground">
          {l('Dasha System', 'दशा पद्धति')}:
        </label>
        <select
          value={selectedSystem}
          onChange={(e) => setSelectedSystem(e.target.value as DashaSystem)}
          className="bg-muted border border-border rounded-lg px-3 py-2 text-foreground text-sm focus:border-primary focus:outline-none"
        >
          {DASHA_SYSTEMS.map((sys) => (
            <option key={sys.key} value={sys.key}>
              {hi ? sys.labelHi : sys.labelEn}
            </option>
          ))}
        </select>
        {loading && currentData && (
          <span className="inline-flex items-center gap-2 text-xs text-foreground/70">
            <Loader2 className="w-3.5 h-3.5 animate-spin text-primary" />
            {l('Refreshing…', 'अपडेट हो रहा है…')}
          </span>
        )}
      </div>

      {/* Loading */}
      {showBlockingLoader && (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="w-6 h-6 animate-spin text-primary" />
          <span className="ml-2 text-foreground">{l('Loading dasha...', 'दशा लोड हो रही है...')}</span>
        </div>
      )}

      {/* Error */}
      {error && !showBlockingLoader && (
        <div className="bg-red-50 border border-red-200 rounded-xl p-4 text-sm text-red-700">
          {error}
          <Button
            size="sm"
            variant="outline"
            className="ml-3"
            onClick={() => {
              setData((prev) => ({ ...prev, [selectedSystem]: null }));
              fetchDasha(selectedSystem);
            }}
          >
            {l('Retry', 'पुनः प्रयास')}
          </Button>
        </div>
      )}

      {/* Current period summary */}
      {currentData && (
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold flex items-center justify-between">
            <span>{l('Current Running Period', 'वर्तमान चल रही दशा')}</span>
            <span className="px-2 py-0.5 bg-white/20 text-white text-[10px] font-bold rounded animate-pulse">
              ● {l('LIVE', 'लाइव')}
            </span>
          </div>
          <div className="p-4">
          {(() => {
            const currentMD = periods.find((p) => p.is_current);
            const currentADList = currentMD?.antardasha?.find((a) => a.is_current);
            const currentPT = currentADList?.pratyantar?.find((p) => p.is_current);
            if (!currentMD && !currentData.current_dasha) return (
              <p className="text-sm text-foreground/70">{l('No current period identified', 'कोई वर्तमान दशा नहीं मिली')}</p>
            );
            const mdLabel = currentMD?.planet || currentData.current_dasha || '';
            const adLabel = currentADList?.planet || currentData.current_antardasha || currentData.current_sub_period || '';
            const ptLabel = currentPT?.planet || currentData.current_pratyantar || '';
            const mdNaturePlanet = naturePlanetFor(selectedSystem, currentMD);
            return (
              <div className="flex flex-wrap gap-3 text-sm">
                <div className="flex items-center gap-1">
                  <span className="text-foreground/70">{t('kundli.mahadasha')}:</span>
                  <span className={`font-bold ${periodColor(mdNaturePlanet || mdLabel)}`}>
                    {formatLabel(selectedSystem, mdLabel, language)}
                  </span>
                  {natureBadge(mdNaturePlanet, hi)}
                </div>
                {adLabel && (
                  <div className="flex items-center gap-1">
                    <span className="text-foreground/70">{t('kundli.antardasha')}:</span>
                    <span className={`font-bold ${periodColor(mdNaturePlanet || adLabel)}`}>
                      {formatLabel(selectedSystem, adLabel, language)}
                    </span>
                  </div>
                )}
                {ptLabel && (
                  <div className="flex items-center gap-1">
                    <span className="text-foreground/70">{t('kundli.pratyantar')}:</span>
                    <span className={`font-bold ${periodColor(mdNaturePlanet || ptLabel)}`}>
                      {formatLabel(selectedSystem, ptLabel, language)}
                    </span>
                  </div>
                )}
              </div>
            );
          })()}
          </div>
        </div>
      )}

      {/* Full timeline with expandable tree */}
      {periods.length > 0 && (
        <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
          <div className="bg-sacred-gold-dark text-white px-4 py-2 text-[15px] font-semibold">
            {l('Dasha Timeline', 'दशा समयरेखा')}
          </div>
          <div className="overflow-x-auto">
            <Table className="w-full text-xs">
              <TableHeader>
                <TableRow>
                  <TableHead className="w-8"></TableHead>
                  <TableHead className="text-left p-1.5 text-primary font-medium">
                    {selectedSystem === 'yogini'
                      ? l('Yogini', 'योगिनी')
                      : selectedSystem === 'moola'
                        ? l('Sign', 'राशि')
                        : selectedSystem === 'tara'
                          ? l('Tara', 'तारा')
                          : l('Dasha Lord', 'दशा स्वामी')}
                  </TableHead>
                  <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.start')}</TableHead>
                  <TableHead className="text-left p-1.5 text-primary font-medium">{t('table.end')}</TableHead>
                  <TableHead className="text-center p-1.5 text-primary font-medium">{t('table.years')}</TableHead>
                  <TableHead className="text-center p-1.5 text-primary font-medium">
                    {l('Nature', 'प्रकृति')}
                  </TableHead>
                </TableRow>
              </TableHeader>
              <TableBody className="divide-y divide-border/30">
                {periods.map((md) => {
                  const mdKey = `${md.planet}-${md.start}-${md.end}`;
                  const mdLabel = formatLabel(selectedSystem, md.planet, language);
                  const mdNaturePlanet = naturePlanetFor(selectedSystem, md);
                  const isMdExpanded = expandedMD === mdKey;
                  const hasChildren = selectedSystem === 'yogini' ? true : (md.antardasha || []).length > 0;
                  const mdYears = md.years ?? md.span ?? (md.duration_years ? parseFloat(String(md.duration_years)).toFixed(1) : '');

                  return (
                    <React.Fragment key={`${selectedSystem}-${mdKey}`}>
                      {/* Mahadasha row */}
                      <TableRow
                        className={`cursor-pointer transition-colors ${md.is_current ? `${periodBg(mdNaturePlanet || md.planet, true)} border-l-2 border-l-primary` : 'hover:bg-muted/5'}`}
                        onClick={() => hasChildren && setExpandedMD(isMdExpanded ? null : mdKey)}
                      >
                        <TableCell className="p-1.5 text-center">
                          {hasChildren ? (
                            isMdExpanded
                              ? <ChevronDown className="w-3.5 h-3.5 text-primary transition-transform" />
                              : <ChevronRight className="w-3.5 h-3.5 text-primary transition-transform" />
                          ) : <span className="w-3.5 h-3.5 inline-block" />}
                        </TableCell>
                        <TableCell className="p-1.5">
                          <span className={`font-bold ${md.is_current ? 'text-primary' : periodColor(mdNaturePlanet || md.planet)}`}>
                            {mdLabel}
                          </span>
                          {md.is_current && (
                            <span className="ml-2 text-[9px] px-1 rounded bg-primary text-white font-bold uppercase">
                              {t('common.current')}
                            </span>
                          )}
                        </TableCell>
                        <TableCell className="p-1.5 text-foreground font-medium">{md.start}</TableCell>
                        <TableCell className="p-1.5 text-foreground font-medium">{md.end}</TableCell>
                        <TableCell className="p-1.5 text-center text-primary font-bold">{mdYears}</TableCell>
                        <TableCell className="p-1.5 text-center">{natureBadge(mdNaturePlanet, hi)}</TableCell>
                      </TableRow>

                      {/* Yogini has no sub-periods in our current API — allow expand to show context */}
                      {selectedSystem === 'yogini' && isMdExpanded && (md.antardasha || []).length === 0 && (
                        <TableRow>
                          <TableCell colSpan={6} className="p-3 pl-10 text-xs text-foreground/70">
                            {l('No sub-periods available for Yogini in this table yet.', 'योगिनी दशा के उप-अवधि इस तालिका में अभी उपलब्ध नहीं हैं।')}
                          </TableCell>
                        </TableRow>
                      )}

                      {/* Antardasha rows */}
                      {isMdExpanded && (md.antardasha || []).map((ad) => {
                        const adKey = `${mdKey}-${ad.planet}-${ad.start}-${ad.end}`;
                        const adLabel = formatLabel(selectedSystem, ad.planet, language);
                        const adNaturePlanet = naturePlanetFor(selectedSystem, ad) || mdNaturePlanet;
                        const isAdExpanded = expandedAD === adKey;
                        const hasADChildren = (ad.pratyantar || []).length > 0;
                        const adYears = ad.years ?? ad.span ?? (ad.duration_years ? parseFloat(String(ad.duration_years)).toFixed(2) : '');

                        return (
                          <React.Fragment key={`${selectedSystem}-${adKey}`}>
                            <TableRow
                              className={`cursor-pointer transition-colors ${ad.is_current ? `${periodBg(adNaturePlanet || ad.planet, true)} border-l-2 border-l-primary` : 'hover:bg-muted/5'}`}
                              onClick={(e) => {
                                e.stopPropagation();
                                if (hasADChildren) setExpandedAD(isAdExpanded ? null : adKey);
                              }}
                            >
                              <TableCell className="p-1.5 text-center pl-4">
                                {hasADChildren ? (
                                  isAdExpanded
                                    ? <ChevronDown className="w-3 h-3 text-primary" />
                                    : <ChevronRight className="w-3 h-3 text-primary" />
                                ) : <span className="w-3 h-3 inline-block" />}
                              </TableCell>
                              <TableCell className="p-1.5 pl-6">
                                <span className={`font-semibold ${ad.is_current ? 'text-primary' : periodColor(adNaturePlanet || ad.planet)}`}>
                                  {adLabel}
                                </span>
                                {ad.is_current && (
                                  <span className="ml-2 text-[8px] px-1 rounded border border-border-dark text-primary font-bold uppercase">
                                    {t('common.current')}
                                  </span>
                                )}
                              </TableCell>
                              <TableCell className="p-1.5 text-foreground italic opacity-80">{ad.start}</TableCell>
                              <TableCell className="p-1.5 text-foreground italic opacity-80">{ad.end}</TableCell>
                              <TableCell className="p-1.5 text-center text-foreground opacity-60">{adYears}</TableCell>
                              <TableCell className="p-1.5 text-center">{natureBadge(adNaturePlanet, hi)}</TableCell>
                            </TableRow>

                            {/* Pratyantardasha rows */}
                            {isAdExpanded && (ad.pratyantar || []).map((pt, idx) => {
                              const ptLabel = formatLabel(selectedSystem, pt.planet, language);
                              const ptKey = `${selectedSystem}-${adKey}-${pt.planet}-${pt.start}-${pt.end}-${idx}`;
                              return (
                                <TableRow
                                  key={ptKey}
                                  className={`transition-colors ${pt.is_current ? periodBg(pt.planet, true) : 'hover:bg-muted/5'}`}
                                >
                                  <TableCell className="p-1"></TableCell>
                                  <TableCell className="p-1.5 pl-12 text-xs">
                                    <span className={`${pt.is_current ? 'text-primary font-bold' : periodColor(pt.planet)} opacity-80`}>
                                      {ptLabel}
                                    </span>
                                    {pt.is_current && <span className="ml-1 text-primary font-bold">{'\u25CF'}</span>}
                                  </TableCell>
                                  <TableCell className="p-1.5 text-xs text-foreground opacity-60">{pt.start}</TableCell>
                                  <TableCell className="p-1.5 text-xs text-foreground opacity-60">{pt.end}</TableCell>
                                  <TableCell className="p-1"></TableCell>
                                  <TableCell className="p-1"></TableCell>
                                </TableRow>
                              );
                            })}
                          </React.Fragment>
                        );
                      })}
                    </React.Fragment>
                  );
                })}
              </TableBody>
            </Table>
          </div>
        </div>
      )}

      {/* Empty state */}
      {!showBlockingLoader && !error && periods.length === 0 && !currentData && (
        <div className="flex flex-col items-center justify-center py-12">
          <p className="text-foreground mb-3 text-sm">
            {l('Select a dasha system to view planetary periods', 'ग्रहीय दशा देखने के लिए एक दशा पद्धति चुनें')}
          </p>
        </div>
      )}

      {/* Educational Summary (placed at the bottom, after tables) */}
      <div className="rounded-xl border border-sacred-gold/20 bg-transparent overflow-hidden">
        <button
          type="button"
          onClick={() => setEduOpen((v) => !v)}
          className="w-full flex items-center justify-between px-4 py-3 bg-sacred-gold-dark text-white text-sm font-semibold"
        >
          <span>{l('Educational Summary', 'शिक्षात्मक सार')}</span>
          {eduOpen ? (
            <ChevronDown className="w-4 h-4 opacity-90" />
          ) : (
            <ChevronRight className="w-4 h-4 opacity-90" />
          )}
        </button>
        {eduOpen && (
          <div className="px-4 py-3 text-sm text-foreground/80 space-y-4">
            <div className="space-y-1">
              <p className="font-semibold text-foreground">{l('How to read this tab', 'इस टैब को कैसे पढ़ें')}</p>
              <ul className="list-disc pl-5 space-y-1">
                <li>{l('Pick a Dasha system from the dropdown.', 'ड्रॉपडाउन से दशा पद्धति चुनें।')}</li>
                <li>{l('The badge “Current” marks the running Mahadasha/period.', '“Current” बैज चल रही महादशा/अवधि बताता है।')}</li>
                <li>{l('Click a row to expand sub-periods (when available).', 'उप-अवधि देखने के लिए रो पर क्लिक करके विस्तार करें (यदि उपलब्ध हो)।')}</li>
              </ul>
            </div>

            <div className="space-y-1">
              <p className="font-semibold text-foreground">{l('Dasha systems in this app (what each is for)', 'इस ऐप की दशाएँ (किसका क्या उपयोग)')}</p>
              <ul className="list-disc pl-5 space-y-1">
                <li>
                  {l(
                    'Vimshottari (120yr): the most common “timing” system (Nakshatra-based). Use for main life timeline + Mahadasha/Antardasha.',
                    'विंशोत्तरी (120 वर्ष): सबसे प्रचलित समय-निर्धारण (नक्षत्र-आधारित)। जीवन की मुख्य टाइमलाइन/महादशा–अन्तरदशा के लिए।'
                  )}
                </li>
                <li>
                  {l(
                    'Yogini (36yr): a compact alternate timing system; often used as a cross-check alongside Vimshottari.',
                    'योगिनी (36 वर्ष): छोटा वैकल्पिक टाइमिंग सिस्टम; अक्सर विंशोत्तरी के साथ क्रॉस-चेक के लिए।'
                  )}
                </li>
                <li>
                  {l(
                    'Ashtottari (108yr): another Nakshatra-based system, traditionally preferred under specific birth conditions; use as a secondary view.',
                    'अष्टोत्तरी (108 वर्ष): एक अन्य नक्षत्र-आधारित प्रणाली; कुछ विशेष जन्म-स्थितियों में अधिक उपयोग; सेकेंडरी व्यू के रूप में देखें।'
                  )}
                </li>
                <li>
                  {l(
                    'Moola: sign/lord-based period view used for quick, simpler sequencing in some traditions (best as a supporting reference).',
                    'मूल: कुछ परंपराओं में सरल क्रम/समयरेखा के लिए राशि/स्वामी-आधारित व्यू (सपोर्टिंग रेफरेंस)।'
                  )}
                </li>
                <li>
                  {l(
                    'Tara: nakshatra-tara based period perspective; useful for another angle on supportive vs. challenging phases.',
                    'तारा: नक्षत्र-तारा आधारित दृष्टि; सहायक बनाम चुनौतीपूर्ण चरण समझने के लिए एक अलग एंगल।'
                  )}
                </li>
              </ul>
            </div>

            {/* Vimshottari planet cycles (only when viewing Vimshottari) */}
            {selectedSystem === 'vimshottari' && (
              <div className="space-y-2">
                <p className="font-semibold text-foreground">
                  {l('Vimshottari Mahadashas (the “Seasons of Life”)', 'विंशोत्तरी महादशाएँ (“जीवन के मौसम”)')}
                </p>
                <p className="text-foreground/80">
                  {l(
                    'Vimshottari divides life into 9 major planetary cycles. The running Mahadasha sets the big theme; sub-periods (Antardasha/Pratyantar) fine-tune events.',
                    'विंशोत्तरी जीवन को 9 प्रमुख ग्रहीय चक्रों में बाँटती है। चल रही महादशा बड़ा थीम तय करती है; अन्तर्दशा/प्रत्यंतर विशिष्ट घटनाएँ और समय को सूक्ष्म बनाते हैं।'
                  )}
                </p>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  <div className="rounded-lg border border-border/40 bg-muted/20 p-3">
                    <p className="text-xs font-bold text-primary mb-1">{l('Sun — 6 years', 'सूर्य — 6 वर्ष')}</p>
                    <p className="text-xs text-foreground/80 leading-relaxed">
                      {l(
                        'Focus on identity, confidence, authority, career direction, and the father/mentors theme. A strong Sun brings leadership and recognition; a weak Sun can bring ego-tests and responsibility lessons.',
                        'पहचान, आत्मविश्वास, अधिकार, करियर दिशा और पिता/गुरु थीम पर फोकस। मजबूत सूर्य नेतृत्व/मान-सम्मान देता है; कमजोर सूर्य अहं-परीक्षा और जिम्मेदारी के पाठ देता है।'
                      )}
                    </p>
                  </div>
                  <div className="rounded-lg border border-border/40 bg-muted/20 p-3">
                    <p className="text-xs font-bold text-primary mb-1">{l('Moon — 10 years', 'चंद्र — 10 वर्ष')}</p>
                    <p className="text-xs text-foreground/80 leading-relaxed">
                      {l(
                        'Emotions, home, mother, mental peace, and inner security become central. Often shows moves/changes in domestic life; good Moon supports calm, care, and emotional maturity.',
                        'भावनाएँ, घर, माता, मानसिक शांति और सुरक्षा केंद्रीय हो जाती है। घर/परिवार में बदलाव/स्थान परिवर्तन संभव; शुभ चंद्र शांति, पोषण और भावनात्मक परिपक्वता देता है।'
                      )}
                    </p>
                  </div>
                  <div className="rounded-lg border border-border/40 bg-muted/20 p-3">
                    <p className="text-xs font-bold text-primary mb-1">{l('Mars — 7 years', 'मंगल — 7 वर्ष')}</p>
                    <p className="text-xs text-foreground/80 leading-relaxed">
                      {l(
                        'Energy, courage, competition, property/land, and decisive action. Great for initiative and breakthroughs; if afflicted, it can show conflict, impatience, injuries, or pressure.',
                        'ऊर्जा, साहस, प्रतिस्पर्धा, संपत्ति/भूमि और निर्णायक कर्म। पहल/ब्रेकथ्रू के लिए अच्छा; पीड़ित होने पर विवाद, उतावलेपन, चोट या दबाव दिखा सकता है।'
                      )}
                    </p>
                  </div>
                  <div className="rounded-lg border border-border/40 bg-muted/20 p-3">
                    <p className="text-xs font-bold text-primary mb-1">{l('Rahu — 18 years', 'राहु — 18 वर्ष')}</p>
                    <p className="text-xs text-foreground/80 leading-relaxed">
                      {l(
                        'Transformative, unusual, and worldly-expansion focused: ambition, foreign links, sudden rises, tech/media, and new identities. Brings breakthroughs—but also illusions if ethics/clarity are weak.',
                        'परिवर्तनकारी और असामान्य: महत्वाकांक्षा, विदेश/नेटवर्क, अचानक उन्नति, टेक/मीडिया और नई पहचान। ब्रेकथ्रू देता है—पर स्पष्टता/नीति कमजोर हो तो भ्रम भी दे सकता है।'
                      )}
                    </p>
                  </div>
                  <div className="rounded-lg border border-border/40 bg-muted/20 p-3">
                    <p className="text-xs font-bold text-primary mb-1">{l('Jupiter — 16 years', 'बृहस्पति — 16 वर्ष')}</p>
                    <p className="text-xs text-foreground/80 leading-relaxed">
                      {l(
                        'Growth through wisdom: education, mentors, marriage support, children, dharma and values. Strong Jupiter brings protection and opportunities; weak Jupiter can bring over-trust or missed guidance.',
                        'ज्ञान से विकास: शिक्षा, गुरु, विवाह-सहायता, संतान, धर्म और मूल्य। मजबूत बृहस्पति संरक्षण/अवसर देता है; कमजोर बृहस्पति अति-विश्वास या गलत मार्गदर्शन दिखा सकता है।'
                      )}
                    </p>
                  </div>
                  <div className="rounded-lg border border-border/40 bg-muted/20 p-3">
                    <p className="text-xs font-bold text-primary mb-1">{l('Saturn — 19 years', 'शनि — 19 वर्ष')}</p>
                    <p className="text-xs text-foreground/80 leading-relaxed">
                      {l(
                        'Discipline, duty, endurance, and long-term foundation-building. Often rewards consistent work and integrity; can feel heavy if shortcuts are taken. Excellent for stability and mastery.',
                        'अनुशासन, कर्तव्य, धैर्य और दीर्घकालीन आधार निर्माण। सतत मेहनत/सच्चाई का फल देता है; शॉर्टकट लेने पर भारीपन महसूस हो सकता है। स्थिरता और महारत के लिए श्रेष्ठ।'
                      )}
                    </p>
                  </div>
                  <div className="rounded-lg border border-border/40 bg-muted/20 p-3">
                    <p className="text-xs font-bold text-primary mb-1">{l('Mercury — 17 years', 'बुध — 17 वर्ष')}</p>
                    <p className="text-xs text-foreground/80 leading-relaxed">
                      {l(
                        'Learning, communication, trade/business, networking, and adaptability. Strong Mercury favors skills, writing, sales, analysis; afflicted Mercury can bring confusion, anxiety, or mixed decisions.',
                        'सीख, संवाद, व्यापार, नेटवर्किंग और अनुकूलन। मजबूत बुध स्किल, लेखन, सेल्स, विश्लेषण में मदद करता है; पीड़ित बुध भ्रम, बेचैनी या मिश्रित निर्णय दे सकता है।'
                      )}
                    </p>
                  </div>
                  <div className="rounded-lg border border-border/40 bg-muted/20 p-3">
                    <p className="text-xs font-bold text-primary mb-1">{l('Ketu — 7 years', 'केतु — 7 वर्ष')}</p>
                    <p className="text-xs text-foreground/80 leading-relaxed">
                      {l(
                        'Detachment and inner breakthroughs: simplification, spiritual focus, cutting what no longer fits. Can feel like endings/reset; used well, it brings clarity and deep karmic resolution.',
                        'वैराग्य और अंदरूनी ब्रेकथ्रू: सरलता, आध्यात्मिक फोकस, जो उपयुक्त नहीं उसे छोड़ना। अंत/रीसेट जैसा लग सकता है; सही उपयोग पर स्पष्टता और गहरी कर्म-शुद्धि देता है।'
                      )}
                    </p>
                  </div>
                  <div className="rounded-lg border border-border/40 bg-muted/20 p-3 md:col-span-2">
                    <p className="text-xs font-bold text-primary mb-1">{l('Venus — 20 years', 'शुक्र — 20 वर्ष')}</p>
                    <p className="text-xs text-foreground/80 leading-relaxed">
                      {l(
                        'Relationships, harmony, luxury, art, comfort and enjoyment. Strong Venus supports love, resources, beauty and social ease; weak Venus can show indulgence, relationship lessons, or value-conflicts.',
                        'रिश्ते, सामंजस्य, विलासिता, कला, सुख-सुविधा और आनंद। मजबूत शुक्र प्रेम, संसाधन, सौंदर्य और सामाजिक सहजता देता है; कमजोर शुक्र अति-भोग, रिश्तों के पाठ या मूल्य-संघर्ष दिखा सकता है।'
                      )}
                    </p>
                  </div>
                </div>

                <div className="rounded-lg bg-muted/30 border border-border/40 p-3">
                  <p className="font-semibold text-foreground mb-1">{l('How to interpret (fast rule)', 'कैसे समझें (फास्ट नियम)')}</p>
                  <p>
                    {l(
                      'Treat the Mahadasha lord as the “temporary boss” of life. If that planet is strong in your chart (good dignity/house support), the period tends to manifest more smoothly; if weak/afflicted, growth often comes through challenge.',
                      'महादशा स्वामी को जीवन का “अस्थायी बॉस” समझें। ग्रह मजबूत (दिग्निटी/भाव समर्थन) हो तो फल अधिक सहज; कमजोर/पीड़ित हो तो विकास अक्सर चुनौती के माध्यम से आता है।'
                    )}
                  </p>
                </div>
              </div>
            )}

            <div className="space-y-1">
              <p className="font-semibold text-foreground">{l('What “Nature” means', '“प्रकृति” का अर्थ')}</p>
              <p>
                {l(
                  'Nature is a simple benefic/malefic indicator for the period’s lord (or sign-lord in sign-based systems). It helps you quickly see if a period is generally supportive vs. challenging.',
                  'प्रकृति अवधि के स्वामी (या राशि-आधारित पद्धतियों में राशि-स्वामी) की शुभ/पाप/मिश्रित प्रवृत्ति का सरल संकेत है — इससे जल्दी समझ आता है कि अवधि सामान्यतः सहायक है या चुनौतीपूर्ण।'
                )}
              </p>
            </div>

            <div className="rounded-lg bg-muted/30 border border-border/40 p-3">
              <p className="font-semibold text-foreground mb-1">{l('Tip', 'टिप')}</p>
              <p>
                {l(
                  'For detailed interpretations (“what it means for you”), open the “Dasha Phala” tab.',
                  'विस्तृत फलादेश/व्याख्या (“आपके लिए इसका अर्थ”) के लिए “दशा फल” टैब खोलें।'
                )}
              </p>
            </div>

            {!kundliId && (
              <p className="text-foreground/70">
                {l('Generate or load a Kundli first to calculate the timeline.', 'समयरेखा देखने के लिए पहले कुंडली जनरेट या लोड करें।')}
              </p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
