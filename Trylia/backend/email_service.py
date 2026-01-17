"""
Email service for Trylia Contact Us feature
Handles email sending and template formatting
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging
from email_validator import validate_email, EmailNotValidError # type: ignore

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        # Email configuration from environment variables
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_username = os.getenv('SMTP_USERNAME', '')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
        self.from_email = os.getenv('FROM_EMAIL', self.smtp_username)
        self.to_email = os.getenv('TO_EMAIL', 'himanshu.kasia@gmail.com')  # Your business email
        
        # Validate configuration
        if not all([self.smtp_username, self.smtp_password]):
            logger.warning("Email configuration incomplete. Email sending will be disabled.")
            logger.warning("Please configure SMTP settings in .env file to enable email functionality.")
            self.enabled = False
        else:
            self.enabled = True
            logger.info(f"Email service initialized with SMTP server: {self.smtp_server}")
    
    def validate_email_address(self, email):
        """Validate email address format"""
        try:
            # Use check_deliverability=False for better user experience
            valid = validate_email(email, check_deliverability=False)
            return True, valid.email
        except EmailNotValidError as e:
            return False, str(e)
    
    def create_contact_email_template(self, form_data):
        """Create professional email template for contact form submission"""
        
        # Format meeting time if provided
        meeting_time = form_data.get('meetingTime', '')
        if meeting_time:
            try:
                # Parse ISO datetime string
                dt = datetime.fromisoformat(meeting_time.replace('Z', '+00:00'))
                meeting_time_formatted = dt.strftime('%B %d, %Y at %I:%M %p UTC')
            except:
                meeting_time_formatted = meeting_time
        else:
            meeting_time_formatted = 'Not specified'
        
        # Create HTML email template
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background-color: #2c3e50; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9f9f9; }}
                .section {{ margin-bottom: 20px; padding: 15px; background-color: white; border-radius: 5px; }}
                .label {{ font-weight: bold; color: #2c3e50; }}
                .value {{ margin-left: 10px; }}
                .footer {{ background-color: #34495e; color: white; padding: 15px; text-align: center; font-size: 12px; }}
                .priority {{ background-color: #e74c3c; color: white; padding: 5px 10px; border-radius: 3px; display: inline-block; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🎯 Trylia - New Business Inquiry</h1>
                <p>Virtual Dressing Room Solutions for E-commerce</p>
            </div>
            
            <div class="content">
                <div class="section">
                    <h2>📋 Contact Information</h2>
                    <p><span class="label">Company Name:</span><span class="value">{form_data.get('companyName', 'N/A')}</span></p>
                    <p><span class="label">Website:</span><span class="value"><a href="{form_data.get('websiteUrl', '#')}">{form_data.get('websiteUrl', 'N/A')}</a></span></p>
                    <p><span class="label">Contact Person:</span><span class="value">{form_data.get('contactPerson', 'N/A')}</span></p>
                    <p><span class="label">Business Email:</span><span class="value"><a href="mailto:{form_data.get('businessEmail', '')}">{form_data.get('businessEmail', 'N/A')}</a></span></p>
                    <p><span class="label">Phone Number:</span><span class="value">{form_data.get('phoneNumber', 'N/A')}</span></p>
                    <p><span class="label">Country/Region:</span><span class="value">{form_data.get('country', 'N/A')}</span></p>
                </div>
                
                <div class="section">
                    <h2>🏢 Company Details</h2>
                    <p><span class="label">Company Size:</span><span class="value">{form_data.get('companySize', 'N/A')}</span></p>
                    <p><span class="label">Inquiry Type:</span><span class="value"><span class="priority">{form_data.get('inquiryType', 'N/A')}</span></span></p>
                </div>
                
                <div class="section">
                    <h2>💬 Message & Requirements</h2>
                    <div style="background-color: #ecf0f1; padding: 15px; border-radius: 5px; border-left: 4px solid #3498db;">
                        {form_data.get('message', 'No message provided').replace('\n', '<br>')}
                    </div>
                </div>
                
                <div class="section">
                    <h2>📅 Meeting Preferences</h2>
                    <p><span class="label">Preferred Meeting Mode:</span><span class="value">{form_data.get('meetingMode', 'N/A')}</span></p>
                    <p><span class="label">Preferred Meeting Time:</span><span class="value">{meeting_time_formatted}</span></p>
                </div>
                
                <div class="section">
                    <h2>⚡ Next Steps</h2>
                    <ul>
                        <li>Response within 24 hours during business days</li>
                        <li>Technical consultation if integration request</li>
                        <li>Custom demo preparation if demo requested</li>
                        <li>Pricing proposal if pricing inquiry</li>
                    </ul>
                </div>
            </div>
            
            <div class="footer">
                <p><strong>Trylia - Virtual Dressing Room Solutions</strong></p>
                <p>Revolutionizing E-commerce with AI-Powered Virtual Try-On Technology</p>
                <p>Submitted on: {datetime.now().strftime('%B %d, %Y at %I:%M %p UTC')}</p>
            </div>
        </body>
        </html>
        """
        
        # Create plain text version
        text_template = f"""
TRYLIA - NEW BUSINESS INQUIRY
Virtual Dressing Room Solutions for E-commerce

CONTACT INFORMATION:
Company Name: {form_data.get('companyName', 'N/A')}
Website: {form_data.get('websiteUrl', 'N/A')}
Contact Person: {form_data.get('contactPerson', 'N/A')}
Business Email: {form_data.get('businessEmail', 'N/A')}
Phone Number: {form_data.get('phoneNumber', 'N/A')}
Country/Region: {form_data.get('country', 'N/A')}

COMPANY DETAILS:
Company Size: {form_data.get('companySize', 'N/A')}
Inquiry Type: {form_data.get('inquiryType', 'N/A')}

MESSAGE & REQUIREMENTS:
{form_data.get('message', 'No message provided')}

MEETING PREFERENCES:
Preferred Meeting Mode: {form_data.get('meetingMode', 'N/A')}
Preferred Meeting Time: {meeting_time_formatted}

NEXT STEPS:
- Response within 24 hours during business days
- Technical consultation if integration request
- Custom demo preparation if demo requested
- Pricing proposal if pricing inquiry

Submitted on: {datetime.now().strftime('%B %d, %Y at %I:%M %p UTC')}
        """
        
        return html_template, text_template
    
    def send_contact_email(self, form_data):
        """Send contact form email"""
        if not self.enabled:
            logger.error("Email service is not configured properly")
            return False, "Email service is not configured"
        
        try:
            # Validate business email
            is_valid, validated_email = self.validate_email_address(form_data.get('businessEmail', ''))
            if not is_valid:
                return False, f"Invalid email address: {validated_email}"
            
            # Create email templates
            html_content, text_content = self.create_contact_email_template(form_data)
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"🎯 Trylia Business Inquiry - {form_data.get('inquiryType', 'General')} from {form_data.get('companyName', 'Unknown Company')}"
            msg['From'] = self.from_email
            msg['To'] = self.to_email
            msg['Reply-To'] = validated_email
            
            # Attach both text and HTML versions
            text_part = MIMEText(text_content, 'plain')
            html_part = MIMEText(html_content, 'html')
            
            msg.attach(text_part)
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Contact email sent successfully for {form_data.get('companyName', 'Unknown')}")
            return True, "Email sent successfully"
            
        except Exception as e:
            logger.error(f"Failed to send contact email: {str(e)}")
            return False, f"Failed to send email: {str(e)}"
    
    def send_confirmation_email(self, form_data):
        """Send confirmation email to the customer"""
        if not self.enabled:
            return False, "Email service is not configured"
        
        try:
            customer_email = form_data.get('businessEmail', '')
            is_valid, validated_email = self.validate_email_address(customer_email)
            if not is_valid:
                return False, f"Invalid customer email: {validated_email}"
            
            # Create confirmation email
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .header {{ background-color: #3498db; color: white; padding: 20px; text-align: center; }}
                    .content {{ padding: 20px; }}
                    .footer {{ background-color: #34495e; color: white; padding: 15px; text-align: center; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>✅ Thank You for Contacting Trylia!</h1>
                </div>
                <div class="content">
                    <p>Dear {form_data.get('contactPerson', 'Valued Partner')},</p>
                    
                    <p>Thank you for your interest in Trylia's virtual dressing room solutions! We have received your inquiry regarding <strong>{form_data.get('inquiryType', 'our services')}</strong>.</p>
                    
                    <h3>What happens next?</h3>
                    <ul>
                        <li>Our team will review your requirements within 24 hours</li>
                        <li>You'll receive a personalized response from our solutions expert</li>
                        <li>We'll schedule a demo or consultation based on your preferences</li>
                    </ul>
                    
                    <p>In the meantime, feel free to explore our technology and see how we're revolutionizing e-commerce with AI-powered virtual try-on solutions.</p>
                    
                    <p>Best regards,<br>
                    <strong>The Trylia Team</strong><br>
                    Virtual Dressing Room Solutions</p>
                </div>
                <div class="footer">
                    <p>This is an automated confirmation. Please do not reply to this email.</p>
                </div>
            </body>
            </html>
            """
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "✅ Trylia - We've Received Your Inquiry!"
            msg['From'] = self.from_email
            msg['To'] = validated_email
            
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Send confirmation email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Confirmation email sent to {validated_email}")
            return True, "Confirmation email sent"
            
        except Exception as e:
            logger.error(f"Failed to send confirmation email: {str(e)}")
            return False, f"Failed to send confirmation email: {str(e)}"

# Global email service instance
email_service = EmailService()