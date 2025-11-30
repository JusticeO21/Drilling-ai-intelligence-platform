'use client'
import { RockComposition } from './rock-composition'
import { DTLogChart } from './dt-log-chart'
import { GRLogChart } from './gr-log-chart'
import { NoData } from './no-data'
import { LoadingOverlay } from '@/components/ui/loading-overlay'
import { useDrillingStore } from '../stores/drilling-store'
import { useWellsStore } from '../stores/wells-store'
import { useScreenSize } from '@/hooks/use-screen-size'
import { useDrillingData } from '../hooks'

export function DrillingDashboard() {
  const { data, loading } = useDrillingStore()
  const { currentWell } = useWellsStore()
  const screenSize = useScreenSize()

  const { filteredData, normalizedData, sharedDomain, normalizedDomain } = useDrillingData(
    data,
    currentWell
  )

  if (!data || data.length === 0) {
    return <NoData className="mx-auto" />
  }

  const shouldHideDTAxis = screenSize === 'tablet' || screenSize === 'desktop'
  const shouldHideGRAxis = screenSize === 'desktop'

  return (
    <div className="h-auto w-full relative mx-auto">
      {loading && (
        <LoadingOverlay
          className="items-start"
          message="plotting data..."
          description="Please wait while we process your drilling data"
        />
      )}

      <div className="grid grid-cols-1 gap-0 sm:grid-cols-2 lg:grid-cols-3 w-full">
        <div className="pr-4 lg:pr-1 col-span-1">
          <RockComposition data={normalizedData} sharedDomain={sharedDomain} />
        </div>

        <div className="pr-4 lg:pr-1 col-span-1 border-l">
          <DTLogChart
            data={normalizedData}
            hideYAxis={shouldHideDTAxis}
            sharedDomain={sharedDomain}
            domain={normalizedDomain}
          />
        </div>

        <div className="pr-4 lg:pr-1 col-span-1 border-l">
          <GRLogChart
            data={normalizedData}
            hideYAxis={shouldHideGRAxis}
            sharedDomain={sharedDomain}
            domain={normalizedDomain}
          />
        </div>
      </div>
    </div>
  )
}
