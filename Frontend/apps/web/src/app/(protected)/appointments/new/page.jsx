'use client';

import { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import appointmentService from '@/services/appointmentService';
import serviceService from '@/services/serviceService';
import Input from '@/components/common/Input';
import Button from '@/components/common/Button';
import ErrorMessage from '@/components/common/ErrorMessage';
import Loading from '@/components/common/Loading';

export default function NewAppointmentPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const serviceId = searchParams.get('serviceId');
  
  const [services, setServices] = useState([]);
  const [selectedService, setSelectedService] = useState(null);
  const [availableSlots, setAvailableSlots] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  
  const [formData, setFormData] = useState({
    serviceId: serviceId || '',
    date: '',
    time: '',
    notes: '',
  });

  useEffect(() => {
    loadServices();
  }, []);

  useEffect(() => {
    if (formData.serviceId && formData.date) {
      checkAvailability();
    }
  }, [formData.serviceId, formData.date]);

  const loadServices = async () => {
    try {
      const data = await serviceService.getAllServices();
      setServices(data);
      
      if (serviceId) {
        const service = data.find(s => s.id === serviceId);
        setSelectedService(service);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const checkAvailability = async () => {
    try {
      const data = await appointmentService.checkAvailability(
        formData.serviceId,
        formData.date
      );
      setAvailableSlots(data.availableSlots || []);
    } catch (err) {
      console.error('Error al verificar disponibilidad:', err);
      // Mostrar slots por defecto si hay error
      setAvailableSlots(['09:00', '10:00', '11:00', '14:00', '15:00', '16:00']);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
    
    if (name === 'serviceId') {
      const service = services.find(s => s.id === value);
      setSelectedService(service);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.serviceId || !formData.date || !formData.time) {
      setError('Por favor complete todos los campos requeridos');
      return;
    }
    
    setSubmitting(true);
    setError('');
    
    try {
      await appointmentService.createAppointment({
        serviceId: formData.serviceId,
        dateTime: `${formData.date}T${formData.time}`,
        notes: formData.notes,
      });
      
      router.push('/appointments?success=true');
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <Loading text="Cargando formulario..." />;

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white rounded-lg shadow-md p-8">
          <h1 className="text-2xl font-bold text-gray-900 mb-6">
            Nueva Cita
          </h1>

          {error && <ErrorMessage message={error} />}

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Servicio */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Servicio *
              </label>
              <select
                name="serviceId"
                value={formData.serviceId}
                onChange={handleChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Seleccione un servicio</option>
                {services.map((service) => (
                  <option key={service.id} value={service.id}>
                    {service.name} - ${service.price}
                  </option>
                ))}
              </select>
            </div>

            {/* Detalles del servicio seleccionado */}
            {selectedService && (
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <h3 className="font-semibold text-gray-900 mb-2">
                  {selectedService.name}
                </h3>
                <p className="text-sm text-gray-600 mb-2">
                  {selectedService.description}
                </p>
                <div className="flex gap-4 text-sm">
                  <span className="text-gray-700">
                    <strong>Duración:</strong> {selectedService.duration} min
                  </span>
                  <span className="text-gray-700">
                    <strong>Precio:</strong> ${selectedService.price}
                  </span>
                </div>
              </div>
            )}

            {/* Fecha */}
            <Input
              label="Fecha *"
              type="date"
              name="date"
              value={formData.date}
              onChange={handleChange}
              min={new Date().toISOString().split('T')[0]}
              required
            />

            {/* Horarios disponibles */}
            {availableSlots.length > 0 && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Horario disponible *
                </label>
                <div className="grid grid-cols-4 gap-2">
                  {availableSlots.map((slot) => (
                    <button
                      key={slot}
                      type="button"
                      onClick={() => setFormData({ ...formData, time: slot })}
                      className={`px-3 py-2 text-sm rounded-lg border ${
                        formData.time === slot
                          ? 'bg-blue-600 text-white border-blue-600'
                          : 'bg-white text-gray-700 border-gray-300 hover:border-blue-600'
                      }`}
                    >
                      {slot}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Notas */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Notas (opcional)
              </label>
              <textarea
                name="notes"
                value={formData.notes}
                onChange={handleChange}
                rows={4}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Información adicional sobre la cita..."
              />
            </div>

            {/* Botones */}
            <div className="flex gap-4">
              <Button
                type="button"
                variant="secondary"
                onClick={() => router.back()}
                className="flex-1"
              >
                Cancelar
              </Button>
              <Button
                type="submit"
                variant="primary"
                loading={submitting}
                className="flex-1"
              >
                Confirmar Cita
              </Button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}