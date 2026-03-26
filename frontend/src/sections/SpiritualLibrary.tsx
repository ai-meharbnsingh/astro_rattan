import { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { BookOpen, Music, Flame, ChevronRight, Play, Sparkles, Loader2 } from 'lucide-react';
import { api } from '@/lib/api';

gsap.registerPlugin(ScrollTrigger);

interface GitaChapter {
  chapter: number;
  title: string;
  verses: number;
  description: string;
}

interface LibraryItem {
  id?: number;
  name: string;
  deity?: string;
  benefit?: string;
  category?: string;
  content?: string;
}

const normalizeGitaChapters = (chapters: any[]): GitaChapter[] =>
  chapters.map((chapter) => ({
    chapter: chapter.chapter,
    title: chapter.title || `Chapter ${chapter.chapter}`,
    verses: chapter.verses_count ?? chapter.verses ?? 0,
    description: chapter.summary || chapter.description || '',
  }));

const normalizeLibraryItems = (items: any[], category: string): LibraryItem[] =>
  items.map((item) => ({
    id: item.id,
    name: item.title || item.name || '',
    deity: item.title_hindi || item.deity || category.replace(/_/g, ' '),
    benefit: item.content_preview || item.benefit || '',
    category: item.category || category,
    content: item.content_preview || item.content || '',
  }));

const fallbackGita: GitaChapter[] = [
  { chapter: 1, title: 'Chapter 1: Arjuna\'s Dilemma', verses: 47, description: 'Arjuna faces moral confusion on the battlefield.' },
  { chapter: 2, title: 'Chapter 2: Sankhya Yoga', verses: 72, description: 'The eternal nature of the soul and duty.' },
  { chapter: 3, title: 'Chapter 3: Karma Yoga', verses: 43, description: 'The path of selfless action.' },
  { chapter: 4, title: 'Chapter 4: Jnana Yoga', verses: 42, description: 'Divine knowledge and wisdom.' },
];

const fallbackMantras: LibraryItem[] = [
  { name: 'Gayatri Mantra', deity: 'Goddess Gayatri', benefit: 'Wisdom' },
  { name: 'Mahamrityunjaya', deity: 'Lord Shiva', benefit: 'Health' },
  { name: 'Hanuman Chalisa', deity: 'Lord Hanuman', benefit: 'Strength' },
  { name: 'Vishnu Sahasranama', deity: 'Lord Vishnu', benefit: 'Peace' },
];

const fallbackAarti: LibraryItem[] = [
  { name: 'Om Jai Jagdish Hare', deity: 'Lord Vishnu' },
  { name: 'Jai Ganesh Deva', deity: 'Lord Ganesha' },
  { name: 'Om Jai Shiv Omkara', deity: 'Lord Shiva' },
  { name: 'Jai Lakshmi Mata', deity: 'Goddess Lakshmi' },
];

export default function SpiritualLibrary() {
  const sectionRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();
  const [gitaChapters, setGitaChapters] = useState<GitaChapter[]>(fallbackGita);
  const [mantras, setMantras] = useState<LibraryItem[]>(fallbackMantras);
  const [aarti, setAarti] = useState<LibraryItem[]>(fallbackAarti);
  const [activeTab, setActiveTab] = useState('gita');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.fromTo('.spiritual-title', { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 0.8, ease: 'power3.out', scrollTrigger: { trigger: sectionRef.current, start: 'top 80%' } });
    }, sectionRef);
    return () => ctx.revert();
  }, []);

  useEffect(() => {
    let cancelled = false;
    const fetchContent = async () => {
      setLoading(true);
      try {
        if (activeTab === 'gita') {
          const data = await api.get('/api/gita/chapters');
          const chapters = Array.isArray(data) ? data : data.chapters || [];
          if (!cancelled && chapters.length > 0) setGitaChapters(normalizeGitaChapters(chapters));
        } else {
          const data = await api.get(`/api/library/${activeTab}`);
          const items = Array.isArray(data) ? data : data.items || [];
          if (!cancelled && items.length > 0) {
            const normalizedItems = normalizeLibraryItems(items, activeTab);
            if (activeTab === 'mantra') setMantras(normalizedItems);
            else if (activeTab === 'aarti') setAarti(normalizedItems);
          }
        }
      } catch {
        // fallback already set
      } finally {
        if (!cancelled) setLoading(false);
      }
    };
    fetchContent();
    return () => { cancelled = true; };
  }, [activeTab]);

  return (
    <section ref={sectionRef} id="spiritual" className="relative py-24 bg-white">
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="spiritual-title text-center mb-12">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-minimal-indigo/10 text-minimal-indigo text-sm font-medium mb-6">
            <BookOpen className="w-4 h-4" />Sacred Wisdom
          </div>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-display font-bold text-minimal-gray-900 mb-4">
            Spiritual<span className="text-gradient-indigo"> Library</span>
          </h2>
        </div>
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid grid-cols-3 max-w-md mx-auto mb-8 bg-minimal-gray-100">
            <TabsTrigger value="gita" className="data-[state=active]:bg-minimal-indigo data-[state=active]:text-white"><BookOpen className="w-4 h-4 mr-2" />Gita</TabsTrigger>
            <TabsTrigger value="mantra" className="data-[state=active]:bg-minimal-violet data-[state=active]:text-white"><Music className="w-4 h-4 mr-2" />Mantras</TabsTrigger>
            <TabsTrigger value="aarti" className="data-[state=active]:bg-minimal-blue data-[state=active]:text-white"><Flame className="w-4 h-4 mr-2" />Aarti</TabsTrigger>
          </TabsList>
          {loading ? (
            <div className="flex items-center justify-center py-16">
              <Loader2 className="w-10 h-10 text-minimal-indigo animate-spin" />
            </div>
          ) : (
            <>
              <TabsContent value="gita" className="mt-0">
                <div className="grid md:grid-cols-2 gap-6">
                  {gitaChapters.map((chapter, index) => (
                    <Card key={index} className="group bg-minimal-gray-50 border-0 hover:shadow-soft-lg transition-all">
                      <CardContent className="p-6">
                        <div className="w-12 h-12 rounded-xl bg-minimal-indigo/10 flex items-center justify-center mb-4">
                          <BookOpen className="w-6 h-6 text-minimal-indigo" />
                        </div>
                        <h3 className="text-xl font-display font-semibold text-minimal-gray-900 mb-2">{chapter.title}</h3>
                        <p className="text-sm text-minimal-gray-500 mb-4">{chapter.description}</p>
                        <span className="text-xs text-minimal-indigo">{chapter.verses} Verses</span>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </TabsContent>
              <TabsContent value="mantra" className="mt-0">
                <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                  {mantras.map((mantra, index) => (
                    <Card key={index} className="group bg-minimal-gray-50 border-0 hover:shadow-soft-lg transition-all text-center">
                      <CardContent className="p-6">
                        <div className="w-12 h-12 rounded-xl bg-minimal-violet/10 flex items-center justify-center mx-auto mb-4">
                          <Music className="w-6 h-6 text-minimal-violet" />
                        </div>
                        <h3 className="text-lg font-display font-semibold text-minimal-gray-900 mb-1">{mantra.name}</h3>
                        <p className="text-sm text-minimal-gray-500">{mantra.deity}</p>
                        {mantra.benefit && <span className="text-xs text-minimal-violet mt-2 inline-block">{mantra.benefit}</span>}
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </TabsContent>
              <TabsContent value="aarti" className="mt-0">
                <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                  {aarti.map((item, index) => (
                    <Card key={index} className="group bg-minimal-gray-50 border-0 hover:shadow-soft-lg transition-all text-center">
                      <CardContent className="p-6">
                        <div className="w-12 h-12 rounded-xl bg-minimal-blue/10 flex items-center justify-center mx-auto mb-4">
                          <Flame className="w-6 h-6 text-minimal-blue" />
                        </div>
                        <h3 className="text-lg font-display font-semibold text-minimal-gray-900 mb-1">{item.name}</h3>
                        <p className="text-sm text-minimal-gray-500">{item.deity}</p>
                        <Button variant="ghost" size="sm" className="mt-3 text-minimal-blue">
                          <Play className="w-4 h-4 mr-2" />Play
                        </Button>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </TabsContent>
            </>
          )}
        </Tabs>
        <div className="mt-16">
          <Card className="bg-minimal-gray-50 border-0 shadow-soft overflow-hidden">
            <CardContent className="p-8">
              <div className="grid md:grid-cols-2 gap-8 items-center">
                <div>
                  <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-minimal-indigo/10 text-minimal-indigo text-sm font-medium mb-4">
                    <Sparkles className="w-4 h-4" />AI Powered
                  </div>
                  <h3 className="text-2xl sm:text-3xl font-display font-bold text-minimal-gray-900 mb-4">
                    Ask AI About the<span className="text-gradient-indigo"> Bhagavad Gita</span>
                  </h3>
                  <Button onClick={() => navigate('/ai-chat')} className="bg-minimal-indigo text-white hover:bg-minimal-violet">
                    <Sparkles className="w-5 h-5 mr-2" />Ask AI Gita<ChevronRight className="w-5 h-5 ml-2" />
                  </Button>
                </div>
                <div className="relative aspect-square max-w-sm mx-auto">
                  <div className="absolute inset-0 rounded-3xl bg-gradient-to-br from-minimal-indigo/10 to-minimal-violet/10" />
                  <div className="absolute inset-4 rounded-2xl bg-white shadow-soft flex items-center justify-center">
                    <BookOpen className="w-16 h-16 text-minimal-indigo" />
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  );
}
