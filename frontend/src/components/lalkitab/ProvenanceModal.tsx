import { useEffect } from 'react';
import { X, BookOpen, Info } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';

/**
 * ProvenanceModal — explains the Lal Kitab source taxonomy to end-users.
 * Triggered by clicking a SourceBadge. Codex D8 follow-up.
 *
 * Covers the 7 current source values:
 *   LK_CANONICAL, LK_DERIVED, LK_ADAPTED, PRODUCT,
 *   ML_SCORED, HEURISTIC, VEDIC_INFLUENCED (+ legacy vedic_influenced alias)
 *
 * Bilingual EN/HI via useTranslation().language.
 */

interface ProvenanceEntry {
  key: string;
  titleEn: string;
  titleHi: string;
  bodyEn: string;
  bodyHi: string;
  swatch: string; // tailwind classes for colour chip
}

const ENTRIES: ProvenanceEntry[] = [
  {
    key: 'LK_CANONICAL',
    titleEn: 'LK 1952 (Canonical)',
    titleHi: 'लाल किताब 1952 (प्रमाणिक)',
    bodyEn:
      'Quoted directly from the Lal Kitab 1952 text by Pt. Roop Chand Joshi. Highest authority — the rule exists verbatim in canon.',
    bodyHi:
      'पं. रूप चंद जोशी रचित लाल किताब 1952 से सीधे उद्धृत। सर्वोच्च प्रमाण — नियम मूल ग्रंथ में स्पष्ट रूप से मौजूद है।',
    swatch: 'bg-green-100 border-green-300',
  },
  {
    key: 'LK_DERIVED',
    titleEn: 'LK Derived',
    titleHi: 'लाल किताब व्युत्पन्न',
    bodyEn:
      'A logical inference drawn from Lal Kitab principles, but not a verbatim 1952 quote. Follows the spirit of the text, extrapolated to your specific chart.',
    bodyHi:
      'लाल किताब के सिद्धांतों से तार्किक निष्कर्ष — मूल 1952 पाठ का शब्दशः उद्धरण नहीं। ग्रंथ की भावना का पालन, आपकी कुंडली पर लागू।',
    swatch: 'bg-amber-100 border-amber-300',
  },
  {
    key: 'LK_ADAPTED',
    titleEn: 'LK Adapted',
    titleHi: 'लाल किताब अनुकूलित',
    bodyEn:
      'A Lal Kitab rule applied to a modern scenario the 1952 text did not explicitly cover (e.g. a planetary combination ignored by canon). Treat with moderate confidence.',
    bodyHi:
      'लाल किताब नियम एक आधुनिक परिस्थिति पर लागू जिसे 1952 पाठ ने स्पष्ट रूप से नहीं लिखा। मध्यम विश्वास रखें।',
    swatch: 'bg-lime-100 border-lime-300',
  },
  {
    key: 'PRODUCT',
    titleEn: 'Product / UX',
    titleHi: 'प्रोडक्ट / यूएक्स',
    bodyEn:
      'A feature built by this app — e.g. feedback buttons, remedy trackers, visualizations. NOT claimed as Lal Kitab canon; purely user-experience.',
    bodyHi:
      'इस ऐप में निर्मित सुविधा — जैसे फ़ीडबैक बटन, उपाय ट्रैकर, चित्र। लाल किताब का हिस्सा नहीं; पूर्णतः यूज़र-अनुभव।',
    swatch: 'bg-gray-100 border-gray-300',
  },
  {
    key: 'ML_SCORED',
    titleEn: 'ML Scored',
    titleHi: 'एमएल स्कोर',
    bodyEn:
      'A score produced by a statistical or learned model (not a hand-written rule). Useful as a signal, not as canonical truth.',
    bodyHi:
      'सांख्यिकीय या शिक्षित मॉडल द्वारा उत्पादित स्कोर (हस्तलिखित नियम नहीं)। संकेत के रूप में उपयोगी, प्रमाण नहीं।',
    swatch: 'bg-purple-100 border-purple-300',
  },
  {
    key: 'HEURISTIC',
    titleEn: 'Heuristic',
    titleHi: 'अनुभवजन्य',
    bodyEn:
      'Empirical weighting built by engineers based on common astrological practice. Not ML, not canon — a reasonable rule-of-thumb.',
    bodyHi:
      'सामान्य ज्योतिष व्यवहार पर आधारित इंजीनियरों द्वारा निर्मित अनुभवजन्य भार। न एमएल, न प्रमाणिक — एक तर्कसंगत थम्ब-रूल।',
    swatch: 'bg-slate-100 border-slate-300',
  },
  {
    key: 'VEDIC_INFLUENCED',
    titleEn: 'Vedic Overlay',
    titleHi: 'वैदिक ओवरले',
    bodyEn:
      'A classical Vedic rule shown for cross-reference with traditional Parashari / Jaimini systems. NOT part of Lal Kitab 1952; included for users who want to compare.',
    bodyHi:
      'पारंपरिक पराशरी / जैमिनी पद्धति से तुलना हेतु दिखाया गया शास्त्रीय वैदिक नियम। लाल किताब 1952 का अंग नहीं; तुलना चाहने वालों के लिए।',
    swatch: 'bg-indigo-100 border-indigo-300',
  },
];

