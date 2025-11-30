export type MessageRole = 'user' | 'assistant' | 'system'
export type MessageStatus = 'sending' | 'sent' | 'error'

export interface ChatMessage {
  id: string
  role: MessageRole
  content: string
  timestamp: Date
  status?: MessageStatus
  error?: string
}

export interface ChatSession {
  id: string
  title?: string
  createdAt: Date
  updatedAt: Date
  metadata?: Record<string, unknown>
}

export interface ChatState {
  messages: ChatMessage[]
  currentSession: ChatSession | null
  sessionId: string | null
  isLoading: boolean
  isSending: boolean
  error: string | null
  isStreaming: boolean
  streamingStatus: string | null
}

export interface ChatActions {
  addMessage: (message: Omit<ChatMessage, 'id' | 'timestamp' | 'status'>) => void
  updateMessage: (id: string, updates: Partial<ChatMessage>) => void
  clearMessages: () => void

  createSession: (session?: Partial<ChatSession>) => void
  loadSession: (sessionId: string) => Promise<void>
  clearSession: () => void
  setSessionId: (sessionId: string | null) => void

  sendMessage: (content: string) => Promise<void>
  uploadFile: (file: File) => Promise<void>

  setLoading: (isLoading: boolean) => void
  setError: (error: string | null) => void

  setStreaming: (isStreaming: boolean) => void
  setStreamingStatus: (streamingStatus: string | null) => void
}

export interface ChatInputProps {
  value: string
  onChange: (value: string) => void
  onSend: () => void
  onFileUpload: (file: File) => void
  disabled?: boolean
  isSending?: boolean
}

export type ChatStore = ChatState & ChatActions

export const chatSelectors = {
  selectMessages: (state: ChatState) => state.messages,
  selectCurrentSession: (state: ChatState) => state.currentSession,
  selectIsLoading: (state: ChatState) => state.isLoading,
  selectIsSending: (state: ChatState) => state.isSending,
  selectError: (state: ChatState) => state.error,
}
