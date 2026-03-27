import { useEffect, useState, useCallback } from 'react';
import { api } from '@/lib/api';
import {
  MessageSquare,
  Heart,
  Eye,
  Pin,
  Lock,
  Award,
  Search,
  ArrowLeft,
  Plus,
  X,
  Loader2,
  ChevronLeft,
  ChevronRight,
  Send,
} from 'lucide-react';

/* ------------------------------------------------------------------ */
/*  Types                                                              */
/* ------------------------------------------------------------------ */
interface ForumCategory {
  id: string;
  name: string;
  description: string | null;
  icon: string | null;
  order_index: number;
  is_active: boolean;
  thread_count: number;
}

interface ThreadResponse {
  id: string;
  category_id: string;
  user_id: string;
  title: string;
  content: string;
  is_pinned: boolean;
  is_locked: boolean;
  views_count: number;
  replies_count: number;
  created_at: string;
  updated_at: string;
  author_name: string | null;
  author_avatar: string | null;
  category_name: string | null;
}

interface ReplyResponse {
  id: string;
  thread_id: string;
  user_id: string;
  content: string;
  is_best_answer: boolean;
  likes_count: number;
  created_at: string;
  updated_at: string;
  author_name: string | null;
  author_avatar: string | null;
  liked_by_me: boolean;
}

type View = 'categories' | 'threads' | 'thread';

/* ------------------------------------------------------------------ */
/*  Helpers                                                            */
/* ------------------------------------------------------------------ */
function timeAgo(dateStr: string): string {
  const diff = Date.now() - new Date(dateStr + 'Z').getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return 'just now';
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  const days = Math.floor(hrs / 24);
  if (days < 30) return `${days}d ago`;
  return new Date(dateStr).toLocaleDateString();
}

function isLoggedIn(): boolean {
  return !!localStorage.getItem('astrovedic_token');
}

function currentUserId(): string | null {
  try {
    const raw = localStorage.getItem('astrovedic_user');
    if (!raw) return null;
    return JSON.parse(raw)?.id ?? null;
  } catch {
    return null;
  }
}

