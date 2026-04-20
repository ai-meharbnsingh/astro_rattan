import { Card, CardContent } from '@/components/ui/card';
import { Calendar, Info, Flame, Leaf, Moon, Sparkles } from 'lucide-react';
import type { FullPanchangData } from '@/sections/Panchang';
import { Heading } from "@/components/ui/heading";
import PanchangTabHeader from './PanchangTabHeader';

interface Props {
  panchang: FullPanchangData;
  language: string;
  t: (key: string) => string;
  selectedDate?: string;
}

export default function FestivalsTab({ panchang, language, t, selectedDate }: Props) {
  const todayFestivals = panchang.festivals || [];

  const getFestivalIcon = (type: string) => {
    const type_lower = type.toLowerCase();
    if (type_lower.includes('fast') || type_lower.includes('vrat')) return Flame;
    if (type_lower.includes('fest')) return Sparkles;
    if (type_lower.includes('moon') || type_lower.includes('purnima') || type_lower.includes('amavasya')) return Moon;
    return Leaf;
  };

  const getFestivalColor = (type: string) => {
    const type_lower = type.toLowerCase();
    if (type_lower.includes('fast') || type_lower.includes('vrat')) return 'text-orange-500 bg-orange-500/10';
    if (type_lower.includes('fest')) return 'text-purple-500 bg-purple-500/10';
    return 'text-green-500 bg-green-500/10';
  };

  return (
    <div className="space-y-4">
      <PanchangTabHeader
        icon={Sparkles}
        title={language === 'hi' ? 'त्योहार और व्रत' : 'Festivals & Vrats'}
        description={language === 'hi'
          ? `चुनी हुई तिथि के त्योहार/व्रत और संबंधित संकेत।${selectedDate ? ` (${selectedDate})` : ''}`
          : `Festivals and vrats for the selected date.${selectedDate ? ` (${selectedDate})` : ''}`}
      />

      {/* Today's Festivals */}
      <Card className="card-sacred border-sacred-gold/30">
        <CardContent className="p-4">
          <h3 className="text-lg font-bold text-foreground mb-4 flex items-center gap-2">
            <Calendar className="h-5 w-5 text-sacred-gold" />
            {language === 'hi' ? 'आज के त्योहार और व्रत' : "Today's Festivals & Vrats"}
          </h3>
          
          {todayFestivals.length > 0 ? (
            <div className="space-y-3">
              {todayFestivals.map((festival, index) => {
                const Icon = getFestivalIcon(festival.type);
                const colorClass = getFestivalColor(festival.type);
                
                return (
                  <div 
                    key={index}
                    className="p-4 rounded-xl bg-card/50 border hover:border-sacred-gold/30 transition-all"
                  >
                    <div className="flex items-start gap-3">
                      <div className={`p-2 rounded-lg ${colorClass}`}>
                        <Icon className="h-5 w-5" />
                      </div>
                      <div className="flex-1">
                        <Heading as={4} variant={4}>
                          {language === 'hi' && festival.name_hindi ? festival.name_hindi : festival.name}
                        </Heading>
                        <span className={`inline-block mt-1 px-2 py-0.5 text-xs rounded-full ${colorClass}`}>
                          {language === 'hi' ? festival.type_hindi || festival.type : festival.type}
                        </span>
                        {((language === 'hi' && festival.description_hindi) || festival.description) && (
                          <p className="text-sm text-muted-foreground mt-2">
                            {language === 'hi' ? festival.description_hindi || festival.description : festival.description}
                          </p>
                        )}
                        {((language === 'hi' && festival.rituals_hindi) || festival.rituals) && (
                          <div className="mt-2 p-2 rounded-lg bg-background/50">
                            <p className="text-xs text-muted-foreground">
                              <strong>{language === 'hi' ? 'अनुष्ठान:' : t('auto.rituals')}</strong> {language === 'hi' ? festival.rituals_hindi || festival.rituals : festival.rituals}
                            </p>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="text-center py-8">
              <Leaf className="h-12 w-12 text-muted-foreground mx-auto mb-3" />
              <p className="text-muted-foreground">
                {t('auto.noSpecialFestivalsTo')}
              </p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Panchaka + Ganda Moola */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">

        {/* ── Panchaka ── */}
        <Card className={`card-sacred border ${panchang.panchaka?.active ? 'border-red-300 bg-red-50/30' : 'border-green-200 bg-green-50/20'}`}>
          <CardContent className="p-4 space-y-2">
            <div className="flex items-center gap-2">
              <Info className={`h-5 w-5 ${panchang.panchaka?.active ? 'text-red-500' : 'text-green-600'}`} />
              <Heading as={4} variant={4}>{t('auto.panchak')}</Heading>
              <span className={`ml-auto text-[11px] font-bold px-2 py-0.5 rounded-full ${
                panchang.panchaka?.active
                  ? 'bg-red-100 text-red-700'
                  : 'bg-green-100 text-green-700'
              }`}>
                {panchang.panchaka?.active
                  ? (language === 'hi' ? 'सक्रिय' : 'Active')
                  : (language === 'hi' ? 'नहीं' : 'Clear')}
              </span>
            </div>

            {panchang.panchaka?.active ? (
              <div className="space-y-1.5 text-sm">
                {panchang.panchaka.type && (
                  <p className="font-semibold text-red-700">
                    {language === 'hi' ? panchang.panchaka.type_hindi || panchang.panchaka.type : panchang.panchaka.type}
                  </p>
                )}
                {panchang.panchaka.unsafe_window && (
                  <div className="flex items-center gap-1.5 text-red-600 text-xs">
                    <span className="font-medium">{language === 'hi' ? '⚠ अशुभ समय:' : '⚠ Avoid:'}</span>
                    <span>{panchang.panchaka.unsafe_window_label || `${panchang.panchaka.unsafe_window.start} – ${panchang.panchaka.unsafe_window.end}`}</span>
                  </div>
                )}
                {panchang.panchaka.safe_window ? (
                  <div className="flex items-center gap-1.5 text-green-700 text-xs">
                    <span className="font-medium">{language === 'hi' ? '✓ शुभ समय:' : '✓ Safe window:'}</span>
                    <span>{panchang.panchaka.safe_window_label || `${panchang.panchaka.safe_window.start} – ${panchang.panchaka.safe_window.end}`}</span>
                  </div>
                ) : panchang.panchaka.active && (
                  <p className="text-xs text-red-500">{language === 'hi' ? 'कोई शुभ समय नहीं' : 'No safe window today'}</p>
                )}
                <p className="text-xs text-muted-foreground pt-1">
                  {language === 'hi'
                    ? 'पंचक में निर्माण, यात्रा, श्राद्ध वर्जित है।'
                    : 'Construction, travel & last rites are inauspicious during Panchaka.'}
                </p>
              </div>
            ) : (
              <div className="space-y-1 text-sm">
                <p className="text-green-700 font-medium text-xs">
                  {language === 'hi' ? 'आज पंचक नहीं है — सभी कार्य शुभ।' : 'No Panchaka today — all activities permitted.'}
                </p>
                <p className="text-xs text-muted-foreground">
                  {language === 'hi'
                    ? 'पंचक धनिष्ठा, शतभिषा, पूर्वाभाद्र, उत्तराभाद्र, रेवती नक्षत्र में होता है।'
                    : 'Panchaka occurs in: Dhanishtha, Shatabhisha, Purva Bhadra, Uttara Bhadra, Revati.'}
                </p>
              </div>
            )}
          </CardContent>
        </Card>

        {/* ── Ganda Moola ── */}
        {(() => {
          const gm = panchang.special_yogas?.ganda_moola;
          return (
            <Card className={`card-sacred border ${gm?.active ? 'border-orange-300 bg-orange-50/30' : 'border-green-200 bg-green-50/20'}`}>
              <CardContent className="p-4 space-y-2">
                <div className="flex items-center gap-2">
                  <Moon className={`h-5 w-5 ${gm?.active ? 'text-orange-500' : 'text-green-600'}`} />
                  <Heading as={4} variant={4}>{t('auto.gandaMoola')}</Heading>
                  <span className={`ml-auto text-[11px] font-bold px-2 py-0.5 rounded-full ${
                    gm?.active
                      ? 'bg-orange-100 text-orange-700'
                      : 'bg-green-100 text-green-700'
                  }`}>
                    {gm?.active
                      ? (language === 'hi' ? 'सक्रिय' : 'Active')
                      : (language === 'hi' ? 'नहीं' : 'Clear')}
                  </span>
                </div>

                {gm?.active ? (
                  <div className="space-y-1.5 text-sm">
                    <p className="font-semibold text-orange-700">
                      {language === 'hi' ? `नक्षत्र: ${gm.nakshatra}` : `Nakshatra: ${gm.nakshatra}`}
                    </p>
                    <p className="text-xs text-muted-foreground">
                      {language === 'hi'
                        ? 'गण्ड मूल में जन्मे शिशु का विशेष नामकरण संस्कार आवश्यक है। शुभ कार्यों में सावधानी रखें।'
                        : 'Special birth purification rites recommended. Avoid major auspicious events if possible.'}
                    </p>
                  </div>
                ) : (
                  <div className="space-y-1 text-sm">
                    <p className="text-green-700 font-medium text-xs">
                      {language === 'hi' ? 'आज गण्ड मूल नहीं है।' : 'No Ganda Moola today.'}
                    </p>
                    <p className="text-xs text-muted-foreground">
                      {language === 'hi'
                        ? 'गण्ड मूल: अश्विनी, अश्लेषा, मघा, ज्येष्ठा, मूल, रेवती नक्षत्र में होता है।'
                        : 'Occurs in: Ashwini, Ashlesha, Magha, Jyeshtha, Moola, Revati.'}
                    </p>
                  </div>
                )}
              </CardContent>
            </Card>
          );
        })()}
      </div>
    </div>
  );
}
