import { useState } from 'react';
import { useTranslation } from '@/lib/i18n';
import ProvenanceModal from './ProvenanceModal';

/**
 * SourceBadge — provenance tag for Lal Kitab backend payloads.
 *
 * Backend `source` values:
 *   - "LK_CANONICAL"      → direct from Lal Kitab 1952 text          (green)
 *   - "LK_DERIVED"        → logical inference from LK principles     (amber)
 *   - "PRODUCT"           → UX feature, not claimed as LK canon      (grey)
 *   - "vedic_influenced"  → Vedic overlay, not LK                    (purple/indigo)
 *   - anything else / null / undefined → renders nothing.
 *
 * Bilingual-aware via useTranslation. Falls back to English if key missing
 * (i18n.ts `t()` returns the key itself on miss, so we check explicitly and
 * substitute a readable English fallback).
 */

export type SourceValue =
  | 'LK_CANONICAL'
  | 'LK_DERIVED'
  | 'LK_ADAPTED'           // Codex D1: rule applied outside 1952 canon
  | 'PRODUCT'
  | 'ML_SCORED'            // Codex D1: learned/model-scored output
  | 'HEURISTIC'            // Codex D1: heuristic weighting
  | 'VEDIC_INFLUENCED'     // canonical upper-case (Codex D2)
  | 'vedic_influenced'     // backwards-compat lowercase alias
  | string
  | null
  | undefined;

export type SourceBadgeSize = 'xs' | 'sm';

interface SourceBadgeProps {
  source: SourceValue;
  size?: SourceBadgeSize;
  title?: string;
  className?: string;
  /** Optional LK reference e.g. "4.08" — shown as `· LK 4.08` after the label. */
  lkRef?: string;
  /** Optional confidence modifier. Reduces badge opacity for low/speculative
   *  signals so users glance-read which provenance is weaker.  */
  confidence?: 'high' | 'moderate' | 'low' | 'speculative';
  /** When true (default), clicking the badge opens the ProvenanceModal
   *  highlighting this source type. Pass false to disable (e.g. when badge
   *  is nested inside another clickable surface). Codex D8. */
  interactive?: boolean;
}

interface BadgeConfig {
  i18nKey: string;
  descKey: string;
  fallback: string;
  descFallback: string;
  classes: string;
}

const CONFIG: Record<string, BadgeConfig> = {
  LK_CANONICAL: {
    i18nKey: 'lk.source.canonical',
    descKey: 'lk.source.canonical.desc',
    fallback: 'LK 1952',
    descFallback: 'Content quoted directly from Lal Kitab 1952 canon.',
    classes: 'bg-green-100 text-green-800 border-green-300',
  },
  LK_DERIVED: {
    i18nKey: 'lk.source.derived',
    descKey: 'lk.source.derived.desc',
    fallback: 'LK derived',
    descFallback: 'Logical inference from Lal Kitab principles — not verbatim quote.',
    classes: 'bg-amber-100 text-amber-800 border-amber-300',
  },
  PRODUCT: {
    i18nKey: 'lk.source.product',
    descKey: 'lk.source.product.desc',
    fallback: 'Product',
    descFallback: 'Product / UX layer — not claimed as Lal Kitab canon.',
    classes: 'bg-gray-100 text-gray-700 border-gray-300',
  },
  vedic_influenced: {
    i18nKey: 'lk.source.vedic',
    descKey: 'lk.source.vedic.desc',
    fallback: 'Vedic overlay',
    descFallback: 'Classical Vedic overlay — shown for cross-reference only.',
    classes: 'bg-indigo-100 text-indigo-800 border-indigo-300',
  },
  // Codex D1 audit — new taxonomy entries
  LK_ADAPTED: {
    i18nKey: 'lk.source.adapted',
    descKey: 'lk.source.adapted.desc',
    fallback: 'LK adapted',
    descFallback: 'LK rule applied to a scenario not explicitly in 1952 text.',
    classes: 'bg-lime-100 text-lime-800 border-lime-300',
  },
  ML_SCORED: {
    i18nKey: 'lk.source.mlScored',
    descKey: 'lk.source.mlScored.desc',
    fallback: 'ML scored',
    descFallback: 'Score produced by a learned / statistical model.',
    classes: 'bg-purple-100 text-purple-800 border-purple-300',
  },
  HEURISTIC: {
    i18nKey: 'lk.source.heuristic',
    descKey: 'lk.source.heuristic.desc',
    fallback: 'Heuristic',
    descFallback: 'Heuristic / empirical weighting — not ML, not canon.',
    classes: 'bg-slate-100 text-slate-800 border-slate-300',
  },
};

