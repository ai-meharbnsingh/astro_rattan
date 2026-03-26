"""Mobile Responsive Verification Tests (M-07)

Verifies Tailwind responsive classes are present and viewport meta is configured.
Screenshots would be taken manually or via Playwright for visual verification.
"""
import pytest


class TestTailwindResponsiveClasses:
    """Verify responsive breakpoints are used throughout the frontend."""

    def test_hero_section_responsive_classes(self):
        """Hero uses sm:, lg: breakpoints for text and layout."""
        hero_content = open("frontend/src/sections/Hero.tsx").read()
        # Text scaling
        assert "sm:text-5xl" in hero_content, "Hero missing sm:text-5xl"
        assert "lg:text-6xl" in hero_content, "Hero missing lg:text-6xl"
        # Layout
        assert "lg:grid-cols-2" in hero_content, "Hero missing lg:grid-cols-2"
        assert "lg:text-left" in hero_content, "Hero missing lg:text-left"

    def test_features_section_responsive_classes(self):
        """Features uses md:, lg: breakpoints for grid."""
        features_content = open("frontend/src/sections/Features.tsx").read()
        assert "sm:text-4xl" in features_content, "Features missing sm:text-4xl"
        assert "lg:text-5xl" in features_content, "Features missing lg:text-5xl"
        assert "md:grid-cols-2" in features_content, "Features missing md:grid-cols-2"
        assert "lg:grid-cols-3" in features_content, "Features missing lg:grid-cols-3"

    def test_panchang_section_responsive_classes(self):
        """Panchang uses lg: breakpoints for 3-column layout."""
        panchang_content = open("frontend/src/sections/Panchang.tsx").read()
        assert "lg:grid-cols-3" in panchang_content, "Panchang missing lg:grid-cols-3"

    def test_shop_section_responsive_classes(self):
        """Shop uses sm:, lg: breakpoints for product grid."""
        shop_content = open("frontend/src/sections/Shop.tsx").read()
        assert "sm:grid-cols-2" in shop_content, "Shop missing sm:grid-cols-2"
        assert "lg:grid-cols-4" in shop_content, "Shop missing lg:grid-cols-4"

    def test_user_profile_responsive_classes(self):
        """UserProfile uses sm: breakpoints for stats grid."""
        profile_content = open("frontend/src/sections/UserProfile.tsx").read()
        assert "sm:grid-cols-4" in profile_content, "Profile missing sm:grid-cols-4"
        assert "sm:grid-cols-2" in profile_content, "Profile missing sm:grid-cols-2"

    def test_navigation_responsive_classes(self):
        """Navigation uses responsive patterns."""
        nav_content = open("frontend/src/sections/Navigation.tsx").read()
        # Check for mobile menu pattern or any responsive class
        has_responsive = 'sm:' in nav_content or 'md:' in nav_content or 'lg:' in nav_content or 'xl:' in nav_content
        assert has_responsive, "Navigation missing responsive mobile classes"


class TestViewportMeta:
    """Verify viewport meta tag is present in index.html."""

    def test_viewport_meta_tag(self):
        """Index.html contains proper viewport meta tag."""
        index_html = open("frontend/dist/index.html").read()
        assert 'name="viewport"' in index_html, "Missing viewport meta tag"
        assert "width=device-width" in index_html, "Missing width=device-width"
        assert "initial-scale=1" in index_html, "Missing initial-scale=1"


class TestMobileBreakpoints:
    """Verify all major pages have responsive considerations."""

    PAGES = [
        "Hero.tsx",
        "Features.tsx", 
        "Panchang.tsx",
        "Shop.tsx",
        "KundliGenerator.tsx",
        "AIChat.tsx",
        "SpiritualLibrary.tsx",
        "CartCheckout.tsx",
        "AuthPage.tsx",
        "UserProfile.tsx",
        "AdminDashboard.tsx",
        "AstrologerDashboard.tsx",
    ]

    @pytest.mark.parametrize("page", PAGES)
    def test_page_has_responsive_classes(self, page):
        """Each page has at least one responsive breakpoint class."""
        content = open(f"frontend/src/sections/{page}").read()
        # Check for any Tailwind responsive prefix
        has_responsive = 'sm:' in content or 'md:' in content or 'lg:' in content or 'xl:' in content
        assert has_responsive, f"{page} missing responsive Tailwind classes"


class TestCommonResponsivePatterns:
    """Verify common responsive patterns are used."""

    def test_container_padding_responsive(self):
        """Containers use responsive padding (px-4 sm:px-6 lg:px-8)."""
        import os
        responsive_padding_count = 0
        for file in os.listdir("frontend/src/sections"):
            if file.endswith(".tsx"):
                content = open(f"frontend/src/sections/{file}").read()
                if "sm:px-6" in content and "lg:px-8" in content:
                    responsive_padding_count += 1
        assert responsive_padding_count >= 5, \
            f"Only {responsive_padding_count} files use responsive container padding"

    def test_hidden_on_mobile_patterns(self):
        """Complex elements hidden on mobile with hidden lg:flex."""
        hero_content = open("frontend/src/sections/Hero.tsx").read()
        assert "hidden lg:flex" in hero_content, \
            "Hero should hide complex elements on mobile"

    def test_text_size_responsive(self):
        """Text sizes scale with breakpoints."""
        patterns = [
            ("Hero.tsx", ["text-4xl sm:text-5xl lg:text-6xl"]),
            ("Features.tsx", ["text-3xl sm:text-4xl lg:text-5xl"]),
            ("Panchang.tsx", ["text-3xl sm:text-4xl lg:text-5xl"]),
        ]
        for page, expected_patterns in patterns:
            content = open(f"frontend/src/sections/{page}").read()
            for pattern in expected_patterns:
                assert pattern in content, f"{page} missing text size pattern: {pattern}"


# Visual regression would be done via Playwright E2E tests
# These tests verify the CSS classes are present for responsiveness
