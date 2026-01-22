'use client';

import { useState } from 'react';
import Input from '@/components/common/Input';
import Button from '@/components/common/Button';
import ErrorMessage from '@/components/common/ErrorMessage';

export default function ServiceForm({ service, onSubmit, onCancel }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    name: service?.name || '',
    description: service?.description || '',
    category: service?.category || 'consulta',
    duration: service?.duration || 30,
    price: service?.price || 0,
    active: service?.active !== undefined ? service.active : true,
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await onSubmit(formData);
    } catch (err) {
      setError(err.message || 'Error al guardar el servicio');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && <ErrorMessage message={error} />}

      <Input
        label="Nombre del Servicio"
        name="name"
        value={formData.name}
        onChange={handleChange}
        required
        placeholder="Ej: Consulta General"
      />

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Descripción
        </label>
        <textarea
          name="description"
          value={formData.description}
          onChange={handleChange}
          rows={3}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Describe el servicio..."
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Categoría
        </label>
        <select
          name="category"
          value={formData.category}
          onChange={handleChange}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        >
          <option value="consulta">Consulta</option>
          <option value="terapia">Terapia</option>
          <option value="diagnostico">Diagnóstico</option>
        </select>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <Input
          label="Duración (minutos)"
          type="number"
          name="duration"
          value={formData.duration}
          onChange={handleChange}
          min="15"
          step="15"
          required
        />

        <Input
          label="Precio ($)"
          type="number"
          name="price"
          value={formData.price}
          onChange={handleChange}
          min="0"
          step="0.01"
          required
        />
      </div>

      <div className="flex items-center">
        <input
          type="checkbox"
          name="active"
          checked={formData.active}
          onChange={handleChange}
          className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
        />
        <label className="ml-2 text-sm text-gray-700">
          Servicio activo
        </label>
      </div>

      <div className="flex gap-4 pt-4">
        <Button
          type="button"
          variant="secondary"
          onClick={onCancel}
          className="flex-1"
        >
          Cancelar
        </Button>
        <Button
          type="submit"
          variant="primary"
          loading={loading}
          className="flex-1"
        >
          {service ? 'Actualizar' : 'Crear'} Servicio
        </Button>
      </div>
    </form>
  );
}