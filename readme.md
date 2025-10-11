# 🛡️ VulnRisk - Open Source Vulnerability Risk Assessment Platform

[![Open Source](https://img.shields.io/badge/Open%20Source-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

> **Stop chasing CVSS scores. Start managing real risk.**

VulnRisk is an open-source vulnerability risk assessment platform that provides transparent, context-aware risk scoring beyond basic CVSS. Perfect for local development and testing.

## 🚀 **Quick Start (5 minutes)**

```bash
# Clone the repository
git clone https://github.com/GurkhaShieldForce/vulnrisk-public.git
cd vulnrisk

# Run the setup script
./setup.sh
```

**What You Get:**
- ✅ **Frontend**: http://localhost:3000
- ✅ **Backend API**: http://localhost:8000  
- ✅ **API Docs**: http://localhost:8000/docs
- ✅ **Database**: PostgreSQL on localhost:5432

## 🎯 **Why VulnRisk?**

| Problem | Solution |
|---------|----------|
| **10,000+ vulnerability alerts** | **90% noise reduction** through context-aware scoring |
| **CVSS scores don't reflect real risk** | **Transparent risk scoring** with complete calculation breakdown |
| **Expensive enterprise tools** | **Open source** with zero cost |
| **Black-box AI scoring** | **100% transparent** methodology |

## 🏗️ **Local Development Architecture**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   Database      │
│   (React/TS)    │◄──►│   (FastAPI)     │◄──►│   (PostgreSQL)  │
│   Port: 3000    │    │   Port: 8000    │    │   Port: 5432    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🔒 **Security Features**

- **Input Validation**: SQL injection, XSS protection
- **Security Headers**: CSP, HSTS, X-Frame-Options
- **Rate Limiting**: Request throttling
- **Audit Logging**: Comprehensive activity tracking

## 📊 **Key Features**

### **Core Risk Assessment**
- ✅ Vulnerability scanning and analysis
- ✅ Risk scoring with AI/ML models
- ✅ Exportable reports (PDF/Excel)

### **AI/ML Analytics**
- ✅ Risk prediction models
- ✅ Anomaly detection
- ✅ Trend analysis
- ✅ Intelligent recommendations

## 🛠️ **Development Setup**

### **Prerequisites**
- Docker & Docker Compose
- Git

### **Local Development**
```bash
# Clone and setup
git clone https://github.com/GurkhaShieldForce/vulnrisk-public.git
cd vulnrisk
./setup.sh

# Development commands
docker compose logs -f          # View logs
docker compose restart          # Restart services
docker compose down            # Stop services
docker compose down -v         # Reset everything
```

## 🤝 **Contributing**

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### **Quick Start for Contributors**
```bash
# Fork the repository
git clone https://github.com/GurkhaShieldForce/vulnrisk-public.git
cd vulnrisk

# Set up development environment
./setup.sh

# Make your changes
git checkout -b feature/amazing-feature
# ... make changes ...

# Submit a pull request
git push origin feature/amazing-feature
```

## 📚 **Documentation**

- **[Developer Setup](DEVELOPER_SETUP.md)** - Detailed setup guide
- **[API Documentation](http://localhost:8000/docs)** - Interactive API docs

## 🆘 **Support**

- **GitHub Issues**: [Report bugs and request features](https://github.com/GurkhaShieldForce/vulnrisk-public/issues)

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎉 **Getting Started**

**Ready to start?** Run `./setup.sh` and you'll have a fully functional VulnRisk environment in 5 minutes!

**Need help?** Check our [Developer Setup Guide](DEVELOPER_SETUP.md) for detailed instructions.