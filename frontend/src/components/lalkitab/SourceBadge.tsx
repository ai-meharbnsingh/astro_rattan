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
}

interface BadgeConfig {
  i18nKey: string;
  fallback: string;
  classes: string;
  defaultTitle: string;
}

const CONFIG: Record<string, BadgeConfig> = {
  LK_CANONICAL: {
    i18nKey: 'lk.source.canonical',
    fallback: 'LK 1952',
    classes: 'bg-green-100 text-green-800 border-green-300',
    defaultTitle: 'Directly sourced from the Lal Kitab 1952 text.',
  },
  LK_DERIVED: {
    i18nKey: 'lk.source.derived',
    fallback: 'LK derived',
    classes: 'bg-amber-100 text-amber-800 border-amber-300',
    defaultTitle: 'Logical inference from Lal Kitab principles (not a direct quote).',
  },
  PRODUCT: {
    i18nKey: 'lk.source.product',
    fallback: 'Product',
    classes: 'bg-gray-100 text-gray-700 border-gray-300',
    defaultTitle: 'Product/UX feature — not claimed as Lal Kitab canon.',
  },
  vedic_influenced: {
    i18nKey: 'lk.source.vedic',
    fallback: 'Vedic overlay',
    classes: 'bg-indigo-100 text-indigo-800 border-indigo-300',
    defaultTitle: 'Vedic astrology overlay — not part of the Lal Kitab system.',
  },
};

const SIZE_CLASSES: Record<SourceBadgeSize, string> = {
  // Matches existing LK tab pill styling (see LalKitabPredictionTab.tsx:214 and :292)
  xs: 'text-[10px] px-2 py-0.5',
  sm: 'text-[11px] px-2.5 py-1',
};

export default function SourceBadge({
  source,
  size = 'xs',
  title,
  className = '',
}: SourceBadgeProps) {
  const { t } = useTranslation();

  if (!source) return null;
  const cfg = CONFIG[source];
  if (!cfg) return null;

  // i18n.ts `t()` returns the key itself when no translation exists.
  // Treat that as a miss and fall back to the English label.
  const translated = t(cfg.i18nKey);
  const label = translated === cfg.i18nKey ? cfg.fallback : translated;

  const sizeClass = SIZE_CLASSES[size];

  return (
    <span
      title={title ?? cfg.defaultTitle}
      className={`inline-flex items-center rounded-full border font-semibold uppercase tracking-wide whitespace-nowrap ${sizeClass} ${cfg.classes} ${className}`.trim()}
      data-source={source}
    >
      {label}
    </span>
  );
}
