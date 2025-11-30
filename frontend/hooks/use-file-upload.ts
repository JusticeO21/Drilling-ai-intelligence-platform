import { useState } from 'react'

interface UseFileUploadProps {
  onUploadSuccess?: (data: any) => void
  onUploadError?: (error: Error) => void
}

export function useFileUpload({ onUploadSuccess, onUploadError }: UseFileUploadProps = {}) {
  const [isUploading, setIsUploading] = useState(false)
  const [error, setError] = useState<Error | null>(null)

  const uploadFile = async (file: File) => {
    if (!file) return

    setIsUploading(true)
    setError(null)

    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error(`Upload failed: ${response.statusText}`)
      }

      const data = await response.json()
      onUploadSuccess?.(data)
      return data
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Failed to upload file')
      setError(error)
      onUploadError?.(error)
      throw error
    } finally {
      setIsUploading(false)
    }
  }

  return {
    uploadFile,
    isUploading,
    error,
  }
}
