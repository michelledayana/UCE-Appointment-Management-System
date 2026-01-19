import { useState, useEffect } from 'react';
import serviceService from '@/services/serviceService';

export const useServices = () => {
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const loadServices = async (params = {}) => {
    try {
      setLoading(true);
      setError(null);
      const data = await serviceService.getAllServices(params);
      setServices(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const createService = async (serviceData) => {
    try {
      setLoading(true);
      setError(null);
      const newService = await serviceService.createService(serviceData);
      setServices([...services, newService]);
      return { success: true, data: newService };
    } catch (err) {
      setError(err.message);
      return { success: false, error: err.message };
    } finally {
      setLoading(false);
    }
  };

  const updateService = async (id, serviceData) => {
    try {
      setLoading(true);
      setError(null);
      const updatedService = await serviceService.updateService(id, serviceData);
      setServices(services.map(s => s.id === id ? updatedService : s));
      return { success: true, data: updatedService };
    } catch (err) {
      setError(err.message);
      return { success: false, error: err.message };
    } finally {
      setLoading(false);
    }
  };

  const deleteService = async (id) => {
    try {
      setLoading(true);
      setError(null);
      await serviceService.deleteService(id);
      setServices(services.filter(s => s.id !== id));
      return { success: true };
    } catch (err) {
      setError(err.message);
      return { success: false, error: err.message };
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadServices();
  }, []);

  return {
    services,
    loading,
    error,
    loadServices,
    createService,
    updateService,
    deleteService,
  };
};