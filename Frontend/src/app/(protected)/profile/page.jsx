'use client';

import { useState } from 'react';
import { useAuth } from '@/context/AuthContext';
import Input from '@/components/common/Input';
import Button from '@/components/common/Button';
import ErrorMessage from '@/components/common/ErrorMessage';
import Card from '@/components/common/Card';

export default function ProfilePage() {
  const { user, updateProfile } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [isChangingPassword, setIsChangingPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const [profileData, setProfileData] = useState({
    name: user?.name || '',
    email: user?.email || '',
    phone: user?.phone || '',
  });

  const [passwordData, setPasswordData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
  });

  const handleProfileChange = (e) => {
    setProfileData({
      ...profileData,
      [e.target.name]: e.target.value,
    });
  };

  const handlePasswordChange = (e) => {
    setPasswordData({
      ...passwordData,
      [e.target.name]: e.target.value,
    });
  };

  const handleProfileSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    const result = await updateProfile(profileData);

    if (result.success) {
      setSuccess('Perfil actualizado exitosamente');
      setIsEditing(false);
    } else {
      setError(result.error);
    }

    setLoading(false);
  };

  const handlePasswordSubmit = async (e) => {
    e.preventDefault();

    if (passwordData.newPassword !== passwordData.confirmPassword) {
      setError('Las contraseñas no coinciden');
      return;
    }

    if (passwordData.newPassword.length < 8) {
      setError('La contraseña debe tener al menos 8 caracteres');
      return;
    }

    setLoading(true);
    setError('');
    setSuccess('');

    try {
      // Aquí llamarías al servicio de cambio de contraseña
      // await authService.changePassword(passwordData);
      setSuccess('Contraseña actualizada exitosamente');
      setIsChangingPassword(false);
      setPasswordData({
        currentPassword: '',
        newPassword: '',
        confirmPassword: '',
      });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Mi Perfil</h1>
          <p className="mt-2 text-gray-600">
            Gestiona tu información personal y configuración
          </p>
        </div>

        {success && (
          <div className="mb-6 bg-green-50 border border-green-200 rounded-lg p-4">
            <p className="text-green-800">{success}</p>
          </div>
        )}

        {error && <ErrorMessage message={error} />}

        <div className="space-y-6">
          {/* Información del Perfil */}
          <Card title="Información Personal">
            {!isEditing ? (
              <div className="space-y-4">
                <div>
                  <label className="text-sm font-medium text-gray-500">Nombre</label>
                  <p className="text-gray-900">{user?.name}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Email</label>
                  <p className="text-gray-900">{user?.email}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Teléfono</label>
                  <p className="text-gray-900">{user?.phone}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Rol</label>
                  <p className="text-gray-900">
                    <span className={`px-3 py-1 text-xs font-medium rounded-full ${
                      user?.role === 'ADMIN' 
                        ? 'bg-purple-100 text-purple-800' 
                        : 'bg-blue-100 text-blue-800'
                    }`}>
                      {user?.role}
                    </span>
                  </p>
                </div>
                <Button
                  variant="primary"
                  onClick={() => setIsEditing(true)}
                >
                  Editar Perfil
                </Button>
              </div>
            ) : (
              <form onSubmit={handleProfileSubmit} className="space-y-4">
                <Input
                  label="Nombre"
                  name="name"
                  value={profileData.name}
                  onChange={handleProfileChange}
                  required
                />
                <Input
                  label="Email"
                  type="email"
                  name="email"
                  value={profileData.email}
                  onChange={handleProfileChange}
                  required
                />
                <Input
                  label="Teléfono"
                  name="phone"
                  value={profileData.phone}
                  onChange={handleProfileChange}
                  required
                />
                <div className="flex gap-4">
                  <Button
                    type="button"
                    variant="secondary"
                    onClick={() => {
                      setIsEditing(false);
                      setProfileData({
                        name: user?.name || '',
                        email: user?.email || '',
                        phone: user?.phone || '',
                      });
                    }}
                  >
                    Cancelar
                  </Button>
                  <Button
                    type="submit"
                    variant="primary"
                    loading={loading}
                  >
                    Guardar Cambios
                  </Button>
                </div>
              </form>
            )}
          </Card>

          {/* Cambiar Contraseña */}
          <Card title="Seguridad">
            {!isChangingPassword ? (
              <div>
                <p className="text-gray-600 mb-4">
                  Actualiza tu contraseña regularmente para mantener tu cuenta segura
                </p>
                <Button
                  variant="outline"
                  onClick={() => setIsChangingPassword(true)}
                >
                  Cambiar Contraseña
                </Button>
              </div>
            ) : (
              <form onSubmit={handlePasswordSubmit} className="space-y-4">
                <Input
                  label="Contraseña Actual"
                  type="password"
                  name="currentPassword"
                  value={passwordData.currentPassword}
                  onChange={handlePasswordChange}
                  required
                />
                <Input
                  label="Nueva Contraseña"
                  type="password"
                  name="newPassword"
                  value={passwordData.newPassword}
                  onChange={handlePasswordChange}
                  required
                />
                <Input
                  label="Confirmar Nueva Contraseña"
                  type="password"
                  name="confirmPassword"
                  value={passwordData.confirmPassword}
                  onChange={handlePasswordChange}
                  required
                />
                <div className="flex gap-4">
                  <Button
                    type="button"
                    variant="secondary"
                    onClick={() => {
                      setIsChangingPassword(false);
                      setPasswordData({
                        currentPassword: '',
                        newPassword: '',
                        confirmPassword: '',
                      });
                    }}
                  >
                    Cancelar
                  </Button>
                  <Button
                    type="submit"
                    variant="primary"
                    loading={loading}
                  >
                    Actualizar Contraseña
                  </Button>
                </div>
              </form>
            )}
          </Card>

          {/* Estadísticas del Usuario */}
          <Card title="Estadísticas">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-blue-50 rounded-lg p-4">
                <p className="text-sm text-gray-600">Citas Totales</p>
                <p className="text-2xl font-bold text-blue-600">12</p>
              </div>
              <div className="bg-green-50 rounded-lg p-4">
                <p className="text-sm text-gray-600">Citas Completadas</p>
                <p className="text-2xl font-bold text-green-600">8</p>
              </div>
              <div className="bg-yellow-50 rounded-lg p-4">
                <p className="text-sm text-gray-600">Citas Pendientes</p>
                <p className="text-2xl font-bold text-yellow-600">4</p>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}