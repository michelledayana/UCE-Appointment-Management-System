'use client';

import { useState, useEffect } from 'react';
import serviceService from '@/services/serviceService';
import Loading from '@/components/common/Loading';
import ErrorMessage from '@/components/common/ErrorMessage';
import Button from '@/components/common/Button';
import Modal from '@/components/common/Modal';
import ServiceForm from '@/components/admin/ServiceForm';

export default function AdminServicesPage() {
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingService, setEditingService] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    loadServices();
  }, []);

  const loadServices = async () => {
    try {
      setLoading(true);
      const data = await serviceService.getAllServices();
      setServices(data);
      setError('');
    } catch (err) {
      setError(err.message);
      // Datos de demostración
      setServices([
        {
          id: '1',
          name: 'Consulta General',
          description: 'Consulta médica general',
          category: 'consulta',
          duration: 30,
          price: 50,
          active: true,
        },
        {
          id: '2',
          name: 'Terapia Física',
          description: 'Sesión de terapia física',
          category: 'terapia',
          duration: 60,
          price: 75,
          active: true,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateService = () => {
    setEditingService(null);
    setIsModalOpen(true);
  };

  const handleEditService = (service) => {
    setEditingService(service);
    setIsModalOpen(true);
  };

  const handleDeleteService = async (id) => {
    if (!confirm('¿Estás seguro de que deseas eliminar este servicio?')) {
      return;
    }

    try {
      await serviceService.deleteService(id);
      setServices(services.filter(s => s.id !== id));
    } catch (err) {
      setError(err.message);
    }
  };

  const handleFormSubmit = async (formData) => {
    try {
      if (editingService) {
        const updated = await serviceService.updateService(editingService.id, formData);
        setServices(services.map(s => s.id === editingService.id ? updated : s));
      } else {
        const newService = await serviceService.createService(formData);
        setServices([...services, newService]);
      }
      setIsModalOpen(false);
      setEditingService(null);
    } catch (err) {
      throw err;
    }
  };

  const filteredServices = services.filter(service =>
    service.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    service.description?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) return <Loading text="Cargando servicios..." />;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                Gestión de Servicios
              </h1>
              <p className="mt-2 text-gray-600">
                Administra el catálogo de servicios
              </p>
            </div>
            <Button variant="primary" onClick={handleCreateService}>
              + Nuevo Servicio
            </Button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Search */}
        <div className="mb-6">
          <input
            type="text"
            placeholder="Buscar servicios..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full max-w-md px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {error && <ErrorMessage message={error} onRetry={loadServices} />}

        {/* Services Table */}
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Servicio
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Categoría
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Duración
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Precio
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Estado
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Acciones
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredServices.map((service) => (
                <tr key={service.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900">
                      {service.name}
                    </div>
                    <div className="text-sm text-gray-500">
                      {service.description}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded">
                      {service.category}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {service.duration} min
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    ${service.price}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 py-1 text-xs font-medium rounded ${
                      service.active
                        ? 'bg-green-100 text-green-800'
                        : 'bg-red-100 text-red-800'
                    }`}>
                      {service.active ? 'Activo' : 'Inactivo'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button
                      onClick={() => handleEditService(service)}
                      className="text-blue-600 hover:text-blue-900 mr-4"
                    >
                      Editar
                    </button>
                    <button
                      onClick={() => handleDeleteService(service.id)}
                      className="text-red-600 hover:text-red-900"
                    >
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {filteredServices.length === 0 && (
            <div className="text-center py-12">
              <p className="text-gray-500">No se encontraron servicios</p>
            </div>
          )}
        </div>
      </div>

      {/* Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          setEditingService(null);
        }}
        title={editingService ? 'Editar Servicio' : 'Nuevo Servicio'}
        size="lg"
      >
        <ServiceForm
          service={editingService}
          onSubmit={handleFormSubmit}
          onCancel={() => {
            setIsModalOpen(false);
            setEditingService(null);
          }}
        />
      </Modal>
    </div>
  );
}