/**
 * Shared severity / urgency Tailwind styling utility for Lal Kitab tabs.
 *
 * Before this file existed, each LK tab duplicated colour maps for
 * "high / medium / low" (or takkar's "destructive / mild friction /
 * moderate friction / philosophical conflict", or the dosha engine's
 * severity enum). Keeping them in one place keeps tone consistent and
 * prevents copy-paste drift.
 *
 * Usage:
 *   import { severityPill, severityBorder } from './severity-styles';
 *   <span className={severityPill(dosha.severity)}>…</span>
 */

export type SeverityLevel =
  | 'high'           // destructive / urgent
  | 'medium'         // moderate / mild friction
  | 'low'            // mild / gentle
  | 'none'           // not detected / safe
  | 'destructive'
  | 'moderate friction'
  | 'mild friction'
  | 'philosophical conflict'
  | string;

// Pill (inline rounded-full badge) — use for row-level severity indicators.
const PILL: Record<string, string> = {
  high:                      'bg-red-500/20 text-red-600 border border-red-300/40',
  medium:                    'bg-orange-500/20 text-orange-600 border border-orange-300/40',
  low:                       'bg-yellow-500/20 text-yellow-700 border border-yellow-300/40',
  none:                      'bg-green-500/10 text-green-700 border border-green-300/30',
  destructive:               'bg-red-500/20 text-red-700 border border-red-400/40',
  'moderate friction':       'bg-amber-500/20 text-amber-700 border border-amber-400/40',
  'mild friction':           'bg-yellow-400/20 text-yellow-800 border border-yellow-300/40',
  'philosophical conflict':  'bg-slate-300/30 text-slate-700 border border-slate-300/40',
};

// Border-driven card (larger card with coloured left border) — use for
// cautionary blocks like Andhe Grah alert or Savdhaniyan reminders.
const CARD_BORDER: Record<string, string> = {
  high:        'border-red-400 bg-red-50',
  medium:      'border-orange-300 bg-orange-50',
  low:         'border-yellow-300 bg-yellow-50/60',
  none:        'border-green-300 bg-green-50/60',
  destructive: 'border-red-500 bg-red-50',
  'moderate friction':      'border-amber-400 bg-amber-50',
  'mild friction':          'border-yellow-300 bg-yellow-50',
  'philosophical conflict': 'border-slate-300 bg-slate-50',
};

// Icon colour (text-*) — use for the single accent-colour lucide icon
// in card / section headers.
const ICON: Record<string, string> = {
  high: 'text-red-600',
  medium: 'text-orange-600',
  low: 'text-yellow-600',
  none: 'text-green-600',
  destructive: 'text-red-700',
  'moderate friction': 'text-amber-700',
  'mild friction': 'text-yellow-700',
  'philosophical conflict': 'text-slate-700',
};

const FALLBACK_PILL = 'bg-gray-200/40 text-gray-600 border border-gray-300/40';
const FALLBACK_CARD = 'border-gray-300 bg-gray-50';
const FALLBACK_ICON = 'text-gray-600';

/** Returns Tailwind classes for a pill badge. Unknown severity → neutral grey. */
export function severityPill(severity: SeverityLevel | null | undefined): string {
  if (!severity) return FALLBACK_PILL;
  return PILL[severity as string] ?? FALLBACK_PILL;
}

/** Returns Tailwind border/background classes for a card-style warning. */
export function severityBorder(severity: SeverityLevel | null | undefined): string {
  if (!severity) return FALLBACK_CARD;
  return CARD_BORDER[severity as string] ?? FALLBACK_CARD;
}

/** Returns Tailwind text colour for a single accent icon in a header. */
export function severityIcon(severity: SeverityLevel | null | undefined): string {
  if (!severity) return FALLBACK_ICON;
  return ICON[severity as string] ?? FALLBACK_ICON;
}

/** Bilingual label for a severity value — used in badges when backend
 * hands back a raw enum ("high") and UI wants to say "Destructive" /
 * "तीव्र". Returns the canonical label in chosen language.  */
const LABEL_EN: Record<string, string> = {
  high: 'High',
  medium: 'Medium',
  low: 'Low',
  none: 'None',
  destructive: 'Destructive',
  'moderate friction': 'Moderate',
  'mild friction': 'Mild',
  'philosophical conflict': 'Philosophical',
};
const LABEL_HI: Record<string, string> = {
  high: 'तीव्र',
  medium: 'मध्यम',
  low: 'हल्का',
  none: 'शून्य',
  destructive: 'विनाशकारी',
  'moderate friction': 'मध्यम घर्षण',
  'mild friction': 'हल्का घर्षण',
  'philosophical conflict': 'दार्शनिक',
};

export function severityLabel(severity: SeverityLevel | null | undefined, isHi: boolean): string {
  if (!severity) return '';
  const table = isHi ? LABEL_HI : LABEL_EN;
  const s = String(severity).toLowerCase();
  return table[s] ?? (
    // Fallback: title-case the raw severity value.
    String(severity).charAt(0).toUpperCase() + String(severity).slice(1)
  );
}
