import type { LogData } from '../types/drilling.types'

const createFormData = (file: File): FormData => {
  const formData = new FormData()
  formData.append('file', file)
  return formData
}

const handleParseError = async (response: Response): Promise<never> => {
  const errorData = await response.json().catch(() => ({ error: 'Unknown error' }))
  const message = errorData.error || `HTTP ${response.status}: ${response.statusText}`
  throw new Error(message)
}

export async function parseDrillingDataFile(file: File): Promise<LogData[]> {
  const formData = createFormData(file)

  const response = await fetch('/api/parse-file', {
    method: 'POST',
    body: formData,
  })

  if (!response.ok) {
    await handleParseError(response)
  }

  const result = await response.json()
  return result.data
}
