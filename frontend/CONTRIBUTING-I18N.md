# Internationalization (i18n) Guide

This project supports English (`en`) and Hindi (`hi`). All user-facing strings must be translated.

## Adding New Translations

1. Open `src/lib/i18n.ts`.
2. Add your key to **both** the `en` and `hi` blocks:
   ```ts
   // In the en: { ... } block:
   'auto.myNewLabel': 'My New Label',

   // In the hi: { ... } block:
   'auto.myNewLabel': 'मेरा नया लेबल',
   ```
3. Use the key in your component:
   ```tsx
   const { t } = useTranslation();
   return <h2>{t('auto.myNewLabel')}</h2>;
   ```

## Key Naming Convention

- Prefix with `auto.` for general UI strings.
- Use descriptive camelCase: `auto.dailyHoroscope`, `auto.submitButton`.
- For section-specific keys, use dot-separated namespaces: `kundli.details`, `blog.title`.

## Rules

1. **No hardcoded user-facing strings.** Every visible English/Hindi string must use `t()`.
2. **Both languages required.** Every key in `en` must exist in `hi` and vice versa.
3. **Run checks before committing:** `npm run i18n:check`

## The `l()` Pattern

Some components use a local `l(en, hi)` helper for data-driven bilingual content
(e.g., API responses that already have en/hi variants). This is acceptable for:

- Dynamic content from API responses with both language values
- Inline bilingual arrays/objects where the translation is co-located with the data

For static UI labels, always prefer `t()` with keys in `i18n.ts`.

## Running Checks

```bash
# Scan for hardcoded strings (detects untranslated text)
npm run i18n:scan

# Validate key completeness (missing keys, EN/HI parity)
npm run i18n:validate

# Run both checks together
npm run i18n:check
```

Use `--fix` with the scanner to see suggested `t()` keys:
```bash
node scripts/scan-hardcoded-strings.cjs --fix
```

## What Does NOT Need Translation

These are automatically skipped by the scanner:

- **CSS classes** inside `className="..."`
- **Console statements** (`console.log`, `console.warn`, `console.error`)
- **Import/export statements**
- **Technical strings**: HTTP methods, MIME types, URLs, paths, date formats
- **Identifiers**: camelCase, PascalCase, snake_case variable/component names
- **Format strings**: `en-IN`, `YYYY-MM-DD`, `utf-8`
- **Pure numbers and CSS values**: `16px`, `100%`, `#ff0000`
- **Strings already wrapped** in `t()` or `l()`
- **Strings under 2 characters**
- **Symbols and punctuation-only strings**
- **Astrological Sanskrit terms** used as technical identifiers (Rahu, Ketu, Lagna, etc.)

## Pre-commit Hook

Install the hook to block commits with missing keys:

```bash
cp scripts/pre-commit-i18n.sh .git/hooks/pre-commit
```

Or add to an existing hook:
```bash
# In .git/hooks/pre-commit
node scripts/validate-i18n-keys.cjs || exit 1
```
