import { useEffect, useCallback } from 'react'
import { toast } from 'sonner'
import { useChatStore } from '../stores/chat-slice'

export function useChatPanel(input: string, setInput: (value: string) => void) {
  const { messages, isSending, isLoading, error, sendMessage, uploadFile, addMessage, setError } =
    useChatStore()

  const handleSend = useCallback(async () => {
    const content = input.trim()
    if (!content || isSending) return

    setInput('')

    try {
      await sendMessage(content)
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to send message'
      toast.error(errorMessage)
    }
  }, [input, isSending, setInput, sendMessage])

  const handleFileUpload = useCallback(
    async (file: File) => {
      try {
        await uploadFile(file)
        toast.success('The file has been successfully processed.')
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : 'Failed to upload file'
        toast.error(errorMessage)
      }
    },
    [uploadFile]
  )

  useEffect(() => {
    if (error) {
      toast.error(error)
      setError(null)
    }
  }, [error, setError])

  useEffect(() => {
    if (messages.length === 0 && !isLoading) {
      addMessage({
        role: 'assistant',
        content:
          "Hi! I'm your drilling data assistant. Upload a file to get started or ask me anything about drilling data.",
      })
    }
  }, [addMessage, isLoading, messages.length])

  return {
    handleSend,
    handleFileUpload,
  }
}
