'use client'

import { LogChart } from './log-chart'
import { LOG_COLORS } from '../utils/chart-config'
import type { LogData } from '../types/drilling.types'

interface GRLogChartProps {
  data: LogData[]
  hideYAxis?: boolean
  sharedDomain?: [number, number]
  domain?: [number, number]
}

export function GRLogChart({ data, hideYAxis, sharedDomain, domain }: GRLogChartProps) {
  return (
    <LogChart
      data={data}
      dataKey="gr"
      color={LOG_COLORS.gr}
      label="GR"
      unit="API"
      domain={domain || [0, 150]}
      reversed={false}
      hideYAxis={hideYAxis}
      sharedDomain={sharedDomain}
    />
  )
}
