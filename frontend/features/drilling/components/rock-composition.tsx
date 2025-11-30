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
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui'
import { ChartLegend } from './chart-label'
import { NoData } from './no-data'
import { ROCK_COLORS, CHART_CONFIG, formatPercentage } from '../utils/chart-config'
import { useChartTicks } from '../hooks'
import type { LogData } from '../types/drilling.types'

interface RockCompositionProps {
  data: LogData[]
  hideYAxis?: boolean
  sharedDomain?: [number, number]
}

interface RockTooltipProps {
  active?: boolean
  payload?: any[]
}

const ROCK_TYPES = [
  { key: 'sh', label: 'SH', color: ROCK_COLORS.sh },
  { key: 'anh', label: 'ANH', color: ROCK_COLORS.anh },
  { key: 'ls', label: 'LS', color: ROCK_COLORS.ls },
  { key: 'coal', label: 'Coal', color: ROCK_COLORS.coal },
  { key: 'salt', label: 'Salt', color: ROCK_COLORS.salt },
  { key: 'dol', label: 'DOL', color: ROCK_COLORS.dol },
] as const

function RockTooltip({ active, payload }: RockTooltipProps) {
  if (!active || !payload?.length) return null

  const data = payload[0].payload

  return (
    <div className="rounded-md border bg-black/40 p-3 shadow-lg">
      <p className="mb-2 text-xs font-semibold text-white/80">
        Depth: {data.depth.toLocaleString()} ft
      </p>
      <div className="space-y-1">
        {ROCK_TYPES.map((rock) => {
          const value = data[rock.key] || 0
          return (
            <div key={rock.key} className="flex items-center gap-2">
              <div className="h-2 w-2 rounded-full" style={{ backgroundColor: rock.color }} />
              <span className="text-sm text-white">
                {rock.label}: {formatPercentage(value)}
              </span>
            </div>
          )
        })}
      </div>
    </div>
  )
}

export function RockComposition({ data, hideYAxis = false, sharedDomain }: RockCompositionProps) {
  const ticks = useChartTicks(sharedDomain, 10)

  if (!data?.length) {
    return <NoData />
  }

  const legendItems = ROCK_TYPES.map((rock) => ({
    label: rock.label,
    color: rock.color,
  }))

  return (
    <Card className="shadow-none border-none rounded-none border-r">
      <CardHeader className="pb-3 h-12">
        <CardTitle className="text-base font-semibold uppercase">Rock Composition</CardTitle>
        <ChartLegend items={legendItems} className="mt-3" />
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
              reversed={false}
              domain={sharedDomain || ['dataMin', 'dataMax']}
              ticks={ticks}
              axisLine={!hideYAxis}
              tickLine={false}
              tick={hideYAxis ? false : { fontSize: 12, fill: CHART_CONFIG.axisColor }}
              tickFormatter={hideYAxis ? undefined : (value) => value.toString()}
            />

            <XAxis
              type="number"
              domain={[0, 100]}
              orientation="top"
              tick={{ fontSize: 12, fill: CHART_CONFIG.axisColor }}
              tickLine={false}
            />

            <Tooltip content={<RockTooltip />} />

            {ROCK_TYPES.map((rock) => (
              <Line
                key={rock.key}
                type="monotone"
                dataKey={rock.key}
                stroke={rock.color}
                strokeWidth={1}
                dot={false}
                isAnimationActive={true}
                animationDuration={CHART_CONFIG.animationDuration}
              />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}
