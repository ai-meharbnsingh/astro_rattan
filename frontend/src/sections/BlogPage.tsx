import { useEffect, useMemo, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Loader2, ArrowLeft, CalendarDays, UserRound, BookOpenText } from 'lucide-react';
import { api, resolveApiUrl } from '@/lib/api';

interface BlogPostSummary { id: string; slug: string; title: string; excerpt: string; cover_image_url?: string | null; tags: string[]; author_name: string; seo_title?: string | null; seo_description?: string | null; published_at: string; }
interface BlogPost extends BlogPostSummary { content: string; }

const DEFAULT_TITLE = 'Astro Rattan Blog - Practical Astrology, Panchang, Remedies';
const DEFAULT_DESCRIPTION = 'Editorial guides on Panchang, Kundli, remedies, spiritual practices, and practical astrology decisions.';

function updateHead(post?: BlogPost | null) {
  const previousTitle = document.title;
  const previousCanonical = document.querySelector<HTMLLinkElement>('link[rel="canonical"]')?.href || '';
  const previousDescription = document.querySelector<HTMLMetaElement>('meta[name="description"]')?.content || '';
  const previousOgTitle = document.querySelector<HTMLMetaElement>('meta[property="og:title"]')?.content || '';
  const previousOgDescription = document.querySelector<HTMLMetaElement>('meta[property="og:description"]')?.content || '';
  const previousOgUrl = document.querySelector<HTMLMetaElement>('meta[property="og:url"]')?.content || '';
  const previousTwitterTitle = document.querySelector<HTMLMetaElement>('meta[name="twitter:title"]')?.content || '';
  const previousTwitterDescription = document.querySelector<HTMLMetaElement>('meta[name="twitter:description"]')?.content || '';

  const setMeta = (selector: string, value: string) => {
    const node = document.querySelector<HTMLMetaElement | HTMLLinkElement>(selector);
    if (!node) return;
    if (node instanceof HTMLLinkElement) node.href = value;
    else node.content = value;
  };

  const url = post ? `${window.location.origin}/blog/${post.slug}` : `${window.location.origin}/blog`;
  const title = post?.seo_title || post?.title || DEFAULT_TITLE;
  const description = post?.seo_description || post?.excerpt || DEFAULT_DESCRIPTION;

  document.title = title;
  setMeta('link[rel="canonical"]', url);
  setMeta('meta[name="description"]', description);
  setMeta('meta[property="og:title"]', title);
  setMeta('meta[property="og:description"]', description);
  setMeta('meta[property="og:url"]', url);
  setMeta('meta[name="twitter:title"]', title);
  setMeta('meta[name="twitter:description"]', description);

  let script = document.getElementById('blog-jsonld') as HTMLScriptElement | null;
  if (script) script.remove();
  script = document.createElement('script');
  script.id = 'blog-jsonld';
  script.type = 'application/ld+json';
  script.text = JSON.stringify(
    post ? { '@context': 'https://schema.org', '@type': 'BlogPosting', headline: post.title, description, datePublished: post.published_at, dateModified: post.published_at, author: { '@type': 'Person', name: post.author_name }, mainEntityOfPage: url, publisher: { '@type': 'Organization', name: 'Astro Rattan' } }
      : { '@context': 'https://schema.org', '@type': 'Blog', name: 'Astro Rattan Blog', description: DEFAULT_DESCRIPTION, url }
  );
  document.head.appendChild(script);

  return () => {
    document.title = previousTitle;
    setMeta('link[rel="canonical"]', previousCanonical);
    setMeta('meta[name="description"]', previousDescription);
    setMeta('meta[property="og:title"]', previousOgTitle);
    setMeta('meta[property="og:description"]', previousOgDescription);
    setMeta('meta[property="og:url"]', previousOgUrl);
    setMeta('meta[name="twitter:title"]', previousTwitterTitle);
    setMeta('meta[name="twitter:description"]', previousTwitterDescription);
    document.getElementById('blog-jsonld')?.remove();
  };
}

