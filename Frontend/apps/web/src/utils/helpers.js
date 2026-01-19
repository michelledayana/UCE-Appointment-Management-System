export const formatDate = (date) => {
  const options = { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  };
  return new Date(date).toLocaleDateString('es-ES', options);
};

export const formatTime = (time) => {
  return new Date(time).toLocaleTimeString('es-ES', {
    hour: '2-digit',
    minute: '2-digit',
  });
};

export const formatCurrency = (amount) => {
  return new Intl.NumberFormat('es-EC', {
    style: 'currency',
    currency: 'USD',
  }).format(amount);
};

export const debounce = (func, delay) => {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func(...args), delay);
  };
};

export const truncateText = (text, maxLength) => {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
};

export const getInitials = (name) => {
  return name
    .split(' ')
    .map(word => word[0])
    .join('')
    .toUpperCase()
    .substring(0, 2);
};

export const classNames = (...classes) => {
  return classes.filter(Boolean).join(' ');
};

export const handleApiError = (error) => {
  if (error.response) {
    return error.response.data.message || 'Error en la petición';
  } else if (error.request) {
    return 'Sin respuesta del servidor';
  } else {
    return error.message || 'Error desconocido';
  }
};