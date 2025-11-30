import { create } from 'zustand'
import { devtools } from 'zustand/middleware'
import { v4 as uuidv4 } from 'uuid'
import { uploadDrillingFile, sendChatMessage, sendStreamingMessage } from '@/lib/api'
import { chatStorage } from '../lib/storage'
import { ChatStore, ChatMessage, ChatSession } from '../types'

const createInitialState = () => ({
  messages: chatStorage.getMessages(),
  currentSession: chatStorage.getSession(),
  sessionId: chatStorage.getSession()?.id || null,
  isLoading: false,
  isSending: false,
  error: null as string | null,
  isStreaming: true,
  streamingStatus: null as string | null,
})

const createMessage = (message: Partial<ChatMessage>): ChatMessage =>
  ({
    id: uuidv4(),
    timestamp: new Date(),
    status: 'sent',
    ...message,
  }) as ChatMessage

const createSession = (session?: Partial<ChatSession>): ChatSession => ({
  id: session?.id || uuidv4(),
  title: session?.title || 'New Chat',
  createdAt: new Date(),
  updatedAt: new Date(),
  metadata: session?.metadata,
})

export const useChatStore = create<ChatStore>()(
  devtools(
    (set, get) => ({
      ...createInitialState(),

      addMessage: (message) => {
        const newMessage = createMessage(message)
        set((state) => {
          const messages = [...state.messages, newMessage]
          chatStorage.saveMessages(messages)
          return { messages }
        })
      },

      updateMessage: (id, updates) => {
        set((state) => {
          const messages = state.messages.map((msg) =>
            msg.id === id ? { ...msg, ...updates } : msg
          )
          chatStorage.saveMessages(messages)
          return { messages }
        })
      },

      clearMessages: () => {
        set({ messages: [] })
        chatStorage.saveMessages([])
      },

      createSession: (session) => {
        const newSession = createSession(session)
        set({
          currentSession: newSession,
          sessionId: newSession.id,
          messages: [],
        })
        chatStorage.saveSession(newSession)
        chatStorage.saveMessages([])
      },

      loadSession: async (sessionId) => {
        const session = chatStorage.getSession()
        if (session?.id === sessionId) {
          set({
            currentSession: session,
            messages: chatStorage.getMessages(),
          })
        }
      },

      clearSession: () => {
        set({
          currentSession: null,
          sessionId: null,
          messages: [],
        })
        chatStorage.clear()
      },

      setSessionId: (sessionId) => set({ sessionId }),

      sendMessage: async (content) => {
        const state = get()
        let currentSessionId = state.sessionId

        if (!currentSessionId) {
          state.createSession({ title: 'New Chat' })
          currentSessionId = get().sessionId
        }

        const userMessage = createMessage({
          role: 'user',
          content,
          status: 'sending',
        })

        state.addMessage(userMessage)

        try {
          set({ isSending: true, error: null })

          if (state.isStreaming) {
            await sendStreamingMessage(
              {
                session_id: currentSessionId!,
                message: { role: 'user', content },
                stream: true,
              },
              state.addMessage,
              state.setStreamingStatus
            )
          } else {
            const chatHistory = state.messages
              .filter((msg) => msg.role !== 'system')
              .map(({ role, content }) => ({ role, content }))

            const response = await sendChatMessage({
              session_id: currentSessionId!,
              message: { role: 'user', content },
              chat_history: chatHistory,
            })

            state.addMessage({
              role: response.message.role as 'assistant',
              content: response.message.content,
            })
          }

          state.updateMessage(userMessage.id, { status: 'sent' })
        } catch (error) {
          const errorMessage = error instanceof Error ? error.message : 'Failed to send message'
          set({ error: errorMessage })
          state.updateMessage(userMessage.id, { status: 'sent' })
          state.addMessage({
            role: 'assistant',
            content: `Sorry, I encountered an error: ${errorMessage}. Please try again.`,
          })
        } finally {
          set({ isSending: false, streamingStatus: null })
        }
      },

      uploadFile: async (file) => {
        const state = get()

        try {
          set({ isLoading: true, error: null })

          state.createSession({
            title: `File: ${file.name}`,
            metadata: { fileName: file.name, fileType: file.type },
          })

          const response = await uploadDrillingFile(file)

          set((state) => ({
            currentSession: state.currentSession
              ? {
                  ...state.currentSession,
                  metadata: {
                    ...state.currentSession.metadata,
                    fileInfo: {
                      name: response.filename,
                      type: response.file_type,
                      size: file.size,
                    },
                  },
                }
              : null,
          }))

          state.addMessage({
            role: 'assistant',
            content: `I've successfully processed your file "${file.name}". You can now ask me questions about the data.`,
          })
        } catch (error) {
          const errorMessage = error instanceof Error ? error.message : 'Failed to process file'
          set({ error: errorMessage })
          state.addMessage({
            role: 'assistant',
            content: `Sorry, I couldn't process the file. ${errorMessage}`,
            error: errorMessage,
          })
        } finally {
          set({ isLoading: false })
        }
      },

      setLoading: (isLoading) => set({ isLoading }),
      setError: (error) => set({ error }),
      setStreaming: (isStreaming) => set({ isStreaming }),
      setStreamingStatus: (streamingStatus) => set({ streamingStatus }),
    }),
    {
      name: 'ChatStore',
      enabled: process.env.NODE_ENV === 'development',
    }
  )
)

export const useMessages = () => useChatStore((state) => state.messages)
export const useCurrentSession = () => useChatStore((state) => state.currentSession)
export const useIsLoading = () => useChatStore((state) => state.isLoading)
export const useIsSending = () => useChatStore((state) => state.isSending)
export const useError = () => useChatStore((state) => state.error)
