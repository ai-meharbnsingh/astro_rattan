'use strict';

const fs = require('fs');
const path = require('path');

const today = new Date().toISOString().split('T')[0];

const routes = [
  { loc: 'https://astrorattan.com/',             changefreq: 'daily',   priority: '1.0' },
  { loc: 'https://astrorattan.com/kundli',       changefreq: 'monthly', priority: '0.9' },
  { loc: 'https://astrorattan.com/horoscope',    changefreq: 'daily',   priority: '0.9' },
  { loc: 'https://astrorattan.com/panchang',     changefreq: 'daily',   priority: '0.8' },
  { loc: 'https://astrorattan.com/blog',         changefreq: 'weekly',  priority: '0.8' },
  { loc: 'https://astrorattan.com/numerology',   changefreq: 'monthly', priority: '0.7' },
  { loc: 'https://astrorattan.com/lal-kitab',    changefreq: 'monthly', priority: '0.7' },
  { loc: 'https://astrorattan.com/vastu',        changefreq: 'monthly', priority: '0.7' },
  { loc: 'https://astrorattan.com/about',        changefreq: 'monthly', priority: '0.5' },
];

const urlEntries = routes
  .map(
    (r) =>
      `  <url>\n    <loc>${r.loc}</loc>\n    <lastmod>${today}</lastmod>\n    <changefreq>${r.changefreq}</changefreq>\n    <priority>${r.priority}</priority>\n  </url>`
  )
  .join('\n');

const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urlEntries}
</urlset>
`;

const outPath = path.resolve(__dirname, '../public/sitemap.xml');
fs.writeFileSync(outPath, xml, 'utf8');

console.log(`✓ Sitemap generated with ${routes.length} URLs (lastmod: ${today})`);
