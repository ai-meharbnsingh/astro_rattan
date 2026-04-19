import React, { useState, useCallback, useEffect } from 'react';
import { Loader2, ChevronDown, ChevronRight } from 'lucide-react';
import { api } from '@/lib/api';
import { translatePlanet, translateName } from '@/lib/backend-translations';
import { PLANET_NATURE } from '@/components/kundli/kundli-utils';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '@/components/ui/table';
import { Heading } from '@/components/ui/heading';
import { Button } from '@/components/ui/button';

/* ------------------------------------------------------------------ */
/*  Types                                                              */
/* ------------------------------------------------------------------ */

interface DashaPeriod {
  planet: string;
  yogini?: string;
  start: string;
  end: string;
  years?: number;
  duration_years?: number;
  span?: number;
  is_current?: boolean;
  antardasha?: DashaPeriod[];
  pratyantar?: DashaPeriod[];
}

interface DashaResponse {
  system: string;
  current_dasha?: string;
  current_antardasha?: string;
  current_pratyantar?: string;
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
}

const DASHA_SYSTEMS: DashaSystemMeta[] = [
  { key: 'vimshottari', labelEn: 'Vimshottari (120yr)', labelHi: 'विंशोत्तरी (120 वर्ष)', endpoint: '/api/kundli/{id}/dasha' },
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
  if (nature === 'Benefic') return 'text-green-600';
  if (nature === 'Malefic') return 'text-red-600';
  return 'text-amber-600';
}

