#!/bin/bash
# Pre-commit hook: block commits with missing i18n keys.
# Install: cp scripts/pre-commit-i18n.sh .git/hooks/pre-commit
#   or add to your existing pre-commit hook.
echo "Running i18n checks..."
node scripts/validate-i18n-keys.cjs
if [ $? -ne 0 ]; then
  echo "Missing translation keys detected. Fix before committing."
  exit 1
fi
echo "i18n checks passed"
