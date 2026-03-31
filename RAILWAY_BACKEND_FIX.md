# Railway Backend Deployment - Fixed Files

## ✅ Fixed Issues

1. **Removed unnecessary packages** (pandas, numpy, boto3, testing tools)
2. **Updated to latest compatible versions** of all packages
3. **Added Python version specification** (Python 3.11)
4. **Fixed motor/pymongo conflict** (motor includes pymongo)
5. **Added multiple deployment configs** (railway.toml, Procfile, runtime.txt)

---

## 📦 Updated Files for Railway

### 1. requirements.txt (MINIMAL & CLEAN)
```
# Core Framework
fastapi==0.115.0
uvicorn[standard]==0.32.1
python-dotenv==1.0.1

# Database (motor includes pymongo)
motor==3.6.0

# Email & File Upload
python-multipart==0.0.20

# Validation
pydantic==2.10.3
pydantic-settings==2.7.0
email-validator==2.2.0
```

### 2. runtime.txt (NEW - Python Version)
```
python-3.11.9
```

### 3. Procfile (NEW - Deployment Command)
```
web: uvicorn server:app --host 0.0.0.0 --port $PORT
```

### 4. railway.toml (UPDATED)
```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "uvicorn server:app --host 0.0.0.0 --port $PORT"
restartPolicyType = "ON_FAILURE"

[build.env]
PYTHON_VERSION = "3.11"
```

---

## 🚀 Railway Deployment Settings

### Root Directory
If deploying whole repo: Set to `backend`

### Build Command (Auto-detected)
```bash
pip install -r requirements.txt
```

### Start Command
```bash
uvicorn server:app --host 0.0.0.0 --port $PORT
```

### Environment Variables (Required)
```
MONGO_URL=<Railway MongoDB connection string>
DB_NAME=millenial_architects
GMAIL_USER=architectsmillennial@gmail.com
GMAIL_PASSWORD=tlurzumbflbqhmnd
BUSINESS_EMAIL=architectsmillennial@gmail.com
CORS_ORIGINS=*
```

---

## 🔧 Troubleshooting Railway Errors

### Error: "pip install failed"
**Solution:** Make sure you're using the updated requirements.txt (minimal packages only)

### Error: "Python version mismatch"
**Solution:** Railway should auto-detect Python 3.11 from runtime.txt

### Error: "Module not found: motor"
**Solution:** Check Railway build logs - motor should install automatically

### Error: "Port binding failed"
**Solution:** Make sure start command uses `--port $PORT` (not hardcoded 8001)

### Error: "Application startup failed"
**Solution:** 
1. Check Environment Variables are set
2. Verify MONGO_URL is correct
3. Check Railway logs for specific error

---

## ✅ Verification Steps After Deployment

1. **Check Build Logs:**
   - Go to Railway → Backend Service → Deployments
   - Click latest deployment
   - Check "Build Logs" - should show successful pip install

2. **Check Deploy Logs:**
   - Look for "Application startup complete"
   - Should see Uvicorn running message

3. **Test API:**
   ```bash
   curl https://your-backend.up.railway.app/api/
   ```
   Should return: `{"message": "Hello from Millenial Architects API"}`

4. **Test Lead Creation:**
   ```bash
   curl -X POST https://your-backend.up.railway.app/api/leads \
     -H "Content-Type: application/json" \
     -d '{"name":"Test","phone":"9999999999","area":"Mumbai","service":"Kitchen","budget":"₹3-7L"}'
   ```

---

## 📋 Common Railway Deployment Patterns

### Pattern 1: Deploy from GitHub
1. Push code to GitHub
2. Connect Railway to repo
3. Railway auto-deploys on push

### Pattern 2: Manual Upload
1. Zip backend folder
2. Upload to Railway
3. Manual redeploy when needed

### Pattern 3: Railway CLI
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and link project
railway login
railway link

# Deploy
cd backend
railway up
```

---

## 🆘 Still Having Issues?

1. **Check Python Version:**
   - Railway logs should show "Using Python 3.11.x"
   - If not, add `PYTHON_VERSION=3.11` in environment variables

2. **Check Package Installation:**
   - Look for "Successfully installed fastapi" in build logs
   - Each package should install without errors

3. **MongoDB Connection:**
   - Verify MongoDB service is running in Railway
   - Copy connection string from MongoDB service variables
   - Format: `mongodb://mongo:PASSWORD@host:port`

4. **Railway Support:**
   - Check Railway Discord: https://discord.gg/railway
   - Railway Docs: https://docs.railway.app

---

## 📦 All Files Ready in Updated Package

Download the updated source code with all fixes:
https://interior-quote-hub.preview.emergentagent.com/millenial-architects-source.zip

**Updated files included:**
✅ `backend/requirements.txt` - Clean, minimal dependencies
✅ `backend/runtime.txt` - Python version specification
✅ `backend/Procfile` - Start command
✅ `backend/railway.toml` - Railway configuration
✅ This troubleshooting guide

---

**Your backend should now deploy successfully on Railway! 🚀**
