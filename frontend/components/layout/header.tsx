'use client'
import { useChatStore } from '@/features/chat/stores/chat-slice'

export const Header = () => {
  const { isStreaming, setStreaming } = useChatStore()

  return (
    <header className="border-b bg-white px-6 py-3 flex items-center justify-between w-full">
      <h1 className="text-xl font-semibold">Drill AI Intelligence Platform</h1>
      <div className="hidden  items-center gap-2 md:flex">
        <label className="text-sm font-medium">Streaming</label>
        <input
          type="checkbox"
          checked={isStreaming}
          onChange={(e) => setStreaming(e.target.checked)}
          className="h-4 w-4"
        />
      </div>
    </header>
  )
}