// Case-normalisation alias (Codex D2) — SCREAMING_SNAKE variant reuses
// the lowercase config.
CONFIG.VEDIC_INFLUENCED = CONFIG.vedic_influenced;

const SIZE_CLASSES: Record<SourceBadgeSize, string> = {
  // Matches existing LK tab pill styling (see LalKitabPredictionTab.tsx:214 and :292)
  xs: 'text-[10px] px-2 py-0.5',
  sm: 'text-[11px] px-2.5 py-1',
};

function translateOrFallback(t: (k: string) => string, key: string, fallback: string): string {
  // useTranslation's `t()` returns the key itself when missing → treat as miss.
  const v = t(key);
  return v === key ? fallback : v;
}

const CONFIDENCE_CLASSES: Record<string, string> = {
  high: '',                       // full opacity — default
  moderate: 'opacity-85',
  low: 'opacity-70',
  speculative: 'opacity-55 italic',
};

export default function SourceBadge({
  source,
  size = 'xs',
  title,
  className = '',
  lkRef,
  confidence,
  interactive = true,
}: SourceBadgeProps) {
  const { t } = useTranslation();
  const [modalOpen, setModalOpen] = useState(false);

  if (!source) return null;
  const cfg = CONFIG[source];
  if (!cfg) return null;

  const label = translateOrFallback(t, cfg.i18nKey, cfg.fallback);
  const description = translateOrFallback(t, cfg.descKey, cfg.descFallback);
  const refSuffix = lkRef ? ` · LK ${lkRef}` : '';
  const confidenceSuffix = confidence ? ` (${confidence} confidence)` : '';
  const tooltip = title ?? `${description}${confidenceSuffix}${interactive ? ' — click for details' : ''}`;
  // aria-label is the full accessible name so screen readers announce
  // the pill's meaning, including confidence if supplied.
  const ariaLabel = `${label}${refSuffix} — ${description}${confidenceSuffix}`;

  const sizeClass = SIZE_CLASSES[size];
  const confClass = confidence ? (CONFIDENCE_CLASSES[confidence] ?? '') : '';
  const interactiveClass = interactive
    ? 'cursor-pointer hover:ring-2 hover:ring-sacred-gold/30 transition-shadow focus:outline-none focus:ring-2 focus:ring-sacred-gold/50'
    : '';

  const badgeContent = (
    <>
      {label}{refSuffix}
    </>
  );

  const sharedClasses = `inline-flex items-center rounded-full border font-semibold uppercase tracking-wide whitespace-nowrap ${sizeClass} ${cfg.classes} ${confClass} ${interactiveClass} ${className}`.trim();

  if (interactive) {
    return (
      <>
        <button
          type="button"
          aria-label={`${ariaLabel} — click for provenance details`}
          title={tooltip}
          className={sharedClasses}
          data-source={source}
          data-confidence={confidence}
          onClick={(e) => {
            e.stopPropagation();
            setModalOpen(true);
          }}
        >
          {badgeContent}
        </button>
        <ProvenanceModal
          open={modalOpen}
          onClose={() => setModalOpen(false)}
          highlight={typeof source === 'string' ? source : null}
        />
      </>
    );
  }

  return (
    <span
      role="note"
      aria-label={ariaLabel}
      title={tooltip}
      className={sharedClasses}
      data-source={source}
      data-confidence={confidence}
    >
      {badgeContent}
    </span>
  );
}
