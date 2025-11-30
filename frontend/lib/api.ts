export interface FileProcessingResponse {
  filename: string
  file_type: string
  num_rows: number
  num_columns: number
  columns: string[]
  sample_data: Record<string, any>[]
  session_id: string
  chunks_count: number
}

export interface QueryRequest {
  session_id: string
  question: string
  n_results?: number
}

export interface QueryResponse {
  session_id: string
  question: string
  relevant_chunks: string[]
  distances: number[]
}

export interface SessionInfo {
  session_id: string
  created_at: string
  expires_at: string
  last_accessed: string
}

export interface Message {
  role: 'user' | 'assistant' | 'system'
  content: string
}

export interface ChatRequest {
  session_id: string
  message: Message
  stream?: boolean
  chat_history?: Message[]
}

export interface ChatResponse {
  message: Message
  session_id: string
  model_provider: string
  processing_time?: number
}

export interface StreamData {
  type: 'status' | 'content' | 'error'
  message?: string
  delta?: string
}

export interface ApiError {
  detail: string
  status?: number
}

// Configuration

class ApiConfig {
  private static instance: ApiConfig
  private baseUrl: string

  private constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'
  }

  static getInstance(): ApiConfig {
    if (!ApiConfig.instance) {
      ApiConfig.instance = new ApiConfig()
    }
    return ApiConfig.instance
  }

  getBaseUrl(): string {
    return this.baseUrl
  }

  setBaseUrl(url: string): void {
    this.baseUrl = url
  }
}

// HTTP Client

class HttpClient {
  private baseUrl: string

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl
  }

  private async handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({
        detail: `HTTP ${response.status}: ${response.statusText}`,
      }))

      const error = new Error(errorData.detail || 'Request failed') as Error & ApiError
      error.status = response.status
      throw error
    }

    return response.json()
  }

  async post<T>(endpoint: string, body: any, headers?: HeadersInit): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...headers,
      },
      body: JSON.stringify(body),
    })

    return this.handleResponse<T>(response)
  }

  async postFormData<T>(endpoint: string, formData: FormData): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      method: 'POST',
      body: formData,
    })

    return this.handleResponse<T>(response)
  }

  async get<T>(endpoint: string): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`)
    return this.handleResponse<T>(response)
  }

  async postStream(endpoint: string, body: any): Promise<ReadableStreamDefaultReader<Uint8Array>> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }))
      throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`)
    }

    const reader = response.body?.getReader()
    if (!reader) {
      throw new Error('Response body not available')
    }

    return reader
  }
}

// Stream Parser

class StreamParser {
  private decoder = new TextDecoder()
  private buffer = ''

  parseChunk(value: Uint8Array): StreamData[] {
    this.buffer += this.decoder.decode(value, { stream: true })
    const lines = this.buffer.split('\n')
    this.buffer = lines.pop() || ''

    const results: StreamData[] = []

    for (const line of lines) {
      if (line.startsWith('data: ')) {
        try {
          const data = JSON.parse(line.slice(6)) as StreamData
          results.push(data)
        } catch (error) {
          console.error('Failed to parse stream data:', error)
        }
      }
    }

    return results
  }

  reset(): void {
    this.buffer = ''
  }
}

// API Services

export class DrillingApiService {
  private client: HttpClient

  constructor(baseUrl?: string) {
    const config = ApiConfig.getInstance()
    this.client = new HttpClient(baseUrl || config.getBaseUrl())
  }

  async uploadFile(file: File): Promise<FileProcessingResponse> {
    const formData = new FormData()
    formData.append('file', file)
    return this.client.postFormData<FileProcessingResponse>('/drilling/upload', formData)
  }

  async query(query: QueryRequest): Promise<QueryResponse> {
    return this.client.post<QueryResponse>('/drilling/query', query)
  }

  async getSession(sessionId: string): Promise<SessionInfo> {
    return this.client.get<SessionInfo>(`/drilling/session/${sessionId}`)
  }
}

export class ChatApiService {
  private client: HttpClient

  constructor(baseUrl?: string) {
    const config = ApiConfig.getInstance()
    this.client = new HttpClient(baseUrl || config.getBaseUrl())
  }

  async sendMessage(chatRequest: ChatRequest): Promise<ChatResponse> {
    return this.client.post<ChatResponse>('/chat/', chatRequest)
  }

  async sendStreamingMessage(
    chatRequest: ChatRequest,
    callbacks: {
      onMessageAdd: (message: Message) => void
      onStatusUpdate: (status: string | null) => void
    }
  ): Promise<void> {
    const reader = await this.client.postStream('/chat/', { ...chatRequest, stream: true })
    const parser = new StreamParser()

    try {
      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const dataItems = parser.parseChunk(value)

        for (const data of dataItems) {
          if (data.type === 'status' && data.message) {
            callbacks.onStatusUpdate(data.message)
          } else if (data.type === 'content' && data.delta) {
            callbacks.onStatusUpdate(null)
            callbacks.onMessageAdd({ role: 'assistant', content: data.delta })
          } else if (data.type === 'error' && data.message) {
            throw new Error(data.message)
          }
        }
      }
    } finally {
      parser.reset()
    }
  }
}

// Factory & Exports

export class ApiServiceFactory {
  static createDrillingService(baseUrl?: string): DrillingApiService {
    return new DrillingApiService(baseUrl)
  }

  static createChatService(baseUrl?: string): ChatApiService {
    return new ChatApiService(baseUrl)
  }
}

export const uploadDrillingFile = (file: File) =>
  ApiServiceFactory.createDrillingService().uploadFile(file)

export const queryDrillingData = (query: QueryRequest) =>
  ApiServiceFactory.createDrillingService().query(query)

export const getSessionInfo = (sessionId: string) =>
  ApiServiceFactory.createDrillingService().getSession(sessionId)

export const sendChatMessage = (chatRequest: ChatRequest) =>
  ApiServiceFactory.createChatService().sendMessage(chatRequest)

export const sendStreamingMessage = (
  chatRequest: ChatRequest,
  onMessageAdd: (message: Message) => void,
  onStatusUpdate: (status: string | null) => void
) =>
  ApiServiceFactory.createChatService().sendStreamingMessage(chatRequest, {
    onMessageAdd,
    onStatusUpdate,
  })
