import { useMemo } from 'react'
import { DrillingData } from '../types'

interface Well {
  depth: number
}

const normalizeValues = (data: DrillingData[], key: 'dt' | 'gr'): DrillingData[] => {
  const values = data.map((d) => d[key]).filter((v) => v !== undefined) as number[]

  if (values.length === 0) {
    return data
  }

  const min = Math.min(...values)
  const max = Math.max(...values)
  const range = max - min || 1

  return data.map((d) => ({
    ...d,
    [key]: d[key] !== undefined ? ((d[key]! - min) / range) * 100 : undefined,
  }))
}

export function useDrillingData(data: DrillingData[] | null, currentWell: Well | null) {
  return useMemo(() => {
    const fullData = data || []

    const filteredData = currentWell
      ? fullData.filter((d) => d.depth <= currentWell.depth)
      : fullData

    if (filteredData.length === 0) {
      return {
        filteredData: [],
        normalizedData: [],
        sharedDomain: [0, 100] as [number, number],
        normalizedDomain: [0, 100] as [number, number],
      }
    }

    const depths = filteredData.map((d) => d.depth)
    const minDepth = Math.min(...depths)
    const maxDepth = currentWell ? currentWell.depth : Math.max(...depths)

    let normalizedData = normalizeValues(filteredData, 'dt')
    normalizedData = normalizeValues(normalizedData, 'gr')

    return {
      filteredData,
      normalizedData,
      sharedDomain: [minDepth, maxDepth] as [number, number],
      normalizedDomain: [0, 100] as [number, number],
    }
  }, [data, currentWell])
}
