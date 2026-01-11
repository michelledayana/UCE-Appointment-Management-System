'use client';

import { useState, useEffect } from 'react';
import adminService from '@/services/adminService';
import Loading from '@/components/common/Loading';
import ErrorMessage from '@/components/common/ErrorMessage';
import Card from '@/components/common/Card';
import Button from '@/components/common/Button';

export default function MonitoringPage() {
  const [systemHealth, setSystemHealth] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [autoRefresh, setAutoRefresh] = useState(false);

  useEffect(() => {
    loadMonitoringData();
  }, []);

  useEffect(() => {
    let interval;
    if (autoRefresh) {
      interval = setInterval(() => {
        loadMonitoringData();
      }, 30000); // Refresh cada 30 segundos
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [autoRefresh]);

  const loadMonitoringData = async () => {
    try {
      setLoading(true);
      const [healthData, metricsData] = await Promise.all([
        adminService.getSystemHealth(),
        adminService.getServiceMetrics(),
      ]);
      setSystemHealth(healthData);
      setMetrics(metricsData);
      setError('');
    } catch (err) {
      setError(err.message);
      // Datos de demostración
      setSystemHealth({
        status: 'healthy',
        services: [
          { name: 'API Gateway', status: 'healthy', uptime: '99.9%', responseTime: '45ms' },
          { name: 'Auth Service', status: 'healthy', uptime: '99.8%', responseTime: '32ms' },
          { name: 'Appointment Service', status: 'healthy', uptime: '99.7%', responseTime: '58ms' },
          { name: 'User Service', status: 'healthy', uptime: '99.9%', responseTime: '28ms' },
          { name: 'Database', status: 'healthy', uptime: '100%', responseTime: '15ms' },
        ],
      });
      setMetrics({
        requestsPerMinute: 142,
        activeUsers: 89,
        averageResponseTime: 43,
        errorRate: 0.2,
        cpuUsage: 45,
        memoryUsage: 62,
        diskUsage: 38,
      });
    } finally {
      setLoading(false);
    }
  };

  if (loading && !systemHealth) return <Loading text="Cargando monitoreo..." />;

  const getStatusColor = (status) => {
    switch (status) {
      case 'healthy':
        return 'text-green-600 bg-green-100';
      case 'warning':
        return 'text-yellow-600 bg-yellow-100';
      case 'error':
        return 'text-red-600 bg-red-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  const getStatusDot = (status) => {
    switch (status) {
      case 'healthy':
        return 'bg-green-500';
      case 'warning':
        return 'bg-yellow-500';
      case 'error':
        return 'bg-red-500';
      default:
        return 'bg-gray-500';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                Monitoreo del Sistema
              </h1>
              <p className="mt-2 text-gray-600">
                Estado y métricas en tiempo real
              </p>
            </div>
            <div className="flex gap-4 items-center">
              <label className="flex items-center gap-2 text-sm text-gray-600">
                <input
                  type="checkbox"
                  checked={autoRefresh}
                  onChange={(e) => setAutoRefresh(e.target.checked)}
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                Auto-actualizar (30s)
              </label>
              <Button variant="outline" onClick={loadMonitoringData}>
                Actualizar
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && <ErrorMessage message={error} onRetry={loadMonitoringData} />}

        {/* Overall Status */}
        <div className="mb-8">
          <Card>
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold text-gray-900">
                  Estado General del Sistema
                </h2>
                <p className="text-gray-600 mt-1">
                  Última actualización: {new Date().toLocaleTimeString('es-ES')}
                </p>
              </div>
              <div className={`px-6 py-3 rounded-full ${getStatusColor(systemHealth?.status)}`}>
                <span className="text-lg font-bold">
                  {systemHealth?.status === 'healthy' ? '✓ Operativo' : 
                   systemHealth?.status === 'warning' ? '⚠ Advertencia' : 
                   '✗ Error'}
                </span>
              </div>
            </div>
          </Card>
        </div>

        {/* Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <MetricCard
            title="Requests/Min"
            value={metrics?.requestsPerMinute || 0}
            icon="📊"
            color="blue"
          />
          <MetricCard
            title="Usuarios Activos"
            value={metrics?.activeUsers || 0}
            icon="👥"
            color="green"
          />
          <MetricCard
            title="Tiempo Respuesta"
            value={`${metrics?.averageResponseTime || 0}ms`}
            icon="⚡"
            color="yellow"
          />
          <MetricCard
            title="Tasa de Error"
            value={`${metrics?.errorRate || 0}%`}
            icon="⚠️"
            color="red"
          />
        </div>

        {/* Services Status */}
        <div className="mb-8">
          <Card title="Estado de Servicios">
            <div className="space-y-4">
              {systemHealth?.services?.map((service, index) => (
                <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                  <div className="flex items-center gap-4 flex-1">
                    <div className={`w-3 h-3 rounded-full ${getStatusDot(service.status)}`} />
                    <div className="flex-1">
                      <h3 className="font-semibold text-gray-900">{service.name}</h3>
                      <div className="flex gap-6 mt-1 text-sm text-gray-600">
                        <span>Uptime: {service.uptime}</span>
                        <span>Response: {service.responseTime}</span>
                      </div>
                    </div>
                  </div>
                  <span className={`px-3 py-1 text-xs font-medium rounded-full ${getStatusColor(service.status)}`}>
                    {service.status === 'healthy' ? 'Saludable' :
                     service.status === 'warning' ? 'Advertencia' : 'Error'}
                  </span>
                </div>
              ))}
            </div>
          </Card>
        </div>

        {/* Resource Usage */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <Card title="Uso de CPU">
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Uso actual</span>
                <span className="font-semibold text-gray-900">{metrics?.cpuUsage}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3">
                <div
                  className="bg-blue-600 h-3 rounded-full transition-all"
                  style={{ width: `${metrics?.cpuUsage}%` }}
                />
              </div>
              <p className="text-xs text-gray-500 mt-2">
                {metrics?.cpuUsage < 70 ? 'Normal' : 
                 metrics?.cpuUsage < 85 ? 'Moderado' : 'Alto'}
              </p>
            </div>
          </Card>

          <Card title="Uso de Memoria">
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Uso actual</span>
                <span className="font-semibold text-gray-900">{metrics?.memoryUsage}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3">
                <div
                  className="bg-green-600 h-3 rounded-full transition-all"
                  style={{ width: `${metrics?.memoryUsage}%` }}
                />
              </div>
              <p className="text-xs text-gray-500 mt-2">
                {metrics?.memoryUsage < 70 ? 'Normal' : 
                 metrics?.memoryUsage < 85 ? 'Moderado' : 'Alto'}
              </p>
            </div>
          </Card>

          <Card title="Uso de Disco">
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Uso actual</span>
                <span className="font-semibold text-gray-900">{metrics?.diskUsage}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3">
                <div
                  className="bg-purple-600 h-3 rounded-full transition-all"
                  style={{ width: `${metrics?.diskUsage}%` }}
                />
              </div>
              <p className="text-xs text-gray-500 mt-2">
                {metrics?.diskUsage < 70 ? 'Normal' : 
                 metrics?.diskUsage < 85 ? 'Moderado' : 'Alto'}
              </p>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}

function MetricCard({ title, value, icon, color }) {
  const colors = {
    blue: 'bg-blue-50 border-blue-200',
    green: 'bg-green-50 border-green-200',
    yellow: 'bg-yellow-50 border-yellow-200',
    red: 'bg-red-50 border-red-200',
  };

  return (
    <div className={`${colors[color]} border rounded-lg p-6`}>
      <div className="flex items-center justify-between mb-2">
        <span className="text-2xl">{icon}</span>
      </div>
      <h3 className="text-gray-600 text-sm font-medium">{title}</h3>
      <p className="text-3xl font-bold text-gray-900 mt-2">{value}</p>
    </div>
  );
}