#!/bin/bash

# 🚀 VulnRisk Local Development Setup
# This script sets up your local development environment

set -e  # Exit on any error

echo "🚀 Setting up VulnRisk local development environment..."

# Check prerequisites
echo "📋 Checking prerequisites..."
command -v docker >/dev/null 2>&1 || { echo "❌ Docker is required but not installed. Please install Docker first."; exit 1; }
command -v docker compose >/dev/null 2>&1 || { echo "❌ Docker Compose is required but not installed. Please install Docker Compose first."; exit 1; }

# Make sure we're in the right directory
if [ ! -f "backend/pyproject.toml" ] || [ ! -f "backend/uv.lock" ]; then
    echo "❌ Please run this script from the VulnRisk root directory"
    exit 1
fi

# Create .env file for local development
echo "🔧 Creating local environment configuration..."
cat > .env << 'ENV_EOF'
# Local Development Configuration
ENVIRONMENT=development
DATABASE_URL=postgresql://vulnrisk:password@localhost:5432/vulnrisk
SECRET_KEY=your-secret-key-here
DEBUG=true
ENABLE_DEBUG_ENDPOINTS=true
ENABLE_AI_RISK_PREDICTION=true
ENABLE_FEDRAMP_COMPLIANCE=true
ENV_EOF

# Start the services
echo "🚀 Starting services..."
docker compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 15

# Test the setup
echo "🧪 Testing setup..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend is running!"
else
    echo "❌ Backend health check failed"
    echo "📋 Check logs with: docker compose logs backend"
    exit 1
fi

if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ Frontend is running!"
else
    echo "❌ Frontend health check failed"
    echo "📋 Check logs with: docker compose logs frontend"
    exit 1
fi

echo ""
echo "🎉 VulnRisk is ready for local development!"
echo ""
echo "📱 Access your application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo "   Database: localhost:5432"
echo ""
echo "🔧 Useful commands:"
echo "   View logs: docker compose logs -f"
echo "   Stop services: docker compose down"
echo "   Restart: docker compose restart"
echo "   Reset everything: docker compose down -v && ./setup.sh"
echo ""
echo "📚 Documentation:"
echo "   See DEVELOPER_SETUP.md for detailed instructions"
echo ""
echo "Happy coding! 🚀"