'use client'

import { ReactNode } from 'react'
import { useAuth } from '@/contexts/AuthContext'
import Navbar from './Navbar'
import Loading from '@/components/common/Loading'

interface LayoutProps {
  children: ReactNode
  requireAuth?: boolean
  requireAdmin?: boolean
}

export default function Layout({
  children,
  requireAuth = true,
  requireAdmin = false,
}: LayoutProps) {
  const { loading, isAuthenticated, isAdmin } = useAuth()

  if (loading) {
    return <Loading />
  }

  if (requireAuth && !isAuthenticated) {
    if (typeof window !== 'undefined') {
      window.location.href = '/login'
    }
    return <Loading />
  }

  if (requireAdmin && !isAdmin) {
    if (typeof window !== 'undefined') {
      window.location.href = '/'
    }
    return <Loading />
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>
    </div>
  )
}
