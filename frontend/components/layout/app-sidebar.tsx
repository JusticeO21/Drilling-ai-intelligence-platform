'use client'
import { Sidebar } from '../ui/sidebar'
import { ChevronRight, ChevronLeft } from 'lucide-react'
import { useWellsStore, Well } from '@/features/drilling'
import { useEffect } from 'react'
import { SidebarItem } from '@/components/ui/sidebar'
import { useScreenSize } from '@/hooks/use-screen-size'

const navigationItems = [
  { id: '1', label: 'Well A', depth: 2000 },
  { id: '2', label: 'Well AA', depth: 3000 },
  { id: '3', label: 'Well AAA', depth: 1500 },
  { id: '4', label: 'Well B', depth: 2500 },
]

export function AppSidebar() {
  const { wells, setWells, setCurrentWell } = useWellsStore()
  const screenSize = useScreenSize()

  useEffect(() => {
    if (wells.length === 0) {
      setWells(navigationItems)
      setCurrentWell(navigationItems[0])
    }
  }, [wells.length, setWells, setCurrentWell])

  return (
    <Sidebar
      defaultOpen={screenSize == 'desktop'}
      className="max-w-100"
      items={navigationItems}
      OpenIcon={ChevronRight}
      CloseIcon={ChevronLeft}
      onItemClick={(item: Omit<SidebarItem, 'icon' | 'badge'>) =>
        setCurrentWell({ id: item.id, label: item.label, depth: item.depth! } as Well)
      }
    />
  )
}
