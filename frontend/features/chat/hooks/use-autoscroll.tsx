import { useEffect, RefObject } from 'react'
import { ChatMessage } from '../types'

export function useAutoScroll(
  scrollAreaRef: RefObject<HTMLDivElement | null>,
  messages: ChatMessage[]
) {
  useEffect(() => {
    const viewport = scrollAreaRef.current?.querySelector('[data-slot="scroll-area-viewport"]')
    if (viewport) {
      viewport.scrollTo({ top: viewport.scrollHeight, behavior: 'smooth' })
    }
  }, [messages, scrollAreaRef])
}
