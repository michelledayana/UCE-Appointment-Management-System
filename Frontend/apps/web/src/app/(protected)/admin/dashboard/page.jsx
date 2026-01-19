'use client';

import { useState, useEffect } from 'react';
import adminService from '@/services/adminService';
import Loading from '@/components/common/Loading';
import ErrorMessage from '@/components/common/ErrorMessage';
import Card from '@/components/common/Card';

export default function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadDashboardStats();
  }, []);

  const loadDashboardStats = async () => {
    try {
      setLoading(true);
      const data = await adminService.getDashboardStats();
      setStats(data);
      setError('');
    } catch (err) {
      setError(err.message);
      // Datos de demostración si falla la API
      setStats({
        totalUsers: 150,
        appointmentsToday: 12,
        activeServices: 8,
        monthlyRevenue: 15000,
        recentAppointments: [
          { id: 1, serviceName: 'Consulta General', userName: 'Juan Pérez', status: 'confirmed' },
          { id: 2, serviceName: 'Terapia Física', userName: 'María García', status: 'pending' },
          { id: 3, serviceName: 'Diagnóstico', userName: 'Carlos López', status: 'confirmed' },
        ],
      });
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Loading text="Cargando dashboard..." />;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl font-bold text-gray-900">
            Panel de Administración
          </h1>
          <p className="mt-2 text-gray-600">
            Vista general del sistema
          </p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && <ErrorMessage message={error} onRetry={loadDashboardStats} />}

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatsCard
            title="Total Usuarios"
            value={stats?.totalUsers || 0}
            icon="👥"
            trend="+12%"
            trendUp={true}
            color="blue"
          />
          <StatsCard
            title="Citas Hoy"
            value={stats?.appointmentsToday || 0}
            icon="📅"
            trend="+5%"
            trendUp={true}
            color="green"
          />
          <StatsCard
            title="Servicios Activos"
            value={stats?.activeServices || 0}
            icon="🛠️"
            trend="0%"
            trendUp={null}
            color="purple"
          />
          <StatsCard
            title="Ingresos del Mes"
            value={`$${stats?.monthlyRevenue || 0}`}
            icon="💰"
            trend="+18%"
            trendUp={true}
            color="yellow"
          />
        </div>

        {/* Recent Activity and System Health */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Recent Appointments */}
          <Card title="Citas Recientes">
            <div className="space-y-3">
              {stats?.recentAppointments?.map((apt) => (
                <div key={apt.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div>
                    <p className="font-medium text-gray-900">{apt.serviceName}</p>
                    <p className="text-sm text-gray-600">{apt.userName}</p>
                  </div>
                  <span className={`px-2 py-1 text-xs rounded ${
                    apt.status === 'confirmed' ? 'bg-green-100 text-green-800' :
                    apt.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {apt.status === 'confirmed' ? 'Confirmada' :
                     apt.status === 'pending' ? 'Pendiente' : apt.status}
                  </span>
                </div>
              ))}
            </div>
          </Card>

          {/* System Health */}
          <Card title="Estado del Sistema">
            <div className="space-y-4">
              <HealthIndicator service="API Gateway" status="healthy" />
              <HealthIndicator service="Base de Datos" status="healthy" />
              <HealthIndicator service="Servicio de Citas" status="healthy" />
              <HealthIndicator service="Servicio de Usuarios" status="healthy" />
            </div>
          </Card>
        </div>

        {/* Quick Actions */}
        <div className="mt-8">
          <Card title="Acciones Rápidas">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <button className="p-4 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors text-left">
                <div className="text-2xl mb-2">➕</div>
                <h3 className="font-semibold text-gray-900">Nuevo Servicio</h3>
                <p className="text-sm text-gray-600">Agregar servicio al catálogo</p>
              </button>
              <button className="p-4 bg-green-50 rounded-lg hover:bg-green-100 transition-colors text-left">
                <div className="text-2xl mb-2">📊</div>
                <h3 className="font-semibold text-gray-900">Ver Reportes</h3>
                <p className="text-sm text-gray-600">Generar reportes del sistema</p>
              </button>
              <button className="p-4 bg-purple-50 rounded-lg hover:bg-purple-100 transition-colors text-left">
                <div className="text-2xl mb-2">👥</div>
                <h3 className="font-semibold text-gray-900">Gestionar Usuarios</h3>
                <p className="text-sm text-gray-600">Administrar usuarios del sistema</p>
              </button>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}

function StatsCard({ title, value, icon, trend, trendUp, color }) {
  const colors = {
    blue: 'bg-blue-50',
    green: 'bg-green-50',
    purple: 'bg-purple-50',
    yellow: 'bg-yellow-50',
  };

  return (
    <div className={`${colors[color]} rounded-lg shadow p-6`}>
      <div className="flex items-center justify-between mb-2">
        <span className="text-2xl">{icon}</span>
        {trend && (
          <span className={`text-sm font-medium ${
            trendUp ? 'text-green-600' : trendUp === false ? 'text-red-600' : 'text-gray-600'
          }`}>
            {trend}
          </span>
        )}
      </div>
      <h3 className="text-gray-600 text-sm font-medium">{title}</h3>
      <p className="text-3xl font-bold text-gray-900 mt-2">{value}</p>
    </div>
  );
}

function HealthIndicator({ service, status }) {
  const statusColors = {
    healthy: 'bg-green-500',
    warning: 'bg-yellow-500',
    error: 'bg-red-500',
  };

  const statusText = {
    healthy: 'Saludable',
    warning: 'Advertencia',
    error: 'Error',
  };

  return (
    <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
      <span className="text-gray-700 font-medium">{service}</span>
      <div className="flex items-center gap-2">
        <div className={`w-3 h-3 rounded-full ${statusColors[status]}`} />
        <span className="text-sm text-gray-600">{statusText[status]}</span>
      </div>
    </div>
  );
}