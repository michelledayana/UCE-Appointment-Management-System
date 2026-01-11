'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';
import Loading from '@/components/common/Loading';

export default function HomePage() {
  const { isAuthenticated, user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading) {
      if (isAuthenticated) {
        if (user?.role === 'ADMIN') {
          router.push('/admin/dashboard');
        } else {
          router.push('/services');
        }
      } else {
        router.push('/login');
      }
    }
  }, [isAuthenticated, user, loading, router]);

  return <Loading text="Redirigiendo..." />;
}