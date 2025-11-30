import { Loader2 } from 'lucide-react'
import { cn } from '@/lib/utils'

interface LoadingOverlayProps {
  message?: string
  description?: string
  className?: string
}

export function LoadingOverlay({
  message = 'Loading...',
  description,
  className,
}: LoadingOverlayProps) {
  return (
    <div
      className={cn(
        'absolute inset-0 bg-white/80 backdrop-blur-sm z-10 flex items-center justify-center',
        className
      )}
    >
      <div className="text-center space-y-2">
        <Loader2 className="h-8 w-8 animate-spin text-blue-500 mx-auto" />
        <p className="text-lg font-semibold text-gray-700">{message}</p>
        {description && <p className="text-sm text-gray-500">{description}</p>}
      </div>
    </div>
  )
}
