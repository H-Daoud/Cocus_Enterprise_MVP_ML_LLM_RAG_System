# 🔒 Server Secret Setup - Step by Step

**When to save secrets on your server**

---

## 📅 **Timeline: When to Save Secrets**

### **Option 1: During Initial Server Setup** ⭐ (Recommended)

**When**: Before deploying your application for the first time

**Steps**:
```bash
# 1. SSH into your server
ssh user@your-server.com

# 2. Run the setup script
cd /path/to/COCUS-MVP_ML_LLM_RAG_System
sudo bash scripts/setup_server_secrets.sh

# 3. Edit the secrets file
sudo nano /opt/secrets/mvp-rag/.env

# 4. Add your real API key
OPENAI_API_KEY=sk-cocus-your-real-key-here

# 5. Save and exit (Ctrl+X, Y, Enter)

# 6. Verify permissions
ls -la /opt/secrets/mvp-rag/.env
# Should show: -rw------- 1 root root

# 7. Deploy application
sudo docker-compose up -d
```

---

### **Option 2: Manual Setup** (Alternative)

**When**: If you prefer manual control

```bash
# 1. SSH into server
ssh user@your-server.com

# 2. Create directory
sudo mkdir -p /opt/secrets/mvp-rag
sudo chmod 700 /opt/secrets/mvp-rag

# 3. Create and edit .env file
sudo nano /opt/secrets/mvp-rag/.env
```

**Add this content**:
```bash
OPENAI_API_KEY=sk-cocus-your-actual-key-here
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_MODEL=gpt-3.5-turbo
PORT=8000
HOST=0.0.0.0
LOG_LEVEL=INFO
```

```bash
# 4. Secure the file
sudo chmod 600 /opt/secrets/mvp-rag/.env
sudo chown root:root /opt/secrets/mvp-rag/.env

# 5. Deploy
cd /path/to/your/app
sudo docker-compose up -d
```

---

## 🎯 **Complete Deployment Workflow**

### **First Time Deployment:**

```bash
# ============================================================================
# STEP 1: Prepare on your laptop (Development)
# ============================================================================
# Clone/copy your project to server
scp -r COCUS-MVP_ML_LLM_RAG_System user@server:/opt/apps/

# ============================================================================
# STEP 2: SSH into your server
# ============================================================================
ssh user@your-server.com

# ============================================================================
# STEP 3: Setup secrets (ONE TIME ONLY)
# ============================================================================
cd /opt/apps/COCUS-MVP_ML_LLM_RAG_System

# Run setup script
sudo bash scripts/setup_server_secrets.sh

# Edit secrets
sudo nano /opt/secrets/mvp-rag/.env
# Add: OPENAI_API_KEY=sk-cocus-your-real-key

# Save and exit

# ============================================================================
# STEP 4: Deploy application
# ============================================================================
sudo docker-compose up -d

# ============================================================================
# STEP 5: Verify
# ============================================================================
# Check if running
sudo docker-compose ps

# Check logs
sudo docker-compose logs -f

# Test API
curl http://localhost:8000/health
```

---

## 📁 **File Locations**

### **On Your Laptop (Development):**
```
COCUS-MVP_ML_LLM_RAG_System/
├── .env.template              ← Template (commit to git)
├── .env                       ← Local dev (in .gitignore)
└── scripts/
    └── setup_server_secrets.sh ← Setup script
```

### **On Your Server (Production):**
```
/opt/
├── apps/
│   └── COCUS-MVP_ML_LLM_RAG_System/  ← Your application
│       ├── docker-compose.yml
│       └── ... (all code)
│
└── secrets/                    ← Secrets directory
    └── mvp-rag/
        └── .env                ← API keys (NEVER in git!)
```

---

## 🔄 **When to Update Secrets**

### **Scenario 1: API Key Rotation**
```bash
# SSH into server
ssh user@server

# Edit secrets
sudo nano /opt/secrets/mvp-rag/.env

# Update OPENAI_API_KEY=new-key-here

# Restart application
cd /opt/apps/COCUS-MVP_ML_LLM_RAG_System
sudo docker-compose restart
```

### **Scenario 2: Add New Secret**
```bash
# Edit secrets
sudo nano /opt/secrets/mvp-rag/.env

# Add new variable
NEW_API_KEY=some-value

# Restart
sudo docker-compose restart
```

---

## ✅ **Verification Checklist**

After saving secrets, verify:

```bash
# 1. File exists
ls -la /opt/secrets/mvp-rag/.env

# 2. Correct permissions (-rw-------)
# Should show: -rw------- 1 root root

# 3. Correct owner (root)
stat /opt/secrets/mvp-rag/.env

# 4. Docker can read it
sudo docker-compose config
# Should show environment variables loaded

# 5. Application works
curl http://localhost:8000/health
```

---

## 🚨 **Important Notes**

### **DO:**
- ✅ Save secrets in `/opt/secrets/` (outside project)
- ✅ Set permissions to `600` (owner read-only)
- ✅ Set owner to `root:root`
- ✅ Use `sudo` to edit secrets
- ✅ Restart Docker after changes

### **DON'T:**
- ❌ Save secrets in project folder
- ❌ Commit `.env` to git
- ❌ Use world-readable permissions
- ❌ Share secrets in chat/email
- ❌ Hardcode in Dockerfile

---

## 📊 **Quick Reference**

| Action | Command |
|--------|---------|
| **Create secrets** | `sudo bash scripts/setup_server_secrets.sh` |
| **Edit secrets** | `sudo nano /opt/secrets/mvp-rag/.env` |
| **View secrets** | `sudo cat /opt/secrets/mvp-rag/.env` |
| **Check permissions** | `ls -la /opt/secrets/mvp-rag/.env` |
| **Deploy app** | `sudo docker-compose up -d` |
| **Restart app** | `sudo docker-compose restart` |

---

## 🎯 **Your Next Steps**

### **Right Now (On Your Laptop):**
```bash
# Nothing to do! 
# Secrets will be saved on the server, not locally
```

### **When You Deploy (On Your Server):**
```bash
# 1. Copy project to server
scp -r COCUS-MVP_ML_LLM_RAG_System user@server:/opt/apps/

# 2. SSH into server
ssh user@server

# 3. Setup secrets (one time)
cd /opt/apps/COCUS-MVP_ML_LLM_RAG_System
sudo bash scripts/setup_server_secrets.sh
sudo nano /opt/secrets/mvp-rag/.env
# Add your API key

# 4. Deploy
sudo docker-compose up -d
```

---

**🔒 Your secrets will be saved on the server in `/opt/secrets/mvp-rag/.env`**

**Not in your project folder, not in git, completely secure!**
