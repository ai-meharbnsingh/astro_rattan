interface Props {
  language: string;
}

export default function BeneficMaleficLegend({ language }: Props) {
  const hi = language === 'hi';
  return (
    <div
      className="rounded-lg bg-sacred-gold/5 px-3 py-1.5 text-sm text-center"
      style={{ fontFamily: 'Inter,sans-serif', color: '#C4611F' }}
    >
      <span className="flex items-center justify-center gap-4 flex-wrap">
        <span className="flex items-center gap-1">
          <span className="w-2 h-2 rounded-full inline-block" style={{ background: '#C4611F' }} />
          {hi ? 'शुभ' : 'Benefic'}
        </span>
        <span className="flex items-center gap-1">
          <span className="w-2 h-2 rounded-full inline-block" style={{ background: '#1a1a2e' }} />
          {hi ? 'पापी' : 'Malefic'}
        </span>
        <span className="flex items-center gap-1">
          <span style={{ color: '#C4611F' }}>▲</span>
          {hi ? 'लग्न' : 'ASC'}
        </span>
      </span>
    </div>
  );
}

