import { Button } from '@/components/ui/button';
import { Sparkles, ChevronRight, Clock } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';

interface KundliListProps {
  savedKundlis: any[];
  onLoadKundli: (kundli: any) => void;
  onNewKundli: () => void;
  onPrashnaKundli: () => void;
}

export default function KundliList({
  savedKundlis,
  onLoadKundli,
  onNewKundli,
  onPrashnaKundli,
}: KundliListProps) {
  const { t } = useTranslation();

  return (
    <div className="max-w-2xl mx-auto py-24 px-4 bg-transparent">
      <div className="text-center mb-8">
        <div className="w-16 h-16 rounded-full bg-gradient-to-br from-sacred-gold to-sacred-saffron flex items-center justify-center mx-auto mb-4">
          <Sparkles className="w-8 h-8 text-[#1a1a2e]" />
        </div>
        <h3 className="text-2xl font-display font-bold text-sacred-brown mb-2">My Kundlis</h3>
        <p className="text-sacred-text-secondary">Your saved birth charts</p>
      </div>
      <div className="space-y-3 mb-6">
        {savedKundlis.map((k: any) => (
          <button key={k.id} onClick={() => onLoadKundli(k)}
            className="w-full text-left p-4 bg-sacred-cream rounded-xl border border-sacred-gold/20 hover:border-sacred-gold/50 transition-colors">
            <div className="flex items-center justify-between">
              <div>
                <h4 className="font-display font-semibold text-sacred-brown">{k.person_name}</h4>
                <p className="text-sm text-sacred-text-secondary">{k.birth_date} | {k.birth_time} | {k.birth_place}</p>
              </div>
              <ChevronRight className="w-5 h-5 text-sacred-gold" />
            </div>
          </button>
        ))}
      </div>
      <Button onClick={onNewKundli} className="w-full btn-sacred">
        <Sparkles className="w-5 h-5 mr-2" />Generate New Kundli
      </Button>
      <Button onClick={onPrashnaKundli} variant="outline" className="w-full mt-3 border-sacred-gold/50 text-sacred-brown hover:bg-sacred-gold/10">
        <Clock className="w-5 h-5 mr-2 text-sacred-gold" />{t('kundli.prashnaKundli')}
        <span className="ml-2 text-xs text-sacred-text-secondary">{t('kundli.prashnaSubtitle')}</span>
      </Button>
    </div>
  );
}
