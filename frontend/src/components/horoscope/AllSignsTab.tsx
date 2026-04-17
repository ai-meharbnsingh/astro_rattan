import { Heading } from "@/components/ui/heading";
interface SignEntry {
  sign: string;
  sign_hindi: string;
  emoji: string;
  dates: string;
  ruling_planet: string;
  ruling_planet_hindi: string;
  element: string;
  element_hindi: string;
  summary: string;
  sections: Record<string, string>;
}

interface AllSignsData {
  period: string;
  date: string;
  signs: SignEntry[];
}

interface Props {
  data: AllSignsData | null;
  loading: boolean;
  language: string;
  t: (key: string) => string;
  onSelectSign: (sign: string) => void;
}

const ELEMENT_COLORS: Record<string, string> = {
  fire: 'bg-red-100 text-red-700 border-red-200',
  earth: 'bg-green-100 text-green-700 border-green-200',
  air: 'bg-sky-100 text-sky-700 border-sky-200',
  water: 'bg-blue-100 text-blue-700 border-blue-200',
};

function txt(v: unknown, lang: string): string {
  if (typeof v === 'string') return v;
  if (v && typeof v === 'object' && 'en' in v) return (lang === 'hi' ? (v as any).hi : (v as any).en) || '';
  return String(v ?? '');
}

export default function AllSignsTab({ data, loading, language, t, onSelectSign }: Props) {
  if (loading) {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
        {Array.from({ length: 12 }).map((_, i) => (
          <div key={i} className="h-40 animate-pulse bg-gray-200 rounded-xl" />
        ))}
      </div>
    );
  }

  if (!data?.signs?.length) {
    return (
      <div className="text-center py-12 text-muted-foreground">
        {t('auto.noHoroscopeDataAvail')}
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
      {data.signs.map((entry) => {
        const elementClass = ELEMENT_COLORS[entry.element] || 'bg-gray-100 text-foreground border-gray-200';
        return (
          <button
            key={entry.sign}
            onClick={() => onSelectSign(entry.sign)}
            className="text-left rounded-xl border bg-card p-4 hover:border-sacred-gold hover:shadow-md transition-all group"
          >
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2">
                <img
                  src={`/images/zodiac-orange/zodiac-${entry.sign}-orange.png`}
                  alt={entry.sign}
                  className="w-10 h-10 object-contain rounded-md"
                />
                <div>
                  <Heading as={4} variant={4}>
                    {language === 'hi' ? entry.sign_hindi : entry.sign.charAt(0).toUpperCase() + entry.sign.slice(1)}
                  </Heading>
                  <p className="text-[10px] text-muted-foreground">{entry.dates}</p>
                </div>
              </div>
              <span className={`text-[10px] px-1.5 py-0.5 rounded border ${elementClass}`}>
                {language === 'hi' ? entry.element_hindi : entry.element.charAt(0).toUpperCase() + entry.element.slice(1)}
              </span>
            </div>
            <p className="text-xs text-muted-foreground leading-relaxed line-clamp-3">
              {txt(entry.summary, language) || txt(entry.sections?.general, language).slice(0, 160)}
            </p>
            <div className="mt-2 text-[10px] text-sacred-gold-dark font-medium group-hover:underline">
              {t('auto.readFullHoroscope')}
            </div>
          </button>
        );
      })}
    </div>
  );
}
