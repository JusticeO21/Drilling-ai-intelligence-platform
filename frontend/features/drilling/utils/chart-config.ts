export const ROCK_COLORS = {
  sh: '#ec4899',
  anh: '#3b82f6',
  ss: '#94a3b8',
  ls: '#fbbf24',
  coal: '#1f2937',
  salt: '#06b6d4',
  dol: '#6366f1',
} as const

export const LOG_COLORS = {
  dt: '#ec4899',
  gr: '#3b82f6',
} as const

export const CHART_CONFIG = {
  margins: { top: 10, right: 0, left: 0, bottom: 0 },
  animationDuration: 300,
  strokeWidth: 1,
  gridColor: '#e5e7eb',
  axisColor: '#6b7280',
  axisWidth: 0.5,
} as const

export const formatDepth = (depth: number): string => {
  return `${depth.toLocaleString()} ft`
}
export const formatPercentage = (value: number): string => {
  return `${value.toFixed(1)}%`
}
