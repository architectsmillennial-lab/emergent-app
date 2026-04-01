# Millenial Architects - Landing Page

A conversion-focused landing page for interior design business with lead capture and email notifications.

## Tech Stack
- **Frontend:** React + Tailwind CSS + Shadcn UI
- **Backend:** FastAPI + Python
- **Database:** MongoDB
- **Email:** Gmail SMTP

## Project Structure
```
├── frontend/          # React application
│   ├── src/
│   │   ├── pages/     # Landing page components
│   │   ├── components/ui/  # Shadcn UI components
│   │   └── data/      # Mock data
│   └── package.json
│
├── backend/           # FastAPI server
│   ├── server.py      # Main API server
│   ├── models/        # Pydantic models
│   ├── services/      # Email service
│   └── requirements.txt
```

## Features
✅ Responsive landing page with warm, earthy design
✅ Quote request form with validation
✅ Lead storage in MongoDB
✅ Email notifications (business owner + customer auto-reply)
✅ WhatsApp integration
✅ Mobile-optimized

## Deployment Options

### Option 1: Split Deployment (Recommended)
**Frontend → Netlify**
**Backend → Render/Railway**
**Database → MongoDB Atlas**

### Option 2: Full-Stack Platforms
- Vercel (with serverless API)
- Railway (frontend + backend together)
- Render (frontend + backend together)

See DEPLOYMENT.md for detailed instructions.

## Environment Variables

### Backend (.env)
```
MONGO_URL=your_mongodb_connection_string
DB_NAME=your_database_name
GMAIL_USER=your_email@gmail.com
GMAIL_PASSWORD=your_gmail_app_password
BUSINESS_EMAIL=your_business_email@gmail.com
CORS_ORIGINS=https://your-frontend-domain.netlify.app
```

### Frontend (.env)
```
REACT_APP_BACKEND_URL=https://your-backend-url.render.com
```

## Local Development

### Frontend
```bash
cd frontend
yarn install
yarn start
```

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn server:app --reload --host 0.0.0.0 --port 8001
```

## Contact
- WhatsApp: +91 8551904280
- Email: architectsmillennial@gmail.com

## License
Private - Millenial Architects
