import { useMemo } from 'react'

export function useChartTicks(
  sharedDomain: [number, number] | undefined,
  interval: number
): number[] | undefined {
  return useMemo(() => {
    if (!sharedDomain) return undefined

    const [min, max] = sharedDomain
    const start = Math.floor(min / interval) * interval
    const end = Math.ceil(max / interval) * interval
    const ticks: number[] = []

    for (let i = start; i <= end; i += interval) {
      ticks.push(i)
    }

    return ticks
  }, [sharedDomain, interval])
}
