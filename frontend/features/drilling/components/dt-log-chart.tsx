'use client'

import { LogChart } from './log-chart'
import { LOG_COLORS } from '../utils/chart-config'
import type { LogData } from '../types/drilling.types'

interface DTLogChartProps {
  data: LogData[]
  hideYAxis?: boolean
  sharedDomain?: [number, number]
  domain?: [number, number]
}

export function DTLogChart({ data, hideYAxis, sharedDomain, domain }: DTLogChartProps) {
  return (
    <LogChart
      data={data}
      dataKey="dt"
      color={LOG_COLORS.dt}
      label="DT"
      unit="µs/ft"
      domain={domain || [40, 140]}
      reversed={false}
      hideYAxis={hideYAxis}
      sharedDomain={sharedDomain}
    />
  )
}