function periodBg(planet: string, isCurrent: boolean): string {
  if (!isCurrent) return '';
  const nature = PLANET_NATURE[planet];
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
      const res = await api.get(url);
      const normalized = (res && typeof res === 'object')
        ? ({ ...(res as any), system } as DashaResponse)
        : ({ system } as DashaResponse);
      setData((prev) => ({ ...prev, [system]: cloneResponse(normalized) }));
    } catch (err: any) {
      // Only surface the error if this is still the latest request (prevents stale errors)
      if (reqId === latestReqRef.current) {
        setError(err?.message || 'Failed to load dasha data');
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
        <div className="bg-muted rounded-xl border border-border p-4">
          <div className="flex items-center justify-between mb-3">
            <Heading as={4} variant={4} className="uppercase tracking-wide">
              {l('Current Running Period', 'वर्तमान चल रही दशा')}
            </Heading>
            <span className="px-2 py-0.5 bg-muted text-white text-[10px] font-bold rounded animate-pulse">
              {l('LIVE', 'लाइव')}
            </span>
          </div>
          {(() => {
            const currentMD = periods.find((p) => p.is_current);
            const currentADList = currentMD?.antardasha?.find((a) => a.is_current);
            const currentPT = currentADList?.pratyantar?.find((p) => p.is_current);
            if (!currentMD && !currentData.current_dasha) return (
              <p className="text-sm text-foreground/70">{l('No current period identified', 'कोई वर्तमान दशा नहीं मिली')}</p>
            );
            const mdLabel = currentMD?.yogini || currentMD?.planet || currentData.current_dasha || '';
            const adLabel = currentADList?.yogini || currentADList?.planet || currentData.current_antardasha || '';
            const ptLabel = currentPT?.yogini || currentPT?.planet || currentData.current_pratyantar || '';
            return (
              <div className="flex flex-wrap gap-3 text-sm">
                <div className="flex items-center gap-1">
                  <span className="text-foreground/70">{t('kundli.mahadasha')}:</span>
                  <span className={`font-bold ${periodColor(mdLabel)}`}>
                    {translatePlanet(mdLabel, language) || translateName(mdLabel, language)}
                  </span>
                  {natureBadge(mdLabel, hi)}
                </div>
                {adLabel && (
                  <div className="flex items-center gap-1">
                    <span className="text-foreground/70">{t('kundli.antardasha')}:</span>
                    <span className={`font-bold ${periodColor(adLabel)}`}>
                      {translatePlanet(adLabel, language) || translateName(adLabel, language)}
                    </span>
                  </div>
                )}
                {ptLabel && (
                  <div className="flex items-center gap-1">
                    <span className="text-foreground/70">{t('kundli.pratyantar')}:</span>
                    <span className={`font-bold ${periodColor(ptLabel)}`}>
                      {translatePlanet(ptLabel, language) || translateName(ptLabel, language)}
                    </span>
                  </div>
                )}
              </div>
            );
          })()}
        </div>
      )}

      {/* Full timeline with expandable tree */}
      {periods.length > 0 && (
        <div className="bg-muted rounded-xl border border-border p-4">
          <Heading as={4} variant={4} className="mb-3">
            {l('Dasha Timeline', 'दशा समयरेखा')}
          </Heading>
          <div className="overflow-x-auto">
            <Table className="w-full text-xs">
              <TableHeader className="bg-muted">
                <TableRow>
                  <TableHead className="w-8"></TableHead>
                  <TableHead className="text-left p-1.5 text-primary font-medium">
                    {l('Dasha Lord', 'दशा स्वामी')}
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
                  const mdKey = md.yogini || md.planet;
                  const mdLabel = md.yogini
                    ? translateName(md.yogini, language)
                    : translatePlanet(md.planet, language);
                  const isMdExpanded = expandedMD === mdKey;
                  const hasChildren = (md.antardasha || []).length > 0;
                  const mdYears = md.years ?? md.span ?? (md.duration_years ? parseFloat(String(md.duration_years)).toFixed(1) : '');

                  return (
                    <React.Fragment key={`${selectedSystem}-${mdKey}`}>
                      {/* Mahadasha row */}
                      <TableRow
                        className={`cursor-pointer transition-colors ${md.is_current ? `${periodBg(md.planet, true)} border-l-2 border-l-primary` : 'hover:bg-muted/5'}`}
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
                          <span className={`font-bold ${md.is_current ? 'text-primary' : periodColor(md.planet)}`}>
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
                        <TableCell className="p-1.5 text-center">{natureBadge(md.planet, hi)}</TableCell>
                      </TableRow>

                      {/* Antardasha rows */}
                      {isMdExpanded && (md.antardasha || []).map((ad) => {
                        const adKey = `${mdKey}-${ad.yogini || ad.planet}`;
                        const adLabel = ad.yogini
                          ? translateName(ad.yogini, language)
                          : translatePlanet(ad.planet, language);
                        const isAdExpanded = expandedAD === adKey;
                        const hasADChildren = (ad.pratyantar || []).length > 0;
                        const adYears = ad.years ?? ad.span ?? (ad.duration_years ? parseFloat(String(ad.duration_years)).toFixed(2) : '');

                        return (
                          <React.Fragment key={`${selectedSystem}-${adKey}`}>
                            <TableRow
                              className={`cursor-pointer transition-colors bg-white/30 ${ad.is_current ? `${periodBg(ad.planet, true)} border-l-2 border-l-primary` : 'hover:bg-muted/10'}`}
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
                                <span className={`font-semibold ${ad.is_current ? 'text-primary' : periodColor(ad.planet)}`}>
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
                              <TableCell className="p-1.5 text-center">{natureBadge(ad.planet, hi)}</TableCell>
                            </TableRow>

                            {/* Pratyantardasha rows */}
                            {isAdExpanded && (ad.pratyantar || []).map((pt, idx) => {
                              const ptLabel = pt.yogini
                                ? translateName(pt.yogini, language)
                                : translatePlanet(pt.planet, language);
                              const ptKey = `${selectedSystem}-${adKey}-${pt.yogini || pt.planet}-${pt.start}-${pt.end}-${idx}`;
                              return (
                                <TableRow
                                  key={ptKey}
                                  className={`bg-white/60 transition-colors ${pt.is_current ? periodBg(pt.planet, true) : 'hover:bg-muted/5'}`}
                                >
                                  <TableCell className="p-1"></TableCell>
                                  <TableCell className="p-1.5 pl-12 text-[11px]">
                                    <span className={`${pt.is_current ? 'text-primary font-bold' : periodColor(pt.planet)} opacity-80`}>
                                      {ptLabel}
                                    </span>
                                    {pt.is_current && <span className="ml-1 text-primary font-bold">{'\u25CF'}</span>}
                                  </TableCell>
                                  <TableCell className="p-1.5 text-[11px] text-foreground opacity-60">{pt.start}</TableCell>
                                  <TableCell className="p-1.5 text-[11px] text-foreground opacity-60">{pt.end}</TableCell>
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
    </div>
  );
}
