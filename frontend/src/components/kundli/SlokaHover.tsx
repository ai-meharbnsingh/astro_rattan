import React, { useState } from 'react';
import slokaData from '@/data/phaladeepika_slokas.json';
import { BookOpen } from 'lucide-react';
import { cn } from '@/lib/utils';

interface SlokaHoverProps {
  slokaRef: string;
  children?: React.ReactNode;
  language?: string;
  className?: string;
}

const SlokaHover: React.FC<SlokaHoverProps> = ({ slokaRef, children, language = 'en', className }) => {
  const [show, setShow] = useState(false);
  const data = (slokaData as any)[slokaRef];
  const isHi = language === 'hi';

  if (!data) {
    return (
      <span className={cn("inline-flex items-center gap-1.5 text-muted-foreground italic", className)}>
        {children || slokaRef}
      </span>
    );
  }

  return (
    <span 
      className="relative inline-block cursor-help group"
      onMouseEnter={() => setShow(true)}
      onMouseLeave={() => setShow(false)}
    >
      <span className={cn(
        "underline decoration-dotted decoration-sacred-gold/50 hover:text-sacred-gold-dark hover:decoration-sacred-gold transition-all duration-200",
        className
      )}>
        {children || slokaRef}
      </span>
      
      {show && (
        <div className="absolute z-[100] bottom-full left-1/2 -translate-x-1/2 mb-3 w-80 p-5 rounded-2xl shadow-[0_20px_50px_rgba(0,0,0,0.2)] border border-sacred-gold/20 bg-white dark:bg-slate-900 text-foreground animate-in fade-in slide-in-from-bottom-2 duration-300">
          <div className="flex items-center gap-2 mb-3 pb-2 border-b border-sacred-gold/10">
            <BookOpen className="w-4 h-4 text-sacred-gold-dark" />
            <span className="text-[10px] font-bold uppercase tracking-widest text-sacred-gold-dark">
              {isHi ? 'फलदीपिका' : 'Phaladeepika Ref'} - {slokaRef.replace('Phaladeepika ', '')}
            </span>
          </div>
          
          <div className="space-y-4">
            <div className="relative">
              <span className="absolute -left-2 top-0 text-3xl text-sacred-gold/10 font-serif leading-none">"</span>
              <p className="text-[15px] font-medium leading-relaxed text-sacred-gold-dark italic px-2">
                {data.sanskrit}
              </p>
            </div>
            
            <div className="bg-sacred-gold/5 rounded-lg p-3 border-l-2 border-sacred-gold/30">
              <p className="text-[13px] leading-relaxed text-muted-foreground mb-1 font-semibold uppercase tracking-tighter text-[9px]">
                {isHi ? 'अर्थ' : 'MEANING'}
              </p>
              <p className="text-[13px] leading-relaxed text-foreground/90">
                {isHi ? data.meaning_hi : data.meaning_en}
              </p>
            </div>
          </div>
          
          <div className="absolute -bottom-2 left-1/2 -translate-x-1/2 w-4 h-4 rotate-45 bg-white dark:bg-slate-900 border-r border-b border-sacred-gold/20 shadow-[5px_5px_10px_rgba(0,0,0,0.05)]"></div>
        </div>
      )}
    </span>
  );
};

export default SlokaHover;
