# Railway Deployment Guide - Millenial Architects

## ✅ Project Structure Confirmed
Your project is correctly structured for Railway deployment. Railway will automatically detect:
- **Backend:** FastAPI (Python) in `/backend`
- **Frontend:** React in `/frontend`

---

## Step-by-Step Railway Deployment

### STEP 1: Create Railway Account & Project

1. Go to https://railway.app
2. Sign up with GitHub/Email
3. Click **"New Project"**
4. Choose **"Deploy from GitHub repo"** OR **"Empty Project"**

---

### STEP 2: Add MongoDB Database

1. In your Railway project, click **"+ New"**
2. Select **"Database"** → **"Add MongoDB"**
3. Railway will automatically create a MongoDB instance
4. **Copy the connection string** - it will look like:
   ```
   mongodb://mongo:PASSWORD@monorail.proxy.rlwy.net:12345
   ```
5. Keep this handy for Step 4

---

### STEP 3: Deploy Backend Service

1. Click **"+ New"** → **"GitHub Repo"** (or Empty Service if uploading manually)
2. Select your repository (or upload `backend/` folder)
3. Railway will auto-detect it's a Python project
4. Go to **Settings** tab and set:
   - **Root Directory:** `backend` (if deploying whole repo)
   - **Start Command:** `uvicorn server:app --host 0.0.0.0 --port $PORT`

5. Go to **Variables** tab and add these environment variables:

---

### 🔑 BACKEND ENVIRONMENT VARIABLES (Railway Dashboard)

Add these in the **Variables** tab of your **backend service**:

```
MONGO_URL
mongodb://mongo:PASSWORD@monorail.proxy.rlwy.net:12345
(Use the connection string from Step 2)

DB_NAME
millenial_architects

GMAIL_USER
architectsmillennial@gmail.com

GMAIL_PASSWORD
<your_gmail_app_password>

BUSINESS_EMAIL
architectsmillennial@gmail.com

CORS_ORIGINS
*
(We'll update this after frontend is deployed)
```

**Important:** Replace the MongoDB URL with the actual one from your Railway MongoDB service!

6. Click **"Deploy"**
7. Wait for deployment to complete
8. Go to **Settings** → **Networking** → Click **"Generate Domain"**
9. **Copy your backend URL** (e.g., `https://millenial-architects-backend.up.railway.app`)

---

### STEP 4: Deploy Frontend Service

1. Click **"+ New"** → **"GitHub Repo"** again (or new empty service)
2. Select your repository
3. Railway will auto-detect it's a Node.js/React project
4. Go to **Settings** tab:
   - **Root Directory:** `frontend` (if deploying whole repo)
   - **Build Command:** `yarn build`
   - **Start Command:** `yarn start` (serves the production build)

5. Go to **Variables** tab and add:

---

### 🔑 FRONTEND ENVIRONMENT VARIABLES (Railway Dashboard)

Add these in the **Variables** tab of your **frontend service**:

```
REACT_APP_BACKEND_URL
https://millenial-architects-backend.up.railway.app
(Use the backend URL from Step 3)

NODE_ENV
production
```

6. Click **"Deploy"**
7. Wait for build to complete
8. Go to **Settings** → **Networking** → Click **"Generate Domain"**
9. **Copy your frontend URL** (e.g., `https://millenial-architects.up.railway.app`)

---

### STEP 5: Update CORS in Backend

1. Go back to your **Backend service**
2. Click **Variables** tab
3. Update `CORS_ORIGINS` to your frontend URL:
   ```
   CORS_ORIGINS=https://millenial-architects.up.railway.app
   ```
4. Backend will auto-redeploy with new settings

---

## Final Setup Summary

You should now have **3 services** in Railway:

| Service | Type | URL |
|---------|------|-----|
| MongoDB | Database | Internal only |
| Backend | FastAPI | `https://your-backend.up.railway.app` |
| Frontend | React | `https://your-frontend.up.railway.app` |

---

## Testing Your Deployment

1. Visit your frontend URL: `https://your-frontend.up.railway.app`
2. Submit a test quote form
3. Verify:
   - ✅ Form submits successfully
   - ✅ You receive email at architectsmillennial@gmail.com
   - ✅ Customer receives auto-reply (if email provided)
   - ✅ WhatsApp button works

---

## Cost on Railway

**Free Trial:** $5 credit (good for ~1 month of testing)

**After Trial:**
- **Starter Plan:** $5/month (500 hours execution time)
- **Developer Plan:** $20/month (unlimited)

**Estimated Usage:**
- MongoDB: ~$5/month
- Backend: ~$3/month
- Frontend: ~$2/month
- **Total: ~$10/month** for always-on services

---

## Adding Custom Domain (Optional)

1. Buy domain from Namecheap/GoDaddy (e.g., `millenialararchitects.com`)
2. In Railway frontend service:
   - Go to **Settings** → **Networking**
   - Click **"Custom Domain"**
   - Add your domain
   - Update DNS records as instructed (CNAME)
3. SSL certificate is automatic!

---

## Troubleshooting

### Backend not starting?
- Check **Deployments** tab for error logs
- Verify `MONGO_URL` is correct
- Ensure all environment variables are set

### Frontend can't reach backend?
- Check `REACT_APP_BACKEND_URL` in frontend variables
- Verify CORS is set correctly in backend
- Test backend directly: `https://your-backend.up.railway.app/api/`

### Email notifications not working?
- Verify `GMAIL_PASSWORD` is the App Password (not regular password)
- Check backend logs for email errors
- Test: `https://your-backend.up.railway.app/api/leads` (POST request)

### MongoDB connection failed?
- Copy the connection string from Railway MongoDB service
- Make sure it's in `MONGO_URL` variable
- Format: `mongodb://mongo:PASSWORD@host:port`

---

## Quick Reference: All Environment Variables

### Backend Service Variables:
```
MONGO_URL=<Railway MongoDB connection string>
DB_NAME=millenial_architects
GMAIL_USER=architectsmillennial@gmail.com
GMAIL_PASSWORD=<your_gmail_app_password>
BUSINESS_EMAIL=architectsmillennial@gmail.com
CORS_ORIGINS=<Your frontend Railway URL>
```

### Frontend Service Variables:
```
REACT_APP_BACKEND_URL=<Your backend Railway URL>
NODE_ENV=production
```

---

## Need Help?

Railway has excellent documentation:
- General: https://docs.railway.app
- MongoDB: https://docs.railway.app/databases/mongodb
- Environment Variables: https://docs.railway.app/develop/variables

Railway Discord community is also very helpful!

---

**You're all set! Follow these steps and your landing page will be live in ~15 minutes! 🚀**
