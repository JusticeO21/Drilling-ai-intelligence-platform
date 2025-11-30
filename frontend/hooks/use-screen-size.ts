import { useState, useEffect } from 'react'

export type ScreenSize = 'mobile' | 'tablet' | 'desktop'

const BREAKPOINTS = {
  mobile: 768,
  tablet: 1024,
} as const

const getScreenSize = (width: number): ScreenSize => {
  if (width < BREAKPOINTS.mobile) return 'mobile'
  if (width < BREAKPOINTS.tablet) return 'tablet'
  return 'desktop'
}

const getInitialScreenSize = (): ScreenSize => {
  if (typeof window === 'undefined') return 'desktop'
  return getScreenSize(window.innerWidth)
}

export function useScreenSize() {
  const [screenSize, setScreenSize] = useState<ScreenSize>(getInitialScreenSize)

  useEffect(() => {
    const handleResize = () => {
      setScreenSize(getScreenSize(window.innerWidth))
    }

    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  return screenSize
}
