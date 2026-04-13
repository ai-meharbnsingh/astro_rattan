import { useState } from 'react';
import { Compass, Home, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useTranslation } from '@/lib/i18n';
import VastuCompass from './VastuCompass';

export interface VastuFormData {
  buildingType: 'residential' | 'commercial' | 'temple';
  entranceDirection: string;
  entranceDegrees: number | null;
  problems: string[];
}

interface Props {
  onGenerate: (formData: VastuFormData) => void;
  loading: boolean;
}

const DIRECTIONS = [
  { code: 'N',  en: 'North',     hi: 'उत्तर' },
  { code: 'NE', en: 'Northeast', hi: 'ईशान' },
  { code: 'E',  en: 'East',      hi: 'पूर्व' },
  { code: 'SE', en: 'Southeast', hi: 'आग्नेय' },
  { code: 'S',  en: 'South',     hi: 'दक्षिण' },
  { code: 'SW', en: 'Southwest', hi: 'नैऋत्य' },
  { code: 'W',  en: 'West',      hi: 'पश्चिम' },
  { code: 'NW', en: 'Northwest', hi: 'वायव्य' },
];

const PROBLEMS = [
  { key: 'wealth',       en: 'Wealth / Finance',   hi: 'धन / वित्त' },
  { key: 'health',       en: 'Health',              hi: 'स्वास्थ्य' },
  { key: 'relationship', en: 'Relationships',       hi: 'रिश्ते' },
  { key: 'career',       en: 'Career',              hi: 'करियर' },
  { key: 'education',    en: 'Education',           hi: 'शिक्षा' },
  { key: 'legal',        en: 'Legal Issues',        hi: 'कानूनी मामले' },
  { key: 'sleep',        en: 'Sleep Issues',        hi: 'नींद की समस्या' },
  { key: 'conflict',     en: 'Family Conflicts',    hi: 'पारिवारिक विवाद' },
  { key: 'fertility',    en: 'Fertility',           hi: 'संतान' },
  { key: 'depression',   en: 'Depression / Anxiety', hi: 'अवसाद / चिंता' },
  { key: 'debt',         en: 'Debt / Losses',       hi: 'कर्ज / हानि' },
  { key: 'accident',     en: 'Accidents',           hi: 'दुर्घटनाएँ' },
];

const BUILDING_TYPES = [
  { key: 'residential', en: 'Residential (Home)',    hi: 'आवासीय (घर)' },
  { key: 'commercial',  en: 'Commercial (Office)',   hi: 'व्यावसायिक (कार्यालय)' },
  { key: 'temple',      en: 'Temple / Ashram',       hi: 'मंदिर / आश्रम' },
];

export default function VastuForm({ onGenerate, loading }: Props) {
  const { language } = useTranslation();
  const isHi = language === 'hi';

  const [formData, setFormData] = useState<VastuFormData>({
    buildingType: 'residential',
    entranceDirection: 'N',
    entranceDegrees: null,
    problems: [],
  });

  const toggleProblem = (key: string) => {
    setFormData(prev => ({
      ...prev,
      problems: prev.problems.includes(key)
        ? prev.problems.filter(p => p !== key)
        : [...prev.problems, key],
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onGenerate(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-8 max-w-2xl mx-auto">
      {/* Building Type */}
      <div>
        <label className="block text-sm font-semibold text-sacred-gold mb-3">
          <Home className="w-4 h-4 inline mr-1" />
          {isHi ? 'भवन का प्रकार' : 'Building Type'}
        </label>
        <div className="grid grid-cols-3 gap-3">
          {BUILDING_TYPES.map(bt => (
            <button
              key={bt.key}
              type="button"
              onClick={() => setFormData(prev => ({ ...prev, buildingType: bt.key as any }))}
              className={`p-3 rounded-lg border text-sm font-medium transition-all ${
                formData.buildingType === bt.key
                  ? 'border-sacred-gold bg-sacred-gold/10 text-sacred-gold'
                  : 'border-white/10 bg-white/5 text-cosmic-text hover:border-white/30'
              }`}
            >
              {isHi ? bt.hi : bt.en}
            </button>
          ))}
        </div>
      </div>

      {/* Entrance Direction — Compass */}
      <div>
        <label className="block text-sm font-semibold text-sacred-gold mb-3">
          <Compass className="w-4 h-4 inline mr-1" />
          {isHi ? 'मुख्य प्रवेश द्वार की दिशा' : 'Main Entrance Direction'}
        </label>
        <p className="text-xs text-cosmic-text/50 mb-2">
          {isHi ? 'कम्पास पर दिशा क्लिक करें — बाहरी रिंग 32 पद दिखाती है' : 'Click a direction on the compass — outer ring shows 32 padas'}
        </p>
        <VastuCompass
          value={formData.entranceDirection}
          onChange={(dir) => setFormData(prev => ({ ...prev, entranceDirection: dir }))}
          onPadaClick={(_pada, degrees) => setFormData(prev => ({ ...prev, entranceDegrees: degrees }))}
          mode="select"
        />
      </div>

      {/* Optional: Precise Degrees */}
      <div>
        <label className="block text-sm font-semibold text-cosmic-text/70 mb-2">
          {isHi ? 'कम्पास डिग्री (वैकल्पिक, 0-360)' : 'Compass Degrees (optional, 0-360)'}
        </label>
        <input
          type="number"
          min={0}
          max={359.99}
          step={0.1}
          value={formData.entranceDegrees ?? ''}
          onChange={e => setFormData(prev => ({
            ...prev,
            entranceDegrees: e.target.value ? parseFloat(e.target.value) : null,
          }))}
          placeholder={isHi ? 'उदा. 45.5' : 'e.g. 45.5'}
          className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-lg text-white placeholder-white/30 focus:border-sacred-gold focus:outline-none"
        />
      </div>

      {/* Problems Selection */}
      <div>
        <label className="block text-sm font-semibold text-sacred-gold mb-3">
          {isHi ? 'समस्याएँ चुनें (वैकल्पिक)' : 'Select Problems (optional)'}
        </label>
        <p className="text-xs text-cosmic-text/60 mb-3">
          {isHi
            ? 'अपनी समस्याएँ चुनें — हम विशिष्ट वास्तु उपाय सुझाएँगे'
            : 'Select your concerns — we\'ll suggest specific Vastu remedies'}
        </p>
        <div className="grid grid-cols-3 gap-2">
          {PROBLEMS.map(p => (
            <button
              key={p.key}
              type="button"
              onClick={() => toggleProblem(p.key)}
              className={`p-2.5 rounded-lg border text-xs font-medium transition-all ${
                formData.problems.includes(p.key)
                  ? 'border-amber-500 bg-amber-500/10 text-amber-400'
                  : 'border-white/10 bg-white/5 text-cosmic-text hover:border-white/30'
              }`}
            >
              {isHi ? p.hi : p.en}
            </button>
          ))}
        </div>
      </div>

      {/* Submit */}
      <Button
        type="submit"
        disabled={loading}
        className="w-full bg-gradient-to-r from-sacred-gold to-amber-600 text-black font-bold py-3 text-base"
      >
        {loading ? (
          <>
            <Loader2 className="w-5 h-5 mr-2 animate-spin" />
            {isHi ? 'विश्लेषण हो रहा है...' : 'Analyzing...'}
          </>
        ) : (
          isHi ? 'वास्तु विश्लेषण करें' : 'Analyze Vastu'
        )}
      </Button>
    </form>
  );
}
