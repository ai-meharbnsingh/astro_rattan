import React from 'react';
import { useSEO } from '../hooks/useSEO';
import { SEOConfig, PAGE_SEO_CONFIG } from '../lib/seoConfig';

interface SEOHeadProps {
  config?: Partial<SEOConfig>;
  pageKey?: keyof typeof PAGE_SEO_CONFIG;
  jsonLd?: Record<string, any>[];
}

const SEOHead: React.FC<SEOHeadProps> = ({ config, pageKey, jsonLd }) => {
  const seoConfig = pageKey ? PAGE_SEO_CONFIG[pageKey] : config || {};
  
  useSEO(seoConfig);

  return (
    <>
      {jsonLd && jsonLd.map((ld, index) => (
        <script
          key={`json-ld-${index}`}
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(ld) }}
        />
      ))}
    </>
  );
};

export default SEOHead;
