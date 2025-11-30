export interface NavigationTab {
  label: string
  href: string
  icon?: React.ComponentType<{ className?: string }>
  disabled?: boolean
}

export interface FileUploadHandlers {
  onUploadStart?: () => void
  onUploadSuccess: (data: any) => void
  onUploadError: (error: Error) => void
}

export interface TabNavigationProps {
  className?: string
  uploadHandlers?: Partial<FileUploadHandlers>
}

export const NAVIGATION_TABS: NavigationTab[] = [
  {
    label: 'Drilling Monitoring',
    href: '/dashboard',
    disabled: false,
  },
  {
    label: 'Offset Wells Map',
    href: '/dashboard/offset-wells',
    disabled: false,
  },
  {
    label: 'Bit Summary',
    href: '/dashboard/bit-summary',
    disabled: true,
  },
]
