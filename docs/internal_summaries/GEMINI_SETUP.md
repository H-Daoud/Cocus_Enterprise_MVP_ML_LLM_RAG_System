# 🤖 Using Google Gemini API - Quick Setup Guide

## ✅ **Good News: Gemini is FREE and Easy to Use!**

Google Gemini offers a **generous free tier** - perfect for testing and development!

---

## 🚀 **Quick Setup (3 Steps)**

### **Step 1: Get Your FREE Gemini API Key**

1. **Visit Google AI Studio:**
   ```
   https://makersuite.google.com/app/apikey
   ```
   Or: https://aistudio.google.com/app/apikey

2. **Sign in** with your Google account

3. **Click "Get API Key"** or "Create API Key"

4. **Copy the key** (starts with `AIza...`)

---

### **Step 2: Configure Your Environment**

```bash
# 1. Copy the example environment file
cp .env.example .env

# 2. Edit .env file
nano .env
# OR
code .env  # if using VS Code
```

**Add your Gemini API key:**
```bash
# LLM Provider Configuration
LLM_PROVIDER=gemini

# Google Gemini API Key (FREE!)
GEMINI_API_KEY=AIzaYourActualKeyHere
GEMINI_MODEL=gemini-pro

# LLM Settings
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=1000
```

---

### **Step 3: Install Dependencies and Run**

```bash
# Install/update dependencies
source venv/bin/activate
pip install -r requirements.txt

# Start the API
uvicorn src.api.main:app --reload

# OR use Docker
docker-compose up -d
```

---

## 🧪 **Test Your Setup**

### **Test 1: Health Check**
```bash
curl http://localhost:8000/api/health
```

### **Test 2: RAG Query with Gemini**
```bash
curl -X POST "http://localhost:8000/api/rag/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is machine learning?",
    "max_results": 5,
    "include_sources": true
  }'
```

**Expected Response:**
```json
{
  "query": "What is machine learning?",
  "answer": "Machine learning is a subset of artificial intelligence...",
  "sources": [...],
  "confidence": 0.85
}
```

---

## 🔄 **Switching Between Providers**

The system supports **3 LLM providers**:

### **1. Google Gemini (Default - FREE)**
```bash
# .env
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_key_here
```

### **2. OpenAI (Alternative)**
```bash
# .env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-3.5-turbo
```

### **3. Mock (Testing without API)**
```bash
# .env
LLM_PROVIDER=mock
# No API key needed - returns mock responses
```

---

## 📊 **Gemini API Free Tier Limits**

✅ **Free Tier Includes:**
- **60 requests per minute**
- **1,500 requests per day**
- **1 million tokens per month**

**Perfect for:**
- Development
- Testing
- Small-scale applications
- MVP demos

---

## 🎯 **Supported Models**

### **Gemini Pro** (Default - Recommended)
```bash
GEMINI_MODEL=gemini-pro
```
- Best for text generation
- Fast and efficient
- FREE tier available

### **Gemini Pro Vision** (For images)
```bash
GEMINI_MODEL=gemini-pro-vision
```
- Supports image inputs
- Multimodal capabilities

---

## 🔍 **Verify Your Configuration**

```bash
# Check which provider is active
python -c "
from src.utils.llm_config import LLMConfig
from dotenv import load_dotenv
load_dotenv()

config = LLMConfig.from_env()
print(f'Provider: {config.provider.value}')
print(f'Model: {config.model}')
print(f'API Key: {config.api_key[:10]}...' if config.api_key else 'No API key')
"
```

---

## 🆚 **Gemini vs OpenAI Comparison**

| Feature | Gemini (Free) | OpenAI (Paid) |
|---------|---------------|---------------|
| **Cost** | ✅ FREE | ❌ Pay-per-use |
| **Free Tier** | ✅ 1M tokens/month | ❌ No free tier |
| **Speed** | ✅ Fast | ✅ Fast |
| **Quality** | ✅ Excellent | ✅ Excellent |
| **Setup** | ✅ Easy | ✅ Easy |
| **Best For** | Development, Testing | Production |

**Recommendation:** Start with Gemini (free), switch to OpenAI if needed for production.

---

## 🐛 **Troubleshooting**

### **Issue: "API key not valid"**

**Solution:**
```bash
# 1. Check your .env file
cat .env | grep GEMINI_API_KEY

# 2. Verify the key format (should start with AIza)
# 3. Make sure .env is in the project root
# 4. Restart the server after changing .env
```

### **Issue: "Module not found: langchain_google_genai"**

**Solution:**
```bash
# Install/update dependencies
pip install -r requirements.txt

# Or install directly
pip install langchain-google-genai google-generativeai
```

### **Issue: "Rate limit exceeded"**

**Solution:**
- Free tier: 60 requests/minute
- Wait a minute and try again
- Or upgrade to paid tier

---

## 📚 **Additional Resources**

- **Gemini API Docs:** https://ai.google.dev/docs
- **Get API Key:** https://makersuite.google.com/app/apikey
- **Pricing:** https://ai.google.dev/pricing
- **Models:** https://ai.google.dev/models/gemini

---

## ✅ **Quick Start Checklist**

- [ ] Get Gemini API key from https://makersuite.google.com/app/apikey
- [ ] Copy `.env.example` to `.env`
- [ ] Add `GEMINI_API_KEY=your_key` to `.env`
- [ ] Set `LLM_PROVIDER=gemini` in `.env`
- [ ] Run `pip install -r requirements.txt`
- [ ] Start API: `uvicorn src.api.main:app --reload`
- [ ] Test: `curl http://localhost:8000/api/rag/query -X POST -H "Content-Type: application/json" -d '{"query":"test"}'`

---

**🎉 You're all set to use Google Gemini for FREE!**

No credit card required, no payment needed - just sign in with your Google account and start building!
