'use client'

import Link from 'next/link'
import { useAuth } from '@/contexts/AuthContext'
import { Calendar, User, Settings, LogOut, Menu } from 'lucide-react'
import { useState } from 'react'

export default function Navbar() {
  const { user, logout, isAdmin } = useAuth()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <nav className="bg-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="flex items-center space-x-2">
              <Calendar className="h-8 w-8 text-primary-600" />
              <span className="text-xl font-bold text-gray-900">
                Sistema de Citas
              </span>
            </Link>
          </div>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center space-x-4">
            <Link
              href="/appointments"
              className="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium"
            >
              Mis Citas
            </Link>
            <Link
              href="/catalog"
              className="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium"
            >
              Servicios
            </Link>
            {isAdmin && (
              <Link
                href="/admin"
                className="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium"
              >
                Administración
              </Link>
            )}
            <Link
              href="/profile"
              className="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium flex items-center"
            >
              <User className="h-4 w-4 mr-1" />
              {user?.full_name || user?.email}
            </Link>
            <button
              onClick={logout}
              className="text-red-600 hover:text-red-700 px-3 py-2 rounded-md text-sm font-medium flex items-center"
            >
              <LogOut className="h-4 w-4 mr-1" />
              Salir
            </button>
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="text-gray-700 hover:text-primary-600"
            >
              <Menu className="h-6 w-6" />
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 border-t">
            <Link
              href="/appointments"
              className="text-gray-700 hover:text-primary-600 block px-3 py-2 rounded-md text-base font-medium"
              onClick={() => setMobileMenuOpen(false)}
            >
              Mis Citas
            </Link>
            <Link
              href="/catalog"
              className="text-gray-700 hover:text-primary-600 block px-3 py-2 rounded-md text-base font-medium"
              onClick={() => setMobileMenuOpen(false)}
            >
              Servicios
            </Link>
            {isAdmin && (
              <Link
                href="/admin"
                className="text-gray-700 hover:text-primary-600 block px-3 py-2 rounded-md text-base font-medium"
                onClick={() => setMobileMenuOpen(false)}
              >
                Administración
              </Link>
            )}
            <Link
              href="/profile"
              className="text-gray-700 hover:text-primary-600 block px-3 py-2 rounded-md text-base font-medium"
              onClick={() => setMobileMenuOpen(false)}
            >
              Perfil
            </Link>
            <button
              onClick={logout}
              className="text-red-600 hover:text-red-700 block w-full text-left px-3 py-2 rounded-md text-base font-medium"
            >
              Salir
            </button>
          </div>
        </div>
      )}
    </nav>
  )
}
