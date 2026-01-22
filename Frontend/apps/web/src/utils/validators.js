export const validateEmail = (email) => {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
};

export const validatePassword = (password) => {
  return password.length >= 8;
};

export const validatePhone = (phone) => {
  const regex = /^[0-9]{10}$/;
  return regex.test(phone.replace(/\D/g, ''));
};

export const validateRequired = (value) => {
  return value !== null && value !== undefined && value.trim() !== '';
};

export const validateForm = (formData, rules) => {
  const errors = {};
  
  Object.keys(rules).forEach((field) => {
    const rule = rules[field];
    const value = formData[field];
    
    if (rule.required && !validateRequired(value)) {
      errors[field] = `${field} es requerido`;
    }
    
    if (rule.email && !validateEmail(value)) {
      errors[field] = 'Email inválido';
    }
    
    if (rule.password && !validatePassword(value)) {
      errors[field] = 'La contraseña debe tener al menos 8 caracteres';
    }
    
    if (rule.phone && !validatePhone(value)) {
      errors[field] = 'Teléfono inválido';
    }
    
    if (rule.min && value.length < rule.min) {
      errors[field] = `Debe tener al menos ${rule.min} caracteres`;
    }
    
    if (rule.max && value.length > rule.max) {
      errors[field] = `No debe exceder ${rule.max} caracteres`;
    }
  });
  
  return {
    isValid: Object.keys(errors).length === 0,
    errors,
  };
};