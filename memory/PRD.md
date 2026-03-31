# Interior Design Landing Page - PRD

## Original Problem Statement
Build a conversion-focused landing page for Millenial Architects, an interior design business based in Mumbai, India. The business offers end-to-end home transformation services targeting middle-income families who discover the business via Instagram ads.

**Primary Goal:** Visitor lands from Instagram ad → gets inspired → submits quote request or contacts via WhatsApp.

**Business Details:**
- Company Name: Millenial Architects
- WhatsApp: +91 8551904280
- Email: architectsmillennial@gmail.com

## User Personas
- **Primary:** Mumbai middle-income families (₹8L–25L/year household income)
- **Discovery Channel:** Instagram ads
- **Device:** Primarily mobile (Instagram users)
- **Intent:** Looking for affordable, quality home interior solutions

## Core Requirements (Static)

### Design Requirements
- Warm, earthy, premium-yet-approachable aesthetic
- Color palette: Terracotta (#C17453), warm white (#FAF7F2), soft gold (#D4AF37), warm browns
- Typography: Playfair Display (serif headings) + Inter (sans-serif body)
- Mobile-first responsive design
- Smooth scroll and fade-in animations
- Single-page layout

### Functional Requirements
- Hero section with dual CTAs (Get Quote + WhatsApp)
- Services showcase (4 service cards)
- Trust section (4 trust points)
- Before/After gallery (6 project images)
- Testimonials (3 client reviews)
- Quote request form with validation
- Floating WhatsApp button
- Footer with contact info

### Technical Requirements
- React frontend with shadcn/ui components
- Client-side form validation
- WhatsApp deep link integration
- Responsive breakpoints for mobile/tablet/desktop
- No backend initially (client-side thank-you message)

## What's Been Implemented (December 2024)

### ✅ Phase 1: Frontend-Only Landing Page (Completed - Dec 2024)

**Date:** December 2024

#### Files Created:
1. `/app/frontend/src/data/mock.js` - Mock data for services, testimonials, gallery, form options
2. `/app/frontend/src/pages/LandingPage.jsx` - Main landing page component (all sections)
3. `/app/frontend/src/App.js` - Updated to route to LandingPage
4. `/app/frontend/src/App.css` - Complete styling with warm earthy aesthetic

#### Design Implementation:
- ✅ Warm color palette with terracotta, cream, and brown tones
- ✅ Google Fonts integration (Playfair Display + Inter)
- ✅ Hero Section: Full-screen with background image, headline, subtitle, dual CTAs
- ✅ Services Section: 4 service cards with icons
- ✅ Trust Section: 4 trust-builder points with icons
- ✅ Gallery Section: 6 project images with overlays and service tags
- ✅ Testimonials Section: 3 client testimonials with star ratings
- ✅ Quote Form Section: Complete form with validation + optional email field
- ✅ Floating WhatsApp Button: Fixed bottom-right with hover effects
- ✅ Footer: Brand name, contact info, Instagram link
- ✅ Mobile-responsive grid layouts

### ✅ Phase 2: Backend Integration & Lead Management (Completed - Dec 2024)

**Date:** December 31, 2024

#### Backend Files Created:
1. `/app/backend/models/lead.py` - Lead model with Pydantic schema
2. `/app/backend/services/email_service.py` - Email service with Gmail SMTP integration
3. `/app/backend/server.py` - Updated with lead management endpoints
4. `/app/backend/.env` - Added Gmail credentials

#### Backend Features:
- ✅ POST /api/leads - Create new lead from form submission
- ✅ GET /api/leads - Retrieve all leads with optional status filter
- ✅ GET /api/leads/{id} - Get specific lead by ID
- ✅ MongoDB integration for lead storage
- ✅ Email notification system (business owner)
- ✅ Auto-reply confirmation emails (customers)
- ✅ Professional HTML email templates

#### Frontend Updates:
- ✅ Updated company name to "Millenial Architects"
- ✅ Updated WhatsApp number to +91 8551904280
- ✅ Added optional email field to quote form
- ✅ Integrated form submission with backend API
- ✅ Error handling for API failures

#### Current Status:
- ✅ Backend API fully functional
- ✅ Leads being saved to MongoDB
- ✅ WhatsApp deep links updated
- ⚠️ **Email notifications pending**: Requires Gmail App Password (see `/app/memory/gmail_app_password_instructions.md`)

## Prioritized Backlog

### P0 (Immediate - Pending)
- [ ] **Generate Gmail App Password** and update `/app/backend/.env` to enable email notifications
  - Follow instructions in `/app/memory/gmail_app_password_instructions.md`
  - Once updated, email notifications will work automatically

### P1 (Next Phase - Enhancements)
- [ ] Replace placeholder images with actual Millenial Architects project photos
- [ ] Test email notifications end-to-end after App Password is configured
- [ ] Admin dashboard to view and manage leads
- [ ] Export leads to CSV/Excel
- [ ] Lead status management (New, Contacted, Quoted, Won, Lost)
- [ ] Instagram feed integration (show recent posts)
- [ ] Google Analytics / Meta Pixel integration for ad tracking
- [ ] WhatsApp Business API integration for automated messages (currently using deep links only)

### P2 (Nice-to-Have)
- [ ] Video testimonials
- [ ] Live chat integration
- [ ] Cost calculator tool
- [ ] Blog section for interior design tips
- [ ] Before/After slider comparison widget
- [ ] Multi-language support (Hindi, Marathi)

## Next Tasks
1. **CRITICAL: Generate Gmail App Password**
   - Follow steps in `/app/memory/gmail_app_password_instructions.md`
   - Update GMAIL_PASSWORD in `/app/backend/.env`
   - Restart backend: `sudo supervisorctl restart backend`
   - Test by submitting a quote form with your email

2. **Content Updates:**
   - Replace placeholder images with actual project photos
   - Update Instagram link in footer when available
   - Review and adjust testimonials with real client feedback

3. **Testing:**
   - Submit test quote requests to verify email notifications
   - Test on mobile devices (Instagram traffic will be mobile-heavy)
   - Check WhatsApp deep link works correctly

4. **Future Enhancements:**
   - Build admin dashboard for lead management
   - Set up Meta Pixel for Instagram ad tracking
   - Consider WhatsApp Business API for automated responses

## API Contracts (Implemented)

### POST /api/leads
**Request Body:**
```json
{
  "name": "string (required)",
  "phone": "string (10 digits, required)",
  "email": "string (optional)",
  "area": "string (required)",
  "service": "string (required)",
  "budget": "string (required)",
  "message": "string (optional)"
}
```

**Response:**
```json
{
  "id": "uuid",
  "name": "string",
  "phone": "string",
  "email": "string",
  "area": "string",
  "service": "string",
  "budget": "string",
  "message": "string",
  "source": "landing_page",
  "status": "new",
  "created_at": "ISO datetime"
}
```

### GET /api/leads
**Query Parameters:**
- `limit`: integer (default: 100)
- `status`: string (optional filter)

**Response:** Array of Lead objects

### GET /api/leads/{lead_id}
**Response:** Single Lead object or 404 if not found

## Email Notifications

### Business Owner Notification
- **To:** architectsmillennial@gmail.com
- **Subject:** "🏠 New Quote Request from {customer_name}"
- **Content:** Professional HTML email with all lead details and WhatsApp CTA

### Customer Auto-Reply
- **To:** Customer's email (if provided)
- **Subject:** "Thank you for your interest in Millenial Architects!"
- **Content:** Branded confirmation email with next steps and WhatsApp link

## Notes
- ✅ Backend implemented with FastAPI + MongoDB
- ✅ Form data is saved to database at each submission
- ✅ WhatsApp number: +91 8551904280
- ✅ Company name: Millenial Architects
- ⚠️ **Email notifications require Gmail App Password** (see instructions)
- All images are from Unsplash placeholders - ready to replace with actual photos
- Email templates are professional and branded
- System handles email failures gracefully (submissions still work)
