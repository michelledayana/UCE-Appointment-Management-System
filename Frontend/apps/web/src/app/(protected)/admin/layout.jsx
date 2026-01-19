'use client';

import ProtectedRoute from '@/components/auth/ProtectedRoute';
import AdminSidebar from '@/components/admin/Sidebar';

export default function AdminLayout({ children }) {
  return (
    <ProtectedRoute requireRole="ADMIN">
      <div className="flex min-h-screen bg-gray-100">
        <AdminSidebar />
        <main className="flex-1">
          {children}
        </main>
      </div>
    </ProtectedRoute>
  );
}