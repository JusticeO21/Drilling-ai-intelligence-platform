'use client'

import { useRef, useState } from 'react'
import { Button, ScrollArea } from '@/components/ui'
import { ArrowUpIcon, Loader2, Upload } from 'lucide-react'
import { useChatStore } from '../stores/chat-slice'
import { useDrillingStore } from '@/features/drilling/stores/drilling-store'
import { ChatMessage } from './chat-message'
import { ClearHistoryDialog } from './clear-history-dialog'
import { ChatInputProps } from '../types'
import { cn } from '@/lib/utils'
import { useChatPanel, useAutoScroll } from '../hooks'

const ChatInput = ({
  value,
  onChange,
  onSend,
  onFileUpload,
  disabled = false,
  isSending = false,
}: ChatInputProps) => {
  const fileInputRef = useRef<HTMLInputElement>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      onSend()
    }
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    onFileUpload(file)
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  return (
    <div className="border-t p-4 bg-background">
      <div className="flex items-end gap-2">
        <label className="cursor-pointer p-2 rounded-full hover:bg-muted transition-colors">
          <Upload className="h-5 w-5 text-muted-foreground" />
          <input
            ref={fileInputRef}
            type="file"
            className="hidden"
            accept=".xlsx,.xls,.csv"
            onChange={handleFileChange}
            disabled={disabled || isSending}
          />
        </label>

        <textarea
          ref={textareaRef}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type a message..."
          className="flex-1 min-h-[40px] max-h-[200px] rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background outline-none resize-none placeholder:text-muted-foreground disabled:cursor-not-allowed disabled:opacity-50 scrollbar-hide"
          disabled={disabled || isSending}
          rows={1}
        />

        <Button
          size="icon"
          onClick={onSend}
          disabled={!value.trim() || disabled || isSending}
          className="h-10 w-10"
        >
          <ArrowUpIcon className="h-4 w-4" />
        </Button>
      </div>
    </div>
  )
}

const ChatHeader = () => {
  const { currentSession, messages } = useChatStore()
  const title = currentSession?.title || 'New Chat'

  return (
    <div className="border-b p-4 flex items-center justify-between">
      <h2 className="text-lg font-semibold truncate">{title}</h2>
      {messages.length > 1 && <ClearHistoryDialog />}
    </div>
  )
}

const LoadingIndicator = ({ type }: { type: 'analyzing' | 'sending' }) => (
  <div className="flex gap-3">
    <div className="rounded-lg px-3 py-2 max-w-[70%] bg-blue-100">
      {type === 'analyzing' ? (
        <p className="text-sm">Analyzing your data...</p>
      ) : (
        <Loader2 className="h-4 w-4 animate-spin text-blue-500" />
      )}
    </div>
  </div>
)

const StreamingStatus = ({ status }: { status: string }) => (
  <div className="flex gap-3">
    <div className="rounded-lg px-3 py-2 max-w-[70%] bg-green-100">
      <div className="flex items-center gap-2">
        <Loader2 className="h-4 w-4 animate-spin text-green-600" />
        <span className="text-sm text-green-800">{status}</span>
      </div>
    </div>
  </div>
)

export function ChatPanel({ className }: { className?: string }) {
  const [input, setInput] = useState('')
  const scrollAreaRef = useRef<HTMLDivElement>(null)

  const { messages, isSending, isLoading, streamingStatus } = useChatStore()
  const { loading: drillingLoading } = useDrillingStore()

  const { handleSend, handleFileUpload } = useChatPanel(input, setInput)

  useAutoScroll(scrollAreaRef, messages)

  const isDisabled = isLoading || drillingLoading

  return (
    <div className={cn('relative bg-background w-full md:w-full lg:w-80 border', className)}>
      <div className="flex flex-col h-full">
        <ChatHeader />

        <ScrollArea className="flex-1 p-4 overflow-y-auto" ref={scrollAreaRef}>
          <div className="space-y-4">
            {messages.map((message) => (
              <ChatMessage key={message.id} message={message} />
            ))}

            {isLoading && <LoadingIndicator type="analyzing" />}
            {isSending && <LoadingIndicator type="sending" />}
            {streamingStatus && <StreamingStatus status={streamingStatus} />}
          </div>
        </ScrollArea>

        <ChatInput
          value={input}
          onChange={setInput}
          onSend={handleSend}
          onFileUpload={handleFileUpload}
          disabled={isDisabled}
          isSending={isSending}
        />
      </div>
    </div>
  )
}
