import React, { useState, useCallback, useEffect } from 'react'
import { Menu, X } from 'lucide-react'

export interface SidebarItem {
  id: string
  label: string
  depth?: number
  icon?: React.ComponentType<{ size?: number; className?: string }>
  badge?: string | number
  metadata?: Record<string, any>
}

export interface SidebarProps {
  items?: SidebarItem[]
  logo?: string
  onItemClick?: (item: SidebarItem) => void
  className?: string
  isOpen?: boolean
  onToggle?: (isOpen: boolean) => void
  defaultOpen?: boolean
  activeItemId?: string
  OpenIcon?: React.ComponentType<{ size?: number; className?: string }>
  CloseIcon?: React.ComponentType<{ size?: number; className?: string }>
  renderItem?: (item: SidebarItem, isActive: boolean) => React.ReactNode
  sidebarWidth?: string
}

/**
 * Responsive Sidebar Component
 *
 * A flexible sidebar that adapts to different screen sizes:
 * - Mobile (< 1024px): Fixed overlay with backdrop
 * - Desktop (>= 1024px): Static sidebar that pushes content
 *
 * Features:
 * - Controlled/uncontrolled mode support
 * - Custom item rendering
 * - Configurable width
 * - Accessible keyboard navigation
 */
export const Sidebar: React.FC<SidebarProps> = ({
  items = [],
  logo = 'App Name',
  onItemClick,
  className = '',
  isOpen: controlledIsOpen,
  onToggle,
  defaultOpen = true,
  activeItemId,
  OpenIcon = Menu,
  CloseIcon = X,
  renderItem,
  sidebarWidth = 'w-64',
}) => {
  // State management
  const [internalIsOpen, setInternalIsOpen] = useState(defaultOpen)
  const [internalActiveItem, setInternalActiveItem] = useState<string | null>(
    activeItemId ?? items[0]?.id ?? null
  )

  // Determine if component is controlled
  const isControlled = controlledIsOpen !== undefined
  const isOpen = isControlled ? controlledIsOpen : internalIsOpen

  // Sync internal active item with prop
  useEffect(() => {
    if (activeItemId !== undefined) {
      setInternalActiveItem(activeItemId)
    }
  }, [activeItemId])

  // Handle sidebar toggle
  const handleToggle = useCallback(
    (newState: boolean) => {
      onToggle?.(newState)
      if (!isControlled) {
        setInternalIsOpen(newState)
      }
    },
    [isControlled, onToggle]
  )

  // Handle item selection
  const handleItemClick = useCallback(
    (item: SidebarItem) => {
      setInternalActiveItem(item.id)
      onItemClick?.(item)

      // Auto-close on mobile after selection
      if (window.innerWidth < 1024) {
        handleToggle(false)
      }
    },
    [onItemClick, handleToggle]
  )

  const activeItem = activeItemId ?? internalActiveItem

  // Default item renderer
  const defaultRenderItem = (item: SidebarItem, isActive: boolean) => {
    const Icon = item.icon

    return (
      <button
        onClick={() => handleItemClick(item)}
        className={`
          w-full flex items-center gap-3 px-4 py-3 rounded-lg
          transition-all duration-200 text-left
          focus:outline-none focus:ring-none hover:cursor-pointer
          ${
            isActive
              ? 'bg-blue-50 text-blue-600 font-medium'
              : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
          }
        `}
        aria-current={isActive ? 'true' : undefined}
        aria-label={`View chart for ${item.label}`}
        type="button"
      >
        {Icon && (
          <Icon
            size={20}
            className={isActive ? 'text-blue-600' : 'text-gray-400'}
            aria-hidden="true"
          />
        )}

        <div className="flex-1 min-w-0">
          <span className="block truncate">{item.label}</span>
          {item.depth !== undefined && (
            <span className="text-xs text-gray-500 mt-0.5 block">
              Depth: {item.depth.toLocaleString()} ft
            </span>
          )}
        </div>

        {item.badge && (
          <span
            className="ml-2 bg-red-500 text-white text-xs px-2 py-0.5 rounded-full font-medium"
            aria-label={`${item.badge} notifications`}
          >
            {item.badge}
          </span>
        )}
      </button>
    )
  }

  const itemRenderer = renderItem || defaultRenderItem

  return (
    <>
      {/* Toggle Button - Shows when sidebar is closed */}
      {!isOpen && (
        <button
          onClick={() => handleToggle(true)}
          className="fixed lg:absolute top-4.5 left-0 z-50 p-0 rounded-lg bg-white/40 hover:bg-gray-50 text-gray-700 focus:outline-1 focus:ring-none hover:cursor-pointer transition-colors"
          aria-label="Open depth selection menu"
          aria-expanded={isOpen}
          type="button"
        >
          <OpenIcon size={24} aria-hidden="true" />
        </button>
      )}

      {/* Backdrop overlay for mobile */}
      {isOpen && (
        <div
          className="lg:hidden fixed inset-0 bg-black/50 z-30 transition-opacity"
          onClick={() => handleToggle(false)}
          aria-hidden="true"
        />
      )}

      {/* Sidebar */}
      <aside
        className={`
          ${sidebarWidth} h-screen
          flex flex-col shrink-0
          fixed lg:static top-0 left-0
          z-40 lg:z-0
          bg-white border-r border-gray-200
          transform transition-transform duration-300 ease-in-out
          ${isOpen ? 'translate-x-0' : '-translate-x-full lg:w-0 lg:border-0'}
          ${className}
        `}
        role="navigation"
        aria-label="Depth selection sidebar"
        aria-hidden={!isOpen}
      >
        {/* Header */}
        <header
          className="h-16 px-4 border-b border-gray-200 flex items-center justify-between shrink-0"
          role="banner"
        >
          <h1 className="text-xl font-semibold text-gray-900 truncate">{logo}</h1>
          <button
            onClick={() => handleToggle(false)}
            className="p-2 rounded-lg hover:bg-gray-100 text-gray-500 hover:text-gray-700 transition-colors focus:outline-none focus:ring-1 focus:ring-blue-500"
            aria-label="Close depth selection menu"
            type="button"
          >
            <CloseIcon size={20} aria-hidden="true" />
          </button>
        </header>

        {/* Navigation Items */}
        <nav className="flex-1 overflow-y-auto p-4">
          {items.length > 0 ? (
            <ul className="space-y-1" role="list">
              {items.map((item) => (
                <li key={item.id}>{itemRenderer(item, activeItem === item.id)}</li>
              ))}
            </ul>
          ) : (
            <div className="text-center text-gray-500 text-sm py-8">No items available</div>
          )}
        </nav>

        {/* Optional Footer */}
        <footer className="p-4 border-t border-gray-200 shrink-0" role="contentinfo">
          <p className="text-xs text-gray-500 text-center">
            {items.length} {items.length === 1 ? 'item' : 'items'}
          </p>
        </footer>
      </aside>
    </>
  )
}
