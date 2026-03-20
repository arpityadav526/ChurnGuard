interface RiskBadgeProps {
  level: 'Low' | 'Medium' | 'High';
  size?: 'sm' | 'md';
}

export function RiskBadge({ level, size = 'md' }: RiskBadgeProps) {
  const colors = {
    Low: 'bg-green-100 text-green-700',
    Medium: 'bg-yellow-100 text-yellow-700',
    High: 'bg-red-100 text-red-700',
  };

  const sizeClasses = {
    sm: 'px-2 py-1 text-xs',
    md: 'px-3 py-1 text-sm',
  };

  return (
    <span className={`${colors[level]} ${sizeClasses[size]} rounded-full font-semibold`}>
      {level} Risk
    </span>
  );
}
