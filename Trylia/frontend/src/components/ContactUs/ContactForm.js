import React, { useState, useEffect } from 'react';
import { validateContactForm, normalizeURL } from '../../utils/validation';
import contactApi from '../../services/contactApi';
import './ContactForm.css';

const ContactForm = () => {
  const [formData, setFormData] = useState({
    companyName: '',
    websiteUrl: '',
    contactPerson: '',
    businessEmail: '',
    phoneNumber: '',
    companySize: '',
    inquiryType: '',
    message: '',
    meetingMode: '',
    meetingTime: '',
    country: ''
  });

  const [formOptions, setFormOptions] = useState({
    companySizes: [],
    inquiryTypes: [],
    meetingModes: [],
    countries: []
  });

  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // Load form options on component mount
  useEffect(() => {
    const loadFormOptions = async () => {
      setIsLoading(true);
      const result = await contactApi.getFormOptions();
      
      if (result.success) {
        setFormOptions(result.options);
      } else {
        console.error('Failed to load form options:', result.error);
        // Use fallback options from the API service
        setFormOptions(result.options);
      }
      setIsLoading(false);
    };

    loadFormOptions();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));

    // Clear error for this field when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }

    // Clear submit status when user makes changes
    if (submitStatus) {
      setSubmitStatus(null);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate form
    const validation = validateContactForm(formData);
    
    if (!validation.isValid) {
      setErrors(validation.errors);
      setSubmitStatus({
        type: 'error',
        message: 'Please fix the errors below and try again.'
      });
      return;
    }

    setIsSubmitting(true);
    setErrors({});

    try {
      // Normalize URL before submission
      const submissionData = {
        ...formData,
        websiteUrl: normalizeURL(formData.websiteUrl)
      };

      const result = await contactApi.submitContactForm(submissionData);

      if (result.success) {
        setSubmitStatus({
          type: 'success',
          message: result.data.message || 'Thank you for your inquiry! We will get back to you within 24 hours.'
        });
        
        // Reset form
        setFormData({
          companyName: '',
          websiteUrl: '',
          contactPerson: '',
          businessEmail: '',
          phoneNumber: '',
          companySize: '',
          inquiryType: '',
          message: '',
          meetingMode: '',
          meetingTime: '',
          country: ''
        });
      } else {
        setSubmitStatus({
          type: 'error',
          message: result.error || 'Failed to submit form. Please try again.'
        });
        
        // If there are field-specific errors from the server
        if (result.errors) {
          setErrors(result.errors);
        }
      }
    } catch (error) {
      setSubmitStatus({
        type: 'error',
        message: 'An unexpected error occurred. Please try again later.'
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const getMinDateTime = () => {
    const now = new Date();
    now.setMinutes(now.getMinutes() + 60); // At least 1 hour from now
    return now.toISOString().slice(0, 16);
  };

  if (isLoading) {
    return (
      <div className="contact-form-container">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Loading contact form...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="contact-form-container">
      <div className="contact-form-header">
        <h1>Contact Trylia</h1>
        <p className="subtitle">
          Ready to revolutionize your e-commerce with AI-powered virtual try-on technology? 
          Let's discuss how Trylia can transform your customer experience.
        </p>
      </div>

      {submitStatus && (
        <div className={`status-message ${submitStatus.type}`}>
          <div className="status-icon">
            {submitStatus.type === 'success' ? '✅' : '❌'}
          </div>
          <p>{submitStatus.message}</p>
        </div>
      )}

      <form onSubmit={handleSubmit} className="contact-form">
        {/* Company Information Section */}
        <div className="form-section">
          <h2>Company Information</h2>
          
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="companyName">
                Company Name <span className="required">*</span>
              </label>
              <input
                type="text"
                id="companyName"
                name="companyName"
                value={formData.companyName}
                onChange={handleInputChange}
                className={errors.companyName ? 'error' : ''}
                placeholder="Enter your company name"
                maxLength="100"
              />
              {errors.companyName && <span className="error-message">{errors.companyName}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="websiteUrl">
                Company Website <span className="required">*</span>
              </label>
              <input
                type="url"
                id="websiteUrl"
                name="websiteUrl"
                value={formData.websiteUrl}
                onChange={handleInputChange}
                className={errors.websiteUrl ? 'error' : ''}
                placeholder="https://www.yourcompany.com"
              />
              {errors.websiteUrl && <span className="error-message">{errors.websiteUrl}</span>}
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="companySize">
                Company Size <span className="required">*</span>
              </label>
              <select
                id="companySize"
                name="companySize"
                value={formData.companySize}
                onChange={handleInputChange}
                className={errors.companySize ? 'error' : ''}
              >
                <option value="">Select company size</option>
                {formOptions.companySizes.map((size) => (
                  <option key={size} value={size}>{size}</option>
                ))}
              </select>
              {errors.companySize && <span className="error-message">{errors.companySize}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="country">
                Country/Region <span className="required">*</span>
              </label>
              <select
                id="country"
                name="country"
                value={formData.country}
                onChange={handleInputChange}
                className={errors.country ? 'error' : ''}
              >
                <option value="">Select your country</option>
                {formOptions.countries.map((country) => (
                  <option key={country} value={country}>{country}</option>
                ))}
              </select>
              {errors.country && <span className="error-message">{errors.country}</span>}
            </div>
          </div>
        </div>

        {/* Contact Information Section */}
        <div className="form-section">
          <h2>Contact Information</h2>
          
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="contactPerson">
                Contact Person Name <span className="required">*</span>
              </label>
              <input
                type="text"
                id="contactPerson"
                name="contactPerson"
                value={formData.contactPerson}
                onChange={handleInputChange}
                className={errors.contactPerson ? 'error' : ''}
                placeholder="Enter contact person's name"
                maxLength="50"
              />
              {errors.contactPerson && <span className="error-message">{errors.contactPerson}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="businessEmail">
                Business Email <span className="required">*</span>
              </label>
              <input
                type="email"
                id="businessEmail"
                name="businessEmail"
                value={formData.businessEmail}
                onChange={handleInputChange}
                className={errors.businessEmail ? 'error' : ''}
                placeholder="contact@yourcompany.com"
              />
              {errors.businessEmail && <span className="error-message">{errors.businessEmail}</span>}
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="phoneNumber">
                Phone Number <span className="required">*</span>
              </label>
              <input
                type="tel"
                id="phoneNumber"
                name="phoneNumber"
                value={formData.phoneNumber}
                onChange={handleInputChange}
                className={errors.phoneNumber ? 'error' : ''}
                placeholder="+1 (555) 123-4567"
              />
              {errors.phoneNumber && <span className="error-message">{errors.phoneNumber}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="inquiryType">
                Inquiry Type <span className="required">*</span>
              </label>
              <select
                id="inquiryType"
                name="inquiryType"
                value={formData.inquiryType}
                onChange={handleInputChange}
                className={errors.inquiryType ? 'error' : ''}
              >
                <option value="">Select inquiry type</option>
                {formOptions.inquiryTypes.map((type) => (
                  <option key={type} value={type}>{type}</option>
                ))}
              </select>
              {errors.inquiryType && <span className="error-message">{errors.inquiryType}</span>}
            </div>
          </div>
        </div>

        {/* Requirements Section */}
        <div className="form-section">
          <h2>Requirements & Message</h2>
          
          <div className="form-group full-width">
            <label htmlFor="message">
              Message / Requirements Description <span className="required">*</span>
            </label>
            <textarea
              id="message"
              name="message"
              value={formData.message}
              onChange={handleInputChange}
              className={errors.message ? 'error' : ''}
              placeholder="Please describe your requirements, integration needs, or any specific questions you have about Trylia's virtual try-on technology..."
              rows="5"
              maxLength="1000"
            />
            <div className="character-count">
              {formData.message.length}/1000 characters
            </div>
            {errors.message && <span className="error-message">{errors.message}</span>}
          </div>
        </div>

        {/* Meeting Preferences Section */}
        <div className="form-section">
          <h2>Meeting Preferences</h2>
          
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="meetingMode">
                Preferred Meeting Mode <span className="required">*</span>
              </label>
              <select
                id="meetingMode"
                name="meetingMode"
                value={formData.meetingMode}
                onChange={handleInputChange}
                className={errors.meetingMode ? 'error' : ''}
              >
                <option value="">Select meeting preference</option>
                {formOptions.meetingModes.map((mode) => (
                  <option key={mode} value={mode}>{mode}</option>
                ))}
              </select>
              {errors.meetingMode && <span className="error-message">{errors.meetingMode}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="meetingTime">
                Preferred Meeting Time <span className="optional">(Optional)</span>
              </label>
              <input
                type="datetime-local"
                id="meetingTime"
                name="meetingTime"
                value={formData.meetingTime}
                onChange={handleInputChange}
                min={getMinDateTime()}
              />
              <small className="field-help">
                Select your preferred date and time for a meeting (your local time)
              </small>
            </div>
          </div>
        </div>

        {/* Submit Button */}
        <div className="form-submit">
          <button 
            type="submit" 
            className="submit-button"
            disabled={isSubmitting}
          >
            {isSubmitting ? (
              <>
                <div className="button-spinner"></div>
                Submitting...
              </>
            ) : (
              'Submit Inquiry'
            )}
          </button>
          
          <p className="submit-note">
            By submitting this form, you agree to be contacted by Trylia regarding your inquiry. 
            We typically respond within 24 hours during business days.
          </p>
        </div>
      </form>
    </div>
  );
};

export default ContactForm;