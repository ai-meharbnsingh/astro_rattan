import { useState, useRef, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, X, Loader2, ShoppingBag, BookOpen, User, FileText } from 'lucide-react';
import { api } from '@/lib/api';

interface SearchResult {
  type: string;
  id: string;
  title: string;
  snippet: string;
  score: number;
}

const TYPE_META: Record<string, { label: string; icon: React.ElementType; route: (id: string) => string }> = {
  product: { label: 'Products', icon: ShoppingBag, route: () => '/shop' },
  content: { label: 'Library', icon: BookOpen, route: () => '/library' },
  astrologer: { label: 'Astrologers', icon: User, route: () => '/consultation' },
};

export default function SearchBar() {
  const navigate = useNavigate();
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Close on outside click
  useEffect(() => {
    const handleClick = (e: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, []);

  const doSearch = useCallback(async (q: string) => {
    if (q.trim().length === 0) {
      setResults([]);
      setOpen(false);
      return;
    }
    setLoading(true);
    try {
      const data = await api.get(`/api/search?q=${encodeURIComponent(q.trim())}`);
      setResults(data.results || []);
      setOpen(true);
    } catch {
      setResults([]);
    }
    setLoading(false);
  }, []);

  const handleChange = (value: string) => {
    setQuery(value);
    if (debounceRef.current) clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(() => doSearch(value), 350);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (debounceRef.current) clearTimeout(debounceRef.current);
    doSearch(query);
  };

  const handleResultClick = (result: SearchResult) => {
    setOpen(false);
    setQuery('');
    const meta = TYPE_META[result.type];
    if (meta) {
      navigate(meta.route(result.id));
    }
  };

  const handleClear = () => {
    setQuery('');
    setResults([]);
    setOpen(false);
  };

  // Group results by type
  const grouped = results.reduce<Record<string, SearchResult[]>>((acc, r) => {
    if (!acc[r.type]) acc[r.type] = [];
    acc[r.type].push(r);
    return acc;
  }, {});

  return (
    <div ref={containerRef} className="relative">
      <form onSubmit={handleSubmit} className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-sacred-gold/60" />
        <input
          type="text"
          value={query}
          onChange={(e) => handleChange(e.target.value)}
          onFocus={() => { if (results.length > 0) setOpen(true); }}
          placeholder="Search..."
          className="w-36 lg:w-48 pl-9 pr-8 py-2 text-sm rounded-full bg-cosmic-card border border-sacred-gold/20 text-cosmic-text placeholder:text-cosmic-text/40 focus:outline-none focus:border-sacred-gold/50 transition-all"
        />
        {query && (
          <button type="button" onClick={handleClear} className="absolute right-3 top-1/2 -translate-y-1/2">
            {loading ? (
              <Loader2 className="w-3.5 h-3.5 animate-spin text-sacred-gold/60" />
            ) : (
              <X className="w-3.5 h-3.5 text-cosmic-text/40 hover:text-cosmic-text" />
            )}
          </button>
        )}
      </form>

      {/* Dropdown */}
      {open && results.length > 0 && (
        <div className="absolute right-0 top-full mt-2 w-80 max-h-96 overflow-y-auto rounded-xl bg-cosmic-card border border-sacred-gold/20 shadow-2xl z-50">
          {Object.entries(grouped).map(([type, items]) => {
            const meta = TYPE_META[type] || { label: type, icon: FileText, route: () => '/' };
            const Icon = meta.icon;
            return (
              <div key={type}>
                <div className="px-4 py-2 text-xs font-semibold uppercase tracking-wider text-sacred-gold/60 border-b border-sacred-gold/10 flex items-center gap-2">
                  <Icon className="w-3.5 h-3.5" />
                  {meta.label}
                </div>
                {items.map((r) => (
                  <button
                    key={`${r.type}-${r.id}`}
                    onClick={() => handleResultClick(r)}
                    className="w-full text-left px-4 py-3 hover:bg-sacred-gold/10 transition-colors border-b border-sacred-gold/5 last:border-0"
                  >
                    <p className="text-sm font-medium text-cosmic-text truncate">{r.title}</p>
                    {r.snippet && (
                      <p className="text-xs text-cosmic-text/50 truncate mt-0.5">{r.snippet}</p>
                    )}
                  </button>
                ))}
              </div>
            );
          })}
        </div>
      )}

      {open && query.trim().length > 0 && results.length === 0 && !loading && (
        <div className="absolute right-0 top-full mt-2 w-80 rounded-xl bg-cosmic-card border border-sacred-gold/20 shadow-2xl z-50 p-6 text-center">
          <p className="text-sm text-cosmic-text/50">No results found for &ldquo;{query}&rdquo;</p>
        </div>
      )}
    </div>
  );
}
