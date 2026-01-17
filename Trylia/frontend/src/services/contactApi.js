/**
 * API service for Trylia Contact Us functionality
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

class ContactApiService {
  async submitContactForm(formData) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/contact`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'Failed to submit contact form');
      }

      return {
        success: true,
        data: data,
      };
    } catch (error) {
      console.error('Contact form submission error:', error);
      return {
        success: false,
        error: error.message || 'Network error occurred',
      };
    }
  }

  async getFormOptions() {
    try {
      const response = await fetch(`${API_BASE_URL}/api/contact/options`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'Failed to load form options');
      }

      return {
        success: true,
        options: data.options,
      };
    } catch (error) {
      console.error('Form options loading error:', error);
      return {
        success: false,
        error: error.message || 'Failed to load form options',
        // Fallback options
        options: {
          companySizes: [
            "1-10 employees",
            "11-50 employees", 
            "51-200 employees",
            "201-1000 employees",
            "1000+ employees",
            "Startup",
            "Enterprise"
          ],
          inquiryTypes: [
            "Integration Request",
            "Pricing Information",
            "Demo Request",
            "Technical Support",
            "Partnership Opportunity",
            "Custom Solution",
            "Other"
          ],
          meetingModes: [
            "Google Meet",
            "Zoom",
            "Microsoft Teams",
            "Phone Call",
            "In-Person Meeting",
            "No Meeting Required"
          ],
          countries: [
            "United States", "United Kingdom", "Canada", "Germany", "France", 
            "India", "Australia", "Japan", "Brazil", "Mexico", "Italy", "Spain",
            "Netherlands", "Sweden", "Norway", "Denmark", "Finland", "Switzerland",
            "Austria", "Belgium", "Ireland", "New Zealand", "South Korea", "Singapore",
            "Hong Kong", "UAE", "Saudi Arabia", "South Africa", "Argentina", "Chile",
            "Colombia", "Peru", "Poland", "Czech Republic", "Hungary", "Romania",
            "Bulgaria", "Croatia", "Slovenia", "Slovakia", "Estonia", "Latvia",
            "Lithuania", "Portugal", "Greece", "Turkey", "Israel", "Egypt",
            "Morocco", "Nigeria", "Kenya", "Ghana", "Thailand", "Vietnam",
            "Philippines", "Indonesia", "Malaysia", "Taiwan", "China", "Russia",
            "Ukraine", "Belarus", "Kazakhstan", "Other"
          ]
        }
      };
    }
  }

  async checkServerHealth() {
    try {
      const response = await fetch(`${API_BASE_URL}/health`, {
        method: 'GET',
      });

      return response.ok;
    } catch (error) {
      console.error('Server health check failed:', error);
      return false;
    }
  }
}

export default new ContactApiService();