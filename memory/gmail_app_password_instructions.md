# How to Generate Gmail App Password

The system is ready but needs a Gmail App Password to send email notifications.

## Steps to Generate App Password:

1. **Enable 2-Factor Authentication** (if not already enabled):
   - Go to: https://myaccount.google.com/security
   - Click on "2-Step Verification"
   - Follow the steps to enable it

2. **Generate App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - Select app: "Mail"
   - Select device: "Other (Custom name)" → Type "Millenial Architects Website"
   - Click "Generate"
   - You'll get a 16-character password (like: abcd efgh ijkl mnop)

3. **Update the Backend**:
   - Replace the current GMAIL_PASSWORD in `/app/backend/.env` with the 16-character app password
   - Remove all spaces from the app password when adding it
   - Restart backend: `sudo supervisorctl restart backend`

## Current Status:
- ✅ Backend API is working
- ✅ Leads are being saved to database
- ✅ WhatsApp number updated to +91 8551904280
- ✅ Company name changed to "Millenial Architects"
- ⚠️ Email notifications pending App Password

Once you provide the App Password, the system will:
- Send you email notifications for every new quote request
- Send auto-reply confirmation emails to customers
