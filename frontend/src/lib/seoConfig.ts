export interface SEOConfig {
  title: string;
  description: string;
  keywords: string;
  canonical: string;
  ogTitle?: string;
  ogDescription?: string;
  ogImage?: string;
  twitterTitle?: string;
  twitterDescription?: string;
  twitterImage?: string;
}

export const SITE_NAME = "Astro Rattan";
export const BASE_URL = "https://astrorattan.com";
export const DEFAULT_OG_IMAGE = `${BASE_URL}/logo.png`;

export const DEFAULT_SEO: SEOConfig = {
  title: `${SITE_NAME} - Vedic Astrology & Spiritual Guidance`,
  description: "Explore ancient Vedic wisdom with AI-powered astrology tools, Panchang, practical editorial guides, tarot, numerology, and live astrologer consultations.",
  keywords: "vedic astrology, kundli, horoscope, panchang, jyotish, birth chart, numerology, tarot, lal kitab, kp system, astrology consultation, astrology blog",
  canonical: BASE_URL,
  ogImage: DEFAULT_OG_IMAGE,
};

export const PAGE_SEO_CONFIG: Record<string, SEOConfig> = {
  home: {
    ...DEFAULT_SEO,
    title: `${SITE_NAME} - Vedic Astrology & Spiritual Guidance`,
    canonical: `${BASE_URL}/`,
  },
  kundli: {
    title: "Free Kundli Generator - Online Vedic Birth Chart | Astro Rattan",
    description: "Generate your detailed Vedic birth chart (Kundli) for free. Get accurate planetary positions, Vimshottari Dasha, and personalized astrological readings.",
    keywords: "free kundli, birth chart, janama kundli, online kundli, vedic astrology chart, horoscope matching",
    canonical: `${BASE_URL}/kundli`,
  },
  horoscope: {
    title: "Daily Horoscope - Today's Astrological Predictions | Astro Rattan",
    description: "Get accurate daily, weekly, and monthly horoscope predictions for all zodiac signs. Discover what the stars have in store for your love, career, and health.",
    keywords: "daily horoscope, today horoscope, zodiac signs, horoscope 2024, rashifal, monthly horoscope",
    canonical: `${BASE_URL}/horoscope`,
  },
  panchang: {
    title: "Daily Panchang - Hindu Calendar & Auspicious Timings | Astro Rattan",
    description: "Access detailed daily Panchang, including Tithi, Nakshatra, Yoga, Karana, and auspicious/inauspicious timings (Choghadiya, Rahu Kaal) for any location.",
    keywords: "daily panchang, hindu calendar, auspicious time, rahu kaal, tithi today, choghadiya",
    canonical: `${BASE_URL}/panchang`,
  },
  lalkitab: {
    title: "Lal Kitab Remedies - Unique Astrological Solutions | Astro Rattan",
    description: "Discover the hidden secrets of Lal Kitab. Get personalized remedies, debt analysis, and unique astrological insights based on Lal Kitab principles.",
    keywords: "lal kitab, lal kitab remedies, lal kitab kundli, astrology remedies, debt removal",
    canonical: `${BASE_URL}/lal-kitab`,
  },
  numerology: {
    title: "Numerology & Tarot - Divine Guidance & Predictions | Astro Rattan",
    description: "Unlock the power of numbers and cards. Get personalized numerology reports and accurate tarot card readings for life's important decisions.",
    keywords: "numerology, tarot reading, life path number, destiny number, online tarot, tarot cards",
    canonical: `${BASE_URL}/numerology`,
  },
  vastu: {
    title: "Vastu Shastra - Vedic Architecture for Harmony | Astro Rattan",
    description: "Balance the energies in your home and workplace with Vastu Shastra. Get expert tips and guidelines for a prosperous and peaceful life.",
    keywords: "vastu shastra, vastu tips, home vastu, office vastu, vedic architecture",
    canonical: `${BASE_URL}/vastu`,
  },
  blog: {
    title: "Astrology Blog - Insights, Guides & Vedic Wisdom | Astro Rattan",
    description: "Stay updated with the latest astrological trends, planetary transits, and spiritual guides. Read expert articles on Vedic astrology and lifestyle.",
    keywords: "astrology blog, jyotish articles, planetary transits, spiritual guides, vedic wisdom",
    canonical: `${BASE_URL}/blog`,
  },
};

export const generateBreadcrumbSchema = (items: { name: string; item: string }[]) => {
  return {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": items.map((item, index) => ({
      "@type": "ListItem",
      "position": index + 1,
      "name": item.name,
      "item": `${BASE_URL}${item.item}`
    }))
  };
};

export const generateFAQSchema = (faqs: { question: string; answer: string }[]) => {
  return {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": faqs.map(faq => ({
      "@type": "Question",
      "name": faq.question,
      "acceptedAnswer": {
        "@type": "Answer",
        "text": faq.answer
      }
    }))
  };
};
