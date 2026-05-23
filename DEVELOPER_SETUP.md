# 🚀 VulnRisk Developer Setup Guide

## 📋 **Quick Start (5 minutes)**

### **Prerequisites**
- Docker & Docker Compose
- Python 3.13+ and [uv](https://docs.astral.sh/uv/) (for local backend development)
- Git

### **1. Clone & Setup**
```bash
git clone https://github.com/yourusername/vulnrisk.git
cd VulnRisk
```

### **2. One-Command Launch**
```bash
# This sets up everything with development features enabled
python scripts/deploy_with_feature_flags.py --environment development
```

**Enhanced Setup Features:**
- 🚀 **Optimized Lambda Configuration** - 512MB memory, 60s timeout
- 📊 **Enhanced Error Handling** - Dead letter queue for debugging
- 🔗 **Direct Testing Endpoint** - Lambda Function URL for bypass testing
- 📈 **Production-Like Environment** - Mirrors production serverless setup

### **3. Access Your Local Environment**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 🔧 **What Happens During Setup**

### **Feature Isolation System**
The setup script automatically configures your local environment with **all features enabled** for development:

| Feature | Local Development | Status |
|---------|------------------|---------|
| **FedRAMP Compliance** | ✅ Enabled | Full access for testing |
| **AI Risk Prediction** | ✅ Enabled | ML models available |
| **Customer API Keys** | ✅ Enabled | API key management |
| **Scanner Integrations** | ✅ Enabled | Multi-scanner support |
| **Debug Endpoints** | ✅ Enabled | Development tools |

### **Environment Configuration**
The script creates/updates:
- `backend/.env` - Backend configuration
- `frontend/.env` - Frontend configuration
- `docker-compose.yml` - Local services

---

## 🎯 **Feature Isolation in Action**

### **How It Works**
Based on `FEATURE_ISOLATION_SUMMARY.md`, the system uses:

1. **Environment Detection**: Automatically detects you're in "development"
2. **Feature Flags**: Enables all features for local development
3. **Protected Endpoints**: Some endpoints require authentication
4. **Graceful Degradation**: Disabled features show appropriate messages

### **Development vs Production**
```bash
# Development (what you get locally)
ENABLE_FEDRAMP_COMPLIANCE=true
ENABLE_AI_RISK_PREDICTION=true
ENABLE_DEBUG_ENDPOINTS=true

# Production (what users get)
ENABLE_FEDRAMP_COMPLIANCE=false
ENABLE_AI_RISK_PREDICTION=false
ENABLE_DEBUG_ENDPOINTS=false
```

---

## 🛠 **Manual Setup (Alternative)**

If you prefer manual setup:

### **1. Backend Setup**
```bash
cd backend
uv sync --all-groups
cp .env.example .env
# Edit .env with your settings
make dev
# Or: uv run uvicorn src.vulnrisk.api.main:app --reload --host 0.0.0.0 --port 8000
```

Optional extras:
```bash
uv sync --extra aws    # Lambda / DynamoDB (boto3)
uv sync --extra nlp    # spaCy / transformers NLP features
```

### **2. Frontend Setup**
```bash
cd frontend
npm install
cp .env.example .env
# Edit .env with your settings
npm run dev
```

### **3. Database Setup**
```bash
# SQLite (default for development)
# No setup needed - auto-created

# PostgreSQL (optional)
docker run -d --name vulnrisk-db \
  -e POSTGRES_DB=vulnrisk \
  -e POSTGRES_USER=vulnrisk \
  -e POSTGRES_PASSWORD=password \
  -p 5432:5432 postgres:13
```

---

## 🔐 **Authentication Setup (Optional)**

### **For Full Feature Testing**
1. **Auth0 Setup** (see `AUTH0_SETUP_GUIDE.md`)
2. **Update `.env` files** with your Auth0 credentials
3. **Test authentication** on protected endpoints

### **For Basic Development**
- Most features work without authentication
- Some advanced features require login
- Debug endpoints available for testing

---

## 📊 **Testing Your Setup**

### **1. Health Check**
```bash
curl http://localhost:8000/health
# Should return: {"status": "healthy"}
```

### **2. Feature Flags**
```bash
curl http://localhost:8000/api/v1/config/features
# Should show all features enabled
```

### **3. Frontend**
- Open http://localhost:3000
- Navigate through different pages
- Test file upload and risk calculation

### **4. API Documentation**
- Open http://localhost:8000/docs
- Test endpoints directly
- View available features

---

## 🐛 **Troubleshooting**

### **Common Issues**

#### **Port Already in Use**

`./setup.sh` automatically selects the next available port when defaults (8000, 3000, 5432) are taken and saves the choice in `.env`.

To set ports manually, copy `.env.example` to `.env` and edit:

```bash
BACKEND_HOST_PORT=8001
FRONTEND_HOST_PORT=3001
DB_HOST_PORT=5433
VITE_API_BASE_URL=http://localhost:8001
```

Then run `./setup.sh` or `docker compose up -d`.

To free a port manually:

```bash
# Kill existing processes
lsof -ti:8000 | xargs kill -9
lsof -ti:3000 | xargs kill -9
```

#### **Docker Issues**
```bash
# Clean up Docker
docker-compose down -v
docker system prune -f
```

#### **Permission Issues**
```bash
# Fix file permissions
chmod +x scripts/deploy_with_feature_flags.py
```

#### **Database Issues**
```bash
# Reset database
rm backend/vulnrisk.db  # SQLite
# Or for PostgreSQL:
docker-compose down -v
docker-compose up -d
```

### **Feature-Specific Issues**

#### **FedRAMP Features Not Working**
- Check `ENABLE_FEDRAMP_COMPLIANCE=true` in `.env`
- Verify Auth0 setup for authentication
- Check logs: `docker-compose logs backend`

#### **AI Features Not Working**
- Check `ENABLE_AI_RISK_PREDICTION=true` in `.env`
- Verify ML models are downloaded
- Check memory usage (AI models need ~2GB RAM)

#### **API Key Management Issues**
- Check `API_KEY_ENCRYPTION_KEY` in `.env`
- Verify encryption key is properly set
- Check database connection

---

## 🔄 **Development Workflow**

### **1. Making Changes**
```bash
# Edit code
# Test locally
# Commit changes
git add .
git commit -m "feat: your feature description"
```

### **2. Testing Features**
```bash
# Test specific features
python backend/test_feature_isolation.py

# Test API endpoints
curl http://localhost:8000/api/v1/vulnerabilities
```

### **3. Switching Environments**
```bash
# Deploy to staging (enhanced serverless)
python scripts/deploy_with_feature_flags.py --environment staging

# Deploy to production (enhanced serverless)
python scripts/deploy_with_feature_flags.py --environment production

# Switch back to development
python scripts/deploy_with_feature_flags.py --environment development
```

**Deployment Enhancements:**
- ✅ **Enhanced Lambda Performance** - 4x memory increase (128MB → 512MB)
- ✅ **Better Timeout Handling** - 2x timeout increase (30s → 60s)
- ✅ **Error Tracking** - SQS dead letter queue for failed requests
- ✅ **Direct Testing** - Lambda Function URL for API Gateway bypass
- ✅ **Production Monitoring** - CloudWatch logs with detailed debugging

---

## 📚 **Key Files to Know**

### **Configuration**
- `scripts/deploy_with_feature_flags.py` - Main setup script
- `backend/src/vulnrisk/config/feature_flags.py` - Feature definitions
- `backend/.env` - Backend environment variables
- `frontend/.env` - Frontend environment variables

### **Documentation**
- `FEATURE_ISOLATION_SUMMARY.md` - Feature isolation system
- `DEVELOPER_QUICK_REFERENCE.md` - Feature isolation quick reference
- `AUTH0_SETUP_GUIDE.md` - Authentication setup
- `README.md` - Project overview

### **Testing**
- `backend/test_feature_isolation.py` - Feature isolation tests
- `test_deployed_app.py` - Integration tests

---

## 🎯 **Next Steps**

### **For New Developers**
1. ✅ Complete the quick start above
2. 🔍 Explore the API documentation
3. 🧪 Run the test suite
4. 📖 Read the feature isolation documentation

### **For Feature Development**
1. 🔧 Set up your development environment
2. 🎯 Enable specific features you're working on
3. 🧪 Write tests for your features
4. 📝 Document your changes

### **For Production Deployment**
1. 🚀 Use staging environment for testing
2. 🔒 Verify security configurations
3. 📊 Run performance tests
4. 🎯 Deploy to production

---

## 🆘 **Getting Help**

### **Documentation**
- Check `FEATURE_ISOLATION_SUMMARY.md` for feature details
- Review `DEVELOPER_QUICK_REFERENCE.md` for feature isolation
- Review `AUTH0_SETUP_GUIDE.md` for authentication
- See `README.md` for project overview

### **Debugging**
- Check Docker logs: `docker-compose logs`
- Test endpoints: `curl http://localhost:8000/health`
- Verify features: `curl http://localhost:8000/api/v1/config/features`

### **Common Commands**
```bash
# Restart everything
python scripts/deploy_with_feature_flags.py development

# Check status
docker-compose ps

# View logs
docker-compose logs -f backend

# Reset database
docker-compose down -v && docker-compose up -d
```

---

## 🎉 **You're Ready!**

Your local VulnRisk environment is now set up with:
- ✅ All development features enabled
- ✅ Feature isolation system active
- ✅ Local database and services running
- ✅ Frontend and backend accessible
- ✅ API documentation available

**Happy coding!** 🚀 