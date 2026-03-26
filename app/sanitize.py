"""Input sanitization utilities for user-supplied text."""
import re

# Strip entire script/style blocks (content + tags)
_SCRIPT_RE = re.compile(r'<script[^>]*>.*?</script>', re.IGNORECASE | re.DOTALL)
_STYLE_RE = re.compile(r'<style[^>]*>.*?</style>', re.IGNORECASE | re.DOTALL)

# Regex to match remaining HTML tags (including self-closing and attributes)
_TAG_RE = re.compile(r'<[^>]+>')

# Default maximum length for sanitized text
_DEFAULT_MAX_LENGTH = 10000


def sanitize_text(text, max_length: int = _DEFAULT_MAX_LENGTH) -> str:
    """Strip HTML tags (including script/style content) and limit text length.

    Args:
        text: Input text to sanitize. None is treated as empty string.
        max_length: Maximum allowed length after sanitization.

    Returns:
        Sanitized string with HTML tags removed and length capped.
    """
    if text is None:
        return ""
    if not isinstance(text, str):
        text = str(text)
    # Remove script and style blocks entirely (content included)
    cleaned = _SCRIPT_RE.sub('', text)
    cleaned = _STYLE_RE.sub('', cleaned)
    # Strip remaining HTML tags
    cleaned = _TAG_RE.sub('', cleaned)
    # Limit length
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length]
    return cleaned
