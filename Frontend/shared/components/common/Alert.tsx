import { ReactNode } from 'react'
import { X } from 'lucide-react'

interface AlertProps {
  type: 'success' | 'error' | 'warning' | 'info'
  message: string
  onClose?: () => void
  children?: ReactNode
}

export default function Alert({ type, message, onClose, children }: AlertProps) {
  const typeClasses = {
    success: 'bg-green-50 text-green-800 border-green-200',
    error: 'bg-red-50 text-red-800 border-red-200',
    warning: 'bg-yellow-50 text-yellow-800 border-yellow-200',
    info: 'bg-blue-50 text-blue-800 border-blue-200',
  }

  return (
    <div
      className={`border rounded-lg p-4 ${typeClasses[type]} ${
        onClose ? 'pr-10' : ''
      }`}
    >
      <div className="flex items-start">
        <div className="flex-1">
          <p className="font-medium">{message}</p>
          {children && <div className="mt-2">{children}</div>}
        </div>
        {onClose && (
          <button
            onClick={onClose}
            className="ml-4 text-current opacity-50 hover:opacity-75"
          >
            <X className="h-5 w-5" />
          </button>
        )}
      </div>
    </div>
  )
}
