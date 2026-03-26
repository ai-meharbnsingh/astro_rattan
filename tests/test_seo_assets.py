"""Static SEO asset regression checks."""
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_index_html_mentions_editorial_blog():
    """Global metadata should mention editorial/blog support."""
    html = (ROOT / "frontend" / "index.html").read_text()
    assert "editorial guides" in html
    assert "astrology blog" in html


def test_static_sitemap_lists_blog_routes():
    """Static sitemap should advertise blog and palmistry entry points."""
    sitemap = (ROOT / "frontend" / "public" / "sitemap.xml").read_text()
    assert "https://astrovedic.com/blog" in sitemap
    assert "https://astrovedic.com/palmistry" in sitemap
    assert "https://astrovedic.com/blog/how-to-read-your-daily-panchang" in sitemap
