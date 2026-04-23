import { useEffect } from 'react';
import { SEOConfig, DEFAULT_SEO, DEFAULT_OG_IMAGE, SITE_NAME } from '../lib/seoConfig';

export const useSEO = (config: Partial<SEOConfig>) => {
  useEffect(() => {
    const title = config.title || DEFAULT_SEO.title;
    const description = config.description || DEFAULT_SEO.description;
    const keywords = config.keywords || DEFAULT_SEO.keywords;
    const canonical = config.canonical || DEFAULT_SEO.canonical;
    const ogTitle = config.ogTitle || title;
    const ogDescription = config.ogDescription || description;
    const ogImage = config.ogImage || DEFAULT_OG_IMAGE;
    
    // Update Title
    document.title = title;

    // Update Meta Tags
    const updateMetaTag = (name: string, content: string, property = false) => {
      let element = document.querySelector(property ? `meta[property="${name}"]` : `meta[name="${name}"]`);
      if (!element) {
        element = document.createElement('meta');
        if (property) {
          element.setAttribute('property', name);
        } else {
          element.setAttribute('name', name);
        }
        document.head.appendChild(element);
      }
      element.setAttribute('content', content);
    };

    updateMetaTag('description', description);
    updateMetaTag('keywords', keywords);
    
    // Canonical
    let linkCanonical = document.querySelector('link[rel="canonical"]');
    if (!linkCanonical) {
      linkCanonical = document.createElement('link');
      linkCanonical.setAttribute('rel', 'canonical');
      document.head.appendChild(linkCanonical);
    }
    linkCanonical.setAttribute('href', canonical);

    // Open Graph
    updateMetaTag('og:title', ogTitle, true);
    updateMetaTag('og:description', ogDescription, true);
    updateMetaTag('og:image', ogImage, true);
    updateMetaTag('og:site_name', SITE_NAME, true);
    updateMetaTag('og:url', canonical, true);

    // Twitter
    updateMetaTag('twitter:title', config.twitterTitle || ogTitle);
    updateMetaTag('twitter:description', config.twitterDescription || ogDescription);
    updateMetaTag('twitter:image', config.twitterImage || ogImage);
    updateMetaTag('twitter:card', 'summary_large_image');

  }, [config]);
};
