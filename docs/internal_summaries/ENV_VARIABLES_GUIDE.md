# 🔐 Environment Variables Guide

## What Each Variable Means

### **GEMINI_API_KEY** ⭐ (MOST IMPORTANT)
**What it is:** Your Google Gemini API key for AI/LLM features  
**Where to get it:** https://makersuite.google.com/app/apikey  
**Example:** `AIzaSyAbc123...`  
**Required:** YES (for RAG features)

---

### **SECRET_KEY**
**What it is:** General encryption key for the application  
**Used for:** Encrypting cookies, sessions, and sensitive data  
**For development:** `dev-secret-key-change-in-production` (current value is OK)  
**For production:** Generate with: `python3 -c "import secrets; print(secrets.token_urlsafe(32))"`  
**Required:** YES

---

### **JWT_SECRET** 
**What it is:** Secret key for JWT (JSON Web Token) authentication  
**Used for:** Creating and verifying login tokens (user authentication)  
**Think of it as:** A password your server uses to sign authentication tokens  
**For development:** `dev-jwt-secret-change-in-production` (current value is OK)  
**For production:** Generate with: `python3 -c "import secrets; print(secrets.token_urlsafe(32))"`  
**Required:** YES (if you implement user authentication)

**How JWT works:**
1. User logs in → Server creates a token signed with JWT_SECRET
2. User sends token with requests → Server verifies using JWT_SECRET
3. If token is valid → User is authenticated

---

### **DATABASE_URL**
**What it is:** Connection string for PostgreSQL database  
**Current value:** `postgresql://postgres:postgres@db:5432/cocus_mvp`  
**For Docker:** Use `@db:5432` (container name)  
**For local:** Use `@localhost:5432`  
**Required:** YES (if using database features)

---

### **LLM_PROVIDER**
**What it is:** Which AI provider to use  
**Options:** `gemini`, `openai`, or `mock`  
**Recommended:** `gemini` (free tier available)  
**Required:** YES

---

### **Other Variables**
- **REDIS_URL**: Cache server (for performance)
- **MLFLOW_TRACKING_URI**: ML experiment tracking
- **AWS_***: Only needed if using AWS S3 for storage
- **LOG_LEVEL**: How much logging (INFO, DEBUG, ERROR)

---

## 📝 Your Current Setup Checklist

### ✅ **For Development (Right Now):**

1. **MUST CHANGE:**
   - [ ] `GEMINI_API_KEY` → Your actual Gemini key

2. **OK to Keep as Default:**
   - [x] `SECRET_KEY=dev-secret-key-change-in-production`
   - [x] `JWT_SECRET=dev-jwt-secret-change-in-production`
   - [x] `DATABASE_URL=postgresql://postgres:postgres@db:5432/cocus_mvp`
   - [x] All other values

### ⚠️ **For Production (Later):**

1. **MUST CHANGE:**
   - [ ] `SECRET_KEY` → Generate strong random secret
   - [ ] `JWT_SECRET` → Generate strong random secret
   - [ ] `DATABASE_URL` → Use production database credentials

---

## 🎯 **What You Need to Do RIGHT NOW:**

### **Step 1: Open your `.env` file**
You already have it open! ✅

### **Step 2: Find line with GEMINI_API_KEY**
Look for:
```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

### **Step 3: Replace with your actual key**
Change to:
```bash
GEMINI_API_KEY=AIzaYourActualKeyFromGemini
```
(Paste the key you copied from https://makersuite.google.com/app/apikey)

### **Step 4: Leave everything else as is**
For development, the default values for `SECRET_KEY` and `JWT_SECRET` are fine!

### **Step 5: Save the file**
Press `Cmd + S` (Mac) or `Ctrl + S` (Windows)

---

## 🔒 **Security Notes**

### **Why JWT_SECRET matters:**
- If someone knows your JWT_SECRET, they can create fake login tokens
- For development: Default value is OK (you're testing locally)
- For production: MUST use a strong random secret

### **How to generate production secrets:**
```bash
# Generate SECRET_KEY
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
# Output: something like "xK7mP9nQ2wR5tY8uI1oP4aS6dF3gH0jK"

# Generate JWT_SECRET  
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
# Output: something like "vB4nM7cX9zL2kJ5hG8fD1aS3qW6eR0tY"
```

---

## ❓ **FAQ**

**Q: Do I need to change SECRET_KEY and JWT_SECRET now?**  
A: No! For development/testing, the default values are fine.

**Q: When do I need to change them?**  
A: When deploying to production or if you implement user authentication.

**Q: What if I forget to change them in production?**  
A: Security risk! Anyone with the default keys could compromise your app.

**Q: Can I use the same value for both SECRET_KEY and JWT_SECRET?**  
A: Not recommended. Use different secrets for different purposes.

**Q: What if I lose my JWT_SECRET?**  
A: All existing user sessions/tokens become invalid. Users need to log in again.

---

## ✅ **Summary: What to Do Now**

1. ✅ **Only change:** `GEMINI_API_KEY` (add your real key)
2. ✅ **Leave as is:** Everything else (including SECRET_KEY and JWT_SECRET)
3. ✅ **Save the file**
4. ✅ **Start the app**

The default security keys are **perfectly fine for development**!

---

## 🚀 **After You Add Your Gemini Key:**

Test if it works:
```bash
cd /Users/daouddaoud_1/Desktop/COCUS-MVP_ML_LLM_RAG_System
source venv/bin/activate
uvicorn src.api.main:app --reload
```

Then test the RAG endpoint:
```bash
curl -X POST "http://localhost:8000/api/rag/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Hello!"}'
```
