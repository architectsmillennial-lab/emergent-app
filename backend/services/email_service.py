import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = os.environ.get('GMAIL_USER')
        self.sender_password = os.environ.get('GMAIL_PASSWORD')
        self.business_email = os.environ.get('BUSINESS_EMAIL', self.sender_email)
        
    def send_email(self, to_email: str, subject: str, html_content: str):
        """Send email using Gmail SMTP"""
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = f"Millenial Architects <{self.sender_email}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
                
            logger.info(f"Email sent successfully to {to_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            raise e
    
    def send_lead_notification(self, lead_data: dict):
        """Send notification to business owner about new lead"""
        subject = f"🏠 New Quote Request from {lead_data['name']}"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: 'Inter', Arial, sans-serif; line-height: 1.6; color: #4A3F35; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #C17453 0%, #A86243 100%); 
                           color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }}
                .header h1 {{ margin: 0; font-family: 'Playfair Display', serif; font-size: 28px; }}
                .content {{ background: #FAF7F2; padding: 30px; border-radius: 0 0 8px 8px; }}
                .field {{ margin-bottom: 20px; }}
                .label {{ font-weight: 600; color: #8B6F47; font-size: 14px; text-transform: uppercase; 
                         letter-spacing: 0.5px; margin-bottom: 5px; }}
                .value {{ font-size: 16px; color: #4A3F35; background: white; padding: 12px; 
                         border-radius: 6px; border-left: 3px solid #C17453; }}
                .cta {{ text-align: center; margin-top: 30px; }}
                .cta a {{ background: #C17453; color: white; padding: 15px 30px; text-decoration: none; 
                         border-radius: 6px; display: inline-block; font-weight: 600; }}
                .footer {{ text-align: center; margin-top: 30px; color: #8B6F47; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>New Quote Request</h1>
                    <p style="margin: 10px 0 0 0; opacity: 0.9;">Someone is interested in your services!</p>
                </div>
                <div class="content">
                    <div class="field">
                        <div class="label">Customer Name</div>
                        <div class="value">{lead_data['name']}</div>
                    </div>
                    <div class="field">
                        <div class="label">Phone Number</div>
                        <div class="value">+91 {lead_data['phone']}</div>
                    </div>
                    <div class="field">
                        <div class="label">Area/Location</div>
                        <div class="value">{lead_data['area']}</div>
                    </div>
                    <div class="field">
                        <div class="label">Service Interested In</div>
                        <div class="value">{lead_data['service']}</div>
                    </div>
                    <div class="field">
                        <div class="label">Budget Range</div>
                        <div class="value">{lead_data['budget']}</div>
                    </div>
                    {f'''<div class="field">
                        <div class="label">Message</div>
                        <div class="value">{lead_data['message']}</div>
                    </div>''' if lead_data.get('message') else ''}
                    <div class="field">
                        <div class="label">Submitted At</div>
                        <div class="value">{datetime.now().strftime('%d %B %Y, %I:%M %p')}</div>
                    </div>
                    <div class="cta">
                        <a href="https://wa.me/91{lead_data['phone']}?text=Hi%20{lead_data['name']}%2C%20thank%20you%20for%20your%20interest%20in%20Millenial%20Architects.%20We%20received%20your%20quote%20request%20for%20{lead_data['service'].replace(' ', '%20')}.%20Let%27s%20discuss%20your%20project!">
                            Contact via WhatsApp
                        </a>
                    </div>
                </div>
                <div class="footer">
                    <p>This is an automated notification from your Millenial Architects website</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(self.business_email, subject, html_content)
    
    def send_customer_confirmation(self, lead_data: dict):
        """Send auto-reply confirmation to customer"""
        subject = "Thank you for your interest in Millenial Architects!"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: 'Inter', Arial, sans-serif; line-height: 1.6; color: #4A3F35; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #C17453 0%, #A86243 100%); 
                           color: white; padding: 40px 30px; text-align: center; border-radius: 8px 8px 0 0; }}
                .header h1 {{ margin: 0; font-family: 'Playfair Display', serif; font-size: 32px; }}
                .content {{ background: #FAF7F2; padding: 30px; border-radius: 0 0 8px 8px; }}
                .greeting {{ font-size: 18px; margin-bottom: 20px; }}
                .message {{ background: white; padding: 20px; border-radius: 6px; 
                           border-left: 4px solid #D4AF37; margin: 20px 0; }}
                .details {{ background: white; padding: 20px; border-radius: 6px; margin: 20px 0; }}
                .detail-row {{ display: flex; padding: 10px 0; border-bottom: 1px solid #EDE7DD; }}
                .detail-row:last-child {{ border-bottom: none; }}
                .detail-label {{ font-weight: 600; color: #8B6F47; min-width: 120px; }}
                .detail-value {{ color: #4A3F35; }}
                .cta {{ text-align: center; margin: 30px 0; }}
                .cta a {{ background: #25D366; color: white; padding: 15px 30px; text-decoration: none; 
                         border-radius: 6px; display: inline-block; font-weight: 600; }}
                .footer {{ text-align: center; margin-top: 30px; padding-top: 20px; 
                          border-top: 1px solid #EDE7DD; color: #8B6F47; font-size: 14px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Millenial Architects</h1>
                    <p style="margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;">
                        Transforming homes, creating dreams
                    </p>
                </div>
                <div class="content">
                    <div class="greeting">
                        Hi {lead_data['name']},
                    </div>
                    <div class="message">
                        <p style="margin: 0 0 15px 0; font-size: 16px;">
                            Thank you for your interest in Millenial Architects! We're excited to help transform your space.
                        </p>
                        <p style="margin: 0; font-size: 16px;">
                            We've received your quote request and our team will get back to you within 24 hours 
                            to discuss your project in detail.
                        </p>
                    </div>
                    
                    <h3 style="color: #4A3F35; font-family: 'Playfair Display', serif; margin-top: 30px;">
                        Your Request Details:
                    </h3>
                    <div class="details">
                        <div class="detail-row">
                            <div class="detail-label">Service:</div>
                            <div class="detail-value">{lead_data['service']}</div>
                        </div>
                        <div class="detail-row">
                            <div class="detail-label">Location:</div>
                            <div class="detail-value">{lead_data['area']}</div>
                        </div>
                        <div class="detail-row">
                            <div class="detail-label">Budget Range:</div>
                            <div class="detail-value">{lead_data['budget']}</div>
                        </div>
                    </div>
                    
                    <div class="cta">
                        <a href="https://wa.me/918551904280?text=Hi%2C%20I%20submitted%20a%20quote%20request%20for%20{lead_data['service'].replace(' ', '%20')}.%20I%20have%20a%20question.">
                            Chat with Us on WhatsApp
                        </a>
                    </div>
                    
                    <div style="background: #F5F1E8; padding: 20px; border-radius: 6px; margin-top: 20px;">
                        <p style="margin: 0 0 10px 0; font-weight: 600; color: #4A3F35;">
                            What happens next?
                        </p>
                        <ul style="margin: 0; padding-left: 20px; color: #4A3F35;">
                            <li>Our design expert will contact you within 24 hours</li>
                            <li>We'll schedule a free consultation at your convenience</li>
                            <li>You'll receive a detailed quote tailored to your needs</li>
                        </ul>
                    </div>
                </div>
                <div class="footer">
                    <p style="margin: 0 0 10px 0; font-weight: 600;">Contact Us</p>
                    <p style="margin: 5px 0;">📞 +91 85519 04280</p>
                    <p style="margin: 5px 0;">📧 {self.sender_email}</p>
                    <p style="margin: 15px 0 0 0; font-size: 12px; color: #8B6F47;">
                        © 2024 Millenial Architects. All rights reserved.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Only send if customer provided email
        if lead_data.get('email'):
            return self.send_email(lead_data['email'], subject, html_content)
        return True  # Skip if no email provided
