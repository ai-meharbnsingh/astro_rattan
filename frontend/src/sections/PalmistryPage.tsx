import { useEffect, useMemo, useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import {
  Hand,
  Sparkles,
  BookOpen,
  Loader2,
  Upload,
  Check,
  Heart,
  Brain,
  Activity,
  Briefcase,
  Star,
  AlertTriangle,
  Camera,
} from 'lucide-react';
import { api, resolveApiUrl } from '@/lib/api';

interface PalmistryGuide {
  meanings: Record<string, string>;
  lines: Array<{
    name: string;
    location: string;
    meanings: Record<string, string>;
  }>;
  mounts: Array<{
    name: string;
    location: string;
    planet: string;
    meaning: string;
  }>;
  shapes: Array<{
    name: string;
    features: string;
    meaning: string;
  }>;
}

interface PalmistryReading {
  hand_type: { type: string; meaning: string };
  personality: { mental_approach: string };
  relationships: { emotional_style: string };
  life_path: { vitality: string };
  career: { destiny: string; success?: string };
  strengths: string[];
  challenges: string[];
  overall: string;
}

interface ImageAnalysis {
  image_url: string;
  image_quality: string;
  confidence: string;
  visual_observations: string[];
  derived_traits: {
    hand_shape: string;
    finger_length: string;
    heart_line: string;
    head_line: string;
    life_line: string;
    fate_line?: string;
    sun_line?: string;
    mounts_prominent: string[];
  };
  metrics: {
    brightness: number;
    contrast: number;
    edge_density: number;
  };
}

const HAND_SHAPES = [
  { id: 'earth', name: 'Earth Hand', features: 'Square palm, short fingers', icon: '🌍' },
  { id: 'air', name: 'Air Hand', features: 'Square palm, long fingers', icon: '💨' },
  { id: 'water', name: 'Water Hand', features: 'Rectangular palm, long fingers', icon: '💧' },
  { id: 'fire', name: 'Fire Hand', features: 'Rectangular palm, short fingers', icon: '🔥' },
];

const LINE_OPTIONS = {
  heart: [
    { id: 'long_curved', label: 'Long & Curved', desc: 'Warm, expressive' },
    { id: 'short_straight', label: 'Short & Straight', desc: 'Practical, stable' },
    { id: 'broken', label: 'Broken', desc: 'Emotional growth through challenges' },
    { id: 'chained', label: 'Chained', desc: 'Deeply sensitive' },
    { id: 'forked', label: 'Forked', desc: 'Balances head and heart' },
  ],
  head: [
    { id: 'long_straight', label: 'Long & Straight', desc: 'Logical, analytical' },
    { id: 'short', label: 'Short', desc: 'Action-oriented' },
    { id: 'curved', label: 'Curved', desc: 'Creative, imaginative' },
    { id: 'broken', label: 'Broken', desc: 'Adaptive thinker' },
    { id: 'double', label: 'Double', desc: 'Exceptional mental power' },
  ],
  life: [
    { id: 'long_deep', label: 'Long & Deep', desc: 'Strong vitality' },
    { id: 'short_shallow', label: 'Short & Shallow', desc: 'Moderate energy' },
    { id: 'curved', label: 'Curved', desc: 'Enthusiastic' },
    { id: 'broken', label: 'Broken', desc: 'Major life changes' },
    { id: 'multiple', label: 'Multiple', desc: 'Extra vitality' },
  ],
  fate: [
    { id: 'deep_clear', label: 'Deep & Clear', desc: 'Strong career path' },
    { id: 'broken', label: 'Broken', desc: 'Career changes' },
    { id: 'starts_life', label: 'Starts at Life Line', desc: 'Self-made success' },
    { id: 'starts_base', label: 'Starts at Base', desc: 'Public life' },
    { id: 'absent', label: 'Absent', desc: 'Freedom-loving' },
  ],
  sun: [
    { id: 'present', label: 'Present & Clear', desc: 'Recognition potential' },
    { id: 'multiple', label: 'Multiple', desc: 'Diverse interests' },
    { id: 'absent', label: 'Absent', desc: 'Success through effort' },
  ],
};

const MOUNTS = [
  { id: 'jupiter', name: 'Jupiter', meaning: 'Leadership' },
  { id: 'saturn', name: 'Saturn', meaning: 'Wisdom' },
  { id: 'apollo', name: 'Apollo', meaning: 'Creativity' },
  { id: 'mercury', name: 'Mercury', meaning: 'Communication' },
  { id: 'venus', name: 'Venus', meaning: 'Love' },
  { id: 'moon', name: 'Moon', meaning: 'Intuition' },
  { id: 'mars_upper', name: 'Upper Mars', meaning: 'Moral courage' },
  { id: 'mars_lower', name: 'Lower Mars', meaning: 'Physical courage' },
];

const toLabel = (value?: string) => value?.replace(/_/g, ' ') || '';

export default function PalmistryPage() {
  const [guide, setGuide] = useState<PalmistryGuide | null>(null);
  const [activeTab, setActiveTab] = useState('analysis');
  const [analyzing, setAnalyzing] = useState(false);
  const [imageAnalyzing, setImageAnalyzing] = useState(false);
  const [reading, setReading] = useState<PalmistryReading | null>(null);
  const [imageAnalysis, setImageAnalysis] = useState<ImageAnalysis | null>(null);
  const [manualError, setManualError] = useState('');
  const [imageError, setImageError] = useState('');

  const [handShape, setHandShape] = useState('');
  const [dominantHand, setDominantHand] = useState('right');
  const [fingerLength, setFingerLength] = useState('');
  const [heartLine, setHeartLine] = useState('');
  const [headLine, setHeadLine] = useState('');
  const [lifeLine, setLifeLine] = useState('');
  const [fateLine, setFateLine] = useState('');
  const [sunLine, setSunLine] = useState('');
  const [prominentMounts, setProminentMounts] = useState<string[]>([]);
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [selectedImageUrl, setSelectedImageUrl] = useState('');

  useEffect(() => {
    api.get('/api/palmistry/guide')
      .then(data => setGuide(data))
      .catch(() => {});
  }, []);

  useEffect(() => {
    if (!selectedImage) {
      setSelectedImageUrl('');
      return;
    }
    const url = URL.createObjectURL(selectedImage);
    setSelectedImageUrl(url);
    return () => URL.revokeObjectURL(url);
  }, [selectedImage]);

  const displayedImage = useMemo(
    () => selectedImageUrl || resolveApiUrl(imageAnalysis?.image_url),
    [imageAnalysis?.image_url, selectedImageUrl],
  );

  const applyDerivedTraits = (traits: ImageAnalysis['derived_traits']) => {
    setHandShape(traits.hand_shape);
    setFingerLength(traits.finger_length);
    setHeartLine(traits.heart_line);
    setHeadLine(traits.head_line);
    setLifeLine(traits.life_line);
    setFateLine(traits.fate_line || '');
    setSunLine(traits.sun_line || '');
    setProminentMounts(traits.mounts_prominent || []);
  };

  const handleAnalyze = async () => {
    if (!handShape || !heartLine || !headLine || !lifeLine) {
      setManualError('Select hand shape plus heart, head, and life lines before requesting a reading.');
      return;
    }

    setManualError('');
    setAnalyzing(true);
    try {
      const result = await api.post('/api/palmistry/analyze', {
        hand_shape: handShape,
        dominant_hand: dominantHand,
        finger_length: fingerLength || 'average',
        heart_line: heartLine,
        head_line: headLine,
        life_line: lifeLine,
        fate_line: fateLine || undefined,
        sun_line: sunLine || undefined,
        mounts_prominent: prominentMounts,
      });
      setReading(result.reading);
      setActiveTab('results');
    } catch (err) {
      setManualError(err instanceof Error ? err.message : 'Analysis failed');
    } finally {
      setAnalyzing(false);
    }
  };

  const handleImageAnalyze = async () => {
    if (!selectedImage) {
      setImageError('Upload a clear palm photo before starting photo analysis.');
      return;
    }

    setImageError('');
    setImageAnalyzing(true);
    try {
      const formData = new FormData();
      formData.append('file', selectedImage);
      formData.append('dominant_hand', dominantHand);
      const result = await api.postForm('/api/palmistry/analyze-image', formData);
      setReading(result.reading);
      setImageAnalysis(result.image_analysis);
      applyDerivedTraits(result.image_analysis.derived_traits);
      setActiveTab('results');
    } catch (err) {
      setImageError(err instanceof Error ? err.message : 'Photo analysis failed');
    } finally {
      setImageAnalyzing(false);
    }
  };

  const toggleMount = (mount: string) => {
    setProminentMounts(prev =>
      prev.includes(mount)
        ? prev.filter(item => item !== mount)
        : [...prev, mount]
    );
  };

  return (
    <section className="max-w-5xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
      <div className="text-center mb-10">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-minimal-indigo/10 text-minimal-indigo text-sm font-medium mb-4">
          <Hand className="w-4 h-4" />Chiromancy
        </div>
        <h1 className="text-3xl sm:text-4xl font-display font-bold text-minimal-gray-900 mb-3">
          Palmistry <span className="text-gradient-indigo">Reading</span>
        </h1>
        <p className="text-minimal-gray-500 max-w-2xl mx-auto">
          Upload a palm photo for image-driven analysis or refine the reading manually with guided palm markers.
        </p>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full max-w-md mx-auto grid-cols-3 mb-8">
          <TabsTrigger value="analysis" className="data-[state=active]:bg-minimal-indigo data-[state=active]:text-white">
            <Sparkles className="w-4 h-4 mr-2" />Analysis
          </TabsTrigger>
          <TabsTrigger value="guide" className="data-[state=active]:bg-minimal-indigo data-[state=active]:text-white">
            <BookOpen className="w-4 h-4 mr-2" />Guide
          </TabsTrigger>
          <TabsTrigger value="results" disabled={!reading} className="data-[state=active]:bg-minimal-indigo data-[state=active]:text-white">
            <Star className="w-4 h-4 mr-2" />Results
          </TabsTrigger>
        </TabsList>

        <TabsContent value="analysis" className="space-y-6">
          <Card className="border-0 shadow-soft bg-gradient-to-br from-minimal-indigo/5 to-minimal-violet/5">
            <CardContent className="p-6">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-12 h-12 rounded-xl bg-minimal-indigo text-white flex items-center justify-center">
                  <Camera className="w-6 h-6" />
                </div>
                <div>
                  <h3 className="text-lg font-display font-semibold text-minimal-gray-900">Photo Reading</h3>
                  <p className="text-sm text-minimal-gray-500">Upload one clear palm image with fingers visible.</p>
                </div>
              </div>
              <div className="grid lg:grid-cols-[1.2fr_0.8fr] gap-6">
                <div className="space-y-4">
                  <label className="flex flex-col items-center justify-center rounded-2xl border-2 border-dashed border-minimal-indigo/30 bg-white/80 px-6 py-8 text-center cursor-pointer hover:border-minimal-indigo transition-colors">
                    <Upload className="w-8 h-8 text-minimal-indigo mb-3" />
                    <p className="font-medium text-minimal-gray-900">Select palm photo</p>
                    <p className="text-sm text-minimal-gray-500 mt-1">PNG, JPG, or WEBP up to 5 MB</p>
                    <input
                      type="file"
                      accept="image/png,image/jpeg,image/webp"
                      className="hidden"
                      onChange={(event) => setSelectedImage(event.target.files?.[0] || null)}
                    />
                  </label>
                  {imageError && (
                    <p className="text-sm text-red-600">{imageError}</p>
                  )}
                  <Button
                    onClick={handleImageAnalyze}
                    disabled={imageAnalyzing || !selectedImage}
                    className="w-full bg-minimal-indigo text-white hover:bg-minimal-violet"
                  >
                    {imageAnalyzing ? (
                      <><Loader2 className="w-4 h-4 mr-2 animate-spin" />Analyzing photo...</>
                    ) : (
                      <><Camera className="w-4 h-4 mr-2" />Analyze Palm Photo</>
                    )}
                  </Button>
                </div>
                <div className="rounded-2xl bg-white/80 border border-minimal-gray-200 overflow-hidden min-h-56 flex items-center justify-center">
                  {displayedImage ? (
                    <img src={displayedImage} alt="Palm preview" className="w-full h-full object-cover" />
                  ) : (
                    <div className="text-center px-6">
                      <Hand className="w-10 h-10 text-minimal-gray-300 mx-auto mb-3" />
                      <p className="text-sm text-minimal-gray-500">Your uploaded palm preview appears here.</p>
                    </div>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-soft">
            <CardContent className="p-6">
              <h3 className="text-lg font-display font-semibold text-minimal-gray-900 mb-4">Dominant Hand</h3>
              <div className="flex gap-4">
                {['right', 'left'].map((hand) => (
                  <button
                    key={hand}
                    onClick={() => setDominantHand(hand)}
                    className={`flex-1 p-4 rounded-xl border-2 capitalize transition-all ${
                      dominantHand === hand
                        ? 'border-minimal-indigo bg-minimal-indigo/5'
                        : 'border-minimal-gray-200 hover:border-minimal-gray-300'
                    }`}
                  >
                    <Hand className={`w-6 h-6 mb-2 ${hand === 'right' ? 'rotate-0' : 'scale-x-[-1]'}`} />
                    <p className="font-medium text-minimal-gray-900">{hand} Hand</p>
                  </button>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-soft">
            <CardContent className="p-6">
              <div className="flex items-center justify-between gap-4 mb-4">
                <div>
                  <h3 className="text-lg font-display font-semibold text-minimal-gray-900">Hand Shape</h3>
                  <p className="text-sm text-minimal-gray-500">Use the photo-derived selections or refine them manually.</p>
                </div>
                {imageAnalysis && (
                  <div className="text-sm text-minimal-indigo">
                    Photo confidence: <span className="font-semibold capitalize">{imageAnalysis.confidence}</span>
                  </div>
                )}
              </div>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                {HAND_SHAPES.map((shape) => (
                  <button
                    key={shape.id}
                    onClick={() => setHandShape(shape.id)}
                    className={`p-4 rounded-xl border-2 text-left transition-all ${
                      handShape === shape.id
                        ? 'border-minimal-indigo bg-minimal-indigo/5'
                        : 'border-minimal-gray-200 hover:border-minimal-gray-300'
                    }`}
                  >
                    <span className="text-2xl mb-2 block">{shape.icon}</span>
                    <p className="font-medium text-minimal-gray-900 text-sm">{shape.name}</p>
                    <p className="text-xs text-minimal-gray-500">{shape.features}</p>
                  </button>
                ))}
              </div>
            </CardContent>
          </Card>

          <div className="grid md:grid-cols-2 gap-6">
            {[
              { title: 'Heart Line', icon: Heart, iconClass: 'text-rose-500', selectedClass: 'border-rose-500 bg-rose-50', key: 'heart', value: heartLine, setter: setHeartLine },
              { title: 'Head Line', icon: Brain, iconClass: 'text-blue-500', selectedClass: 'border-blue-500 bg-blue-50', key: 'head', value: headLine, setter: setHeadLine },
              { title: 'Life Line', icon: Activity, iconClass: 'text-green-500', selectedClass: 'border-green-500 bg-green-50', key: 'life', value: lifeLine, setter: setLifeLine },
              { title: 'Fate Line (Optional)', icon: Briefcase, iconClass: 'text-amber-500', selectedClass: 'border-amber-500 bg-amber-50', key: 'fate', value: fateLine, setter: setFateLine },
            ].map(({ title, icon: Icon, iconClass, selectedClass, key, value, setter }) => (
              <Card key={title} className="border-0 shadow-soft">
                <CardContent className="p-6">
                  <h3 className="text-lg font-display font-semibold text-minimal-gray-900 mb-4 flex items-center gap-2">
                    <Icon className={`w-5 h-5 ${iconClass}`} />
                    {title}
                  </h3>
                  <div className="space-y-2">
                    {(LINE_OPTIONS[key as keyof typeof LINE_OPTIONS] || []).map((option) => (
                      <button
                        key={option.id}
                        onClick={() => setter(key === 'fate' ? (option.id === value ? '' : option.id) : option.id)}
                        className={`w-full p-3 rounded-lg border text-left transition-all ${
                          value === option.id
                            ? selectedClass
                            : 'border-minimal-gray-200 hover:border-minimal-gray-300'
                        }`}
                      >
                        <p className="font-medium text-minimal-gray-900 text-sm">{option.label}</p>
                        <p className="text-xs text-minimal-gray-500">{option.desc}</p>
                      </button>
                    ))}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          <Card className="border-0 shadow-soft">
            <CardContent className="p-6">
              <h3 className="text-lg font-display font-semibold text-minimal-gray-900 mb-4">Sun Line (Optional)</h3>
              <div className="grid md:grid-cols-3 gap-3">
                {LINE_OPTIONS.sun.map((option) => (
                  <button
                    key={option.id}
                    onClick={() => setSunLine(option.id === sunLine ? '' : option.id)}
                    className={`p-3 rounded-lg border text-left transition-all ${
                      sunLine === option.id
                        ? 'border-minimal-indigo bg-minimal-indigo/5'
                        : 'border-minimal-gray-200 hover:border-minimal-gray-300'
                    }`}
                  >
                    <p className="font-medium text-minimal-gray-900 text-sm">{option.label}</p>
                    <p className="text-xs text-minimal-gray-500">{option.desc}</p>
                  </button>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-soft">
            <CardContent className="p-6">
              <h3 className="text-lg font-display font-semibold text-minimal-gray-900 mb-4">
                Prominent Mounts (Select all that apply)
              </h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                {MOUNTS.map((mount) => (
                  <button
                    key={mount.id}
                    onClick={() => toggleMount(mount.id)}
                    className={`p-3 rounded-lg border text-left transition-all ${
                      prominentMounts.includes(mount.id)
                        ? 'border-minimal-indigo bg-minimal-indigo/5'
                        : 'border-minimal-gray-200 hover:border-minimal-gray-300'
                    }`}
                  >
                    <div className="flex items-center gap-2">
                      {prominentMounts.includes(mount.id) && <Check className="w-4 h-4 text-minimal-indigo" />}
                      <div>
                        <p className="font-medium text-minimal-gray-900 text-sm">{mount.name}</p>
                        <p className="text-xs text-minimal-gray-500">{mount.meaning}</p>
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            </CardContent>
          </Card>

          {manualError && (
            <p className="text-sm text-red-600">{manualError}</p>
          )}

          <Button
            onClick={handleAnalyze}
            disabled={analyzing || !handShape || !heartLine || !headLine || !lifeLine}
            className="w-full bg-minimal-indigo text-white hover:bg-minimal-violet py-6 text-lg"
          >
            {analyzing ? (
              <><Loader2 className="w-5 h-5 mr-2 animate-spin" />Analyzing...</>
            ) : (
              <><Sparkles className="w-5 h-5 mr-2" />Get My Guided Reading</>
            )}
          </Button>
        </TabsContent>

        <TabsContent value="guide" className="space-y-6">
          {guide ? (
            <>
              <Card className="border-0 shadow-soft">
                <CardContent className="p-6">
                  <h3 className="text-lg font-display font-semibold text-minimal-gray-900 mb-4">Hand Shapes</h3>
                  <div className="grid md:grid-cols-2 gap-4">
                    {guide.shapes.map((shape) => (
                      <div key={shape.name} className="p-4 bg-minimal-gray-50 rounded-xl">
                        <p className="font-semibold text-minimal-gray-900">{shape.name}</p>
                        <p className="text-sm text-minimal-gray-500">{shape.features}</p>
                        <p className="text-sm text-minimal-gray-600 mt-2">{shape.meaning}</p>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              <Card className="border-0 shadow-soft">
                <CardContent className="p-6">
                  <h3 className="text-lg font-display font-semibold text-minimal-gray-900 mb-4">Major Lines</h3>
                  <div className="space-y-4">
                    {guide.lines.map((line) => (
                      <div key={line.name} className="p-4 bg-minimal-gray-50 rounded-xl">
                        <p className="font-semibold text-minimal-gray-900">{line.name}</p>
                        <p className="text-sm text-minimal-gray-500 mb-2">{line.location}</p>
                        <ul className="text-sm text-minimal-gray-600 space-y-1">
                          {Object.entries(line.meanings).map(([key, meaning]) => (
                            <li key={key}>• <span className="capitalize">{key.replace(/_/g, ' ')}</span>: {meaning}</li>
                          ))}
                        </ul>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              <Card className="border-0 shadow-soft">
                <CardContent className="p-6">
                  <h3 className="text-lg font-display font-semibold text-minimal-gray-900 mb-4">Mounts of the Palm</h3>
                  <div className="grid md:grid-cols-2 gap-4">
                    {guide.mounts.map((mount) => (
                      <div key={mount.name} className="p-4 bg-minimal-gray-50 rounded-xl">
                        <p className="font-semibold text-minimal-gray-900">{mount.name}</p>
                        <p className="text-sm text-minimal-gray-500">{mount.location} • Planet: {mount.planet}</p>
                        <p className="text-sm text-minimal-gray-600 mt-1">{mount.meaning}</p>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </>
          ) : (
            <div className="flex items-center justify-center py-16">
              <Loader2 className="w-8 h-8 text-minimal-indigo animate-spin" />
            </div>
          )}
        </TabsContent>

        <TabsContent value="results" className="space-y-6">
          {reading && (
            <>
              <Card className="border-0 shadow-soft bg-gradient-to-br from-minimal-indigo/5 to-minimal-violet/5">
                <CardContent className="p-6">
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-12 h-12 rounded-full bg-minimal-indigo text-white flex items-center justify-center">
                      <Sparkles className="w-6 h-6" />
                    </div>
                    <div>
                      <h3 className="text-xl font-display font-bold text-minimal-gray-900">Your Palm Reading</h3>
                      <p className="text-sm text-minimal-gray-500">
                        {imageAnalysis ? 'Photo-derived interpretation with guided palm markers' : 'Guided palm analysis'}
                      </p>
                    </div>
                  </div>
                  <p className="text-minimal-gray-700 leading-relaxed">{reading.overall}</p>
                </CardContent>
              </Card>

              {imageAnalysis && (
                <Card className="border-0 shadow-soft">
                  <CardContent className="p-6">
                    <div className="grid lg:grid-cols-[0.9fr_1.1fr] gap-6">
                      <div className="space-y-4">
                        {displayedImage && (
                          <img src={displayedImage} alt="Analyzed palm" className="w-full rounded-2xl border border-minimal-gray-200 object-cover" />
                        )}
                        <div className="grid grid-cols-3 gap-3 text-center">
                          <div className="rounded-xl bg-minimal-gray-50 p-3">
                            <p className="text-xs text-minimal-gray-500">Quality</p>
                            <p className="font-semibold capitalize text-minimal-gray-900">{imageAnalysis.image_quality}</p>
                          </div>
                          <div className="rounded-xl bg-minimal-gray-50 p-3">
                            <p className="text-xs text-minimal-gray-500">Confidence</p>
                            <p className="font-semibold capitalize text-minimal-gray-900">{imageAnalysis.confidence}</p>
                          </div>
                          <div className="rounded-xl bg-minimal-gray-50 p-3">
                            <p className="text-xs text-minimal-gray-500">Edge Density</p>
                            <p className="font-semibold text-minimal-gray-900">{imageAnalysis.metrics.edge_density}</p>
                          </div>
                        </div>
                      </div>
                      <div className="space-y-4">
                        <div>
                          <h4 className="font-display font-semibold text-minimal-gray-900 mb-2">Detected Traits</h4>
                          <div className="flex flex-wrap gap-2">
                            {[imageAnalysis.derived_traits.hand_shape, imageAnalysis.derived_traits.finger_length, imageAnalysis.derived_traits.heart_line, imageAnalysis.derived_traits.head_line, imageAnalysis.derived_traits.life_line]
                              .filter(Boolean)
                              .map((trait) => (
                                <span key={trait} className="px-3 py-1 rounded-full bg-minimal-indigo/10 text-minimal-indigo text-sm capitalize">
                                  {toLabel(trait)}
                                </span>
                              ))}
                          </div>
                        </div>
                        <div>
                          <h4 className="font-display font-semibold text-minimal-gray-900 mb-2">Visual Observations</h4>
                          <ul className="space-y-2 text-sm text-minimal-gray-600">
                            {imageAnalysis.visual_observations.map((observation) => (
                              <li key={observation} className="flex gap-2">
                                <Check className="w-4 h-4 text-minimal-indigo mt-0.5" />
                                <span>{observation}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )}

              <div className="grid md:grid-cols-2 gap-6">
                <Card className="border-0 shadow-soft">
                  <CardContent className="p-6">
                    <h4 className="font-display font-semibold text-minimal-gray-900 mb-3 flex items-center gap-2">
                      <Hand className="w-5 h-5 text-minimal-indigo" />
                      Hand Type
                    </h4>
                    <p className="text-minimal-gray-700">{reading.hand_type.meaning}</p>
                  </CardContent>
                </Card>

                <Card className="border-0 shadow-soft">
                  <CardContent className="p-6">
                    <h4 className="font-display font-semibold text-minimal-gray-900 mb-3 flex items-center gap-2">
                      <Brain className="w-5 h-5 text-blue-500" />
                      Mental Approach
                    </h4>
                    <p className="text-minimal-gray-700">{reading.personality.mental_approach}</p>
                  </CardContent>
                </Card>

                <Card className="border-0 shadow-soft">
                  <CardContent className="p-6">
                    <h4 className="font-display font-semibold text-minimal-gray-900 mb-3 flex items-center gap-2">
                      <Heart className="w-5 h-5 text-rose-500" />
                      Relationships
                    </h4>
                    <p className="text-minimal-gray-700">{reading.relationships.emotional_style}</p>
                  </CardContent>
                </Card>

                <Card className="border-0 shadow-soft">
                  <CardContent className="p-6">
                    <h4 className="font-display font-semibold text-minimal-gray-900 mb-3 flex items-center gap-2">
                      <Activity className="w-5 h-5 text-green-500" />
                      Life Energy
                    </h4>
                    <p className="text-minimal-gray-700">{reading.life_path.vitality}</p>
                  </CardContent>
                </Card>

                <Card className="border-0 shadow-soft">
                  <CardContent className="p-6">
                    <h4 className="font-display font-semibold text-minimal-gray-900 mb-3 flex items-center gap-2">
                      <Briefcase className="w-5 h-5 text-amber-500" />
                      Career Path
                    </h4>
                    <p className="text-minimal-gray-700">{reading.career.destiny}</p>
                    {reading.career.success && (
                      <p className="text-minimal-gray-600 mt-2">{reading.career.success}</p>
                    )}
                  </CardContent>
                </Card>

                {reading.strengths.length > 0 && (
                  <Card className="border-0 shadow-soft">
                    <CardContent className="p-6">
                      <h4 className="font-display font-semibold text-minimal-gray-900 mb-3 flex items-center gap-2">
                        <Star className="w-5 h-5 text-yellow-500" />
                        Key Strengths
                      </h4>
                      <ul className="space-y-1">
                        {reading.strengths.map((strength) => (
                          <li key={strength} className="text-minimal-gray-700 flex items-center gap-2">
                            <Check className="w-4 h-4 text-green-500" /> {strength}
                          </li>
                        ))}
                      </ul>
                    </CardContent>
                  </Card>
                )}
              </div>

              {reading.challenges.length > 0 && (
                <Card className="border-0 shadow-soft border-l-4 border-l-amber-500">
                  <CardContent className="p-6">
                    <h4 className="font-display font-semibold text-minimal-gray-900 mb-3 flex items-center gap-2">
                      <AlertTriangle className="w-5 h-5 text-amber-500" />
                      Growth Areas
                    </h4>
                    <ul className="space-y-1">
                      {reading.challenges.map((challenge) => (
                        <li key={challenge} className="text-minimal-gray-700">• {challenge}</li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>
              )}

              <Button onClick={() => setActiveTab('analysis')} variant="outline" className="w-full">
                Start Another Reading
              </Button>
            </>
          )}
        </TabsContent>
      </Tabs>
    </section>
  );
}
