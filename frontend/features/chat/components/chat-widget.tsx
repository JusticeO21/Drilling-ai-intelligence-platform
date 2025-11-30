'use client'

import { useState } from 'react'
import { MessageCircle, X } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { ChatPanel } from './chat-panel'
import { useScreenSize } from '@/hooks/use-screen-size'

export function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false)
  const screenSize = useScreenSize()

  const isDesktop = screenSize === 'desktop'

  if (isDesktop) {
    return <ChatPanel className="h-full lg:w-100" />
  }

  return (
    <>
      <Button
        onClick={() => setIsOpen(true)}
        className="fixed bottom-4 right-4 z-50 h-14 w-14 rounded-full shadow-lg"
        size="icon"
      >
        <MessageCircle className="h-6 w-6" />
      </Button>

      {isOpen && (
        <div className="fixed inset-0 z-50 flex">
          <div className="absolute inset-0 bg-black/50" onClick={() => setIsOpen(false)} />

          <div className="relative ml-auto flex h-full w-full max-w-md flex-col bg-background shadow-xl">
            <Button
              onClick={() => setIsOpen(false)}
              variant="ghost"
              size="icon"
              className="absolute -top-1 right-4 lg:top-2 lg:right-2 z-10"
            >
              <X className="h-4 w-4" />
            </Button>

            <ChatPanel className="h-full border-0" />
          </div>
        </div>
      )}
    </>
  )
}
