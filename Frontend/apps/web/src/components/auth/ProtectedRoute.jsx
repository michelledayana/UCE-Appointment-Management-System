'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';
import Loading from '@/components/common/Loading';

const ProtectedRoute = ({ children, requireRole = null }) => {
  const { user, isAuthenticated, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading) {
      if (!isAuthenticated) {
        router.push('/login');
        return;
      }

      if (requireRole && user?.role !== requireRole) {
        router.push('/services');
      }
    }
  }, [isAuthenticated, user, loading, requireRole, router]);

  if (loading) {
    return <Loading />;
  }

  if (!isAuthenticated) {
    return null;
  }

  if (requireRole && user?.role !== requireRole) {
    return null;
  }

  return <>{children}</>;
};

export default ProtectedRoute;