export default function BlogPage() {
  const { slug } = useParams();
  const [posts, setPosts] = useState<BlogPostSummary[]>([]);
  const [post, setPost] = useState<BlogPost | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let cancelled = false;
    const load = async () => {
      setLoading(true); setError('');
      try {
        if (slug) { const data = await api.get(`/api/blog/posts/${slug}`); if (!cancelled) setPost(data); }
        else { const data = await api.get('/api/blog/posts'); const items = Array.isArray(data) ? data : data.items || []; if (!cancelled) setPosts(items); }
      } catch (err) { if (!cancelled) setError(err instanceof Error ? err.message : 'Failed to load blog content'); }
      finally { if (!cancelled) setLoading(false); }
    };
    load();
    return () => { cancelled = true; };
  }, [slug]);

  useEffect(() => updateHead(post), [post]);

  const featuredPost = useMemo(() => posts[0], [posts]);
  const remainingPosts = useMemo(() => posts.slice(1), [posts]);

  if (loading) return <div className="flex items-center justify-center py-32"><Loader2 className="w-10 h-10 text-sacred-gold animate-spin" /></div>;

  if (error) {
    return (
      <section className="max-w-5xl mx-auto py-24 px-4 text-center">
        <BookOpenText className="w-12 h-12 text-cosmic-text-muted mx-auto mb-4" />
        <h2 className="text-2xl font-sacred font-bold text-cosmic-text mb-2">Blog unavailable</h2>
        <p className="text-cosmic-text-secondary mb-6">{error}</p>
        <Button asChild variant="outline" className="border-sacred-gold/30 text-cosmic-text hover:bg-sacred-gold/10"><Link to="/">Return Home</Link></Button>
      </section>
    );
  }

  if (slug && post) {
    return (
      <section className="max-w-4xl mx-auto py-16 px-4 sm:px-6 lg:px-8">
        <Button asChild variant="ghost" className="mb-6 text-cosmic-text-secondary hover:text-sacred-gold">
          <Link to="/blog"><ArrowLeft className="w-4 h-4 mr-2" />Back to Blog</Link>
        </Button>
        {post.cover_image_url && (
          <img src={resolveApiUrl(post.cover_image_url)} alt={post.title} className="w-full max-h-[420px] object-cover rounded-3xl border border-sacred-gold/20 mb-8" />
        )}
        <div className="mb-6">
          <div className="flex flex-wrap gap-2 mb-4">
            {post.tags.map((tag) => <Badge key={tag} className="bg-sacred-gold/10 text-sacred-gold border border-sacred-gold/20">{tag}</Badge>)}
          </div>
          <h1 className="text-3xl sm:text-4xl font-sacred font-bold text-cosmic-text mb-4">{post.title}</h1>
          <div className="flex flex-wrap gap-4 text-sm text-cosmic-text-secondary">
            <span className="inline-flex items-center gap-2"><UserRound className="w-4 h-4" />{post.author_name}</span>
            <span className="inline-flex items-center gap-2"><CalendarDays className="w-4 h-4" />{new Date(post.published_at).toLocaleDateString('en-IN')}</span>
          </div>
        </div>
        <article>
          {post.content.split(/\n\s*\n/).map((paragraph, index) => (
            <p key={`${post.id}-${index}`} className="text-cosmic-text-secondary leading-8 mb-5 whitespace-pre-line">{paragraph}</p>
          ))}
        </article>
      </section>
    );
  }

  return (
    <section className="max-w-6xl mx-auto py-16 px-4 sm:px-6 lg:px-8">
      <div className="text-center mb-12">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-sacred-gold/10 text-sacred-gold text-sm font-medium mb-4 border border-sacred-gold/30">
          <BookOpenText className="w-4 h-4" />Editorial
        </div>
        <h1 className="text-3xl sm:text-4xl font-sacred font-bold text-cosmic-text mb-3">
          Astro Rattan <span className="text-gradient-gold">Blog</span>
        </h1>
        <p className="text-cosmic-text-secondary max-w-2xl mx-auto">
          Practical astrology guides for Panchang timing, Kundli decisions, remedies, and spiritual routines.
        </p>
      </div>
      {featuredPost && (
        <Card className="card-sacred border-sacred-gold/20 overflow-hidden mb-8">
          <div className="grid lg:grid-cols-[1.15fr_0.85fr]">
            <div className="p-8">
              <Badge className="bg-sacred-gold/10 text-sacred-gold border border-sacred-gold/20 mb-4">Featured</Badge>
              <h2 className="text-2xl font-sacred font-bold text-cosmic-text mb-3">{featuredPost.title}</h2>
              <p className="text-cosmic-text-secondary mb-5">{featuredPost.excerpt}</p>
              <div className="flex flex-wrap gap-2 mb-6">
                {featuredPost.tags.map((tag) => <Badge key={tag} variant="outline" className="border-sacred-gold/20 text-cosmic-text-secondary">{tag}</Badge>)}
              </div>
              <Button asChild className="btn-sacred"><Link to={`/blog/${featuredPost.slug}`}>Read Article</Link></Button>
            </div>
            <div className="bg-cosmic-card flex items-center justify-center p-8 border-l border-sacred-gold/10">
              {featuredPost.cover_image_url ? (
                <img src={resolveApiUrl(featuredPost.cover_image_url)} alt={featuredPost.title} className="w-full h-full max-h-80 object-cover rounded-3xl border border-sacred-gold/20" />
              ) : (
                <div className="w-full h-full min-h-64 rounded-3xl bg-gradient-to-br from-sacred-purple/20 to-sacred-gold/10 border border-sacred-gold/15 flex items-center justify-center">
                  <BookOpenText className="w-14 h-14 text-sacred-gold/40" />
                </div>
              )}
            </div>
          </div>
        </Card>
      )}
      <div className="grid md:grid-cols-2 gap-6">
        {remainingPosts.map((item) => (
          <Card key={item.id} className="card-sacred border-sacred-gold/15 hover:border-sacred-gold/30">
            <CardContent className="p-6">
              <div className="flex flex-wrap gap-2 mb-3">
                {item.tags.map((tag) => <Badge key={tag} className="bg-cosmic-card text-cosmic-text-secondary border border-sacred-gold/10">{tag}</Badge>)}
              </div>
              <h3 className="text-xl font-sacred font-semibold text-cosmic-text mb-2">{item.title}</h3>
              <p className="text-cosmic-text-secondary mb-5">{item.excerpt}</p>
              <div className="flex items-center justify-between gap-4">
                <span className="text-sm text-cosmic-text-muted">{new Date(item.published_at).toLocaleDateString('en-IN')}</span>
                <Button asChild variant="outline" className="border-sacred-gold/30 text-cosmic-text hover:bg-sacred-gold/10 hover:text-sacred-gold">
                  <Link to={`/blog/${item.slug}`}>Read More</Link>
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </section>
  );
}
