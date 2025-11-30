'use client'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { ChartLabel } from './chart-label'
import { NoData } from './no-data'
import { CHART_CONFIG } from '../utils/chart-config'
import { useChartTicks } from '../hooks'
import type { LogChartProps } from '../types/drilling.types'

interface CustomTooltipProps {
  active?: boolean
  payload?: any[]
  label: string
  unit: string
}

function CustomTooltip({ active, payload, label, unit }: CustomTooltipProps) {
  if (!active || !payload?.length) return null

  const data = payload[0].payload
  const value = payload[0].value

  return (
    <div className="rounded-none bg-black/40 p-3 shadow-none">
      <p className="mb-2 text-xs font-semibold text-white/80">
        Depth: {data.depth.toLocaleString()} ft
      </p>
      <div className="flex items-center gap-2">
        <div className="h-2 w-2 rounded-full" style={{ backgroundColor: payload[0].color }} />
        <p className="text-sm font-medium text-white/80">
          {label}: {value.toFixed(1)} {unit}
        </p>
      </div>
    </div>
  )
}

export function LogChart({
  data,
  dataKey,
  color,
  label,
  unit = '',
  domain,
  reversed = false,
  hideYAxis = false,
  sharedDomain,
  interval = 10,
}: LogChartProps) {
  const ticks = useChartTicks(sharedDomain, interval)

  if (!data?.length) {
    return <NoData />
  }

  return (
    <Card className="shadow-none border-none rounded-none border-r">
      <CardHeader className="pb-3 h-5 md:h-12">
        <CardTitle className="text-base font-semibold">{label}</CardTitle>
        <div className="flex items-center justify-center gap-2">
          <ChartLabel label={label} color={color} />
        </div>
      </CardHeader>

      <CardContent className="p-0">
        <ResponsiveContainer width="100%" height={1200}>
          <LineChart data={data} margin={CHART_CONFIG.margins} layout="vertical">
            <CartesianGrid
              strokeDasharray="3 3"
              stroke={CHART_CONFIG.gridColor}
              horizontal={false}
            />

            <YAxis
              type="number"
              dataKey="depth"
              reversed={reversed}
              domain={sharedDomain || ['dataMin', 'dataMax']}
              ticks={ticks}
              axisLine={!hideYAxis}
              tickLine={false}
              tick={hideYAxis ? false : { fontSize: 12, fill: CHART_CONFIG.axisColor }}
              tickFormatter={hideYAxis ? undefined : (value) => value.toString()}
            />

            <XAxis
              type="number"
              domain={domain || ['auto', 'auto']}
              orientation="top"
              tick={{ fontSize: 12, fill: CHART_CONFIG.axisColor }}
              tickLine={false}
            />

            <Tooltip
              content={<CustomTooltip label={label} unit={unit} />}
              cursor={{ stroke: color, strokeWidth: 1, strokeDasharray: '5 5' }}
            />

            <Line
              type="monotone"
              dataKey={dataKey}
              stroke={color}
              strokeWidth={1}
              dot={false}
              isAnimationActive={true}
              animationDuration={CHART_CONFIG.animationDuration}
            />
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}
