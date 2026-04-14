import { useState, useEffect } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Calendar, Sparkles, Info, Flame, Leaf, Moon } from 'lucide-react';
import { api } from '@/lib/api';
import type { FullPanchangData } from '@/sections/Panchang';

interface Props {
  panchang: FullPanchangData;
  language: string;
  t: (key: string) => string;
  selectedDate: string;
}

export default function FestivalsTab({ panchang, language, t, selectedDate }: Props) {
  const [monthlyFestivals, setMonthlyFestivals] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  
  const todayFestivals = panchang.festivals || [];

  // Fetch monthly festivals
  useEffect(() => {
    const fetchMonthly = async () => {
      setLoading(true);
      try {
        const date = new Date(selectedDate);
        const year = date.getFullYear();
        const month = date.getMonth() + 1;
        const res = await api.get(`/api/festivals?year=${year}&month=${month}`);
        setMonthlyFestivals(res.data?.festivals || []);
      } catch (e) {
        setMonthlyFestivals([]);
      }
      setLoading(false);
    };
    fetchMonthly();
  }, [selectedDate]);

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
          <h3 className="text-lg font-bold text-cosmic-text-primary mb-4 flex items-center gap-2">
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
                    className="p-4 rounded-xl bg-cosmic-card/50 border border-cosmic-border hover:border-sacred-gold/30 transition-all"
                  >
                    <div className="flex items-start gap-3">
                      <div className={`p-2 rounded-lg ${colorClass}`}>
                        <Icon className="h-5 w-5" />
                      </div>
                      <div className="flex-1">
                        <h4 className="font-semibold text-cosmic-text-primary">
                          {language === 'hi' && festival.name_hindi ? festival.name_hindi : festival.name}
                        </h4>
                        <span className={`inline-block mt-1 px-2 py-0.5 text-xs rounded-full ${colorClass}`}>
                          {language === 'hi' ? festival.type_hindi || festival.type : festival.type}
                        </span>
                        {festival.description && (
                          <p className="text-sm text-cosmic-text-secondary mt-2">
                            {language === 'hi' ? festival.description : festival.description}
                          </p>
                        )}
                        {festival.rituals && (
                          <div className="mt-2 p-2 rounded-lg bg-cosmic-bg/50">
                            <p className="text-xs text-cosmic-text-secondary">
                              <strong>{language === 'hi' ? 'विधि:' : 'Rituals:'}</strong> {festival.rituals}
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
              <Leaf className="h-12 w-12 text-cosmic-text-secondary mx-auto mb-3" />
              <p className="text-cosmic-text-secondary">
                {language === 'hi' ? 'आज कोई विशेष त्योहार नहीं' : 'No special festivals today'}
              </p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Monthly Festivals */}
      <Card className="card-sacred">
        <CardContent className="p-4">
          <h3 className="text-lg font-bold text-cosmic-text-primary mb-4 flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-purple-500" />
            {language === 'hi' ? 'इस महीने के त्योहार' : 'This Month\'s Festivals'}
          </h3>
          
          {loading ? (
            <div className="text-center py-8">
              <div className="animate-spin h-8 w-8 border-2 border-sacred-gold border-t-transparent rounded-full mx-auto" />
            </div>
          ) : monthlyFestivals.length > 0 ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {monthlyFestivals.slice(0, 10).map((festival, index) => {
                const Icon = getFestivalIcon(festival.type);
                const colorClass = getFestivalColor(festival.type);
                
                return (
                  <div 
                    key={index}
                    className="p-3 rounded-xl bg-cosmic-card/30 border border-transparent hover:border-cosmic-border transition-all"
                  >
                    <div className="flex items-center gap-2">
                      <Icon className={`h-4 w-4 ${colorClass.split(' ')[0]}`} />
                      <span className="font-medium text-cosmic-text-primary text-sm">
                        {language === 'hi' && festival.name_hindi ? festival.name_hindi : festival.name}
                      </span>
                    </div>
                    <p className="text-xs text-cosmic-text-secondary mt-1">
                      {festival.date} • {language === 'hi' ? festival.type_hindi || festival.type : festival.type}
                    </p>
                  </div>
                );
              })}
            </div>
          ) : (
            <p className="text-center text-cosmic-text-secondary py-4">
              {language === 'hi' ? 'कोई डेटा उपलब्ध नहीं' : 'No data available'}
            </p>
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
                <h4 className="font-semibold text-cosmic-text-primary mb-1">
                  {language === 'hi' ? 'पंचक' : 'Panchak'}
                </h4>
                <p className="text-sm text-cosmic-text-secondary">
                  {panchang.panchaka?.active 
                    ? (language === 'hi' ? 'पंचक चल रहा है - नए कार्य टालें' : 'Panchak is active - postpone new work')
                    : (language === 'hi' ? 'पंचक नहीं है' : 'No Panchak today')
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
                <h4 className="font-semibold text-cosmic-text-primary mb-1">
                  {language === 'hi' ? 'गंड मूल' : 'Ganda Moola'}
                </h4>
                <p className="text-sm text-cosmic-text-secondary">
                  {panchang.ganda_moola?.active 
                    ? `${language === 'hi' ? 'सक्रिय' : 'Active'}: ${panchang.ganda_moola.nakshatra}`
                    : (language === 'hi' ? 'आज गंड मूल नहीं है' : 'No Ganda Moola today')
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
