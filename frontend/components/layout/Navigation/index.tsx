'use client'

import { usePathname, useRouter } from 'next/navigation'
import { cn } from '@/lib/utils'
import { TabsDesktop } from './desktop-tabs'
import { NavigationTab } from '../types'
import { SelectDropdown } from '@/components/ui'

interface NavigationTabsProps {
  tabs: NavigationTab[]
  className?: string
}

export function NavigationTabs({ tabs, className }: NavigationTabsProps) {
  const pathname = usePathname()
  const router = useRouter()

  const active = tabs.find((t) => t.href === pathname)?.href

  return (
    <div className={cn('w-full', className)}>
      <TabsDesktop tabs={tabs} />

      <div className="block lg:hidden">
        <SelectDropdown
          items={tabs}
          value={active}
          onChange={(v) => router.push(v)}
          valueKey="href"
          labelKey="label"
          disabledKey="disabled"
        />
      </div>
    </div>
  )
}
