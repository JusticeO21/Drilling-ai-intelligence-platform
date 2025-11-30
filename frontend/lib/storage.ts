export interface DrillingSession {
  sessionId: string
  filename: string
  uploadedAt: string
}

export interface ChatMessage {
  role: 'user' | 'assistant' | 'system'
  content: string
  timestamp: string
}

export type ChatHistory = ChatMessage[]

export const STORAGE_KEYS = {
  DRILLING_SESSION: 'drilling_session',
  CHAT_HISTORY: 'chat_history',
} as const

export type StorageKey = (typeof STORAGE_KEYS)[keyof typeof STORAGE_KEYS]

export interface StorageOptions {
  maxSize?: number
  ttl?: number
  version?: string
}

export interface StorageMetadata {
  version: string
  timestamp: number
  size: number
}

export interface StorageItem<T> {
  data: T
  metadata: StorageMetadata
}

// Custom Errors

export class StorageError extends Error {
  constructor(
    message: string,
    public readonly key: string,
    public readonly cause?: unknown
  ) {
    super(message)
    this.name = 'StorageError'
  }
}

export class StorageQuotaExceededError extends StorageError {
  constructor(key: string, cause?: unknown) {
    super('Storage quota exceeded', key, cause)
    this.name = 'StorageQuotaExceededError'
  }
}

export class StorageCorruptedError extends StorageError {
  constructor(key: string, cause?: unknown) {
    super('Storage data is corrupted', key, cause)
    this.name = 'StorageCorruptedError'
  }
}

// Storage Adapter Interface

interface IStorageAdapter {
  getItem(key: string): string | null
  setItem(key: string, value: string): void
  removeItem(key: string): void
  clear(): void
}

class LocalStorageAdapter implements IStorageAdapter {
  private isAvailable(): boolean {
    return typeof window !== 'undefined' && 'localStorage' in window
  }

  getItem(key: string): string | null {
    if (!this.isAvailable()) return null
    return localStorage.getItem(key)
  }

  setItem(key: string, value: string): void {
    if (!this.isAvailable()) {
      throw new StorageError('localStorage not available', key)
    }
    localStorage.setItem(key, value)
  }

  removeItem(key: string): void {
    if (!this.isAvailable()) return
    localStorage.removeItem(key)
  }

  clear(): void {
    if (!this.isAvailable()) return
    localStorage.clear()
  }
}

// Core Storage Service

export class StorageService {
  private adapter: IStorageAdapter
  private defaultOptions: Required<StorageOptions>

  constructor(
    adapter: IStorageAdapter = new LocalStorageAdapter(),
    defaultOptions?: StorageOptions
  ) {
    this.adapter = adapter
    this.defaultOptions = {
      maxSize: 5 * 1024 * 1024, // 5MB default
      ttl: 0, // no expiration by default
      version: '1.0',
      ...defaultOptions,
    }
  }

  private createStorageItem<T>(data: T, options: StorageOptions): StorageItem<T> {
    const serialized = JSON.stringify(data)
    return {
      data,
      metadata: {
        version: options.version || this.defaultOptions.version,
        timestamp: Date.now(),
        size: new Blob([serialized]).size,
      },
    }
  }

  private validateStorageItem<T>(item: StorageItem<T>, options: StorageOptions): void {
    const { ttl, maxSize } = { ...this.defaultOptions, ...options }

    if (ttl > 0 && Date.now() - item.metadata.timestamp > ttl) {
      throw new StorageError('Storage item has expired', 'ttl_expired')
    }

    if (maxSize > 0 && item.metadata.size > maxSize) {
      throw new StorageError('Storage item exceeds max size', 'max_size_exceeded')
    }
  }

  getItem<T>(key: StorageKey, options?: StorageOptions): T | null {
    try {
      const raw = this.adapter.getItem(key)
      if (!raw) return null

      const item = JSON.parse(raw) as StorageItem<T>

      this.validateStorageItem(item, options || {})

      return item.data
    } catch (error) {
      if (error instanceof StorageError) {
        throw error
      }

      console.warn(`Error reading from storage key "${key}":`, error)

      // Clean up corrupted data
      this.removeItem(key)
      throw new StorageCorruptedError(key, error)
    }
  }

  setItem<T>(key: StorageKey, value: T, options?: StorageOptions): void {
    try {
      const mergedOptions = { ...this.defaultOptions, ...options }
      const item = this.createStorageItem(value, mergedOptions)
      const serialized = JSON.stringify(item)

      // Check if serialized data exceeds max size
      const size = new Blob([serialized]).size
      if (mergedOptions.maxSize > 0 && size > mergedOptions.maxSize) {
        throw new StorageError(
          `Data size (${size} bytes) exceeds max size (${mergedOptions.maxSize} bytes)`,
          key
        )
      }

      this.adapter.setItem(key, serialized)
    } catch (error) {
      if (error instanceof DOMException && error.name === 'QuotaExceededError') {
        throw new StorageQuotaExceededError(key, error)
      }

      if (error instanceof StorageError) {
        throw error
      }

      console.warn(`Error writing to storage key "${key}":`, error)
      throw new StorageError('Failed to write to storage', key, error)
    }
  }

