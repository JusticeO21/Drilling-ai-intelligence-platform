'use client'
import { Button } from '@/components/ui/button'
import { Filter } from 'lucide-react'
import { cn } from '@/lib/utils'
import { NAVIGATION_TABS } from './types/navigation.types'
import { FileUploadButton } from '@/components/ui'
import { NavigationTabs } from '.'
import { useFileUpload } from './hooks/useFileUploadHandler'
import { useScreenSize } from '@/hooks/use-screen-size'

interface TabNavigationProps {
  className?: string
}

export function TabNavigation({ className }: TabNavigationProps) {
  const { inputRef, handleFileChange, isUploading } = useFileUpload()
  const screenSize = useScreenSize()

  return (
    <div
      className={cn(
        'flex items-center justify-between border-b bg-white px-2 md:px-6 py-3 w-full',
        className
      )}
    >
      <NavigationTabs tabs={NAVIGATION_TABS} className="flex-1" />

      <div className="flex items-center gap-3">
        <Button
          variant="default"
          className="bg-green-500 hover:bg-green-600 hidden md:flex"
          aria-label="Filter data"
        >
          <Filter className="mr-2 h-4 w-4" />
          Filter
        </Button>

        <FileUploadButton
          ref={inputRef}
          onFileChange={handleFileChange}
          isUploading={isUploading}
          buttonText={screenSize == 'mobile' ? 'Upload' : 'Upload Data'}
          className="rounded-sm"
        />
      </div>
    </div>
  )
}
