'use client';

import { createContext, useContext, useState, useEffect } from 'react';
import authService from '@/services/authService';
import { useRouter } from 'next/navigation';

const AuthContext = createContext({});

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const currentUser = authService.getCurrentUser();
    if (currentUser) {
      setUser(currentUser);
    }
    setLoading(false);
  }, []);

  const login = async (credentials) => {
    try {
      const { user } = await authService.login(credentials);
      setUser(user);
      
      if (user.role === 'ADMIN') {
        router.push('/admin/dashboard');
      } else {
        router.push('/services');
      }
      
      return { success: true };
    } catch (error) {
      return { 
        success: false, 
        error: error.message || 'Error al iniciar sesión' 
      };
    }
  };

  const register = async (userData) => {
    try {
      await authService.register(userData);
      router.push('/login');
      return { success: true };
    } catch (error) {
      return { 
        success: false, 
        error: error.message || 'Error al registrar usuario' 
      };
    }
  };

  const logout = () => {
    authService.logout();
    setUser(null);
    router.push('/login');
  };

  const updateProfile = async (userData) => {
    try {
      const updatedUser = await authService.updateProfile(userData);
      setUser(updatedUser);
      return { success: true };
    } catch (error) {
      return { 
        success: false, 
        error: error.message || 'Error al actualizar perfil' 
      };
    }
  };

  const hasRole = (role) => {
    return user?.role === role;
  };

  const value = {
    user,
    login,
    register,
    logout,
    updateProfile,
    hasRole,
    isAuthenticated: !!user,
    loading,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth debe usarse dentro de AuthProvider');
  }
  return context;
};