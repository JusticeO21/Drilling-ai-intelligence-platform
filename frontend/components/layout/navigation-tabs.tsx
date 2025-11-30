'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { memo, useCallback } from 'react'
import { cn } from '@/lib/utils'
import type { NavigationTab } from './types'

interface NavigationTabsProps {
  tabs: NavigationTab[]
  className?: string
  tabClassName?: string
  activeClassName?: string
  inactiveClassName?: string
}

export const NavigationTabs = memo(function NavigationTabs({
  tabs,
  className,
  tabClassName,
  activeClassName = 'text-blue-600 bg-blue-100 dark:bg-blue-900/30',
  inactiveClassName = 'text-muted-foreground hover:bg-accent hover:text-accent-foreground',
}: NavigationTabsProps) {
  const pathname = usePathname()

  const isActiveRoute = useCallback(
    (href: string) => pathname === href || pathname.startsWith(href + '/'),
    [pathname]
  )

  return (
    <nav
      className={cn('flex flex-wrap items-center gap-2', className)}
      aria-label="Navigation Tabs"
    >
      {tabs.map(({ href, label, icon: Icon, disabled }) => {
        const active = isActiveRoute(href)

        return (
          <Link
            key={href}
            href={disabled ? '#' : href}
            aria-disabled={disabled}
            tabIndex={disabled ? -1 : 0}
            className={cn(
              'inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium',
              'px-4 py-2 transition-colors ring-offset-background',
              'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',

              disabled && 'pointer-events-none opacity-50',
              active ? activeClassName : inactiveClassName,
              tabClassName
            )}
          >
            {Icon && <Icon className="mr-2 h-4 w-4 shrink-0" />}
            <span className="truncate">{label}</span>
          </Link>
        )
      })}
    </nav>
  )
})
