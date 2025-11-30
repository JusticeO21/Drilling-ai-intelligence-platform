import { useCallback, useRef, ChangeEvent } from 'react'
import { toast } from 'sonner'
import { useDrillingStore } from '@/features/drilling/stores/drilling-store'
import { useChatStore } from '@/features/chat/stores/chat-slice'
import { parseDrillingDataFile } from '@/features/drilling/utils/data-parser'
import { uploadDrillingFile } from '@/lib/api'
import { CheckCircle2, AlertCircle } from 'lucide-react'

const UPLOAD_TOAST_ID = 'file-upload'

export function useFileUpload() {
  const { setData, setLoading, setError, loading } = useDrillingStore()
  const { setLoading: setChatLoading, createSession } = useChatStore()
  const inputRef = useRef<HTMLInputElement>(null)

  const handleUploadClick = useCallback(() => {
    inputRef.current?.click()
  }, [])

  const handleFileChange = useCallback(
    async (event: ChangeEvent<HTMLInputElement>) => {
      const file = event.target.files?.[0]
      if (!file) return

      toast.loading('Uploading file...', {
        id: UPLOAD_TOAST_ID,
        duration: Infinity,
      })

      setLoading(true)
      setError(null)

      try {
        const parsedData = await parseDrillingDataFile(file)
        setData(parsedData)

        setChatLoading(true)
        const response = await uploadDrillingFile(file)
        createSession({
          id: response.session_id,
          title: `File: ${file.name}`,
          metadata: { fileName: file.name, fileType: file.type },
        })
        setChatLoading(false)

        toast.dismiss(UPLOAD_TOAST_ID)
        toast.success('File uploaded successfully!', {
          description: 'Your drilling data has been processed and is now available.',
          duration: 5000,
          icon: <CheckCircle2 className="h-5 w-5 text-green-500" />,
        })
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Failed to process file'
        setError(errorMessage)

        toast.dismiss(UPLOAD_TOAST_ID)
        toast.error('Upload failed', {
          description: errorMessage,
          duration: 7000,
          icon: <AlertCircle className="h-5 w-5 text-red-500" />,
          action: {
            label: 'Retry',
            onClick: handleUploadClick,
          },
        })
      } finally {
        setLoading(false)
        if (inputRef.current) {
          inputRef.current.value = ''
        }
      }
    },
    [setData, setError, setLoading, setChatLoading, createSession, handleUploadClick]
  )

  return {
    inputRef,
    handleFileChange,
    isUploading: loading,
  }
}
