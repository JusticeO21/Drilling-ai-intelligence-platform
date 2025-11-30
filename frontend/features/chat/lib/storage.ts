import { ChatMessage, ChatSession } from '../types'

const STORAGE_KEYS = {
  MESSAGES: 'chat_messages',
  SESSION: 'chat_session',
} as const

const parseJSON = <T>(data: string | null, fallback: T): T => {
  if (!data) return fallback
  try {
    return JSON.parse(data)
  } catch {
    return fallback
  }
}

const safeStorage = {
  get: (key: string): string | null => {
    try {
      return localStorage.getItem(key)
    } catch {
      return null
    }
  },
  set: (key: string, value: string): void => {
    try {
      localStorage.setItem(key, value)
    } catch (error) {
      console.error(`Storage error (${key}):`, error)
    }
  },
  remove: (key: string): void => {
    try {
      localStorage.removeItem(key)
    } catch (error) {
      console.error(`Storage error (${key}):`, error)
    }
  },
}

const serializeMessage = (msg: ChatMessage) => ({
  ...msg,
  timestamp: msg.timestamp.toISOString(),
})

const deserializeMessage = (msg: any): ChatMessage => ({
  ...msg,
  timestamp: new Date(msg.timestamp),
})

const serializeSession = (session: ChatSession) => ({
  ...session,
  createdAt: session.createdAt.toISOString(),
  updatedAt: session.updatedAt.toISOString(),
})

const deserializeSession = (session: any): ChatSession => ({
  ...session,
  createdAt: new Date(session.createdAt),
  updatedAt: new Date(session.updatedAt),
})

export const chatStorage = {
  getMessages: (): ChatMessage[] => {
    const data = safeStorage.get(STORAGE_KEYS.MESSAGES)
    const messages = parseJSON<any[]>(data, [])
    return messages.map(deserializeMessage)
  },

  saveMessages: (messages: ChatMessage[]): void => {
    const serialized = JSON.stringify(messages.map(serializeMessage))
    safeStorage.set(STORAGE_KEYS.MESSAGES, serialized)
  },

  getSession: (): ChatSession | null => {
    const data = safeStorage.get(STORAGE_KEYS.SESSION)
    const session = parseJSON<any>(data, null)
    return session ? deserializeSession(session) : null
  },

  saveSession: (session: ChatSession | null): void => {
    if (!session) {
      safeStorage.remove(STORAGE_KEYS.SESSION)
      return
    }
    const serialized = JSON.stringify(serializeSession(session))
    safeStorage.set(STORAGE_KEYS.SESSION, serialized)
  },

  clear: (): void => {
    safeStorage.remove(STORAGE_KEYS.MESSAGES)
    safeStorage.remove(STORAGE_KEYS.SESSION)
  },
}
