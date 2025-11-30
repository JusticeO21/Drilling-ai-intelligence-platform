import { cn } from '@/lib/utils'
import { MessageRole } from '../types'
import ReactMarkdown from 'react-markdown'

interface ChatMessageProps {
  message: {
    id: string
    role: MessageRole
    content: string
    status?: 'sending' | 'sent' | 'error'
    error?: string
  }
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === 'user'
  const isError = message.status === 'error'

  return (
    <div
      className={cn(
        'w-full flex mb-4 last:mb-0 animate-in fade-in slide-in-from-bottom-2 duration-500',
        isUser ? 'justify-end' : 'justify-start'
      )}
    >
      <div
        className={cn(
          'whitespace-pre-wrap font-medium rounded-lg px-4 py-2 max-w-[80%] shadow-sm',
          isUser
            ? 'bg-gray-800 text-primary-foreground rounded-br-none'
            : 'bg-blue-300/40 rounded-bl-none',
          isError && 'border border-destructive'
        )}
      >
        <div className="whitespace-pre-wrap text-sm">
          <ReactMarkdown>{message.content}</ReactMarkdown>
        </div>

        {isError && message.error && (
          <div className="text-xs text-destructive mt-1">{message.error}</div>
        )}
      </div>
    </div>
  )
}
