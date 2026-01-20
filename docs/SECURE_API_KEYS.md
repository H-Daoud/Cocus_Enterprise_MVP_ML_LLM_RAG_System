# 🔒 Secure API Key Management Guide

**Best practices for production deployment**

---

## 🎯 The Problem

**❌ NEVER do this:**
```bash
# Hardcoded in command (visible in process list!)
docker run -e OPENAI_API_KEY="sk-cocus-xxx" my-app

# Hardcoded in Dockerfile (committed to git!)
ENV OPENAI_API_KEY="sk-cocus-xxx"
```

**Why it's dangerous:**
- Visible in `docker ps` and process lists
- Stored in shell history
- Committed to git (if in Dockerfile)
- Accessible to anyone with server access

---

## ✅ Secure Solutions

### **Option 1: Environment File (Local/On-Premise)** ⭐ Recommended for Docker

#### **Step 1: Create secure .env file**
```bash
# Create .env file (NEVER commit to git!)
cat > .env << 'EOF'
OPENAI_API_KEY=sk-cocus-your-real-key-here
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_MODEL=gpt-3.5-turbo
EOF

# Set restrictive permissions (owner read-only)
chmod 600 .env

# Verify .env is in .gitignore
grep "^\.env$" .gitignore
```

#### **Step 2: Run Docker with --env-file**
```bash
# Secure: Load from file
docker run --env-file .env -p 8000:8000 my-app

# Or with Docker Compose (even better)
docker-compose up -d
```

**docker-compose.yml:**
```yaml
services:
  mvp-rag:
    image: my-app
    env_file:
      - .env  # Loads all variables from .env
    ports:
      - "8000:8000"
```

**Security:**
- ✅ Not visible in process list
- ✅ Not in shell history
- ✅ File permissions protect it
- ✅ .gitignore prevents commits

---

### **Option 2: GCP Secret Manager** ⭐ Recommended for GCP Cloud Run

#### **Step 1: Store secret in GCP**
```bash
# Create secret
echo -n "sk-cocus-your-real-key" | \
  gcloud secrets create openai-api-key \
  --data-file=- \
  --replication-policy="automatic"

# Verify
gcloud secrets versions access latest --secret="openai-api-key"
```

#### **Step 2: Deploy with secret reference**
```bash
# Cloud Run automatically injects secret as env var
gcloud run deploy mvp-rag \
  --source . \
  --set-secrets OPENAI_API_KEY=openai-api-key:latest
```

**Security:**
- ✅ Encrypted at rest
- ✅ Encrypted in transit
- ✅ Access control (IAM)
- ✅ Audit logging
- ✅ Automatic rotation support

---

### **Option 3: Kubernetes Secrets** (For GKE)

#### **Step 1: Create Kubernetes secret**
```bash
# Create secret
kubectl create secret generic api-keys \
  --from-literal=OPENAI_API_KEY=sk-cocus-your-real-key

# Verify (base64 encoded)
kubectl get secret api-keys -o yaml
```

#### **Step 2: Reference in deployment**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mvp-rag
spec:
  template:
    spec:
      containers:
      - name: app
        image: my-app
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: OPENAI_API_KEY
```

**Security:**
- ✅ Encrypted in etcd
- ✅ RBAC access control
- ✅ Not visible in pod spec
- ✅ Can be rotated

---

### **Option 4: HashiCorp Vault** (Enterprise)

```bash
# Store in Vault
vault kv put secret/api-keys OPENAI_API_KEY=sk-cocus-xxx

# Retrieve in application
vault kv get -field=OPENAI_API_KEY secret/api-keys
```

---

## 🏢 Production Setup Guide

### **For On-Premise (Docker Compose)**

#### **1. Create secure directory**
```bash
# Create secrets directory (outside git repo)
sudo mkdir -p /opt/secrets/mvp-rag
sudo chmod 700 /opt/secrets/mvp-rag

# Create .env file
sudo cat > /opt/secrets/mvp-rag/.env << 'EOF'
OPENAI_API_KEY=sk-cocus-your-real-key
OPENAI_API_BASE=https://api.openai.com/v1
EOF

# Restrict permissions
sudo chmod 600 /opt/secrets/mvp-rag/.env
sudo chown root:root /opt/secrets/mvp-rag/.env
```

#### **2. Update docker-compose.yml**
```yaml
services:
  mvp-rag:
    image: my-app
    env_file:
      - /opt/secrets/mvp-rag/.env  # Absolute path
    ports:
      - "8000:8000"
```

#### **3. Run with restricted access**
```bash
# Only root can read secrets
sudo docker-compose up -d
```

---

### **For GCP Cloud Run**

#### **1. Store secret**
```bash
# One-time setup
echo -n "sk-cocus-your-real-key" | \
  gcloud secrets create openai-api-key --data-file=-
