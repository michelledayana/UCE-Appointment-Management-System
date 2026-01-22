import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Rutas públicas que no requieren autenticación
  const publicRoutes = ['/login', '/register']
  const isPublicRoute = publicRoutes.some((route) =>
    request.nextUrl.pathname.startsWith(route)
  )

  // Rutas de administración
  const adminRoutes = ['/admin']
  const isAdminRoute = adminRoutes.some((route) =>
    request.nextUrl.pathname.startsWith(route)
  )

  // Obtener token de cookies
  const token = request.cookies.get('token')?.value

  // Si no hay token y no es ruta pública, redirigir a login
  if (!token && !isPublicRoute) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  // Si hay token y está en ruta pública, redirigir a home
  if (token && isPublicRoute) {
    return NextResponse.redirect(new URL('/', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
}
