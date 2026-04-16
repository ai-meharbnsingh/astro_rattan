interface ScoreBarProps {
  label: string;
  score: number; // 1-10
  color: string; // tailwind color like "amber", "pink", "blue", "green", "purple"
}

const COLOR_MAP: Record<string, { bg: string; text: string }> = {
  amber: { bg: 'bg-amber-500', text: 'text-amber-700' },
  pink: { bg: 'bg-pink-500', text: 'text-pink-700' },
  blue: { bg: 'bg-blue-500', text: 'text-blue-700' },
  green: { bg: 'bg-green-500', text: 'text-green-700' },
  purple: { bg: 'bg-purple-500', text: 'text-purple-700' },
};

export default function ScoreBar({ label, score, color }: ScoreBarProps) {
  const clampedScore = Math.max(0, Math.min(10, score));
  const widthPercent = clampedScore * 10;
  const colors = COLOR_MAP[color] || COLOR_MAP.amber;

  return (
    <div className="flex items-center gap-3">
      <span className="text-sm text-muted-foreground w-20 shrink-0">{label}</span>
      <div className="flex-1 h-2.5 bg-gray-200 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full ${colors.bg} transition-all duration-500`}
          style={{ width: `${widthPercent}%` }}
        />
      </div>
      <span className={`text-sm font-medium ${colors.text} w-10 text-right shrink-0`}>
        {clampedScore}/10
      </span>
    </div>
  );
}
