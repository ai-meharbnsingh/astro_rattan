/**
 * SafeRender utilities to prevent React Error #31
 * (Cannot render object with keys {hi, en} in JSX)
 *
 * Use these helpers for ANY field that might be a bilingual object.
 * This is a safety layer to catch edge cases where backend returns unexpected data.
 */

import type React from 'react';

export function pickLang(value: any, isHi: boolean): string {
  if (value === null || value === undefined) return '';
  if (typeof value === 'string') return value;
  if (typeof value === 'number') return String(value);
  if (typeof value === 'boolean') return String(value);

  // Handle bilingual objects { hi: string, en: string }
  if (typeof value === 'object' && !Array.isArray(value)) {
    const lang = isHi ? 'hi' : 'en';
    const text = (value as any)[lang];
    if (typeof text === 'string' && text.length > 0) return text;
    if (typeof text === 'number') return String(text);
    // Fallback to other language if preferred language missing
    const otherLang = isHi ? 'en' : 'hi';
    const otherText = (value as any)[otherLang];
    if (typeof otherText === 'string' && otherText.length > 0) return otherText;
    if (typeof otherText === 'number') return String(otherText);
    return '';
  }

  // For arrays or other types, return empty string to prevent React Error #31
  return '';
}

export function safeRender(value: any, isHi?: boolean): string {
  if (isHi === undefined) isHi = false;

  if (value === null || value === undefined) return '';
  if (typeof value === 'string') return value;
  if (typeof value === 'number') return String(value);
  if (typeof value === 'boolean') return String(value);

  // For bilingual objects, use pickLang
  if (typeof value === 'object' && !Array.isArray(value)) {
    return pickLang(value, isHi);
  }

  // For arrays or other objects, return empty string to prevent React Error #31
  return '';
}

/**
 * Type guard to check if value is a bilingual object
 */
export function isBilingualObject(value: any): boolean {
  return (
    typeof value === 'object' &&
    value !== null &&
    !Array.isArray(value) &&
    (typeof (value as any).hi === 'string' || typeof (value as any).en === 'string')
  );
}

/**
 * Safe wrapper for rendering any value - catches bilingual objects at render time
 * Returns the value as-is if it's a safe primitive, converts to string if object
 */
export function safeValue(value: any, isHi?: boolean): string | React.ReactNode {
  if (isHi === undefined) isHi = false;

  if (value === null || value === undefined) return '';
  if (typeof value === 'string') return value;
  if (typeof value === 'number') return value;
  if (typeof value === 'boolean') return value ? 'true' : 'false';

  // Convert objects and arrays to safe strings
  if (typeof value === 'object') {
    // Bilingual object
    if (!Array.isArray(value) && (value.hi || value.en)) {
      return pickLang(value, isHi);
    }
    // Other objects/arrays - return empty to prevent React Error #31
    return '';
  }

  return value;
}
