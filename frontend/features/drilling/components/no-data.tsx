import { Upload } from 'lucide-react'
import { cn } from '@/lib/utils'

export function NoData({ className }: { className?: string }) {
  return (
    <div className={cn('flex items-center justify-center h-[calc(100vh-5rem)]', className)}>
      <div className="text-center">
        <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
        <h2 className="text-2xl font-semibold text-gray-500 mb-2">No Data Available</h2>
        <p className="text-gray-400">Please upload a drilling data file to view charts.</p>
      </div>
    </div>
  )
}
