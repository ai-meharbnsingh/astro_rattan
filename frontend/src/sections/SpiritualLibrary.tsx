import { useCallback, useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { BookOpen, Music, Flame, ChevronRight, Play, Pause, Sparkles, Loader2 } from 'lucide-react';
import { api } from '@/lib/api';

gsap.registerPlugin(ScrollTrigger);

interface GitaChapter { chapter: number; title: string; verses: number; description: string; }
interface LibraryItem { id?: number; name: string; deity?: string; benefit?: string; category?: string; content?: string; }

const normalizeGitaChapters = (chapters: any[]): GitaChapter[] =>
  chapters.map((chapter) => ({ chapter: chapter.chapter, title: chapter.title || `Chapter ${chapter.chapter}`, verses: chapter.verses_count ?? chapter.verses ?? 0, description: chapter.summary || chapter.description || '' }));
const normalizeLibraryItems = (items: any[], category: string): LibraryItem[] =>
  items.map((item) => ({ id: item.id, name: item.title || item.name || '', deity: item.title_hindi || item.deity || category.replace(/_/g, ' '), benefit: item.content_preview || item.benefit || '', category: item.category || category, content: item.content_preview || item.content || '' }));

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

/* ------------------------------------------------------------------ */
/*  Inline Audio Player Component                                      */
/* ------------------------------------------------------------------ */

interface AudioPlayerProps {
  src: string;
  isPlaying: boolean;
  onToggle: () => void;
  progress: number;       // 0-100
  currentTime: number;
  duration: number;
  onSeek: (pct: number) => void;
}

const formatTime = (seconds: number) => {
  if (!seconds || !isFinite(seconds)) return '0:00';
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${s.toString().padStart(2, '0')}`;
};

function AudioPlayer({ isPlaying, onToggle, progress, currentTime, duration, onSeek }: AudioPlayerProps) {
  const barRef = useRef<HTMLDivElement>(null);

  const handleBarClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!barRef.current) return;
    const rect = barRef.current.getBoundingClientRect();
    const pct = Math.max(0, Math.min(100, ((e.clientX - rect.left) / rect.width) * 100));
    onSeek(pct);
  };

  return (
    <div className="flex items-center gap-3 mt-3 w-full">
      <button
        type="button"
        onClick={onToggle}
        className="w-8 h-8 rounded-full bg-sacred-gold/20 border border-sacred-gold/30 flex items-center justify-center text-sacred-gold hover:bg-sacred-gold/30 transition-colors flex-shrink-0"
      >
        {isPlaying ? <Pause className="w-3.5 h-3.5" /> : <Play className="w-3.5 h-3.5 ml-0.5" />}
      </button>
      <div className="flex-1 min-w-0">
        <div
          ref={barRef}
          onClick={handleBarClick}
          className="h-1.5 rounded-full bg-cosmic-surface cursor-pointer relative overflow-hidden"
        >
          <div
            className="absolute inset-y-0 left-0 rounded-full bg-gradient-to-r from-sacred-gold to-sacred-gold-light transition-[width] duration-200"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>
      <span className="text-[10px] text-cosmic-text-secondary tabular-nums flex-shrink-0">
        {formatTime(currentTime)}/{formatTime(duration)}
      </span>
    </div>
  );
}

/* Mini progress bar shown below the mantra/aarti name when playing */
function MiniProgressBar({ progress }: { progress: number }) {
  return (
    <div className="w-full h-0.5 rounded-full bg-cosmic-surface mt-1 overflow-hidden">
      <div
        className="h-full rounded-full bg-sacred-gold transition-[width] duration-200"
        style={{ width: `${progress}%` }}
      />
    </div>
  );
}

export default function SpiritualLibrary() {
  const sectionRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();
  const [gitaChapters, setGitaChapters] = useState<GitaChapter[]>(fallbackGita);
  const [mantras, setMantras] = useState<LibraryItem[]>(fallbackMantras);
  const [aarti, setAarti] = useState<LibraryItem[]>(fallbackAarti);
  const [activeTab, setActiveTab] = useState('gita');
  const [loading, setLoading] = useState(false);

  /* ---- Audio state ---- */
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const [playingId, setPlayingId] = useState<string | null>(null);   // "mantra-2" or "aarti-0"
  const [isPlaying, setIsPlaying] = useState(false);
  const [audioProgress, setAudioProgress] = useState(0);
  const [audioCurrent, setAudioCurrent] = useState(0);
  const [audioDuration, setAudioDuration] = useState(0);

  const stopAudio = useCallback(() => {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.removeAttribute('src');
      audioRef.current.load();
    }
    setPlayingId(null);
    setIsPlaying(false);
    setAudioProgress(0);
    setAudioCurrent(0);
    setAudioDuration(0);
  }, []);

  const toggleAudio = useCallback((id: string, src: string) => {
    // If the same item is already playing, toggle pause/play
    if (playingId === id && audioRef.current) {
      if (isPlaying) {
        audioRef.current.pause();
        setIsPlaying(false);
      } else {
        audioRef.current.play().catch(() => {});
        setIsPlaying(true);
      }
      return;
    }
    // Otherwise start new track
    stopAudio();
    if (!audioRef.current) {
      audioRef.current = new Audio();
      audioRef.current.addEventListener('timeupdate', () => {
        const a = audioRef.current;
        if (!a) return;
        setAudioCurrent(a.currentTime);
        setAudioDuration(a.duration);
        setAudioProgress(a.duration ? (a.currentTime / a.duration) * 100 : 0);
      });
      audioRef.current.addEventListener('ended', () => {
        setIsPlaying(false);
        setAudioProgress(100);
      });
    }
    audioRef.current.src = src;
    audioRef.current.play().catch(() => {});
    setPlayingId(id);
    setIsPlaying(true);
  }, [playingId, isPlaying, stopAudio]);

  const seekAudio = useCallback((pct: number) => {
    if (audioRef.current && audioRef.current.duration) {
      audioRef.current.currentTime = (pct / 100) * audioRef.current.duration;
    }
  }, []);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current = null;
      }
    };
  }, []);

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
            const normalized = normalizeLibraryItems(items, activeTab);
            if (activeTab === 'mantra') setMantras(normalized);
            else if (activeTab === 'aarti') setAarti(normalized);
          }
        }
      } catch { /* fallback already set */ } finally { if (!cancelled) setLoading(false); }
    };
    fetchContent();
    return () => { cancelled = true; };
  }, [activeTab]);

  return (
    <section ref={sectionRef} id="spiritual" className="relative py-24 bg-cosmic-bg bg-mandala">
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="spiritual-title text-center mb-12">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-sacred-gold/10 text-sacred-gold text-sm font-medium mb-6 border border-sacred-gold/30">
            <BookOpen className="w-4 h-4" />Sacred Wisdom
          </div>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-sacred font-bold text-cosmic-text mb-4">
            Spiritual<span className="text-gradient-gold"> Library</span>
          </h2>
        </div>
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid grid-cols-3 max-w-md mx-auto mb-8 bg-cosmic-card border border-sacred-gold/10">
            <TabsTrigger value="gita" className="data-[state=active]:bg-sacred-gold data-[state=active]:text-cosmic-bg text-cosmic-text-secondary"><BookOpen className="w-4 h-4 mr-2" />Gita</TabsTrigger>
            <TabsTrigger value="mantra" className="data-[state=active]:bg-sacred-gold data-[state=active]:text-cosmic-bg text-cosmic-text-secondary"><Music className="w-4 h-4 mr-2" />Mantras</TabsTrigger>
            <TabsTrigger value="aarti" className="data-[state=active]:bg-sacred-gold data-[state=active]:text-cosmic-bg text-cosmic-text-secondary"><Flame className="w-4 h-4 mr-2" />Aarti</TabsTrigger>
          </TabsList>
          {loading ? (
            <div className="flex items-center justify-center py-16"><Loader2 className="w-10 h-10 text-sacred-gold animate-spin" /></div>
          ) : (
            <>
              <TabsContent value="gita" className="mt-0">
                <div className="grid md:grid-cols-2 gap-6">
                  {gitaChapters.map((chapter, index) => (
                    <Card key={index} className="group card-sacred border-sacred-gold/15 hover:border-sacred-gold/40 transition-all">
                      <CardContent className="p-6">
                        <div className="w-12 h-12 rounded-xl bg-sacred-gold/10 flex items-center justify-center mb-4 border border-sacred-gold/20">
                          <BookOpen className="w-6 h-6 text-sacred-gold" />
                        </div>
                        <h3 className="text-xl font-sacred font-semibold text-cosmic-text mb-2">{chapter.title}</h3>
                        <p className="text-sm text-cosmic-text-secondary mb-4">{chapter.description}</p>
                        <span className="text-xs text-sacred-gold">{chapter.verses} Verses</span>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </TabsContent>
              <TabsContent value="mantra" className="mt-0">
                <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                  {mantras.map((mantra, index) => {
                    const audioId = `mantra-${mantra.id ?? index}`;
                    const audioSrc = `/api/library/mantra/${mantra.id ?? index}/audio`;
                    const active = playingId === audioId;
                    return (
                      <Card key={index} className={`group card-sacred border-sacred-gold/15 hover:border-sacred-gold/40 transition-all text-center ${active ? 'border-sacred-gold/50 ring-1 ring-sacred-gold/20' : ''}`}>
                        <CardContent className="p-6">
                          <div className="w-12 h-12 rounded-xl bg-sacred-purple/30 flex items-center justify-center mx-auto mb-4 border border-sacred-violet/20">
                            <Music className="w-6 h-6 text-sacred-violet" />
                          </div>
                          <h3 className="text-lg font-sacred font-semibold text-cosmic-text mb-1">{mantra.name}</h3>
                          {active && <MiniProgressBar progress={audioProgress} />}
                          <p className="text-sm text-cosmic-text-secondary">{mantra.deity}</p>
                          {mantra.benefit && <span className="text-xs text-sacred-gold mt-2 inline-block">{mantra.benefit}</span>}
                          <AudioPlayer
                            src={audioSrc}
                            isPlaying={active && isPlaying}
                            onToggle={() => toggleAudio(audioId, audioSrc)}
                            progress={active ? audioProgress : 0}
                            currentTime={active ? audioCurrent : 0}
                            duration={active ? audioDuration : 0}
                            onSeek={seekAudio}
                          />
                        </CardContent>
                      </Card>
                    );
                  })}
                </div>
              </TabsContent>
              <TabsContent value="aarti" className="mt-0">
                <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                  {aarti.map((item, index) => {
                    const audioId = `aarti-${item.id ?? index}`;
                    const audioSrc = `/api/library/aarti/${item.id ?? index}/audio`;
                    const active = playingId === audioId;
                    return (
                      <Card key={index} className={`group card-sacred border-sacred-gold/15 hover:border-sacred-gold/40 transition-all text-center ${active ? 'border-sacred-gold/50 ring-1 ring-sacred-gold/20' : ''}`}>
                        <CardContent className="p-6">
                          <div className="w-12 h-12 rounded-xl bg-sacred-saffron/10 flex items-center justify-center mx-auto mb-4 border border-sacred-saffron/20">
                            <Flame className="w-6 h-6 text-sacred-saffron" />
                          </div>
                          <h3 className="text-lg font-sacred font-semibold text-cosmic-text mb-1">{item.name}</h3>
                          {active && <MiniProgressBar progress={audioProgress} />}
                          <p className="text-sm text-cosmic-text-secondary">{item.deity}</p>
                          <AudioPlayer
                            src={audioSrc}
                            isPlaying={active && isPlaying}
                            onToggle={() => toggleAudio(audioId, audioSrc)}
                            progress={active ? audioProgress : 0}
                            currentTime={active ? audioCurrent : 0}
                            duration={active ? audioDuration : 0}
                            onSeek={seekAudio}
                          />
                        </CardContent>
                      </Card>
                    );
                  })}
                </div>
              </TabsContent>
            </>
          )}
        </Tabs>
        <div className="mt-16">
          <Card className="card-sacred border-sacred-gold/20 overflow-hidden">
            <CardContent className="p-8">
              <div className="grid md:grid-cols-2 gap-8 items-center">
                <div>
                  <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-sacred-gold/10 text-sacred-gold text-sm font-medium mb-4 border border-sacred-gold/30">
                    <Sparkles className="w-4 h-4" />AI Powered
                  </div>
                  <h3 className="text-2xl sm:text-3xl font-sacred font-bold text-cosmic-text mb-4">
                    Ask AI About the<span className="text-gradient-gold"> Bhagavad Gita</span>
                  </h3>
                  <Button onClick={() => navigate('/ai-chat')} className="btn-sacred">
                    <Sparkles className="w-5 h-5 mr-2" />Ask AI Gita<ChevronRight className="w-5 h-5 ml-2" />
                  </Button>
                </div>
                <div className="relative aspect-square max-w-sm mx-auto">
                  <div className="absolute inset-0 rounded-3xl bg-gradient-to-br from-sacred-purple/30 to-sacred-gold/10 border border-sacred-gold/15" />
                  <div className="absolute inset-4 rounded-2xl card-sacred flex items-center justify-center">
                    <BookOpen className="w-16 h-16 text-sacred-gold/50" />
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
