import { useState, useEffect } from 'react';
import { useTranslation } from '@/lib/i18n';
import { useLalKitab } from './LalKitabContext';
import { apiFetch } from '@/lib/api';
import { AlertTriangle, CheckCircle, Shield, Info } from 'lucide-react';
import { pickLang } from './safe-render';
import { severityPill } from './severity-styles';

type DoshaSource =
  | 'LK_CANONICAL'
  | 'LK_DERIVED'
  | 'VEDIC_INFLUENCED'   // canonical upper-case (Codex D2)
  | 'vedic_influenced'   // backwards-compat lowercase alias
  | 'none'
  | string;

// Helper: both case variants count as "vedic overlay".
function isVedicSource(source: string | null | undefined): boolean {
  if (!source) return false;
  const s = source.toLowerCase();
  return s === 'vedic_influenced';
}

interface DoshaResult {
  key: string;
  nameEn: string;
  nameHi: string;
  detected: boolean;
  severity: 'high' | 'medium' | 'low';
  descEn: string;
  descHi: string;
  remedyEn: string;
  remedyHi: string;
  source: DoshaSource;
  isLkCanonical: boolean;
  isVedicInfluenced: boolean;
}

// Severity pill classes now come from the shared severity-styles helper.
// (Previously this file had its own 3-entry map which broke on unknown values.)

/**
 * Map backend dosha format (snake_case) to frontend DoshaResult (camelCase).
 * Backend returns: name_en, name_hi, description_en, description_hi, remedy_hint_en, remedy_hint_hi,
 *                  source, is_lk_canonical, is_vedic_influenced
 */
function mapBackendDosha(d: any): DoshaResult {
  const source: DoshaSource = d?.source ?? 'LK_CANONICAL';
  const isVedic =
    typeof d?.is_vedic_influenced === 'boolean'
      ? d.is_vedic_influenced
      : isVedicSource(source);
  const isLk =
    typeof d?.is_lk_canonical === 'boolean'
      ? d.is_lk_canonical
      : !isVedicSource(source);
  return {
    key: d?.key ?? '',
    nameEn: pickLang(d?.name_en ?? d?.nameEn ?? '', false),
    nameHi: pickLang(d?.name_hi ?? d?.nameHi ?? '', true),
    detected: d?.detected ?? false,
    severity: d?.severity ?? 'low',
    descEn: pickLang(d?.description_en ?? d?.descEn ?? '', false),
    descHi: pickLang(d?.description_hi ?? d?.descHi ?? '', true),
    remedyEn: pickLang(d?.remedy_hint_en ?? d?.remedyEn ?? '', false),
    remedyHi: pickLang(d?.remedy_hint_hi ?? d?.remedyHi ?? '', true),
    source,
    isLkCanonical: isLk,
    isVedicInfluenced: isVedic,
  };
}