/* ------------------------------------------------------------------ */
/*  Component                                                          */
/* ------------------------------------------------------------------ */
export default function CommunityPage() {
  const [view, setView] = useState<View>('categories');
  const [categories, setCategories] = useState<ForumCategory[]>([]);
  const [threads, setThreads] = useState<ThreadResponse[]>([]);
  const [threadTotal, setThreadTotal] = useState(0);
  const [threadPage, setThreadPage] = useState(1);
  const [selectedCategory, setSelectedCategory] = useState<ForumCategory | null>(null);
  const [selectedThread, setSelectedThread] = useState<ThreadResponse | null>(null);
  const [replies, setReplies] = useState<ReplyResponse[]>([]);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchMode, setSearchMode] = useState(false);

  // New thread form
  const [showNewThread, setShowNewThread] = useState(false);
  const [newTitle, setNewTitle] = useState('');
  const [newContent, setNewContent] = useState('');
  const [creating, setCreating] = useState(false);

  // Reply form
  const [replyContent, setReplyContent] = useState('');
  const [replying, setReplying] = useState(false);

  const perPage = 20;

  /* ---------- data fetchers ---------- */
  const fetchCategories = useCallback(async () => {
    setLoading(true);
    try {
      const data = await api.get('/api/forum/categories');
      setCategories(data);
    } catch {
      /* ignore */
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchThreads = useCallback(
    async (categoryId: string | null, page: number) => {
      setLoading(true);
      try {
        const qs = categoryId
          ? `/api/forum/threads?category_id=${categoryId}&page=${page}&per_page=${perPage}`
          : `/api/forum/threads?page=${page}&per_page=${perPage}`;
        const data = await api.get(qs);
        setThreads(data.threads);
        setThreadTotal(data.total);
        setThreadPage(page);
      } catch {
        /* ignore */
      } finally {
        setLoading(false);
      }
    },
    [],
  );

  const fetchThread = useCallback(async (threadId: string) => {
    setLoading(true);
    try {
      const data = await api.get(`/api/forum/thread/${threadId}`);
      setSelectedThread(data.thread);
      setReplies(data.replies);
    } catch {
      /* ignore */
    } finally {
      setLoading(false);
    }
  }, []);

  const doSearch = useCallback(
    async (q: string, page: number) => {
      if (q.length < 2) return;
      setLoading(true);
      try {
        const data = await api.get(
          `/api/forum/search?q=${encodeURIComponent(q)}&page=${page}&per_page=${perPage}`,
        );
        setThreads(data.threads);
        setThreadTotal(data.total);
        setThreadPage(page);
      } catch {
        /* ignore */
      } finally {
        setLoading(false);
      }
    },
    [],
  );

  /* ---------- initial load ---------- */
  useEffect(() => {
    fetchCategories();
  }, [fetchCategories]);

  /* ---------- navigation helpers ---------- */
  const openCategory = (cat: ForumCategory) => {
    setSelectedCategory(cat);
    setView('threads');
    setSearchMode(false);
    setSearchQuery('');
    fetchThreads(cat.id, 1);
  };

  const openThread = (t: ThreadResponse) => {
    setView('thread');
    fetchThread(t.id);
  };

  const goBackToCategories = () => {
    setView('categories');
    setSelectedCategory(null);
    setSelectedThread(null);
    setReplies([]);
    setSearchMode(false);
    setSearchQuery('');
    fetchCategories();
  };

  const goBackToThreads = () => {
    setView('threads');
    setSelectedThread(null);
    setReplies([]);
    if (searchMode) {
      doSearch(searchQuery, threadPage);
    } else if (selectedCategory) {
      fetchThreads(selectedCategory.id, threadPage);
    }
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim().length < 2) return;
    setSearchMode(true);
    setSelectedCategory(null);
    setView('threads');
    doSearch(searchQuery.trim(), 1);
  };

  /* ---------- create thread ---------- */
  const handleCreateThread = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedCategory || !newTitle.trim() || !newContent.trim()) return;
    setCreating(true);
    try {
      await api.post('/api/forum/thread', {
        category_id: selectedCategory.id,
        title: newTitle.trim(),
        content: newContent.trim(),
      });
      setShowNewThread(false);
      setNewTitle('');
      setNewContent('');
      fetchThreads(selectedCategory.id, 1);
    } catch {
      /* ignore */
    } finally {
      setCreating(false);
    }
  };

  /* ---------- reply ---------- */
  const handleReply = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedThread || !replyContent.trim()) return;
    setReplying(true);
    try {
      await api.post(`/api/forum/thread/${selectedThread.id}/reply`, {
        content: replyContent.trim(),
      });
      setReplyContent('');
      fetchThread(selectedThread.id);
    } catch {
      /* ignore */
    } finally {
      setReplying(false);
    }
  };

  /* ---------- like ---------- */
  const handleLike = async (replyId: string) => {
    if (!isLoggedIn()) return;
    try {
      await api.post(`/api/forum/reply/${replyId}/like`, {});
      if (selectedThread) fetchThread(selectedThread.id);
    } catch {
      /* ignore */
    }
  };

  /* ---------- best answer ---------- */
  const handleBestAnswer = async (replyId: string) => {
    if (!isLoggedIn() || !selectedThread) return;
    try {
      await api.post(`/api/forum/reply/${replyId}/best-answer`, {});
      fetchThread(selectedThread.id);
    } catch {
      /* ignore */
    }
  };

  /* ---------- pagination ---------- */
  const totalPages = Math.ceil(threadTotal / perPage);

  const changePage = (p: number) => {
    if (searchMode) {
      doSearch(searchQuery, p);
    } else {
      fetchThreads(selectedCategory?.id ?? null, p);
    }
  };

  /* ================================================================ */
  /*  RENDER                                                           */
  /* ================================================================ */
  return (
    <section className="min-h-screen bg-cosmic-bg pt-24 pb-16 px-4">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="text-center mb-10">
          <h1 className="text-4xl md:text-5xl font-sacred text-sacred-gold mb-3">
            Community Forums
          </h1>
          <p className="text-cosmic-text-secondary max-w-2xl mx-auto">
            Join the discussion — share insights, ask questions, and connect with fellow seekers on
            their spiritual journey.
          </p>
        </div>

        {/* Search Bar */}
        <form onSubmit={handleSearch} className="mb-8 flex gap-2 max-w-xl mx-auto">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-cosmic-text-secondary" />
            <input
              type="text"
              placeholder="Search threads..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2.5 rounded-lg bg-cosmic-bg border border-sacred-gold/20 text-cosmic-text placeholder:text-cosmic-text-secondary/50 focus:outline-none focus:border-sacred-gold/50 font-sacred"
            />
          </div>
          <button
            type="submit"
            className="btn-sacred px-5 py-2.5 rounded-lg font-sacred text-sm"
          >
            Search
          </button>
        </form>

        {/* Loading */}
        {loading && (
          <div className="flex justify-center py-12">
            <Loader2 className="w-8 h-8 text-sacred-gold animate-spin" />
          </div>
        )}

        {/* =================== CATEGORIES VIEW =================== */}
        {!loading && view === 'categories' && (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {categories.map((cat) => (
              <button
                key={cat.id}
                onClick={() => openCategory(cat)}
                className="card-sacred border border-sacred-gold/20 rounded-xl p-5 text-left hover:border-sacred-gold/40 transition-all group"
              >
                <div className="text-3xl mb-3">{cat.icon || '💬'}</div>
                <h3 className="font-sacred text-sacred-gold text-lg mb-1 group-hover:text-sacred-gold/80">
                  {cat.name}
                </h3>
                <p className="text-cosmic-text-secondary text-sm mb-3 line-clamp-2">
                  {cat.description}
                </p>
                <div className="flex items-center gap-1 text-xs text-cosmic-text-secondary">
                  <MessageSquare className="w-3.5 h-3.5" />
                  <span>{cat.thread_count} threads</span>
                </div>
              </button>
            ))}
          </div>
        )}

        {/* =================== THREADS VIEW =================== */}
        {!loading && view === 'threads' && (
          <div>
            {/* Breadcrumb */}
            <div className="flex items-center justify-between mb-6 flex-wrap gap-3">
              <button
                onClick={goBackToCategories}
                className="flex items-center gap-1 text-sacred-gold hover:text-sacred-gold/80 text-sm font-sacred"
              >
                <ArrowLeft className="w-4 h-4" />
                All Categories
              </button>
              <div className="flex items-center gap-3">
                {searchMode && (
                  <span className="text-cosmic-text-secondary text-sm">
                    Results for &ldquo;{searchQuery}&rdquo; ({threadTotal})
                  </span>
                )}
                {!searchMode && selectedCategory && (
                  <span className="text-cosmic-text-secondary text-sm font-sacred">
                    {selectedCategory.icon} {selectedCategory.name}
                  </span>
                )}
                {isLoggedIn() && selectedCategory && (
                  <button
                    onClick={() => setShowNewThread(true)}
                    className="btn-sacred px-4 py-2 rounded-lg font-sacred text-sm flex items-center gap-1"
                  >
                    <Plus className="w-4 h-4" /> New Thread
                  </button>
                )}
              </div>
            </div>

            {/* New Thread Modal */}
            {showNewThread && (
              <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 px-4">
                <div className="card-sacred border border-sacred-gold/20 rounded-xl p-6 w-full max-w-lg relative">
                  <button
                    onClick={() => setShowNewThread(false)}
                    className="absolute top-3 right-3 text-cosmic-text-secondary hover:text-cosmic-text"
                  >
                    <X className="w-5 h-5" />
                  </button>
                  <h2 className="font-sacred text-sacred-gold text-xl mb-4">Create New Thread</h2>
                  <form onSubmit={handleCreateThread} className="space-y-4">
                    <div>
                      <label className="block text-cosmic-text-secondary text-sm mb-1 font-sacred">
                        Title
                      </label>
                      <input
                        type="text"
                        value={newTitle}
                        onChange={(e) => setNewTitle(e.target.value)}
                        className="w-full px-4 py-2.5 rounded-lg bg-cosmic-bg border border-sacred-gold/20 text-cosmic-text placeholder:text-cosmic-text-secondary/50 focus:outline-none focus:border-sacred-gold/50 font-sacred"
                        placeholder="Thread title..."
                        required
                        minLength={3}
                      />
                    </div>
                    <div>
                      <label className="block text-cosmic-text-secondary text-sm mb-1 font-sacred">
                        Content
                      </label>
                      <textarea
                        value={newContent}
                        onChange={(e) => setNewContent(e.target.value)}
                        rows={5}
                        className="w-full px-4 py-2.5 rounded-lg bg-cosmic-bg border border-sacred-gold/20 text-cosmic-text placeholder:text-cosmic-text-secondary/50 focus:outline-none focus:border-sacred-gold/50 font-sacred resize-none"
                        placeholder="What's on your mind?"
                        required
                        minLength={10}
                      />
                    </div>
                    <div className="flex justify-end gap-3">
                      <button
                        type="button"
                        onClick={() => setShowNewThread(false)}
                        className="px-4 py-2 rounded-lg border border-sacred-gold/20 text-cosmic-text-secondary hover:text-cosmic-text font-sacred text-sm"
                      >
                        Cancel
                      </button>
                      <button
                        type="submit"
                        disabled={creating}
                        className="btn-sacred px-5 py-2 rounded-lg font-sacred text-sm flex items-center gap-1 disabled:opacity-50"
                      >
                        {creating && <Loader2 className="w-4 h-4 animate-spin" />}
                        Post Thread
                      </button>
                    </div>
                  </form>
                </div>
              </div>
            )}

            {/* Thread List */}
            {threads.length === 0 ? (
              <div className="text-center py-16 text-cosmic-text-secondary">
                <MessageSquare className="w-12 h-12 mx-auto mb-3 opacity-40" />
                <p className="font-sacred">No threads yet. Be the first to start a discussion!</p>
              </div>
            ) : (
              <div className="space-y-3">
                {threads.map((t) => (
                  <button
                    key={t.id}
                    onClick={() => openThread(t)}
                    className="card-sacred border border-sacred-gold/20 rounded-xl p-4 w-full text-left hover:border-sacred-gold/40 transition-all flex gap-4"
                  >
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 flex-wrap mb-1">
                        {t.is_pinned && (
                          <Pin className="w-3.5 h-3.5 text-sacred-gold flex-shrink-0" />
                        )}
                        {t.is_locked && (
                          <Lock className="w-3.5 h-3.5 text-cosmic-text-secondary flex-shrink-0" />
                        )}
                        <h3 className="font-sacred text-cosmic-text text-base truncate">
                          {t.title}
                        </h3>
                      </div>
                      <p className="text-cosmic-text-secondary text-sm line-clamp-1 mb-2">
                        {t.content}
                      </p>
                      <div className="flex items-center gap-4 text-xs text-cosmic-text-secondary">
                        <span>{t.author_name || 'Anonymous'}</span>
                        {t.category_name && (
                          <span className="text-sacred-gold/70">{t.category_name}</span>
                        )}
                        <span>{timeAgo(t.created_at)}</span>
                      </div>
                    </div>
                    <div className="flex flex-col items-end gap-1 text-xs text-cosmic-text-secondary flex-shrink-0">
                      <span className="flex items-center gap-1">
                        <MessageSquare className="w-3.5 h-3.5" /> {t.replies_count}
                      </span>
                      <span className="flex items-center gap-1">
                        <Eye className="w-3.5 h-3.5" /> {t.views_count}
                      </span>
                    </div>
                  </button>
                ))}
              </div>
            )}

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="flex justify-center items-center gap-2 mt-8">
                <button
                  onClick={() => changePage(threadPage - 1)}
                  disabled={threadPage <= 1}
                  className="p-2 rounded-lg border border-sacred-gold/20 text-cosmic-text-secondary hover:text-cosmic-text disabled:opacity-30"
                >
                  <ChevronLeft className="w-4 h-4" />
                </button>
                <span className="text-sm text-cosmic-text-secondary font-sacred">
                  Page {threadPage} of {totalPages}
                </span>
                <button
                  onClick={() => changePage(threadPage + 1)}
                  disabled={threadPage >= totalPages}
                  className="p-2 rounded-lg border border-sacred-gold/20 text-cosmic-text-secondary hover:text-cosmic-text disabled:opacity-30"
                >
                  <ChevronRight className="w-4 h-4" />
                </button>
              </div>
            )}
          </div>
        )}

        {/* =================== THREAD DETAIL VIEW =================== */}
        {!loading && view === 'thread' && selectedThread && (
          <div>
            {/* Breadcrumb */}
            <button
              onClick={goBackToThreads}
              className="flex items-center gap-1 text-sacred-gold hover:text-sacred-gold/80 text-sm font-sacred mb-6"
            >
              <ArrowLeft className="w-4 h-4" />
              Back to threads
            </button>

            {/* Original Post */}
            <div className="card-sacred border border-sacred-gold/20 rounded-xl p-6 mb-6">
              <div className="flex items-center gap-2 mb-1 flex-wrap">
                {selectedThread.is_pinned && (
                  <Pin className="w-4 h-4 text-sacred-gold" />
                )}
                {selectedThread.is_locked && (
                  <Lock className="w-4 h-4 text-cosmic-text-secondary" />
                )}
                <h2 className="font-sacred text-sacred-gold text-2xl">{selectedThread.title}</h2>
              </div>
              <div className="flex items-center gap-3 text-xs text-cosmic-text-secondary mb-4">
                <span className="font-sacred">{selectedThread.author_name || 'Anonymous'}</span>
                <span>{timeAgo(selectedThread.created_at)}</span>
                {selectedThread.category_name && (
                  <span className="text-sacred-gold/70">{selectedThread.category_name}</span>
                )}
                <span className="flex items-center gap-1">
                  <Eye className="w-3 h-3" /> {selectedThread.views_count}
                </span>
              </div>
              <div className="text-cosmic-text whitespace-pre-wrap leading-relaxed">
                {selectedThread.content}
              </div>
            </div>

            {/* Replies */}
            <h3 className="font-sacred text-cosmic-text-secondary text-sm mb-4">
              {replies.length} {replies.length === 1 ? 'Reply' : 'Replies'}
            </h3>

            {replies.length > 0 && (
              <div className="space-y-3 mb-6">
                {replies.map((r) => (
                  <div
                    key={r.id}
                    className={`card-sacred border rounded-xl p-4 ${
                      r.is_best_answer
                        ? 'border-green-500/40 bg-green-500/5'
                        : 'border-sacred-gold/20'
                    }`}
                  >
                    {r.is_best_answer && (
                      <div className="flex items-center gap-1 text-green-400 text-xs font-sacred mb-2">
                        <Award className="w-4 h-4" /> Best Answer
                      </div>
                    )}
                    <div className="text-cosmic-text whitespace-pre-wrap leading-relaxed mb-3">
                      {r.content}
                    </div>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3 text-xs text-cosmic-text-secondary">
                        <span className="font-sacred">{r.author_name || 'Anonymous'}</span>
                        <span>{timeAgo(r.created_at)}</span>
                      </div>
                      <div className="flex items-center gap-3">
                        {/* Like button */}
                        <button
                          onClick={() => handleLike(r.id)}
                          disabled={!isLoggedIn()}
                          className="flex items-center gap-1 text-xs text-cosmic-text-secondary hover:text-red-400 transition-colors disabled:opacity-40"
                        >
                          <Heart
                            className={`w-4 h-4 ${r.likes_count > 0 ? 'fill-red-400 text-red-400' : ''}`}
                          />
                          {r.likes_count > 0 && <span>{r.likes_count}</span>}
                        </button>
                        {/* Best answer toggle (thread owner only) */}
                        {isLoggedIn() &&
                          selectedThread.user_id === currentUserId() && (
                            <button
                              onClick={() => handleBestAnswer(r.id)}
                              className={`flex items-center gap-1 text-xs transition-colors ${
                                r.is_best_answer
                                  ? 'text-green-400'
                                  : 'text-cosmic-text-secondary hover:text-green-400'
                              }`}
                              title="Mark as best answer"
                            >
                              <Award className="w-4 h-4" />
                            </button>
                          )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Reply Form */}
            {isLoggedIn() && !selectedThread.is_locked ? (
              <form
                onSubmit={handleReply}
                className="card-sacred border border-sacred-gold/20 rounded-xl p-4"
              >
                <textarea
                  value={replyContent}
                  onChange={(e) => setReplyContent(e.target.value)}
                  rows={3}
                  className="w-full px-4 py-2.5 rounded-lg bg-cosmic-bg border border-sacred-gold/20 text-cosmic-text placeholder:text-cosmic-text-secondary/50 focus:outline-none focus:border-sacred-gold/50 font-sacred resize-none mb-3"
                  placeholder="Write your reply..."
                  required
                />
                <div className="flex justify-end">
                  <button
                    type="submit"
                    disabled={replying || !replyContent.trim()}
                    className="btn-sacred px-5 py-2 rounded-lg font-sacred text-sm flex items-center gap-1 disabled:opacity-50"
                  >
                    {replying ? (
                      <Loader2 className="w-4 h-4 animate-spin" />
                    ) : (
                      <Send className="w-4 h-4" />
                    )}
                    Reply
                  </button>
                </div>
              </form>
            ) : selectedThread.is_locked ? (
              <div className="text-center py-6 text-cosmic-text-secondary text-sm font-sacred">
                <Lock className="w-5 h-5 mx-auto mb-2 opacity-50" />
                This thread is locked.
              </div>
            ) : (
              <div className="text-center py-6 text-cosmic-text-secondary text-sm font-sacred">
                <a href="/login" className="text-sacred-gold hover:text-sacred-gold/80 underline">
                  Sign in
                </a>{' '}
                to join the discussion.
              </div>
            )}
          </div>
        )}
      </div>
    </section>
  );
}
