'use client'
import Link from 'next/link'
import { Button } from '@/components/ui/button'

export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center h-screen gap-4">
      <div className="text-center space-y-2">
        <h1 className="text-6xl font-bold text-gray-900 dark:text-gray-100">404</h1>
        <p className="text-lg text-gray-600 dark:text-gray-400">Page not found</p>
      </div>

      <Button asChild variant="default">
        <Link href="/">Go back home</Link>
      </Button>
    </div>
  )
}
