import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Particle Painting Animator',
  description: 'Transform your paintings into magical particle animations',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-gradient-to-br from-dark-900 via-dark-800 to-dark-900 min-h-screen`}>
        {children}
      </body>
    </html>
  )
}
