# Interior Design Landing Page - PRD

## Original Problem Statement
Build a conversion-focused landing page for an interior design business based in Mumbai, India. The business offers end-to-end home transformation services targeting middle-income families who discover the business via Instagram ads.

**Primary Goal:** Visitor lands from Instagram ad → gets inspired → submits quote request or contacts via WhatsApp.

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

### ✅ Phase 1: Frontend-Only Landing Page (Completed)

**Date:** December 2024

#### Files Created:
1. `/app/frontend/src/data/mock.js` - Mock data for services, testimonials, gallery, form options
2. `/app/frontend/src/pages/LandingPage.jsx` - Main landing page component (all sections)
3. `/app/frontend/src/App.js` - Updated to route to LandingPage
4. `/app/frontend/src/App.css` - Complete styling with warm earthy aesthetic

#### Sections Implemented:
- ✅ Hero Section: Full-screen with background image, headline, subtitle, dual CTAs
- ✅ Services Section: 4 service cards with icons (Modular Kitchen, False Ceilings, Wardrobes, Full Home)
- ✅ Trust Section: 4 trust-builder points with icons
- ✅ Gallery Section: 6 project images with overlays and service tags
- ✅ Testimonials Section: 3 client testimonials with star ratings
- ✅ Quote Form Section: Complete form with validation (Name, Phone, Area, Service, Budget, Message)
- ✅ Floating WhatsApp Button: Fixed bottom-right with hover effects
- ✅ Footer: Brand name, contact info, Instagram link

#### Features:
- ✅ Client-side form validation (required fields, phone format check)
- ✅ Thank-you message display on form submission
- ✅ WhatsApp integration (deep links with pre-filled message)
- ✅ Smooth scroll navigation
- ✅ Fade-in animations using IntersectionObserver
- ✅ Hover effects on cards, buttons, and interactive elements
- ✅ Mobile-responsive grid layouts

#### Design Implementation:
- ✅ Warm color palette with terracotta, cream, and brown tones
- ✅ Google Fonts integration (Playfair Display + Inter)
- ✅ Proper spacing and typography hierarchy
- ✅ Card hover effects with shadow and transform
- ✅ Gallery image overlays with gradient
- ✅ Button transitions with color and shadow changes

## Prioritized Backlog

### P0 (Next Phase - Backend Integration)
- [ ] Backend API for form submission
- [ ] MongoDB schema for lead storage
- [ ] Email notification on form submission
- [ ] Admin dashboard to view submitted leads
- [ ] Form submission to send WhatsApp notification

### P1 (Enhancement Features)
- [ ] Replace placeholder images with actual client project photos
- [ ] Instagram feed integration (show recent posts)
- [ ] Add more detailed service pages with routing
- [ ] Lead analytics (track conversion rates)
- [ ] A/B testing for different CTAs
- [ ] Google Analytics / Meta Pixel integration

### P2 (Nice-to-Have)
- [ ] Video testimonials
- [ ] Live chat integration
- [ ] Cost calculator tool
- [ ] Blog section for interior design tips
- [ ] Before/After slider comparison widget
- [ ] Multi-language support (Hindi, Marathi)

## Next Tasks
1. **User Review:** Client to review the landing page design and provide feedback
2. **Image Replacement:** Replace placeholder images with actual project photos
3. **Content Review:** Verify copy, testimonials, and service descriptions
4. **Backend Development:** Implement lead capture API if client wants to store submissions
5. **Testing:** Mobile device testing on actual phones (iPhone, Android)
6. **Launch Preparation:** Domain setup, hosting, analytics integration

## API Contracts (For Future Backend)

### POST /api/leads
**Request Body:**
```json
{
  "name": "string (required)",
  "phone": "string (10 digits, required)",
  "area": "string (required)",
  "service": "string (required)",
  "budget": "string (required)",
  "message": "string (optional)",
  "source": "landing_page",
  "timestamp": "ISO datetime"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Quote request received",
  "lead_id": "string"
}
```

## Notes
- Current implementation uses client-side only (no backend)
- Form data is logged to console but not stored
- WhatsApp links use the number: +91 96992 61435
- All images are from Unsplash placeholders
- Ready for client to provide actual images and content