export default function LalKitabDoshaTab() {
  const { t, language } = useTranslation();
  const isHi = language === 'hi';
  const { fullData, kundliId } = useLalKitab();
  const [backendDoshas, setBackendDoshas] = useState<DoshaResult[] | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);

  useEffect(() => {
    // Priority 1: Use doshas from consolidated /api/lalkitab/full/{id} response
    if (fullData?.doshas && !fullData?._errors?.doshas) {
      setBackendDoshas(fullData.doshas.map(mapBackendDosha));
      setLoadError(null);
      return;
    }

    // Priority 2: Fetch from dedicated dosha endpoint
    if (kundliId) {
      apiFetch(`/api/lalkitab/doshas/${kundliId}`)
        .then((res: any) => {
          if (res?.doshas && Array.isArray(res.doshas)) {
            setBackendDoshas(res.doshas.map(mapBackendDosha));
            setLoadError(null);
          }
        })
        .catch(() => {
          setBackendDoshas([]);
          setLoadError(isHi ? 'दोष लोड नहीं हो सके' : 'Could not load doshas');
        });
    }
  }, [kundliId, fullData]);

  const doshas: DoshaResult[] = backendDoshas ?? [];

  // Split into LK canonical vs Vedic overlays (handles both
  // SCREAMING_SNAKE and legacy lowercase source values — Codex D2).
  const lkDoshas = doshas.filter((d) => !isVedicSource(d.source));
  const vedicDoshas = doshas.filter((d) => isVedicSource(d.source));

  const sortByDetected = (arr: DoshaResult[]) => {
    const detected = arr.filter((d) => d.detected);
    const clean = arr.filter((d) => !d.detected);
    return [...detected, ...clean];
  };

  const sortedLk = sortByDetected(lkDoshas);
  const sortedVedic = sortByDetected(vedicDoshas);

  const detectedLk = lkDoshas.filter((d) => d.detected);
  const detectedVedic = vedicDoshas.filter((d) => d.detected);

  const renderCard = (dosha: DoshaResult, variant: 'lk' | 'vedic') => {
    const name = isHi ? dosha.nameHi : dosha.nameEn;
    const desc = isHi ? dosha.descHi : dosha.descEn;
    const remedy = isHi ? dosha.remedyHi : dosha.remedyEn;

    const detectedBorder =
      variant === 'vedic'
        ? 'border-indigo-300/40 bg-indigo-500/5'
        : 'border-red-300/30 bg-red-500/5';
    const cleanBorder =
      variant === 'vedic'
        ? 'border-indigo-200/30 bg-indigo-50/30'
        : 'border-green-300/30 bg-green-500/5';

    return (
      <div
        key={dosha.key}
        className={`rounded-xl p-5 border transition-all ${
          dosha.detected ? detectedBorder : cleanBorder
        }`}
      >
        {/* Card header */}
        <div className="flex items-center justify-between flex-wrap gap-2">
          <div className="flex items-center gap-2">
            <h3 className="font-sans text-lg text-sacred-brown">{name}</h3>
            {variant === 'vedic' && (
              <span className="text-xs font-medium px-2 py-0.5 rounded-full bg-indigo-500/15 text-indigo-600 border border-indigo-300/40">
                {isHi ? 'केवल संदर्भ' : 'reference only'}
              </span>
            )}
          </div>
          {dosha.detected ? (
            <span
              className={`flex items-center gap-1.5 text-sm font-medium ${
                variant === 'vedic' ? 'text-indigo-600' : 'text-red-500'
              }`}
            >
              <AlertTriangle className="w-4 h-4" />
              {t('lk.dosha.detected')}
            </span>
          ) : (
            <span className="flex items-center gap-1.5 text-green-500 text-sm font-medium">
              <CheckCircle className="w-4 h-4" />
              {t('lk.dosha.notDetected')}
            </span>
          )}
        </div>

        {/* Detected details */}
        {dosha.detected && (
          <div className="mt-3 space-y-3">
            {/* Severity badge */}
            <div className="flex items-center gap-2">
              <span className="text-sm text-gray-600">
                {t('lk.dosha.severity')}:
              </span>
              <span
                className={`text-sm font-semibold px-2.5 py-0.5 rounded-full ${severityPill(dosha.severity)}`}
              >
                {dosha.severity === 'high'
                  ? t('lk.dosha.high')
                  : dosha.severity === 'medium'
                    ? t('lk.dosha.medium')
                    : t('lk.dosha.low')}
              </span>
            </div>

            {/* Description */}
            {desc && <p className="text-sm text-gray-700">{desc}</p>}

            {/* Remedy box */}
            {remedy && (
              <div
                className={`rounded-xl p-4 mt-3 border ${
                  variant === 'vedic'
                    ? 'bg-indigo-500/5 border-indigo-300/30'
                    : 'bg-sacred-gold/5 border-sacred-gold/20'
                }`}
              >
                <p
                  className={`text-sm font-medium ${
                    variant === 'vedic' ? 'text-indigo-700' : 'text-sacred-gold'
                  }`}
                >
                  {remedy}
                </p>
              </div>
            )}
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="font-sans text-2xl text-sacred-gold flex items-center gap-2">
          <Shield className="w-6 h-6" />
          {t('lk.dosha.title')}
        </h2>
        <p className="text-gray-500 mt-1">{t('lk.dosha.desc')}</p>
      </div>

      {/* Summary bar (LK canon only) */}
      <div className="rounded-xl p-5 border border-sacred-gold/20 bg-sacred-gold/5 flex items-center justify-between">
        <span className="font-sans text-lg text-sacred-gold">
          {t('lk.dosha.detected')}: {detectedLk.length} / {lkDoshas.length}
        </span>
        <div className="flex items-center gap-2">
          {detectedLk.length > 0 ? (
            <AlertTriangle className="w-5 h-5 text-red-500" />
          ) : (
            <CheckCircle className="w-5 h-5 text-green-500" />
          )}
        </div>
      </div>

      {loadError && (
        <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-red-700 text-sm">
          {loadError}
        </div>
      )}

      {/* ============ SECTION 1: LK CANONICAL ============ */}
      {sortedLk.length > 0 && (
        <section className="space-y-4">
          <div className="flex items-center gap-2 border-b border-sacred-gold/20 pb-2">
            <Shield className="w-5 h-5 text-sacred-gold" />
            <h3 className="font-sans text-xl text-sacred-gold">
              {isHi ? 'दोष (लाल किताब प्रमाणिक)' : 'Doshas (Lal Kitab canon)'}
            </h3>
          </div>
          <div className="space-y-4">
            {sortedLk.map((d) => renderCard(d, 'lk'))}
          </div>
        </section>
      )}

      {/* ============ SECTION 2: VEDIC OVERLAYS ============ */}
      {sortedVedic.length > 0 && (
        <section className="space-y-4 mt-8">
          <div className="flex items-center gap-2 border-b border-indigo-300/40 pb-2">
            <Info className="w-5 h-5 text-indigo-500" />
            <h3 className="font-sans text-xl text-indigo-600">
              {isHi
                ? 'वैदिक ओवरले (केवल संदर्भ के लिए)'
                : 'Vedic Overlays (for reference only)'}
            </h3>
          </div>

          {/* Disclaimer */}
          <div className="rounded-xl border border-indigo-300/40 bg-indigo-50/50 p-4 flex items-start gap-2">
            <Info className="w-4 h-4 text-indigo-500 mt-0.5 flex-shrink-0" />
            <p className="text-sm text-indigo-700">
              {isHi
                ? 'लाल किताब 1952 के मूल सिद्धांत का हिस्सा नहीं। केवल शास्त्रीय वैदिक तुलना हेतु दिखाया गया है।'
                : 'Not part of LK 1952 canon. Shown for cross-reference with classical Vedic tradition.'}
            </p>
          </div>

          {/* Summary for vedic */}
          <div className="text-sm text-indigo-600/80">
            {isHi ? 'पता चले' : 'Detected'}: {detectedVedic.length} / {vedicDoshas.length}
          </div>

          <div className="space-y-4">
            {sortedVedic.map((d) => renderCard(d, 'vedic'))}
          </div>
        </section>
      )}

      {/* Empty state */}
      {sortedLk.length === 0 && sortedVedic.length === 0 && !loadError && (
        <div className="rounded-xl border border-sacred-gold/20 bg-sacred-gold/5 p-6 text-center text-gray-500">
          {isHi ? 'कोई दोष डेटा उपलब्ध नहीं' : 'No dosha data available'}
        </div>
      )}
    </div>
  );
}
