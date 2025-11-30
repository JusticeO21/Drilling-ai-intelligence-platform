import { cn } from '@/lib/utils'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { NavigationTab } from '../types'

interface TabsDesktopProps {
  tabs: NavigationTab[]
  className?: string
  tabClassName?: string
}

export function TabsDesktop({ tabs, className, tabClassName }: TabsDesktopProps) {
  const pathname = usePathname()

  return (
    <div className={cn('hidden lg:flex items-center gap-2', className)}>
      {tabs.map((tab) => {
        const isActive = pathname === tab.href
        const Icon = tab.icon

        return (
          <Link
            key={tab.href}
            href={tab.href}
            aria-disabled={tab.disabled}
            tabIndex={tab.disabled ? -1 : undefined}
            className={cn(
              'inline-flex items-center whitespace-nowrap rounded-md text-sm font-medium transition-colors px-4 py-2',
              'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
              tab.disabled && 'opacity-50 pointer-events-none',
              isActive
                ? 'bg-blue-100 text-blue-600 dark:bg-blue-900/30'
                : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground',
              tabClassName
            )}
          >
            {Icon && <Icon className="mr-2 h-4 w-4" />}
            {tab.label}
          </Link>
        )
      })}
    </div>
  )
}
