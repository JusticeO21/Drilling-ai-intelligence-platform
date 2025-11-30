import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'
import type { DrillingState, DrillingActions, LogData } from '../types/drilling.types'
import { parseDrillingDataFile } from '../utils/data-parser'

const createInitialState = (): DrillingState => ({
  data: null,
  currentWell: undefined,
  loading: false,
  error: null,
})

const generateWellId = () => `local-${Date.now()}`

const extractFileName = (file: File) => file.name.replace(/\.[^/.]+$/, '')

export const useDrillingStore = create<DrillingState & DrillingActions>()(
  devtools(
    persist(
      (set, get) => ({
        ...createInitialState(),

        setData: (data) => set({ data }),

        setLoading: (loading) => set({ loading }),

        setError: (error) => set({ error }),

        loadWell: async (wellId: string) => get().data,

        loadWells: async () => [],

        clearWellData: () => set(createInitialState()),

        uploadDrillingFile: async (file: File) => {
          try {
            set({ loading: true, error: null })

            const logData = await parseDrillingDataFile(file)

            set({
              data: logData,
              currentWell: {
                id: generateWellId(),
                name: extractFileName(file),
              },
              loading: false,
            })

            return logData
          } catch (error) {
            const message = error instanceof Error ? error.message : 'Failed to process file'
            set({ error: message, loading: false })
            throw error
          }
        },
      }),
      {
        name: 'drilling-data-storage',
        partialize: (state) => ({
          data: state.data,
          currentWell: state.currentWell,
        }),
      }
    ),
    {
      name: 'drilling-store',
    }
  )
)

export const useDrillingData = () => useDrillingStore((state) => state.data)
export const useCurrentWell = () => useDrillingStore((state) => state.currentWell)
export const useIsLoading = () => useDrillingStore((state) => state.loading)
export const useError = () => useDrillingStore((state) => state.error)
