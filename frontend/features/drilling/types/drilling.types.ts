export interface LogData {
  depth: number
  dt?: number
  gr?: number
  sh?: number
  anh?: number
  ls?: number
  coal?: number
  salt?: number
  dol?: number
}

export interface RockCompositionData {
  depth: number
  sh: number
  anh: number
  ls: number
  coal: number
  salt: number
  dol: number
}

export interface DrillingData {
  depth: number
  dt?: number
  gr?: number
  [key: string]: any
}

export interface ChartLabelProps {
  label: string
  color: string
  value?: string | number
  unit?: string
  className?: string
}

export interface LogChartProps {
  data: LogData[]
  dataKey: string
  color: string
  label: string
  unit?: string
  interval?: number
  domain?: [number, number]
  reversed?: boolean
  hideYAxis?: boolean
  sharedDomain?: [number, number]
}

export interface Well {
  id: string
  name: string
}

export interface DrillingState {
  data: LogData[] | null
  currentWell?: Well
  loading: boolean
  error: string | null
}

export interface DrillingActions {
  setData: (data: LogData[] | null) => void
  setLoading: (loading: boolean) => void
  setError: (error: string | null) => void
  loadWell: (wellId: string) => Promise<LogData[] | null>
  loadWells: () => Promise<Well[]>
  clearWellData: () => void
  uploadDrillingFile: (file: File) => Promise<LogData[]>
}