  removeItem(key: StorageKey): void {
    try {
      this.adapter.removeItem(key)
    } catch (error) {
      console.warn(`Error removing storage key "${key}":`, error)
      throw new StorageError('Failed to remove from storage', key, error)
    }
  }

  clear(keysOnly?: StorageKey[]): void {
    try {
      if (keysOnly) {
        keysOnly.forEach((key) => this.adapter.removeItem(key))
      } else {
        Object.values(STORAGE_KEYS).forEach((key) => this.adapter.removeItem(key))
      }
    } catch (error) {
      console.warn('Error clearing storage:', error)
      throw new StorageError('Failed to clear storage', 'clear', error)
    }
  }

  has(key: StorageKey): boolean {
    try {
      return this.adapter.getItem(key) !== null
    } catch {
      return false
    }
  }

  getMetadata(key: StorageKey): StorageMetadata | null {
    try {
      const raw = this.adapter.getItem(key)
      if (!raw) return null

      const item = JSON.parse(raw) as StorageItem<unknown>
      return item.metadata
    } catch {
      return null
    }
  }
}

//  Storage Repositories

export class TypedStorageRepository<T> {
  constructor(
    private storage: StorageService,
    private key: StorageKey,
    private options?: StorageOptions
  ) {}

  get(): T | null {
    try {
      return this.storage.getItem<T>(this.key, this.options)
    } catch (error) {
      if (error instanceof StorageCorruptedError) {
        return null
      }
      throw error
    }
  }

  set(value: T): void {
    this.storage.setItem(this.key, value, this.options)
  }

  remove(): void {
    this.storage.removeItem(this.key)
  }

  exists(): boolean {
    return this.storage.has(this.key)
  }

  getMetadata(): StorageMetadata | null {
    return this.storage.getMetadata(this.key)
  }

  update(updater: (current: T | null) => T): void {
    const current = this.get()
    const updated = updater(current)
    this.set(updated)
  }
}

// Domain-Specific Storage Repositories

export class DrillingSessionRepository extends TypedStorageRepository<DrillingSession> {
  constructor(storage: StorageService) {
    super(storage, STORAGE_KEYS.DRILLING_SESSION, {
      ttl: 24 * 60 * 60 * 1000, // 24 hours
    })
  }

  updateSession(updates: Partial<DrillingSession>): void {
    this.update((current) => ({
      ...current!,
      ...updates,
    }))
  }
}

export class ChatHistoryRepository extends TypedStorageRepository<ChatHistory> {
  constructor(storage: StorageService) {
    super(storage, STORAGE_KEYS.CHAT_HISTORY, {
      maxSize: 2 * 1024 * 1024,
    })
  }

  addMessage(message: ChatMessage): void {
    this.update((current) => [...(current || []), message])
  }

  getRecentMessages(count: number): ChatMessage[] {
    const history = this.get() || []
    return history.slice(-count)
  }

  clearOldMessages(olderThanMs: number): void {
    const cutoff = Date.now() - olderThanMs
    this.update((current) =>
      (current || []).filter((msg) => new Date(msg.timestamp).getTime() > cutoff)
    )
  }

  getMessageCount(): number {
    return (this.get() || []).length
  }
}

// Factory & Singleton

export class StorageFactory {
  private static storageService: StorageService | null = null

  static getStorageService(options?: StorageOptions): StorageService {
    if (!this.storageService) {
      this.storageService = new StorageService(new LocalStorageAdapter(), options)
    }
    return this.storageService
  }

  static createDrillingSessionRepository(): DrillingSessionRepository {
    return new DrillingSessionRepository(this.getStorageService())
  }

  static createChatHistoryRepository(): ChatHistoryRepository {
    return new ChatHistoryRepository(this.getStorageService())
  }

  static reset(): void {
    this.storageService = null
  }
}

// Exports purposes

const defaultStorage = StorageFactory.getStorageService()

export const getStorageItem = <T>(key: StorageKey): T | null => {
  try {
    return defaultStorage.getItem<T>(key)
  } catch (error) {
    if (error instanceof StorageCorruptedError) {
      return null
    }
    throw error
  }
}

export const setStorageItem = <T>(key: StorageKey, value: T): boolean => {
  try {
    defaultStorage.setItem(key, value)
    return true
  } catch {
    return false
  }
}

export const removeStorageItem = (key: StorageKey): void => {
  defaultStorage.removeItem(key)
}

export const clearStorage = (): void => {
  defaultStorage.clear()
}

export const drillingSessionStorage = StorageFactory.createDrillingSessionRepository()
export const chatHistoryStorage = StorageFactory.createChatHistoryRepository()
