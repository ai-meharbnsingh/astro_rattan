"""Seed data and shared helpers for editorial blog content."""
import json
import re
import sqlite3
from typing import Iterable


DEFAULT_BLOG_POSTS = [
    {
        "slug": "how-to-read-your-daily-panchang",
        "title": "How to Read Your Daily Panchang Before Planning Important Work",
        "excerpt": "A practical guide to tithi, nakshatra, yoga, karana, and Rahu Kaal so users can make better day-to-day timing decisions.",
        "content": """
Daily Panchang is most useful when it helps real decisions. Start with the tithi to understand the lunar tone of the day, then check the nakshatra for mental and emotional quality. Yoga and karana add practical nuance for rituals, travel, and agreements. Rahu Kaal, Gulika Kaal, and Yamaganda matter most when you are selecting a start time for something important rather than when you are simply continuing ordinary work.

If you are planning a ceremony, compare the Panchang factors instead of relying on only one label. A good tithi with a weak nakshatra can still be workable for routine tasks, while a strong nakshatra with a blocked Rahu Kaal window may simply require a different time slot. Sunrise and sunset also matter because many Panchang calculations are day-bound and location-sensitive.

For ordinary users, the simplest method is this: identify the activity, remove clearly blocked periods, and then choose the strongest remaining time window. That is enough for a reliable daily practice. Advanced users can layer in muhurat logic, local festival context, and personal chart timing only after the daily foundation is clear.
""".strip(),
        "tags": ["panchang", "muhurat", "daily astrology"],
        "author_name": "AstroVedic Editorial",
        "seo_title": "Daily Panchang Guide for Real Decisions | AstroVedic",
        "seo_description": "Learn how to read tithi, nakshatra, yoga, karana, and Rahu Kaal to plan important work with more clarity.",
    },
    {
        "slug": "kundli-matching-beyond-guna-score",
        "title": "Kundli Matching Beyond Guna Score: What Actually Needs Review",
        "excerpt": "Why couples should look past a single guna score and examine dosha balance, emotional compatibility, timing, and practical life alignment.",
        "content": """
Kundli matching becomes misleading when it is reduced to a single guna score. The score is a useful screening tool, but it is not the full decision. A serious review must also check Mangal influence, emotional patterns, family compatibility, health indicators, and the quality of timing across major dasha periods.

Marriage is lived in routine, conflict, money, family roles, and health. That means chart review should test whether both people handle stress in similar or complementary ways. Strong attraction with unstable long-term timing often needs caution. Moderate attraction with stable values and compatible dasha support can perform much better over time.

The right workflow is simple: use guna matching for the first pass, review doshas and house-level compatibility next, and then combine astrology with ordinary due diligence. Astrology should sharpen judgment, not replace it. That is where matching becomes useful instead of theatrical.
""".strip(),
        "tags": ["kundli matching", "marriage", "guna milan"],
        "author_name": "AstroVedic Editorial",
        "seo_title": "Kundli Matching Beyond Guna Milan | AstroVedic",
        "seo_description": "Understand why guna score alone is not enough for marriage matching and what deeper compatibility checks matter.",
    },
    {
        "slug": "gemstones-remedies-and-when-not-to-wear-them",
        "title": "Gemstones, Remedies, and When Not to Wear Them",
        "excerpt": "A grounded overview of planetary remedies, why blind gemstone use is risky, and when simpler corrective actions are better.",
        "content": """
Gemstones are not decorative astrology shortcuts. They amplify a planetary current, which means they can help when the underlying recommendation is correct and create noise when it is not. A weak benefic planet is a different case from a troubled malefic planet, and the remedy logic is not interchangeable.

Before recommending a gemstone, confirm the chart context, the specific objective, and whether a lower-risk remedy would work first. Mantra, discipline, donations, fasting, and timing corrections are often more appropriate starting points because they are easier to reverse and easier to observe. Gemstones make more sense when the chart supports strengthening a planet and the user is prepared to wear it consistently.

The practical rule is conservative: never prescribe a gemstone just because a planet rules a popular result like career or wealth. Start with the chart, confirm the intention, and choose the least risky remedy that can produce a measurable improvement.
""".strip(),
        "tags": ["gemstones", "remedies", "astro shop"],
        "author_name": "AstroVedic Editorial",
        "seo_title": "Gemstones and Remedies: A Practical Guide | AstroVedic",
        "seo_description": "Understand when gemstones may help, when they may not, and why conservative astrology remedies are often better first steps.",
    },
]


CORE_SITEMAP_PATHS = [
    "",
    "/kundli",
    "/horoscope",
    "/panchang",
    "/ai-chat",
    "/library",
    "/shop",
    "/consultation",
    "/prashnavali",
    "/numerology",
    "/palmistry",
    "/reports",
    "/blog",
]


def slugify(value: str) -> str:
    """Normalize a title into a URL-safe slug."""
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "post"


def seed_blog_posts(conn: sqlite3.Connection, posts: Iterable[dict] = DEFAULT_BLOG_POSTS):
    """Seed starter blog posts once."""
    existing = conn.execute("SELECT COUNT(*) FROM blog_posts").fetchone()[0]
    if existing:
        return

    for post in posts:
        conn.execute(
            """
            INSERT INTO blog_posts
                (slug, title, excerpt, content, cover_image_url, tags, author_name,
                 seo_title, seo_description, is_published)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
            """,
            (
                post["slug"],
                post["title"],
                post["excerpt"],
                post["content"],
                post.get("cover_image_url"),
                json.dumps(post.get("tags", [])),
                post.get("author_name", "AstroVedic Editorial"),
                post.get("seo_title"),
                post.get("seo_description"),
            ),
        )
    conn.commit()
