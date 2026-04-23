import { useState } from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft, Check, X, Minus, ExternalLink } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';
import SEOHead from '@/components/SEOHead';
import { generateBreadcrumbSchema } from '@/lib/seoConfig';

import blogContent from '@/content/blog-accuracy-problem.md?raw';
import comparisonData from '@/content/comparison-data.json';
import landingHero from '@/content/landing-hero.json';
import accuracyAudit from '@/content/accuracy-audit.json';

/* ---------- tiny markdown to JSX (no deps) ---------- */
function renderMarkdown(md: string) {
  const lines = md.split('\n');
  const elements: React.ReactNode[] = [];
  let inTable = false;
  let tableRows: string[][] = [];
  let inList = false;
  let listItems: React.ReactNode[] = [];
  let key = 0;

  const flushTable = () => {
    if (tableRows.length < 2) return;
    const headers = tableRows[0];
    const body = tableRows.slice(2); // skip separator row
    elements.push(
      <div key={key++} className="overflow-x-auto my-6">
        <table className="table-sacred w-full text-sm border-collapse">
          <thead>
            <tr className="border-b-2 border-sacred-gold/30">
              {headers.map((h, i) => (
                <th key={i} className="text-left py-2 px-3 text-sacred-gold-dark font-semibold">{h.trim()}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {body.map((row, ri) => (
              <tr key={ri} className="border-b border-cosmic-border hover:bg-sacred-gold/5">
                {row.map((cell, ci) => (
                  <td key={ci} className="py-2 px-3 text-foreground/80">{cell.trim()}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
    tableRows = [];
    inTable = false;
  };

  const flushList = () => {
    if (!listItems.length) return;
    elements.push(<ol key={key++} className="list-decimal list-inside space-y-1 my-4 text-foreground/80 pl-2">{listItems}</ol>);
    listItems = [];
    inList = false;
  };

  const inlineFormat = (text: string): React.ReactNode => {
    const parts: React.ReactNode[] = [];
    const remaining = text;
    let pk = 0;
    const regex = /(\*\*(.+?)\*\*)|(\*(.+?)\*)|(`(.+?)`)|(\[(.+?)\]\((.+?)\))|(--)|(--)/g;
    let lastIndex = 0;
    let match;
    while ((match = regex.exec(remaining)) !== null) {
      if (match.index > lastIndex) parts.push(remaining.slice(lastIndex, match.index));
      if (match[1]) parts.push(<strong key={pk++} className="text-sacred-gold-dark font-semibold">{match[2]}</strong>);
      else if (match[3]) parts.push(<em key={pk++} className="italic text-foreground/70">{match[4]}</em>);
      else if (match[5]) parts.push(<code key={pk++} className="bg-sacred-gold/10 px-1.5 py-0.5 rounded text-sacred-gold-dark text-xs">{match[6]}</code>);
      else if (match[7]) parts.push(<a key={pk++} href={match[9]} className="text-sacred-gold hover:text-sacred-gold-dark underline" target="_blank" rel="noopener noreferrer">{match[8]}</a>);
      else if (match[10] || match[11]) parts.push(<span key={pk++}>&mdash;</span>);
      lastIndex = match.index + match[0].length;
    }
    if (lastIndex < remaining.length) parts.push(remaining.slice(lastIndex));
    return parts.length === 1 ? parts[0] : <>{parts}</>;
  };

  for (const line of lines) {
    const trimmed = line.trim();

    if (trimmed.startsWith('|') && trimmed.endsWith('|')) {
      if (!inTable) { flushList(); inTable = true; }
      const cells = trimmed.split('|').slice(1, -1);
      tableRows.push(cells);
      continue;
    } else if (inTable) {
      flushTable();
    }

    if (/^\d+\.\s/.test(trimmed)) {
      if (!inList) inList = true;
      listItems.push(<li key={key++} className="text-foreground/80 leading-relaxed">{inlineFormat(trimmed.replace(/^\d+\.\s/, ''))}</li>);
      continue;
    } else if (inList) {
      flushList();
    }

    if (trimmed === '' || trimmed === '---') {
      if (trimmed === '---') elements.push(<hr key={key++} className="border-sacred-gold/20 my-8" />);
      continue;
    }
    if (trimmed.startsWith('# ')) {
      elements.push(<h1 key={key++} className="text-3xl md:text-4xl font-bold text-foreground mt-10 mb-4 leading-tight">{inlineFormat(trimmed.slice(2))}</h1>);
    } else if (trimmed.startsWith('## ')) {
      elements.push(<h2 key={key++} className="text-2xl font-bold text-sacred-gold-dark mt-8 mb-3">{inlineFormat(trimmed.slice(3))}</h2>);
    } else if (trimmed.startsWith('### ')) {
      elements.push(<h3 key={key++} className="text-xl font-semibold text-sacred-gold mt-6 mb-2">{inlineFormat(trimmed.slice(4))}</h3>);
    } else if (trimmed.startsWith('- ')) {
      elements.push(<div key={key++} className="flex gap-2 my-1 text-foreground/80 pl-2"><span className="text-sacred-gold mt-1.5 shrink-0">&#8226;</span><span className="leading-relaxed">{inlineFormat(trimmed.slice(2))}</span></div>);
    } else {
      elements.push(<p key={key++} className="text-foreground/80 leading-relaxed my-3">{inlineFormat(trimmed)}</p>);
    }
  }
  if (inTable) flushTable();
  if (inList) flushList();
  return elements;
}

/* ---------- Comparison Table ---------- */
function ComparisonTable() {
  const { t } = useTranslation();
  const data = comparisonData as any;

  return (
    <div className="mt-12">
      <h2 className="text-2xl font-bold text-foreground mb-6">{t('blog.compare.title')}</h2>
      <div className="overflow-x-auto rounded-xl border border-cosmic-border">
        <table className="table-sacred w-full text-sm">
          <thead>
            <tr className="bg-sacred-gold/10">
              <th className="text-left py-3 px-4 text-sacred-gold-dark font-semibold">{t('blog.compare.feature')}</th>
              <th className="text-center py-3 px-4 text-sacred-gold font-bold">AstroRattan</th>
              <th className="text-center py-3 px-4 text-foreground/60">{t('blog.compare.genericFree')}</th>
              <th className="text-center py-3 px-4 text-foreground/60">{t('blog.compare.premium')}</th>
            </tr>
          </thead>
          <tbody>
            {data.categories?.map((cat: any, ci: number) => (
              <>
                <tr key={`cat-${ci}`} className="bg-sacred-gold/5">
                  <td colSpan={4} className="py-2 px-4 text-sacred-gold-dark font-semibold text-xs uppercase tracking-wider">{cat.name}</td>
                </tr>
                {cat.features?.map((f: any, fi: number) => (
                  <tr key={`f-${ci}-${fi}`} className="border-b border-cosmic-border hover:bg-sacred-gold/5">
                    <td className="py-2.5 px-4 text-foreground/80">{f.name}</td>
                    <td className="py-2.5 px-4 text-center">
                      {f.astrorattan?.supported === true ? <Check className="inline w-5 h-5 text-green-600" /> :
                       f.astrorattan?.supported === false ? <X className="inline w-5 h-5 text-red-500" /> :
                       <Minus className="inline w-5 h-5 text-yellow-500" />}
                    </td>
                    <td className="py-2.5 px-4 text-center">
                      {f.competitor_generic?.supported === true ? <Check className="inline w-5 h-5 text-green-600" /> :
                       f.competitor_generic?.supported === false ? <X className="inline w-5 h-5 text-red-500" /> :
                       <Minus className="inline w-5 h-5 text-yellow-500" />}
                    </td>
                    <td className="py-2.5 px-4 text-center">
                      {f.competitor_premium?.supported === true ? <Check className="inline w-5 h-5 text-green-600" /> :
                       f.competitor_premium?.supported === false ? <X className="inline w-5 h-5 text-red-500" /> :
                       <Minus className="inline w-5 h-5 text-yellow-500" />}
                    </td>
                  </tr>
                ))}
              </>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

/* ---------- Stats Banner ---------- */
function StatsBanner() {
  const { language } = useTranslation();
  const hero = landingHero as any;
  return (
    <div className="grid grid-cols-2 md:grid-cols-5 gap-4 my-10">
      {hero.stats?.map((s: any, i: number) => (
        <div key={i} className="bg-white border border-cosmic-border rounded-xl p-4 text-center shadow-sm">
          <div className="text-3xl font-bold text-sacred-gold">{s.value}</div>
          <div className="text-xs text-foreground/60 mt-1">{language === 'hi' ? (s.label_hi || s.label_en) : s.label_en}</div>
          <div className="text-[10px] text-foreground/40">{language === 'hi' ? (s.detail_hi || s.detail_en) : s.detail_en}</div>
        </div>
      ))}
    </div>
  );
}

/* ---------- Main Blog Page ---------- */
export default function BlogPage() {
  const { t, language } = useTranslation();
  const hero = landingHero as any;
  const [activeTab, setActiveTab] = useState<'article' | 'compare' | 'accuracy'>('article');

  const breadcrumbs = generateBreadcrumbSchema([
    { name: 'Home', item: '/' },
    { name: 'Blog', item: '/blog' }
  ]);

  return (
    <div className="min-h-screen bg-[var(--parchment)]">
      <SEOHead pageKey="blog" jsonLd={[breadcrumbs]} />
      {/* Hero */}
      <div className="relative overflow-hidden bg-gradient-to-b from-sacred-gold/5 to-transparent">
        <div className="max-w-4xl mx-auto px-4 pt-8 pb-6 relative">
          <Link to="/" className="inline-flex items-center gap-2 text-sacred-gold hover:text-sacred-gold-dark text-sm mb-6 transition-colors">
            <ArrowLeft className="w-4 h-4" /> {t('blog.backToHome')}
          </Link>
          <div className="inline-block bg-sacred-gold/10 border border-sacred-gold/30 text-sacred-gold-dark text-xs font-medium px-3 py-1 rounded-full mb-4">
            {language === 'hi' ? (hero.accuracy_badge_hi || hero.accuracy_badge) : hero.accuracy_badge}
          </div>
          <h1 className="text-3xl md:text-5xl font-bold text-foreground leading-tight mb-3">
            {language === 'hi' ? hero.headline_hi : hero.headline_en}
          </h1>
          <p className="text-lg text-foreground/60 max-w-2xl">
            {language === 'hi' ? hero.subheadline_hi : hero.subheadline_en}
          </p>
          <StatsBanner />
        </div>
      </div>

      {/* Tab nav */}
      <div className="max-w-4xl mx-auto px-4">
        <div className="flex gap-1 bg-sacred-gold/10 rounded-lg p-1 mb-8 border border-sacred-gold/20">
          {([
            { key: 'article' as const, label: t('blog.tab.article') },
            { key: 'compare' as const, label: t('blog.tab.compare') },
            { key: 'accuracy' as const, label: t('blog.tab.accuracy') },
          ]).map(tab => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              className={`flex-1 py-2.5 px-4 rounded-md text-sm font-medium transition-all ${
                activeTab === tab.key
                  ? 'bg-sacred-gold text-white shadow-sm'
                  : 'text-foreground/50 hover:text-foreground/80'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Article */}
        {activeTab === 'article' && (
          <article className="max-w-none pb-20">
            {renderMarkdown(blogContent)}
          </article>
        )}

        {/* Comparison */}
        {activeTab === 'compare' && (
          <div className="pb-20">
            <ComparisonTable />
            {(comparisonData as any).unique_to_astrorattan && (
              <div className="mt-8 p-6 bg-sacred-gold/5 border border-sacred-gold/20 rounded-xl">
                <h3 className="text-lg font-semibold text-sacred-gold-dark mb-3">{t('blog.article.uniqueTitle')}</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
                  {(comparisonData as any).unique_to_astrorattan.map((item: string, i: number) => (
                    <div key={i} className="flex items-center gap-2 text-sm text-foreground/80">
                      <Check className="w-4 h-4 text-green-600 shrink-0" />
                      {item}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Accuracy Audit */}
        {activeTab === 'accuracy' && (
          <div className="pb-20 space-y-8">
            <h2 className="text-2xl font-bold text-foreground">{t('blog.accuracy.title')}</h2>

            {/* Engine */}
            {(accuracyAudit as any).engine && (
              <div className="bg-white border border-cosmic-border rounded-xl p-6 shadow-sm">
                <h3 className="text-lg font-semibold text-sacred-gold-dark mb-3">{t('blog.accuracy.calculationEngine')}</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                  {Object.entries((accuracyAudit as any).engine).map(([k, v]: [string, any]) => (
                    <div key={k}>
                      <div className="text-foreground/40 text-xs uppercase">{k.replace(/_/g, ' ')}</div>
                      <div className="text-foreground mt-0.5">{String(v)}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Dasha Systems */}
            {(accuracyAudit as any).dasha_systems && (
              <div className="bg-white border border-cosmic-border rounded-xl p-6 shadow-sm">
                <h3 className="text-lg font-semibold text-sacred-gold-dark mb-3">
                  {(accuracyAudit as any).dasha_systems.length} {t('blog.accuracy.dashaSystems')}
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {(accuracyAudit as any).dasha_systems.map((d: any, i: number) => (
                    <div key={i} className="flex justify-between items-center bg-sacred-gold/5 rounded-lg px-4 py-2.5">
                      <div>
                        <span className="text-sacred-gold-dark font-medium">{d.name}</span>
                        <span className="text-foreground/40 text-xs ml-2">{d.cycle}</span>
                      </div>
                      <code className="text-xs text-foreground/40">{d.engine_file}</code>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Yogas */}
            {(accuracyAudit as any).yogas && (
              <div className="bg-white border border-cosmic-border rounded-xl p-6 shadow-sm">
                <h3 className="text-lg font-semibold text-sacred-gold-dark mb-3">
                  {(accuracyAudit as any).yogas.total_count} {t('blog.accuracy.yogasDetected')}
                </h3>
                <div className="space-y-3">
                  {(accuracyAudit as any).yogas.categories?.map((cat: any, i: number) => (
                    <div key={i}>
                      <div className="text-xs text-sacred-gold font-medium mb-1">{cat.name} ({cat.count})</div>
                      <div className="flex flex-wrap gap-1.5">
                        {cat.yogas?.map((y: string, j: number) => (
                          <span key={j} className="bg-sacred-gold/10 text-foreground/60 text-xs px-2 py-0.5 rounded">{y}</span>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Divisional Charts */}
            {(accuracyAudit as any).divisional_charts && (
              <div className="bg-white border border-cosmic-border rounded-xl p-6 shadow-sm">
                <h3 className="text-lg font-semibold text-sacred-gold-dark mb-3">
                  {(accuracyAudit as any).divisional_charts.length} {t('blog.accuracy.divisionalCharts')}
                </h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-sm">
                  {(accuracyAudit as any).divisional_charts.map((d: any, i: number) => (
                    <div key={i} className="bg-sacred-gold/5 rounded px-3 py-2">
                      <span className="text-sacred-gold font-mono">{d.chart}</span>
                      <span className="text-foreground/50 ml-2 text-xs">{d.name}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* CTA */}
            <div className="text-center pt-4">
              <Link
                to="/kundli"
                className="inline-flex items-center gap-2 bg-sacred-gold hover:bg-sacred-gold-dark text-white font-semibold px-8 py-3 rounded-xl transition-colors"
              >
                {t('blog.cta.generateKundli')} <ExternalLink className="w-4 h-4" />
              </Link>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
