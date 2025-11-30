import { create } from 'zustand'

export interface Well {
  id: string
  label: string
  depth: number
}

interface WellsState {
  wells: Well[]
  currentWell: Well | null
  setWells: (wells: Well[]) => void
  setCurrentWell: (well: Well | null) => void
}

export const useWellsStore = create<WellsState>((set) => ({
  wells: [],
  currentWell: null,
  setWells: (wells) => set({ wells }),
  setCurrentWell: (currentWell) => set({ currentWell }),
}))
