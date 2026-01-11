'use client';

import { useAuth } from '@/context/AuthContext';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Navbar() {
  const { user, logout } = useAuth();
  const pathname = usePathname();

  const isActive = (path) => pathname === path;

  return (
    <nav className="bg-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <Link href="/" className="flex items-center">
              <span className="text-2xl font-bold text-blue-600">
                MediCitas
              </span>
            </Link>
            
            <div className="hidden sm:ml-8 sm:flex sm:space-x-4">
              <NavLink href="/services" active={isActive('/services')}>
                Servicios
              </NavLink>
              <NavLink href="/appointments" active={isActive('/appointments')}>
                Mis Citas
              </NavLink>
              {user?.role === 'ADMIN' && (
                <NavLink href="/admin/dashboard" active={isActive('/admin/dashboard')}>
                  Administración
                </NavLink>
              )}
            </div>
          </div>

          <div className="flex items-center space-x-4">
            <Link
              href="/profile"
              className="text-gray-700 hover:text-blue-600"
            >
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white">
                  {user?.name?.charAt(0)?.toUpperCase() || 'U'}
                </div>
                <span className="hidden md:block">{user?.name}</span>
              </div>
            </Link>
            
            <button
              onClick={logout}
              className="text-gray-700 hover:text-red-600 font-medium"
            >
              Salir
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}

function NavLink({ href, active, children }) {
  return (
    <Link
      href={href}
      className={`inline-flex items-center px-3 py-2 text-sm font-medium ${
        active
          ? 'text-blue-600 border-b-2 border-blue-600'
          : 'text-gray-700 hover:text-blue-600'
      }`}
    >
      {children}
    </Link>
  );
}