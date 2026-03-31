# Deployment Guide - Millenial Architects Landing Page

## Quick Overview
Since you have a **full-stack application** (React frontend + FastAPI backend + MongoDB), you need to deploy them separately:

1. **Frontend** → Netlify (static hosting)
2. **Backend** → Render/Railway (API server)
3. **Database** → MongoDB Atlas (cloud database)

---

## Step-by-Step Deployment

### STEP 1: Deploy Backend (Render.com - FREE)

1. **Create MongoDB Atlas Database** (Free):
   - Go to https://www.mongodb.com/cloud/atlas
   - Sign up and create a free cluster
   - Get your connection string (looks like: `mongodb+srv://username:password@cluster.mongodb.net/`)

2. **Deploy Backend to Render**:
   - Go to https://render.com and sign up
   - Click "New +" → "Web Service"
   - Connect your GitHub repo (or upload backend folder)
   - Settings:
     - Name: `millenial-architects-api`
     - Environment: `Python 3`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `uvicorn server:app --host 0.0.0.0 --port $PORT`
   
3. **Add Environment Variables** in Render:
   ```
   MONGO_URL=your_mongodb_atlas_connection_string
   DB_NAME=millenial_architects
   GMAIL_USER=architectsmillennial@gmail.com
   GMAIL_PASSWORD=tlurzumbflbqhmnd
   BUSINESS_EMAIL=architectsmillennial@gmail.com
   CORS_ORIGINS=*
   ```

4. **Deploy** - Copy your backend URL (e.g., `https://millenial-architects-api.onrender.com`)

---

### STEP 2: Deploy Frontend (Netlify)

1. **Update Frontend Environment**:
   - Edit `frontend/.env`:
     ```
     REACT_APP_BACKEND_URL=https://millenial-architects-api.onrender.com
     ```

2. **Build Frontend**:
   ```bash
   cd frontend
   yarn install
   yarn build
   ```

3. **Deploy to Netlify**:
   - Go to https://www.netlify.com and sign up
   - Drag and drop the `frontend/build` folder
   - Or connect GitHub repo:
     - Build command: `cd frontend && yarn build`
     - Publish directory: `frontend/build`

4. **Add Environment Variable** in Netlify:
   - Site settings → Environment variables
   - Add: `REACT_APP_BACKEND_URL` = your Render backend URL

5. **Get your Netlify URL** (e.g., `https://millenial-architects.netlify.app`)

---

### STEP 3: Update CORS in Backend

Go back to Render and update the CORS_ORIGINS environment variable:
```
CORS_ORIGINS=https://millenial-architects.netlify.app
```

Redeploy the backend.

---

## Alternative: All-in-One Deployment

### Railway.app (Easier, ~$5/month)
Railway can host both frontend and backend together:

1. Go to https://railway.app
2. Create new project from GitHub
3. Railway auto-detects both frontend and backend
4. Add environment variables
5. Get single URL for everything

### Vercel (Frontend + Serverless API)
Good alternative to Netlify, can also host backend as serverless functions.

---

## Custom Domain Setup

### For Netlify (Frontend):
1. Buy domain from Namecheap/GoDaddy (e.g., millenialararchitects.com)
2. In Netlify: Site settings → Domain management → Add custom domain
3. Update DNS records as instructed

### For Render (Backend):
Backend URL stays as `*.onrender.com` (users won't see it)

---

## Testing After Deployment

1. Visit your Netlify URL
2. Submit a test quote form
3. Check:
   - ✅ Lead saved to MongoDB
   - ✅ Email received at architectsmillennial@gmail.com
   - ✅ Customer auto-reply sent
   - ✅ WhatsApp button works

---

## Cost Summary

**Free Option:**
- MongoDB Atlas: Free (512MB)
- Render Backend: Free tier (spins down after inactivity)
- Netlify Frontend: Free (100GB bandwidth)
- **Total: ₹0/month** (just domain ~₹500/year)

**Paid Option (Better performance):**
- MongoDB Atlas: Free
- Render: $7/month (always on)
- Netlify: Free
- **Total: ~₹600/month**

---

## Need Help?

If you run into issues:
1. Check Render logs for backend errors
2. Check Netlify deploy logs for frontend errors
3. Verify environment variables are set correctly
4. Test backend API directly: `https://your-backend.onrender.com/api/`

---

## Files Included in Source Code

- `frontend/` - Complete React application
- `backend/` - Complete FastAPI server
- `.env.example` - Template for environment variables
- `README.md` - Project overview
- `DEPLOYMENT.md` - This file
