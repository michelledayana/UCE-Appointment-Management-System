import { useState, useEffect } from 'react';
import appointmentService from '@/services/appointmentService';

export const useAppointments = () => {
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const loadAppointments = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await appointmentService.getMyAppointments();
      setAppointments(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const createAppointment = async (appointmentData) => {
    try {
      setLoading(true);
      setError(null);
      const newAppointment = await appointmentService.createAppointment(appointmentData);
      setAppointments([...appointments, newAppointment]);
      return { success: true, data: newAppointment };
    } catch (err) {
      setError(err.message);
      return { success: false, error: err.message };
    } finally {
      setLoading(false);
    }
  };

  const cancelAppointment = async (id) => {
    try {
      setLoading(true);
      setError(null);
      await appointmentService.cancelAppointment(id);
      setAppointments(appointments.filter(apt => apt.id !== id));
      return { success: true };
    } catch (err) {
      setError(err.message);
      return { success: false, error: err.message };
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAppointments();
  }, []);

  return {
    appointments,
    loading,
    error,
    loadAppointments,
    createAppointment,
    cancelAppointment,
  };
};