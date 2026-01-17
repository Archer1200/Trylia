/**
 * Frontend validation utilities for Trylia Contact Us form
 */

export const validateEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

export const validateURL = (url) => {
  try {
    // Add protocol if missing
    const urlToTest = url.startsWith('http') ? url : `https://${url}`;
    new URL(urlToTest);
    return true;
  } catch {
    return false;
  }
};

export const validatePhone = (phone) => {
  // Remove all non-digit characters
  const cleaned = phone.replace(/\D/g, '');
  // Check if it's between 7 and 15 digits
  return cleaned.length >= 7 && cleaned.length <= 15;
};

export const validateRequired = (value, minLength = 1) => {
  return value && value.trim().length >= minLength;
};

export const validateLength = (value, minLength, maxLength) => {
  if (!value) return false;
  const length = value.trim().length;
  return length >= minLength && length <= maxLength;
};

export const validateContactForm = (formData) => {
  const errors = {};

  // Company Name
  if (!validateRequired(formData.companyName, 2)) {
    errors.companyName = 'Company name is required (minimum 2 characters)';
  } else if (!validateLength(formData.companyName, 2, 100)) {
    errors.companyName = 'Company name must be between 2 and 100 characters';
  }

  // Website URL
  if (!validateRequired(formData.websiteUrl)) {
    errors.websiteUrl = 'Website URL is required';
  } else if (!validateURL(formData.websiteUrl)) {
    errors.websiteUrl = 'Please enter a valid website URL';
  }

  // Contact Person
  if (!validateRequired(formData.contactPerson, 2)) {
    errors.contactPerson = 'Contact person name is required (minimum 2 characters)';
  } else if (!validateLength(formData.contactPerson, 2, 50)) {
    errors.contactPerson = 'Contact person name must be between 2 and 50 characters';
  }

  // Business Email
  if (!validateRequired(formData.businessEmail)) {
    errors.businessEmail = 'Business email is required';
  } else if (!validateEmail(formData.businessEmail)) {
    errors.businessEmail = 'Please enter a valid email address';
  }

  // Phone Number
  if (!validateRequired(formData.phoneNumber)) {
    errors.phoneNumber = 'Phone number is required';
  } else if (!validatePhone(formData.phoneNumber)) {
    errors.phoneNumber = 'Please enter a valid phone number (7-15 digits)';
  }

  // Company Size
  if (!validateRequired(formData.companySize)) {
    errors.companySize = 'Please select your company size';
  }

  // Inquiry Type
  if (!validateRequired(formData.inquiryType)) {
    errors.inquiryType = 'Please select an inquiry type';
  }

  // Message
  if (!validateRequired(formData.message, 10)) {
    errors.message = 'Message is required (minimum 10 characters)';
  } else if (!validateLength(formData.message, 10, 1000)) {
    errors.message = 'Message must be between 10 and 1000 characters';
  }

  // Meeting Mode
  if (!validateRequired(formData.meetingMode)) {
    errors.meetingMode = 'Please select a preferred meeting mode';
  }

  // Country
  if (!validateRequired(formData.country)) {
    errors.country = 'Please select your country';
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors
  };
};

export const formatPhoneNumber = (phone) => {
  // Remove all non-digit characters
  const cleaned = phone.replace(/\D/g, '');
  
  // Format US phone numbers
  if (cleaned.length === 10) {
    return `(${cleaned.slice(0, 3)}) ${cleaned.slice(3, 6)}-${cleaned.slice(6)}`;
  }
  
  // For international numbers, just return with spaces
  if (cleaned.length > 10) {
    return cleaned.replace(/(\d{3})/g, '$1 ').trim();
  }
  
  return phone;
};

export const normalizeURL = (url) => {
  if (!url) return '';
  return url.startsWith('http') ? url : `https://${url}`;
};