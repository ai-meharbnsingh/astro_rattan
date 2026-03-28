import { useCallback, useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { BookOpen, Music, Flame, ChevronRight, Play, Pause, Sparkles, Loader2, X } from 'lucide-react';
import { api } from '@/lib/api';
import { resolveApiUrl } from '@/lib/api';

gsap.registerPlugin(ScrollTrigger);

interface GitaChapter { chapter: number; title: string; verses: number; description: string; }
interface GitaVerse { id?: string; verse?: number; title?: string; sanskrit?: string; translation?: string; commentary?: string; content?: string; audio_url?: string; }
interface LibraryItem { id?: number; name: string; deity?: string; benefit?: string; category?: string; content?: string; audio_url?: string; }

const normalizeGitaChapters = (chapters: any[]): GitaChapter[] =>
  chapters.map((chapter) => ({ chapter: chapter.chapter, title: chapter.title || `Chapter ${chapter.chapter}`, verses: chapter.verses_count ?? chapter.verses ?? 0, description: chapter.summary || chapter.description || '' }));
const normalizeLibraryItems = (items: any[], category: string): LibraryItem[] =>
  items.map((item) => ({ id: item.id, name: item.title || item.name || '', deity: item.title_hindi || item.deity || category.replace(/_/g, ' '), benefit: item.content_preview || item.benefit || '', category: item.category || category, content: item.content_preview || item.content || '', audio_url: item.audio_url || '' }));

// Sample verses for each chapter (shown when API fails)
const sampleVerses: Record<number, GitaVerse[]> = {
  1: [
    { verse: 1, sanskrit: 'धृतराष्ट्र उवाच | धर्मक्षेत्रे कुरुक्षेत्रे समवेता युयुत्सवः | मामकाः पाण्डवाश्चैव किमकुर्वत सञ्जय ||1||', translation: 'Dhritarashtra said: O Sanjaya, what did my sons and the sons of Pandu do when they assembled on the sacred field of Kurukshetra, eager for battle?', commentary: 'The Bhagavad Gita begins with Dhritarashtra asking Sanjaya about the events on the battlefield.' },
    { verse: 2, sanskrit: 'सञ्जय उवाच | दृष्ट्वा तु पाण्डवानीकं व्यूढं दुर्योधनस्तदा | आचार्यमुपसङ्गम्य राजा वचनमब्रवीत् ||2||', translation: 'Sanjaya said: Seeing the Pandava army arrayed in battle formation, King Duryodhana approached his teacher Drona and spoke these words.', commentary: 'Duryodhana observes the military formation of the Pandavas.' },
    { verse: 3, sanskrit: 'पश्यैतां पाण्डुपुत्राणामाचार्य महतीं चमूम् | व्यूढां द्रुपदपुत्रेण तव शिष्येण धीमता ||3||', translation: 'Behold, O Teacher, this mighty army of the sons of Pandu, arrayed by your wise disciple, the son of Drupada.', commentary: 'Duryodhana points out the strength of the Pandava army.' },
    { verse: 4, sanskrit: 'अत्र शूरा महेष्वासा भीमार्जुनसमा युधि | युयुधानो विराटश्च द्रुपदश्च महारथः ||4||', translation: 'Here are heroes, mighty archers, equal in battle to Bhima and Arjuna - Yuyudhana, Virata, and Drupada, the great chariot-warrior.', commentary: 'Listing the great warriors on the Pandava side.' },
    { verse: 5, sanskrit: 'धृष्टकेतुश्चेकितानः काशिराजश्च वीर्यवान् | पुरुजित्कुन्तिभोजश्च शैब्यश्च नरपुङ्गवः ||5||', translation: 'Dhrishtaketu, Chekitana, the valiant king of Kashi, Purujit, Kuntibhoja, and Shaibya, the best among men.', commentary: 'More warriors of the Pandava army are named.' },
  ],
  2: [
    { verse: 1, sanskrit: 'सञ्जय उवाच | तं तथा कृपयाविष्टमश्रुपूर्णाकुलेक्षणम् | विषीदन्तमिदं वाक्यमुवाच मधुसूदनः ||1||', translation: 'Sanjaya said: To him overcome with compassion, with blurred tearful eyes, Madhusudana spoke these words.', commentary: 'Krishna sees Arjuna\'s emotional state.' },
    { verse: 2, sanskrit: 'श्रीभगवानुवाच | कुतस्त्वा कश्मलमिदं विषमे समुपस्थितम् | अनार्यजुष्टमस्वर्ग्यमकीर्तिकरमर्जुन ||2||', translation: 'The Blessed Lord said: From where has this impurity come in this crisis? It is unworthy, prevents heaven entry, and causes disgrace.', commentary: 'Krishna questions Arjuna\'s despair.' },
    { verse: 3, sanskrit: 'क्लैब्यं मा स्म गमः पार्थ नैतत्त्वय्युपपद्यते | क्षुद्रं हृदयदौर्बल्यं त्यक्त्वोत्तिष्ठ परन्तप ||3||', translation: 'O Partha, do not yield to unmanliness. It does not befit you. Abandon this weakness and arise, O conqueror.', commentary: 'Krishna urges Arjuna to fulfill his duty.' },
    { verse: 4, sanskrit: 'अर्जुन उवाच | कथं भीष्ममहं सङ्ख्ये द्रोणं च मधुसूदन | इषुभिः प्रतियोत्स्यामि पूजार्हावरिसूदन ||4||', translation: 'Arjuna said: How shall I fight Bhishma and Drona with arrows, O Madhusudana? They are worthy of worship, O enemy-slayer.', commentary: 'Arjuna\'s dilemma about fighting his teachers.' },
    { verse: 5, sanskrit: 'गुरूनहत्वा हि महानुभावान् श्रेयो भोक्तुं भैक्ष्यमपीह लोके | हत्वार्थकामांस्तु गुरूनिहैव भुञ्जीय भोगान् रुधिरप्रदिग्धान् ||5||', translation: 'Better to eat beggar\'s food in this world than to kill these noble teachers. If I kill them, I would enjoy pleasures stained with their blood.', commentary: 'Arjuna prefers poverty over killing his elders.' },
  ],
  3: [
    { verse: 1, sanskrit: 'अर्जुन उवाच | ज्यायसी चेत्कर्मणस्ते मता बुद्धिर्जनार्दन | तत्किं कर्मणि घोरे मां नियोजयसि केशव ||1||', translation: 'Arjuna said: O Janardana, if knowledge is superior to action, why do you urge me to this terrible action?', commentary: 'Arjuna questions the apparent contradiction.' },
    { verse: 2, sanskrit: 'व्यामिश्रेणेव वाक्येन बुद्धिं मोहयसीव मे | तदेकं वद निश्चित्य येन श्रेयोऽहमाप्नुयाम् ||2||', translation: 'Your words confuse me. Tell me with certainty that one path to highest good.', commentary: 'Arjuna seeks clarity.' },
    { verse: 3, sanskrit: 'श्रीभगवानुवाच | लोकेऽस्मिन्द्विविधा निष्ठा पुरा प्रोक्ता मयानघ | ज्ञानयोगेन साङ्ख्यानां कर्मयोगेन योगिनाम् ||3||', translation: 'The Blessed Lord said: In this world, two paths I have declared before: Jnana Yoga for the contemplative, Karma Yoga for the active.', commentary: 'Krishna explains the two paths to liberation.' },
  ],
  4: [
    { verse: 1, sanskrit: 'श्रीभगवानुवाच | इमं विवस्वते योगं प्रोक्तवानहमव्ययम् | विवस्वान्मनवे प्राह मनुरिक्ष्वाकवेऽब्रवीत् ||1||', translation: 'I taught this imperishable yoga to Vivasvan, who taught Manu, and Manu taught Ikshvaku.', commentary: 'The ancient lineage of this knowledge.' },
    { verse: 2, sanskrit: 'एवं परम्पराप्राप्तमिमं राजर्षयो विदुः | स कालेनेह महता योगो नष्टः परन्तप ||2||', translation: 'Thus royal sages knew it. But after long time, this yoga was lost from earth.', commentary: 'Knowledge lost over time.' },
    { verse: 3, sanskrit: 'स एवायं मया तेऽद्य योगः प्रोक्तः पुरातनः | भक्तोऽसि मे सखा चेति रहस्यं ह्येतदुत्तमम् ||3||', translation: 'Today I declare this ancient yoga to you, for you are my devotee and friend. This is supreme secret.', commentary: 'Krishna reveals the secret to Arjuna.' },
  ],
};

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
const fallbackChalisa: LibraryItem[] = [
  { name: 'Hanuman Chalisa', deity: 'Lord Hanuman' },
  { name: 'Shiv Chalisa', deity: 'Lord Shiva' },
  { name: 'Durga Chalisa', deity: 'Goddess Durga' },
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
  const [chalisa, setChalisa] = useState<LibraryItem[]>(fallbackChalisa);
  const [activeTab, setActiveTab] = useState('gita');
  const [loading, setLoading] = useState(false);
  const [selectedChapter, setSelectedChapter] = useState<number | null>(null);
  const [chapterVerses, setChapterVerses] = useState<Record<number, GitaVerse[]>>({});
  const [chapterTitle, setChapterTitle] = useState<Record<number, string>>({});
  const [versesLoading, setVersesLoading] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);

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
            else if (activeTab === 'chalisa') setChalisa(normalized);
          }
        }
      } catch { /* fallback already set */ } finally { if (!cancelled) setLoading(false); }
    };
    fetchContent();
    return () => { cancelled = true; };
  }, [activeTab]);

  const loadChapterVerses = useCallback(async (chapter: number) => {
    setSelectedChapter(chapter);
    setIsModalOpen(true);
    if (chapterVerses[chapter]) {
      setVersesLoading(false);
      return;
    }
    setVersesLoading(true);
    try {
      const data = await api.get(`/api/gita/chapter/${chapter}`);
      const verses = Array.isArray(data?.verses) ? data.verses : [];
      if (verses.length > 0) {
        setChapterVerses((prev) => ({ ...prev, [chapter]: verses }));
        setChapterTitle((prev) => ({ ...prev, [chapter]: data?.title || `Chapter ${chapter}` }));
      } else {
        // Use sample verses if API returns empty
        setChapterVerses((prev) => ({ ...prev, [chapter]: sampleVerses[chapter] || [] }));
        setChapterTitle((prev) => ({ ...prev, [chapter]: data?.title || `Chapter ${chapter}` }));
      }
    } catch {
      // Use sample verses on API error
      setChapterVerses((prev) => ({ ...prev, [chapter]: sampleVerses[chapter] || [] }));
      setChapterTitle((prev) => ({ ...prev, [chapter]: `Chapter ${chapter}` }));
    } finally {
      setVersesLoading(false);
    }
  }, [chapterVerses]);

  // Auto-load first chapter data silently (without opening modal) when tab changes
  useEffect(() => {
    if (activeTab !== 'gita') return;
    const firstWithVerses = gitaChapters.find((c) => c.verses > 0);
    if (!firstWithVerses) return;
    if (!selectedChapter) {
      setSelectedChapter(firstWithVerses.chapter);
      // Load verses silently without opening modal
      if (!chapterVerses[firstWithVerses.chapter]) {
        setVersesLoading(true);
        api.get(`/api/gita/chapter/${firstWithVerses.chapter}`).then((data) => {
          const verses = Array.isArray(data?.verses) ? data.verses : [];
          if (verses.length > 0) {
            setChapterVerses((prev) => ({ ...prev, [firstWithVerses.chapter]: verses }));
            setChapterTitle((prev) => ({ ...prev, [firstWithVerses.chapter]: data?.title || `Chapter ${firstWithVerses.chapter}` }));
          } else {
            setChapterVerses((prev) => ({ ...prev, [firstWithVerses.chapter]: sampleVerses[firstWithVerses.chapter] || [] }));
            setChapterTitle((prev) => ({ ...prev, [firstWithVerses.chapter]: data?.title || `Chapter ${firstWithVerses.chapter}` }));
          }
        }).catch(() => {
          setChapterVerses((prev) => ({ ...prev, [firstWithVerses.chapter]: sampleVerses[firstWithVerses.chapter] || [] }));
          setChapterTitle((prev) => ({ ...prev, [firstWithVerses.chapter]: `Chapter ${firstWithVerses.chapter}` }));
        }).finally(() => {
          setVersesLoading(false);
        });
      }
    }
  }, [activeTab, gitaChapters, selectedChapter, chapterVerses]);

  return (
    <section ref={sectionRef} id="spiritual" className="relative py-24 bg-transparent">
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
          <TabsList className="grid grid-cols-4 max-w-2xl mx-auto mb-8 bg-cosmic-card border border-sacred-gold/10">
            <TabsTrigger value="gita" className="data-[state=active]:bg-sacred-gold data-[state=active]:text-cosmic-bg text-cosmic-text-secondary"><BookOpen className="w-4 h-4 mr-2" />Gita</TabsTrigger>
            <TabsTrigger value="mantra" className="data-[state=active]:bg-sacred-gold data-[state=active]:text-cosmic-bg text-cosmic-text-secondary"><Music className="w-4 h-4 mr-2" />Mantras</TabsTrigger>
            <TabsTrigger value="aarti" className="data-[state=active]:bg-sacred-gold data-[state=active]:text-cosmic-bg text-cosmic-text-secondary"><Flame className="w-4 h-4 mr-2" />Aarti</TabsTrigger>
            <TabsTrigger value="chalisa" className="data-[state=active]:bg-sacred-gold data-[state=active]:text-cosmic-bg text-cosmic-text-secondary"><BookOpen className="w-4 h-4 mr-2" />Chalisa</TabsTrigger>
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
                        <div className="mt-4">
                          {chapter.verses > 0 ? (
                            <Button
                              size="sm"
                              onClick={() => loadChapterVerses(chapter.chapter)}
                              className="bg-sacred-gold/10 text-sacred-gold hover:bg-sacred-gold hover:text-cosmic-bg border border-sacred-gold/30"
                            >
                              View {chapter.verses} Verses
                            </Button>
                          ) : (
                            <Button
                              size="sm"
                              disabled
                              className="border border-sacred-gold/20 bg-cosmic-surface text-cosmic-text-muted"
                            >
                              Verses Coming Soon
                            </Button>
                          )}
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
                
                {/* Modal for Chapter Verses */}
                {isModalOpen && selectedChapter && (
                  <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-[#F5F0E8]/80 backdrop-blur-sm" onClick={() => setIsModalOpen(false)}>
                    <div className="relative w-full max-w-4xl max-h-[85vh] bg-[#E8E0D4] rounded-2xl border border-[#9A7B0A]/30 shadow-2xl overflow-hidden" onClick={(e) => e.stopPropagation()}>
                      {/* Modal Header */}
                      <div className="sticky top-0 z-10 bg-[#E8E0D4] border-b border-[#9A7B0A]/20 p-6 flex items-center justify-between">
                        <div>
                          <h3 className="text-2xl font-sacred font-bold text-[#1a1a2e]">
                            Bhagavad Gita - Chapter {selectedChapter}
                          </h3>
                          <p className="text-[#9A7B0A]">
                            {chapterTitle[selectedChapter] || `Chapter ${selectedChapter}`}
                          </p>
                        </div>
                        <button
                          onClick={() => setIsModalOpen(false)}
                          className="w-10 h-10 rounded-full bg-[#9A7B0A]/10 hover:bg-[#9A7B0A]/20 border border-[#9A7B0A]/30 flex items-center justify-center text-[#9A7B0A] transition-colors"
                        >
                          <X className="w-5 h-5" />
                        </button>
                      </div>
                      
                      {/* Modal Content */}
                      <div className="p-6 overflow-y-auto max-h-[calc(85vh-100px)]">
                        {versesLoading ? (
                          <div className="flex items-center justify-center gap-3 py-12 text-[#1a1a2e]/60">
                            <Loader2 className="w-6 h-6 animate-spin text-[#9A7B0A]" />
                            Loading verses...
                          </div>
                        ) : (
                          <div className="space-y-8">
                            {/* Sample data notice */}
                            {(chapterVerses[selectedChapter] || []).length <= 5 && (
                              <div className="bg-[#9A7B0A]/10 border border-[#9A7B0A]/30 rounded-lg p-4">
                                <p className="text-base text-[#9A7B0A]">
                                  📖 Showing {sampleVerses[selectedChapter]?.length || 0} sample verses. Connect to backend for all {(gitaChapters.find(c => c.chapter === selectedChapter)?.verses || 0)} verses.
                                </p>
                              </div>
                            )}
                            {(chapterVerses[selectedChapter] || []).map((v, idx) => (
                              <Card key={v.id || idx} className="bg-[#111] border-[#9A7B0A]/30 hover:border-[#9A7B0A]/50 transition-colors">
                                <CardContent className="p-6">
                                  {/* Verse Header */}
                                  <div className="flex items-center gap-3 mb-4">
                                    <span className="w-10 h-10 rounded-full bg-[#9A7B0A]/20 flex items-center justify-center text-[#9A7B0A] font-bold text-lg">
                                      {v.verse ?? idx + 1}
                                    </span>
                                    <span className="text-lg font-medium text-[#1a1a2e]/80">
                                      Verse {v.verse ?? idx + 1}
                                    </span>
                                  </div>
                                  
                                  {/* Sanskrit */}
                                  {v.sanskrit && (
                                    <div className="mb-5 p-5 bg-[#E8E0D4] rounded-lg border-l-4 border-[#9A7B0A]">
                                      <p className="text-xl text-[#B8860B] leading-relaxed font-medium" style={{ fontFamily: 'serif' }}>
                                        {v.sanskrit}
                                      </p>
                                    </div>
                                  )}
                                  
                                  {/* Translation */}
                                  {v.translation && (
                                    <div className="mb-4">
                                      <p className="text-sm text-[#9A7B0A] uppercase tracking-wide mb-2 font-semibold">Translation</p>
                                      <p className="text-lg text-[#1a1a2e] leading-relaxed">{v.translation}</p>
                                    </div>
                                  )}
                                  
                                  {/* Commentary */}
                                  {v.commentary && (
                                    <div className="mt-5 pt-4 border-t border-[#8B7355]/10">
                                      <p className="text-sm text-[#9A7B0A] uppercase tracking-wide mb-2 font-semibold">Commentary</p>
                                      <p className="text-base text-[#1a1a2e]/80 leading-relaxed italic">{v.commentary}</p>
                                    </div>
                                  )}
                                  
                                  {v.audio_url && (
                                    <a
                                      href={resolveApiUrl(v.audio_url)}
                                      download
                                      className="mt-5 inline-flex items-center gap-2 text-base text-[#9A7B0A] hover:text-[#B8860B] underline"
                                    >
                                      🔊 Download Audio
                                    </a>
                                  )}
                                </CardContent>
                              </Card>
                            ))}
                            {(chapterVerses[selectedChapter] || []).length === 0 && (
                              <div className="text-center py-12">
                                <p className="text-[#1a1a2e]/60 text-lg">No verses available for this chapter.</p>
                              </div>
                            )}
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                )}
              </TabsContent>
              <TabsContent value="mantra" className="mt-0">
                <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                  {mantras.map((mantra, index) => {
                    const audioId = `mantra-${mantra.id ?? index}`;
                    const audioSrc = resolveApiUrl((mantra as any).audio_url);
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
                          {audioSrc ? (
                            <>
                              <AudioPlayer
                                src={audioSrc}
                                isPlaying={active && isPlaying}
                                onToggle={() => toggleAudio(audioId, audioSrc)}
                                progress={active ? audioProgress : 0}
                                currentTime={active ? audioCurrent : 0}
                                duration={active ? audioDuration : 0}
                                onSeek={seekAudio}
                              />
                              <a
                                href={audioSrc}
                                download
                                className="mt-2 inline-block text-xs text-sacred-gold hover:text-sacred-gold-light underline"
                              >
                                Download Audio
                              </a>
                            </>
                          ) : (
                            <p className="mt-3 text-xs text-cosmic-text-muted">Audio not available</p>
                          )}
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
                    const audioSrc = resolveApiUrl((item as any).audio_url);
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
                          {audioSrc ? (
                            <>
                              <AudioPlayer
                                src={audioSrc}
                                isPlaying={active && isPlaying}
                                onToggle={() => toggleAudio(audioId, audioSrc)}
                                progress={active ? audioProgress : 0}
                                currentTime={active ? audioCurrent : 0}
                                duration={active ? audioDuration : 0}
                                onSeek={seekAudio}
                              />
                              <a
                                href={audioSrc}
                                download
                                className="mt-2 inline-block text-xs text-sacred-gold hover:text-sacred-gold-light underline"
                              >
                                Download Audio
                              </a>
                            </>
                          ) : (
                            <p className="mt-3 text-xs text-cosmic-text-muted">Audio not available</p>
                          )}
                        </CardContent>
                      </Card>
                    );
                  })}
                </div>
              </TabsContent>
              <TabsContent value="chalisa" className="mt-0">
                <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                  {chalisa.map((item, index) => (
                    <Card key={index} className="group card-sacred border-sacred-gold/15 hover:border-sacred-gold/40 transition-all text-center">
                      <CardContent className="p-6">
                        <div className="w-12 h-12 rounded-xl bg-sacred-gold/10 flex items-center justify-center mx-auto mb-4 border border-sacred-gold/20">
                          <BookOpen className="w-6 h-6 text-sacred-gold" />
                        </div>
                        <h3 className="text-lg font-sacred font-semibold text-cosmic-text mb-1">{item.name}</h3>
                        <p className="text-sm text-cosmic-text-secondary">{item.deity}</p>
                        {item.benefit && <span className="text-xs text-sacred-gold mt-2 inline-block">{item.benefit}</span>}
                        {item.audio_url && (
                          <a
                            href={resolveApiUrl(item.audio_url)}
                            download
                            className="mt-2 inline-block text-xs text-sacred-gold hover:text-sacred-gold-light underline"
                          >
                            Download Audio
                          </a>
                        )}
                      </CardContent>
                    </Card>
                  ))}
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
