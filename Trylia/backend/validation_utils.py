"""
Validation utilities for Trylia Contact Us feature
"""

import re
from urllib.parse import urlparse
from email_validator import validate_email, EmailNotValidError # type: ignore

class ContactFormValidator:
    """Validator for contact form data"""
    
    # Valid options for dropdowns
    COMPANY_SIZES = [
        "1-10 employees",
        "11-50 employees", 
        "51-200 employees",
        "201-1000 employees",
        "1000+ employees",
        "Startup",
        "Enterprise"
    ]
    
    INQUIRY_TYPES = [
        "Integration Request",
        "Pricing Information",
        "Demo Request",
        "Technical Support",
        "Partnership Opportunity",
        "Custom Solution",
        "Other"
    ]
    
    MEETING_MODES = [
        "Google Meet",
        "Zoom",
        "Microsoft Teams",
        "Phone Call",
        "In-Person Meeting",
        "No Meeting Required"
    ]
    
    COUNTRIES = [
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
    
    @staticmethod
    def validate_required_field(value, field_name, min_length=1, max_length=None):
        """Validate required field with length constraints"""
        if not value or not value.strip():
            return False, f"{field_name} is required"
        
        value = value.strip()
        if len(value) < min_length:
            return False, f"{field_name} must be at least {min_length} characters"
        
        if max_length and len(value) > max_length:
            return False, f"{field_name} must not exceed {max_length} characters"
        
        return True, value
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        try:
            # Use check_deliverability=False to avoid strict domain checking
            # This allows valid email formats without checking if domain accepts email
            valid = validate_email(email, check_deliverability=False)
            return True, valid.email
        except EmailNotValidError as e:
            return False, f"Invalid email format: {str(e)}"
    
    @staticmethod
    def validate_url(url):
        """Validate URL format"""
        if not url or not url.strip():
            return False, "Website URL is required"
        
        url = url.strip()
        
        # Add protocol if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        try:
            result = urlparse(url)
            if not all([result.scheme, result.netloc]):
                return False, "Invalid URL format"
            
            # Basic domain validation
            if '.' not in result.netloc:
                return False, "Invalid domain format"
            
            return True, url
        except Exception:
            return False, "Invalid URL format"
    
    @staticmethod
    def validate_phone(phone):
        """Validate phone number format"""
        if not phone or not phone.strip():
            return False, "Phone number is required"
        
        phone = phone.strip()
        
        # Remove common separators and spaces
        cleaned_phone = re.sub(r'[\s\-\(\)\+\.]', '', phone)
        
        # Check if it contains only digits after cleaning
        if not cleaned_phone.isdigit():
            return False, "Phone number should contain only digits, spaces, hyphens, parentheses, and plus sign"
        
        # Check length (international format can be 7-15 digits)
        if len(cleaned_phone) < 7 or len(cleaned_phone) > 15:
            return False, "Phone number should be between 7 and 15 digits"
        
        return True, phone
    
    @staticmethod
    def validate_dropdown_choice(value, valid_choices, field_name):
        """Validate dropdown selection"""
        if not value or value not in valid_choices:
            return False, f"Please select a valid {field_name}"
        return True, value
    
    @classmethod
    def validate_contact_form(cls, form_data):
        """Validate entire contact form"""
        errors = {}
        validated_data = {}
        
        # Company Name
        is_valid, result = cls.validate_required_field(
            form_data.get('companyName'), 'Company Name', 2, 100
        )
        if not is_valid:
            errors['companyName'] = result
        else:
            validated_data['companyName'] = result
        
        # Website URL
        is_valid, result = cls.validate_url(form_data.get('websiteUrl'))
        if not is_valid:
            errors['websiteUrl'] = result
        else:
            validated_data['websiteUrl'] = result
        
        # Contact Person
        is_valid, result = cls.validate_required_field(
            form_data.get('contactPerson'), 'Contact Person Name', 2, 50
        )
        if not is_valid:
            errors['contactPerson'] = result
        else:
            validated_data['contactPerson'] = result
        
        # Business Email
        is_valid, result = cls.validate_email(form_data.get('businessEmail'))
        if not is_valid:
            errors['businessEmail'] = result
        else:
            validated_data['businessEmail'] = result
        
        # Phone Number
        is_valid, result = cls.validate_phone(form_data.get('phoneNumber'))
        if not is_valid:
            errors['phoneNumber'] = result
        else:
            validated_data['phoneNumber'] = result
        
        # Company Size
        is_valid, result = cls.validate_dropdown_choice(
            form_data.get('companySize'), cls.COMPANY_SIZES, 'company size'
        )
        if not is_valid:
            errors['companySize'] = result
        else:
            validated_data['companySize'] = result
        
        # Inquiry Type
        is_valid, result = cls.validate_dropdown_choice(
            form_data.get('inquiryType'), cls.INQUIRY_TYPES, 'inquiry type'
        )
        if not is_valid:
            errors['inquiryType'] = result
        else:
            validated_data['inquiryType'] = result
        
        # Message
        is_valid, result = cls.validate_required_field(
            form_data.get('message'), 'Message', 10, 1000
        )
        if not is_valid:
            errors['message'] = result
        else:
            validated_data['message'] = result
        
        # Meeting Mode
        is_valid, result = cls.validate_dropdown_choice(
            form_data.get('meetingMode'), cls.MEETING_MODES, 'meeting mode'
        )
        if not is_valid:
            errors['meetingMode'] = result
        else:
            validated_data['meetingMode'] = result
        
        # Country
        is_valid, result = cls.validate_dropdown_choice(
            form_data.get('country'), cls.COUNTRIES, 'country'
        )
        if not is_valid:
            errors['country'] = result
        else:
            validated_data['country'] = result
        
        # Meeting Time (optional)
        meeting_time = form_data.get('meetingTime')
        if meeting_time and meeting_time.strip():
            validated_data['meetingTime'] = meeting_time.strip()
        
        return len(errors) == 0, errors, validated_data