interface ProvenanceModalProps {
  open: boolean;
  onClose: () => void;
  /** If provided, highlights that entry in the modal. */
  highlight?: string | null;
}

export default function ProvenanceModal({ open, onClose, highlight }: ProvenanceModalProps) {
  const { language } = useTranslation();
  const isHi = language === 'hi';

  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    document.addEventListener('keydown', onKey);
    document.body.style.overflow = 'hidden';
    return () => {
      document.removeEventListener('keydown', onKey);
      document.body.style.overflow = '';
    };
  }, [open, onClose]);

  if (!open) return null;

  // Normalise highlight key (accept both canonical and legacy lowercase vedic)
  const highlightKey =
    highlight && highlight.toLowerCase() === 'vedic_influenced'
      ? 'VEDIC_INFLUENCED'
      : highlight ?? null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="provenance-modal-title"
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm"
      onClick={onClose}
    >
      <div
        className="relative w-full max-w-2xl max-h-[90dvh] overflow-y-auto rounded-2xl bg-white border border-sacred-gold/20 shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="sticky top-0 bg-white border-b border-sacred-gold/20 p-5 flex items-start justify-between gap-4">
          <div>
            <h2
              id="provenance-modal-title"
              className="font-sans text-xl text-sacred-gold flex items-center gap-2"
            >
              <BookOpen className="w-5 h-5" />
              {isHi ? 'स्रोत प्रमाण' : 'Source Provenance'}
            </h2>
            <p className="text-xs text-gray-500 mt-1">
              {isHi
                ? 'प्रत्येक दावा कहाँ से आता है — पारदर्शिता के लिए।'
                : 'Where each claim comes from — for transparency.'}
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg hover:bg-gray-100 transition-colors"
            aria-label={isHi ? 'बंद करें' : 'Close'}
          >
            <X className="w-5 h-5 text-gray-600" />
          </button>
        </div>

        {/* Intro */}
        <div className="p-5 border-b border-gray-100 bg-sacred-gold/5">
          <div className="flex items-start gap-2">
            <Info className="w-4 h-4 text-sacred-gold mt-0.5 flex-shrink-0" />
            <p className="text-sm text-gray-700 leading-relaxed">
              {isHi
                ? 'हर भविष्यवाणी, दोष, या उपाय एक स्रोत से जुड़ा है। पिल पर क्लिक करके स्रोत देखें। नीचे प्रत्येक प्रकार का अर्थ समझें।'
                : 'Every prediction, dosha, and remedy is tagged with its source. Click a pill to see what it means. The categories below explain each type.'}
            </p>
          </div>
        </div>

        {/* Entries */}
        <div className="p-5 space-y-3">
          {ENTRIES.map((e) => {
            const isHighlighted = highlightKey === e.key;
            return (
              <div
                key={e.key}
                className={`rounded-xl border p-4 transition-all ${
                  isHighlighted
                    ? 'border-sacred-gold/60 bg-sacred-gold/10 shadow-sm ring-2 ring-sacred-gold/30'
                    : 'border-gray-200 bg-white'
                }`}
              >
                <div className="flex items-center gap-3 mb-2">
                  <span
                    className={`inline-block w-4 h-4 rounded-full border-2 ${e.swatch}`}
                    aria-hidden="true"
                  />
                  <h3 className="font-sans text-base font-semibold text-sacred-brown">
                    {isHi ? e.titleHi : e.titleEn}
                  </h3>
                  <code className="text-[10px] text-gray-400 font-mono ml-auto">
                    {e.key}
                  </code>
                </div>
                <p className="text-sm text-gray-600 leading-relaxed">
                  {isHi ? e.bodyHi : e.bodyEn}
                </p>
              </div>
            );
          })}
        </div>

        {/* Footer */}
        <div className="sticky bottom-0 bg-white border-t border-gray-100 p-4 text-center">
          <p className="text-xs text-gray-500">
            {isHi
              ? 'लाल किताब 1952 — पं. रूप चंद जोशी द्वारा रचित मूल ग्रंथ।'
              : 'Lal Kitab 1952 — original text by Pt. Roop Chand Joshi.'}
          </p>
        </div>
      </div>
    </div>
  );
}
