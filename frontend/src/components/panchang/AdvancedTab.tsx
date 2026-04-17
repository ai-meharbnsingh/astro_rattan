import { Shield, Microscope, Clock, Table, BadgeCheck } from 'lucide-react';
import type { FullPanchangData } from '@/sections/Panchang';
import { Card, CardContent } from '@/components/ui/card';
import { Heading } from '@/components/ui/heading';

interface Props {
  panchang: any; // Using any because of highly nested misc fields
  language: string;
  t: (key: string) => string;
}

export default function AdvancedTab({ panchang, language, t }: Props) {
  const l = (en: string, hi: string) => language === 'hi' ? hi : en;
  
  const mantriMandala = panchang.misc?.mantri_mandala || [];
  const astronomical = panchang.misc?.astronomical || {};
  const doGhati = panchang.do_ghati_muhurta || [];

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Mantri Mandala / Planetary Cabinet */}
        <Card className="card-sacred border-sacred-gold/30">
          <CardContent className="p-4">
            <h3 className="text-lg font-bold text-foreground mb-4 flex items-center gap-2">
              <Shield className="h-5 w-5 text-sacred-gold" />
              {l('Mantri Mandala (Planetary Cabinet)', 'मन्त्री मण्डल (ग्रह मण्डल)')}
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {mantriMandala.map((item: any, idx: number) => (
                <div key={idx} className="flex items-center justify-between p-3 rounded-lg bg-card/50 border border-border/40">
                  <span className="text-xs font-semibold text-muted-foreground uppercase">
                    {language === 'hi' ? item.role_hindi : item.role}
                  </span>
                  <span className="text-sm font-bold text-sacred-gold-dark">
                    {language === 'hi' ? item.planet_hindi : item.planet}
                  </span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Astronomical Data */}
        <Card className="card-sacred border-blue-500/20">
          <CardContent className="p-4">
            <h3 className="text-lg font-bold text-foreground mb-4 flex items-center gap-2">
              <Microscope className="h-5 w-5 text-blue-500" />
              {l('Astronomical Epoch Data', 'खगोलीय युग डेटा')}
            </h3>
            <div className="space-y-3">
              {[
                { label: l('Kaliyuga Year', 'कलियुग वर्ष'), value: astronomical.kaliyuga_year_label_hindi || astronomical.kaliyuga_year_label },
                { label: l('Kali Ahargana', 'कलि अहर्गण'), value: astronomical.kali_ahargana_label_hindi || astronomical.kali_ahargana_label },
                { label: l('Julian Day', 'जूलियन दिन'), value: astronomical.julian_day_label_hindi || astronomical.julian_day_label },
                { label: l('Modified Julian Day', 'एमजेडी'), value: astronomical.modified_julian_day_label_hindi || astronomical.modified_julian_day_label },
                { label: l('Rata Die', 'राटा डाई'), value: astronomical.rata_die_label_hindi || astronomical.rata_die_label },
                { label: l('Ayanamsha (Lahiri)', 'अयनांश'), value: astronomical.ayanamsha_label_hindi || astronomical.ayanamsha_label },
              ].map((item, idx) => (
                <div key={idx} className="flex items-center justify-between py-2 border-b border-border/40 last:border-0 text-sm">
                  <span className="text-muted-foreground">{item.label}</span>
                  <span className="font-mono font-medium text-foreground">{item.value || '—'}</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Do Ghati Muhurtas (30 Muhurtas) */}
      <Card className="card-sacred border-sacred-gold/30">
        <CardContent className="p-4">
          <h3 className="text-lg font-bold text-foreground mb-4 flex items-center gap-2">
            <Clock className="h-5 w-5 text-sacred-gold" />
            {l('Do-Ghati Muhurtas (30 Daily Muhurtas)', 'दो-घटी मुहूर्त (दिन के ३० मुहूर्त)')}
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-3">
            {doGhati.map((m: any, idx: number) => {
              const isAuspicious = m.quality === 'Auspicious' || m.quality === 'Good';
              return (
                <div 
                  key={idx} 
                  className={`p-3 rounded-xl border transition-all ${
                    isAuspicious 
                      ? 'bg-green-500/5 border-green-500/20 hover:border-green-500/40' 
                      : 'bg-card/50 border-border/40 hover:border-border'
                  }`}
                >
                  <div className="flex justify-between items-start mb-1">
                    <span className="text-[10px] font-bold text-muted-foreground uppercase opacity-70">
                      #{idx + 1}
                    </span>
                    <BadgeCheck className={`h-3.5 w-3.5 ${isAuspicious ? 'text-green-500' : 'text-muted-foreground/30'}`} />
                  </div>
                  <Heading as={4} variant={4} className="!text-sm mb-1">
                    {m.name}
                  </Heading>
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-muted-foreground">{m.start} – {m.end}</span>
                    <span className={`font-semibold ${isAuspicious ? 'text-green-600' : 'text-stone-500'}`}>
                      {l(m.quality, translateQuality(m.quality))}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

function translateQuality(q: string): string {
  switch(q) {
    case 'Auspicious': return 'शुभ';
    case 'Inauspicious': return 'अशुभ';
    case 'Good': return 'अच्छा';
    case 'Bad': return 'बुरा';
    default: return q;
  }
}
