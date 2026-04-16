import { Hash, Palette, Clock, Users, Gem, BookOpen } from 'lucide-react';

interface LuckyMetadataProps {
  lucky: {
    number: number;
    color: { en: string; hi: string };
    time: { en: string; hi: string };
    compatible_sign: { en: string; hi: string };
    gemstone: { en: string; hi: string };
    mantra: string;
  };
  language: string;
  t: (key: string) => string;
}

const ITEMS = [
  { key: 'number', icon: Hash, chipBg: 'bg-amber-100 text-amber-800' },
  { key: 'color', icon: Palette, chipBg: 'bg-pink-100 text-pink-800' },
  { key: 'time', icon: Clock, chipBg: 'bg-blue-100 text-blue-800' },
  { key: 'compatible_sign', icon: Users, chipBg: 'bg-green-100 text-green-800' },
  { key: 'gemstone', icon: Gem, chipBg: 'bg-purple-100 text-purple-800' },
  { key: 'mantra', icon: BookOpen, chipBg: 'bg-sacred-gold/20 text-sacred-gold-dark' },
] as const;

const LABEL_KEYS: Record<string, string> = {
  number: 'auto.luckyNumber',
  color: 'auto.luckyColor',
  time: 'auto.luckyTime',
  compatible_sign: 'auto.compatibleSign',
  gemstone: 'auto.gemstone',
  mantra: 'auto.mantra',
};

export default function LuckyMetadataCard({ lucky, language, t }: LuckyMetadataProps) {
  const getValue = (key: string): string => {
    if (key === 'number') return String(lucky.number);
    if (key === 'mantra') return lucky.mantra;
    const field = lucky[key as keyof typeof lucky];
    if (field && typeof field === 'object' && 'en' in field) {
      return language === 'hi' ? field.hi : field.en;
    }
    return '';
  };

  return (
    <div className="rounded-xl border bg-gradient-to-r from-sacred-gold/5 to-amber-50 p-4">
      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
        {ITEMS.map(({ key, icon: Icon, chipBg }) => (
          <div key={key} className="flex items-start gap-2">
            <div className={`rounded-lg p-1.5 ${chipBg}`}>
              <Icon className="w-3.5 h-3.5" />
            </div>
            <div className="min-w-0">
              <p className="text-[11px] text-muted-foreground leading-tight">{t(LABEL_KEYS[key])}</p>
              <p className="text-sm font-medium text-foreground truncate">{getValue(key)}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
