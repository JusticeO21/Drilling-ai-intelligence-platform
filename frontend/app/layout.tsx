import type { Metadata } from 'next'
import { Inter, IBM_Plex_Sans } from 'next/font/google'
import './globals.css'
import { Providers } from './providers'
import { Toaster } from '@/components/ui/sonner'

const inter = Inter({
  variable: '--font-inter',
  subsets: ['latin'],
})

const ibmPlexSans = IBM_Plex_Sans({
  variable: '--font-ibm-plex-sans',
  subsets: ['latin'],
})

export const metadata: Metadata = {
  title: 'Drill AI Intelligence Dashboard',
  description: 'Intelligent platform for oil and gas drilling operations',
  icons: {
    icon: [
      { url: '/favicon.ico', type: 'image/x-icon' },
      { url: '/favicon-32x32.png', type: 'image/png', sizes: '32x32' },
      {
        url: '/android-chrome-192x192.png',
        type: 'image/png',
        sizes: '192x192',
      },
    ],
    apple: [{ url: '/apple-touch-icon.png', sizes: '180x180', type: 'image/png' }],
  },
  keywords: ['drilling', 'oil', 'gas', 'AI', 'dashboard', 'intelligence'],
  authors: [{ name: 'Justice Owusu' }],
  openGraph: {
    title: 'Drill AI Intelligence Dashboard',
    description: 'AI-powered drilling intelligence dashboard for oil and gas operations.',
    url: 'https://drill-intelligence.justiceowusu.com',
    siteName: 'Drill AI Intelligence Dashboard',
    images: [
      {
        url: '/og-image.jpg',
        width: 1200,
        height: 630,
        alt: 'Drill AI Intelligence Dashboard',
      },
    ],
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    site: '@_owusudev',
    creator: '@_owusudev',
  },
  alternates: {
    canonical: 'https://drill-intelligence.justiceowusu.com',
  },
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body className={`${inter.variable} ${ibmPlexSans.variable} antialiased  `}>
        <Toaster position="top-right" duration={8000} />
        <Providers>{children}</Providers>
      </body>
    </html>
  )
}