```

#### **2. Deploy**
```bash
# Secret automatically injected
gcloud run deploy mvp-rag \
  --source . \
  --set-secrets OPENAI_API_KEY=openai-api-key:latest
```

#### **3. Rotate secret (when needed)**
```bash
# Add new version
echo -n "sk-cocus-new-key" | \
  gcloud secrets versions add openai-api-key --data-file=-

# Cloud Run automatically uses latest
```

---

## 🔒 Security Best Practices

### **1. File Permissions**
```bash
# .env file should be 600 (owner read/write only)
chmod 600 .env

# Verify
ls -la .env
# Output: -rw------- 1 user user 123 Jan 20 09:00 .env
```

### **2. .gitignore**
```gitignore
# CRITICAL: Never commit secrets!
.env
.env.*
*.key
*.pem
secrets/
```

### **3. Separate Secrets from Code**
```
# Good structure
/opt/
  ├── app/              # Application code (git repo)
  └── secrets/          # Secrets (NOT in git)
      └── mvp-rag/
          └── .env
```

### **4. Use Secret Scanning**
```bash
# Install git-secrets
brew install git-secrets

# Prevent commits with secrets
git secrets --install
git secrets --register-aws
```

---

## 📊 Security Comparison

| Method | Security | Ease | Rotation | Cost | Best For |
|--------|----------|------|----------|------|----------|
| **Environment File** | Medium | Easy | Manual | Free | Development, On-Premise |
| **GCP Secret Manager** | High | Easy | Easy | ~$0.06/month | GCP Cloud Run |
| **Kubernetes Secrets** | High | Medium | Medium | Free | GKE |
| **HashiCorp Vault** | Very High | Hard | Easy | $$$ | Enterprise |

---

## 🎯 Recommended Approach

### **For Your MVP:**

#### **Development/Testing:**
```bash
# Use .env file
cp .env.template .env
# Edit .env
docker-compose up -d
```

#### **Production (GCP):**
```bash
# Use Secret Manager
gcloud secrets create openai-api-key --data-file=-
gcloud run deploy mvp-rag --set-secrets OPENAI_API_KEY=openai-api-key:latest
```

#### **Production (On-Premise):**
```bash
# Secure .env file
sudo mkdir -p /opt/secrets/mvp-rag
sudo nano /opt/secrets/mvp-rag/.env
sudo chmod 600 /opt/secrets/mvp-rag/.env

# docker-compose.yml
env_file:
  - /opt/secrets/mvp-rag/.env
```

---

## 🚨 Common Mistakes to Avoid

### **❌ Don't:**
```bash
# 1. Hardcode in Dockerfile
ENV OPENAI_API_KEY="sk-xxx"  # NEVER!

# 2. Pass on command line
docker run -e OPENAI_API_KEY="sk-xxx"  # Visible in ps!

# 3. Commit .env to git
git add .env  # NEVER!

# 4. Use world-readable permissions
chmod 644 .env  # Too permissive!

# 5. Store in application code
api_key = "sk-xxx"  # NEVER!
```

### **✅ Do:**
```bash
# 1. Use .env file with --env-file
docker run --env-file .env my-app

# 2. Use Secret Manager (GCP)
gcloud run deploy --set-secrets KEY=secret:latest

# 3. Restrict permissions
chmod 600 .env

# 4. Keep .env in .gitignore
echo ".env" >> .gitignore

# 5. Load from environment
api_key = os.getenv("OPENAI_API_KEY")
```

---

## 📝 Quick Reference

### **Docker Run:**
```bash
# Secure
docker run --env-file .env -p 8000:8000 my-app

# Or with specific file
docker run --env-file /opt/secrets/.env my-app
```

### **Docker Compose:**
```yaml
services:
  app:
    env_file: .env  # or /opt/secrets/.env
```

### **GCP Cloud Run:**
```bash
# Store secret
gcloud secrets create openai-api-key --data-file=-

# Deploy
gcloud run deploy mvp-rag \
  --set-secrets OPENAI_API_KEY=openai-api-key:latest
```

---

## ✅ Your Setup

**For your MVP, use this:**

### **1. Create .env file (if not exists)**
```bash
cp .env.template .env
nano .env  # Add your real API key
chmod 600 .env
```

### **2. Run with Docker Compose**
```bash
docker-compose up -d
```

**docker-compose.yml already configured:**
```yaml
services:
  mvp-rag:
    env_file:
      - .env  # ✅ Secure!
```

---

**🔒 Your secrets are now secure!**
