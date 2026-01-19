'use client';

import ProtectedRoute from '@/components/auth/ProtectedRoute';
import Navbar from '@/components/common/Navbar';

export default function ProtectedLayout({ children }) {
  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <main>{children}</main>
      </div>
    </ProtectedRoute>
  );
}