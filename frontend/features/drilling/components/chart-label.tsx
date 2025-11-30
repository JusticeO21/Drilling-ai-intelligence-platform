import { cn } from '@/lib/utils'
import type { ChartLabelProps } from '../types/drilling.types'

export function ChartLabel({ label, color, className }: ChartLabelProps) {
  return (
    <div className={cn('flex items-center gap-2', className)}>
      <div className="h-2 w-6 rounded-none" style={{ backgroundColor: color }} />
      <span className="text-xs font-medium text-gray-700">{label}</span>
    </div>
  )
}

// Multiple labels in a row
export function ChartLegend({
  items,
  className,
}: {
  items: ChartLabelProps[]
  className?: string
}) {
  return (
    <div className={cn('flex flex-wrap items-center gap-4', className)}>
      {items.map((item, index) => (
        <ChartLabel key={index} {...item} />
      ))}
    </div>
  )
}
