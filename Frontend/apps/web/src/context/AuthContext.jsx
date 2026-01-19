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
      const response = await authService.login(credentials);
      
      // Manejar diferentes estructuras de respuesta
      const userData = response.user || response.data || response;
      
      setUser(userData);
      
      // Verificar el rol de manera segura
      const userRole = userData?.role || userData?.roles?.[0] || 'USUARIO';
      
      if (userRole === 'ADMIN') {
        router.push('/admin/dashboard');
      } else {
        router.push('/services');
      }
      
      return { success: true };
    } catch (error) {
      console.error('Login error:', error);
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
      console.error('Register error:', error);
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
      console.error('Update profile error:', error);
      return { 
        success: false, 
        error: error.message || 'Error al actualizar perfil' 
      };
    }
  };

  const hasRole = (role) => {
    if (!user) return false;
    
    // Verificar diferentes estructuras posibles
    const userRole = user.role || user.roles?.[0] || 'USUARIO';
    return userRole === role;
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