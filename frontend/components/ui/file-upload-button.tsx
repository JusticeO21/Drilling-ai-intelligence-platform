import { Button } from './button'
import { Upload } from 'lucide-react'
import { ChangeEvent, forwardRef, Ref } from 'react'

interface FileUploadButtonProps {
  onFileChange: (event: ChangeEvent<HTMLInputElement>) => void
  isUploading?: boolean
  accept?: string
  className?: string
  buttonText?: string
}

export const FileUploadButton = forwardRef<HTMLInputElement, FileUploadButtonProps>(
  (
    {
      onFileChange,
      isUploading = false,
      accept = '.xlsx,.xls,.csv',
      className = '',
      buttonText = 'Upload',
    },
    ref
  ) => {
    return (
      <div className={className}>
        <input
          type="file"
          ref={ref}
          onChange={onFileChange}
          className="hidden"
          accept={accept}
          disabled={isUploading}
        />
        <Button
          type="button"
          variant="secondary"
          onClick={() => (ref as any)?.current?.click()}
          disabled={isUploading}
          className="bg-blue-500 hover:bg-blue-400 transition-colors text-white/80"
        >
          <Upload className="mr-2 h-4 w-4" />
          {isUploading ? 'Uploading...' : buttonText}
        </Button>
      </div>
    )
  }
)

FileUploadButton.displayName = 'FileUploadButton'
