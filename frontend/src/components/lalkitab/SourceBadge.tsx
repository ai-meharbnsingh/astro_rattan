import { useTranslation } from '@/lib/i18n';

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
  | 'PRODUCT'
  | 'vedic_influenced'
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
};

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

export default function SourceBadge({
  source,
  size = 'xs',
  title,
  className = '',
  lkRef,
}: SourceBadgeProps) {
  const { t } = useTranslation();

  if (!source) return null;
  const cfg = CONFIG[source];
  if (!cfg) return null;

  const label = translateOrFallback(t, cfg.i18nKey, cfg.fallback);
  const description = translateOrFallback(t, cfg.descKey, cfg.descFallback);
  const refSuffix = lkRef ? ` · LK ${lkRef}` : '';
  const tooltip = title ?? description;
  // aria-label is the full accessible name (label + LK ref + description)
  // so screen readers announce what the pill means, not just the abbreviation.
  const ariaLabel = `${label}${refSuffix} — ${description}`;

  const sizeClass = SIZE_CLASSES[size];

  return (
    <span
      role="note"
      aria-label={ariaLabel}
      title={tooltip}
      className={`inline-flex items-center rounded-full border font-semibold uppercase tracking-wide whitespace-nowrap ${sizeClass} ${cfg.classes} ${className}`.trim()}
      data-source={source}
    >
      {label}{refSuffix}
    </span>
  );
}
