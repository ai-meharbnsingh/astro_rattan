import { Card, CardContent } from '@/components/ui/card';
import { Calendar, Info, Flame, Leaf, Moon } from 'lucide-react';
import type { FullPanchangData } from '@/sections/Panchang';
import { Heading } from "@/components/ui/heading";

interface Props {
  panchang: FullPanchangData;
  language: string;
  t: (key: string) => string;
}

export default function FestivalsTab({ panchang, language, t }: Props) {
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
    <div className="space-y-6">
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

      {/* Special Days Info */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <Card className="card-sacred">
          <CardContent className="p-4">
            <div className="flex items-start gap-3">
              <Info className="h-5 w-5 text-sacred-gold mt-0.5" />
              <div>
                <Heading as={4} variant={4}>
                  {t('auto.panchak')}
                </Heading>
                <p className="text-sm text-muted-foreground">
                  {panchang.panchaka?.active 
                    ? (t('auto.panchakIsActivePostp'))
                    : (t('auto.noPanchakToday'))
                  }
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="card-sacred">
          <CardContent className="p-4">
            <div className="flex items-start gap-3">
              <Moon className="h-5 w-5 text-sacred-gold mt-0.5" />
              <div>
                <Heading as={4} variant={4}>
                  {t('auto.gandaMoola')}
                </Heading>
                <p className="text-sm text-muted-foreground">
                  {panchang.ganda_moola?.active 
                    ? `${t('auto.active')}: ${panchang.ganda_moola.nakshatra}`
                    : (t('auto.noGandaMoolaToday'))
                  }
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}