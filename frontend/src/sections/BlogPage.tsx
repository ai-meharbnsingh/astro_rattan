import { useState } from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft, Check, X, Minus, ExternalLink } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';

import blogContent from '@/content/blog-accuracy-problem.md?raw';
import comparisonData from '@/content/comparison-data.json';
import landingHero from '@/content/landing-hero.json';
import accuracyAudit from '@/content/accuracy-audit.json';

/* ---------- tiny markdown → JSX (no deps) ---------- */
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
        <table className="w-full text-sm border-collapse">
          <thead>
            <tr className="border-b-2 border-amber-300/30">
              {headers.map((h, i) => (
                <th key={i} className="text-left py-2 px-3 text-amber-200 font-semibold">{h.trim()}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {body.map((row, ri) => (
              <tr key={ri} className="border-b border-white/10 hover:bg-white/5">
                {row.map((cell, ci) => (
                  <td key={ci} className="py-2 px-3 text-gray-300">{cell.trim()}</td>
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
    elements.push(<ol key={key++} className="list-decimal list-inside space-y-1 my-4 text-gray-300 pl-2">{listItems}</ol>);
    listItems = [];
    inList = false;
  };

  const inlineFormat = (text: string): React.ReactNode => {
    // bold + italic + links + code
    const parts: React.ReactNode[] = [];
    let remaining = text;
    let pk = 0;
    const regex = /(\*\*(.+?)\*\*)|(\*(.+?)\*)|(`(.+?)`)|(\[(.+?)\]\((.+?)\))|(--)|(--)/g;
    let lastIndex = 0;
    let match;
    while ((match = regex.exec(remaining)) !== null) {
      if (match.index > lastIndex) parts.push(remaining.slice(lastIndex, match.index));
      if (match[1]) parts.push(<strong key={pk++} className="text-amber-200 font-semibold">{match[2]}</strong>);
      else if (match[3]) parts.push(<em key={pk++} className="italic text-amber-100/80">{match[4]}</em>);
      else if (match[5]) parts.push(<code key={pk++} className="bg-white/10 px-1.5 py-0.5 rounded text-amber-300 text-xs">{match[6]}</code>);
      else if (match[7]) parts.push(<a key={pk++} href={match[9]} className="text-amber-400 underline hover:text-amber-300" target="_blank" rel="noopener noreferrer">{match[8]}</a>);
      else if (match[10] || match[11]) parts.push(<span key={pk++}>&mdash;</span>);
      lastIndex = match.index + match[0].length;
    }
    if (lastIndex < remaining.length) parts.push(remaining.slice(lastIndex));
    return parts.length === 1 ? parts[0] : <>{parts}</>;
  };

  for (const line of lines) {
    const trimmed = line.trim();

    // table rows
    if (trimmed.startsWith('|') && trimmed.endsWith('|')) {
      if (!inTable) { flushList(); inTable = true; }
      const cells = trimmed.split('|').slice(1, -1);
      tableRows.push(cells);
      continue;
    } else if (inTable) {
      flushTable();
    }

    // ordered list
    if (/^\d+\.\s/.test(trimmed)) {
      if (!inList) inList = true;
      listItems.push(<li key={key++} className="text-gray-300 leading-relaxed">{inlineFormat(trimmed.replace(/^\d+\.\s/, ''))}</li>);
      continue;
    } else if (inList) {
      flushList();
    }

    if (trimmed === '' || trimmed === '---') {
      if (trimmed === '---') elements.push(<hr key={key++} className="border-amber-600/20 my-8" />);
      continue;
    }
    if (trimmed.startsWith('# ')) {
      elements.push(<h1 key={key++} className="text-3xl md:text-4xl font-bold text-amber-100 mt-10 mb-4 leading-tight">{inlineFormat(trimmed.slice(2))}</h1>);
    } else if (trimmed.startsWith('## ')) {
      elements.push(<h2 key={key++} className="text-2xl font-bold text-amber-200 mt-8 mb-3">{inlineFormat(trimmed.slice(3))}</h2>);
    } else if (trimmed.startsWith('### ')) {
      elements.push(<h3 key={key++} className="text-xl font-semibold text-amber-300 mt-6 mb-2">{inlineFormat(trimmed.slice(4))}</h3>);
    } else if (trimmed.startsWith('- ')) {
      elements.push(<div key={key++} className="flex gap-2 my-1 text-gray-300 pl-2"><span className="text-amber-500 mt-1.5 shrink-0">&#8226;</span><span className="leading-relaxed">{inlineFormat(trimmed.slice(2))}</span></div>);
    } else {
      elements.push(<p key={key++} className="text-gray-300 leading-relaxed my-3">{inlineFormat(trimmed)}</p>);
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
      <h2 className="text-2xl font-bold text-amber-100 mb-6">Feature Comparison</h2>
      <div className="overflow-x-auto rounded-xl border border-amber-600/20">
        <table className="w-full text-sm">
          <thead>
            <tr className="bg-amber-900/30">
              <th className="text-left py-3 px-4 text-amber-200 font-semibold">Feature</th>
              <th className="text-center py-3 px-4 text-amber-400 font-bold">AstroRattan</th>
              <th className="text-center py-3 px-4 text-gray-400">Generic Free</th>
              <th className="text-center py-3 px-4 text-gray-400">Premium</th>
            </tr>
          </thead>
          <tbody>
            {data.categories?.map((cat: any, ci: number) => (
              <>
                <tr key={`cat-${ci}`} className="bg-amber-900/10">
                  <td colSpan={4} className="py-2 px-4 text-amber-300 font-semibold text-xs uppercase tracking-wider">{cat.name}</td>
                </tr>
                {cat.features?.map((f: any, fi: number) => (
                  <tr key={`f-${ci}-${fi}`} className="border-b border-white/5 hover:bg-white/5">
                    <td className="py-2.5 px-4 text-gray-300">{f.name}</td>
                    <td className="py-2.5 px-4 text-center">
                      {f.astrorattan?.supported === true ? <Check className="inline w-5 h-5 text-green-400" /> :
                       f.astrorattan?.supported === false ? <X className="inline w-5 h-5 text-red-400" /> :
                       <Minus className="inline w-5 h-5 text-yellow-400" />}
                    </td>
                    <td className="py-2.5 px-4 text-center">
                      {f.competitor_generic?.supported === true ? <Check className="inline w-5 h-5 text-green-400" /> :
                       f.competitor_generic?.supported === false ? <X className="inline w-5 h-5 text-red-400" /> :
                       <Minus className="inline w-5 h-5 text-yellow-400" />}
                    </td>
                    <td className="py-2.5 px-4 text-center">
                      {f.competitor_premium?.supported === true ? <Check className="inline w-5 h-5 text-green-400" /> :
                       f.competitor_premium?.supported === false ? <X className="inline w-5 h-5 text-red-400" /> :
                       <Minus className="inline w-5 h-5 text-yellow-400" />}
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
  const hero = landingHero as any;
  return (
    <div className="grid grid-cols-2 md:grid-cols-5 gap-4 my-10">
      {hero.stats?.map((s: any, i: number) => (
        <div key={i} className="bg-gradient-to-br from-amber-900/40 to-amber-800/20 border border-amber-600/20 rounded-xl p-4 text-center">
          <div className="text-3xl font-bold text-amber-400">{s.value}</div>
          <div className="text-xs text-gray-400 mt-1">{s.label_en}</div>
          <div className="text-[10px] text-gray-500">{s.detail_en}</div>
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

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#1a0e05] via-[#2a1a0a] to-[#1a0e05]">
      {/* Hero */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-amber-900/20 via-transparent to-transparent" />
        <div className="max-w-4xl mx-auto px-4 pt-8 pb-6 relative">
          <Link to="/" className="inline-flex items-center gap-2 text-amber-400/70 hover:text-amber-300 text-sm mb-6 transition-colors">
            <ArrowLeft className="w-4 h-4" /> Back to Home
          </Link>
          <div className="inline-block bg-amber-600/20 border border-amber-500/30 text-amber-300 text-xs font-medium px-3 py-1 rounded-full mb-4">
            {hero.accuracy_badge}
          </div>
          <h1 className="text-3xl md:text-5xl font-bold text-amber-50 leading-tight mb-3">
            {language === 'hi' ? hero.headline_hi : hero.headline_en}
          </h1>
          <p className="text-lg text-gray-400 max-w-2xl">
            {language === 'hi' ? hero.subheadline_hi : hero.subheadline_en}
          </p>
          <StatsBanner />
        </div>
      </div>

      {/* Tab nav */}
      <div className="max-w-4xl mx-auto px-4">
        <div className="flex gap-1 bg-amber-900/20 rounded-lg p-1 mb-8 border border-amber-600/10">
          {([
            { key: 'article' as const, label: 'Blog Article' },
            { key: 'compare' as const, label: 'Feature Comparison' },
            { key: 'accuracy' as const, label: 'Accuracy Audit' },
          ]).map(tab => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              className={`flex-1 py-2.5 px-4 rounded-md text-sm font-medium transition-all ${
                activeTab === tab.key
                  ? 'bg-amber-600/30 text-amber-200 shadow-sm'
                  : 'text-gray-500 hover:text-gray-300'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Article */}
        {activeTab === 'article' && (
          <article className="prose-invert max-w-none pb-20">
            {renderMarkdown(blogContent)}
          </article>
        )}

        {/* Comparison */}
        {activeTab === 'compare' && (
          <div className="pb-20">
            <ComparisonTable />
            {(comparisonData as any).unique_to_astrorattan && (
              <div className="mt-8 p-6 bg-amber-900/20 border border-amber-600/20 rounded-xl">
                <h3 className="text-lg font-semibold text-amber-200 mb-3">Unique to AstroRattan</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
                  {(comparisonData as any).unique_to_astrorattan.map((item: string, i: number) => (
                    <div key={i} className="flex items-center gap-2 text-sm text-gray-300">
                      <Check className="w-4 h-4 text-green-400 shrink-0" />
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
            <h2 className="text-2xl font-bold text-amber-100">Technical Accuracy Audit</h2>

            {/* Engine */}
            {(accuracyAudit as any).engine && (
              <div className="bg-amber-900/20 border border-amber-600/20 rounded-xl p-6">
                <h3 className="text-lg font-semibold text-amber-200 mb-3">Calculation Engine</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                  {Object.entries((accuracyAudit as any).engine).map(([k, v]: [string, any]) => (
                    <div key={k}>
                      <div className="text-gray-500 text-xs uppercase">{k.replace(/_/g, ' ')}</div>
                      <div className="text-gray-200 mt-0.5">{String(v)}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Dasha Systems */}
            {(accuracyAudit as any).dasha_systems && (
              <div className="bg-amber-900/20 border border-amber-600/20 rounded-xl p-6">
                <h3 className="text-lg font-semibold text-amber-200 mb-3">
                  {(accuracyAudit as any).dasha_systems.length} Dasha Systems
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {(accuracyAudit as any).dasha_systems.map((d: any, i: number) => (
                    <div key={i} className="flex justify-between items-center bg-black/20 rounded-lg px-4 py-2.5">
                      <div>
                        <span className="text-amber-200 font-medium">{d.name}</span>
                        <span className="text-gray-500 text-xs ml-2">{d.cycle}</span>
                      </div>
                      <code className="text-xs text-gray-500">{d.engine_file}</code>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Yogas */}
            {(accuracyAudit as any).yogas && (
              <div className="bg-amber-900/20 border border-amber-600/20 rounded-xl p-6">
                <h3 className="text-lg font-semibold text-amber-200 mb-3">
                  {(accuracyAudit as any).yogas.total_count} Yogas Detected
                </h3>
                <div className="space-y-3">
                  {(accuracyAudit as any).yogas.categories?.map((cat: any, i: number) => (
                    <div key={i}>
                      <div className="text-xs text-amber-400 font-medium mb-1">{cat.name} ({cat.count})</div>
                      <div className="flex flex-wrap gap-1.5">
                        {cat.yogas?.map((y: string, j: number) => (
                          <span key={j} className="bg-black/30 text-gray-400 text-xs px-2 py-0.5 rounded">{y}</span>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Divisional Charts */}
            {(accuracyAudit as any).divisional_charts && (
              <div className="bg-amber-900/20 border border-amber-600/20 rounded-xl p-6">
                <h3 className="text-lg font-semibold text-amber-200 mb-3">
                  {(accuracyAudit as any).divisional_charts.length} Divisional Charts
                </h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-sm">
                  {(accuracyAudit as any).divisional_charts.map((d: any, i: number) => (
                    <div key={i} className="bg-black/20 rounded px-3 py-2">
                      <span className="text-amber-300 font-mono">{d.chart}</span>
                      <span className="text-gray-500 ml-2 text-xs">{d.name}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* CTA */}
            <div className="text-center pt-4">
              <Link
                to="/kundli"
                className="inline-flex items-center gap-2 bg-amber-600 hover:bg-amber-500 text-white font-semibold px-8 py-3 rounded-xl transition-colors"
              >
                Generate Your Kundli <ExternalLink className="w-4 h-4" />
              </Link>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
